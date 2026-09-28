"""Generate WI-081 in isolation, then verify its real TEAx execution contract."""
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-081_aries-hollow-finite-edge-density-profile/evidence'
PACKAGE = HERE / 'generated'
PREFIX = 'aries_cs_density_profile__plasma_profile__'


def generate():
    import syside
    staged = HERE / 'staged_models'
    staged.mkdir(exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    sources = [ROOT / 'models/library/analyses/radial_density_profile.sysml',
               ROOT / 'models/designs/aries_cs_transfer/density_profile.sysml']
    _, diagnostics = syside.try_load_model([str(path) for path in sources])
    errors = [str(item) for category in ('parser', 'sema')
              for item in getattr(diagnostics, category)
              if item.severity == syside.DiagnosticSeverity.Error]
    (EVIDENCE / 'parse-api.json').write_text(json.dumps({'errors': errors}, indent=2)+'\n')
    assert not errors, errors
    for source in sources:
        shutil.copy2(source, staged / source.name)
    command = [str(ROOT / '.codex-test/run'), 'sysml-codegen', 'generate',
               '--models', str(staged), '--output', str(PACKAGE),
               '--package-name', 'aries_density_tea', '--overwrite']
    with (EVIDENCE / 'generation.log').open('w') as log:
        subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    target = PACKAGE / 'handwritten/radial_density_profile/radial_density_profile_impl.py'
    shutil.copy2(HERE / 'radial_density_profile_impl.py', target)
    with (EVIDENCE / 'generation-completed.log').open('w') as log:
        subprocess.run(command + ['--preserve-handwritten'], cwd=ROOT,
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    assert target.read_bytes() == (HERE / 'radial_density_profile_impl.py').read_bytes()
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sources + [HERE / 'radial_density_profile_impl.py']}


def verify(hashes):
    import yaml
    from simkit.core.pipeline import execute_pipeline
    from simkit.evaluation.package_load import ProvisionalPackageLoader

    module, fingerprint = ProvisionalPackageLoader(
        package_dir=PACKAGE, package_name='aries_density_tea', link_root=HERE / 'links'
    ).load()
    registry = module.create_aries_density_tea_registry()
    defaults = json.loads((PACKAGE / 'inputs/density_profile_params.json').read_text())
    pipeline = yaml.safe_load((PACKAGE / 'pipelines/pipeline.yaml').read_text())
    rows = []

    def run(name, changes, expected=None, invalid=False):
        inputs = {**defaults, **{PREFIX + key: value for key, value in changes.items()}}
        directory = HERE / 'native_runs' / name
        directory.mkdir(parents=True, exist_ok=True)
        input_path = directory / 'inputs.json'
        input_path.write_text(json.dumps(inputs))
        pipeline['modules']['entry_fusion']['inputs']['density_profile_params'] = (
            'DensityProfileParams ' + str(input_path)
        )
        spec = directory / 'pipeline.yaml'
        spec.write_text(yaml.safe_dump(pipeline, sort_keys=False))
        try:
            result = execute_pipeline(spec, directory / 'outputs', registry=registry,
                                      custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        except Exception as error:
            if not invalid:
                raise
            message = str(error)
            assert ('density profile' in message or 'finite' in message.lower()
                    or 'nan' in message.lower() or 'infinity' in message.lower()), message
            rows.append({'test': name, 'status': 'refused', 'error': message,
                         'chosen_inputs': inputs})
            return
        assert not invalid, f'{name}: unsupported case returned success'
        density = result.outputs[PREFIX + 'profile__density'].root
        edge = result.outputs[PREFIX + 'edge_density__edge_density'].root
        assert math.isclose(density, expected, rel_tol=2e-14, abs_tol=1e-15), (name, density, expected)
        assert edge == inputs[PREFIX + 'amplitude'] * inputs[PREFIX + 'edge_ratio']
        assert json.loads(input_path.read_text()) == inputs
        rows.append({'test': name, 'status': 'passed', 'density': density,
                     'expected': expected, 'edge_density': edge, 'chosen_inputs': inputs})

    # Expanded reference polynomial: structurally independent of the implementation.
    for rho in [0.0, 0.25, 0.5, 0.75, 1.0]:
        expected = 0.694 + 0.306*rho**2 - 0.594*rho**12 - 0.306*rho**14
        run(f'reference_{rho}', {'rho': rho}, expected)
    midpoint = 0.694 + 0.306/4 - 0.594/4096 - 0.306/16384
    run('amplitude_scaled', {'amplitude': 7.0}, 7*midpoint)
    run('physical_unit_conversion_demo', {'amplitude': 1e20}, 1e20*midpoint)
    run('edge_changed_center', {'rho': 0.0, 'edge_ratio': 0.4}, 0.6*0.66+0.4)
    run('constant_edge_equals_amplitude', {'edge_ratio': 1.0}, 1.0)
    run('nonhollow', {'hollowness': 1.0}, 0.9*(1-1/4096)+0.1)
    run('hollow_zero_center', {'rho': 0.0, 'hollowness': 0.0, 'edge_ratio': 0.0}, 0.0)
    run('different_exponents', {'radial_exponent': 2.0, 'profile_exponent': 2.0,
                              'hollowness': 0.5, 'edge_ratio': 0.2}, 0.8*(9/16)*(5/8)+0.2)
    run('largest_finite_constant', {'amplitude': sys.float_info.max, 'edge_ratio': 1.0}, sys.float_info.max)
    for key, value in [('amplitude', 0), ('amplitude', -1), ('edge_ratio', -0.1),
                       ('edge_ratio', 1.1), ('rho', -0.1), ('rho', 1.1),
                       ('radial_exponent', 0), ('radial_exponent', -1),
                       ('profile_exponent', 0), ('profile_exponent', -1),
                       ('hollowness', -0.1), ('hollowness', 1.1)]:
        run(f'invalid_{key}_{value}', {key: value}, invalid=True)
    for key in ['amplitude', 'edge_ratio', 'rho', 'radial_exponent', 'profile_exponent', 'hollowness']:
        for label, value in [('nan', float('nan')), ('inf', float('inf'))]:
            run(f'invalid_{key}_{label}', {key: value}, invalid=True)
    run('edge_binding_overflow', {'amplitude': sys.float_info.max, 'edge_ratio': 2.0}, invalid=True)
    report = {'claim': 'Local density equation and supplied-parameter native transfer only',
              'fingerprint': str(fingerprint), 'source_hashes': hashes,
              'passed': sum(row['status'] == 'passed' for row in rows),
              'refused': sum(row['status'] == 'refused' for row in rows), 'checks': rows}
    def json_safe(value):
        if isinstance(value, float) and not math.isfinite(value):
            return str(value)
        if isinstance(value, dict):
            return {key: json_safe(item) for key, item in value.items()}
        if isinstance(value, list):
            return [json_safe(item) for item in value]
        return value
    (EVIDENCE / 'verification.json').write_text(json.dumps(json_safe(report), indent=2, allow_nan=False)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'checks'}, indent=2))


if __name__ == '__main__':
    verify(generate())
