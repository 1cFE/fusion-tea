"""FastAPI server for the Fusion TEA Concept Explorer.

Start with:
    uv run python exploration/concept_explorer/server.py [--port PORT]

The server:
- Loads all data/*.json into memory on startup (fails loudly if data/ is absent).
- Renders Jinja2 page templates to dist/ on startup (skips templates not yet written).
- Serves static/ at /static and pre-rendered dist/ at page routes.
- Exposes typed data API endpoints backed by the in-memory loaded models.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import importlib.util
import inspect
import json
import sys
import threading
import types
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, redirect_stdout
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import Any

# Ensure project root is on sys.path so fully-qualified package imports work
# when the script is run directly (uv run python exploration/.../server.py)
_PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import uvicorn  # noqa: E402
from fastapi import Depends, FastAPI, HTTPException, Request  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from jinja2 import Environment, FileSystemLoader, TemplateNotFound  # noqa: E402

from exploration.concept_explorer.models import (  # noqa: E402
    FUEL_DISPLAY,
    ComputeRequest,
    ConceptData,
    ConceptManifest,
    CostLandscape,
    CostModelData,
    ExplorerState,
    FuelType,
    ParameterIndex,
    ParameterIndexEntry,
    build_cost_landscape,
    build_manifest,
    build_parameter_index,
    load_omit_list,
)
from exploration.concept_explorer.similarity import (  # noqa: E402
    ConceptSimilarityReport,
    ConstellationData,
    SimilarityResult,
    compare_pair,
    compute_constellation,
    compute_similarity_matrix,
    explain_difference,
    find_nearest,
)
from exploration.concept_explorer.taxonomy_models import (  # noqa: E402
    ConceptRegistry,
    ConceptTaxonomy,
    prune_decision_tree,
)

BASE_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Parameter sets for model.forward() re-invocation (compute endpoint)
# ---------------------------------------------------------------------------


def _derive_forward_named() -> frozenset[str]:
    """Extract named parameters from CostModel.forward() via introspection.

    Falls back to a hardcoded set if costingfe is not installed (e.g. in test
    environments that don't depend on it).
    """
    try:
        from costingfe.model import CostModel

        sig = inspect.signature(CostModel.forward)
        skip = {"self", "cost_overrides"}
        return frozenset(
            name
            for name, param in sig.parameters.items()
            if name not in skip
            and param.kind
            not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
        )
    except ImportError:
        return frozenset(
            {
                "net_electric_mw",
                "availability",
                "lifetime_yr",
                "n_mod",
                "construction_time_yr",
                "interest_rate",
                "inflation_rate",
                "noak",
            }
        )


# Named args that forward() takes explicitly (not via **overrides)
_FORWARD_NAMED = _derive_forward_named()
# Keys present in result.params that are model properties — never re-pass to forward()
_FORWARD_SKIP = frozenset({"fuel", "concept"})


def _derive_enabled_overrides() -> Any:
    """Return the canonical ``enabled_overrides`` projector.

    Prefer the shared three-forward helper (the source of truth for how the
    analyst override registry is projected to the ``cost_overrides`` dict
    ``forward()`` consumes).  Falls back to an inline projection when the helper
    module is unavailable — it imports ``costingfe.validation`` at module scope,
    so a costingfe-free environment (e.g. some test runs) cannot import it; the
    fallback keeps the same last-wins, enabled-only semantics.
    """
    try:
        helper_scripts = _PROJECT_ROOT / "exploration" / "concept_analysis" / "scripts"
        if str(helper_scripts) not in sys.path:
            sys.path.insert(0, str(helper_scripts))
        from lib.model_setup_helpers import enabled_overrides

        return enabled_overrides
    except Exception:

        def _inline_enabled_overrides(overrides: list[dict[str, Any]]) -> dict[str, float]:
            return {o["account"]: o["value"] for o in overrides if o["enabled"]}

        return _inline_enabled_overrides


# Projects the analyst override registry (module-level `overrides` list) to the
# {account: value} dict forward() takes; filters disabled entries.
_enabled_overrides = _derive_enabled_overrides()

# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

_MODULE_LOAD_LOCK = threading.Lock()


@lru_cache(maxsize=32)
def _load_model_module(path: Path, module_name: str = "_concept_module") -> types.ModuleType:
    """Import a model_setup.py file, suppressing stdout from module-level prints.

    Module-level print() calls in model_setup.py are suppressed so they don't
    pollute server logs during live recompute requests.  The lock ensures
    redirect_stdout (which modifies sys.stdout globally) is thread-safe.
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    with _MODULE_LOAD_LOCK:
        buf = StringIO()
        with redirect_stdout(buf):
            spec.loader.exec_module(module)
    return module


def _forward_with_overrides(
    model: Any,
    base_params: dict[str, Any],
    overrides: dict[str, Any],
    *,
    cost_overrides: dict[str, float] | None = None,
    override_reference_mw: float | None = None,
) -> Any:
    """Re-run model.forward() with base_params updated by overrides.

    Follows costingfe's _build_lcoe_fn param-extraction pattern: the named args
    required by forward() are extracted explicitly; remaining physics/plant params
    pass as **kwargs. `fuel` and `concept` are skipped — they are model instance
    properties inferred from self, not caller-supplied kwargs.

    Override semantics (explorer-slider-override-semantics, FR-SO1/FR-SO3): when
    ``cost_overrides`` is given, the analyst registry is re-applied exactly as
    ``run_native_and_1gw`` does (``cost_overrides=enabled``,
    ``override_reference_mw=P_native``), so a no-op recompute reproduces the
    stored ``result_1gw`` headline. When ``cost_overrides`` is None the recompute
    is the library-bare LCOE (registry dropped) — the same answer
    ``model.sensitivity()`` describes with ``cost_overrides=None``. The caller
    (the ``apply_analyst_overrides`` flag) selects which LCOE function is computed.

    ``cost_overrides`` and ``override_reference_mw`` are forward()'s own named
    args, so they are excluded from ``extra`` via ``_FORWARD_NAMED`` and never
    leak in twice; they are also absent from ``result_1gw.params``.
    """
    params = {**base_params, **overrides}
    extra = {k: v for k, v in params.items() if k not in _FORWARD_NAMED and k not in _FORWARD_SKIP}
    return model.forward(
        net_electric_mw=float(params["net_electric_mw"]),
        availability=float(params["availability"]),
        lifetime_yr=float(params["lifetime_yr"]),
        n_mod=float(params.get("n_mod", 1)),
        construction_time_yr=float(params.get("construction_time_yr", 6.0)),
        interest_rate=float(params.get("interest_rate", 0.07)),
        inflation_rate=float(params.get("inflation_rate", 0.02)),
        noak=bool(params.get("noak", True)),
        cost_overrides=cost_overrides,
        override_reference_mw=override_reference_mw,
        **extra,
    )


# ---------------------------------------------------------------------------
# Per-app state (populated by lifespan, held for the server's lifetime)
# ---------------------------------------------------------------------------


@dataclass
class _State:
    concepts: dict[str, ConceptData]
    manifest: ConceptManifest
    parameter_index: ParameterIndex
    cost_landscape: CostLandscape
    dist_dir: Path
    # Explorer base directory (concept_explorer/). Used to locate sibling
    # paths like concept_analysis/analyses/ for the findings endpoint.
    base_dir: Path = field(default_factory=Path)
    explorer_state: ExplorerState = field(default_factory=ExplorerState)
    registry: ConceptRegistry | None = None
    decision_tree: dict | None = None
    similarity_reports: dict[str, ConceptSimilarityReport] = field(default_factory=dict)
    constellation: ConstellationData | None = None
    _state_lock: threading.Lock = field(default_factory=threading.Lock)


def get_state(request: Request) -> _State:
    """FastAPI dependency: extract _State from app.state."""
    state: _State | None = getattr(request.app.state, "data", None)
    if state is None:
        raise RuntimeError("App state not initialised — lifespan must run first")
    return state


# ---------------------------------------------------------------------------
# Canonical identity resolution (A1) — the single identity authority
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Identity:
    """Resolved canonical identity for one concept: code + Name (Fuel) + fuel."""

    code: str
    name: str
    fuel: FuelType | None


def _compose_name(base_name: str, fuel: FuelType | None) -> str:
    """Return the canonical ``Name (Fuel)`` form.

    * If *base_name* already ends with the structured fuel's display suffix
      (the clean-CSV case for 35/36 served concepts), it is returned unchanged
      — so this is idempotent and never double-suffixes.
    * Otherwise, when *fuel* has a display form, the suffix is appended. This is
      the Option-1 decision (2026-06-06): the one CSV row whose authored name
      omits the suffix despite a *known* fuel (concept 35, "PoloMac Magnetic
      Confinement", fuel D-D) gets ``(D-D)`` composed from the structured field.
      The fuel is real registry data, so this composes — it never fabricates.
    * When *fuel* is None or has no display form (FuelType.OTHER → ""), the bare
      name is returned with no parenthetical — never ``(None)`` (FR-A1.5).

    Latent-data note: a name ending in a *different* fuel suffix than the
    structured fuel (e.g. authored ``"X (D-T)"`` but ``fuel=DD``) would get a
    second suffix appended (``"X (D-T) (D-D)"``). This is a registry/CSV data
    contradiction, not a display concern — stripping it here would silently mask
    the bad data and could also mangle legitimate non-fuel parentheticals
    (``"Reactor (Mk II)"`` *should* gain its fuel suffix). The Phase-1 audit
    (test_identity.py) is the guard: it asserts every served name resolves to its
    structured fuel's suffix, so such a contradiction fails the suite loudly.
    """
    if fuel is None:
        return base_name
    disp = FUEL_DISPLAY.get(fuel, "")
    if not disp:
        return base_name
    suffix = f"({disp})"
    if base_name.rstrip().endswith(suffix):
        return base_name
    return f"{base_name} {suffix}"


# ---------------------------------------------------------------------------
# Display-only generic names for the explorer (anonymized, agreed 2026-06-08).
#
# Replaces the canonical "Name (Fuel)" produced by resolve_identity + clears
# the Company field on every served surface (manifest, per-concept JSON,
# parameter index, cost landscape). Source CSV / frontmatter / model_setup.py
# are unchanged — the canonical taxonomy still has Commonwealth Fusion / TAE /
# Helion / etc., and resolve_identity is still the upstream source of the
# served name. The override is applied last, in _stamp_identity, so other
# explorer logic that depends on resolve_identity (test_identity.py audit,
# similarity reports, etc.) continues to see canonical names.
#
# Format convention: "<Technical descriptor> — <P_native rounded to 50 MWe> (<Fuel>)"
# Concepts with unspecified P_native or sub-MW pilot scale omit the size or
# use "sub-MW pilot". Company-coined technology names (Type One Energy,
# Renaissance Fusion, Deutelio PoloMac, NearStar MTIF, Neo Fusion BEST)
# generalized per analyst direction.
#
# To revert: delete the dict (or specific rows). To add a new concept: append
# a row; concepts absent from this dict fall through unchanged (and surface
# their analyst name + company).
# Per-concept company name + URL, rendered as the "Example: <Company>" disclaimer
# subheader on the entry surfaces (matrix / pipeline cards) ONLY. The full name
# may differ from what's in analysis.md frontmatter (some concepts have no
# analysis.md or no Company field — e.g. concept 12 OpenStar Technologies is
# only mentioned in its model_setup.py docstring). The disclaimer framing
# emphasizes that the rendered concept is one representative example, not the
# company's definitive published design.
#
# Each value is (display_name, url). URL may be None when not registered;
# in that case the company renders as plain italic text (no link).
#
# ⚠ URLs marked TODO need verification — included as best-effort placeholders
# from public knowledge but not authoritatively confirmed at this commit.
_COMPANIES: dict[str, tuple[str, str | None]] = {
    "01": ("Commonwealth Fusion Systems", "https://cfs.energy"),
    "02": ("Sonofusion Energy", None),  # No public website found (UCLA spinoff)
    "03": ("Cortex Fusion Systems", "https://cortexfusion.systems"),
    "04": ("HB11 Energy", "https://hb11.energy"),
    "05": ("Thea Energy", "https://theaenergy.com"),
    "06": ("Pale Blue Fusion", None),  # No public website found (Princeton early-stage)
    "07": ("Pacific Fusion", "https://www.pacificfusion.com"),
    "08": ("Helion Energy", "https://helionenergy.com"),
    "09": ("Type One Energy", "https://typeoneenergy.com"),
    "10": ("Gauss Fusion", "https://gauss-fusion.com"),
    "11": ("Realta Fusion", "https://realtafusion.com"),
    "12": ("OpenStar Technologies", "https://openstartech.com"),
    "13": ("Avalanche Energy", "https://www.avalanchefusion.com"),
    "14": ("General Fusion", "https://generalfusion.com"),
    "15": ("Zap Energy", "https://zapenergy.com"),
    "16": ("Acceleron Fusion", "https://www.acceleron.energy"),
    "17a": ("Xcimer Energy", "https://xcimer.energy"),
    "17b": ("Focused Energy", "https://www.focused-energy.co"),
    "18": ("TAE Technologies", "https://tae.com"),
    "19": ("Zephyr Fusion", "https://zephyrfusion.com"),
    "20a": ("Type One Energy", "https://typeoneenergy.com"),
    "20b": ("Renaissance Fusion", "https://stellarators.com"),
    "21": ("Tokamak Energy", "https://www.tokamakenergy.com"),
    "22": ("First Light Fusion", "https://firstlightfusion.com"),
    "23": ("Marvel Fusion", "https://marvelfusion.com"),
    "24": ("LPP Fusion", "https://lppfusion.com"),
    "25": ("Intensity Energy", None),  # No public website found
    "26": ("Inertia Enterprises", "https://inertia.com"),
    "28": ("Energy Singularity", "https://energysingularity.cn"),
    "29": ("Firefly Fusion", "https://fireflyfusion.energy"),
    "30": ("Inertia Enterprises", "https://inertia.com"),
    "31": ("Blue Laser Fusion", "https://bluelaserfusion.com"),
    "32": ("GenF (Thales spin-off / Taranis project)", None),  # No public website found
    "33": ("Neo Fusion (BEST program)", None),  # State-backed CN, no public corporate site
    "35": ("Deutelio", None),  # No public website found (Italian-Swiss early-stage)
    "36": ("Helical Fusion", "https://www.helicalfusion.com"),
    "37": ("NearStar Fusion", "https://www.nearstarfusion.com"),
    "39": ("ENN Energy", "https://enn.cn"),
}


_GENERIC_NAMES: dict[str, str] = {
    "01": "HTS Compact Tokamak — 250 MWe (D-T)",
    "02": "Acoustic ICF / Sonofusion (D-D)",
    "03": "Laser ICF - Liquid Jet Target — sub-MW pilot (D-D)",
    "04": "Laser ICF — 500 MWe (p-B11)",
    "05": "Planar Coil Stellarator — 400 MWe (D-T)",
    "06": "Magnetic Mirror — 150 MWe (p-B11)",
    "07": "MagLIF — 200 MWe (D-T)",
    "08": "FRC w/ Direct Conversion — 50 MWe (D-He3)",
    "09": "QI Stellarator - HTS — 1000 MWe (D-T)",
    "10": "Large-Scale Stellarator — 1000 MWe (D-T)",
    "11": "Magnetic Mirror — 50 MWe (D-T)",
    "12": "Levitated Dipole — 200 MWe (D-T)",
    "13": "Electrostatic Hybrid — sub-MW pilot (D-T)",
    "14": "Magnetized Target Fusion - Pneumatic Compression — 150 MWe (D-T)",
    "15": "Sheared-Flow Stabilized Z-Pinch — 50 MWe (D-T)",
    "16": "Muon-Catalyzed Fusion (D-T)",
    "17a": "Laser ICF - Hybrid Direct Drive — 400 MWe (D-T)",
    "17b": "Laser ICF - Direct Drive Fast Ignition — 1000 MWe (D-T)",
    "18": "p-B11 FRC — 50 MWe (p-B11)",
    "19": "Orbital Levitated Dipole — 100 MWe (D-He3)",
    "20a": "Modular HTS Stellarator — 350 MWe (D-T)",
    "20b": "3D-Coil HTS Stellarator — 1000 MWe (D-T)",
    "21": "Spherical Tokamak - HTS — 450 MWe (D-T)",
    "22": "Projectile ICF — 150 MWe (D-T)",
    "23": "Laser ICF - Nanostructured Target — 100 MWe (p-B11)",
    "24": "Dense Plasma Focus — sub-MW pilot (p-B11)",
    "25": "Heavy Ion Beam ICF — 950 MWe (D-T)",
    "26": "Laser ICF - Indirect Drive — 1500 MWe (D-T)",
    "28": "HTS Tokamak - Full HTS — 500 MWe (D-T)",
    "29": "Negative Triangularity Tokamak — 100 MWe (D-T)",
    "30": "Laser ICF - NIF Commercialization — 1500 MWe (D-T)",
    "31": "Laser ICF - OEC Architecture — 1000 MWe (D-T)",
    "32": "Laser ICF - French National — 1000 MWe (D-T)",
    "33": "State-Backed Tokamak — 400 MWe (D-T)",
    "35": "Poloidal-Tunnel Magnetic Confinement (D-D)",
    "36": "Helical Coil Stellarator — 50 MWe (D-T)",
    "37": "Magnetized Target Inertial Fusion — 200 MWe (D-D)",
    "39": "Spherical Tokamak - CS-free — 500 MWe (p-B11)",
}


def resolve_identity(
    concept_id: str,
    registry: ConceptRegistry | None,
    *,
    served_name: str | None = None,
) -> Identity:
    """Resolve one concept's canonical identity — the single identity authority (A1).

    Identity is sourced from the CSV-backed registry (``concept_registry.json``,
    built by ``seed_registry`` from ``table.csv``). The canonical ``name`` is the
    registry's ``Name (Fuel)``, composed from the structured fuel when the
    authored name omits the suffix (see ``_compose_name``). ``code`` is the
    ``concept_id`` verbatim, so letter-suffix variants (``17a``, ``20b``) carry
    through unchanged.

    A served concept absent from the registry degrades honestly: it returns its
    stored *served_name* (or, lacking that, the bare code) with ``fuel=None``.
    This function never raises and never returns a blank name (invariant).
    """
    tax = registry.by_id(concept_id) if registry is not None else None
    if tax is not None:
        return Identity(code=concept_id, name=_compose_name(tax.name, tax.fuel), fuel=tax.fuel)
    return Identity(code=concept_id, name=served_name or concept_id, fuel=None)


def _load_fit_grades(csv_path: Path) -> dict[str, str]:
    """Read archetype-fit grades from ``tables/archetype_fit.csv`` (A3).

    Returns ``{code: fit_grade}`` keyed by the short concept code (the CSV's
    ``concept_id`` is the full slug ``01-hts-compact-tokamak``; the code is the
    token before the first hyphen, matching ``seed_registry``'s ID parse and the
    ``data/{code}.json`` convention, so suffix variants like ``17a`` carry
    through). Non-fatal: a missing file yields ``{}`` (every concept then stamps
    ``fit_grade=None`` — honest "not recorded", never a fabricated grade).
    """
    if not csv_path.exists():
        return {}
    grades: dict[str, str] = {}
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            raw_id = (row.get("concept_id") or "").strip()
            grade = (row.get("fit_grade") or "").strip()
            if not raw_id or not grade:
                continue
            grades[raw_id.split("-", 1)[0]] = grade
    return grades


def _stamp_identity(
    concepts: dict[str, ConceptData],
    registry: ConceptRegistry | None,
    fit_grades: dict[str, str] | None = None,
) -> tuple[dict[str, ConceptData], ConceptManifest, ParameterIndex]:
    """Overlay canonical identity + archetype-fit onto each served ConceptData
    and rebuild the manifest + parameter index from the stamped concepts.

    The display ``name`` becomes the CSV-backed canonical ``Name (Fuel)``; the
    raw frontmatter phrasing is preserved on ``analyst_name``; the structured
    ``fuel`` is stamped from the registry; ``fit_grade`` (A3) is stamped from
    ``archetype_fit.csv``. Rebuilding the manifest and parameter index from the
    *stamped* concepts means every derived surface (landing cards, compare
    picker, cross-concept parameter index) carries the canonical name + fit
    grade too — one resolution, everywhere. A concept absent from the fit table
    gets ``fit_grade=None`` (honest "not recorded", never fabricated).
    """
    fit_grades = fit_grades or {}
    stamped: dict[str, ConceptData] = {}
    for cid, concept in concepts.items():
        ident = resolve_identity(cid, registry, served_name=concept.name)
        # Display-only generic-name override (see _GENERIC_NAMES). Concepts
        # absent from the dict pass through with the canonical resolve_identity
        # name. Company is preserved on the data model — the entry surfaces
        # (matrix + pipeline) render it as "Example: <Company>" to disclaim
        # that the concept is one possible instantiation, not THE company's
        # definitive LCOE. Profile / compare / cost-landscape surfaces hide
        # the company in their own JS.
        display_name = _GENERIC_NAMES.get(cid, ident.name)
        company_entry = _COMPANIES.get(cid)
        if company_entry is not None:
            display_company, display_company_url = company_entry
        else:
            # Concept absent from _COMPANIES — fall back to whatever the
            # extraction stamped from frontmatter, with no URL.
            display_company, display_company_url = concept.company, None
        stamped[cid] = concept.model_copy(
            update={
                "analyst_name": concept.name,
                "name": display_name,
                "company": display_company,
                "company_url": display_company_url,
                "fuel": ident.fuel,
                "fit_grade": fit_grades.get(cid),
            }
        )
    concept_list = list(stamped.values())
    manifest = build_manifest(concept_list)
    parameter_index = build_parameter_index(concept_list)
    return stamped, manifest, parameter_index


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def _load_data(
    data_dir: Path,
    omitted: set[str] | None = None,
) -> tuple[dict[str, ConceptData], ConceptManifest, ParameterIndex]:
    """Load all data files from *data_dir*.

    Raises RuntimeError with a clear message when data/ is absent or empty.
    Called once during server startup — errors here abort the process.

    The manifest and parameter index are computed in-memory from the loaded
    per-concept JSONs. The names ``manifest.json`` / ``parameter_index.json``
    remain in ``_NON_CONCEPT_FILES`` so any stale files left on disk from
    earlier extractions don't get globbed as concept data.

    *omitted* is the omit-list set (FR-4); concept files whose stem (the concept
    ID, by the ``data/{id}.json`` convention) is in it are dropped before
    validation, so omitted concepts never enter the loaded set — and therefore
    never reach the manifest or parameter index, which are derived from it (I-4).
    The on-disk files are read-filtered only, never modified (I-6). ``None``
    defaults to the shipped omit list so the server enforces it independently of
    the extractor (FR-6); tests pass an explicit set for isolation.
    """
    if not data_dir.is_dir():
        raise RuntimeError(
            f"data/ directory not found at {data_dir}. "
            "Run extract_explorer_data.py to populate it before starting the server."
        )

    omit_set = load_omit_list() if omitted is None else omitted

    _NON_CONCEPT_FILES = {
        "manifest.json", "parameter_index.json",
        "concept_registry.json", "decision_tree.json",
    }
    concept_files = [
        f
        for f in data_dir.glob("*.json")
        if f.name not in _NON_CONCEPT_FILES and f.stem not in omit_set
    ]
    if not concept_files:
        raise RuntimeError(
            f"No concept data files found in {data_dir}. "
            "Re-run extract_explorer_data.py to populate it."
        )

    concepts: dict[str, ConceptData] = {}
    for path in concept_files:
        concept = ConceptData.model_validate_json(path.read_text())
        concepts[concept.concept_id] = concept

    # generated_at on the returned manifest now records server start time,
    # not extraction time. Functionally equivalent (used as a frontend cache key).
    concept_list = list(concepts.values())
    manifest = build_manifest(concept_list)
    parameter_index = build_parameter_index(concept_list)

    return concepts, manifest, parameter_index


def _load_taxonomy(
    data_dir: Path,
    omitted: set[str] | None = None,
) -> tuple[
    ConceptRegistry | None,
    dict | None,
    dict[str, ConceptSimilarityReport],
    ConstellationData | None,
]:
    """Load taxonomy data if available. Returns (registry, tree, reports, constellation).

    Non-fatal: if taxonomy files don't exist, returns all None/empty.
    Taxonomy is an additive feature — the server works without it.

    *omitted* is the omit-list set (FR-5). Filtering ``registry.concepts`` once,
    before similarity/constellation are computed from it, removes omitted concepts
    from the registry, similarity reports, and constellation in a single place
    (I-5); the decision tree is a separate dict, pruned independently. ``None``
    defaults to the shipped omit list so the server enforces it independently of
    the extractor (FR-6); tests pass an explicit set for isolation. The on-disk
    taxonomy JSON is read-filtered only, never modified (I-6).
    """
    registry_path = data_dir / "concept_registry.json"
    tree_path = data_dir / "decision_tree.json"

    if not registry_path.exists() or not tree_path.exists():
        return None, None, {}, None

    omit_set = load_omit_list() if omitted is None else omitted

    registry = ConceptRegistry.model_validate_json(registry_path.read_text())
    if omit_set:
        kept = [c for c in registry.concepts if c.concept_id not in omit_set]
        registry = registry.model_copy(update={"concepts": kept})

    # Canonical-name overlay (A1): compose Name (Fuel) onto each registry concept
    # *before* similarity reports and the constellation are derived from it, so
    # every taxonomy-layer surface (taxonomy endpoint, similarity hover,
    # constellation nodes) carries the same canonical name the explorer layer
    # gets via `resolve_identity`. `_compose_name` is idempotent — concepts whose
    # authored name already ends in the fuel suffix pass through unchanged.
    registry = registry.model_copy(
        update={
            "concepts": [
                c.model_copy(update={"name": _compose_name(c.name, c.fuel)})
                for c in registry.concepts
            ]
        }
    )

    decision_tree = json.loads(tree_path.read_text())
    if omit_set and "root" in decision_tree:
        pruned_root = prune_decision_tree(decision_tree["root"], omit_set)
        decision_tree = {**decision_tree, "root": pruned_root}

    # Precompute similarity reports for all concepts
    similarity_reports: dict[str, ConceptSimilarityReport] = {}
    for concept in registry.concepts:
        nearest = find_nearest(concept, registry, top_n=15)
        similarity_reports[concept.concept_id] = ConceptSimilarityReport(
            query_concept_id=concept.concept_id,
            query_concept_name=concept.name,
            nearest=nearest,
        )

    # Compute constellation
    matrix = compute_similarity_matrix(registry)
    constellation = compute_constellation(matrix, registry)

    return registry, decision_tree, similarity_reports, constellation


# ---------------------------------------------------------------------------
# Template rendering
# ---------------------------------------------------------------------------


def _render_templates(
    templates_dir: Path,
    dist_dir: Path,
    concepts: dict[str, ConceptData],
) -> None:
    """Render Jinja2 page templates to *dist_dir*.

    Silently skips templates that do not yet exist — page templates are
    written in Tasks 10-12 and server startup must not fail before them.
    The corresponding page routes return 404 until those tasks complete.
    """
    if not templates_dir.is_dir():
        return

    dist_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(templates_dir)), autoescape=True)

    def _try_render(template_name: str, dest: Path, **ctx: object) -> None:
        try:
            tmpl = env.get_template(template_name)
        except TemplateNotFound:
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(tmpl.render(**ctx), encoding="utf-8")

    # B1: the ontology matrix is the home page (/); the Approved/In-Progress
    # card grid (index.html) relocates to /pipeline. Both render here.
    _try_render("matrix.html.j2", dist_dir / "matrix.html", active_nav="matrix")
    _try_render("index.html.j2", dist_dir / "index.html", active_nav="pipeline")
    _try_render("compare.html.j2", dist_dir / "compare.html", active_nav="compare")
    _try_render(
        "cost_landscape.html.j2", dist_dir / "cost_landscape.html", active_nav="cost_landscape"
    )

    for concept_id in concepts:
        _try_render(
            "concept.html.j2",
            dist_dir / "concept" / f"{concept_id}.html",
            concept_id=concept_id,
            active_nav="matrix",
        )


