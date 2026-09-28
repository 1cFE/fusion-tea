"""WI-057 commit B: template calcs on the part definitions; EXPOSEs, inputs and the two magnet seams.

usage: transform_B_full.py <models_root> <lib_prefix> <calc_hosts.json> <report_out.json>
Runs on a commit-A tree. No calc def, constraint def, formula or value is touched.
"""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1]); LIB = sys.argv[2]; hosts = json.loads(Path(sys.argv[3]).read_text()); report_out = Path(sys.argv[4])
PLANT = root / "designs/generic_mfe/mfe_plant.sysml"; SUBS = root / "designs/generic_mfe/mfe_subsystems.sysml"
CORE = root / f"{LIB}cost_structure/mfe_power_core.sysml"; INST = root / "designs/stellarator_09/stellarator_plant.sysml"
STRUCT = root / f"{LIB}structure"; ANALYSES = root / f"{LIB}analyses"
DEF_OF = {"plasma": ("Plasma", STRUCT / "mfe_plasma.sysml"), "blanket": ("Blanket", SUBS), "blanket.first_wall": ("First Wall", STRUCT / "mfe_radial_build_parts.sysml"),
          "shield": ("Shield", SUBS), "structure": ("Primary Structure", SUBS), "vessel": ("Vacuum Vessel", SUBS), "magnet": ("Magnet System", CORE),
          "heat_transport": ("Primary Heat Transport", STRUCT / "mfe_plant_systems.sysml"), "turbine": ("Turbine Plant", SUBS), "electric_plant": ("Electric Plant", SUBS),
          "power_supplies": ("Power Supplies", SUBS), "cryoplant": ("Cryoplant", STRUCT / "mfe_plant_systems.sysml"), "heating": ("Heating and CD", CORE), "divertor": ("Divertor", CORE),
          "fuel_cycle": ("Fuel Cycle", STRUCT / "mfe_plant_systems.sysml"), "vacuum_pumping": ("Vacuum Pumping", STRUCT / "mfe_plant_systems.sysml"), "buildings": ("Buildings", SUBS),
          "heat_rejection": ("Heat Rejection", SUBS), "misc_plant": ("Miscellaneous Plant", SUBS)}
PLANT_DEF = "MFE Power Plant"
SEAMS = {"magnet": {"winding_cost": "winding_pack_cost.cost", "structure_cost": "magnet_structure_cost.cost"}}
SEAM_REWRITE = {("magnet_capital_rollup", "winding_cost"): "'Magnet System'::winding_cost", ("magnet_capital_rollup", "structure_cost_in"): "structure_cost"}
EXPOSE_RENAME = {("magnet_cost", "capital_cost"): "capital_cost_1cfe"}
host_of = {c: h for h, cs in hosts.items() if not h.startswith("_") and h != "plant" for c in cs}
plant_calcs = set(hosts["plant"])
part_usages = set(DEF_OF)  # usage names on the plant (dotted for first_wall)
# calc def -> package
pkg_of_def = {}
for f in ANALYSES.glob("*.sysml"):
    pkg = re.search(r"^package (\w+)", f.read_text(), re.M).group(1)
    for name in re.findall(r"calc def '([^']+)'", f.read_text()): pkg_of_def[name] = pkg

def take_block(text, header_re):
    m = re.search(header_re, text, re.M); assert m, header_re
    start = m.start()
    while True:
        prev = text.rfind("\n", 0, start - 1) + 1; line = text[prev:start]
        if line.strip().startswith("//") and prev < start: start = prev
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

def def_attrs(text, defname):
    m = re.search(r"    part def '" + re.escape(defname) + r"'[^\n]*\{\n(.*?)\n    \}\n", text, re.S); assert m, defname
    return set(re.findall(r"^\s{8}attribute (\w+)\s*:", m.group(1), re.M)) | set(re.findall(r"^\s{8}:>> (\w+)\s*=", m.group(1), re.M))

files = {p: p.read_text() for p in {PLANT, SUBS, CORE, INST, *[v[1] for v in DEF_OF.values()]}}
plant_expose = dict(re.findall(r"^        attribute (\w+) : Real = ([a-z_0-9]+\.[A-Za-z_0-9]+);", files[PLANT], re.M))

