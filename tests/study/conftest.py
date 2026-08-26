"""Fixtures for the study indicator tool tests.

The committed package under ``exploration/stellarator_e2e/pkg/`` is read-only in
these tests. Anything that mutates a package goes through the ``package_copy``
factory (added in Phase 4), which copies into ``tmp_path``.
"""

import itertools
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_PACKAGE = REPO_ROOT / "exploration" / "stellarator_e2e" / "pkg" / "stellarator_tea"
REAL_MANIFEST = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies" / "manifest.json"
SCHEMA_DIR = REPO_ROOT / "scripts" / "study" / "schemas"
DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def real_package_path() -> Path:
    """The committed stellarator package. Read-only — never mutate in place."""
    assert REAL_PACKAGE.is_dir(), f"missing committed package at {REAL_PACKAGE}"
    return REAL_PACKAGE


@pytest.fixture
def real_manifest_path() -> Path:
    assert REAL_MANIFEST.is_file(), f"missing committed manifest at {REAL_MANIFEST}"
    return REAL_MANIFEST


@pytest.fixture
def load_schema():
    """Load one of the committed JSON Schema files by stem."""

    def _load(stem: str) -> dict:
        path = SCHEMA_DIR / f"{stem}.schema.json"
        assert path.is_file(), f"missing schema {path}"
        return json.loads(path.read_text())

    return _load


@pytest.fixture
def minimal_manifest_dict() -> dict:
    """The smallest manifest that validates — the shape, with placeholder facts."""
    return {
        "schema_version": "study-package-manifest/v1",
        "package": {"name": "some_pkg", "path": "some/where/some_pkg"},
        "fingerprints": {
            "indicator_inputs": {
                "recipe": "indicator-input-fingerprint/v1",
                "digest": "0" * 64,
                "files": ["contracts/model_contract.json", "inputs/a.json", "pipelines/p.yaml"],
            },
            "recorded_provenance": {
                "executable_fingerprint": "1" * 64,
                "semantic_fingerprint": "2" * 64,
            },
        },
        "objective_catalog": [{"name": "cost", "channel": "some_pkg__cost_calc__cost"}],
        "ties": [{"key": "some_pkg__b__x0", "rides_with": ["some_pkg__a__x"]}],
        "baseline": {
            "point": {"some_pkg__a__x": 1.0},
            "headline": {"channel": "some_pkg__cost_calc__cost", "value": 2.0},
            "verdicts": [{"source_local_identity": "ok", "expected": "satisfied"}],
        },
        "oracle": {
            "kind": "python_callable",
            "module": "some_oracle",
            "callable": "compute",
            "sys_path": "some/where",
        },
    }


KNOWN_ANSWER_DECLARATION = DATA_DIR / "axes.known_answers.json"
INDICATORS_CLI = REPO_ROOT / "scripts" / "study" / "indicators.py"


def run_tool_raw(package, manifest_path, groups, *, out=None, group=(), cwd=None):
    """Invoke the CLI as a subprocess. Returns (returncode, stdout, stderr).

    A subprocess is the honest check for Invariant 1: a partial report would show up
    as bytes on stdout or a file on disk, and neither survives an in-process call.
    """
    argv = [
        sys.executable,
        str(INDICATORS_CLI),
        "--package", str(package),
        "--manifest", str(manifest_path),
        "--groups", str(groups),
    ]
    for name in group:
        argv += ["--group", name]
    if out is not None:
        argv += ["--out", str(out)]
    done = subprocess.run(
        argv, capture_output=True, text=True, cwd=str(cwd) if cwd else str(REPO_ROOT)
    )
    return done.returncode, done.stdout, done.stderr


def run_tool(package, manifest_path, groups, *, group=(), cwd=None):
    """Invoke the CLI and return the parsed report. Raises if the run failed."""
    rc, out, err = run_tool_raw(package, manifest_path, groups, group=group, cwd=cwd)
    assert rc == 0, f"tool exited {rc}\n{err}"
    return json.loads(out)


