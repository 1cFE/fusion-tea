from tests.models.current_mfe_regressions import (CURRENT_PREDICATES, historical_point, assert_historical_native, assert_current_predicates, PARTITIONS)
"""WI-038 conditional field-envelope identities, distinct demand, and deliberate domains.

These are arithmetic/accounting tests, not qualification of the extrapolated REBCO law.
Priced transfer holds the 20 K, reference-density and composition assumptions fixed.
"""
import importlib
import json
import math
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
P = "stellarator_09__stellaris__"
REFERENCE = dict(B_design=24.9, B_reference=24.9, field_exponent=.6,
                 j_reference=118.8271604938272)


@pytest.fixture(scope="module")
def runtime_paths():
    paths = [str(ROOT / "exploration/stellarator_e2e/pkg"),
             str(ROOT / "exploration/stellarator_e2e/studies")]
    if os.environ.get("STOP_PARSER_TEAX_ROOT"):
        paths.append(str(Path(os.environ["STOP_PARSER_TEAX_ROOT"]) / "packages/teax-simkit"))
    for path in paths:
        sys.path.insert(0, path)
    yield
    for path in paths:
        sys.path.remove(path)


@pytest.fixture(scope="module")
def calculation(runtime_paths, optional_analysis):
    module = importlib.import_module("optional_magnet_tea.modules.mfe_conductor_grade.conductor_field_capability")
    impl = importlib.import_module("optional_magnet_tea.handwritten.mfe_conductor_grade.conductor_field_capability_impl")
    assert Path(module.__file__).resolve().is_relative_to(optional_analysis)
    assert impl.AUTO_IMPLEMENTED is False
    fields = tuple(module.Conductor_Field_CapabilityOutput.model_fields)
    assert set(fields) == {"quantity_factor", "j_wp_effective"}
    wrapper = module.Conductor_Field_CapabilityModule()

    def run(values):
        direct = dict(zip(fields, impl.run_conductor_field_capability(
            module.Conductor_Field_CapabilityInput(**values)), strict=True))
        public = wrapper.run(**values).data.model_dump()
        assert direct == public
        return public

    return run


@pytest.mark.parametrize("field,exponent", [(24.9, .6), (20., .6), (27.5, .6), (30., .6), (30., .7)])
def test_named_wrapper_outputs_and_quantity_identities(calculation, field, exponent):
    row = calculation(REFERENCE | dict(B_design=field, field_exponent=exponent))
    q = math.exp(exponent * math.log(field / 24.9))
    assert row["quantity_factor"] == pytest.approx(q, rel=1e-14)
    assert row["j_wp_effective"] * q == pytest.approx(REFERENCE["j_reference"], rel=1e-14)
    if field == 24.9:
        assert row == dict(quantity_factor=1., j_wp_effective=REFERENCE["j_reference"])


@pytest.mark.parametrize("key", list(REFERENCE))
@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_all_nonfinite_inputs_have_named_errors(calculation, key, value):
    with pytest.raises(ValueError, match="Conductor Field Capability:.*" + key):
        calculation(REFERENCE | {key: value})


@pytest.mark.parametrize("key,value", [
    *[(key, value) for key in REFERENCE if key != "price_reference" for value in (0., -1.)],
])
def test_nonphysical_inputs_have_named_errors(calculation, key, value):
    with pytest.raises(ValueError, match="Conductor Field Capability:.*" + key):
        calculation(REFERENCE | {key: value})


@pytest.mark.parametrize("overrides", [
    dict(B_design=1e308, B_reference=1e-308),  # finite inputs, infinite ratio
    dict(B_design=1e-308, B_reference=1e308),  # ratio underflow
    dict(B_design=249., field_exponent=1e308),  # exponentiation overflow
    dict(B_design=2.49, field_exponent=1e308),  # quantity underflow
    dict(B_design=249., field_exponent=308., j_reference=1e-308),  # density underflow
    dict(B_design=2.49, field_exponent=308., j_reference=1e308),  # density overflow
])
def test_finite_extremes_fail_deliberately(calculation, overrides):
    with pytest.raises(ValueError, match="Conductor Field Capability:"):
        calculation(REFERENCE | overrides)


@pytest.fixture(scope="module")
def evaluate(runtime_paths, tmp_path_factory):
    from simkit.study.bridge import CandidateBridge
    import study_route
    evaluator = study_route.prepare(ROOT / "exploration/stellarator_e2e/generated", tmp_path_factory.mktemp("wi038-public"))
    bridge = CandidateBridge(evaluator.entry_models)

    def run(overrides=None):
        result = evaluator.evaluate(bridge.build({P + key: value for key, value in (overrides or {}).items()}))
        assert result.outputs, result
        return result

    return run


def output(row, suffix):
    return row.outputs[P + suffix]


def verdicts(row):
    import study_route
    # Evaluator responses use emitted constraint IDs, not the source-local names.
    catalog = study_route._export_catalog(ROOT / "exploration/stellarator_e2e/generated")
    return study_route._short_verdicts(
        SimpleNamespace(verdicts={key: row.responses[key] for key in catalog}), catalog)


@pytest.mark.codegen_available
def test_supplied_reference_inventory_matches_independent_oracle(evaluate):
    import oracle_entry
    row = evaluate()
    expected = oracle_entry.evaluate({})
    for key, value in expected.items():
        assert row.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
    assert not any('__conductor_grade__' in key for key in row.outputs)


@pytest.mark.codegen_available
@pytest.mark.parametrize("field", [27.5, 30.])
def test_ceiling_changes_no_purchased_inventory_or_operating_demand(evaluate, field):
    before = evaluate()
    after = evaluate({"magnet__winding_pack__B_max": field})
    # MR-7: the former field-grade selection remains an optional helper above.
    # The direct evaluator changes only its ceiling verdict.
    assert before.outputs == after.outputs
    assert verdicts(after)["peak_field_ok"] == "satisfied"


@pytest.mark.codegen_available
def test_crossed_operating_current_and_ceiling_verdicts(evaluate):
    low_capacity = evaluate({"magnet__winding_pack__B_max": 24.})
    high_current = evaluate({"magnet__coil__turn_current": 17e6/308.})
    ceiling = evaluate({"magnet__coil__turn_current": 17e6/308., "magnet__winding_pack__B_max": 30.})
    reference = evaluate()
    assert verdicts(low_capacity)["peak_field_ok"] == "violated"
    assert verdicts(high_current)["peak_field_ok"] == "violated"
    assert verdicts(ceiling)["peak_field_ok"] == "satisfied"
    assert output(low_capacity, "magnet__peak_field_calc__B_peak") == output(reference, "magnet__peak_field_calc__B_peak")
    assert output(high_current, "magnet__peak_field_calc__B_peak") > output(reference, "magnet__peak_field_calc__B_peak")
    assert output(ceiling, "magnet__peak_field_calc__B_peak") == output(high_current, "magnet__peak_field_calc__B_peak")
    for row in (low_capacity, high_current, ceiling):
        assert output(row, "magnet__winding_procurement__cost") == output(reference, "magnet__winding_procurement__cost")
