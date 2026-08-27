"""The exit-0 empty result: a fact, not a failure.

A broken analysis and an empty one must never share an exit code. This is the
empty one, and it exits 0 with a full report.
"""

import json

from tests.study.conftest import DATA_DIR, REAL_MANIFEST, REAL_PACKAGE, run_tool_raw

EXTRAS = DATA_DIR / "axes.extras.json"


def group_by_axis(doc, axis):
    return next(g for g in doc["groups"] if g["axis"] == axis)


def test_a_group_with_no_constraint_reach_exits_zero(tmp_path):
    out_path = tmp_path / "indicators.json"
    rc, out, err = run_tool_raw(REAL_PACKAGE, REAL_MANIFEST, EXTRAS, out=out_path)
    assert rc == 0, err
    assert out == ""  # --out was given, so the document went to the file
    doc = json.loads(out_path.read_text())

    group = group_by_axis(doc, "land_cost")
    assert group["group_valid"] is True
    assert group["no_constraint_response"] is True
    assert group["constraints_reachable"] == []
    assert group["objectives_reachable"] == ["lcoe", "lcoe_1cfe", "total_capital"]
    assert group["objectives_unreachable"] == ["beta", "cas27", "cas72", "fuel", "magnet_capital"]


def test_the_empty_result_still_carries_the_whole_catalog(tmp_path):
    """Invariant 4 and 5: no_constraint_response is emitted with the full bounds
    list under this axis, so a reader sees what was checked, not just what was found."""
    rc, out, err = run_tool_raw(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    assert rc == 0, err
    group = group_by_axis(json.loads(out), "land_cost")
    assert len(group["bounds"]) == 6
    assert len(group["constraints_unreachable"]) == 6
    assert all(not any(o["reached"] for o in c["operands"]) for c in group["bounds"])


def test_no_constraint_response_is_emitted_even_when_false(tmp_path):
    rc, out, err = run_tool_raw(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    assert rc == 0, err
    doc = json.loads(out)
    for group in doc["groups"]:
        assert "no_constraint_response" in group
        assert group["no_constraint_response"] == (group["constraints_reachable"] == [])
    assert group_by_axis(doc, "R_partial")["no_constraint_response"] is False


def test_the_document_goes_to_stdout_and_the_summary_to_stderr():
    """The human summary can never contaminate the report."""
    rc, out, err = run_tool_raw(REAL_PACKAGE, REAL_MANIFEST, EXTRAS)
    assert rc == 0
    json.loads(out)  # stdout is the document and nothing else
    assert "land_cost:" in err
    assert "possible path exists" in err
