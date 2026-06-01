#!/usr/bin/env python3
"""Tests for lib/validators.py — shared regex constants and output validators."""

import re
from pathlib import Path

from lib.validators import (
    CORRECTIVE_ACTIONS_RE,
    FINDING_CATEGORY_RE,
    ValidationResult,
    _verdict_token,
    chain_validators,
    has_model_category_findings,
    validate_feedback_verdict,
    validate_review_verdict,
)

# ---------------------------------------------------------------------------
# Shared regex constant tests
# ---------------------------------------------------------------------------
# The verdict / finding-header / proposed-action constants were deleted in
# Item 8 Phase 4 (FR-28); their behaviour now lives in the line-anchored helpers
# (covered by test_parsers_new_format.py). Only the two surviving constants
# (FINDING_CATEGORY_RE, CORRECTIVE_ACTIONS_RE) are exercised here.


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


class TestCorrectiveActionsRE:
    def test_matches(self):
        assert CORRECTIVE_ACTIONS_RE.search("## Corrective Actions\n")

    def test_with_content_after(self):
        assert CORRECTIVE_ACTIONS_RE.search("## Corrective Actions\n\n### F-1:")


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
        return list(analyses.glob("*/iter-*/post_feedback.md"))

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
            if _verdict_token(text, frozenset({"PROCEED", "REVISE"})) is None:
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


# ---------------------------------------------------------------------------
# Item 7 — structural model_setup.py validators (AST-based).
# ---------------------------------------------------------------------------

# The Phase 0 prototype is the live oracle for the *inline* form.
PROTOTYPE_PATH = (
    Path(__file__).parents[3]
    / ".project/active/concept-rework-prototype/artifacts/model_setup.py"
)
PROTOTYPE_TEXT = PROTOTYPE_PATH.read_text(encoding="utf-8")

# The production (Item 8) shape — the four-step helper form. Inlined here as a
# fixture so the dual-form path can't silently pass only the prototype.
HELPER_FORM_TEXT = '''\
from lib.model_setup_helpers import run_native_and_1gw, print_cas_breakdown
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, elon=1.84, eta_th=0.46, p_input=38.6)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "Sorbom 2015", "rationale": "magnet"},
    {"account": "CAS27", "value": 146.0, "enabled": True,
     "provenance": "derived", "source": "Araiinejad 2025", "rationale": "FLiBe"},
]

result, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)

if __name__ == "__main__":
    print_cas_breakdown(result, result_1gw, overrides)
'''

# Broken contract variants ---------------------------------------------------

MISSING_RESULT_1GW = '''\
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
result = model.forward(net_electric_mw=233.0, n_mod=1)
'''

INLINE_NO_NET_1000 = '''\
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
result = model.forward(net_electric_mw=233.0, n_mod=1)
result_1gw = model.forward(net_electric_mw=500.0, n_mod=2.0)
'''

HAS_DEFAULT_COMMENT = '''\
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
result = model.forward(net_electric_mw=233.0, n_mod=1)
result_1gw = model.forward(
    net_electric_mw=1000,
    availability=0.85,  # DEFAULT: library default re-passed
    n_mod=4.3,
)
'''


