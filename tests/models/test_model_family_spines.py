"""Each design family generates alone from the canonical tree, and mutations arrive -- publicly.

`models/` holds two design families (IFE and MFE) that share three foundation files
(`tests/model_families.py`, design D6–D8 of the stellarator model migration). This module
is the regression spine for both, replacing the migration-era
`test_self_binding_replacement.py` whose assertions assumed `models/` was one IFE plant:

* **twins** -- every canonical file owned by a family is byte-identical to that family's
  exploration twin, the owned paths cover every canonical file, and the shared files agree
  in all three homes;
* **generation** -- each family's materialized canonical subset generates with zero
  readiness diagnostics (which seals), and the v6 snapshot route reproduces the live
  package byte for byte;
* **census** -- the entry-point classification is exact: IFE keeps 23 entry points / 18
  design attributes (the D-5 migration's eleven renamed-supplier identities and seven
  unrenamed ones merged into one neutral set, design D7); MFE is the census captured from
  its first clean 2.0.0 package (`data/mfe_census.json`), bound to the semantic
  fingerprint it was derived against;
* **mutations** -- an off-default mutation of one authored design attribute reaches
  **every and only** its bound consumers, read off shipped public artifacts
  (`inputs/*.json`, `pipelines/pipeline.yaml`, `contracts/model_contract.json`): two IFE
  proofs (unchanged) and two MFE proofs (CAS28 capital, a nested radial-build thickness).

Every test works on copies under pytest temporary directories; tracked models are never
rewritten. All generating tests need a live SysIDE license and **fail** (never skip)
without one. TEAx execution is out of scope here (`tests/test_*_teax.py`).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import yaml
from sysml_codegen.cli import GenerationConfig, run_codegen
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot

from tests.model_families import (
    FAMILIES,
    SHARED_PATHS,
    Family,
    canonical_files,
    canonical_path,
    materialize_canonical_subset,
)

REPO = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parent / "data"

# ------------------------------------------------------------------ IFE expectations
#: The IFE design-attribute census: the eleven keys the D-5 migration renamed the
#: suppliers of and the seven it did not, merged into one neutral set (D7). The
#: partition was a one-time migration fact; the set is the regression guard.
IFE_DESIGN_ATTRIBUTES = {
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
    "hif_plant_pkg__hif_plant__driver__efficiency",
    "hif_plant_pkg__hif_plant__driver__energy",
    "hif_plant_pkg__hif_plant__driver__lifetime_shots",
    "hif_plant_pkg__hif_plant__driver__pulse_rate_ref",
    "hif_plant_pkg__hif_plant__chamber__blanket_energy_multiple",
    "hif_plant_pkg__hif_plant__chamber__yield_cost_constant",
    "hif_plant_pkg__hif_plant__target_factory__cost_per_target",
}
IFE_LIBRARY_DEFAULTS = {
    "hif_plant_pkg__hif_plant__lcoe_calc__construction_years",
    "hif_plant_pkg__hif_plant__lcoe_calc__operational_years",
    "hif_plant_pkg__hif_plant__viability__threshold",
}
IFE_USAGE_LITERALS = {
    "hif_plant_pkg__hif_plant__meier_capital_calc__target_factory_cost",
    "hif_plant_pkg__hif_plant__meier_reactor_cost_calc__num_units",
}

#: Mutated sources as complete public identities: ``(input group, key)``. A bare key is
#: not an identity -- two groups could mint the same key (audit F1).
GAIN_SOURCE = ("hif_plant_params", "hif_plant_pkg__hif_plant__gain")
BEAM_SOURCE = ("hif_plant_params", "hif_plant_pkg__hif_plant__driver__beam_energy_mj")
#: Every bound consumer as complete ``(module, formal)`` port identities (audit F1).
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

# ------------------------------------------------------------------ MFE expectations
P = "stellarator_09__stellaris__"
CAS28_SOURCE = ("stellarator_plant_params", f"{P}cas28_capital")
CAS28_CONSUMERS = {
    (f"{P}cas23_to_28_capital", "cas28_capital"),
    (f"{P}cas2x_pre_contingency", "cas28_capital"),
}
BLANKET_T_SOURCE = ("stellarator_plant_params", f"{P}blanket_t")
BLANKET_T_CONSUMERS = {(f"{P}rb", "blanket_t_in")}


@pytest.fixture(scope="module", autouse=True)
def license_must_be_loaded() -> None:
    """A run without the key is a failed run, not a skipped one."""
    assert os.environ.get("SYSIDE_LICENSE_KEY"), (
        "SYSIDE_LICENSE_KEY is not loaded; source /home/reid/1cfe/agentic-mbse/.env — "
        "this suite must fail, not skip, without it"
    )


# ------------------------------------------------------------------------ helpers


def _generate(models: Path, output: Path, package_name: str) -> bool:
    return run_codegen(
        GenerationConfig(
            output_path=output,
            models_path=models,
            package_name=package_name,
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

    Asserts identity uniqueness both ways: no ``(group, key)`` repeats, and no bare key
    appears in two groups -- either duplication would let a merged view silently drop a
    value (audit F1).
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


def _contract(output: Path) -> dict:
    return json.loads((output / "contracts" / "model_contract.json").read_text())


def _by_entry_type(output: Path) -> dict[str, set[str]]:
    by_type: dict[str, set[str]] = {}
    for parameter in _contract(output)["parameters"]:
        by_type.setdefault(parameter["entry_type"], set()).add(parameter["qualified_name"])
    return by_type


def _consumers_of(output: Path, source: tuple[str, str]) -> set[tuple[str, str]]:
    """Complete ``(module, formal)`` port identities wired to one ``(group, key)``.

    The pipeline serializes an entry-point input as ``"<type> <group>.<key>"``; the match
    is on the exact source token, never a suffix, and every bound port is kept."""
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
    """Every ``feature_ref`` node in a catalog entry's predicate IR, walked structurally."""
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


