#!/usr/bin/env python3
"""Tests for lib/validators.py — shared regex constants and output validators."""

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

# The Phase 0 prototype is the (two-forward) oracle for the override registry —
# its overrides are all constants, so it still passes the registry validator.
# It is NOT a valid three-forward *contract* fixture (it binds `result`, not
# `generic`/`native`); the contract fixtures below supply that shape.
PROTOTYPE_PATH = (
    Path(__file__).parents[3]
    / ".project/completed/20260821_concept-rework-prototype/artifacts/model_setup.py"
)
PROTOTYPE_TEXT = PROTOTYPE_PATH.read_text(encoding="utf-8")

# The three-forward integration fixture (prompt <-> validator agreement check).
FIXTURES = Path(__file__).parent / "tests" / "fixtures"
CONCEPT01_THREE_FORWARD = (FIXTURES / "concept01_model_setup.py").read_text(
    encoding="utf-8"
)

# The production (Item 8) shape — the three-forward helper form. Inlined here as
# a fixture so the dual-form path is exercised on a real generated shape.
HELPER_FORM_TEXT = '''\
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, elon=1.84, p_input=38.6)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

generic = generic_reference(model, spec, P_native)

overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "Sorbom 2015",

     "rationale": "magnet"},
    {"account": "CAS27", "value": 146.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "Araiinejad 2025",

     "rationale": "FLiBe"},
]

native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)

if __name__ == "__main__":
    print_cas_breakdown(generic, native, result_1gw, overrides)
'''

# Three-forward inline form — `generic` still via generic_reference (mandatory),
# but `native` / `result_1gw` are hand-rolled forwards (the non-strict escape
# hatch). Strict mode rejects this; non-strict accepts it.
INLINE_FORM_TEXT = '''\
from lib.model_setup_helpers import generic_reference
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, elon=1.84, p_input=38.6)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

generic = generic_reference(model, spec, P_native)
overrides = []
native = model.forward(
    net_electric_mw=233.0, n_mod=1, cost_overrides={}, override_reference_mw=233.0,
)
result_1gw = model.forward(
    net_electric_mw=1000, n_mod=4.3, cost_overrides={}, override_reference_mw=233.0,
)
'''

# Broken contract variants ---------------------------------------------------

# Helper form with `native` dropped from the tuple-unpack (only result_1gw).
MISSING_NATIVE = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''

# The old two-forward residue — binds `result`/`result_1gw`, never `generic`/`native`.
TWO_FORWARD_RESIDUE = '''\
from lib.model_setup_helpers import run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
overrides = []
result, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''

MISSING_RESULT_1GW = '''\
from lib.model_setup_helpers import generic_reference
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
spec = dict(R0=3.3)
P_native = 233.0
generic = generic_reference(model, spec, P_native)
native = model.forward(net_electric_mw=233.0, n_mod=1, cost_overrides={})
'''

INLINE_NO_NET_1000 = '''\
from lib.model_setup_helpers import generic_reference
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
spec = dict(R0=3.3)
P_native = 233.0
generic = generic_reference(model, spec, P_native)
native = model.forward(net_electric_mw=233.0, n_mod=1, cost_overrides={})
result_1gw = model.forward(net_electric_mw=500.0, n_mod=2.0)
'''

# `generic` hand-rolled (not via generic_reference) — rejected even non-strict.
GENERIC_NOT_VIA_HELPER = '''\
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = model.forward(net_electric_mw=233.0, n_mod=1)
native = model.forward(net_electric_mw=233.0, n_mod=1, cost_overrides={})
result_1gw = model.forward(net_electric_mw=1000, n_mod=4.3)
'''

HAS_DEFAULT_COMMENT = '''\
from lib.model_setup_helpers import generic_reference
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
spec = dict(R0=3.3)
P_native = 233.0
generic = generic_reference(model, spec, P_native)
native = model.forward(net_electric_mw=233.0, n_mod=1, cost_overrides={})
result_1gw = model.forward(
    net_electric_mw=1000,
    availability=0.85,  # DEFAULT: library default re-passed
    n_mod=4.3,
)
'''


class TestModelSetupContract:
    def test_accepts_inline_three_forward(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(INLINE_FORM_TEXT)
        assert r.valid, r.details
        assert "inline" in r.details

    def test_accepts_helper_form(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(HELPER_FORM_TEXT)
        assert r.valid, r.details
        assert "helper" in r.details

    def test_strict_rejects_inline(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(INLINE_FORM_TEXT, strict_helper_only=True)
        assert not r.valid

    def test_strict_accepts_helper(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(HELPER_FORM_TEXT, strict_helper_only=True)
        assert r.valid, r.details

    def test_rejects_missing_native(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(MISSING_NATIVE)
        assert not r.valid
        assert "native" in r.details

    def test_rejects_two_forward_residue(self):
        """A file still binding only `result`/`result_1gw` (the old shape) is
        rejected — it lacks `generic` and `native`."""
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(TWO_FORWARD_RESIDUE)
        assert not r.valid
        assert "generic" in r.details and "native" in r.details

    def test_rejects_missing_result_1gw(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(MISSING_RESULT_1GW)
        assert not r.valid
        assert "result_1gw" in r.details

    def test_rejects_generic_not_via_helper(self):
        """`generic` must come from generic_reference(), not a hand-rolled forward."""
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(GENERIC_NOT_VIA_HELPER)
        assert not r.valid
        assert "generic" in r.details

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
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "r"},
]
'''

