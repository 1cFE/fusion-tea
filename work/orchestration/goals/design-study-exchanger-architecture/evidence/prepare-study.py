"""Goal-owned preparation on the unchanged ARIES package; no main execution command.

All physics and predicates come from the package-owned oracle or native route.
The local composer labels search and sensitivity honestly, checks full maps, and
deduplicates identical maps with explicit candidate aliases.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from exploration.aries_integrated.studies import study_route as route, oracle_entry
from scripts.study import common, manifest, verify

GOAL = ROOT / 'work/orchestration/goals/design-study-exchanger-architecture'
RECORD = ROOT / 'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture'
P = 'aries_integrated_plant__'
LOADS = [1650., 1835.4512830147435, 2000., 2100., 2200., 2250., 2300., 2350., 2400., 2450., 2500., 2600.]
FLOWS = [1300., 1400., 1500., 1600.]
SPLITS = [.50, .60, .65, .70, .75, .80, .85, .90]
BRANCHES = ['he', 'pbli', 'divertor']


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(owner, field):
    return P + owner + '__' + field


def point_key(point):
    checked = route.validate_proposal(point)
    if checked is None:
        raise ValueError('incomplete, unknown or nonfinite input map')
    return tuple(sorted(checked.items()))


def definitions():
    # Ties are coordinated uncertainty scenarios, never assertions that distinct
    # physical pumps or exchangers have the same dimensional value.
    raw = [
        ('source_mode', ['source__producer_mode'], 'sensitivity', '1 calculated control; 0 supplied downstream family; no sustained plasma claim'),
        ('source_load', ['source__reference_fusion_mw'], 'search', 'Supplied common-load boundary; exact nominal source anchor and engineered 1650–2600 MW window'),
        ('architecture', ['heat_exchangers__network_mode'], 'search', 'Existing series or series-then-parallel connection graph'),
        ('cycle_flow', ['cycle__selected_flow'], 'search', 'Same four supplied operating choices for both architectures; installed capacities fixed'),
        ('branch_split', ['heat_exchangers__pbli_split_fraction'], 'search', 'Supplied network operating choice; inert .85 placeholder in series'),
        ('conductance_uncertainty', [b+'_hx__assumed_u' for b in BRANCHES], 'sensitivity', '[AGENT] correlated 0.8/1.2 multiplier on each inherited U; shared uncertainty, no physical identity or hardware change asserted'),
        ('pressure_loss', ['pressure_loss__loss_fraction'], 'sensitivity', 'Common .02/.08 sensitivity and network .08 differential against inherited .045 series'),
        ('pump_mode', [b+'_pump__pump_mode' for b in BRANCHES], 'sensitivity', '[AGENT] coordinated switch to existing fixed-power mode 1 for all pumps'),
        ('pump_power', [b+'_pump__fixed_power' for b in BRANCHES], 'sensitivity', '[AGENT] coordinated 0.8/1.2 multiplier on each own reference power; preserves distinct powers and existing heat recovery'),
        ('tritium_price', ['fuel_inventory__tritium_price'], 'sensitivity', '[AGENT] selected zero-price bookkeeping endpoint within owner-authorized fuel sensitivity; reprices annual purchases and initial stock; no breeding claim'),
    ]
    axes = []
    ties = []
    for axis, names, framing, note in raw:
        keys = [P+n for n in names]
        axes.append({'axis': axis, 'keys': [{'key': k, 'provenance': 'fan_out' if i == 0 else 'tie'} for i, k in enumerate(keys)], 'framing': framing, 'basis': note, 'window_provenance': 'engineered'})
        for k in keys[1:]:
            ties.append({'key': k, 'rides_with': [keys[0]], 'note': note})
    declared = [k['key'] for a in axes for k in a['keys']]
    assert len(declared) == len(set(declared)) and set(declared) <= set(route.interface()['entry_keys'])
    return axes, ties


def prepare():
    if RECORD.exists():
        raise ValueError('record exists; preserve preparation')
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    source = route.HERE / '20260925-aries-revised-reference-network/results/cases.json'
    old = next(r for r in read(source)['cases'] if r['case'] == 'nominal-calculated')
    assert old['executable_fingerprint'] == route.interface()['executable_fingerprint']
    base = {k: float(v) for k, v in old['inputs'].items()}
    assert base[key('source', 'producer_mode')] == 1 and base[key('pressure_loss', 'loss_fraction')] == .045
    assert old['outputs'][key('source', 'evaluate__selected_power')] == LOADS[1]
    axes, ties = definitions()
    declared = {k['key'] for a in axes for k in a['keys']}
    m = loaded.data | {'ties': ties}
    RECORD.mkdir(parents=True)
    write(RECORD / 'manifest.json', m)
    write(RECORD / 'axes.json', {'schema_version': 'study-axis-declaration/v1', 'groups': [{'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in axes]})
    write(RECORD / 'axis-plan.json', {'study_id': RECORD.name, 'axes': axes, 'loads': LOADS, 'flows': FLOWS, 'splits': SPLITS, 'main_count': 432, 'paired_sensitivity_count': 192, 'selection_tolerance_MW': .01, 'baseline_loss': .045, 'main_execution_authorized': False})
    write(RECORD / 'baseline-control.json', old)
    write(RECORD / 'preparation-provenance.json', {'source': source.relative_to(ROOT).as_posix(), 'source_sha256': sha(source), 'case': old['case'], 'executable': old['executable_fingerprint'], 'base_manifest_sha256': sha(route.MANIFEST_PATH), 'composer_sha256': sha(Path(__file__)), 'contract_sha256': sha(GOAL/'evidence/comparison-contract.md'), 'brief_sha256': sha(GOAL/'evidence/study-preparation-brief.md'), 'native_main_evaluations': 0})
    for name in ('owner-brief.md', 'comparison-contract.md', 'study-preparation-brief.md'):
        shutil.copyfile(GOAL/'evidence'/name, RECORD/name)
    template = (ROOT/'.agents/skills/run-study/record-template.md').read_text()
    shutil.copyfile(ROOT/'.agents/skills/run-study/record-template.md', RECORD/'record-template-source.md')
    headings = re.findall(r'^## (?:[1-9]|1[0-7])\. .+$', template, re.M)[:17]
    assert len(headings) == 17
    text = '# Study record — exchanger architecture\n\n' + '\n\n'.join(h+'\n\n[AGENT] Preparation pending; main execution has not been released.' for h in headings) + '\n'
    (RECORD/'record.md').write_text(text)
    rows, aliases, seen = [], [], {}

    def add(name, classification, changes, meta):
        point = base | {k: float(v) for k, v in changes.items()}
        changed = {k for k in point if point[k] != base[k]}
        assert changed <= declared, changed - declared
        identity = point_key(point)
        if identity in seen:
            aliases.append({'case': name, 'canonical_case': seen[identity], 'classification': classification, 'metadata': meta})
            return
        seen[identity] = name
        rows.append({'case': name, 'classification': classification, 'arm': 'architecture', 'changes': {k: point[k] for k in sorted(changed)}, 'metadata': meta, 'point': point})

    def operating(load, flow, mode, split):
        return {key('source','producer_mode'): 0, key('source','reference_fusion_mw'): load, key('cycle','selected_flow'): flow, key('heat_exchangers','network_mode'): mode, key('heat_exchangers','pbli_split_fraction'): split}

    def label(load, flow, mode, split):
        return f'L{load:.15g}-F{flow:g}-M{mode}-S{split:g}'

    for load in LOADS:
        for flow in FLOWS:
            for mode, split in [(0,.85)] + [(1,s) for s in SPLITS]:
                add('main-'+label(load,flow,mode,split), 'main', operating(load,flow,mode,split), {'load_MW':load,'flow_kg_s':flow,'mode':mode,'split':split,'scenario':'baseline'})
    add('control-calculated-N', 'control', {}, {'scenario':'original-calculated-N'})
    add('control-supplied-N', 'control', operating(LOADS[1],1400,0,.85), {'scenario':'exact-supplied-replay'})
    for load in (2200.,2300.):
        for flow in FLOWS:
            for mode, split in [(0,.85)] + [(1,s) for s in (.65,.75,.85)]:
                for scenario, factor in [('U',.8),('U',1.2),('loss',.02),('loss',.08),('pump',.8),('pump',1.2)]:
                    changes = operating(load,flow,mode,split)
                    if scenario == 'U':
                        changes.update({key(b+'_hx','assumed_u'):base[key(b+'_hx','assumed_u')]*factor for b in BRANCHES})
                    elif scenario == 'loss':
                        changes[key('pressure_loss','loss_fraction')] = factor
                    else:
                        changes.update({key(b+'_pump','pump_mode'):1 for b in BRANCHES})
                        changes.update({key(b+'_pump','fixed_power'):base[key(b+'_pump','reference_power')]*factor for b in BRANCHES})
                    add(f'sens-{scenario}{factor:g}-'+label(load,flow,mode,split), 'sensitivity', changes, {'load_MW':load,'flow_kg_s':flow,'mode':mode,'split':split,'scenario':scenario,'level':factor})
    assert sum(r['classification']=='main' for r in rows) == 432
    assert sum(r['classification']=='sensitivity' for r in rows) == 192
    write(RECORD/'candidate-points-initial.json', {'study_id':RECORD.name,'cases':rows,'aliases':aliases})
    print(json.dumps({'record':str(RECORD),'unique_initial':len(rows),'aliases':len(aliases)}))


def scan():
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(RECORD/'manifest.json')
    manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    proposals = read(RECORD/'candidate-points-initial.json')
    catalog = route._catalog_by_constraint_id(route.PACKAGE_DIR)
    bindings = oracle_entry.operand_bindings()
    results = []

    def evaluate(row):
        try:
            values = oracle_entry.evaluate(row['point'])
            verdicts = {cid:'satisfied' if verify.derive_verdict(cid,e,bindings,row['point'],{},values)[0] else 'violated' for cid,e in catalog.items()}
            net = values[key('plant_ledger','evaluate__net_electric')]
            return {'case':row['case'],'status':'evaluated','numerically_retained':net>0,'numerical_exclusion':None if net>0 else 'nonpositive net: native positive-energy lifecycle domain','values':values,'verdicts':verdicts}
        except Exception as error:
            return {'case':row['case'],'status':'refused','numerically_retained':False,'error':f'{type(error).__name__}: {error}'}

    for row in proposals['cases']:
        results.append(evaluate(row))
    write(RECORD/'oracle-initial-scan.json',{'kind':'independent-oracle-only','cases':results})
    by_name = {r['case']:r for r in results}
    selected=[]
    extra=[]
    aliases=list(proposals['aliases'])
    seen={point_key(r['point']):r['case'] for r in proposals['cases']}
    base=read(RECORD/'baseline-control.json')['inputs']

    def extra_case(name, parent, changes, scenario):
        point=parent['point']|changes
        identity=point_key(point)
        meta=parent['metadata']|{'scenario':scenario,'parent':parent['case']}
        if identity in seen:
            aliases.append({'case':name,'canonical_case':seen[identity],'classification':'sensitivity','metadata':meta})
            return
        seen[identity]=name
        row={'case':name,'classification':'sensitivity','arm':'architecture','metadata':meta,'point':point,'changes':{k:v for k,v in point.items() if v!=base[k]}}
        extra.append(row)
        results.append(evaluate(row))

    for load in LOADS:
        pair=[]
        for mode in (0,1):
            passing=[r for r in proposals['cases'] if r['classification']=='main' and r['metadata']['load_MW']==load and r['metadata']['mode']==mode and by_name[r['case']]['numerically_retained'] and all(v=='satisfied' for v in by_name[r['case']]['verdicts'].values())]
            if not passing:
                selected.append({'load_MW':load,'mode':mode,'status':'no_passing_tested_case','ties':[]})
                continue
            best=max(by_name[r['case']]['values'][key('plant_ledger','evaluate__net_electric')] for r in passing)
            ties=sorted([r for r in passing if abs(by_name[r['case']]['values'][key('plant_ledger','evaluate__net_electric')]-best)<=.01], key=lambda r:(r['metadata']['flow_kg_s'],r['metadata']['split'],r['case']))
            representative=ties[0]
            selected.append({'load_MW':load,'mode':mode,'status':'passing_tested','maximum_net_MW':best,'ties':[r['case'] for r in ties],'representative':representative['case'],'representative_policy':'lowest tested flow then lowest split among 0.01 MW ties; all ties retained'})
            pair.append(representative)
        if len(pair)==2:
            for parent in pair:
                extra_case('sens-zero-tritium-'+parent['case'],parent,{key('fuel_inventory','tritium_price'):0.},'zero-tritium-price')
            if load in (2200.,2300.):
                network=next(p for p in pair if p['metadata']['mode']==1)
                extra_case('sens-network-extra-loss-'+network['case'],network,{key('pressure_loss','loss_fraction'):.08},'network-only-loss-0.08-versus-series-0.045')
    write(RECORD/'oracle-selection.json',{'kind':'oracle-only explicit operating selection, never inventory selection','tolerance_MW':.01,'selected':selected})
    all_rows=proposals['cases']+extra
    assert len(all_rows)==len(results)
    by_name={r['case']:r for r in results}
    retained=[r for r in all_rows if by_name[r['case']]['numerically_retained']]
    excluded=[{'case':r['case'],'classification':r['classification'],'metadata':r['metadata'],'scan':by_name[r['case']]} for r in all_rows if not by_name[r['case']]['numerically_retained']]
    write(RECORD/'candidate-points-complete.json',{'study_id':RECORD.name,'cases':all_rows,'aliases':aliases})
    write(RECORD/'oracle-window-scan.json',{'kind':'independent-oracle-only','fingerprints':loaded.data['fingerprints'],'cases':results})
    write(RECORD/'proposed-points.json',{'study_id':RECORD.name,'cases':retained,'aliases':aliases})
    ledger=[{'case':r['case'],'canonical_case':r['case'],'classification':r['classification'],'metadata':r['metadata'],'status':'retained' if by_name[r['case']]['numerically_retained'] else 'numerically_excluded','oracle_status':by_name[r['case']]['status'],'oracle_violations':[k for k,v in by_name[r['case']].get('verdicts',{}).items() if v!='satisfied']} for r in all_rows]
    ledger.extend(a|{'status':'alias','canonical_status':'retained' if by_name[a['canonical_case']]['numerically_retained'] else 'numerically_excluded'} for a in aliases)
    write(RECORD/'candidate-ledger.json',{'candidates':ledger,'excluded':excluded,'unique_retained':len(retained),'unique_excluded':len(excluded),'aliases':len(aliases)})
    print(json.dumps({'scanned':len(results),'retained':len(retained),'excluded':len(excluded),'aliases':len(aliases),'selection_count':len(selected)}))


def baseline():
    out=RECORD/'preparation'
    if (out/'baseline_result.json').exists():
        raise ValueError('baseline evidence exists; preserve it')
    out.mkdir(exist_ok=True)
    print(route.execute_baseline(out,manifest_path=RECORD/'manifest.json'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['prepare','scan','baseline'])
    args=parser.parse_args()
    {'prepare':prepare,'scan':scan,'baseline':baseline}[args.command]()
