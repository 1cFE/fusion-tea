"""Cross-concept memory and reuse pool discovery."""

import re
from pathlib import Path

from lib.frontmatter import parse_frontmatter
from lib.paths import ANALYSES_DIR, HANDWRITTEN_DIR, MEMORY_DIR


def find_approved(analyses_dir: Path = ANALYSES_DIR) -> list[Path]:
    """Find all approved analysis.md files (the reuse pool).

    Returns sorted list of absolute paths to analysis.md files
    where frontmatter Status == approved.
    """
    approved = []
    if not analyses_dir.exists():
        return approved

    for analysis_path in sorted(analyses_dir.glob("*/analysis.md")):
        fm = parse_frontmatter(analysis_path)
        if fm.get("Status") == "approved":
            approved.append(analysis_path)
    return approved


def find_approved_syntheses(analyses_dir: Path = ANALYSES_DIR) -> list[Path]:
    """Find synthesis.md files from approved concepts for cross-concept context."""
    results = []
    if not analyses_dir.exists():
        return results

    for analysis_path in sorted(analyses_dir.glob("*/analysis.md")):
        synthesis_path = analysis_path.parent / "synthesis.md"
        if synthesis_path.exists():
            fm = parse_frontmatter(analysis_path)
            if fm.get("Status") == "approved":
                results.append(synthesis_path)
    return results


def find_exemplars(handwritten_dir: Path = HANDWRITTEN_DIR) -> list[Path]:
    """Find all handwritten exemplar analysis files.

    Returns sorted list of absolute paths.
    """
    if not handwritten_dir.exists():
        return []
    return sorted(handwritten_dir.glob("*.md"))


def format_path_list(paths: list[Path], empty_msg: str = "(none)") -> str:
    """Format a list of paths as markdown bullet points."""
    if not paths:
        return empty_msg
    return "\n".join(f"- `{p}`" for p in paths)


# Regex for metadata line: "Date: 2026-03-29 | Concepts: 09, IFE, all"
_MEMORY_META_RE = re.compile(
    r"^Date:\s*\d{4}-\d{2}-\d{2}\s*\|\s*Concepts:\s*(.+)$", re.MULTILINE
)


def load_relevant_memories(
    concept_id: str, memory_dir: Path, family: str = "",
) -> str:
    """Load memory entries relevant to a concept.

    Args:
        concept_id: Full concept ID, e.g. "09-laser-ife". Short ID
            extracted as the leading numeric segment.
        memory_dir: Path to the memory directory.
        family: Confinement family tag, e.g. "IFE". Empty string if unknown.

    Returns:
        Matched entries as a markdown string, or "" if none found
        or memory dir doesn't exist.
    """
    if not memory_dir.is_dir():
        return ""

    md_files = sorted(memory_dir.glob("*.md"))
    if not md_files:
        return ""

    # Extract short ID: "09" from "09-laser-ife"
    short_id = concept_id.split("-")[0]

    # Build match set, dropping empty strings
    match_set = {short_id, family.upper(), "all"} - {""}

    matched: list[str] = []
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        # Split on H2 boundaries — everything from one "## " to the next (or EOF)
        entries = re.split(r"(?=^## )", content, flags=re.MULTILINE)
        for entry in entries:
            entry = entry.strip()
            if not entry.startswith("## "):
                continue
            m = _MEMORY_META_RE.search(entry)
            if not m:
                continue
            tags = {t.strip() for t in m.group(1).split(",")}
            if tags & match_set:
                matched.append(entry)

    return "\n\n".join(matched)
