"""Actual Fusion models generate identically and execute through real TEAx."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
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
EXPECTED_CHANNELS = {
    "constraint_report",
    "hif_plant_pkg__hif_plant__driver__meier_cost__cost_billions",
    "hif_plant_pkg__hif_plant__driver__meier_cost__gamma",
    "hif_plant_pkg__hif_plant__lcoe_calc__lcoe",
    "hif_plant_pkg__hif_plant__meier_capital_calc__total_capital_billions",
    "hif_plant_pkg__hif_plant__meier_coe_calc__coe_cents_kwh",
    "hif_plant_pkg__hif_plant__meier_reactor_cost_calc__reactor_cost_billions",
    "hif_plant_pkg__hif_plant__recirc_calc__f_recirc",
    "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b__evaluation",
}


def _tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def _generate(config: GenerationConfig) -> Path:
    assert run_codegen(config) is True
    return Path(config.output_path)


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
    assert report.assessed_entry_count == 1
    assert len(report.results) == 1
    assert report.results[0].status == "satisfied"
    inputs = json.loads(
        (public_routes["live"][0] / "inputs" / "hif_plant_params.json").read_text()
    )
    assert inputs["hif_plant_pkg__hif_plant__gain"] == 80.0
