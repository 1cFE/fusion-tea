"""Scratch: write designs/stellarator_09_probe/probe_plant.sysml into a staged probe tree (P1-P3, P5)."""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
names = sys.argv[2:] or ['probe_a', 'probe_b']
src = (tree / 'designs/stellarator_09/stellarator_plant.sysml').read_text()
lines = src.split('\n')
start = lines.index("    part stellaris : 'MFE Power Plant' {")
end = len(lines) - 1 - lines[::-1].index('    }')
block = '\n'.join(lines[start:end + 1])
header = '\n'.join(l for l in lines[1:start] if l.strip().startswith('private import'))


def copy(name):
    b = block.replace("    part stellaris : 'MFE Power Plant' {", f"    part {name} : 'MFE Power Plant' {{", 1)
    b, n = re.subn(r'(?<![\w])stellaris\.', name + '.', b)
    assert n == 7, n
    old = '        part :>> magnet {\n'
    assert b.count(old) == 1
    b = b.replace(old, "        part :>> magnet : 'Probe Magnet System' {\n            :>> probe_winding_extra = 1000.0;\n            :>> probe_knot = 20.0;\n", 1)
    old = '        part :>> cryoplant {\n'
    assert b.count(old) == 1
    b = b.replace(old, "        part :>> cryoplant : 'Probe Cryoplant' {\n            :>> probe_p_extra = 0.25;\n            :>> probe_drive = 0.0502673272;\n            :>> probe_q_cold = 21933.902368719853;\n            :>> probe_q_shield = 41599.953939961626;\n            :>> probe_capital = 31478692.121086925;\n", 1)
    i = b.index("        part :>> cryoplant : 'Probe Cryoplant' {\n")
    j = b.index('\n        }\n', i)
    cryo = b[i:j]
    cryo, n = re.subn(r'\n            :>> purchase_cost_per_module = 31478692\.121086925 \{[^\n]*\}', '', cryo)
    assert n == 1, n
    cryo, n = re.subn(r'\n            :>> inventory_enabled = true \{\n[^\n]*\n            \}', '', cryo)
    assert n == 1, n
    return b[:i] + cryo + b[j:]


out = 'package stellarator_09_probe {\n' + header + '\n    private import probe_variants::*;\n' + '\n'.join(copy(n) for n in names) + '\n}\n'
target = tree / 'designs/stellarator_09_probe/probe_plant.sysml'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(out)
print(target, len(out.splitlines()))
