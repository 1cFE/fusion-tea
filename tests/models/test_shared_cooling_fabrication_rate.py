"""WI-071 shared source interpretation, independent units and native preservation."""
import importlib
import json
import math
from pathlib import Path

import pytest

from tests.models.test_installed_cooling_equipment import runtime, equipment
from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output, P

ROOT = Path(__file__).resolve().parents[2]
KEY = 'heat_transport__equipment_stainless_fabrication_usd2017_per_kg'
E = 'heat_transport__equipment__'
MONEY = {
    'hx_purchase', 'hx_installation', 'exchangers_cost',
    'primary_pipe_purchase', 'primary_pipe_installation', 'primary_piping_cost',
    'secondary_pipe_purchase', 'secondary_pipe_installation', 'secondary_piping_cost',
    'bundle_event_purchase', 'bundle_event_installation', 'bundle_event_removal',
    'replacement_annual', 'purchased_total', 'installation_total', 'installed_total',
    'delivered_total',
}


@pytest.mark.parametrize('ratio', [2., 3.])
def test_source_metric_ton_conversion_and_four_linked_bills(equipment, ratio):
    # ANL printed26 carbon base120000 USD/metric tonne, printed27 ratio2..3.
    raw_rate = 120000.0 / 1000.0 * ratio
    row = equipment(stainless_fabrication_usd2017_per_kg_in=raw_rate)
    converted = raw_rate * 321.9 / 245.1
    for bill, mass, count in [('hx_purchase', 'hx_mass', 18),
                              ('primary_pipe_purchase', 'primary_pipe_mass', 1),
                              ('secondary_pipe_purchase', 'secondary_pipe_mass', 1),
                              ('bundle_event_purchase', 'bundle_mass', 18)]:
        assert row[bill] == pytest.approx(row[mass] * count * converted, rel=2e-14)
    assert row['hx_installation'] == pytest.approx(.026 * row['hx_purchase'])
    assert row['primary_pipe_installation'] == pytest.approx(.5 * row['primary_pipe_purchase'])
    assert row['secondary_pipe_installation'] == pytest.approx(.5 * row['secondary_pipe_purchase'])
    assert row['bundle_event_installation'] == pytest.approx(.026 * row['bundle_event_purchase'])
    assert row['bundle_event_removal'] == pytest.approx(.024 * row['bundle_event_purchase'])
    baseline = equipment()
    assert {k: v for k, v in row.items() if k not in MONEY} == {
        k: v for k, v in baseline.items() if k not in MONEY}
    # Independent present-value increment: exactly one bundle replacement at15y.
    crf = .07 / (1 - 1.07 ** -30)
    bundle_change = (row['bundle_event_purchase'] - baseline['bundle_event_purchase']) * 1.05
    assert row['replacement_annual'] - baseline['replacement_annual'] == pytest.approx(
        bundle_change / 1.07 ** 15 * crf, rel=2e-13)


def test_general_multiplier_stays_separate_from_stainless_source(equipment):
    base = equipment(stainless_fabrication_usd2017_per_kg_in=240.)
    doubled = equipment(stainless_fabrication_usd2017_per_kg_in=240., costscale_in=2.)
    for k in ('hx_purchase', 'bundle_event_purchase', 'primary_vendor', 'secondary_vendor',
              'salt_inventory_cost', 'helium_inventory_cost'):
        assert doubled[k] == pytest.approx(2*base[k])


@pytest.mark.parametrize('price', [0., -1., math.inf, -math.inf, math.nan])
def test_active_bad_rate_rejected_and_dormant_rate_ignored(equipment, runtime, price):
    with pytest.raises(ValueError):
        equipment(stainless_fabrication_usd2017_per_kg_in=price)
    dormant = equipment(enabled_in=False, stainless_fabrication_usd2017_per_kg_in=price)
    assert all(value == 0 for value in dormant.values())
    import oracle_cooling
    with pytest.raises(ValueError):
        oracle_cooling.calculate({'enabled': True, 'fabrication_rate_2017': price})
    assert all(value == 0 for value in oracle_cooling.calculate({'enabled': False, 'fabrication_rate_2017': price}).values())


