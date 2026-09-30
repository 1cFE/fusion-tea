"""Build the isolated WI-100 plant-level conductor material packages (design section 1.6, option Y).

Three generation units from one staged source set (probe P2 fallback, design K21: codegen refuses any package with two
or more instances of 'MFE Power Plant', REGISTRY_CLASS_NAME_COLLISION; work/active/WI-100_stellarator-material-variants/
prototype/P2-double-retype.md):

  reference  stellarator_materials_reference_tea  the 42 stellarator_e2e twin files with the 15 seam hunks; the
                                                   Stellaris design file byte-identical (the regression witness)
  rebco      stellarator_materials_rebco_tea      the same staged files without the Stellaris design file, plus Round 1's
                                                   library, the variants library and rebco_material.sysml
  nb3sn      stellarator_materials_nb3sn_tea      the same, with nb3sn_material.sysml

Steps (design section 1.6): 1 hash the protected trees and assert twin == canonical for the 42 MFE files; 2 stage each
unit in twin layout under units/<unit>/input_models/, apply seams/seam_hunks.json (each old string exactly once; the
reversed set reproduces the source bytes), refuse if author_materials_design.py drifts from the committed design files;
3 check positional bindings of every usage of a hunked or new definition, and require the unbound trailing formals to
be exactly the two named calc-usage keys; 4 generate, install bodies (the 51 prefix-rewritten stellarator_e2e manual
bodies with their helper, bodies B1 and B2 with whole-body diff receipts, Round 1's bodies with the WI-099 typed adapter,
the REBCO shape-branch fallback body), assert the installed set against the emitted manual-stub set, regenerate with
the handwritten files preserved, prove a fixed point, write the snapshot, the census and the build-hash receipt;
5 is two separate commands, run after this build with the sealed teax runtime on the path: studies/prepare_interface.py
(interface and manifests), then regression.py (the reference parity, the baseline points and the preservation receipt).

Evidence goes under work/active/WI-100_stellarator-material-variants/build/. Nothing existing is modified.
Build: .codex-test/run python exploration/stellarator_materials/build.py
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-100_stellarator-material-variants/build'
TWIN = ROOT / 'exploration/stellarator_e2e/models'
E2E_BODIES = ROOT / 'exploration/stellarator_e2e/generated/handwritten'
ROUND1_BODIES = ROOT / 'exploration/magnet_materials/bodies/magnet_conductor_alternatives'
HUNKS = HERE / 'seams/seam_hunks.json'
STELLARIS = 'designs/stellarator_09/stellarator_plant.sysml'
ROUND1_LIBRARY = ROOT / 'models/library/analyses/magnet_conductor_alternatives.sysml'
VARIANTS = HERE / 'models/library/analyses/magnet_material_variants.sysml'
DESIGN_DIR = HERE / 'models/designs/stellarator_09_materials'
UNITS = {
    'reference': dict(package='stellarator_materials_reference_tea', design=None, round1=()),
    'rebco': dict(package='stellarator_materials_rebco_tea', design='rebco_material.sysml',
                  round1=('rebco_cable_critical_surface', 'winding_turn_area_screen', 'winding_inventory_and_cost',
                          'magnet_cold_stage_load', 'staged_refrigeration_screen'), extra=('rebco_shape_branch',)),
    'nb3sn': dict(package='stellarator_materials_nb3sn_tea', design='nb3sn_material.sysml',
                  round1=('nb3sn_cable_critical_surface', 'winding_turn_area_screen', 'winding_inventory_and_cost',
                          'magnet_cold_stage_load', 'staged_refrigeration_screen'), extra=()),
}
PROTECTED = [ROOT / 'models', ROOT / 'exploration/stellarator_e2e', ROOT / 'exploration/magnet_materials',
             ROOT / 'tests/model_families.py']
# stellarator_e2e manual bodies whose stub the derived generation does not emit, installed for bit parity with the pin:
# three calcs codegen could auto-implement but the pinned package completes by hand, and four inert orphans the pinned
# package carries for definitions no usage instantiates (reused as the pinned handwritten tree holds them).
E2E_PRESERVED = {
    'mfe_account_costs/structure_cost_impl.py': 'manual completion preferred over auto-implementation in the pin',
    'mfe_cryo_inventory/cold_load_sum_impl.py': 'manual completion preferred over auto-implementation in the pin',
    'mfe_magnet_cost/magnet_structure_cost_impl.py': 'manual completion preferred over auto-implementation in the pin',
    'mfe_conductor_current/current_driven_pack_sizing_impl.py': 'inert orphan carried by the pinned handwritten tree',
    'mfe_conductor_grade/conductor_field_capability_impl.py': 'inert orphan carried by the pinned handwritten tree',
    'mfe_magnet_cost/magnet_support_mass_impl.py': 'inert orphan carried by the pinned handwritten tree',
    'mfe_magnet_field/winding_pack_sizing_impl.py': 'inert orphan carried by the pinned handwritten tree',
}
MODIFIED = {'mfe_conductor_current/rebco_conductor_current_impl.py': 'B1', 'mfe_plasma_scaling/conductor_peak_field_impl.py': 'B2'}
# Unbound trailing formals of the staged definitions' usages, by (usage, formal). Both material units stage the whole
# variants library, so both list the Nb3Sn conductor's eps_intrinsic_in; only the instantiated variant's keys are emitted
# (checked per unit by studies/prepare_interface.py).
NAMED_UNBOUND = {'rebco': {('conductor', 'eps_intrinsic_in'), ('pack_field', 'mu0_in')},
                 'nb3sn': {('conductor', 'eps_intrinsic_in'), ('pack_field', 'mu0_in')}, 'reference': set()}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def unit_dir(unit):
    return HERE / 'units' / unit


def package_dir(unit):
    return unit_dir(unit) / UNITS[unit]['package']


def run(command, name, check=True):
    """Run a toolchain command through the sealed environment, logging to the evidence directory."""
    target = EVIDENCE / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        number = 1
        while target.with_name(target.stem + f'.attempt{number}' + target.suffix).exists():
            number += 1
        target.rename(target.with_name(target.stem + f'.attempt{number}' + target.suffix))
    with target.open('w') as log:
        done = subprocess.run([str(ROOT / '.codex-test/run'), 'bash', '-c',
                               'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec "$@"', 'wi100'] + command,
                              cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    if check and done.returncode != 0:
        raise SystemExit(f'{" ".join(command[:3])} failed; see {target.relative_to(ROOT)}')
    return done.returncode


def tree_hashes(root: Path) -> dict[str, str]:
    root = Path(root)
    if root.is_file():
        return {str(root.relative_to(ROOT)): sha(root)}
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def protected_hashes():
    out = {}
    for root in PROTECTED:
        out.update(tree_hashes(root))
    return out


def twin_files():
    return sorted(p.relative_to(TWIN).as_posix() for p in TWIN.rglob('*') if p.is_file() and '__pycache__' not in p.parts)


def canonical(logical: str) -> Path:
    return ROOT / 'models' / (logical if logical.startswith('designs/') else 'library/' + logical)


# ---------------------------------------------------------------------------------------------- step 2: staging


def apply_hunks(staging: Path) -> list[dict]:
    doc = json.loads(HUNKS.read_text())
    texts, receipts = {}, []
    for hunk in doc['hunks']:
        path = staging / hunk['file']
        text = texts.get(hunk['file'], path.read_text())
        count = text.count(hunk['old'])
        if count != 1:
            raise SystemExit(f"hunk {hunk['id']}: old text occurs {count} times in {hunk['file']}")
        texts[hunk['file']] = text.replace(hunk['old'], hunk['new'])
        receipts.append(dict(id=hunk['id'], file=hunk['file'], old_sha256=hashlib.sha256(hunk['old'].encode()).hexdigest(),
                             new_sha256=hashlib.sha256(hunk['new'].encode()).hexdigest()))
    for name, text in texts.items():
        source = (TWIN / name).read_text()
        reverse = text
        for hunk in reversed([h for h in doc['hunks'] if h['file'] == name]):
            if reverse.count(hunk['new']) != 1:
                raise SystemExit(f"hunk {hunk['id']}: new text is not unique, the set is not reversible")
            reverse = reverse.replace(hunk['new'], hunk['old'])
        if reverse != source:
            raise SystemExit(f'hunks on {name} are not reversible')
        (staging / name).write_text(text)
    return receipts


def stage(unit: str) -> dict:
    staging = unit_dir(unit) / 'input_models'
    if staging.exists():
        shutil.rmtree(staging)
    files = twin_files()
    spec = UNITS[unit]
    if spec['design']:
        files = [f for f in files if f != STELLARIS]
    for logical in files:
        target = staging / logical
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TWIN / logical, target)
    receipts = apply_hunks(staging)
    added = {}
    if spec['design']:
        for source, logical in ((ROUND1_LIBRARY, 'analyses/magnet_conductor_alternatives.sysml'),
                                (VARIANTS, 'analyses/magnet_material_variants.sysml'),
                                (DESIGN_DIR / spec['design'], 'designs/stellarator_09_materials/' + spec['design'])):
            target = staging / logical
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            added[logical] = dict(source=str(source.relative_to(ROOT)), sha256=sha(source))
    staged = {p.relative_to(staging).as_posix(): sha(p) for p in sorted(staging.rglob('*')) if p.is_file()}
    patched = sorted({h['file'] for h in receipts})
    for logical in files:
        expected = sha(TWIN / logical)
        if logical in patched:
            assert staged[logical] != expected, logical
        elif staged[logical] != expected:
            raise SystemExit(f'staged {logical} differs from the twin')
    return dict(unit=unit, twin_files=len(files), patched=patched, hunks=receipts, added=added, staged=staged)


# ---------------------------------------------------------------------------------------------- step 3: bindings

DEF = re.compile(r"^(\s*)(?:calc|constraint) def '([^']+)' \{")
USAGE = re.compile(r"^\s*(?:calc|assert constraint) (\w+) : '([^']+)' \{")


def definitions(staging: Path) -> dict[str, list[str]]:
    """Every calc/constraint definition's ordered `in attribute` formals across the staged tree."""
    found = {}
    for path in sorted(staging.rglob('*.sysml')):
        lines = path.read_text().split('\n')
        k = 0
        while k < len(lines):
            match = DEF.match(lines[k])
            if match:
                indent, name = match.groups()
                formals, j = [], k + 1
                while not lines[j].startswith(indent + '}'):
                    formal = re.match(r'\s*in attribute (\w+)\s*:', lines[j])
                    if formal:
                        formals.append(formal.group(1))
                    j += 1
                assert name not in found, f'duplicate definition {name}'
                found[name] = formals
                k = j
            k += 1
    return found


