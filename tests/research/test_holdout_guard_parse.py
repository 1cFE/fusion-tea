"""Phase 2 — the barred set comes from PROTOCOL.md, and a reformat fails closed.

The expected path set below is transcribed from `knowledge/holdout/aries-cs/PROTOCOL.md`
§3. Bibliographic references to barred paths are not barred data (PROTOCOL §3), so
pinning them here is admissible; no ARIES-CS design or cost content appears anywhere
in this suite (spec R-D4).
"""

import ast
import re
from pathlib import Path

import holdout_guard
import pytest

FIXTURES = Path(__file__).parent / "fixtures" / "protocol"

EXPECTED_BARRED = frozenset({
    "knowledge/holdout/aries-cs/*.pdf",
    "exploration/concept_analysis/analyses/09-qi-stellarator-hts/**",
    "knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-compact-stellarator-study.md",
    "knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-systems-optimization.md",
    "knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md",
    "knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/**",
    "knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326-the-aries-cs-compact-stellarator-fusion*",
    "knowledge/sources/aries_cost_account_documentation/**",
    "knowledge/sources/tea_dt_mfe_cost_analysis/**",
})


def test_parsed_set_pinned_exactly():
    got = holdout_guard.barred_paths()
    assert got == EXPECTED_BARRED
    assert len(got) == len(EXPECTED_BARRED) == 9


def test_both_section_three_lists_are_parsed():
    """A shortened list fails open, so each list is asserted non-empty on its own."""
    got = holdout_guard.barred_paths()
    assert "knowledge/holdout/aries-cs/*.pdf" in got                    # ### Barred
    assert "knowledge/sources/tea_dt_mfe_cost_analysis/**" in got       # exception-path list


def test_reformatted_bullet_fails_closed():
    with pytest.raises(holdout_guard.ProtocolParseError):
        holdout_guard.barred_paths(protocol=FIXTURES / "reformatted_bullets.md")


def test_missing_section_fails_closed(tmp_path):
    stub = tmp_path / "PROTOCOL.md"
    stub.write_text("# Protocol\n\n## 3. Clean-room admissibility\n\nNo lists here.\n")
    with pytest.raises(holdout_guard.ProtocolParseError):
        holdout_guard.barred_paths(protocol=stub)


@pytest.mark.parametrize("text", [
    "ARIES-CS cost",
    "ARIES‑CS cost",          # non-breaking hyphen
    "ARIES-\nCS cost",             # PDF line-break hyphenation
    "ARIES\nCS cost",              # line-broken, no hyphen
    "aries cs cost",
    "ariescs",
])
def test_term_match_survives_hyphenation_and_line_breaks(text):
    matches = holdout_guard.scan_terms(text)
    assert [m.rule_id for m in matches] == ["term:aries-cs"]
    assert matches[0].count == 1
    assert matches[0].offsets


def test_sealed_paper_stems_and_host_are_terms():
    got = {m.rule_id for m in holdout_guard.scan_terms(
        "see 08-FST-Najmabadi.pdf mirrored at aries.ucsd.edu/LIB")}
    assert got == {"term:08-fst-najmabadi", "term:aries.ucsd.edu"}


def test_clean_text_matches_nothing():
    assert holdout_guard.scan_terms("Stellaris quasi-isodynamic coil set, W7-X data") == []


def test_offsets_point_into_the_original_text():
    text = "prefix prefix ARIES-CS tail"
    (match,) = holdout_guard.scan_terms(text)
    start = match.offsets[0]
    assert text[start:start + len("ARIES-CS")] == "ARIES-CS"


@pytest.mark.parametrize("path,expected", [
    ("knowledge/holdout/aries-cs/08-FST-Ku.pdf", "path:knowledge/holdout/aries-cs/*.pdf"),
    ("knowledge/sources/tea_dt_mfe_cost_analysis/output.md",
     "path:knowledge/sources/tea_dt_mfe_cost_analysis/**"),
    ("exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md",
     "path:exploration/concept_analysis/analyses/09-qi-stellarator-hts/**"),
])
def test_check_input_path_bars_barred_inputs(path, expected):
    match = holdout_guard.check_input_path(Path(path))
    assert match is not None and match.rule_id == expected


def test_check_input_path_allows_a_clean_input():
    assert holdout_guard.check_input_path(Path("knowledge/raw/some_clean_paper.pdf")) is None


def test_no_waiver_identifier_exists_in_the_guard():
    """D12: no in-code waiver. Checked against identifiers, not prose."""
    tree = ast.parse(Path(holdout_guard.__file__).read_text())
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc:
                docstrings.add(doc)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value not in docstrings:
                names.add(node.value)
    waiver = re.compile(r"(ack\b|_ack|acknowledge|override|waiv|bypass|allowlist)", re.I)
    assert not [n for n in names if waiver.search(n)]
