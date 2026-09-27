"""Independent read-only arithmetic and identity checks; no model/report imports."""
import collections
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
BASE = ROOT / 'exploration/component_alternatives/studies'
NEW = BASE / '20260926-design-study-component-alternatives-b'
OLD = BASE / '20260926-design-study-component-alternatives'
REPORT = Path(__file__).resolve().parents[1] / 'verified-comparison'
P = 'component_alternatives__plant__'

def read(p):
    return json.loads(p.read_text())

def out(row, owner, key):
    return row['outputs'][P + owner + '__evaluate__' + key]

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-6), (a, b)

new = {r['case']: r for r in read(NEW/'results/cases.json')['cases']}
old = {r['case']: r for r in read(OLD/'results/cases.json')['cases']}
v = read(NEW/'results/verification_summary.json')
s = read(REPORT/'matched-study-summary.json')
assert len(new) == len(old) == 498 and set(new) == set(old)
assert v['outcome'] == 'pass' and len(v['channels_checked']) == 872
assert len(v['constraints_rederived']) == 84 and not v['not_independently_verified']
assert not v['verdict_mismatches'] and v['verdicts_rederived']
assert {r['candidate_id'] for r in new.values()} == {i for st in v['stores'] for i in st['sampling']['sampled_case_ids']}
assert {r['executable_fingerprint'] for r in new.values()} == {v['identity']['digest']}
roles = {r['case']: {r['role']} for r in read(NEW/'proposed-points.json')['cases']}
for a in read(NEW/'window.json')['duplicate_aliases']:
    roles[a['native_case']].add(a['role'])
counts = collections.Counter()
units = collections.Counter()
overlap = 0
for name, r in new.items():
    assert r['inputs'] == old[name]['inputs'] and r['verdicts'] == old[name]['verdicts']
    assert len(r['inputs']) == 490 and len(r['outputs']) == 876 and len(r['verdicts']) == 84
    assert r['state'] == 'completed'
    failed = [k for k, value in r['verdicts'].items() if value != 'satisfied']
    classes = set()
    for owner, hotowner, hotkey in [('water_ic1','compressor_1','temperature_out'), ('water_ic2','compressor_2','temperature_out'), ('water_pre','recuperator','hot_out')]:
        code = out(r, owner, 'failure_code')
        if code == 0:
            continue
        assert code == 2
        ua = r['inputs'][P+owner+'__ua']
        if ua < out(r, owner, 'bracket_low_ua'):
            kind = 'lower'
        else:
            assert ua > out(r, owner, 'bracket_high_ua')
            assert out(r, hotowner, hotkey) - 273.15 >= 60
            kind = 'upper_60C'
        units[kind] += 1
        classes.add(kind)
    status = 'mixed' if len(classes) == 2 else next(iter(classes)) if classes else 'failed_solved' if failed else 'pass'
    if 'gas_catalog' in roles[name]:
        counts[status] += 1
    if classes and any('water_ic' not in k and 'water_pre' not in k for k in failed):
        overlap += 1
    for b in ['steam', 'gas']:
        l = b+'_ledger'
        close(out(r,l,'gross_electric') - out(r,l,'electrical_load'), out(r,l,'net_electric'))
        k = out(r,l,'capital_total') + out(r,l,'replacement_pv') + (out(r,l,'annual_service')+out(r,l,'annual_makeup'))*out(r,l,'annuity_factor')
        close(k, out(r,l,'accounted_pv'))
        if out(r,l,'economic_defined'):
            close(out(r,l,'corrected_pv')/out(r,l,'discounted_energy'), out(r,l,'cost_per_net_MWh'))
        if not failed:
            close(out(r,l,'net_electric')+out(r,l,'total_rejected'), out(r,'primary_loop','q_ihx'))
assert counts == {'upper_60C':233,'lower':78,'mixed':11,'failed_solved':39,'pass':14}
assert units == {'upper_60C':464,'lower':153}
anchors=[]
for a in s['anchors']:
    r = new[a['selected_steam_case']]
    q = a['source_MW']
    for b, role in [('steam','steam_connector_catalog'), ('gas','gas_catalog')]:
        rr = [x for n,x in new.items() if role in roles[n] and x['inputs'][P+'blanket_source__q_source']==q and all(z=='satisfied' for z in x['verdicts'].values())]
        close(out(r,b+'_ledger','cost_per_net_MWh'), min(out(x,b+'_ledger','cost_per_net_MWh') for x in rr))
    es,eb=[out(r,b+'_ledger','discounted_energy') for b in ['steam','gas']]
    ks,kb=[out(r,b+'_ledger','accounted_pv') for b in ['steam','gas']]
    gap=ks/es-kb/eb
    close(gap,a['steam_minus_gas_cost_per_MWh'])
    f=a['frontier']
    close(es/eb,f['slope']);close(es/eb*kb-ks,f['intercept_USD2025'])
    common=-gap/(1/es-1/eb)
    close(common,f['common_source_break_even_PV_USD2025'])
    close((ks+common)/es,(kb+common)/eb)
    sensitivity={}
    for label, token in [('efficiency','-eta'),('quote','-quote-')]:
        vals=[out(x,'steam_ledger','cost_per_net_MWh')-out(x,'gas_ledger','cost_per_net_MWh') for n,x in new.items() if 'sensitivity' in roles[n] and x['inputs'][P+'blanket_source__q_source']==q and token in n]
        sensitivity[label]=[min(vals),max(vals)]
    anchors.append(dict(source_MW=q,steam_case=r['case'],gap=gap,common_PV=common,sensitivity=sensitivity))
result=dict(status='PASS',cases=498,scalar_comparisons=498*872,predicate_comparisons=498*84,input_changes=0,predicate_changes=0,passing=sum(all(v=='satisfied' for v in r['verdicts'].values()) for r in new.values()),gas_counts=dict(counts),cooler_occurrences=dict(units),cooler_cases_with_other_predicate_failures=overlap,anchors=anchors,verification_sha256=hashlib.sha256((NEW/'results/verification_summary.json').read_bytes()).hexdigest())
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
