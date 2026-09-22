"""Stock native generation, reviewed completion reuse and reproducible snapshot."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'aries_integrated'
EVIDENCE = ROOT / 'work/active/WI-089_aries-integrated-heat-and-electricity/evidence'
SOURCES = [ROOT / path for path in [
    'models/library/analyses/integrated_heat_electricity.sysml',
    'models/library/analyses/radial_density_profile.sysml',
    'models/library/analyses/supplied_profile_plasma.sysml',
    'models/library/analyses/mfe_plasma_scaling.sysml',
    'models/library/analyses/mfe_fuel_cycle.sysml',
    'models/library/analyses/mfe_viability.sysml',
    'models/library/analyses/dual_circuit_heat_accounting.sysml',
    'models/library/analyses/ideal_gas_brayton_components.sysml',
    'models/designs/aries_cs_transfer/plasma_integration.sysml',
    'models/designs/aries_cs_integrated/plant.sysml',
]]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, name):
    with (EVIDENCE / name).open('w') as log:
        subprocess.run([str(ROOT / '.codex-test/run')] + command, check=True, cwd=ROOT,
                       stdout=log, stderr=subprocess.STDOUT)


def build():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    staging = HERE / 'input_models'
    staging.mkdir(exist_ok=True)
    for source in SOURCES:
        shutil.copy2(source, staging / source.name)
    command = ['sysml-codegen','generate','--models',str(staging),'--output',str(PACKAGE),
               '--package-name','aries_integrated','--overwrite']
    run(command, 'generation.log')
    receipts = []
    def copy(source, relative, old_prefix=None):
        target = PACKAGE / 'handwritten' / relative
        content = source.read_text()
        if old_prefix:
            content = content.replace('from '+old_prefix+'.','from aries_integrated.')
        target.write_text(content)
        normalized = content.replace('from aries_integrated.','from '+old_prefix+'.') if old_prefix else content
        assert normalized == source.read_text()
        receipts.append(dict(source=str(source.relative_to(ROOT)),target=str(target.relative_to(ROOT)),
                             source_sha256=sha(source),target_sha256=sha(target),prefix_only=bool(old_prefix)))
    reused = [
        ('exploration/aries_transfer/plasma_integration/supplied_profile_plasma_impl.py','supplied_profile_plasma/supplied_profile_plasma_impl.py','aries_plasma_tea'),
        ('exploration/aries_transfer/density_profile/radial_density_profile_impl.py','radial_density_profile/radial_density_profile_impl.py','aries_density_tea'),
        ('exploration/stellarator_e2e/generated/handwritten/mfe_viability/offered_capacity_screen_impl.py','mfe_viability/offered_capacity_screen_impl.py','stellarator_tea'),
    ]
    for source,target,prefix in reused:
        copy(ROOT/source,target,prefix)
    for name in ['ideal_gas_compressor','ideal_gas_expander','fixed_outlet_conditioning','fractional_pressure_loss']:
        copy(ROOT/('exploration/aries_transfer/nominal_brayton/native_completions/'+name+'_impl.py'),
             'ideal_gas_brayton_components/'+name+'_impl.py','brayton_tea')
    for source in (ROOT/'exploration/aries_transfer/dual_blanket_heat/native_completions').glob('*.py'):
        copy(source,'dual_circuit_heat_accounting/'+source.name,'dual_heat_tea')
    for source in (HERE/'native_completions').glob('*.py'):
        copy(source,'integrated_heat_electricity/'+source.name)
    kernel = ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py'
    node = next(n for n in ast.parse(kernel.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='_sigv_dt')
    (PACKAGE/'handwritten/supplied_profile_plasma/reused_reactivity.py').write_text(
        '"""Unchanged accepted kernel; integration guards its domain."""\nimport math\n\n'+ast.get_source_segment(kernel.read_text(),node)+'\n')
    run(command+['--preserve-handwritten'], 'completion-generation.log')
    before = {str(p.relative_to(PACKAGE)):sha(p) for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    run(command+['--preserve-handwritten'], 'fixed-point-generation.log')
    after = {str(p.relative_to(PACKAGE)):sha(p) for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert before == after, sorted(key for key in set(before)|set(after) if before.get(key)!=after.get(key))
    run(['sysml-codegen','snapshot','--models',str(staging),'--output',str(HERE/'integrated.snapshot.json')], 'snapshot.log')
    receipt = dict(sources={str(p.relative_to(ROOT)):sha(p) for p in SOURCES},
                   staged={str(p.relative_to(ROOT)):sha(staging/p.name) for p in SOURCES},
                   completions=receipts,fixed_point=True,reactivity_ast_sha256=hashlib.sha256(ast.dump(node).encode()).hexdigest())
    assert receipt['sources']==receipt['staged']
    (EVIDENCE/'build-hashes.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'package':str(PACKAGE.relative_to(ROOT)),'source_count':len(SOURCES),'fixed_point':True}))


if __name__ == '__main__':
    build()
