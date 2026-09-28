"""Prototype Stage B (on top of Stage A): the thirteen magnet calcs move under `part magnet`,
with their cross-boundary outputs surfaced as EXPOSE attributes on 'Magnet System'.

usage: proto_transform_B.py <models_root> <movemap.json (updated in place)>
"""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1]); mm_path = Path(sys.argv[2])
MAGNET_CALCS = ["field_calc", "peak_field_calc", "stored_energy", "casing_mass", "wp_sizing", "coil_length",
                "wp_volume", "wp_stress", "cond_strain", "magnet_cost", "winding_pack_cost",
                "magnet_structure_cost", "magnet_capital_rollup"]
# calc output consumed outside the magnet -> EXPOSE attribute on the magnet
EXPOSES = {"peak_field_calc.B_peak": "B_peak", "wp_stress.sigma_wp": "sigma_wp",
           "cond_strain.eps_cond": "eps_cond", "wp_volume.vol_cold_total": "vol_cold_total",
           "magnet_cost.capital_cost": "capital_cost_1cfe"}

def take_block(text, header_re):
    m = re.search(header_re, text, re.M)
    assert m, header_re
    # include preceding // comment lines
    start = m.start()
    while True:
        prev = text.rfind("\n", 0, start - 1)
        line = text[prev + 1:start]
        if line.strip().startswith("//"):
            start = prev + 1
        else:
            break
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
    return "".join((" " * delta + ln if ln.strip() else ln) for ln in stmt.splitlines(True))

# ---- library: EXPOSE attributes on the magnet def --------------------------------------
lib = root / "cost_structure/mfe_power_core.sysml"
s = lib.read_text()
anchor = "        part coil : 'Modular Coil';\n"
assert anchor in s
exposes = "".join(f"        // WI-057 prototype EXPOSE: {src} surfaced at the part boundary\n        attribute {name} : Real;\n" for src, name in EXPOSES.items())
s = s.replace(anchor, exposes + anchor)
lib.write_text(s)

# ---- plant: cut the calcs, nest them, bind the EXPOSEs, re-point outside consumers -------
plant = root / "designs/generic_mfe/mfe_plant.sysml"
ps = plant.read_text()
blocks = []
for name in MAGNET_CALCS:
    blk, ps = take_block(ps, r"^        calc " + name + r" : '[^']+' \{")
    # inside the magnet: the sub-part references drop the `magnet.` prefix; `magnet.B`/`magnet.r_coil` keep it (self-named formals)
    blk = re.sub(r"\bmagnet\.(coil|winding_pack|casing)\.", r"\1.", blk)
    blocks.append(reindent(blk, 4))
# outside consumers (the calcs are cut out of ps at this point) read the EXPOSEs
for src, name in EXPOSES.items():
    ps = ps.replace(f"= {src};", f"= magnet.{name};")
expose_binds = "".join(f"            :>> {name} = {src};\n" for src, name in EXPOSES.items())
magnet_open = "        part magnet : 'Magnet System' {\n"
k = ps.index(magnet_open); close = ps.index("\n        }\n", k) + 1
ps = ps[:close] + "            // WI-057 prototype: the magnet's own calcs live on the magnet.\n" + "".join(blocks) + expose_binds + ps[close:]
plant.write_text(ps)

mm = json.loads(mm_path.read_text())
mm["__calcs__"] = {c: "magnet" for c in MAGNET_CALCS}
mm["__exposes__"] = {f"magnet__{v}": f"magnet__{k.replace('.', '__')}" for k, v in EXPOSES.items()}
mm_path.write_text(json.dumps(mm, indent=1, sort_keys=True))
print("nested", len(blocks), "calcs under magnet; exposes:", list(EXPOSES.values()))
