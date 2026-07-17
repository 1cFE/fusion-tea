"""WI-018 stellarator end-to-end: generated SysML -> teax -> LCOE + CAS breakdown.

Executes the generated Stellaris (concept-09) pipeline through the teax executor
and checks every channel against the pure-Python oracle (verify_stellaris.py,
which mirrors the SysML calc defs line-for-line) and the WI-018 headline numbers.

What is generated code vs harness glue (all glue is loudly labeled):

  GENERATED + EXECUTED under teax (single generated package, from the SysML):
    - physics spine: Plasma Geometry (V), DT Fusion Power (p_fus),
      MFE Power Balance (p_th/p_the/p_et/q_eng/rec_frac/p_net)
    - every per-account cost module: magnet, heating, divertor, blanket, shield,
      structure, vessel, power_supplies, turbine, electric, heat_rejection, misc
    - contingency, indirect, and the LCOE DCF core

  HARNESS GLUE (the cross-part edges sysml-codegen cannot wire, per findings):
    1. BOP power wiring (NEW finding): the 4 Linear_Power_Cost accounts bind
       `in power = p_the/p_et/p_th` (calc input name != alias name), so the
       cost-spine alias -> pb-output edge is not formed and codegen emits a
       dangling `mfe_plant__MFE_Power_Plant__p_*` schema field. We repoint those
       4 inputs to the real pb output channels in the emitted YAML (single-pass
       wiring closure). The volume-scaled accounts (which bind `in p_th = p_th`)
       wire correctly via the self-named rescue and need no patch.
    2. Capital rollup (WI-015 finding 4): powercore/bop/direct/total sum each
       subsystem capital_cost across parts (feature-chain in a CalcDef output),
       which codegen cannot compile. We sum the generated per-account module
       outputs in Python and feed direct/total back through the emitted input
       JSON, then re-run so the generated contingency/indirect/LCOE modules
       produce the final numbers. Only the additions are harness code.

Run:  cd .../exploration/stellarator_e2e && \
      /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py
"""

import json
import sys
from pathlib import Path

E2E = Path(__file__).parent
sys.path.insert(0, str(E2E))
from verify_stellaris import compute as oracle_compute  # noqa: E402

# Make the generated package importable as `stellarator_tea`.
pkg_dir = E2E / "pkg"
pkg_dir.mkdir(exist_ok=True)
link = pkg_dir / "stellarator_tea"
if not link.exists():
    link.symlink_to(E2E / "generated")
sys.path.insert(0, str(pkg_dir))

from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    WriteHandler,
    create_output_router_with_json_schemas,
)

from stellarator_tea import CUSTOM_SCHEMA_TYPES, create_stellarator_tea_registry  # noqa: E402
from stellarator_tea.handwritten.mfe_account_costs.contingency_cost_impl import (  # noqa: E402
    run_contingency_cost,
)
from stellarator_tea.handwritten.mfe_account_costs.indirect_cost_impl import (  # noqa: E402
    run_indirect_cost,
)
from stellarator_tea.modules.mfe_account_costs.contingency_cost import Contingency_CostInput  # noqa: E402
from stellarator_tea.modules.mfe_account_costs.indirect_cost import Indirect_CostInput  # noqa: E402

GEN = E2E / "generated"
PIPELINE = GEN / "pipelines" / "mfe_stellarator.yaml"
MFE_PARAMS = GEN / "inputs" / "mfe_plant_params.json"
SYS_DESIGN = GEN / "inputs" / "system_design.json"
REL_TOL = 1e-9  # generated arithmetic vs oracle; expect bit-exact

P = "stellarator_09__stellaris__"

# Channel names (from the emitted pipeline YAML).
CH = dict(
    V=f"{P}geom__V", p_fus=f"{P}fusion__p_fus", wall_load=f"{P}wall_load_calc__wall_load",
    p_th=f"{P}pb__p_th", p_the=f"{P}pb__p_the", p_et=f"{P}pb__p_et",
    q_eng=f"{P}pb__q_eng", rec_frac=f"{P}pb__rec_frac", p_net=f"{P}pb__p_net",
    magnet=f"{P}magnet_cost__capital_cost", heating=f"{P}heating_cost__cost",
    divertor=f"{P}divertor_cost__cost", blanket=f"{P}blanket_cost__cost",
    shield=f"{P}shield_cost__cost", structure=f"{P}structure_cost__cost",
    vessel=f"{P}vessel_cost__cost", power_supplies=f"{P}power_supplies_cost__cost",
    turbine=f"{P}turbine_cost__cost", electric=f"{P}electric_cost__cost",
    heat_rejection=f"{P}heat_rejection_cost__cost", misc=f"{P}misc_cost__cost",
    contingency=f"{P}contingency__cost", indirect=f"{P}indirect__cost",
    lcoe=f"{P}lcoe_calc__lcoe",
)

