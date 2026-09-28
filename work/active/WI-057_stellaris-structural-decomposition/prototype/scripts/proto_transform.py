"""Prototype transformation, Stage A: magnet sub-parts + a plasma part; calcs stay on the plant.

Edits the scratch twin tree in place. Writes a move map (attribute -> new owner path) as JSON.
usage: proto_transform.py <models_root> <movemap_out.json>
"""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])

# ---- the regrouping map (prototype scope) ---------------------------------------------
COIL = ["n_coils", "I_coil", "k_link", "f_set", "R0", "G", "c_coil", "k_coil", "cost_per_kAm",
        "coil_markup", "peak_ratio", "I_ref", "R_ref", "a_coil_ref"]
WP = ["j_wp", "wp_side", "f_wp_vol", "E_wp", "f_cond", "eps_cond_allow", "f_wp_fab", "k_sigma", "B_max"]
CASING = ["m_casing", "m_casing_ref", "W_mag_ref", "steel_price", "f_steel_fab", "sigma_allow"]
MAGNET_KEEP = ["B", "r_coil"]
PLASMA = ["R", "a", "kappa", "f_shape", "n_e", "sigma_v", "E_fus", "T_i0", "alpha_n", "alpha_T",
          "n_e0", "iota_23", "f_ren", "f_alpha_fast", "tau_ratio_ash", "f_suppr_ash",
          "Z_eff_core", "f_W_core", "Ti_over_Te"]
SUB = {**{a: "coil" for a in COIL}, **{a: "winding_pack" for a in WP}, **{a: "casing" for a in CASING}}

def read(p): return p.read_text()
def write(p, s): p.write_text(s)

# ---- 1. library: mfe_power_core.sysml -------------------------------------------------
lib = root / "cost_structure/mfe_power_core.sysml"
s = read(lib)
m = re.search(r"    part def 'Magnet System' :> 'CAS22\.1\.3 Magnet System' \{\n(.*?)\n    \}\n", s, re.S)
assert m, "magnet def not found"
body = m.group(1) + "\n"
# pull every attribute declaration line (with its preceding // comments) out of the body
attr_re = re.compile(r"((?:        //[^\n]*\n)*)        attribute (\w+) : Real;\n")
decls = {}
for cm, name in attr_re.findall(body):
    decls[name] = cm + f"        attribute {name} : Real;\n"
doc = re.search(r"        doc /\*.*?\*/\n", body, re.S).group(0)
def block(defname, names):
    inner = "".join(decls[n] for n in names)
    return f"    part def '{defname}' {{\n{inner}    }}\n"
new_defs = (
    "    // WI-057 prototype: the magnet system decomposed into the physical parts its calcs price.\n"
    + block("Modular Coil", COIL) + block("Winding Pack", WP) + block("Coil Casing", CASING)
    + "    part def 'Magnet System' :> 'CAS22.1.3 Magnet System' {\n" + doc
    + "".join(decls[n] for n in MAGNET_KEEP)
    + "        part coil : 'Modular Coil';\n        part winding_pack : 'Winding Pack';\n        part casing : 'Coil Casing';\n    }\n"
)
s = s[:m.start()] + new_defs + s[m.end():]
write(lib, s)

# ---- 2. library: a Plasma part def in a new structure/ file ---------------------------
plant = root / "designs/generic_mfe/mfe_plant.sysml"
ps = read(plant)
plasma_decls = []
for name in PLASMA:
    mm = re.search(r"((?:        //[^\n]*\n)*)        attribute " + name + r" : Real( default [^;]+)?;\n", ps)
    assert mm, name
    plasma_decls.append(mm.group(1) + f"        attribute {name} : Real{mm.group(2) or ''};\n")
    ps = ps[:mm.start()] + ps[mm.end():]
(root / "structure").mkdir(exist_ok=True)
write(root / "structure/mfe_plasma.sysml",
      "package mfe_plasma {\n    private import ScalarValues::*;\n"
      "    // WI-057 prototype: the plasma as a part owning its geometry, density, temperature and profile facts.\n"
      "    part def 'Plasma' {\n" + "".join(plasma_decls) + "    }\n}\n")

