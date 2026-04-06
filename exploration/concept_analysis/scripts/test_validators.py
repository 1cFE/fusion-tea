#!/usr/bin/env python3
"""Tests for lib/validators.py — shared regex constants and output validators."""

import re
from pathlib import Path

from lib.validators import (
    CORRECTIVE_ACTIONS_RE,
    FEEDBACK_VERDICT_RE,
    FINDING_CATEGORY_RE,
    FINDING_HEADER_RE,
    PROPOSED_ACTION_RE,
    REVIEW_VERDICT_RE,
    ValidationResult,
    validate_feedback_verdict,
    validate_review_verdict,
)

# ---------------------------------------------------------------------------
# Shared regex constant tests
# ---------------------------------------------------------------------------


class TestFeedbackVerdictRE:
    def test_pass(self):
        assert FEEDBACK_VERDICT_RE.search("VERDICT: PASS\n")

    def test_findings(self):
        assert FEEDBACK_VERDICT_RE.search("VERDICT: FINDINGS\n")

    def test_extracts_group(self):
        m = FEEDBACK_VERDICT_RE.search("VERDICT: PASS\n")
        assert m.group(1) == "PASS"

    def test_rejects_unknown_verdict(self):
        assert not FEEDBACK_VERDICT_RE.search("VERDICT: MAYBE\n")

    def test_rejects_trailing_text(self):
        assert not FEEDBACK_VERDICT_RE.search("VERDICT: PASS — all goals met\n")

    def test_allows_trailing_whitespace(self):
        assert FEEDBACK_VERDICT_RE.search("VERDICT: PASS   \n")

    def test_multiline(self):
        text = "Some preamble\nVERDICT: FINDINGS\n\n### F-1: stuff"
        m = FEEDBACK_VERDICT_RE.search(text)
        assert m and m.group(1) == "FINDINGS"

    def test_indented_does_not_match(self):
        assert not FEEDBACK_VERDICT_RE.search("  VERDICT: PASS\n")


class TestFindingHeaderRE:
    def test_simple(self):
        assert FINDING_HEADER_RE.search("### F-1: Title here")

    def test_multi_digit(self):
        assert FINDING_HEADER_RE.search("### F-12: Title")

    def test_findall(self):
        text = "### F-1: A\nstuff\n### F-2: B\nmore"
        assert len(FINDING_HEADER_RE.findall(text)) == 2


class TestFindingCategoryRE:
    def test_analysis(self):
        m = FINDING_CATEGORY_RE.search("- **Category:** analysis")
        assert m and m.group(1) == "analysis"

    def test_model(self):
        m = FINDING_CATEGORY_RE.search("- **Category:** model")
        assert m and m.group(1) == "model"

    def test_bold_with_colon_inside(self):
        # Variant: **Category**: (colon outside bold)
        m = FINDING_CATEGORY_RE.search("- **Category**: model")
        assert m and m.group(1) == "model"


class TestReviewVerdictRE:
    def test_proceed(self):
        m = REVIEW_VERDICT_RE.search("VERDICT: PROCEED\n")
        assert m and m.group(1) == "PROCEED"

    def test_revise(self):
        m = REVIEW_VERDICT_RE.search("VERDICT: REVISE\n")
        assert m and m.group(1) == "REVISE"

    def test_rejects_pass(self):
        assert not REVIEW_VERDICT_RE.search("VERDICT: PASS\n")

    def test_rejects_trailing_text(self):
        assert not REVIEW_VERDICT_RE.search("VERDICT: PROCEED with caution\n")


class TestCorrectiveActionsRE:
    def test_matches(self):
        assert CORRECTIVE_ACTIONS_RE.search("## Corrective Actions\n")

    def test_with_content_after(self):
        assert CORRECTIVE_ACTIONS_RE.search("## Corrective Actions\n\n### F-1:")


class TestProposedActionRE:
    def test_matches(self):
        m = PROPOSED_ACTION_RE.search("### PA-1: Fix the thing")
        assert m and m.group(1) == "PA-1" and m.group(2) == "Fix the thing"

    def test_multi_digit(self):
        m = PROPOSED_ACTION_RE.search("### PA-12: Another fix")
        assert m and m.group(1) == "PA-12"


# ---------------------------------------------------------------------------
# validate_feedback_verdict tests
# ---------------------------------------------------------------------------