class TestModelSetupContract:
    def test_accepts_inline_prototype(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(PROTOTYPE_TEXT)
        assert r.valid, r.details
        assert "inline" in r.details

    def test_accepts_helper_form(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(HELPER_FORM_TEXT)
        assert r.valid, r.details
        assert "helper" in r.details

    def test_strict_rejects_inline(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(PROTOTYPE_TEXT, strict_helper_only=True)
        assert not r.valid

    def test_strict_accepts_helper(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(HELPER_FORM_TEXT, strict_helper_only=True)
        assert r.valid, r.details

    def test_rejects_missing_result_1gw(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(MISSING_RESULT_1GW)
        assert not r.valid
        assert "result_1gw" in r.details

    def test_rejects_inline_without_net_1000(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(INLINE_NO_NET_1000)
        assert not r.valid

    def test_warns_on_default_comment(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(HAS_DEFAULT_COMMENT)
        assert r.valid  # advisory only
        assert "DEFAULT" in r.details

    def test_default_warning_suppressible(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(
            HAS_DEFAULT_COMMENT, warn_on_default_comments=False
        )
        assert r.valid
        assert "DEFAULT" not in r.details

    def test_rejects_syntax_error(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract("result_1gw = (\n")
        assert not r.valid
        assert "SyntaxError" in r.details


# ---------------------------------------------------------------------------
# Item 7 — override registry validator.
# ---------------------------------------------------------------------------

MISSING_PROVENANCE = '''\
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "source": "Sorbom 2015", "rationale": "magnet"},
]
'''

NONNUMERIC_VALUE = '''\
overrides = [
    {"account": "C220103", "value": "6901", "enabled": True,
     "provenance": "derived", "source": "s", "rationale": "r"},
]
'''

CONST_EXPRESSION_VALUE = '''\
overrides = [
    {"account": "C220103", "value": 5150 * 1.34, "enabled": True,
     "provenance": "derived", "source": "s", "rationale": "r"},
]
'''

RESULT_RELATIVE_VALUE = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * result.costs.cas21, "enabled": True,
     "provenance": "derived", "source": "s", "rationale": "30% prefab reduction"},
]
'''

RESULT_1GW_VALUE = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * result_1gw.costs.cas21, "enabled": True,
     "provenance": "derived", "source": "s", "rationale": "wrong frame"},
]
'''

PROVENANCE_GUESS = '''\
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "guess", "source": "s", "rationale": "r"},
]
'''

DUP_ACCOUNT = '''\
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "s", "rationale": "r"},
    {"account": "C220103", "value": 42.0, "enabled": False,
     "provenance": "direct", "source": "s", "rationale": "r"},
]
'''

NO_OVERRIDES = '''\
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
'''


class TestOverrideRegistry:
    def test_accepts_prototype_registry(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(PROTOTYPE_TEXT)
        assert r.valid, r.details

    def test_accepts_helper_form_registry(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(HELPER_FORM_TEXT)
        assert r.valid, r.details

    def test_accepts_empty_registry(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry("overrides = []\n")
        assert r.valid

    def test_rejects_missing_provenance(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(MISSING_PROVENANCE)
        assert not r.valid
        assert "provenance" in r.details

    def test_rejects_nonnumeric_value(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(NONNUMERIC_VALUE)
        assert not r.valid

    def test_accepts_constant_expression_value(self):
        # A constant arithmetic expression (e.g. CPI inflation) is allowed; it
        # documents its own derivation and folds to a number statically.
        from lib.validators import validate_override_registry

        r = validate_override_registry(CONST_EXPRESSION_VALUE)
        assert r.valid, r.details

    def test_accepts_result_relative_value(self):
        # A relative override referencing the native `result` is allowed; its
        # numeric type is enforced at runtime, not statically.
        from lib.validators import validate_override_registry

        r = validate_override_registry(RESULT_RELATIVE_VALUE)
        assert r.valid, r.details

    def test_rejects_result_1gw_frame(self):
        # Referencing `result_1gw` is a frame error — overrides are written at
        # the native (n_mod=1 / P_native) reference, not the 1 GWe projection.
        from lib.validators import validate_override_registry

        r = validate_override_registry(RESULT_1GW_VALUE)
        assert not r.valid
        assert "result_1gw" in r.details

    def test_rejects_provenance_guess(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(PROVENANCE_GUESS)
        assert not r.valid

    def test_rejects_duplicate_account(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(DUP_ACCOUNT)
        assert not r.valid
        assert "C220103" in r.details

    def test_rejects_no_overrides_binding(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(NO_OVERRIDES)
        assert not r.valid


# ---------------------------------------------------------------------------
# Item 7 — coherence checks (multi-input, advisory / cross-artifact).
# ---------------------------------------------------------------------------

# MS_233 / MS_400 differ only in P_native (the Phase 0 operator error).
MS_233 = '''\
P_native = 233.0
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "direct", "source": "s", "rationale": "r"},
]
'''

MS_400 = '''\
P_native = 400.0
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "direct", "source": "s", "rationale": "r"},
]
'''

ROW = {"concept_id": "01-hts-compact-tokamak", "p_native_mwe": 233}

# Provisional analysis.md leg: P_native agrees (233) but C220103 provenance is
# `derived`, conflicting with MS_233's `direct`.
ANALYSIS_DERIVED = '''\
## Design Point

P_native: 233 MWe

## Overrides

- C220103 — provenance: derived (magnet+structure)
'''


class TestDesignPointCoherence:
    def test_two_legs_agree(self):
        from lib.validators import validate_design_point_coherence

        r = validate_design_point_coherence("01-hts-compact-tokamak", MS_233, ROW)
        assert r.valid, r.details

    def test_flags_pnative_operator_error(self):
        from lib.validators import validate_design_point_coherence

        r = validate_design_point_coherence("01-hts-compact-tokamak", MS_400, ROW)
        assert not r.valid
        assert "P_native" in r.details

    def test_flags_provenance_mismatch_third_leg(self):
        from lib.validators import validate_design_point_coherence

        r = validate_design_point_coherence(
            "01-hts-compact-tokamak", MS_233, ROW, ANALYSIS_DERIVED
        )
        assert not r.valid
        assert "C220103" in r.details

    def test_three_legs_agree(self):
        """Analysis leg supplied and consistent (provenance direct == direct)."""
        from lib.validators import validate_design_point_coherence

        analysis_direct = (
            "P_native: 233 MWe\n\n- C220103 — provenance: direct\n"
        )
        r = validate_design_point_coherence(
            "01-hts-compact-tokamak", MS_233, ROW, analysis_direct
        )
        assert r.valid, r.details
        assert "3-leg" in r.details

    def test_missing_pnative_in_code(self):
        from lib.validators import validate_design_point_coherence

        r = validate_design_point_coherence(
            "x", "overrides = []\n", ROW
        )
        assert not r.valid


def _flagged(result) -> bool:
    return "FLAG" in result.details


class TestOverrideCountVsFitGrade:
    def test_high_with_few_is_quiet(self):
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("High", 4)
        assert r.valid and not _flagged(r)

    def test_high_with_many_flagged(self):
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("High", 12)
        assert r.valid and _flagged(r)

    def test_low_with_zero_flagged(self):
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("Low", 0)
        assert r.valid and _flagged(r)

    def test_med_with_zero_flagged(self):
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("Med", 0)
        assert r.valid and _flagged(r)

    def test_low_below_band_flagged(self):
        """Low band is 6–12; 3 corrections is below it → flag (too few)."""
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("Low", 3)
        assert r.valid and _flagged(r)

    def test_low_within_band_quiet(self):
        """Low fit with a count inside the 6–12 band stays quiet."""
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("Low", 8)
        assert r.valid and not _flagged(r)

    def test_med_within_band_quiet(self):
        """Med band is 3–8; a mid-band count stays quiet."""
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("Med", 5)
        assert r.valid and not _flagged(r)

    def test_none_grade_quiet(self):
        from lib.validators import check_override_count_vs_fit_grade

        r = check_override_count_vs_fit_grade("None", 0)
        assert r.valid and not _flagged(r)

    def test_boundary_band_single_sourced(self):
        """High band upper bound now comes from FIT_GRADE_OVERRIDE_BAND (0–4),
        not a bare threshold: High+4 quiet, High+5 flagged."""
        from lib.validators import check_override_count_vs_fit_grade

        assert not _flagged(check_override_count_vs_fit_grade("High", 4))
        assert _flagged(check_override_count_vs_fit_grade("High", 5))
