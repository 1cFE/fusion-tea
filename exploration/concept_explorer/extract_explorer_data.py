"""extract_explorer_data.py — Convert concept analysis artifacts to validated JSON.

Reads exploration/concept_analysis/analyses/ and writes to data/.

Usage:
    uv run python exploration/concept_explorer/extract_explorer_data.py
    uv run python exploration/concept_explorer/extract_explorer_data.py --concept 01 04
    uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import re
import subprocess
import sys
import types
import warnings
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

_HERE = Path(__file__).parent
_PROJECT_ROOT = _HERE.parent.parent  # .../exploration/concept_explorer/ → project root
_ANALYSES_DIR = _HERE.parent / "concept_analysis" / "analyses"
_DATA_DIR = _HERE / "data"
_DISPLAY_REGISTRY_PATH = _DATA_DIR / "parameter_display_registry.yaml"

# Fields the shared display registry is allowed to patch on a ParameterMetadata.
# Other fields (baseline, range, category, confidence, etc.) come from
# generation or per-concept yaml.
_REGISTRY_PATCH_FIELDS = frozenset({"display_name", "display_unit", "display_multiplier"})

# Sensitivity keys we deliberately drop from the tornado / slider UI.
#
# Two reasons a key lands here:
#
# 1. Fixed-geometry-fixed-target-net sensitivity is misleading. For plasma-
#    physics knobs (B, q95, f_GW, plasma_t internals like T_e/n_e/etc.), the
#    library back-solves T_e to maintain the target net, so the marginal cost
#    response at fixed geometry doesn't match the engineering question an
#    analyst is asking ("would the LCOE shift if this design choice changed"
#    — which would require re-sizing the machine). Until the projection
#    pipeline supports proper design-point re-solving per-slider (the
#    R0-bisection follow-up), these knobs read as ~0 elasticity or worse,
#    and we'd rather hide them than show misleading bars.
#
# 2. Library-side broken (pre-fix). The p_nbi/p_ecrh/p_icrf/p_lhcd heating-
#    mix breakdown was the original 1costingfe#35 bug: the renormalization
#    branch is guarded by ``isinstance(v, numbers.Real)`` which is False
#    under JAX tracing, so jax.grad reports ~0.44 elasticities that
#    production never produces. Reid removed these from the sensitivity
#    dict library-side in efcf5cc; post-regen they're naturally gone. We
#    exclude them defensively so the stale pre-efcf5cc JSONs also drop
#    them without waiting for the regen.
#
# Kept (engineering choices where fixed-geometry sensitivity IS meaningful):
# R0, plasma_t, elon — cost cards scale with machine size; all eta_* —
# plant conversion efficiencies; parasitic loads (p_coils, p_cool, etc.);
# financial knobs; engineering thicknesses (blanket_t, vessel_t, etc.).
_SENSITIVITY_EXCLUDE_KEYS: frozenset[str] = frozenset({
    # Field strength — library cost cards don't scale with B; FD ≈ 0
    "B", "b_center",
    # Plasma operating point (back-solved or no cost path)
    "q95", "f_GW",
    "T_e", "T_min", "T_max", "n_e",
    "Z_eff", "lambda_q", "M_ion", "T_i_over_T_e", "tau_ratio",
    # Fuel mix (set by fuel choice, not analyst slider)
    "dhe3_dd_frac", "dhe3_fuel_ratio", "pb11_fuel_ratio",
    "dhe3_dd_frac_pin",
    "dd_f_T", "dd_f_He3", "dhe3_f_T", "dhe3_f_He3",
    "pb11_f_alpha_n", "pb11_f_p_n",
    # Radiation / boundary
    "f_rad_fus", "T_edge",
    # Heating power (total + mix). p_input would re-design heating;
    # p_nbi/p_ecrh/p_icrf/p_lhcd were the 1costingfe#35 broken sliders.
    "p_input", "p_nbi", "p_ecrh", "p_icrf", "p_lhcd",
    # Derived / deprecated
    "eta_pin", "r_bore", "fw_area",
    # Derived outputs masquerading as inputs. q_eng (engineering Q,
    # p_net_electric / p_input_electric) and q_sci (scientific Q,
    # p_fus / p_input) are computed by the forward and reported on the
    # power_table, but the library schema also exposes them as keys in
    # `result.params` with non-zero gradients. Overriding either via a
    # slider has no effect on LCOE (the forward ignores the override
    # because q_eng/q_sci aren't forward kwargs), so the elasticity is
    # misleading.
    "q_eng", "q_sci",
    # Modeling factor — neutron energy multiplication is a blanket-physics
    # constant tied to fuel choice, not an analyst-tunable input.
    "mn",
    # Behavior flag
    "enforce_plasma_limits",
})

# Additional exclusions applied only to non-tokamak concepts. R0, plasma_t,
# and elon are meaningful tokamak design knobs whose cost cards scale with
# machine size (the user-accepted reasoning: "coil/blanket/vessel cost
# scales with R0"). But they appear in every concept's params dict because
# the library uses one schema across all families — for laser IFE, mirror,
# FRC, etc., these keys carry library defaults (e.g. plasma_t=4.0 for
# laser ICF concepts) with no physical correspondence to the concept's
# geometry, and the tornado renders nonsensical "Minor Radius" sliders.
# Drop them for everyone except tokamak.
_NON_TOKAMAK_EXCLUDE_KEYS: frozenset[str] = frozenset({"R0", "plasma_t", "elon"})

# Ensure project root is on sys.path so fully-qualified package imports work
# when the script is run directly (uv run python exploration/.../extract_explorer_data.py)
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from exploration.concept_explorer.models import (  # noqa: E402, I001
    Confidence,
    CostModelData,
    ConceptData,
    ConceptStatus,
    ConfinementFamily,
    ModelType,
    NarrativeData,
    OverrideRecord,
    ParameterCategory,
    ParameterMetadata,
    SensitivityAnalysis,
    SensitivityEntry,
    load_omit_list,
)


def _resolve_account_name(
    account: str, family: ConfinementFamily | None = None,
) -> str:
    """Resolve a CAS account code to its human-readable name.

    Single source of names = the CAS_NAMES / CAS22_NAMES maps on CostModelData.
    Override codes are authored as upper/``C…`` (e.g. "CAS27", "C220103") while
    the top-level map keys are lowercase, so try the CAS22 map first, then the
    case-normalized top-level map, then fall back to the bare code (visible, not
    blank — an unknown code should surface, not vanish).

    ``family`` is forwarded to ``resolve_cas22_name`` so the shared C220108
    account renders as "Divertor" (MFE) or "Target Factory" (IFE/MIF) instead
    of the ambiguous combined label.
    """
    if account in CostModelData.CAS22_NAMES:
        return CostModelData.resolve_cas22_name(account, family)
    return CostModelData.CAS_NAMES.get(account.lower(), account)


def _build_override_records(
    overrides: list[dict[str, Any]],
    family: ConfinementFamily | None = None,
) -> list[OverrideRecord]:
    """Project a concept's raw ``overrides`` list into OverrideRecord payload.

    Carries every entry (enabled and disabled) so the inspection panel can show
    not-applied entries too (FR-5). A genuinely-absent narrative field becomes
    ``None`` (panel renders "not recorded", FR-6) rather than "".
    """
    records: list[OverrideRecord] = []
    for o in overrides:
        account = str(o["account"])
        records.append(
            OverrideRecord(
                account=account,
                account_name=_resolve_account_name(account, family),
                value=float(o["value"]),
                enabled=bool(o["enabled"]),
                provenance=o.get("provenance"),
                source=o.get("source"),
                rationale=o.get("rationale"),
                cost_basis=o.get("cost_basis"),
                blocked_by=o.get("blocked_by"),
            )
        )
    return records


def _derive_enabled_overrides() -> Any:
    """Return the canonical ``enabled_overrides`` projector.

    Prefer the shared three-forward helper (the source of truth for how the
    analyst override registry projects to the ``cost_overrides`` dict, filtering
    disabled entries). Falls back to an inline last-wins/enabled-only projection
    when the helper module is unavailable — it imports ``costingfe.validation`` at
    module scope, so importing the extractor must not hard-require costingfe (the
    mock-based extractor tests don't install it). Mirrors ``server.py``'s
    identical accessor.
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


# Projects a concept module's `overrides` registry to {account: value}, enabled only.
_enabled_overrides = _derive_enabled_overrides()


class ExtractionError(Exception):
    """Fatal error that should terminate the extraction script with exit code 1."""


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def parse_concept_id(dir_name: str) -> str:
    """Extract concept ID from directory name like '04-laser-icf' → '04'."""
    m = re.match(r"^(\d+[a-z]?)", dir_name)
    if not m:
        raise ValueError(f"Cannot extract concept ID from directory name: {dir_name!r}")
    return m.group(1)


def parse_frontmatter(analysis_path: Path) -> dict[str, Any]:
    """Parse YAML frontmatter from an analysis.md file (returns {} if absent)."""
    text = analysis_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    try:
        end = text.index("---", 3)
    except ValueError:
        return {}
    return yaml.safe_load(text[3:end]) or {}


def _to_confinement_family(raw: Any) -> ConfinementFamily:
    """Map a raw frontmatter value to ConfinementFamily, defaulting to NONSTANDARD.

    Tolerant of missing / unknown values — Invariant 1's strictness applies to
    `Comparison-Status` and `result_1gw`, not to this enum. Frontmatter writes
    one of MFE / IFE / MIF / NONSTANDARD (see lib/frontmatter.py).
    """
    if not raw:
        return ConfinementFamily.NONSTANDARD
    try:
        return ConfinementFamily(str(raw).strip().upper())
    except ValueError:
        return ConfinementFamily.NONSTANDARD


def verify_two_knob(
    result_1gw: Any,
    p_native: float,
    concept_id: str,
    *,
    tolerance_rel: float = 1e-9,
) -> None:
    """Assert result_1gw was reached via forward(net_electric_mw=1000, n_mod=1000/P_native).

    Raises ExtractionError on missing or mismatched params (Invariant 1 / FR-4).
    """
    params = getattr(result_1gw, "params", None) or {}
    net = params.get("net_electric_mw")
    n_mod = params.get("n_mod")

    if net is None or abs(float(net) - 1000.0) > 1e-9:
        raise ExtractionError(
            f"{concept_id}: result_1gw.params['net_electric_mw'] expected 1000, got {net!r}. "
            "result_1gw must come from run_native_and_1gw(...) — see Item 7 helper."
        )

    try:
        p_native_f = float(p_native)
    except (TypeError, ValueError) as exc:
        raise ExtractionError(
            f"{concept_id}: P-Native missing or non-numeric in frontmatter (got {p_native!r})"
        ) from exc

    if p_native_f <= 0:
        raise ExtractionError(
            f"{concept_id}: P-Native must be positive, got {p_native_f}"
        )

    # n_mod check is path-dependent (post-R0-bisection):
    # - use_0d_model=True (tokamak 0D path): the projection scales R0 of a
    #   single bigger machine to deliver 1 GWe at the native plasma regime,
    #   so n_mod is held at 1. The helper bisects R0 instead of stacking
    #   modules.
    # - Otherwise (n_mod-stacking path for FRC / mirror / IFE / non-standard):
    #   n_mod = max(1, round(1000/P_native)) is the replication count to
    #   reach 1 GWe at native module power.
    if params.get("use_0d_model"):
        if n_mod is None or abs(float(n_mod) - 1.0) > 1e-9:
            raise ExtractionError(
                f"{concept_id}: result_1gw.params['n_mod'] expected 1 for "
                f"use_0d_model=True (R0-bisection projection), got {n_mod!r}"
            )
    else:
        expected = max(1, round(1000.0 / p_native_f))
        if n_mod is None or abs(float(n_mod) - expected) > 1e-9:
            raise ExtractionError(
                f"{concept_id}: result_1gw.params['n_mod'] expected {expected} "
                f"(max(1, round(1000/{p_native_f}))), got {n_mod!r}"
            )


def parse_status(frontmatter: dict[str, Any]) -> ConceptStatus:
    raw = str(frontmatter.get("Status", "draft")).lower()
    return ConceptStatus.APPROVED if raw == "approved" else ConceptStatus.IN_PROGRESS


# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------


def load_module_from_path(path: Path, module_name: str = "_concept_module") -> types.ModuleType:
    """Import a Python file, suppressing stdout from module-level side-effects."""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    buf = StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Costingfe pathway
# ---------------------------------------------------------------------------


def _ns_to_dict(obj: Any) -> dict[str, Any]:
    """Flatten a SimpleNamespace's attrs into a dict; pass through if dict."""
    if isinstance(obj, dict):
        return dict(obj)
    return {k: v for k, v in vars(obj).items() if not k.startswith("_")}


def _forward_result_to_dict(result: Any) -> dict[str, Any]:
    """Convert the _wrap-produced result (SimpleNamespace) into the dict shape
    CostModelData.from_forward_result expects.

    Post-PR-#84 the adapter returns a FusionTeaOutput which model_setup_helpers
    re-wraps into a SimpleNamespace mimicking the legacy ForwardResult surface
    (``.costs.cas21``, ``.cas22_detail["C220103"]``, ``.power_table.rec_frac``
    as attributes). That surface isn't a dataclass, so ``dataclasses.asdict``
    can't flatten it; we vars() the nested namespaces by hand.
    """
    return {
        "costs": _ns_to_dict(result.costs),
        "cas22_detail": dict(result.cas22_detail),
        "power_table": _ns_to_dict(result.power_table),
        "overridden": list(getattr(result, "overridden", [])),
        "params": dict(getattr(result, "params", {})),
    }


def build_sensitivity_analysis(
    model: Any,
    result: Any,
    cost_overrides: dict[str, float] | None = None,
    *,
    confinement_family: ConfinementFamily | None = None,
) -> SensitivityAnalysis:
    """Call model.sensitivity(result.params) and wrap output in SensitivityAnalysis.

    model.sensitivity() returns {"engineering": {k: elasticity}, "financial": {k: elasticity}}.
    Baselines come from result.params; missing keys default to 0.0.

    ``cost_overrides`` selects which LCOE function is differentiated (FR-SO4):
    ``None`` → the library-bare tornado; the enabled analyst registry → the
    analyst-applied tornado. The two are computed by independent honest calls
    (INV-3) — the applied tornado is *not* the bare one with overridden accounts
    zeroed (``_scale_overrides`` keeps a rescaled library shape), so callers must
    pass the registry through, never post-adjust.

    Two filters applied:

    1. Pre-call: drop None-valued + ``eta_pin`` keys from ``result.params``
       before passing to ``model.sensitivity``. The library re-runs forward
       internally for each continuous key, and forward() strictly rejects
       unknown / None-valued kwargs (e.g. ``dhe3_dd_frac_pin=None`` on a D-T
       tokamak — present in the all-fuel union schema but invalid for the
       active fuel). ``eta_pin`` is derived from ``eta_source × eta_couple``
       for NBI/RF-heated concepts and the library refuses to pin it. Same
       defensive filter as server._forward_with_overrides (PR #90).

    2. Post-call: drop ``_SENSITIVITY_EXCLUDE_KEYS`` from the returned
       sensitivity dicts before wrapping — see that constant's docstring for
       which keys and why.

    3. If ``confinement_family`` is set and is not MFE/tokamak-routed (i.e.,
       any non-tokamak family — IFE / MIF / stellarator / mirror / FRC /
       NONSTANDARD), additionally drop ``_NON_TOKAMAK_EXCLUDE_KEYS``
       (``R0``, ``plasma_t``, ``elon``). The union-schema library populates
       these keys for every concept with placeholder values, but they have
       no physical correspondence outside tokamaks. NOTE: this only filters
       *non-tokamak* concepts. Stellarator/mirror also map to ConfinementFamily.MFE
       in this codebase, so we'd ideally key off the model's confinement
       concept too. Today the corpus has only tokamak as the MFE family
       that actually uses these knobs; if stellarator/mirror concepts re-
       enter the MFE bucket with valid R0/plasma_t/elon defaults, revisit.
    """
    family_excludes = (
        _NON_TOKAMAK_EXCLUDE_KEYS
        if confinement_family is not None and confinement_family != ConfinementFamily.MFE
        else frozenset()
    )
    sens_params = {k: v for k, v in result.params.items() if v is not None}
    sens_params.pop("eta_pin", None)
    sens_raw: dict[str, dict[str, float]] = model.sensitivity(
        sens_params, cost_overrides=cost_overrides
    )
    params: dict[str, Any] = result.params

    def _entries(group: dict[str, float]) -> dict[str, SensitivityEntry]:
        import math

        return {
            k: SensitivityEntry(elasticity=float(v), baseline=float(params.get(k, 0.0)))
            for k, v in group.items()
            if k not in _SENSITIVITY_EXCLUDE_KEYS
            and k not in family_excludes
            and v is not None
            and math.isfinite(float(v))
        }

    return SensitivityAnalysis(
        engineering=_entries(sens_raw.get("engineering", {})),
        financial=_entries(sens_raw.get("financial", {})),
    )


_FRACTIONAL_NAME_TOKENS = ("eta", "efficiency", "availability", "fraction")
_FRACTIONAL_NAME_EXACT = {"burn_fraction", "fuel_recovery"}


def generate_parameter_metadata(
    sensitivities: SensitivityAnalysis,
) -> dict[str, ParameterMetadata]:
    """Derive ParameterMetadata for every sensitivity param from baselines alone.

    Range strategy: baseline ± 30%, clamped to [0, ∞). Fractional params
    (efficiencies, availability, etc.) additionally clamp to [0, 1]. If the
    baseline is 0 — degenerate range — fall back to (0, 1) so the slider is
    still draggable.

    yaml-authored entries (loaded by `load_parameter_metadata`) override these
    via dict-spread merge in `extract_costingfe()`.
    """
    out: dict[str, ParameterMetadata] = {}
    all_entries = {**sensitivities.engineering, **sensitivities.financial}

    for name, entry in all_entries.items():
        baseline = entry.baseline
        is_fractional = (
            0 < baseline <= 1
            and (
                name in _FRACTIONAL_NAME_EXACT
                or name.startswith("f_")
                or any(tok in name.lower() for tok in _FRACTIONAL_NAME_TOKENS)
            )
        )

        if baseline == 0:
            lo, hi = 0.0, 1.0
        else:
            lo = max(0.0, baseline * 0.7)
            hi = baseline * 1.3
            if is_fractional:
                hi = min(1.0, hi)
            if hi <= lo:
                lo, hi = 0.0, 1.0

        try:
            out[name] = ParameterMetadata(
                display_name=name.replace("_", " ").title(),
                category=ParameterCategory.UNCLASSIFIED,
                confidence=Confidence.UNKNOWN,
                baseline=baseline,
                range=(lo, hi),
            )
        except ValidationError as exc:
            warnings.warn(
                f"generate_parameter_metadata: skipped {name!r}: {exc}",
                UserWarning,
                stacklevel=2,
            )

    return out


def _build_sensitivity_from_dict(
    sens_raw: dict[str, dict[str, float]],
    params: dict[str, float],
    *,
    confinement_family: ConfinementFamily | None = None,
) -> SensitivityAnalysis:
    """Build SensitivityAnalysis from freeform compute_sensitivity() output.

    sens_raw: {"engineering": {param: elasticity}, "financial": {param: elasticity}}
    params: {param: baseline_value} from to_explorer_dict()["params"]

    Applies the same exclude filters as ``build_sensitivity_analysis``: global
    ``_SENSITIVITY_EXCLUDE_KEYS`` always, plus ``_NON_TOKAMAK_EXCLUDE_KEYS``
    for any non-MFE concept. Freeform scripts rarely produce these keys, but
    if they do (e.g. a tokamak-style freeform with R0), the same UX rules
    apply.
    """
    import math

    family_excludes = (
        _NON_TOKAMAK_EXCLUDE_KEYS
        if confinement_family is not None and confinement_family != ConfinementFamily.MFE
        else frozenset()
    )

    def _entries(group: dict[str, float]) -> dict[str, SensitivityEntry]:
        return {
            k: SensitivityEntry(
                elasticity=float(v),
                baseline=float(params.get(k, 0.0)),
            )
            for k, v in group.items()
            if k not in _SENSITIVITY_EXCLUDE_KEYS
            and k not in family_excludes
            and v is not None
            and math.isfinite(float(v))
        }

    return SensitivityAnalysis(
        engineering=_entries(sens_raw.get("engineering", {})),
        financial=_entries(sens_raw.get("financial", {})),
    )


def extract_costingfe(
    concept_dir: Path,
    concept_id: str,
    frontmatter: dict[str, Any],
    analysis_path: Path,
    narrative: NarrativeData | None,
    param_metadata: dict[str, ParameterMetadata],
    *,
    comparison_status: str = "",
) -> ConceptData:
    """Extract a costingfe-backed concept (has model_setup.py with CostModel.forward()).

    When `comparison_status` is "costingfe" or "costingfe-asterisked" (Item 6 frontmatter
    present), the strict-consumer contract applies: result_1gw must exist and pass
    verify_two_knob. `result_1gw` is the single authoritative ForwardResult the
    explorer reads (post-rework; the legacy `result` symbol is gone — three-forward
    contract, see model_setup_helpers.py).
    """
    module = load_module_from_path(concept_dir / "model_setup.py")

    model = getattr(module, "model", None)
    if model is None:
        raise ExtractionError(
            f"{concept_id}: model_setup.py must define module-level 'model'"
        )

    result_1gw = getattr(module, "result_1gw", None)
    if result_1gw is None:
        raise ExtractionError(
            f"{concept_id}: result_1gw missing at module level. The strict-consumer "
            "contract requires model_setup.py to expose result_1gw via "
            "run_native_and_1gw(...). Comparison-Status="
            f"{comparison_status!r}."
        )

    # verify_two_knob only when P-Native is available (Item 6 frontmatter present).
    # Un-migrated concepts won't have P-Native; the strict result_1gw check above
    # is the only invariant they exercise until Item 11 regenerates them.
    p_native = frontmatter.get("P-Native")
    if p_native is not None:
        verify_two_knob(result_1gw, p_native, concept_id)

    effective_result = result_1gw

    # Dual sensitivities (FR-SO4 / Bet 3): `sensitivities` is the analyst-applied
    # tornado (registry re-applied) — the new default, consistent with the applied
    # headline; `sensitivities_bare` is the library-bare alternate the toggle swaps
    # to. Independent honest calls (INV-3). Empty registry → the two are equal
    # (INV-6). The param *keys* are identical across both (cost_overrides changes
    # elasticity values, not which continuous params exist), so metadata generated
    # from the applied set covers the bare set too.
    # Resolve family up-front: needed by both _build_override_records (so the
    # override panel labels C220108 family-aware) and from_forward_result below.
    confinement_family = _to_confinement_family(frontmatter.get("Confinement-Family"))

    raw_overrides = getattr(module, "overrides", []) or []
    enabled = _enabled_overrides(raw_overrides)
    override_records = _build_override_records(raw_overrides, confinement_family)
    sensitivities = build_sensitivity_analysis(
        model, effective_result, cost_overrides=enabled,
        confinement_family=confinement_family,
    )
    sensitivities_bare = build_sensitivity_analysis(
        model, effective_result, cost_overrides=None,
        confinement_family=confinement_family,
    )
    # Three-layer merge (later wins):
    #   1. generate_parameter_metadata() — auto baseline + range + auto display_name
    #   2. shared display registry       — patches display_name/_unit/_multiplier
    #   3. per-concept model_metadata.yaml — full overrides (passed in via param_metadata)
    generated = generate_parameter_metadata(sensitivities)
    patched = apply_display_patches(generated, _DISPLAY_REGISTRY)
    merged_metadata = {**patched, **param_metadata}

    # Flatten the wrapped result (a SimpleNamespace produced by
    # model_setup_helpers._wrap post-PR-#84 adapter migration) into the dict
    # shape CostModelData.from_forward_result expects. Was dataclasses.asdict()
    # when result_1gw was a real ForwardResult; the adapter wrap is a
    # SimpleNamespace, so we vars()-flatten the nested namespaces by hand.
    raw: dict[str, Any] = _forward_result_to_dict(effective_result)

    # availability lives in params, not power_table — inject it so from_forward_result
    # can compute capacity_factor via its "availability" fallback
    params_dict = raw.get("params", {})
    if "availability" in params_dict:
        raw.setdefault("power_table", {})["availability"] = params_dict["availability"]

    cost_model = CostModelData.from_forward_result(
        raw,
        sensitivities,
        sensitivities_bare,
        confinement_family=confinement_family,
    )

    name = str(frontmatter.get("Concept", concept_dir.name))
    company_raw = frontmatter.get("Company")
    company = str(company_raw) if company_raw else None

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        concept = ConceptData(
            concept_id=concept_id,
            name=name,
            confinement_family=confinement_family,
            company=company,
            status=parse_status(frontmatter),
            illustration=None,
            has_cost_model=True,
            has_sensitivities=True,
            model_type=ModelType.COSTINGFE,
            # Read DATA_GROUNDED module-level constant set by analysts in
            # model_setup.py when running the costingfe library against an
            # empty/minimal spec (no disclosed reactor design point). Mirrors
            # the data_grounded flag they already pass to print_cas_breakdown.
            # Default True preserves behavior for the ~33 grounded concepts.
            data_grounded=bool(getattr(module, "DATA_GROUNDED", True)),
            cost_model=cost_model,
            parameter_metadata=merged_metadata,
            narrative=narrative,
            asterisk_in_comparison=(comparison_status == "costingfe-asterisked"),
            analyst_override_count=len(enabled),
            overrides=override_records,
        )

    for w in caught:
        warnings.warn(w.message, w.category, stacklevel=2)

    return concept


# ---------------------------------------------------------------------------
# Centralized freeform adapters
# ---------------------------------------------------------------------------


def _freeform_to_explorer_dict(results: dict[str, Any], params_obj: Any) -> dict[str, Any]:
    """Map freeform compute() output to the explorer dict schema.

    All freeform scripts follow the 5-layer architecture from model_setup_freeform.md,
    producing standardized CAS keys. This centralizes the mapping that was previously
    required as a per-script to_explorer_dict() function.
    """
    c = results.get("costs", {})
    econ = results.get("economics", {})
    cas22 = results.get("cas22", {})
    pw = results.get("power", {})

    n_mod = getattr(params_obj, "n_mod", 1)
    p_net_plant = pw.get("p_net_plant", pw.get("p_net", 0) * n_mod)
    overnight = c.get("overnight_capital", 0)
    overnight_per_kw = (overnight * 1e3 / p_net_plant) if p_net_plant > 0 else 0

    return {
        "costs": {
            "cas10": c.get("CAS10", 0), "cas21": c.get("CAS21", 0),
            "cas22": c.get("CAS22", 0), "cas23": c.get("CAS23", 0),
            "cas24": c.get("CAS24", 0), "cas25": c.get("CAS25", 0),
            "cas26": c.get("CAS26", 0), "cas27": c.get("CAS27", 0),
            "cas28": c.get("CAS28", 0), "cas29": c.get("CAS29", 0),
            "cas20": c.get("CAS20", 0),
            "cas30": c.get("CAS30", 0), "cas40": c.get("CAS40", 0),
            "cas50": c.get("CAS50", 0), "cas60": c.get("CAS60", 0),
            "cas70": econ.get("CAS70", 0), "cas71": econ.get("CAS71", 0),
            "cas72": econ.get("CAS72", 0),
            "cas80": econ.get("CAS80", 0), "cas90": econ.get("CAS90", 0),
            "total_capital": c.get("total_capital", 0),
            "lcoe": econ.get("lcoe_USD_per_MWh", 0),
            "overnight_cost": overnight_per_kw,
        },
        "power_table": {
            "p_fus": pw.get("p_fus", 0) * n_mod,
            "p_th": pw.get("p_th", 0) * n_mod,
            "p_et": pw.get("p_et", 0) * n_mod,
            "p_net": p_net_plant,
            "q_sci": pw.get("Q_sci", 0),
            "q_eng": pw.get("Q_eng", 0),
            "availability": getattr(
                params_obj, "plant_availability",
                getattr(params_obj, "availability", 0),
            ),
            "rec_frac": pw.get("recirc_fraction", 0),
        },
        "cas22_detail": {
            k: cas22.get(k, 0)
            for k in [
                "C220101", "C220102", "C220103", "C220104", "C220105",
                "C220106", "C220107", "C220108", "C220109", "C220111", "C220112",
                "C220200", "C220300", "C220400", "C220500", "C220600", "C220700",
            ]
        },
        "params": {
            f.name: getattr(params_obj, f.name)
            for f in dataclasses.fields(params_obj)
            if isinstance(getattr(params_obj, f.name), (int, float))
        },
        "overridden": [],
    }


def _find_freeform_dataclass(module: types.ModuleType) -> Any | None:
    """Find a @dataclass in the module that has a compute() method.

    Returns an instance created with default field values, or None.
    """
    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and dataclasses.is_dataclass(obj)
            and hasattr(obj, "compute")
            and callable(getattr(obj, "compute"))
        ):
            try:
                return obj()  # instantiate with defaults
            except Exception:
                continue
    return None


