"""Shared internals for the study gate tools (design D10).

Four jobs, and nothing above them:

1. The git-cleanliness gate over a package tree.
2. Atomic, deterministic document writing — a non-zero exit never leaves a torn file.
3. The per-tool source digest under ``tool-source-digest/v1``, over a *named* file list.
4. The exit and error convention both tools share: :class:`ToolError` for every
   mechanical failure, caught once at the CLI boundary and turned into exit 1.

One implementation of "clean" and one of "wrote it", so the two tools cannot
disagree about what those words mean.

`tool-source-digest/v1` names an algorithm — canonical text over a named file list —
not one particular list. Every emission carries its ``files`` list in the same
``{path, sha256}`` shape ``manifest.tool_source_digest()`` uses, so a record can tell
whose revision it is reading (design Risks, L5c).

Generic by construction: this module names no package, no key prefix, and no adapter
(Invariant 1). It imports no teax.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from scripts.study import manifest as manifest_mod

TOOL_SOURCE_RECIPE = manifest_mod.TOOL_SOURCE_RECIPE


class ToolError(Exception):
    """A mechanical failure. Every one exits non-zero; no interpretive fact raises."""


def tool_source_digest(files: tuple[str, ...]) -> dict:
    """``tool-source-digest/v1`` over a named list of repo-relative source files."""
    root = manifest_mod.repo_root()
    entries = []
    for rel in files:
        path = root / rel
        if not path.is_file():
            raise ToolError(f"tool source file missing: {rel}")
        entries.append((rel, manifest_mod.sha256_file(path)))
    # Item 3's canonical-text implementation, not a second copy of it. One recipe id
    # must mean one algorithm across all three tools, and two implementations of a
    # digest recipe disagree exactly once, silently, long after anyone is watching.
    return {
        "recipe": TOOL_SOURCE_RECIPE,
        "digest": manifest_mod._canonical_digest(TOOL_SOURCE_RECIPE, entries),
        "files": [{"path": rel, "sha256": digest} for rel, digest in entries],
    }


def git_status_porcelain(tree: Path | str) -> str:
    """``git status --porcelain`` over one tree, from the repository root."""
    root = manifest_mod.repo_root()
    done = subprocess.run(
        # --untracked-files=all: git collapses an untracked directory to one line, and a
        # gate that reports a directory cannot tell you which file a run left behind.
        ["git", "status", "--porcelain", "--untracked-files=all", "--", str(Path(tree).resolve())],
        cwd=str(root), capture_output=True, text=True,
    )
    if done.returncode != 0:
        raise ToolError(
            f"git status failed over {manifest_mod.repo_relative_posix(tree)}: "
            f"{done.stderr.strip()}"
        )
    return done.stdout.strip()


def assert_tree_clean(tree: Path | str) -> None:
    """The gate: a package tree must be byte-untouched. Names every offending file."""
    dirty = git_status_porcelain(tree)
    if dirty:
        raise ToolError(
            f"package tree is not git-clean: {manifest_mod.repo_relative_posix(tree)}\n{dirty}"
        )


def canonical_json(document: object) -> str:
    """The bytes a document is written and digested as: indent 2, key order preserved."""
    return json.dumps(document, indent=2) + "\n"


def digest_of_document(document: object) -> str:
    """sha256 over a document's canonical bytes, so two tools cite one value for it."""
    return hashlib.sha256(canonical_json(document).encode("utf-8")).hexdigest()


def write_document(document: object, path: Path | str) -> Path:
    """Write a document atomically: a full file appears, or nothing does.

    Rename within the destination directory, so the replace is atomic on POSIX and
    a crash mid-write cannot leave a half-parsed JSON file for the next reader.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as fh:
            fh.write(canonical_json(document))
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return path


def read_json(path: Path | str, what: str) -> object:
    """Read and parse a JSON document, naming the file and what it was wanted for."""
    path = Path(path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ToolError(
            f"cannot read {what} at {manifest_mod.repo_relative_posix(path)}: {exc}"
        ) from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ToolError(
            f"{what} at {manifest_mod.repo_relative_posix(path)} is not valid JSON: {exc}"
        ) from exc


def relative_deviation(got: float, expected: float) -> float:
    """Relative deviation, guarded so an expected zero does not divide by zero."""
    return abs(got - expected) / max(abs(expected), 1e-30)
