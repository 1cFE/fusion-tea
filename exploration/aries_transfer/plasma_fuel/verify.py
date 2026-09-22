"""WI-085 actual native calculated-plasma to fuel/capacity integration proof."""
import ast
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
EVIDENCE=ROOT/'work/active/WI-085_aries-calculated-plasma-to-fuel-integration/evidence'
PACKAGE=HERE/'generated'
NAME='plasma_fuel_tea'
PLASMA='aries_cs_plasma_integration__plasma__'
FUEL='aries_plasma_fuel__fuel_system__flows__'
CAPACITY='aries_plasma_fuel__processing__capacity__'
PROCESSING='aries_plasma_fuel__processing__'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    import syside
    staged=HERE/'staged_models'
    staged.mkdir(exist_ok=True)
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    sources=[ROOT/path for path in [
        'models/library/analyses/supplied_profile_plasma.sysml',
        'models/library/analyses/radial_density_profile.sysml',
        'models/library/analyses/mfe_plasma_scaling.sysml',
        'models/library/analyses/mfe_fuel_cycle.sysml',
        'models/library/analyses/mfe_viability.sysml',
        'models/designs/aries_cs_transfer/plasma_integration.sysml',
        'models/designs/aries_cs_transfer/plasma_fuel.sysml']]
    for source in sources:
        shutil.copy2(source,staged/source.name)
    _,diagnostics=syside.try_load_model([str(path) for path in sources])
    errors=[str(item) for category in ('parser','sema') for item in getattr(diagnostics,category)
            if item.severity==syside.DiagnosticSeverity.Error]
    (EVIDENCE/'parse.json').write_text(json.dumps({'errors':errors},indent=2)+'\n')
    assert not errors,errors
    command=[str(ROOT/'.codex-test/run'),'sysml-codegen','generate','--models',str(staged),
             '--output',str(PACKAGE),'--package-name',NAME,'--overwrite']
    with (EVIDENCE/'generation.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    completions=[
        ('exploration/aries_transfer/plasma_integration/supplied_profile_plasma_impl.py',
         'supplied_profile_plasma/supplied_profile_plasma_impl.py','aries_plasma_tea'),
        ('exploration/aries_transfer/density_profile/radial_density_profile_impl.py',
         'radial_density_profile/radial_density_profile_impl.py','aries_density_tea'),
        ('exploration/stellarator_e2e/generated/handwritten/mfe_viability/offered_capacity_screen_impl.py',
         'mfe_viability/offered_capacity_screen_impl.py','stellarator_tea')]
    receipts=[]
    for relative,target_relative,old_prefix in completions:
        source=ROOT/relative
        target=PACKAGE/'handwritten'/target_relative
        target.write_text(source.read_text().replace('from '+old_prefix+'.','from '+NAME+'.'))
        assert target.read_text().replace('from '+NAME+'.','from '+old_prefix+'.')==source.read_text()
        receipts.append({'source':relative,'source_sha256':sha(source),'target_sha256':sha(target),'prefix_only':True})
    kernel=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py'
    node=next(node for node in ast.parse(kernel.read_text()).body if isinstance(node,ast.FunctionDef) and node.name=='_sigv_dt')
    target=PACKAGE/'handwritten/supplied_profile_plasma/reused_reactivity.py'
    target.write_text('"""Unchanged accepted kernel; integration guards its domain."""\nimport math\n\n'+ast.get_source_segment(kernel.read_text(),node)+'\n')
    with (EVIDENCE/'generation-completed.log').open('w') as log:
        subprocess.run(command+['--preserve-handwritten'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    wrapper=(PACKAGE/'modules/supplied_profile_plasma/supplied_profile_plasma.py').read_text()
    order=re.search(r'^        ([\w, ]+) = run_supplied_profile_plasma\(validated_inputs\)',wrapper,re.M).group(1)
    seed_tree=ast.parse((ROOT/completions[0][0]).read_text())
    expected=next(ast.literal_eval(item.value) for item in seed_tree.body if isinstance(item,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='OUTPUT_ORDER' for t in item.targets))
    assert tuple(order.split(', '))==expected,order
    for relative,target_relative,old_prefix in completions:
        assert (PACKAGE/'handwritten'/target_relative).read_text().replace('from '+NAME+'.','from '+old_prefix+'.')==(ROOT/relative).read_text()
    receipt={'sources':{str(p.relative_to(ROOT)):sha(p) for p in sources},
             'staged':{str(p.relative_to(ROOT)):sha(staged/p.name) for p in sources},'completions':receipts,
             'reactivity_ast_sha256':hashlib.sha256(ast.dump(node).encode()).hexdigest()}
    assert receipt['sources']==receipt['staged']
    (EVIDENCE/'reuse-identity.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def verify(receipt):
    import yaml
    from simkit.core.pipeline import execute_pipeline
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module,fingerprint=ProvisionalPackageLoader(package_dir=PACKAGE,package_name=NAME,link_root=HERE/'links').load()
    registry=module.create_plasma_fuel_tea_registry()
    original_pipeline=yaml.safe_load((PACKAGE/'pipelines/pipeline.yaml').read_text())
    fuel_module=original_pipeline['modules']['aries_plasma_fuel__fuel_system__flows']
    binding=fuel_module['inputs']['p_fus_in']
    assert binding=='float '+PLASMA+'integration__fusion_power_MW',binding
    from plasma_fuel_tea.schemas.fuel_cycle_flows_output import Fuel_Cycle_FlowsOutput
    baseline_path=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/fuel_cycle_flows_impl.py'
    namespace={}
    exec(compile(baseline_path.read_text().replace('from stellarator_tea.','from '+NAME+'.'),str(baseline_path),'exec'),namespace)
    baseline=namespace['run_fuel_cycle_flows']
    cases=[('nominal',{},True,True),
           ('amplitude_1_5',{PLASMA+'amplitude':7.5e20},False,True),
           ('insufficient_rating',{PROCESSING+'selected_rating_atoms_s':1e22},False,True),
           ('larger_rating',{PROCESSING+'selected_rating_atoms_s':3e22},True,True),
           ('unsupported_conditions',{PROCESSING+'assumed_conditions_supported':False},False,False),
           ('unsupported_plasma',{PLASMA+'temperature_edge':.023},None,None)]
    rows=[]
    for name,changes,expected_ok,expected_defined in cases:
        folder=HERE/'native_runs'/name
        folder.mkdir(parents=True,exist_ok=True)
        spec=yaml.safe_load((PACKAGE/'pipelines/pipeline.yaml').read_text())
        effective={}
        paths=[]
        for key,entry in spec['modules']['entry_fusion']['inputs'].items():
            schema,relative=entry.split(' ',1)
            values=json.loads((PACKAGE/'pipelines'/relative).read_text())
            for parameter in values:
                if parameter in changes:values[parameter]=changes[parameter]
            if key=='mfe_viability_params':values={k:bool(v) for k,v in values.items()}
            assert not any('fusion_load' in key or key.endswith('__p_fus_in') for key in values),values
            path=folder/(key+'.json')
            path.write_text(json.dumps(values,indent=2)+'\n')
            paths.append((path,values))
            spec['modules']['entry_fusion']['inputs'][key]=schema+' '+str(path)
            effective.update(values)
        assert all(effective[key]==value for key,value in changes.items())
        pipeline=folder/'pipeline.yaml'
        pipeline.write_text(yaml.safe_dump(spec,sort_keys=False))
        try:
            result=execute_pipeline(pipeline,folder/'outputs',registry=registry,custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        except Exception as error:
            assert name=='unsupported_plasma',str(error)
            assert 'profile integration outside declared domain' in str(error),str(error)
            rows.append({'case':name,'status':'refused','error':str(error),'effective_inputs':effective})
            continue
        assert name!='unsupported_plasma'
        output={k:(v.model_dump(mode='json') if hasattr(v,'model_dump') else v) for k,v in result.outputs.items()}
        power=output[PLASMA+'integration__fusion_power_MW']
        inputs=SimpleNamespace(p_fus_in=power,q_eff_in=17.58,mev_to_joules_in=1.6021766339999998e-13,
            burn_fraction_in=.05,t_recycle_in=.99,tbr_available_in=0.,eta_extract_in=1.,
            lambda_T_in=1.782785958230312e-09,I_total_in=0.,G_stock_in=0.,
            m_T_kg_in=5.008267663228036e-27,s_per_fpy_in=31536000.)
        reference=dict(zip(Fuel_Cycle_FlowsOutput.model_fields,baseline(inputs)))
        for key,value in reference.items():assert output[FUEL+key]==value,(name,key,output[FUEL+key],value)
        with localcontext() as context:
            context.prec=50
            burn=float(Decimal(str(power))*Decimal('1e6')/(Decimal('17.58')*Decimal('1.6021766339999998e-13')))
        assert math.isclose(output[FUEL+'burn_rate'],burn,rel_tol=2e-15)
        assert math.isclose(output[FUEL+'inject_rate'],output[FUEL+'burn_rate']+output[FUEL+'exhaust_rate'],rel_tol=2e-15)
        assert math.isclose(output[FUEL+'loss_rate'],.01*output[FUEL+'exhaust_rate'],rel_tol=2e-15)
        rating=effective[PROCESSING+'selected_rating_atoms_s']
        assert output[CAPACITY+'margin']==rating-output[FUEL+'exhaust_rate']
        assert output[CAPACITY+'capacity_ok'] is expected_ok
        assert output[CAPACITY+'evaluation_defined']==float(expected_defined)
        report=output['constraint_report']
        assert report['assessed_entry_count']==1
        assert report['results'][0]['status']==('satisfied' if expected_ok else 'violated')
        for path,values in paths:assert json.loads(path.read_text())==values
        rows.append({'case':name,'status':'evaluated','fusion_power_MW':power,'selected_rating_atoms_s':rating,
                     'effective_inputs':effective,'outputs':output,'exact_flow_checks':len(reference)})
    nominal,amplitude,insufficient,larger,unsupported=rows[:5]
    assert nominal['selected_rating_atoms_s']==amplitude['selected_rating_atoms_s']==2e22
    assert math.isclose(amplitude['fusion_power_MW'],2.25*nominal['fusion_power_MW'],rel_tol=2e-14)
    assert math.isclose(amplitude['outputs'][FUEL+'exhaust_rate'],2.25*nominal['outputs'][FUEL+'exhaust_rate'],rel_tol=2e-14)
    assert all(row['fusion_power_MW']==nominal['fusion_power_MW'] for row in [insufficient,larger,unsupported])
    evidence={'claim':'Calculated conditioned plasma to fuel demand and selected tritium capacity; no ARIES equipment qualification',
              'fingerprint':str(fingerprint),'reuse':receipt,'actual_fuel_load_binding':binding,
              'cases':rows,'exact_flow_checks':sum(row.get('exact_flow_checks',0) for row in rows),'passed':True}
    (EVIDENCE/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({'passed':True,'cases':len(rows),'exact_flow_checks':evidence['exact_flow_checks'],
        'actual_fuel_load_binding':binding,'nominal_fusion_MW':nominal['fusion_power_MW'],
        'nominal_exhaust_atoms_s':nominal['outputs'][FUEL+'exhaust_rate'],
        'raised_fusion_MW':amplitude['fusion_power_MW'],
        'raised_exhaust_atoms_s':amplitude['outputs'][FUEL+'exhaust_rate'],
        'fixed_rating_atoms_s':2e22},indent=2))


if __name__=='__main__':
    verify(build())
