"""Ingest design-point proposals into the project tables.

For each `*.proposal.yaml` in `.project/completed/20260821_concept-rework-tables/proposals/`:
- Validate the YAML schema against the spec.
- Copy the trace.md and proposal.yaml into the per-concept analysis directory at
  `exploration/concept_analysis/analyses/{cid}/design-points/baseline.{md,yaml}`.
- Write/update a row in `exploration/concept_analysis/tables/design_point.csv`.

The proposals working area is preserved for audit — this script reads, never deletes.

Handles two YAML shapes:
- Standard `proposal` with a design-point selection.
- Special-case `proposal: {route_to_freeform: true, ...}` which logs the routing
  but does not emit a CSV row (the concept is freeform-deferred, like fit_grade=None).

Validation is non-fatal per row: a malformed proposal is reported and skipped, the rest
continue. The script exits non-zero if any row failed validation.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2].parent
PROPOSALS_DIR = ROOT / ".project/completed/20260821_concept-rework-tables/proposals"
ANALYSES_DIR = ROOT / "exploration/concept_analysis/analyses"
DESIGN_POINT_CSV = ROOT / "exploration/concept_analysis/tables/design_point.csv"
FREEFORM_LOG = ROOT / "exploration/concept_analysis/tables/design_point_freeform_routes.md"

CSV_COLUMNS = [
    "concept_id",
    "design_name",
    "maturity_tier",
    "grounding_confidence",
    "p_native_mwe",
    "primary_sources",
    "selection_rationale",
    "alternatives_considered",
    "trace_path",
    "proposal_model",
    "verified_by",
    "verified_date",
]

MATURITY_TIERS = {"paper-concept", "pilot-demonstrator", "proposed-commercial"}
GROUNDING_CONFIDENCE = {"high", "medium", "low"}


class ValidationError(Exception):
    pass


def validate_proposal(p: dict, cid: str) -> None:
    """Raise ValidationError if the proposal payload is malformed."""
    if not isinstance(p, dict):
        raise ValidationError(f"`proposal` is not a mapping (got {type(p).__name__})")

    if p.get("route_to_freeform"):
        # Freeform shape: just needs `reason` and `designs_considered`.
        if not p.get("reason"):
            raise ValidationError("freeform proposal missing `reason`")
        return

    required = ["concept_id", "design_name", "maturity_tier", "grounding_confidence", "p_native_mwe", "primary_sources", "selection_rationale", "alternatives_considered"]
    missing = [k for k in required if k not in p]
    if missing:
        raise ValidationError(f"missing required fields: {missing}")

    if p["concept_id"] != cid:
        raise ValidationError(f"YAML concept_id {p['concept_id']!r} does not match filename {cid!r}")

    if p["maturity_tier"] not in MATURITY_TIERS:
        raise ValidationError(f"maturity_tier {p['maturity_tier']!r} not in {MATURITY_TIERS}")

    if p["grounding_confidence"] not in GROUNDING_CONFIDENCE:
        raise ValidationError(f"grounding_confidence {p['grounding_confidence']!r} not in {GROUNDING_CONFIDENCE}")

    if not isinstance(p["p_native_mwe"], (int, float)) or p["p_native_mwe"] <= 0:
        raise ValidationError(f"p_native_mwe must be a positive number (got {p['p_native_mwe']!r})")

    if not isinstance(p["primary_sources"], list) or len(p["primary_sources"]) < 2:
        raise ValidationError(f"primary_sources must have >= 2 entries (got {len(p.get('primary_sources') or [])})")

    if not isinstance(p["alternatives_considered"], list):
        raise ValidationError("alternatives_considered must be a list")

    for i, alt in enumerate(p["alternatives_considered"]):
        if not isinstance(alt, dict) or not alt.get("design"):
            raise ValidationError(f"alternatives_considered[{i}] missing `design`")
        if "reason_rejected" not in alt:
            raise ValidationError(f"alternatives_considered[{i}] missing `reason_rejected`")


def flatten_alternatives(alts: list[dict]) -> str:
    return "; ".join(a["design"] for a in alts)


def flatten_sources(srcs: list[str]) -> str:
    return "; ".join(srcs)


def one_sentence(rationale: str) -> str:
    """Extract a CSV-friendly excerpt from the rationale block.

    The full prose lives in `baseline.md`; this column is a search-friendly hint
    for grep / spreadsheet pivots. Take the first paragraph (or whole thing if
    no paragraph break), normalize whitespace, cap at 280 chars.
    """
    first_para = rationale.split("\n\n", 1)[0]
    text = " ".join(first_para.split())
    if len(text) <= 280:
        return text
    return text[:277] + "..."


def install_trace(cid: str, yaml_path: Path, trace_path: Path) -> Path:
    """Copy the trace + yaml into analyses/{cid}/design-points/. Return the trace target path."""
    dest_dir = ANALYSES_DIR / cid / "design-points"
    dest_dir.mkdir(parents=True, exist_ok=True)
    md_target = dest_dir / "baseline.md"
    yaml_target = dest_dir / "baseline.yaml"
    shutil.copy2(trace_path, md_target)
    shutil.copy2(yaml_path, yaml_target)
    return md_target


def ingest_one(cid: str, model: str) -> tuple[str, dict | None, str | None]:
    """Process one proposal. Returns (status, row_or_none, error_or_none).

    status ∈ {"ingested", "freeform", "error"}.
    """
    yaml_path = PROPOSALS_DIR / f"{cid}.proposal.yaml"
    trace_path = PROPOSALS_DIR / f"{cid}.trace.md"

    if not yaml_path.exists() or not trace_path.exists():
        return "error", None, f"missing trace.md or proposal.yaml for {cid}"

    try:
        data = yaml.safe_load(yaml_path.read_text())
    except yaml.YAMLError as e:
        return "error", None, f"YAML parse error: {e}"

    if not isinstance(data, dict) or "proposal" not in data:
        return "error", None, "top-level must be a mapping with a `proposal` key"

    p = data["proposal"]
    try:
        validate_proposal(p, cid)
    except ValidationError as e:
        return "error", None, str(e)

    if p.get("route_to_freeform"):
        designs = p.get("designs_considered", [])
        designs_str = "; ".join(d.get("design", "?") for d in designs) or "(none listed)"
        return "freeform", {"reason": p["reason"], "designs": designs_str}, None

    # Standard proposal: install trace + emit CSV row.
    md_target = install_trace(cid, yaml_path, trace_path)
    trace_rel = md_target.relative_to(ROOT).as_posix()

    row = {
        "concept_id": cid,
        "design_name": p["design_name"],
        "maturity_tier": p["maturity_tier"],
        "grounding_confidence": p["grounding_confidence"],
        "p_native_mwe": p["p_native_mwe"],
        "primary_sources": flatten_sources(p["primary_sources"]),
        "selection_rationale": one_sentence(p["selection_rationale"]),
        "alternatives_considered": flatten_alternatives(p["alternatives_considered"]),
        "trace_path": trace_rel,
        "proposal_model": model,
        "verified_by": "",
        "verified_date": "",
    }
    return "ingested", row, None


def write_csv(rows: list[dict], merge: bool) -> None:
    """Write rows to design_point.csv.

    If merge=True and the CSV exists, preserve existing rows for concepts not in
    the new batch (rows for matching concept_ids are replaced). This preserves
    verified_by / verified_date on rows already gated.
    """
    DESIGN_POINT_CSV.parent.mkdir(parents=True, exist_ok=True)
    by_id = {r["concept_id"]: r for r in rows}
    if merge and DESIGN_POINT_CSV.exists():
        with DESIGN_POINT_CSV.open() as f:
            for existing in csv.DictReader(f):
                if existing["concept_id"] not in by_id:
                    by_id[existing["concept_id"]] = existing
    merged = sorted(by_id.values(), key=lambda r: r["concept_id"])
    with DESIGN_POINT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        w.writerows(merged)


def append_freeform_log(routes: list[tuple[str, dict]]) -> None:
    if not routes:
        return
    today = date.today().isoformat()
    lines = [f"# Freeform Routes — Design-Point Proposals\n",
             f"_Auto-appended by `ingest_design_point_proposals.py` on {today}._\n"]
    for cid, info in sorted(routes):
        lines.append(f"\n## {cid}\n")
        lines.append(f"- **Reason**: {info['reason']}\n")
        lines.append(f"- **Designs considered**: {info['designs']}\n")
    FREEFORM_LOG.write_text("".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sonnet", help="model attribution for proposal_model column")
    parser.add_argument("--only", nargs="*", help="restrict to these concept_ids (default: all proposals/*.proposal.yaml)")
    args = parser.parse_args()

    if args.only:
        cids = args.only
    else:
        cids = sorted(p.stem.replace(".proposal", "") for p in PROPOSALS_DIR.glob("*.proposal.yaml"))

    print(f"Ingesting {len(cids)} proposals...")
    rows, freeform, errors = [], [], []
    for cid in cids:
        status, payload, err = ingest_one(cid, args.model)
        if status == "ingested":
            rows.append(payload)
            print(f"  ✓ {cid}: ingested → {payload['trace_path']}")
        elif status == "freeform":
            freeform.append((cid, payload))
            print(f"  ↦ {cid}: routed to freeform")
        else:
            errors.append((cid, err))
            print(f"  ✗ {cid}: {err}")

    if rows:
        write_csv(rows, merge=bool(args.only))
        print(f"\nWrote {len(rows)} rows to {DESIGN_POINT_CSV.relative_to(ROOT)} ({'merged' if args.only else 'full overwrite'})")
    if freeform:
        append_freeform_log(freeform)
        print(f"Logged {len(freeform)} freeform routes to {FREEFORM_LOG.relative_to(ROOT)}")
    if errors:
        print(f"\n{len(errors)} errors:")
        for cid, e in errors:
            print(f"  {cid}: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