CONST_EXPRESSION_VALUE = '''\
overrides = [
    {"account": "C220103", "value": 5150 * 1.34, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "r"},
]
'''

GENERIC_RELATIVE_VALUE = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * generic.costs.cas21, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "30% prefab reduction"},
]
'''

NATIVE_VALUE = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * native.costs.cas21, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "wrong frame"},
]
'''

RESULT_1GW_VALUE = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * result_1gw.costs.cas21, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "wrong frame"},
]
'''

RESULT_VALUE = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * result.costs.cas21, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "removed two-forward name"},
]
'''

PROVENANCE_GUESS = '''\
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "cost_basis": "noak", "provenance": "guess",

     "source": "s",

     "rationale": "r"},
]
'''

DUP_ACCOUNT = '''\
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "r"},
    {"account": "C220103", "value": 42.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "r"},
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

    def test_accepts_generic_relative_value(self):
        # A relative override referencing `generic` (the overrides-off library
        # value) is allowed; its numeric type is enforced at runtime, not
        # statically.
        from lib.validators import validate_override_registry

        r = validate_override_registry(GENERIC_RELATIVE_VALUE)
        assert r.valid, r.details

    def test_rejects_native_frame(self):
        # Referencing `native` is a frame error — a relative override must be
        # written against `generic`, not the overrides-on design-point forward.
        from lib.validators import validate_override_registry

        r = validate_override_registry(NATIVE_VALUE)
        assert not r.valid
        assert "native" in r.details
        assert "generic" in r.fix_message

    def test_rejects_result_1gw_frame(self):
        # Referencing `result_1gw` is a frame error — overrides are written
        # against `generic`, not the 1 GWe projection.
        from lib.validators import validate_override_registry

        r = validate_override_registry(RESULT_1GW_VALUE)
        assert not r.valid
        assert "result_1gw" in r.details
        assert "generic" in r.fix_message

    def test_rejects_result_frame(self):
        # `result` is the removed two-forward name; referencing it is a frame
        # error (and would NameError at runtime).
        from lib.validators import validate_override_registry

        r = validate_override_registry(RESULT_VALUE)
        assert not r.valid
        assert "result" in r.details
        assert "generic" in r.fix_message

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
# Three-forward integration — a real concept-01 model_setup.py (the shape the
# model-setup prompt instructs) must pass BOTH AST gates. This is the
# prompt<->validator agreement check (acceptance tests 1 & 2): if it fails, the
# prompt shape and the validators have diverged.
# ---------------------------------------------------------------------------


class TestThreeForwardIntegration:
    def test_concept01_threeforward_passes_contract(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(
            CONCEPT01_THREE_FORWARD, strict_helper_only=True
        )
        assert r.valid, r.details
        assert "helper" in r.details

    def test_concept01_threeforward_passes_registry(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(CONCEPT01_THREE_FORWARD)
        assert r.valid, r.details


# ---------------------------------------------------------------------------
# Item 7 — coherence checks (multi-input, advisory / cross-artifact).
# ---------------------------------------------------------------------------

# MS_233 / MS_400 differ only in P_native (the Phase 0 operator error).
MS_233 = '''\
P_native = 233.0
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "r"},
]
'''

MS_400 = '''\
P_native = 400.0
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "r"},
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


