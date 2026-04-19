"""YAML frontmatter parsing and manipulation for analysis markdown files."""

import re
from datetime import date
from pathlib import Path


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


def make_frontmatter(concept: dict) -> str:
    """Generate YAML frontmatter deterministically.

    Reuses starts as [] — the agent updates it via Edit tool if it
    references approved prior analyses during Stage 2.
    """
    today = date.today().isoformat()
    lines = [
        "---",
        f"ID: {concept['_id']}",
        f"Concept: {concept['Concept Name']}",
        f"Company: {concept.get('Company', '')}",
        "Status: draft",
        f"Created: {today}",
        "Approved-Date:",
        "Reuses: []",
        "---",
    ]
    return "\n".join(lines) + "\n"
