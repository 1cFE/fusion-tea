"""scoring_v2 score driver.

Loads schema, validates every features/*.yaml, evaluates the embedding registry
against each concept, applies weights, emits scores/table.csv. Deterministic
(byte-identical across runs over unchanged inputs). No LLM. No file I/O from
embedding functions (they receive their declared inputs as a dict).

P2 of the scoring-v3 rewrite replaced the 3-dimension model
(economic_potential / technical_feasibility / manufacturability_scale_out)
with 7 peer axes + a weighted-average composite:

    modularity, supply_chain, plant_complexity, customization,
    upper_cf, technical_feasibility, data_availability
    + composite

Each axis declares `axis_weight` (composite contribution) and
`embedding_weights` (within-axis blend) in weights/default.yaml. The
composite skips null axes and rescales the remaining weights so a
concept with 5 valid axes still gets a meaningful composite.
"""
from __future__ import annotations

import argparse
import csv
import inspect
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io, schema as schema_mod
from exploration.scoring_v2.embeddings import rulebook  # noqa: F401  registers embeddings

# The seven peer axes. Order matters for CSV column layout.
AXES = (
    "modularity",
    "supply_chain",
    "plant_complexity",
    "customization",
    "upper_cf",
    "technical_feasibility",
    "data_availability",
)

CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}
CONFIDENCE_NAME = {0: "low", 1: "medium", 2: "high"}

DEFAULT_SCORES_DIR = Path(__file__).resolve().parent / "scores"
DEFAULT_WEIGHTS = Path(__file__).resolve().parent / "weights" / "default.yaml"


