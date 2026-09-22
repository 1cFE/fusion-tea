"""WI-083 build and native forward-contract verification. Run from repository root."""
import ast
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-083_aries-supplied-profile-plasma-integration/evidence'
PACKAGE = HERE / 'generated'
PREFIX = 'aries_cs_plasma_integration__plasma__'
KERNEL = ROOT / 'exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py'
DENSITY = ROOT / 'exploration/aries_transfer/density_profile/radial_density_profile_impl.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    import syside
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    staged = HERE / 'staged_models'
    staged.mkdir(exist_ok=True)
    sources = [ROOT / path for path in ['models/library/analyses/supplied_profile_plasma.sysml',
               'models/library/analyses/radial_density_profile.sysml',
               'models/library/analyses/mfe_plasma_scaling.sysml',
               'models/designs/aries_cs_transfer/plasma_integration.sysml']]
    for source in sources:
        shutil.copy2(source, staged/source.name)
    _, diagnostics = syside.try_load_model([str(path) for path in sources])
    errors = [str(item) for category in ('parser', 'sema') for item in getattr(diagnostics, category)
              if item.severity == syside.DiagnosticSeverity.Error]
    (EVIDENCE/'parse.json').write_text(json.dumps({'errors': errors}, indent=2)+'\n')
    assert not errors, errors
    command = [str(ROOT/'.codex-test/run'), 'sysml-codegen', 'generate', '--models', str(staged),
               '--output', str(PACKAGE), '--package-name', 'aries_plasma_tea', '--overwrite']
    with (EVIDENCE/'generation.log').open('w') as log:
        subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    target = PACKAGE/'handwritten/supplied_profile_plasma/supplied_profile_plasma_impl.py'
    shutil.copy2(HERE/'supplied_profile_plasma_impl.py', target)
    density_target = PACKAGE/'handwritten/radial_density_profile/radial_density_profile_impl.py'
    density_target.write_text(DENSITY.read_text().replace('from aries_density_tea.', 'from aries_plasma_tea.'))
    kernel_node = next(node for node in ast.parse(KERNEL.read_text()).body
                       if isinstance(node, ast.FunctionDef) and node.name == '_sigv_dt')
    kernel_source = ast.get_source_segment(KERNEL.read_text(), kernel_node)
    kernel_target = target.parent/'reused_reactivity.py'
    kernel_target.write_text('"""Unchanged existing DT kernel; caller enforces inherited .2..100 keV domain."""\nimport math\n\n'+kernel_source+'\n')
    with (EVIDENCE/'generation-completed.log').open('w') as log:
        subprocess.run(command+['--preserve-handwritten'], cwd=ROOT, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    assert target.read_bytes() == (HERE/'supplied_profile_plasma_impl.py').read_bytes()
    wrapper = (PACKAGE/'modules/supplied_profile_plasma/supplied_profile_plasma.py').read_text()
    actual_order = re.search(r'^        ([\w, ]+) = run_supplied_profile_plasma\(validated_inputs\)', wrapper, re.M).group(1)
    seed_tree = ast.parse(target.read_text())
    expected_order = next(ast.literal_eval(node.value) for node in seed_tree.body
                          if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'OUTPUT_ORDER' for t in node.targets))
    assert tuple(actual_order.split(', ')) == expected_order, actual_order
    hashes = {str(path.relative_to(ROOT)): digest(path) for path in sources+[DENSITY,KERNEL,HERE/'supplied_profile_plasma_impl.py']}
    hashes['reactivity_function_ast_sha256'] = hashlib.sha256(ast.dump(kernel_node).encode()).hexdigest()
    (EVIDENCE/'reuse-identity.json').write_text(json.dumps(hashes, indent=2)+'\n')
    return hashes, kernel_source


