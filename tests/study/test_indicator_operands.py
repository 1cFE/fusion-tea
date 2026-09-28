"""Actual IFE multiplication leaves and bounded refusal semantics for indicators."""
from copy import deepcopy
import json
from pathlib import Path

import jsonschema
import pytest
from scripts.study import indicators as tool, manifest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "exploration/ife_e2e/generated"
STUDIES = PACKAGE.parent / "studies"


def actual_entry():
    entries = json.loads((PACKAGE / "contracts/model_contract.json").read_text())["constraint_catalog"]["concrete_entries"]
    return next(e for e in entries if e["source_local_identity"] == "viability")


def test_actual_multiplication_leaves_remain_ordered():
    operator, leaves = tool.predicate_operands(actual_entry())
    assert operator == ">="
    assert leaves == [{"kind": "feature_ref", "name": name} for name in ("eta", "gain_in", "threshold")]


def test_nested_products_preserve_literals_and_repeated_features():
    entry = actual_entry()
    ir = json.loads(entry["predicate_ir"])
    eta = ir["operands"][0]["operands"][0]
    ir["operands"][0] = {"kind": "operator", "operator": "*", "operands": [
        {"kind": "operator", "operator": "*", "operands": [eta, deepcopy(eta)]},
        {"kind": "literal", "literal": {"value": 2.0}},
    ]}
    entry["predicate_ir"] = json.dumps(ir)
    assert tool.predicate_operands(entry)[1] == [
        {"kind": "feature_ref", "name": "eta"}, {"kind": "feature_ref", "name": "eta"},
        {"kind": "literal", "value": 2.0}, {"kind": "feature_ref", "name": "threshold"}]


@pytest.mark.parametrize("operator", ["+", "/", "**"])
def test_other_nested_operators_are_refused(operator):
    entry = actual_entry()
    ir = json.loads(entry["predicate_ir"])
    ir["operands"][0]["operator"] = operator
    entry["predicate_ir"] = json.dumps(ir)
    with pytest.raises(tool.IndicatorError, match="unsupported nested"):
        tool.predicate_operands(entry)


@pytest.mark.parametrize("arity", [0, 1, 3])
def test_malformed_product_arity_is_refused(arity):
    entry = actual_entry()
    ir = json.loads(entry["predicate_ir"])
    product = ir["operands"][0]
    product["operands"] = [product["operands"][0]] * arity
    entry["predicate_ir"] = json.dumps(ir)
    with pytest.raises(tool.IndicatorError, match="exactly two"):
        tool.predicate_operands(entry)


def test_unknown_nested_kind_is_refused():
    entry = actual_entry()
    ir = json.loads(entry["predicate_ir"])
    ir["operands"][0]["operands"][0] = {"kind": "invocation"}
    entry["predicate_ir"] = json.dumps(ir)
    with pytest.raises(tool.IndicatorError, match="unknown predicate operand kind"):
        tool.predicate_operands(entry)


def test_actual_ife_report_preserves_schema_and_conservative_classification(tmp_path):
    # This regression exercises the physical axes independently of the current study question.
    path = tmp_path / "physical-axes.json"
    prefix = "hif_plant_pkg__hif_plant__"
    path.write_text(json.dumps({"schema_version": "study-axis-declaration/v1", "groups": [
        {"axis": axis, "keys": [{"key": prefix + key, "provenance": "fan_out"}]}
        for axis, key in (("beam_energy_mj", "driver__beam_energy_mj"), ("frequency", "frequency"))
    ]}))
    declaration = tool.read_axis_declaration(path)
    report = tool.build_report(PACKAGE, manifest.load(STUDIES / "manifest.json"), declaration, [])
    jsonschema.validate(report, json.loads((ROOT / "scripts/study/schemas/indicators.v1.schema.json").read_text()))
    assert len(report["groups"]) == 2
    assert report["axis_declaration"]["subset"] is False
    assert {g["axis"] for g in report["groups"]} == {"beam_energy_mj", "frequency"}
    for group in report["groups"]:
        assert group["no_constraint_response"] is False
        assert [e["source_local_identity"] for e in group["constraints_reachable"]] == ["net_positive"]
        heuristic, = group["constraints_unreachable"]
        assert heuristic["source_local_identity"] == "viability"
        assert heuristic["operator"] == ">="
        assert [(o["operand"], o["class"], o["reached"]) for o in heuristic["operands"]] == [
            ("eta", "bound", False), ("gain_in", "bound", False), ("threshold", "bound", False)]
