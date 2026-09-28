"""Read-only isolation of sealed WI-096 gas-root errors; writes fresh --out receipts.

Decimal roots independently solve the unchanged series exchanger and bypass
equations with 70-digit arithmetic, starting from exact binary input floats.
Sealed native code is executed in memory with I/O adapters only; no files mutate.
"""
from __future__ import annotations
import argparse, ast, hashlib, json, math, sys, tarfile
from decimal import Decimal as D, localcontext
from pathlib import Path
from types import SimpleNamespace
import yaml

ROOT=Path(__file__).resolve().parents[4]
STUDY=ROOT/'exploration/component_alternatives/studies/20260926-design-study-component-alternatives'
ORACLE=ROOT/'exploration/component_alternatives'
P='component_alternatives__plant__'
sys.path.insert(0,str(ORACLE))
import verify

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def d(x):return D.from_float(x) if isinstance(x,float) else D(x)
def coefficient(ua,ch,cs):
    if ua==0 or ch==0 or cs==0:return D(0)
    low,high=min(ch,cs),max(ch,cs);ratio=low/high;ntu=ua/low
    if abs(1-ratio)<D('1e-10'):eps=ntu/(1+ntu)
    else:
        decay=(-ntu*(1-ratio)).exp();eps=(1-decay)/(1-ratio*decay)
    return low*eps

def network(x):
    v={k:d(v) for k,v in x.items()};assert v['network_mode']==0
    c=v['flow']*v['cp']/10**6;e=v['recuperator_effectiveness'];cold=v['cold_temperature']
    k=1-v['turbine_efficiency']*(1-(v['return_pressure']/v['turbine_pressure'])**((v['gamma']-1)/v['gamma']))
    coeff={b:coefficient(v[b+'_ua'],v[b+'_flow']*v[b+'_cp']/10**6,c) for b in ('he','divertor','pbli')}
    def evaluate(t):
        inlet=cold+e*max(k*t-cold,D(0));temp=inlet;heat=D(0);out={}
        for b in coeff:
            q=min(v[b+'_available'],coeff[b]*max(v[b+'_limit']-temp,D(0)))
            if b=='he':out=dict(heater_inlet=inlet,he_hot_bound_margin=v['he_limit']-temp-q/coeff[b],he_transferred=q)
            heat+=q;temp+=q/c
        return c*(t-inlet)-heat,out
    lo=cold;hi=max([lo]+[v[b+'_limit'] for b in coeff]);assert evaluate(lo)[0]<=0<=evaluate(hi)[0]
    for _ in range(230):
        mid=(lo+hi)/2
        if evaluate(mid)[0]>0:hi=mid
        else:lo=mid
    t=(lo+hi)/2;res,out=evaluate(t)
    out.update(turbine_temperature=t,closure_residual=res,bracket_low=lo,bracket_high=hi,expansion_factor=k)
    return out

def controller(x):
    v={k:d(v) for k,v in x.items()};ch=v['primary_flow']*v['primary_cp']/10**6;cs=v['secondary_flow']*v['secondary_cp']/10**6
    drive=max(v['primary_limit']-v['secondary_inlet'],D(0))
    def cap(f):return coefficient(v['ua'],(1-f)*ch,cs)*drive
    feasible=cap(D(0))>=v['duty'];lo=D(0);hi=1-D('1e-9')
    if feasible:
        assert cap(hi)<=v['duty']
        for _ in range(230):
            mid=(lo+hi)/2
            if cap(mid)>v['duty']:lo=mid
            else:hi=mid
        f=(lo+hi)/2
    else:f=D(0)
    return dict(bypass_fraction=f,bypass_flow=f*v['primary_flow'],capability_at_solution=cap(f),
                heat_residual=cap(f)-v['duty'],bracket_low=lo,bracket_high=hi,feasible=feasible)

def sealed_code(text,name,network_body=False):
    tree=ast.parse(text)
    tree.body=[n for n in tree.body if not (isinstance(n,ast.ImportFrom) and (n.module or '').startswith('component_alternatives_tea'))]
    def require(ok,message):
        if not ok:raise ValueError(message)
    env=dict(__name__=name,Network_Heat_Driven_ClosureInput=object,
             values=lambda x:{k.removesuffix('_in'):v for k,v in vars(x).items()},require=require,finish=lambda name,out:out)
    exec(compile(tree,name,'exec'),env)
    return env