# ---------------------------------------------------------------- 1. cut the hosted calcs from the plant
ps = files[PLANT]; blocks = {}
for calc, host in host_of.items():
    blk, ps = take_block(ps, r"^        calc " + calc + r" : '[^']+' \{"); blocks[calc] = blk
print("calcs cut from the plant:", len(blocks))

# ---------------------------------------------------------------- 2. classify every binding
inputs = {h: {} for h in DEF_OF}          # host -> {input name: plant bind expr}
exposes = {h: {} for h in DEF_OF}         # host -> {expose name: producer expr inside the def}
reexpose_blanket = {}                     # first-wall outputs re-exposed on the blanket
own_attrs = {h: def_attrs(files[DEF_OF[h][1]], DEF_OF[h][0]) for h in DEF_OF}
def expose_name(calc, out):
    if (calc, out) in EXPOSE_RENAME: return EXPOSE_RENAME[(calc, out)]
    if out == "cost": return f"{calc}_cost"
    return out
def consumer_path_for(calc, out):
    """How anything OUTSIDE the host reads calc.out after commit B (and the EXPOSEs it needs)."""
    h = host_of[calc]; name = expose_name(calc, out)
    exposes[h][name] = f"{calc}.{out}"
    if h == "blanket.first_wall":
        reexpose_blanket[name] = f"first_wall.{name}"; return f"blanket.{name}", name
    return f"{h}.{name}", name

def rewrite_block(calc, blk):
    host = hosts_host = host_of[calc]; defname = DEF_OF[host][0]
    def repl(m):
        formal, rhs = m.group(1), m.group(2).strip()
        if (calc, formal) in SEAM_REWRITE: return f"in {formal} = {SEAM_REWRITE[(calc, formal)]};"
        if re.fullmatch(r"[-+]?\d[\d.eE+-]*", rhs): return m.group(0)
        segs = rhs.split(".")
        if rhs.startswith(host + "."):            # own attribute (possibly on a sub-part)
            rest = rhs[len(host) + 1:]
            if "." in rest: return f"in {formal} = {rest};"
            return f"in {formal} = {(chr(39) + defname + chr(39) + '::' + rest) if rest == formal else rest};"
        a = segs[0]
        if a in host_of and host_of[a] == host: return m.group(0)          # sibling calc on the same definition
        if len(segs) == 1:                                                   # bare plant attribute
            name = a
            if name not in own_attrs[host]:
                inputs[host][name] = plant_expose.get(name, f"'{PLANT_DEF}'::{name}")
            return f"in {formal} = {(chr(39) + defname + chr(39) + '::' + name) if name == formal else name};"
        if a in host_of:                                                     # a calc hosted on another part
            path, name = consumer_path_for(a, segs[1])
            inputs[host][name] = path
            return f"in {formal} = {(chr(39) + defname + chr(39) + '::' + name) if name == formal else name};"
        if a in plant_calcs:                                                 # a plant calc's output
            name = segs[1]
            if name not in own_attrs[host]: inputs[host][name] = rhs
            return f"in {formal} = {(chr(39) + defname + chr(39) + '::' + name) if name == formal else name};"
        if a in part_usages or ".".join(segs[:2]) in part_usages:            # another part's attribute
            name = segs[-1]
            assert name not in own_attrs[host], (calc, rhs, "collides with an own attribute")
            inputs[host][name] = rhs
            return f"in {formal} = {(chr(39) + defname + chr(39) + '::' + name) if name == formal else name};"
        raise AssertionError(f"unclassified binding in {calc}: {formal} = {rhs}")
    return re.sub(r"in (\w+) = ([^;]+);", repl, blk)

rewritten = {c: rewrite_block(c, b) for c, b in blocks.items()}

# ---------------------------------------------------------------- 3. plant usages: moved :>> lines, new input binds
moved_redefs = {h: [] for h in DEF_OF}   # host -> statements to place inside the definition (incl. nested sub-part blocks)
def edit_usage(ps, usage_re, host):
    m = re.search(usage_re, ps, re.M); assert m, usage_re
    i = ps.index("{", m.start()) if ps[m.end() - 2] == "{" or "{" in ps[m.start():m.end()] else None
    return m, i
