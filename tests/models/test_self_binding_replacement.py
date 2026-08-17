"""The D-5 migrated whole-plant model generates, and mutations arrive — publicly.

self-binding-replacement Phase 4 (sysml-codegen `.project/active/self-binding-replacement/`).
The customer model used to carry 15 self-named bindings per model set (`in gain = gain`),
which the exact route refuses as `SI_SELF_BINDING`. After the mechanical D-5 migration the
model must not merely generate: an off-default mutation of a migrated design attribute must
reach **every and only** its bound consumers, read off shipped public artifacts
(`inputs/*.json`, `pipelines/pipeline.yaml`, `contracts/model_contract.json`) — TEAx
execution is out of scope.

Every test works on copies under pytest temporary directories; tracked models are never
rewritten. All tests need a live SysIDE license and **fail** (never skip) without one.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest
import yaml
from sysml_codegen.cli import GenerationConfig, run_codegen
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot

REPO = Path(__file__).resolve().parents[2]

#: The two synchronized customer model sets (D12).
MODEL_SETS = ("models", "exploration/ife_e2e/models")

#: The 11 renamed-supplier keys — the migrated formals' supplying attributes.
EXPECTED_ELEVEN = {
    "hif_plant_pkg__hif_plant__availability",
    "hif_plant_pkg__hif_plant__discount_rate",
    "hif_plant_pkg__hif_plant__frequency",
    "hif_plant_pkg__hif_plant__gain",
    "hif_plant_pkg__hif_plant__net_electric_power_gw",
    "hif_plant_pkg__hif_plant__om_cost_constant",
    "hif_plant_pkg__hif_plant__plant_cost_constant",
    "hif_plant_pkg__hif_plant__thermal_efficiency",
    "hif_plant_pkg__hif_plant__thermal_power_gw",
    "hif_plant_pkg__hif_plant__driver__beam_energy_mj",
    "hif_plant_pkg__hif_plant__driver__num_chambers",
}

#: The seven design attributes the migration must NOT have renamed-supplied.
NON_RENAMED_DESIGN = {
    "hif_plant_pkg__hif_plant__driver__efficiency",
    "hif_plant_pkg__hif_plant__driver__energy",
    "hif_plant_pkg__hif_plant__driver__lifetime_shots",
    "hif_plant_pkg__hif_plant__driver__pulse_rate_ref",
    "hif_plant_pkg__hif_plant__chamber__blanket_energy_multiple",
    "hif_plant_pkg__hif_plant__chamber__yield_cost_constant",
    "hif_plant_pkg__hif_plant__target_factory__cost_per_target",
}

LIBRARY_DEFAULTS = {
    "hif_plant_pkg__hif_plant__lcoe_calc__construction_years",
    "hif_plant_pkg__hif_plant__lcoe_calc__operational_years",
    "hif_plant_pkg__hif_plant__viability__threshold",
}

USAGE_LITERALS = {
    "hif_plant_pkg__hif_plant__meier_capital_calc__target_factory_cost",
    "hif_plant_pkg__hif_plant__meier_reactor_cost_calc__num_units",
}

#: Mutated sources as complete public identities: ``(input group, key)``. A bare
#: key is not an identity — two groups could mint the same key and a merged dict
#: would hide one of them (audit F1).
GAIN_SOURCE = ("hif_plant_params", "hif_plant_pkg__hif_plant__gain")
BEAM_SOURCE = ("hif_plant_params", "hif_plant_pkg__hif_plant__driver__beam_energy_mj")

#: Every bound consumer of the two mutated sources as complete ``(module, formal)``
#: port identities — a ``{module: formal}`` dict would collapse two bound ports on
#: one module (audit F1). The viability constraint module is a consumer of gain —
#: the consumer class every-and-only has historically dropped.
GAIN_CONSUMERS = {
    ("hif_plant_pkg__hif_plant__lcoe_calc", "gain_in"),
    ("hif_plant_pkg__hif_plant__recirc_calc", "gain_in"),
    ("hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b", "gain_in"),
}
BEAM_CONSUMERS = {
    ("hif_plant_pkg__hif_plant__driver__meier_cost", "beam_energy_mj_in"),
}

VIABILITY_DEF_QN = "fusion_cycle::'Viability Threshold'"
VIABILITY_FORMAL_QN = "fusion_cycle::'Viability Threshold'::gain_in"


@pytest.fixture(scope="module", autouse=True)
def license_must_be_loaded() -> None:
    """The plan accepts no license skip: a run without the key is a failed run."""
    assert os.environ.get("SYSIDE_LICENSE_KEY"), (
        "SYSIDE_LICENSE_KEY is not loaded; source /home/reid/1cfe/agentic-mbse/.env — "
        "this suite must fail, not skip, without it"
    )


def _copy_set(destination: Path, model_set: str = "models") -> Path:
    target = destination / "model_copy"
    shutil.copytree(REPO / model_set, target)
    return target


def _generate(models: Path, output: Path) -> bool:
    return run_codegen(
        GenerationConfig(
            output_path=output,
            models_path=models,
            package_name="self_binding_check",
            overwrite=True,
        )
    )


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _entry_sources(output: Path) -> dict[tuple[str, str], float]:
    """Every shipped input value keyed by its complete ``(group, key)`` identity.

    Asserts identity uniqueness both ways: no ``(group, key)`` repeats, and no
    bare key appears in two groups — either duplication would let a merged view
    silently drop a value (audit F1).
    """
    sources: dict[tuple[str, str], float] = {}
    for group_file in sorted((output / "inputs").glob("*.json")):
        group = group_file.stem
        for key, value in json.loads(group_file.read_text()).items():
            identity = (group, key)
            assert identity not in sources, f"duplicate input identity {identity}"
            sources[identity] = value
    bare_keys = [key for (_group, key) in sources]
    assert len(bare_keys) == len(set(bare_keys)), (
        "a bare key appears in more than one input group; the oracle must not merge"
    )
    return sources


def _parameters(output: Path) -> list[dict]:
    contract = json.loads((output / "contracts" / "model_contract.json").read_text())
    return contract["parameters"]


def _consumers_of(output: Path, source: tuple[str, str]) -> set[tuple[str, str]]:
    """Complete ``(module, formal)`` port identities wired to one ``(group, key)``.

    The pipeline serializes an entry-point input as ``"<type> <group>.<key>"``;
    the match is on the exact source token, never a suffix, and every bound port
    is kept — two ports on one module stay two identities (audit F1)."""
    group, key = source
    expected = f"{group}.{key}"
    pipeline = yaml.safe_load((output / "pipelines" / "pipeline.yaml").read_text())
    consumers: set[tuple[str, str]] = set()
    for name, module in pipeline["modules"].items():
        if module.get("module_type") == "EntryPoint":
            continue
        for formal, wired in (module.get("inputs") or {}).items():
            if not isinstance(wired, str):
                continue
            parts = wired.split()
            if len(parts) == 2 and parts[1] == expected:
                consumers.add((name, formal))
    return consumers


def _predicate_feature_refs(entry: dict) -> list[dict]:
    """Every ``feature_ref`` reference node in a catalog entry's predicate IR,
    walked structurally from the parsed JSON — never matched as substrings."""
    predicate = json.loads(entry["predicate_ir"])
    references: list[dict] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            if node.get("kind") == "feature_ref":
                references.append(node["reference"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(predicate)
    return references


def _mutated_copy(destination: Path, original: str, replacement: str) -> Path:
    models = _copy_set(destination)
    site = models / "designs" / "hif_ife" / "hif_plant.sysml"
    text = site.read_text()
    assert text.count(original) == 1, f"mutation site not unique: {original!r}"
    site.write_text(text.replace(original, replacement))
    return models


@pytest.fixture(scope="module")
def baseline(tmp_path_factory) -> Path:
    """One live generation of a copy of ``models/``; the package all oracles read."""
    root = tmp_path_factory.mktemp("baseline")
    output = root / "package"
    assert _generate(_copy_set(root), output), (
        "the migrated customer model must generate with zero readiness diagnostics"
    )
    return output


@pytest.mark.parametrize("model_set", MODEL_SETS)
def test_each_model_set_generates_with_zero_readiness_diagnostics(
    model_set: str, tmp_path: Path
) -> None:
    """Both synchronized sets, independently: generation (which seals) succeeds."""
    assert _generate(_copy_set(tmp_path, model_set), tmp_path / "package"), model_set


def test_live_and_snapshot_generation_are_byte_identical(tmp_path: Path) -> None:
    """The v6 snapshot route reproduces the live package exactly."""
    models = _copy_set(tmp_path)
    live = tmp_path / "live"
    assert _generate(models, live)

    snapshot = tmp_path / "instance_graph_snapshot.json"
    capture_instance_graph_snapshot([models], snapshot)
    from_snapshot = tmp_path / "from_snapshot"
    assert run_codegen(
        GenerationConfig(
            output_path=from_snapshot,
            from_snapshot=snapshot,
            package_name="self_binding_check",
            overwrite=True,
        )
    )

    assert _tree_bytes(live) == _tree_bytes(from_snapshot)


def test_full_classification_oracle_is_23_entry_points_18_design_attributes(
    baseline: Path,
) -> None:
    parameters = _parameters(baseline)
    by_type: dict[str, set[str]] = {}
    for parameter in parameters:
        by_type.setdefault(parameter["entry_type"], set()).add(
            parameter["qualified_name"]
        )
    assert len(parameters) == 23, sorted(p["qualified_name"] for p in parameters)
    assert len(by_type["design_attribute"]) == 18
    assert by_type["library_default"] == LIBRARY_DEFAULTS
    assert by_type["usage_literal"] == USAGE_LITERALS


def test_renamed_supplier_sub_oracle_is_exactly_the_eleven_keys(baseline: Path) -> None:
    """The migrated formals' suppliers: every one a design-attribute entry point
    keyed by its display path, present in exactly one shipped input group with a
    numeric value."""
    design = {
        p["qualified_name"]
        for p in _parameters(baseline)
        if p["entry_type"] == "design_attribute"
    }
    assert EXPECTED_ELEVEN <= design, sorted(EXPECTED_ELEVEN - design)
    assert design - NON_RENAMED_DESIGN == EXPECTED_ELEVEN

    sources = _entry_sources(baseline)
    for expected_key in EXPECTED_ELEVEN:
        carriers = [
            (group, key, value)
            for (group, key), value in sources.items()
            if key == expected_key
        ]
        assert len(carriers) == 1, f"{expected_key}: {carriers}"
        assert isinstance(carriers[0][2], (int, float)), carriers


def test_the_seven_non_renamed_design_attributes_survive_unrenamed(
    baseline: Path,
) -> None:
    design = {
        p["qualified_name"]
        for p in _parameters(baseline)
        if p["entry_type"] == "design_attribute"
    }
    assert NON_RENAMED_DESIGN <= design, sorted(NON_RENAMED_DESIGN - design)


def test_gain_mutation_reaches_every_and_only_its_three_consumers(
    baseline: Path, tmp_path: Path
) -> None:
    """The spine. 80.0 → 81.0 at the one authored site: exactly the gain source
    identity moves, and its consumers are the two calc modules plus the viability
    constraint module — asserted structurally down to the constraint's formal."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_copy(tmp_path, ":>> gain = 80.0", ":>> gain = 81.0"), mutated
    )

    before, after = _entry_sources(baseline), _entry_sources(mutated)
    assert set(before) == set(after)
    changed = {source for source in before if before[source] != after[source]}
    assert changed == {GAIN_SOURCE}
    assert after[GAIN_SOURCE] == 81.0

    assert _consumers_of(mutated, GAIN_SOURCE) == GAIN_CONSUMERS

    catalog = json.loads(
        (mutated / "contracts" / "model_contract.json").read_text()
    )["constraint_catalog"]
    viability = [
        entry
        for entry in catalog["concrete_entries"]
        if entry["definition_qualified_name"] == VIABILITY_DEF_QN
    ]
    assert len(viability) == 1

    # The formal identity, read structurally from the parsed predicate IR: the
    # predicate consumes gain through exactly one feature reference whose target
    # is the renamed formal on the constraint's own definition — never a
    # substring match over the serialized payload (audit F2).
    gain_refs = [
        reference
        for reference in _predicate_feature_refs(viability[0])
        if reference["target"]["qualified_name"] == VIABILITY_FORMAL_QN
    ]
    assert len(gain_refs) == 1, gain_refs
    assert gain_refs[0]["source_name"] == "gain_in"
    assert gain_refs[0]["target"]["kind"] == "AttributeUsage"