def invoke(env,function,x):
    trace={}
    def tracer(frame,event,arg):
        if event=='return' and frame.f_code.co_name==function:
            for k in ('lo','hi','residual','iteration','f','mid','g_mid','g_lo','g_hi'):
                if k in frame.f_locals:trace[k]=frame.f_locals[k]
        return tracer
    sys.settrace(tracer)
    try:out=env[function](SimpleNamespace(**{k+'_in':v for k,v in x.items()}))
    finally:sys.settrace(None)
    return out,trace

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=args.out.resolve();md=out.with_suffix('.md')
    if out.exists() or md.exists():raise SystemExit('Use a fresh --out path; receipts are not overwritten')
    watched=[STUDY/'sealed-package.tar.gz',STUDY/'results/cases.json',STUDY/'snapshot.json',STUDY/'numerical-tolerances.json',
             ROOT/'models/designs/component_alternatives/plant.sysml',ORACLE/'verify.py',*ORACLE.glob('oracle*.py'),ORACLE/'oracle_matched_cycle_properties.json']
    before={str(p.relative_to(ROOT)):sha(p) for p in watched}
    with tarfile.open(STUDY/'sealed-package.tar.gz') as archive:
        read=lambda p:archive.extractfile('component_alternatives_tea/'+p).read()
        pipeline=yaml.safe_load(read('pipelines/pipeline.yaml'))['modules']
        sources={key:read(path) for key,path in dict(network='handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py',control='handwritten/loop_return_control/primary_bypass_control_impl.py').items()}
    net=sealed_code(sources['network'],'sealed_network');control=sealed_code(sources['control'],'sealed_control')
    def inputs(row,owner,outputs):
        result={}
        for key,binding in pipeline[P+owner+'__evaluate']['inputs'].items():
            channel=binding.split(' ',1)[1]
            result[key.removesuffix('_in')]=row['inputs'][channel.split('.',1)[1]] if channel.startswith('plant_params.') else outputs[channel.removesuffix('.root')]
        return result
    rows=json.loads((STUDY/'results/cases.json').read_text())['cases'];reports=[]
    for row in rows:
        if row['candidate_id'].split(':')[-1] not in ('c0480','c0484','c0481','c0482','c0485','c0206'):continue
        expected=verify.evaluate(row['inputs']);native=row['outputs']
        nx=inputs(row,'heat_exchangers',native);ox=inputs(row,'heat_exchangers',expected)
        cx=inputs(row,'return_control',native);ocx=inputs(row,'return_control',expected)
        replay,nt=invoke(net,'_reviewed_run_network_heat_driven_closure',nx)
        cr,ct=invoke(control,'calculate',cx)
        assert all(replay[k]==native[P+'heat_exchangers__evaluate__'+k] for k in replay)
        assert all(cr[k]==native[P+'return_control__evaluate__'+k] for k in cr)
        with localcontext() as ctx:
            ctx.prec=70
            accurate=network(nx);oracle_tuple_accurate=network(ox)
            local_control=controller(cx)
            fixed=dict(cx,secondary_inlet=accurate['heater_inlet']);corrected_control=controller(fixed)
            oracle_control=controller(ocx)
            native_bypass=d(native[P+'gas_boundary__evaluate__bypass_flow']);oracle_bypass=d(expected[P+'gas_boundary__evaluate__bypass_flow'])
            # Separate local controller error from closure input propagation.
            split=dict(native_minus_exact_same_inputs=native_bypass-local_control['bypass_flow'],
                       upstream_closure_propagation=local_control['bypass_flow']-corrected_control['bypass_flow'],
                       high_accuracy_minus_oracle=corrected_control['bypass_flow']-oracle_bypass)
            f=d(cr['bypass_fraction']);flow=d(cx['primary_flow'])
            cancel=dict(native_subtracted_flow=native_bypass,exact_product_of_native_f_and_flow=f*flow,
                        subtraction_and_product_roundoff=native_bypass-f*flow,
                        relative_subtraction_condition=(2*flow-native_bypass)/abs(native_bypass) if native_bypass else None)
            hot=d(native[P+'heat_exchangers__evaluate__he_hot_bound_margin']);ohot=d(expected[P+'heat_exchangers__evaluate__he_hot_bound_margin'])
            hot_split=dict(native_minus_exact_same_inputs=hot-accurate['he_hot_bound_margin'],
                           upstream_tuple_effect=accurate['he_hot_bound_margin']-oracle_tuple_accurate['he_hot_bound_margin'],
                           exact_oracle_tuple_minus_oracle=oracle_tuple_accurate['he_hot_bound_margin']-ohot)
            report=dict(case=row['case'],candidate_id=row['candidate_id'],all_predicates_pass=row['headline'],
                native_fingerprint=row['executable_fingerprint'],sealed_replay_bit_exact=True,
                exact_native_network_inputs=nx,exact_oracle_network_inputs=ox,
                exact_native_controller_inputs=cx,exact_oracle_controller_inputs=ocx,
                network_input_differences={k:dict(native=nx[k],oracle=ox[k]) for k in nx if nx[k]!=ox[k]},
                native_root_trace=nt,native_controller_trace=ct,
                native_network=replay,native_controller=cr,decimal_network_same_inputs=accurate,
                decimal_network_oracle_inputs=oracle_tuple_accurate,decimal_controller_same_inputs=local_control,
                decimal_controller_accurate_network=corrected_control,decimal_controller_oracle_inputs=oracle_control,
                bypass_error_decomposition=split,bypass_cancellation=cancel,hot_margin_error_decomposition=hot_split,
                original_comparison=dict(bypass_flow=dict(native=float(native_bypass),oracle=float(oracle_bypass)),
                    he_hot_bound_margin=dict(native=float(hot),oracle=float(ohot))))
            reports.append(report)
    after={str(p.relative_to(ROOT)):sha(p) for p in watched};assert after==before,'Protected diagnostic inputs changed during execution'
    result=dict(scope='Sealed original replay and independent 70-digit root isolation; no model/oracle/tolerance changes and no certification of future repairs',
                inputs_sha256=before,sealed_body_sha256={k:hashlib.sha256(v).hexdigest() for k,v in sources.items()},
                decimal_input_convention='Exact binary floats via Decimal.from_float; 230 bracket halvings at precision 70',cases=reports)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,default=str)+'\n')
    lines=['# Sealed gas-root numerical diagnosis','', 'The unchanged sealed native network and bypass bodies replay bit-exact in all six selected cases. The JSON retains exact input tuples, native root brackets, and independent 70-digit roots. No model, oracle, tolerance, or historical receipt was changed.','', '| Case | Native minus exact hot margin (K) | Local bypass error (kg/s) | Propagated closure error (kg/s) | Accurate bypass minus oracle (kg/s) |','| --- | ---: | ---: | ---: | ---: |']
    for r in reports:
        b=r['bypass_error_decomposition'];h=r['hot_margin_error_decomposition']
        lines.append(f"| {r['candidate_id'].split(':')[-1]} | {h['native_minus_exact_same_inputs']:.6E} | {b['native_minus_exact_same_inputs']:.6E} | {b['upstream_closure_propagation']:.6E} | {b['high_accuracy_minus_oracle']:.6E} |")
    lines+=['','## Interpretation','','[AGENT] Diagnosis covers original c0480/c0484 and nearby efficiency variants c0481/c0482/c0485, plus engineering-failing c0206. Each contribution is computed independently: the controller is first solved with its exact native inlet, then with the accurate exchanger inlet. The hot-margin decomposition separately substitutes the full oracle input tuple. The original oracle is only evaluated; its stopping behavior is not copied into these roots.','','Numerical interpretation and minimal repair rationale follow the values in the JSON; this evidence does not certify any future implementation.']
    md.write_text('\n'.join(lines)+'\n')
    print(json.dumps({'out':str(out),'cases':len(reports),'protected_inputs_unchanged':True}))

if __name__=='__main__':main()
