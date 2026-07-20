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
module + the native capital rollup + contingency/indirect/LCOE) is already
certified bit-exact against the pure-Python oracle by run_stellaris_single.py
(rel tol 1e-9); this handshake reuses the same single teax-simkit pass but drives
it with 1costingFE's point instead of the Stellaris design-point bindings.

Item 10 note: the capital rollup (powercore/bop/direct/total_capital) is compiled
by codegen as instance-scoped aggregation producers, so ONE pass computes it in
the graph. The former two-pass HARNESS GLUE #2 (a Python capital rollup that
overwrote three placeholder bridge keys via set_params) is retired. CAS27 special
materials is fed as a declared design input via the injection map. CAS21 buildings
and CAS10 preconstruction are NO LONGER 1costingFE pass-throughs: WI-025 made them
SysML forward-computed modules, so the graph computes them at 1costingFE's fed
powers and the rollup rows below compare that against 1costingFE (a formula check,
not a tautology).
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
    # native capital-rollup aggregation channels (Item 10; no Python glue)
    buildings=f"{P}buildings_cost__cost", precon=f"{P}precon_cost__cost",
    powercore_capital=f"{P}powercore_capital__powercore_capital",
    bop_capital=f"{P}bop_capital__bop_capital",
    direct_capital=f"{P}direct_capital__direct_capital",
    total_capital=f"{P}total_capital__total_capital",
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
    rbld = o["radial_build"]  # WI-021: 1cfe's radial-build inputs, fed into rb
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
        # WI-020: 1costingFE's geometry is a pure elongated torus (no stellarator
        # shaping), and the V above (line ~175) is the torus volume. The
        # generated params carry the Stellaris instance's shape factor 0.794259,
        # so f_shape MUST be overridden to 1.0 here to reproduce 1cfe's torus
        # point — otherwise V (and the injected p_fus) is shrunk by 0.794259.
        f"{P}geom__f_shape": 1.0,
        # WI-021: feed 1costingFE's OWN radial build into the 'MFE Radial Build'
        # calc (rb) so it reproduces 1cfe's aggregate material volumes (blanket/
        # shield/structure/vessel), first-wall area, and coil bore. rb has its own
        # params (rb__*), separate from geom, so the geom__a=1.8 plasma-path
        # override above does NOT leak here. This replaces the former direct
        # blanket__blanket_vol / ... volume injections (now computed, not settable).
        f"{P}rb__R": rbld["R0"], f"{P}rb__a": rbld["plasma_t"], f"{P}rb__kappa": rbld["elon"],
        f"{P}rb__vacuum_t": rbld["vacuum_t"], f"{P}rb__firstwall_t": rbld["firstwall_t"],
        f"{P}rb__blanket_t": rbld["blanket_t"], f"{P}rb__reflector_t": rbld["reflector_t"],
        f"{P}rb__ht_shield_t": rbld["ht_shield_t"], f"{P}rb__structure_t": rbld["structure_t"],
        f"{P}rb__gap1_t": rbld["gap1_t"], f"{P}rb__vessel_t": rbld["vessel_t"],
        f"{P}rb__coil_t": rbld["coil_t"], f"{P}rb__gap2_t": rbld["gap2_t"],
        f"{P}rb__lt_shield_t": rbld["lt_shield_t"],
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
        # WI-024 (design D7 successor injection): pb__p_cryo is now a
        # chain-wired channel, not a settable leaf. Zero the chain's heat
        # inputs and feed 1cfe's p_cryo through the additive direct term —
        # the identity path is exact in IEEE arithmetic (0-heat chain
        # contributes exactly 0; baked f_uplift/T/f_carnot values are inert
        # at zero heat), so downstream floats match the pre-WI-024 record
        # bit for bit.
        f"{P}cryo_elec__q_nuc": 0.0, f"{P}cryo_elec__vol_cold": 0.0,
        f"{P}cryo_elec__p_fixed": 0.0, f"{P}cryo_elec__p_direct": pb["p_cryo"],
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
        # CAS27 special materials: declared design input to the direct_capital
        # aggregation, fed 1costingFE's pass-through value (M$ -> $). Replaces the
        # retired glue's Python addition of `special` into the capital sum.
        f"{P}direct_capital__special_materials_capital": o["costs_musd"]["cas27"] * M,
        # WI-025 (design D6 successor injection): lcoe_calc__annual_om is now
        # a chain-wired channel (annual_om = om_cost.annual_om), not a
        # settable leaf. Zero the O&M reference here so the chain computes
        # 0.0*(p_net/1000)^0.5 + om_direct = om_direct — exact in IEEE
        # arithmetic (0*finite = 0, 0 + v = v; the WI-024 D7 identity-path
        # precedent) — and feed 1cfe's unlevelized annual O&M through the
        # additive om_direct term in the params block below, so lcoe receives
        # 1cfe's value bit for bit.
        f"{P}om_cost__om_ref": 0.0,
        # LCOE financing / performance
        f"{P}lcoe_calc__availability": o["target"]["availability"],
        f"{P}lcoe_calc__construction_years": o["target"]["construction_time_yr"],
        f"{P}lcoe_calc__discount_rate": o["target"]["interest_rate"],
        f"{P}lcoe_calc__operational_years": float(o["target"]["lifetime_yr"]),
    })
    SYS_DESIGN.write_text(json.dumps(sd, indent=2))

    mp = json.loads(MFE_PARAMS.read_text())
    mp.update({
        # blanket (C220101). WI-021: blanket_vol is no longer an injectable param
        # — it is computed by the 'MFE Radial Build' calc (rb), fed 1cfe's own
        # radial build in the sd.update block above, so rb reproduces geo's
        # aggregate volumes. Same for shield/structure/vessel volumes and r_coil.
        f"{P}blanket__structure_factor": 1.0,  # liquid_metal (PbLi) -> 1.0
        f"{P}blanket__unit_cost": uc["blanket_unit_cost_dt"] * M,
        f"{P}blanket_cost__alpha": 0.6, f"{P}blanket_cost__p_th_ref": refs["P_TH_REF"],
        # shield (C220102)
        f"{P}shield__shield_scale": refs["shield_scale_dt"],
        f"{P}shield__unit_cost": uc["shield_unit_cost"] * M,
        f"{P}shield_cost__alpha": 0.6, f"{P}shield_cost__p_th_ref": refs["P_TH_REF"],
        # structure (C220105)
        f"{P}structure__unit_cost": uc["structure_unit_cost"] * M,
        f"{P}structure_cost__alpha": 0.5,
        f"{P}structure_cost__p_et_ref": refs["ref_gross_power_mwe"],
        # vessel (C220106_vessel — shell term only)
        f"{P}vessel__unit_cost": uc["vessel_unit_cost"] * M,
        f"{P}vessel_cost__alpha": 0.6,
        f"{P}vessel_cost__p_et_ref": refs["ref_gross_power_mwe"],
        # power supplies (C220107, ARIES-CS-derived base — footnoted)
        f"{P}power_supplies__base": uc["power_supplies_base"] * M,
        f"{P}power_supplies_cost__alpha": 0.7,
        f"{P}power_supplies_cost__p_et_ref": refs["ref_gross_power_mwe"],
        # divertor (C220108)
        f"{P}divertor_cost__alpha": 0.5, f"{P}divertor_cost__p_th_ref": 1000.0,
        # magnet (C220103): B <- b_center (NOT radiation B); r_coil now from rb.
        f"{P}magnet__B": coil["b_center"], f"{P}magnet__G": coil["G_8pi2"],
        f"{P}magnet__R0": coil["R0"], f"{P}magnet__coil_markup": coil["coil_markup"],
        f"{P}magnet__cost_per_kAm": coil["cost_per_kam"],
        # BOP per-MW rates (M$/MW -> $/MW)
        f"{P}turbine__cost_per_mw": uc["turbine_per_mw"] * M,
        f"{P}electric_plant__cost_per_mw": uc["electric_per_mw"] * M,
        f"{P}misc_plant__cost_per_mw": uc["misc_per_mw"] * M,
        f"{P}heat_rejection__cost_per_mw": uc["heat_rej_per_mw"] * M,
        # indirect reference construction time
        f"{P}indirect__reference_construction_time": refs["reference_construction_time"],
        # WI-025 (D6): 1cfe's unlevelized annual O&M through the om_cost
        # additive direct term (om_ref zeroed in the sd block above —
        # IEEE-exact identity path; defaulted-input keys are settable here,
        # the blanket_cost__alpha precedent).
        f"{P}om_cost__om_direct": refs["annual_om_unlevelized_musd"] * M,
    })
    MFE_PARAMS.write_text(json.dumps(mp, indent=2))
    return dict(V=V, sigma_v=sigma_v, p_fus_target=p_fus_target)


