"""Check native attempt retention, reporting selection and decomposition after native-ready."""
import collections
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
RECORD = ROOT / 'exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
digest = lambda x: hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
P = 'whole_plant_conversion__plant__'
F = '6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f'
proposed = read(RECORD / 'proposed-points.json')['cases']
rows = read(RECORD / 'results/cases.json')['cases']
members = read(RECORD / 'preparation/case-membership.json')['cases']
predicates = read(RECORD / 'preparation/predicate-catalog.json')
assert len(rows) == len(proposed) == 2496
assert len(members) == 2651
assert {r['case'] for r in rows} == {p['case'] for p in proposed}
assert {r['executable_fingerprint'] for r in rows} == {F}
proposals = {p['case']: p for p in proposed}
by_id = {}
decompositions = 0
def value(row, owner, name):
    return row['outputs'][P + owner + '__evaluate__' + name]
def close(a, b, atol=1e-6):
    assert math.isclose(a, b, rel_tol=1e-12, abs_tol=atol), (a, b)
pv_fields = ('initial_financed_capital', 'annual_expense_pv', 'blanket_replacement_pv', 'magnet_replacement_pv', 'primary_replacement_pv', 'overhaul_pv', 'conversion_replacement_pv', 'terminal_pv')
eligible = {}
for row in rows:
    assert row['state'] == 'completed'
    assert row['inputs'] == proposals[row['case']]['point']
    point_id = digest(row['inputs'])
    assert point_id not in by_id
    by_id[point_id] = row
    assert set(row['verdicts']) == set(predicates)
    assert all(math.isfinite(v) for v in row['outputs'].values())
    for owner, field in [('source_basis', 'source_qualified'), ('supplied_core', 'nuclear_transport_qualified'), ('supplied_core', 'global_construction_qualified')]:
        assert value(row, owner, field) == 0
    for branch in ('steam', 'gas'):
        whole, operating, capital, conversion = (branch + s for s in ('_whole', '_operating', '_overheads', '_ledger'))
        close(math.fsum(value(row, whole, f) for f in pv_fields), value(row, whole, 'total_cost_pv'), 1e-4)
        close(value(row, operating, 'net_export_MW') + value(row, operating, 'upstream_electric_MW') + value(row, conversion, 'electrical_load'), value(row, conversion, 'gross_electric'), 1e-8)
        close(math.fsum(value(row, capital, f) for f in ('common_purchases', 'branch_purchases', 'contingency', 'indirect', 'freight', 'general_spares', 'tax', 'insurance', 'nonfuel_commissioning')), value(row, capital, 'initial_capital'), 1e-4)
        failures = [cid for cid, p in predicates.items() if p['branch'] in ('shared', branch) and row['verdicts'][cid] != 'satisfied']
        ok = not failures and value(row, whole, 'economic_defined') == 1 and value(row, whole, 'energy_pv') > 0 and value(row, whole, 'lcoe_USD2025_MWh') > 0 and value(row, operating, 'net_export_MW') > 0 and value(row, operating, 'annual_net_grid_MWh') > 0
        eligible[(point_id, branch)] = ok
        if ok:
            close(sum(value(row, whole, f) / value(row, whole, 'energy_pv') for f in pv_fields), value(row, whole, 'lcoe_USD2025_MWh'), 1e-8)
        decompositions += 1
native_checks = dict(status='pass', scope='native retention and decomposition only; presentation comparison follows', native_cases=len(rows), branch_decompositions=decompositions, native_sha256=sha(RECORD / 'results/cases.json'))
(HERE / 'native-retention-checks.json').write_text(json.dumps(native_checks, indent=2) + '\n')
print(json.dumps(native_checks), flush=True)
presentation = read(RECORD / 'results/presentation/native-ranking.json')
roles = {'gas_catalog', 'steam_connector_catalog', 'rerank_nominal_supported_catalog', 'newly_admitted_scenario_offer', 'rerank_performance_supported_catalog', 'rerank_performance_supported_catalog_at_price_bracket', 'rerank_performance_supported_catalog_at_reporting_band'}
groups = collections.defaultdict(list)
for a in members:
    groups[(a['scenario'], a['source_MW'], a['branch'])].append(a)
rankings = {(r['scenario'], r['source_MW'], r['branch']): r for r in presentation['rankings']}
assert set(rankings) == set(groups)
for key, aliases in groups.items():
    branch = key[2]
    candidates = {a['point_id'] for a in aliases if a['role'] in roles and eligible[(a['point_id'], branch)]}
    selected = rankings[key]['selected']
    if candidates:
        winner = min(candidates, key=lambda pid: (value(by_id[pid], branch + '_whole', 'lcoe_USD2025_MWh'), by_id[pid]['case']))
        assert selected['point_id'] == winner
        assert selected['native_lcoe_USD2025_MWh'] == value(by_id[winner], branch + '_whole', 'lcoe_USD2025_MWh')
    else:
        assert selected is None
for pair in presentation['matched_pairs']:
    if pair['matched_supported']:
        steam = by_id[pair['steam_case']['point_id']]
        gas = by_id[pair['gas_case']['point_id']]
        gap = value(gas, 'gas_whole', 'lcoe_USD2025_MWh') - value(steam, 'steam_whole', 'lcoe_USD2025_MWh')
        assert pair['cost_gap_gas_minus_steam_USD2025_MWh'] == gap
        assert pair['preference'] == ('indeterminate' if abs(gap) <= 5 else 'steam' if gap > 0 else 'gas')
        power_gap = value(gas, 'gas_operating', 'net_export_MW') - value(steam, 'steam_operating', 'net_export_MW')
        assert pair['net_power_gap_gas_minus_steam_MW'] == power_gap
        assert pair['power_comparison'] == ('indeterminate' if abs(power_gap) <= 5 else 'gas' if power_gap > 0 else 'steam')
result = dict(status='pass', native_cases=len(rows), aliases=len(members), ranking_groups=len(groups), branch_decompositions=decompositions,
              native_sha256=sha(RECORD / 'results/cases.json'), presentation_sha256=sha(RECORD / 'results/presentation/native-ranking.json'),
              executable=F, nominal_pairs=[r for r in presentation['matched_pairs'] if r['scenario'] == 'nominal'])
(HERE / 'native-result-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'nominal_pairs'}, indent=2))
