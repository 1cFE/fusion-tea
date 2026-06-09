"""Agentic research findings — synthesis exec summary + full analysis.md content.

Renders the concept-analysis markdown corpus into HTML for display on the
concept profile page. Hybrid approach: when ``synthesis.md`` exists, its
"## 1. Executive Summary" section is rendered as a TL;DR above the full
``analysis.md`` content. Either or both may be missing — the renderer handles
each case independently and the API response advertises which sections are
present so the frontend can render only what's available.

Source location: ``exploration/concept_analysis/analyses/{slug}/`` where the
slug is the directory name (e.g. ``01-hts-compact-tokamak``). The slug is
discovered by scanning for a directory matching ``{concept_id}-*``; the
short concept_id (e.g. ``01``, ``17a``) is enough to look up by prefix.

YAML frontmatter is stripped from both files before rendering. Image
references are left as-is — markdown renders them as ``<img>`` tags whose
``src`` may 404 if the path is repo-relative, but the alt text remains
readable and the page degrades gracefully.

Pure module — no FastAPI dependencies. The server's findings endpoint calls
``build_findings(concept_id, base_dir)`` and serializes the result.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import markdown


@dataclass
class FindingsPayload:
    """API response shape for ``/api/concepts/{id}/findings``.

    Each field is HTML (already rendered from markdown) or None when the
    source file is absent. The frontend renders only the non-None sections.
    """

    exec_summary_html: str | None
    analysis_html: str | None


_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n?", re.DOTALL)
# Matches the first "## 1. Executive Summary" heading and captures everything
# until the next H2 (## ) heading or end of file. Synthesis files follow a
# numbered-section convention ("## 1. ...", "## 2. ...") so this anchors
# specifically on the "1. Executive Summary" header to avoid grabbing a later
# section if the doc gets reorganized.
_EXEC_SUMMARY_RE = re.compile(
    r"^##\s+1\.\s+Executive Summary\s*\n(.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)

_MD = markdown.Markdown(extensions=["tables", "fenced_code"])


def _strip_frontmatter(text: str) -> str:
    """Remove a leading ``---\\n...---\\n`` YAML frontmatter block."""
    return _FRONTMATTER_RE.sub("", text, count=1)


def _extract_exec_summary(synthesis_text: str) -> str | None:
    """Return just the "## 1. Executive Summary" section body, no header."""
    body = _strip_frontmatter(synthesis_text)
    match = _EXEC_SUMMARY_RE.search(body)
    if match is None:
        return None
    return match.group(1).strip() or None


def _find_concept_dir(concept_id: str, analyses_root: Path) -> Path | None:
    """Find ``{analyses_root}/{concept_id}-*`` matching the short concept_id.

    Returns None when no directory matches. Letter-suffix IDs (``17a``,
    ``20b``) are anchored via the trailing hyphen — ``17`` doesn't match
    ``17a-*`` because the prefix check requires the next character to be ``-``.
    """
    prefix = f"{concept_id}-"
    for child in analyses_root.iterdir():
        if child.is_dir() and child.name.startswith(prefix):
            return child
    return None


def build_findings(concept_id: str, analyses_root: Path) -> FindingsPayload:
    """Build the findings payload for one concept.

    Returns a payload with both fields None when the concept directory
    doesn't exist or neither markdown file is present.
    """
    concept_dir = _find_concept_dir(concept_id, analyses_root)
    if concept_dir is None:
        return FindingsPayload(exec_summary_html=None, analysis_html=None)

    exec_summary_html: str | None = None
    analysis_html: str | None = None

    synthesis_path = concept_dir / "synthesis.md"
    if synthesis_path.exists():
        text = synthesis_path.read_text(encoding="utf-8", errors="replace")
        body = _extract_exec_summary(text)
        if body:
            # Markdown.reset() between calls so the parser doesn't leak state
            # (extensions like footnotes accumulate references across calls).
            _MD.reset()
            exec_summary_html = _MD.convert(body)

    analysis_path = concept_dir / "analysis.md"
    if analysis_path.exists():
        text = analysis_path.read_text(encoding="utf-8", errors="replace")
        body = _strip_frontmatter(text)
        _MD.reset()
        analysis_html = _MD.convert(body)

    return FindingsPayload(
        exec_summary_html=exec_summary_html,
        analysis_html=analysis_html,
    )
