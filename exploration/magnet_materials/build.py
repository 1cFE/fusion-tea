"""Build the isolated WI-099 magnet conductor alternatives package `magnet_materials_tea`.

Stage exactly the two declared SysML sources (the new library and the new design; no other library
imports except ScalarValues), check that every calc and constraint usage binds its parameters in the
definition's order (usage parameters redefine definition parameters by position), generate with
sysml-codegen, install the handwritten bodies with typed adapters, regenerate with the handwritten files
preserved, prove a fixed point, and write the snapshot, the entry-point census and the build-hash receipt.
Build evidence goes under work/active/WI-099_magnet-conductor-alternatives/build/. Nothing existing is
modified. Build: .codex-test/run python exploration/magnet_materials/build.py
"""
import ast
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
NAME = 'magnet_materials_tea'
PACKAGE = HERE / NAME
BODIES = HERE / 'bodies'
LIBRARY_PACKAGE = 'magnet_conductor_alternatives'
EVIDENCE = ROOT / 'work/active/WI-099_magnet-conductor-alternatives/build'
LIBRARY = ['models/library/analyses/magnet_conductor_alternatives.sysml']
DESIGNS = ['models/designs/magnet_materials/magnet_subsystem.sysml']
SOURCES = [ROOT / p for p in LIBRARY + DESIGNS]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def run(command, name):
    """Run a toolchain command through the sealed environment, logging to the evidence directory."""
    target = EVIDENCE / name
    if target.exists():
        number = 1
        while target.with_name(target.stem + f'.attempt{number}' + target.suffix).exists():
            number += 1
        target.rename(target.with_name(target.stem + f'.attempt{number}' + target.suffix))
    with target.open('w') as log:
        subprocess.run([str(ROOT / '.codex-test/run'), 'bash', '-c',
                        'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec "$@"', 'wi099'] + command,
                       check=True, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)


def definition_parameters(text):
    """Map each calc/constraint definition name to its ordered `in attribute` parameter names."""
    result = {}
    for match in re.finditer(r"(?:calc|constraint) def '([^']+)' \{(.*?)\n    \}", text, re.S):
        result[match.group(1)] = re.findall(r'^\s*in attribute (\w+)\s*:', match.group(2), re.M)
    return result


def check_positional_bindings():
    """Every usage binds a prefix of its definition's parameters, in order, by the same names.

    SysML usage parameters redefine the definition's parameters by position; a reordered binding
    list would silently wire a value to a different formal. Unbound trailing formals keep their
    library default and become calc-usage entry keys."""
    definitions = definition_parameters((ROOT / LIBRARY[0]).read_text())
    design = (ROOT / DESIGNS[0]).read_text()
    usages = re.findall(r"(?:calc|assert constraint) (\w+) : '([^']+)' \{\n(.*?)\n\s*\}", design, re.S)
    report = []
    for usage, definition, body in usages:
        bound = re.findall(r'^\s*in (\w+) = ', body, re.M)
        formals = definitions[definition]
        if bound != formals[:len(bound)]:
            raise AssertionError(f'{usage}: bindings {bound} are not the ordered prefix of {definition} {formals}')
        report.append(dict(usage=usage, definition=definition, bound=len(bound), unbound=formals[len(bound):]))
    if len(usages) != 23:  # 2 materials x (6 calcs + 5 constraints) + the pair comparison
        raise AssertionError(f'expected 23 usages, found {len(usages)}')
    return report


def first_run(tree):
    return next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith('run_')), None)