def run_pipeline(tag):
    # Register the constraint ExitPoint schema types alongside RootModel[float] so the
    # regenerated package's ConstraintReport exit points get a write handler (the
    # run_stellaris_single adapter pattern); float exits keep the plain JSON handler.
    schema_names = dict.fromkeys(["RootModel[float]"] + [t.__name__ for t in CUSTOM_SCHEMA_TYPES])
    router = create_output_router_with_json_schemas(list(schema_names))
    router.register_handler(
        "float",
        WriteHandler(fn=lambda v, p: Path(p).write_text(json.dumps(v)), extension=".json"),
    )
    result = execute_pipeline(
        PIPELINE, output_dir=E2E / "outputs" / tag,
        registry=create_stellarator_tea_registry(),
        output_router=router, custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    # Keep only float-valued channels; the constraint ExitPoints emit ConstraintEvaluation
    # objects (the five verdicts), which the cost/power comparison below does not consume.
    return {c: (float(v.root) if hasattr(v, "root") else float(v))
            for c, v in result.outputs.items()
            if hasattr(v, "root") or isinstance(v, (int, float))}


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
        patch_bop_wiring(o)          # HARNESS GLUE #1 (BOP wiring) — kept
        inj = set_1cfe_inputs(o)     # 1costingFE injection map (incl. CAS27 special input)

        # ---- SINGLE PASS: physics spine + per-account costs + native capital rollup ----
        # The capital rollup (powercore/bop/direct/total_capital), contingency, indirect and
        # LCOE are all computed in the graph in one pass — codegen compiles the rollup as
        # instance-scoped aggregation producers. The former two-pass HARNESS GLUE #2 (Python
        # capital rollup + placeholder set_params overwrite) is retired.
        M = 1e6
        b = run_pipeline("hs")
        acc = {k: b[CH[k]] for k in ACCOUNTS}

        # verify fusion-power injection reproduced 1cfe p_fus
        p_fus_sysml = b[CH["p_fus"]]

        # capital rollup sourced from the graph's native aggregation channels (no Python glue)
        powercore = b[CH["powercore_capital"]]
        bop = b[CH["bop_capital"]]
        direct = b[CH["direct_capital"]]
        total = b[CH["total_capital"]]
        # CAS27 special is a declared design input, fed 1cfe's value via the injection map.
        special = o["costs_musd"]["cas27"] * M

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

        # CAS21/CAS10 are now SysML forward-computed (WI-025) at 1cfe's fed powers — a
        # formula comparison vs 1cfe, no longer a tautological pass-through. CAS27 special
        # is still a fed design input (tautological). Buildings/precon divergence here is
        # the model's documented simplification, previously masked by the retired glue.
        buildings = b[CH["buildings"]]
        precon = b[CH["precon"]]
        pass_rows = [
            ("buildings (CAS21) [SysML fwd@1cfe-pwr]", o["costs_musd"]["cas21"] * M, buildings),
            ("preconstruction (CAS10) [SysML fwd@1cfe-pwr]", o["costs_musd"]["cas10"] * M, precon),
            ("special_materials (CAS27) [design-input]", o["costs_musd"]["cas27"] * M, special),
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

        print("\n--- CAS21/CAS10 (SysML fwd-computed @ 1cfe power) + CAS27 (design input), $ ---")
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