# ---------------------------------------------------------------------------
# OpenStar-surfaced override-side validators (F1, F2, F4, F5a, F5b).
#
# Each fixture below shows the minimum-viable model_setup.py shape that
# isolates the rule being tested. The shared assumptions (`generic` from
# generic_reference, helper-form `native`/`result_1gw`) match the contract
# fixtures above; only the registry/spec contents differ.
# ---------------------------------------------------------------------------


_F1_RAW_DOLLARS = '''\
overrides = [
    {"account": "C220105", "value": 20.0e6, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "raw-$ typo"},
]
'''

_F1_NEGATIVE_RAW_DOLLARS = '''\
overrides = [
    {"account": "C220105", "value": -20.0e6, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "negative raw $"},
]
'''

_F1_AT_BOUND = '''\
overrides = [
    {"account": "C220103", "value": 50000.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "at the bound, OK"},
]
'''

_F2_WRONG_ACCOUNT_FOR_ARCHETYPE = '''\
overrides = [
    {"account": "C220109", "value": 100.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "DIPOLE has no DEC; C220109 not in archetype set"},
]
'''

_F2_VALID_ACCOUNT_FOR_DIPOLE = '''\
overrides = [
    {"account": "C220103", "value": 100.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "valid"},
]
'''

_F4_DISABLED_NO_BLOCKED_BY = '''\
overrides = [
    {"account": "C220103", "value": 100.0, "enabled": False,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "disabled but no blocked_by"},
]
'''

_F4_DISABLED_BAD_BLOCKED_BY = '''\
overrides = [
    {"account": "C220103", "value": 100.0, "enabled": False,
     "cost_basis": "noak", "provenance": "direct", "source": "s",
     "rationale": "wrong shape",
     "blocked_by": "this is not org/repo#NN"},
]
'''

_F4_DISABLED_VALID_BLOCKED_BY = '''\
overrides = [
    {"account": "C220103", "value": 100.0, "enabled": False,
     "cost_basis": "noak", "provenance": "direct", "source": "s",
     "rationale": "OK",
     "blocked_by": "1cFE/1costingfe#42"},
]
'''

_F5A_ROLLUP_C220111 = '''\
overrides = [
    {"account": "C220111", "value": 50.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "installation labor"},
]
'''

_F5A_ROLLUP_C220000 = '''\
overrides = [
    {"account": "C220000", "value": 1000.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "CAS22 grand rollup"},
]
'''

_F5B_SPEC_HAS_ETA_TH = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, eta_th=0.46, p_input=38.6)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''

_F5B_SPEC_HAS_INTEREST_RATE = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, p_input=38.6, interest_rate=0.05)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''

_F5B_SPEC_HAS_F_DEC_OK = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, p_input=38.6, f_dec=0.4)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


class TestF1MagnitudeBound:
    """F1 — raw-$ unit error catch (|value| > 5e4 M$)."""

    def test_rejects_raw_dollars(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F1_RAW_DOLLARS)
        assert not r.valid
        assert "M$" in r.fix_message
        msg = r.fix_message
        assert "raw" in msg.lower() or "20.0e6" in msg or "20000000" in msg

    def test_rejects_negative_raw_dollars(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F1_NEGATIVE_RAW_DOLLARS)
        assert not r.valid

    def test_accepts_value_at_bound(self):
        # 50000 is the upper bound; everything <= passes.
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F1_AT_BOUND)
        assert r.valid, r.details


