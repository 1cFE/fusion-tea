"""Waivers (D7, Appendix E): hand-written entries in waivers.toml, each clearing the
failure keys its `match` names. Standard library only."""

from __future__ import annotations

import datetime
import re
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from contract_rules import rule_of

# Rules whose keys are printed, never matched (M4), and how each failure clears instead.
UNWAIVABLE = {
    "cors": "put https://1cf.energy back in the CORS allowlist (_ExplorerApp in server.py)",
    "files": "fix runtime_paths.txt or .dockerignore",
}
_WAIVER_FIELDS = ("match", "reason", "evidence", "date")
# An unpopulated waiver must show the pinned JavaScript was read: a file.js:N cite of
# the JS that reads the path, or "unread:" and the search terms that found no reader
# (orchestrator, 2026-10-08, replacing N4's cite-only wording).
_JS_CITE = re.compile(r"\b[\w-]+\.js:\d+")
_UNREAD = re.compile(r"\bunread:\s*\S")
_MATCH_PARTS = re.compile(r"([ .])")  # a key's separators: tokens by spaces, paths by dots


class WaiverError(ValueError):
    """waivers.toml breaks the waiver grammar."""


@dataclass(frozen=True)
class Waiver:
    match: str
    reason: str
    evidence: str
    date: datetime.date


def load_waivers(path: Path) -> list[Waiver]:
    """Read waivers.toml, raising WaiverError on anything outside the grammar."""
    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise WaiverError(str(error)) from error
    entries = document.get("waiver", [])
    if set(document) - {"waiver"} or not isinstance(entries, list):
        raise WaiverError("write each waiver as a [[waiver]] table, and nothing else")
    return [_waiver(entry, f"waiver {number}") for number, entry in enumerate(entries, 1)]


def _waiver(entry: Mapping[str, Any], where: str) -> Waiver:
    if set(entry) != set(_WAIVER_FIELDS):
        raise WaiverError(
            f"{where}: needs exactly the fields {', '.join(_WAIVER_FIELDS)}, "
            f"has {', '.join(sorted(entry)) or 'none'}"
        )
    for field in ("match", "reason", "evidence"):
        if not isinstance(entry[field], str) or not entry[field].strip():
            raise WaiverError(f"{where}: {field} must be a non-empty string")
    if not isinstance(entry["date"], datetime.date):
        raise WaiverError(f"{where}: date must be a TOML date, like 2026-10-08")
    waiver = Waiver(**entry)
    _check_match(waiver.match, where)
    rule = rule_of(waiver.match)
    if rule in UNWAIVABLE:
        raise WaiverError(f"{where}: {rule} failures can't be waived; {UNWAIVABLE[rule]}")
    if waiver.match.startswith("unpopulated ") and not (
        _JS_CITE.search(waiver.evidence) or _UNREAD.search(waiver.evidence)
    ):
        raise WaiverError(
            f"{where}: an unpopulated waiver's evidence must cite the JavaScript that reads "
            "the path (file.js:N), or say 'unread:' and the search terms that found no reader"
        )
    return waiver


def _check_match(match: str, where: str) -> None:
    """A match is a failure key, with `*` standing for one whole token or path segment."""
    tokens = match.split(" ")
    if "" in tokens:
        raise WaiverError(f"{where}: match {match!r} must be tokens separated by single spaces")
    if "*" in tokens[0]:
        raise WaiverError(f"{where}: match {match!r} must name its rule; * can't stand for it")
    for part in _MATCH_PARTS.split(match):
        if "*" in part.replace("{*}", "") and part != "*":
            raise WaiverError(f"{where}: * must be a whole token or path segment, not {part!r}")


def waiver_matches(match: str, key: str) -> bool:
    """Whether a waiver's match names `key`: equal parts, each `*` standing for any one."""
    pattern = "".join(
        "[^ .]+" if part == "*" else re.escape(part) for part in _MATCH_PARTS.split(match)
    )
    return re.fullmatch(pattern, key) is not None


@dataclass(frozen=True)
class Verdict:
    failing: tuple[str, ...]  # failure keys no waiver clears
    waived: tuple[str, ...]  # failure keys a waiver clears
    stale: tuple[Waiver, ...]  # waivers that match no waivable failure


def apply_waivers(failures: Sequence[str], waivers: Sequence[Waiver]) -> Verdict:
    """Split failures into waived and failing; CORS and Files keys are never waived."""
    waivable = [key for key in failures if rule_of(key) not in UNWAIVABLE]
    waived = {key for key in waivable if any(waiver_matches(w.match, key) for w in waivers)}
    return Verdict(
        failing=tuple(key for key in failures if key not in waived),
        waived=tuple(key for key in failures if key in waived),
        stale=tuple(w for w in waivers if not any(waiver_matches(w.match, k) for k in waivable)),
    )
