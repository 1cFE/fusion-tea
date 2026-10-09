"""The file audit and the Files rule (design D5, D6, Appendix G).

The server degrades to null when a file it reads is missing (findings.py:121,131-138,
server.py:825), so the contract alone can't see a file missing from the gate's trimmed
checkout or kept out of Railway's image by .dockerignore. The audit records every path
under the tree the server opens for reading, lists or stats; the Files rule fails on each
such path tracked at the reference commit that the tree lacks or .dockerignore excludes.
Files keys are never waived. Standard library only.
"""

from __future__ import annotations

import os
import posixpath
import re
import sys
from collections.abc import Callable, Collection, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pin_source import git_stdout

DOCKERIGNORE = ".dockerignore"  # at the build context root, which is the repo root

# ---------------------------------------------------------------------------
# Recording what the server touches
# ---------------------------------------------------------------------------

_recording: list[str] | None = None  # raw paths, while a touched_paths block runs
_hook_installed = False
_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT


@contextmanager
def touched_paths(tree: Path) -> Iterator[set[str]]:
    """Record the paths under `tree` this process reads, lists or stats inside the block.

    Yields a set that holds them, relative to `tree` with "/" separators, once the block
    ends. Reads are `open` without a write mode; listings are `os.listdir` and
    `os.scandir`, both seen through an audit hook; stats go through a wrapper on `os.stat`,
    which is how pathlib and os.path check that a file exists.
    """
    global _recording
    if _recording is not None:
        raise RuntimeError("touched_paths blocks don't nest")
    _install_hook()
    root, real_stat, touched = tree.resolve(), os.stat, set()

    def recording_stat(path: Any, *args: Any, **kwargs: Any) -> Any:
        if kwargs.get("dir_fd") is None:  # a path relative to a directory descriptor
            _record(path)
        return real_stat(path, *args, **kwargs)

    _recording, os.stat = [], recording_stat
    try:
        yield touched
    finally:
        raw, _recording, os.stat = _recording, None, real_stat
        touched |= _under(root, raw)


def _install_hook() -> None:
    """Add the audit hook once per process; an audit hook can't be removed (PEP 578)."""
    global _hook_installed
    if not _hook_installed:
        sys.addaudithook(_hook)
        _hook_installed = True


def _hook(event: str, args: tuple[Any, ...]) -> None:
    # Only appends: calling into os from a hook would raise more events.
    if _recording is None:
        return
    if event == "open":
        path, mode, flags = args
        writes = any(c in mode for c in "wax+") if isinstance(mode, str) else flags & _WRITE_FLAGS
        if not writes:
            _record(path)
    elif event in ("os.listdir", "os.scandir"):
        _record(args[0])


def _record(path: Any) -> None:
    """Keep a path given as text; file descriptors and bytes paths name nothing to audit."""
    recording = _recording  # the block may end on another thread
    if isinstance(path, os.PathLike):
        path = os.fspath(path)
    if isinstance(path, str) and recording is not None:
        recording.append(path)


def _under(root: Path, raw: Collection[str]) -> set[str]:
    """The paths in `raw` strictly inside `root`, relative to it, with "/" separators."""
    prefix = str(root) + os.sep
    absolute = {os.path.abspath(path) for path in raw}
    return {Path(path).relative_to(root).as_posix() for path in absolute if path.startswith(prefix)}


# ---------------------------------------------------------------------------
# Tracked paths
# ---------------------------------------------------------------------------


def tracked_paths(repo: Path, ref: str) -> frozenset[str]:
    """Every file tracked at `ref` in `repo`, and every directory holding one.

    `git ls-tree` reads trees only, so it works in a blobless clone; `git ls-files`
    would change under a sparse index.
    """
    files = git_stdout(repo, "ls-tree", "-r", "--name-only", "-z", ref).split("\0")[:-1]
    directories: set[str] = set()
    for path in files:
        parent = posixpath.dirname(path)
        while parent and parent not in directories:
            directories.add(parent)
            parent = posixpath.dirname(parent)
    return frozenset(files) | directories


# ---------------------------------------------------------------------------
# The .dockerignore matcher: Docker's rules, as BuildKit applies them when it sends
# the build context (moby/patternmatcher; tonistiigi/fsutil filter.go)
# ---------------------------------------------------------------------------


class UnsupportedPattern(ValueError):
    """A .dockerignore pattern uses syntax this matcher doesn't implement (m4)."""


@dataclass(frozen=True)
class _Pattern:
    reincludes: bool  # a "!" pattern
    matches: Callable[[str], bool]