def _subset(destination: Path, family: Family) -> Path:
    return materialize_canonical_subset(family, destination / "model_copy")


def _mutated_subset(
    destination: Path, family: Family, logical_site: str, original: str, replacement: str
) -> Path:
    models = _subset(destination, family)
    site = models / logical_site
    text = site.read_text()
    assert text.count(original) == 1, f"mutation site not unique: {original!r}"
    site.write_text(text.replace(original, replacement))
    return models


def _assert_every_and_only(
    baseline: Path, mutated: Path, source: tuple[str, str], value: float, consumers: set
) -> None:
    before, after = _entry_sources(baseline), _entry_sources(mutated)
    assert set(before) == set(after)
    changed = {identity for identity in before if before[identity] != after[identity]}
    assert changed == {source}
    assert after[source] == value
    assert _consumers_of(mutated, source) == consumers


@pytest.fixture(scope="module")
def baselines(tmp_path_factory) -> dict[str, Path]:
    """One live generation per family from its materialized canonical subset."""
    packages: dict[str, Path] = {}
    for name, family in FAMILIES.items():
        root = tmp_path_factory.mktemp(f"baseline-{name}")
        output = root / "package"
        assert _generate(_subset(root, family), output, family.package_name), (
            f"{name}: the canonical subset must generate with zero readiness diagnostics"
        )
        packages[name] = output
    return packages


# --------------------------------------------------------------------- the twins


def test_owned_paths_cover_every_canonical_file() -> None:
    """D8: the union of the families' owned paths is exactly the canonical tree."""
    owned = {path for family in FAMILIES.values() for path in family.owned}
    assert owned == set(canonical_files()), sorted(owned ^ set(canonical_files()))


@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_canonical_files_equal_the_family_twin_byte_for_byte(family: str) -> None:
    """I9: the twin stores the library files without the ``library/`` prefix; every owned
    canonical file has a twin counterpart with the same bytes, and the twin has no extra."""
    spec = FAMILIES[family]
    twin_files = {
        path.relative_to(spec.twin).as_posix() for path in spec.twin.rglob("*.sysml")
    }
    assert twin_files == set(spec.owned), sorted(twin_files ^ set(spec.owned))
    diverged = [
        logical
        for logical in spec.owned
        if canonical_path(logical).read_bytes() != (spec.twin / logical).read_bytes()
    ]
    assert diverged == [], diverged


def test_shared_files_agree_in_all_three_homes() -> None:
    assert SHARED_PATHS == (
        "cost_structure/cas_hierarchy.sysml",
        "foundation/costed_component.sysml",
        "foundation/economic_parameter.sysml",
    )
    for logical in SHARED_PATHS:
        canonical = canonical_path(logical).read_bytes()
        for family in FAMILIES.values():
            assert (family.twin / logical).read_bytes() == canonical, (family.name, logical)


def test_the_layout_mapping_refuses_a_logical_path_collision(tmp_path: Path) -> None:
    """Audit falsifier: ``library/x.sysml`` and ``x.sysml`` must not collapse."""
    root = tmp_path / "models"
    (root / "library").mkdir(parents=True)
    (root / "library" / "x.sysml").write_text("package library_x {}\n")
    (root / "x.sysml").write_text("package root_x {}\n")
    with pytest.raises(AssertionError, match="logical path collision"):
        canonical_files(root)


# ----------------------------------------------------------------- generation


@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_family_subset_generates_and_live_equals_snapshot(family: str, tmp_path: Path) -> None:
    """Each family alone: generation (which seals) succeeds, and the v6 snapshot route
    reproduces the live package exactly."""
    spec = FAMILIES[family]
    models = _subset(tmp_path, spec)
    live = tmp_path / "live"
    assert _generate(models, live, spec.package_name), family

    snapshot = tmp_path / "instance_graph_snapshot.json"
    capture_instance_graph_snapshot([models], snapshot)
    from_snapshot = tmp_path / "from_snapshot"
    assert run_codegen(
        GenerationConfig(
            output_path=from_snapshot,
            from_snapshot=snapshot,
            package_name=spec.package_name,
            overwrite=True,
        )
    )
    assert _tree_bytes(live) == _tree_bytes(from_snapshot)


# --------------------------------------------------------------------- censuses


