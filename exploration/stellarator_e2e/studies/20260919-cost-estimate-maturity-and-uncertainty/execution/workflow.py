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
def point_key(p):return json.dumps({k:float(v) for k,v in p.items()},sort_keys=True)
def cli(script,*args):
    return subprocess.run([str(ROOT/'.codex-test/run'),'python',str(ROOT/script),*map(str,args)],cwd=ROOT,capture_output=True,text=True)

def live():
    candidate=study.release()
    from exploration.stellarator_e2e.studies import study_route as route
    seal=read(route.PACKAGE_DIR/'contracts/package_contract.json')
    if seal['executable_fingerprint']!=candidate['candidate']['executable_fingerprint']:
        raise RuntimeError('Live package differs from released integration candidate')
    return route,candidate

def prepare():
    route,candidate=live()
    from exploration.stellarator_e2e.studies import oracle_entry as oe
    from scripts.study.verify import package_input_values
    for src,name in [(route.MANIFEST_PATH,'manifest.json'),(route.PACKAGE_DIR/'contracts/model_contract.json','model-contract.json'),(route.PACKAGE_DIR/'contracts/package_contract.json','package-contract.json')]:
        shutil.copy2(src,H/'preparation'/name)
    required=sorted(o['channel_name'] for o in read(H/'preparation/model-contract.json')['outputs'] if o['python_type'] in ('float','int'))
    mapped=set(oe.ORACLE_OUTPUT_TO_CHANNEL.values())
    native={o['channel_name'] for o in read(H/'preparation/model-contract.json')['outputs']}
    if not mapped <= native:raise RuntimeError(f'Oracle channels absent from native contract: {sorted(mapped-native)}')
    write(H/'preparation/coverage.json',{'native_numeric':len(required),'native_all':len(native),'mapped':len(mapped),'mapped_numeric':len(mapped & set(required)),'mapped_other':sorted(mapped-set(required)),'unmapped_numeric':sorted(set(required)-mapped),'unmapped_all':sorted(native-mapped)})
    write(H/'preparation/required-channels.json',required)
    write(H/'preparation/oracle-channels.json',sorted(oe.ORACLE_OUTPUT_TO_CHANNEL.values()))
    defaults=package_input_values(route.PACKAGE_DIR)
    write(H/'preparation/resolved-defaults.json',defaults)
    from proposals import build
    build(H,defaults)
    for name in ['verify_stellaris.py','oracle_finance.py','oracle_breeding.py','oracle_cooling.py','oracle_facilities.py','oracle_fuel_inventory.py','oracle_fuel_processing.py']:
        source=ROOT/'exploration/stellarator_e2e'/name
        if source.exists():shutil.copy2(source,H/'preparation'/name)
    shutil.copy2(ROOT/'exploration/stellarator_e2e/studies/oracle_entry.py',H/'preparation/oracle_entry.py')
    run=cli('scripts/study/indicators.py','--package',route.PACKAGE_DIR,'--manifest',route.MANIFEST_PATH,'--groups',H/'axes.json','--out',H/'indicators.json')
    (R/'indicators.log').write_text(run.stdout+run.stderr)
    if run.returncode:raise RuntimeError('Indicators refused; inspect captured log')
    from scripts.study import indicators
    parsed=indicators.read_pipelines(route.PACKAGE_DIR)
    fanout=[]
    for group in read(H/'axes.json')['groups']:
        keys=[item['key'] for item in group['keys']]
        siblings=sorted(key for key in defaults if key.endswith('__'+group['axis']))
        if siblings!=sorted(keys):raise RuntimeError(f'Unexpected input siblings: {group["axis"]} {siblings}')
        consumers=[]
        for module in parsed.modules.values():
            for name,port in module.inputs.items():
                if any(port.ref.endswith('.'+key) for key in keys):
                    consumers.append({'module':module.name,'input':name,'ref':port.ref,'pipeline':str(module.file.relative_to(route.PACKAGE_DIR)),'line':port.line})
        if not consumers:raise RuntimeError(f'No direct consumers for {keys}')
        fanout.append({'axis':group['axis'],'declared_keys':keys,'same_suffix_entry_keys':siblings,'direct_consumers':consumers,'finding':'All direct consumers of the authored public key captured; no declared tie.'})
    write(H/'preparation/fan-out-evidence.json',fanout)
    write(H/'preparation/indicator-summary.json',[{'axis':g['axis'],'indicator':'no_constraint_response' if g['no_constraint_response'] else 'constraints_reachable','constraints':[c['source_local_identity'] for c in g['constraints_reachable']]} for g in read(H/'indicators.json')['groups']])
    print('Prepared candidate identities, all scalar channel names, defaults, fan-out and indicators')

