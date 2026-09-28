"""Real IFE stored execution, independent verification and consumer eligibility."""
from dataclasses import replace
import json
from pathlib import Path

import pytest

from exploration.ife_e2e.studies import oracle_entry as oracle, study_route as route
from scripts.study import manifest, verify
from tests.ife_oracle import BOUNDARIES, PREFIX as P, assert_source_outputs


@pytest.fixture(scope="module")
def executed(tmp_path_factory):
    work = tmp_path_factory.mktemp("ife-native-route")
    overrides = [{}, {"driver__beam_energy_mj": 10.0}, {"frequency": 5.0},
                 BOUNDARIES["counterexample"], BOUNDARIES["zero"]]
    overrides += [point | {"discount_rate": rate}
                  for rate in (0.0, 1e-12, -1e-12, 1e-16, -1e-16)
                  for point in ({}, BOUNDARIES["counterexample"], BOUNDARIES["zero"])]
    points = [{P + k: v for k, v in p.items()} for p in overrides]
    cases, db = route.run_points("ife-native-validation", points, work)
    assert len(cases) == len(points) == 20
    assert all(c.state == "completed" for c in cases)
    identity = route.write_identity_document(route.PACKAGE_DIR, work / "identity.json")
    return cases, db, identity, points


def test_stored_outputs_and_eligibility(executed):
    cases, _, _, points = executed
    by_point = {tuple(sorted(c.inputs.items())): c for c in cases}
    for point in points:
        case = by_point[tuple(sorted(point.items()))]
        assert_source_outputs(case.outputs, {k.removeprefix(P): v for k, v in point.items()})
        assert set(case.outputs) == set(route.CHANNELS.values())
        verdicts = route.short_verdicts(case)
        assert verdicts["viability"] == "satisfied"
        generating = case.outputs[P + "lcoe_calc__net_electric_power"] > 0
        assert verdicts["net_positive"] == ("satisfied" if generating else "violated")
        assert set(route.eligible_prices(case).values()) == {generating}
    zero = by_point[tuple(sorted(points[4].items()))]
    assert zero.outputs[P + "lcoe_calc__net_electric_power"] == 0.0
    assert zero.outputs[P + "hawker_price__price"] == zero.outputs[P + "meier_price__price"] == 0.0


def test_generic_verifier_compares_all_channels_and_predicates(executed):
    _, db, identity, points = executed
    summary = verify.build_summary(route.PACKAGE_DIR, route.MANIFEST_PATH, identity, [db], 100, None, [])
    assert len(summary["channels_checked"]) == 32
    assert summary["verdicts_rederived"] is True
    assert len(summary["constraints_rederived"]) == 2
    assert summary["stores"][0]["sampling"]["sampled_rows"] == len(points)


def test_incompatible_store_is_preserved(executed):
    _, db, _, _ = executed
    before = db.read_bytes()
    from simkit.study.store import IncompatibleStore
    with pytest.raises(IncompatibleStore):
        route.run_points("ife-native-validation", [{P + "frequency": 6.0}], db.parent)
    assert db.read_bytes() == before


@pytest.mark.parametrize("channel", ["hawker_price__price", "pv_factors__construction_factor",
                                     "pv_factors__operation_factor"])
def test_missing_numeric_or_verdict_evidence_is_refused(executed, channel):
    case = executed[0][0]
    outputs = dict(case.outputs)
    outputs.pop(P + channel)
    with pytest.raises(route.RouteError, match="missing required"):
        route.eligible_prices(replace(case, outputs=outputs))
    with pytest.raises(route.RouteError, match="verdicts do not match"):
        route.eligible_prices(replace(case, verdicts={}))


@pytest.mark.parametrize("point", [{"unknown": 1}, {P + "frequency": float("nan")},
                                  {P + "frequency": True}])
def test_invalid_proposals_are_refused(point):
    assert route.validate_proposal(point) is None
    with pytest.raises(oracle.OracleSeamError):
        oracle.evaluate(point)


@pytest.mark.parametrize("years", [0, -1, 1.5])
@pytest.mark.parametrize("name", ["construction_duration", "operational_duration"])
def test_oracle_does_not_truncate_years(name, years):
    with pytest.raises(oracle.OracleSeamError, match="positive integral"):
        oracle.evaluate({P + name: years})


@pytest.mark.parametrize("name", ["construction_years", "operational_years"])
def test_retired_duration_keys_are_refused(name):
    point = {P + "lcoe_calc__" + name: 5.0}
    assert route.validate_proposal(point) is None
    with pytest.raises(oracle.OracleSeamError, match="undeclared entry keys"):
        oracle.evaluate(point)


def test_metadata_and_full_input_mapping():
    loaded = manifest.load(route.MANIFEST_PATH)
    contract = json.loads((route.PACKAGE_DIR / "contracts/model_contract.json").read_text())
    assert set(oracle.ENTRY_KEYS) == {p["qualified_name"] for p in contract["parameters"]}
    assert len(loaded.data["objective_catalog"]) == 32
    assert len(oracle.operand_bindings()) == 2
    axes = json.loads((route.HERE / "axes.json").read_text())["groups"]
    assert len(axes) == 1
    assert axes[0]["axis"] == "discount_rate"
    assert axes[0]["keys"] == [{"key": P + "discount_rate", "provenance": "fan_out"}]
    assert_source_outputs(oracle.evaluate(loaded.data["baseline"]["point"]))


def test_baseline_documents_use_the_stored_identity(tmp_path):
    paths = route.execute_baseline(tmp_path)
    identity = json.loads(paths["identity"].read_text())
    result = json.loads(paths["baseline_result"].read_text())
    assert result["executed_under"]["identity_digest"] == identity["identity"]["digest"]
    assert_source_outputs(result["channels"])
    assert {v["source_local_identity"]: v["status"] for v in result["verdicts"]} == {
        "net_positive": "satisfied", "viability": "satisfied"}


def test_contradictory_recorded_verdict_is_refused(executed):
    case = executed[0][0]
    changed = dict(case.verdicts)
    changed[oracle.NET_GATE] = "violated" if changed[oracle.NET_GATE] == "satisfied" else "satisfied"
    loaded = manifest.load(route.MANIFEST_PATH)
    with pytest.raises(verify.VerifyError, match="verdict mismatch"):
        verify.check_case(replace(case, verdicts=changed), oracle.evaluate, oracle.operand_bindings(),
                          route._catalog_by_constraint_id(route.PACKAGE_DIR),
                          verify.objective_channels(loaded), verify.package_input_values(route.PACKAGE_DIR),
                          case.executable_fingerprint)


def test_eligibility_uses_catalog_names_when_emitted_ids_change(executed, monkeypatch):
    catalog = route._catalog_by_constraint_id(route.PACKAGE_DIR)
    renamed = {cid: f"regenerated-{index}" for index, cid in enumerate(catalog)}
    new_catalog = {renamed[cid]: entry | {"constraint_id": renamed[cid]}
                   for cid, entry in catalog.items()}
    expected = [route.eligible_prices(case) for case in executed[0]]
    monkeypatch.setattr(route, "_catalog_by_constraint_id", lambda package: new_catalog)
    for case, flags in zip(executed[0], expected, strict=True):
        changed = replace(case, verdicts={renamed[cid]: value for cid, value in case.verdicts.items()})
        assert route.eligible_prices(changed) == flags