def check_positional_bindings(unit: str) -> list[dict]:
    """Every usage of a hunked or new definition binds an ordered prefix of its formals by the same names (usage
    parameters redefine definition parameters by position); unbound trailing formals become calc-usage entry keys and
    must be exactly the design's named keys (review R5)."""
    staging = unit_dir(unit) / 'input_models'
    defs = definitions(staging)
    watched = {'REBCO Conductor Current', 'Conductor Peak Field'}
    variants = staging / 'analyses/magnet_material_variants.sysml'
    if variants.exists():
        watched |= set(definitions_in(variants)) | set(definitions_in(staging / 'analyses/magnet_conductor_alternatives.sysml'))
    report, unbound = [], set()
    for path in sorted(staging.rglob('*.sysml')):
        lines = path.read_text().split('\n')
        for k, line in enumerate(lines):
            match = USAGE.match(line)
            if not match or match.group(2) not in watched:
                continue
            usage, definition = match.groups()
            bound, j = [], k + 1
            depth = 1
            while depth:
                depth += lines[j].count('{') - lines[j].count('}')
                formal = re.match(r'\s*in (\w+) = ', lines[j])
                if formal and depth == 1:
                    bound.append(formal.group(1))
                j += 1
            formals = defs[definition]
            if bound != formals[:len(bound)]:
                raise SystemExit(f'{path.name}:{k + 1} {usage}: bindings {bound} are not the ordered prefix of {definition} {formals}')
            rest = formals[len(bound):]
            report.append(dict(file=path.relative_to(staging).as_posix(), line=k + 1, usage=usage, definition=definition,
                               bound=len(bound), unbound=rest))
            unbound |= {(usage, name) for name in rest}
    if unbound != NAMED_UNBOUND[unit]:
        raise SystemExit(f'{unit}: unbound trailing formals {sorted(unbound)} differ from the named calc-usage keys '
                         f'{sorted(NAMED_UNBOUND[unit])}')
    return report


