"""Independent comparison of replayed channels, edges, identities and preserved surfaces."""
import collections,csv,hashlib,json,math,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import yaml
ROOT=Path.cwd();A=Path(__file__).resolve().parent;I=A.parent/'implementation';F=A.parent/'prototype';P='stellarator_09__stellaris__';G=ROOT/'exploration/stellarator_e2e/generated'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(A/n).write_text(json.dumps(x,indent=2)+'\n')
def git(ref,path):return subprocess.check_output(['git','show',ref+':'+path])
reference=json.loads(git('2f8856b7','work/analysis/20260911-230953_radius-ownership-evidence/results.json'))
for frozen,original in [('frozen-results.json','results.json'),('frozen-inventory.json','inventory.json'),('frozen-checks.json','checks.json'),('frozen-source-meaning.md','source-meaning.md')]:assert (F/frozen).read_bytes()==git('2f8856b7','work/analysis/20260911-230953_radius-ownership-evidence/'+original)
assert sha(F/'expectations.json')==j(F/'execution-start.json')['expectations_sha256']
results=j(A/'acceptance/results.json');direct=j(A/'acceptance/direct-production.json')['results'];raw=j(F/'direct-entering.json')['results']
rows=[];verdicts={}
for case,prior in [('baseline','baseline'),('R14','tied_R14')]:
    expected=reference['cases'][prior]['native'];actual=results[case]
    assert set(actual['outputs'])==set(expected['outputs'])==set(direct[case]['helper']['outputs'])
    for name,value in sorted(expected['outputs'].items()):
        got=actual['outputs'][name];assert (got==value if case=='baseline' else math.isclose(got,value,rel_tol=1e-9,abs_tol=1e-9))
        assert direct[case]['helper']['outputs'][name]==got
        rows.append({'case':case,'channel':name,'expected':value,'actual':got,'difference':got-value,'relative_error':0 if got==value else abs((got-value)/value) if value else None,'pass':True})
    assert actual['responses']==expected['responses'];assert actual['report']==expected['report']
    assert direct[case]['single']['outputs']==raw[case]['single']['outputs']
    verdicts[case]={r['constraint_id']:r['status'] for r in actual['report']['results']}
    assert len(verdicts[case])==18
    scratch=A/'acceptance/direct-production'/case
    assert (scratch/'pipelines/pipeline.yaml').read_bytes()==(G/'pipelines/pipeline.yaml').read_bytes()
    for f in (G/'inputs').glob('*.json'):
        desired=j(f)
        if case=='R14' and f.stem=='stellarator_plant_params':desired[P+'R']=14.
        assert j(scratch/'inputs'/f.name)==desired
# Re-derive ratios arithmetically rather than importing the frozen expected ratios.
b=results['baseline']['outputs'];r=results['R14']['outputs'];c=b[P+'rb__r_coil_centre']
ratios={}
for key,expected in [('geom__V',14/12.7),('coil_length__c_coil',14/12.7),('field_calc__B_axis',12.7/14),('stored_energy__W_mag',12.7/14),('peak_field_calc__B_peak',(12.7-c)/(14-c)),('magnet_cost__capital_cost',1.)]:
    actual=r[P+key]/b[P+key];assert math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9);ratios[key]={'expected':expected,'actual':actual}
old=I/'entering-package'
def records(pkg):
    values=j(pkg/'contracts/model_contract.json')['parameters'];result={(x['param_group'],x['qualified_name']):x for x in values};assert len(result)==len(values);return result
