"""Data Availability axis acceptance tests.

DA is a deterministic 1-5 bracket lookup on the design_point.csv row for
each concept (grounding_confidence + primary_sources_count). The score is
computed inline by the rulebook embedding from those two fields; the
populate script writes them into each features YAML and also writes an
informational diagnostic block.
"""
from __future__ import annotations

import csv
from pathlib import Path

import yaml

from exploration.scoring_v2.embeddings.rulebook import (
    _data_availability_score,
    _load_da_brackets,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())
BRACKETS = _load_da_brackets(WEIGHTS)


def _read_actual(run_cli, tmp_scores_dir: Path) -> dict[str, float | None]:
    run_cli("score.py")
    out = {}
    with open(tmp_scores_dir / "table.csv") as f:
        for r in csv.DictReader(f):
            v = r["data_availability"]
            out[r["concept_id"]] = float(v) if v else None
    return out


# ─── Weights surface ─────────────────────────────────────────────────────


class TestWeightsSurface:
    def test_axis_exists(self):
        assert "data_availability" in WEIGHTS

    def test_brackets_present(self):
        for key in (
            "missing", "low", "medium",
            "high_without_sources", "high_with_sources",
            "high_sources_threshold",
        ):
            assert key in BRACKETS, f"missing bracket key {key!r}"

    def test_bracket_values_monotone(self):
        assert (
            BRACKETS["missing"]
            < BRACKETS["low"]
            < BRACKETS["medium"]
            < BRACKETS["high_without_sources"]
            < BRACKETS["high_with_sources"]
        )

    def test_axis_weight_default(self):
        assert WEIGHTS["data_availability"]["axis_weight"] == 1.0
        ew = WEIGHTS["data_availability"]["embedding_weights"]
        assert ew == {"data_availability_score": 1.0}


# ─── Embedding behavior ──────────────────────────────────────────────────


class TestScoreLookup:
    def _score(self, gc, n):
        return _data_availability_score(gc, n, weights_yaml=WEIGHTS)

    def test_missing_concept_floors_to_one(self):
        assert self._score(None, None) == 1.0
        assert self._score("", 0) == 1.0

    def test_low_confidence(self):
        assert self._score("low", 0) == 2.0
        assert self._score("low", 5) == 2.0

    def test_medium_confidence(self):
        assert self._score("medium", 0) == 3.0
        assert self._score("medium", 10) == 3.0

    def test_high_confidence_below_threshold(self):
        threshold = BRACKETS["high_sources_threshold"]
        assert self._score("high", 0) == BRACKETS["high_without_sources"]
        assert self._score("high", threshold - 1) == BRACKETS["high_without_sources"]

    def test_high_confidence_at_or_above_threshold(self):
        threshold = BRACKETS["high_sources_threshold"]
        assert self._score("high", threshold) == BRACKETS["high_with_sources"]
        assert self._score("high", threshold + 5) == BRACKETS["high_with_sources"]

    def test_case_insensitive_confidence(self):
        assert self._score("HIGH", 5) == BRACKETS["high_with_sources"]
        assert self._score("  Low  ", 0) == 2.0

    def test_unknown_confidence_floors(self):
        assert self._score("unknown", 5) == 1.0


# ─── CSV ↔ feature alignment ────────────────────────────────────────────


class TestCsvAlignment:
    """The populate script should mirror every row in design_point.csv
    into the per-concept feature YAML. Concepts absent from the CSV
    should have the manual fields omitted entirely (floors to 1.0)."""

    def _csv_rows(self) -> dict[str, dict[str, str]]:
        path = REPO_ROOT / "exploration" / "concept_analysis" / "tables" / "design_point.csv"
        with path.open(encoding="utf-8") as f:
            return {r["concept_id"]: r for r in csv.DictReader(f)}

    def test_csv_exists_and_has_rows(self):
        rows = self._csv_rows()
        assert len(rows) > 20, "design_point.csv should cover most concepts"

    def test_csv_row_count_consistent_with_populate_script_floor(self):
        """The populate script logs how many concepts floor at 1.0.
        Manual sanity: there shouldn't be more than half the corpus."""
        csv_count = len(self._csv_rows())
        # 40 concepts in features/; allow up to half to be missing.
        assert csv_count >= 20
