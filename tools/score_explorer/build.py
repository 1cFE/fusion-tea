"""Build tools/score_explorer/data/{concepts.json,weights.json} from
scoring_v2 output.

  concepts.json — one entry per concept, with every axis score, every
                  axis evidence, the composite, composite_axes_included,
                  and every per-axis diagnostic block.
  weights.json  — initial axis_weight values + the axis-specific sub-tables
                  needed to render the "advanced expansion" UI sections.

Usage:
    uv run python tools/score_explorer/build.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORES_CSV = REPO_ROOT / "exploration" / "scoring_v2" / "scores" / "table.csv"
FEATURES_DIR = REPO_ROOT / "exploration" / "scoring_v2" / "features"
TAXONOMY_CSV = REPO_ROOT / "exploration" / "concept_analysis" / "table.csv"
WEIGHTS_PATH = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"
OUT_DIR = Path(__file__).resolve().parent / "data"

AXES = (
    "modularity",
    "supply_chain",
    "plant_complexity",
    "customization",
    "upper_cf",
    "technical_feasibility",
    "data_availability",
)

DIAGNOSTIC_BLOCKS = tuple(f"{a}_diagnostics" for a in AXES)

# Concepts the scoring framework scores but the Score Explorer UI hides.
# Display-only exclusion — score.py still scores all 40; these just don't
# appear in concepts.json.
#   30-laser-icf-nif-commercialization: redundant with
#     26-laser-icf-indirect-drive — both are Inertia Enterprises laser-ICF
#     indirect-drive concepts (the modularity spec's v5 ID-drift table maps
#     both to a single v5 matrix entry).
EXCLUDED_FROM_UI = {
    "30-laser-icf-nif-commercialization",
}


def _maybe_float(s: str) -> float | None:
    return float(s) if s else None


def _load_taxonomy() -> dict[str, dict[str, str]]:
    """Load the v3 ontology table indexed by concept ID. Provides the
    Company column that the scoring CSV doesn't carry."""
    out: dict[str, dict[str, str]] = {}
    with open(TAXONOMY_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cid = r.get("ID", "").strip()
            if cid:
                out[cid] = r
    return out


# Trailing-fuel suffix stripper. Concept names like "HTS Compact Tokamak (D-T)"
# duplicate the fuel that's already shown in the subheader.
_FUEL_SUFFIXES = (" (D-T)", " (D-D)", " (D-He3)", " (p-B11)")


def _display_name(name: str) -> str:
    """Strip ' (D-T)' / ' (p-B11)' etc. trailing suffixes so the name is
    consistent across concepts (the fuel lives in the subheader)."""
    for suf in _FUEL_SUFFIXES:
        if name.endswith(suf):
            return name[: -len(suf)]
    return name


def _concept_features(doc: dict) -> dict:
    """Extract the human-readable feature subset for the concept card."""
    keys = (
        "confinement_family", "mfe_topology", "ife_driver", "mif_method",
        "non_standard_mechanism", "tokamak_shape", "stellarator_type",
        "laser_approach", "confinement_concept",
        "fuel", "operation_mode", "repetition_rate",
        "primary_heating", "driver_technology",
        "magnet_type", "blanket_config", "energy_capture",
        "unit_count_estimate",
    )
    out = {}
    for k in keys:
        block = doc.get(k)
        if isinstance(block, dict) and "value" in block:
            out[k] = block["value"]
    return out


def build_concepts() -> list[dict]:
    """Produce the concepts.json list."""
    with open(SCORES_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    taxonomy = _load_taxonomy()

    out = []
    for row in rows:
        cid = row["concept_id"]
        if cid in EXCLUDED_FROM_UI:
            continue
        feature_path = FEATURES_DIR / f"{cid}.yaml"
        with open(feature_path, encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
        diagnostics = {
            block: doc[block] for block in DIAGNOSTIC_BLOCKS if block in doc
        }
        composite_axes_included = []
        try:
            composite_axes_included = json.loads(row["composite_axes_included"])
        except (json.JSONDecodeError, KeyError):
            pass
        tax_row = taxonomy.get(cid, {})
        out.append({
            "concept_id": cid,
            "name": row["name"],
            "display_name": _display_name(row["name"]),
            "company": tax_row.get("Company", "").strip() or None,
            "scores": {a: _maybe_float(row.get(a, "")) for a in AXES},
            "composite": _maybe_float(row.get("composite", "")),
            "composite_axes_included": composite_axes_included,
            "evidence": {
                a: row.get(f"{a}_evidence", "") or None for a in AXES
            },
            "composite_evidence": row.get("composite_evidence", "") or None,
            "features": _concept_features(doc),
            "diagnostics": diagnostics,
        })
    return out


def build_weights() -> dict:
    """Produce the weights.json with axis weights + advanced sub-tables."""
    with open(WEIGHTS_PATH, encoding="utf-8") as f:
        full = yaml.safe_load(f) or {}
    out = {
        "axes": [],
        "composite": full.get("composite", {}),
    }
    for axis in AXES:
        block = full.get(axis) or {}
        # Capture sub-tables (anything except axis_weight + embedding_weights)
        sub_tables = {
            k: v for k, v in block.items()
            if k not in ("axis_weight", "embedding_weights")
        }
        out["axes"].append({
            "name": axis,
            "axis_weight": float(block.get("axis_weight", 1.0)),
            "embedding_weights": block.get("embedding_weights") or {},
            "sub_tables": sub_tables,
        })
    return out


def main() -> int:
    if not SCORES_CSV.exists():
        print(f"ERROR: {SCORES_CSV} not found — run score.py first.", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    concepts = build_concepts()
    weights = build_weights()

    concepts_path = OUT_DIR / "concepts.json"
    weights_path = OUT_DIR / "weights.json"
    concepts_path.write_text(
        json.dumps(concepts, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    weights_path.write_text(
        json.dumps(weights, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"wrote {concepts_path.relative_to(REPO_ROOT)}  ({len(concepts)} concepts)")
    print(f"wrote {weights_path.relative_to(REPO_ROOT)}  ({len(weights['axes'])} axes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
