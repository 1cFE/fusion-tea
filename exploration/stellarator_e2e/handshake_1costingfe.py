"""Anchor A — the 1costingFE machinery handshake (WI-018 / concept SC-3).

Feed the generated SysML forward model the EXACT plant point 1costingFE solved
for (its solved fusion power + its full merged parameter set), then check that
the generated SysML pipeline reproduces 1costingFE's per-account costs and LCOE.

This isolates the codegen/execution machinery from modeling judgment: the SysML
calc defs were reproduced from 1costingFE formulas, so where the formula is
identical and codegen is faithful the numbers match tightly. Divergences reveal
the initial (Stellaris) model's documented simplifications.

Two interpreters are involved (costingfe and simkit never coexist in one venv):
  1. 1costingFE point: emitted to onecfe_point.json by a subprocess run in the
     1costingfe uv env. Commit is pinned + recorded.
  2. SysML pipeline: this file runs in the teax exec venv
     (fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python), which has
     simkit + the generated stellarator_tea package.

Run:  cd .../exploration/stellarator_e2e && \
      /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python \
        handshake_1costingfe.py

The generated pipeline's execution path (physics spine + every per-account cost
module + contingency/indirect/LCOE) is already certified bit-exact against the
pure-Python oracle by run_stellaris.py (rel tol 1e-9); this handshake reuses the
same execution path but drives it with 1costingFE's point instead of the
Stellaris design-point bindings.
"""

import json
import math
import subprocess
import sys
from pathlib import Path

E2E = Path(__file__).parent
sys.path.insert(0, str(E2E))

# Make the generated package importable as `stellarator_tea` (same shim as run_stellaris).
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
POINT_JSON = E2E / "onecfe_point.json"
ONECFE_REPO = Path("/home/reid/1cfe/1costingfe")
EMITTER = E2E / "emit_1cfe_point.py"

P = "stellarator_09__stellaris__"

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

# SysML powercore account -> 1costingFE cas22_detail key (formula-reproduced).
# vessel maps to C220106_vessel: the SysML vessel calc is the vessel-shell term
# only; 1costingFE's canonical C220106 additionally carries a gas-load pumping
# sub-term (C220106_pump), a documented SysML simplification.
POWERCORE_MAP = {
    "magnet": "C220103", "heating": "C220104", "divertor": "C220108",
    "blanket": "C220101", "shield": "C220102", "structure": "C220105",
    "vessel": "C220106_vessel", "power_supplies": "C220107",
}
# SysML BOP account -> 1costingFE top-level CAS (formula-reproduced).
BOP_MAP = {"turbine": "cas23", "electric": "cas24",
           "heat_rejection": "cas26", "misc": "cas25"}

POWERCORE = list(POWERCORE_MAP)
BOP = list(BOP_MAP)
ACCOUNTS = POWERCORE + BOP


def emit_point():
    """Run the emitter in the 1costingfe uv env; record the pinned commit."""
    commit = subprocess.check_output(
        ["git", "-C", str(ONECFE_REPO), "rev-parse", "--short", "HEAD"]
    ).decode().strip()
    subprocess.run(
        ["uv", "run", "python", str(EMITTER), str(POINT_JSON)],
        cwd=str(ONECFE_REPO), check=True,
    )
    pt = json.loads(POINT_JSON.read_text())
    assert pt["commit"] == commit, f"commit drift: {pt['commit']} vs {commit}"
    print(f"[1cfe] emitted point at commit {commit}")
    return pt


def snapshot():
    return {f: f.read_bytes() for f in (MFE_PARAMS, SYS_DESIGN, PIPELINE)}


def restore(snap):
    for f, b in snap.items():
        f.write_bytes(b)


