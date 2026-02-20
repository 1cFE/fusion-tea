#!/usr/bin/env python3
"""Verify pipeline output against expected ground truth values.

V5: Clean regeneration — no workarounds. Bug 11/12 fix validation.
Same 7 ground truth values as v1-v4.

Usage:
    PYTHONPATH=generated uv run python generated/solar_battery_v5/verify_pipeline.py
"""
import json
import sys
from pathlib import Path


# Ground truth from v1/v2 validation (see V2 report)
# Format: (json_filename, expected_value, relative_tolerance)
EXPECTED_VALUES = {
    "total_capex": (
        "SolarBatteryDesign__solar_battery_plant__capital_cost__capital_cost.json",
        41205.0, 0.0
    ),
    "annual_energy_mwh": (
        "SolarBatteryDesign__solar_battery_plant__energy_production__annual_energy_mwh.json",
        11.14272, 0.01
    ),
    "annual_om_cost": (
        "SolarBatteryDesign__solar_battery_plant__annualized_om__annual_om_cost.json",
        160.0, 0.01
    ),
    "annual_fuel_cost": (
        "SolarBatteryDesign__solar_battery_plant__annualized_fuel__annual_fuel_cost.json",
        0.0, 0.0
    ),
    "capital_recovery_factor": (
        "SolarBatteryDesign__solar_battery_plant__annualized_financial__capital_recovery_factor.json",
        0.07095246, 0.01
    ),
    "annualized_capital_cost": (
        "SolarBatteryDesign__solar_battery_plant__annualized_financial__annualized_capital_cost.json",
        2923.60, 0.01
    ),
    "lcoe_per_mwh": (
        "SolarBatteryDesign__solar_battery_plant__lcoe__lcoe_per_mwh.json",
        288.68, 0.01
    ),
}


def find_latest_output_dir(base_dir: Path) -> Path | None:
    """Find the most recently modified output directory."""
    candidates = sorted(
        (d for d in base_dir.iterdir() if d.is_dir()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def check_value(name: str, actual: float, expected: float, tolerance: float) -> bool:
    """Compare actual vs expected with tolerance."""
    if expected == 0.0:
        passed = actual == 0.0
    elif tolerance == 0.0:
        passed = abs(actual - expected) < 0.01  # exact within rounding
    else:
        passed = abs(actual - expected) / abs(expected) <= tolerance
    status = "PASS" if passed else "FAIL"
    print(f"  {status} {name}: expected={expected}, actual={actual}")
    return passed


def main():
    base_dir = Path(__file__).resolve().parent / "outputs"
    output_dir = find_latest_output_dir(base_dir)
    if output_dir is None:
        print("ERROR: No output directory found. Run the pipeline first.")
        return 1

    print(f"Verifying pipeline output in: {output_dir.name}")

    print("\n--- 7 Ground Truth Values ---")
    all_pass = True
    for name, (filename, expected, tolerance) in EXPECTED_VALUES.items():
        output_file = output_dir / filename
        if not output_file.exists():
            print(f"  FAIL {name}: output file not found ({filename})")
            all_pass = False
            continue
        with open(output_file) as f:
            actual = json.load(f)
        if isinstance(actual, dict) and "root" in actual:
            actual = actual["root"]
        if not check_value(name, actual, expected, tolerance):
            all_pass = False

    print("\n" + "=" * 50)
    print(f"Overall: {'ALL 7 VALUES PASS' if all_pass else 'FAIL'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
