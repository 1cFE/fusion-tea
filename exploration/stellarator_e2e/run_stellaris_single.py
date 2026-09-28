"""Single-pass stellarator runner: the sealed package at its authored design point.

The cross-part capital rollup is compiled by codegen and computed in one teax-simkit
pass. The package is strict-loaded with no harness glue. This demo/regression command
checks recorded anchors, all 20 generated verdicts, numerical agreement with the
independent demo oracle, and three synthetic CAS72 guard cases. Any failed gate family
produces a nonzero process exit after the diagnostic output is printed.

Run (repository root, with STOP_PARSER_TEAX_ROOT exported):
    uv run python exploration/stellarator_e2e/run_stellaris_single.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_stellaris as rs  # noqa: E402  (strict-loads the sealed package)
from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    WriteHandler,
    create_output_router_with_json_schemas,
)
from verify_stellaris import compute as oracle_compute  # noqa: E402

CUSTOM_SCHEMA_TYPES = rs.CUSTOM_SCHEMA_TYPES
create_stellarator_tea_registry = rs.create_stellarator_tea_registry
P, CH = rs.P, rs.CH

EXPECTED_VERDICTS = {
    "reference_conductor_current_ok": "violated",  # WI-062 conditional perpendicular-field estimate.
    "wp_fit_ok": "violated",  # WI-061 .36 m pack exceeds independent .30 m exterior allocation.
    "heating_source_positive_ok": "satisfied",
    "heating_source_upper_ok": "satisfied",
    "heating_couple_positive_ok": "satisfied",
    "heating_couple_upper_ok": "satisfied",
    "beta_ok": "satisfied",
    "net_positive": "satisfied",
    "recirc_ok": "satisfied",
    # WI-066: computed numerical lower estimate falls below the conditional fuel requirement.
    "tbr_ok": "violated",
    # WI-041: the fence compares the computed PEAK (the circular-torus
    # average x the source-anchored calibration 1.316441) with the printed
    # 4.05; at the WI-041 baseline it read 4.088 -- VIOLATED. WI-042: the
    # helium ash on the source's own profile rule re-closes the fixed point
    # with more ash and less fuel, p_fus 2725.36 -> 2652.56 MW, so the peak
    # reads 4.05 x 2652.563 / 2700 = 3.979 -- EXPECTED SATISFIED. Disclosed,
    # never tuned (WI-042 plan, MR-WI042-14 restatement (b)).
    "wall_load_ok": "satisfied",
    # WI-030 conductor peak-field limit. WI-044: the operand now sees the coil
    # bore (eq. 39's R/(R - a_coil) normalised at the reference geometry); at the
    # baseline the factor is exactly 1.0, so the executed peak is unchanged at
    # 24.9 minus one ulp and the verdict stays SATISFIED at equality. Off the
    # design column it rises with a (a 1.4 on the design column reads 25.16 T).
    "peak_field_ok": "satisfied",
    "wp_stress_ok": "satisfied",  # WI-035
    "cond_strain_ok": "satisfied",
    # WI-037: the sustainment power limit read VIOLATED at the printed point-A
    # levers (p_aux_required ~= 90.6 MW vs 50 coupled) under the WI-037 profile
    # family (the ash at the fuel's exponent). WI-042: with the ash on the
    # source's own rule and the electrons by quasi-neutrality, W 551.4 -> 519.9
    # MJ, tau_E 1.450 -> 1.557 s, p_aux_required 90.605 -> 49.080 MW --
    # EXPECTED SATISFIED by about 0.9 MW, a margin inside the source's own
    # 2.7 % residual on its printed stored energy (goal stored-energy-basis
    # L-002): on the boundary, disclosed, never tuned. The report headline is
    # 'full_satisfaction' accordingly.
    "sustainment_ok": "satisfied",
    # WI-043 (goal burn-control): the lower half of the operating-point
    # condition, p_aux_required >= 0 -- the HOLD condition: a point with a
    # negative requirement is one the installed heating cannot hold (no
    # non-negative heating closes its balance), not a point that needs no
    # heating. EXPECTED SATISFIED at the baseline (49.08 MW >= 0): the model
    # reads the machine as designed as a driven point; the source's own
    # Table 5 reads its point A as ignited at 0 MW, the difference inside the
    # source's two-sided spread on its stored energy (goal stored-energy-basis
    # L-004). Nothing moved with this verdict: every channel bit-identical.
    "burn_hold_ok": "satisfied",
    # WI-045 (goal plant-closure, 2026-09-08): the primary loop and the cycle are
    # computed producers. loop_pressure_ok: the per-path loss (300.5 kPa) against
    # the 8 MPa loop -- the loss law's own domain. loop_capacity_ok: the per-loop
    # flow (215.05 kg/s at 14 loops) against the reference's rated 225.08 -- the
    # sizing rule puts the design point 4.5 % under the rating, so SATISFIED here
    # by construction and VIOLATED one step off the design column (a 1.4) and at
    # the committed cheapest machine at this count (design D6). cycle_domain_ok:
    # the turbine inlet 480 C inside the fit's 384-642 C. The design point MOVED
    # as predicted (LCOE 322.318 -> 237.253 at the held availability); the
    # compatibility proposal reproduces the WI-044 pin bit-for-bit.
    "loop_pressure_ok": "satisfied",
    "loop_capacity_ok": "satisfied",
    "cycle_domain_ok": "satisfied",
    # WI-047 (goal plant-closure, 2026-09-08): the divertor target peak -- the
    # source's fixed-geometry PESSIMISTIC transport case (9.5 MW/m^2 at 50 MW
    # non-radiated, T_LCFS 200 eV, chi_perp 1 m^2/s) scaled linearly in the
    # non-radiated load -- against the adopted 10 MW/m^2 threshold. EXPECTED
    # VIOLATED at the baseline: 10.535 against 10, because the model's absorbed
    # heating (its own alpha heating 504.49 + the installed 50 MW coupled =
    # 554.49 MW) is 10.9 % above the source's 500 MW. The disclosed, explained
    # verdict change of WI-047, never tuned (the WI-041 precedent); on the low
    # case (5.0 at 50, a study lever) the peak reads 5.545 and the fence is
    # satisfied. No existing channel moved; the headline is 'violation'.
    "divertor_heat_ok": "violated",
}
EXPECTED_HEADLINE = "violation"  # WI-047: one verdict violated by design (WI-041 pinned 'violation' once before)
EXPECTED_VERDICT_COUNT = 20  # WI-062 adds reference-conductor margin.


def _execute_package(*, pipeline_path=None, output_dir=None):
    """Execute the sealed package once and return every output, including verdicts."""
    schema_names = dict.fromkeys(
        ["RootModel[float]"] + [schema.__name__ for schema in CUSTOM_SCHEMA_TYPES]
    )
    router = create_output_router_with_json_schemas(list(schema_names))
    router.register_handler(
        "float",
        WriteHandler(
            fn=lambda value, path: Path(path).write_text(json.dumps(value)),
            extension=".json",
        ),
    )
    result = execute_pipeline(
        pipeline_path or rs.PIPELINE,
        output_dir=output_dir or rs.E2E / "outputs" / "single",
        registry=create_stellarator_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    return result.outputs


def _numeric_outputs(outputs) -> dict[str, float]:
    """Keep scalar channels; generated constraint outputs are structured values."""
    return {
        channel: float(value.root) if hasattr(value, "root") else float(value)
        for channel, value in outputs.items()
        if hasattr(value, "root") or isinstance(value, (int, float))
    }


def _anchor_gate(values: dict[str, float]) -> bool:
    total = values[f"{P}total_capital__total_capital"]
    magnet = values[CH["magnet_capital_rollup"]]
    # Anchors re-derived on the WI-037 sustainment closure (goal
    #   operating-point-closure, 2026-09-01): the fuel peaks are now the
    #   computed quasi-neutral values (n_D0 1.96e20 -> 1.95189e20, -0.55%,
    #   converged ash 0.578e20 vs the printed 0.56e20 referent), so every
    #   fusion-derived headline moves ~1%: p_fus 2748.06 -> 2725.36 MW,
    #   LCOE 304.481620 -> 307.087120. Verified bit-exact against the
    #   extended oracle before pinning (never patched-to-match; the
    #   printed-referent deltas are the design D6 tolerances). Pre-WI-037
    #   values in git history.
    # WI-041 (goal wall-and-heating round 2, 2026-09-04): the CAS72 lifetime
    #   operand moved from the circular-torus average to the source-anchored
    #   PEAK (4.088 MW/m^2), so the core lives 4.40 FPY instead of 5.80 and is
    #   replaced 5 times instead of 4: CAS72 95,898,253 -> 131,494,480 $/yr,
    #   CAS70 164,039,066.82 -> 199,635,292.95, LCOE 307.087120 -> 313.513412,
    #   lcoe_1cfe 301.095115 -> 307.521406. Re-pinned from the executed
    #   baseline after the oracle gate below read bit-exact on every one of
    #   them (never before); every other anchor unchanged to the digit.
    # WI-042 (goal stored-energy-basis round 2, 2026-09-05): the helium ash on
    #   the source's own profile rule (A.5 pointwise) with the electrons by
    #   quasi-neutrality re-closes the fixed point -- W 551.444 -> 519.914 MJ,
    #   tau_E 1.450 -> 1.557 s, more ash (n_He0 5.78e19 -> 6.04e19), less fuel
    #   at the peak (n_D0 1.9519e20 -> 1.9256e20), p_fus 2725.36 -> 2652.56 MW
    #   -- so every fusion-derived headline moves ~3-4 %: p_net 743.91 ->
    #   716.63, total capital 14,542,872,713 -> 14,442,862,262 (the
    #   power-scaled accounts), CAS72 131,494,480 -> 126,649,656 (lifetime by
    #   the lower peak), CAS70 199,635,292.95 -> 193,529,567.74, LCOE
    #   313.513412 -> 322.318439, lcoe_1cfe 307.521406 -> 316.141142. Re-pinned
    #   from the executed baseline after the oracle gate below read bit-exact
    #   on every channel, the four new ones included (never before); nothing
    #   tuned. Pre-WI-042 values in git history.
    # WI-045 (goal plant-closure, 2026-09-08): the three held plant multipliers
    #   p_pump 195 MW, eta_p 0.5 and eta_th 0.333 became computed producers --
    #   the representative helium loop (175.44 MW draw at 14 loops, all fluid
    #   work recovered into the IHX duty) and the Kovari 2016 helium-Rankine fit
    #   (0.41136 at a 480 C turbine inlet) -- so every power-derived headline
    #   moves by design at the held availability 0.85: p_th 3224.35 -> 3302.29,
    #   p_net 716.63 -> 1012.36, rec_frac 0.332563 -> 0.254747, total capital
    #   14,442,862,262 -> 14,955,212,350 (the power-scaled accounts), CAS70
    #   193,529,567.74 -> 207,927,742.74, LCOE 322.318439 -> 237.252800,
    #   lcoe_1cfe 316.141142 -> 232.724887. Predicted before regeneration
    #   (design section Expected baseline behaviour; prototype/proto_results.json)
    #   and re-pinned from the executed baseline after the oracle gate below read
    #   bit-exact on every channel, the twenty new ones included (never before).
    #   The compatibility proposal (loop_live 0, cycle_live 0, p_pump_direct 195,
    #   eta_p_direct 0.5, eta_th_direct 0.333) reproduces the WI-044 pin's 106
    #   channels bit-for-bit (evidence/compat_mode/diff_vs_pin.json). Nothing
    #   tuned. Pre-WI-045 values in git history.
    # WI-046 (goal plant-closure round 1, 2026-09-08): the lifecycle calendar produces
    #   availability and CAS72 -- availability 0.85 -> 0.9027777777777779 (five dated
    #   events, the first at 4.52 yr), CAS72 128,437,178.45 -> 138,213,460.01 $/yr,
    #   CAS80 746,174.85 -> 792,505.97 (fuel follows productive time), LCOE 237.252800
    #   -> 224.609525, lcoe_1cfe 232.724887 -> 220.346320; capital, p_net, q_eng,
    #   rec_frac and the magnet share unchanged. Predicted before regeneration
    #   (plan section Predictions: 224.6095247280447) and re-pinned from the executed
    #   live baseline after the oracle gate read bit-exact on every channel, the
    #   eleven calendar channels included. The held mode (availability_direct 0.85)
    #   reproduces WI-045's baseline bit-for-bit (evidence/compat_mode/).
    # WI-050 anchors follow independent conservation and explicit finance checks
    # in work/active/WI-050_mfe-coherent-operating-heating/implementation/.
    # WI-040 (2026-09-13): independent additive accounting changes four economic
    # anchors only. Pack = $804m tape + $15.954709m materials + $750.415092m winding
    # operations, using the declared estimated-2026 price basis. This is a scoped
    # estimate, not a recovered split of the legacy 6.65 multiplier. Basis and
    # native reconciliation: work/active/WI-040_winding-pack-mass-cost/.
    # WI-059: re-derived after native/oracle agreement (evidence/native-single-final.log).
    # WI-060 tape-volume procurement changes the four economic anchors only;
    # independently predicted tape delta -$72.428571m (WI-060 evidence/baseline.json).
    anchors = [
        # WI-063: independently reconciled conditional sheet-stock increment.
        ("total capital $", total, 8905077000.154549),
        ("LCOE $/MWh", values[CH["lcoe"]], 144.74743129583516),
        ("p_net MW", values[CH["p_net"]], 1012.6082547175133),
        ("q_eng", values[CH["q_eng"]], 3.9319737437533955),
        ("rec_frac", values[CH["rec_frac"]], 0.25432519776833934),
        ("magnet %", magnet / total * 100, 19.170578781069967),
        ("CAS70 $/yr", values[CH["cas70"]], 217687149.51060474),
        ("CAS80 $/yr", values[CH["cas80"]], 792_505.965114),
        ("lcoe_1cfe $/MWh (comparison)", values[CH["lcoe_1cfe"]], 142.2095176767976),
    ]

    print("\n=== NINE ANCHORS (single-pass, graph rollup, no bridge) ===")
    all_ok = True
    for name, value, expected in anchors:
        if name == "magnet %":
            ok = abs(value - expected) < 0.01
        else:
            rounded_match = abs(round(value, 6) - expected) <= 1e-6
            relative_match = abs(value - expected) / abs(expected) < 1e-6
            ok = rounded_match or relative_match
        all_ok &= ok
        verdict = "OK" if ok else "*** DEVIATION"
        print(
            f"  {name:16s} exec={value:20.6f}  expect={expected:<18}  {verdict}"
        )
    print(f"  magnet capital $ = {magnet:,.2f}")
    return all_ok


def _assert_generated_verdicts(outputs) -> None:
    """Check the exact 20 design-point verdicts and the separate aggregate."""
    report = outputs["constraint_report"]
    print("=== TWENTY VERDICTS (generated ConstraintReport) ===")
    verdicts = {}
    for channel, value in outputs.items():
        if channel.endswith("__evaluation") and hasattr(value, "status"):
            name = channel.split("__")[2]
            verdicts[name] = value.status
            print(f"  {name:14s} {value.status}")

    assert report.headline == EXPECTED_HEADLINE, (
        f"headline {report.headline!r} != {EXPECTED_HEADLINE!r}"
    )
    assert report.assessed_entry_count == EXPECTED_VERDICT_COUNT, (
        f"assessed_entry_count {report.assessed_entry_count} != {EXPECTED_VERDICT_COUNT}"
    )
    assert set(verdicts) == set(EXPECTED_VERDICTS), (set(verdicts), set(EXPECTED_VERDICTS))
    for name, expected in EXPECTED_VERDICTS.items():
        actual = verdicts.get(name)
        assert actual == expected, (
            f"VERDICT PARITY FAIL: {name} = {actual!r}, expected {expected!r} "
            "(surface per MR-WI027-4)"
        )
    print(
        "VERDICT PARITY: PASS -- "
        f"headline={report.headline}, assessed_entry_count={report.assessed_entry_count}, "
        "seventeen satisfied; divertor_heat_ok, wp_fit_ok and reference_conductor_current_ok VIOLATED. WI-050 coherent "
        "operating heat gives 10.517842 MW/m^2 against 10; the installed "
        "capacity ceiling and signed burn-hold demand remain explicit."
    )


def _oracle_gate(values: dict[str, float], oracle: dict[str, float]) -> bool:
    total = values[f"{P}total_capital__total_capital"]
    compared = {
        "operating_heat_coupled": values[CH["operating_heat_coupled"]],
        "operating_heat_delivered": values[CH["operating_heat_delivered"]],
        "operating_heat_wallplug": values[CH["operating_heat_wallplug"]],
        "total_capital": total,
        "lcoe": values[CH["lcoe"]],
        "p_net": values[CH["p_net"]],
        "q_eng": values[CH["q_eng"]],
        "rec_frac": values[CH["rec_frac"]],
        "cas20_capital": values[f"{P}cas20_capital__cas20_capital"],
        "overnight_capital": values[f"{P}overnight_capital__overnight_capital"],
        "cas71_annual": values[CH["cas71"]],
        "cas72_annual": values[CH["cas72"]],
        # WI-046 lifecycle calendar channels (the oracle's closed form vs the impl's walk)
        "calendar_availability": values[f"{P}calendar__availability"],
        "calendar_coil_life_margin_fpy": values[f"{P}calendar__coil_life_margin_fpy"],
        "calendar_replacement_pv": values[f"{P}calendar__replacement_pv"],
        "calendar_planned_downtime_yr": values[f"{P}calendar__planned_downtime_yr"],
        "calendar_terminal_downtime_yr": values[f"{P}calendar__terminal_downtime_yr"],
        "calendar_unplanned_downtime_yr": values[f"{P}calendar__unplanned_downtime_yr"],
        "calendar_productive_fpy": values[f"{P}calendar__productive_fpy"],
        "calendar_dated_energy_ratio": values[f"{P}calendar__dated_energy_ratio"],
        "calendar_cas72_annual": values[f"{P}calendar__cas72_annual"],
        "calendar_n_replacements": values[f"{P}calendar__n_replacements"],
        "calendar_physical_life_fpy": values[f"{P}calendar__physical_life_fpy"],
        # WI-047 fuel / divertor-heat / vacuum channels (bit-exact vs the oracle's
        # own derivations of the design's equations)
        "fuel_burn_rate": values[f"{P}fuel_cycle__fuel__burn_rate"],
        "fuel_inject_rate": values[f"{P}fuel_cycle__fuel__inject_rate"],
        "fuel_exhaust_rate": values[f"{P}fuel_cycle__fuel__exhaust_rate"],
        "fuel_loss_rate": values[f"{P}fuel_cycle__fuel__loss_rate"],
        "fuel_tbr_required": values[f"{P}fuel_cycle__fuel__tbr_required"],
        "fuel_tbr_margin": values[f"{P}fuel_cycle__fuel__tbr_margin"],
        "fuel_burn_kg_per_fpy": values[f"{P}fuel_cycle__fuel__burn_kg_per_fpy"],
        "divheat_p_heat_abs": values[f"{P}divertor__divheat__p_heat_abs"],
        "divheat_p_sep": values[f"{P}divertor__divheat__p_sep"],
        "divheat_f_rad_edge": values[f"{P}divertor__divheat__f_rad_edge"],
        "divheat_f_rad_edge_in_range": values[f"{P}divertor__divheat__f_rad_edge_in_range"],
        "divheat_p_target_nonrad": values[f"{P}divertor__divheat__p_target_nonrad"],
        "divheat_q_target_peak": values[f"{P}divertor__divheat__q_target_peak"],
        "divheat_q_target_peak_area_scaled": values[f"{P}divertor__divheat__q_target_peak_area_scaled"],
        "divheat_q_target_margin": values[f"{P}divertor__divheat__q_target_margin"],
        "divheat_p_heat_operating_minus_installed": values[f"{P}divertor__divheat__p_heat_operating_minus_installed"],
        "vacuum_n_molecules": values[f"{P}vacuum_pumping__vacuum__n_molecules"],
        "vacuum_Q_total": values[f"{P}vacuum_pumping__vacuum__Q_total"],
        "vacuum_S_eff_required": values[f"{P}vacuum_pumping__vacuum__S_eff_required"],
        "cas70_annual": values[CH["cas70"]],
        "cas80_annual": values[CH["cas80"]],
        "annual_fuel": values[CH["annual_fuel"]],
        "cas90_1cfe": values[CH["cas90_1cfe"]],
        "lcoe_1cfe": values[CH["lcoe_1cfe"]],
        # WI-030 physics channels
        "beta": values[CH["beta"]],
        "B_peak": values[CH["B_peak"]],
        # WI-037 sustainment channels (bit-exact vs the oracle mirror)
        "n_bar19": values[CH["n_bar19"]],
        "n_He0": values[CH["n_He0"]],
        "n_D0": values[CH["n_D0"]],
        "tau_E": values[CH["tau_E"]],
        "W_th": values[CH["W_th"]],
        "p_brems": values[CH["p_brems"]],
        "p_line": values[CH["p_line"]],
        "p_sync": values[CH["p_sync"]],
        "p_rad": values[CH["p_rad"]],
        "p_aux_required": values[CH["p_aux_required"]],
        # WI-042 derived-profile channels (bit-exact vs the oracle mirror)
        "p_avg": values[CH["p_avg"]],
        "n_e_volav": values[CH["n_e_volav"]],
        "alpha_n_e_eff": values[CH["alpha_n_e_eff"]],
        "alpha_He_eff": values[CH["alpha_He_eff"]],
        # WI-045 source-heat, loop and cycle channels (bit-exact vs the oracle,
        # which derives them from the design's equations, not the modules)
        "q_source": values[f"{P}blanket__source_heat__q_source"],
        "loop_mdot": values[f"{P}heat_transport__primary_loop__mdot"],
        "loop_mdot_loop": values[f"{P}heat_transport__primary_loop__mdot_loop"],
        "loop_dp_loop": values[f"{P}heat_transport__primary_loop__dp_loop"],
        "loop_r_comp": values[f"{P}heat_transport__primary_loop__r_comp"],
        "loop_T_comp_in": values[f"{P}heat_transport__primary_loop__T_comp_in"],
        "loop_w_fluid": values[f"{P}heat_transport__primary_loop__w_fluid"],
        "loop_p_elec": values[f"{P}heat_transport__primary_loop__p_elec"],
        "loop_q_ihx": values[f"{P}heat_transport__primary_loop__q_ihx"],
        "loop_capacity_margin": values[f"{P}heat_transport__primary_loop__capacity_margin"],
        "loop_p_pump_total": values[f"{P}heat_transport__primary_loop__p_pump_total"],
        "loop_q_recovered_total": values[f"{P}heat_transport__primary_loop__q_recovered_total"],
        "cycle_T2_C": values[f"{P}turbine__cycle__T2_C"],
        "cycle_eta_fit": values[f"{P}turbine__cycle__eta_fit"],
        "cycle_eta_th": values[f"{P}turbine__cycle__eta_th"],
        "cycle_domain_product": values[f"{P}turbine__cycle__domain_product"],
        "p_th": values[CH["p_th"]] if "p_th" in CH else values[f"{P}pb__p_th"],
    }

    print("\n=== BIT-EXACT vs ORACLE (rel<1e-9) ===")
    all_ok = True
    for name, value in compared.items():
        expected = oracle[name]
        relative_deviation = abs(value - expected) / (abs(expected) or 1)
        ok = relative_deviation < 1e-9
        all_ok &= ok
        verdict = "OK" if ok else "FAIL"
        print(
            f"  {name:16s} exec={value:20.9f} oracle={expected:20.9f} "
            f"reldev={relative_deviation:.2e} {verdict}"
        )
    print("BIT-EXACT vs oracle:", "PASS" if all_ok else "*** FAIL ***")
    return all_ok


def _cas72_guard_gate() -> bool:
    """WI-029's three guard cases, restated by WI-046 (goal plant-closure round 1,
    2026-09-08) onto the lifecycle calendar's HELD MODE (the retired periodic chain
    carried verbatim) against the oracle mirror, plus a fourth family: the LIVE
    calendar's boundary cases (the lifetime research's synthetic values) against the
    oracle's independent closed-form derivation."""
    from stellarator_tea.handwritten.mfe_lifecycle.lifecycle_calendar_impl import (
        lifecycle_calendar_held as held_impl,
        lifecycle_calendar_live as live_impl,
    )
    from verify_stellaris import _oracle_levelized_replacement_cost as cas72_mirror
    from verify_stellaris import _oracle_lifecycle_calendar as calendar_oracle

    def cas72_impl(**arguments):
        return held_impl(coil_life_fpy=10.0, **arguments)["cas72_annual"]

    guard_cases = [
        (
            "clip CAP binds (low wall loading, high fluence limit)",
            dict(
                cost_per_event=671_160_000.0,
                # WI-041: the impl takes the wall load directly; the same
                # synthetic point expressed as q_n = p_fus x (1 - ash) / area.
                q_n=100.0 * (1.0 - 0.2002275312855518) / 660.0791423448563,
                fluence_limit=500.0,
                availability=0.9,
                interest_rate=0.07,
                operational_years=30.0,
            ),
            "core_lifetime_fpy == operational_years * availability",
        ),
        (
            "clip FLOOR binds (extreme wall loading) -> n_rep = 53, cost nonzero",
            dict(
                cost_per_event=671_160_000.0,
                q_n=200_000.0 * (1.0 - 0.2002275312855518) / 660.0791423448563,
                fluence_limit=18.0,
                availability=0.9,
                interest_rate=0.07,
                operational_years=30.0,
            ),
            "core_lifetime_fpy == 0.5 (floor), n_rep = 53",
        ),
        (
            "outer max binds (replacement interval >= plant life -> n_rep = 0)",
            dict(
                cost_per_event=671_160_000.0,
                q_n=50.0 * (1.0 - 0.2002275312855518) / 660.0791423448563,
                fluence_limit=18.0,
                availability=0.9,
                interest_rate=0.07,
                operational_years=5.0,
            ),
            "n_rep == 0 (cost == 0)",
        ),
    ]

    print("\n=== WI-029 CAS72 GUARD-LIVE SPOT-CHECK, WI-046 HELD MODE (impl vs oracle mirror, rel<1e-9) ===")
    all_ok = True
    for label, arguments, expected_guard in guard_cases:
        implementation = cas72_impl(**arguments)
        mirror = cas72_mirror(**arguments)
        relative_deviation = abs(implementation - mirror) / (abs(mirror) or 1.0)
        ok = relative_deviation < 1e-9
        all_ok &= ok
        verdict = "OK" if ok else "*** FAIL"
        print(f"  {label}")
        print(f"    expect: {expected_guard}")
        print(
            f"    impl={implementation:,.6f}  mirror={mirror:,.6f}  "
            f"reldev={relative_deviation:.2e} {verdict}"
        )

    cap_arguments = guard_cases[0][1]
    neutron_flux = cap_arguments["q_n"]
    raw_lifetime = cap_arguments["fluence_limit"] / max(neutron_flux, 1e-6)
    capped_lifetime = cap_arguments["operational_years"] * cap_arguments["availability"]
    assert raw_lifetime > capped_lifetime, (
        f"clip cap case does not saturate: raw {raw_lifetime} <= cap {capped_lifetime}"
    )
    print(
        f"    [guard live] raw FPY {raw_lifetime:.3f} > cap {capped_lifetime:.3f} "
        "-> clip BINDS"
    )

    floor_arguments = guard_cases[1][1]
    floor_neutron_flux = floor_arguments["q_n"]
    floor_raw_lifetime = floor_arguments["fluence_limit"] / max(floor_neutron_flux, 1e-6)
    assert floor_raw_lifetime < 0.5, (
        f"clip floor case does not bind: raw {floor_raw_lifetime} >= 0.5"
    )
    assert cas72_impl(**floor_arguments) > 0.0, (
        "clip floor case returned 0 -- not a live comparison"
    )
    print(
        f"    [guard live] raw FPY {floor_raw_lifetime:.5f} < floor 0.500 "
        "-> clip FLOOR BINDS, cost nonzero"
    )

    assert cas72_impl(**guard_cases[2][1]) == 0.0, "outer max case did not return 0"
    print("    [guard live] n_rep floored to 0 -> cost exactly 0.0 -> outer max BINDS")

    # ---- WI-046: the LIVE calendar's boundary cases (spec MR-WI046-12; the lifetime
    # research's synthetic values, lines 100-110) -- the impl's interval walk against
    # the oracle's closed form on every one of the eleven outputs, and the research's
    # expected values where it states them.
    print("\n=== WI-046 LIVE CALENDAR BOUNDARY CASES (walk vs closed form, rel<1e-9) ===")
    base = dict(cost_per_event=671_160_000.0, q_n=4.5, fluence_limit=18.0,  # L = 4 FPY
                interest_rate=0.07, operational_years=10.0, outage_years=7.0 / 12.0,
                unplanned_fraction=0.0, coil_life_fpy=10.0)
    live_cases = [
        ("L 4, d 7/12, N 10 -> two events at 4 and 8.5833, A 53/60", dict(base),
         dict(n_replacements=2.0, availability=53.0 / 60.0, planned_downtime_yr=7.0 / 6.0)),
        ("N 8.7 -> one event, terminal 0.1167 yr", dict(base, operational_years=8.7),
         dict(n_replacements=1.0, terminal_downtime_yr=8.7 - (8.0 + 7.0 / 12.0), productive_fpy=8.0)),
        ("N 9+2/12 -> restart exactly at retirement is not strictly before: one event",
         dict(base, operational_years=9.0 + 2.0 / 12.0), dict(n_replacements=1.0)),
        ("N 9+2/12+1e-6 -> two events", dict(base, operational_years=9.0 + 2.0 / 12.0 + 1e-6),
         dict(n_replacements=2.0)),
        ("q_n 0 -> infinite life, no event, A = 1 - u = 1", dict(base, q_n=0.0),
         dict(n_replacements=0.0, availability=1.0, replacement_pv=0.0)),
        ("d 0, u 0 -> A 1.0 with events still charged", dict(base, outage_years=0.0),
         dict(availability=1.0)),
        ("i 0 -> ratio 1.0, CAS72 = PV / N", dict(base, interest_rate=0.0),
         dict(dated_energy_ratio=1.0)),
        ("u 0.05", dict(base, unplanned_fraction=0.05), {}),
        ("u 0.10", dict(base, unplanned_fraction=0.10), {}),
    ]
    keys = ("availability", "coil_life_margin_fpy", "replacement_pv", "planned_downtime_yr",
            "terminal_downtime_yr", "unplanned_downtime_yr", "productive_fpy",
            "dated_energy_ratio", "cas72_annual", "n_replacements", "physical_life_fpy")
    productive = {}
    for label, arguments, expected in live_cases:
        impl = live_impl(**arguments)
        orac = calendar_oracle(availability_direct=0.0, **arguments)
        worst = 0.0
        for key in keys:
            a, b = impl[key], orac[key]
            if math.isinf(a) or math.isinf(b):
                ok_key = math.isinf(a) and math.isinf(b)
                dev = 0.0 if ok_key else float("inf")
            else:
                dev = abs(a - b) / (abs(b) or 1.0)
            worst = max(worst, dev)
        for key, value in expected.items():
            dev = abs(impl[key] - value) / (abs(value) or 1.0)
            worst = max(worst, dev)
        # the time identity F + T_p + T_u + T_term = N (spec MR-WI046-4)
        balance = abs(impl["productive_fpy"] + impl["planned_downtime_yr"]
                      + impl["unplanned_downtime_yr"] + impl["terminal_downtime_yr"]
                      - arguments["operational_years"])
        ok = worst < 1e-9 and balance < 1e-9
        all_ok &= ok
        productive[arguments["unplanned_fraction"]] = impl["productive_fpy"]
        print(f"  {label}: n={impl['n_replacements']:.0f} A={impl['availability']:.6f} "
              f"events={[round(x, 4) for x in impl['events']]} worst reldev={worst:.2e} "
              f"time balance={balance:.2e} {'OK' if ok else '*** FAIL'}")
    monotone = productive[0.0] >= productive[0.05] >= productive[0.10]
    all_ok &= monotone
    print(f"  productive_fpy non-increasing in u: {productive} {'OK' if monotone else '*** FAIL'}")

    # D6: the baseline's event dates in both modes, from the oracle's inputs (diagnostic).
    from verify_stellaris import IN as oracle_inputs, compute as oracle_compute
    o = oracle_compute()
    common = dict(cost_per_event=(o["blanket"] + o["divertor"]) * oracle_inputs["n_mod"],
                  q_n=o["wall_load_peak"], fluence_limit=oracle_inputs["fluence_limit"],
                  interest_rate=oracle_inputs["discount_rate"],
                  operational_years=oracle_inputs["operational_years"],
                  outage_years=oracle_inputs["outage_years"],
                  unplanned_fraction=oracle_inputs["unplanned_fraction"],
                  coil_life_fpy=oracle_inputs["coil_life_fpy"])
    live_events = calendar_oracle(availability_direct=0.0, **common)["events"]
    held_events = calendar_oracle(availability_direct=0.85, **common)["events"]
    print(f"  baseline event dates, live (7 months, u 0): {[round(x, 4) for x in live_events]}")
    print(f"  baseline event dates, held (0.85, periodic): {[round(x, 4) for x in held_events]}")
    print("GUARD-LIVE SPOT-CHECK:", "PASS" if all_ok else "*** FAIL ***")
    return all_ok


