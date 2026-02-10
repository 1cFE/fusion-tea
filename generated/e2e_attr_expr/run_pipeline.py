#!/usr/bin/env python3
"""Execute the e2e_attr_expr TEAx pipeline.

Usage:
    PYTHONPATH=generated uv run python generated/e2e_attr_expr/run_pipeline.py
"""
import json
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from e2e_attr_expr import create_e2e_attr_expr_registry, CUSTOM_SCHEMA_TYPES


# Multi-output channels that ExitPoint can't serialize (codegen bug: float has no write handler)
# These map from channel name → simplified output filename
MULTI_OUTPUT_CHANNELS = {
    "E2EAttrExprDesign__e2e_plant__component_cost__material_cost": "material_cost",
    "E2EAttrExprDesign__e2e_plant__component_cost__fab_cost": "fab_cost",
    "E2EAttrExprDesign__e2e_plant__component_cost__install_cost": "install_cost",
    "E2EAttrExprDesign__e2e_plant__component_cost__total_cost": "total_cost",
    "E2EAttrExprDesign__e2e_plant__component_cost__idiot_index": "idiot_index",
    "E2EAttrExprDesign__e2e_plant__financial__crf": "crf",
    "E2EAttrExprDesign__e2e_plant__financial__annualized_cost": "annualized_cost",
}


def main():
    pipeline_dir = Path(__file__).resolve().parent
    pipeline_path = pipeline_dir / "pipelines" / "pipeline.yaml"
    output_dir = pipeline_dir / "outputs"
    registry = create_e2e_attr_expr_registry()

    result = execute_pipeline(
        spec_path=str(pipeline_path),
        output_dir=str(output_dir),
        registry=registry,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )

    # Write multi-output float channels that ExitPoint couldn't serialize
    # Find the latest output directory (ExitPoint creates timestamped dirs)
    output_dirs = sorted(
        (d for d in output_dir.iterdir() if d.is_dir()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if output_dirs:
        latest_dir = output_dirs[0]
        for channel_name, filename in MULTI_OUTPUT_CHANNELS.items():
            if channel_name in result.outputs:
                value = result.outputs[channel_name]
                val = getattr(value, "root", value)
                out_path = latest_dir / f"{filename}.json"
                with open(out_path, "w") as f:
                    json.dump({"root": float(val)}, f)

    # Print results
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
