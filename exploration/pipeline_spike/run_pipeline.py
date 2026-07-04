"""WI-013 execution harness: run the generated solar_battery pipeline through
the teax executor and assert numeric outputs against hand-computed expectations.

Expectations are derived by hand from the SysML expressions in
tests/fixtures/solar_battery_model/library.sysml + design values in design.sysml.
Full arithmetic in findings.md.

Run:  .venv-exec/bin/python run_pipeline.py   (venv has teax-simkit editable)
"""

import sys
from pathlib import Path

SPIKE = Path(__file__).parent

# Make the generated package importable as `solar_battery_tea`
# (generation wrote into generated/; the package expects its own name on sys.path)
pkg_dir = SPIKE / "pkg"
pkg_dir.mkdir(exist_ok=True)
link = pkg_dir / "solar_battery_tea"
if not link.exists():
    link.symlink_to(SPIKE / "generated")
sys.path.insert(0, str(pkg_dir))

from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    create_output_router_with_json_schemas,
)

from solar_battery_tea import (  # noqa: E402
    DesignParams,
    LibraryParams,
    SystemDesign,
    create_solar_battery_tea_registry,
)

# ---------------------------------------------------------------------------
# Hand-computed expectations (all exact per SysML expressions; see findings.md)
# ---------------------------------------------------------------------------
# total_cost = material * (1 + 0.45 + 0.30) = material * 1.75 for hardware parts
EXPECTED = {
    # Solar array: 20 PV modules (400W * 1.07 $/W), 4 inverters (2000W * 0.286),
    # array BOS (4*150 + 20*30), allocation (25*0.5 + 25*0.3 + 50*2.0)
    "SolarBatteryDesign__solar_battery_plant__solar_array__capital_cost__capital_cost": 21204.0,
    # Battery: 8 packs (5 kWh * 171.5 * 1.0), hybrid inverter (10000 * 0.1714),
    # battery BOS (8 * 71.5)
    "SolarBatteryDesign__solar_battery_plant__battery_system__capital_cost__capital_cost": 16005.5,
    # Site: racking (20*57), panel (150 + 4*34), permitting (8 kW * 187.5, soft)
    "SolarBatteryDesign__solar_battery_plant__site_infra__capital_cost__capital_cost": 3995.5,
    # Plant rollup
    "SolarBatteryDesign__solar_battery_plant__capital_cost__capital_cost": 41205.0,
    # 8760 * 0.008 MW * 1 * 0.159
    "SolarBatteryDesign__solar_battery_plant__energy_production__annual_energy_mwh": 11.14272,
    # 20 $/kW-yr * 8 kW
    "SolarBatteryDesign__solar_battery_plant__annualized_om__annual_om_cost": 160.0,
    "SolarBatteryDesign__solar_battery_plant__annualized_fuel__annual_fuel_cost": 0.0,
    # CRF = 0.05*1.05^25/(1.05^25-1)
    "SolarBatteryDesign__solar_battery_plant__annualized_financial__capital_recovery_factor": 0.05 * 1.05**25 / (1.05**25 - 1),
    "SolarBatteryDesign__solar_battery_plant__annualized_financial__annualized_capital_cost": (0.05 * 1.05**25 / (1.05**25 - 1)) * 41205.0,
    # p_net_kw = p_net_mw * 1000
    "SolarBatteryDesign__solar_battery_plant__p_net_kw__p_net_kw": 8.0,
    # LCOE = (acc + (om + fuel) * 1.0245^25) / energy
    "SolarBatteryDesign__solar_battery_plant__lcoe__lcoe_per_mwh": (
        (0.05 * 1.05**25 / (1.05**25 - 1)) * 41205.0 + (160.0 + 0.0) * 1.0245**25
    ) / 11.14272,
}

REL_TOL = 1e-12  # float-representation tolerance only; arithmetic must be exact


def main() -> None:
    # GAP (filed in findings): the generated YAML ExitPoint declares primitive
    # types ("RootModel[float]", "float") that the default OutputRouter has no
    # write handlers for. execute_pipeline's custom_schema_types only registers
    # class-named handlers, so we must pass an explicit router.
    router = create_output_router_with_json_schemas(
        ["RootModel[float]", "DesignParams", "LibraryParams", "SystemDesign"]
    )
    # GAP 2 (filed in findings): plain-float channels can't use write_json_model
    # (writers.py:25 assumes .model_dump). Register a scalar JSON handler.
    import json

    from simkit.io.output_router import WriteHandler

    router.register_handler(
        "float",
        WriteHandler(
            fn=lambda value, path: Path(path).write_text(json.dumps(value)),
            extension=".json",
        ),
    )
    result = execute_pipeline(
        SPIKE / "generated/pipelines/solar_battery.yaml",
        output_dir=SPIKE / "outputs",
        registry=create_solar_battery_tea_registry(),
        output_router=router,
        custom_schema_types=[DesignParams, LibraryParams, SystemDesign],
    )

    outputs = result.outputs
    print(f"Pipeline executed: {len(outputs)} channels produced\n")

    failures = 0
    print(f"{'channel (leaf)':60s} {'executed':>18s} {'expected':>18s}")
    for chan, expected in EXPECTED.items():
        val = outputs[chan]
        actual = float(val.root) if hasattr(val, "root") else float(val)
        ok = (
            abs(actual - expected) <= REL_TOL * max(abs(actual), abs(expected), 1.0)
        )
        leaf = "__".join(chan.split("__")[-2:])
        print(f"{leaf:60s} {actual:18.9f} {expected:18.9f}  {'OK' if ok else 'FAIL'}")
        if not ok:
            failures += 1

    print()
    if failures:
        raise SystemExit(f"{failures} assertion(s) FAILED")
    print(f"ALL {len(EXPECTED)} ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
