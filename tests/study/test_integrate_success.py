"""SC1: one invocation, one candidate, every field resolving to something that exists.

The fixture is the committed stellarator package as it stands — WI-030's audited model
change, already integrated — so no new modeling work is minted to prove the seam works.
Its recorded fingerprints are the expected lineage the request names.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import integrate
from tests.study.conftest import read_return, run_seam_raw

REPO_ROOT = Path(__file__).resolve().parents[2]

CANDIDATE_FIELDS = (
    "package", "manifest", "pin", "semantic_fingerprint", "executable_fingerprint",
    "identity_document", "baseline_result", "verification_summary",
)


@pytest.fixture
def candidate_run(integration_workspace, tmp_path):
    """One full, passing invocation. Shared by the assertions below so it runs once."""
    out = tmp_path / "out"
    entry = integrate.package_digests(integration_workspace.package)
    done = run_seam_raw(integration_workspace.request_argv(out))
    document = read_return(done, out)
    assert done.returncode == 0, json.dumps(document["blocker"], indent=2)
    return {
        "document": document, "out": out, "entry": entry,
        "workspace": integration_workspace,
    }


def test_committed_package_yields_one_candidate(candidate_run):
    document = candidate_run["document"]
    assert document["class"] == "CANDIDATE"
    assert document["blocker"] is None
    assert document["exit_code"] == 0
    assert len(document["gates"]) == 10
    assert all(gate["status"] == "pass" for gate in document["gates"])
    assert all(gate["scope"] in ("repo", "request") for gate in document["gates"])


def test_every_candidate_field_resolves(candidate_run):
    """R-E3: a bare number with no home is not evidence."""
    candidate = candidate_run["document"]["candidate"]
    assert set(candidate) == set(CANDIDATE_FIELDS)
    for field in ("package", "manifest", "identity_document", "baseline_result",
                  "verification_summary"):
        assert (REPO_ROOT / candidate[field]).exists(), field
    for field in ("pin", "semantic_fingerprint", "executable_fingerprint"):
        assert len(candidate[field]) == 64, field


def test_the_candidate_names_the_lineage_the_request_named(candidate_run):
    candidate = candidate_run["document"]["candidate"]
    workspace = candidate_run["workspace"]
    assert candidate["semantic_fingerprint"] == workspace.expected_semantic_fingerprint
    assert candidate["executable_fingerprint"] == workspace.expected_executable_fingerprint


def test_the_pin_is_the_manifests_own_value_not_a_new_number(candidate_run):
    """The seam adds no identity scheme; it names the ones the producers already compute."""
    candidate = candidate_run["document"]["candidate"]
    manifest = json.loads((REPO_ROOT / candidate["manifest"]).read_text())
    assert candidate["pin"] == manifest["fingerprints"]["indicator_inputs"]["digest"]


def test_the_package_is_byte_identical_before_and_after(candidate_run):
    """The seam proves; it does not perform. A passing run moves nothing either."""
    workspace = candidate_run["workspace"]
    assert integrate.package_digests(workspace.package) == candidate_run["entry"]


def test_the_verification_summary_the_candidate_cites_reads_pass(candidate_run):
    summary = json.loads((candidate_run["out"] / "verification_summary.json").read_text())
    assert summary["outcome"] == "pass"
    assert summary["verdicts_rederived"] is True


def test_the_preflight_results_the_run_produced_read_six_of_six(candidate_run):
    results = json.loads((candidate_run["out"] / "preflight_results.json").read_text())
    assert results["outcome"] == "pass"
    assert len(results["gates"]) == 6


def test_the_toolchain_the_candidate_ran_under_is_recorded(candidate_run):
    toolchain = candidate_run["document"]["toolchain"]
    assert toolchain["sysml_codegen"] and toolchain["agentic_mbse"] and toolchain["costingfe"]
    assert len(toolchain["teax_revision"]) == 40
    assert toolchain["teax_module_path"]
