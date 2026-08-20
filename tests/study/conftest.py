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


# --------------------------------------------------------------- Item 4: the era dependency
#
# The era teax worktree is a read-only external dependency: not in this repo, not
# installed by uv. A machine without it legitimately cannot run the era-dependent
# tests, so those tests skip with a reason that names the resolved path, the pinned
# commit, what was found, and the override. Silence is the real risk, so
# ``STUDY_REQUIRE_ERA=1`` turns every such skip into a hard failure — this item's
# own validation runs set it, and it is the flag CI would use.
#
# The committed proof-of-life stores under ``study/_work/`` are gitignored, so they
# are the same kind of dependency and follow the same rule.

ERA_PIN_COMMIT = "fa0e06a"
ERA_DEFAULT_WORKTREE = Path("/home/reid/1cfe/teax-v1-era")
ERA_SIMKIT_SUBPATH = "packages/teax-simkit"


def _require_era() -> bool:
    return os.environ.get("STUDY_REQUIRE_ERA") == "1"


def _unavailable(reason: str):
    """Skip on an absent external dependency, unless STUDY_REQUIRE_ERA=1 promotes it."""
    if _require_era():
        pytest.fail(reason)
    pytest.skip(reason)


def _era_worktree() -> Path:
    return Path(os.environ.get("TEAX_V1_ERA") or ERA_DEFAULT_WORKTREE)


@pytest.fixture
def era_simkit_path() -> Path:
    """The pinned era ``teax-simkit`` directory, put on ``sys.path``.

    Resolves ``$TEAX_V1_ERA`` if set, else the default worktree. Requires both the
    ``packages/teax-simkit`` directory and the pinned HEAD.
    """
    worktree = _era_worktree()
    simkit = worktree / ERA_SIMKIT_SUBPATH
    override = "set TEAX_V1_ERA to override the worktree location"
    if not simkit.is_dir():
        _unavailable(
            f"era teax worktree unavailable: expected {ERA_SIMKIT_SUBPATH} under "
            f"{worktree} at commit {ERA_PIN_COMMIT}, found no such directory ({override})"
        )
    head = subprocess.run(
        ["git", "-C", str(worktree), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True,
    )
    found = head.stdout.strip()
    if head.returncode != 0 or not found.startswith(ERA_PIN_COMMIT[:7]):
        _unavailable(
            f"era teax worktree is at the wrong commit: {worktree} expected "
            f"{ERA_PIN_COMMIT}, found {found or 'no git HEAD'} ({override})"
        )
    if str(simkit) not in sys.path:
        sys.path.insert(0, str(simkit))
    return simkit


COMMITTED_STUDY_DIR = REPO_ROOT / "exploration" / "stellarator_e2e" / "study"
COMMITTED_WORK_DIR = COMMITTED_STUDY_DIR / "_work"


@pytest.fixture
def committed_store_path():
    """Factory for a proof-of-life store path. Read-only — these stores are evidence."""

    def _store(name: str) -> Path:
        path = COMMITTED_WORK_DIR / name
        if not path.is_file():
            _unavailable(
                f"proof-of-life store unavailable: {path} (gitignored executed evidence; "
                f"re-produce it by running exploration/stellarator_e2e/study/run_design_search.py "
                f"under the era pin {ERA_PIN_COMMIT})"
            )
        return path

    return _store
