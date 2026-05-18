"""Taxonomy extractor: reads exploration/concept_analysis/table.csv."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

# table.csv path is resolvable from repo root.
ROOT = Path(__file__).resolve().parents[4]
TAXONOMY_CSV = ROOT / "exploration" / "concept_analysis" / "table.csv"

_cache: dict[str, dict[str, str]] | None = None


def _load(csv_path: Path | str = TAXONOMY_CSV) -> dict[str, dict[str, str]]:
    global _cache
    if _cache is not None:
        return _cache
    rows: dict[str, dict[str, str]] = {}
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            cid = row["ID"].strip()
            if cid:
                rows[cid] = row
    _cache = rows
    return rows


def all_concept_ids(csv_path: Path | str = TAXONOMY_CSV) -> list[str]:
    return sorted(_load(csv_path).keys())


def concept_name(concept_id: str, csv_path: Path | str = TAXONOMY_CSV) -> str:
    return _load(csv_path)[concept_id]["Concept Name"]


def extract(
    concept_id: str, feature_name: str, schema_entry: dict[str, Any]
) -> tuple[Any, str, str]:
    rows = _load()
    if concept_id not in rows:
        raise KeyError(f"concept {concept_id!r} not present in {TAXONOMY_CSV.name}")
    column = schema_entry.get("taxonomy_column")
    if not column:
        raise ValueError(
            f"feature {feature_name!r}: taxonomy extractor requires "
            f"'taxonomy_column' in schema entry"
        )
    value = rows[concept_id].get(column, "").strip()
    return value, "taxonomy", "high"
