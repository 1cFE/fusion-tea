"""Invariant 3: the loader's accept-set is EXACTLY a TAMPER on the two glue files.

The adapter is a precisely scoped exception, not a relaxation of sealing. The test
that proves that is the negative one: modify a *third* sealed artifact and the load
must refuse. Without it, "accepts the documented glue edits" and "accepts anything"
look identical from the outside.
"""

import json
import shutil

import pytest


@pytest.fixture
def adapter(era_simkit_path, repo_root):
    import sys

    studies = repo_root / "exploration" / "stellarator_e2e" / "studies"
    if str(studies) not in sys.path:
        sys.path.insert(0, str(studies))
    import era_adapter

    return era_adapter


@pytest.fixture
def package_tree(real_package_path, tmp_path):
    """A writable copy. Asserts the source is intact before copying (Item 3's rule)."""
    contract = json.loads((real_package_path / "contracts" / "package_contract.json").read_text())
    assert contract["artifact_hashes"], "package contract carries no artifact hashes"
    dest = tmp_path / "pkg"
    shutil.copytree(real_package_path, dest)
    return dest


def _touch_json(path):
    """Change a sealed artifact's bytes, asserting the target first."""
    text = path.read_text()
    assert text.rstrip().endswith("}"), f"unexpected shape for {path}"
    path.write_text(text.rstrip()[:-1].rstrip().rstrip(",") + ',\n  "_probe_mutation": 1\n}\n')


def test_the_documented_glue_edits_still_load(adapter, package_tree, tmp_path):
    module, fingerprint = adapter.loader(package_tree, tmp_path / "link").load()
    assert module.__name__ == "stellarator_tea"
    assert fingerprint == adapter.effective_fingerprint(package_tree)
    # Never the sealed value: that is the whole point of the effective fingerprint.
    sealed = json.loads(
        (package_tree / "contracts" / "package_contract.json").read_text()
    )["executable_fingerprint"]
    assert fingerprint != sealed


def test_a_third_modified_sealed_artifact_is_refused(adapter, package_tree, tmp_path):
    from simkit.evaluation.package_load import SealVerificationError

    third = package_tree / "inputs" / "stellarator_plant_params.json"
    _touch_json(third)
    with pytest.raises(SealVerificationError) as exc:
        adapter.loader(package_tree, tmp_path / "link").load()
    assert "inputs/stellarator_plant_params.json" in str(exc.value)
    assert "beyond the documented glue edits" in str(exc.value)


def test_a_wrong_era_version_is_refused(adapter, package_tree, tmp_path):
    from simkit.evaluation.package_load import SealVerificationError

    contract_path = package_tree / "contracts" / "package_contract.json"
    contract = json.loads(contract_path.read_text())
    contract["runtime_contract_version"] = "99.0.0"
    contract_path.write_text(json.dumps(contract, indent=2))
    with pytest.raises(SealVerificationError) as exc:
        adapter.loader(package_tree, tmp_path / "link").load()
    assert "99.0.0" in str(exc.value)


def test_a_live_schema_filler_refuses_the_load(adapter, package_tree, tmp_path):
    """The dead-filler assertion is adapter-owned and runs on every load (Invariant 8)."""
    spec = package_tree / "pipelines" / "mfe_stellarator.yaml"
    text = spec.read_text()
    assert "MFE_Power_Plant__p_" not in text, "the fillers are already live in the committed spec"
    spec.write_text(text + "\n# resurrected: mfe_plant__MFE_Power_Plant__p_th\n")
    with pytest.raises(adapter.EraAdapterError) as exc:
        adapter.assert_schema_fillers_are_dead(package_tree, spec)
    assert "LIVE" in str(exc.value) and "circular" in str(exc.value)


def test_the_era_pin_is_asserted_not_merely_recorded(adapter, tmp_path):
    """Point the check at a directory that is not the pinned worktree."""

    class FakeSimkit:
        __file__ = str(tmp_path / "packages" / "teax-simkit" / "simkit" / "__init__.py")

    with pytest.raises(adapter.EraAdapterError) as exc:
        adapter.assert_era_pin(FakeSimkit)
    assert adapter.ERA_PIN_COMMIT in str(exc.value)
    assert "era pin violated" in str(exc.value)


def test_the_real_era_passes_the_pin_check(adapter, era_simkit_path):
    import simkit

    assert adapter.assert_era_pin(simkit).startswith(adapter.ERA_PIN_COMMIT)


def test_the_adapter_declares_exactly_three_sources(adapter, repo_root):
    """Invariant 4: every file that can move a number or the accept-set."""
    assert adapter.DECLARED_SOURCES == (
        "exploration/stellarator_e2e/studies/era_adapter.py",
        "exploration/stellarator_e2e/studies/oracle_entry.py",
        "exploration/stellarator_e2e/verify_stellaris.py",
    )
    for rel in adapter.DECLARED_SOURCES:
        assert (repo_root / rel).is_file(), rel


def test_the_identity_document_declares_the_accept_set_as_its_allowed_set(
    adapter, real_package_path, load_schema
):
    import jsonschema

    doc = adapter.identity_document(real_package_path)
    jsonschema.validate(doc, load_schema("package_identity.v1"))
    assert [f["path"] for f in doc["identity"]["allowed_modified_files"]] == sorted(
        adapter.GLUE_EDITED_FILES
    )
    assert [r["rung"] for r in doc["glue_ledger"]] == ["g1", "g2", "g3"]
    not_verified = [r["rung"] for r in doc["glue_ledger"] if not r["independently_verified"]]
    assert not_verified == ["g3"], "the CAS27 rung is the one fed identically to both sides"
