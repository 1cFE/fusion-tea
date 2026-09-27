"""Generate the isolated WI-097 package using the existing stock build machinery.

Run with .codex-test/run python exploration/exchanger_architecture/thermal_requirements/build.py.
Historical packages and the independently owned studies directory are read-only here.
"""
import ast
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
NAME = 'exchanger_architecture_thermal_tea'
PACKAGE = HERE / NAME
EVIDENCE = ROOT / 'work/active/WI-097_exchanger-thermal-requirements/evidence'
SOURCES = [ROOT / p for p in (
    'models/library/analyses/integrated_lifecycle_costs.sysml',
    'models/library/analyses/mfe_lcoe_dcf.sysml',
    'models/library/analyses/integrated_heat_electricity.sysml',
    'models/library/analyses/integrated_equipment_costs.sysml',
    'models/library/structure/integrated_equipment_parts.sysml',
    'models/library/foundation/costed_component.sysml',
    'models/library/analyses/mfe_account_costs.sysml',
    'models/library/analyses/source_budget_accounting.sysml',
    'models/library/analyses/radial_density_profile.sysml',
    'models/library/analyses/supplied_profile_plasma.sysml',
    'models/library/analyses/mfe_plasma_scaling.sysml',
    'models/library/analyses/mfe_fuel_cycle.sysml',
    'models/library/analyses/mfe_viability.sysml',
    'models/library/analyses/dual_circuit_heat_accounting.sysml',
    'models/library/analyses/ideal_gas_brayton_components.sysml',
    'models/designs/aries_cs_transfer/plasma_integration.sysml',
)] + [HERE/'models/library/controlled_exchanger_closure.sysml', HERE/'models/designs/plant.sysml']


def helper_module():
    path = ROOT/'exploration/costed_loop_brayton/build.py'
    spec = importlib.util.spec_from_file_location('wi097_build_helper', path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    helper.ROOT, helper.HERE = ROOT, HERE
    helper.PACKAGE, helper.NAME, helper.EVIDENCE = PACKAGE, NAME, EVIDENCE
    return helper


def build():
    h = helper_module()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    staging = HERE/'input_models'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    for source in SOURCES:
        shutil.copy2(source, staging/source.name)
    command = ['sysml-codegen','generate','--models',str(staging),'--output',str(PACKAGE),'--package-name',NAME,'--overwrite']
    h.run(command, 'generation.log')
    receipts = []
    original = ROOT/'exploration/aries_integrated/aries_integrated/handwritten'
    for source in sorted(original.rglob('*.py')):
        if source.name in ('__init__.py', 'network_heat_driven_closure_impl.py'):
            continue
        content = source.read_text()
        if 'AUTO_IMPLEMENTED = False' in content or 'AUTO_IMPLEMENTED' not in content:
            h.copy(source, str(source.relative_to(original)), 'aries_integrated', receipts)
    for source in sorted((HERE/'bodies/controlled_exchanger_closure').glob('*.py')):
        h.copy(source, 'controlled_exchanger_closure/'+source.name, NAME, receipts)
    legacy_source = ROOT/'exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py'
    legacy_copy = HERE/'bodies/controlled_exchanger_closure/legacy_network.py'
    functions = lambda p: [ast.dump(n) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)]
    assert functions(legacy_source) == functions(legacy_copy), 'legacy arithmetic changed'
    command += ['--smart-regen','--preserve-handwritten']
    h.run(command, 'generation-completions.log')
    before = h.tree_hashes()
    h.run(command, 'generation-fixed-point.log')
    after = h.tree_hashes()
    assert before == after, sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k))
    for receipt in receipts:
        assert h.sha(ROOT/receipt['target']) == receipt['target_sha256'], receipt['target']
    snapshot = HERE/'thermal_requirements.snapshot.json'
    h.run(['sysml-codegen','snapshot','--models',str(staging),'--output',str(snapshot)], 'build-snapshot.log')
    h.write_census()
    # Rename the inherited helper's log into this task's owned evidence namespace.
    (EVIDENCE/'census-generation.log').replace(EVIDENCE/'build-census.log')
    result = {'package':str(PACKAGE.relative_to(ROOT)), 'package_name':NAME,
              'build_helper_sha256':h.sha(ROOT/'exploration/costed_loop_brayton/build.py'),
              'legacy_source_sha256':h.sha(legacy_source), 'legacy_function_ast_unchanged':True,
              'sources':{str(p.relative_to(ROOT)):h.sha(p) for p in SOURCES},
              'staged':{str(p.relative_to(ROOT)):h.sha(staging/p.name) for p in SOURCES},
              'completions':receipts,'fixed_point':True,'package_tree':after,
              'snapshot_sha256':h.sha(snapshot),'census_sha256':h.sha(HERE/'census.json')}
    assert result['sources'] == result['staged']
    (EVIDENCE/'build-hashes.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('package','fixed_point','snapshot_sha256','census_sha256')}))


if __name__ == '__main__':
    build()
