"""Read only the named study JSON; check arithmetic and qualified verdict claims."""
import json
import math
from pathlib import Path
root = Path('exploration/stellarator_e2e/studies/20260911-model-owned-radius')
def read(name):
    return json.loads((root / 'results' / (name + '.json')).read_text())
cases = read('cases')
catalog = read('constraint-catalog')
ledger = read('all-channel-verification')
base = cases[2]['outputs']
prefix = 'stellarator_09__stellaris__'
summary = []
worst = 0.0
assert len(cases) == 7 and len(catalog) == 18
for case, check in zip(cases, ledger['cases'], strict=True):
    r = case['inputs'][prefix+'R']
    outputs = case['outputs']
    assert case['state'] == 'completed'
    assert set(case['verdicts']) == set(catalog)
    assert len(check['channels']) == 141 and len(check['verdicts']) == 18
    violations = []
    for cid, value in case['verdicts'].items():
        assert cid in catalog
        assert check['verdicts'][cid]['native'] == value
        assert check['verdicts'][cid]['oracle_rederived'] == value
        assert value in ('satisfied', 'violated')
        if value == 'violated':
            violations.append(catalog[cid]['source_local_identity'])
    expected = {'peak_field_ok'} if r < 12.7 else {'divertor_heat_ok'} if r == 12.7 else {'divertor_heat_ok','wall_load_ok','sustainment_ok','loop_capacity_ok'}
    assert set(violations) == expected
    for channel, evidence in check['channels'].items():
        assert outputs[channel] == evidence['native']
        assert math.isclose(evidence['native'], evidence['oracle'], rel_tol=1e-9, abs_tol=1e-9)
        worst = max(worst, evidence['relative_deviation'])
    ratios = {'geom__V': r/12.7, 'coil_length__c_coil':r/12.7, 'field_calc__B_axis':12.7/r, 'stored_energy__W_mag':12.7/r, 'peak_field_calc__B_peak':(12.7-3.1500000000000004)/(r-3.1500000000000004), 'magnet_cost__capital_cost':1.0}
    for key, expected_ratio in ratios.items():
        assert math.isclose(outputs[prefix+key]/base[prefix+key], expected_ratio,rel_tol=1e-9,abs_tol=1e-9)
    summary.append({'R':r,'lcoe': outputs[prefix+'lcoe_calc__lcoe'],'lcoe_1cfe':outputs[prefix+'lcoe_1cfe_calc__lcoe'],'violated':sorted(violations)})
coverage = read('coverage')
assert len(coverage['unsupported_inputs']) == 147
assert len(coverage['omitted_independent_channels']) == 17
assert read('fixed-input-verification')['public_inputs'] == 246
assert all(x['all_other_fields_identical'] for x in read('fixed-input-verification')['cases'])
for control in read('frozen-control-verification')['controls']:
    assert len(control['scalars']) == 158
    assert all(x['pass'] for x in control['scalars'].values())
result={'outcome':'PASS','scope':'read-only named JSON; no model/oracle execution or store access','cases':summary,'channel_comparisons':7*141,'qualified_verdict_comparisons':7*18,'independent_ratio_recalculations':42,'worst_recorded_channel_deviation':worst,'unsupported_inputs':147,'omitted_independent_outputs':17}
print(json.dumps(result,indent=2))