def defaults(pkg):return {(f.stem,k):v for f in (pkg/'inputs').glob('*.json') for k,v in j(f).items()}
def binds(pkg):return {(m,k):v for m,row in yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())['modules'].items() for k,v in row.get('inputs',{}).items()}
previous,current=records(old),records(G);retired=('stellarator_plant_params',P+'magnet__R0')
assert previous.keys()-current.keys()=={retired} and not current.keys()-previous.keys()
assert all(current[k]==previous[k] for k in current)
d1,d2=defaults(old),defaults(G);assert d1.keys()-d2.keys()=={retired} and not d2.keys()-d1.keys();assert all(d1[k]==v for k,v in d2.items())
a,z=binds(old),binds(G);assert a.keys()==z.keys()
expected_edges={(P+m,f) for m,f in [('rb','R_in'),('geom','R_in'),('sustain','R_in'),('divheat','R_in'),('coil_length','R0'),('field_calc','R0'),('peak_field_calc','R_in'),('magnet_cost','R0'),('stored_energy','R0')]}
assert {k for k,v in z.items() if v=='float stellarator_plant_params.'+P+'R'}==expected_edges
changed={k for k in a if a[k]!=z[k]};assert changed=={(P+m,f) for m,f in [('coil_length','R0'),('field_calc','R0'),('peak_field_calc','R_in'),('magnet_cost','R0'),('stored_energy','R0')]}
anchor_values={'magnet__R_ref':12.7,'magnet__a_coil_ref':3.1500000000000004,'wall_peak_R_ref':12.7,'R_ref_divertor':12.7}
for key,value in anchor_values.items():assert d2[('stellarator_plant_params',P+key)]==value
for case in ('baseline','R14'):
    values=j(A/'acceptance/direct-production'/case/'inputs/stellarator_plant_params.json')
    assert all(values[P+k]==v for k,v in anchor_values.items())
# Census classification compared as full sets against current fresh-generated contract.
census=j(ROOT/'tests/models/data/mfe_census.json');bytype={}
for x in current.values():bytype.setdefault(x['entry_type'],[]).append(x['qualified_name'])
assert {k:sorted(v) for k,v in bytype.items()}==census['by_entry_type']
assert census['entry_points']==len(current) and census['derived_against_semantic_fingerprint']==j(G/'contracts/model_contract.json')['semantic_fingerprint']
# Every inherited cost/finance classification has complete output coverage.
coverage=j(ROOT/'work/active/WI-050_mfe-coherent-operating-heating/implementation/cost-operand-coverage.json');costs={}
modules=yaml.safe_load((G/'pipelines/pipeline.yaml').read_text())['modules']
for name,entry in coverage.items():
    emitted={binding.split(' ',1)[1] for binding in modules[P+name]['outputs'].values()}
    assert emitted<=b.keys() and emitted<=r.keys(),name
    costs[name]={'classification':entry['classification'],'outputs':{k:{'baseline':b[k],'R14':r[k]} for k in sorted(emitted)}}
# Per-node outcomes and exact inherited skip reasons.
def nodes(p):
    out={}
    for n in ET.parse(p).getroot().iter('testcase'):
        status=next((c for c in n if c.tag in ('failure','error','skipped')),None)
        out[n.attrib['classname']+'::'+n.attrib['name']]={'outcome':'passed' if status is None else status.tag,'reason':'' if status is None else status.attrib.get('message','')}
    return out
enter=nodes(I/'entering-tests.xml');now=nodes(A/'tests.xml');added=now.keys()-enter.keys()
assert not enter.keys()-now.keys() and all(enter[k]==now[k] for k in enter)
assert len(added)==64 and all(now[k]['outcome']=='passed' for k in added)
dump('regression.json',{'entering':enter,'audit':now,'added':sorted(added),'removed':[],'changed':[],'audit_counts':dict(collections.Counter(v['outcome'] for v in now.values()))})
# Recalculate the exact protected manifest, with only documented changes admitted.
protected=j(I/'protected-before.json');changed_protected={}
for name,prior in protected.items():
    assert not name.startswith('knowledge/holdout/')
    path=ROOT/name
    actual={'symlink':str(path.readlink())} if path.is_symlink() else {'sha256':sha(path)} if path.is_file() else None
    if actual!=prior:changed_protected[name]={'before':prior,'actual':actual}
