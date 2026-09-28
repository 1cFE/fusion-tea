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
def point_key(p):return json.dumps(p,sort_keys=True)
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
    assert len(required)==261,len(required)
    assert len(oe.ORACLE_OUTPUT_TO_CHANNEL)==245
    write(H/'preparation/required-channels.json',required)
    write(H/'preparation/oracle-channels.json',sorted(oe.ORACLE_OUTPUT_TO_CHANNEL.values()))
    write(H/'preparation/resolved-defaults.json',package_input_values(route.PACKAGE_DIR))
    for name in ['verify_stellaris.py','oracle_finance.py','oracle_breeding.py']:
        source=ROOT/'exploration/stellarator_e2e'/name
        if source.exists():shutil.copy2(source,H/'preparation'/name)
    shutil.copy2(ROOT/'exploration/stellarator_e2e/studies/oracle_entry.py',H/'preparation/oracle_entry.py')
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
    assert len(catalog)==20
    rows=[]
    for row in read(H/'preparation/candidate-proposals.json'):
        try:
            values=oe.evaluate(row['point']);assert len(values)==245
            verdicts={cid:'satisfied' if derive_verdict(cid,e,bindings,row['point'],params,values)[0] else 'violated' for cid,e in catalog.items()}
            defined=bool(values[route.P+'blanket__breeding__defined_flag'])
            if defined!=row['expected_breeding_defined']:raise ValueError('Unexpected applicability behavior')
            rows.append(row|{'outcome':'evaluated','channels':values,'verdicts':verdicts,'breeding_defined':defined})
        except Exception as error:
            rows.append(row|{'outcome':'refused','error':repr(error)})
    write(R/'oracle-scan.json',{'rows':rows,'scope':'Independent software scan; shared transport data are not independent physical validation'})
    if any(r['outcome']!='evaluated' for r in rows):raise RuntimeError('Oracle scan has refused cases; all retained')
    write(H/'preparation/proposals.json',read(H/'preparation/candidate-proposals.json'))
    (H/'reviews/window-selection.md').write_text('# Window selection after oracle scan\n\nExecutor check: the complete candidate list ran through the independent oracle after the released baseline/preflight. The supported window is the frozen transport domain, not a fitted feasibility boundary. The three deliberately unsupported diagnostics produce undefined breeding. All candidates are retained; no point is removed to improve feasibility. This is a sensitivity study and claims no whole-plant feasible anchor or optimum.\n')
    write(R/'predicate-catalog.json',catalog)
    print('Oracle scanned all13 candidates; final list retained unchanged')

def execute():
    route,_=live()
    from scripts.study import preflight,verify
    from simkit.study.store import StudyStore
    assert read(R/'preflight_results.json')['outcome']=='pass'
    assert (H/'reviews/window-selection.md').exists()
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
    assert len(cases)==13
    print('Executed13 native cases through stock StudyRunner; all results retained')

def verify_all():
    route,_=live()
    from scripts.study.verify import derive_verdict,evaluate_operand
    from exploration.stellarator_e2e.studies import oracle_entry as oe
    scan={point_key(r['point']):r for r in read(R/'oracle-scan.json')['rows']}
    catalog=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json');bindings=oe.operand_bindings()
    failures=[];strict_misses=[];scalar_count=predicate_count=0
    for case in read(R/'native-cases.json'):
        expected=scan[point_key(case['inputs'])];assert len(expected['channels'])==245 and len(case['outputs'])==261
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
    write(R/'oracle-all-points.json',{'outcome':'fail' if failures else 'pass','scalar_comparisons':scalar_count,'predicate_comparisons':predicate_count,'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'strict_relative_misses':strict_misses,'failures':failures,'limits':'Transport table data shared; this verifies independent implementation, not physical accuracy.16 native channels outside oracle map remain native evidence only.'})
    db=H/read(R/'execution-summary.json')['store']
    run=cli('scripts/study/verify.py','--package',route.PACKAGE_DIR,'--manifest',route.MANIFEST_PATH,'--identity',R/'package_identity.json','--store',db,'--sample-size','40','--out',R/'verification_summary.json')
    (R/'generic-verification.log').write_text(run.stdout+run.stderr)
    if failures or run.returncode:raise RuntimeError('Verification refused; original failures and generic log retained')
    print('All245 scalars and20 predicates verified at all13 cases; generic verifier passed')

def export():
    route,_=live();prefix=route.P
    proposals={point_key(r['point']):r for r in read(H/'preparation/proposals.json')}
    catalog=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json');rows=[]
    for case in read(R/'native-cases.json'):
        meta=proposals[point_key(case['inputs'])];inputs=defaults|case['inputs'];values=case['outputs'];defined=bool(values[prefix+'blanket__breeding__defined_flag'])
        def value(k,breeding=False):return values[prefix+k] if defined or not breeding else None
        row={'case_id':case['candidate_id'],'proposal_id':meta['id'],'family':meta['family'],'thickness_m':inputs[prefix+'blanket__blanket_t'],'R_m':inputs[prefix+'plasma__R'],'breeding_defined':defined,'breeding_interpretation':'conditional physical prediction' if defined else 'undefined numerical carriers; no physical deficit inferred','wholeplant_satisfied':all(x=='satisfied' for x in case['verdicts'].values()),'held_neutron_energy_multiplier':inputs[prefix+'blanket__mn']}
        for name in ['tbr_li6','tbr_li7','tbr_mean','tbr_std_error','interpolation_allowance','tbr_lower']:row[name]=value('blanket__breeding__'+name,True)
        for name in ['required_tbr','design_margin','fuel_margin','numerical_margin','production_rate','extracted_supply_rate','extraction_loss_rate','recycle_loss_rate','decay_rate','stock_growth_rate','balance_rate']:row[name]=value('breeding_adequacy__'+name,name not in {'required_tbr','recycle_loss_rate','decay_rate','stock_growth_rate'})
        for name,key in {'blanket_volume_m3':'rb__blanket_vol','coil_bore_m':'rb__r_coil','coil_centre_minor_radius_m':'rb__r_coil_centre','blanket_cost_dollars':'blanket__blanket_cost__cost','shield_cost_dollars':'shield__shield_cost__cost','magnet_capital_dollars':'magnet__magnet_capital_rollup__capital_cost','total_capital_dollars':'total_capital__total_capital','LCOE_dollars_MWh':'lcoe_calc__lcoe','thermal_power_MW':'pb__p_th','net_power_MW':'pb__p_net','availability':'calendar__availability'}.items():row[name]=value(key)
        row.update(case['verdicts']);row['violated']=';'.join(catalog[cid]['source_local_identity'] for cid,s in case['verdicts'].items() if s!='satisfied');rows.append(row)
    write(R/'interpreted-cases.json',rows)
    with (R/'points.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print('Exported complete cases, including explicit undefined diagnostics')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','baseline','scan','execute','verify','export']);args=parser.parse_args()
    {'prepare':prepare,'baseline':baseline,'scan':scan,'execute':execute,'verify':verify_all,'export':export}[args.phase]()
