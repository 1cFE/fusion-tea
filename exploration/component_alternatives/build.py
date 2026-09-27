"""Build the additive WI-096 component-alternatives native package.

Stage the 14 declared model sources, install reviewed reused bodies and the five
approved additions, preserve them through regeneration, prove a fixed point and
record source, package, snapshot and interface hashes. Original packages remain
unchanged. Build: .codex-test/run python exploration/component_alternatives/build.py
"""
import ast
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'component_alternatives_tea'
EVIDENCE = ROOT / 'work/active/WI-096_matched-conversion-subsystems/numerical-repair/build'
LIBRARY = [
 'models/library/analyses/mfe_primary_loop.sysml', 'models/library/analyses/mfe_viability.sysml',
 'models/library/analyses/integrated_heat_electricity.sysml', 'models/library/analyses/ideal_gas_brayton_components.sysml',
 'models/library/analyses/integrated_equipment_costs.sysml', 'models/library/structure/integrated_equipment_parts.sysml',
 'models/library/foundation/costed_component.sysml', 'models/library/analyses/mfe_account_costs.sysml',
 'models/library/analyses/mfe_lcoe_dcf.sysml', 'models/library/analyses/loop_return_control.sysml',
 'models/library/analyses/mfe_matched_steam_cycle.sysml', 'models/library/analyses/cooling_equipment_selected_pumps.sysml',
 'models/library/analyses/component_alternatives_thermal.sysml',
]
DESIGNS = ['models/designs/component_alternatives/plant.sysml']
SOURCES = [ROOT / p for p in LIBRARY + DESIGNS]
STELLARIS = ROOT / 'exploration/stellarator_e2e/generated/handwritten'
ARIES = ROOT / 'exploration/aries_integrated/aries_integrated/handwritten'
# Reviewed handwritten bodies to reuse (AUTO_IMPLEMENTED = False in their source packages): (root, relative path, import prefix).
# financial_factors.py is the reviewed Stellaris helper the levelized-cost and LCOE bodies import (the ARIES package carries the same copy).
BODIES = [
 (STELLARIS, 'mfe_primary_loop/primary_coolant_loop_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_viability/offered_capacity_screen_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_viability/steam_offered_conditions_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_viability/pump_pressure_rise_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_matched_steam_cycle/matched_steam_cycle_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_matched_steam_cycle/cooling_water_rejection_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_account_costs/financial_factors.py','stellarator_tea'),
 (STELLARIS, 'mfe_account_costs/supplied_purchase_cost_impl.py','stellarator_tea'),
 (STELLARIS, 'mfe_lcoe_dcf/lcoe_dcf_impl.py','stellarator_tea'),
 (ARIES, 'integrated_heat_electricity/common.py','aries_integrated'),
 (HERE/'bodies', 'integrated_heat_electricity/network_heat_driven_closure_impl.py','aries_integrated'),
 (ARIES, 'integrated_heat_electricity/passive_recuperator_impl.py','aries_integrated'),
 (ARIES, 'integrated_heat_electricity/plant_electrical_balance_impl.py','aries_integrated'),
 (ARIES, 'ideal_gas_brayton_components/ideal_gas_compressor_impl.py','aries_integrated'),
 (ARIES, 'ideal_gas_brayton_components/ideal_gas_expander_impl.py','aries_integrated'),
 (ARIES, 'ideal_gas_brayton_components/fixed_outlet_conditioning_impl.py','aries_integrated'),
 (ARIES, 'ideal_gas_brayton_components/fractional_pressure_loss_impl.py','aries_integrated'),
 (ARIES, 'integrated_equipment_costs/common.py','aries_integrated'),
 (ARIES, 'integrated_equipment_costs/exchanger_area_conductance_impl.py','aries_integrated'),
 (ARIES, 'integrated_equipment_costs/selected_inventory_purchase_impl.py','aries_integrated'),
 (ARIES, 'integrated_equipment_costs/eight_amount_sum_impl.py','aries_integrated'),
 (ARIES, 'integrated_equipment_costs/scaled_amount_impl.py','aries_integrated'),
 (HERE/'bodies','loop_return_control/primary_bypass_control_impl.py','costed_loop_brayton_tea'),
 (HERE/'bodies','cooling_equipment_selected_pumps/cooling_equipment_with_selected_salt_pump_count_impl.py','component_alternatives_tea'),
]
NAME = 'component_alternatives_tea'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def run(command, name):
    target=EVIDENCE/name
    if target.exists():
        number=1
        while target.with_name(target.stem+f'.attempt{number}'+target.suffix).exists(): number+=1
        target.rename(target.with_name(target.stem+f'.attempt{number}'+target.suffix))
    with target.open('w') as log:
        subprocess.run([str(ROOT / '.codex-test/run'), 'bash', '-c', 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec "$@"', 'wi096'] + command, check=True, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)


def first_run(tree):
    return next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith('run_')), None)