class TestF2ArchetypeAccountWhitelist:
    """F2 — archetype-canonical account check (opt-in via kwarg)."""

    def test_rejects_account_not_in_dipole_set(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(
            _F2_WRONG_ACCOUNT_FOR_ARCHETYPE, archetype_enum="DIPOLE"
        )
        assert not r.valid
        assert "C220109" in r.fix_message
        assert "DIPOLE" in r.fix_message

    def test_accepts_account_in_dipole_set(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(
            _F2_VALID_ACCOUNT_FOR_DIPOLE, archetype_enum="DIPOLE"
        )
        assert r.valid, r.details

    def test_no_archetype_kwarg_skips_check(self):
        # Backward compat: when archetype_enum is None, F2 is a no-op.
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F2_WRONG_ACCOUNT_FOR_ARCHETYPE)
        assert r.valid, r.details

    def test_unknown_archetype_enum_errors(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(
            _F2_VALID_ACCOUNT_FOR_DIPOLE, archetype_enum="NOT_AN_ENUM"
        )
        assert not r.valid
        assert "NOT_AN_ENUM" in r.fix_message


class TestF4BlockedByRequired:
    """F4 — disabled overrides must carry a tracker link."""

    def test_rejects_disabled_without_blocked_by(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F4_DISABLED_NO_BLOCKED_BY)
        assert not r.valid
        assert "blocked_by" in r.fix_message

    def test_rejects_malformed_blocked_by(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F4_DISABLED_BAD_BLOCKED_BY)
        assert not r.valid
        assert "org/repo" in r.fix_message or "org" in r.fix_message

    def test_accepts_valid_blocked_by(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F4_DISABLED_VALID_BLOCKED_BY)
        assert r.valid, r.details


class TestF5aForbiddenRollupAccounts:
    """F5a — derived rollups cannot be overridden at the dollar level."""

    def test_rejects_c220111(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F5A_ROLLUP_C220111)
        assert not r.valid
        assert "C220111" in r.fix_message
        assert "installation_frac" in r.fix_message

    def test_rejects_c220000_rollup(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F5A_ROLLUP_C220000)
        assert not r.valid
        assert "C220000" in r.fix_message
        assert "constituent" in r.fix_message or "C220101" in r.fix_message


class TestF5bSpecForbiddenKeys:
    """F5b — spec dict cannot carry ENUM-owned efficiencies or financial knobs."""

    def test_rejects_eta_th_in_spec(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F5B_SPEC_HAS_ETA_TH)
        assert not r.valid
        assert "eta_th" in r.fix_message
        assert "PowerCycle" in r.fix_message

    def test_rejects_interest_rate_in_spec(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F5B_SPEC_HAS_INTEREST_RATE)
        assert not r.valid
        assert "interest_rate" in r.fix_message
        assert "library" in r.fix_message.lower()

    def test_accepts_f_dec_in_spec(self):
        # f_dec is a physics/architecture property, NOT an efficiency claim;
        # the prompt template explicitly allows it.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F5B_SPEC_HAS_F_DEC_OK)
        assert r.valid, r.details


# ---------------------------------------------------------------------------
# F6 — `generic.<chain>` schema whitelist. The two stellarator-regen
# hallucinations from concepts 05 + 09 are the prosecutor's fixtures here.
# ---------------------------------------------------------------------------


# Concept 05 (planar-coil-stellarator) iter-1 actual code:
_F6_C220103_NOT_ON_COSTS = '''\
overrides = [
    {"account": "C220103", "value": 0.75 * generic.costs.c220103, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "stellarator hallucination 1"},
]
'''

# Concept 09 (qi-stellarator-hts) iter-1 actual code:
_F6_FAKE_ROLLUP_NAME = '''\
overrides = [
    {"account": "C220103", "value": 0.85 * generic.costs.cas22_reactor_equipment_total,
     "enabled": True, "cost_basis": "noak", "provenance": "derived",
 "source": "s",
 "rationale": "stellarator hallucination 2"},
]
'''

_F6_VALID_CAS22_DETAIL = '''\
overrides = [
    {"account": "C220103", "value": 0.85 * generic.cas22_detail["C220103"],
     "enabled": True, "cost_basis": "noak", "provenance": "derived",
 "source": "s",
 "rationale": "the correct CAS22 sub-account pattern"},
]
'''

_F6_VALID_COSTS_ROLLUP = '''\
overrides = [
    {"account": "C220101", "value": 0.70 * generic.costs.cas21, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "the correct top-level rollup pattern"},
]
'''

_F6_BARE_GENERIC_OK = '''\
overrides = [
    {"account": "C220101", "value": generic.costs.cas22, "enabled": True,
     "cost_basis": "noak", "provenance": "direct",

     "source": "s",

     "rationale": "bare access to cas22 rollup"},
]
'''

_F6_UNKNOWN_TOP_LEVEL = '''\
overrides = [
    {"account": "C220101", "value": 0.5 * generic.bogus_attr, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",

     "source": "s",

     "rationale": "unknown top-level"},
]
'''

_F6_BAD_CAS22_KEY = '''\
overrides = [
    {"account": "C220103", "value": generic.cas22_detail["NOT_AN_ACCOUNT"],
     "enabled": True, "cost_basis": "noak", "provenance": "direct",
 "source": "s",
 "rationale": "subscript key not a valid CAS22 code"},
]
'''


class TestF6GenericChainWhitelist:
    """F6 — reject hallucinated `generic.<attr>` chains; accept real ones."""

    def test_rejects_c220103_on_costs(self):
        # Concept 05's literal regen output: `0.75 * generic.costs.c220103`.
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_C220103_NOT_ON_COSTS)
        assert not r.valid
        assert "c220103" in r.fix_message
        # Redirect hint must point at the real path:
        assert 'cas22_detail["C220103"]' in r.fix_message

    def test_rejects_fake_rollup_name(self):
        # Concept 09's literal regen output:
        # `0.85 * generic.costs.cas22_reactor_equipment_total`.
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_FAKE_ROLLUP_NAME)
        assert not r.valid
        assert "cas22_reactor_equipment_total" in r.fix_message

    def test_accepts_valid_cas22_detail(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_VALID_CAS22_DETAIL)
        assert r.valid, r.details

    def test_accepts_valid_costs_rollup(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_VALID_COSTS_ROLLUP)
        assert r.valid, r.details

    def test_accepts_bare_generic_chain(self):
        # Not multiplied by anything — still a valid reference.
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_BARE_GENERIC_OK)
        assert r.valid, r.details

    def test_rejects_unknown_top_level_attr(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_UNKNOWN_TOP_LEVEL)
        assert not r.valid
        assert "bogus_attr" in r.fix_message

    def test_rejects_bad_cas22_subscript_key(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F6_BAD_CAS22_KEY)
        assert not r.valid
        assert "NOT_AN_ACCOUNT" in r.fix_message


