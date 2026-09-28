"""WI-057 commit A: parts and attribute homes on a model tree (canonical or twin layout).

usage: transform_A_full.py <models_root> <lib_prefix: 'library/' or ''> <attribute_homes.json>
Moves every attribute with a component home from the plant (and the magnet's from 'Magnet System')
to its owner's definition; declares the new definitions; composes the new parts; re-points every
binding; nests the instance's bindings. No calc def, constraint def, formula or value is touched.
"""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1]); LIB = sys.argv[2]; homes = json.loads(Path(sys.argv[3]).read_text())
PLANT = root / "designs/generic_mfe/mfe_plant.sysml"
SUBS = root / "designs/generic_mfe/mfe_subsystems.sysml"
CORE = root / f"{LIB}cost_structure/mfe_power_core.sysml"
INST = root / "designs/stellarator_09/stellarator_plant.sysml"
STRUCT = root / f"{LIB}structure"; STRUCT.mkdir(exist_ok=True)

home_of = {a: k for k, v in homes.items() if not k.startswith("_") and not k.startswith("plant") for a in v}
# the costed subsystem defs' own attributes already live on them: not moved
SUBSYS_OWN = {"unit_cost", "structure_factor", "blanket_vol", "shield_scale", "shield_vol", "structure_vol", "vessel_vol", "base", "cost_per_mw"}
MAGNET_OWN_TODAY = set(re.findall(r"^        attribute (\w+) : Real;", re.search(r"part def 'Magnet System'.*?\n    \}\n", CORE.read_text(), re.S).group(0), re.M))

# ------------------------------------------------------------------ helpers
def take_decl(text, name, indent="        "):
    """Cut `attribute name : Real[ default v];` with the // comment lines immediately above it."""
    m = re.search(r"^" + indent + r"attribute " + name + r" : Real( default [^;\n]+)?;[^\n]*\n", text, re.M)
    assert m, f"declaration of {name} not found"
    start = m.start()
    while True:
        prev = text.rfind("\n", 0, start - 1) + 1
        line = text[prev:start]
        if line.strip().startswith("//") and prev < start: start = prev
        else: break
    return text[start:m.end()], text[:start] + text[m.end():]

def take_binding(text, indent, name):
    pat = re.compile(r"^" + indent + r":>> " + name + r" = [^;{\n]*", re.M)
    mm = pat.search(text); assert mm, f"binding {name} not found"
    i = mm.end()
    if text[i] == ";": end = i + 1
    else:
        assert text[i] == "{", (name, text[i:i + 20]); depth = 0; j = i
        while True:
            c = text[j]
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            j += 1
        end = j + 1
    if text[end] == "\n": end += 1
    start = mm.start()
    while True:  # carry the // comment lines immediately above the binding
        prev = text.rfind("\n", 0, start - 1) + 1
        line = text[prev:start]
        if line.strip().startswith("//") and not line.strip().startswith("// ---") and prev < start: start = prev
        else: break
    return text[start:end], text[:start] + text[end:]

def reindent(stmt, delta):
    if delta >= 0: return "".join((" " * delta + ln if ln.strip() else ln) for ln in stmt.splitlines(True))
    return "".join((ln[-delta:] if ln.startswith(" " * -delta) else ln) for ln in stmt.splitlines(True))

def rewrite_refs(text, mapping, skip_doc=True):
    """On binding/expression lines, rewrite bare references on the right of `=` to owner-qualified ones."""
    out = []; in_doc = False
    for ln in text.splitlines(True):
        st = ln.strip()
        if in_doc:
            out.append(ln)
            if "*/" in st: in_doc = False
            continue
        if st.startswith("doc /*") or st.startswith("/*"):
            out.append(ln)
            if "*/" not in st: in_doc = True
            continue
        if st.startswith("//") or not st:
            out.append(ln); continue
        if "=" in ln and (st.startswith("in ") or st.startswith(":>>") or st.startswith("attribute ")):
            lhs, rhs = ln.split("=", 1)
        elif not re.match(r"\s*(in |:>>|attribute |part |calc |assert |connect |doc|private import|//|\})", ln) and re.search(r"[+\-*/(]", ln):
            lhs, rhs = "", ln  # continuation line of a multi-line expression
        else:
            out.append(ln); continue
        # do not rewrite inside a trailing comment or an opening doc brace
        cut = len(rhs)
        for tok in ("//", "{"):
            k = rhs.find(tok)
            if k != -1: cut = min(cut, k)
        head, tail = rhs[:cut], rhs[cut:]
        for name, repl in mapping.items():
            head = re.sub(r"(?<![\w.'])" + re.escape(name) + r"(?![\w'])", repl, head)
        out.append(lhs + ("=" if lhs else "") + head + tail)
    return "".join(out)