@pytest.mark.codegen_available
def test_nominal_is_exact_frozen_wi070_estimate(evaluate):
    old = json.loads((ROOT/'exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs/results/baseline_result.json').read_text())
    row = evaluate()
    assert dict(row.outputs) == old['channels']
    expected = {v['constraint_id']: v['status'] for v in old['verdicts']}
    assert {k: row.responses[k] for k in expected} == expected
    assert row.responses['headline'] == 'violated'
    assert dict(evaluate({KEY: 310.}).outputs) == dict(row.outputs)


@pytest.mark.codegen_available
@pytest.mark.parametrize('price,contingency', [(240., .1), (310., .1), (360., .1), (240., 0.), (310., 0.), (360., 0.)])
def test_public_price_and_contingency_native_oracle_and_all_invariants(evaluate, price, contingency):
    import oracle_entry
    base = evaluate({'contingency_rate': contingency})
    changes = {KEY: price, 'contingency_rate': contingency}
    row = evaluate(changes)
    expected = oracle_entry.evaluate({P+k: v for k, v in changes.items()})
    for key, value in expected.items():
        assert row.outputs[key] == pytest.approx(value, rel=1e-9,
            abs=1e-18 if '__inventory__' in key else 1e-6), key
    allowed = {P+E+k for k in MONEY}
    financial = ('heat_transport__cooling_selection__', 'shipping_scope__',
                 'cas22_capital__', 'cas2x_pre_contingency__', 'contingency__',
                 'cas20_capital__', 'indirect__', 'supplementary__', 'overnight_capital__',
                 'idc__', 'total_capital__', 'cas90_1cfe_calc__', 'lcoe_calc__',
                 'lcoe_1cfe_calc__', 'cooling_annual__', 'cas70_calc__')
    allowed |= {k for k in row.outputs if k.removeprefix(P).startswith(financial)}
    different = {k for k in row.outputs if row.outputs[k] != base.outputs[k]}
    assert different <= allowed, different - allowed
    assert row.responses == base.responses
    for channel in ('pb__p_net', 'calendar__availability', 'calendar__cas72_annual',
                    E+'primary_vendor', E+'secondary_vendor', E+'inventory_cost', E+'spares_cost'):
        assert output(row, channel) == output(base, channel)
    direct_delta = output(row, E+'installed_total')-output(base, E+'installed_total')
    delivered_delta = output(row, E+'delivered_total')-output(base, E+'delivered_total')
    assert output(row, 'cas2x_pre_contingency__cas2x_pre_contingency') - output(base, 'cas2x_pre_contingency__cas2x_pre_contingency') == pytest.approx(direct_delta, abs=2e-6)
    assert output(row, 'shipping_scope__cooling_exclusion') - output(base, 'shipping_scope__cooling_exclusion') == pytest.approx(delivered_delta, abs=2e-6)
    c20 = direct_delta*(1+contingency)
    c30 = c20*.2*8/6
    c50 = .015*(c20-delivered_delta)+.01*c20+.015*(c20+c30)
    assert output(row, 'total_capital__total_capital')-output(base, 'total_capital__total_capital') == pytest.approx(c20+c30+c50, abs=1e-5)
    energy = 8760*output(row, 'pb__p_net')*output(row, 'calendar__availability')
    lcoe_delta = ((c20+c30+c50)*1.07**4*output(row, 'cas71_calc__crf')
                  + output(row, E+'replacement_annual')-output(base, E+'replacement_annual'))/energy
    assert output(row, 'lcoe_calc__lcoe')-output(base, 'lcoe_calc__lcoe') == pytest.approx(lcoe_delta, abs=1e-10)


@pytest.mark.codegen_available
def test_exact_native_input_identity_and_existing_contingency_map(evaluate):
    import oracle_entry
    contract = json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    parameters = contract['parameters']
    # Contract serialization is a list of parameter records; check canonical key.
    encoded = json.dumps(parameters)
    assert P+KEY in encoded
    assert oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT[P+KEY] == 'cooling_fabrication_rate_2017'
    assert oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT[P+'contingency_rate'] == 'contingency_rate'
