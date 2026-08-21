"""The annex is the runbook's other half: every link it makes must land somewhere.

The runbook is delivered and its links are the contract, so the section headings are
asserted verbatim rather than approximately. Two of the runbook's links are optional --
`§ Loader exception and glue` and `§ Era pin` exist only for a package that runs through
an adapter -- and this package runs sealed on stock teax since the stellarator model
migration (2026-08-21), so the annex must *not* carry them and must say why.
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
]
#: Linked by the runbook "when the annex has one"; absent for a package with no adapter.
OPTIONAL_SECTIONS = ["§ Loader exception and glue", "§ Era pin"]


@pytest.fixture
def annex(repo_root):
    return (repo_root / ANNEX).read_text()


@pytest.mark.parametrize("section", SECTIONS)
def test_every_linked_section_exists_verbatim(section, annex):
    assert f"\n## {section}\n" in annex, section


def test_the_runbook_links_no_section_the_annex_lacks(repo_root, annex):
    """An orphaned link is a runbook step whose package fact does not exist -- unless the
    runbook itself marks the link as conditional on the annex having that section."""
    runbook = (repo_root / RUNBOOK).read_text()
    linked = set(re.findall(r"`§ ([^`]+)`", runbook))
    assert linked, "the runbook links no annex sections at all"
    allowed = {s.removeprefix("§ ") for s in SECTIONS + OPTIONAL_SECTIONS}
    assert linked <= allowed, sorted(linked)
    for section in OPTIONAL_SECTIONS:
        for line in runbook.splitlines():
            if f"`{section}`" in line:
                assert "when the annex has one" in line, line


def test_the_annex_has_exactly_the_four_sections(annex):
    headings = re.findall(r"^## (.+)$", annex, flags=re.MULTILINE)
    assert headings == SECTIONS, headings


def test_the_optional_sections_are_absent_and_the_annex_says_why(annex):
    """Gone, not dormant: no adapter section survives, and the reader is told there is no
    adapter and no glue rather than left to infer it from an absence."""
    for section in OPTIONAL_SECTIONS:
        assert f"## {section}" not in annex, section
    assert "no adapter and no glue" in annex
    assert "AFTER_MIGRATION_RECORD.md" in annex


def test_the_radial_build_mask_is_stated_as_a_derived_bound_not_a_design_screen(annex):
    section = annex.split("## § Validity masks")[1].split("\n## ")[0]
    assert "R > a + 2.25 m" in section
    assert "derived geometric bound" in section
    assert "not a design screen" in section
    # The number must be itemized, so a moved layer thickness moves the bound.
    assert "2.25" in section and "blanket" in section


def test_the_oracle_section_publishes_two_surfaces_and_compares_cas27(annex):
    section = annex.split("## § Oracle")[1].split("\n## ")[0]
    assert "`evaluate(point)`" in section and "`operand_bindings()`" in section
    assert "glue_values" not in section
    assert "special_materials_capital" in section
    assert "net_positive.net_electric" in section
