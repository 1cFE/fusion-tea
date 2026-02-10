#!/usr/bin/env python3
"""Execute the solar+battery LCOE pipeline.

Usage:
    uv run python generated/solar_battery/run_pipeline.py
"""
import json
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from solar_battery import create_solar_battery_registry, CUSTOM_SCHEMA_TYPES


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
    registry = create_solar_battery_registry()

    result = execute_pipeline(
        spec_path=str(pipeline_path),
        output_dir=str(output_dir),
        registry=registry,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )

    # Write annualized_financial outputs that ExitPoint can't serialize
    # (codegen regenerated module with float MultiOutput; ExitPoint has no float write handler)
    # Compute via direct _impl call using pipeline values
    output_dirs = sorted(
        (d for d in output_dir.iterdir() if d.is_dir()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if output_dirs:
        latest_dir = output_dirs[0]
        total_capex = result.outputs["component_costs__total_capex"].root
        from solar_battery.modules.solarbatterylibrary.annualizedfinancialcalc import AnnualizedFinancialCalcInput
        from solar_battery.handwritten.solarbatterylibrary.annualizedfinancialcalc_impl import run_annualizedfinancialcalc
        fin_input = AnnualizedFinancialCalcInput(
            total_capex=total_capex, discount_rate=0.05, plant_lifetime=25.0
        )
        crf, annualized = run_annualizedfinancialcalc(fin_input)
        for name, val in [("capital_recovery_factor", crf), ("annualized_capital_cost", annualized)]:
            with open(latest_dir / f"{name}.json", "w") as f:
                json.dump({"root": float(val)}, f)

    # Print results
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
