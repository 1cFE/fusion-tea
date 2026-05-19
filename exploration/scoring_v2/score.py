"""scoring_v2 score driver.

Loads schema, validates every features/*.yaml, evaluates the embedding registry
against each concept, applies weights, emits scores/table.csv. Deterministic
(byte-identical across runs over unchanged inputs). No LLM. No file I/O from
embedding functions (they receive their declared inputs as a dict).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io, schema as schema_mod
from exploration.scoring_v2.embeddings import rulebook  # noqa: F401  registers embeddings

DIMENSIONS = [
    "economic_potential",
    "technical_feasibility",
    "manufacturability_scale_out",
]
EVIDENCE_COLUMNS = ["ep_evidence", "tf_evidence", "mso_evidence"]
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}
CONFIDENCE_NAME = {0: "low", 1: "medium", 2: "high"}

DEFAULT_SCORES_DIR = Path(__file__).resolve().parent / "scores"
DEFAULT_WEIGHTS = Path(__file__).resolve().parent / "weights" / "default.yaml"


def _evaluate_concept(doc: dict) -> tuple[dict[str, float | None], dict[str, str]]:
    """Run every embedding against one concept's feature doc.

    Embeddings may declare other embeddings as inputs (a one-level dependency
    DAG). We resolve in dependency order: each pass evaluates any embedding
    whose inputs are now all available (either features in ``doc`` or
    previously-resolved embeddings). Cycles or unresolvable embeddings get
    ``None`` and confidence "low".

    Returns:
        emb_values: {embedding_name: scalar or None}
        emb_confidence: {embedding_name: min-confidence over inputs}
    """
    emb_values: dict[str, float | None] = {}
    emb_confidence: dict[str, str] = {}
    remaining = dict(rulebook.REGISTRY)

    def _input_state(inp: str) -> tuple[bool, Any, str]:
        """Return (available, value, confidence) for one input name."""
        if inp in doc:
            block = doc[inp]
            return True, block["value"], block["confidence"]
        if inp in emb_values:
            return True, emb_values[inp], emb_confidence.get(inp, "low")
        return False, None, "low"

    while remaining:
        progress = False
        for name in list(remaining):
            emb = remaining[name]
            states = [_input_state(inp) for inp in emb.inputs]
            if not all(avail for avail, _, _ in states):
                continue
            kwargs = {inp: v for inp, (_, v, _) in zip(emb.inputs, states)}
            try:
                emb_values[name] = emb.fn(**kwargs)
            except Exception:
                emb_values[name] = None
            rank = min(CONFIDENCE_RANK[c] for _, _, c in states) if states else CONFIDENCE_RANK["high"]
            emb_confidence[name] = CONFIDENCE_NAME[rank]
            del remaining[name]
            progress = True
        if not progress:
            for name in remaining:
                emb_values[name] = None
                emb_confidence[name] = "low"
            break
    return emb_values, emb_confidence


def _validate_weights(weights: dict) -> None:
    registry = rulebook.REGISTRY
    for dim, mapping in weights.items():
        if dim not in DIMENSIONS:
            raise ValueError(f"weights: unknown dimension {dim!r}")
        if not mapping:
            continue
        for emb_name in mapping:
            if emb_name not in registry:
                raise ValueError(
                    f"weights: dimension {dim!r} references unregistered embedding {emb_name!r}"
                )


def _score_dimension(
    dim_weights: dict[str, float],
    emb_values: dict[str, float | None],
    emb_confidence: dict[str, str],
) -> tuple[float, str]:
    total = 0.0
    min_rank: int | None = None
    for emb_name, w in dim_weights.items():
        v = emb_values.get(emb_name)
        contribution = 0.0 if v is None else float(v) * float(w)
        total += contribution
        if w != 0:
            r = CONFIDENCE_RANK[emb_confidence.get(emb_name, "low")]
            min_rank = r if min_rank is None else min(min_rank, r)
    evidence = CONFIDENCE_NAME[min_rank] if min_rank is not None else "high"
    return total, evidence


def run(features_dir: Path, scores_dir: Path, weights_path: Path) -> Path:
    schema = schema_mod.load_schema()
    files = sorted(Path(features_dir).glob("*.yaml"))
    if not files:
        raise SystemExit(f"no feature files in {features_dir}")
    for f in files:
        schema_mod.validate_features_file(f, schema)

    with open(weights_path) as f:
        weights = yaml.safe_load(f) or {}
    _validate_weights(weights)

    rows: list[dict] = []
    for fpath in files:
        doc = yaml.safe_load(fpath.read_text())
        meta = doc["_meta"]
        emb_values, emb_conf = _evaluate_concept(doc)
        row: dict[str, str] = {
            "concept_id": meta["concept_id"],
            "name": meta["name"],
        }
        for dim, ev_col in zip(DIMENSIONS, EVIDENCE_COLUMNS):
            score, evidence = _score_dimension(weights.get(dim) or {}, emb_values, emb_conf)
            row[dim] = f"{score:.4f}"
            row[ev_col] = evidence
        rows.append(row)

    rows.sort(key=lambda r: r["concept_id"])
    scores_dir.mkdir(parents=True, exist_ok=True)
    out = scores_dir / "table.csv"
    fieldnames = ["concept_id", "name", *DIMENSIONS, *EVIDENCE_COLUMNS]
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features-dir", type=Path, default=schema_mod.FEATURES_DIR)
    parser.add_argument("--scores-dir", type=Path, default=DEFAULT_SCORES_DIR)
    parser.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS)
    args = parser.parse_args(argv)
    out = run(args.features_dir, args.scores_dir, args.weights)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
