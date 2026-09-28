"""Artificial reporter contract tests; no reference observations or model runs."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

SPEC = importlib.util.spec_from_file_location("reporter", Path(__file__).parents[1] / "scripts/compare_fixed_point.py")
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


def fixture():
    rows = []
    for name, axis in [("structure", "structural"), ("prediction", "derived"), ("component", "cost")]:
        rows.append(dict(id=name, axis=axis, formal=True, meaning="Artificial test quantity", unit="MW" if axis == "derived" else "USD" if axis == "cost" else "1", aggregation="single artificial unit", producers=[], calculation=None, role="derived", depends_on=[], included_scope=["artificial_scope"], excluded_scope=[], technology="artificial_technology", validity_limits=[], reference_required=["artificial evidence"], conversion={"basis": "artificial_basis", "allowed_units": ["MW" if axis == "derived" else "USD" if axis == "cost" else "1"], "allowed_basis_conversions": []}, verification=[], applicability="supported", reference_value=None, exclusion=None))
    manifest = dict(schema_version=1, package_path="artificial", prefix="artificial", quantities=rows, accounting=[], required_constraints=["artificial_constraint"])
    observations = dict(schema_version=1, run_kind="blind", execution_status="completed", constraints={"artificial_constraint": True}, extrapolations=[], quantities={})
    for q in rows:
        side = dict(value=1, unit=q["unit"], basis="artificial_basis", scope=q["included_scope"], technology=q["technology"])
        observations["quantities"][q["id"]] = dict(model=copy.deepcopy(side), reference=copy.deepcopy(side), model_valid=True, applicability_evidence="Artificial evidence")
    observations["quantities"]["structure"]["structural_evidence"] = dict(corresponds=True, evidence="Artificial correspondence evidence")
    return manifest, observations


def row(report, name="prediction"):
    return next(x for x in report["rows"] if x["id"] == name)


def test_exact_match_and_complete_denominator():
    m, o = fixture()
    report = r.compare(m, o)
    assert report["pass"] and len(report["rows"]) == len(m["quantities"])
    del o["quantities"]["prediction"]
    report = r.compare(m, o)
    assert not report["pass"] and len(report["rows"]) == 3
    assert row(report)["issues"] == ["missing_observation"]


@pytest.mark.parametrize("name,boundary,direction,expected", [
    ("prediction", 1/3, None, True), ("prediction", 3, None, True),
    ("prediction", 1/3, -math.inf, False), ("prediction", 3, math.inf, False),
    ("component", .5, None, True), ("component", 2, None, True),
    ("component", .5, -math.inf, False), ("component", 2, math.inf, False),
])
def test_inclusive_exact_bands_without_tolerance(name, boundary, direction, expected):
    m, o = fixture()
    o["quantities"][name]["model"]["value"] = boundary if direction is None else math.nextafter(boundary, direction)
    assert r.compare(m, o)["pass"] == expected


@pytest.mark.parametrize("value", [None, 0, -1, math.inf, -math.inf, math.nan, "1", True])
def test_invalid_denominator_fails_closed(value):
    m, o = fixture()
    o["quantities"]["prediction"]["reference"]["value"] = value
    assert row(r.compare(m, o))["status"] == "blocked"


@pytest.mark.parametrize("side", ["model", "reference"])
def test_unit_and_authorized_basis_conversion_preserve_raw(side):
    m, o = fixture()
    q = m["quantities"][1]
    q["conversion"]["allowed_units"].append("kW")
    q["conversion"]["allowed_basis_conversions"] = [dict(id="artificial_double", **{"from": "artificial_half", "to": "artificial_basis"}, factor=2, evidence="Artificial exact doubling for test only")]
    value = o["quantities"]["prediction"][side]
    value.update(value=500, unit="kW", basis="artificial_half", basis_conversion="artificial_double")
    report = r.compare(m, o)
    assert report["pass"]
    assert row(report)[side]["raw"]["value"] == 500
    assert row(report)[side]["adjusted"]["value"] == 1
    assert len(row(report)[side]["conversions"]) == 2


@pytest.mark.parametrize("field,value", [("unit", "kW"), ("basis", "unsupported_year"), ("scope", ["other"]), ("technology", "other")])
def test_unsupported_conversion_scope_technology(field, value):
    m, o = fixture()
    o["quantities"]["prediction"]["reference"][field] = value
    assert not r.compare(m, o)["pass"]


def test_supported_unit_must_have_same_dimension():
    m, o = fixture()
    m["quantities"][1]["conversion"]["allowed_units"].append("kg")
    o["quantities"]["prediction"]["reference"]["unit"] = "kg"
    assert "reference:unsupported_unit" in row(r.compare(m, o))["issues"]


@pytest.mark.parametrize("role", ["supplied", "held"])
def test_supplied_and_held_receive_no_prediction_credit(role):
    m, o = fixture()
    m["quantities"][1]["role"] = role
    report = r.compare(m, o)
    assert row(report)["status"] == "informational_match"
    assert not row(report)["independent_credit"]
    assert not report["axes"]["derived"]["pass"]


def test_validity_applicability_and_dependencies():
    m, o = fixture()
    o["quantities"]["prediction"]["model_valid"] = False
    m["quantities"][2]["depends_on"] = ["prediction"]
    report = r.compare(m, o)
    assert "model_invalid" in row(report)["issues"]
    assert "blocked_dependency" in row(report, "component")["issues"]
    o["quantities"]["prediction"]["model_valid"] = True
    m["quantities"][1]["applicability"] = "unresolved"
    assert not r.compare(m, o)["pass"]
    m["quantities"][1]["applicability"] = "conditional"
    assert r.compare(m, o)["pass"]
    o["quantities"]["prediction"]["applicability_evidence"] = ""
    assert not r.compare(m, o)["pass"]


@pytest.mark.parametrize("evidence", [None, {"corresponds": True, "evidence": ""}, {"corresponds": False, "evidence": "Mismatch"}])
def test_structural_requires_actual_evidence(evidence):
    m, o = fixture()
    if evidence is None:
        del o["quantities"]["structure"]["structural_evidence"]
    else:
        o["quantities"]["structure"]["structural_evidence"] = evidence
    assert not r.compare(m, o)["pass"]


def accounting_fixture():
    m, o = fixture()
    for name in ("excluded", "aggregate", "plant"):
        q = copy.deepcopy(m["quantities"][2])
        q["id"] = name
        q["exclusion"] = "C220107" if name == "excluded" else None
        m["quantities"].append(q)
        o["quantities"][name] = copy.deepcopy(o["quantities"]["component"])
    for name, value in [("aggregate", 2), ("plant", 2)]:
        for side in ("model", "reference"):
            o["quantities"][name][side]["value"] = value
    m["accounting"] = [dict(id="sum", parent="aggregate", children=["component", "excluded"], meaning="Artificial disjoint sum"), dict(id="plant_sum", parent="plant", children=["aggregate"], meaning="Artificial plant sum")]
    return m, o


def test_reconciliation_and_c220107_transitive_disclosure():
    m, o = accounting_fixture()
    report = r.compare(m, o)
    assert all(x["status"] == "pass" for x in report["accounting"])
    for name in ("aggregate", "plant"):
        assert row(report, name)["contains_C220107"]
        assert not row(report, name)["independent_credit"]
        assert "footnoted" in row(report, name)["disclosure"]
    o["quantities"]["aggregate"]["model"]["value"] = 2.1
    assert not r.compare(m, o)["pass"]
    del o["quantities"]["excluded"]
    assert any(x["status"] == "blocked" for x in r.compare(m, o)["accounting"])


def test_parent_and_child_double_count_rejected():
    m, o = accounting_fixture()
    m["accounting"][1]["children"].append("component")
    with pytest.raises(r.InvalidInput, match="double counts"):
        r.compare(m, o)


@pytest.mark.parametrize("status", ["failed", "refused"])
def test_failed_execution_retained(status):
    m, o = fixture()
    o["execution_status"] = status
    report = r.compare(m, o)
    assert not report["pass"] and report["execution_status"] == status
    assert all(x["status"] == "blocked" for x in report["rows"])


def test_constraints_extrapolation_and_conditioned_separation():
    m, o = fixture()
    o["constraints"]["artificial_constraint"] = False
    o["extrapolations"] = ["Artificial out-of-domain flag"]
    report = r.compare(m, o)
    assert report["numerical_comparison_pass"] and report["pass"]
    assert not report["physical_feasibility"] and report["extrapolations"] == o["extrapolations"]
    o["constraints"]["artificial_constraint"] = True
    o["extrapolations"] = []
    o["run_kind"] = "conditioned"
    report = r.compare(m, o)
    assert report["numerical_comparison_pass"] and not report["blind_comparison_pass"] and not report["pass"]
    o["constraints"] = {}
    assert not r.compare(m, o)["constraints_complete"]


@pytest.mark.parametrize("key,value", [("role", "derived"), ("formal", False), ("conversion_factor", 2)])
def test_input_cannot_override_frozen_decisions(key, value):
    m, o = fixture()
    o["quantities"]["prediction"][key] = value
    with pytest.raises(r.InvalidInput, match="unknown"):
        r.compare(m, o)


def test_malformed_and_duplicate_json(tmp_path):
    m, o = fixture()
    o["quantities"]["prediction"]["model_valid"] = "true"
    with pytest.raises(r.InvalidInput):
        r.compare(m, o)
    path = tmp_path / "duplicate.json"
    path.write_text('{"role":"held","role":"derived"}')
    with pytest.raises(r.InvalidInput, match="duplicate"):
        r.load_json(path)


def test_cli_deterministic_and_fail_closed(tmp_path):
    m, o = fixture()
    manifest, obs, output = [tmp_path / f"{name}.json" for name in ("manifest", "input", "report")]
    manifest.write_text(json.dumps(m))
    obs.write_text(json.dumps(o))
    command = [sys.executable, str(Path(r.__file__)), "--manifest", str(manifest), "--input", str(obs), "--output", str(output)]
    assert subprocess.run(command).returncode == 0
    first = output.read_bytes()
    assert subprocess.run(command).returncode == 0 and output.read_bytes() == first
    obs.write_text('{"bad":true}')
    assert subprocess.run(command).returncode == 2
    assert not json.loads(output.read_text())["pass"]


def test_structural_null_values_require_correspondence_not_numbers():
    m, o = fixture()
    for side in ("model", "reference"):
        o["quantities"]["structure"][side]["value"] = None
    report = r.compare(m, o)
    assert report["pass"]
    assert row(report, "structure")["ratio"] is None
    assert row(report, "structure")["model"]["adjusted"]["value"] is None


def test_missing_formal_held_row_cannot_disappear_from_success():
    m, o = fixture()
    q = copy.deepcopy(m["quantities"][1])
    q.update(id="held_input", role="held")
    m["quantities"].append(q)
    assert not r.compare(m, o)["pass"]


def test_accounting_incompatible_basis_cannot_pass():
    m, o = accounting_fixture()
    m["quantities"][3]["conversion"]["basis"] = "different_basis"
    for side in ("model", "reference"):
        o["quantities"]["excluded"][side]["basis"] = "different_basis"
    report = r.compare(m, o)
    assert not report["pass"]
    assert report["accounting"][0]["status"] == "blocked"


def test_actual_manifest_complete_synthetic_denominator():
    package = Path(__file__).parents[1] / ".project/active/aries-comparison-preparation/package"
    m = r.load_json(package / "manifest.json")
    o = r.load_json(package / "synthetic-input.json")
    report = r.compare(m, o)
    assert len(report["rows"]) == len(m["quantities"])
    assert {x["id"] for x in report["rows"]} == {x["id"] for x in m["quantities"]}
    assert not report["pass"]
    assert report == r.load_json(package / "synthetic-report.json")


@pytest.mark.parametrize("value", [None, math.nan, math.inf, -math.inf])
def test_nonfinite_or_missing_model_value(value):
    m, o = fixture()
    o["quantities"]["prediction"]["model"]["value"] = value
    assert not r.compare(m, o)["pass"]


def test_arbitrary_basis_factor_and_unknown_constraint_cannot_authorize_pass():
    m, o = fixture()
    o["quantities"]["prediction"]["reference"]["factor"] = 1
    with pytest.raises(r.InvalidInput, match="unknown"):
        r.compare(m, o)
    del o["quantities"]["prediction"]["reference"]["factor"]
    o["constraints"]["invented_constraint"] = True
    assert not r.compare(m, o)["pass"]


def test_malformed_required_field_and_independent_role():
    m, o = fixture()
    m["quantities"][1]["role"] = "independent"
    assert row(r.compare(m, o))["independent_credit"]
    del o["quantities"]["prediction"]["reference"]["unit"]
    with pytest.raises(r.InvalidInput, match="missing"):
        r.compare(m, o)


def test_c220107_propagates_through_nonadditive_dependency_chains():
    m, o = accounting_fixture()
    # Reverse order tests transitive propagation independent of manifest order.
    for name, dependency, axis in [("lcoe", "idc", "diagnostic"), ("idc", "installation", "cost"), ("installation", "aggregate", "cost")]:
        q = copy.deepcopy(m["quantities"][2])
        q.update(id=name, depends_on=[dependency], axis=axis, formal=axis != "diagnostic")
        m["quantities"].append(q)
        o["quantities"][name] = copy.deepcopy(o["quantities"]["component"])
    report = r.compare(m, o)
    for name in ("installation", "idc", "lcoe"):
        result = row(report, name)
        assert result["contains_C220107"]
        assert not result["independent_credit"]
        assert "depends on excluded C220107" in result["disclosure"]


@pytest.mark.parametrize("value", [.01, 1, 100])
def test_lcoe_is_diagnostic_without_acceptance_band(value):
    m, o = fixture()
    q = copy.deepcopy(m["quantities"][1])
    q.update(id="lcoe", axis="diagnostic", formal=False)
    m["quantities"].append(q)
    o["quantities"]["lcoe"] = copy.deepcopy(o["quantities"]["prediction"])
    o["quantities"]["lcoe"]["model"]["value"] = value
    report = r.compare(m, o)
    result = row(report, "lcoe")
    assert result["ratio"] == value and result["status"] == "diagnostic"
    assert "band" not in result and not result["independent_credit"]
    assert report["pass"]


def test_actual_lcoe_conventions_have_no_acceptance_band():
    package = Path(__file__).parents[1] / ".project/active/aries-comparison-preparation/package"
    report = r.compare(r.load_json(package / "manifest.json"), r.load_json(package / "synthetic-input.json"))
    for name in ("lcoe_dcf", "lcoe_1cfe"):
        result = row(report, name)
        assert result["axis"] == "diagnostic" and "band" not in result
        assert not result["independent_credit"]


def test_conditioned_supplied_cycle_output_never_gets_independent_credit():
    m, o = fixture()
    m["quantities"][1]["role"] = "independent"
    o["run_kind"] = "conditioned"
    o["notes"] = "Artificial conditioned held-cycle diagnostic: cycle output supplied externally"
    report = r.compare(m, o)
    result = row(report)
    assert result["ratio"] == 1 and result["status"] == "pass"
    assert report["numerical_comparison_pass"] and not report["blind_comparison_pass"]
    assert all(not result["independent_credit"] for result in report["rows"])


def test_actual_nonadditive_costs_and_both_lcoes_disclose_c220107():
    package = Path(__file__).parents[1] / ".project/active/aries-comparison-preparation/package"
    report = r.compare(r.load_json(package / "manifest.json"), r.load_json(package / "synthetic-input.json"))
    for name in ("C220111", "CAS29", "CAS30", "CAS50", "CAS60", "total_capital", "CAS90_1cfe", "lcoe_dcf", "lcoe_1cfe"):
        result = row(report, name)
        assert result["contains_C220107"] and "disclosure" in result
        assert not result["independent_credit"]


@pytest.mark.parametrize("execution_status", ["failed", "refused"])
def test_stale_true_constraints_do_not_establish_feasibility(execution_status):
    m, o = fixture()
    o["execution_status"] = execution_status
    report = r.compare(m, o)
    assert report["constraints_complete"]
    assert report["constraints"] == {"artificial_constraint": True}
    assert not report["physical_feasibility"] and not report["pass"]


def test_actual_passthrough_rows_never_receive_prediction_credit():
    package = Path(__file__).parents[1] / ".project/active/aries-comparison-preparation/package"
    report = r.compare(r.load_json(package / "manifest.json"), r.load_json(package / "synthetic-input.json"))
    for name in ("fit_cavity_y", "fit_exterior_x", "installed_wallplug"):
        result = row(report, name)
        assert result["role"] in ("held", "supplied")
        assert not result["independent_credit"]
