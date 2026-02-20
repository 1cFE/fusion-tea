#!/usr/bin/env python3
"""Execute the solar_battery_v5 TEAx pipeline.

V5: Clean regeneration — no workarounds. Bug 11/12 fix validation.

Usage:
    PYTHONPATH=generated uv run python generated/solar_battery_v5/run_pipeline.py
"""
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from solar_battery_v5 import create_solar_battery_v5_registry, CUSTOM_SCHEMA_TYPES


def main():
    pipeline_dir = Path(__file__).resolve().parent
    pipeline_path = pipeline_dir / "pipelines" / "pipeline.yaml"
    output_dir = pipeline_dir / "outputs"
    registry = create_solar_battery_v5_registry()

    result = execute_pipeline(
        spec_path=str(pipeline_path),
        output_dir=str(output_dir),
        registry=registry,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )

    print("Pipeline completed successfully!")
    for name, value in result.outputs.items():
        val = getattr(value, "root", value)
        if hasattr(val, "model_dump"):
            print(f"  {name}: <multi-output with {len(val.model_fields)} fields>")
        else:
            print(f"  {name}: {val}")

    return result


if __name__ == "__main__":
    main()