def patch_bop_wiring(o):
    """HARNESS GLUE #1 (identical to run_stellaris): repoint the 4 BOP
    Linear_Power_Cost `power` inputs from the dangling
    mfe_plant__MFE_Power_Plant__p_* schema field to the real pb output channels,
    and fill the 3 now-unread SystemDesign schema fields so the EntryPoint
    validates. Idempotent."""
    text = PIPELINE.read_text()
    repl = {
        f"mfe_plant_params.mfe_plant__MFE_Power_Plant__p_the": f"{P}pb__p_the",
        f"mfe_plant_params.mfe_plant__MFE_Power_Plant__p_et": f"{P}pb__p_et",
        f"mfe_plant_params.mfe_plant__MFE_Power_Plant__p_th": f"{P}pb__p_th",
    }
    for old, new in repl.items():
        text = text.replace(old, new)
    PIPELINE.write_text(text)
    sd = json.loads(SYS_DESIGN.read_text())
    sd.update({
        "mfe_plant__MFE_Power_Plant__p_th": o["power_table"]["p_th"],
        "mfe_plant__MFE_Power_Plant__p_the": o["power_table"]["p_the"],
        "mfe_plant__MFE_Power_Plant__p_et": o["power_table"]["p_et"],
    })
    SYS_DESIGN.write_text(json.dumps(sd, indent=2))