# ------------------------------------------------------------------ 1. plant: cut the moving declarations
ps = PLANT.read_text()
moved = {}  # name -> declaration text
for name, owner in home_of.items():
    if name in SUBSYS_OWN or name in MAGNET_OWN_TODAY: continue
    decl, ps = take_decl(ps, name); moved[name] = decl
print("plant declarations moved:", len(moved))

# ------------------------------------------------------------------ 2. definitions
DOCS = {
 "Plasma": """        doc /*
        The confined D-T plasma, as a part: its geometry (major and minor radius, elongation,
        the stellarator shape factor), its operating point (peak density and ion temperature,
        the profile exponents), and the sustainment facts the source states for the design
        point (rotational transform, ISS04 renormalisation, fast-alpha confinement, the
        particle-to-energy confinement ratio, helium suppression, core impurities, the
        ion-to-electron temperature ratio). Every value is bound by the concept instance with
        its own citation; nothing here is concept-specific (MR-3). WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: secs. 2.2-2.5 (the design point, Table 2 image page_002_table_0.png; profiles Fig. 16)
        **Basis**: the plasma as the owner of the quantities the geometry, sustainment, beta and fusion calcs read
        */
""",
 "First Wall": """        doc /*
        The plasma-facing wall of the blanket module. In the source: EUROFER97 with a 2 mm
        tungsten armour, helium-cooled at 8 MPa (350 C in, below 370 C out) on a loop the
        model does not compute separately -- the model carries one primary loop (see
        'Primary Heat Transport'). Owns its radial thickness, the vacuum gap it stands off
        from the plasma, the neutron wall-load peak calibration facts (WI-041) and the
        fluence replacement limit the lifecycle calendar reads (WI-046). WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: first-wall section (Fig. 27; lines ~1300-1350); Table 6 image page_021_table_6.png (radial build)
        **Basis**: the first wall as the owner of the wall-load and lifetime quantities
        */
""",
 "Modular Coil": """        doc /*
        One of the modular non-planar HTS coils (50 in the source, 6 unique shapes, 5-fold
        symmetry): the coil-set current and its distribution facts, the coil geometry facts
        (major radius, geometry factor, winding circumference and shape factor, the radial
        thickness of the coil in the build), the conductor cost rate and manufacturing markup,
        the peak-to-axis field ratio and the WI-044 reference anchors, and the coil dose life.
        WI-057: regrouped from 'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (coils; Table 8 image page_022_table_0.png)
        **Basis**: the coil as the owner of the current, geometry and conductor-cost facts
        */
""",
 "Winding Pack": """        doc /*
        The coil's winding pack: REBCO tape stacks in a copper jacket (15 % conductor, 10 % Cu,
        45 % insulation, 26 % steel, 4 % helium in the source's composition), sized by the
        current it carries (WI-036). Owns the current density, the pack-volume distribution
        and fabrication factors, the conductor's modulus, load share and strain limit, the
        conductor field ceiling, the peak-stress transfer fact and the mean nuclear heating the
        cryoplant removes. WI-057: regrouped from 'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (winding pack composition; Table 8 image page_022_table_0.png)
        **Basis**: the winding pack as the owner of the conductor and pack facts
        */
""",
 "Coil Casing": """        doc /*
        The cast steel casing around each winding pack (AISI 316LN, 63-200 t each in the
        source), the part the structure-cost account prices (WI-035 D5: casings only; the
        inter-coil plates and support rings are the plant's 'Primary Structure', CAS22.1.5).
        Owns the casing mass (computed since WI-044), its reference anchors, the steel price,
        the fabrication markup and the structural allowable stress. WI-057: regrouped from
        'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (casings; the 800 MPa design limit)
        **Basis**: the casing as the owner of the structural-mass and steel-cost facts
        */
""",
 "Primary Heat Transport": """        doc /*
        The primary coolant loop between the blanket and the power cycle. WHAT THE MODEL
        COMPUTES: the representative helium primary circuit of WI-045 (Moscato et al. 2017, the
        EU DEMO HCLL balance of plant), in sized-flow mode with its pumping power. WHAT THE
        SOURCE SAYS: the Stellaris breeding zone is water-cooled at PWR conditions and the first
        wall helium-cooled at 8 MPa (output.md lines 1490-1491, 1534-1536) -- goal
        structural-decomposition fact 6, surfaced and carried as a follow-on, not changed here.
        Owns the loop facts and mode flags and the two coolant cost bases. WI-057.
        **Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
        **Ref**: WI-045 design; output.md:79 (helium at 8 MPa)
        **Basis**: the loop as the owner of the circuit facts the primary-loop calc reads
        */
""",
 "Cryoplant": """        doc /*
        The cryogenic plant that holds the magnet cold mass at its operating temperature
        (20 K in the source). Owns the cryoplant chain facts (WI-024: nuclear heating uplift,
        fixed load, Carnot fraction, cold and ambient temperatures, the direct term), the coil
        cooling powers and the cryoplant cost base. WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (20 K operation); WI-024 design
        **Basis**: the cryoplant as the owner of the cold-load-to-electrical chain facts
        */
""",
 "Fuel Cycle": """        doc /*
        The tritium fuel cycle: the D-T fuel cost facts and the reduced flows of WI-047 (burn
        fraction, recovery and recycle, extraction efficiency, decay, inventory and stock
        growth), the tritium-systems power and the fuel-handling cost base. Tritium is bred in
        the blanket (see 'Blanket'::tbr) and returned to the plasma. WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: blanket and fuel-cycle statements (TBR 1.074, Table 6 image page_021_table_6.png); WI-047 design
        **Basis**: the fuel cycle as the owner of the flow and fuel-cost facts
        */
""",
 "Vacuum Pumping": """        doc /*
        The torus exhaust pumping: the exhaust gas temperature and pressure the gas-load calc
        reads (WI-047; the source prints neither). WI-057.
        **Source**: work/active/WI-047_fuel-divertor-vacuum-flows/design.md
        **Ref**: the vacuum gas load
        **Basis**: the pumping system as the owner of the exhaust-state facts
        */
""",
}
def new_def(name, attrs, extra=""):
    body = "".join(reindent(moved[a], 0) for a in attrs if a in moved)
    return f"    part def '{name}' {{\n{DOCS[name]}{extra}{body}    }}\n"