@pytest.fixture
def known_answer_declaration() -> Path:
    return KNOWN_ANSWER_DECLARATION


SYNTHETIC_DIR = DATA_DIR / "synthetic_pkg"


@dataclass
class PackageCopy:
    """A writable copy of a package plus its manifest and axis declaration.

    Two rules make the negative tests trustworthy:

    * **Assert before mutating.** ``edit`` asserts its target substring exists in the
      copy before replacing. Item 1's probe 4 passed against an uncorrupted file
      because the target string was wrong — a negative test that corrupts nothing
      looks exactly like a passing one.
    * **Re-pin unless the test is about the pin.** The fingerprint gate runs before
      the parse, so a mutation test must rewrite the copy's pinned digest to reach
      the failure it means to test. ``run`` re-pins by default; ``run(repin=False)``
      is the fingerprint-mismatch test.
    """

    path: Path
    manifest: Path
    axes: Path

    def edit(self, relative: str, old: str, new: str) -> None:
        """Replace a substring inside one file of the copy, asserting the target first."""
        target = self.path / relative
        text = target.read_text()
        assert old in text, f"mutation target not found in {relative}: {old!r}"
        target.write_text(text.replace(old, new, 1))

    def edit_manifest(self, mutate) -> None:
        data = json.loads(self.manifest.read_text())
        mutate(data)
        self.manifest.write_text(json.dumps(data, indent=2) + "\n")

    def edit_axes(self, mutate) -> None:
        data = json.loads(self.axes.read_text())
        mutate(data)
        self.axes.write_text(json.dumps(data, indent=2) + "\n")

    def write(self, relative: str, text: str) -> None:
        """Add a new file to the copy. Only for tests about files that should not exist."""
        target = self.path / relative
        assert not target.exists(), f"{relative} already exists in the copy"
        target.write_text(text)

    def repin(self) -> None:
        from scripts.study import manifest as manifest_mod

        computed = manifest_mod.indicator_input_fingerprint(self.path)
        self.edit_manifest(
            lambda data: data["fingerprints"]["indicator_inputs"].update(
                digest=computed["digest"], files=[f["path"] for f in computed["files"]]
            )
        )

    def run(self, *, repin=True, out=None, group=()):
        if repin:
            self.repin()
        return run_tool_raw(self.path, self.manifest, self.axes, out=out, group=group)


@pytest.fixture
def package_copy(tmp_path):
    """Factory: copy a package tree plus its manifest and axes into tmp_path."""

    counter = itertools.count()

    def _copy(package: Path, manifest_path: Path, axes_path: Path) -> PackageCopy:
        root = tmp_path / f"copy{next(counter)}"
        root.mkdir()
        package_dest = root / "pkg"
        shutil.copytree(package, package_dest)
        manifest_dest = root / "manifest.json"
        manifest_dest.write_bytes(manifest_path.read_bytes())
        axes_dest = root / "axes.json"
        axes_dest.write_bytes(axes_path.read_bytes())
        copy = PackageCopy(path=package_dest, manifest=manifest_dest, axes=axes_dest)
        # package.path is repo-relative by schema; the copy lives outside the repo.
        copy.edit_manifest(
            lambda data: data["package"].update(path=os.path.relpath(package_dest, REPO_ROOT))
        )
        return copy

    return _copy


@pytest.fixture
def synthetic_copy(package_copy):
    return package_copy(
        SYNTHETIC_DIR / "pkg", SYNTHETIC_DIR / "manifest.json", SYNTHETIC_DIR / "axes.json"
    )


@pytest.fixture
def real_copy(package_copy):
    return package_copy(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWER_DECLARATION)


# ------------------------------------------------ stellarator-model-migration: the stock route
#
# The regenerated package runs on stock teax, reached through the sealed-runner contract's
# ``STOP_PARSER_TEAX_ROOT`` (design D4): the root of a teax checkout whose
# ``packages/teax-simkit`` goes on ``sys.path``. It is an
# external dependency that uv does not install, so its absence skips with the resolved path
# in the reason; ``STUDY_REQUIRE_TEAX=1`` turns that skip into a failure.