def _compute_sensitivity_from_params(
    params_obj: Any, results: dict[str, Any], dp_fraction: float = 0.01
) -> dict[str, dict[str, float]]:
    """Compute LCOE elasticities via central difference on a freeform params dataclass.

    Returns {"engineering": {param: elasticity}, "financial": {param: elasticity}}.
    """
    import math

    base_lcoe = results.get("economics", {}).get("lcoe_USD_per_MWh", 0)
    if base_lcoe <= 0 or not math.isfinite(base_lcoe):
        return {"engineering": {}, "financial": {}}

    financial_keys = {"interest_rate", "inflation_rate"}
    engineering: dict[str, float] = {}
    financial: dict[str, float] = {}
    base_dict = dataclasses.asdict(params_obj)

    for f in dataclasses.fields(params_obj):
        val = getattr(params_obj, f.name)
        if not isinstance(val, float) or val == 0.0:
            continue
        dp = abs(val) * dp_fraction
        try:
            kw_up = {**base_dict, f.name: val + dp}
            lcoe_up = type(params_obj)(**kw_up).compute()["economics"]["lcoe_USD_per_MWh"]
            kw_dn = {**base_dict, f.name: val - dp}
            lcoe_dn = type(params_obj)(**kw_dn).compute()["economics"]["lcoe_USD_per_MWh"]
        except Exception:
            continue
        if not (math.isfinite(lcoe_up) and math.isfinite(lcoe_dn)):
            continue
        elast = (lcoe_up - lcoe_dn) / (2 * dp) * val / base_lcoe
        target = financial if f.name in financial_keys else engineering
        target[f.name] = elast

    return {"engineering": engineering, "financial": financial}


