"""DE-RISK 2: the promoted route is still the proof-of-life's route.

The promoted structure — adapter, shim, identity document, definition, export —
must reproduce both committed CSVs byte for byte. If it does not, every gate built
on it is being built on a route that is not the one that produced the evidence.

The 19-point availability sweep runs in the default suite because it fails first and
cheaply. The 948-point grid runs behind ``-m slow``.

The committed proof-of-life directory is read and never written; both studies export
to ``tmp_path``, outside the repository.
"""

import sys

import jsonschema
import pytest


@pytest.fixture
def promoted(era_simkit_path, repo_root):
    studies = repo_root / "exploration" / "stellarator_e2e" / "studies"
    for path in (str(studies), str(repo_root)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import promotion_equivalence

    return promotion_equivalence


def first_difference(got_bytes: bytes, expected_bytes: bytes) -> str:
    got = got_bytes.decode().splitlines()
    expected = expected_bytes.decode().splitlines()
    for i, (a, b) in enumerate(zip(got, expected)):
        if a != b:
            return f"first difference at line {i + 1}:\n  got      {a}\n  expected {b}"
    return f"line counts differ: got {len(got)}, expected {len(expected)}"


def _committed(repo_root, name):
    return (repo_root / "exploration" / "stellarator_e2e" / "study" / name).read_bytes()


def test_the_availability_sweep_reproduces_byte_for_byte(promoted, tmp_path, repo_root):
    out = promoted.run_availability_sweep(tmp_path)
    expected = _committed(repo_root, "availability_sweep.csv")
    got = out.read_bytes()
    assert got == expected, first_difference(got, expected)


@pytest.mark.slow
def test_the_design_search_grid_reproduces_byte_for_byte(promoted, tmp_path, repo_root):
    out = promoted.run_design_search(tmp_path)
    expected = _committed(repo_root, "design_search_R_a.csv")
    got = out.read_bytes()
    assert got == expected, first_difference(got, expected)


def test_the_grid_is_the_same_948_points_the_proof_of_life_ran(promoted):
    """Cheap structural half of the slow test: the point set, without executing it."""
    proposals = promoted.design_search_proposals()
    assert len(proposals) == 948
    assert len(promoted.availability_sweep_proposals()) == 19


def test_the_route_executes_the_baseline_and_deposits_both_documents(
    promoted, tmp_path, repo_root, load_schema
):
    """D1: preflight's inputs come into existence here, which is why this step is first."""
    written = promoted.execute_baseline(tmp_path)
    import json

    identity_doc = json.loads(written["identity"].read_text())
    result = json.loads(written["baseline_result"].read_text())
    jsonschema.validate(identity_doc, load_schema("package_identity.v1"))
    jsonschema.validate(result, load_schema("baseline_result.v1"))

    # Identity continuity: the point ran under the identity the document declares.
    assert result["executed_under"]["identity_digest"] == identity_doc["identity"]["digest"]

    manifest = json.loads(
        (repo_root / "exploration" / "stellarator_e2e" / "studies" / "manifest.json").read_text()
    )
    headline = manifest["baseline"]["headline"]
    got = result["channels"][headline["channel"]]
    assert abs(got - headline["value"]) / abs(headline["value"]) < 1e-9, got
    assert result["point"] == {k: float(v) for k, v in manifest["baseline"]["point"].items()}

    # source_local_identity comes from the contract's catalog (S3), not the era view.
    pinned = {v["source_local_identity"]: v["expected"] for v in manifest["baseline"]["verdicts"]}
    executed = {v["source_local_identity"]: v["status"] for v in result["verdicts"]}
    assert executed == pinned


def test_the_committed_evidence_is_never_written(promoted, tmp_path, repo_root):
    from scripts.study import common

    promoted.run_availability_sweep(tmp_path)
    common.assert_tree_clean(repo_root / "exploration" / "stellarator_e2e" / "study")
    common.assert_tree_clean(repo_root / "exploration" / "stellarator_e2e" / "pkg")