def owner_attrs(owner): return [a for a in homes.get(owner, []) if a in moved]

# 2a. structure files
(STRUCT / "mfe_plasma.sysml").write_text("package mfe_plasma {\n    private import ScalarValues::*;\n\n" + new_def("Plasma", owner_attrs("plasma")) + "}\n")
(STRUCT / "mfe_radial_build_parts.sysml").write_text("package mfe_radial_build_parts {\n    private import ScalarValues::*;\n\n" + new_def("First Wall", owner_attrs("blanket.first_wall")) + "}\n")
(STRUCT / "mfe_plant_systems.sysml").write_text("package mfe_plant_systems {\n    private import ScalarValues::*;\n\n"
    + new_def("Primary Heat Transport", owner_attrs("heat_transport")) + "\n" + new_def("Cryoplant", owner_attrs("cryoplant")) + "\n"
    + new_def("Fuel Cycle", owner_attrs("fuel_cycle")) + "\n" + new_def("Vacuum Pumping", owner_attrs("vacuum_pumping")) + "}\n")

# 2b. the magnet: split 'Magnet System' by the home map
cs = CORE.read_text()
m = re.search(r"    part def 'Magnet System' :> 'CAS22\.1\.3 Magnet System' \{\n(.*?)\n    \}\n", cs, re.S)
body = m.group(1) + "\n"
attr_re = re.compile(r"((?:        //[^\n]*\n)*)        attribute (\w+) : Real;\n")
mdecls = {n: c + f"        attribute {n} : Real;\n" for c, n in attr_re.findall(body)}
mdoc = re.search(r"        doc /\*.*?\*/\n", body, re.S).group(0)
mdoc = mdoc.replace("        Concept-agnostic magnet/coil system carrying the coil-cost parameters",
    "        Concept-agnostic magnet/coil system, decomposed since WI-057 into the physical parts\n        its calcs price -- 'Modular Coil', 'Winding Pack', 'Coil Casing' (mfe_magnet_parts) -- and\n        carrying the coil-cost parameters")