# ---------------------------------------------------------------------------
# Standalone pathway
# ---------------------------------------------------------------------------


def extract_standalone(
    concept_dir: Path,
    concept_id: str,
    frontmatter: dict[str, Any],
    analysis_path: Path,
    narrative: NarrativeData | None,
    param_metadata: dict[str, ParameterMetadata],
) -> ConceptData:
    """Extract a standalone concept (analysis.md only, no costingfe).

    If a Python script with to_explorer_dict() is present, calls it and validates
    the result as CostModelData (sensitivities=None). Otherwise produces a
    ConceptData with cost_model=None.
    """
    cost_model: CostModelData | None = None
    has_cost_model = False
    has_sensitivities = False

    # Family is needed by CostModelData.from_forward_result() so that the
    # shared C220108 account renders as "Divertor" (MFE) or "Target Factory"
    # (IFE/MIF) instead of the ambiguous combined label.
    confinement_family = _to_confinement_family(frontmatter.get("Confinement-Family"))

    # Prefer model_setup.py if present; otherwise first non-test .py file
    script_path: Path | None = None
    model_setup = concept_dir / "model_setup.py"
    if model_setup.exists():
        script_path = model_setup
    else:
        for py_file in sorted(concept_dir.glob("*.py")):
            if not py_file.name.startswith("test_"):
                script_path = py_file
                break

    if script_path is not None:
        loaded_module: types.ModuleType | None = None
        try:
            loaded_module = load_module_from_path(script_path)
        except Exception as exc:
            warnings.warn(
                f"{concept_id}: failed to import {script_path.name}: {exc}",
                UserWarning,
                stacklevel=2,
            )

        if loaded_module is not None:
            to_explorer_dict = getattr(loaded_module, "to_explorer_dict", None)
            params_obj = getattr(loaded_module, "params", None)
            results_obj = getattr(loaded_module, "results", None)

            # Helper: override headline metrics from scaled_headline if present
            def _apply_scaled_headline(rd: dict[str, Any]) -> None:
                sh = getattr(loaded_module, "scaled_headline", None)
                if sh and isinstance(sh, dict):
                    rd.setdefault("costs", {})["lcoe"] = sh.get("lcoe_per_mwh", rd.get("costs", {}).get("lcoe", 0))
                    rd.setdefault("costs", {})["overnight_cost"] = sh.get("overnight_per_kw", rd.get("costs", {}).get("overnight_cost", 0))
                    rd.setdefault("power_table", {})["p_net"] = sh.get("p_net_mw", rd.get("power_table", {}).get("p_net", 0))

            # Path 1: script provides its own mapping (backward compat)
            if to_explorer_dict is not None:
                raw_dict = to_explorer_dict()
                _apply_scaled_headline(raw_dict)
                cost_model = CostModelData.from_forward_result(
                    raw_dict, sensitivities=None, confinement_family=confinement_family,
                )
                has_cost_model = True
            # Path 2: centralized adapter from module-level params + results
            elif (
                params_obj is not None
                and results_obj is not None
                and isinstance(results_obj, dict)
                and dataclasses.is_dataclass(params_obj)
            ):
                raw_dict = _freeform_to_explorer_dict(results_obj, params_obj)
                _apply_scaled_headline(raw_dict)
                cost_model = CostModelData.from_forward_result(
                    raw_dict, sensitivities=None, confinement_family=confinement_family,
                )
                has_cost_model = True
            else:
                # Path 3: discover dataclass with compute(), instantiate with defaults
                if params_obj is None:
                    params_obj = _find_freeform_dataclass(loaded_module)
                if params_obj is not None and dataclasses.is_dataclass(params_obj):
                    try:
                        results_obj = params_obj.compute()
                    except Exception as exc:
                        results_obj = None
                        warnings.warn(
                            f"{concept_id}: compute() failed: {exc}",
                            UserWarning,
                            stacklevel=2,
                        )
                    if isinstance(results_obj, dict):
                        raw_dict = _freeform_to_explorer_dict(results_obj, params_obj)
                        _apply_scaled_headline(raw_dict)
                        cost_model = CostModelData.from_forward_result(
                            raw_dict,
                            sensitivities=None,
                            confinement_family=confinement_family,
                        )
                        has_cost_model = True

                if not has_cost_model:
                    raw_dict = None
                    warnings.warn(
                        f"{concept_id}: {script_path.name} has no to_explorer_dict(), "
                        "no module-level params/results, and no discoverable dataclass "
                        "with compute() — no cost model included",
                        UserWarning,
                        stacklevel=2,
                    )

            # Sensitivity: try script's own function, then centralized
            if has_cost_model and raw_dict is not None:
                compute_sensitivity = getattr(loaded_module, "compute_sensitivity", None)
                if compute_sensitivity is not None:
                    sens_raw = compute_sensitivity()
                elif (
                    params_obj is not None
                    and results_obj is not None
                    and isinstance(results_obj, dict)
                    and dataclasses.is_dataclass(params_obj)
                ):
                    sens_raw = _compute_sensitivity_from_params(params_obj, results_obj)
                else:
                    sens_raw = None

                if sens_raw is not None:
                    params_dict = raw_dict.get("params", {})
                    cost_model.sensitivities = _build_sensitivity_from_dict(
                        sens_raw, params_dict,
                        confinement_family=confinement_family,
                    )
                    has_sensitivities = True

    name = str(frontmatter.get("Concept", concept_dir.name))
    company_raw = frontmatter.get("Company")
    company = str(company_raw) if company_raw else None
    # confinement_family was already resolved at the top of extract_standalone()
    # so the C220108 name on the cost model would render family-aware.

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        concept = ConceptData(
            concept_id=concept_id,
            name=name,
            confinement_family=confinement_family,
            company=company,
            status=parse_status(frontmatter),
            illustration=None,
            has_cost_model=has_cost_model,
            has_sensitivities=has_sensitivities,
            model_type=ModelType.STANDALONE,
            # Same DATA_GROUNDED contract as costingfe path: read the
            # module-level constant set by the analyst, defaulting True for
            # backward compat. Freeform/standalone analysts who have no
            # disclosed design point should set DATA_GROUNDED=False so the
            # explorer drops the concept from cross-concept views. (The
            # model_type==STANDALONE check in build_cost_landscape already
            # excludes freeform LCOEs as methodologically incomparable; this
            # flag provides an explicit, audit-friendly source-level marker
            # — `grep "DATA_GROUNDED = False"` returns the complete list.)
            data_grounded=bool(getattr(loaded_module, "DATA_GROUNDED", True))
            if loaded_module is not None
            else True,
            cost_model=cost_model,
            parameter_metadata=param_metadata,
            narrative=narrative,
        )

    for w in caught:
        warnings.warn(w.message, w.category, stacklevel=2)

    return concept


