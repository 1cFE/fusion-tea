"""Every-and-only mutation proof against the actual Fusion model tree."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from sysml_codegen.cli import GenerationConfig, run_codegen  # type: ignore[import-untyped]
from sysml_codegen.orchestration.exact_pipeline_context import (  # type: ignore[import-untyped]
    build_exact_pipeline_context,
    build_exact_pipeline_context_from_snapshot,
)
from sysml_codegen.snapshot.capture import (  # type: ignore[import-untyped]
    capture_instance_graph_snapshot,
)

REPOSITORY = Path(__file__).resolve().parents[1]
MODEL_TREES = {
    "primary": REPOSITORY / "models",
    "exploration": REPOSITORY / "exploration" / "ife_e2e" / "models",
}
GAIN = "hif_plant_pkg__hif_plant__gain"
AVAILABILITY = "hif_plant_pkg__hif_plant__availability"
LCOE = "hif_plant_pkg__hif_plant__lcoe_calc__lcoe"
RECIRC = "hif_plant_pkg__hif_plant__recirc_calc__f_recirc"
COE = "hif_plant_pkg__hif_plant__meier_coe_calc__coe_cents_kwh"
VIABILITY = "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b"


def _consumer_ports(graph, source: str) -> set[tuple[str, str]]:
    return {
        (module.name, formal.param_name)
        for module in graph.modules
        for formal in module.inputs
        if formal.source.qualified_name == source
    }


def _all_ports(graph) -> set[tuple[str, str]]:
    return {
        (module.name, formal.param_name)
        for module in graph.modules
        for formal in module.inputs
    }


def _harness(package: Path, name: str, graph, root: Path):
    from simkit.evaluation.evaluator import PreparedEvaluator  # type: ignore[import-untyped]
    from simkit.evaluation.package_load import (  # type: ignore[import-untyped]
        ProvisionalPackageLoader,
    )
    from simkit.study.bridge import CandidateBridge  # type: ignore[import-untyped]

    loader = ProvisionalPackageLoader(package, name, root / "link")
    evaluator = PreparedEvaluator(
        loader,
        package / "pipelines" / "pipeline.yaml",
        expects_constraint_report=True,
    )
    return graph, evaluator, CandidateBridge(evaluator.entry_models)


@pytest.fixture(scope="module", params=tuple(MODEL_TREES))
def routes(request, tmp_path_factory):
    tree_name = request.param
    models = MODEL_TREES[tree_name]
    root = tmp_path_factory.mktemp(f"fusion-mutation-{tree_name}")
    live_name = f"fusion_mutation_{tree_name}_live"
    live_package = root / live_name
    assert run_codegen(
        GenerationConfig(
            models_path=models,
            output_path=live_package,
            package_name=live_name,
            overwrite=True,
        )
    )
    snapshot = capture_instance_graph_snapshot([models], root / "snapshot.json")
    snapshot_name = f"fusion_mutation_{tree_name}_snapshot"
    snapshot_package = root / snapshot_name
    assert run_codegen(
        GenerationConfig(
            from_snapshot=snapshot,
            output_path=snapshot_package,
            package_name=snapshot_name,
            overwrite=True,
        )
    )
    return {
        "live": _harness(
            live_package,
            live_name,
            build_exact_pipeline_context([models]).computation_graph,
            root / "live-harness",
        ),
        "snapshot": _harness(
            snapshot_package,
            snapshot_name,
            build_exact_pipeline_context_from_snapshot(snapshot).computation_graph,
            root / "snapshot-harness",
        ),
    }


def _evaluate(route, values: dict[str, float]):
    _, evaluator, bridge = route
    return evaluator.evaluate(bridge.build(values))


def _movers(before, after) -> set[str]:
    assert set(before.outputs) == set(after.outputs)
    assert set(before.responses) == set(after.responses)
    moved = {name for name in before.outputs if before.outputs[name] != after.outputs[name]}
    moved |= {
        name for name in before.responses if before.responses[name] != after.responses[name]
    }
    return moved


@pytest.mark.parametrize("route_name", ["live", "snapshot"])
def test_gain_has_one_source_and_exact_consumer_ports(routes, route_name: str) -> None:
    graph = routes[route_name][0]
    published = [
        parameter.qualified_name
        for group in graph.entry_point_groups
        for parameter in group.parameters
    ]
    assert published.count(GAIN) == 1
    fed = _consumer_ports(graph, GAIN)
    assert fed == {
        ("hif_plant_pkg__hif_plant__lcoe_calc", "gain_in"),
        ("hif_plant_pkg__hif_plant__recirc_calc", "gain_in"),
        (VIABILITY, "gain_in"),
    }
    assert len(_all_ports(graph) - fed) == len(_all_ports(graph)) - 3


@pytest.mark.parametrize("route_name", ["live", "snapshot"])
def test_gain_mutates_every_and_only_its_outputs_and_constraint(routes, route_name: str) -> None:
    route = routes[route_name]
    baseline = _evaluate(route, {})
    high = _evaluate(route, {GAIN: 100.0})
    low = _evaluate(route, {GAIN: 20.0})
    assert _movers(baseline, high) == {LCOE, RECIRC}
    assert _movers(baseline, low) == {LCOE, RECIRC, VIABILITY, "headline"}
    assert low.responses[VIABILITY] == "violated"
    assert low.responses["headline"] == "violated"


@pytest.mark.parametrize("route_name", ["live", "snapshot"])
def test_availability_mutates_every_and_only_two_outputs(routes, route_name: str) -> None:
    route = routes[route_name]
    graph = route[0]
    assert _consumer_ports(graph, AVAILABILITY) == {
        ("hif_plant_pkg__hif_plant__lcoe_calc", "availability_in"),
        ("hif_plant_pkg__hif_plant__meier_coe_calc", "availability_in"),
    }
    baseline = _evaluate(route, {})
    changed = _evaluate(route, {AVAILABILITY: 0.91})
    assert _movers(baseline, changed) == {LCOE, COE}


def test_live_and_snapshot_mutations_are_equal(routes) -> None:
    for values in ({}, {GAIN: 100.0}, {GAIN: 20.0}, {AVAILABILITY: 0.91}):
        live = _evaluate(routes["live"], values)
        snapshot = _evaluate(routes["snapshot"], values)
        assert live.outputs == snapshot.outputs
        assert live.responses == snapshot.responses
    teax = Path(os.environ["STOP_PARSER_TEAX_ROOT"]).resolve()
    import simkit  # type: ignore[import-untyped]

    assert simkit.__file__ is not None
    assert Path(simkit.__file__).resolve().is_relative_to(teax)
