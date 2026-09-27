"""WI-096 independent calculation oracle and native receipt verification.

Bindings are read from the authored, additive SysML (not native pipeline math).
Physics/accounting use independent retained/adapted oracles; no native body import.
Native manifest bindings are used only to identify constraint operands. Solver
iteration counts are diagnostics and excluded from independent value comparisons.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import json,math,re,sys
from pathlib import Path
import yaml
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PACKAGE=HERE/'component_alternatives_tea';P='component_alternatives__plant__'
sys.path.insert(0,str(HERE))
import oracle_gas,oracle_matched_cycle

@lru_cache(None)
def authored():
    text=(ROOT/'models/designs/component_alternatives/plant.sysml').read_text()
    text=re.sub(r'/\*.*?\*/','',text,flags=re.S)
    matches=list(re.finditer(r'^        part (\w+)[^\n]*\{',text,re.M))
    attrs=[];calcs=[]
    for i,m in enumerate(matches):
        owner=m.group(1);chunk=text[m.end():matches[i+1].start() if i+1<len(matches) else text.rfind('\n    }')]
        attrs.extend((owner,name,typ,expr.strip()) for name,typ,expr in re.findall(r'attribute (\w+) : (Real|Boolean) = ([^;]+);',chunk))
        for name,definition,body in re.findall(r"calc (\w+) : '([^']+)' \{(.*?)\}",chunk,re.S):
            bindings=dict(re.findall(r'in (\w+) = ([^;]+);',body))
            calcs.append((owner,name,definition,{k:v.strip() for k,v in bindings.items()}))
    return attrs,calcs

def defaults():
    result={}
    for path in sorted((PACKAGE/'inputs').glob('*_params.json')):result.update(json.loads(path.read_text()))
    return result
def literal(expr):
    if expr in ('true','false'):return expr=='true'
    try:return float(expr)
    except ValueError:return None

def primary_control(v):
    from scipy.optimize import brentq
    ch=v['primary_flow']*v['primary_cp']/1e6;cs=v['secondary_flow']*v['secondary_cp']/1e6
    drive=max(v['primary_limit']-v['secondary_inlet'],0)
    def capability(f):
        a=(1-f)*ch;lo,hi=min(a,cs),max(a,cs)
        if lo<=0 or v['ua']<=0 or drive<=0:return 0.,0.,0.
        cr=lo/hi;ntu=v['ua']/lo
        eps=ntu/(1+ntu) if abs(cr-1)<1e-10 else -math.expm1(-ntu*(1-cr))/(1-cr*math.exp(-ntu*(1-cr)))
        return eps*lo*drive,eps,ntu
    open_heat=capability(0)[0];feasible=open_heat>=v['duty']
    f=brentq(lambda z:capability(z)[0]-v['duty'],0,1-1e-9,xtol=5e-16,rtol=1e-15) if feasible else 0.
    heat,eps,ntu=capability(f);back=v['primary_limit']-heat/((1-f)*ch)
    mixed=v['primary_limit']-heat/ch;residual=mixed-v['required_return']
    return dict(bypass_fraction=f,feasible=float(feasible),capability_open=open_heat,capability_at_solution=heat,
      exchanger_primary_flow=(1-f)*v['primary_flow'],exchanger_return=back,mixed_return=mixed,return_residual=residual,
      return_residual_magnitude=abs(residual),effectiveness_at_solution=eps,ntu_at_solution=ntu)

def calculate(definition,v,owner,calc,gas):
    import oracle_thermal,oracle_cooling
    prefix=P+owner+'__'+calc+'__'
    known={k[len(prefix):]:value for k,value in gas.items() if k.startswith(prefix)}
    if known:return known
    if definition=='Cooling Equipment With Selected Salt Pump Count':return oracle_cooling.calculate(v)
    if definition=='Matched Steam Cycle':return oracle_matched_cycle.matched_interface(v)
    if definition=='Cooling Water Rejection':return oracle_matched_cycle.cooling_interface(v)
    if definition=='Primary Bypass Control':return primary_control(v)
    if definition=='Controlled Conversion Boundary':return oracle_thermal.boundary(v)
    if definition=='Finite Water Cooler':return oracle_thermal.cooler(v)
    if definition=='Recuperator Installed Capability':return oracle_thermal.recuperator(v)
    if definition=='Conversion Subsystem Ledger':return oracle_thermal.ledger(v)
    if definition=='Steam Offered Conditions':
        pairs=[k.removeprefix('actual_') for k in v if k.startswith('actual_')]
        supported=bool(v['enabled']) and all(abs(v['actual_'+k]-v['rated_'+k])<=8*max(math.ulp(v['actual_'+k]),math.ulp(v['rated_'+k])) for k in pairs)
        return dict(applicable=bool(v['enabled']),supported=supported,evaluation_defined=float(supported))
    if definition=='Offered Capacity Screen':
        active=bool(v['applicable']);ok=active and bool(v['conditions_supported']) and bool(v['demand_available'])
        margin=v['rating']-v['demand'] if active else 0.
        return dict(margin=margin,applicable=active,supported=ok,evaluation_defined=float(ok),capacity_ok=ok and margin>=0)
    if definition=='Pump Pressure Rise':return dict(demand=v['outlet_MPa']-v['inlet_MPa'] if v['active'] else 0.)
    if definition=='Selected Inventory Purchase':
        ratio=v['quantity']/v['reference_quantity']
        return dict(capital=v['reference_cost']*v['price_factor']*(ratio if v['mode']==0 else 1),purchased_quantity=v['quantity'],quantity_ratio=ratio,source_budget=v['reference_cost'],extrapolated=float(not .5<=ratio<=1.5))
    if definition=='Eight Amount Sum':return dict(total=math.fsum(v.values()))
    if definition=='Scaled Amount':return dict(amount=v['amount']*v['factor'])
    if definition=='Supplied Purchase Cost':return dict(cost=v['purchase_cost']*v['n_mod'])
    raise ValueError('unverified calculation definition '+definition+' at '+owner+'.'+calc)

def evaluate(point):
    values=defaults();unknown=set(point)-set(values)
    if unknown:raise ValueError('unknown oracle inputs '+repr(sorted(unknown)))
    values.update(point)
    attrs,calcs=authored();parts={a[0] for a in attrs};state={};result={}
    gas=oracle_gas.evaluate(values)
    def resolve(owner,expr):
        n=literal(expr)
        if n is not None:return n
        key=expr if expr.split('.')[0] in parts else owner+'.'+expr
        return state[key]
    pending_attrs=list(attrs);pending_calcs=list(calcs)
    while pending_attrs or pending_calcs:
        progress=False
        for item in pending_attrs[:]:
            owner,name,typ,expr=item
            # An unused iteration diagnostic has no independent analogue.
            if expr=='evaluate.iterations':pending_attrs.remove(item);continue
            try:v=values[P+owner+'__'+name] if P+owner+'__'+name in values else resolve(owner,expr)
            except KeyError:continue
            state[owner+'.'+name]=bool(v) if typ=='Boolean' else float(v)
            pending_attrs.remove(item);progress=True
        for item in pending_calcs[:]:
            owner,name,definition,bindings=item
            try:
                inputs={k.removesuffix('_in'):values[P+owner+'__'+name+'__'+k] if P+owner+'__'+name+'__'+k in values else resolve(owner,expr) for k,expr in bindings.items()}
            except KeyError:continue
            outputs=calculate(definition,inputs,owner,name,gas)
            for field,value in outputs.items():
                state[owner+'.'+name+'.'+field]=value;result[P+owner+'__'+name+'__'+field]=float(value)
            pending_calcs.remove(item);progress=True
        if not progress:raise ValueError('unresolved authored oracle bindings '+repr(pending_attrs[:4])+repr(pending_calcs[:2]))
    return result

@lru_cache(None)
def operand_bindings():
    pipeline=yaml.safe_load((PACKAGE/'pipelines/pipeline.yaml').read_text());result={}
    for cid,module in pipeline['modules'].items():
        if not module['module_type'].endswith('ConstraintModule'):continue
        bindings={}
        for formal,source in module['inputs'].items():
            key=source.split(' ',1)[1]
            bindings[formal]={'kind':'input' if key.split('.')[0].endswith('_params') else 'channel','key':key.split('.',1)[1] if key.split('.')[0].endswith('_params') else key}
        identity=module['outputs']['evaluation'].split(' ',1)[1].removesuffix('__evaluation')
        result[identity]=bindings
    return result

@lru_cache(None)
def comparison_catalog():
    # Explicit equation outputs from the fully independent model-specific oracle.
    return sorted(evaluate(defaults()))

@lru_cache(None)
def absolute_tolerances():
    """Declared numerical classes before the main study; no capacity allowances."""
    result={}
    for key in comparison_catalog():
        field=key.rsplit('__',1)[-1]
        if field in ('raw_heat_residual','duty_correction','ua_residual'):result[key]=1e-8
        elif 'residual' in field:result[key]=1e-6
        elif field=='bypass_fraction':result[key]=1e-10
    return result

def agreement(key,actual,expected):
    scale=max(abs(actual),abs(expected))
    relative=abs(actual-expected)/scale if scale else 0.
    return relative<1e-9 or abs(actual-expected)<absolute_tolerances().get(key,0.)

def predicate(operands):
    keys=set(operands)
    if keys=={'defined_in','margin_in'}:return operands['defined_in']>=1 and operands['margin_in']>=0
    if keys=={'margin_in'}:return operands['margin_in']>=0
    if keys=={'flag_in'}:return operands['flag_in']>=1
    if keys=={'residual_in','tolerance_in'}:return abs(operands['residual_in'])<=operands['tolerance_in']
    if keys=={'net_electric'}:return operands['net_electric']>0
    if keys=={'mdot_loop_in','mdot_loop_rated_in'}:return operands['mdot_loop_in']<=operands['mdot_loop_rated_in']
    if keys=={'p_loop_margin_in'}:return operands['p_loop_margin_in']>0
    raise ValueError('unverified predicate operands '+repr(keys))

def verify_row(row):
    if row['status']!='evaluated':return dict(status='refused',reason=row['error'],comparisons=0)
    expected=evaluate(row['effective_inputs']);native=row['outputs'];diffs=[]
    for key,value in expected.items():
        if key not in native:continue # unused independent bookkeeping channels are not claimed native comparisons
        if not agreement(key,float(native[key]),value):diffs.append(dict(channel=key,expected=value,actual=native[key]))
    bindings=operand_bindings();reports={v['constraint_id']:v for v in native['constraint_report']['results']}
    if set(reports)!=set(bindings):diffs.append(dict(constraint_census=sorted(set(reports)^set(bindings))))
    for cid,mapping in bindings.items():
        operands={k:(row['effective_inputs'] if v['kind']=='input' else expected)[v['key']] for k,v in mapping.items()}
        wanted='satisfied' if predicate(operands) else 'violated'
        if reports[cid]['status']!=wanted:diffs.append(dict(constraint=cid,expected=wanted,actual=reports[cid]['status']))
    scalar=[k for k,v in native.items() if isinstance(v,(float,int,bool))]
    omitted=[k for k in scalar if k not in expected]
    allowed=[k for k in omitted if k.endswith('__iterations')]
    if sorted(omitted)!=sorted(allowed):diffs.append(dict(uncovered_scalar=sorted(set(omitted)-set(allowed))))
    return dict(status='pass' if not diffs else 'fail',comparisons=len(set(expected)&set(scalar)),predicates=len(bindings),diagnostic_only=allowed,differences=diffs)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--runs',type=Path,default=ROOT/'work/active/WI-096_matched-conversion-subsystems/evidence/native_runs');parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    records={}
    for p in sorted(args.runs.glob('*/result.json')):
        if '.attempt' in p.parent.name:continue
        try:records[p.parent.name]=verify_row(json.loads(p.read_text()))
        except Exception as error:records[p.parent.name]=dict(status='verification_refused',error=repr(error))
    if args.out.exists():raise FileExistsError(args.out)
    args.out.write_text(json.dumps(records,indent=2)+'\n')
    for name,result in records.items():print(name,result['status'],result.get('differences',result.get('error','')))
    raise SystemExit(any(r['status'] in ('fail','verification_refused') for r in records.values()))
