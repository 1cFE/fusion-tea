"""The seam's own byte-movement detector, and the restore that undoes what moved.

Both exist because git cannot do either job where the gate tests run. The workspace is
gitignored, so ``git status --untracked-files=all`` reports nothing whatever the bytes do
and ``git checkout -- <ignored path>`` matches no pathspec. A detector that trusted git
would be silently vacuous in its own harness, and a restore that used git would be a
silent no-op exactly on the path that matters most and runs least.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from scripts import integrate

REPO_ROOT = Path(__file__).resolve().parents[2]

CONTRACT = "contracts/model_contract.json"


def test_the_package_root_resolves_through_its_symlink_before_digesting(
    integration_workspace,
):
    resolved = integrate.resolve_package(integration_workspace.package)
    assert resolved == integration_workspace.root / "generated"
    assert not resolved.is_symlink()
    assert integrate.package_digests(integration_workspace.package)[CONTRACT]


def test_digest_catches_movement_where_git_reports_clean(integration_workspace):
    package = integration_workspace.package
    before = integrate.package_digests(package)

    (integrate.resolve_package(package) / CONTRACT).write_text("{}")

    done = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--",
         str(integrate.resolve_package(package))],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert done.stdout.strip() == "", "git is blind inside the ignored workspace"
    assert integrate.moved_paths(before, integrate.package_digests(package)) == [CONTRACT]


def test_restore_covers_changed_added_and_removed(integration_workspace, tmp_path):
    package = integration_workspace.package
    resolved = integrate.resolve_package(package)
    before = integrate.package_digests(package)
    backup_dir = tmp_path / "_backup"
    integrate.backup(package, backup_dir)

    (resolved / CONTRACT).write_text("{}")
    (resolved / "inputs" / "a_file_the_run_added.json").write_text("{}")
    (resolved / "pipelines" / "pipeline.yaml").unlink()

    moved = integrate.restore(package, backup_dir, before)

    assert set(moved) == {
        CONTRACT, "inputs/a_file_the_run_added.json", "pipelines/pipeline.yaml",
    }
    assert integrate.package_digests(package) == before
    assert not (resolved / "inputs" / "a_file_the_run_added.json").exists()


def test_restore_touches_nothing_outside_what_moved(integration_workspace, tmp_path):
    """The before-digest *is* the restore set, so an untouched file is never rewritten."""
    package = integration_workspace.package
    resolved = integrate.resolve_package(package)
    before = integrate.package_digests(package)
    integrate.backup(package, tmp_path / "_backup")

    untouched = resolved / "contracts" / "package_contract.json"
    stat_before = untouched.stat().st_mtime_ns
    (resolved / CONTRACT).write_text("{}")

    assert integrate.restore(package, tmp_path / "_backup", before) == [CONTRACT]
    assert untouched.stat().st_mtime_ns == stat_before


def test_a_no_op_run_moves_nothing(integration_workspace):
    before = integrate.package_digests(integration_workspace.package)
    assert integrate.moved_paths(
        before, integrate.package_digests(integration_workspace.package)
    ) == []


def test_moved_paths_are_cited_repo_relative(integration_workspace):
    cited = integrate.cite_moved(integration_workspace.package, [CONTRACT])
    assert cited == [f".integration_workspace/generated/{CONTRACT}"]


def test_no_mtime_is_read_anywhere_in_the_seam():
    """95 of 153 files move mtime on a byte-identical regeneration; a detector built on
    that reports a false positive on every re-run."""
    source = (REPO_ROOT / "scripts" / "integrate.py").read_text()
    assert "st_mtime" not in source
    assert "getmtime" not in source
