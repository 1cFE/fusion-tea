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

CASES = ["availability", "interest_rate", "R", "R+tie", "a", "I_coil"]

EXPECTED_SEMANTIC_FINGERPRINT = (
    # WI-039 heating power chain (goal wall-and-heating, 2026-09-03)
    "48731d1570bb20cdeae45faa20545aae46aeda5982a4fbc2129d7784a66595ba"
)

#: axis -> (no_constraint_response, reachable constraints, reachable objectives,
#:          modules fired, channels tainted). Read straight off the Item 1 fixture
#: contract in .project/completed/20260821_run-study-reachability-spike/findings.md, re-derived
#: on the 2.0.0 package after the stellarator model migration (2026-08-21): the
#: qualitative contract is unchanged; R and a fire one more module and taint one
#: more channel because CAS27 is now computed in-package and declared as the
#: `cas27` objective, and each swept attribute is one plant-level entry point.
FIXTURE_CONTRACT = {
    # WI-039 (goal wall-and-heating, 2026-09-03) re-derived every expectation file
    # on the heating-chain package and this contract is UNCHANGED, field for field:
    # same reachable constraints, same objectives, same trace sizes for all six axes.
    # What moved is inside sustainment_ok, and it moved in the right direction --
    # its p_aux_installed_in operand was `bound` to the held design attribute
    # p_input and is now `computed` from the chain's heat.p_coupled, so the fence
    # is computed-vs-computed rather than computed-vs-held.
    #
    # Re-derived from the live report on the WI-036 package (2026-09-03, goal
    # priced-levers): the winding pack is now sized by the current it carries and
    # the winding length follows machine scale, so two reaches EXPANDED.
    # (1) cond_strain_ok -- the new conductor check -- is reachable from both
    # field levers (I_coil, R+tie), so the conductor is checked by the same
    # sweeps that check the structure, not left inert.
    # (2) R+tie now reaches magnet_capital, which it did not before: c_coil =
    # k_coil * R means the major radius finally reaches the magnet conductor
    # cost through the winding length (MR-WI036-4). availability and
    # interest_rate are untouched (still no_constraint_response -- the Row 11
    # finding stands).
    "availability": (True, [], ['cas72', 'fuel', 'lcoe', 'lcoe_1cfe'], 6, 8),
    "interest_rate": (True, [], ['cas72', 'lcoe', 'lcoe_1cfe'], 8, 11),
    "R": (False, ['beta_ok', 'net_positive', 'recirc_ok', 'sustainment_ok', 'wall_load_ok'], ['beta', 'cas27', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 59, 86),
    "R+tie": (False, ['beta_ok', 'cond_strain_ok', 'net_positive', 'peak_field_ok', 'recirc_ok', 'sustainment_ok', 'wall_load_ok', 'wp_stress_ok'], ['beta', 'cas27', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 71, 98),
    "a": (False, ['beta_ok', 'net_positive', 'recirc_ok', 'sustainment_ok', 'wall_load_ok'], ['beta', 'cas27', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 59, 86),
    "I_coil": (False, ['beta_ok', 'cond_strain_ok', 'net_positive', 'peak_field_ok', 'recirc_ok', 'sustainment_ok', 'wall_load_ok', 'wp_stress_ok'], ['beta', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 68, 90),
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
    assert len(group["constraints_unreachable"]) == 9


def test_I_coil_reaches_the_field_constraints_through_calcs(report):
    """WI-035 gave the coil-current lever the field-side constraints (beta_ok,
    peak_field_ok, wp_stress_ok). WI-037 extends its reach through the ISS04
    sustainment chain: B feeds tau_E, the ash/fuel state, and p_aux_required,
    so I_coil now also reaches sustainment_ok and — through the computed fuel —
    the whole fusion-derived chain (net_positive, recirc_ok, wall_load_ok).
    This is the structural close of discovery row 20260823-magnet-technology-ab#4
    ("field is never rewarded"): the field lever finally has a path to fusion
    power. All computed-vs-bound except net_positive (computed vs literal 0)."""
    group = group_by_axis(report, "I_coil")
    reached = {c["source_local_identity"]: c for c in group["constraints_reachable"]}
    # WI-036 adds cond_strain_ok: the winding-pack sizing chain runs off I_coil,
    # so the conductor's own check is reached by the same lever that reaches the
    # structure's -- the conductor is not left unchecked by the field sweep.
    assert set(reached) == {
        "beta_ok", "peak_field_ok", "wp_stress_ok", "cond_strain_ok",
        "sustainment_ok", "net_positive", "recirc_ok", "wall_load_ok",
    }
    for name in ("beta_ok", "peak_field_ok", "wp_stress_ok", "cond_strain_ok", "sustainment_ok"):
        constraint = reached[name]
        assert constraint["operator"] == "<="
        assert constraint["bound_vs_bound"] is False
        assert [o["class"] for o in constraint["operands"]] == ["computed", "bound"]
        computed, bound = constraint["operands"]
        assert computed["reached"] is True and bound["reached"] is False
    assert "beta" in group["objectives_reachable"]


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


def test_the_declared_tie_extends_reach_through_the_field(report):
    """WI-035 inverted the old invariant: magnet__R0 now feeds 'Coil Set Axis
    Field', so declaring the physical-identity tie ADDS the field-side reach —
    beta_ok, peak_field_ok, wp_stress_ok — that plain R (plant geometry only)
    cannot see. Before WI-035 the tie changed nothing; that this test had to
    flip is the design response the rubric row asked for."""
    plain = group_by_axis(report, "R")
    tied = group_by_axis(report, "R+tie")
    plain_reach = {c["source_local_identity"] for c in plain["constraints_reachable"]}
    tied_reach = {c["source_local_identity"] for c in tied["constraints_reachable"]}
    assert plain_reach < tied_reach
    # WI-037: plain R now reaches beta_ok on its own (R feeds tau_E through the
    # sustainment chain, the converged ash moves the fuel peaks, and beta reads
    # the computed fuel), so beta_ok left the tie-exclusive set; the tie still
    # adds the two field-side fences only R0 can see.
    # WI-036 adds cond_strain_ok to the tie-exclusive set for the same reason as
    # wp_stress_ok: both hang off B_peak, which only R0 feeds.
    assert tied_reach - plain_reach == {"peak_field_ok", "wp_stress_ok", "cond_strain_ok"}
    # WI-036: the objective sets are equal again EXCEPT magnet_capital, which is
    # now tie-exclusive. c_coil = k_coil * R0 means the winding length -- and so
    # the ampere-metre conductor cost -- responds to the major radius, and only
    # the tie carries R0. Under WI-037 the two sets were equal and the tie's
    # added value was purely fence-side; that is no longer the whole story.
    assert set(tied["objectives_reachable"]) - set(plain["objectives_reachable"]) == {"magnet_capital"}
    assert "beta" in tied["objectives_reachable"]
    # WI-036 closed the disclosed WI-035 limitation recorded here: the winding
    # length was the held c_coil, so the decomposed rollup could not respond to R.
    # It is now c_coil = k_coil * R0, so magnet_capital DOES respond to the major
    # radius through the winding length (MR-WI036-4).
    assert "magnet_capital_1cfe" in tied["objectives_reachable"]
    assert "magnet_capital" in tied["objectives_reachable"]
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
