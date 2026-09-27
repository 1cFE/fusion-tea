"""Independent reporting audit from retained native maps; no renderer imports."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
RECORD = ROOT / 'exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison-b'
P = 'aries_integrated_plant__'
BRANCHES = ('he', 'pbli', 'divertor')


def read(path):
    return json.loads(path.read_text())


def close(a, b, absolute=1e-7):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=absolute), (a, b)


def main():
    cases = read(RECORD / 'results/cases.json')['cases']
    by = {r['case']: r for r in cases}
    proposals = {r['case']: r for r in read(RECORD / 'proposed-points.json')['cases']}
    report = read(HERE / 'r3-data/reporting.json')
    verified = read(RECORD / 'results/verification_summary.json')
    prior = read(RECORD.parent / '20260927-exchanger-thermal-comparison/results/cases.json')['cases']
    assert len(cases) == len(prior) == 1277
    assert verified['outcome'] == 'pass'
    assert verified['verdict_mismatches'] == verified['not_independently_verified'] == []
    assert len(verified['channels_checked']) == 435 and len(verified['constraints_rederived']) == 35
    assert set(verified['stores'][0]['sampling']['sampled_case_ids']) == {r['candidate_id'] for r in cases}
    for old in prior:
        new = by[old['case']]
        assert new['state'] == 'completed' and new['inputs'] == old['inputs'] == proposals[new['case']]['point']
        assert new['executable_fingerprint'] == '668b903599f995fd6e9038d61a2401144d79f1db13f221b4a663df7cb24a2a23'
        if old['state'] == 'completed':
            assert new['verdicts'] == old['verdicts']
    passed = lambda r: len(r['verdicts']) == 35 and set(r['verdicts'].values()) == {'satisfied'} and value(r, 'plant_ledger', 'net_electric') > 0
    assert sum(map(passed, cases)) == 535
    selected = report['selected']
    main_rows = [r for r in selected if r['scenario'] == 'main']
    assert len(main_rows) == 15
    min_gap, max_return = float('inf'), 0.
    for row in selected:
        native = by[row['case']]
        assert passed(native)
        close(row['net_MW'], value(native, 'plant_ledger', 'net_electric'))
        meta = proposals[row['case']]['metadata']
        pool = [r for r in cases if passed(r) and all(proposals[r['case']]['metadata'][k] == meta[k] for k in ('load', 'offer', 'mode', 'scenario'))]
        assert row['net_MW'] >= max(value(r, 'plant_ledger', 'net_electric') for r in pool) - 1e-9
    for row in main_rows:
        n = by[row['case']]
        inp = n['inputs']
        for b in BRANCHES:
            h = lambda field: value(n, 'heat_exchangers', b + '_' + field)
            target = inp[P + 'heat_exchangers__' + b + '_required_return']
            ch = inp[P + 'heat_exchangers__' + b + '_flow'] * inp[P + 'heat_exchangers__' + b + '_cp'] / 1e6
            duty = value(n, b + '_coolant', 'delivered_heat')
            close(h('hot'), target + duty / ch)
            close(h('mixed_return'), h('bypass_fraction') * h('hot') + (1-h('bypass_fraction')) * h('hx_return'))
            close(h('transferred'), ch * (1-h('bypass_fraction')) * (h('hot')-h('hx_return')))
            close(h('hot_terminal_difference'), h('hot')-h('secondary_out'))
            close(h('cold_terminal_difference'), h('hx_return')-h('secondary_in'))
            assert h('hot_bound_margin') >= 0 and h('required_hot_margin') >= 0
            assert h('state_defined') == 1 and h('control_margin') >= 0
            assert h('hot_terminal_difference') >= 30 and h('cold_terminal_difference') >= 30
            assert abs(h('mixed_return')-target) <= 1e-6 and abs(h('unmet')) <= 1e-6
            min_gap = min(min_gap, h('hot_terminal_difference'), h('cold_terminal_difference'))
            max_return = max(max_return, abs(h('mixed_return')-target))
            close(n['outputs'][P+b+'_hx__purchase__capital'], 58325700., 1e-6)
            assert n['outputs'][P+b+'_hx__purchase__extrapolated'] == 1
    for pair in report['pairs']:
        s, n = by[pair['series_case']], by[pair['network_case']]
        assert passed(s) and passed(n)
        differences = {k for k in s['inputs'] if s['inputs'][k] != n['inputs'][k]}
        allowed = {P+'cycle__selected_flow', P+'heat_exchangers__network_mode', P+'heat_exchangers__pbli_split_fraction'}
        if pair['kind'] == 'differential-network-loss':
            allowed.add(P+'pressure_loss__loss_fraction')
        assert differences <= allowed, differences-allowed
        ps, pn = [value(r, 'plant_ledger', 'net_electric') for r in (s, n)]
        costs = [value(r, 'lifecycle_accounts', 'annual_capital') + value(r, 'lifecycle_accounts', 'noncapital_annual') for r in (s, n)]
        for r, power, cost in zip((s, n), (ps, pn), costs):
            energy = 8760*r['inputs'][P+'cost_schedule__availability']*power
            close(energy, value(r, 'lifecycle_accounts', 'annual_energy'))
            close(cost/energy, value(r, 'lifecycle_accounts', 'lcoe_sum'))
        close(pair['delta_net_MW'], pn-ps)
        close(pair['annual_budget_Bs0_pS0_pN0_USD2004'], pn/ps*costs[0]-costs[1], 1e-5)
        close(pair['power_budget_Bs0_Bn0_pS0_MW'], pn-costs[1]*ps/costs[0])
    for row in report['break_even']:
        s, n = by[row['series_case']], by[row['network_case']]
        ps, pn = [value(r, 'plant_ledger', 'net_electric') for r in (s, n)]
        a = [value(r, 'lifecycle_accounts', 'annual_capital') + value(r, 'lifecycle_accounts', 'noncapital_annual') for r in (s, n)]
        common = row['common_annual_cost_USD2004']
        ratio = (pn-row['network_extra_power_MW'])/(ps-row['series_extra_power_MW'])
        close(row['allowed_differential_annual_cost_USD2004'], ratio*(a[0]+common)-(a[1]+common), 1e-5)
        assert pn-row['network_extra_power_MW'] > 0 and ps-row['series_extra_power_MW'] > 0
    for r in report['refinement']:
        if r['native_selected_case'] is None:
            continue
        n, lower = by[r['native_selected_case']], by[r['lower_native_failure_case']]
        assert passed(n) and not passed(lower)
        diff = {k for k in n['inputs'] if n['inputs'][k] != lower['inputs'][k]}
        assert diff == {P+'cycle__selected_flow'}
        close(n['inputs'][P+'cycle__selected_flow']-lower['inputs'][P+'cycle__selected_flow'], .00625)
        assert not r['edge_passes'] and r['stability_pass']
        check = r['final_split_check']
        if check:
            assert abs(check['delta_net']) <= .2 and abs(check['delta_lcoe']) <= .1
    assert len(report['equal_flow']) == 7
    assert all(r['comparison_usable'] and r['delta_net_MW'] == 0 for r in report['equal_flow'])
    assert all(r['same_selected_parent'] for r in report['financial_parent_receipts'])
    headline = [p for p in report['pairs'] if p['offer'] == 'B' and 1835 < p['load_MW'] < 1836 and p['scenario'] in ('main','zero-tritium') and p['kind'] == 'matched']
    receipt = {'status':'PASS','native_cases':1277,'engineering_passes':535,'engineering_failures':742,'selected_main':15,'matched_or_differential_pairs':len(report['pairs']),'break_even_points':len(report['break_even']),'minimum_main_terminal_K':min_gap,'maximum_main_return_error_K':max_return,'headline_pairs':headline,'native_cases_sha256':hashlib.sha256((RECORD/'results/cases.json').read_bytes()).hexdigest(),'reporting_sha256':hashlib.sha256((HERE/'r3-data/reporting.json').read_bytes()).hexdigest()}
    (HERE/'r4-review-probe.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('headline_pairs',)},indent=2))


def value(row, owner, field):
    return row['outputs'][P+owner+'__evaluate__'+field]


if __name__ == '__main__':
    main()
