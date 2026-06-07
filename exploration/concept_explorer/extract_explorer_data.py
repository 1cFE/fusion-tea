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
    NarrativeData,
    ParameterCategory,
    ParameterMetadata,
    SensitivityAnalysis,
    SensitivityEntry,
    SourcePaths,
)


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

    # The helper (model_setup_helpers.py:169) rounds n_mod to an integer:
    #   n_mod = max(1, int(round(1000.0 / p_native)))
    # The 1 GWe projection is a comparison convenience, not a real plant design
    # point, so the rounding has no analytical meaning beyond "how many of this
    # module to reach ~1 GWe." Verifier matches what the helper actually emits.
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


def build_sensitivity_analysis(model: Any, result: Any) -> SensitivityAnalysis:
    """Call model.sensitivity(result.params) and wrap output in SensitivityAnalysis.

    model.sensitivity() returns {"engineering": {k: elasticity}, "financial": {k: elasticity}}.
    Baselines come from result.params; missing keys default to 0.0.
    """
    sens_raw: dict[str, dict[str, float]] = model.sensitivity(result.params)
    params: dict[str, Any] = result.params

    def _entries(group: dict[str, float]) -> dict[str, SensitivityEntry]:
        import math

        return {
            k: SensitivityEntry(elasticity=float(v), baseline=float(params.get(k, 0.0)))
            for k, v in group.items()
            if v is not None and math.isfinite(float(v))
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
) -> SensitivityAnalysis:
    """Build SensitivityAnalysis from freeform compute_sensitivity() output.

    sens_raw: {"engineering": {param: elasticity}, "financial": {param: elasticity}}
    params: {param: baseline_value} from to_explorer_dict()["params"]
    """
    import math

    def _entries(group: dict[str, float]) -> dict[str, SensitivityEntry]:
        return {
            k: SensitivityEntry(
                elasticity=float(v),
                baseline=float(params.get(k, 0.0)),
            )
            for k, v in group.items()
            if v is not None and math.isfinite(float(v))
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

    sensitivities = build_sensitivity_analysis(model, effective_result)
    # Three-layer merge (later wins):
    #   1. generate_parameter_metadata() — auto baseline + range + auto display_name
    #   2. shared display registry       — patches display_name/_unit/_multiplier
    #   3. per-concept model_metadata.yaml — full overrides (passed in via param_metadata)
    generated = generate_parameter_metadata(sensitivities)
    patched = apply_display_patches(generated, _DISPLAY_REGISTRY)
    merged_metadata = {**patched, **param_metadata}

    # dataclasses.asdict() flattens the nested ForwardResult into plain dicts
    raw: dict[str, Any] = dataclasses.asdict(effective_result)

    # availability lives in params, not power_table — inject it so from_forward_result
    # can compute capacity_factor via its "availability" fallback
    params_dict = raw.get("params", {})
    if "availability" in params_dict:
        raw.setdefault("power_table", {})["availability"] = params_dict["availability"]

    cost_model = CostModelData.from_forward_result(raw, sensitivities)

    name = str(frontmatter.get("Concept", concept_dir.name))
    company_raw = frontmatter.get("Company")
    company = str(company_raw) if company_raw else None
    confinement_family = _to_confinement_family(frontmatter.get("Confinement-Family"))

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
            cost_model=cost_model,
            parameter_metadata=merged_metadata,
            narrative=narrative,
            sources=SourcePaths(
                model_setup=str(concept_dir / "model_setup.py"),
                analysis=str(analysis_path) if analysis_path.exists() else None,
            ),
            asterisk_in_comparison=(comparison_status == "costingfe-asterisked"),
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
                cost_model = CostModelData.from_forward_result(raw_dict, sensitivities=None)
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
                cost_model = CostModelData.from_forward_result(raw_dict, sensitivities=None)
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
                            raw_dict, sensitivities=None
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
                        sens_raw, params_dict
                    )
                    has_sensitivities = True

    name = str(frontmatter.get("Concept", concept_dir.name))
    company_raw = frontmatter.get("Company")
    company = str(company_raw) if company_raw else None
    confinement_family = _to_confinement_family(frontmatter.get("Confinement-Family"))

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
            cost_model=cost_model,
            parameter_metadata=param_metadata,
            narrative=narrative,
            sources=SourcePaths(
                model_setup=None,
                analysis=str(analysis_path) if analysis_path.exists() else None,
            ),
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
) -> list[Path]:
    """Return sorted concept directories that have model_setup.py or analysis.md."""
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

    concept_dirs = discover_concepts(analyses_dir, concept_filter)
    if not concept_dirs:
        print("WARNING: no concept directories found", file=sys.stderr)
        return 0

    extracted: list[ConceptData] = []
    skipped: list[tuple[str, str]] = []  # (concept_id, reason)
    failed: list[tuple[str, str]] = []  # (concept_id, short_error)

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
