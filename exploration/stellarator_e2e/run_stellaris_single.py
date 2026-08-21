"""Single-pass stellarator runner: the sealed package at its authored design point.

The cross-part capital rollup is compiled by codegen and computed in one teax-simkit
pass. The package is strict-loaded with no harness glue. This demo/regression command
checks recorded anchors, all five generated verdicts, numerical agreement with the
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
    "wall_load_ok": "satisfied",
}


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
    magnet = values[CH["magnet"]]
    anchors = [
        ("total capital $", total, 16_129_706_216.04),
        ("LCOE $/MWh", values[CH["lcoe"]], 275.264220),
        ("p_net MW", values[CH["p_net"]], 915.081088),
        ("q_eng", values[CH["q_eng"]], 6.606662),
        ("rec_frac", values[CH["rec_frac"]], 0.151362),
        ("magnet %", magnet / total * 100, 39.203876),
        ("CAS70 $/yr", values[CH["cas70"]], 170_974_516.955938),
        ("CAS80 $/yr", values[CH["cas80"]], 773_037.517724),
        ("lcoe_1cfe $/MWh (comparison)", values[CH["lcoe_1cfe"]], 269.861538),
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
    """The model's five design-point verdicts remain a separate assertion gate."""
    report = outputs["constraint_report"]
    print("=== FIVE VERDICTS (generated ConstraintReport) ===")
    verdicts = {}
    for channel, value in outputs.items():
        if channel.endswith("__evaluation") and hasattr(value, "status"):
            name = channel.split("__")[2]
            verdicts[name] = value.status
            print(f"  {name:14s} {value.status}")

    assert report.headline == "full_satisfaction", (
        f"headline {report.headline!r} != full_satisfaction"
    )
    assert report.assessed_entry_count == 5, (
        f"assessed_entry_count {report.assessed_entry_count} != 5"
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
        "all five == satisfied"
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
                p_fus=100.0,
                ash_frac=0.2002275312855518,
                firstwall_area=660.0791423448563,
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
                p_fus=200_000.0,
                ash_frac=0.2002275312855518,
                firstwall_area=660.0791423448563,
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
                p_fus=50.0,
                ash_frac=0.2002275312855518,
                firstwall_area=660.0791423448563,
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
    neutron_power = cap_arguments["p_fus"] * (1 - cap_arguments["ash_frac"])
    neutron_flux = neutron_power / cap_arguments["firstwall_area"]
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
    floor_neutron_power = floor_arguments["p_fus"] * (1 - floor_arguments["ash_frac"])
    floor_neutron_flux = floor_neutron_power / floor_arguments["firstwall_area"]
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


def _run_gate_families() -> tuple[bool, bool, bool]:
    oracle = oracle_compute()
    outputs = _execute_package()
    values = _numeric_outputs(outputs)
    anchors_ok = _anchor_gate(values)
    _assert_generated_verdicts(outputs)
    print("ANCHORS", "GREEN" if anchors_ok else "*** STOP -- DEVIATION ***")
    oracle_ok = _oracle_gate(values, oracle)
    guards_ok = _cas72_guard_gate()
    return anchors_ok, oracle_ok, guards_ok


def main() -> int:
    anchors_ok, oracle_ok, guards_ok = _run_gate_families()
    return 0 if anchors_ok and oracle_ok and guards_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
