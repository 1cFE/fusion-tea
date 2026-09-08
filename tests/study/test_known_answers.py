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
    # WI-045 the primary loop and the temperature-compatible cycle (goal
    # plant-closure round 1, 2026-09-08); was 39e931fa... at WI-044 (the magnet
    # chain sees the coil bore, 2026-09-07), baab7e4c... at WI-043 (two-sided sustainment condition,
    # 2026-09-07), c37fb58a... at WI-042 (sourced helium-ash profile, 2026-09-05),
    # d468f3b6... at WI-041 (source-anchored wall-load fence, 2026-09-04) and
    # 48731d15... at WI-039 (heating power chain, 2026-09-03)
    "a331cd82e48f19d5ce2c684188abce9b8da07ab408576c7164880c9d44d4bc92"
)

#: axis -> (no_constraint_response, reachable constraints, reachable objectives,
#:          modules fired, channels tainted). Read straight off the Item 1 fixture
#: contract in .project/completed/20260821_run-study-reachability-spike/findings.md, re-derived
#: on the 2.0.0 package after the stellarator model migration (2026-08-21): the
#: qualitative contract is unchanged; R and a fire one more module and taint one
#: more channel because CAS27 is now computed in-package and declared as the
#: `cas27` objective, and each swept attribute is one plant-level entry point.
FIXTURE_CONTRACT = {
    # WI-045 (goal plant-closure round 1, 2026-09-08) re-derived every expectation file on
    # the loop-and-cycle package. Three verdicts added (loop_pressure_ok, loop_capacity_ok,
    # cycle_domain_ok). What moved, read off the report: the reactor source heat, the
    # primary loop and the cycle sit downstream of the fusion power, so every axis that
    # reaches `fusion` (R, R+tie, a, I_coil) fires the three new modules and reaches the
    # three new constraints, and their traces grow (R, a: 71 -> 77 fired, 104 -> 127
    # tainted; R+tie: 76 -> 82, 109 -> 132; I_coil: 73 -> 79, 99 -> 122). availability
    # and interest_rate are unchanged (6/8 and 8/11): neither reaches the loop, and the
    # thirteen constraints are all unreachable from them. Counts are read from the report,
    # never fitted.
    # WI-044 (goal minor-radius round 1, 2026-09-07) had re-derived every file on the
    # coil-bore package; WI-043 (goal burn-control round 1, 2026-09-07) had added
    # burn_hold_ok on every axis reaching the sustainment operand; earlier history in git.
    "availability": (True, [], ['cas72', 'fuel', 'lcoe', 'lcoe_1cfe'], 6, 8),
    "interest_rate": (True, [], ['cas72', 'lcoe', 'lcoe_1cfe'], 8, 11),
    "R": (False, ['beta_ok', 'burn_hold_ok', 'cond_strain_ok', 'cycle_domain_ok', 'loop_capacity_ok', 'loop_pressure_ok', 'net_positive', 'peak_field_ok', 'recirc_ok', 'sustainment_ok', 'wall_load_ok', 'wp_stress_ok'], ['beta', 'cas27', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 77, 127),
    "R+tie": (False, ['beta_ok', 'burn_hold_ok', 'cond_strain_ok', 'cycle_domain_ok', 'loop_capacity_ok', 'loop_pressure_ok', 'net_positive', 'peak_field_ok', 'recirc_ok', 'sustainment_ok', 'wall_load_ok', 'wp_stress_ok'], ['beta', 'cas27', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 82, 132),
    "a": (False, ['beta_ok', 'burn_hold_ok', 'cond_strain_ok', 'cycle_domain_ok', 'loop_capacity_ok', 'loop_pressure_ok', 'net_positive', 'peak_field_ok', 'recirc_ok', 'sustainment_ok', 'wall_load_ok', 'wp_stress_ok'], ['beta', 'cas27', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 77, 127),
    "I_coil": (False, ['beta_ok', 'burn_hold_ok', 'cond_strain_ok', 'cycle_domain_ok', 'loop_capacity_ok', 'loop_pressure_ok', 'net_positive', 'peak_field_ok', 'recirc_ok', 'sustainment_ok', 'wall_load_ok', 'wp_stress_ok'], ['beta', 'cas72', 'fuel', 'lcoe', 'lcoe_1cfe', 'magnet_capital', 'magnet_capital_1cfe', 'p_aux_required', 'tau_E', 'total_capital'], 79, 122),
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
    assert len(group["constraints_unreachable"]) == 13  # WI-045: three loop/cycle fences joined the ten (WI-043: burn_hold_ok joined the nine)


def test_I_coil_reaches_the_field_constraints_through_calcs(report):
    """WI-035 gave the coil-current lever the field-side constraints (beta_ok,
    peak_field_ok, wp_stress_ok). WI-037 extends its reach through the ISS04
    sustainment chain: B feeds tau_E, the ash/fuel state, and p_aux_required,
    so I_coil now also reaches sustainment_ok and — through the computed fuel —
    the whole fusion-derived chain (net_positive, recirc_ok, wall_load_ok).
    This is the structural close of discovery row 20260823-magnet-technology-ab#4
    ("field is never rewarded"): the field lever finally has a path to fusion
    power. Computed-vs-bound throughout, with two exceptions: net_positive is
    computed vs a literal 0, and since WI-039 sustainment_ok is computed vs
    *computed* — its installed side is the heating chain's coupled power, not the
    held p_input it used to be."""
    group = group_by_axis(report, "I_coil")
    reached = {c["source_local_identity"]: c for c in group["constraints_reachable"]}
    # WI-036 adds cond_strain_ok: the winding-pack sizing chain runs off I_coil,
    # so the conductor's own check is reached by the same lever that reaches the
    # structure's -- the conductor is not left unchecked by the field sweep.
    # WI-043 adds burn_hold_ok: the lower half of the sustainment condition reads the
    # same computed operand, so every lever that reaches sustainment_ok reaches it.
    # WI-045 (goal plant-closure, 2026-09-08) adds the two loop fences and the cycle
    # domain fence: the reactor source heat sizes the loop's flow from the fusion power,
    # so every lever that reaches fusion reaches loop_pressure_ok, loop_capacity_ok and
    # cycle_domain_ok (the cycle reads the loop's outlet).
    assert set(reached) == {
        "beta_ok", "peak_field_ok", "wp_stress_ok", "cond_strain_ok",
        "sustainment_ok", "net_positive", "recirc_ok", "wall_load_ok",
        "burn_hold_ok", "loop_pressure_ok", "loop_capacity_ok", "cycle_domain_ok",
    }
    # The limit side of each field constraint is a bound design value; sustainment_ok
    # is the one whose limit side is itself computed (WI-039 heating chain), so it
    # gets its own assertion rather than a weakened shared one.
    for name in ("beta_ok", "peak_field_ok", "wp_stress_ok", "cond_strain_ok"):
        constraint = reached[name]
        assert constraint["operator"] == "<="
        assert constraint["bound_vs_bound"] is False
        assert [o["class"] for o in constraint["operands"]] == ["computed", "bound"]
        computed, bound = constraint["operands"]
        assert computed["reached"] is True and bound["reached"] is False

    sustainment = reached["sustainment_ok"]
    assert sustainment["operator"] == "<="
    assert sustainment["bound_vs_bound"] is False
    assert [o["class"] for o in sustainment["operands"]] == ["computed", "computed"]
    required, installed = sustainment["operands"]
    assert required["reached"] is True and installed["reached"] is False
    # burn_hold_ok (WI-043): computed vs the literal 0.0, the net_positive shape, on the
    # sustainment operand -- reached exactly where sustainment_ok's required side is.
    burn_hold = reached["burn_hold_ok"]
    assert burn_hold["operator"] == ">="
    assert burn_hold["bound_vs_bound"] is False
    assert [o["class"] for o in burn_hold["operands"]] == ["computed", "literal"]
    assert burn_hold["operands"][0]["ref"] == required["ref"]
    assert burn_hold["operands"][0]["reached"] is True
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
    flip is the design response the rubric row asked for.

    WI-044 (goal minor-radius round 1, 2026-09-07) flipped it again, at the
    REACHABILITY level only: 'Conductor Peak Field' now takes the radial
    build's coil-centre radius (r_coil_centre), the radial build takes plain R,
    and the trace is module-level (the report's own not_derivable statement:
    intra-module operand dependency is not resolved), so every rb output --
    r_coil_centre included -- counts as tainted when R moves, and plain R
    "reaches" the three magnet fences and magnet_capital exactly as the tie
    does. The executed response still differs: bore_factor, W_mag and the
    winding length read magnet__R0, not plant R, so plain R moves none of
    them (WI-044 evidence/offdesign_points, design D1). The tie's exclusive
    reach is therefore empty on the report; what the tie adds is now only
    visible in executed channels, not in reachability. Restated from the
    report, never patched; the tie-exclusive sets are asserted empty so a
    future package that separates them again has to say so here."""
    plain = group_by_axis(report, "R")
    tied = group_by_axis(report, "R+tie")
    plain_reach = {c["source_local_identity"] for c in plain["constraints_reachable"]}
    tied_reach = {c["source_local_identity"] for c in tied["constraints_reachable"]}
    assert plain_reach == tied_reach
    assert tied_reach - plain_reach == set()
    assert {"peak_field_ok", "wp_stress_ok", "cond_strain_ok"} <= tied_reach
    # WI-044: magnet_capital is reachable from plain R through the same
    # module-level path (rb -> stored energy -> casing mass -> structure cost).
    assert set(tied["objectives_reachable"]) - set(plain["objectives_reachable"]) == set()
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