# ---------------------------------------------------------------------------
# F7 — `spec` key whitelist against CostingInput.model_fields.
# Concept 04 (laser-icf) was the prosecutor's fixture: its `spec` carried
# `laser_pulse_energy_kJ=30.0, rep_rate_hz=1.0, target_gain=200.0` — none of
# which are CostingInput fields, all of which were silently dropped at
# forward() time, leaving the library to use its YAML defaults (1.4 MJ /
# 10 Hz derived from the engineering Q balance instead of the McKenzie
# 30 kJ / 1 Hz design point).
# ---------------------------------------------------------------------------


# Concept 04's literal regen output (verbatim from the bulk run):
_F7_CONCEPT_04_LITERAL = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    laser_pulse_energy_kJ=30.0,
    rep_rate_hz=1.0,
    target_gain=200.0,
    p_input=50.0,
)
P_native = 500.0
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.PB11)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


_F7_ALL_VALID_SPEC = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=3.3,
    plasma_t=1.13,
    p_input=38.6,
    n_e=1e20,
    T_e=15.0,
)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


_F7_BOGUS_SINGLE_KEY = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, bogus_key=42.0)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


class TestF7SpecKeyWhitelist:
    """F7 — reject `spec` keys outside CostingInput's authoritative schema."""

    def test_rejects_concept04_spec_verbatim(self):
        # Concept 04's literal regen carried three keys forward() drops:
        #   laser_pulse_energy_kJ  — not in CostingInput at all
        #                            (e_driver_mj is derived, not settable)
        #   rep_rate_hz            — should be f_rep
        #   target_gain            — not in CostingInput; closest is p_target
        # F7 must flag all three. difflib's suggester finds at least the
        # target_gain → p_target match; the full allow-list (which includes
        # f_rep) is printed as the authoritative fallback.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F7_CONCEPT_04_LITERAL)
        assert not r.valid
        for k in ("laser_pulse_energy_kJ", "rep_rate_hz", "target_gain"):
            assert k in r.fix_message
        # At least one difflib suggestion fires (target_gain → p_target):
        assert "p_target" in r.fix_message
        # And the canonical allow-list contains the real rep-rate field:
        assert "f_rep" in r.fix_message
        # The error explicitly names the failure mode:
        assert "silently drop" in r.fix_message

    def test_accepts_all_valid_spec(self):
        # A spec containing only real CostingInput field names passes.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F7_ALL_VALID_SPEC)
        assert r.valid, r.details

    def test_rejects_single_bogus_key(self):
        # One bad key among valid ones is still rejected.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F7_BOGUS_SINGLE_KEY)
        assert not r.valid
        assert "bogus_key" in r.fix_message
        assert "allow-list" in r.fix_message.lower()


