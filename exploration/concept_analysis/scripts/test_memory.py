#!/usr/bin/env python3
"""Tests for load_relevant_memories() in run_analysis.py."""

import tempfile
from pathlib import Path

from lib.memory import load_relevant_memories

SAMPLE_ENTRIES = """\
# Cross-Concept Learnings

## ARIES Studies Are Best Parameter Source for MFE Concepts
Date: 2026-03-29 | Concepts: MFE

ARIES-AT and ARIES-CS studies provide the most complete parameter sets
for magnetic confinement cost modeling.

## FLiBe Coolant Cost Data Is Consistently Sparse
Date: 2026-03-29 | Concepts: 09, 14, 22, IFE

IFE concepts using FLiBe as primary coolant/breeder consistently lack
cost data for coolant inventory and processing.

## Assessment Repeatedly Flags Missing O&M Breakdown
Date: 2026-03-29 | Concepts: all

The assessment agent flags missing O&M cost breakdown in >80% of
first-pass analyses.
"""


def _make_memory_dir(content: str | None = None) -> tempfile.TemporaryDirectory:
    """Create a temp dir with an optional learnings.md file."""
    td = tempfile.TemporaryDirectory()
    if content is not None:
        Path(td.name, "learnings.md").write_text(content, encoding="utf-8")
    return td


def test_empty_dir():
    """NF-1: empty dir returns empty string."""
    with tempfile.TemporaryDirectory() as d:
        assert load_relevant_memories("09-laser-ife", Path(d)) == ""


def test_nonexistent_dir():
    """Non-existent dir returns empty string."""
    assert load_relevant_memories("09-laser-ife", Path("/nonexistent")) == ""


def test_empty_file():
    """Dir with a file containing no entries returns empty string."""
    with _make_memory_dir("# Cross-Concept Learnings\n") as d:
        assert load_relevant_memories("09-laser-ife", Path(d)) == ""


def test_concept_match():
    """Concept-specific entry matches by short ID."""
    with _make_memory_dir(SAMPLE_ENTRIES) as d:
        result = load_relevant_memories("09-laser-ife", Path(d))
        assert "FLiBe Coolant" in result
        assert "Missing O&M" in result  # 'all' matches too
        # MFE-only entry should NOT match (no family provided)
        assert "ARIES Studies" not in result


def test_concept_no_match():
    """Concept not tagged in any entry gets only 'all' entries."""
    with _make_memory_dir(SAMPLE_ENTRIES) as d:
        result = load_relevant_memories("35-some-concept", Path(d))
        assert "Missing O&M" in result  # 'all' matches
        assert "ARIES" not in result
        assert "FLiBe" not in result


def test_family_match():
    """Family-tagged entry matches by confinement family."""
    with _make_memory_dir(SAMPLE_ENTRIES) as d:
        result = load_relevant_memories("01-hts-compact-tokamak", Path(d), family="MFE")
        assert "ARIES Studies" in result  # MFE match
        assert "Missing O&M" in result   # 'all' match
        assert "FLiBe" not in result      # IFE only


def test_family_match_ife():
    """IFE family matches IFE-tagged entries."""
    with _make_memory_dir(SAMPLE_ENTRIES) as d:
        result = load_relevant_memories("09-laser-ife", Path(d), family="IFE")
        assert "FLiBe Coolant" in result  # concept 09 + IFE
        assert "Missing O&M" in result    # 'all'
        assert "ARIES" not in result      # MFE only


def test_all_match():
    """Universal entry matches every concept."""
    with _make_memory_dir(SAMPLE_ENTRIES) as d:
        result = load_relevant_memories("99-nonexistent", Path(d))
        assert "Missing O&M" in result


def test_family_case_insensitive():
    """Family matching is case-insensitive (lowercased input still works)."""
    with _make_memory_dir(SAMPLE_ENTRIES) as d:
        result = load_relevant_memories("01-tok", Path(d), family="mfe")
        assert "ARIES Studies" in result


def test_multiple_files():
    """Memories are loaded from all .md files in the directory."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "learnings.md").write_text(
            "## Entry A\nDate: 2026-03-29 | Concepts: 01\n\nFirst file.\n",
            encoding="utf-8",
        )
        (d / "patterns.md").write_text(
            "## Entry B\nDate: 2026-03-29 | Concepts: 01\n\nSecond file.\n",
            encoding="utf-8",
        )
        result = load_relevant_memories("01-tok", d)
        assert "Entry A" in result
        assert "Entry B" in result


def test_entry_without_metadata_skipped():
    """Entries missing the Date/Concepts metadata line are skipped."""
    content = """\
# Learnings

## Has Metadata
Date: 2026-03-29 | Concepts: 01

Good entry.

## No Metadata Line

This entry lacks the Date | Concepts line and should be skipped.
"""
    with _make_memory_dir(content) as d:
        result = load_relevant_memories("01-tok", Path(d))
        assert "Has Metadata" in result
        assert "No Metadata" not in result


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    if passed < len(tests):
        raise SystemExit(1)