def test_beam_energy_mutation_reaches_its_nested_consumer_and_nothing_else(
    baseline: Path, tmp_path: Path
) -> None:
    """A second occurrence depth: the nested driver's beam_energy_mj. Only the
    nested source identity moves, and every bound consumer port is enumerated —
    never weakened to 'the package still generates'."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_copy(
            tmp_path, ":>> beam_energy_mj = 5.0;", ":>> beam_energy_mj = 6.5;"
        ),
        mutated,
    )

    before, after = _entry_sources(baseline), _entry_sources(mutated)
    assert set(before) == set(after)
    changed = {source for source in before if before[source] != after[source]}
    assert changed == {BEAM_SOURCE}
    assert after[BEAM_SOURCE] == 6.5

    assert _consumers_of(mutated, BEAM_SOURCE) == BEAM_CONSUMERS


def test_the_two_maintained_model_trees_cannot_diverge() -> None:
    """The retained cross-tree gate (audit F2): the customer keeps two
    synchronized model sets, and the spine's mutations run against ``models/``.
    That coverage is only honest while the trees agree, so this kept test fails
    on any divergence — a missing counterpart or a byte difference — instead of
    letting the second tree drift silently. The exploration set stores the
    library files without the ``library/`` prefix; the mapping below is that
    layout fact, not a fuzz."""
    primary_root = REPO / MODEL_SETS[0]
    secondary_root = REPO / MODEL_SETS[1]

    def logical(path: Path, root: Path, strip_library: bool) -> str:
        relative = path.relative_to(root).as_posix()
        if strip_library and relative.startswith("library/"):
            relative = relative[len("library/") :]
        return relative

    primary = {
        logical(path, primary_root, strip_library=True): path
        for path in sorted(primary_root.rglob("*.sysml"))
    }
    secondary = {
        logical(path, secondary_root, strip_library=False): path
        for path in sorted(secondary_root.rglob("*.sysml"))
    }
    assert set(primary) == set(secondary), (
        sorted(set(primary) ^ set(secondary))
    )
    diverged = [
        name
        for name in sorted(primary)
        if primary[name].read_bytes() != secondary[name].read_bytes()
    ]
    assert diverged == [], diverged
