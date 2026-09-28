"""Native study phases; no phase executes without the coordinator's candidate release."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

H=Path(__file__).resolve().parents[1]
ROOT=H.parents[3]
R=H/'results'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H))
SIMKIT=Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'
sys.path.insert(0,str(SIMKIT))
os.environ['PYTHONPATH']=os.pathsep.join([str(ROOT),str(SIMKIT),os.environ.get('PYTHONPATH','')])
os.environ['STUDY_REQUIRE_TEAX']='1'
import study

def read(p):return json.loads(p.read_text())
def write(p,value):p.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def point_key(p):
    return json.dumps({k:('bool',v) if isinstance(v,bool) else ('number',float(v)) for k,v in p.items()},sort_keys=True)
def cli(script,*args):
    return subprocess.run([str(ROOT/'.codex-test/run'),'python',str(ROOT/script),*map(str,args)],cwd=ROOT,capture_output=True,text=True)

def live(require_rulings=True):
    candidate=study.release(require_rulings=require_rulings)
    from exploration.stellarator_e2e.studies import study_route as route
    seal=read(route.PACKAGE_DIR/'contracts/package_contract.json')
    if seal['executable_fingerprint']!=candidate['candidate']['executable_fingerprint']:
        raise RuntimeError('Live package differs from released integration candidate')
    return route,candidate

def prepare():
    route,candidate=live(require_rulings=False)
    from exploration.stellarator_e2e.studies import oracle_entry as oe
    from scripts.study.verify import package_input_values
    for src,name in [(route.MANIFEST_PATH,'manifest.json'),(route.PACKAGE_DIR/'contracts/model_contract.json','model-contract.json'),(route.PACKAGE_DIR/'contracts/package_contract.json','package-contract.json')]:
        shutil.copy2(src,H/'preparation'/name)
    required=sorted(o['channel_name'] for o in read(H/'preparation/model-contract.json')['outputs'] if o['python_type'] in ('float','int'))
    write(H/'preparation/required-channels.json',required)
    write(H/'preparation/oracle-channels.json',sorted(oe.ORACLE_OUTPUT_TO_CHANNEL.values()))
    write(H/'preparation/resolved-defaults.json',package_input_values(route.PACKAGE_DIR))
    for name in ['verify_stellaris.py','oracle_finance.py','oracle_breeding.py','oracle_cooling.py','oracle_facilities.py']:
        source=ROOT/'exploration/stellarator_e2e'/name
        if source.exists():shutil.copy2(source,H/'preparation'/name)
    shutil.copy2(ROOT/'exploration/stellarator_e2e/studies/oracle_entry.py',H/'preparation/oracle_entry.py')
    shutil.copy2(ROOT/'exploration/stellarator_e2e/studies/study_route.py',H/'preparation/study_route.py')
    for source,name in [
        ('work/active/WI-068_layout-based-facilities/layout-capacity-design.md','layout-capacity-design.md'),
        ('work/active/WI-068_layout-based-facilities/design.md','facility-design.md'),
        ('work/active/WI-068_layout-based-facilities/audit.md','integrated-audit.md'),
        ('work/active/WI-068_layout-based-facilities/review.md','design-review.md'),
        ('work/orchestration/goals/layout-based-facilities/evidence/civil-cost-basis.md','civil-cost-basis.md'),
        ('work/orchestration/goals/layout-based-facilities/evidence/source-review.md','source-review.md'),
        ('work/orchestration/goals/layout-based-facilities/evidence/inventory.md','entering-account-boundaries.md'),
        ('work/orchestration/goals/layout-based-facilities/evidence/entering-replay.json','entering-replay.json'),
    ]:
        shutil.copy2(ROOT/source,H/'preparation'/name)
    run=cli('scripts/study/indicators.py','--package',route.PACKAGE_DIR,'--manifest',route.MANIFEST_PATH,'--groups',H/'axes.json','--out',H/'indicators.json')
    (R/'indicators.log').write_text(run.stdout+run.stderr)
    if run.returncode:raise RuntimeError('Indicators refused; inspect captured log')
    print('Prepared candidate identities, all scalar channel names, defaults and indicators')

def baseline():
    route,candidate=live()
    from scripts.study import preflight
    route.execute_baseline(R)
    result=preflight.run_gates(route.PACKAGE_DIR,route.MANIFEST_PATH,H/'axes.json',R/'package_identity.json',R/'baseline_result.json')
    write(R/'preflight_results.json',result)
    assert result['outcome']=='pass',result
    assert read(R/'package_identity.json')['identity']['digest']==candidate['candidate']['executable_fingerprint']
    print('Pinned baseline and preflight passed')

def scan():
    route,_=live()
    assert read(R/'preflight_results.json')['outcome']=='pass'
    from exploration.stellarator_e2e.studies import oracle_entry as oe
    from scripts.study.verify import derive_verdict,package_input_values
    params=package_input_values(route.PACKAGE_DIR);catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR);bindings=oe.operand_bindings()
    rows=[]
    for row in read(H/'preparation/candidate-proposals.json'):
        try:
            values=oe.evaluate(row['point'])
            verdicts={cid:'satisfied' if derive_verdict(cid,e,bindings,row['point'],params,values)[0] else 'violated' for cid,e in catalog.items()}
            rows.append(row|{'outcome':'evaluated','channels':values,'verdicts':verdicts})
        except Exception as error:
            rows.append(row|{'outcome':'refused','error':repr(error)})
    write(R/'oracle-scan.json',{'rows':rows,'scope':'Independent software scan; shared transport data are not independent physical validation'})
    if any(r['outcome']!='evaluated' for r in rows):raise RuntimeError('Oracle scan has refused cases; all retained')
    # Coordinator reviews scan and writes final proposals/window selection separately.
    # No automatic window acceptance is made by the scan.

    write(R/'predicate-catalog.json',catalog)
    print('Oracle scanned',len(rows),'candidates; coordinator window decision pending')

def execute():
    route,_=live()
    from scripts.study import preflight,verify
    from simkit.study.store import StudyStore
    assert read(R/'preflight_results.json')['outcome']=='pass'
    assert (H/'reviews/window-selection.md').exists()
    before=preflight.run_clean(route.PACKAGE_DIR);write(R/'execution-clean-before.json',before);assert before['outcome']=='pass'
    write(R/'execution-environment.json',{'repo_revision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'python_executable':sys.executable,'teax_root':str(Path(os.environ['STOP_PARSER_TEAX_ROOT']).resolve()),'candidate_pin':study.release()['candidate']['pin']})
    start=time.monotonic();cases,db=study.run()
    raw=[]
    for c in cases:
        raw.append({'candidate_id':c.candidate_id,'inputs':dict(c.inputs),'outputs':dict(c.outputs or {}),'verdicts':dict(c.verdicts or {}),'state':c.state,'headline':c.headline})
    write(R/'native-cases.json',raw)
    write(R/'execution-summary.json',{'cases':len(cases),'states':dict(Counter(c.state for c in cases)),'store':str(db.relative_to(H)),'elapsed_seconds':time.monotonic()-start})
    store=StudyStore(db)
    try:write(R/'store-compatibility.json',verify.compatibility_digest(store)[1])
    finally:store.close()
    prepared=route.prepare(route.PACKAGE_DIR,R/'entry-model-inspection')
    write(R/'entry-models.json',{k:{'module':v.__module__,'qualname':v.__qualname__,'schema':v.model_json_schema()} for k,v in prepared.entry_models.items()})
    after=preflight.run_clean(route.PACKAGE_DIR);write(R/'post-run-clean.json',after);assert after['outcome']=='pass'
    if any(c.state!='completed' for c in cases):raise RuntimeError('Unsuccessful native evaluations retained in store and native-cases.json')
    assert len(cases)==len(read(H/'preparation/proposals.json'))
    print('Executed',len(cases),'native cases; all results retained')

def verify_all():
    route,_=live()
    from scripts.study.verify import derive_verdict,evaluate_operand
    from exploration.stellarator_e2e.studies import oracle_entry as oe
    scan={point_key(r['point']):r for r in read(R/'oracle-scan.json')['rows']}
    catalog=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json');bindings=oe.operand_bindings()
    failures=[];strict_misses=[];scalar_count=predicate_count=0
    for case in read(R/'native-cases.json'):
        expected=scan[point_key(case['inputs'])]
        assert set(expected['channels']) <= set(case['outputs'])
        assert set(read(H/'preparation/required-channels.json')) <= set(case['outputs'])
        for channel,value in expected['channels'].items():
            got=case['outputs'][channel];scalar_count+=1
            if not math.isclose(got,value,rel_tol=1e-9,abs_tol=0):strict_misses.append({'case':case['candidate_id'],'channel':channel,'native':got,'oracle':value})
            if not math.isfinite(got) or not math.isclose(got,value,rel_tol=1e-9,abs_tol=1e-9):failures.append({'case':case['candidate_id'],'channel':channel,'native':got,'oracle':value})
        assert set(case['verdicts'])==set(catalog)==set(expected['verdicts'])
        for cid,e in catalog.items():
            predicate_count+=1
            oracle_verdict=expected['verdicts'][cid]
            native_derived='satisfied' if derive_verdict(cid,e,bindings,case['inputs'],defaults,case['outputs'])[0] else 'violated'
            if case['verdicts'][cid]!=oracle_verdict or case['verdicts'][cid]!=native_derived:failures.append({'case':case['candidate_id'],'constraint_id':cid,'native':case['verdicts'][cid],'oracle':oracle_verdict,'from_native_operands':native_derived})
    write(R/'oracle-all-points.json',{'outcome':'fail' if failures else 'pass','scalar_comparisons':scalar_count,'predicate_comparisons':predicate_count,'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'strict_relative_misses':strict_misses,'failures':failures,'limits':'Transport table data shared; this verifies independent implementation, not physical accuracy.Channels outside the captured oracle map remain native evidence only.'})
    db=H/read(R/'execution-summary.json')['store']
    run=cli('scripts/study/verify.py','--package',route.PACKAGE_DIR,'--manifest',route.MANIFEST_PATH,'--identity',R/'package_identity.json','--store',db,'--sample-size',str(len(read(H/'preparation/proposals.json'))),'--out',R/'verification_summary.json')
    (R/'generic-verification.log').write_text(run.stdout+run.stderr)
    if failures or run.returncode:raise RuntimeError('Verification refused; original failures and generic log retained')
    print('Verified',scalar_count,'scalar comparisons and',predicate_count,'predicates; generic verifier passed')

def export():
    route,_=live()
    proposals={point_key(r['point']):r for r in read(H/'preparation/proposals.json')}
    catalog=read(R/'predicate-catalog.json');rows=[]
    for case in read(R/'native-cases.json'):
        meta=proposals[point_key(case['inputs'])]
        row={'case_id':case['candidate_id'],'proposal_id':meta['id'],'family':meta['family'],'wholeplant_satisfied':all(x=='satisfied' for x in case['verdicts'].values())}
        row.update({'input:'+k:v for k,v in (read(H/'preparation/resolved-defaults.json')|case['inputs']).items()})
        row.update(case['outputs']);row.update(case['verdicts'])
        row['violated']=';'.join(catalog[cid]['source_local_identity'] for cid,status in case['verdicts'].items() if status!='satisfied');rows.append(row)
    write(R/'interpreted-cases.json',rows)
    with (R/'points.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['arm_id']+sorted({k for r in rows for k in r}));writer.writeheader();writer.writerows(dict(arm_id='arm-native',**r) for r in rows)
    print('Exported all inputs, scalar channels and predicates; failed checks retained')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','baseline','scan','execute','verify','export']);args=parser.parse_args()
    {'prepare':prepare,'baseline':baseline,'scan':scan,'execute':execute,'verify':verify_all,'export':export}[args.phase]()