TEAX_ROOT_ENV = "STOP_PARSER_TEAX_ROOT"
TEAX_SIMKIT_SUBPATH = "packages/teax-simkit"


def _unavailable_teax(reason: str):
    if os.environ.get("STUDY_REQUIRE_TEAX") == "1":
        pytest.fail(reason)
    pytest.skip(reason)


def _stock_simkit_path() -> Path:
    root = os.environ.get(TEAX_ROOT_ENV)
    if not root:
        _unavailable_teax(f"{TEAX_ROOT_ENV} is not set; point it at a teax checkout")
    simkit_dir = Path(root) / TEAX_SIMKIT_SUBPATH
    if not simkit_dir.is_dir():
        _unavailable_teax(f"{TEAX_ROOT_ENV}={root} has no {TEAX_SIMKIT_SUBPATH}")
    if str(simkit_dir) not in sys.path:
        sys.path.insert(0, str(simkit_dir))
    import simkit

    assert Path(simkit.__file__).resolve().is_relative_to(simkit_dir.resolve()), simkit.__file__
    return simkit_dir


@pytest.fixture
def stock_simkit_path() -> Path:
    """Stock teax's ``teax-simkit`` directory from ``STOP_PARSER_TEAX_ROOT``, on ``sys.path``,
    with the imported ``simkit`` asserted to come from under that root."""
    return _stock_simkit_path()


@pytest.fixture(scope="session")
def stock_simkit_session_path() -> Path:
    """The same, for the session-scoped route fixtures (one baseline execution per session)."""
    return _stock_simkit_path()


@pytest.fixture(scope="session")
def stock_route_run(tmp_path_factory, stock_simkit_session_path):
    """One stock-route execution per session: the availability sweep's store plus the
    sealed identity document and baseline result the route deposits."""
    studies = str(REPO_ROOT / "exploration" / "stellarator_e2e" / "studies")
    if studies not in sys.path:
        sys.path.insert(0, studies)
    import study_route

    out = tmp_path_factory.mktemp("stock_route_run")
    study_route.run_availability_sweep(out)
    study_route.execute_baseline(out)
    return {
        "dir": out,
        "identity": out / "package_identity.json",
        "baseline_result": out / "baseline_result.json",
        "store": out / "_work" / "stellarator-availability-sweep-v1.db",
        "simkit": stock_simkit_session_path,
    }


# --------------------------------------------- the integration seam's hermetic workspace
#
# The seam's gates run producers that regenerate a package in place and read
# ``repo_root()``-relative paths, so a gate test needs a package tree *inside* the worktree
# (``tmp_path`` is outside it, and git errors rather than judging there) that no test may
# write into if it were tracked. The answer is a gitignored directory at the repo root,
# materialized from the committed state and removed in a ``finally``.
#
# The equality assertion is the point, not a formality. Two of the seam's ten gates judge
# the **repository** — the toolchain pin and the model-family spine suite, whose producers
# accept no package argument. Those gates only mean something while the workspace really is
# the committed state, so that is checked before the seam ever sees it rather than hoped.

WORKSPACE_ROOT = REPO_ROOT / ".integration_workspace"
E2E = REPO_ROOT / "exploration" / "stellarator_e2e"
REAL_MODELS = E2E / "models"
REAL_SNAPSHOT = E2E / "stellarator.snapshot.json"
REAL_ROUTE_DIR = E2E / "studies"
REAL_CENSUS = REPO_ROOT / "tests" / "models" / "data" / "mfe_census.json"


@dataclass
class IntegrationWorkspace:
    """A committed-state copy of everything one integration request names.

    ``source_digests`` maps each workspace-relative path to the sha256 of the **tracked**
    file it came from, so a test can prove materialization moved no byte.
    ``entry_digests`` is what the workspace actually holds once it is ready — the same
    values, except for the one file the manifest schema forces the fixture to rewrite,
    ``package.path``. A restore is proven against ``entry_digests``.
    """

    root: Path
    package: Path
    models: Path
    manifest: Path
    axes: Path
    census: Path
    snapshot: Path
    route_sys_path: Path
    source_digests: dict[str, str]
    entry_digests: dict[str, str]
    repo_clean_over_sources: bool