for host in DEF_OF:
    if "." in host: continue
    m = re.search(r"^        part " + host + r" : '[^']+'( \{\n|;\n)", ps, re.M); assert m, host
    if m.group(1) == ";\n":
        body = ""; start, end = m.start(), m.end()
        header = ps[m.start():m.end() - 2] + " {\n"
    else:
        start = m.start(); end = ps.index("\n        }\n", start) + len("\n        }\n")
        header = ps[m.start():m.end()]; body = ps[m.end():end - len("        }\n")]
    # nested sub-part blocks (magnet): their :>> of hosted calcs move into the definition's sub-part usage
    nested = {}
    def sub_repl(mm):
        sub, inner = mm.group(1), mm.group(2)
        kept = []; pending = []
        for line in inner.splitlines(True):
            m2 = re.match(r"\s*:>> (\w+) = ([a-z_0-9]+)\.(\w+);", line)
            if m2 and m2.group(2) in host_of and host_of[m2.group(2)] == host:
                nested.setdefault(sub, []).extend(reindent(x, -4) for x in pending); pending = []
                nested.setdefault(sub, []).append(f"            :>> {m2.group(1)} = {m2.group(2)}.{m2.group(3)};\n")
            elif line.strip().startswith("//"): pending.append(line)
            else: kept.extend(pending); pending = []; kept.append(line)
        kept.extend(pending)
        return (f"            part :>> {sub} {{\n" + "".join(kept) + "            }\n") if "".join(kept).strip() else ""
    body = re.sub(r"            part :>> (\w+) \{\n(.*?)            \}\n", sub_repl, body, flags=re.S)
    for sub, stmts in nested.items(): moved_redefs[host].append(("__sub__", sub, stmts))
    # flat statements inside the usage that read a calc now hosted on this part move into the definition,
    # with the comment lines immediately above them
    keep = []; pending = []
    for stmt in re.split(r"(?<=\n)", body):
        if not stmt.strip(): keep.extend(pending); pending = []; keep.append(stmt); continue
        mm = re.match(r"\s*:>> (\w+) = ([a-z_0-9]+)\.(\w+);", stmt)
        if mm and mm.group(2) in host_of and host_of[mm.group(2)] == host:
            moved_redefs[host].append(("__own__", mm.group(1), f"{mm.group(2)}.{mm.group(3)}", [reindent(x, -4) for x in pending])); pending = []; continue
        if stmt.strip().startswith("//") and not stmt.strip().startswith("// WI-057"): pending.append(stmt); continue
        keep.extend(pending); pending = []; keep.append(stmt)
    keep.extend(pending)
    body = "".join(keep)
    # the plant wires this part's inputs
    binds = "".join(f"            :>> {n} = {e};\n" for n, e in sorted(inputs[host].items()))
    fw = inputs.get("blanket.first_wall", {}) if host == "blanket" else {}
    fw_block = ("            part :>> first_wall {\n" + "".join(f"                :>> {n} = {e};\n" for n, e in sorted(fw.items())) + "            }\n") if fw else ""
    comment = "            // WI-057: inputs the plant wires from the parts and calcs that produce them\n" if (binds or fw_block) else ""
    ps = ps[:start] + header + body + comment + binds + fw_block + "        }\n" + ps[end:]

# ---------------------------------------------------------------- 4. plant-level consumers read the EXPOSEs
def rewrite_consumers(text):
    def repl(m):
        calc, out = m.group(1), m.group(2)
        if calc in host_of:
            path, _ = consumer_path_for(calc, out); return path
        return m.group(0)
    return re.sub(r"(?<![\w.])([a-z_0-9]+)\.([A-Za-z_0-9]+)(?![\w(])", repl, text)
def rewrite_outside_docs(text, fn):
    out = []; in_doc = False
    for ln in text.splitlines(True):
        st = ln.strip()
        if in_doc:
            out.append(ln); in_doc = "*/" not in st; continue
        if st.startswith("doc /*") or st.startswith("/*"):
            out.append(ln); in_doc = "*/" not in st; continue
        if st.startswith("//"): out.append(ln); continue
        code, sep, comment = ln.partition("//")
        out.append(fn(code) + sep + comment)
    return "".join(out)
ps = rewrite_outside_docs(ps, rewrite_consumers)
files[PLANT] = ps
files[INST] = rewrite_outside_docs(files[INST], rewrite_consumers)