def _evaluate_concept(
    doc: dict, weights_yaml: dict, schema: dict
) -> tuple[dict[str, float | None], dict[str, str]]:
    """Run every embedding against one concept's feature doc.

    Embeddings may declare other embeddings as inputs (a one-level dependency
    DAG). We resolve in dependency order: each pass evaluates any embedding
    whose inputs are now all available (either features in ``doc`` or
    previously-resolved embeddings). Cycles or unresolvable embeddings get
    ``None`` and confidence "low".

    Input resolution rules (in priority order):
      1. If the input is a feature block on disk → use its value/confidence
      2. If the input is another embedding already resolved → use that
      3. If the input is a schema-declared feature but absent for this
         concept (necessarily `required: false`) → resolve to (None, "low")
         so embeddings that explicitly handle missing inputs (e.g.
         `_percent_mod`'s equal-weight fallback for missing capex shares)
         can fire. validate_features_file ensures required: true features
         are always present.
      4. Otherwise the input is unresolvable → the embedding short-circuits
         to None.

    Embeddings whose signature includes a keyword-only `weights_yaml`
    parameter (used by lookup-table-based embeddings) receive the parsed
    weights dict as that kwarg; others do not. Detection is via
    inspect.signature at registration time (see rulebook.py).
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
        if inp in schema:
            # Schema-declared but absent for this concept (required:false).
            # Resolve to None so the embedding can fire and apply its own
            # missing-input policy.
            return True, None, "low"
        return False, None, "low"

    while remaining:
        progress = False
        for name in list(remaining):
            emb = remaining[name]
            states = [_input_state(inp) for inp in emb.inputs]
            if not all(avail for avail, _, _ in states):
                continue
            kwargs = {inp: v for inp, (_, v, _) in zip(emb.inputs, states)}
            if emb.needs_weights:
                kwargs["weights_yaml"] = weights_yaml
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
    for key, block in weights.items():
        if key == "composite":
            continue
        if key not in AXES:
            raise ValueError(
                f"weights: unknown top-level key {key!r}; expected one of "
                f"{AXES} or 'composite'"
            )
        if not isinstance(block, dict):
            raise ValueError(f"weights: axis {key!r} must be a mapping")
        emb_weights = block.get("embedding_weights") or {}
        for emb_name in emb_weights:
            if emb_name not in registry:
                raise ValueError(
                    f"weights: axis {key!r} references unregistered embedding {emb_name!r}"
                )


def _score_axis(
    axis_block: dict,
    emb_values: dict[str, float | None],
    emb_confidence: dict[str, str],
) -> tuple[float | None, str | None]:
    """Compute a single axis score from its embedding_weights block.

    Returns (None, None) if no embeddings are declared for the axis (the
    axis is "not wired yet" — composite skips it) or if any non-zero-
    weighted embedding evaluates to None (incomplete inputs — can't
    confidently blend).

    Embedding weights need not sum to 1.0; we normalize by the sum of
    non-zero weights so the resulting score is in the same scale as the
    individual embeddings (1-5).
    """
    weights = axis_block.get("embedding_weights") or {}
    if not weights:
        return None, None
    total_w = 0.0
    weighted_sum = 0.0
    min_rank: int | None = None
    for emb_name, w in weights.items():
        w = float(w)
        if w == 0:
            continue
        v = emb_values.get(emb_name)
        if v is None:
            return None, None
        weighted_sum += float(v) * w
        total_w += w
        r = CONFIDENCE_RANK[emb_confidence.get(emb_name, "low")]
        min_rank = r if min_rank is None else min(min_rank, r)
    if total_w == 0:
        return None, None
    score = weighted_sum / total_w
    evidence = CONFIDENCE_NAME[min_rank] if min_rank is not None else "high"
    return score, evidence


def _normalize_axes(
    per_concept_axis_scores: dict[str, dict[str, float | None]],
    weights: dict,
) -> dict[str, dict[str, float | None]]:
    """Apply corpus-wide stretch + offset normalization to axes that declare
    a `normalization:` block in weights/default.yaml.

    For each declaring axis, finds (scale, offset) that:
      1. Stretches the raw score distribution around its corpus mean by
         `scale` so the corpus variance approaches `target_variance`.
      2. Adds an offset so the corpus mean lands at `target_mean`.
      3. Applies `floor` (default 1.0) at every transform step.

    Iterates on `scale` to compensate when the floor clips concepts and
    pulls the achieved variance below target. Returns within
    `tolerance` of both targets (default 0.1) or with the best-achievable
    fit if the floor prevents reaching them.

    Returns a new per-concept axis_scores dict with the normalized values.
    The diagnostic blocks in feature files keep the raw scores (debug aid).
    """
    import statistics
    out = {cid: dict(scores) for cid, scores in per_concept_axis_scores.items()}
    for axis in AXES:
        norm_block = (weights.get(axis) or {}).get("normalization")
        if not norm_block:
            continue
        target_mean = float(norm_block["target_mean"])
        target_var = float(norm_block["target_variance"])
        tol = float(norm_block.get("tolerance", 0.1))
        floor = float(norm_block.get("floor", 1.0))

        items = [(cid, s[axis]) for cid, s in out.items() if s.get(axis) is not None]
        if len(items) < 2:
            continue
        cid_order = [cid for cid, _ in items]
        vals = [v for _, v in items]
        raw_mean = statistics.mean(vals)
        raw_var = statistics.variance(vals)
        if raw_var <= 0:
            continue

        base_scale = (target_var / raw_var) ** 0.5
        best = None
        best_var_err = float("inf")
        # Search scale up to 4x the naive sqrt to compensate for floor clipping
        for s_mult_idx in range(0, 300):
            s_mult = 1.0 + 0.01 * s_mult_idx
            scale = base_scale * s_mult
            stretched = [max(floor, raw_mean + scale * (v - raw_mean)) for v in vals]
            # Iterate offset to converge mean (floor shifts it after each apply)
            offset = target_mean - statistics.mean(stretched)
            final: list[float] = []
            for _ in range(15):
                final = [max(floor, s + offset) for s in stretched]
                m = statistics.mean(final)
                if abs(target_mean - m) < 1e-4:
                    break
                offset += target_mean - m
            m = statistics.mean(final)
            v_final = statistics.variance(final)
            if abs(m - target_mean) > tol:
                continue
            var_err = abs(v_final - target_var)
            if var_err < best_var_err:
                best_var_err = var_err
                best = list(final)
                if var_err < 0.01:
                    break
        if best is None:
            # Fall back: naive transform, accept whatever lands
            stretched = [max(floor, raw_mean + base_scale * (v - raw_mean)) for v in vals]
            offset = target_mean - statistics.mean(stretched)
            best = [max(floor, s + offset) for s in stretched]
        for cid, normalized in zip(cid_order, best):
            out[cid][axis] = normalized
    return out


def _compute_composite(
    axis_scores: dict[str, float | None],
    axis_evidences: dict[str, str | None],
    weights: dict,
) -> tuple[float | None, str | None, list[str]]:
    """Weighted-average composite over the non-null axis scores.

    Null-handling per spec: axes whose score is None are excluded entirely
    (rather than substituted to a floor); the remaining axis_weights are
    rescaled to renormalize. Concepts with all-null axes produce a null
    composite.

    Returns (composite_score, composite_evidence, axes_included).
    """
    included = {
        a: s for a, s in axis_scores.items() if s is not None
    }
    if not included:
        return None, None, []
    rescaled = {}
    for a in included:
        block = weights.get(a) or {}
        rescaled[a] = float(block.get("axis_weight", 1.0))
    norm = sum(rescaled.values())
    if norm == 0:
        return None, None, sorted(included.keys())
    composite = sum(included[a] * rescaled[a] for a in included) / norm
    # Composite evidence: minimum confidence across included axes.
    ranks = [
        CONFIDENCE_RANK[axis_evidences[a]]
        for a in included
        if axis_evidences.get(a)
    ]
    evidence = CONFIDENCE_NAME[min(ranks)] if ranks else None
    return composite, evidence, sorted(included.keys())


def _fmt_score(v: float | None) -> str:
    """Format a score for CSV: 4-decimal float, or empty string for null."""
    return "" if v is None else f"{v:.4f}"


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

    # Pass 1: per-concept axis scores (raw, pre-normalization)
    per_concept_raw: dict[str, dict[str, float | None]] = {}
    per_concept_evidence: dict[str, dict[str, str | None]] = {}
    per_concept_meta: dict[str, dict] = {}
    for fpath in files:
        doc = yaml.safe_load(fpath.read_text())
        meta = doc["_meta"]
        emb_values, emb_conf = _evaluate_concept(doc, weights, schema)
        axis_scores: dict[str, float | None] = {}
        axis_evidences: dict[str, str | None] = {}
        for axis in AXES:
            score, evidence = _score_axis(
                weights.get(axis) or {}, emb_values, emb_conf
            )
            axis_scores[axis] = score
            axis_evidences[axis] = evidence
        per_concept_raw[meta["concept_id"]] = axis_scores
        per_concept_evidence[meta["concept_id"]] = axis_evidences
        per_concept_meta[meta["concept_id"]] = meta

    # Pass 2: corpus-wide normalization for axes that declare a `normalization:`
    # block (currently modularity + upper_cf). Stretches each axis to hit a
    # target mean and variance so the composite isn't dominated by any one axis.
    per_concept_normalized = _normalize_axes(per_concept_raw, weights)

    # Pass 3: composite per concept, from normalized axis scores
    rows: list[dict] = []
    for cid in sorted(per_concept_normalized.keys()):
        meta = per_concept_meta[cid]
        axis_scores = per_concept_normalized[cid]
        axis_evidences = per_concept_evidence[cid]
        row: dict[str, str] = {"concept_id": cid, "name": meta["name"]}
        for axis in AXES:
            row[axis] = _fmt_score(axis_scores.get(axis))
            row[f"{axis}_evidence"] = axis_evidences.get(axis) or ""
        composite, composite_ev, axes_included = _compute_composite(
            axis_scores, axis_evidences, weights
        )
        row["composite"] = _fmt_score(composite)
        row["composite_evidence"] = composite_ev or ""
        row["composite_axes_included"] = json.dumps(axes_included)
        rows.append(row)

    rows.sort(key=lambda r: r["concept_id"])
    scores_dir.mkdir(parents=True, exist_ok=True)
    out = scores_dir / "table.csv"
    fieldnames = [
        "concept_id", "name",
        *AXES,
        "composite",
        *(f"{a}_evidence" for a in AXES),
        "composite_evidence",
        "composite_axes_included",
    ]
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