def verify(hashes, kernel_source):
    import yaml
    from simkit.core.pipeline import execute_pipeline
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module, fingerprint = ProvisionalPackageLoader(package_dir=PACKAGE,
        package_name='aries_plasma_tea', link_root=HERE/'links').load()
    from aries_plasma_tea.handwritten.supplied_profile_plasma.supplied_profile_plasma_impl import _moments, _relative_changes, KEV_TO_J, FUSION_ENERGY_J
    from aries_plasma_tea.handwritten.supplied_profile_plasma.reused_reactivity import _sigv_dt
    from aries_plasma_tea.modules.supplied_profile_plasma.supplied_profile_plasma import Supplied_Profile_PlasmaInput
    registry = module.create_aries_plasma_tea_registry()
    defaults = json.loads((PACKAGE/'inputs/plasma_integration_params.json').read_text())
    pipeline = yaml.safe_load((PACKAGE/'pipelines/pipeline.yaml').read_text())
    for name, binding in pipeline['modules']['entry_fusion']['inputs'].items():
        schema, relative = binding.split(' ', 1)
        pipeline['modules']['entry_fusion']['inputs'][name] = schema+' '+str((PACKAGE/'pipelines'/relative).resolve())
    rows = []

    def run(name, changes, invalid=False):
        inputs = {**defaults, **{PREFIX+key:value for key,value in changes.items()}}
        folder = HERE/'native_runs'/name
        folder.mkdir(parents=True, exist_ok=True)
        path = folder/'inputs.json'
        path.write_text(json.dumps(inputs))
        pipeline['modules']['entry_fusion']['inputs']['plasma_integration_params'] = 'PlasmaIntegrationParams '+str(path)
        spec = folder/'pipeline.yaml'
        spec.write_text(yaml.safe_dump(pipeline, sort_keys=False))
        try:
            result = execute_pipeline(spec, folder/'outputs', registry=registry,
                                      custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        except Exception as error:
            if not invalid:
                raise
            message = str(error)
            assert any(s in message.lower() for s in ['profile integration', 'density profile', 'finite', 'nan', 'infinity']), message
            rows.append({'test':name,'status':'refused','inputs':inputs,'error':message})
            return None
        assert not invalid, name
        outputs = {key[len(PREFIX):]:getattr(value,'root',value) for key,value in result.outputs.items()}
        assert json.loads(path.read_text()) == inputs
        rows.append({'test':name,'status':'passed','inputs':inputs,'outputs':outputs})
        return outputs

    def get(outputs, name):
        return outputs['integration__'+name]

    def close(actual, expected, tolerance=2e-7):
        assert math.isclose(actual,expected,rel_tol=tolerance,abs_tol=1e-12),(actual,expected)

    base = run('conditioned_source_shape', {})
    # Independent polynomial antiderivative, not the quadrature implementation.
    polynomial = {0:.694,2:.306,12:-.594,14:-.306}
    density_factor = sum(2*c/(power+2) for power,c in polynomial.items())
    density_temperature_factor = sum(2*c*(11.83/(power+2)-11.63/(power+4)) for power,c in polynomial.items())
    expected_density = 5e20*density_factor
    expected_pressure = (2-.0335)*5e20*density_temperature_factor*KEV_TO_J
    close(get(base,'density_mean'),expected_density)
    close(get(base,'thermal_pressure'),expected_pressure)
    close(get(base,'stored_thermal_MJ'),1.5*expected_pressure*444*1e-6)
    close(base['beta_calculation__beta'],2*1.25663706212e-6*expected_pressure/5.7**2)
    scaled = run('amplitude_double',{'amplitude':1e21})
    for name in ['density_mean','thermal_pressure','stored_thermal_MJ']:
        close(get(scaled,name),2*get(base,name),1e-12)
    close(get(scaled,'fusion_power_MW'),4*get(base,'fusion_power_MW'),1e-12)
    volume = run('volume_double',{'volume':888.0})
    for name in ['fusion_power_MW','stored_thermal_MJ']:
        close(get(volume,name),2*get(base,name),1e-12)
    close(get(volume,'thermal_pressure'),get(base,'thermal_pressure'),1e-12)
    field = run('field_double',{'field':11.4})
    close(field['beta_calculation__beta'],base['beta_calculation__beta']/4,1e-12)
    close(get(field,'fusion_power_MW'),get(base,'fusion_power_MW'),1e-12)
    d20 = run('deuterium_20pct',{'deuterium_fraction':.2})
    d80 = run('deuterium_80pct',{'deuterium_fraction':.8})
    close(get(d20,'fusion_power_MW'),get(d80,'fusion_power_MW'),1e-12)
    close(get(d20,'fusion_power_MW'),.64*get(base,'fusion_power_MW'),1e-12)
    for name,changes in [('pure_deuterium',{'deuterium_fraction':1.0}),
                         ('pure_tritium',{'deuterium_fraction':0.0}),
                         ('helium_only',{'helium_fraction':.5})]:
        output=run(name,changes)
        assert get(output,'fusion_power_MW') == 0 and get(output,'thermal_pressure') > 0
    flat = run('constant_density_temperature',{'edge_ratio':1.0,'temperature_axis':10.0,'temperature_edge':10.0})
    close(get(flat,'density_mean'),5e20,1e-12)
    close(get(flat,'fusion_power_MW'),444*.25*(.933*5e20)**2*_sigv_dt(10)*FUSION_ENERGY_J*1e-6,1e-12)
    fractional = run('fractional_endpoint_shapes',{'temperature_profile_exponent':.5,'volume_exponent':1.5})
    assert get(fractional,'quadrature_relative_change') <= 1e-6
    run('alternative_measure',{'volume_exponent':3.0})
    run('kernel_low_boundary',{'temperature_axis':.2,'temperature_edge':.2})
    run('kernel_high_boundary',{'temperature_axis':100.0,'temperature_edge':100.0})
    invalids=[('temperature_edge',.023),('temperature_axis',101),('temperature_edge',12),
              ('temperature_profile_exponent',0),('temperature_radial_exponent',0),
              ('helium_fraction',.51),('helium_fraction',-.1),('deuterium_fraction',1.1),
              ('volume',0),('field',0),('field',-1),('volume_exponent',.9),('volume_exponent',4.1),
              ('amplitude',0),('edge_ratio',1.1),('density_radial_exponent',0),('hollowness',-1)]
    for key,value in invalids:
        run(f'invalid_{key}_{value}',{key:value},True)
    for key in ['amplitude','temperature_axis','temperature_edge','helium_fraction','volume','field','volume_exponent']:
        run('nonfinite_'+key,{key:float('inf')},True)
    run('unresolved_boundary_layer',{'density_profile_exponent':1e-10,'temperature_edge':1.0},True)
    # Preserve old kernel function byte semantics; compare representative in-domain values exactly.
    original_namespace={'math':math}
    exec(kernel_source,original_namespace)
    kernel_checks=[{'temperature':t,'old':original_namespace['_sigv_dt'](t),'new':_sigv_dt(t)}
                   for t in [.2,.5,1,5,11.83,25,100]]
    assert all(row['old']==row['new'] for row in kernel_checks)
    kwargs={key[len(PREFIX):]:value for key,value in defaults.items()}
    contract=Supplied_Profile_PlasmaInput(amplitude_in=kwargs['amplitude'],
        edge_density_in=kwargs['amplitude']*kwargs['edge_ratio'],
        density_radial_exponent_in=kwargs['density_radial_exponent'],
        density_profile_exponent_in=kwargs['density_profile_exponent'],hollowness_in=kwargs['hollowness'],
        temperature_axis_in=kwargs['temperature_axis'],temperature_edge_in=kwargs['temperature_edge'],
        temperature_radial_exponent_in=kwargs['temperature_radial_exponent'],
        temperature_profile_exponent_in=kwargs['temperature_profile_exponent'],
        helium_fraction_in=kwargs['helium_fraction'],deuterium_fraction_in=kwargs['deuterium_fraction'],
        volume_in=kwargs['volume'],volume_exponent_in=kwargs['volume_exponent'],field_in=kwargs['field'])
    moments={n:_moments(contract,n) for n in [2048,4096,8192]}
    assert max(_relative_changes(moments[4096],moments[8192])) < 1e-6
    report={'claim':'Conditioned supplied-profile forward evaluation; not ARIES reference prediction',
            'fingerprint':str(fingerprint),'hashes':hashes,'baseline':base,
            'passed':sum(row['status']=='passed' for row in rows),
            'refused':sum(row['status']=='refused' for row in rows),
            'kernel_checks':kernel_checks,'convergence_moments':moments,'checks':rows}
    def safe(value):
        if isinstance(value,float) and not math.isfinite(value):return str(value)
        if isinstance(value,dict):return {key:safe(v) for key,v in value.items()}
        if isinstance(value,(list,tuple)):return [safe(v) for v in value]
        return value
    (EVIDENCE/'verification.json').write_text(json.dumps(safe(report),indent=2,allow_nan=False)+'\n')
    print(json.dumps({key:report[key] for key in ['claim','fingerprint','passed','refused','baseline']},indent=2))


if __name__=='__main__':
    verify(*build())
