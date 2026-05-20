"""Populate gap_report_path manual feature + data_availability_diagnostics
block for every concept. Idempotent.

Auto-detects the gap report at
    exploration/concept_analysis/analyses/{concept_id}/gap_report.md
and populates gap_report_path as a repo-relative path. Concepts without
a gap report get gap_report_path = null and score the data_availability
axis null (composite skips them).

Usage:
    uv run python exploration/scoring_v2/scripts/populate_data_availability.py
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io
from exploration.scoring_v2.lib.extractors import taxonomy as taxonomy_ext
from exploration.scoring_v2.embeddings import rulebook  # noqa: F401
from exploration.scoring_v2.embeddings.rulebook import (
    _count_blocking_markers,
    _da_score_from_count,
    _load_da_weights,
)

WEIGHTS_PATH = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"
ANALYSES_DIR = REPO_ROOT / "exploration" / "concept_analysis" / "analyses"


def _gap_report_relpath(concept_id: str) -> str | None:
    """Return the repo-relative path to the gap report if it exists."""
    candidate = ANALYSES_DIR / concept_id / "gap_report.md"
    if candidate.exists():
        return str(candidate.relative_to(REPO_ROOT)).replace("\\", "/")
    return None


def main() -> int:
    weights = yaml.safe_load(WEIGHTS_PATH.read_text())
    brackets, floor = _load_da_weights(weights)
    today = _dt.date.today().isoformat()
    ids = taxonomy_ext.all_concept_ids()
    populated = 0
    missing = []
    for cid in ids:
        doc = feature_io.read_features(cid)
        doc["_meta"] = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        relpath = _gap_report_relpath(cid)
        # 1) gap_report_path manual block (null if no report)
        if relpath is None:
            missing.append(cid)
            existing_path = doc.get("gap_report_path")
            if existing_path is not None and existing_path.get("value") is not None:
                doc.pop("gap_report_path", None)
        else:
            doc["gap_report_path"] = {
                "value": relpath,
                "provenance": "auto-detected",
                "confidence": "high",
                "extracted_at": today,
            }
        # 2) diagnostic block
        if relpath is None:
            block = {
                "gap_report_path": None,
                "report_exists": False,
                "blocking_count": None,
                "data_availability_score": None,
            }
        else:
            abs_path = REPO_ROOT / relpath
            try:
                text = abs_path.read_text(encoding="utf-8")
                count = _count_blocking_markers(text)
                score = _da_score_from_count(count, brackets, floor)
            except (OSError, UnicodeDecodeError):
                count = None
                score = None
            block = {
                "gap_report_path": relpath,
                "report_exists": True,
                "blocking_count": count,
                "data_availability_score": score,
            }
        existing = doc.get("data_availability_diagnostics") or {}
        existing_no_ts = {k: v for k, v in existing.items() if k != "extracted_at"}
        if existing_no_ts != block:
            doc["data_availability_diagnostics"] = dict(block, extracted_at=today)
            populated += 1
        feature_io.write_features(cid, doc)
    print(f"populated/updated gap_report_path + diagnostics for "
          f"{populated} of {len(ids)} concepts; "
          f"{len(missing)} concept(s) without gap_report.md: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