# ---------------------------------------------------------------------------
# Parameter metadata
# ---------------------------------------------------------------------------


def load_parameter_metadata(concept_dir: Path, concept_id: str) -> dict[str, ParameterMetadata]:
    """Load model_metadata.yaml if present; warn on invalid entries but don't fail."""
    meta_path = concept_dir / "model_metadata.yaml"
    if not meta_path.exists():
        return {}

    raw = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    result: dict[str, ParameterMetadata] = {}
    for key, entry in raw.items():
        try:
            result[key] = ParameterMetadata.model_validate(entry)
        except ValidationError as exc:
            warnings.warn(
                f"{concept_id}: invalid model_metadata.yaml entry for {key!r}: {exc}",
                UserWarning,
                stacklevel=2,
            )
    return result


def load_parameter_display_registry(
    path: Path = _DISPLAY_REGISTRY_PATH,
) -> dict[str, dict[str, Any]]:
    """Load the shared display-name registry as partial-field patches.

    Each entry maps `param_key -> {display_name?, display_unit?, display_multiplier?}`.
    Unknown fields are dropped with a warning. Returns {} if the file is absent.

    Unlike `load_parameter_metadata`, the registry is intentionally partial — it
    patches display fields on top of `generate_parameter_metadata()` output rather
    than replacing the whole `ParameterMetadata`.
    """
    if not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, dict[str, Any]] = {}
    for key, entry in raw.items():
        if not isinstance(entry, dict):
            warnings.warn(
                f"parameter_display_registry: ignoring non-dict entry for {key!r}",
                UserWarning,
                stacklevel=2,
            )
            continue
        unknown = set(entry) - _REGISTRY_PATCH_FIELDS
        if unknown:
            warnings.warn(
                f"parameter_display_registry: unknown fields for {key!r}: {sorted(unknown)}",
                UserWarning,
                stacklevel=2,
            )
        out[key] = {k: v for k, v in entry.items() if k in _REGISTRY_PATCH_FIELDS}
    return out