class Matcher:
    """Decides, as Docker does, whether .dockerignore patterns leave a path out of the image."""

    def __init__(self, patterns: Sequence[str]) -> None:
        """Patterns as ignorefile.ReadAll returns them (`dockerignore_patterns`)."""
        self._patterns = [_pattern(text) for text in patterns if text.strip()]

    def excluded(self, path: str) -> bool:
        """Whether `path`, relative to the context root with "/" separators, stays out.

        BuildKit walks the context from the root and judges each path with its parent
        directory's per-pattern results (patternmatcher MatchesUsingParentResults). So a
        pattern matching a directory matches everything under it, and the last pattern
        that matches decides, with one subtlety kept here: a pattern skipped at a
        directory, because it couldn't change that directory's result, isn't inherited.
        """
        parts = path.split("/")
        inherited = [False] * len(self._patterns)
        excluded = False
        for depth in range(1, len(parts) + 1):
            excluded, inherited = self._judge("/".join(parts[:depth]), inherited)
        return excluded

    def _judge(self, path: str, inherited: Sequence[bool]) -> tuple[bool, list[bool]]:
        excluded, matched = False, []
        for pattern, parent_matched in zip(self._patterns, inherited):
            match = parent_matched or (pattern.reincludes == excluded and pattern.matches(path))
            matched.append(match)
            if match:
                excluded = not pattern.reincludes
        return excluded, matched


def dockerignore_patterns(text: str) -> list[str]:
    """The patterns in a .dockerignore file, read as Docker reads them (ignorefile.ReadAll).

    A leading byte-order mark goes; a line starting with "#" is a comment; each pattern
    is trimmed and cleaned, and loses a leading "/", keeping its "!".
    """
    patterns = []
    for line in text.removeprefix("\ufeff").split("\n"):
        line = line.removesuffix("\r")
        if line.startswith("#") or not line.strip():
            continue
        line = line.strip()
        reincludes = line.startswith("!")
        line = line.removeprefix("!").strip()
        if line:
            line = _clean(line)
            if len(line) > 1 and line.startswith("/"):
                line = line[1:]
        patterns.append("!" + line if reincludes else line)
    return patterns


def read_dockerignore(tree: Path) -> Matcher:
    """The matcher for `tree`'s .dockerignore; without one, Docker excludes nothing."""
    path = tree / DOCKERIGNORE
    if not path.exists():
        return Matcher([])
    return Matcher(dockerignore_patterns(path.read_text(encoding="utf-8")))


def _pattern(text: str) -> _Pattern:
    """One pattern, as patternmatcher.New and Pattern.compile prepare it."""
    text = _clean(text.strip())
    reincludes = text.startswith("!")
    if reincludes:
        text = text[1:]
        if not text:
            raise UnsupportedPattern('the pattern "!" excludes nothing; Docker rejects it')
    unsupported = sorted(set(text) & set("?[]\\"))
    if unsupported:
        raise UnsupportedPattern(
            f"{text!r} uses {' '.join(unsupported)}, which the gate's matcher doesn't implement"
        )
    return _Pattern(reincludes, _compile(text))


def _compile(text: str) -> Callable[[str], bool]:
    """How Docker matches a cleaned pattern against one path (Pattern.compile and match).

    A pattern without wildcards matches exactly; a trailing "**" makes a prefix match and
    a leading "**" a suffix match, unless another wildcard follows; anything else becomes
    a regular expression where "*" stays within one segment and "**" spans segments.
    """
    regex, kind, position = "", "exact", 0
    while position < len(text):
        start, char = position, text[position]
        position += 1
        if char == "*" and text[position : position + 1] == "*":
            position += 1
            if text[position : position + 1] == "/":
                position += 1
            if position == len(text) and kind == "exact":
                kind = "prefix"
            else:
                regex += ".*" if position == len(text) else "(.*/)?"
                kind = "regexp"
            if start == 0:
                kind = "suffix"
        elif char == "*":
            regex, kind = regex + "[^/]*", "regexp"
        elif char in ".+()|{}$":
            regex += "\\" + char
        else:
            regex += char
    if kind == "exact":
        return lambda path: path == text
    if kind == "prefix":
        return lambda path: path.startswith(text[:-2])
    if kind == "suffix":
        suffix = text[2:]
        return lambda path: path.endswith(suffix) or (suffix.startswith("/") and path == suffix[1:])
    compiled = re.compile(regex)
    return lambda path: compiled.fullmatch(path) is not None


def _clean(path: str) -> str:
    """Go's filepath.Clean on a "/"-separated path."""
    cleaned = posixpath.normpath(path)
    return cleaned[1:] if cleaned.startswith("//") else cleaned


# ---------------------------------------------------------------------------
# The Files rule (decision 10: only paths tracked at the reference commit count)
# ---------------------------------------------------------------------------


def missing_failures(tree: Path, paths: Collection[str]) -> set[str]:
    """`files missing <path>` for each of `paths` absent from `tree`."""
    return {f"files missing {path}" for path in paths if not (tree / path).exists()}


def excluded_failures(image: Matcher, paths: Collection[str]) -> set[str]:
    """`files dockerignore <path>` for each of `paths` the image's .dockerignore leaves out."""
    return {f"files dockerignore {path}" for path in paths if image.excluded(path)}
