"""Every-and-only mutation proof against the actual Fusion model tree."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from tests.ife_execution import complete_ife_package
from sysml_codegen.cli import GenerationConfig, run_codegen  # type: ignore[import-untyped]
from sysml_codegen.orchestration.exact_pipeline_context import (  # type: ignore[import-untyped]
    build_exact_pipeline_context,
    build_exact_pipeline_context_from_snapshot,
)
from sysml_codegen.snapshot.capture import (  # type: ignore[import-untyped]
    capture_instance_graph_snapshot,
)

REPOSITORY = Path(__file__).resolve().parents[1]
#: The IFE family's two model trees. ``models/`` holds two design families since the
#: stellarator model migration, so "primary" is the IFE family's canonical subset,
#: materialized per module (tests/model_families.py); "exploration" is the IFE twin.
MODEL_TREES = {
    "primary": "canonical-ife-subset",
    "exploration": REPOSITORY / "exploration" / "ife_e2e" / "models",
}


def _resolve_models(tree_name: str, root: Path) -> Path:
    from tests.model_families import IFE, materialize_canonical_subset

    if MODEL_TREES[tree_name] == "canonical-ife-subset":
        return materialize_canonical_subset(IFE, root / "canonical-ife-subset")
    return MODEL_TREES[tree_name]
GAIN = "hif_plant_pkg__hif_plant__gain"
AVAILABILITY = "hif_plant_pkg__hif_plant__availability"
LCOE = "hif_plant_pkg__hif_plant__hawker_price__price"
RECIRC = "hif_plant_pkg__hif_plant__recirc_calc__f_recirc"
COE = "hif_plant_pkg__hif_plant__meier_price__price"
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
    root = tmp_path_factory.mktemp(f"fusion-mutation-{tree_name}")
    models = _resolve_models(tree_name, root)
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
    complete_ife_package(GenerationConfig(models_path=models, output_path=live_package, package_name=live_name, overwrite=True))
    complete_ife_package(GenerationConfig(from_snapshot=snapshot, output_path=snapshot_package, package_name=snapshot_name, overwrite=True))
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
    prefix = "hif_plant_pkg__hif_plant__"
    physics = {prefix + "lcoe_calc__" + field for field in (
        "fusion_energy_per_shot", "fusion_power", "thermal_power", "thermal_power_gw",
        "gross_electric_power", "net_electric_power", "net_electric_power_gw",
        "driver_recirculating_fraction", "total_recirculating_fraction",
        "discounted_cost", "discounted_energy",
    )}
    costs = {LCOE, COE, RECIRC} | {prefix + field for field in (
        "meier_reactor_cost_calc__reactor_cost_billions",
        "meier_capital_calc__total_capital_billions", "meier_coe_calc__annualized_cost",
        "meier_coe_calc__energy_denominator",
    )}
    assert _movers(baseline, high) == physics | costs
    assert _movers(baseline, low) == physics | costs | {VIABILITY, "headline"}
    assert low.responses[VIABILITY] == "violated"
    assert low.responses["headline"] == "violated"


@pytest.mark.parametrize("route_name", ["live", "snapshot"])
def test_availability_mutates_shots_replacements_and_both_costs(routes, route_name: str) -> None:
    route = routes[route_name]
    graph = route[0]
    assert _consumer_ports(graph, AVAILABILITY) == {
        ("hif_plant_pkg__hif_plant__lcoe_calc", "availability_in"),
        ("hif_plant_pkg__hif_plant__meier_coe_calc", "availability_in"),
    }
    baseline = _evaluate(route, {})
    changed = _evaluate(route, {AVAILABILITY: 0.91})
    prefix = "hif_plant_pkg__hif_plant__"
    assert _movers(baseline, changed) == {LCOE, COE, prefix + "meier_coe_calc__energy_denominator"} | {
        prefix + "lcoe_calc__" + field for field in (
            "shots_per_year", "driver_lifetime_years", "annual_driver_replacement_cost",
            "discounted_cost", "discounted_energy",
        )
    }


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


@pytest.mark.parametrize('route_name', ['live', 'snapshot'])
def test_sv074_source_cashflow_and_dependency_mutations(routes, route_name):
    from tests.ife_oracle import PREFIX, MUTATIONS, assert_source_outputs

    for overrides in MUTATIONS.values():
        result = _evaluate(routes[route_name], {PREFIX+k:v for k,v in overrides.items()})
        assert_source_outputs(result.outputs, overrides)


@pytest.mark.parametrize('route_name', ['live', 'snapshot'])
def test_sv075_non_generators_survive_execution_with_named_rejection(routes, route_name):
    from tests.ife_oracle import PREFIX, NET_GATE, HEURISTIC, BOUNDARIES
    import math

    for name, overrides in BOUNDARIES.items():
        result = _evaluate(routes[route_name], {PREFIX+k:v for k,v in overrides.items()})
        net = result.outputs[PREFIX+'lcoe_calc__net_electric_power']
        if name == 'zero':
            assert net == 0.0
        elif name == 'negative_neighbor':
            assert net == -2.5
        elif name == 'positive_neighbor':
            assert net == 2.5
        elif name == 'roundoff_positive':
            assert net == 5.960464477539063e-8
        else:
            assert net < 0
        assert result.responses[HEURISTIC] == 'satisfied'
        assert result.responses[NET_GATE] == ('satisfied' if net > 0 else 'violated')
        for channel in ('hawker_price', 'meier_price'):
            assert result.outputs[PREFIX+channel+'__generating'] == float(net > 0)
            price = result.outputs[PREFIX+channel+'__price']
            assert math.isfinite(price)
            assert price > 0 if net > 0 else price == 0
