"""Phase 8 — the acquisition command carries protocol, not registry logic (design D4)."""

import subprocess
from pathlib import Path

import pytest

COMMAND = Path(".claude/commands/research-acquire.md")
GUIDE = Path("docs/research_seam_operator_guide.md")


@pytest.fixture(scope="module")
def command_body() -> str:
    return COMMAND.read_text()


def test_the_command_is_committed_not_ignored():
    """`.claude/commands/*` is gitignored; this one needs its own negation."""
    ignored = subprocess.run(["git", "check-ignore", str(COMMAND)], capture_output=True)
    assert ignored.returncode != 0, f"{COMMAND} is gitignored and would not be committed"
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(COMMAND)],
                             capture_output=True)
    assert tracked.returncode == 0, f"{COMMAND} is not tracked"


def test_the_command_calls_the_two_clis(command_body):
    assert "source_registry.py" in command_body
    assert "research_seam.py" in command_body


@pytest.mark.parametrize("forbidden", ["SOURCE_INDEX.md", "MANIFEST.jsonl",
                                       "--index", "--summarize"])
def test_the_command_never_touches_registry_files_itself(command_body, forbidden):
    assert forbidden not in command_body


def test_the_command_states_the_standing_prohibitions(command_body):
    lowered = command_body.lower()
    assert "webfetch" in lowered and "triage" in lowered          # R-C2
    assert "di-" in lowered or "domain insight" in lowered        # R-C3
    assert "/research" in command_body                            # R-C4, the approval gate


def test_the_guide_covers_all_four_return_classes():
    body = GUIDE.read_text()
    for klass in ("REGISTERED", "BOUNDED_NEGATIVE", "OPERATOR_QUEUE", "BLOCKER"):
        assert klass in body


def test_the_guide_covers_the_three_operator_actions_and_the_blind_spot():
    body = GUIDE.read_text()
    for heading in ("Act on a queued source", "Act on a bounded negative",
                    "Read a `verify` report"):
        assert heading in body
    assert "term" in body and "PROTOCOL.md" in body               # B3 blind spot, §6 route
    assert "--use-for" in body                                    # the --local-pdf break


def test_the_guide_records_the_two_upstream_filings():
    body = GUIDE.read_text()
    assert "PM-APPROVE-RESEARCH-EMPTY-INSIGHTS" in body
    assert "EXTRACT-PROVENANCE-HOOK" in body
