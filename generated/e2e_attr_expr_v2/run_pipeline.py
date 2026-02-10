#!/usr/bin/env python3
"""Execute the e2e_attr_expr_v2 TEAx pipeline.

V2: No manual workarounds. All 7 codegen bugs are expected to be fixed.
Bug 4 (ExitPoint float handler) is fixed — no manual channel writes needed.

Usage:
    PYTHONPATH=generated uv run python generated/e2e_attr_expr_v2/run_pipeline.py
"""
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from e2e_attr_expr_v2 import create_e2e_attr_expr_v2_registry, CUSTOM_SCHEMA_TYPES


def main():
    pipeline_dir = Path(__file__).resolve().parent
    pipeline_path = pipeline_dir / "pipelines" / "pipeline.yaml"
    output_dir = pipeline_dir / "outputs"
    registry = create_e2e_attr_expr_v2_registry()

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
            print(f"  {name}: <multi-output with {len(val.model_fields)} fields>")
        else:
            print(f"  {name}: {val}")

    return result


if __name__ == "__main__":
    main()