# Pass-through direct accounts — model literals (stellarator_plant.sysml), not
# calc outputs (documented Stage-3 pass-throughs). Supplied as harness inputs.
BUILDINGS = 613650000.0
PRECON = 33896000.0
SPECIAL = 26289000.0

# Rollup rates / financing needed for the harness contingency+indirect closure
# (also generated-module inputs; these match the instance bindings).
CONTINGENCY_RATE = 0.10
INDIRECT_FRACTION = 0.20
CONSTRUCTION_YEARS = 8.0
REFERENCE_CONSTRUCTION_TIME = 6.0

failures = []


def check(label, actual, expected):
    denom = max(abs(actual), abs(expected), 1e-30)
    ok = abs(actual - expected) <= REL_TOL * denom
    print(f"  {label:26s} exec={actual:20.6f}  oracle={expected:20.6f}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(label)


def patch_bop_wiring():
    """HARNESS GLUE #1: repoint the 4 BOP Linear_Power_Cost `power` inputs from the
    dangling `mfe_plant__MFE_Power_Plant__p_*` schema field to the real pb output
    channels. Idempotent."""
    text = PIPELINE.read_text()
    repl = {
        "mfe_plant_params.mfe_plant__MFE_Power_Plant__p_the": f"{P}pb__p_the",
        "mfe_plant_params.mfe_plant__MFE_Power_Plant__p_et": f"{P}pb__p_et",
        "mfe_plant_params.mfe_plant__MFE_Power_Plant__p_th": f"{P}pb__p_th",
    }
    n = 0
    for old, new in repl.items():
        n += text.count(old)
        text = text.replace(old, new)
    PIPELINE.write_text(text)
    # The same dangling alias leaves 3 required-but-unminted fields in the
    # SystemDesign schema; the EntryPoint fails validating system_design.json
    # without them. After the repoint above nothing reads these, so fill them
    # with the oracle pb powers (unused, only to satisfy the generated schema).
    o = oracle_compute()
    sd = json.loads(SYS_DESIGN.read_text())
    sd.update({
        "mfe_plant__MFE_Power_Plant__p_th": o["p_th"],
        "mfe_plant__MFE_Power_Plant__p_the": o["p_the"],
        "mfe_plant__MFE_Power_Plant__p_et": o["p_et"],
    })
    SYS_DESIGN.write_text(json.dumps(sd, indent=2))
    print(f"[glue-1] BOP power wiring: repointed {n} input(s) to pb output "
          "channels; filled 3 spurious SystemDesign schema fields (unused)")


def run_pipeline(tag):
    router = create_output_router_with_json_schemas(["RootModel[float]"])
    router.register_handler(
        "float",
        WriteHandler(fn=lambda v, p: Path(p).write_text(json.dumps(v)), extension=".json"),
    )
    result = execute_pipeline(
        PIPELINE,
        output_dir=E2E / "outputs" / tag,
        registry=create_stellarator_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    return {c: (float(v.root) if hasattr(v, "root") else float(v))
            for c, v in result.outputs.items()}


def set_params(**kv):
    data = json.loads(MFE_PARAMS.read_text())
    data.update(kv)
    MFE_PARAMS.write_text(json.dumps(data, indent=2))


def main():
    patch_bop_wiring()

    # ---- PASS A: placeholder rollup; harvest physics + per-account costs -----
    print("=== PASS A: physics spine + per-account cost modules (teax) ===")
    a = run_pipeline("pass_a")

    accounts = ["magnet", "heating", "divertor", "blanket", "shield", "structure",
                "vessel", "power_supplies", "turbine", "electric",
                "heat_rejection", "misc"]
    acc = {k: a[CH[k]] for k in accounts}

    # ---- HARNESS GLUE #2: capital rollup from generated module outputs -------
    powercore = sum(acc[k] for k in ["magnet", "heating", "divertor", "blanket",
                                     "shield", "structure", "vessel", "power_supplies"])
    bop = sum(acc[k] for k in ["turbine", "electric", "heat_rejection", "misc"])
    direct = powercore + bop + BUILDINGS + PRECON + SPECIAL
    contingency = run_contingency_cost(Contingency_CostInput(
        contingency_rate=CONTINGENCY_RATE, direct_subtotal=direct))
    indirect = run_indirect_cost(Indirect_CostInput(
        indirect_fraction=INDIRECT_FRACTION, direct_cost=direct,
        construction_time=CONSTRUCTION_YEARS,
        reference_construction_time=REFERENCE_CONSTRUCTION_TIME))
    total = direct + contingency + indirect
    print(f"[glue-2] rolled up from generated modules: powercore=${powercore/1e9:.4f}B "
          f"bop=${bop/1e9:.4f}B direct=${direct/1e9:.4f}B total=${total/1e9:.4f}B")

    # Feed the closed rollup back into the emitted input JSON.
    set_params(**{
        f"{P}contingency__direct_subtotal": direct,
        f"{P}indirect__direct_cost": direct,
        f"{P}lcoe_calc__total_capital": total,
    })

    # ---- PASS B: contingency + indirect + LCOE from generated modules --------
    print("=== PASS B: contingency + indirect + LCOE DCF (teax, rollup fed) ===")
    b = run_pipeline("pass_b")

    # ---- Oracle comparison --------------------------------------------------
    o = oracle_compute()
    print("\n=== PHYSICS SPINE (executed vs oracle) ===")
    for k in ["V", "p_fus", "p_th", "p_the", "p_et", "q_eng", "rec_frac", "p_net",
              "wall_load"]:
        check(k, b[CH[k]], o[k])

    print("\n=== PER-ACCOUNT CAPITAL, $ (executed vs oracle) ===")
    for k in accounts:
        check(k, b[CH[k]], o[k])

    print("\n=== ROLLUP + LCOE (executed vs oracle) ===")
    check("contingency", b[CH["contingency"]], o["contingency_capital"])
    check("indirect", b[CH["indirect"]], o["indirect_capital"])
    check("direct_capital", direct, o["direct_capital"])
    check("total_capital", total, o["total_capital"])
    check("lcoe", b[CH["lcoe"]], o["lcoe"])

    # ---- WI-019 headline oracle (looser, sanity band) ------------------------
    # Updated for the WI-019 faithful power balance (was the WI-018 table:
    # p_net 575, rec_frac 0.36, q_eng 2.8, total 9.78, LCOE 251).
    print("\n=== WI-019 HEADLINE CHECK ===")
    heads = [
        ("plasma volume V [m3]", b[CH["V"]], 564, 2),
        ("fusion power [MW]", b[CH["p_fus"]], 2700, 5),
        ("net electric [MW]", b[CH["p_net"]], 786, 3),
        ("rec_frac", b[CH["rec_frac"]], 0.258, 0.01),
        ("q_eng", b[CH["q_eng"]], 3.87, 0.05),
        ("total capital [$B]", total / 1e9, 10.09, 0.05),
        ("LCOE [$/MWh]", b[CH["lcoe"]], 189, 2),
        ("magnet capital [$B]", b[CH["magnet"]] / 1e9, 4.39, 0.05),
    ]
    for label, val, target, tol in heads:
        ok = abs(val - target) <= tol
        print(f"  {label:24s} exec={val:14.4f}  WI-019~={target:<10}  "
              f"{'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append("HEAD:" + label)

    # ---- CAS breakdown table ------------------------------------------------
    print("\n=== STELLARIS CAS CAPITAL BREAKDOWN (teax-executed, $) ===")
    rows = [
        ("22.1.3 Magnet System", b[CH["magnet"]]),
        ("22.1.4 Heating & CD", b[CH["heating"]]),
        ("22.1.8 Divertor", b[CH["divertor"]]),
        ("22.1.1 Blanket", b[CH["blanket"]]),
        ("22.1.2 Shield", b[CH["shield"]]),
        ("22.1.5 Primary Structure", b[CH["structure"]]),
        ("22.1.6 Vacuum Vessel", b[CH["vessel"]]),
        ("22.1.7 Power Supplies", b[CH["power_supplies"]]),
        ("  -> CAS22 Power Core", powercore),
        ("23 Turbine Plant", b[CH["turbine"]]),
        ("24 Electric Plant", b[CH["electric"]]),
        ("25 Heat Rejection", b[CH["heat_rejection"]]),
        ("26 Miscellaneous", b[CH["misc"]]),
        ("  -> CAS23-26 BOP", bop),
        ("21 Buildings (pass-thru)", BUILDINGS),
        ("10 Preconstruction (pass-thru)", PRECON),
        ("27 Special Materials (pass-thru)", SPECIAL),
        ("  -> Direct capital", direct),
        ("29 Contingency", b[CH["contingency"]]),
        ("30 Indirect", b[CH["indirect"]]),
        ("  == TOTAL OVERNIGHT", total),
    ]
    for name, val in rows:
        print(f"  {name:34s} {val:18,.0f}   ({val/total*100:5.1f}%)")
    print(f"\n  LCOE (FOAK) = ${b[CH['lcoe']]:.2f}/MWh   net electric = {b[CH['p_net']]:.1f} MW")

    print()
    if failures:
        raise SystemExit(f"{len(failures)} check(s) FAILED: {failures}")
    print(f"ALL CHECKS PASSED (channel-vs-oracle rel tol {REL_TOL}); "
          "WI-019 headline reproduced.")


if __name__ == "__main__":
    main()