def part_block(defname, sub):
    return "".join(mdecls[a] if a in mdecls else reindent(moved[a], 0) for a in homes[sub] if a in mdecls or a in moved)
magnet_parts = ("package mfe_magnet_parts {\n    private import ScalarValues::*;\n\n"
    + f"    part def 'Modular Coil' {{\n{DOCS['Modular Coil']}{part_block('Modular Coil', 'magnet.coil')}    }}\n\n"
    + f"    part def 'Winding Pack' {{\n{DOCS['Winding Pack']}{part_block('Winding Pack', 'magnet.winding_pack')}    }}\n\n"
    + f"    part def 'Coil Casing' {{\n{DOCS['Coil Casing']}{part_block('Coil Casing', 'magnet.casing')}    }}\n}}\n")
(STRUCT / "mfe_magnet_parts.sysml").write_text(magnet_parts)
magnet_own = "".join(mdecls[a] if a in mdecls else reindent(moved[a], 0) for a in homes["magnet"] if a in mdecls or a in moved)
new_magnet = ("    part def 'Magnet System' :> 'CAS22.1.3 Magnet System' {\n" + mdoc + magnet_own
    + "        // the physical parts the magnet calcs price (WI-057)\n        part coil : 'Modular Coil';\n        part winding_pack : 'Winding Pack';\n        part casing : 'Coil Casing';\n    }\n")
cs = cs[:m.start()] + new_magnet + cs[m.end():]
cs = cs.replace("    private import economic_parameter::'CAS Scope';\n", "    private import economic_parameter::'CAS Scope';\n    private import mfe_magnet_parts::*;\n", 1)
# heating and divertor gain their facts
for defname, owner in (("Heating and CD", "heating"), ("Divertor", "divertor")):
    hdr = re.search(r"    part def '" + re.escape(defname) + r"' :> '[^']+' \{\n", cs)
    ins = "".join(reindent(moved[a], 0) for a in owner_attrs(owner))
    cs = cs[:hdr.end()] + f"        // WI-057: the {owner}'s own facts, moved from the plant (formerly plant-level inputs)\n" + ins + cs[hdr.end():]
CORE.write_text(cs)

# 2c. the costed subsystems gain their facts; the blanket gains the first wall
ss = SUBS.read_text()
ss = ss.replace("    private import economic_parameter::'CAS Scope';\n", "    private import economic_parameter::'CAS Scope';\n    private import mfe_radial_build_parts::*;\n", 1)
for defname, owner in (("Blanket", "blanket"), ("Shield", "shield"), ("Primary Structure", "structure"), ("Vacuum Vessel", "vessel"),
                       ("Power Supplies", "power_supplies"), ("Turbine Plant", "turbine"), ("Buildings", "buildings")):
    hdr = re.search(r"    part def '" + re.escape(defname) + r"' :> '[^']+' \{\n", ss); assert hdr, defname
    ins = "".join(reindent(moved[a], 0) for a in owner_attrs(owner))
    extra = "        // WI-057: the first wall is a part of the blanket module (the C220101 account prices both)\n        part first_wall : 'First Wall';\n" if owner == "blanket" else ""
    ss = ss[:hdr.end()] + (f"        // WI-057: the {owner}'s own facts, moved from the plant (formerly plant-level inputs)\n" if ins else "") + ins + extra + ss[hdr.end():]
SUBS.write_text(ss)

# ------------------------------------------------------------------ 3. plant: compose, nest, re-point
ps = ps.replace("    private import mfe_power_core::*;\n", "    private import mfe_power_core::*;\n    private import mfe_plasma::*;\n    private import mfe_magnet_parts::*;\n    private import mfe_radial_build_parts::*;\n    private import mfe_plant_systems::*;\n", 1)
ps = ps.replace("        part magnet : 'Magnet System' {\n",
    "        // WI-057: the plasma and the plant systems the calcs already model, as parts.\n        part plasma : 'Plasma';\n        part heat_transport : 'Primary Heat Transport';\n        part cryoplant : 'Cryoplant';\n        part fuel_cycle : 'Fuel Cycle';\n        part vacuum_pumping : 'Vacuum Pumping';\n        part magnet : 'Magnet System' {\n", 1)
