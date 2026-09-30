"""The stock magnet_materials manifest binds a real package-level oracle entry and declares its tolerances.

Finding 20260929-magnet-material-comparison#2: the stock manifest named an oracle module that did not exist and
carried no tolerance clause, so the stock verifier could not run from it. These tests load the manifest the way
`scripts/study/verify.py` does (its own loader, no shortcut), require both published surfaces, and check the
tolerance clause covers exactly the channels the verifier compares (contract r3 section 8: rel 1e-9 or abs 1e-9
per unit). The baseline point then reproduces the pinned headline and every pinned verdict through the entry.
Run: .codex-test/run python -m pytest tests/study/test_magnet_materials_oracle_entry.py -q
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest

from scripts.study import common, verify
from scripts.study import manifest as manifest_mod

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "exploration" / "magnet_materials" / "studies" / "manifest.json"
MODULE = "exploration.magnet_materials.studies.oracle_entry"
CONTRACT_TOLERANCE = 1e-9
CONSTANT_CHANNEL_COUNT = 9  # nb3sn eps_min, k_a, k_d, k_g, k_i; rebco k_a, k_d, k_g, k_i


@pytest.fixture(scope="module")
def loaded():
    return manifest_mod.load(MANIFEST)


@pytest.fixture(scope="module")
def entry(loaded):
    module, evaluate, bindings = verify.load_oracle(loaded)
    return module, evaluate, bindings


@pytest.fixture(scope="module")
def catalog(loaded):
    package = manifest_mod.repo_root() / loaded.data["package"]["path"]
    contract = json.loads((package / "contracts" / "model_contract.json").read_text())
    entries = {e["constraint_id"]: e for e in contract["constraint_catalog"]["concrete_entries"]}
    return entries, verify.package_input_values(package)


def test_manifest_names_the_package_level_module_and_the_verifier_can_load_it(loaded, entry):
    block = loaded.data["oracle"]
    assert block["module"] == MODULE
    assert block["sys_path"] == "."
    assert block["callable"] == "evaluate"
    module, evaluate, bindings = entry
    assert module.__name__ == MODULE
    assert callable(evaluate) and evaluate is module.evaluate
    assert callable(module.operand_bindings) and callable(module.constant_channels)
    assert bindings and all(table for table in bindings.values())


def test_manifest_declares_the_contract_tolerance_on_every_compared_channel(loaded, entry):
    module, _, bindings = entry
    declared = loaded.data["absolute_tolerances"]
    assert declared, "the stock manifest carries no absolute_tolerances clause"
    objectives = set(verify.objective_channels(loaded))
    bound = {b["key"] for table in bindings.values() for b in table.values() if b["kind"] == "channel"}
    assert {t["channel"] for t in declared} == objectives | bound  # exactly what verify.py compares
    assert all(t["value"] == CONTRACT_TOLERANCE for t in declared)
    assert all("section 8" in t["basis"] for t in declared)
    constants = set(module.constant_channels())
    assert len(constants) == CONSTANT_CHANNEL_COUNT
    assert not constants & {t["channel"] for t in declared}, "constant channels are excluded, never toleranced"



def test_baseline_point_reproduces_the_pinned_headline_and_verdicts(loaded, entry, catalog):
    module, evaluate, bindings = entry
    baseline = loaded.data["baseline"]
    channels = evaluate(baseline["point"])
    assert all(isinstance(v, float) and math.isfinite(v) for v in channels.values())
    assert not set(module.constant_channels()) & set(channels)
    headline = baseline["headline"]
    assert common.relative_deviation(headline["value"], channels[headline["channel"]]) < CONTRACT_TOLERANCE
    entries, package_inputs = catalog
    assert set(entries) == set(bindings)
    expected = {v["source_local_identity"]: v["expected"] for v in baseline["verdicts"]}
    for constraint_id, entry_doc in entries.items():
        satisfied, resolved = verify.derive_verdict(
            constraint_id, entry_doc, bindings, baseline["point"], package_inputs, channels
        )
        assert resolved >= 1
        assert ("satisfied" if satisfied else "violated") == expected[entry_doc["source_local_identity"]]


def test_operand_bindings_are_a_copy_a_caller_cannot_corrupt(entry):
    module, _, _ = entry
    first = module.operand_bindings()
    constraint_id = next(iter(first))
    first[constraint_id].clear()
    assert module.operand_bindings()[constraint_id], "operand_bindings() handed out its own state"


def test_unknown_entry_key_refuses(loaded, entry):
    _, evaluate, _ = entry
    point = copy.deepcopy(loaded.data["baseline"]["point"])
    point["magnet_subsystem__subsystem__duty__not_a_key"] = 1.0
    with pytest.raises(KeyError, match="unknown entry key"):
        evaluate(point)