def apply_display_patches(
    generated: dict[str, ParameterMetadata],
    patches: dict[str, dict[str, Any]],
) -> dict[str, ParameterMetadata]:
    """Apply field-level display patches to generated parameter metadata.

    Only `display_name`, `display_unit`, and `display_multiplier` are patched.
    Generated fields like `baseline`, `range`, `category`, `confidence` are
    preserved. Patches for keys not present in `generated` are ignored
    (registry-key not in this concept's sensitivity output).
    """
    out: dict[str, ParameterMetadata] = {}
    for key, meta in generated.items():
        patch = patches.get(key)
        if not patch:
            out[key] = meta
            continue
        out[key] = meta.model_copy(update=patch)
    return out


# Loaded once; cheap and stateless. Tests can monkeypatch
# `_DISPLAY_REGISTRY` or call `load_parameter_display_registry(custom_path)` directly.
_DISPLAY_REGISTRY: dict[str, dict[str, Any]] = load_parameter_display_registry()


# ---------------------------------------------------------------------------
# Narrative extraction
# ---------------------------------------------------------------------------

_NARRATIVE_PROMPT = """\
You are extracting structured narrative data from a fusion concept analysis document.
Restructure information already present in the source — do NOT invent facts.

Source document:
--- analysis.md ---
{analysis_md}
--- end ---
{model_output_section}
Extract the following and return as JSON only (no preamble, no code fences):

{{
  "key_bets": ["3-7 strings: core technical claims this concept depends on"],
  "eliminated_costs": ["2-5 strings: major costs this concept avoids vs conventional fusion"],
  "novel_costs": ["2-5 strings: unique cost drivers not present in other concepts"],
  "risks": [
    {{"description": "...", "severity": "high|medium|low"}}
  ]
}}
"""


