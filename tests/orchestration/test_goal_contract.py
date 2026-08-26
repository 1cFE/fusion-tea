"""Consistency checks for the goal layer's documents.

Lightweight-consistency altitude only: these tests check that the surfaces
described by `.project/active/goal-harness-contract/design.md` exist and still
agree with each other. They check documents, never runtime behaviour.
"""

import re

import yaml

ADR_FILE = re.compile(r"^\d{3}-.*\.md$")


def _frontmatter(path):
    """Parse a record's YAML frontmatter, tolerating `---` later in the body."""
    text = path.read_text()
    assert text.startswith("---\n"), f"{path.name} opens with a frontmatter block"
    return yaml.safe_load(text.split("---", 2)[1])


def test_register_is_coherent(repo_root):
    """I12: every register id resolves to one file; every file is indexed."""
    adr = repo_root / ".project" / "adr"
    files = {p.name.split("-")[0] for p in adr.glob("*.md") if ADR_FILE.match(p.name)}
    assert files, "the register holds at least one record"
    indexed = set(re.findall(r"^\| `(\d{3})`", (adr / "INDEX.md").read_text(), re.M))
    assert files == indexed

    for p in sorted(adr.glob("*.md")):
        if not ADR_FILE.match(p.name):
            continue
        fm = _frontmatter(p)
        assert fm["grade"], f"{p.name} carries a capture-fidelity grade"
        if fm["amends"] != "none":
            amended = repo_root / str(fm["amends"]).split(":")[0]
            assert amended.exists(), f"{p.name} amends a surface that exists"
