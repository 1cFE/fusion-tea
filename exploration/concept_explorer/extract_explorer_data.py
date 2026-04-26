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
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

_HERE = Path(__file__).parent
_PROJECT_ROOT = _HERE.parent.parent  # .../exploration/concept_explorer/ → project root
_ANALYSES_DIR = _HERE.parent / "concept_analysis" / "analyses"
_DATA_DIR = _HERE / "data"

# Ensure project root is on sys.path so fully-qualified package imports work
# when the script is run directly (uv run python exploration/.../extract_explorer_data.py)
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from exploration.concept_explorer.models import (  # noqa: E402, I001
    CostModelData,
    ConceptData,
    ConceptManifest,
    ConceptManifestEntry,
    ConceptStatus,
    ConfinementFamily,
    Confidence,
    NarrativeData,
    ParameterCategory,
    ParameterConceptEntry,
    ParameterIndex,
    ParameterIndexEntry,
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


def parse_confinement_family(analysis_path: Path) -> ConfinementFamily:
    """Derive ConfinementFamily from '**Confinement Family**: ...' in analysis.md."""
    text = analysis_path.read_text(encoding="utf-8")
    m = re.search(r"\*\*Confinement Family\*\*:\s*(.+)", text)
    if not m:
        return ConfinementFamily.NONSTANDARD
    raw = m.group(1).strip().upper()
    if raw.startswith("MFE"):
        return ConfinementFamily.MFE
    if raw.startswith("IFE"):
        return ConfinementFamily.IFE
    if raw.startswith("MIF"):
        return ConfinementFamily.MIF
    return ConfinementFamily.NONSTANDARD


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
) -> ConceptData:
    """Extract a costingfe-backed concept (has model_setup.py with CostModel.forward())."""
    module = load_module_from_path(concept_dir / "model_setup.py")

    model = getattr(module, "model", None)
    result = getattr(module, "result", None)
    if model is None or result is None:
        raise ExtractionError(
            f"{concept_id}: model_setup.py must define module-level 'model' and 'result'"
        )

    # Use result_1gw (per-account scaled) when present, otherwise native result
    result_1gw = getattr(module, "result_1gw", None)
    effective_result = result_1gw if result_1gw is not None else result

    sensitivities = build_sensitivity_analysis(model, effective_result)
    # Auto-derive ParameterMetadata for every sensitivity param; yaml-authored
    # entries (passed in via param_metadata) override generated entries.
    merged_metadata = {**generate_parameter_metadata(sensitivities), **param_metadata}

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
    confinement_family = (
        parse_confinement_family(analysis_path)
        if analysis_path.exists()
        else ConfinementFamily.NONSTANDARD
    )

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
    confinement_family = (
        parse_confinement_family(analysis_path)
        if analysis_path.exists()
        else ConfinementFamily.NONSTANDARD
    )

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
# Manifest and parameter index builders
# ---------------------------------------------------------------------------


def build_manifest(concepts: list[ConceptData]) -> ConceptManifest:
    """Build a ConceptManifest from extracted concepts."""
    entries: list[ConceptManifestEntry] = []
    for concept in concepts:
        lcoe: float | None = None
        confidence: Confidence | None = None

        if concept.cost_model is not None:
            lcoe = concept.cost_model.headline.lcoe_per_mwh

        if concept.parameter_metadata:
            conf_values = [pm.confidence for pm in concept.parameter_metadata.values()]
            # Pick the most common confidence level as the overall concept confidence
            counts = {c: conf_values.count(c) for c in set(conf_values)}
            confidence = max(counts, key=lambda c: counts[c])

        entries.append(
            ConceptManifestEntry(
                concept_id=concept.concept_id,
                name=concept.name,
                confinement_family=concept.confinement_family,
                company=concept.company,
                status=concept.status,
                illustration=concept.illustration,
                has_cost_model=concept.has_cost_model,
                has_sensitivities=concept.has_sensitivities,
                lcoe_per_mwh=lcoe,
                confidence=confidence,
                data_file=f"data/{concept.concept_id}.json",
            )
        )

    return ConceptManifest(
        generated_at=datetime.now(UTC).isoformat(),
        concepts=entries,
    )


