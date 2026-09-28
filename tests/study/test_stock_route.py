"""The regenerated stellarator package on the stock teax route.

stellarator-model-migration Phase 2 (`.project/active/stellarator-model-migration/plan.md`).
The package is sealed at runtime contract ``2.0.0`` by the pinned codegen; stock teax's
``ProvisionalPackageLoader`` must accept it with ``strict=True``, its study identity must be
the sealed executable fingerprint itself (design D3, invariant I5), and the five values the
era adapter used to inject must arrive from model source (invariant I6, bet B2):

* g1 -- current BOP prices read supplied package amounts or guarded design classes;
* g2 -- ``cas28_capital`` (5.0 M$) and the replacement-schedule ``n_mod`` (1.0) are
  shipped entry-point inputs;
* g3 -- ``special_materials_capital`` (CAS27) is produced in-package and consumed by both
  CAS2x rollups, never shipped as an input;
* the three dead schema fillers (plant-level ``p_th``/``p_the``/``p_et``) are gone.

Teax comes from ``STOP_PARSER_TEAX_ROOT`` (the ``stock_simkit_path`` fixture, design D4).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from scripts.study import identity

PACKAGE_NAME = "stellarator_tea"
DEAD_FILLER_SUFFIXES = ("__p_th", "__p_the", "__p_et")


def _seal(package: Path) -> dict:
    return json.loads((package / "contracts" / "package_contract.json").read_text())


def _artifacts_differing_from_seal(package: Path) -> list[str]:
    return [
        relative
        for relative, digest in _seal(package)["artifact_hashes"].items()
        if hashlib.sha256((package / relative).read_bytes()).hexdigest() != digest
    ]


def _entry_sources(package: Path) -> dict[tuple[str, str], float]:
    """Every shipped input keyed by its complete ``(group, key)`` identity."""
    sources: dict[tuple[str, str], float] = {}
    for group_file in sorted((package / "inputs").glob("*.json")):
        for key, value in json.loads(group_file.read_text()).items():
            assert (group_file.stem, key) not in sources
            sources[(group_file.stem, key)] = value
    return sources


def _one_supplier(sources: dict[tuple[str, str], float], suffix: str) -> float:
    carriers = [(group, key) for (group, key) in sources if key.endswith(suffix)]
    assert len(carriers) == 1, f"{suffix}: {carriers}"
    return sources[carriers[0]]


def _modules(package: Path) -> dict[str, dict]:
    pipelines = sorted((package / "pipelines").glob("*.yaml"))
    assert len(pipelines) == 1, pipelines
    return yaml.safe_load(pipelines[0].read_text())["modules"]


def _wired_input(modules: dict[str, dict], module_suffix: str, formal: str) -> str:
    """The source token of one bound input: ``"<type> <source>"`` with the type stripped."""
    names = [name for name in modules if name.endswith(module_suffix)]
    assert len(names) == 1, (module_suffix, names)
    wired = modules[names[0]]["inputs"][formal]
    assert isinstance(wired, str), (names[0], formal, wired)
    return wired.split()[-1]


def test_stock_strict_loader_accepts_the_sealed_package(
    stock_simkit_path, real_package_path, tmp_path
) -> None:
    from simkit.evaluation.package_load import ProvisionalPackageLoader

    seal = _seal(real_package_path)
    assert seal["runtime_contract_version"] == "2.0.0"
    assert _artifacts_differing_from_seal(real_package_path) == []

    # The strict verifier forbids a symlink as the package root (``INVALID_PATH(.)``), so the
    # loader gets the resolved directory; ``pkg/stellarator_tea`` stays the manifest/test alias.
    module, fingerprint = ProvisionalPackageLoader(
        package_dir=real_package_path.resolve(),
        package_name=PACKAGE_NAME,
        link_root=tmp_path / "link",
        strict=True,
    ).load()
    assert module.__name__ == PACKAGE_NAME
    assert fingerprint == seal["executable_fingerprint"]


def test_the_package_link_resolves_inside_this_worktree(real_package_path, repo_root) -> None:
    """The tracked ``pkg/stellarator_tea`` link is relative (design D10): a link into
    another worktree would make every cleanliness check read someone else's files."""
    assert real_package_path.is_symlink()
    assert not Path(real_package_path.readlink()).is_absolute(), real_package_path.readlink()
    assert real_package_path.resolve().is_relative_to(repo_root.resolve())


def test_sealed_identity_is_the_executable_fingerprint(real_package_path) -> None:
    document = identity.build_sealed(package_name=PACKAGE_NAME, package_root=real_package_path)
    block = document["identity"]
    assert block["digest"] == block["sealed_executable_fingerprint"]
    assert block["sealed_executable_fingerprint"] == (
        _seal(real_package_path)["executable_fingerprint"]
    )
    assert block["allowed_modified_files"] == []
    assert block["adapter_sources"] == []
    assert document["glue_ledger"] == []


