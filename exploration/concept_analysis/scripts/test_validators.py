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
    chain_validators,
    has_model_category_findings,
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


# ---------------------------------------------------------------------------
# New validators (FR-9, FR-10, FR-11) — added in Phase 2 of pipeline hardening.
# Tests are intentionally RED in Phase 1 (ImportError) until implemented.
# ---------------------------------------------------------------------------


class TestValidateNonEmpty:
    def test_rejects_empty_string(self):
        from lib.validators import validate_non_empty

        result = validate_non_empty("")
        assert result.valid is False
        assert result.fix_message is not None

    def test_rejects_whitespace_only(self):
        from lib.validators import validate_non_empty

        result = validate_non_empty("   \n\t  \n")
        assert result.valid is False

    def test_accepts_content(self):
        from lib.validators import validate_non_empty

        result = validate_non_empty("hello")
        assert result.valid is True


class TestValidatePythonSyntax:
    def test_rejects_bad_syntax(self):
        from lib.validators import validate_python_syntax

        result = validate_python_syntax("def f(\n")
        assert result.valid is False
        assert result.fix_message is not None
        assert "1" in result.details  # lineno surfaced in details

    def test_accepts_valid_python(self):
        from lib.validators import validate_python_syntax

        result = validate_python_syntax("def f(): pass\nresult = f()\n")
        assert result.valid is True

    def test_accepts_empty_string(self):
        """An empty string IS valid Python (``compile('', ...)`` succeeds).
        validate_non_empty is the right check for non-emptiness."""
        from lib.validators import validate_python_syntax

        result = validate_python_syntax("")
        assert result.valid is True

    def test_surfaces_lineno_and_msg_in_fix_message(self):
        from lib.validators import validate_python_syntax

        src = "a = 1\nb = 2\ndef f(\n"  # SyntaxError on line 3
        result = validate_python_syntax(src)
        assert result.valid is False
        assert result.fix_message is not None
        assert "3" in result.fix_message


class TestMakeFileModifiedValidator:
    def test_rejects_unchanged(self, tmp_path):
        from lib.validators import make_file_modified_validator

        f = tmp_path / "analysis.md"
        f.write_text("original content\n", encoding="utf-8")
        validator = make_file_modified_validator(f)

        result = validator("original content\n")  # text argument is ignored
        assert result.valid is False
        assert result.fix_message is not None
        assert "Edit" in result.fix_message or "edit" in result.fix_message.lower()

    def test_accepts_changed(self, tmp_path):
        from lib.validators import make_file_modified_validator

        f = tmp_path / "analysis.md"
        f.write_text("original\n", encoding="utf-8")
        validator = make_file_modified_validator(f)

        f.write_text("modified content\n", encoding="utf-8")
        result = validator("modified content\n")
        assert result.valid is True

    def test_ignores_text_argument(self, tmp_path):
        """The validator must re-read bytes from disk, not trust the ``text``
        argument. Reading bytes avoids UTF-8 / line-ending / BOM round-trips
        that produce false positives (see design §component-3).
        """
        from lib.validators import make_file_modified_validator

        f = tmp_path / "analysis.md"
        f.write_text("original\n", encoding="utf-8")
        validator = make_file_modified_validator(f)

        # File unchanged on disk — a different text argument must NOT fool
        # the validator into reporting changed.
        result = validator("something completely different")
        assert result.valid is False

    def test_crlf_identical_rewrite_rejects(self, tmp_path):
        """Byte-exact rewrite with CRLF line endings must be rejected.

        The factory snapshots ``sha256(read_bytes())``. A file with CRLF line
        endings read through ``read_text`` normalizes to LF, so hashing the
        encoded string can disagree with the bytes-on-disk hash. The validator
        MUST read bytes directly to avoid this false-pass.
        """
        from lib.validators import make_file_modified_validator

        f = tmp_path / "analysis.md"
        crlf_content = b"line1\r\nline2\r\nline3\r\n"
        f.write_bytes(crlf_content)
        validator = make_file_modified_validator(f)

        f.write_bytes(crlf_content)  # identical bytes

        result = validator("line1\nline2\nline3\n")  # normalized text arg
        assert result.valid is False, (
            "CRLF file re-written byte-identical must be rejected — "
            "the validator is hashing text not bytes (false pass)"
        )

    def test_bom_identical_rewrite_rejects(self, tmp_path):
        """Same concern as CRLF but for a UTF-8 BOM."""
        from lib.validators import make_file_modified_validator

        f = tmp_path / "analysis.md"
        bom_content = b"\xef\xbb\xbfhello world\n"
        f.write_bytes(bom_content)
        validator = make_file_modified_validator(f)

        f.write_bytes(bom_content)
        result = validator("hello world\n")  # BOM stripped in text
        assert result.valid is False

    def test_validator_name_is_validate_file_modified(self, tmp_path):
        """Log entries use ``validator.__name__`` — the factory must rename
        the returned callable for readable log entries."""
        from lib.validators import make_file_modified_validator

        f = tmp_path / "x.md"
        f.write_text("x", encoding="utf-8")
        validator = make_file_modified_validator(f)
        assert validator.__name__ == "validate_file_modified"