def build_parameter_index(concepts: list[ConceptData]) -> ParameterIndex:
    """Build a cross-concept ParameterIndex from all sensitivity data."""
    # param_name → list of per-concept entries
    param_concepts: dict[str, list[ParameterConceptEntry]] = {}
    # param_name → (display_name, category) — first match wins
    param_info: dict[str, tuple[str, ParameterCategory]] = {}

    for concept in concepts:
        if concept.cost_model is None or concept.cost_model.sensitivities is None:
            continue

        sens = concept.cost_model.sensitivities
        all_entries = {**sens.engineering, **sens.financial}

        for param_name, entry in all_entries.items():
            param_concepts.setdefault(param_name, []).append(
                ParameterConceptEntry(
                    concept_id=concept.concept_id,
                    name=concept.name,
                    elasticity=entry.elasticity,
                )
            )
            if param_name not in param_info:
                pm = concept.parameter_metadata.get(param_name)
                if pm is not None:
                    param_info[param_name] = (pm.display_name, pm.category)
                else:
                    param_info[param_name] = (param_name, ParameterCategory.UNCLASSIFIED)

    parameters: dict[str, ParameterIndexEntry] = {
        param_name: ParameterIndexEntry(
            param_name=param_name,
            display_name=param_info[param_name][0],
            category=param_info[param_name][1],
            concepts=concept_entries,
        )
        for param_name, concept_entries in param_concepts.items()
    }

    return ParameterIndex(parameters=parameters)


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


def run_extraction(
    analyses_dir: Path,
    data_dir: Path,
    concept_filter: list[str] | None = None,
    skip_narrative: bool = False,
) -> None:
    """Main extraction logic. Separated from CLI parsing for testability."""
    if not analyses_dir.exists():
        raise ExtractionError(f"Analyses directory not found: {analyses_dir}")

    data_dir.mkdir(parents=True, exist_ok=True)

    concept_dirs = discover_concepts(analyses_dir, concept_filter)
    if not concept_dirs:
        print("WARNING: no concept directories found", file=sys.stderr)
        return

    extracted: list[ConceptData] = []

    for concept_dir in concept_dirs:
        concept_id = parse_concept_id(concept_dir.name)
        print(f"Extracting {concept_id} ({concept_dir.name})...", flush=True)

        analysis_path = concept_dir / "analysis.md"
        frontmatter: dict[str, Any] = {}
        if analysis_path.exists():
            frontmatter = parse_frontmatter(analysis_path)

        param_metadata = load_parameter_metadata(concept_dir, concept_id)

        narrative: NarrativeData | None = None
        if not skip_narrative and analysis_path.exists():
            narrative = extract_narrative(concept_dir, concept_id)

        # NOTE: import-based detection logic parallels run_model() in
        # scripts/lib/claude.py. If you change detection here, update there too.
        model_setup_path = concept_dir / "model_setup.py"
        if model_setup_path.exists():
            source = model_setup_path.read_text(encoding="utf-8")
            is_costingfe = "CostModel" in source and (
                "from costingfe" in source or "import costingfe" in source
            )
        else:
            is_costingfe = False

        if is_costingfe:
            concept_data = extract_costingfe(
                concept_dir, concept_id, frontmatter, analysis_path, narrative, param_metadata
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

    if not extracted:
        print("WARNING: no concepts extracted", file=sys.stderr)
        return

    manifest = build_manifest(extracted)
    manifest_path = data_dir / "manifest.json"
    manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    print(f"Wrote manifest ({len(extracted)} concepts) → {manifest_path}")

    param_index = build_parameter_index(extracted)
    index_path = data_dir / "parameter_index.json"
    index_path.write_text(param_index.model_dump_json(indent=2), encoding="utf-8")
    print(f"Wrote parameter index ({len(param_index.parameters)} params) → {index_path}")


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

    try:
        run_extraction(
            analyses_dir=_ANALYSES_DIR,
            data_dir=_DATA_DIR,
            concept_filter=args.concept,
            skip_narrative=args.skip_narrative,
        )
    except ExtractionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