def copy(source, relative, old_prefix, receipts):
    """The WI-093 reuse rule: prefix rewrite in both forms (import statement and the string-literal module path the shared
    helpers build for importlib), asserted reversible; a typed adapter only where the stock signature reader needs one."""
    target = PACKAGE / 'handwritten' / relative
    forms = [('from ' + old_prefix + '.', 'from ' + NAME + '.'), ("'" + old_prefix + '.', "'" + NAME + '.')]
    content = source.read_text()
    for before, after in forms:
        content = content.replace(before, after)
    reverse = content
    for before, after in forms:
        reverse = reverse.replace(after, before)
    assert reverse == source.read_text(), relative
    if relative == 'mfe_lcoe_dcf/lcoe_dcf_impl.py':
        # Reused DCF helper is called only inside the positive-net ledger branch;
        # its unused definition has no generated input module. Type-only adaptation.
        line=f'from {NAME}.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFInput'
        content=content.replace(line,'from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    '+line)
        content=content.replace('inputs: LCOE_DCFInput','inputs: \'LCOE_DCFInput\'')
    original = first_run(ast.parse(content))
    expected = first_run(ast.parse(target.read_text())) if target.exists() else None
    adapted = False
    if original is not None and expected is not None:
        same_types = (ast.dump(original.args) == ast.dump(expected.args) and original.returns is not None
                      and expected.returns is not None and ast.dump(original.returns) == ast.dump(expected.returns))
        method_ref = any(isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'inputs'
                         and n.attr == 'model_dump' for n in ast.walk(original))
        if not same_types or method_ref:
            reviewed_name = '_reviewed_' + original.name
            content = content.replace('def ' + original.name + '(', 'def ' + reviewed_name + '(', 1)
            module_path = relative.removesuffix('_impl.py').replace('/', '.')
            input_type = ast.unparse(expected.args.args[0].annotation)
            return_type = ast.unparse(expected.returns)
            content += ('\n\nfrom ' + NAME + '.modules.' + module_path + ' import ' + input_type + '\n\n\n'
                        + 'def ' + original.name + '(inputs: ' + input_type + ') -> ' + return_type + ':\n'
                        + '    """Typed native adapter; delegates unchanged reviewed calculation."""\n'
                        + '    return ' + reviewed_name + '(inputs)\n')
            adapted = True
            reviewed = next(n for n in ast.parse(content).body if isinstance(n, ast.FunctionDef) and n.name == reviewed_name)
            assert [ast.dump(n) for n in original.body] == [ast.dump(n) for n in reviewed.body]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    receipts.append(dict(source=str(source.relative_to(ROOT)), target=str(target.relative_to(ROOT)), source_sha256=sha(source),
                         target_sha256=sha(target), prefix_only=not adapted and relative!='mfe_lcoe_dcf/lcoe_dcf_impl.py', typed_adapter=adapted, unbound_helper_type_import_only=relative=='mfe_lcoe_dcf/lcoe_dcf_impl.py', reviewed_body_ast_unchanged=True))


