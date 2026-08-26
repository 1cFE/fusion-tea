"""Consistency checks for the goal layer's documents.

Lightweight-consistency altitude only: these tests check that the surfaces
described by `.project/active/goal-harness-contract/design.md` exist and still
agree with each other. They check documents, never runtime behaviour.
"""

import re

import pytest
import yaml

ADR_FILE = re.compile(r"^\d{3}-.*\.md$")

RUNBOOK_STUDY = ".claude/skills/run-study/runbook.md"
DISCOVERY_LOG = "exploration/stellarator_e2e/studies/DISCOVERY_LOG.md"

# The five textual homes that a joined disposition row breaks unless they are amended
# together (spec § Writer ownership). `present` is the load-bearing phrase the home must
# carry; `absent` is the retired clause, matched as a whole clause or with a negative
# lookahead — never as a bare substring, because "one row per finding" is a prefix of
# its own replacement "one row per finding sighting" and would pass forever.
WRITER_HOMES = [
    # runbook step 14 — the sole-writer rule, now scoped to first-sighting rows
    (RUNBOOK_STUDY, r"sole writer of first-sighting rows", r"sole writer of the log"),
    # runbook § Administer — the goal round's append is not an administrator act
    (RUNBOOK_STUDY, r"not an administrator act", None),
    # runbook § DISCOVERY_LOG.md prose — one row per finding *sighting*
    (
        RUNBOOK_STUDY,
        r"one row per finding \*sighting\*",
        r"one row per finding(?! sighting| \*sighting\*)",
    ),
    # runbook schema-table note — a row's kind is positional, newest row is current state
    (RUNBOOK_STUDY, r"joined disposition update, written by a goal round", None),
    # the log header — writer rule, cardinality rule, and the corrected authority citation
    (DISCOVERY_LOG, r"sole writer of first-sighting rows", r"Only a study's executor appends rows"),
    (DISCOVERY_LOG, r"One row per finding sighting", r"one row per finding(?! sighting)"),
]


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


@pytest.mark.parametrize("path,present,absent", WRITER_HOMES)
def test_writer_ownership_agrees(repo_root, path, present, absent):
    """SC4: the five homes agree on writer ownership and joined disposition rows.

    A goal round appends a disposition row under an existing `<study-id>#<n>` id
    (ADR-004). Every home that used to forbid that has to say so, or an operator
    following one document contradicts an operator following another.
    """
    text = (repo_root / path).read_text()
    assert re.search(present, text, re.I | re.S), f"{path} must carry: {present}"
    if absent:
        assert not re.search(absent, text, re.I), f"{path} still carries the retired clause"


RUNBOOK = "work/orchestration/GOAL_RUNBOOK.md"
TEMPLATES = [
    "work/orchestration/goal-templates/goal.md",
    "work/orchestration/goal-templates/trail.md",
    "work/orchestration/goal-templates/learnings.md",
]
SKILL = ".claude/skills/run-goal/SKILL.md"

GOAL_HEADINGS = [
    "Status", "Question", "Consumer", "Answered when", "Invariants",
    "Grounding evidence", "Limits", "Reserved gates", "Close rule", "Amendments",
]
TRAIL_ENTRIES = [
    "Strategy revision", "T-001 scope", "T-001 start", "T-001 return",
    "Checkpoint C-001.r1", "Round 1 result", "Round 1 review", "Stop",
]
# Every stage an operator has to find. The runbook is the only place they are described.
RUNBOOK_STAGES = [
    "Grounding a goal", "Opening and closing a round", "Running one task",
    "The pre-execution disposition checkpoint", "The fresh review",
    "The two checks are distinct", "When a cited artifact moves",
    "Resuming an interruption", "Limits", "The discovery log", "The native seams",
]


def test_goal_template_headings_are_in_the_contracted_order(repo_root):
    """SC2: the headings are the contract (design § Section conventions).

    A fresh reader finds every fixed fact of a goal in one file, in one order.
    """
    text = (repo_root / TEMPLATES[0]).read_text()
    found = re.findall(r"^##\s+(.*)$", text, re.M)
    assert [h for h in found if h in GOAL_HEADINGS] == GOAL_HEADINGS


