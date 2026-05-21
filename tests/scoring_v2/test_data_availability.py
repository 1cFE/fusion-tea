"""Data Availability axis acceptance tests."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2.embeddings.rulebook import (
    _BLOCKING_MARKER,
    _count_blocking_markers,
    _structured_blocking_count,
    _da_score_from_count,
    _load_da_weights,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
PREDICTED = REPO_ROOT / "tests" / "scoring_v2" / "predicted_scores.yaml"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())
BRACKETS, FLOOR = _load_da_weights(WEIGHTS)

PER_CONCEPT_TOLERANCE = 0.55

# Empty since the gap-report format standardization: every report now
# carries a `## Structured summary` block, blocking_count is the
# deduplicated structured count, and predicted_scores.yaml's
# data_availability column was regenerated from those structured blocks
# — so predicted == actual for this axis by construction.
KNOWN_DRIFTS: dict[str, str] = {}


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
        assert BRACKETS
        assert all("max_count" in b and "score" in b for b in BRACKETS)

    def test_floor_score(self):
        assert FLOOR == 1.0


# ─── Counting + bucket schedule ──────────────────────────────────────────


class TestCounting:
    def test_count_zero(self):
        assert _count_blocking_markers("nothing here") == 0

    def test_count_one(self):
        assert _count_blocking_markers("**blocking**") == 1

    def test_count_case_insensitive(self):
        assert _count_blocking_markers("**Blocking**") == 1
        assert _count_blocking_markers("**BLOCKING**") == 1

    def test_count_multiple(self):
        text = "foo **blocking** bar **blocking** baz"
        assert _count_blocking_markers(text) == 2

    def test_important_not_counted(self):
        assert _count_blocking_markers("**important** **blocking**") == 1


class TestStructuredSummaryCount:
    """The structured `## Structured summary` block is the authoritative
    blocking-count source; the prose regex is only the legacy fallback."""

    def test_parses_blocking_count_field(self):
        text = (
            "# Gap Assessment\n\n## Structured summary (machine-readable)\n\n"
            "```yaml\noverall_rating: \"Mostly Ready\"\n"
            "blocking_count: 4\nimportant_count: 7\n```\n"
        )
        assert _structured_blocking_count(text) == 4

    def test_returns_none_when_no_block(self):
        text = "# Gap Assessment\n\nSome prose with **blocking** markers.\n"
        assert _structured_blocking_count(text) is None

    def test_structured_block_overrides_prose_regex(self):
        """A report whose prose has many **blocking** bolds but whose
        structured block says 4 must count as 4 (the dedup fix)."""
        text = (
            "**blocking** **blocking** **blocking** **blocking** "
            "**blocking** **blocking**\n\n"
            "## Structured summary (machine-readable)\n\n"
            "```yaml\nblocking_count: 4\n```\n"
        )
        # prose regex would say 6; structured says 4
        assert _count_blocking_markers(text) == 6
        assert _structured_blocking_count(text) == 4

    def test_every_gap_report_has_a_structured_block(self):
        """After the format-standardization pass, every gap_report.md
        carries a structured block with a blocking_count."""
        analyses = REPO_ROOT / "exploration" / "concept_analysis" / "analyses"
        reports = sorted(analyses.glob("*/gap_report.md"))
        assert reports, "no gap reports found"
        missing = []
        for path in reports:
            if _structured_blocking_count(path.read_text(encoding="utf-8")) is None:
                missing.append(path.parent.name)
        assert not missing, (
            f"gap reports without a structured-summary block: {missing}"
        )


class TestBucketSchedule:
    def test_zero_blockers_top_score(self):
        assert _da_score_from_count(0, BRACKETS, FLOOR) == 5.0

    def test_two_blockers(self):
        assert _da_score_from_count(2, BRACKETS, FLOOR) == 4.0

    def test_five_blockers(self):
        assert _da_score_from_count(5, BRACKETS, FLOOR) == 3.0

    def test_nine_blockers(self):
        assert _da_score_from_count(9, BRACKETS, FLOOR) == 2.0

    def test_ten_blockers_floor(self):
        assert _da_score_from_count(10, BRACKETS, FLOOR) == 1.0
        assert _da_score_from_count(50, BRACKETS, FLOOR) == 1.0


# ─── Score invariants ────────────────────────────────────────────────────


class TestScoreInvariants:
    def test_all_in_band_or_null(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        for cid, v in scores.items():
            if v is None:
                continue
            assert 1.0 <= v <= 5.0, f"{cid}: {v}"

    def test_all_40_concepts_have_gap_reports(self, run_cli, tmp_scores_dir: Path):
        """As of the gap-report-stub work, all 40 concepts have a
        gap_report.md (37/38/39 — Mallory's net-new concepts — got
        stub reports). No concept should score null on this axis."""
        scores = _read_actual(run_cli, tmp_scores_dir)
        nulls = [cid for cid, v in scores.items() if v is None]
        assert not nulls, f"concepts still missing a gap report: {nulls}"


class TestNullHandling:
    """The null-handling path is no longer exercised by any live concept
    (all 40 have reports), so it's pinned at the unit level here. R9 in
    spec.md: a missing gap report yields a null score, not a floor."""

    def test_score_embedding_returns_none_for_none_count(self):
        from exploration.scoring_v2.embeddings.rulebook import (  # noqa: PLC0415
            _data_availability_score,
        )
        assert _data_availability_score(None, weights_yaml=WEIGHTS) is None

    def test_count_embedding_returns_none_for_empty_path(self):
        from exploration.scoring_v2.embeddings.rulebook import (  # noqa: PLC0415
            _gap_report_blocking_count,
        )
        assert _gap_report_blocking_count("") is None
        assert _gap_report_blocking_count(None) is None

    def test_count_embedding_returns_none_for_missing_file(self):
        from exploration.scoring_v2.embeddings.rulebook import (  # noqa: PLC0415
            _gap_report_blocking_count,
        )
        assert _gap_report_blocking_count(
            "exploration/concept_analysis/analyses/__no_such_concept__/gap_report.md"
        ) is None


def test_predicted_scores_match_exactly(run_cli, tmp_scores_dir: Path):
    """predicted_scores.yaml's data_availability column is regenerated
    from the gap reports' structured blocks, so it must match the
    framework's computed scores exactly — this axis has no calibration
    gap, only a deterministic count."""
    predicted = yaml.safe_load(PREDICTED.read_text()).get("data_availability", {})
    actual = _read_actual(run_cli, tmp_scores_dir)
    mismatches = []
    for cid, exp in predicted.items():
        v = actual.get(cid)
        if exp is None:
            continue
        if v is None or abs(v - float(exp)) > 1e-9:
            mismatches.append(f"{cid}: predicted {exp} vs actual {v}")
    assert not mismatches, (
        "data_availability predicted != actual (re-run "
        "add_gap_report_summary_blocks.py + score.py and refresh "
        "predicted_scores.yaml):\n  " + "\n  ".join(mismatches)
    )
