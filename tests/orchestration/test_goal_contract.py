"""Records remain findable and presentation links resolve.

Editorial wording and document layout belong to document review, not pytest.
"""
import re
from pathlib import Path
import yaml

ADR_FILE = re.compile(r"^\d{4}-.*\.md$")


def _frontmatter(path):
    return yaml.safe_load(path.read_text().split("---", 2)[1])


def test_register_is_coherent(repo_root):
    """I12: every register id resolves to one file; every file is indexed."""
    adr = repo_root / ".project" / "adr"
    files = {p.name.split("-")[0] for p in adr.glob("*.md") if ADR_FILE.match(p.name)}
    assert files, "the register holds at least one record"
    indexed = set(re.findall(r"^- (\d{4}) · ", (adr / "INDEX.md").read_text(), re.M))
    assert files == indexed

    for p in sorted(adr.glob("*.md")):
        if not ADR_FILE.match(p.name):
            continue
        fm = _frontmatter(p)
        assert fm["provenance"], f"{p.name} carries a capture-fidelity provenance grade"
        if fm["promoted_to"] is not None:
            promoted = repo_root / str(fm["promoted_to"]).split(":")[0]
            assert promoted.exists(), f"{p.name} names an existing promoted surface"


def _local_link_targets(path: Path, text: str):
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = target.split("#", 1)[0]
        if relative:
            yield (path.parent / relative).resolve(), target



def test_narrative_evidence_links_resolve(repo_root):
    for path in (repo_root / "work/narratives").glob("*.md"):
        for target, written_target in _local_link_targets(path, path.read_text()):
            assert target.exists(), f"{path}: unresolved link {written_target}"
