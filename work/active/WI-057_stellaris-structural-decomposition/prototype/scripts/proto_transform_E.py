"""Prototype Stage E (on the Stage D tree): the magnet's thirteen calcs become template calcs
owned by the 'Magnet System' DEFINITION; the plant only wires the two radial-build inputs; a
variant definition replaces one calc by same-name redefinition with a different formula.

usage: proto_transform_E.py <models_root> <f_ins_markup value>
"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]); markup = sys.argv[2]

def take_block(text, header_re):
    m = re.search(header_re, text, re.M); assert m, header_re
    start = m.start()
    while True:
        prev = text.rfind("\n", 0, start - 1); line = text[prev + 1:start]
        if line.strip().startswith("//"): start = prev + 1
        else: break
    i = text.index("{", m.start()); depth = 0; j = i
    while True:
        c = text[j]
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: break
        j += 1
    end = j + 1
    if text[end] == "\n": end += 1
    return text[start:end], text[:start] + text[end:]

def reindent(stmt, delta):
    if delta >= 0: return "".join((" " * delta + ln if ln.strip() else ln) for ln in stmt.splitlines(True))
    return "".join((ln[-delta:] if ln.startswith(" " * -delta) else ln) for ln in stmt.splitlines(True))

MAGNET_CALCS = ["field_calc", "peak_field_calc", "stored_energy", "casing_mass", "wp_sizing", "coil_length",
                "wp_volume", "wp_stress", "cond_strain", "magnet_cost", "winding_pack_cost",
                "magnet_structure_cost", "magnet_capital_rollup"]

# ---- plant: cut the magnet usage body down to the two radial-build inputs -----------------
plant = root / "designs/generic_mfe/mfe_plant.sysml"; ps = plant.read_text()
blocks = []
for name in MAGNET_CALCS:
    blk, ps = take_block(ps, r"^            calc " + name + r" : '[^']+' \{")
    blocks.append(reindent(blk, -4))
# the usage body: remove capital_cost/B/expose binds and the sub-part blocks
mstart = ps.index("        part magnet : 'Magnet System' {\n"); mend = ps.index("\n        }\n", mstart) + len("\n        }\n")
body = ps[mstart:mend]
sub_blocks = []
for sub in ("winding_pack", "casing", "coil"):
    blk, body = take_block(body, r"^            part :>> " + sub + r" \{")
    sub_blocks.append(reindent(blk, -4))
body = re.sub(r"^            :>> (capital_cost|B|B_peak|sigma_wp|eps_cond|vol_cold_total|capital_cost_1cfe) = [^\n]*\n", "", body, flags=re.M)
body = re.sub(r"^            // WI-057 prototype: the magnet's own calcs live on the magnet\.\n", "", body, flags=re.M)
body = body.replace("            :>> r_coil = rb.r_coil;   // coil bore = radial-build vessel_or (WI-021)\n",
                    "            :>> r_coil = rb.r_coil;   // coil bore = radial-build vessel_or (WI-021)\n            :>> r_coil_centre = rb.r_coil_centre;   // WI-057: the coil-centre radius the magnet's own calcs read\n")
ps = ps[:mstart] + body + ps[mend:]
# vol_cold_cryo moves onto the magnet (review F3): drop the plant declaration
ps = re.sub(r"^        attribute vol_cold_cryo : Real default 0\.0;\n", "", ps, flags=re.M)
plant.write_text(ps)

# ---- library: template calcs on the definition ---------------------------------------------
lib = root / "cost_structure/mfe_power_core.sysml"; s = lib.read_text()
s = s.replace("    private import mfe_interfaces::*;\n",
              "    private import mfe_interfaces::*;\n    private import mfe_magnet_field::*;\n    private import mfe_magnet_cost::*;\n    private import mfe_plasma_scaling::'Conductor Peak Field';\n", 1)
calcs = "".join(blocks)
# inside the definition: read the producing calc directly where the formal shares the attribute's name
calcs = calcs.replace("in B = magnet.B;", "in B = field_calc.B_axis;   // the formal shares the EXPOSE's name: read the producer (D-5)")
calcs = calcs.replace("in B_axis_in = magnet.B;", "in B_axis_in = field_calc.B_axis;")
calcs = calcs.replace("in a_coil_in = rb.r_coil_centre;", "in a_coil_in = r_coil_centre;")
calcs = calcs.replace("in a_coil = rb.r_coil_centre;", "in a_coil = r_coil_centre;")
calcs = calcs.replace("in r_coil = rb.r_coil;", "in r_coil = 'Magnet System'::r_coil;   // formal and attribute share a name: owner-qualified")
calcs = calcs.replace("in structure_cost_in = magnet_structure_cost.cost;", "in structure_cost_in = structure_cost;   // the swap seam: a default-valued EXPOSE a variant may rebind")
calcs = calcs.replace("in vol_extra = vol_cold_cryo;", "in vol_extra = vol_cold_cryo;   // the magnet's own extra cold volume (review F3)")
sub_defs = "".join(sub_blocks)
sub_defs = sub_defs.replace("part :>> winding_pack {", "part winding_pack : 'Winding Pack' {").replace("part :>> casing {", "part casing : 'Coil Casing' {").replace("part :>> coil {", "part coil : 'Modular Coil' {")
mdef_start = s.index("    part def 'Magnet System' :> 'CAS22.1.3 Magnet System' {\n"); mdef_end = s.index("\n    }\n", mdef_start) + len("\n    }\n")
mdef = s[mdef_start:mdef_end]
mdef = re.sub(r"^        part (coil|winding_pack|casing) : '[^']+';\n", "", mdef, flags=re.M)
mdef = mdef.replace("        attribute B : Real;\n", "        // the axis field, an EXPOSE of the definition's own field calc\n        attribute B : Real = field_calc.B_axis;\n")
for name, src in (("B_peak", "peak_field_calc.B_peak"), ("sigma_wp", "wp_stress.sigma_wp"), ("eps_cond", "cond_strain.eps_cond"),
                  ("vol_cold_total", "wp_volume.vol_cold_total"), ("capital_cost_1cfe", "magnet_cost.capital_cost")):
    mdef = mdef.replace(f"        attribute {name} : Real;\n", f"        attribute {name} : Real = {src};\n")
tail = ("        // inputs the plant wires from the radial build (the r_coil pattern)\n        attribute r_coil_centre : Real;\n"
        "        // additional cold volume beyond the winding pack [m^3] (review F3: the magnet's, not the cryoplant's)\n        attribute vol_cold_cryo : Real default 0.0;\n"
        "        // SWAP SEAM: the structure cost the rollup reads, as a DEFAULT so a variant definition can point it at its own calc\n        attribute structure_cost : Real default magnet_structure_cost.cost;\n"
        "        :>> capital_cost = magnet_capital_rollup.capital_cost;\n" + sub_defs + calcs)
k = mdef.rindex("\n    }\n"); mdef = mdef[:k + 1] + tail + mdef[k + 1:]
s = s[:mdef_start] + mdef + s[mdef_end:]
# the variant: replaces ONE template calc by same-name redefinition with a different formula
s = re.sub(r"    part def 'NI Winding Pack' :> 'Winding Pack' \{\n.*?\n    \}\n", "", s, flags=re.S)
old_variant = re.search(r"    part def 'NI HTS Magnet System' :> 'Magnet System' \{\n.*?\n    \}\n", s, re.S).group(0)
new_variant = """    part def 'NI HTS Magnet System' :> 'Magnet System' {
        attribute t_charge_h : Real;
        // an insulation-free winding needs a thicker casing: the variant prices the casing with its own formula
        attribute f_ins_markup : Real default 0.0;
        calc magnet_structure_cost_ni : 'Magnet Structure Cost NI' {
            in n_coils = coil.n_coils;
            in m_casing = casing.m_casing;
            in steel_price = casing.steel_price;
            in f_steel_fab = casing.f_steel_fab;
            in f_ins = f_ins_markup;
        }
        :>> structure_cost = magnet_structure_cost_ni.cost;
    }