# ---------------------------------------------------------------------------
# F8 — strict cost_basis: NOAK-only. Concept 01 (ARC) was the prosecutor's
# fixture: its C220103 override transcribed Sorbom 2015's $5.1B verbatim,
# but Sorbom's $1.06M/tonne mass scaling pre-dates the FOAK/NOAK
# convention. The framework runs noak=True; the only honest answer is
# either (a) defer to library, (b) adjust to NOAK with documented
# derivation, or (c) file a tracker for a new variant.
# ---------------------------------------------------------------------------


_F8_MISSING_COST_BASIS = '''\
overrides = [
    {"account": "C220103", "value": 100.0, "enabled": True,
     "provenance": "direct", "source": "s", "rationale": "no cost_basis"},
]
'''

_F8_FOAK_REJECTED = '''\
overrides = [
    {"account": "C220103", "value": 5100.0, "enabled": True,
     "cost_basis": "foak", "provenance": "derived",
     "source": "Sorbom 2015", "rationale": "vintage-unspecified academic"},
]
'''

_F8_CONCEPTUAL_REJECTED = '''\
overrides = [
    {"account": "C220103", "value": 5100.0, "enabled": True,
     "cost_basis": "conceptual_design", "provenance": "derived",
     "source": "Sorbom 2015", "rationale": "$1.06M/tonne scaling"},
]
'''

_F8_NOAK_ACCEPTED = '''\
overrides = [
    {"account": "C220103", "value": 1020.0, "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": "Sorbom 2015 + 5x learning curve derivation",
     "rationale": "$5.1B Sorbom 2014 conceptual x 0.2 (10x learning curve "
                  "applied: REBCO 2014-2026 + structural fab mass mfg) = $1.02B NOAK"},
]
'''


class TestF8CostBasisNoakOnly:
    """F8 — strict NOAK-only cost_basis; everything else is rejected."""

    def test_rejects_missing_cost_basis(self):
        # Field-shape rejection: missing required field "cost_basis".
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F8_MISSING_COST_BASIS)
        assert not r.valid
        assert "cost_basis" in r.fix_message

    def test_rejects_foak(self):
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F8_FOAK_REJECTED)
        assert not r.valid
        assert "foak" in r.fix_message
        # Redirect must mention the three options:
        assert "library default" in r.fix_message
        assert "learning" in r.fix_message.lower() or "vintage" in r.fix_message.lower()
        assert "noak" in r.fix_message.lower()

    def test_rejects_conceptual_design(self):
        # Any value other than "noak" is rejected (no hedge categories).
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F8_CONCEPTUAL_REJECTED)
        assert not r.valid
        assert "conceptual_design" in r.fix_message

    def test_accepts_explicit_noak(self):
        # cost_basis: "noak" + documented learning-curve derivation = accepted.
        from lib.validators import validate_override_registry

        r = validate_override_registry(_F8_NOAK_ACCEPTED)
        assert r.valid, r.details


# ---------------------------------------------------------------------------
# F9 — physical-sense ratio bounds (value/P_native) for spec values. Concepts
# 05 (planar-coil stellarator) and 09 (QI stellarator) of the bulk-run regen
# were the prosecutor's fixtures: each transcribed published fusion power
# (958 MW and 2700 MW) into the `p_input` slot, which the library faithfully
# read as auxiliary-heating wallplug. The inverse power balance then
# manufactured fusion powers of 5-10x the actual design point, every CAS22
# account scaling with p_th inflated, and the resulting LCOEs jumped to
# ~$304/MWh (vs ~$187/MWh for concept 10, the matched control). F9 rejects
# any p_input/P_native > 0.5 — the order-of-magnitude band that order-of-
# magnitude transcription errors fall outside of.
# ---------------------------------------------------------------------------


