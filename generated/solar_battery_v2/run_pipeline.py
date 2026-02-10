#!/usr/bin/env python3
"""Execute the solar+battery LCOE pipeline V2.

V2: No manual workarounds for codegen bugs.
Bug 4 fixed — capital_recovery_factor and annualized_capital_cost
now written by ExitPoint (no manual _impl calls needed).

Usage:
    PYTHONPATH=generated uv run python generated/solar_battery_v2/run_pipeline.py
"""
import json
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from solar_battery_v2 import create_solar_battery_v2_registry, CUSTOM_SCHEMA_TYPES


def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    pipeline_dir = Path(__file__).resolve().parent

    # Resolve model path to absolute (ensures working directory independence)
    config_path = pipeline_dir / "inputs" / "pipeline_config.json"
    with open(config_path) as f:
        config = json.load(f)
    model_path = (project_root / config["model_path"]).resolve()

    # Write resolved config for pipeline execution
    resolved_config = pipeline_dir / "inputs" / "pipeline_config_resolved.json"
    with open(resolved_config, "w") as f:
        json.dump({"model_path": str(model_path)}, f, indent=2)

    # Execute pipeline
    pipeline_path = pipeline_dir / "pipelines" / "pipeline.yaml"
    output_dir = pipeline_dir / "outputs"
    registry = create_solar_battery_v2_registry()

    result = execute_pipeline(
        spec_path=str(pipeline_path),
        output_dir=str(output_dir),
        registry=registry,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )

    # Print results — no manual channel writes (Bug 4 fixed in TEAx)
    print("Pipeline completed successfully!")
    for name, value in result.outputs.items():
        val = getattr(value, "root", value)
        if hasattr(val, "model_dump"):
            print(f"  {name}: <CostEvaluatorResult with {len(val.model_fields)} fields>")
        else:
            print(f"  {name}: {val}")

    return result


if __name__ == "__main__":
    main()
