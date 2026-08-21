"""The annex is the runbook's other half: every link it makes must land somewhere.

The runbook is delivered and its links are the contract, so the section headings are
asserted verbatim rather than approximately. The two content assertions are the two
facts a reader is most likely to get wrong if the annex softens them.
"""

import re

import pytest

ANNEX = "exploration/stellarator_e2e/studies/ANNEX.md"
RUNBOOK = ".claude/skills/run-study/runbook.md"

SECTIONS = [
    "§ Declared ties",
    "§ Baseline pin",
    "§ Oracle",
    "§ Validity masks",
    "§ Loader exception and glue",
    "§ Era pin",
]


@pytest.fixture
def annex(repo_root):
    return (repo_root / ANNEX).read_text()


@pytest.mark.parametrize("section", SECTIONS)
def test_every_linked_section_exists_verbatim(section, annex):
    assert f"\n## {section}\n" in annex, section


def test_the_runbook_links_no_section_the_annex_lacks(repo_root, annex):
    """An orphaned link is a runbook step whose package fact does not exist."""
    linked = set(re.findall(r"`§ ([^`]+)`", (repo_root / RUNBOOK).read_text()))
    assert linked, "the runbook links no annex sections at all"
    assert linked <= {s.removeprefix("§ ") for s in SECTIONS}, sorted(linked)


def test_the_annex_has_no_seventh_section(annex):
    headings = re.findall(r"^## (.+)$", annex, flags=re.MULTILINE)
    assert headings == SECTIONS, headings


def test_the_radial_build_mask_is_stated_as_a_derived_bound_not_a_design_screen(annex):
    section = annex.split("## § Validity masks")[1].split("\n## ")[0]
    assert "R > a + 2.25 m" in section
    assert "derived geometric bound" in section
    assert "not a design screen" in section
    # The number must be itemized, so a moved layer thickness moves the bound.
    assert "2.25" in section and "blanket" in section


def test_the_deletion_condition_lives_with_the_loader_exception(annex):
    """Deletion is a fact about the exception, so it lives with it — not in a seventh
    section no runbook step links."""
    section = annex.split("## § Loader exception and glue")[1].split("\n## ")[0]
    assert "Deletion condition" in section
    assert "ProvisionalPackageLoader" in section and "strict=True" in section
    assert "deleted whole" in section
    assert "no dormant" in section or "no partial retirement" in section


def test_the_glue_ledger_names_g3_as_not_independently_verified(annex):
    section = annex.split("## § Loader exception and glue")[1].split("\n## ")[0]
    assert "`g3`" in section and "special_materials_capital" in section
    assert "**No.**" in section


def test_the_era_pin_section_states_that_mains_refusal_is_principled(annex):
    section = annex.split("## § Era pin")[1]
    assert "principled" in section
    assert "not to be chased upstream" in section