def test_ife_census_is_23_entry_points_18_design_attributes(baselines) -> None:
    output = baselines["ife"]
    by_type = _by_entry_type(output)
    assert len(_contract(output)["parameters"]) == 23
    assert by_type["design_attribute"] == IFE_DESIGN_ATTRIBUTES
    assert len(by_type["design_attribute"]) == 18
    assert by_type["library_default"] == IFE_LIBRARY_DEFAULTS
    assert by_type["usage_literal"] == IFE_USAGE_LITERALS

    sources = _entry_sources(output)
    for expected_key in IFE_DESIGN_ATTRIBUTES:
        carriers = [(g, k, v) for (g, k), v in sources.items() if k == expected_key]
        assert len(carriers) == 1, f"{expected_key}: {carriers}"
        assert isinstance(carriers[0][2], (int, float)), carriers


def test_mfe_census_is_the_one_captured_from_the_first_clean_package(baselines) -> None:
    """Bound to the semantic fingerprint it was derived against: a regenerated model
    re-derives the fixture from the new package, never patches it to match."""
    output = baselines["mfe"]
    expected = json.loads((DATA / "mfe_census.json").read_text())
    assert _contract(output)["semantic_fingerprint"] == (
        expected["derived_against_semantic_fingerprint"]
    ), "model meaning moved — re-derive tests/models/data/mfe_census.json from the new package"
    assert len(_contract(output)["parameters"]) == expected["entry_points"]
    assert {k: sorted(v) for k, v in _by_entry_type(output).items()} == expected["by_entry_type"]
    _entry_sources(output)  # identity uniqueness both ways


# -------------------------------------------------------------------- mutations


def test_ife_gain_mutation_reaches_every_and_only_its_three_consumers(
    baselines, tmp_path: Path
) -> None:
    """The spine. 80.0 → 81.0 at the one authored site: exactly the gain source identity
    moves, and its consumers are the two calc modules plus the viability constraint
    module -- asserted structurally down to the constraint's formal."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_subset(
            tmp_path, FAMILIES["ife"], "designs/hif_ife/hif_plant.sysml",
            ":>> gain = 80.0", ":>> gain = 81.0",
        ),
        mutated, FAMILIES["ife"].package_name,
    )
    _assert_every_and_only(baselines["ife"], mutated, GAIN_SOURCE, 81.0, GAIN_CONSUMERS)

    catalog = _contract(mutated)["constraint_catalog"]
    viability = [
        entry
        for entry in catalog["concrete_entries"]
        if entry["definition_qualified_name"] == VIABILITY_DEF_QN
    ]
    assert len(viability) == 1
    gain_refs = [
        reference
        for reference in _predicate_feature_refs(viability[0])
        if reference["target"]["qualified_name"] == VIABILITY_FORMAL_QN
    ]
    assert len(gain_refs) == 1, gain_refs
    assert gain_refs[0]["source_name"] == "gain_in"
    assert gain_refs[0]["target"]["kind"] == "AttributeUsage"


def test_ife_beam_energy_mutation_reaches_its_nested_consumer_and_nothing_else(
    baselines, tmp_path: Path
) -> None:
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_subset(
            tmp_path, FAMILIES["ife"], "designs/hif_ife/hif_plant.sysml",
            ":>> beam_energy_mj = 5.0;", ":>> beam_energy_mj = 6.5;",
        ),
        mutated, FAMILIES["ife"].package_name,
    )
    _assert_every_and_only(baselines["ife"], mutated, BEAM_SOURCE, 6.5, BEAM_CONSUMERS)


def test_mfe_cas28_capital_mutation_reaches_every_and_only_its_two_rollups(
    baselines, tmp_path: Path
) -> None:
    """SC10 on the stellarator: the CAS28 digital-twin constant the era adapter used to
    inject is an authored design attribute; moving it reaches exactly the two CAS2x
    rollups that bind it."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_subset(
            tmp_path, FAMILIES["mfe"], "designs/stellarator_09/stellarator_plant.sysml",
            ":>> cas28_capital = 5000000.0 {", ":>> cas28_capital = 6000000.0 {",
        ),
        mutated, FAMILIES["mfe"].package_name,
    )
    _assert_every_and_only(baselines["mfe"], mutated, CAS28_SOURCE, 6000000.0, CAS28_CONSUMERS)


def test_mfe_blanket_thickness_mutation_reaches_the_radial_build_and_nothing_else(
    baselines, tmp_path: Path
) -> None:
    """A nested occurrence: the blanket layer thickness feeds the radial build alone;
    everything downstream (blanket volume, CAS27, the outward layers) reaches it through
    the radial build's outputs, not through a second binding of the source."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_subset(
            tmp_path, FAMILIES["mfe"], "designs/stellarator_09/stellarator_plant.sysml",
            ":>> blanket_t = 0.80 {", ":>> blanket_t = 0.90 {",
        ),
        mutated, FAMILIES["mfe"].package_name,
    )
    _assert_every_and_only(
        baselines["mfe"], mutated, BLANKET_T_SOURCE, 0.9, BLANKET_T_CONSUMERS
    )