# ---------------------------------------------------------------------------
# FR-8: existing feedback/review verdict validators must surface detected
# verdict type in ``details`` on success.
# ---------------------------------------------------------------------------


class TestValidateFeedbackVerdictDetailsIncludeType:
    def test_pass_details_contains_pass(self):
        result = validate_feedback_verdict("VERDICT: PASS\n")
        assert result.valid is True
        assert "PASS" in result.details

    def test_findings_details_contains_findings(self):
        text = (
            "VERDICT: FINDINGS\n\n"
            "### F-1: Title\n"
            "- **Category:** analysis\n"
        )
        result = validate_feedback_verdict(text)
        assert result.valid is True
        assert "FINDINGS" in result.details


class TestValidateReviewVerdictDetailsIncludeType:
    def test_proceed_details_contains_proceed(self):
        result = validate_review_verdict("VERDICT: PROCEED\n")
        assert result.valid is True
        assert "PROCEED" in result.details

    def test_revise_details_contains_revise(self):
        text = (
            "VERDICT: REVISE\n\n"
            "## Corrective Actions\n\n"
            "### F-1: Fix\n"
            "- **Category:** analysis\n"
        )
        result = validate_review_verdict(text)
        assert result.valid is True
        assert "REVISE" in result.details


# ---------------------------------------------------------------------------
# chain_validators tests
# ---------------------------------------------------------------------------


class TestChainValidators:
    def _make_validator(self, name: str, valid: bool, details: str = ""):
        """Helper: create a named validator returning a fixed result."""
        def v(text: str) -> ValidationResult:
            return ValidationResult(
                valid=valid,
                fix_message=None if valid else f"Fix: {name}",
                details=details or name,
            )
        v.__name__ = name
        return v

    def test_both_pass(self):
        v1 = self._make_validator("a", valid=True)
        v2 = self._make_validator("b", valid=True)
        chain = chain_validators(v1, v2)
        result = chain("anything")
        assert result.valid is True

    def test_first_fails(self):
        v1 = self._make_validator("a", valid=False)
        v2 = self._make_validator("b", valid=True)
        chain = chain_validators(v1, v2)
        result = chain("anything")
        assert result.valid is False
        assert "Fix: a" in result.fix_message

    def test_second_fails(self):
        v1 = self._make_validator("a", valid=True)
        v2 = self._make_validator("b", valid=False)
        chain = chain_validators(v1, v2)
        result = chain("anything")
        assert result.valid is False
        assert "Fix: b" in result.fix_message

    def test_name_concatenation(self):
        v1 = self._make_validator("alpha", valid=True)
        v2 = self._make_validator("beta", valid=True)
        chain = chain_validators(v1, v2)
        assert chain.__name__ == "alpha+beta"


# ---------------------------------------------------------------------------
# has_model_category_findings tests
# ---------------------------------------------------------------------------


class TestHasModelCategoryFindings:
    def test_empty_string(self):
        assert has_model_category_findings("") is False

    def test_no_findings(self):
        assert has_model_category_findings("Some text without F-N blocks") is False

    def test_analysis_only(self):
        text = (
            "### F-1: First finding\n"
            "- **Category:** analysis\n\n"
            "### F-2: Second finding\n"
            "- **Category:** analysis\n"
        )
        assert has_model_category_findings(text) is False

    def test_model_finding(self):
        text = (
            "### F-1: Model issue\n"
            "- **Category:** model\n"
        )
        assert has_model_category_findings(text) is True

    def test_missing_category(self):
        text = (
            "### F-1: No category field\n"
            "- **Target:** Section 2\n"
            "- **Finding:** Something\n"
        )
        assert has_model_category_findings(text) is True

    def test_mixed_categories(self):
        text = (
            "### F-1: Analysis finding\n"
            "- **Category:** analysis\n\n"
            "### F-2: Model finding\n"
            "- **Category:** model\n"
        )
        assert has_model_category_findings(text) is True
