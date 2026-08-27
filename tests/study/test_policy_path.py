"""The study policy has one home after ratification, and the live surfaces cite it.

Ratified whole by the owner (RUN-STUDY Item 6 Align, 2026-08-21) and moved from its
active-work draft path to `modeling_project/STUDY_POLICY.md`. The skill, the runbook,
and the proof-of-life runner name the policy by path, so a stale path there would send
the next study to a file that no longer exists. Historical records (completed items,
reports, research) keep the path they were written against and are not checked.
"""

import re

import pytest

POLICY = "modeling_project/STUDY_POLICY.md"
DRAFT_PATH = ".project/active/demo-study-parameterization-policy"

#: Files a study session reads or runs. Each must name the ratified path and must not
#: name the retired draft path.
LIVE = [
    ".claude/skills/run-study/SKILL.md",
    ".claude/skills/run-study/runbook.md",
    "exploration/stellarator_e2e/study/run_design_search.py",
]


@pytest.fixture
def policy(repo_root):
    path = repo_root / POLICY
    assert path.is_file(), f"{POLICY} missing: the policy was not moved"
    return path.read_text()


@pytest.mark.parametrize("rel", LIVE)
def test_live_surface_cites_the_ratified_policy(repo_root, rel):
    text = (repo_root / rel).read_text()
    assert POLICY in text, f"{rel} does not name {POLICY}"
    assert DRAFT_PATH not in text, f"{rel} still names the retired draft path"


def test_draft_path_is_gone(repo_root):
    assert not (repo_root / DRAFT_PATH).exists(), "the draft directory still exists"


def test_policy_is_ratified_not_draft(policy):
    status = re.search(r"^\*\*Status\*\*: (.+)$", policy, re.M)
    assert status and status.group(1).startswith("Ratified"), status


def test_policy_carries_the_axis_forces_section(policy):
    assert "## 9. Axis forces and framing" in policy
    section = policy.split("## 9. Axis forces and framing", 1)[1]
    assert "no_constraint_response" in section
    assert "never gate" in section


def test_h1_is_scoped_to_search_framed_studies(policy):
    h1 = policy.split("**H1 (parameterization holds)**", 1)[1][:900]
    assert "search-framed" in h1
    assert "sensitivity" in h1


def test_policy_records_the_verification_dispositions(policy):
    assert "## 10. Verification" in policy
    section = policy.split("## 10. Verification", 1)[1]
    assert "1costingFE is the validation reference" in section
    assert "not a study obligation" in section
