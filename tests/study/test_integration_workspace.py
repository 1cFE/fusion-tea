"""The workspace the seam's gate tests run in is the committed state, checked not assumed.

Two of the seam's ten gates judge the repository rather than the request. They mean
something in a test only while the workspace really is what is committed, so that is an
asserted precondition here rather than a property the gate tests quietly depend on.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts.study import manifest as manifest_mod

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_every_materialized_file_matches_the_tracked_digest(integration_workspace):
    """What the workspace holds is what is committed, one rewritten path aside."""
    for relative, digest in integration_workspace.entry_digests.items():
        assert manifest_mod.sha256_file(integration_workspace.root / relative) == digest, relative


def test_only_the_manifests_own_package_path_differs_from_the_tracked_bytes(
    integration_workspace,
):
    """The schema forces one rewrite; every other byte is the committed byte."""
    rewritten = [
        relative
        for relative, digest in integration_workspace.source_digests.items()
        if integration_workspace.entry_digests[relative] != digest
    ]
    assert rewritten == [str(integration_workspace.manifest.relative_to(
        integration_workspace.root
    ))]


def test_the_workspace_holds_every_input_one_request_names(integration_workspace):
    for path in (
        integration_workspace.package,
        integration_workspace.models,
        integration_workspace.manifest,
        integration_workspace.axes,
        integration_workspace.census,
        integration_workspace.snapshot,
    ):
        assert path.exists(), path


def test_repo_is_clean_over_the_source_paths(integration_workspace):
    assert integration_workspace.repo_clean_over_sources is True


def test_the_package_root_is_a_symlink_as_it_is_in_the_tracked_tree(integration_workspace):
    assert integration_workspace.package.is_symlink()
    assert integration_workspace.package.resolve() == integration_workspace.root / "generated"


def test_manifest_package_path_is_repo_relative_and_points_at_the_workspace(
    integration_workspace,
):
    data = json.loads(integration_workspace.manifest.read_text())
    declared = data["package"]["path"]
    assert not Path(declared).is_absolute()
    assert (REPO_ROOT / declared).resolve() == integration_workspace.package.resolve()


def test_the_snapshot_sits_beside_the_models_root_as_it_does_in_the_tracked_tree(
    integration_workspace,
):
    """Gate 4 finds the tracked snapshot rather than being told it, so the layout matters."""
    siblings = sorted(integration_workspace.models.parent.glob("*.snapshot.json"))
    assert siblings == [integration_workspace.snapshot]


def test_workspace_is_gitignored(integration_workspace):
    done = subprocess.run(
        ["git", "check-ignore", str(integration_workspace.root)],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert done.returncode == 0, "the workspace is not ignored; a gate test would dirty the repo"


def test_the_repo_stays_clean_while_a_workspace_exists(integration_workspace):
    done = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert ".integration_workspace" not in done.stdout


def test_the_workspace_is_removed_after_the_fixture(request):
    """The ``finally`` is what keeps a failed gate test from leaving a tree behind."""
    from tests.study.conftest import WORKSPACE_ROOT

    assert not WORKSPACE_ROOT.exists()
