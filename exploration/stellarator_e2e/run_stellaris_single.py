"""Single-pass stellarator runner (Item 10 cutover) — NO bridge, NO two-pass rollup glue.

The cross-part capital rollup (powercore/bop/direct/total_capital) is now compiled by codegen
as instance-scoped aggregation producers, so a single teax-simkit pass computes it in the graph.
glue-1 (patch_bop_wiring) is kept; glue-2 (the Python rollup + placeholder overwrite) is retired
with bridge_v11_generate.py. special_materials_capital (CAS27 pass-through, a declared plain
design input) is harness-supplied. Anchors verified bit-exact vs oracle (rel<1e-9); five verdicts
all satisfied.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, "/home/reid/1cfe/teax/packages/teax-simkit")
sys.path.insert(0, ".")
import run_stellaris as rs
from verify_stellaris import compute as oracle_compute
from simkit.core.pipeline import execute_pipeline
from simkit.io.output_router import WriteHandler, create_output_router_with_json_schemas
from stellarator_tea import CUSTOM_SCHEMA_TYPES, create_stellarator_tea_registry

rs.patch_bop_wiring()  # glue-1 (kept); NO rollup glue-2, single pass
o = oracle_compute()
special = o["special_materials"]
# Inject the leaf design inputs surfaced as per-module entry points (WI-028: the
# rebuilt overnight assembly consumes special_materials_capital in both
# cas2x_pre_contingency and cas23_to_28_capital, and cas28_capital likewise;
# each surfaces as its own module-scoped entry point). CAS27 special materials is
# the harness-supplied pass-through; CAS28 digital twin is the 5.0 M$ constant.
CAS28_CAPITAL = 5_000_000.0  # costing_constants.yaml:229 (digital_twin 5.0 M$) x 1e6
# WI-029: the CAS72 replaceable-account aggregation carries a plant-level n_mod
# LocalTerm that codegen cannot resolve inside an aggregation, so it surfaces as
# a NULL entry point (the WI-028 I7 class). Fill it with the plant's own value —
# mfe_plant.sysml:328 `attribute n_mod : Real default 1.0`, the single-module
# demo. Value-preserving: it restores the declared default, it does not choose one.
N_MOD = 1.0
for f in Path("generated/inputs").glob("*.json"):
    d = json.loads(f.read_text())
    changed = False
    for k in list(d):
        if k.endswith("__special_materials_capital"): d[k] = special; changed = True
        elif k.endswith("__cas28_capital"): d[k] = CAS28_CAPITAL; changed = True
        elif k == "stellarator_09__stellaris__replacement_cost_per_event__n_mod":
            d[k] = N_MOD; changed = True
    if changed:
        f.write_text(json.dumps(d, indent=2)); print(f"[inject] special_materials={special:,.2f}, cas28={CAS28_CAPITAL:,.2f} into {f.name}")

# CONSTRAINT-EXEC (WI-027 adapter 1): the generated CUSTOM_SCHEMA_TYPES already carry
# ConstraintEvaluation + ConstraintReport, so registering write handlers for every
# CUSTOM_SCHEMA_TYPES name registers the constraint exit-point handlers generically —
# no per-type hand wiring. Without them PipelineValidator would reject the constraint run.
schema_names = dict.fromkeys(["RootModel[float]"] + [t.__name__ for t in CUSTOM_SCHEMA_TYPES])
router = create_output_router_with_json_schemas(list(schema_names))
router.register_handler("float", WriteHandler(fn=lambda v,p: Path(p).write_text(json.dumps(v)), extension=".json"))
result = execute_pipeline(rs.PIPELINE, output_dir=rs.E2E/"outputs"/"single",
    registry=create_stellarator_tea_registry(), output_router=router, custom_schema_types=CUSTOM_SCHEMA_TYPES)
out = result.outputs
# CONSTRAINT-EXEC (WI-027 adapter 2): oracle-comparison map keeps ONLY scalar channels;
# the two non-scalar verdict channels (ConstraintEvaluation/ConstraintReport) are skipped,
# so MR-5.1 bit-exactness on numeric channels is exactly as it was — verdicts are not numbers.
b = {c:(float(v.root) if hasattr(v,'root') else float(v)) for c,v in out.items() if hasattr(v,'root') or isinstance(v,(int,float))}
P, CH = rs.P, rs.CH
total = b[f"{P}total_capital__total_capital"]; magnet = b[CH["magnet"]]
# WI-029 re-baseline (MR-WI029-9): total_capital/LCOE/magnet-share MOVE again,
# for EXACTLY TWO causes and no third:
#   1. The annual-cost side enters the LCOE numerator. CAS71 (levelized O&M)
#      + CAS72 (levelized scheduled replacement) + CAS80 (levelized fuel)
#      replace the unlevelized WI-025 O&M line: +17.498627 $/MWh.
#   2. The CAS10 error fix takes exactly $16,000,000.00 off total_capital
#      (precon_fixed_base 32M -> 16M, FOAK plant_studies 20 -> NOAK 4):
#      16,145,706,216.04 -> 16,129,706,216.04, i.e. -0.248047 $/MWh.
#   Sum +17.250580 $/MWh = the observed 258.013640 -> 275.264220 exactly.
# There is NO multiplier-swap component: under the ruled Option (ii) the
# headline convention is unchanged (idc_factor untouched, total_capital ==
# overnight_capital). The 1cfe-form comparison channel is reported alongside
# and is NOT the design-point headline.
# p_net/q_eng/rec_frac (the physics spine) are UNCHANGED, as they must be.
# Authoritative gate is bit-exact vs oracle below.
anchors = [("total capital $",total,16_129_706_216.04),("LCOE $/MWh",b[CH["lcoe"]],275.264220),
    ("p_net MW",b[CH["p_net"]],915.081088),("q_eng",b[CH["q_eng"]],6.606662),
    ("rec_frac",b[CH["rec_frac"]],0.151362),("magnet %",magnet/total*100,39.203876),
    # WI-029 additions to the recorded headline: the annual-cost side and the
    # Option-(ii) comparison channel (reported, NOT the headline).
    ("CAS70 $/yr",b[CH["cas70"]],170_974_516.955938),
    ("CAS80 $/yr",b[CH["cas80"]],773_037.517724),
    ("lcoe_1cfe $/MWh (comparison)",b[CH["lcoe_1cfe"]],269.861538)]
print("\n=== SIX ANCHORS (single-pass, graph rollup, no bridge) ===")
allok=True
for name,val,exp in anchors:
    # Recorded anchors are truncated to their printed precision; the authoritative
    # gate is BIT-EXACT vs oracle below. Here compare at the recorded precision.
    ok = (abs(val-exp)<0.01) if name=="magnet %" else (abs(round(val,6)-exp)<=1e-6 or abs(val-exp)/abs(exp)<1e-6)
    allok &= ok
    print(f"  {name:16s} exec={val:20.6f}  expect={exp:<18}  {'OK' if ok else '*** DEVIATION'}")
print(f"  magnet capital $ = {magnet:,.2f}")
# CONSTRAINT-EXEC (WI-027 adapter 3): harvest the generated ConstraintReport into the run
# report and assert verdict PARITY against the static expected set (design §Decision 6).
# This is a string-equality regression check on the model's own reported status — NOT a
# physics comparison: no operand-vs-bound test appears here (MR-WI027-2). The verdict source
# is the generated ConstraintReport; a non-satisfied verdict is a demo finding to surface
# (MR-WI027-4), never tuned away.
EXPECTED_VERDICTS = {  # design-point actuals table — all five satisfied, none on a boundary
    "beta_ok": "satisfied", "net_positive": "satisfied", "recirc_ok": "satisfied",
    "tbr_ok": "satisfied", "wall_load_ok": "satisfied",
}
report = out["constraint_report"]
print("=== FIVE VERDICTS (generated ConstraintReport) ===")
verdicts = {}
for c,v in out.items():
    if c.endswith('__evaluation') and hasattr(v,'status'):
        name = c.split("__")[2]
        verdicts[name] = v.status
        print(f"  {name:14s} {v.status}")
assert report.headline == "all_satisfied", f"headline {report.headline!r} != all_satisfied"
assert report.assessed_count == 5, f"assessed_count {report.assessed_count} != 5"
for name, exp in EXPECTED_VERDICTS.items():
    got = verdicts.get(name)
    assert got == exp, f"VERDICT PARITY FAIL: {name} = {got!r}, expected {exp!r} (surface per MR-WI027-4)"
print(f"VERDICT PARITY: PASS — headline={report.headline}, assessed_count={report.assessed_count}, all five == satisfied")
print("ANCHORS", "GREEN" if allok else "*** STOP — DEVIATION ***")

# --- Bit-exact oracle comparison (WI-027 standard: rel dev < 1e-9) ---
print("\n=== BIT-EXACT vs ORACLE (rel<1e-9) ===")
omap = {"total_capital":total, "lcoe":b[CH["lcoe"]], "p_net":b[CH["p_net"]],
        "q_eng":b[CH["q_eng"]], "rec_frac":b[CH["rec_frac"]],
        "cas20_capital":b[f"{P}cas20_capital__cas20_capital"],
        "overnight_capital":b[f"{P}overnight_capital__overnight_capital"],
        # WI-029: the annual-cost side and the Option-(ii) comparison channels.
        # cas72_annual is the CAS72 HANDWRITTEN RUNG vs its independent oracle
        # mirror — this row is the rel-1e-9 impl-vs-mirror gate (design MF-1).
        "cas71_annual":b[CH["cas71"]], "cas72_annual":b[CH["cas72"]],
        "cas70_annual":b[CH["cas70"]], "cas80_annual":b[CH["cas80"]],
        "annual_fuel":b[CH["annual_fuel"]],
        "cas90_1cfe":b[CH["cas90_1cfe"]], "lcoe_1cfe":b[CH["lcoe_1cfe"]]}
bit=True
for k,val in omap.items():
    exp=o[k]; rd=abs(val-exp)/(abs(exp) or 1); ok=rd<1e-9; bit&=ok
    print(f"  {k:16s} exec={val:20.9f} oracle={exp:20.9f} reldev={rd:.2e} {'OK' if ok else 'FAIL'}")
print("BIT-EXACT vs oracle:", "PASS" if bit else "*** FAIL ***")


# --- WI-029: CAS72 handwritten rung vs its oracle mirror, and the GUARD-LIVE
# spot-check. The impl is imported here only to CALL it on synthetic inputs;
# the mirror in verify_stellaris.py is an independent statement of the chain,
# so the comparison is not vacuous. Guards that never bind are decoration —
# these two cases drive them live and prove they are structural.
from stellarator_tea.handwritten.mfe_account_costs.levelized_replacement_cost_impl import (
    levelized_replacement_cost as _cas72_impl,
)
from verify_stellaris import _oracle_levelized_replacement_cost as _cas72_mirror

print("\n=== WI-029 CAS72 GUARD-LIVE SPOT-CHECK (impl vs oracle mirror, rel<1e-9) ===")
GUARD_CASES = [
    # (label, kwargs, which guard must bind)
    ("clip CAP binds (low wall loading, high fluence limit)",
     dict(cost_per_event=671_160_000.0, p_fus=100.0, ash_frac=0.2002275312855518,
          firstwall_area=660.0791423448563, fluence_limit=500.0, availability=0.9,
          interest_rate=0.07, operational_years=30.0),
     "core_lifetime_fpy == operational_years * availability"),
    ("clip FLOOR binds (extreme wall loading) -> n_rep = 53, cost nonzero",
     dict(cost_per_event=671_160_000.0, p_fus=200_000.0, ash_frac=0.2002275312855518,
          firstwall_area=660.0791423448563, fluence_limit=18.0, availability=0.9,
          interest_rate=0.07, operational_years=30.0),
     "core_lifetime_fpy == 0.5 (floor), n_rep = 53"),
    ("outer max binds (replacement interval >= plant life -> n_rep = 0)",
     dict(cost_per_event=671_160_000.0, p_fus=50.0, ash_frac=0.2002275312855518,
          firstwall_area=660.0791423448563, fluence_limit=18.0, availability=0.9,
          interest_rate=0.07, operational_years=5.0),
     "n_rep == 0 (cost == 0)"),
]
guards_ok = True
for label, kw, expect in GUARD_CASES:
    a = _cas72_impl(**kw); m = _cas72_mirror(**kw)
    rd = abs(a - m) / (abs(m) or 1.0)
    ok = rd < 1e-9
    guards_ok &= ok
    print(f"  {label}")
    print(f"    expect: {expect}")
    print(f"    impl={a:,.6f}  mirror={m:,.6f}  reldev={rd:.2e} {'OK' if ok else '*** FAIL'}")
# The cap case must actually saturate, and the n_rep case must actually zero.
_cap_kw = GUARD_CASES[0][1]
_pn = _cap_kw["p_fus"] * (1 - _cap_kw["ash_frac"]); _qn = _pn / _cap_kw["firstwall_area"]
_raw = _cap_kw["fluence_limit"] / max(_qn, 1e-6)
_cap = _cap_kw["operational_years"] * _cap_kw["availability"]
assert _raw > _cap, f"clip cap case does not saturate: raw {_raw} <= cap {_cap}"
print(f"    [guard live] raw FPY {_raw:.3f} > cap {_cap:.3f} -> clip BINDS")
_flo_kw = GUARD_CASES[1][1]
_fpn = _flo_kw["p_fus"] * (1 - _flo_kw["ash_frac"]); _fqn = _fpn / _flo_kw["firstwall_area"]
_fraw = _flo_kw["fluence_limit"] / max(_fqn, 1e-6)
assert _fraw < 0.5, f"clip floor case does not bind: raw {_fraw} >= 0.5"
assert _cas72_impl(**_flo_kw) > 0.0, "clip floor case returned 0 — not a live comparison"
print(f"    [guard live] raw FPY {_fraw:.5f} < floor 0.500 -> clip FLOOR BINDS, cost nonzero")
assert _cas72_impl(**GUARD_CASES[2][1]) == 0.0, "outer max case did not return 0"
print("    [guard live] n_rep floored to 0 -> cost exactly 0.0 -> outer max BINDS")
print("GUARD-LIVE SPOT-CHECK:", "PASS" if guards_ok else "*** FAIL ***")
