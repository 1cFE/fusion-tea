"""YAML frontmatter parsing and manipulation for analysis markdown files."""

import re
from datetime import date
from pathlib import Path

from lib.concepts import get_comparison_status


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Returns dict of key-value pairs. Simple parser — handles single-line
    key: value pairs and list items under a key.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    fm_text = text[3:end].strip()
    result = {}
    current_list_key = None

    for line in fm_text.splitlines():
        stripped = line.strip()
        if not stripped:
            current_list_key = None
            continue

        # List item under current key
        if stripped.startswith("- ") and current_list_key:
            if current_list_key not in result:
                result[current_list_key] = []
            if isinstance(result[current_list_key], list):
                result[current_list_key].append(stripped[2:].strip())
            continue

        # Key: value pair
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if val:
                result[key] = val
                current_list_key = None
            else:
                # Key with no value — next lines might be list items
                result[key] = []
                current_list_key = key

    return result


def update_frontmatter_field(text: str, key: str, value: str) -> str:
    """Update or insert a field in YAML frontmatter.

    If the key exists (with or without a value), replace the line.
    If the key doesn't exist, insert before the closing ---.
    """
    if not text.startswith("---"):
        return text

    end = text.find("---", 3)
    if end == -1:
        return text

    fm_section = text[3:end]
    body = text[end:]

    # Try to replace existing key
    pattern = re.compile(rf"^({re.escape(key)})\s*:.*$", re.MULTILINE)
    new_line = f"{key}: {value}"
    if pattern.search(fm_section):
        fm_section = pattern.sub(new_line, fm_section)
    else:
        # Insert before end of frontmatter
        fm_section = fm_section.rstrip("\n") + f"\n{new_line}\n"

    return "---" + fm_section + body


def remove_frontmatter_field(text: str, key: str) -> str:
    """Remove a field line from YAML frontmatter if present.

    Returns the text unchanged when there is no frontmatter, no closing ``---``,
    or the key is absent. Order of remaining fields is preserved.
    """
    if not text.startswith("---"):
        return text

    end = text.find("---", 3)
    if end == -1:
        return text

    fm_section = text[3:end]
    body = text[end:]

    # Match the full line (including its trailing newline) so removal does
    # not leave a blank line behind.
    pattern = re.compile(
        rf"^{re.escape(key)}\s*:.*(?:\r\n|\r|\n)?", re.MULTILINE
    )
    if not pattern.search(fm_section):
        return text

    fm_section = pattern.sub("", fm_section)
    return "---" + fm_section + body


def make_frontmatter(record: dict) -> str:
    """Generate the orchestrator-owned YAML frontmatter block from a record.

    All fields are deterministic table reads (design.md Invariant #2) and
    orchestrator-owned: ``Confinement-Family``, ``Archetype``, ``Archetype-Fit``,
    ``Comparison-Status``, ``Comparables``, and the four ``Design-Point-*`` /
    ``P-Native`` / ``Grounding-Confidence`` fields are written once at concept
    init and never edited by the analyzer (Invariant #3). ``Comparables``
    replaces the retired ``Reuses:`` field.

    Reads canonical snake_case keys, falling back to the read-only legacy
    aliases so a record (or a legacy-shaped dict carrying the aliases) both work.
    The four design-point fields are emitted only when ``design_point`` is set.
    """
    cid = record.get("concept_id") or record.get("_id", "")
    name = record.get("concept_name") or record.get("Concept Name", "")
    company = record.get("company") or record.get("Company", "")
    family = record.get("confinement_family") or record.get("Confinement Family", "")
    archetype = record.get("archetype_enum", "") or ""
    fit_grade = record.get("fit_grade", "") or ""
    comparables = record.get("comparables") or []
    design_point = record.get("design_point")
    comparison_status = get_comparison_status(record)

    lines = [
        "---",
        f"ID: {cid}",
        f"Concept: {name}",
        f"Company: {company}",
        "Status: draft",
        f"Created: {date.today().isoformat()}",
        "Approved-Date:",
        f"Confinement-Family: {family}",
        # Archetype is empty for fit_grade=None concepts.
        f"Archetype: {archetype}".rstrip(),
        f"Archetype-Fit: {fit_grade}",
        f"Comparison-Status: {comparison_status}",
    ]

    # Comparables MUST be a YAML block list (one `  - id` per line), not a flow
    # list, so parse_frontmatter's block-list parser round-trips it. Empty → [].
    if comparables:
        lines.append("Comparables:")
        lines.extend(f"  - {c}" for c in comparables)
    else:
        lines.append("Comparables: []")

    # Design-point selection fields — present only when a design_point.csv row
    # exists. These are the *selection* (named plant, maturity, P_native,
    # grounding); the quantitative geometry/physics stays in analyze (Item 8).
    if design_point:
        lines.extend([
            f"Design-Point-Name: {design_point.get('design_name', '')}",
            f"Design-Point-Maturity: {design_point.get('maturity_tier', '')}",
            f"P-Native: {design_point.get('p_native_mwe', '')}",
            f"Grounding-Confidence: {design_point.get('grounding_confidence', '')}",
        ])

    lines.append("---")
    return "\n".join(lines) + "\n"