def definitions_in(path: Path) -> list[str]:
    return [DEF.match(line).group(2) for line in path.read_text().split('\n') if DEF.match(line)]


# ---------------------------------------------------------------------------------------------- step 4: bodies


def first_run(tree):
    return next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith('run_')), None)


def stubs(package: Path) -> set[str]:
    """Emitted manual stubs: generated implementation files that are not auto-implemented."""
    out = set()
    for path in (package / 'handwritten').rglob('*_impl.py'):
        text = path.read_text()
        if 'AUTO_IMPLEMENTED = True' not in text and 'raise NotImplementedError(' in text:
            out.add(path.relative_to(package / 'handwritten').as_posix())
    return out


def install_e2e(unit: str, receipts: list[dict]):
    """The WI-093 reuse rule: prefix rewrite in both forms, asserted reversible; a typed adapter only where the stock
    signature differs. B1 and B2 come from exploration/stellarator_materials/bodies/ with whole-body diff receipts."""
    name = UNITS[unit]['package']
    package = package_dir(unit)
    forms = [('from stellarator_tea.', f'from {name}.'), ("'stellarator_tea.", f"'{name}.")]
    installed = set()
    for source in sorted(E2E_BODIES.rglob('*.py')):
        if '__pycache__' in source.parts:
            continue
        relative = source.relative_to(E2E_BODIES).as_posix()
        text = source.read_text()
        if 'AUTO_IMPLEMENTED = False' not in text and relative != 'mfe_account_costs/financial_factors.py':
            continue
        original = text
        if relative in MODIFIED:
            copy = HERE / 'bodies' / relative
            text = copy.read_text()
            diff = ''.join(difflib.unified_diff(original.splitlines(True), text.splitlines(True),
                                                fromfile='exploration/stellarator_e2e/generated/handwritten/' + relative,
                                                tofile='exploration/stellarator_materials/bodies/' + relative))
            (EVIDENCE / 'bodies').mkdir(parents=True, exist_ok=True)
            (EVIDENCE / 'bodies' / (MODIFIED[relative] + '.diff')).write_text(diff)
        content = text
        for before, after in forms:
            content = content.replace(before, after)
        reverse = content
        for before, after in forms:
            reverse = reverse.replace(after, before)
        assert reverse == text, relative
        target = package / 'handwritten' / relative
        expected = first_run(ast.parse(target.read_text())) if target.exists() else None
        actual = first_run(ast.parse(content))
        if expected is not None and actual is not None:
            same = ast.dump(actual.args) == ast.dump(expected.args) and (ast.dump(actual.returns) if actual.returns else None) == (
                ast.dump(expected.returns) if expected.returns else None)
            if not same:
                raise SystemExit(f'{unit}: {relative} signature differs from the generated stub; no adapter is declared for it')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        installed.add(relative)
        receipts.append(dict(source=str((HERE / 'bodies' / relative if relative in MODIFIED else source).relative_to(ROOT)),
                             target=str(target.relative_to(ROOT)), source_sha256=sha(HERE / 'bodies' / relative)
                             if relative in MODIFIED else sha(source), target_sha256=sha(target), prefix_only=True,
                             modified=MODIFIED.get(relative), e2e_original_sha256=sha(source)))
    return installed