def tree_hashes():
    return {str(p.relative_to(PACKAGE)): sha(p) for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def write_census():
    """The entry-point census through the integration producer's own classification (the ARIES build's pattern)."""
    code = """
import json
import sys
from pathlib import Path
from scripts.integrate import rederived_census
from scripts.study.manifest import read_semantic_fingerprint
package, target = map(Path, sys.argv[1:])
census = rederived_census(package)
census['derived_against_semantic_fingerprint'] = read_semantic_fingerprint(package)
target.write_text(json.dumps(census, indent=2) + '\\n')
print(json.dumps({'entry_points': census['entry_points'], 'semantic_fingerprint': census['derived_against_semantic_fingerprint']}))
"""
    run(['python', '-c', code, str(PACKAGE), str(HERE / 'census.json')], 'census-generation.log')


def build():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    staging = HERE / 'input_models'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    for source in SOURCES:
        shutil.copy2(source, staging / source.name)
    command = ['sysml-codegen', 'generate', '--models', str(staging), '--output', str(PACKAGE), '--package-name', NAME, '--overwrite']
    run(command, 'generation.log')
    receipts = []
    for root, relative, prefix in BODIES:
        copy(root / relative, relative, prefix, receipts)
    for source in (HERE/'bodies/component_alternatives_thermal').glob('*_impl.py'):
        relative=source.relative_to(HERE/'bodies')
        target=PACKAGE/'handwritten'/relative
        stub=first_run(ast.parse(target.read_text()))
        module_path=str(relative).removesuffix('_impl.py').replace('/','.')
        schema_name=relative.name.removesuffix('_impl.py')+'_output'
        schema=ast.parse((PACKAGE/'schemas'/ (schema_name+'.py')).read_text())
        cls=next(n for n in schema.body if isinstance(n,ast.ClassDef))
        order=[n.target.id for n in cls.body if isinstance(n,ast.AnnAssign)]
        input_type=ast.unparse(stub.args.args[0].annotation)
        content=source.read_text()+f"\nfrom {NAME}.modules.{module_path} import {input_type}\n\n"
        content+="def _native_result(inputs):\n"
        content+="    result=calculate({k.removesuffix('_in'):v for k,v in inputs.model_dump().items()})\n"
        content+=f"    return tuple(result[k] for k in {order!r})\n"
        content+=f"\ndef {stub.name}(inputs: {input_type}) -> {ast.unparse(stub.returns)}:\n    return _native_result(inputs)\n"
        target.write_text(content)
        receipts.append(dict(source=str(source.relative_to(ROOT)),target=str(target.relative_to(ROOT)),source_sha256=sha(source),target_sha256=sha(target),new_body=True,typed_adapter=True))
    command += ['--smart-regen', '--preserve-handwritten']
    run(command, 'completion-generation.log')
    before = tree_hashes()
    run(command, 'fixed-point-generation.log')
    after = tree_hashes()
    assert before == after, sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    for receipt in receipts:
        assert sha(ROOT / receipt['target']) == receipt['target_sha256'], receipt['target']
    run(['sysml-codegen', 'snapshot', '--models', str(staging), '--output', str(HERE / 'component_alternatives.snapshot.json')], 'snapshot.log')
    write_census()
    receipt = {'package': str(PACKAGE.relative_to(ROOT)), 'package_name': NAME,
               'sources': {str(p.relative_to(ROOT)): sha(p) for p in SOURCES},
               'staged': {str(p.relative_to(ROOT)): sha(staging / p.name) for p in SOURCES},
               'completions': receipts, 'fixed_point': True, 'package_tree': after,
               'snapshot_sha256': sha(HERE / 'component_alternatives.snapshot.json'), 'census_sha256': sha(HERE / 'census.json')}
    assert receipt['sources'] == receipt['staged']
    (EVIDENCE / 'build-hashes.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'package': receipt['package'], 'sources': len(SOURCES), 'bodies': len(receipts),
                      'adapted': sum(r.get('typed_adapter',False) for r in receipts), 'fixed_point': True, 'snapshot_sha256': receipt['snapshot_sha256']}))


if __name__ == '__main__':
    build()
