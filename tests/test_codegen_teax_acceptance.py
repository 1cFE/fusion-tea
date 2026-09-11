"""Actual Fusion models generate identically and execute through real TEAx."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
from tests.ife_execution import complete_ife_package
from sysml_codegen.cli import GenerationConfig, run_codegen  # type: ignore[import-untyped]
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
PACKAGE_NAME = "fusion_tea_final"
P = "hif_plant_pkg__hif_plant__"
EXPECTED_CHANNELS = {"constraint_report"} | {P + suffix for suffix in (
    "driver__meier_cost__cost_billions", "driver__meier_cost__gamma",
    "driver__meier_cost__bank_energy_joules", "meier_capital_calc__total_capital_billions",
    "meier_reactor_cost_calc__reactor_cost_billions", "recirc_calc__f_recirc",
    "meier_coe_calc__annualized_cost", "meier_coe_calc__energy_denominator",
    "hawker_price__price", "hawker_price__generating", "meier_price__price", "meier_price__generating",
    "net_positive__1d299cceab19c61c__evaluation", "viability__81ddf10fb1d1749b__evaluation",
)} | {P + "lcoe_calc__" + field for field in (
    "energy_on_target", "fusion_energy_per_shot", "fusion_power", "thermal_power",
    "thermal_power_gw", "gross_electric_power", "driver_electric_power", "other_parasitic_power",
    "net_electric_power", "net_electric_power_gw", "driver_recirculating_fraction",
    "total_recirculating_fraction", "discounted_cost", "discounted_energy", "shots_per_year",
    "driver_lifetime_years", "driver_capital_cost", "annual_driver_replacement_cost",
)}



def _tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def _generate(config: GenerationConfig) -> Path:
    assert run_codegen(config) is True
    return complete_ife_package(config)


def _execute(package: Path, root: Path):
    from simkit.core.pipeline import execute_pipeline  # type: ignore[import-untyped]
    from simkit.core.registry_builder import create_registry  # type: ignore[import-untyped]
    from simkit.evaluation.package_load import (  # type: ignore[import-untyped]
        ProvisionalPackageLoader,
    )

    loader = ProvisionalPackageLoader(
        package_dir=package,
        package_name=PACKAGE_NAME,
        link_root=root / "link",
    )
    module, fingerprint = loader.load()
    factory = getattr(module, f"create_{PACKAGE_NAME}_registry")
    assert factory.__globals__.get("create_registry") is create_registry
    registry = factory()
    result = execute_pipeline(
        package / "pipelines" / "pipeline.yaml",
        root / "run",
        registry=registry,
        custom_schema_types=module.CUSTOM_SCHEMA_TYPES,
    )
    return fingerprint, result


@pytest.fixture(scope="module", params=tuple(MODEL_TREES))
def public_routes(request, tmp_path_factory):
    tree_name = request.param
    root = tmp_path_factory.mktemp(f"fusion-final-{tree_name}")
    models = _resolve_models(tree_name, root)
    live = _generate(
        GenerationConfig(
            models_path=models,
            output_path=root / "live" / PACKAGE_NAME,
            package_name=PACKAGE_NAME,
            overwrite=True,
        )
    )
    snapshot = capture_instance_graph_snapshot([models], root / "snapshot.json")
    captured = _generate(
        GenerationConfig(
            from_snapshot=snapshot,
            output_path=root / "snapshot" / PACKAGE_NAME,
            package_name=PACKAGE_NAME,
            overwrite=True,
        )
    )
    assert _tree(live) == _tree(captured)
    return {
        "models": models,
        "live": (live, *_execute(live, root / "live-exec")),
        "snapshot": (captured, *_execute(captured, root / "snapshot-exec")),
    }


def test_imports_and_execution_use_only_recorded_real_roots(public_routes) -> None:
    import agentic_mbse
    import simkit  # type: ignore[import-untyped]
    import sysml_codegen  # type: ignore[import-untyped]

    target = Path(os.environ["STOP_PARSER_WHEEL_TARGET"]).resolve()
    teax = Path(os.environ["STOP_PARSER_TEAX_ROOT"]).resolve()
    assert agentic_mbse.__file__ is not None
    assert sysml_codegen.__file__ is not None
    assert simkit.__file__ is not None
    assert Path(agentic_mbse.__file__).resolve().is_relative_to(target)
    assert Path(sysml_codegen.__file__).resolve().is_relative_to(target)
    assert Path(simkit.__file__).resolve().is_relative_to(teax)
    assert sys.modules.get("tests.runtime.pipeline_runner") is None
    assert public_routes


def test_live_and_snapshot_packages_are_byte_identical(public_routes) -> None:
    live, live_fingerprint, live_result = public_routes["live"]
    captured, captured_fingerprint, captured_result = public_routes["snapshot"]
    assert _tree(live) == _tree(captured)
    assert live_fingerprint == captured_fingerprint
    assert set(live_result.outputs) == EXPECTED_CHANNELS
    assert set(captured_result.outputs) == EXPECTED_CHANNELS
    assert live_result.outputs == captured_result.outputs


def test_complete_model_tree_and_constraint_verdict_execute(public_routes) -> None:
    _, _, result = public_routes["live"]
    assert len(list(public_routes["models"].rglob("*.sysml"))) == 11
    report = result.outputs["constraint_report"]
    assert report.headline == "full_satisfaction"
    assert report.coverage.coverage_state == "complete"
    assert report.assessed_entry_count == 2
    assert len(report.results) == 2
    assert all(entry.status == "satisfied" for entry in report.results)
    inputs = json.loads(
        (public_routes["live"][0] / "inputs" / "hif_plant_params.json").read_text()
    )
    assert inputs["hif_plant_pkg__hif_plant__gain"] == 87.0


@pytest.mark.parametrize('smart', [False, True])
def test_typed_handwritten_quotient_survives_supported_regeneration(public_routes, smart, tmp_path):
    from tests.ife_execution import HANDWRITTEN

    package = public_routes['live'][0]
    implementation = (package / HANDWRITTEN).read_bytes()
    assert b'inputs: Generating_Electricity_PriceInput) -> tuple[float, float]' in implementation
    assert b'NotImplementedError' not in implementation
    before = _tree(package)
    assert run_codegen(GenerationConfig(
        models_path=public_routes['models'], output_path=package, package_name=PACKAGE_NAME,
        overwrite=True, preserve_handwritten=True, smart_regen=smart,
    ))
    assert (package / HANDWRITTEN).read_bytes() == implementation
    assert _tree(package) == before
    fingerprint, result = _execute(package, tmp_path)
    assert fingerprint == public_routes['live'][1]
    assert result.outputs == public_routes['live'][2].outputs
