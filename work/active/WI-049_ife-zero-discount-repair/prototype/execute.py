from pathlib import Path
import json
from decimal import Decimal as D, localcontext
from sysml_codegen.cli import GenerationConfig, run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
from tests.ife_oracle import BASE, BOUNDARIES, PREFIX as P

root=Path(__file__).resolve().parent
package=root/'generated'
config=dict(models_path=root/'models',output_path=package,package_name='wi049_probe',overwrite=True)
assert run_codegen(GenerationConfig(**config))
hand=package/'handwritten/ife_lcoe'
(hand/'ife_present_value_factors_impl.py').write_text((root/'factors_impl.py').read_text())
price=Path('exploration/ife_e2e/generated/handwritten/ife_lcoe/generating_electricity_price_impl.py').read_text().replace('ife_tea.', 'wi049_probe.')
(hand/'generating_electricity_price_impl.py').write_text(price)
assert run_codegen(GenerationConfig(**config,preserve_handwritten=True))
def tree():
    return {p.relative_to(package).as_posix():p.read_bytes() for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
original=tree()
assert run_codegen(GenerationConfig(**config,preserve_handwritten=True))
assert tree()==original
assert run_codegen(GenerationConfig(**config,preserve_handwritten=True,smart_regen=True))
assert tree()==original
print('PASS byte equality: preserve and smart regeneration')
ev=PreparedEvaluator(ProvisionalPackageLoader(package,'wi049_probe',root/'link'),package/'pipelines/pipeline.yaml',expects_constraint_report=True)
bridge=CandidateBridge(ev.entry_models)
# Independent Decimal annual inputs and directly dated streams for integral years.
def reference(overrides):
    with localcontext() as ctx:
        ctx.prec=80
        v={k:D(str(x)) for k,x in (BASE | overrides).items()}
        beam=v['driver__beam_energy_mj']*D('1e6'); bank=beam/v['driver__efficiency']; f=v['frequency']
        fusion=beam*v['gain']; net=fusion*f*v['chamber__blanket_energy_multiple']*v['thermal_efficiency']-2*bank*f
        shots=D(31557600)*f*v['availability']
        procurement=(D('.32')+D('.088')*beam/D('1e6'))*(D('1.25')+D('.05')*v['driver__num_chambers'])*(1+D('.0088')*(f-5))*D('1e9')
        capital=v['plant_cost_constant']*net/1000+v['chamber__yield_cost_constant']*fusion/D('1e9')+procurement
        operating=v['target_factory__cost_per_target']*shots+v['om_cost_constant']*net/1000+procurement*shots/v['driver__lifetime_shots']
        annual=net/D('1e6')*8760*v['availability']
        yc=v['lcoe_calc__construction_years']; no=v['lcoe_calc__operational_years']; d=v['discount_rate']
        integer=yc==int(yc) and no==int(no)
        if integer:
            cf=sum((1+d)**(-y) for y in range(1,int(yc)+1))
            of=sum((1+d)**(-y) for y in range(int(yc)+1,int(yc+no)+1))
        elif d==0:
            cf=yc; of=no
        else:
            cf=(1-(1+d)**(-yc))/d
            of=((1+d)**(-yc)-(1+d)**(-yc-no))/d
        cost=capital/yc*cf+operating*of; energy=annual*of
        return {k:float(x) for k,x in dict(discounted_cost=cost,discounted_energy=energy,price=cost/energy if net>0 else 0,construction_factor=cf,operation_factor=of).items()}, 'dated_integer_sums' if integer else 'fractional_algebra'
rates=[.08,0.]+[s*10.**(-n) for n in (4,8,12,14,16,18) for s in (1,-1)]
rows=[]
for yc,no in ((5.,40.),(5.5,40.5),(.25,.5),(1.,1.),(20.,100.),(50.5,200.5)):
    for name,mutation in [('baseline',{}),('zero',BOUNDARIES['zero']),('negative',BOUNDARIES['counterexample'])]:
        for rate in rates + ([.5,-.5] if name=='baseline' else []):
            overrides=mutation | {'discount_rate':rate,'lcoe_calc__construction_years':yc,'lcoe_calc__operational_years':no}
            candidate=mutation | {'discount_rate':rate,'construction_duration':yc,'operational_duration':no}
            result=ev.evaluate(bridge.build({P+k:v for k,v in candidate.items()}))
            o=dict(result.outputs)
            actual={k:o[P+'lcoe_calc__'+k] for k in ('discounted_cost','discounted_energy')}
            actual['price']=o[P+'hawker_price__price']
            actual.update({k:o[P+'pv_factors__'+k] for k in ('construction_factor','operation_factor')})
            expected,kind=reference(overrides)
            errors={k:abs(actual[k]-x)/abs(x) if x else abs(actual[k]) for k,x in expected.items()}
            assert max(errors.values())<=1e-9,(name,yc,no,rate,errors)
            assert o[P+'hawker_price__generating']==float(name=='baseline')
            rows.append(dict(scenario=name,construction=yc,operation=no,rate=rate,actual=actual,expected=expected,errors=errors,reference=kind,responses=dict(result.responses)))
(root/'execution.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS',len(rows),'sealed public executions; maximum channel error',max(max(r['errors'].values()) for r in rows))
print('zero baseline', rows[1]['actual'])
# Required tiny-positive point: explicitly expose independent ideal-decimal residual.
near=[]
for rate in [0.,1e-12,-1e-12,.08]:
    v=BOUNDARIES['positive_neighbor']|{'discount_rate':rate}
    result=ev.evaluate(bridge.build({P+k:x for k,x in v.items()}))
    expct,kind=reference(v); actual={k:result.outputs[P+'lcoe_calc__'+k] for k in ('discounted_cost','discounted_energy')}; actual['price']=result.outputs[P+'hawker_price__price']
    near.append(dict(rate=rate,actual=actual,expected=expct,errors={k:abs(x-expct[k])/abs(expct[k]) for k,x in actual.items()},net=result.outputs[P+'lcoe_calc__net_electric_power'],generating=result.outputs[P+'hawker_price__generating']))
(root/'positive-neighbor.json').write_text(json.dumps(near,indent=2)+'\n')
print('positive-neighbor ideal-decimal maximum',max(max(r['errors'].values()) for r in near))