def install_adapted(unit: str, source: Path, relative: str, receipts: list[dict]):
    """Append the WI-099 typed adapter to a reviewed calculate() body; the body itself is unchanged."""
    name = UNITS[unit]['package']
    package = package_dir(unit)
    target = package / 'handwritten' / relative
    stub = first_run(ast.parse(target.read_text()))
    module_path = relative.removesuffix('_impl.py').replace('/', '.')
    body = source.read_text()
    declared = ast.literal_eval(next(n.value for n in ast.parse(body).body
                                     if isinstance(n, ast.Assign) and n.targets[0].id == 'OUTPUTS'))
    schema_path = package / 'schemas' / (Path(relative).name.removesuffix('_impl.py') + '_output.py')
    input_type = ast.unparse(stub.args.args[0].annotation)
    content = body + f'\n\nfrom {name}.modules.{module_path} import {input_type}\n\n\n'
    content += 'def _native_result(inputs):\n'
    content += '    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""\n'
    content += "    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})\n"
    if schema_path.exists():
        schema = ast.parse(schema_path.read_text())
        cls = next(n for n in schema.body if isinstance(n, ast.ClassDef))
        order = [n.target.id for n in cls.body if isinstance(n, ast.AnnAssign)]
        if sorted(declared) != sorted(order):
            raise SystemExit(f'{relative}: body OUTPUTS {declared} differ from generated schema {order}')
        content += f'    return tuple(result[k] for k in {order!r})\n'
    else:
        if len(declared) != 1 or ast.unparse(stub.returns) != 'float':
            raise SystemExit(f'{relative}: no output schema, so the stub must return one float')
        order = list(declared)
        content += f'    return result[{declared[0]!r}]\n'
    content += f'\n\ndef {stub.name}(inputs: {input_type}) -> {ast.unparse(stub.returns)}:\n    return _native_result(inputs)\n'
    target.write_text(content)
    receipts.append(dict(source=str(source.relative_to(ROOT)), target=str(target.relative_to(ROOT)), source_sha256=sha(source),
                         target_sha256=sha(target), new_body=True, typed_adapter=True, schema_order=order))
    return relative


