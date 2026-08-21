"""The six Item 1 cases, field for field, against the committed package.

The expectation files in ``data/`` are bound to the semantic fingerprint they were
derived against. If the package is regenerated they are re-derived from the new
package, never patched to match — ``test_fixture_binding`` fails first and says so.

The table below restates the fixture contract's headline facts in the test itself,
so the frozen expectation files are not the only thing guarding the trace.
"""

import json

import pytest

from scripts.study import manifest
from tests.study.conftest import DATA_DIR, run_tool

CASES = ["availability", "interest_rate", "R", "R+tie", "a", "beta"]

EXPECTED_SEMANTIC_FINGERPRINT = (
    "1be51d890e5e2f973da919a9ff3cb5ef04a75652e5f906f13cea2a519f97b3aa"
)

#: axis -> (no_constraint_response, reachable constraints, reachable objectives,
#:          modules fired, channels tainted). Read straight off the Item 1 fixture
#: contract in .project/active/run-study-reachability-spike/findings.md, re-derived
#: on the 2.0.0 package after the stellarator model migration (2026-08-21): the
#: qualitative contract is unchanged; R and a fire one more module and taint one
#: more channel because CAS27 is now computed in-package and declared as the
#: `cas27` objective, and each swept attribute is one plant-level entry point.
FIXTURE_CONTRACT = {
    "availability": (True, [], ["cas72", "fuel", "lcoe", "lcoe_1cfe"], 6, 8),
    "interest_rate": (True, [], ["cas72", "lcoe", "lcoe_1cfe"], 8, 11),
    "R": (
        False,
        ["net_positive", "recirc_ok", "wall_load_ok"],
        ["cas27", "cas72", "fuel", "lcoe", "lcoe_1cfe", "total_capital"],
        55,
        68,
    ),
    "R+tie": (
        False,
        ["net_positive", "recirc_ok", "wall_load_ok"],
        ["cas27", "cas72", "fuel", "lcoe", "lcoe_1cfe", "total_capital"],
        55,
        68,
    ),
    "a": (
        False,
        ["net_positive", "recirc_ok", "wall_load_ok"],
        ["cas27", "cas72", "fuel", "lcoe", "lcoe_1cfe", "total_capital"],
        55,
        68,
    ),
    "beta": (False, ["beta_ok"], [], 2, 2),
}


@pytest.fixture(scope="module")
def report(request):
    package = request.config.rootpath / "exploration/stellarator_e2e/pkg/stellarator_tea"
    manifest_path = request.config.rootpath / "exploration/stellarator_e2e/studies/manifest.json"
    return run_tool(package, manifest_path, DATA_DIR / "axes.known_answers.json")


def group_by_axis(doc, axis):
    return next(g for g in doc["groups"] if g["axis"] == axis)


def test_fixture_binding(real_package_path):
    """Fixtures are bound to the fingerprint they were derived against (spec)."""
    live = manifest.read_semantic_fingerprint(real_package_path)
    assert live == EXPECTED_SEMANTIC_FINGERPRINT, (
        "package regenerated — re-derive the expectation files from the new package, "
        "never patch them to match"
    )


@pytest.mark.parametrize("axis", CASES)
def test_expectation_files_record_their_fingerprint(axis):
    expected = json.loads((DATA_DIR / f"{axis}.expected.json").read_text())
    assert expected["derived_against_semantic_fingerprint"] == EXPECTED_SEMANTIC_FINGERPRINT


@pytest.mark.parametrize("axis", CASES)
def test_known_answer(axis, report):
    """Field for field: operand class per reached operand, operator, bound_vs_bound,
    both objective lists, sibling candidates, and the module/channel counts."""
    got = group_by_axis(report, axis)
    expected = json.loads((DATA_DIR / f"{axis}.expected.json").read_text())["group"]
    assert got == expected


@pytest.mark.parametrize("axis", CASES)
def test_matches_the_item_1_fixture_contract(axis, report):
    no_response, constraints, objectives, fired, tainted = FIXTURE_CONTRACT[axis]
    group = group_by_axis(report, axis)
    assert group["group_valid"] is True
    assert group["no_constraint_response"] is no_response
    assert sorted(c["source_local_identity"] for c in group["constraints_reachable"]) == constraints
    assert group["objectives_reachable"] == objectives
    assert group["trace_size"] == {"modules_fired": fired, "channels_tainted": tainted}
    assert group["sibling_candidates"] == []  # every declared group, per the contract


def test_availability_reaches_no_constraint(report):
    """The original finding, now mechanical: the availability sweep that ran to
    completion could not have been a design search, because nothing constrains it."""
    group = group_by_axis(report, "availability")
    assert group["no_constraint_response"] is True
    assert group["constraints_reachable"] == []
    assert len(group["constraints_unreachable"]) == 5


def test_beta_is_a_bound_versus_bound_comparison(report):
    group = group_by_axis(report, "beta")
    (beta_ok,) = group["constraints_reachable"]
    assert beta_ok["source_local_identity"] == "beta_ok"
    assert beta_ok["operator"] == "<="
    assert beta_ok["bound_vs_bound"] is True
    assert [o["class"] for o in beta_ok["operands"]] == ["bound", "bound"]
    assert group["objectives_reachable"] == []


def test_r_reaches_net_positive_through_a_computed_operand(report):
    """R3's `.root` strip is load-bearing: without it R loses net_positive."""
    group = group_by_axis(report, "R")
    net_positive = next(
        c for c in group["constraints_reachable"] if c["source_local_identity"] == "net_positive"
    )
    reached = next(o for o in net_positive["operands"] if o["reached"])
    assert reached["class"] == "computed"
    assert reached["ref"].endswith("pb__p_net")
    literal = next(o for o in net_positive["operands"] if o["class"] == "literal")
    assert literal["value"] == 0.0


def test_the_declared_tie_does_not_change_reach(report):
    """R+tie differs from R only in the declared key list and the tie warning."""
    plain = group_by_axis(report, "R")
    tied = group_by_axis(report, "R+tie")
    traced = ("constraints_reachable", "constraints_unreachable", "bounds",
              "objectives_reachable", "objectives_unreachable", "trace_size",
              "no_constraint_response", "sibling_candidates")
    assert {k: plain[k] for k in traced} == {k: tied[k] for k in traced}
    assert len(tied["declared_keys"]) == 2


def test_every_constraint_carries_all_three_identities(report):
    """D10: constraint_id locates the module; the record correlates across
    fingerprints on definition qualified name plus local identity."""
    for group in report["groups"]:
        for constraint in group["bounds"]:
            assert constraint["constraint_id"]
            assert constraint["definition_qualified_name"]
            assert constraint["source_local_identity"]
            # R9: the id is the pipeline module name, which carries the local identity
            # plus a hash suffix that does not survive regeneration.
            assert constraint["source_local_identity"] in constraint["constraint_id"]
