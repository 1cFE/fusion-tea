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
                 j_reference=118.8271604938272, price_reference=50.)


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
def calculation(runtime_paths):
    module = importlib.import_module("stellarator_tea.modules.mfe_conductor_grade.conductor_field_capability")
    impl = importlib.import_module("stellarator_tea.handwritten.mfe_conductor_grade.conductor_field_capability_impl")
    assert Path(module.__file__).resolve().is_relative_to(ROOT / "exploration/stellarator_e2e/generated")
    assert impl.AUTO_IMPLEMENTED is False
    fields = tuple(module.Conductor_Field_CapabilityOutput.model_fields)
    assert set(fields) == {"quantity_factor", "j_wp_effective", "cost_per_kAm_effective"}
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
    assert row["cost_per_kAm_effective"] / q == pytest.approx(50., rel=1e-14)
    if field == 24.9:
        assert row == dict(quantity_factor=1., j_wp_effective=REFERENCE["j_reference"], cost_per_kAm_effective=50.)


@pytest.mark.parametrize("key", list(REFERENCE))
@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_all_nonfinite_inputs_have_named_errors(calculation, key, value):
    with pytest.raises(ValueError, match="Conductor Field Capability:.*" + key):
        calculation(REFERENCE | {key: value})


@pytest.mark.parametrize("key,value", [
    *[(key, value) for key in REFERENCE if key != "price_reference" for value in (0., -1.)],
    ("price_reference", -1.),
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
    dict(B_design=249., field_exponent=2., price_reference=1e308),
])
def test_finite_extremes_fail_deliberately(calculation, overrides):
    with pytest.raises(ValueError, match="Conductor Field Capability:"):
        calculation(REFERENCE | overrides)


def test_free_reference_price_is_allowed_without_changing_quantity(calculation):
    free = calculation(REFERENCE | dict(B_design=30., price_reference=0.))
    priced = calculation(REFERENCE | dict(B_design=30.))
    assert free["cost_per_kAm_effective"] == 0.
    assert free["quantity_factor"] == priced["quantity_factor"]
    assert free["j_wp_effective"] == priced["j_wp_effective"]


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
def test_reference_preserves_every_audited_wi040_channel_and_verdict(evaluate):
    from tests.models.current_mfe_regressions import WI059_REPLAY
    baseline = json.loads((ROOT / "work/completed/20260914_WI-038_conductor-grade-lever/baseline-before.json").read_text())
    assert len(baseline["channels"]) == 174
    assert len(baseline["verdicts"]) == 18
    row = evaluate({key.removeprefix(P): value for key, value in WI059_REPLAY.items()})
    assert {key: row.outputs[key] for key in baseline["channels"]} == baseline["channels"]
    assert verdicts(row) == baseline["verdicts"]
    assert output(row, "magnet__conductor_grade__quantity_factor") == 1.


@pytest.mark.codegen_available
@pytest.mark.parametrize("field", [27.5, 30.])
def test_purchased_envelope_prices_each_volume_once_and_keeps_demand_separate(evaluate, field):
    # Freeze reference j, family, price anchor, composition, geometry and 20 K state.
    before = evaluate()
    after = evaluate({"magnet__winding_pack__B_max": field})
    q = (field / 24.9) ** .6
    assert output(after, "magnet__conductor_grade__quantity_factor") == pytest.approx(q)
    assert output(after, "magnet__conductor_grade__j_wp_effective") == pytest.approx(118.8271604938272 / q)
    proportional = ["wp_volume__vol_winding_pack", "material_inventory__tape_volume",
                    "material_inventory__material_cost", "winding_procurement__tape_cost"]
    proportional += ["material_inventory__" + kind + material
                     for kind in ("mass_", "cost_") for material in ("copper", "solder", "steel", "helium")]
    for suffix in proportional:
        assert output(after, "magnet__" + suffix) == pytest.approx(q * output(before, "magnet__" + suffix), rel=1e-12)
    for suffix, factor in (("wp_sizing__wp_side", math.sqrt(q)),
                           ("wp_stress__sigma_wp", 1 / math.sqrt(q)),
                           ("cond_strain__eps_cond", 1 / math.sqrt(q))):
        assert output(after, "magnet__" + suffix) == pytest.approx(factor * output(before, "magnet__" + suffix), rel=1e-12)
    for suffix in ("field_calc__B_axis", "peak_field_calc__B_peak", "winding_pack_cost__cost",
                   "magnet_cost__capital_cost", "winding_procurement__conductor_length",
                   "winding_procurement__winding_fabrication_cost", "material_inventory__helium_density"):
        assert output(after, "magnet__" + suffix) == output(before, "magnet__" + suffix)
    # Additive account catches q applied twice to inventory or to the full pack cost.
    procurement = sum(output(after, "magnet__" + suffix) for suffix in (
        "winding_procurement__tape_cost", "material_inventory__material_cost",
        "winding_procurement__winding_fabrication_cost"))
    assert output(after, "magnet__winding_procurement__cost") == pytest.approx(procurement, rel=1e-14)
    for suffix in ("cryoplant__cryo_elec__p_elec", "cryoplant__aux_cooling__cryo_cost",
                   "cryoplant__aux_cooling__cost", "total_capital__total_capital"):
        assert output(after, suffix) > output(before, suffix)
    assert verdicts(after)["peak_field_ok"] == "satisfied"


@pytest.mark.codegen_available
def test_crossed_operating_current_and_envelope_verdicts(evaluate):
    low_capacity = evaluate({"magnet__winding_pack__B_max": 24.})
    high_current = evaluate({"magnet__coil__I_coil": 17e6})
    purchased = evaluate({"magnet__coil__I_coil": 17e6, "magnet__winding_pack__B_max": 30.})
    reference = evaluate()
    assert verdicts(low_capacity)["peak_field_ok"] == "violated"
    assert verdicts(high_current)["peak_field_ok"] == "violated"
    assert verdicts(purchased)["peak_field_ok"] == "satisfied"
    assert output(low_capacity, "magnet__peak_field_calc__B_peak") == output(reference, "magnet__peak_field_calc__B_peak")
    assert output(high_current, "magnet__peak_field_calc__B_peak") > output(reference, "magnet__peak_field_calc__B_peak")
    assert output(purchased, "magnet__peak_field_calc__B_peak") == output(high_current, "magnet__peak_field_calc__B_peak")
    assert output(high_current, "magnet__conductor_grade__quantity_factor") == 1.
    assert output(purchased, "magnet__winding_procurement__cost") > output(high_current, "magnet__winding_procurement__cost")