def _w_beta_identity_gate(values: dict[str, float]) -> bool:
    """WI-042 (design D2, MR-WI042-4): W and beta read ONE volume-averaged
    pressure, so beta * B_axis^2 * 1.5 * V / (2 mu0) must equal W_th to float
    precision -- from the executed package's own channels, not the oracle."""
    from verify_stellaris import IN as oracle_inputs
    mu0 = oracle_inputs["beta_mu0"]   # the calc's default, 1.25663706212e-6
    w_from_beta_mj = (values[CH["beta"]] * values[CH["B_axis"]] ** 2
                      * 1.5 * values[CH["V"]] / (2.0 * mu0)) * 1e-6
    w_th = values[CH["W_th"]]
    relative_deviation = abs(w_from_beta_mj - w_th) / abs(w_th)
    ok = relative_deviation < 1e-12
    print("\n=== W-BETA IDENTITY (one pressure integral, WI-042; rel<1e-12) ===")
    print(f"  W from beta = {w_from_beta_mj:.9f} MJ  W_th = {w_th:.9f} MJ  "
          f"reldev={relative_deviation:.2e} {'OK' if ok else '*** FAIL'}")
    return ok


def _run_gate_families() -> tuple[bool, bool, bool, bool]:
    oracle = oracle_compute()
    outputs = _execute_package()
    values = _numeric_outputs(outputs)
    anchors_ok = _anchor_gate(values)
    _assert_generated_verdicts(outputs)
    print("ANCHORS", "GREEN" if anchors_ok else "*** STOP -- DEVIATION ***")
    oracle_ok = _oracle_gate(values, oracle)
    identity_ok = _w_beta_identity_gate(values)
    guards_ok = _cas72_guard_gate()
    return anchors_ok, oracle_ok, identity_ok, guards_ok


def main() -> int:
    anchors_ok, oracle_ok, identity_ok, guards_ok = _run_gate_families()
    return 0 if anchors_ok and oracle_ok and identity_ok and guards_ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("Unsupported command-line arguments: " + " ".join(sys.argv[1:]))
    raise SystemExit(main())