def test_formerly_injected_values_come_from_model_source(real_package_path) -> None:
    sources = _entry_sources(real_package_path)
    modules = _modules(real_package_path)

    # g2: the CAS28 digital-twin constant and the replacement-schedule module count.
    assert _one_supplier(sources, "__cas28_capital") == 5_000_000.0
    plant_n_mod = [
        (group, key) for (group, key) in sources if key == "stellarator_09__stellaris__n_mod"
    ]
    assert len(plant_n_mod) == 1, plant_n_mod
    assert sources[plant_n_mod[0]] == 1.0
    # This def's formal was never self-named (it was glue-fed), so it keeps the bare name.
    assert _wired_input(modules, "__replacement_cost_per_event", "n_mod").endswith(
        "stellarator_09__stellaris__n_mod"
    )

    # dead fillers: no shipped plant-level p_th / p_the / p_et.
    dead = [
        (group, key)
        for (group, key) in sources
        if key.endswith(DEAD_FILLER_SUFFIXES) and key.count("__") == 2
    ]
    assert dead == [], dead

    # g3: CAS27 is produced in-package and consumed by both CAS2x rollups.
    producer = [name for name in modules if name.endswith("__special_materials_capital")]
    assert len(producer) == 1, producer
    assert not any(key.endswith("__special_materials_capital") for (_g, key) in sources)
    for consumer in ("__cas23_to_28_capital", "__cas2x_pre_contingency"):
        assert _wired_input(modules, consumer, "special_materials_capital").startswith(
            producer[0]
        )

    # WI-079: procurement consumes selected specifications, independently of operation.
    for owner, calc in (("turbine", "turbine_cost"), ("heat_rejection", "heat_rejection_cost")):
        assert _wired_input(modules, "__"+owner+"__"+calc, "purchase_cost_in").endswith("__"+owner+"__purchase_cost_per_module")
    assert _wired_input(modules, "__electric_plant__electric_cost", "power").endswith("__electric_plant__installed_gross_rating_MWe")
    assert _wired_input(modules, "__misc_plant__misc_cost", "power").endswith("__misc_plant__cost_gross_class_MWe_guard__value.root")


import pytest
from exploration.stellarator_e2e.studies import study_route as route


@pytest.mark.parametrize('key', sorted(route.BOOLEAN_KEYS))
@pytest.mark.parametrize('value', [True, False, 0, 1, 0.0, 1.0])
def test_all_declared_boolean_values_normalize(key, value, real_package_path):
    route.assert_boolean_declarations(real_package_path)
    result = route.validate_proposal({key: value})
    assert result[key] is bool(value)


@pytest.mark.parametrize('key', sorted(route.BOOLEAN_KEYS))
@pytest.mark.parametrize('value', [2, -1, float('nan'), float('inf'), '0', 'true', None, [], {}])
def test_invalid_boolean_proposals_are_deliberate_refusals(key, value):
    with pytest.raises(route.RouteError, match=key + ': Boolean'):
        route.validate_proposal({key: value})


@pytest.mark.parametrize('suffix', ['plasma__R', 'magnet__coil__reference_turns', 'magnet__winding_pack__tape_price_per_m'])
@pytest.mark.parametrize('value', [True, False])
def test_boolean_numeric_controls_refuse(suffix, value):
    with pytest.raises(route.RouteError, match='finite numeric'):
        route.validate_proposal({route.P + suffix: value})


def test_invalid_batch_executes_nothing(tmp_path, stock_simkit_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('preparation must not run for a mixed invalid batch')
    monkeypatch.setattr(route, 'prepare', forbidden)
    out = tmp_path / 'not-created'
    with pytest.raises(route.RouteError, match='Boolean'):
        route.run_points('mixed', [{route.P+'plasma__R': 12.7}, {next(iter(route.BOOLEAN_KEYS)): 2}], out)
    assert not out.exists()


def test_all_booleans_survive_bridge_native_and_store(tmp_path, stock_simkit_path):
    from simkit.study.bridge import CandidateBridge
    points = []
    for key in sorted(route.BOOLEAN_KEYS):
        for value in (False, True):
            point = {key: value, route.P+'plasma__R': 12.7 + len(points)*.001}
            if not value:
                if key == route.P+'heat_transport__equipment_enabled':
                    point.update({route.P+'turbine__matched_cycle_enabled':0., route.P+'heat_rejection__cooling_water_enabled':0., route.P+'heat_transport__equipment_cost_mode':0., route.P+'heat_transport__secondary_energy_mode':0.,
                                  route.P+'buildings__facilities_enabled':False, route.P+'buildings__facilities_cost_mode':0.})
                if key == route.P+'buildings__facilities_enabled':
                    point.update({route.P+'buildings__facilities_cost_mode':0.})
                if key in {route.P+'fuel_cycle__inventory_enabled', route.P+'fuel_cycle__processing_source_conditions'}:
                    point[route.P+'fuel_cycle__processing_enabled'] = False
            points.append(route.validate_proposal(point))
    prepared = route.prepare(route.PACKAGE_DIR, tmp_path/'bridge')
    bridge = CandidateBridge(prepared.entry_models)
    for point in points:
        typed = bridge.build(point)
        fields = {k:v for model in typed.values() for k,v in model.model_dump().items()}
        for key in point.keys() & route.BOOLEAN_KEYS:
            assert fields[key] is point[key]
    cases, _ = route.run_points('boolean-transport', points, tmp_path/'native')
    assert len(cases) == len(points) == 2 * len(route.BOOLEAN_KEYS)
    assert all(case.state == 'completed' for case in cases)
    for point in points:
        case = next(case for case in cases if dict(case.inputs) == point)
        for key in point.keys() & route.BOOLEAN_KEYS:
            assert case.inputs[key] is point[key]
