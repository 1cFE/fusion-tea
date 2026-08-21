"""The regenerated stellarator package on the stock teax route.

stellarator-model-migration Phase 2 (`.project/active/stellarator-model-migration/plan.md`).
The package is sealed at runtime contract ``2.0.0`` by the pinned codegen; stock teax's
``ProvisionalPackageLoader`` must accept it with ``strict=True``, its study identity must be
the sealed executable fingerprint itself (design D3, invariant I5), and the five values the
era adapter used to inject must arrive from model source (invariant I6, bet B2):

* g1 -- the four BOP ``power`` inputs are wired to power-balance outputs;
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

    # g1: every BOP power input reads a power-balance output, not a shipped input.
    bop_power_sources = {
        name: module["inputs"]["power"].split()[-1]
        for name, module in modules.items()
        if isinstance((module.get("inputs") or {}).get("power"), str)
    }
    assert bop_power_sources, "no module binds a `power` input"
    for name, source in bop_power_sources.items():
        assert "__pb__" in source, (name, source)
