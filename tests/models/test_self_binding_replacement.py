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

GAIN_KEY = "hif_plant_pkg__hif_plant__gain"
BEAM_KEY = "hif_plant_pkg__hif_plant__driver__beam_energy_mj"

#: Every bound consumer of the two mutated keys, by pipeline module name and the
#: formal it binds. The viability constraint module is a consumer of gain — the
#: consumer class every-and-only has historically dropped.
GAIN_CONSUMERS = {
    "hif_plant_pkg__hif_plant__lcoe_calc": "gain_in",
    "hif_plant_pkg__hif_plant__recirc_calc": "gain_in",
    "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b": "gain_in",
}
BEAM_CONSUMERS = {
    "hif_plant_pkg__hif_plant__driver__meier_cost": "beam_energy_mj_in",
}

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


def _entry_values(output: Path) -> dict[str, float]:
    values: dict[str, float] = {}
    for group in sorted((output / "inputs").glob("*.json")):
        values.update(json.loads(group.read_text()))
    return values


def _parameters(output: Path) -> list[dict]:
    contract = json.loads((output / "contracts" / "model_contract.json").read_text())
    return contract["parameters"]


def _consumers_of(output: Path, key: str) -> dict[str, str]:
    """``{module_name: formal_name}`` for every pipeline input wired to ``key``."""
    pipeline = yaml.safe_load((output / "pipelines" / "pipeline.yaml").read_text())
    consumers: dict[str, str] = {}
    for name, module in pipeline["modules"].items():
        for formal, source in (module.get("inputs") or {}).items():
            if isinstance(source, str) and source.endswith("." + key):
                consumers[name] = formal
    return consumers


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
    keyed by its display path, present in the shipped inputs with a value."""
    design = {
        p["qualified_name"]
        for p in _parameters(baseline)
        if p["entry_type"] == "design_attribute"
    }
    assert EXPECTED_ELEVEN <= design, sorted(EXPECTED_ELEVEN - design)
    assert design - NON_RENAMED_DESIGN == EXPECTED_ELEVEN

    values = _entry_values(baseline)
    missing = [key for key in EXPECTED_ELEVEN if not isinstance(values.get(key), (int, float))]
    assert missing == [], missing


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
    """The spine. 80.0 → 81.0 at the one authored site: exactly the gain key moves,
    and its consumers are the two calc modules plus the viability constraint module
    — asserted by the constraint's formal identity, not only its module name."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_copy(tmp_path, ":>> gain = 80.0", ":>> gain = 81.0"), mutated
    )

    before, after = _entry_values(baseline), _entry_values(mutated)
    assert set(before) == set(after)
    changed = {key for key in before if before[key] != after[key]}
    assert changed == {GAIN_KEY}
    assert after[GAIN_KEY] == 81.0

    assert _consumers_of(mutated, GAIN_KEY) == GAIN_CONSUMERS

    catalog = json.loads(
        (mutated / "contracts" / "model_contract.json").read_text()
    )["constraint_catalog"]
    viability = [
        entry
        for entry in catalog["concrete_entries"]
        if entry["definition_qualified_name"] == "fusion_cycle::'Viability Threshold'"
    ]
    assert len(viability) == 1
    assert VIABILITY_FORMAL_QN in viability[0]["predicate_ir"], (
        "the constraint consumes gain through its own renamed formal identity"
    )


def test_beam_energy_mutation_reaches_its_nested_consumer_and_nothing_else(
    baseline: Path, tmp_path: Path
) -> None:
    """A second occurrence depth: the nested driver's beam_energy_mj. Only the
    nested key moves, and every bound consumer is enumerated — never weakened to
    'the package still generates'."""
    mutated = tmp_path / "package"
    assert _generate(
        _mutated_copy(
            tmp_path, ":>> beam_energy_mj = 5.0;", ":>> beam_energy_mj = 6.5;"
        ),
        mutated,
    )

    before, after = _entry_values(baseline), _entry_values(mutated)
    assert set(before) == set(after)
    changed = {key for key in before if before[key] != after[key]}
    assert changed == {BEAM_KEY}
    assert after[BEAM_KEY] == 6.5

    assert _consumers_of(mutated, BEAM_KEY) == BEAM_CONSUMERS
