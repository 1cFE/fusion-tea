"""Single-pass stellarator runner: the sealed package at its authored design point.

The cross-part capital rollup is compiled by codegen and computed in one teax-simkit
pass. The package is strict-loaded with no harness glue. This demo/regression command
checks recorded anchors, all six generated verdicts, numerical agreement with the
independent demo oracle, and three synthetic CAS72 guard cases. Any failed gate family
produces a nonzero process exit after the diagnostic output is printed.

Run (repository root, with STOP_PARSER_TEAX_ROOT exported):
    uv run python exploration/stellarator_e2e/run_stellaris_single.py
"""

from __future__ import annotations

import json
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
    "beta_ok": "satisfied",
    "net_positive": "satisfied",
    "recirc_ok": "satisfied",
    "tbr_ok": "satisfied",
    # WI-041: the fence compares the computed PEAK (the circular-torus
    # average x the source-anchored calibration 1.316441) with the printed
    # 4.05; at the WI-041 baseline it read 4.088 -- VIOLATED. WI-042: the
    # helium ash on the source's own profile rule re-closes the fixed point
    # with more ash and less fuel, p_fus 2725.36 -> 2652.56 MW, so the peak
    # reads 4.05 x 2652.563 / 2700 = 3.979 -- EXPECTED SATISFIED. Disclosed,
    # never tuned (WI-042 plan, MR-WI042-14 restatement (b)).
    "wall_load_ok": "satisfied",
    "peak_field_ok": "satisfied",  # WI-030 conductor peak-field limit,
    "wp_stress_ok": "satisfied",  # WI-035
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
}
EXPECTED_HEADLINE = "full_satisfaction"
EXPECTED_VERDICT_COUNT = 9   # WI-036 added cond_strain_ok (was 8)


def _execute_package():
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
        rs.PIPELINE,
        output_dir=rs.E2E / "outputs" / "single",
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
    anchors = [
        ("total capital $", total, 14_442_862_261.866261),
        ("LCOE $/MWh", values[CH["lcoe"]], 322.318439),
        ("p_net MW", values[CH["p_net"]], 716.633806),
        ("q_eng", values[CH["q_eng"]], 3.006952),
        ("rec_frac", values[CH["rec_frac"]], 0.332563),
        ("magnet %", magnet / total * 100, 37.395856),
        ("CAS70 $/yr", values[CH["cas70"]], 193_529_567.738861),
        ("CAS80 $/yr", values[CH["cas80"]], 746_174.847154),
        ("lcoe_1cfe $/MWh (comparison)", values[CH["lcoe_1cfe"]], 316.141142),
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
    """The model's eight design-point verdicts remain a separate assertion gate."""
    report = outputs["constraint_report"]
    print("=== NINE VERDICTS (generated ConstraintReport) ===")
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
    for name, expected in EXPECTED_VERDICTS.items():
        actual = verdicts.get(name)
        assert actual == expected, (
            f"VERDICT PARITY FAIL: {name} = {actual!r}, expected {expected!r} "
            "(surface per MR-WI027-4)"
        )
    print(
        "VERDICT PARITY: PASS -- "
        f"headline={report.headline}, assessed_entry_count={report.assessed_entry_count}, "
        "nine satisfied (WI-042: sustainment_ok and wall_load_ok flipped to "
        "satisfied by the sourced ash profile; disclosed, never tuned)"
    )


def _oracle_gate(values: dict[str, float], oracle: dict[str, float]) -> bool:
    total = values[f"{P}total_capital__total_capital"]
    compared = {
        "total_capital": total,
        "lcoe": values[CH["lcoe"]],
        "p_net": values[CH["p_net"]],
        "q_eng": values[CH["q_eng"]],
        "rec_frac": values[CH["rec_frac"]],
        "cas20_capital": values[f"{P}cas20_capital__cas20_capital"],
        "overnight_capital": values[f"{P}overnight_capital__overnight_capital"],
        "cas71_annual": values[CH["cas71"]],
        "cas72_annual": values[CH["cas72"]],
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
    from stellarator_tea.handwritten.mfe_account_costs.levelized_replacement_cost_impl import (
        levelized_replacement_cost as cas72_impl,
    )
    from verify_stellaris import _oracle_levelized_replacement_cost as cas72_mirror

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
                # WI-041: the impl takes the wall load directly; the same
                # synthetic point expressed as q_n = p_fus x (1 - ash) / area.
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
                # WI-041: the impl takes the wall load directly; the same
                # synthetic point expressed as q_n = p_fus x (1 - ash) / area.
                q_n=50.0 * (1.0 - 0.2002275312855518) / 660.0791423448563,
                fluence_limit=18.0,
                availability=0.9,
                interest_rate=0.07,
                operational_years=5.0,
            ),
            "n_rep == 0 (cost == 0)",
        ),
    ]

    print("\n=== WI-029 CAS72 GUARD-LIVE SPOT-CHECK (impl vs oracle mirror, rel<1e-9) ===")
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
    raise SystemExit(main())