def install_bodies(unit: str) -> tuple[list[dict], dict]:
    package = package_dir(unit)
    emitted = stubs(package)
    receipts = []
    installed = install_e2e(unit, receipts)
    for body in UNITS[unit]['round1']:
        installed.add(install_adapted(unit, ROUND1_BODIES / (body + '_impl.py'),
                                      f'magnet_conductor_alternatives/{body}_impl.py', receipts))
    for body in UNITS[unit].get('extra', ()):
        installed.add(install_adapted(unit, HERE / 'bodies/magnet_material_variants' / (body + '_impl.py'),
                                      f'magnet_material_variants/{body}_impl.py', receipts))
    missing = sorted(emitted - installed)
    extra = sorted(installed - emitted - set(E2E_PRESERVED) - {'mfe_account_costs/financial_factors.py'})
    if missing or extra:
        raise SystemExit(f'{unit}: body set differs from the emitted manual stubs: missing={missing}, unexpected={extra}')
    return receipts, dict(emitted_stubs=sorted(emitted), installed=sorted(installed),
                          preserved_without_stub=sorted(set(installed) - emitted), preserved_reasons=E2E_PRESERVED)


def write_census(unit: str):
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
    run(['python', '-c', code, str(package_dir(unit)), str(unit_dir(unit) / 'census.json')], f'{unit}/census-generation.log')


