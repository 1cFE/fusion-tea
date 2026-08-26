"""Real refusals from real producers, each driven by a caller-supplied input.

No mocks anywhere in the gate path. A seam that only knows how to report simulated
failures has not been shown to fail closed, so every fixture here drives a producer the
seam actually invokes into a genuine negative verdict, and asserts the whole shape of the
blocker the caller reads: which producer, over what scope, refused or could not run, which
condition slug, and where its own evidence sits.
"""

from __future__ import annotations

import hashlib
import json
import os

import pytest

from scripts import integrate
from scripts.study import manifest as manifest_mod
from tests.study.conftest import run_seam, run_seam_raw

CONTRACT = "contracts/model_contract.json"


@pytest.fixture
def seam_environment() -> dict[str, str]:
    """The session's own environment, which a fixture doctors one variable of."""
    return dict(os.environ)


def test_wrong_expected_teax_revision_refuses_gate_1b(integration_workspace, tmp_path):
    out = tmp_path / "out"
    argv = integration_workspace.request_argv(out, **{"--expected-teax-revision": "0" * 40})
    document = run_seam(argv, out)

    blocker = document["blocker"]
    assert blocker["gate"] == "teax-revision"
    assert blocker["producer"] == "scripts/integrate.py"
    assert blocker["scope"] == "request"
    assert blocker["mode"] == "refused"
    assert blocker["condition"] == "toolchain-drift"
    assert blocker["expected"] == "0" * 40
    assert blocker["actual"] == integration_workspace.expected_teax_revision
    assert document["gates"][0]["status"] == "pass"
    assert [gate["status"] for gate in document["gates"][2:]] == ["not reached"] * 8
    assert document["candidate"] is None


def test_absent_expected_teax_revision_could_not_run_rather_than_pass(
    integration_workspace, tmp_path
):
    """The seam does not mint a pin of its own, so an unasked question is not a pass."""
    out = tmp_path / "out"
    argv = integration_workspace.request_argv(out, **{"--expected-teax-revision": None})
    blocker = run_seam(argv, out)["blocker"]
    assert blocker["gate"] == "teax-revision"
    assert blocker["mode"] == "could_not_run"
    assert blocker["condition"] == "input-missing"


def _wrong_bytes_wheel(tmp_path):
    """A file that is not the recorded wheel, so the hash assertion fails for real."""
    wheel = tmp_path / "not_the_recorded_wheel.whl"
    wheel.write_bytes(b"this is not the wheel the toolchain was pinned to")
    assert hashlib.sha256(wheel.read_bytes()).hexdigest() != (
        "cca661ce1ad5b7c7326cf48f8167e9358c22982343185bb82a8e059089cddbc5"
    )
    return wheel


def test_doctored_wheel_hash_refuses_gate_1a(
    integration_workspace, tmp_path, seam_environment
):
    """A genuine ``<failure>`` from a genuine producer, driven entirely by environment.

    This is also the only proof the junit-to-``refused`` mapping gets: gate 5 shares the
    mapping and its own refusal path cannot be driven without editing a tracked file or a
    frozen producer, which is the stated coverage boundary.
    """
    out = tmp_path / "out"
    env = dict(seam_environment)
    env["STOP_PARSER_CODEGEN_WHEEL"] = str(_wrong_bytes_wheel(tmp_path))

    document = run_seam(integration_workspace.request_argv(out), out, env)

    blocker = document["blocker"]
    assert blocker["gate"] == "pinned-packages"
    assert blocker["producer"] == "tests/test_dependency_provenance.py"
    assert blocker["scope"] == "repo"
    assert blocker["mode"] == "refused"
    assert blocker["condition"] == "toolchain-drift"
    junit = out / "junit" / "pinned-packages.xml"
    assert junit.is_file()
    assert blocker["evidence"] == [manifest_mod.repo_relative_posix(junit)]
    assert [gate["status"] for gate in document["gates"][1:]] == ["not reached"] * 9
    assert document["candidate"] is None


def test_a_refusing_run_exits_one_and_leaves_the_repo_clean(
    integration_workspace, tmp_path, seam_environment
):
    out = tmp_path / "out"
    env = dict(seam_environment)
    env["STOP_PARSER_CODEGEN_WHEEL"] = str(_wrong_bytes_wheel(tmp_path))
    done = run_seam_raw(integration_workspace.request_argv(out), env)
    assert done.returncode == 1
    assert integration_workspace.repo_clean_over_sources is True


# --------------------------------------------------- gates 2, 3 and 4: the mutating gates


def test_edited_package_byte_refuses_gate_2_and_the_tree_is_restored(
    integration_workspace, tmp_path
):
    """A package that regeneration rewrites was not the integrated form of its model."""
    out = tmp_path / "out"
    target = integrate.resolve_package(integration_workspace.package) / CONTRACT
    target.write_text(target.read_text().replace('"parameters"', '"parameters_edited"', 1))
    entry = integrate.package_digests(integration_workspace.package)

    document = run_seam(integration_workspace.request_argv(out), out)

    blocker = document["blocker"]
    assert blocker["gate"] == "regeneration"
    assert blocker["producer"] == "sysml-codegen generate"
    assert blocker["scope"] == "request"
    assert blocker["mode"] == "refused"
    assert blocker["condition"] == "package-not-integrated"
    assert blocker["evidence"] == [manifest_mod.repo_relative_posix(out / "moved_files.txt")]
    assert CONTRACT in (out / "moved_files.txt").read_text()
    assert integrate.package_digests(integration_workspace.package) == entry, (
        "a byte-movement refusal must leave the tree exactly as it found it"
    )
    assert [gate["status"] for gate in document["gates"][3:]] == ["not reached"] * 7


def test_doctored_census_refuses_gate_4(integration_workspace, tmp_path):
    out = tmp_path / "out"
    census = json.loads(integration_workspace.census.read_text())
    census["entry_points"] += 1
    integration_workspace.census.write_text(json.dumps(census, indent=2) + "\n")

    document = run_seam(integration_workspace.request_argv(out), out)

    blocker = document["blocker"]
    assert blocker["gate"] == "census-snapshot"
    assert blocker["producer"] == "tests/models/test_model_family_spines.py::_by_entry_type"
    assert blocker["scope"] == "request"
    assert blocker["mode"] == "refused"
    assert blocker["condition"] == "census-stale"
    assert "entry points" in blocker["detail"]
    assert [gate["status"] for gate in document["gates"][:4]] == ["pass"] * 4, (
        "gates 1a, 1b, 2 and 3 must pass before a census refusal means anything"
    )


def test_absent_census_file_could_not_run_rather_than_pass(integration_workspace, tmp_path):
    out = tmp_path / "out"
    argv = integration_workspace.request_argv(out, **{"--census-file": None})
    blocker = run_seam(argv, out)["blocker"]
    assert blocker["gate"] == "census-snapshot"
    assert blocker["mode"] == "could_not_run"
    assert blocker["condition"] == "input-missing"


def test_two_snapshots_beside_the_models_root_are_input_invalid(
    integration_workspace, tmp_path
):
    """The snapshot is found rather than named, so ambiguity refuses rather than guesses."""
    out = tmp_path / "out"
    (integration_workspace.models.parent / "a_second.snapshot.json").write_text("{}")

    blocker = run_seam(integration_workspace.request_argv(out), out)["blocker"]
    assert blocker["gate"] == "census-snapshot"
    assert blocker["mode"] == "could_not_run"
    assert blocker["condition"] == "input-invalid"
    assert "exactly one *.snapshot.json" in blocker["detail"]