"""
s = s.replace(old_variant, new_variant)
s = s.replace("    private import mfe_magnet_cost::*;\n", "    private import mfe_magnet_cost::*;\n    private import mfe_magnet_cost_variants::*;\n", 1)
lib.write_text(s)
(root / "analyses/mfe_magnet_cost_variants.sysml").write_text("""package mfe_magnet_cost_variants {
    private import ScalarValues::*;
    // WI-057 prototype: a formula variant for the swap demonstration (not a sourced model).
    calc def 'Magnet Structure Cost NI' {
        in n_coils : Real;
        in m_casing : Real;
        in steel_price : Real;
        in f_steel_fab : Real;
        in f_ins : Real;
        return cost : Real = n_coils * m_casing * steel_price * f_steel_fab * (1.0 + f_ins);
    }
}
""")

# ---- instance: bind the moved attribute and the variant's markup; drop the sub-part retype ----
inst = root / "designs/stellarator_09/stellarator_plant.sysml"; ts = inst.read_text()
ts = ts.replace("            part :>> winding_pack : 'NI Winding Pack' {\n                :>> f_insulation = 0.0;\n", "            part :>> winding_pack {\n")
stmt, ts = take_block(ts, r"^        :>> vol_cold_cryo = ") if re.search(r"^        :>> vol_cold_cryo = [^;\n]*\{", ts, re.M) else (None, ts)
if stmt is None:
    m = re.search(r"^        :>> vol_cold_cryo = [^\n]*\n", ts, re.M); stmt = m.group(0); ts = ts[:m.start()] + ts[m.end():]
ts = ts.replace("            :>> t_charge_h = 600.0;\n", f"            :>> t_charge_h = 600.0;\n            :>> f_ins_markup = {markup};\n" + reindent(stmt, 4))
inst.write_text(ts)
print("Stage E applied: 13 template calcs on the definition; variant redefines magnet_structure_cost; f_ins_markup =", markup)