# ---- 3. plant: compose plasma, nest the magnet's computed bindings, re-point references -
ps = ps.replace("    private import mfe_power_core::*;\n", "    private import mfe_power_core::*;\n    private import mfe_plasma::*;\n")
ps = ps.replace("        part magnet : 'Magnet System' {\n",
                "        part plasma : 'Plasma';\n        part magnet : 'Magnet System' {\n")
ps = ps.replace("            :>> wp_side = wp_sizing.wp_side;\n",
                "            part :>> winding_pack {\n                :>> wp_side = wp_sizing.wp_side;\n            }\n")
ps = ps.replace("            :>> m_casing = casing_mass.m_casing;\n            :>> c_coil = coil_length.c_coil;\n",
                "            part :>> casing {\n                :>> m_casing = casing_mass.m_casing;\n            }\n"
                "            part :>> coil {\n                :>> c_coil = coil_length.c_coil;\n            }\n")
for name, sub in SUB.items():
    ps = re.sub(r"\bmagnet\." + name + r"\b", f"magnet.{sub}.{name}", ps)
# plasma attributes: bare references inside calc bindings / expressions -> plasma.<name>
for name in PLASMA:
    ps = re.sub(r"(= )" + name + r"(;)", rf"\1plasma.{name}\2", ps)
write(plant, ps)

# ---- 4. instance: nest the magnet bindings and the plasma bindings -----------------------
inst = root / "designs/stellarator_09/stellarator_plant.sysml"
ts = read(inst)

def take_binding(text, indent, name):
    """Cut one `:>> name = value;` or `:>> name = value { ... }` statement (balanced braces)."""
    pat = re.compile(r"^" + indent + r":>> " + name + r" = [^;{\n]*", re.M)
    mm = pat.search(text)
    assert mm, f"binding {name} not found"
    i = mm.end()
    if text[i] == ";":
        end = i + 1
    else:
        assert text[i] == "{", (name, text[i:i+20])
        depth = 0
        j = i
        while True:
            c = text[j]
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            j += 1
        end = j + 1
    if text[end] == "\n": end += 1
    return text[mm.start():end], text[:mm.start()] + text[end:]

def reindent(stmt, delta):
    return "".join((" " * delta + ln if ln.strip() else ln) for ln in stmt.splitlines(True))

# magnet block: move the 26 subsystem bindings into sub-part blocks
mstart = ts.index("        part :>> magnet {\n")
mend = ts.index("        part :>> blanket {\n")
mblock = ts[mstart:mend]
moved = {"coil": [], "winding_pack": [], "casing": []}
for name in COIL + WP + CASING:
    if re.search(r"^            :>> " + name + r" = ", mblock, re.M):
        stmt, mblock = take_binding(mblock, "            ", name)
        moved[SUB[name]].append(reindent(stmt, 4))
tail = "\n".join([f"            part :>> {sub} {{\n" + "".join(stmts) + "            }\n" for sub, stmts in moved.items() if stmts])
k = mblock.rindex("\n        }\n")
mblock = mblock[:k + 1] + tail + mblock[k + 1:]
ts = ts[:mstart] + mblock + ts[mend:]

# plasma: cut the 19 plant-level bindings and re-home them in a plasma block after the magnet block
pl_stmts = []
for name in PLASMA:
    stmt, ts = take_binding(ts, "        ", name)
    pl_stmts.append(reindent(stmt, 4))
insert_at = ts.index("        part :>> blanket {\n")
ts = ts[:insert_at] + "        part :>> plasma {\n" + "".join(pl_stmts) + "        }\n" + ts[insert_at:]
write(inst, ts)

movemap = {**{n: f"magnet.{s}" for n, s in SUB.items()}, **{n: "plasma" for n in PLASMA}}
out.write_text(json.dumps(movemap, indent=1, sort_keys=True))
print("moved", len(movemap), "attributes; magnet bindings relocated:", {k: len(v) for k, v in moved.items()})