def set_1cfe_inputs(o):
    """Map 1costingFE's merged point onto the generated pipeline inputs.

    Money unit: 1costingFE rolls up in M$; the SysML rolls up in $. Every
    coefficient 1costingFE stores in M$ (unit costs, per-MW rates, bases) is
    fed x1e6 so the SysML produces $. magnet cost_per_kAm ($/kA-m) is fed as-is
    (the SysML magnet calc omits the /1e6, so it already yields $).
    """
    pb = o["pb_params"]
    pw = o["power_table"]
    uc = o["unit_costs_musd"]
    geo = o["geometry"]
    coil = o["coil"]
    refs = o["refs"]
    M = 1e6

    # --- fusion-power injection: p_fus is GIVEN by 1costingFE's solve. ---
    # Short-circuit the SysML DT Fusion Power calc by choosing sigma_v so the
    # geometry x density x reactivity product reproduces 1costingFE's p_fus
    # exactly (mapping trap: fusion power is given, not recomputed).
    n_e, E_fus = 3.37e20, 2.817e-12
    R, a, kappa, pi = coil["R0"], 1.8, 1.6, 3.14159265358979
    V = 2.0 * pi**2 * R * a**2 * kappa
    p_fus_target = pw["p_fus"]
    sigma_v = p_fus_target / (0.25 * n_e**2 * E_fus * V * 1e-6)

    eta_pin = o["eta_pin_effective"]

    sd = json.loads(SYS_DESIGN.read_text())
    sd.update({
        # fusion-power injector
        f"{P}fusion__n_e": n_e, f"{P}fusion__E_fus": E_fus,
        f"{P}fusion__sigma_v": sigma_v,
        f"{P}geom__R": R, f"{P}geom__a": a, f"{P}geom__kappa": kappa,
        # power-balance params mapped from 1costingFE merged params
        f"{P}pb__p_input": pb["p_input"], f"{P}pb__mn": pb["mn"],
        f"{P}pb__eta_th": pb["eta_th"], f"{P}pb__eta_p": pb["eta_p"],
        f"{P}pb__eta_pin": eta_pin, f"{P}pb__f_sub": pb["f_sub"],
        # WI-019: pumping power is now the same absolute p_pump [MW] input as
        # 1costingFE (former fpcppf mapping trap resolved).
        f"{P}pb__p_pump": pb["p_pump"],
        # SysML splits coils/cooling into tf/pf; 1costingFE has single
        # p_coils / p_cool. Put the full 1cfe value in the tf slot, 0 in pf.
        f"{P}pb__p_tf": pb["p_coils"], f"{P}pb__p_pf": 0.0,
        f"{P}pb__p_tfcool": pb["p_cool"], f"{P}pb__p_pfcool": 0.0,
        f"{P}pb__p_trit": pb["p_trit"], f"{P}pb__p_house": pb["p_house"],
        f"{P}pb__p_cryo": pb["p_cryo"],
        # heating (ECRH-only for the stellarator point)
        f"{P}heating_cost__ecrh_per_mw": uc["heating_ecrh_per_mw"] * M,
        f"{P}heating_cost__nbi_per_mw": uc["heating_nbi_per_mw"] * M,
        f"{P}heating_cost__icrf_per_mw": 0.0, f"{P}heating_cost__lhcd_per_mw": 0.0,
        f"{P}heating_cost__p_ecrh": pb["p_ecrh"], f"{P}heating_cost__p_nbi": 0.0,
        f"{P}heating_cost__p_icrf": 0.0, f"{P}heating_cost__p_lhcd": 0.0,
        # divertor base
        f"{P}divertor_cost__base": uc["divertor_base"] * M,
        # rollup rates: 1costingFE point is NOAK -> contingency_rate = 0.
        # (The SysML/Stellaris model default is 0.10; fed 0 here to match the
        #  1cfe point, footnoted in the report.)
        f"{P}contingency__contingency_rate": refs["contingency_rate_noak"],
        f"{P}indirect__indirect_fraction": refs["indirect_fraction"],
        f"{P}indirect__construction_time": o["target"]["construction_time_yr"],
        # LCOE financing / performance
        f"{P}lcoe_calc__annual_om": refs["annual_om_unlevelized_musd"] * M,
        f"{P}lcoe_calc__availability": o["target"]["availability"],
        f"{P}lcoe_calc__construction_years": o["target"]["construction_time_yr"],
        f"{P}lcoe_calc__discount_rate": o["target"]["interest_rate"],
        f"{P}lcoe_calc__operational_years": float(o["target"]["lifetime_yr"]),
    })
    SYS_DESIGN.write_text(json.dumps(sd, indent=2))

    mp = json.loads(MFE_PARAMS.read_text())
    mp.update({
        # blanket (C220101)
        f"{P}blanket__blanket_vol": geo["blanket_vol"],
        f"{P}blanket__structure_factor": 1.0,  # liquid_metal (PbLi) -> 1.0
        f"{P}blanket__unit_cost": uc["blanket_unit_cost_dt"] * M,
        f"{P}blanket_cost__alpha": 0.6, f"{P}blanket_cost__p_th_ref": refs["P_TH_REF"],
        # shield (C220102)
        f"{P}shield__shield_scale": refs["shield_scale_dt"],
        f"{P}shield__shield_vol": geo["shield_vol"],
        f"{P}shield__unit_cost": uc["shield_unit_cost"] * M,
        f"{P}shield_cost__alpha": 0.6, f"{P}shield_cost__p_th_ref": refs["P_TH_REF"],
        # structure (C220105)
        f"{P}structure__structure_vol": geo["structure_vol"],
        f"{P}structure__unit_cost": uc["structure_unit_cost"] * M,
        f"{P}structure_cost__alpha": 0.5,
        f"{P}structure_cost__p_et_ref": refs["ref_gross_power_mwe"],
        # vessel (C220106_vessel — shell term only)
        f"{P}vessel__unit_cost": uc["vessel_unit_cost"] * M,
        f"{P}vessel__vessel_vol": geo["vessel_vol"],
        f"{P}vessel_cost__alpha": 0.6,
        f"{P}vessel_cost__p_et_ref": refs["ref_gross_power_mwe"],
        # power supplies (C220107, ARIES-CS-derived base — footnoted)
        f"{P}power_supplies__base": uc["power_supplies_base"] * M,
        f"{P}power_supplies_cost__alpha": 0.7,
        f"{P}power_supplies_cost__p_et_ref": refs["ref_gross_power_mwe"],
        # divertor (C220108)
        f"{P}divertor_cost__alpha": 0.5, f"{P}divertor_cost__p_th_ref": 1000.0,
        # magnet (C220103): B <- b_center (NOT radiation B); r_coil <- vessel_or
        f"{P}magnet__B": coil["b_center"], f"{P}magnet__G": coil["G_8pi2"],
        f"{P}magnet__R0": coil["R0"], f"{P}magnet__coil_markup": coil["coil_markup"],
        f"{P}magnet__cost_per_kAm": coil["cost_per_kam"],
        f"{P}magnet__r_coil": geo["r_coil_vessel_or"],
        # BOP per-MW rates (M$/MW -> $/MW)
        f"{P}turbine__cost_per_mw": uc["turbine_per_mw"] * M,
        f"{P}electric_plant__cost_per_mw": uc["electric_per_mw"] * M,
        f"{P}misc_plant__cost_per_mw": uc["misc_per_mw"] * M,
        f"{P}heat_rejection__cost_per_mw": uc["heat_rej_per_mw"] * M,
        # indirect reference construction time
        f"{P}indirect__reference_construction_time": refs["reference_construction_time"],
    })
    MFE_PARAMS.write_text(json.dumps(mp, indent=2))
    return dict(V=V, sigma_v=sigma_v, p_fus_target=p_fus_target)


