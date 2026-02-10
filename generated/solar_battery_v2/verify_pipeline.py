#!/usr/bin/env python3
"""Verify pipeline output against expected values.

V2: All 7 metrics read from ExitPoint JSON files.
Bug 4 fixed — capital_recovery_factor and annualized_capital_cost
now in ExitPoint (no manual writes needed).

Usage:
    PYTHONPATH=generated uv run python generated/solar_battery_v2/verify_pipeline.py
"""
import json
import sys
from pathlib import Path

EXPECTED_VALUES = {
    "total_capex": (41205.0, 0.0),          # exact match
    "annual_energy_mwh": (11.14272, 0.01),   # 1% tolerance
    "annual_om_cost": (160.0, 0.01),
    "annual_fuel_cost": (0.0, 0.0),          # exact
    "capital_recovery_factor": (0.070952, 0.01),
    "annualized_capital_cost": (2923.60, 0.01),
    "lcoe_per_mwh": (288.68, 0.01),
}


def find_latest_output_dir(base_dir: Path) -> Path | None:
    """Find the most recently modified output directory."""
    candidates = sorted(
        (d for d in base_dir.iterdir() if d.is_dir()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def verify(output_dir: Path) -> bool:
    all_pass = True
    for name, (expected, tolerance) in EXPECTED_VALUES.items():
        output_file = output_dir / f"{name}.json"
        if not output_file.exists():
            print(f"  FAIL {name}: output file not found")
            all_pass = False
            continue

        with open(output_file) as f:
            actual = json.load(f)

        # RootModel[float] may serialize as {"root": value} or bare float
        if isinstance(actual, dict) and "root" in actual:
            actual = actual["root"]

        if expected == 0.0:
            passed = actual == 0.0
        elif tolerance == 0.0:
            passed = abs(actual - expected) < 0.01  # exact within rounding
        else:
            passed = abs(actual - expected) / abs(expected) <= tolerance

        status = "PASS" if passed else "FAIL"
        print(f"  {status} {name}: expected={expected}, actual={actual}")
        if not passed:
            all_pass = False

    return all_pass


def main():
    base_dir = Path(__file__).resolve().parent / "outputs"
    output_dir = find_latest_output_dir(base_dir)
    if output_dir is None:
        print("ERROR: No output directory found. Run the pipeline first.")
        return 1

    print(f"Verifying pipeline output in: {output_dir.name}")
    success = verify(output_dir)
    print(f"\nOverall: {'ALL 7 METRICS PASS' if success else 'FAIL'}")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
