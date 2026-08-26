"""Gate 0: the seam decides every precondition before it invokes any producer.

These tests read the committed package and never write to it — gate 0 runs no producer,
so a real request against the tracked tree is safe here and is the honest input. Every
artifact the seam writes lands under ``tmp_path``.

The one that matters most is the six-variable sweep. The wheel variables are read inside
``tests/test_dependency_provenance.py``'s *test body*, so an absence lands as a junit
``<failure>`` and would be reported as a toolchain refusal by any seam that let gate 1a
run first. That misreport is the failure these tests exist to make impossible.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import integrate

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_PACKAGE = REPO_ROOT / "exploration" / "stellarator_e2e" / "pkg" / "stellarator_tea"
REAL_MANIFEST = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies" / "manifest.json"
REAL_MODELS = REPO_ROOT / "exploration" / "stellarator_e2e" / "models"
ROUTE_SYS_PATH = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies"
AXES = Path(__file__).parent / "data" / "axes.known_answers.json"
SEAM = REPO_ROOT / "scripts" / "integrate.py"


def request_argv(out_dir: Path) -> list[str]:
    """A complete, resolvable request. Gate 0 accepts it; no producer runs past it."""
    return [
        "--audited-work", "exploration/stellarator_e2e/generated@HEAD",
        "--models-root", str(REAL_MODELS),
        "--package", str(REAL_PACKAGE),
        "--manifest", str(REAL_MANIFEST),
        "--groups", str(AXES),
        "--route-sys-path", str(ROUTE_SYS_PATH),
        "--route-module", "study_route",
        "--route-callable", "execute_baseline",
        "--out-dir", str(out_dir),
    ]


def drop_flag(argv: list[str], flag: str) -> list[str]:
    index = argv.index(flag)
    return argv[:index] + argv[index + 2:]


def run_seam_raw(argv: list[str], env: dict[str, str] | None = None):
    """Invoke the seam as a caller does: a subprocess, read back by exit code and JSON."""
    done = subprocess.run(
        [sys.executable, str(SEAM), *argv],
        capture_output=True, text=True, cwd=str(REPO_ROOT), env=env,
    )
    return done


def read_return(done, out_dir: Path) -> dict:
    """The return document, from ``--out-dir`` when gate 0 accepted the request else stdout."""
    written = out_dir / "integration_return.json"
    if written.is_file():
        return json.loads(written.read_text())
    return json.loads(done.stdout)


def run_seam(argv: list[str], out_dir: Path, env: dict[str, str] | None = None) -> dict:
    return read_return(run_seam_raw(argv, env), out_dir)


@pytest.fixture
def full_env() -> dict[str, str]:
    """A copy of this session's environment, so a test can remove one variable from it."""
    import os

    return dict(os.environ)


@pytest.mark.parametrize("missing", integrate.REQUIRED_ENV)
def test_each_env_var_unset_refuses_at_gate_zero(tmp_path, full_env, missing):
    env = {name: value for name, value in full_env.items() if name != missing}
    done = run_seam_raw(request_argv(tmp_path / "out"), env)
    assert done.returncode == 1
    document = read_return(done, tmp_path / "out")
    assert document["class"] == "BLOCKER"
    blocker = document["blocker"]
    assert blocker["gate"] == "preconditions"
    assert blocker["mode"] == "could_not_run"
    assert blocker["condition"] == "env-missing"
    assert missing in blocker["detail"]
    assert [gate["status"] for gate in document["gates"]] == ["not reached"] * 10


def test_missing_required_input_is_a_blocker_not_a_usage_error(tmp_path):
    argv = drop_flag(request_argv(tmp_path / "out"), "--manifest")
    done = run_seam_raw(argv)
    assert done.returncode == 1, "a missing input must never be argparse's exit 2"
    document = read_return(done, tmp_path / "out")
    assert document["blocker"]["condition"] == "input-missing"
    assert "--manifest" in document["blocker"]["detail"]


def test_out_dir_inside_package_root_is_input_invalid(tmp_path):
    out_dir = REAL_PACKAGE / "out"
    argv = request_argv(out_dir)
    done = run_seam_raw(argv)
    assert done.returncode == 1
    document = json.loads(done.stdout)
    assert document["blocker"]["condition"] == "input-invalid"
    assert not out_dir.exists(), "the seam wrote into the package it was refusing to touch"


def test_two_packages_are_ambiguous_lineage_not_a_last_one_wins(tmp_path):
    argv = [*request_argv(tmp_path / "out"), "--package", str(REPO_ROOT / "models")]
    document = run_seam(argv, tmp_path / "out")
    assert document["blocker"]["condition"] == "input-invalid"
    assert "exactly one package" in document["blocker"]["detail"]


def test_audited_work_must_carry_its_commit(tmp_path):
    argv = drop_flag(request_argv(tmp_path / "out"), "--audited-work")
    argv += ["--audited-work", "exploration/stellarator_e2e/generated"]
    document = run_seam(argv, tmp_path / "out")
    assert document["blocker"]["condition"] == "input-invalid"
    assert "PATH@COMMIT" in document["blocker"]["detail"]


def test_the_return_document_is_complete_on_every_exit_path(tmp_path):
    document = run_seam(drop_flag(request_argv(tmp_path / "out"), "--groups"), tmp_path / "out")
    assert document["schema_version"] == "integration-seam-return/v1"
    assert document["tool"]["path"] == "scripts/integrate.py"
    assert document["tool"]["source_digest"]["recipe"] == "tool-source-digest/v1"
    assert document["command"][0] == "scripts/integrate.py"
    assert document["candidate"] is None
    assert document["exit_code"] == 1
    assert set(document["toolchain"]) == {
        "agentic_mbse", "sysml_codegen", "costingfe", "teax_revision", "teax_module_path",
    }
    assert [gate["gate"] for gate in document["gates"]] == [g.name for g in integrate.GATES]
    assert all(gate["scope"] in ("repo", "request") for gate in document["gates"])


def test_the_condition_slug_set_is_closed():
    """A slug the guide does not enumerate cannot reach a caller: the constructor refuses."""
    with pytest.raises(ValueError, match="closed set"):
        integrate.SeamBlocker(
            gate="preconditions", producer="scripts/integrate.py", scope="request",
            mode="could_not_run", condition="not-a-real-slug", detail="",
        )


# ------------------------------------------------- the de-risk (design.md, Next-Stage)


def independently_can_import_simkit(env: dict[str, str]) -> bool:
    """What a ``verify.py`` subprocess under ``env`` actually does, built without the seam.

    ``verify.build_summary`` opens with a bare ``import simkit``; this is that import, in
    a fresh interpreter, reached the same way the producer reaches it.
    """
    done = subprocess.run(
        [sys.executable, "-c", "import simkit"],
        capture_output=True, text=True, cwd=str(REPO_ROOT), env=env,
    )
    return done.returncode == 0


def test_simkit_probe_agrees_with_the_verify_subprocess(full_env):
    """Gate 8's residual is only narrow while this holds (design D15)."""
    env = integrate.seam_env()
    assert (integrate.simkit_module_path(env) is not None) is (
        independently_can_import_simkit(env)
    )


def test_simkit_probe_refuses_without_the_teax_root(full_env, monkeypatch):
    monkeypatch.delenv("STOP_PARSER_TEAX_ROOT", raising=False)
    env = integrate.seam_env()
    assert integrate.simkit_module_path(env) is None
    assert independently_can_import_simkit(env) is False