ps = ps.replace("            :>> wp_side = wp_sizing.wp_side;\n", "            part :>> winding_pack {\n                :>> wp_side = wp_sizing.wp_side;\n            }\n")
ps = ps.replace("            :>> m_casing = casing_mass.m_casing;\n            :>> c_coil = coil_length.c_coil;\n",
                "            part :>> casing {\n                :>> m_casing = casing_mass.m_casing;\n            }\n            part :>> coil {\n                :>> c_coil = coil_length.c_coil;\n            }\n")
mapping = {}
for name, owner in home_of.items():
    if name in SUBSYS_OWN: continue
    if name in MAGNET_OWN_TODAY: continue
    mapping[name] = owner.replace(".", ".") + "." + name  # e.g. plasma.R, blanket.first_wall.firstwall_t
ps = rewrite_refs(ps, mapping)
for name in MAGNET_OWN_TODAY:
    owner = home_of.get(name, "magnet")
    if owner != "magnet": ps = re.sub(r"\bmagnet\." + name + r"\b", f"{owner}.{name}", ps)
PLANT.write_text(ps)

# ------------------------------------------------------------------ 4. instance: nest the bindings
ts = INST.read_text()
# 4a. the magnet block's sub-part blocks
mstart = ts.index("        part :>> magnet {\n"); mend = ts.index("        part :>> blanket {\n")
mblock = ts[mstart:mend]; msub = {"coil": [], "winding_pack": [], "casing": []}
for name in MAGNET_OWN_TODAY:
    owner = home_of.get(name, "magnet")
    if owner.startswith("magnet.") and re.search(r"^            :>> " + name + r" = ", mblock, re.M):
        stmt, mblock = take_binding(mblock, "            ", name); msub[owner.split(".")[1]].append(reindent(stmt, 4))
# 4b. top-level bindings of moved attributes -> per-owner statements
per_owner = {}
for name in moved:
    if re.search(r"^        :>> " + name + r" = ", ts, re.M):
        stmt, ts = take_binding(ts, "        ", name)
        per_owner.setdefault(home_of[name], []).append(stmt)
for sub in ("coil", "winding_pack", "casing"):
    for stmt in per_owner.pop(f"magnet.{sub}", []): msub[sub].append(reindent(stmt, 4))
for stmt in per_owner.pop("magnet", []):
    k = mblock.rindex("\n        }\n"); mblock = mblock[:k + 1] + reindent(stmt, 4) + mblock[k + 1:]
tail = "".join(f"            part :>> {sub} {{\n" + "".join(stmts) + "            }\n" for sub, stmts in msub.items() if stmts)
k = mblock.rindex("\n        }\n"); mblock = mblock[:k + 1] + tail + mblock[k + 1:]
ts = ts[:mstart] + mblock + ts[mend:]
# 4c. existing subsystem blocks receive their statements; the blanket receives the first wall
def append_into_block(text, part, stmts, nested=None):
    start = text.index(f"        part :>> {part} {{\n"); end = text.index("\n        }\n", start) + 1
    ins = "".join(reindent(s, 4) for s in stmts)
    if nested:
        ins += f"            part :>> {nested[0]} {{\n" + "".join(reindent(s, 8) for s in nested[1]) + "            }\n"
    return text[:end] + ins + text[end:]
for part in ("blanket", "shield", "structure", "vessel", "power_supplies", "turbine"):
    nested = ("first_wall", per_owner.pop("blanket.first_wall", [])) if part == "blanket" else None
    stmts = per_owner.pop(part, [])
    if stmts or nested: ts = append_into_block(ts, part, stmts, nested)
# 4d. new blocks for the parts the instance did not have, after the misc_plant block
new_blocks = ""
for part in ("plasma", "heating", "divertor", "heat_transport", "cryoplant", "fuel_cycle", "vacuum_pumping", "buildings"):
    stmts = per_owner.pop(part, [])
    if stmts: new_blocks += f"        part :>> {part} {{\n" + "".join(reindent(s, 4) for s in stmts) + "        }\n"
assert not per_owner, f"unplaced instance bindings: {per_owner.keys()}"
mstart = ts.index("        part :>> misc_plant {\n"); mend = ts.index("\n        }\n", mstart) + len("\n        }\n")
ts = ts[:mend] + "\n        // WI-057: the plasma, the plant systems and the remaining subsystems' own facts, nested on their parts.\n" + new_blocks + ts[mend:]
ts = rewrite_refs(ts, mapping)
INST.write_text(ts)
print("done: definitions written; plant re-pointed; instance nested. New magnet sub-blocks:", {k: len(v) for k, v in msub.items()})
