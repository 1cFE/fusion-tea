"""WI-013 pipeline execution spike: generate the solar_battery package from the
extraction snapshot, bypassing syside (license expired 2026-07).

Replicates run_codegen() from sysml_codegen/cli/__init__.py, but builds the
PipelineContext from tests/fixtures/solar_battery_model/extraction_snapshot.json
using the same helpers the conformance tests use (build_full_graph_from_snapshot).

Run from the sysml-codegen repo so its venv + tests package resolve:
    cd ~/1cfe/sysml-codegen && uv run python \
        ~/1cfe/fusion-tea/exploration/pipeline_spike/generate_from_snapshot.py
"""

import sys
from pathlib import Path

CODEGEN_REPO = Path("/home/reid/1cfe/sysml-codegen")
OUTPUT = Path("/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/generated")

sys.path.insert(0, str(CODEGEN_REPO))  # for tests.helpers

from tests.helpers.snapshot_loader import load_extraction_snapshot  # noqa: E402

from sysml_codegen.analysis.dependency_backtracker import (  # noqa: E402
    DependencyBacktracker,
)
from sysml_codegen.analysis.parameter_groups import ParameterGroupDeriver  # noqa: E402
from sysml_codegen.orchestration.output_registry_builder import (  # noqa: E402
    build_output_registry,
)
from sysml_codegen.resolution.graph_builder import build_computation_graph  # noqa: E402

from sysml_codegen.cli import GenerationConfig  # noqa: E402
from sysml_codegen.cli import (  # noqa: E402
    _clear_output_directory,
    _generate_backlog,
    _generate_entry_points,
    _generate_modules,
    _generate_pipeline,
    _generate_primitives,
    _generate_registry,
    _generate_schemas,
    _generate_stencils,
    _generate_tests,
    _get_template_env,
    _setup_output_directories,
)
from sysml_codegen.orchestration.pipeline_context import PipelineContext  # noqa: E402

MODEL = "solar_battery_model"


def main() -> None:
    # Mirrors tests/conformance/test_entry_point_classifier.py::
    # build_classifier_inputs_from_snapshot + build_full_graph_from_snapshot
    # (not imported directly: test modules require pytest, absent from venv).
    snap = load_extraction_snapshot(MODEL)

    registry = build_output_registry(
        calc_usages=snap["calc_usages"],
        calc_defs=snap["calc_defs"],
        aggregation_data=snap["aggregation_expressions"],
        computed_attributes=snap["computed_attributes"],
        channel_aliases=snap.get("channel_aliases", []),
        design_attributes=snap.get("design_attributes", {}),
    )
    backtracker = DependencyBacktracker(
        all_usages=snap["calc_usages"],
        calc_defs=snap["calc_defs"],
        design_attributes=snap.get("design_attributes", {}),
        output_registry=registry,
    )
    result = backtracker.find_required_modules([], include_all=True)
    design_attrs = {Path(k): v for k, v in snap["design_attributes"].items()}
    group_deriver = ParameterGroupDeriver(
        design_attrs, snap["calc_usages"], snap["calc_defs"]
    )
    hierarchy_data = snap["hierarchy_data"]
    graph = build_computation_graph(
        result=result,
        calc_defs=snap["calc_defs"],
        design_attrs=design_attrs,
        group_deriver=group_deriver,
        output_registry=registry,
        compilation_results=None,
        computed_attributes=snap["computed_attributes"],
        aggregation_data=snap["aggregation_expressions"],
        hierarchy_redefinitions=hierarchy_data.redefinitions,
        usage_type_map=hierarchy_data.usage_type_map,
    )

    ctx = PipelineContext(
        extractor=None,  # not needed by generation (boundary = ComputationGraph)
        calc_defs=snap["calc_defs"],
        calc_usages=snap["calc_usages"],
        design_attributes=design_attrs,
        group_deriver=group_deriver,
        backtracker=backtracker,
        backtracking_result=result,
        computation_graph=graph,
        compilation_results={},  # ASTs not in snapshot; AI pass writes bodies
        computed_attributes=snap["computed_attributes"],
        hierarchy_data=hierarchy_data,
        aggregation_expressions=snap["aggregation_expressions"],
        channel_aliases=snap.get("channel_aliases", []),
        output_registry=registry,
    )

    config = GenerationConfig(
        models_path=CODEGEN_REPO / "tests/fixtures/solar_battery_model",
        output_path=OUTPUT,
        package_name="solar_battery_tea",
        pipeline_name="solar_battery",
        overwrite=True,
    )

    print(f"Graph modules: {len(graph.modules)}")
    _clear_output_directory(config)
    _setup_output_directories(config)
    _generate_primitives(config)
    env = _get_template_env()
    _generate_schemas(ctx, config, env)
    _generate_modules(ctx, config, env)
    _generate_stencils(ctx, config, env)
    _generate_pipeline(ctx, config, env)
    _generate_registry(ctx, config, env)
    _generate_entry_points(ctx, config, env)
    _generate_backlog(ctx, config)
    _generate_tests(ctx, config, env)
    print("Generation complete:", OUTPUT)


if __name__ == "__main__":
    main()