def set_params(**kv):
    data = json.loads(MFE_PARAMS.read_text())
    data.update(kv)
    MFE_PARAMS.write_text(json.dumps(data, indent=2))


def run_pipeline(tag):
    router = create_output_router_with_json_schemas(["RootModel[float]"])
    router.register_handler(
        "float",
        WriteHandler(fn=lambda v, p: Path(p).write_text(json.dumps(v)), extension=".json"),
    )
    result = execute_pipeline(
        PIPELINE, output_dir=E2E / "outputs" / tag,
        registry=create_stellarator_tea_registry(),
        output_router=router, custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    return {c: (float(v.root) if hasattr(v, "root") else float(v))
            for c, v in result.outputs.items()}


def sysml_account_formula(name, o, p_th, p_et):
    """Recompute a SysML powercore account with GIVEN thermal/gross power, in $.

    Mirrors the generated calc def line-for-line. Used for the formula-isolation
    check: fed 1costingFE's OWN p_th/p_et it must reproduce 1costingFE's account
    to floating point (proving the formula/codegen is faithful and that the
    end-to-end gap is caused by the power-balance inputs, not the cost formula).
    """
    uc, geo, coil, refs = (o["unit_costs_musd"], o["geometry"], o["coil"], o["refs"])
    M = 1e6
    et_ref, th_ref = refs["ref_gross_power_mwe"], refs["P_TH_REF"]
    if name == "magnet":
        mu0 = 1.25663706212e-06
        total_kAm = coil["G_8pi2"] * coil["b_center"] * coil["R0"] * geo["r_coil_vessel_or"] / (mu0 * 1000.0)
        return total_kAm * coil["cost_per_kam"] * coil["coil_markup"]
    if name == "heating":
        return uc["heating_ecrh_per_mw"] * M * o["pb_params"]["p_ecrh"]
    if name == "blanket":
        return uc["blanket_unit_cost_dt"] * M * 1.0 * geo["blanket_vol"] * (p_th / th_ref) ** 0.6
    if name == "shield":
        return uc["shield_unit_cost"] * M * geo["shield_vol"] * refs["shield_scale_dt"] * (p_th / th_ref) ** 0.6
    if name == "structure":
        return uc["structure_unit_cost"] * M * geo["structure_vol"] * (p_et / et_ref) ** 0.5
    if name == "vessel":
        return uc["vessel_unit_cost"] * M * geo["vessel_vol"] * (p_et / et_ref) ** 0.6
    if name == "power_supplies":
        return uc["power_supplies_base"] * M * (p_et / et_ref) ** 0.7
    if name == "divertor":
        return uc["divertor_base"] * M * (p_th / 1000.0) ** 0.5
    raise KeyError(name)


def rel(a, b):
    d = max(abs(a), abs(b), 1e-30)
    return (a - b) / d


def main():
    o = emit_point()
    snap = snapshot()
    rows_out = {}
    try:
        patch_bop_wiring(o)
        inj = set_1cfe_inputs(o)

        # ---- PASS A: physics spine + per-account cost modules -----------------
        a = run_pipeline("hs_pass_a")
        acc = {k: a[CH[k]] for k in ACCOUNTS}

        # verify fusion-power injection reproduced 1cfe p_fus
        p_fus_sysml = a[CH["p_fus"]]

        # ---- HARNESS GLUE #2: capital rollup with 1cfe pass-throughs ----------
        M = 1e6
        buildings = o["costs_musd"]["cas21"] * M   # <- 1cfe CAS21 (pass-through)
        precon = o["costs_musd"]["cas10"] * M       # <- 1cfe CAS10 (pass-through)
        special = o["costs_musd"]["cas27"] * M      # <- 1cfe CAS27 (pass-through)
        contingency_rate = o["refs"]["contingency_rate_noak"]
        indirect_fraction = o["refs"]["indirect_fraction"]
        construction_years = o["target"]["construction_time_yr"]
        ref_ct = o["refs"]["reference_construction_time"]

        powercore = sum(acc[k] for k in POWERCORE)
        bop = sum(acc[k] for k in BOP)
        direct = powercore + bop + buildings + precon + special
        contingency = run_contingency_cost(Contingency_CostInput(
            contingency_rate=contingency_rate, direct_subtotal=direct))
        indirect = run_indirect_cost(Indirect_CostInput(
            indirect_fraction=indirect_fraction, direct_cost=direct,
            construction_time=construction_years, reference_construction_time=ref_ct))
        total = direct + contingency + indirect

        set_params(**{
            f"{P}contingency__direct_subtotal": direct,
            f"{P}indirect__direct_cost": direct,
            f"{P}lcoe_calc__total_capital": total,
        })

        # ---- PASS B: contingency + indirect + LCOE DCF ------------------------
        b = run_pipeline("hs_pass_b")

        # ---- power balance (SysML pipeline vs 1cfe) ---------------------------
        pw = o["power_table"]
        pb_rows = []
        for k in ["p_th", "p_the", "p_et", "p_net", "q_eng", "rec_frac"]:
            pb_rows.append((k, pw[k], b[CH[k]], rel(b[CH[k]], pw[k])))

        # ---- per-account comparison (SysML $ vs 1cfe $) -----------------------
        p_th_1c, p_et_1c = pw["p_th"], pw["p_et"]
        p_th_sy, p_et_sy = b[CH["p_th"]], b[CH["p_et"]]
        acct_rows = []
        for k in ACCOUNTS:
            if k in POWERCORE_MAP:
                onecfe = o["cas22_detail_musd"][POWERCORE_MAP[k]] * M
            else:
                onecfe = o["costs_musd"][BOP_MAP[k]] * M
            sysml = b[CH[k]]
            # formula-isolation: SysML formula fed 1cfe's OWN power
            iso = None
            if k in POWERCORE_MAP:
                iso = sysml_account_formula(k, o, p_th_1c, p_et_1c)
            acct_rows.append(dict(account=k, onecfe=onecfe, sysml=sysml,
                                  rel_dev=rel(sysml, onecfe),
                                  iso_at_1cfe_power=iso,
                                  iso_rel=(rel(iso, onecfe) if iso is not None else None)))

        # pass-throughs (tautological — fed 1cfe values)
        pass_rows = [
            ("buildings (CAS21)", o["costs_musd"]["cas21"] * M, buildings),
            ("preconstruction (CAS10)", o["costs_musd"]["cas10"] * M, precon),
            ("special_materials (CAS27)", o["costs_musd"]["cas27"] * M, special),
        ]

        # rollup + LCOE
        onec = o["costs_musd"]
        rollup = dict(
            contingency=(onec["cas29"] * M, b[CH["contingency"]]),
            indirect=(onec["cas30"] * M, b[CH["indirect"]]),
            direct_or_cas20=(onec["cas20"] * M, direct),
            total_capital=(onec["total_capital"] * M, total),
            lcoe=(onec["lcoe"], b[CH["lcoe"]]),
            net_electric=(pw["p_net"], b[CH["p_net"]]),
        )

        # ---------------------- PRINT ----------------------------------------
        print("\n" + "=" * 78)
        print("ANCHOR A — 1costingFE MACHINERY HANDSHAKE")
        print("=" * 78)
        print(f"1costingFE commit: {o['commit']}")
        t = o["target"]
        print(f"target: {t['concept']} {t['fuel']}, net_electric={t['net_electric_mw']} MW, "
              f"avail={t['availability']}, life={t['lifetime_yr']} yr, "
              f"ct={t['construction_time_yr']} yr, i={t['interest_rate']}, elon={t['elon']}")
        print(f"solved p_fus = {pw['p_fus']:.3f} MW  (SysML injector reproduced "
              f"{p_fus_sysml:.3f} MW, rel {rel(p_fus_sysml, pw['p_fus']):+.2e})")
        print(f"1cfe LCOE={onec['lcoe']:.3f} $/MWh  net={pw['p_net']:.1f} MW  "
              f"total_capital={onec['total_capital']:.1f} M$  cas22(full)={onec['cas22']:.1f} M$")

        print("\n--- POWER BALANCE (SysML pipeline vs 1costingFE) ---")
        print(f"{'channel':10s} {'1cfe':>14s} {'SysML':>14s} {'rel dev':>10s}")
        for k, one, sy, r in pb_rows:
            print(f"{k:10s} {one:14.4f} {sy:14.4f} {r:+10.3%}")

        print("\n--- PER-ACCOUNT (formula-reproduced), $  ---")
        print(f"{'account':16s} {'1costingFE $':>16s} {'SysML $':>16s} {'rel dev':>9s} "
              f"{'iso@1cfe-pwr rel':>16s}")
        worst = (None, 0.0)
        worst_iso = (None, 0.0)
        for r in acct_rows:
            iso_s = f"{r['iso_rel']:+.2e}" if r["iso_rel"] is not None else "   (n/a: no p)"
            print(f"{r['account']:16s} {r['onecfe']:16,.0f} {r['sysml']:16,.0f} "
                  f"{r['rel_dev']:+9.2%} {iso_s:>16s}")
            if abs(r["rel_dev"]) > abs(worst[1]):
                worst = (r["account"], r["rel_dev"])
            if r["iso_rel"] is not None and abs(r["iso_rel"]) > abs(worst_iso[1]):
                worst_iso = (r["account"], r["iso_rel"])
        print(f"worst end-to-end rel dev: {worst[0]} = {worst[1]:+.2%}")
        print(f"worst formula-isolation rel dev (SysML formula @ 1cfe power): "
              f"{worst_iso[0]} = {worst_iso[1]:+.2e}")

        print("\n--- PASS-THROUGH (tautological — fed 1cfe values), $ ---")
        for name, one, sy in pass_rows:
            print(f"{name:28s} {one:16,.0f} {sy:16,.0f} {rel(sy, one):+9.2%}")

        print("\n--- ROLLUP + LCOE (SysML simplified model vs 1costingFE) ---")
        for k, (one, sy) in rollup.items():
            unit = "$/MWh" if k == "lcoe" else ("MW" if k == "net_electric" else "$")
            print(f"{k:20s} 1cfe={one:16,.4f}  SysML={sy:16,.4f}  "
                  f"rel={rel(sy, one):+8.2%}  [{unit}]")

        rows_out = dict(commit=o["commit"], target=t, injection=inj,
                        p_fus=dict(onecfe=pw["p_fus"], sysml=p_fus_sysml),
                        power_balance=[dict(channel=k, onecfe=one, sysml=sy, rel=r)
                                       for k, one, sy, r in pb_rows],
                        accounts=acct_rows,
                        passthrough=[dict(name=n, onecfe=one, sysml=sy) for n, one, sy in pass_rows],
                        rollup={k: dict(onecfe=one, sysml=sy) for k, (one, sy) in rollup.items()},
                        cas22_gap_musd=dict(
                            onecfe_cas22_full=onec["cas22"],
                            sysml_powercore_musd=powercore / M,
                            unmodeled_musd=onec["cas22"] - powercore / M))
        (E2E / "handshake_comparison.json").write_text(json.dumps(rows_out, indent=2))
        print(f"\n[out] wrote {E2E / 'handshake_comparison.json'}")
    finally:
        restore(snap)
        print("[cleanup] restored generated input JSONs + pipeline YAML to pre-handshake state")


if __name__ == "__main__":
    main()
