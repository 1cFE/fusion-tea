"""The five current axis cases, field for field, against the committed package.

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

# WI-046 (goal plant-closure round 1, 2026-09-08): the `availability` axis is renamed
# `availability_direct` -- the lifecycle calendar produces availability; the lever is its
# held-mode switch (design D5). The known answer is re-derived, its no-response claim kept.
CASES = ["availability_direct", "interest_rate", "R", "a", "I_coil"]

# WI-059 (2026-09-15): re-derived from the completed package indicator report.
EXPECTED_SEMANTIC_FINGERPRINT = '17da5a058e674547143f7df8ddb3a71909e4b9f06f465fcdff051b0fb20ac209'

#: axis -> (no_constraint_response, reachable constraints, reachable objectives,
#:          modules fired, channels tainted). Read straight off the Item 1 fixture
#: contract in .project/completed/20260821_run-study-reachability-spike/findings.md, re-derived
#: on the 2.0.0 package after the stellarator model migration (2026-08-21): the
#: qualitative contract is unchanged; R and a fire one more module and taint one
#: more channel because CAS27 is now computed in-package and declared as the
#: `cas27` objective, and each swept attribute is one plant-level entry point.
# WI-051: re-derived by the radius item metadata caller from the native graph.
# WI-057 (2026-09-13, the structural decomposition re-applied onto feat/demo-maturation): re-derived on the
# restructured package -- every count identical; only the entry-point names carry their part's path.
# WI-058 (2026-09-14): the winding length follows the coil bore (k_coil retired, c_coil_ref bound), re-derived
# from the indicator report at semantic 8eb332b9…; what moved per axis: I_coil: fired 86->86, tainted 171->171, constraints +[] -[], objectives +[] -[]; R: fired 89->89, tainted 181->181, constraints +[] -[], objectives +[] -[]; a: fired 82->88, tainted 160->180, constraints +[] -[], objectives +[] -[]; availability_direct: fired 6->6, tainted 18->18, constraints +[] -[], objectives +[] -[]; interest_rate: fired 9->9, tainted 22->22, constraints +[] -[], objectives +[] -[]
# WI-059 (2026-09-15): re-derived from the completed package indicator report.
FIXTURE_CONTRACT = {'I_coil': (False,
            ['beta_ok',
             'burn_hold_ok',
             'cond_strain_ok',
             'cycle_domain_ok',
             'divertor_heat_ok',
             'loop_capacity_ok',
             'loop_pressure_ok',
             'net_positive',
             'peak_field_ok',
             'recirc_ok',
             'reference_conductor_current_ok',
             'sustainment_ok',
             'wall_load_ok',
             'wp_fit_ok',
             'wp_stress_ok'],
            ['beta',
             'cas72',
             'fuel',
             'lcoe',
             'lcoe_1cfe',
             'magnet_capital',
             'magnet_capital_1cfe',
             'operating_heat_coupled',
             'operating_heat_delivered',
             'operating_heat_wallplug',
             'p_aux_required',
             'tau_E',
             'total_capital'],
            97,
            225),
 'R': (False,
       ['beta_ok',
        'burn_hold_ok',
        'cond_strain_ok',
        'cycle_domain_ok',
        'divertor_heat_ok',
        'loop_capacity_ok',
        'loop_pressure_ok',
        'net_positive',
        'peak_field_ok',
        'recirc_ok',
        'reference_conductor_current_ok',
        'sustainment_ok',
        'wall_load_ok',
        'wp_stress_ok'],
       ['beta',
        'cas27',
        'cas72',
        'fuel',
        'lcoe',
        'lcoe_1cfe',
        'magnet_capital',
        'magnet_capital_1cfe',
        'operating_heat_coupled',
        'operating_heat_delivered',
        'operating_heat_wallplug',
        'p_aux_required',
        'tau_E',
        'total_capital'],
       98,
       217),
 'a': (False,
       ['beta_ok',
        'burn_hold_ok',
        'cond_strain_ok',
        'cycle_domain_ok',
        'divertor_heat_ok',
        'loop_capacity_ok',
        'loop_pressure_ok',
        'net_positive',
        'peak_field_ok',
        'recirc_ok',
        'reference_conductor_current_ok',
        'sustainment_ok',
        'wall_load_ok',
        'wp_stress_ok'],
       ['beta',
        'cas27',
        'cas72',
        'fuel',
        'lcoe',
        'lcoe_1cfe',
        'magnet_capital',
        'magnet_capital_1cfe',
        'operating_heat_coupled',
        'operating_heat_delivered',
        'operating_heat_wallplug',
        'p_aux_required',
        'tau_E',
        'total_capital'],
       97,
       216),
 'availability_direct': (True,
                         [],
                         ['cas72', 'fuel', 'lcoe', 'lcoe_1cfe'],
                         6,
                         18),
 'interest_rate': (True, [], ['cas72', 'fuel', 'lcoe', 'lcoe_1cfe'], 9, 22)}


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


def test_availability_direct_reaches_no_constraint(report):
    """The original finding, now mechanical: the availability sweep that ran to
    completion could not have been a design search, because nothing constrains it.

    WI-046 (goal plant-closure round 1, 2026-09-08): the lever is now the lifecycle
    calendar's held-mode switch `availability_direct`. Every nonzero value selects the
    retired periodic chain at that availability, so the sweep's response is the old one
    and still reaches no constraint; the live chain's response to design lives on the
    wall-load axes (`a`, `R`, `I_coil`), which now reach the eleven calendar channels."""
    group = group_by_axis(report, "availability_direct")
    assert group["no_constraint_response"] is True
    assert group["constraints_reachable"] == []
    assert len(group["constraints_unreachable"]) == 20


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
    # WI-047 (goal plant-closure, 2026-09-08) adds divertor_heat_ok: the ledger's absorbed
    # heating is the sustainment chain's alpha heating plus the coupled heating, so every
    # lever that reaches the sustainment chain reaches the computed target peak.
    assert set(reached) == {
        "beta_ok", "peak_field_ok", "wp_stress_ok", "cond_strain_ok",
        "sustainment_ok", "net_positive", "recirc_ok", "wall_load_ok",
        "burn_hold_ok", "loop_pressure_ok", "loop_capacity_ok", "cycle_domain_ok",
        "divertor_heat_ok", "wp_fit_ok", "reference_conductor_current_ok",
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


def test_model_owned_radius_reaches_magnet_and_plasma(report):
    plain = group_by_axis(report, "R")
    reached = {c["source_local_identity"] for c in plain["constraints_reachable"]}
    assert {"peak_field_ok", "wp_stress_ok", "cond_strain_ok", "sustainment_ok"} <= reached
    assert {"beta", "magnet_capital", "magnet_capital_1cfe"} <= set(plain["objectives_reachable"])
    assert len(plain["declared_keys"]) == 1


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


def test_current_heating_reachability(real_package_path, real_manifest_path, tmp_path):
    """Module reachability distinguishes installed reserve from operating demand."""
    axes = tmp_path / "heating-axes.json"
    names = ["p_wallplug_heat", "eta_source_heat", "eta_couple_heat"]
    axes.write_text(json.dumps({"schema_version": "study-axis-declaration/v1", "groups": [
        {"axis": name, "keys": [
            {"key": f"stellarator_09__stellaris__heating__{name}", "provenance": "fan_out"}  # WI-057 (2026-09-13): the key carries its part's path
        ]}
        for name in names
    ]}))
    doc = run_tool(real_package_path, real_manifest_path, axes)
    reserve = group_by_axis(doc, "p_wallplug_heat")
    assert {c["source_local_identity"] for c in reserve["constraints_reachable"]} == {
        "sustainment_ok", "divertor_heat_ok"
    }
    assert reserve["trace_size"] == {"modules_fired": 21, "channels_tainted": 32}
    assert reserve["objectives_reachable"] == ["lcoe", "lcoe_1cfe", "total_capital"]
    for stage in ("source", "couple"):
        group = group_by_axis(doc, f"eta_{stage}_heat")
        assert {c["source_local_identity"] for c in group["constraints_reachable"]} == {
            "cycle_domain_ok", "divertor_heat_ok", "loop_capacity_ok", "loop_pressure_ok",
            "net_positive", "recirc_ok", "sustainment_ok",
            f"heating_{stage}_positive_ok", f"heating_{stage}_upper_ok",
        }
        # WI-059: unchanged reached modules; Structure Cost adds its legacy_cost diagnostic.
        assert group["trace_size"] == {"modules_fired": 62, "channels_tainted": 113}
        assert {
            "operating_heat_coupled", "operating_heat_delivered", "operating_heat_wallplug"
        } <= set(
            group["objectives_reachable"]
        )