def install_bodies(receipts):
    """Append a typed native adapter to each reviewed body; the calculate function is unchanged."""
    sources = sorted((BODIES / LIBRARY_PACKAGE).glob('*_impl.py'))
    stubs = sorted((PACKAGE / 'handwritten' / LIBRARY_PACKAGE).glob('*_impl.py'))
    if [p.name for p in sources] != [p.name for p in stubs]:
        raise AssertionError(f'bodies {[p.name for p in sources]} differ from generated stubs {[p.name for p in stubs]}')
    for source in sources:
        relative = source.relative_to(BODIES)
        target = PACKAGE / 'handwritten' / relative
        stub = first_run(ast.parse(target.read_text()))
        module_path = str(relative).removesuffix('_impl.py').replace('/', '.')
        schema = ast.parse((PACKAGE / 'schemas' / (relative.name.removesuffix('_impl.py') + '_output.py')).read_text())
        cls = next(n for n in schema.body if isinstance(n, ast.ClassDef))
        order = [n.target.id for n in cls.body if isinstance(n, ast.AnnAssign)]
        body = source.read_text()
        declared = ast.literal_eval(next(n.value for n in ast.parse(body).body
                                         if isinstance(n, ast.Assign) and n.targets[0].id == 'OUTPUTS'))
        if sorted(declared) != sorted(order):
            raise AssertionError(f'{relative}: body OUTPUTS {declared} differ from generated schema {order}')
        input_type = ast.unparse(stub.args.args[0].annotation)
        content = body + f'\n\nfrom {NAME}.modules.{module_path} import {input_type}\n\n\n'
        content += 'def _native_result(inputs):\n'
        content += '    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""\n'
        content += "    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})\n"
        content += f'    return tuple(result[k] for k in {order!r})\n'
        content += f'\n\ndef {stub.name}(inputs: {input_type}) -> {ast.unparse(stub.returns)}:\n    return _native_result(inputs)\n'
        target.write_text(content)
        receipts.append(dict(source=str(source.relative_to(ROOT)), target=str(target.relative_to(ROOT)), source_sha256=sha(source),
                             target_sha256=sha(target), new_body=True, typed_adapter=True, schema_order=order))


def tree_hashes():
    return {str(p.relative_to(PACKAGE)): sha(p) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def write_census():
    """The entry-point census through the integration producer's own classification (component-alternatives pattern)."""
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
    bindings = check_positional_bindings()
    staging = HERE / 'input_models'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    for source in SOURCES:
        shutil.copy2(source, staging / source.name)
    command = ['sysml-codegen', 'generate', '--models', str(staging), '--output', str(PACKAGE), '--package-name', NAME, '--overwrite']
    run(command, 'generation.log')
    receipts = []
    install_bodies(receipts)
    command += ['--smart-regen', '--preserve-handwritten']
    run(command, 'completion-generation.log')
    for receipt in receipts:
        assert sha(ROOT / receipt['target']) == receipt['target_sha256'], f"regeneration changed {receipt['target']}"
    before = tree_hashes()
    run(command, 'fixed-point-generation.log')
    after = tree_hashes()
    assert before == after, sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    for receipt in receipts:
        assert sha(ROOT / receipt['target']) == receipt['target_sha256'], receipt['target']
    run(['sysml-codegen', 'snapshot', '--models', str(staging), '--output', str(HERE / 'magnet_materials.snapshot.json')], 'snapshot.log')
    write_census()
    receipt = {'package': str(PACKAGE.relative_to(ROOT)), 'package_name': NAME,
               'sources': {str(p.relative_to(ROOT)): sha(p) for p in SOURCES},
               'staged': {str(p.relative_to(ROOT)): sha(staging / p.name) for p in SOURCES},
               'positional_bindings': bindings, 'completions': receipts, 'fixed_point': True, 'package_tree': after,
               'snapshot_sha256': sha(HERE / 'magnet_materials.snapshot.json'), 'census_sha256': sha(HERE / 'census.json')}
    assert receipt['sources'] == receipt['staged']
    (EVIDENCE / 'build-hashes.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'package': receipt['package'], 'sources': len(SOURCES), 'bodies': len(receipts), 'usages_checked': len(bindings),
                      'fixed_point': True, 'files': len(after), 'snapshot_sha256': receipt['snapshot_sha256']}))


if __name__ == '__main__':
    build()