def build_unit(unit: str) -> dict:
    spec = UNITS[unit]
    staging_receipt = stage(unit)
    run(['python', '-m', 'syside', 'check', str(unit_dir(unit) / 'input_models')], f'{unit}/syside-check.log')
    bindings = check_positional_bindings(unit)
    staging = unit_dir(unit) / 'input_models'
    package = package_dir(unit)
    command = ['sysml-codegen', 'generate', '--models', str(staging), '--output', str(package), '--package-name', spec['package'],
               '--overwrite']
    run(command, f'{unit}/generation.log')
    receipts, body_set = install_bodies(unit)
    command += ['--smart-regen', '--preserve-handwritten']
    run(command, f'{unit}/completion-generation.log')
    for receipt in receipts:
        assert sha(ROOT / receipt['target']) == receipt['target_sha256'], f"regeneration changed {receipt['target']}"
    before = tree_hashes(package)
    run(command, f'{unit}/fixed-point-generation.log')
    after = tree_hashes(package)
    if before != after:
        raise SystemExit(f'{unit}: no fixed point: {sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))}')
    snapshot = unit_dir(unit) / (spec['package'].removesuffix('_tea') + '.snapshot.json')
    run(['sysml-codegen', 'snapshot', '--models', str(staging), '--output', str(snapshot)], f'{unit}/snapshot.log')
    write_census(unit)
    return dict(unit=unit, package=str(package.relative_to(ROOT)), package_name=spec['package'], staging=staging_receipt,
                positional_bindings=bindings, bodies=receipts, body_set=body_set, fixed_point=True,
                package_tree={k.removeprefix(str(package.relative_to(ROOT)) + '/'): v for k, v in after.items()},
                snapshot=str(snapshot.relative_to(ROOT)), snapshot_sha256=sha(snapshot),
                census=str((unit_dir(unit) / 'census.json').relative_to(ROOT)), census_sha256=sha(unit_dir(unit) / 'census.json'))


def build(units):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    before = protected_hashes()
    diverged = [logical for logical in twin_files() if canonical(logical).read_bytes() != (TWIN / logical).read_bytes()]
    if diverged or len(twin_files()) != 42:
        raise SystemExit(f'twin differs from canonical: {diverged} ({len(twin_files())} twin files)')
    if run(['python', str(HERE / 'author_materials_design.py'), '--check'], 'design-drift-check.log', check=False) != 0:
        raise SystemExit('the committed materials design files differ from author_materials_design.py output')
    receipt = dict(design='work/active/WI-100_stellarator-material-variants/design.md', hunks=str(HUNKS.relative_to(ROOT)),
                   hunks_sha256=sha(HUNKS), variants_sha256=sha(VARIANTS), round1_library_sha256=sha(ROUND1_LIBRARY),
                   design_files={p.name: sha(p) for p in sorted(DESIGN_DIR.glob('*.sysml'))},
                   reference_designs_sha256=sha(HERE / 'reference_designs.json'), twin_equals_canonical=True, units={})
    path = EVIDENCE / 'build-hashes.json'
    if path.exists():
        previous = json.loads(path.read_text())
        receipt['units'] = {k: v for k, v in previous.get('units', {}).items() if k not in units}
    for unit in units:
        receipt['units'][unit] = build_unit(unit)
    after = protected_hashes()
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    preservation = dict(scope='build', protected_roots=[str(p.relative_to(ROOT)) for p in PROTECTED], files=len(before),
                        changed=changed)
    (EVIDENCE / 'preservation-build.json').write_text(json.dumps(preservation, indent=2) + '\n')
    if changed:
        raise SystemExit(f'protected files changed during the build: {changed[:10]}')
    receipt['protected_files_unchanged'] = len(before)
    path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({unit: dict(files=len(r['package_tree']), bodies=len(r['bodies']), stubs=len(r['body_set']['emitted_stubs']),
                                 usages_checked=len(r['positional_bindings']), snapshot_sha256=r['snapshot_sha256'][:12])
                      for unit, r in receipt['units'].items()}, indent=1))


if __name__ == '__main__':
    selected = [a for a in sys.argv[1:] if a in UNITS] or list(UNITS)
    build(selected)