# ---------------------------------------------------------------------------
# Route handlers — module-level functions, state injected via Depends()
# ---------------------------------------------------------------------------


def _serve(path: Path) -> FileResponse:
    """Return FileResponse if *path* exists; 404 otherwise."""
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"{path.name} not found")
    return FileResponse(
        str(path),
        headers={"Cache-Control": "no-cache"},
    )


# -- Data API --

def health() -> dict[str, str]:
    return {"status": "ok"}


def api_get_manifest(state: _State = Depends(get_state)) -> ConceptManifest:
    return state.manifest


def api_cost_landscape(state: _State = Depends(get_state)) -> CostLandscape:
    """The cross-concept LCOE-decomposition aggregate (Theme F).

    Precomputed at load (like the manifest); the page fetches it once and never
    refetches on re-group (NFR-1).
    """
    return state.cost_landscape


def api_get_concept(concept_id: str, state: _State = Depends(get_state)) -> ConceptData:
    concept = state.concepts.get(concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
    return concept


def api_get_findings(concept_id: str, state: _State = Depends(get_state)) -> dict:
    """Agentic research findings: synthesis exec summary + full analysis.md HTML.

    Returns a dict with ``exec_summary_html`` and ``analysis_html`` keys —
    either may be None when the corresponding markdown file is absent. The
    concept must be served (404 otherwise) to keep the route surface aligned
    with /api/concepts/{id}.
    """
    if state.concepts.get(concept_id) is None:
        raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
    from exploration.concept_explorer.findings import build_findings
    analyses_root = state.base_dir.parent / "concept_analysis" / "analyses"
    # Fallback for analyses that haven't been regenerated under the new
    # three-forward pipeline since Reid's 2026-05-31 bulk archive (commit
    # 3f28671). Surfaces the legacy analysis with a disclaimer.
    archive_root = state.base_dir.parent.parent / "archive" / "concept_analysis_pre_rework"
    payload = build_findings(
        concept_id,
        analyses_root,
        archive_root=archive_root if archive_root.is_dir() else None,
    )
    return {
        "exec_summary_html": payload.exec_summary_html,
        "analysis_html": payload.analysis_html,
        "analysis_from_archive": payload.analysis_from_archive,
    }


def api_get_parameter_index(state: _State = Depends(get_state)) -> ParameterIndex:
    return state.parameter_index


def api_get_parameter(param_name: str, state: _State = Depends(get_state)) -> ParameterIndexEntry:
    entry = state.parameter_index.parameters.get(param_name)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Parameter {param_name} not found")
    return entry


# -- Explorer state API --

def api_get_state(state: _State = Depends(get_state)) -> ExplorerState:
    return state.explorer_state


def api_post_state(body: ExplorerState, state: _State = Depends(get_state)) -> dict[str, str]:
    """Store explorer state; timestamp is set server-side (client value ignored)."""
    ts = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    with state._state_lock:
        state.explorer_state = body.model_copy(update={"timestamp": ts})
    return {"status": "ok"}


# -- Taxonomy API --

def api_taxonomy_tree(state: _State = Depends(get_state)) -> dict:
    """Return the full decision tree structure."""
    tree = state.decision_tree
    if tree is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    return tree


def api_taxonomy_registry(state: _State = Depends(get_state)) -> ConceptRegistry:
    """Return the full concept registry."""
    reg = state.registry
    if reg is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    return reg


def api_taxonomy_concept(concept_id: str, state: _State = Depends(get_state)) -> ConceptTaxonomy:
    """Return a single concept's taxonomy record."""
    reg = state.registry
    if reg is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    concept = reg.by_id(concept_id)
    if concept is None:
        raise HTTPException(
            status_code=404, detail=f"Concept '{concept_id}' not found in registry"
        )
    return concept


def api_taxonomy_similarity(
    concept_id: str, top_n: int = 5, state: _State = Depends(get_state)
) -> ConceptSimilarityReport:
    """Return precomputed similarity report (nearest neighbors + bridges).

    The ``top_n`` query parameter controls how many neighbors are returned
    (default 5, clamped to 1–15).
    """
    report = state.similarity_reports.get(concept_id)
    if report is None:
        raise HTTPException(
            status_code=404, detail=f"No similarity report for '{concept_id}'"
        )
    top_n = max(1, min(top_n, 15))
    return ConceptSimilarityReport(
        query_concept_id=report.query_concept_id,
        query_concept_name=report.query_concept_name,
        nearest=report.nearest[:top_n],
    )


def api_taxonomy_compare(
    concept_a: str, concept_b: str, state: _State = Depends(get_state)
) -> SimilarityResult:
    """Compare any two concepts on demand."""
    reg = state.registry
    if reg is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    a = reg.by_id(concept_a)
    b = reg.by_id(concept_b)
    if a is None or b is None:
        raise HTTPException(
            status_code=404, detail="One or both concept IDs not found"
        )
    comparison = compare_pair(a, b)
    bridges = explain_difference(a, b, reg)
    return SimilarityResult(
        concept_id=b.concept_id,
        concept_name=b.name,
        confinement_family=b.confinement_family,
        comparison=comparison,
        bridges=bridges,
    )


def api_taxonomy_constellation(state: _State = Depends(get_state)) -> ConstellationData:
    """Return 2D constellation coordinates for all concepts."""
    const = state.constellation
    if const is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    return const


# -- Page routes --

def matrix_page(state: _State = Depends(get_state)) -> FileResponse:
    """Home page (B1): the ontology matrix."""
    return _serve(state.dist_dir / "matrix.html")


def pipeline_page(state: _State = Depends(get_state)) -> FileResponse:
    """Relocated Approved/In-Progress card grid (B1, FR-B1.10)."""
    return _serve(state.dist_dir / "index.html")


def compare_page(state: _State = Depends(get_state)) -> FileResponse:
    return _serve(state.dist_dir / "compare.html")


def cost_landscape_page(state: _State = Depends(get_state)) -> FileResponse:
    """Cross-concept LCOE-decomposition page (Theme F)."""
    return _serve(state.dist_dir / "cost_landscape.html")


def concept_page(concept_id: str, state: _State = Depends(get_state)) -> FileResponse:
    return _serve(state.dist_dir / "concept" / f"{concept_id}.html")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app(base_dir: Path = BASE_DIR) -> FastAPI:
    """Return a configured FastAPI application rooted at *base_dir*.

    Using a factory (rather than a module-level singleton) lets tests inject
    a temporary directory without touching the real data/ tree.
    """
    data_dir = base_dir / "data"
    dist_dir = base_dir / "dist"
    templates_dir = base_dir / "templates"
    static_dir = base_dir / "static"
    # Archetype-fit table lives in the sibling concept_analysis tree (A3).
    fit_csv_path = base_dir.parent / "concept_analysis" / "tables" / "archetype_fit.csv"

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        concepts, manifest, parameter_index = _load_data(data_dir)
        registry, decision_tree, similarity_reports, constellation = _load_taxonomy(
            data_dir
        )
        # Stamp canonical identity + archetype-fit onto the explorer-layer
        # payloads and rebuild the manifest/parameter index from the stamped
        # concepts (A1/A3). Runs after both loaders so the registry (identity
        # source of truth) is available.
        fit_grades = _load_fit_grades(fit_csv_path)
        concepts, manifest, parameter_index = _stamp_identity(
            concepts, registry, fit_grades
        )
        _render_templates(templates_dir, dist_dir, concepts)

        app.state.data = _State(
            concepts=concepts,
            manifest=manifest,
            parameter_index=parameter_index,
            cost_landscape=build_cost_landscape(list(concepts.values())),
            dist_dir=dist_dir,
            base_dir=base_dir,
            registry=registry,
            decision_tree=decision_tree,
            similarity_reports=similarity_reports,
            constellation=constellation,
        )
        yield
        _compute_cached.cache_clear()
        _load_model_module.cache_clear()
        app.state.data = None

    # -- Computation closure (per-app-instance cache for test isolation) --

    @lru_cache(maxsize=128)
    def _compute_cached(
        concept_id: str,
        overrides_frozen: frozenset[tuple[str, float]],
        apply_analyst_overrides: bool,
    ) -> CostModelData:
        """Compute CostModelData with overridden params; result is LRU-cached.

        Cache key is (concept_id, frozenset(overrides.items()),
        apply_analyst_overrides) (INV-4 / FR-SO5).  Identical triples return the
        cached result without reloading the module.  Baseline sensitivities come
        from the stored concept data — they are never recomputed on slider change
        (per spec 12).

        ``apply_analyst_overrides`` selects which LCOE function the recompute
        describes (explorer-slider-override-semantics):

        * ``True`` (default UI state) — re-apply the analyst override registry
          read from the live concept module (``module.overrides`` projected by
          ``enabled_overrides``, ``override_reference_mw=module.P_native``),
          mirroring ``run_native_and_1gw`` so a no-op recompute reproduces the
          stored ``result_1gw`` headline (FR-SO1 / INV-1).
        * ``False`` — drop the registry; recompute the library-bare LCOE.

        An empty / absent registry makes the two branches identical (INV-6).
        """
        state: _State = app.state.data
        concept = state.concepts.get(concept_id)
        if concept is None:
            raise ValueError(f"Concept {concept_id!r} not found in loaded data")
        model_setup = concept.sources.model_setup
        if model_setup is None:
            raise ValueError("compute called for a concept with no model_setup")

        module = _load_model_module(Path(model_setup))
        model = getattr(module, "model", None)
        if model is None:
            raise ImportError(f"Module {model_setup} does not define 'model'")
        result_1gw = getattr(module, "result_1gw", None)
        if result_1gw is None:
            raise ImportError(
                f"Module {model_setup} does not define 'result_1gw' at module level. "
                "See rework epic Items 10/11."
            )

        if apply_analyst_overrides:
            # Read the registry from the live module (already loaded, always in
            # sync with the source of truth — Bet 1). Empty/absent registry →
            # cost_overrides={}, which reproduces the bare forward (INV-6).
            registry = getattr(module, "overrides", []) or []
            cost_overrides: dict[str, float] | None = _enabled_overrides(registry)
            override_reference_mw = getattr(module, "P_native", None)
        else:
            cost_overrides = None
            override_reference_mw = None

        new_result = _forward_with_overrides(
            model,
            result_1gw.params,
            dict(overrides_frozen),
            cost_overrides=cost_overrides,
            override_reference_mw=override_reference_mw,
        )

        raw: dict[str, Any] = dataclasses.asdict(new_result)
        params_dict: dict[str, Any] = raw.get("params", {})
        # Inject availability into power_table for capacity_factor fallback (same
        # fix as extract_explorer_data.py — availability lives in params, not power_table)
        if "availability" in params_dict:
            raw.setdefault("power_table", {})["availability"] = params_dict["availability"]

        baseline_sensitivities = concept.cost_model.sensitivities if concept.cost_model else None
        return CostModelData.from_forward_result(raw, baseline_sensitivities)

    def compute(body: ComputeRequest, state: _State = Depends(get_state)) -> CostModelData:
        concept = state.concepts.get(body.concept_id)
        if concept is None:
            raise HTTPException(status_code=404, detail=f"Concept {body.concept_id} not found")
        if concept.sources.model_setup is None:
            raise HTTPException(
                status_code=422,
                detail="Slider computation only available for costingfe-backed concepts",
            )
        return _compute_cached(
            body.concept_id,
            frozenset(body.overrides.items()),
            body.apply_analyst_overrides,
        )

    app = FastAPI(title="Fusion TEA Concept Explorer", lifespan=lifespan)

    # Static assets (CSS, JS, vendor libs, images)
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # -- Register routes --
    app.get("/api/health")(health)
    app.get("/api/manifest", response_model=ConceptManifest)(api_get_manifest)
    app.get("/api/cost-landscape", response_model=CostLandscape)(api_cost_landscape)
    app.get("/api/concepts/{concept_id}", response_model=ConceptData)(api_get_concept)
    app.get("/api/concepts/{concept_id}/findings")(api_get_findings)
    app.get("/api/parameter_index", response_model=ParameterIndex)(api_get_parameter_index)
    app.get("/api/parameters/{param_name}", response_model=ParameterIndexEntry)(api_get_parameter)
    app.get("/api/state", response_model=ExplorerState)(api_get_state)
    app.post("/api/state")(api_post_state)
    app.post("/api/compute", response_model=CostModelData)(compute)
    app.get("/api/taxonomy/tree")(api_taxonomy_tree)
    app.get("/api/taxonomy/registry", response_model=ConceptRegistry)(api_taxonomy_registry)
    app.get("/api/taxonomy/concepts/{concept_id}", response_model=ConceptTaxonomy)(api_taxonomy_concept)
    app.get("/api/taxonomy/similarity/{concept_id}", response_model=ConceptSimilarityReport)(api_taxonomy_similarity)
    app.get("/api/taxonomy/compare/{concept_a}/{concept_b}", response_model=SimilarityResult)(api_taxonomy_compare)
    app.get("/api/taxonomy/constellation", response_model=ConstellationData)(api_taxonomy_constellation)
    app.get("/")(matrix_page)
    app.get("/pipeline")(pipeline_page)
    app.get("/compare")(compare_page)
    app.get("/cost-landscape")(cost_landscape_page)
    app.get("/concept/{concept_id}")(concept_page)

    return app


# ---------------------------------------------------------------------------
# Module-level app instance (used when running directly or via uvicorn string ref)
# ---------------------------------------------------------------------------

# The lifespan runs only when uvicorn starts — not at import time.
app = create_app()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Fusion TEA Concept Explorer server")
    parser.add_argument(
        "--port",
        type=int,
        default=8421,
        help="TCP port to listen on (default: 8421)",
    )
    args = parser.parse_args()
    uvicorn.run(app, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