# Concept 05's literal regen output — p_input = 958.0 against P_native = 390.0
# gives p_input/P_native = 2.46 (well above the 0.5 cap).
_F9_CONCEPT_05_LITERAL = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=15.4,
    plasma_t=1.46,
    p_input=958.0,
)
P_native = 390.0
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Concept 09's literal regen output — p_input = 2700.0 vs P_native = 1000.0
# gives ratio 2.7 (also above the cap).
_F9_CONCEPT_09_LITERAL = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=11.4,
    plasma_t=1.6,
    p_input=2700.0,
)
P_native = 1000.0
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Healthy reference — p_input = 38.6 against P_native = 233.0 gives ratio
# 0.166 (well inside the [0.005, 0.5] band).
_F9_HEALTHY = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=3.3,
    plasma_t=1.1,
    p_input=38.6,
)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Edge-case lower bound — p_input = 1.0 / P_native = 1000.0 gives ratio
# 0.001, below the 0.005 floor. Should be rejected.
_F9_TOO_LOW = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=3.3,
    plasma_t=1.1,
    p_input=1.0,
)
P_native = 1000.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# No P_native — F9 must skip silently (other validators catch the missing
# P_native; F9 is not the right error for that).
_F9_NO_PNATIVE = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.1, p_input=2000.0)
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, 233.0)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, 233.0)
'''


class TestF9SpecRatioBounds:
    """F9 — reject spec values whose ratio to P_native is physically impossible."""

    def test_rejects_concept_05_literal(self):
        # p_input=958.0 / P_native=390.0 = 2.46, above the 0.5 cap.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_CONCEPT_05_LITERAL)
        assert not r.valid
        assert "p_input" in r.fix_message
        assert "P_native" in r.fix_message
        # Redirect must name fusion-power-into-heating-slot as the failure mode:
        assert "fusion power" in r.fix_message.lower()
        # Details report the actual ratio so we can grep regen logs:
        assert "2.4" in r.details or "2.5" in r.details

    def test_rejects_concept_09_literal(self):
        # p_input=2700.0 / P_native=1000.0 = 2.7.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_CONCEPT_09_LITERAL)
        assert not r.valid
        assert "p_input" in r.fix_message
        assert "fusion power" in r.fix_message.lower()

    def test_accepts_healthy_ratio(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_HEALTHY)
        assert r.valid, r.details

    def test_rejects_too_low_ratio(self):
        # 0.001 — below the floor; almost certainly p_input mistakenly in GW
        # or a comma error in the source paper.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_TOO_LOW)
        assert not r.valid
        assert "p_input" in r.fix_message

    def test_skips_when_no_pnative(self):
        # F9 needs P_native; without one, it must defer to the
        # design-point-coherence check rather than firing a confusing F9 error.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_NO_PNATIVE)
        # The contract validator will still pass (P_native is not required
        # by validate_model_setup_contract — it's required by
        # validate_design_point_coherence). F9 must not block here.
        assert r.valid, r.details


# ---------------------------------------------------------------------------
# F9 extension — load-field ratio bounds (p_house, p_cool, p_pump, p_cryo,
# p_trit, p_coils) and heating sub-fractions (p_nbi, p_icrf, p_ecrh, p_lhcd).
# Concept 20a (Type One Energy) was the prosecutor's fixture: its model_setup.py
# set p_house = 800 MW (Type One's published fusion power) into the
# housekeeping slot. p_house/P_native = 800/350 = 2.3 drove the library's
# inverse power balance to inflate every p_th-scaled CAS22 account, raising
# LCOE from a realistic ~$208 to a bogus $285. Same class as concept-05/09's
# p_input bug, just on a different spec key — F9's original bound only covered
# p_input. This extension covers the load fields the LLM is most likely to
# confuse with fusion-or-thermal power, plus the heating sub-fractions that
# share p_input's bound.
# ---------------------------------------------------------------------------


# Concept 20a's literal regen output — p_house = 800.0 against P_native = 350.0
# gives p_house/P_native = 2.29 (well above the 0.05 cap).
_F9_CONCEPT_20A_LITERAL = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=12.5,
    plasma_t=1.25,
    B=9.0,
    p_house=800.0,
    p_input=20.0,
    elon=1.0,
)
P_native = 350.0
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Healthy 20a — p_house at the library-default level (4 MW for a stellarator,
# = 1.1% of 350 MWe P_native, well inside the [0%, 5%] band).
_F9_20A_HEALTHY = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=12.5,
    plasma_t=1.25,
    B=9.0,
    p_house=4.0,
    p_input=20.0,
    elon=1.0,
)
P_native = 350.0
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Cooling-pump fusion-power mistake: p_cool = 500 MW for a 1000 MWe plant
# (50% of native) is way above the 10% cap.
_F9_PCOOL_TOO_HIGH = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.1, p_input=50.0, p_cool=500.0)
P_native = 1000.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Cryogenic overcount: p_cryo = 100 MW (10%) for a 1 GWe plant blows the 2% cap.
_F9_PCRYO_TOO_HIGH = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.1, p_input=50.0, p_cryo=100.0)
P_native = 1000.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# All loads at zero — DD/aneutronic plants with no p_trit, no p_cryo
# (resistive coils), etc. F9 must pass when fields are zero.
_F9_ALL_LOADS_ZERO = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(
    R0=3.3, plasma_t=1.1, p_input=50.0,
    p_house=0.0, p_cool=0.0, p_pump=0.0, p_cryo=0.0, p_trit=0.0, p_coils=0.0,
)
P_native = 1000.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.PB11)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


# Heating sub-fraction fusion-power mistake: p_nbi = 2000 MW for a 1000 MWe
# plant (2x) blows the p_nbi 50% cap.
_F9_PNBI_TOO_HIGH = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.1, p_input=50.0, p_nbi=2000.0)
P_native = 1000.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''


class TestF9ExtensionLoadFields:
    """F9 extension — reject fusion/thermal-power transcription errors on
    load-field spec keys (p_house, p_cool, p_pump, p_cryo, p_trit, p_coils)
    and heating sub-fractions (p_nbi, p_icrf, p_ecrh, p_lhcd)."""

    def test_rejects_concept_20a_literal(self):
        # The Type One Energy fixture: p_house = fusion power.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_CONCEPT_20A_LITERAL)
        assert not r.valid
        assert "p_house" in r.fix_message
        # Redirect must specifically call out the housekeeping role:
        assert "housekeeping" in r.fix_message.lower()
        # And reference the 20a Type One Energy incident, so operators
        # grepping regen logs can connect to this PR:
        assert "20a" in r.fix_message or "Type One" in r.fix_message
        # Details surface the actual ratio (2.28 or 2.29 depending on rounding):
        assert "2.2" in r.details or "2.3" in r.details

    def test_accepts_20a_after_fix(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_20A_HEALTHY)
        assert r.valid, r.details

    def test_rejects_pcool_above_bound(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_PCOOL_TOO_HIGH)
        assert not r.valid
        assert "p_cool" in r.fix_message
        assert "cooling pump" in r.fix_message.lower()

    def test_rejects_pcryo_above_bound(self):
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_PCRYO_TOO_HIGH)
        assert not r.valid
        assert "p_cryo" in r.fix_message
        assert "cryogenic" in r.fix_message.lower()

    def test_accepts_all_loads_zero(self):
        # Aneutronic / non-SC / DD plants legitimately zero out load fields.
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_ALL_LOADS_ZERO)
        assert r.valid, r.details

    def test_rejects_heating_subfraction_overload(self):
        # p_nbi = 2000 / P_native = 1000 = 2.0 (above the 0.5 cap).
        from lib.validators import validate_model_setup_contract

        r = validate_model_setup_contract(_F9_PNBI_TOO_HIGH)
        assert not r.valid
        assert "p_nbi" in r.fix_message

    def test_first_failing_key_reported(self):
        # When multiple bounds would fire, F9 reports the FIRST failure in
        # iteration order (dict insertion order: p_input → p_house → ...).
        # This test pins that ordering by giving 20a's p_house alongside an
        # also-bad p_cool, and asserting p_house is the reported failure.
        from lib.validators import validate_model_setup_contract

        text = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.1, p_input=50.0, p_house=800.0, p_cool=500.0)
P_native = 350.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
generic = generic_reference(model, spec, P_native)
overrides = []
native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''
        r = validate_model_setup_contract(text)
        assert not r.valid
        # p_house comes before p_cool in _SPEC_RATIO_BOUNDS' insertion order,
        # so p_house is reported first:
        assert "p_house" in r.fix_message
