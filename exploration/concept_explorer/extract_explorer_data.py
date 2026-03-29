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

    sensitivities = build_sensitivity_analysis(model, result)

    # dataclasses.asdict() flattens the nested ForwardResult into plain dicts
    raw: dict[str, Any] = dataclasses.asdict(result)

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
            parameter_metadata=param_metadata,
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

    # Look for any .py file in the concept dir (excluding test files)
    script_path: Path | None = None
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
            if to_explorer_dict is not None:
                raw_dict = to_explorer_dict()
                cost_model = CostModelData.model_validate(raw_dict)
                has_cost_model = True
            else:
                warnings.warn(
                    f"{concept_id}: {script_path.name} has no to_explorer_dict() "
                    "— no cost model included",
                    UserWarning,
                    stacklevel=2,
                )

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
            has_sensitivities=False,
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

        is_costingfe = (concept_dir / "model_setup.py").exists()
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