def baseline():
    route,candidate=live()
    assert read(H/'reviews/axis-rulings.json')['authorized_by']=='coordinator', 'Axis framing disposition required before native baseline'
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
            values=oe.evaluate(row['point']);assert set(values)==set(oe.ORACLE_OUTPUT_TO_CHANNEL.values())
            verdicts={cid:'satisfied' if derive_verdict(cid,e,bindings,row['point'],params,values)[0] else 'violated' for cid,e in catalog.items()}
            defined=bool(values[route.P+'blanket__breeding__defined_flag'])
            rows.append(row|{'outcome':'evaluated','channels':values,'verdicts':verdicts,'breeding_defined':defined})
        except Exception as error:
            rows.append(row|{'outcome':'refused','error':repr(error)})
    write(R/'oracle-scan.json',{'rows':rows,'scope':'Independent software scan; shared transport data are not independent physical validation'})
    if any(r['outcome']!='evaluated' for r in rows):raise RuntimeError('Oracle scan has refused cases; all retained')
    write(H/'preparation/proposals.json',read(H/'preparation/candidate-proposals.json'))
    (H/'reviews/window-selection.md').write_text('# Window selection after oracle scan\n\nExecutor check: the complete candidate list ran through the independent oracle after the released baseline/preflight. The finite list combines four reviewed source-interpretation/model-analogy axes at fixed design, with a matched zero-direct-contingency diagnostic and two separately labeled downtime stresses. The source envelope excludes the diagnostic and stress families; none is a probability distribution or a qualified procurement interval. All candidates are retained; no point is removed to improve feasibility. This is a sensitivity study and claims no whole-plant feasible anchor or optimum.\n')
    write(R/'predicate-catalog.json',catalog)
    print(f'Oracle scanned all{len(rows)} candidates; final list retained unchanged')

def execute():
    route,_=live()
    from scripts.study import preflight,verify
    from simkit.study.store import StudyStore
    assert read(R/'preflight_results.json')['outcome']=='pass'
    assert (H/'reviews/window-selection.md').exists()
    assert read(H/'reviews/window-release.json')['authorized_by']=='coordinator', 'Window release required before study execution'
    write(R/'execution-environment.json',{'repo_revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'launcher':'.codex-test/run','runtime_import_setup':'STOP_PARSER_TEAX_ROOT/packages/teax-simkit on sys.path/PYTHONPATH; STUDY_REQUIRE_TEAX=1','execution_revision_scope':'candidate code revision, before study result commit'})
    before=preflight.run_clean(route.PACKAGE_DIR);write(R/'execution-clean-before.json',before);assert before['outcome']=='pass'
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
    print(f'Executed{len(cases)} native cases through stock StudyRunner; all results retained')

def verify_all():
    route,_=live()
    from scripts.study.verify import derive_verdict,evaluate_operand
    from exploration.stellarator_e2e.studies import oracle_entry as oe
    scan={point_key(r['point']):r for r in read(R/'oracle-scan.json')['rows']}
    catalog=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json');bindings=oe.operand_bindings()
    failures=[];strict_misses=[];scalar_count=predicate_count=0
    for case in read(R/'native-cases.json'):
        expected=scan[point_key(case['inputs'])]
        assert set(expected['channels'])==set(oe.ORACLE_OUTPUT_TO_CHANNEL.values())
        numeric=set(read(H/'preparation/required-channels.json'))
        boolean={o['channel_name'] for o in read(H/'preparation/model-contract.json')['outputs'] if o['python_type']=='bool'}
        assert set(case['outputs'])==numeric|boolean
        for channel,value in expected['channels'].items():
            got=case['outputs'][channel];scalar_count+=1
            if not math.isclose(got,value,rel_tol=1e-9,abs_tol=0):strict_misses.append({'case':case['candidate_id'],'channel':channel,'native':got,'oracle':value})
            if not math.isfinite(got) or not math.isclose(got,value,rel_tol=1e-9,abs_tol=1e-18 if '__fuel_cycle__inventory__' in channel else 1e-9):failures.append({'case':case['candidate_id'],'channel':channel,'native':got,'oracle':value})
        assert set(case['verdicts'])==set(catalog)==set(expected['verdicts'])
        for cid,e in catalog.items():
            predicate_count+=1
            oracle_verdict=expected['verdicts'][cid]
            native_derived='satisfied' if derive_verdict(cid,e,bindings,case['inputs'],defaults,case['outputs'])[0] else 'violated'
            if case['verdicts'][cid]!=oracle_verdict or case['verdicts'][cid]!=native_derived:failures.append({'case':case['candidate_id'],'constraint_id':cid,'native':case['verdicts'][cid],'oracle':oracle_verdict,'from_native_operands':native_derived})
    write(R/'oracle-all-points.json',{'outcome':'fail' if failures else 'pass','scalar_comparisons':scalar_count,'predicate_comparisons':predicate_count,'relative_tolerance':1e-9,'absolute_tolerance':{'inventory':1e-18,'inherited':1e-9},'strict_relative_misses':strict_misses,'failures':failures,'limits':'Transport data and source assumptions shared; this verifies independent implementation, not physical accuracy. Exact omitted native channels are in preparation/coverage.json.','mapped_channels':len(set(oe.ORACLE_OUTPUT_TO_CHANNEL.values())),'oracle_semantic_names':len(oe.ORACLE_OUTPUT_TO_CHANNEL),'authored_predicates':len(catalog),'unmapped_native_numeric':read(H/'preparation/coverage.json')['unmapped_numeric']})
    db=H/read(R/'execution-summary.json')['store']
    run=cli('scripts/study/verify.py','--package',route.PACKAGE_DIR,'--manifest',route.MANIFEST_PATH,'--identity',R/'package_identity.json','--store',db,'--sample-size',str(len(read(R/'native-cases.json'))),'--out',R/'verification_summary.json')
    (R/'generic-verification.log').write_text(run.stdout+run.stderr)
    if failures or run.returncode:raise RuntimeError('Verification refused; original failures and generic log retained')
    print(f'All {len(set(oe.ORACLE_OUTPUT_TO_CHANNEL.values()))} unique mapped channels and {len(catalog)} predicates verified at every case; generic verifier passed')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','baseline','scan','execute','verify']);args=parser.parse_args()
    {'prepare':prepare,'baseline':baseline,'scan':scan,'execute':execute,'verify':verify_all}[args.phase]()
