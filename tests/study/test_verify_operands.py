"""Re-derive the actual IFE expression and refuse unsupported operand grammar."""
import copy
import json
from pathlib import Path

import pytest

from scripts.study.verify import VerifyError, derive_verdict

ROOT = Path(__file__).resolve().parents[2]
P = "hif_plant_pkg__hif_plant__"


@pytest.fixture
def viability():
    contract = json.loads((ROOT / "exploration/ife_e2e/generated/contracts/model_contract.json").read_text())
    entry = next(e for e in contract["constraint_catalog"]["concrete_entries"]
                 if e["source_local_identity"] == "viability")
    inputs = {p["qualified_name"]: p["default_value"] for p in contract["parameters"]}
    bindings = {entry["constraint_id"]: {
        "eta": {"kind": "input", "key": P + "driver__efficiency"},
        "gain_in": {"kind": "input", "key": P + "gain"},
        "threshold": {"kind": "input", "key": P + "viability__threshold"},
    }}
    return entry, bindings, inputs


@pytest.mark.parametrize("gain,expected", [(99.0, False), (100.0, True), (101.0, True)])
def test_actual_ife_product_below_at_and_above_threshold(viability, gain, expected):
    entry, bindings, inputs = viability
    point = {P + "driver__efficiency": 0.1, P + "gain": gain}
    assert derive_verdict(entry["constraint_id"], entry, bindings, point, inputs, {}) == (expected, 3)


def test_nested_multiplication_counts_feature_occurrences_and_preserves_negation(viability):
    entry, bindings, inputs = viability
    ir = json.loads(entry["predicate_ir"])
    product = ir["operands"][0]
    eta_again = copy.deepcopy(product["operands"][0])
    ir["operands"][0] = {"kind": "operator", "operator": "*", "operands": [product, eta_again]}
    entry["predicate_ir"] = json.dumps(ir)
    entry["is_negated"] = True
    point = {P + "driver__efficiency": 0.1, P + "gain": 100.0}
    # (0.1 * 100) * 0.1 < 10, then negated. eta occurs twice.
    assert derive_verdict(entry["constraint_id"], entry, bindings, point, inputs, {}) == (True, 4)


def test_multiplication_accepts_literal_operands_without_counting_them(viability):
    entry, bindings, inputs = viability
    ir = json.loads(entry["predicate_ir"])
    ir["operands"][0]["operands"][0] = {"kind": "literal", "literal": {"value": 0.1}}
    entry["predicate_ir"] = json.dumps(ir)
    assert derive_verdict(entry["constraint_id"], entry, bindings, {P + "gain": 100.0}, inputs, {}) == (True, 2)


@pytest.mark.parametrize("operator", ["+", "/", "**", "unknown"])
def test_unsupported_arithmetic_is_named_and_refused(viability, operator):
    entry, bindings, inputs = viability
    ir = json.loads(entry["predicate_ir"])
    ir["operands"][0]["operator"] = operator
    entry["predicate_ir"] = json.dumps(ir)
    with pytest.raises(VerifyError, match="unsupported arithmetic operator") as error:
        derive_verdict(entry["constraint_id"], entry, bindings, {}, inputs, {})
    assert entry["constraint_id"] in str(error.value)
    assert repr(operator) in str(error.value)


@pytest.mark.parametrize("arity", [0, 1, 3])
def test_multiplication_arity_is_checked(viability, arity):
    entry, bindings, inputs = viability
    ir = json.loads(entry["predicate_ir"])
    product = ir["operands"][0]
    product["operands"] = [product["operands"][0]] * arity
    entry["predicate_ir"] = json.dumps(ir)
    with pytest.raises(VerifyError, match="two multiplication operands"):
        derive_verdict(entry["constraint_id"], entry, bindings, {}, inputs, {})


def test_nested_missing_binding_is_not_guessed(viability):
    entry, bindings, inputs = viability
    del bindings[entry["constraint_id"]]["eta"]
    with pytest.raises(VerifyError, match="eta.*no published binding"):
        derive_verdict(entry["constraint_id"], entry, bindings, {}, inputs, {})


def test_unsupported_operand_kind_is_refused(viability):
    entry, bindings, inputs = viability
    ir = json.loads(entry["predicate_ir"])
    ir["operands"][0] = {"kind": "invocation"}
    entry["predicate_ir"] = json.dumps(ir)
    with pytest.raises(VerifyError, match="operand kind 'invocation'"):
        derive_verdict(entry["constraint_id"], entry, bindings, {}, inputs, {})
