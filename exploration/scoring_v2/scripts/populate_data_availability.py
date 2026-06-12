"""Populate the Data Availability feature blocks from
`exploration/concept_analysis/tables/design_point.csv`.

For each concept this writes:
  * `design_point_grounding_confidence` — manual feature (low/medium/high or null)
  * `design_point_primary_sources_count` — manual feature (int or null)
  * `data_availability_diagnostics`     — informational block

Concepts that are absent from the CSV get null fields; the scoring embedding
floors them to score 1.0 ("no documented design point").

Bracket (defined in weights/default.yaml, applied by the embedding):
  * not in CSV                          -> 1.0
  * grounding_confidence = low          -> 2.0
  * grounding_confidence = medium       -> 3.0
  * grounding_confidence = high, n<3    -> 4.0
  * grounding_confidence = high, n>=3   -> 5.0

Refresh workflow: when a new primary source lands in
`knowledge/concept_research/{cid}/iter-NN/sources/`, re-run the LLM proposer
(see exploration/concept_analysis/scripts/ingest_design_point_proposals.py)
for that concept, then re-run this script.

Usage:
    uv run python exploration/scoring_v2/scripts/populate_data_availability.py
"""
from __future__ import annotations

import csv
import datetime as _dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io  # noqa: E402
from exploration.scoring_v2.lib.extractors import taxonomy as taxonomy_ext  # noqa: E402

CSV_PATH = REPO_ROOT / "exploration" / "concept_analysis" / "tables" / "design_point.csv"


def _count_primary_sources(raw: str) -> int:
    """Count primary sources in the `; `-separated field. Robust to commas."""
    if not raw:
        return 0
    # Normalize ", " to "; " then split — CSV authors have used both.
    normalized = raw.replace(", ", "; ")
    return sum(1 for s in normalized.split("; ") if s.strip())


def _load_csv() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with CSV_PATH.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["concept_id"].strip()
            if not cid:
                continue
            rows[cid] = {
                "grounding_confidence": (row.get("grounding_confidence") or "").strip().lower() or None,
                "primary_sources_count": _count_primary_sources(row.get("primary_sources", "")),
                "design_name": row.get("design_name", "").strip(),
                "verified_by": (row.get("verified_by") or "").strip() or None,
            }
    return rows


def main() -> int:
    rows = _load_csv()
    today = _dt.date.today().isoformat()
    ids = taxonomy_ext.all_concept_ids()
    populated = 0
    missing: list[str] = []
    for cid in ids:
        doc = feature_io.read_features(cid)
        doc["_meta"] = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        row = rows.get(cid)
        if row is None:
            missing.append(cid)
            gc_value = None
            n_sources = None
            design_name = None
            in_csv = False
            verified_by = None
        else:
            gc_value = row["grounding_confidence"]
            n_sources = row["primary_sources_count"]
            design_name = row["design_name"]
            in_csv = True
            verified_by = row["verified_by"]

        # Manual feature blocks — referenced by the rulebook embedding.
        if gc_value is not None:
            doc["design_point_grounding_confidence"] = {
                "value": gc_value,
                "provenance": "exploration/concept_analysis/tables/design_point.csv",
                "confidence": "high",
                "extracted_at": today,
            }
        else:
            doc.pop("design_point_grounding_confidence", None)

        if n_sources is not None:
            doc["design_point_primary_sources_count"] = {
                "value": n_sources,
                "provenance": "exploration/concept_analysis/tables/design_point.csv",
                "confidence": "high",
                "extracted_at": today,
            }
        else:
            doc.pop("design_point_primary_sources_count", None)

        # Informational diagnostic block (mirrors the old gap_report shape).
        block: dict = {
            "source_csv": "exploration/concept_analysis/tables/design_point.csv",
            "in_csv": in_csv,
            "design_name": design_name,
            "grounding_confidence": gc_value,
            "primary_sources_count": n_sources,
            "verified_by": verified_by,
        }
        # Pre-compute the score for the diagnostic block (mirrors how the
        # embedding will score it — purely informational; the embedding is the
        # source of truth for the composite).
        block["data_availability_score"] = _score(gc_value, n_sources)

        existing = doc.get("data_availability_diagnostics") or {}
        existing_no_ts = {k: v for k, v in existing.items() if k != "extracted_at"}
        if existing_no_ts != block:
            doc["data_availability_diagnostics"] = dict(block, extracted_at=today)
            populated += 1

        # Legacy gap_report_path block — drop it; embedding no longer reads it.
        doc.pop("gap_report_path", None)

        feature_io.write_features(cid, doc)

    print(f"populated/updated design-point DA blocks for "
          f"{populated} of {len(ids)} concepts; "
          f"{len(missing)} concept(s) not in design_point.csv (score 1.0 floor): "
          f"{missing}")
    return 0


def _score(gc: str | None, n: int | None) -> float:
    if gc is None:
        return 1.0
    if gc == "low":
        return 2.0
    if gc == "medium":
        return 3.0
    if gc == "high":
        if (n or 0) >= 3:
            return 5.0
        return 4.0
    return 1.0


if __name__ == "__main__":
    raise SystemExit(main())