parent=set(subprocess.check_output(['git','diff','--name-only','45003717..4fc05302']).decode().splitlines())
for name in parent:assert (ROOT/name).read_bytes()==git('4fc05302',name)
assert set(changed_protected)<=parent|{'tests/models/test_mfe_operating_heating.py'}
expected=git('45003717','tests/models/test_mfe_operating_heating.py').decode().replace("assert len(contract['parameters'])==247", "assert len(contract['parameters'])==246  # WI-051 retires the duplicate magnet radius.")
assert (ROOT/'tests/models/test_mfe_operating_heating.py').read_text()==expected
# Ensure original prototype/review/revision/assessment and excluded surfaces have no git diff.
protected_paths=[str(F.relative_to(ROOT)),str((A.parent/'review-evidence').relative_to(ROOT)),str((A.parent/'design-revision').relative_to(ROOT)),'work/analysis/20260911-230953_radius-ownership-evidence','exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/studies','exploration/stellarator_e2e/study_route.py','exploration/stellarator_e2e/ANNEX.md','tests/study','models/library','knowledge/SOURCE_INDEX.md','knowledge/KNOWLEDGE.md','modeling_project/REQUIREMENTS.md','modeling_project/ARCHITECTURE.md']
assert not subprocess.check_output(['git','diff','45003717','--',*protected_paths])
dump('protection.json',{'protected_manifest_entries':len(protected),'changed':changed_protected,'parent_commits':['2a55615b','4fc05302'],'parent_paths_verified':sorted(parent),'git_byte_comparison_paths':protected_paths,'unexpected_deltas':[]})
contract=j(G/'contracts/model_contract.json');runtime=j(A/'acceptance/contract-delta.json');handoff=(I/'consumer-handoff.md').read_text()
identities={'semantic':contract['semantic_fingerprint'],'executable':runtime['executable_fingerprint'],'seal_sha256':sha(G/'contracts/package_contract.json'),'contract_sha256':sha(G/'contracts/model_contract.json'),'snapshot_sha256':sha(ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json')}
assert all(v in handoff for v in identities.values())
trace=list(csv.DictReader((ROOT/'data/traceability_matrix.csv').open(newline='')))
dump('comparison.json',{'channels':rows,'verdicts':verdicts,'ratios':ratios,'cost_finance_modules':costs,'old_census':[list(k) for k in sorted(previous)],'new_census':[list(k) for k in sorted(current)],'all_surviving_parameter_records_and_defaults_exact':True,'nine_edges':[{'module':m,'formal':f,'binding':z[(m,f)]} for m,f in sorted(expected_edges)],'changed_bindings':[{'module':m,'formal':f,'old':a[(m,f)],'new':z[(m,f)]} for m,f in sorted(changed)],'anchors':anchor_values,'identities':identities,'trace_rows':trace[-2:]})
lines=['# Independent numerical comparisons','','Every emitted scalar is compared to T-021 at `2f8856b7`. Baseline is exact; R14 tolerance is relative/absolute 1e-9 in unchanged channel units. The replay actually matched every value exactly. Full reports, observed operands, margins and 18 named verdicts plus aggregate also match.','','| Channel | Baseline expected / actual | R14 expected / actual |','|---|---:|---:|']
for k in sorted(b):lines.append(f'| `{k}` | {b[k]!r} | {r[k]!r} |')
lines+=['','## Named verdicts','','| ID | Baseline | R14 |','|---|---|---|']
for k in sorted(verdicts['baseline']):lines.append(f'| `{k}` | {verdicts["baseline"][k]} | {verdicts["R14"][k]} |')
(A/'numerics.md').write_text('\n'.join(lines)+'\n')
print('PASS independent complete numerical/input/binding/cost/identity and protected-surface comparisons')
print('cost modules',len(costs),'channels',len(b),'ratios',ratios)