class TestValidateFeedbackVerdict:
    def test_pass(self):
        result = validate_feedback_verdict("VERDICT: PASS\n")
        assert result.valid is True

    def test_findings_with_category(self):
        text = (
            "VERDICT: FINDINGS\n\n"
            "---\n\n"
            "### F-1: Title\n"
            "- **Category:** model\n"
            "- **Finding:** Something\n"
        )
        result = validate_feedback_verdict(text)
        assert result.valid is True

    def test_findings_multiple_with_categories(self):
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: First\n"
            "- **Category:** analysis\n\n"
            "### F-2: Second\n"
            "- **Category:** model\n"
        )
        result = validate_feedback_verdict(text)
        assert result.valid is True

    def test_missing_verdict(self):
        result = validate_feedback_verdict("Some analysis without a verdict line")
        assert result.valid is False
        assert result.fix_message is not None
        assert "VERDICT" in result.fix_message

    def test_findings_no_blocks(self):
        text = "VERDICT: FINDINGS\n\nSome prose but no ### F-N headers"
        result = validate_feedback_verdict(text)
        assert result.valid is False
        assert "F-N" in result.fix_message or "### F-" in result.fix_message

    def test_findings_missing_category(self):
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: Title\n"
            "- **Target:** Section 2\n"
            "- **Finding:** Something\n"
        )
        result = validate_feedback_verdict(text)
        assert result.valid is False
        assert "Category" in result.fix_message

    def test_findings_partial_category(self):
        """One finding has Category, another doesn't."""
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: Good\n"
            "- **Category:** analysis\n\n"
            "### F-2: Bad\n"
            "- **Target:** Section 3\n"
        )
        result = validate_feedback_verdict(text)
        assert result.valid is False
        assert "F-2" in result.fix_message

    def test_verdict_with_trailing_text_rejected(self):
        text = "VERDICT: PASS — all goals met\n"
        result = validate_feedback_verdict(text)
        assert result.valid is False

    def test_multiple_verdict_lines_first_wins(self):
        """If text has multiple verdict lines, the first match is used."""
        text = (
            "VERDICT: PASS\n\n"
            "VERDICT: FINDINGS\n\n"
            "### F-1: Oops\n"
            "- **Category:** analysis\n"
        )
        result = validate_feedback_verdict(text)
        assert result.valid is True  # PASS is the first match


class TestValidateFeedbackVerdictRealFiles:
    """Test against real pipeline output files on disk.

    Only checks files that have a VERDICT line — older files may predate
    the current format (no Category fields).
    """

    def _find_feedback_files(self):
        analyses = Path(__file__).parent.parent / "analyses"
        return list(analyses.glob("*/iter-*/feedback.md"))

    def test_real_feedback_files_with_categories_pass(self):
        files = self._find_feedback_files()
        if not files:
            return
        tested = 0
        for f in files:
            text = f.read_text(encoding="utf-8")
            # Only test files that have Category fields (current format)
            if not FINDING_CATEGORY_RE.search(text):
                continue
            result = validate_feedback_verdict(text)
            assert result.valid, f"{f}: {result.details}"
            tested += 1
            if tested >= 5:
                break


# ---------------------------------------------------------------------------
# validate_review_verdict tests
# ---------------------------------------------------------------------------


class TestValidateReviewVerdict:
    def test_proceed(self):
        text = "## Verdict\n\nVERDICT: PROCEED\n\nLooks good."
        result = validate_review_verdict(text)
        assert result.valid is True

    def test_proceed_with_pa_blocks(self):
        text = (
            "VERDICT: PROCEED\n\n"
            "### PA-1: Minor fix\n"
            "- **Category:** analysis\n"
        )
        result = validate_review_verdict(text)
        assert result.valid is True

    def test_revise_with_corrective_actions(self):
        text = (
            "Review content\n\n"
            "VERDICT: REVISE\n\n"
            "## Corrective Actions\n\n"
            "### F-1: Fix this\n"
            "- **Category:** analysis\n"
        )
        result = validate_review_verdict(text)
        assert result.valid is True

    def test_missing_verdict(self):
        result = validate_review_verdict("Review content without verdict")
        assert result.valid is False
        assert result.fix_message is not None

    def test_revise_no_corrective_actions(self):
        text = "VERDICT: REVISE\n\nSome text but no ## Corrective Actions"
        result = validate_review_verdict(text)
        assert result.valid is False
        assert "Corrective Actions" in result.fix_message

    def test_revise_empty_corrective_actions(self):
        text = (
            "VERDICT: REVISE\n\n"
            "## Corrective Actions\n\n"
            "## Next Section\n"
        )
        result = validate_review_verdict(text)
        assert result.valid is False

    def test_revise_corrective_actions_no_findings(self):
        text = (
            "VERDICT: REVISE\n\n"
            "## Corrective Actions\n\n"
            "Some prose but no ### F-N headers.\n"
        )
        result = validate_review_verdict(text)
        assert result.valid is False

    def test_verdict_with_trailing_text_rejected(self):
        text = "VERDICT: PROCEED with changes\n"
        result = validate_review_verdict(text)
        assert result.valid is False


class TestValidateReviewVerdictRealFiles:
    """Test against real review.md files on disk.

    Only checks files that contain a VERDICT line (current format).
    Old-format reviews (e.g., **Overall:** CLEAN) are skipped.
    """

    def _find_review_files(self):
        analyses = Path(__file__).parent.parent / "analyses"
        return list(analyses.glob("*/review.md"))

    def test_real_review_files_with_verdict_pass(self):
        files = self._find_review_files()
        if not files:
            return
        tested = 0
        for f in files:
            text = f.read_text(encoding="utf-8")
            # Only test files that have new-format VERDICT line
            if not REVIEW_VERDICT_RE.search(text):
                continue
            result = validate_review_verdict(text)
            assert result.valid, f"{f}: {result.details}"
            tested += 1
            if tested >= 5:
                break
