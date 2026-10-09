"""Derive the WI-100 material-instance design files from the staged Stellaris design file (design section 2.10).

Copies `part stellaris : 'MFE Power Plant' { ... }` from the staged, byte-identical
models/designs/stellarator_09/stellarator_plant.sysml and applies the declared edit list E1-E9, once per material:

  E1 rename the part; E2 rewrite the seven self-references with the word-boundary pattern (count asserted 7);
  E3 retype the magnet; E4 retype the cryoplant; E5 delete the cryoplant purchase_cost_per_module and
  inventory_enabled bindings (final in the variant); E6 re-point reference_conductor_current_ok to the variant's
  acceptance margin; E7 add the variant attribute bindings (Round 1 values cited by path and line, arm_x_ref on the
  coil); E8 the material values and default supplied quantities of reference_designs.json; E9 the package header.

Output (probe P2 fallback, K21): one file per material instance, both in package `stellarator_09_materials` so the
entry-key prefixes are `stellarator_09_materials__<rebco_material|nb3sn_material>__` (design section 5.1), because
a generation unit may hold only one instance of 'MFE Power Plant'. The two files are never staged together.

Docs of every attribute written here state their basis in words with no bracketed token: a bracket in a formula
operand's doc causes SI_RENDERING_COLLISION (WI-099 implementation-notes.md:27; design D14).

Usage: .codex-test/run python exploration/stellarator_materials/author_materials_design.py [--check]
  --check refuses (exit 1) if the committed design files differ from this script's output (build drift check).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STELLARIS = ROOT / 'exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml'
DESIGNS = json.loads((HERE / 'reference_designs.json').read_text())['designs']
OUT_DIR = HERE / 'models/designs/stellarator_09_materials'
PACKAGE = 'stellarator_09_materials'
MAGNET_TYPES = {'rebco_material': 'Round1 REBCO Magnet System', 'nb3sn_material': 'Nb3Sn Magnet System'}
SOURCE_DOC = 'exploration/stellarator_materials/reference_designs.json'
DATE = '2026-09-30'


def fmt(value: float) -> str:
    text = repr(float(value))
    return text if ('.' in text or 'e' in text or 'inf' in text) else text + '.0'


def strip_comments(line: str, in_block: bool) -> tuple[str, bool]:
    """The line's code outside /* */ blocks and // comments, and whether a block comment is still open."""
    out, i = [], 0
    while i < len(line):
        if in_block:
            j = line.find('*/', i)
            if j < 0:
                return ''.join(out), True
            i, in_block = j + 2, False
        elif line.startswith('/*', i):
            in_block, i = True, i + 2
        elif line.startswith('//', i):
            break
        else:
            out.append(line[i])
            i += 1
    return ''.join(out), in_block


def block_end(lines: list[str], start: int) -> int:
    """Index of the line holding the brace that closes the block opened on lines[start]."""
    depth, in_block, opened = 0, False, False
    for k in range(start, len(lines)):
        code, in_block = strip_comments(lines[k], in_block)
        for ch in code:
            if ch == '{':
                depth += 1
                opened = True
            elif ch == '}':
                depth -= 1
                if opened and depth == 0:
                    return k
    raise AssertionError(f'unclosed block at line {start + 1}')


def child(lines: list[str], span: tuple[int, int], pattern: str) -> int:
    """The unique line in the span, at the span's direct child depth, whose text matches pattern."""
    start, end = span
    depth, in_block, hits = 0, False, []
    for k in range(start, end + 1):
        code, before = strip_comments(lines[k], in_block)
        if depth == 1 and re.match(pattern, lines[k]):
            hits.append(k)
        for ch in code:
            depth += (ch == '{') - (ch == '}')
        in_block = before
    assert len(hits) == 1, (pattern, [h + 1 for h in hits])
    return hits[0]


def span_of(lines: list[str], span: tuple[int, int], pattern: str) -> tuple[int, int]:
    k = child(lines, span, pattern)
    return k, block_end(lines, k)


def binding_span(lines, span, name):
    k = child(lines, span, r'\s*:>> ' + re.escape(name) + r' = ')
    code, _ = strip_comments(lines[k], False)
    return (k, block_end(lines, k)) if '{' in code else (k, k)


def doc_binding(indent: str, name: str, value: float, text: str, reference: str, basis: str) -> list[str]:
    return [f'{indent}:>> {name} = {fmt(value)} {{',
            f'{indent}    doc /* {text} **Source**: {SOURCE_DOC} **Reference**: {reference} **Basis**: {basis} **Last Updated**: {DATE} */',
            f'{indent}}}']


def value_of(lines, k):
    match = re.match(r'\s*:>> \w+ = ([-0-9.eE+]+)', lines[k])
    return float(match.group(1))