def extract_narrative(concept_dir: Path, concept_id: str) -> NarrativeData:
    """Run claude -p to extract NarrativeData from analysis.md.

    Raises ExtractionError if claude fails or output fails Pydantic validation.
    """
    analysis_path = concept_dir / "analysis.md"
    if not analysis_path.exists():
        raise ExtractionError(f"{concept_id}: analysis.md not found at {analysis_path}")

    analysis_md = analysis_path.read_text(encoding="utf-8")

    model_output_section = ""
    model_output_path = concept_dir / "model_output.txt"
    if model_output_path.exists():
        txt = model_output_path.read_text(encoding="utf-8")
        model_output_section = f"\n--- model_output.txt ---\n{txt}\n--- end ---\n"

    prompt = _NARRATIVE_PROMPT.format(
        analysis_md=analysis_md,
        model_output_section=model_output_section,
    )

    proc = subprocess.run(
        ["claude", "-p", "-"],
        input=prompt,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:
        raise ExtractionError(f"{concept_id}: claude -p exited {proc.returncode}\n{proc.stderr}")

    output = proc.stdout.strip()

    # Strip markdown code fences if present
    fence_m = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", output)
    if fence_m:
        output = fence_m.group(1)

    try:
        return NarrativeData.model_validate_json(output)
    except ValidationError as exc:
        raise ExtractionError(
            f"{concept_id}: NarrativeData validation failed:\n{exc}\n\nRaw output:\n{output}"
        ) from exc


# ---------------------------------------------------------------------------
# Core extraction runner (injectable paths for testing)
# ---------------------------------------------------------------------------


def discover_concepts(
    analyses_dir: Path,
    concept_filter: list[str] | None,
    omitted: set[str] | None = None,
) -> list[Path]:
    """Return sorted concept directories that have model_setup.py or analysis.md.

    *omitted* is the set of concept IDs excluded by the omit list (FR-3); those
    dirs are dropped so no ``data/{id}.json`` is written for them. ``None`` means
    omit nothing — callers that want the unfiltered eligible set (e.g. to report
    what was omitted) pass ``omitted=None``.
    """
    omit_set = omitted or set()
    dirs: list[Path] = []
    for d in sorted(analyses_dir.iterdir()):
        if not d.is_dir():
            continue
        has_model = (d / "model_setup.py").exists()
        has_analysis = (d / "analysis.md").exists()
        if not (has_model or has_analysis):
            continue
        concept_id = parse_concept_id(d.name)
        if concept_filter is not None and concept_id not in concept_filter:
            continue
        if concept_id in omit_set:
            continue
        dirs.append(d)
    return dirs


def _short_error(exc: BaseException) -> str:
    """One-line, type-agnostic summary of a failure for the run report.

    Display only — the batch boundary never branches on the exception; this just
    gives the end-of-run failure banner something human-readable. Returns
    ``"<ExceptionType>: <first line of message>"``, truncated for tidiness.
    """
    text = (str(exc).strip() or repr(exc)).splitlines()
    first_line = text[0] if text else repr(exc)
    if len(first_line) > 200:
        first_line = first_line[:197] + "..."
    return f"{type(exc).__name__}: {first_line}"


def run_extraction(
    analyses_dir: Path,
    data_dir: Path,
    concept_filter: list[str] | None = None,
    skip_narrative: bool = False,
) -> int:
    """Main extraction logic. Separated from CLI parsing for testability.

    Returns the number of concepts that failed. A failure in one concept is
    recorded and the run continues to the next (FR-1); the count lets the CLI
    set a non-zero exit code without aborting the batch.
    """
    if not analyses_dir.exists():
        raise ExtractionError(f"Analyses directory not found: {analyses_dir}")

    data_dir.mkdir(parents=True, exist_ok=True)

    # Omit list (FR-3): load once and enforce here, independently of the server
    # (FR-6). Omitted dirs are dropped from extraction so no data/{id}.json is
    # written or refreshed for them.
    omitted = load_omit_list()
    concept_dirs = discover_concepts(analyses_dir, concept_filter, omitted)
    if not concept_dirs:
        print("WARNING: no concept directories found", file=sys.stderr)
        return 0

    extracted: list[ConceptData] = []
    skipped: list[tuple[str, str]] = []  # (concept_id, reason)
    failed: list[tuple[str, str]] = []  # (concept_id, short_error)

    # Report omitted concepts that actually have an eligible analysis dir present.
    # Re-discover with omitted=None to get the unfiltered eligible set (respecting
    # any --concept filter), then surface the ones the omit list withheld so the
    # run report shows what was excluded rather than silently dropping it.
    if omitted:
        for d in discover_concepts(analyses_dir, concept_filter, omitted=None):
            cid = parse_concept_id(d.name)
            if cid in omitted:
                skipped.append((cid, "omit_list"))

    for concept_dir in concept_dirs:
        concept_id = parse_concept_id(concept_dir.name)
        print(f"Extracting {concept_id} ({concept_dir.name})...", flush=True)

        # Batch boundary (FR-1/FR-4): any failure in a single concept is recorded
        # and the run continues. Intentionally error-agnostic — we do not branch
        # on the exception's type or origin, only capture a short message for the
        # end-of-run summary. The unit functions (extract_costingfe, etc.) keep
        # raising their normal contracts; resilience lives only at this layer.
        try:
            analysis_path = concept_dir / "analysis.md"
            model_setup_path = concept_dir / "model_setup.py"
            frontmatter: dict[str, Any] = {}
            if analysis_path.exists():
                frontmatter = parse_frontmatter(analysis_path)
            elif model_setup_path.exists():
                # Old-shape concept (PR #39 refreshed model_setup.py but did not
                # produce analysis.md). Extraction continues with defaults; the
                # warning makes the degraded state visible to whoever ran extract.
                warnings.warn(
                    f"{concept_id}: no analysis.md — fields defaulted to: "
                    f"Concept (dir name '{concept_dir.name}'), "
                    f"Confinement-Family (NONSTANDARD), "
                    f"Comparison-Status (''), P-Native (None). "
                    f"See rework epic Item 11 to regenerate.",
                    UserWarning,
                    stacklevel=2,
                )

            comparison_status = str(frontmatter.get("Comparison-Status", "")).strip()

            # Bet 8: pending-design-point → skip with explicit message, no ConceptData
            if comparison_status == "pending-design-point":
                msg = (
                    f"  skipped {concept_id}: Comparison-Status=pending-design-point "
                    f"(Item 5 design-point row not yet present; concept omitted from explorer)"
                )
                print(msg)
                skipped.append((concept_id, "pending-design-point"))
                continue

            # NOTE: import-based detection logic parallels run_model() in
            # scripts/lib/claude.py. If you change detection here, update there too.
            if model_setup_path.exists():
                source = model_setup_path.read_text(encoding="utf-8")
                is_costingfe = "CostModel" in source and (
                    "from costingfe" in source or "import costingfe" in source
                )
            else:
                is_costingfe = False

            # Bet 7: routing cross-check (only when frontmatter actually carries the field).
            if comparison_status in {"costingfe", "costingfe-asterisked"} and not is_costingfe:
                raise ExtractionError(
                    f"{concept_id}: routing disagreement — Comparison-Status="
                    f"{comparison_status!r} but model_setup.py is missing or not "
                    "costingfe-shaped (no CostModel + costingfe import). Either the "
                    "concept's model_setup.py is stale / wasn't regenerated, or the "
                    "orchestrator routed it incorrectly."
                )
            if comparison_status == "freeform-deferred" and is_costingfe:
                raise ExtractionError(
                    f"{concept_id}: routing disagreement — Comparison-Status="
                    "'freeform-deferred' but model_setup.py looks costingfe-shaped. "
                    "Likely a stale costingfe model_setup.py from before the concept "
                    "was deferred; remove or regenerate."
                )

            param_metadata = load_parameter_metadata(concept_dir, concept_id)

            narrative: NarrativeData | None = None
            if not skip_narrative and analysis_path.exists():
                narrative = extract_narrative(concept_dir, concept_id)

            if is_costingfe:
                concept_data = extract_costingfe(
                    concept_dir,
                    concept_id,
                    frontmatter,
                    analysis_path,
                    narrative,
                    param_metadata,
                    comparison_status=comparison_status,
                )
            else:
                concept_data = extract_standalone(
                    concept_dir, concept_id, frontmatter, analysis_path, narrative, param_metadata
                )

            out_path = data_dir / f"{concept_id}.json"
            out_path.write_text(concept_data.model_dump_json(indent=2), encoding="utf-8")
            print(f"  wrote {out_path}")

            # Clear staleness sidecar if present (analysis pipeline creates these)
            stale_marker = out_path.with_suffix(".json.stale")
            if stale_marker.exists():
                stale_marker.unlink()
                print(f"  cleared stale marker: {stale_marker.name}")

            extracted.append(concept_data)
        except Exception as exc:  # noqa: BLE001 — batch boundary, see comment above
            short = _short_error(exc)
            failed.append((concept_id, short))
            print(f"  FAILED {concept_id}: {short}", flush=True)
            continue

    if skipped:
        print("", flush=True)
        print(f"Skipped {len(skipped)} concept(s):", flush=True)
        for cid, reason in skipped:
            print(f"  - {cid}: {reason}", flush=True)

    if failed:
        bar = "=" * 64
        print("", flush=True)
        print(bar, flush=True)
        print(f"EXTRACTION FAILED — {len(failed)} concept(s) did NOT refresh:", flush=True)
        print(bar, flush=True)
        for cid, short in failed:
            print(f"  {cid:<6} {short}", flush=True)
        print(bar, flush=True)
        print(
            "Each concept above kept its previous data/ JSON (if any); it was NOT "
            "regenerated this run. Fix the concept and re-run to refresh it.",
            flush=True,
        )

    if not extracted:
        print("WARNING: no concepts extracted", file=sys.stderr)

    return len(failed)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract concept explorer data from analysis pipeline artifacts."
    )
    parser.add_argument(
        "--concept",
        nargs="+",
        metavar="ID",
        help="Restrict to specific concept IDs (e.g. --concept 01 04)",
    )
    parser.add_argument(
        "--skip-narrative",
        action="store_true",
        help="Skip LLM narrative extraction (sets narrative=null)",
    )
    args = parser.parse_args()

    # Per-concept failures are caught inside run_extraction (keep-going); the only
    # ExtractionError that reaches here is a whole-run fatal (e.g. missing analyses
    # dir). Those still abort. A keep-going run that had per-concept failures
    # completes, then exits non-zero so a wrapper/CI sees the run as not clean.
    try:
        failures = run_extraction(
            analyses_dir=_ANALYSES_DIR,
            data_dir=_DATA_DIR,
            concept_filter=args.concept,
            skip_narrative=args.skip_narrative,
        )
    except ExtractionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