def _copy_tree_digests(source: Path, destination: Path, root: Path) -> dict[str, str]:
    """Copy a tree and return the *source* digest of every file, keyed workspace-relative."""
    from scripts.study import manifest as manifest_mod

    shutil.copytree(source, destination, symlinks=True)
    digests = {}
    for path in sorted(p for p in source.rglob("*") if p.is_file() and not p.is_symlink()):
        relative = destination / path.relative_to(source)
        digests[str(relative.relative_to(root))] = manifest_mod.sha256_file(path)
    return digests


def _copy_file_digest(source: Path, destination: Path, root: Path) -> dict[str, str]:
    from scripts.study import manifest as manifest_mod

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())
    return {str(destination.relative_to(root)): manifest_mod.sha256_file(source)}


def _repo_clean_over(paths) -> bool:
    done = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", *(str(p) for p in paths)],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert done.returncode == 0, done.stderr
    return not done.stdout.strip()


@pytest.fixture
def integration_workspace(stock_simkit_path):
    """The committed stellarator package and its inputs, materialized inside the worktree.

    Function-scoped: the refusal fixtures doctor different files, and a shared workspace
    would couple their assertions to each other's mutations.
    """
    from scripts.study import manifest as manifest_mod

    assert not WORKSPACE_ROOT.exists(), f"a previous run left {WORKSPACE_ROOT} behind"
    root = WORKSPACE_ROOT
    root.mkdir()
    try:
        digests: dict[str, str] = {}
        # The package root is a tracked symlink to ``../generated``; the layout is mirrored
        # so the seam's resolve-before-digesting is exercised the way production hits it.
        digests |= _copy_tree_digests(REAL_PACKAGE.resolve(), root / "generated", root)
        (root / "pkg").mkdir()
        (root / "pkg" / REAL_PACKAGE.name).symlink_to(Path("..") / "generated")
        digests |= _copy_tree_digests(REAL_MODELS, root / "models", root)
        digests |= _copy_file_digest(REAL_SNAPSHOT, root / REAL_SNAPSHOT.name, root)
        digests |= _copy_file_digest(REAL_MANIFEST, root / "studies" / "manifest.json", root)
        digests |= _copy_file_digest(KNOWN_ANSWER_DECLARATION, root / "studies" / "axes.json", root)
        digests |= _copy_file_digest(REAL_CENSUS, root / "mfe_census.json", root)

        for relative, digest in digests.items():
            assert manifest_mod.sha256_file(root / relative) == digest, relative

        package = root / "pkg" / REAL_PACKAGE.name
        manifest_path = root / "studies" / "manifest.json"
        # package.path is repo-relative by schema, and the workspace is a different root.
        data = json.loads(manifest_path.read_text())
        data["package"]["path"] = os.path.relpath(package.resolve(), REPO_ROOT)
        manifest_path.write_text(json.dumps(data, indent=2) + "\n")
        entry_digests = dict(digests)
        entry_digests[str(manifest_path.relative_to(root))] = manifest_mod.sha256_file(
            manifest_path
        )

        yield IntegrationWorkspace(
            root=root,
            package=package,
            models=root / "models",
            manifest=manifest_path,
            axes=root / "studies" / "axes.json",
            census=root / "mfe_census.json",
            snapshot=root / REAL_SNAPSHOT.name,
            route_sys_path=REAL_ROUTE_DIR,
            source_digests=digests,
            entry_digests=entry_digests,
            repo_clean_over_sources=_repo_clean_over(
                [REAL_PACKAGE.resolve(), REAL_MODELS, REAL_SNAPSHOT, REAL_MANIFEST, REAL_CENSUS]
            ),
        )
    finally:
        shutil.rmtree(root, ignore_errors=True)