# ---------------------------------------------------------------- 5. write the definitions
imports_needed = {}
for calc, blk in rewritten.items():
    defn = re.search(r"calc \w+ : '([^']+)'", blk).group(1); host = host_of[calc]
    imports_needed.setdefault(DEF_OF[host][1], set()).add(pkg_of_def[defn])
for host, (defname, path) in DEF_OF.items():
    text = files[path]
    m = re.search(r"    part def '" + re.escape(defname) + r"'[^\n]*\{\n", text); assert m, defname
    close = text.index("\n    }\n", m.end()) + 1
    parts = []
    if inputs[host]:
        parts.append("        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----\n")
        for n, e in sorted(inputs[host].items()): parts.append(f"        attribute {n} : Real;   // <- {e}\n")
    if exposes[host] or (host == "blanket" and reexpose_blanket) or host in SEAMS:
        parts.append("        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----\n")
        for n, e in sorted(exposes[host].items()): parts.append(f"        attribute {n} : Real = {e};\n")
        if host == "blanket":
            for n, e in sorted(reexpose_blanket.items()): parts.append(f"        attribute {n} : Real = {e};   // the first wall's, re-exposed\n")
        for n, e in SEAMS.get(host, {}).items():
            parts.append(f"        // SWAP SEAM: declared `default` so a variant definition may point it at its own calc (design D5, D9)\n        attribute {n} : Real default {e};\n")
    for item in moved_redefs[host]:
        if isinstance(item, tuple) and item[0] == "__own__":
            _, name, expr, comments = item
            decl = re.search(r"^        attribute " + name + r" : Real;\n", text[m.start():close], re.M)
            if decl:  # the definition's own attribute: the value goes on the declaration (a :>> of an owned feature is not legal)
                seg = text[m.start():close].replace(decl.group(0), "".join(comments) + f"        attribute {name} : Real = {expr};\n", 1)
                text = text[:m.start()] + seg + text[close:]; close = text.index("\n    }\n", m.end()) + 1
            else:      # inherited (capital_cost from 'Costed Component'): redefine it
                parts.append("".join(comments) + f"        :>> {name} = {expr};\n")
            continue
        if isinstance(item, tuple):
            _, sub, stmts = item
            # the sub-part usage gains a body
            text_sub = re.search(r"        part " + sub + r" : '[^']+';\n", text[m.start():close])
            assert text_sub, (host, sub)
            new_sub = text_sub.group(0)[:-2] + " {\n" + "".join(stmts) + "        }\n"
            text = text[:m.start()] + text[m.start():close].replace(text_sub.group(0), new_sub) + text[close:]
            close = text.index("\n    }\n", m.end()) + 1
        else: parts.append(item)
    if any(c for c in host_of if host_of[c] == host):
        parts.append("        // ---- template calcs (WI-057): the analyses this part owns ----\n")
        for calc in hosts[host]: parts.append(reindent(rewritten[calc], 0))
    text = text[:close] + "".join(parts) + text[close:]
    files[path] = text
for path, pkgs in imports_needed.items():
    text = files[path]; pkgname = re.search(r"^package (\w+)", text, re.M).group(1)
    for pkg in sorted(pkgs):
        if pkg == pkgname or re.search(r"^    private import " + pkg + r"::", text, re.M): continue
        text = text.replace("    private import ScalarValues::*;\n", f"    private import ScalarValues::*;\n    private import {pkg}::*;\n", 1)
    files[path] = text
for p, t in files.items(): p.write_text(t)
report = {"calcs_moved": len(blocks), "inputs": {h: v for h, v in inputs.items() if v}, "exposes": {h: v for h, v in exposes.items() if v},
          "reexposed_on_blanket": reexpose_blanket, "moved_redefinitions": {h: [f"{x[0]} {x[1]}" for x in v] for h, v in moved_redefs.items() if v},
          "imports_added": {str(k): sorted(v) for k, v in imports_needed.items()}}
report_out.write_text(json.dumps(report, indent=1))
print("inputs:", {h: len(v) for h, v in inputs.items() if v}); print("exposes:", {h: len(v) for h, v in exposes.items() if v}); print("re-exposed on blanket:", sorted(reexpose_blanket))