def test_trail_template_carries_every_entry_heading_in_occurrence_order(repo_root):
    """SC2: a round is reconstructed from these headings alone (design I15, D12)."""
    text = (repo_root / TEMPLATES[1]).read_text()
    found = [h.split(" — ")[0].strip() for h in re.findall(r"^###\s+(.*)$", text, re.M)]
    assert [h for h in found if h in TRAIL_ENTRIES] == TRAIL_ENTRIES
    # I8/I4: the two rules a writer breaks first, stated where they are broken.
    assert re.search(r"retry is \*\*not\*\* a new entry kind", text, re.I)
    assert re.search(r"never an amendment to the previous one", text, re.I)


def test_learnings_template_carries_its_entry_shape(repo_root):
    """SC2: one claim per entry, accepted by a round review before append."""
    text = (repo_root / TEMPLATES[2]).read_text()
    assert re.search(r"^## L-001 — ", text, re.M)
    for field in ["Evidence", "Scope", "Implication", "Supersedes", "Accepted by"]:
        assert re.search(rf"\*\*{field}:\*\*", text), field
    assert re.search(r"[Mm]echanical failures produce no learning", text)


@pytest.mark.parametrize("stage", RUNBOOK_STAGES)
def test_the_runbook_names_every_stage(repo_root, stage):
    """SC5: one document describes every stage, for a human or an agent alike."""
    text = (repo_root / RUNBOOK).read_text()
    assert re.search(rf"^##\s+{re.escape(stage)}\s*$", text, re.M), stage


def test_the_skill_is_a_door_and_not_a_second_copy(repo_root):
    """SC5/D7: the agent's entry surface points at the runbook and restates no rule."""
    text = (repo_root / SKILL).read_text()
    fm = yaml.safe_load(text.split("---", 2)[1])
    assert fm["name"] == "run-goal"
    assert fm["description"].strip(), "the trigger description is how an agent finds it"
    assert "GOAL_RUNBOOK.md" in text, "the skill points at the runbook"
    assert "goal-templates" in text, "the skill points at the templates"
    assert ".project/adr/" in text, "the skill points at the register"


def test_the_amendments_are_live(repo_root):
    """SC1: the guidance CLAUDE.md gives and the record that amends it agree.

    Before this item, CLAUDE.md's blanket rule and the Goal evidence seam ruling
    told an agent to do different things (spec § Problem).
    """
    claude = (repo_root / "CLAUDE.md").read_text()
    # The permission, and the prohibition it narrows rather than removes.
    assert re.search(r"Do not cross-reference \*state\* between them", claude)
    assert re.search(r"cite a `\.project/` artifact by path and digest", claude)
    assert re.search(r"[Cc]iting is not mirroring", claude)
    assert "006-goal-evidence-seam.md" in claude, "CLAUDE.md cites the record"
    record = (repo_root / ".project/adr/006-goal-evidence-seam.md").read_text()
    assert "CLAUDE.md" in record, "the record names the surface it amends"


def _names_the_bar(sentence):
    """A sentence may say the barred act is barred. It may not instruct it."""
    return bool(re.search(r"no goal procedure|barred|never|not a machine check", sentence, re.I))


def test_the_hardening_boundary_is_stated_and_not_crossed(repo_root):
    """SC6, document half: the docs must not instruct the barred act.

    This checks *documents*, not runtime behaviour, and does not claim otherwise —
    a goal agent that compares a digest anyway is caught by review, not by this
    test. Design I6 and the ADR-003 hardening table are the rule; this is the
    prose guard on it.
    """
    for rel in [RUNBOOK, *TEMPLATES]:
        text = (repo_root / rel).read_text()
        for hit in re.finditer(
            r"[^.\n]*\b(?:match\w*|compar\w+|recomput\w+|verif\w+)\b[^.\n]{0,80}digest[^.\n]*",
            text,
            re.I,
        ):
            assert _names_the_bar(hit.group(0)), f"{rel} instructs the barred act: {hit.group(0)!r}"
    runbook = (repo_root / RUNBOOK).read_text()
    # I6, stated where an operator writing a citation will read it.
    assert re.search(r"[Dd]igests are read by people", runbook)
    # I13: external mutation is noticed by a reader, and the runbook says so plainly.
    assert re.search(r"external mutation", runbook)
    assert re.search(r"a reading, not a machine check", runbook)
