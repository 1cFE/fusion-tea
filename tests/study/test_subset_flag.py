"""S1 / Invariant 11: a subset run cannot pass for a complete one.

The record-feeding invocation traces every group in the declaration and emits
`subset: false`. `--group` is a debugging aid and always emits `subset: true`, so
a record reader can see the difference mechanically instead of trusting a runbook.
"""

import hashlib

from tests.study.conftest import DATA_DIR, REAL_MANIFEST, REAL_PACKAGE, run_tool

KNOWN_ANSWERS = DATA_DIR / "axes.known_answers.json"
ALL_AXES = ["R", "R+tie", "a", "availability", "beta", "interest_rate"]


def test_a_full_run_covers_the_whole_declaration():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    assert doc["axis_declaration"]["subset"] is False
    assert doc["axis_declaration"]["groups_declared"] == ALL_AXES
    assert [g["axis"] for g in doc["groups"]] == ALL_AXES


def test_a_group_run_is_visibly_narrower():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS, group=("R",))
    assert doc["axis_declaration"]["subset"] is True
    assert doc["axis_declaration"]["groups_declared"] == ALL_AXES  # still the whole file
    assert [g["axis"] for g in doc["groups"]] == ["R"]


def test_several_groups_can_be_selected():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS, group=("beta", "R"))
    assert doc["axis_declaration"]["subset"] is True
    assert [g["axis"] for g in doc["groups"]] == ["R", "beta"]


def test_a_subset_group_is_byte_identical_to_its_full_run_counterpart():
    """The debugging aid answers the same question, just about fewer axes."""
    full = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    subset = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS, group=("beta",))
    assert next(g for g in full["groups"] if g["axis"] == "beta") == subset["groups"][0]


def test_the_axis_declaration_digest_matches_the_file_bytes():
    doc = run_tool(REAL_PACKAGE, REAL_MANIFEST, KNOWN_ANSWERS)
    expected = hashlib.sha256(KNOWN_ANSWERS.read_bytes()).hexdigest()
    assert doc["axis_declaration"]["digest"] == expected
    assert doc["axis_declaration"]["schema_version"] == "study-axis-declaration/v1"
    assert doc["axis_declaration"]["path"] == "tests/study/data/axes.known_answers.json"
