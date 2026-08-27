#!/usr/bin/env python3
"""The barred set for the ARIES-CS hold-out, derived from the protocol itself.

`knowledge/holdout/aries-cs/PROTOCOL.md` is the single rule home. This module
parses its §3 path lists rather than keeping a copy, and refuses to answer at all
if that parse does not produce the shape it expects — a shortened list would fail
open, which is the one failure direction that matters here.

There is no waiver. A match is reported; adjudicating it is the owner's job,
through the protocol's own §6 exception log, outside this seam.
"""

import re
import unicodedata
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

PROTOCOL_PATH = Path("knowledge/holdout/aries-cs/PROTOCOL.md")

BARRED_SECTION_HEADINGS = (
    "### Barred (do not read in demo sessions)",
    "### Barred by default, documented-exception path",
)

# Terms that mark ARIES-CS material. The four stems are the sealed papers
# (PROTOCOL §7); the host is the canonical program mirror.
BARRED_TERMS = (
    "aries-cs",
    "aries.ucsd.edu",
    "08-fst-ku",
    "08-fst-lyon",
    "08-fst-najmabadi",
    "08-fst-raffray",
)

_HYPHENS = "-‐‑‒–—­"


class ProtocolParseError(RuntimeError):
    """PROTOCOL.md did not parse into the expected §3 shape. Fail closed."""


@dataclass(frozen=True)
class Match:
    """One barred rule that fired, with where in the original text it fired."""

    rule_id: str
    count: int
    offsets: tuple[int, ...]


def barred_paths(protocol: Path = PROTOCOL_PATH) -> frozenset[str]:
    """The union of both §3 path lists, as glob patterns.

    Raises ProtocolParseError if either heading is missing or a list yields no
    backticked path.
    """
    text = protocol.read_text()
    patterns: set[str] = set()
    for heading in BARRED_SECTION_HEADINGS:
        section = _section_after(text, heading, protocol)
        found = _backticked_paths(section)
        if not found:
            raise ProtocolParseError(
                f"{protocol}: section '{heading}' yielded no backticked path bullets"
            )
        patterns |= found
    return frozenset(patterns)


def check_input_path(path: Path, protocol: Path = PROTOCOL_PATH) -> Match | None:
    """Return the rule barring this input path, or None.

    Applies to the *input identity* of a registration — a local PDF handed in, or
    a URL naming a repo path. A destination slug is newly minted and can never match.
    """
    candidate = _repo_relative(path)
    for pattern in sorted(barred_paths(protocol)):
        if _path_matches(candidate, pattern):
            return Match(rule_id=f"path:{pattern}", count=1, offsets=(0,))
    return None


def scan_terms(text: str) -> list[Match]:
    """Every barred term appearing in `text`, with offsets into `text` itself.

    Matching is done on a normalized copy — casefolded, dehyphenated, whitespace
    collapsed — so that "ARIES-CS", "ARIES-\\nCS" and "ARIES CS" all hit the same
    rule. Offsets are mapped back to the original string.
    """
    normalized, origin = _normalize_with_offsets(text)
    matches = []
    for term in BARRED_TERMS:
        offsets = []
        for variant in _term_variants(term):
            start = normalized.find(variant)
            while start != -1:
                offsets.append(origin[start])
                start = normalized.find(variant, start + 1)
        if offsets:
            unique = tuple(sorted(set(offsets)))
            matches.append(Match(rule_id=f"term:{term}", count=len(unique), offsets=unique))
    return matches


def scan_file(path: Path) -> list[Match]:
    """Scan a file's text. Bytes that are not valid UTF-8 are replaced, not skipped."""
    return scan_terms(path.read_text(encoding="utf-8", errors="replace"))


def _section_after(text: str, heading: str, protocol: Path) -> str:
    if heading not in text:
        raise ProtocolParseError(f"{protocol}: expected §3 heading not found: '{heading}'")
    rest = text.split(heading, 1)[1]
    return rest.split("\n### ", 1)[0]


def _backticked_paths(section: str) -> set[str]:
    found = set()
    for line in section.splitlines():
        if not line.startswith("- "):
            continue
        quoted = re.findall(r"`([^`]+)`", line)
        if quoted:
            found.add(quoted[0])
    return found


def repo_root() -> Path:
    """This checkout's root, derived from where this module actually sits.

    `scripts/holdout_guard.py` is one directory below the root, and that holds in
    any clone or worktree whatever the directory is called. The previous version
    looked for the literal string "fusion-tea" in the path, so a checkout under
    any other name left the path absolute, matched no glob, and silently let the
    path bar through — failing open, in the one module where that is the wrong
    direction (audit F6).
    """
    return Path(__file__).resolve().parent.parent


def _repo_relative(path: Path) -> str:
    """The path as the protocol's globs spell it: relative to this checkout's root."""
    if path.is_absolute():
        try:
            return path.resolve().relative_to(repo_root()).as_posix()
        except ValueError:
            # Outside this checkout. Nothing under a barred repo path can be, so
            # the absolute form is returned and simply matches no glob.
            return path.as_posix()
    return path.as_posix().lstrip("./")


def _path_matches(candidate: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[: -len("/**")]
        return candidate == prefix or candidate.startswith(prefix + "/")
    return fnmatch(candidate, pattern)


def _term_variants(term: str) -> tuple[str, ...]:
    """A term as it reads dehyphenated, and as it reads with the hyphen broken to a space."""
    joined = _strip_hyphens(term)
    spaced = re.sub(f"[{re.escape(_HYPHENS)}]", " ", term)
    return (joined,) if spaced == term else (joined, spaced)


def _strip_hyphens(text: str) -> str:
    return re.sub(f"[{re.escape(_HYPHENS)}]", "", text)


def _normalize_with_offsets(text: str) -> tuple[str, list[int]]:
    """Casefold, dehyphenate, collapse whitespace — keeping an index back to `text`.

    A hyphen followed by whitespace is dropped together with that whitespace, which
    is what rejoins a word broken across a line in a PDF extraction.
    """
    folded = unicodedata.normalize("NFKC", text).casefold()
    out: list[str] = []
    origin: list[int] = []
    i = 0
    while i < len(folded):
        ch = folded[i]
        if ch in _HYPHENS:
            j = i + 1
            while j < len(folded) and folded[j].isspace():
                j += 1
            if j > i + 1:      # hyphen + line break: rejoin the word
                i = j
                continue
            i += 1
            continue
        if ch.isspace():
            if out and out[-1] != " ":
                out.append(" ")
                origin.append(i)
            i += 1
            continue
        out.append(ch)
        origin.append(i)
        i += 1
    return "".join(out), origin
