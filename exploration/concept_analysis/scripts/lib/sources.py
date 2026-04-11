"""Source file discovery, slugification, and management helpers."""

import re
from pathlib import Path

from lib.paths import EXTRACT_OUTPUT, RESEARCH_DIR


def find_sources(concept_id: str, research_dir: Path = RESEARCH_DIR) -> list[Path]:
    """Find all extracted source documents for a concept from Phase 1a.

    Scans all iter-*/sources/ directories for .md files.
    Returns sorted list of absolute paths.
    """
    concept_dir = research_dir / concept_id
    if not concept_dir.exists():
        return []

    sources = []
    for iter_dir in sorted(concept_dir.glob("iter-*")):
        sources_dir = iter_dir / "sources"
        if sources_dir.exists():
            sources.extend(sorted(sources_dir.glob("*.md")))
    return sources


def _slugify_text(text: str, max_len: int = 60) -> str:
    """Slugify text into a hyphenated lowercase string."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if len(slug) <= max_len:
        return slug
    truncated = slug[:max_len]
    last_sep = truncated.rfind("-")
    return truncated[:last_sep] if last_sep > max_len // 2 else truncated


def _slugify_url(url: str, max_len: int = 60) -> str:
    """Slugify a URL into a descriptive hyphenated name."""
    from urllib.parse import urlparse

    parsed = urlparse(url)
    # Use domain + path for descriptive names
    domain = parsed.netloc.replace("www.", "").split(".")[0]  # e.g., "arxiv", "realta"
    path = parsed.path.rstrip("/")
    # Strip common prefixes
    for prefix in ("/abs/", "/pdf/", "/html/", "/article/", "/papers/"):
        if path.startswith(prefix):
            path = path[len(prefix) :]
            break
    # Strip file extensions
    path = re.sub(r"\.(pdf|html|htm)$", "", path)
    # Combine domain + meaningful path
    combined = f"{domain}-{path}" if path else domain
    return _slugify_text(combined, max_len)


def slugify_source(input_str: str, max_len: int = 60) -> str:
    """Derive a hyphenated source name from a file path or URL."""
    if input_str.startswith(("http://", "https://")):
        return _slugify_url(input_str, max_len)
    # Local file: use stem
    name = Path(input_str).stem
    return _slugify_text(name, max_len)


def flatten_companion_dir(companion_dir: Path) -> None:
    """Flatten nested extraction subdirectory if present.

    PDF extraction via agentic-mbse creates a nested subdir named after the
    input file. This moves its contents up one level and removes the empty
    nested dir.
    """
    subdirs = [d for d in companion_dir.iterdir() if d.is_dir()]
    candidates = [d for d in subdirs if (d / EXTRACT_OUTPUT).exists()]
    if len(candidates) != 1:
        return  # already flat or ambiguous
    nested = candidates[0]
    for item in nested.iterdir():
        dest = companion_dir / item.name
        if item.is_file():
            item.rename(dest)
        elif not dest.exists():
            item.rename(dest)
    if not any(nested.iterdir()):
        nested.rmdir()


def find_latest_sources_dir(
    concept_id: str, research_dir: Path = RESEARCH_DIR
) -> Path:
    """Find the latest iter-NN/sources/ dir, or create iter-01/sources/."""
    concept_dir = research_dir / concept_id
    iter_dirs = sorted(concept_dir.glob("iter-*"))
    if iter_dirs:
        sources_dir = iter_dirs[-1] / "sources"
        sources_dir.mkdir(exist_ok=True)
        return sources_dir
    # No iterations exist — create iter-01
    sources_dir = concept_dir / "iter-01" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    return sources_dir


def check_duplicate_source(
    concept_id: str, name: str, research_dir: Path = RESEARCH_DIR
) -> Path | None:
    """Check if a source with this name already exists in any iteration."""
    concept_dir = research_dir / concept_id
    for iter_dir in concept_dir.glob("iter-*"):
        candidate = iter_dir / "sources" / f"{name}.md"
        if candidate.exists():
            return candidate
    return None


def resolve_source_names(
    concept_id: str, names: list[str], research_dir: Path = RESEARCH_DIR
) -> list[Path]:
    """Resolve short source names to full paths under the concept."""
    concept_dir = research_dir / concept_id
    resolved = []
    for name in names:
        # Append .md if not present
        fname = name if name.endswith(".md") else f"{name}.md"
        matches = list(concept_dir.glob(f"iter-*/sources/{fname}"))
        if not matches:
            raise ValueError(
                f"Source '{name}' not found under {concept_dir}/iter-*/sources/"
            )
        if len(matches) > 1:
            raise ValueError(
                f"Source '{name}' found in multiple iterations: {matches}"
            )
        resolved.append(matches[0])
    return resolved


def get_dossier_path(concept_id: str, research_dir: Path = RESEARCH_DIR) -> Path | None:
    """Get path to Phase 1a dossier for a concept. Returns None if not found."""
    path = research_dir / concept_id / "dossier.md"
    return path if path.exists() else None


def format_source_list(sources: list[Path]) -> str:
    """Format source file list for inclusion in prompts.

    Shows each source with its file size for context.
    """
    if not sources:
        return "(no extracted source documents found)"

    lines = []
    for src in sources:
        size_kb = src.stat().st_size / 1024
        lines.append(f"- `{src}` ({size_kb:.0f} KB)")
    return "\n".join(lines)


def parse_proposed_actions(review_path: Path) -> list[dict]:
    """Parse Proposed Actions from review.md.

    Returns list of dicts with keys: id, description, category, severity,
    location, finding, proposed_fix, decision, user_notes.
    """
    from lib.validators import PROPOSED_ACTION_RE

    text = review_path.read_text(encoding="utf-8")
    actions = []

    matches = list(PROPOSED_ACTION_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        action = {
            "id": m.group(1),
            "description": m.group(2).strip(),
        }

        # Extract fields from **Key:** Value pattern
        for field_key, dict_key in [
            ("Category", "category"),
            ("Severity", "severity"),
            ("Location", "location"),
            ("Finding", "finding"),
            ("Proposed Fix", "proposed_fix"),
            ("Decision", "decision"),
            ("User Notes", "user_notes"),
        ]:
            field_pattern = re.compile(
                rf"^\-\s*\*\*{re.escape(field_key)}:\*\*\s*(.+)$",
                re.MULTILINE,
            )
            field_match = field_pattern.search(block)
            if field_match:
                val = field_match.group(1).strip()
                # Strip italic placeholder markers
                if val.startswith("_[") and val.endswith("]_"):
                    val = ""  # unfilled placeholder
                elif val.startswith("_") and val.endswith("_"):
                    val = ""
                action[dict_key] = val
            else:
                action[dict_key] = ""

        actions.append(action)

    return actions
