#!/usr/bin/env python3
"""Tests for the Item 8 line-anchored parser rewrite — Phase 2.

The five named producers (parse_verdict_from_feedback, has_model_category_findings,
validate_feedback_verdict, validate_review_verdict, parse_proposed_actions) had
their internals swapped from the MULTILINE regex constants to line-anchored
scanning. These tests pin the return shapes row-for-row against
.project/active/concept-rework-helpers-validators/signal_contract.md and prove
that pre-rework "old format" artifacts are rejected loudly (at the validator
gate) rather than silently mis-parsed.

Stencil source: .project/active/concept-rework-prompt-templates/plan.md, Phase 2.

Deviation from the plan stencil (documented in plan.md Phase 2 Completion):
`parse_verdict_from_feedback` keeps its `("FAIL", 0)` contract on unrecognized
input instead of raising — the loud-fail guarantee is owned by
`validate_feedback_verdict` (the loop gate), which is the only place that runs
before parsing in the live loop, and the historical-feedback reader
(migrate_iterations) relies on the non-raising contract. The old-format test
below therefore asserts the loud fail at the validator, per the stencil's
explicit "returns an unambiguous sentinel — not a silent mis-parse" allowance.
"""

from pathlib import Path

from lib.iteration import parse_verdict_from_feedback
from lib.sources import parse_proposed_actions
from lib.validators import (
    has_model_category_findings,
    validate_feedback_verdict,
    validate_review_verdict,
)

FIXTURES = Path(__file__).parent / "tests" / "fixtures"
NEW = FIXTURES / "feedback_new_format"
OLD = FIXTURES / "feedback_old_format"

NEW_FORMAT_PASS = NEW / "pass.md"
NEW_FORMAT_FINDINGS = NEW / "findings_mixed.md"
NEW_FORMAT_REVISE = NEW / "revise_with_pa.md"
OLD_FORMAT_ANY = OLD / "any.md"


# ---------------------------------------------------------------------------
# parse_verdict_from_feedback -> tuple[str, int]   (signal_contract row 1)
# ---------------------------------------------------------------------------


def test_parse_verdict_pass_returns_pass_zero():
    assert parse_verdict_from_feedback(NEW_FORMAT_PASS.read_text()) == ("PASS", 0)


def test_parse_verdict_findings_returns_fail_count():
    verdict, count = parse_verdict_from_feedback(NEW_FORMAT_FINDINGS.read_text())
    assert verdict == "FAIL" and count == 2


def test_parse_verdict_return_shape_is_str_int_tuple():
    out = parse_verdict_from_feedback(NEW_FORMAT_FINDINGS.read_text())
    assert isinstance(out, tuple) and len(out) == 2
    assert isinstance(out[0], str) and isinstance(out[1], int)


# ---------------------------------------------------------------------------
# has_model_category_findings -> bool   (signal_contract row 2)
# ---------------------------------------------------------------------------


def test_has_model_category_findings_true_on_mixed_fixture():
    # findings_mixed.md has an F-2 tagged `Category: model`.
    assert has_model_category_findings(NEW_FORMAT_FINDINGS.read_text()) is True


def test_has_model_category_findings_uncategorized_is_conservative_true():
    text = "### F-1: title\n- **Finding:** ...\n"  # no Category line
    assert has_model_category_findings(text) is True


def test_has_model_category_findings_analysis_only_is_false():
    text = (
        "### F-1: only analysis\n- **Category:** analysis\n\n"
        "### F-2: also analysis\n- **Category:** analysis\n"
    )
    assert has_model_category_findings(text) is False


# ---------------------------------------------------------------------------
# validate_feedback_verdict / validate_review_verdict -> ValidationResult
# (signal_contract rows 3 + the feedback gate)
# ---------------------------------------------------------------------------


def test_validate_feedback_verdict_accepts_new_pass():
    r = validate_feedback_verdict(NEW_FORMAT_PASS.read_text())
    assert r.valid and "PASS" in r.details


def test_validate_feedback_verdict_accepts_new_findings():
    r = validate_feedback_verdict(NEW_FORMAT_FINDINGS.read_text())
    assert r.valid and "FINDINGS" in r.details


def test_validate_review_verdict_accepts_new_proceed():
    r = validate_review_verdict(NEW_FORMAT_REVISE.read_text())
    assert r.valid and "PROCEED" in r.details


# ---------------------------------------------------------------------------
# parse_proposed_actions -> list[dict] with nine keys   (signal_contract row 4)
# ---------------------------------------------------------------------------

NINE_KEYS = {
    "id", "description", "category", "severity", "location",
    "finding", "proposed_fix", "decision", "user_notes",
}


def test_parse_proposed_actions_returns_nine_keys_per_dict():
    actions = parse_proposed_actions(NEW_FORMAT_REVISE)
    assert len(actions) == 2
    for a in actions:
        assert set(a.keys()) == NINE_KEYS


def test_parse_proposed_actions_extracts_id_description_and_fields():
    actions = parse_proposed_actions(NEW_FORMAT_REVISE)
    pa1 = actions[0]
    assert pa1["id"] == "PA-1"
    assert pa1["description"].startswith("Net output reconciliation")
    assert pa1["category"] == "inconsistency"
    assert pa1["severity"] == "minor"
    assert "P_native" in pa1["location"]
    assert pa1["finding"]
    assert pa1["proposed_fix"]
    # Unfilled italic placeholders collapse to "".
    assert pa1["decision"] == ""
    assert pa1["user_notes"] == ""


# ---------------------------------------------------------------------------
# Old-format artifacts fail loudly (at the validator gate, not silently)
# ---------------------------------------------------------------------------


def test_old_format_feedback_rejected_by_gate():
    # The pre-rework `**Overall:** CLEAN` artifact has no VERDICT line; the gate
    # must reject it (loud) rather than let it through to a misleading parse.
    r = validate_feedback_verdict(OLD_FORMAT_ANY.read_text())
    assert not r.valid
    assert "VERDICT" in (r.fix_message or "")


def test_old_format_review_rejected_by_gate():
    r = validate_review_verdict(OLD_FORMAT_ANY.read_text())
    assert not r.valid
    assert "VERDICT" in (r.fix_message or "")


def test_old_format_parse_does_not_silently_claim_pass():
    # parse_verdict_from_feedback is downstream of the gate; on the unrecognized
    # old format it must NOT report PASS (which would silently continue the loop).
    verdict, count = parse_verdict_from_feedback(OLD_FORMAT_ANY.read_text())
    assert verdict == "FAIL"
    assert count == 0


# ---------------------------------------------------------------------------
# Line-anchored robustness the old regex got right — keep it right
# ---------------------------------------------------------------------------


def test_verdict_trailing_prose_rejected():
    # "VERDICT: PASS — all goals met" must not validate (token must stand alone).
    r = validate_feedback_verdict("VERDICT: PASS — all goals met\n")
    assert not r.valid


def test_first_verdict_line_wins():
    text = "VERDICT: PASS\n\nVERDICT: FINDINGS\n\n### F-1: x\n- **Category:** model\n"
    assert parse_verdict_from_feedback(text)[0] == "PASS"
