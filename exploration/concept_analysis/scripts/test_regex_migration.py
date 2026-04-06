#!/usr/bin/env python3
"""Tests for Phase 2: verify existing parsers still work after migration to shared constants."""

import json
import tempfile
from pathlib import Path

from lib.iteration import parse_verdict_from_feedback
from lib.loop import _extract_model_findings, _split_findings, _get_review_feedback
from lib.sources import parse_proposed_actions


# ---------------------------------------------------------------------------
# parse_verdict_from_feedback (iteration.py)
# ---------------------------------------------------------------------------


class TestParseVerdictFromFeedback:
    def test_pass(self):
        assert parse_verdict_from_feedback("VERDICT: PASS\n") == ("PASS", 0)

    def test_pass_with_trailing_whitespace(self):
        assert parse_verdict_from_feedback("VERDICT: PASS   \n") == ("PASS", 0)

    def test_findings(self):
        text = "VERDICT: FINDINGS\n\n### F-1: X\nstuff\n### F-2: Y\nmore"
        assert parse_verdict_from_feedback(text) == ("FAIL", 2)

    def test_findings_single(self):
        text = "VERDICT: FINDINGS\n\n### F-1: Only one"
        assert parse_verdict_from_feedback(text) == ("FAIL", 1)

    def test_no_verdict(self):
        verdict, count = parse_verdict_from_feedback("No verdict here")
        assert verdict == "FAIL"
        assert count == 0

    def test_pass_ignores_findings(self):
        """PASS verdict with F-N blocks — PASS wins."""
        text = "VERDICT: PASS\n\n### F-1: Stale finding"
        verdict, count = parse_verdict_from_feedback(text)
        assert verdict == "PASS"
        assert count == 1  # finding count is still reported


# ---------------------------------------------------------------------------
# _extract_model_findings (loop.py)
# ---------------------------------------------------------------------------


class TestExtractModelFindings:
    def test_extracts_model_category(self, tmp_path):
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: Analysis issue\n"
            "- **Category:** analysis\n\n"
            "### F-2: Model issue\n"
            "- **Category:** model\n"
        )
        fb = tmp_path / "feedback.md"
        fb.write_text(text)
        result = _extract_model_findings(fb)
        assert "F-2" in result
        assert "F-1" not in result

    def test_no_model_findings(self, tmp_path):
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: Analysis only\n"
            "- **Category:** analysis\n"
        )
        fb = tmp_path / "feedback.md"
        fb.write_text(text)
        result = _extract_model_findings(fb)
        assert result == ""

    def test_missing_file(self):
        result = _extract_model_findings(Path("/nonexistent/feedback.md"))
        assert result == ""

    def test_none_path(self):
        result = _extract_model_findings(None)
        assert result == ""

    def test_colon_inside_bold(self, tmp_path):
        """Real format: **Category:** not **Category**:"""
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: Model fix\n"
            "- **Category:** model\n"
            "- **Finding:** Something\n"
        )
        fb = tmp_path / "feedback.md"
        fb.write_text(text)
        result = _extract_model_findings(fb)
        assert "F-1" in result


# ---------------------------------------------------------------------------
# _split_findings (loop.py)
# ---------------------------------------------------------------------------


class TestSplitFindings:
    def test_splits_correctly(self):
        text = "VERDICT: FINDINGS\n\n### F-1: A\ndetails\n\n### F-2: B\nmore"
        blocks = _split_findings(text)
        assert len(blocks) == 2
        assert blocks[0].startswith("### F-1:")
        assert blocks[1].startswith("### F-2:")

    def test_no_findings(self):
        assert _split_findings("Just some text") == []


# ---------------------------------------------------------------------------
# _get_review_feedback (loop.py)
# ---------------------------------------------------------------------------


class TestGetReviewFeedback:
    def test_revise_with_corrective_actions(self, tmp_path):
        text = (
            "## Assessment\n\nSome review content.\n\n"
            "VERDICT: REVISE\n\n"
            "## Corrective Actions\n\n"
            "### F-1: Fix this\n"
            "- **Category:** analysis\n"
            "- **Finding:** Something broken\n"
        )
        review_path = tmp_path / "review.md"
        review_path.write_text(text)
        result = _get_review_feedback(tmp_path)
        assert result is not None
        assert result.startswith("VERDICT: FINDINGS")
        assert "F-1" in result

    def test_proceed_returns_none(self, tmp_path):
        text = "VERDICT: PROCEED\n\nLooks good."
        (tmp_path / "review.md").write_text(text)
        result = _get_review_feedback(tmp_path)
        assert result is None

    def test_no_review_file(self, tmp_path):
        result = _get_review_feedback(tmp_path)
        assert result is None

    def test_revise_no_corrective_actions(self, tmp_path):
        text = "VERDICT: REVISE\n\nSome text but no corrective actions section."
        (tmp_path / "review.md").write_text(text)
        result = _get_review_feedback(tmp_path)
        assert result is None


# ---------------------------------------------------------------------------
# parse_proposed_actions (sources.py)
# ---------------------------------------------------------------------------


class TestParseProposedActions:
    def test_parses_actions(self, tmp_path):
        text = (
            "## Proposed Actions\n\n"
            "### PA-1: Fix the widget\n"
            "- **Category:** analysis\n"
            "- **Severity:** minor\n"
            "- **Location:** Section 3\n"
            "- **Finding:** Widget is broken\n"
            "- **Proposed Fix:** Replace widget\n"
            "- **Decision:** \n"
            "- **User Notes:** \n\n"
            "### PA-2: Update model\n"
            "- **Category:** model\n"
            "- **Severity:** major\n"
            "- **Location:** model_setup.py\n"
            "- **Finding:** Missing parameter\n"
            "- **Proposed Fix:** Add parameter\n"
            "- **Decision:** \n"
            "- **User Notes:** \n"
        )
        review = tmp_path / "review.md"
        review.write_text(text)
        actions = parse_proposed_actions(review)
        assert len(actions) == 2
        assert actions[0]["id"] == "PA-1"
        assert actions[0]["description"] == "Fix the widget"
        assert actions[0]["category"] == "analysis"
        assert actions[1]["id"] == "PA-2"
