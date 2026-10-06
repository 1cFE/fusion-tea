"""Read-only failed-case investigation; candidate formula is patched in memory only.

No package/store file changes. Scratch pipeline receipts under /tmp are development
probes, not fingerprint-valid native evidence for the candidate formula.
"""
import hashlib
import importlib
import importlib.util
import json
import math
from pathlib import Path
import sqlite3
import sys
import tempfile

import mpmath as mp
mp.mp.dps=160

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
BASE=ROOT/'exploration/exchanger_architecture/thermal_requirements'
STORE=BASE/'studies/20260927-exchanger-thermal-comparison/results/native/20260927-exchanger-thermal-comparison.db'
BODY=BASE/'exchanger_architecture_thermal_tea/handwritten/controlled_exchanger_closure/controlled_network_heat_driven_closure_impl.py'
spec=importlib.util.spec_from_file_location('repair_probe_runner',BASE/'run.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)


def stable_conductance(ua,ch,cs):
    if ua<=0. or ch<=0.:return 0.
    low,high=min(ch,cs),max(ch,cs)
    ratio,ntu=low/high,ua/low
    if ratio==1.:
        epsilon=ntu/(1+ntu)
    else:
        loss=-math.expm1(-ntu*(1-ratio))
        epsilon=loss/((1-ratio)+ratio*loss)
    return epsilon*low


def denominator_only(ua,ch,cs):
    if ua<=0. or ch<=0.:return 0.
    low,high=min(ch,cs),max(ch,cs)
    ratio,ntu=low/high,ua/low
    if abs(1-ratio)<1e-10:return low*ntu/(1+ntu)
    return stable_conductance(ua,ch,cs)


def precise_conductance(ua,ch,cs,dps):
    with mp.workdps(dps):
        ua,ch,cs=map(mp.mpf,(ua,ch,cs))
        low,high=min(ch,cs),max(ch,cs);ratio=low/high;ntu=ua/low
        if ratio==1:epsilon=ntu/(1+ntu)
        else:
            loss=-mp.expm1(-ntu*(1-ratio))
            epsilon=loss/((1-ratio)+ratio*loss)
        return epsilon*low


def main():
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (BODY,STORE)}
    connection=sqlite3.connect('file:'+str(STORE.resolve())+'?mode=ro',uri=True)
    failures=[dict(candidate_id=cid,inputs=json.loads(raw),failure=json.loads(failure))
              for cid,raw,failure in connection.execute("select candidate_id,inputs_json,failure_json from cases where state='execution_failed' order by candidate_id")]
    connection.close()
    runtime=runner.load_runtime()
    body=importlib.import_module('exchanger_architecture_thermal_tea.handwritten.controlled_exchanger_closure.controlled_network_heat_driven_closure_impl')
    original=body.conductance
    temporary=Path(tempfile.mkdtemp(prefix='wi097-numerical-repair-'))
    rows=[]
    for failure in failures:
        captures=[]
        def trace(frame,event,arg):
            if event=='exception' and frame.f_code.co_name=='bypass_stage' and Path(frame.f_code.co_filename).name==BODY.name:
                typ,value,tb=arg
                if 'bypass solve did not converge' in str(value):
                    state={k:v for k,v in frame.f_locals.items() if isinstance(v,(float,int,str,bool))}
                    stack=[];parent=frame.f_back
                    while parent:
                        if parent.f_code.co_name in ('stage','evaluate','calculate'):
                            stack.append({'function':parent.f_code.co_name,
                                          'locals':{k:v for k,v in parent.f_locals.items() if isinstance(v,(float,int,str,bool))}})
                        parent=parent.f_back
                    captures.append({'state':state,'stack':stack,'exception':str(value)})
            return trace
        sys.settrace(trace)
        try:
            failed=runner.execute_case('original-'+failure['candidate_id'].rsplit(':',1)[-1],failure['inputs'],runtime,temporary)
        finally:
            sys.settrace(None)
        assert failed['status']=='refused' and captures
        stage=captures[-1]['state'];ua,ch,cs=stage['ua'],stage['ch'],stage['cs']
        drive=stage['drive'];q=stage['q_available']
        table=[]
        for label,f in [('lo',stage['lo']),('hi',stage['hi']),('last',stage['fraction'])]:
            active=(1-f)*ch
            precise80=precise_conductance(ua,active,cs,80)*mp.mpf(drive)
            precise120=precise_conductance(ua,active,cs,120)*mp.mpf(drive)
            ratio=min(active,cs)/max(active,cs)
            table.append({'label':label,'fraction':f,'active_capacity_mw_k':active,'capacity_ratio':ratio,
                          'one_minus_ratio':1-ratio,'native_residual_mw':original(ua,active,cs)*drive-q,
                          'denominator_only_residual_mw':denominator_only(ua,active,cs)*drive-q,
                          'candidate_residual_mw':stable_conductance(ua,active,cs)*drive-q,
                          'mp_residual_mw':float(precise120-mp.mpf(q)),
                          'mp80_vs_mp120_mw':float(abs(precise80-precise120))})
        body.conductance=stable_conductance
        try:
            candidate=runner.execute_case('candidate-'+failure['candidate_id'].rsplit(':',1)[-1],failure['inputs'],runtime,temporary)
            branch=next(x['locals']['b'] for x in captures[-1]['stack'] if x['function']=='stage')
            at_failure=body.bypass_stage(q,ua,ch,cs,stage['hot'],stage['secondary'])
        finally:
            body.conductance=original
        assert candidate['status']=='evaluated'
        active=(1-at_failure['bypass_fraction'])*ch
        precise_residual=float(precise_conductance(ua,active,cs,120)*mp.mpf(drive)-mp.mpf(q))
        rows.append(failure|{'original_reproduction':failed['error'],'captured_exceptions':captures,
                            'failed_branch':branch,'last_bracket':table,
                            'candidate_at_failed_trial':at_failure,'candidate_mp_residual_mw':precise_residual,
                            'candidate_outputs':candidate['outputs'],
                            'candidate_probe_kind':'in-memory formula substitution, not fingerprint-valid native evidence'})
    # Distinguish cancellation outside the old cutoff from its discontinuous
    # equal-capacity approximation. All three candidates use the same solver.
    conditioning=[]
    for delta in (-1e-4,-1e-6,-1e-8,-2e-10,-1.0001e-10,-.9999e-10,-5e-11,0.,5e-11,.9999e-10,1.0001e-10,2e-10,1e-8,1e-6,1e-4):
        ua,cs=18.,6.;ch=cs*(1+delta)
        precise=float(precise_conductance(ua,ch,cs,120))
        conditioning.append({'relative_capacity_offset':delta,'ua_mw_k':ua,'ch_mw_k':ch,'cs_mw_k':cs,
                             'original_error_mw_k':original(ua,ch,cs)-precise,
                             'denominator_only_error_mw_k':denominator_only(ua,ch,cs)-precise,
                             'candidate_error_mw_k':stable_conductance(ua,ch,cs)-precise})
    root_fixtures=[]
    for delta in (-2e-10,-1.0001e-10,-.9999e-10,-5e-11,0.,5e-11,.9999e-10,1.0001e-10,2e-10):
        ua,ch,cs,hot,secondary=18.,12.,6.,800.,500.
        desired_active=cs*(1+delta)
        duty=float(precise_conductance(ua,desired_active,cs,120)*(hot-secondary))
        fixture={'capacity_offset':delta,'ua_mw_k':ua,'primary_capacity_mw_k':ch,'secondary_capacity_mw_k':cs,
                 'hot_k':hot,'secondary_in_k':secondary,'duty_mw':duty,'expected_bypass':1-desired_active/ch}
        for label,fn in (('original',original),('denominator_only',denominator_only),('continuous_candidate',stable_conductance)):
            body.conductance=fn
            try:
                result=body.bypass_stage(duty,ua,ch,cs,hot,secondary)
                active=(1-result['bypass_fraction'])*ch
                residual=float(precise_conductance(ua,active,cs,120)*(hot-secondary)-duty)
                fixture[label]={'status':'evaluated','bypass_fraction':result['bypass_fraction'],
                                'independent_residual_mw':residual,
                                'native_residual_mw':result['capability_at_solution']-duty}
            except ValueError as error:
                fixture[label]={'status':'refused','error':str(error)}
            finally:
                body.conductance=original
        root_fixtures.append(fixture)
    after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (BODY,STORE)}
    assert before==after,'preserved artifacts changed'
    result={'kind':'development numerical investigation only','scratch':str(temporary),
            'preserved_hashes':before,'preservation_pass':True,'failed_cases':rows,'conditioning':conditioning,'root_fixtures':root_fixtures,
            'candidate_change':'algebraically equivalent denominator: (1-r)+r*(-expm1(-NTU*(1-r)))',
            'equality_limit':'Analytic equal-capacity limit only at Cr==1; stable unequal-capacity equation otherwise.',
            'unchanged':'inputs, equations,1e-10MW bypass residual,100iterations,cycle tolerances,requirements,offers,oracle'}
    (HERE/'numerical-repair-probe.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'preserved':True,'failures':[{'candidate_id':r['candidate_id'],'branch':r['failed_branch'],
              'bracket':r['last_bracket'],'candidate_mp_residual_mw':r['candidate_mp_residual_mw']} for r in rows]},indent=2))


if __name__=='__main__':main()