def material_block(block: list[str], name: str) -> list[str]:
    design = DESIGNS[name]
    lines = list(block)
    # E1
    assert lines[0] == "    part stellaris : 'MFE Power Plant' {"
    lines[0] = f"    part {name} : 'MFE Power Plant' {{"
    # E2
    text = '\n'.join(lines)
    text, count = re.subn(r'(?<![\w])stellaris\.', name + '.', text)
    assert count == 7, count
    lines = text.split('\n')
    whole = (0, len(lines) - 1)
    # E3, E4
    magnet = span_of(lines, whole, r'\s*part :>> magnet \{')
    lines[magnet[0]] = lines[magnet[0]].replace('part :>> magnet {', f"part :>> magnet : '{MAGNET_TYPES[name]}' {{")
    cryo = span_of(lines, whole, r'\s*part :>> cryoplant \{')
    lines[cryo[0]] = lines[cryo[0]].replace('part :>> cryoplant {', "part :>> cryoplant : 'Staged Cryoplant' {")
    # E6
    k = child(lines, whole, r'\s*assert constraint reference_conductor_current_ok ')
    assert lines[k + 1].strip() == 'in margin_fraction_in = magnet.conductor_margin_fraction;', lines[k + 1]
    lines[k + 1] = lines[k + 1].replace('magnet.conductor_margin_fraction', 'magnet.conductor_acceptance_margin')
    # E8: existing supplied bindings whose values change (edits collected, applied bottom-up below)
    edits = []
    for path, value in design['existing']['values'].items():
        part, *rest = path.split('.')
        span = magnet if part == 'magnet' else cryo
        if len(rest) == 2:
            span = span_of(lines, span, r'\s*part :>> ' + rest[0] + r' \{')
        k, end = binding_span(lines, span, rest[-1])
        current = value_of(lines, k)
        if current == value:
            continue
        indent = re.match(r'(\s*)', lines[k]).group(1)
        reference = design['existing']['references'][path]
        text = f'WI-100 {name} default supplied value (replaces the Stellaris {fmt(current)}).'
        edits.append((k, end, doc_binding(indent, rest[-1], value, text, f'designs.{name}.existing {path}; {reference}',
                                          'material default design, supplied and evaluated as given, never resized')))
    # E5: the cryoplant's purchase price and inventory switch are final in 'Staged Cryoplant'
    for binding in ('purchase_cost_per_module', 'inventory_enabled'):
        k, end = binding_span(lines, cryo, binding)
        edits.append((k, end, []))
    # E7: new variant attribute bindings
    coil = span_of(lines, magnet, r'\s*part :>> coil \{')
    inserts = []
    for group, span in (('magnet', magnet), ('coil', coil), ('cryoplant', cryo)):
        indent = re.match(r'(\s*)', lines[span[0]]).group(1) + '    '
        new = []
        for key, value in design[group]['values'].items():
            reference = design[group]['references'][key]
            text = f'WI-100 {name} variant input {key}.'
            new += doc_binding(indent, key, value, text, reference, 'inherited Round 1 or contract value as cited, held for this material'
                               if group != 'coil' else 'arm anchor R over the pack side at the Stellaris point, derived, bound only in the material instances')
        inserts.append((span[0] + 1, new))
    # one bottom-up pass so no edit moves the line numbers of another
    changes = sorted([(k, end + 1, new) for k, end, new in edits] + [(at, at, new) for at, new in inserts], reverse=True)
    for (start, stop, _), (next_start, next_stop, _) in zip(changes, changes[1:]):
        assert next_stop <= start, 'overlapping edits'
    for start, stop, new in changes:
        lines[start:stop] = new
    return lines


def render() -> dict[str, str]:
    source = STELLARIS.read_text().split('\n')
    start = source.index("    part stellaris : 'MFE Power Plant' {")
    end = block_end(source, start)
    block = source[start:end + 1]
    imports = [line for line in source[:start] if line.strip().startswith('private import')]
    assert len(imports) == 9, imports
    files = {}
    for name in DESIGNS:
        header = [f'package {PACKAGE} {{',
                  f'    doc /* WI-100 material-variant copy of the Stellaris plant instance ({name}): the staged '
                  f'models/designs/stellarator_09/stellarator_plant.sysml part stellaris (lines {start + 1}-{end + 1}) with the declared '
                  f'edit list E1-E9 of work/active/WI-100_stellarator-material-variants/design.md section 2.10, generated by '
                  f'exploration/stellarator_materials/author_materials_design.py from reference_designs.json. The magnet is retyped '
                  f"'{MAGNET_TYPES[name]}' and the cryoplant 'Staged Cryoplant'; every other binding is the Stellaris file's. "
                  f'**Source**: {SOURCE_DOC} **Reference**: designs.{name} **Basis**: [AGENT] reviewed design; do not edit by hand, '
                  f'regenerate. **Last Updated**: {DATE} */'] + imports + ['    private import magnet_material_variants::*;', '']
        files[name] = '\n'.join(header + material_block(block, name) + ['}', ''])
    return files


def main(argv):
    files = render()
    drift = []
    for name, text in files.items():
        target = OUT_DIR / f'{name}.sysml'
        if '--check' in argv:
            if not target.exists() or target.read_text() != text:
                drift.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
            print(target.relative_to(ROOT), len(text.splitlines()), 'lines')
    if drift:
        print('design files differ from author_materials_design.py output:', drift)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
