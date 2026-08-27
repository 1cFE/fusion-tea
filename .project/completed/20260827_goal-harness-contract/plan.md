# Implementation Plan: Lean Goal Contract and Operator Runbook

**Status:** Complete — all seven phases plus the audit-fix hop; `staging/skill-edit-2.md` pending application
**Created:** 2026-08-25
**Last Updated:** 2026-08-25
**Branch:** `feat/run-study-first-consumer` (`[OWNER 2026-08-25]` — no child branch; merge/push and item close stay owner-held)
**Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` — Item 1

## Source Documents

- **Spec:** `.project/active/goal-harness-contract/spec.md`
- **Design:** `.project/active/goal-harness-contract/design.md` (rev 2, approved) ← component detail, invariants I1–I15, decisions D1–D12, bets B1–B5
- **Align:** `.project/active/goal-harness-contract/align.md` — owner rulings, 2026-08-25

The design is approved. This plan does not re-decide it. Where a question about *what* to build arises, the answer is in `design.md`; this plan owns *in what order*, *proved how*.

## The Point

Item 1 puts the goal layer on disk so someone who did not build it can operate it.

The owner's bar is verbatim: `[OWNER-VERBATIM]` "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human," run by an operator who `[OWNER-VERBATIM]` "shouldn't have to be me (who built this and therefore is mostly familiar)" (`.project/concepts/goal-driven-model-development-harness.md` § Owner's Words). That ladders to the epic's critical success factor: a non-builder resumes and completes a real goal round from the goal directory and native records alone, every touched study finding dispositioned, no completed native work repeated.

Four obligations fall out of that:

1. The seven approved decisions become live records with their recorded grades intact, and the one live guidance sentence they contradict (`CLAUDE.md:73`) gets amended.
2. The three lean files (`goal.md`, `trail.md`, `learnings.md`) get conventions detailed enough that current goal state is derivable without mirroring native stage state.
3. The five textual homes that today forbid a goal round from appending a disposition row get amended, so no touched finding is left `unrouted`.
4. One shared `GOAL_RUNBOOK.md` describes the same artifacts, gates, returns, and reviews whether a human or an agent operates the loop.

All of it under the owner's lean-first rule: no hardening mechanism without a recorded observed failure of the prose-and-native-facts route. Items 4–6 test the cold grounding, the resume, and the closure against exactly these documents — so this item is what everything after it reads.

## Implementation Strategy

**Phasing Rationale.**

- **The ADR home lands first, alone, in one complete commit.** Not a de-risking choice — a hard scheduling dependency. Epic Item 2 is running now in a parallel worktree and files decisions into this register "once it exists" (Align ruling 3, design D5). A partial home is worse than none: Item 2 would file against a convention that then changes.
- **The runbook is written before the templates** (design § De-risk first). The templates are the runbook's headings made copyable. Writing them first invites a document that describes the templates instead of the operation — which is the exact failure B1 and the owner's bar are aimed at.
- **The `test_records.py` helper extraction precedes the joined-row fixture test**, so the fixture exercises the same code path the real test does. A fixture with its own parser proves nothing.
- **The joined-row test lands before the shared-file edits.** Today append-as-update passes only by accident of a set comparison (spec `[HARD]`, `test_records.py:64`). Making the accident a stated guarantee before amending the prose homes means the prose and the test never disagree, in either direction.
- **The shared-file edits are their own phase, gated on a re-check** of Item 6's landed state. Both files are shared with a concurrently-running item.
- **Validation is a phase, not a footnote.** Each spec success criterion gets a named concrete check before the item is called done.

**Critical Path.**

Phase 1 (ADR home, one commit) → Phase 2 (runbook) → Phase 3 (templates + skill) → Phase 4 (`test_records.py` refactor + joined-row test) → Phase 5 (re-check + six edits, test-first) → Phase 6 (remaining contract tests) → Phase 7 (validation).

Only Phase 1 → everything and Phase 2 → Phase 3 and Phase 4 → Phase 5 are hard orderings. Phases 2/3 and Phase 4 are independent of each other and could swap if a session is interrupted.

**First Proof Point.**

Phase 4's joined-row fixture test going green *and* going red when `_ids_in_log` is rewritten from a set comprehension to a list. That is the one moment where the design's central mechanism — a disposition update delivered as an appended row under the same id — stops being prose and becomes a checkable fact.

**Overall Validation Approach.**

- Each phase that touches tests starts by writing the test.
- Each phase has automated checks plus a manual read, and states what we then know works.
- `uv run python -m pytest tests/study` must stay green in every phase that touches `tests/study/` or the discovery log. `tests/models` is not touched by this item (needs the SYSIDE env; out of scope here).
- One commit per phase, on `feat/run-study-first-consumer`. No merge, no push, no item close — owner-held.

---

## Phase 1: The ADR home, complete, in one commit

**Grain:** ~2h. **Blocking:** everything, and Item 2 in the parallel worktree.

### Goal

Create `.project/adr/` with its README, index, template, filing script, and all seven records — then commit it as one unit, and only then tell Item 2 it exists. Nothing else lands in this commit.

### Assumption Under Test

That the seven approved decisions can be *filed* without re-deciding anything — that every record's Context, Decision, Rationale, Rejected alternatives, and grade already exist in `.project/concepts/goal-strategy-task-harness-design.md` § Recorded Rulings and ADR Candidates. If a record cannot be written without inventing content, the decision was not actually approved and that is an owner question, not an authoring one.

### Test Stencil (Write This First)

Register coherence, written before the seven records exist so it fails loudly on a partial home. It lands in `tests/orchestration/test_goal_contract.py` (created here, extended in Phase 6):

```python
def test_register_is_coherent(repo_root):
    """I12: every register id resolves to one file; every file is indexed."""
    adr = repo_root / ".project" / "adr"
    files = {p.name.split("-")[0] for p in adr.glob("[0-9][0-9][0-9]-*.md")}
    indexed = set(re.findall(r"^\| `?(\d{3})", (adr / "INDEX.md").read_text(), re.M))
    assert files == indexed
    for p in sorted(adr.glob("[0-9][0-9][0-9]-*.md")):
        fm = yaml.safe_load(p.read_text().split("---")[1])
        assert fm["grade"], f"{p.name} carries a capture-fidelity grade"
        if fm["amends"] != "none":
            assert (repo_root / fm["amends"].split(":")[0]).exists()
```

### Changes Required

**See `design.md` for:** register charter and separation → `design.md#key-decisions` (D1–D4); record form and frontmatter → `design.md#implementation-notes`; the seven records and their grades → `design.md#component-overview`.

- [x] `tests/orchestration/__init__.py` (if the suite needs it), `tests/orchestration/conftest.py` with a single `repo_root` fixture (`design.md#next-stage-handoff` — "probably one `repo_root` fixture")
- [x] `tests/orchestration/test_goal_contract.py` (NEW) — the stencil above only; the other four tests come in Phase 6
- [x] `.project/adr/README.md` — charter; the separation from `modeling_project/ARCHITECTURE.md` stated explicitly (`AD-XXX` = model architecture, `ADR-NNN` = repository/orchestration/tooling); record form; grade vocabulary; the filing procedure
- [x] `.project/adr/template.md` — frontmatter block from `design.md#implementation-notes`, then Context · Decision · Rationale · Rejected alternatives · Affected seams · Consequences
- [x] `.project/adr/INDEX.md` — one line per record, plus the **"Prior art, outside the register"** line for `exploration/phase_1a/ADR-001_csv-source-of-truth.md` with its one-line note (D3 — not renumbered, not moved)
- [x] `.project/scripts/adr.sh` (NEW, ~40 lines, `chmod +x`) — `new <slug>` mints the next id, copies the template, appends the index row; `supersede <old> <new>` flips status and cross-links; `list` prints the index. No other logic (D4)
- [x] `.project/adr/001-strategy-and-task.md` — grade `[AGENT]` ratified by owner
- [x] `.project/adr/002-round-boundary.md` — split grade: `[OWNER]` purpose + `[AGENT]` mechanism
- [x] `.project/adr/003-lean-first-persistence.md` — split grade: `[OWNER]` 2026-08-23 + `[AGENT]` separate-`learnings.md` mechanism
- [x] `.project/adr/004-finding-disposition.md` — `[OWNER]` 2026-08-23
- [x] `.project/adr/005-review-topology.md` — `[AGENT]`, owner may override
- [x] `.project/adr/006-goal-evidence-seam.md` — `[OWNER]` 2026-08-23; frontmatter `amends: CLAUDE.md:73`; names that surface in Affected seams
- [x] `.project/adr/007-supersession.md` — split candidate: `[AGENT]` task-as-authority half, owner-ruled finding-obligation half

**Grades are copied, not re-derived** (`design.md#implementation-notes`). Each grade comes verbatim from `goal-strategy-task-harness-design.md` § Recorded Rulings, including both split grades and the split candidate.

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/orchestration -q` → the register test passes
- [x] `uv run ruff check tests/orchestration` → clean
- [x] `bash .project/scripts/adr.sh list` → prints the seven records
- [x] `bash .project/scripts/adr.sh new scratch-check` → mints `008-scratch-check.md` and an index row; **delete both and revert the index edit** before commit

**Manual:**
- [x] Read `INDEX.md` cold: is the stray `ADR-001` visible and explained where a reader will hit it?
- [x] Diff each record's Decision and Rationale against § Recorded Rulings — nothing invented, nothing dropped
- [x] `git status` shows only `.project/adr/`, `.project/scripts/adr.sh`, and `tests/orchestration/` — nothing else in this commit

**Commit:** one commit, message naming it as the ADR home landing complete (D5).

**Then, and only then:** notify the Item 2 worktree that `.project/adr/` exists and `adr.sh new <slug>` is the filing call.

**What We Know Works After This Phase:** `/_my_design`'s ADR touch points resolve for the first time; Item 2 has a stable convention to file into; the seven rulings are citable by path.

---

## Phase 2: `GOAL_RUNBOOK.md`

**Grain:** ~2h.

### Goal

Write the shared operator deliverable — one document, no copies — to the referent's prose bar. This is the item's headline artifact and the one Item 4 will test cold.

### Assumption Under Test

B1 and B4 together: that a fixed-shape prose document is enough for a non-builder to run a round, and that one document with two doors keeps a human and an agent on the same contract. If a section cannot be written without saying "the agent does X, the human does Y," B4 is wrong and the seam it was written to protect has already failed.

### Test Stencil (Write This First)

Not a pytest stencil — a reading stencil, applied per section as it is written. Every section must answer four questions for a stranger:

```text
what do I do  ·  what do I write  ·  where does it go  ·  who checks it
```

A section that cannot answer all four is not finished. (The pytest form of this — that the runbook names every stage — lands in Phase 6, test 2.)

### Changes Required

**See `design.md` for:** the full section list → `design.md#component-overview` (`GOAL_RUNBOOK.md` entry); entry headings and vocabularies → `design.md#section-conventions`; the caps and their grounding → `design.md#default-limits`; the checkpoint-vs-review split → `design.md#architecture` (last paragraph); the external-mutation reading → I13 and D11.

- [x] `work/orchestration/GOAL_RUNBOOK.md` (NEW) — sections in this order:
  - [x] What the layer is and what it is not
  - [x] The five surfaces and which question each answers
  - [x] Grounding a goal (draft → grounded; I1)
  - [x] Opening and closing a round — the one-pin/one-study bound, the six close triggers, stop reason *derived* from last outcome + limits, and how to tell an open round from a closed one (I14, I15, D12)
  - [x] Running one task — scope → write-ahead → native work → return (I2, I3, I5)
  - [x] The pre-execution disposition checkpoint
  - [x] The fresh `RoundReview` — including the post-execution disposition audit (owner criterion 5's home)
  - [x] **The two checks are distinct** — one table, timing and responsibility side by side (SC3)
  - [x] When a cited artifact moves — how to check, what to write, re-ground or close; the plain statement that this is a *reading*, and that a machine check is the barred stale-authority guard needing an owner ruling (I13, I6)
  - [x] Resuming an interruption
  - [x] The limits table (2 retries / 2 checkpoint revisions / 6 rounds; the declared value wins; hitting the checkpoint cap **stops**, it does not permit execution)
  - [x] The discovery-log rules an operator must know — append only under an existing `<study-id>#<n>`, never mint one, **scan for the id rather than stopping at the first matching row** because the newest row is current state, and where a goal-originated finding goes instead (I7, I8, `design.md#component-overview` last entry)
  - [x] The native seams table — `research` and `integrate` labelled **pending native repair**, naming the documented WI-031 hand pattern and the current manual integration pattern, with the standing rule that a goal round may not silently absorb either repair
  - [x] Citations to the seven ADR records — cited, never restated

**Prose convention:** unwrapped paragraphs, matching `work/orchestration/handshake-lcoe-construction.md` and the other files in that directory.

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/orchestration -q` → still green (Phase 6 adds the runbook assertions)

**Manual:**
- [x] Read `GOAL_RUNBOOK.md` beside `work/orchestration/handshake-lcoe-construction.md` — same density, same explicit grading, same dated-entry discipline
- [x] For each section, confirm the four stencil questions are answered
- [x] Confirm no section splits into a human path and an agent path (B4)
- [x] Grep the file for the comparison verbs applied to "digest" — `matches`, `compare`, `recompute`, `verify the digest`. Any hit is either a violation of I6 or must be the sentence that *names the bar*, not one that instructs the act

**What We Know Works After This Phase:** the operating contract exists in one place; SC5's document exists to be tested.

**Commit.**

---

## Phase 3: The three templates and the `run-goal` skill

**Grain:** ~1h.

### Goal

Make the runbook's headings copyable, and give the agent a door onto the same document.

### Assumption Under Test

That the templates are *derivable from the runbook* — that writing them requires no new rule. If a template needs a convention the runbook does not carry, the runbook is incomplete and gets fixed there, not in the template.

### Test Stencil (Write This First)

```python
def test_templates_carry_their_contracted_headings(repo_root):
    """The headings are the contract (design § Section conventions)."""
    goal = (repo_root / "work/orchestration/goal-templates/goal.md").read_text()
    order = ["Status", "Question", "Consumer", "Answered when", "Invariants",
             "Grounding evidence", "Limits", "Reserved gates", "Close rule", "Amendments"]
    found = re.findall(r"^##\s+(.*)$", goal, re.M)
    assert [h for h in found if h in order] == order
```

### Changes Required

**See `design.md` for:** template home and why → D6; heading lists and entry shapes → `design.md#section-conventions`; skill form and why a skill not a command → D7.

- [x] `work/orchestration/goal-templates/goal.md` (NEW) — headings in the fixed order; `Limits` restates the four numbers explicitly (never inherited silently)
- [x] `work/orchestration/goal-templates/trail.md` (NEW) — `## Round N — <strategy-slug>` and the entry headings in occurrence order: `Strategy revision` · `T-00N scope` · `T-00N start` · `T-00N return` · `Checkpoint C-00N.rK` · `Round N result` · `Round N review` · `Stop`. Each with its named fields. Note in place: a `RetryCheck` is a `### T-00N start` under the same id, not a new entry kind; each checkpoint submission is a **new** `rK` entry, never an amendment (I4)
- [x] `work/orchestration/goal-templates/learnings.md` (NEW) — `## L-00N — <one-line claim>` with Evidence · Scope · Implication · Supersedes · Accepted by
- [x] `.claude/skills/run-goal/SKILL.md` (NEW) — frontmatter (`name`, `description` with triggers, `allowed-tools`, `user-invocable: true`), then the three roles, the four modes (`ground | round | checkpoint | review`), name the goal directory, then "go here" → `GOAL_RUNBOOK.md`, the templates, the ADR register. **Restates no rule** — the `run-study/SKILL.md` precedent

Shared conventions across all three templates: unwrapped prose, newest entry last, ISO dates, no entry edited in place, corrections as `### Amendment YYYY-MM-DD — amends <entry heading>`.

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/orchestration -q` → the heading test passes
- [x] `uv run python -c "import yaml,sys; print(yaml.safe_load(open('.claude/skills/run-goal/SKILL.md').read().split('---')[1]))"` → frontmatter parses

**Manual:**
- [x] Copy `trail.md` into a scratch directory and hand-write one round of the `20260823-magnet-technology-ab` study through it. Every field must have somewhere to go without invention
- [x] Confirm `SKILL.md` states no rule the runbook owns — the staged fix landed in `21c46dc5` and was verified against `staging/skill-edit-1.md` by the audit (2026-08-25). Note: the audit found the attached claim "the only such sentence in the file" does not hold — `SKILL.md:42` and `:46` still restate `GOAL_RUNBOOK.md:72` and `:35`. See `audit.md` § Plan completion.

**What We Know Works After This Phase:** the contract surfaces exist at their contracted paths; SC2's conventions are copyable.

**Commit.**

---

## Phase 4: Joined-row shape, made deliberate

**Grain:** ~1h. **First proof point.**

### Goal

Turn the accidental pass into a stated guarantee: extract the join logic to shared helpers, correct the docstring, and add a fixture test that goes red if append-as-update is undone.

### Assumption Under Test

That the existing set comparison really does guarantee the joined-row shape — and that this is provable by a fixture rather than asserted in prose. Spec `[HARD]`: "the accident becomes a stated guarantee."

### Test Stencil (Write This First)

```python
def test_a_joined_disposition_row_is_legal(tmp_path):
    """I8: a second row under an existing id is a disposition update, not a duplicate.
    Rewriting _ids_in_log to a list — the exact edit that kills append-as-update —
    turns this red."""
    rec = "| `20260823-x#1` | model | a finding |\n"
    log = (
        "| 2026-08-23 | `model` | `20260823-x#1` | sighting | open | `unrouted` |\n"
        "| 2026-08-25 | `model` | `20260823-x#1` | sighting | routed | `work/active/WI-040` |\n"
    )
    assert _ids_in_record(rec, "20260823-x") == _ids_in_log(log, "20260823-x")
```

### Changes Required

**See `design.md` for:** the split-by-subject rule → D9; what the extraction must preserve → `design.md#validation-approach` (first block); I8 (positional row kind) and I9 (six columns, order fixed).

- [x] `tests/study/test_records.py` — extract the join logic from `test_findings_join_the_discovery_log` (`:41-64`) into two module-level helpers, `_ids_in_record(text, prefix)` and `_ids_in_log(text, prefix)`. The existing test then calls them, unchanged in behaviour. **`_ids_in_log` keeps `line.split("|")[3]`** — the `Record` column at index 3 (I9)
- [x] `tests/study/test_records.py` — correct the docstring of `test_findings_join_the_discovery_log`: the set comparison guarantees the joined-row shape *by intent*, not by accident
- [x] `tests/study/test_records.py` — add the fixture test above, with a comment naming the obligation it guards. The disposition row **follows** its sighting in file order, because row kind is positional (I8), and the assertion is that multiplicity is *legal*, not merely tolerated

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/study -q` → full suite green, no regressions
- [x] **Red check:** temporarily rewrite `_ids_in_log`'s set comprehension to a list, rerun → the fixture test fails. Revert. Record the observed failure in Implementation Notes
- [x] `uv run ruff check tests/study` → no *new* findings (a pre-existing E501 at `tests/study/test_mechanical_failures.py:131` is not this item's; leave it)

**Manual:**
- [x] Confirm the fixture uses the same helpers the real test uses — no second parser (D9's whole reason)

**What We Know Works After This Phase:** append-as-update is a checked guarantee, before any prose says it is allowed.

**Commit.**

---

## Phase 5: The six edits across five homes

**Grain:** ~1.5h. **Gated on the re-check below.**

### Goal

Amend every home that forbids a joined disposition row, plus `CLAUDE.md:73`, with test 1 written red first.

### Assumption Under Test

That Item 6's pending runbook sentences and this item's edits are textually disjoint — on the *corrected* list of up to four protected sentences, not the spec's list of three.

### Step 0 — the re-check, before any edit

Item 6 runs concurrently in `.project/active/run-study-first-consumer/`. Finding ids are **study-scoped and both studies carry a `#10`**, so the protected set is up to four sentences, not three (`design.md#amendment-text-plan` § Room for Item 6).

- [x] Read `.project/active/run-study-first-consumer/plan.md` Phase 3 and Phase 4 **Implementation Notes** at `:309`, `:323`, `:335` — *not* Phase 4's § Changes Required at `:224-227`, which carries no runbook-sentence checkbox at all
- [x] Resolve each `#10` to its study:
  - study 1 (`20260821-power-cycle-ab`) `#10` — oracle operands emitted as a labelled artifact before verification; "the runbook sentence lands at Phase 4" (`:309`)
  - study 1 `#11` — study stores go beside the record directory, not inside it
  - study 2 (`20260823-magnet-technology-ab`) `#10` — re-run preflight whenever `axes.json` changes; home runbook step 6 (`:335`)
  - study 2 `#6` — export `case_id` in `points.csv`
- [x] Their homes are runbook steps 5/6/7/9 and the study-definition convention. This item touches step 14, the administrator paragraph, and § `DISCOVERY_LOG.md` — disjoint
- [x] `git log --oneline -- .claude/skills/run-study/runbook.md` — if Item 6 has landed any of the four, apply the edits below **around** the new sentences, never through them
- [x] If any edit below cannot be applied without displacing a landed Item 6 sentence: **stop and surface it** — do not resolve it silently in either direction (capture-fidelity law 4)

### Test Stencil (Write This First, Red)

```python
WRITER_HOMES = [
    (".claude/skills/run-study/runbook.md", r"sole writer of first-sighting rows",
     r"sole writer of the log"),
    (".claude/skills/run-study/runbook.md", r"not an administrator act", None),
    (".claude/skills/run-study/runbook.md", r"one row per finding \*sighting\*",
     r"one row per finding(?! sighting)"),
    # ... schema-table note, DISCOVERY_LOG.md header
]

@pytest.mark.parametrize("path,present,absent", WRITER_HOMES)
def test_writer_ownership_agrees(repo_root, path, present, absent):
    """SC4: the five homes agree on writer ownership and joined disposition rows."""
    text = (repo_root / path).read_text()
    assert re.search(present, text, re.I | re.S)
    if absent:
        assert not re.search(absent, text, re.I)   # negative lookahead, not bare substring
```

**The trap (review n1):** "One row per finding" is a prefix of its own replacement "One row per finding sighting". A bare-substring absence check passes forever. Use a negative lookahead or match the whole retired clause.

### Changes Required

Exact replacement text. The runbook is hard-wrapped at ~90 columns — **match the surrounding wrap**; `DISCOVERY_LOG.md` and `CLAUDE.md` are unwrapped.

**Edit 1 — `.claude/skills/run-study/runbook.md:221` (step 14).**

Replace: `The executor is the sole writer of the log.`

With:

```text
The executor is the sole writer of first-sighting rows. A goal round may later
append a joined disposition row under the same `<study-id>#<n>` id; it never edits a
first-sighting row and never mints a new id (`work/orchestration/GOAL_RUNBOOK.md`).
```

- [x] Applied, wrap preserved

**Edit 2 — `runbook.md:270` (administrator).** Keep the existing sentence; append after it:

```text
The goal round's joined disposition append is not an administrator act — the
administrator stays read-only.
```

- [x] Applied

**Edit 3 — `runbook.md:291` (§ `DISCOVERY_LOG.md` prose).**

Replace: `one row per finding, never a second copy of the finding's account.`

With:

```text
one row per finding *sighting*, plus any joined disposition rows a goal round later
appends under the same id — never a second copy of the finding's account.
```

The "never a second copy of the account" rule is untouched: a disposition row carries a disposition, not a restatement.

- [x] Applied

**Edit 4 — `runbook.md:294-296` (schema table).** **No column change** (I9 — `tests/study/test_records.py:60` reads `Record` at index 3). Add one sentence directly under the table:

```text
A row is either a first sighting, written by the executor at step 14, or a joined
disposition update, written by a goal round. `Disposition` and `Home` carry that row's
own state; for an id with more than one row, the newest row is its current state — scan
for the id rather than stopping at the first row that matches.
```

- [x] Applied, table untouched

**Edit 5 — `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3` (header).** Rewrite the cardinality clause and the writer clause together, and fix the authority citation — the header today attributes the writer rule to "`runbook.md § DISCOVERY_LOG.md`", which carries no writer rule; the sentence is at step 14 (`:221`).

Replace the sentences after "newest row last." with:

```text
One row per finding sighting; a goal round may append joined disposition rows under the same id. The finding's account lives in its record's § 15 and is never copied here. `Record` joins to that section by the same `<study-id>#<n>` id. A study's executor is the sole writer of first-sighting rows (`.claude/skills/run-study/runbook.md` step 14); a goal round writes joined disposition rows and never mints an id (`work/orchestration/GOAL_RUNBOOK.md`); an administrator never appends.
```

- [x] Applied; **the six-column schema table below it is not touched**

**Edit 6 — `CLAUDE.md:73`.**

Replace: `**CRITICAL: Do not cross-reference between them.**`

With: `**CRITICAL: Do not cross-reference *state* between them.**` — keep the existing two sentences that follow ("Coding epics belong in `.project/backlog/`. Modeling epics belong in `work/backlog/`. Each system manages its own state."), then append:

```text
Each system is mutated only through its own operations. Reading across is permitted as evidence: a goal artifact under `work/orchestration/goals/` may cite a `.project/` artifact by path and digest (`<path>@<commit-sha>`), and the reverse. Citing is not mirroring — never copy or restate the other system's state. See `.project/adr/006-goal-evidence-seam.md`.
```

- [x] Applied

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/orchestration -q` → test 1 now green (it was red before the edits)
- [x] `uv run python -m pytest tests/study -q` → **full suite green**; in particular `test_findings_join_the_discovery_log` and `test_record_is_closed` unaffected by the header rewrite
- [x] `grep -c '^|' exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` → row count unchanged (no rows added or removed by this item)

**Manual:**
- [x] Diff the runbook: exactly three prose edits plus one added sentence under the table, nothing else
- [x] Confirm none of the four protected Item 6 sentences is pre-empted or contradicted
- [x] Read `CLAUDE.md` §  Project Management — Two Systems end to end: does the permission read as a permission, and does the prohibition still prohibit mirroring?
- [x] Confirm the discovery-log schema table still has six columns in order: `Date | Kind | Record | Finding | Disposition | Home` (I9)

**What We Know Works After This Phase:** SC4 — the five homes agree; a goal round can legally append a disposition row without contradicting any live instruction.

**Commit.**

---

## Phase 6: The remaining contract tests

**Grain:** ~1.5h.

### Goal

Finish `tests/orchestration/test_goal_contract.py` — tests 2 through 5 — so the surfaces cannot drift apart silently.

### Assumption Under Test

That drift is detectable at the lightweight-consistency altitude without the tests becoming string-matching noise that fails on any reword (`design.md#potential-risks`, last bullet).

### Test Stencil (Write This First)

```python
def test_the_hardening_boundary_is_stated_and_not_crossed(repo_root):
    """SC6, document half: the docs must not instruct the barred act.
    This cannot check runtime behaviour and does not claim to."""
    for rel in [RUNBOOK, *TEMPLATES]:
        text = (repo_root / rel).read_text()
        for verb in [r"match\w*", r"compar\w+", r"recomput\w+", r"verif\w+"]:
            for hit in re.finditer(rf"{verb}[^.]{{0,60}}digest", text, re.I):
                assert "barred" in hit.group(0).lower() or _names_the_bar(text, hit)
    assert re.search(r"digests are read by people", (repo_root / RUNBOOK).read_text(), re.I)
```

### Changes Required

**See `design.md#validation-approach`** for all five tests; tests 1 and 3 already landed in Phases 5 and 1.

- [x] Test 2 — *the contract surfaces exist and carry their headings*: the three templates at their contracted paths with contracted top-level headings in order (extended from Phase 3's stencil to all three); `GOAL_RUNBOOK.md` names every stage; `run-goal/SKILL.md` frontmatter parses and points at the runbook
- [x] Test 4 — *the amendments are live*: `CLAUDE.md` carries the amended cross-reference sentence and cites record 006; record 006 names `CLAUDE.md`
- [x] Test 5 — *the hardening boundary is stated and not crossed in prose*: the stencil above. `GOAL_RUNBOOK.md` and the three templates carry I6's and I13's sentences and contain no instruction that compares or recomputes a digest
- [x] Every assertion gets a comment naming the obligation it guards (risk mitigation), and asserts on the **load-bearing phrase only**, with a whole-clause or lookahead match rather than a bare substring

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/orchestration -q` → all five tests green
- [x] `uv run python -m pytest tests/study -q` → green
- [x] `uv run ruff check tests/orchestration` → clean

**Manual:**
- [x] Reword one non-load-bearing sentence in `GOAL_RUNBOOK.md` and rerun: the tests must **not** fail. Revert. This is the noise check
- [x] Confirm test 5's docstring states plainly what it cannot check — the runtime half is manual verification, not a test (review M1). No test may imply otherwise

**What We Know Works After This Phase:** the five surfaces are guarded against silent drift at the stated altitude.

**Commit.**

---

## Phase 7: Validation — every success criterion to a concrete check

**Grain:** ~1h. No new artifacts; this phase is the gate before the item is called done.

### Goal

Walk each spec success criterion to a named check and record the result. Nothing is called done on a self-certification.

### Assumption Under Test

That the item as built actually satisfies the criteria as written — and, specifically, that a stranger can operate the runbook. The last one only Item 4 truly tests; treat any finding it raises as an **Item 1 defect**, not an Item 4 one (`design.md#potential-risks`).

### The mapping

| # | Spec success criterion | Concrete check |
|---|---|---|
| SC1 | Architecture decisions live, provenance-graded, cited by the runbook and affected guidance | Phase 1 register test (I12, every `grade` present) + Phase 6 test 4 (`CLAUDE.md` ↔ record 006) + manual: `GOAL_RUNBOOK.md` cites all seven records |
| SC2 | Three lean files and conventions sufficient to derive goal state without copying native stage state | Phase 3/6 heading tests + manual: answer "is round N open?" from `trail.md` headings alone (I15); walk the `20260823-magnet-technology-ab` study through the templates on paper |
| SC3 | Pre-execution checkpoint and `RoundReview` have distinct timing and responsibilities | Manual: the runbook's one table shows both, side by side, differing in timing *and* responsibility; Phase 6 test 2 asserts the runbook names both stages |
| SC4 | Step 14, administrator section, and log header agree on writer ownership and joined rows | Phase 5 test 1 across five homes (present-clause + lookahead absent-clause) + Phase 4 joined-row fixture test |
| SC5 | `GOAL_RUNBOOK.md` describes the same artifacts, gates, returns, reviews for human and agent | Manual: no section splits into a human path and an agent path; `run-goal/SKILL.md` restates no rule and points at the runbook (Phase 6 test 2) |
| SC6 | Tests pass; no hardening-path mechanism enters the implementation | `uv run python -m pytest tests/study tests/orchestration` green + Phase 6 test 5 (documents do not instruct the barred act) + manual § Non-Goals walk. **The runtime half is manual verification, not a test** — stated, not claimed away |

### Changes Required

- [x] Run the full mapping; record each result in § Implementation Notes below
- [x] `uv run python -m pytest tests/study tests/orchestration -q` → green, counts recorded
- [x] `uv run ruff check tests/study tests/orchestration .project/scripts` → no new findings
- [x] Walk `design.md#non-goals` item by item and confirm none entered: no envelope files, no event ledger, no authority digests, no idempotency keys, no effect queries, no reconciliation operation, no denser per-stage trail events, no concurrent runs, no unattended dispatch, **no stale-authority guard**; no executable goal-agent code; no digest scheme for untracked evidence; nothing touched under `scripts/zotero_*`, research entry surfaces, or `knowledge/`; `exploration/phase_1a/ADR-001_csv-source-of-truth.md` unmoved
- [x] Manual verification per `design.md#validation-approach`: read `GOAL_RUNBOOK.md` cold against `handshake-lcoe-construction.md`; walk the `20260823-magnet-technology-ab` findings through the templates and confirm the disposition rows they would produce are legal under the amended homes; confirm the round-open question is answerable from headings alone
- [x] `git log --oneline` on the branch shows one commit per phase, nothing merged, nothing pushed

**Owner-held, not done here:** merge, push, and item close (Align ruling 2).

### Validation

**What We Know Works After This Phase:** every criterion has a named check with a recorded result, and the item is ready for `/_my_audit`.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Relevant here:

- `uv run python -m pytest tests/study` and `uv run python -m pytest tests/orchestration` are the two suites this item touches
- `tests/models` needs the SYSIDE env (`set -a; source ~/1cfe/agentic-mbse/.env; set +a`) and is **not** touched by this item
- `uv run ruff check <path>` — line length 100, `select = ["E", "F", "I", "W"]`
- A pre-existing `E501` at `tests/study/test_mechanical_failures.py:131` is not this item's; leave it

## Risk Management

**See `design.md#potential-risks` for the full analysis.**

**Phase-specific mitigations:**

- **Phase 1 — Item 2 files before the home settles.** One complete commit, then notify. Nothing else in that commit.
- **Phase 2 — the runbook is written by a builder and reads like one.** Write every section against one question a stranger would ask; hold to the four-question stencil; treat any Item 4 finding as an Item 1 defect.
- **Phase 4 — the fixture proves nothing if it has its own parser.** Extraction before fixture, and the fixture calls the extracted helpers.
- **Phase 5 — Item 6 lands its runbook sentences concurrently.** Step 0's re-check, on the corrected four-sentence list; surface rather than resolve if they collide.
- **Phase 6 — tests become string-matching noise.** Load-bearing phrase only, lookahead not substring, a comment per assertion, and the reword noise check.
- **Standing (B5) — external mutation is noticed only if a reader looks.** It is on two checklists (resume and `RoundReview`), it has its own stop kind, and its failure is pre-declared as the observed failure that promotes the guard. Being wrong produces a recorded promotion, not a silent wrong answer.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-08-25

**Actual Changes:**
- `tests/orchestration/conftest.py` (NEW) — one `repo_root` fixture. No `__init__.py`: `tests/study/` has none either, and pytest collects without it.
- `tests/orchestration/test_goal_contract.py` (NEW) — `test_register_is_coherent` only, written first and observed failing against the empty register before any record existed. Frontmatter is parsed with `split("---", 2)[1]` rather than the stencil's `split("---")[1]`, so a record whose body contains a `---` still parses.
- `.project/adr/README.md`, `template.md`, `INDEX.md` (NEW) — charter, the `AD-XXX` vs `ADR-NNN` separation, record form, grade vocabulary, filing procedure; index table plus the "Prior art, outside the register" entry for `exploration/phase_1a/ADR-001_csv-source-of-truth.md`.
- `.project/scripts/adr.sh` (NEW, executable) — `list`, `new <slug>`, `supersede <old> <new>`.
- `.project/adr/001-strategy-and-task.md` … `007-supersession.md` (NEW) — the seven records, grades copied verbatim from `goal-strategy-task-harness-design.md` § Recorded Rulings. `006` carries `amends: CLAUDE.md:73`; `004` carries `amends: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3`.

**Validation run:**
- `uv run python -m pytest tests/orchestration -q` → 1 passed (red before the records landed, green after).
- `uv run ruff check tests/orchestration` → clean.
- `uv run python -m pytest tests/study -q` → 231 passed, 43 skipped (untouched, confirmed green).
- `bash .project/scripts/adr.sh list` → prints the index; `new scratch-check` → mints `008-scratch-check.md` and an in-table index row; `supersede 001 008` → flips `001` to `status: superseded`, inserts a `> Superseded by …` pointer, sets `supersedes: 001` on the successor, and flips the index row. All scratch artifacts deleted and the index reverted before commit.

**Issues:**
- The first `new` appended its index row after the "Prior art" section rather than into the table. Fixed: the row is inserted after the last existing table row.
- `supersede` initially wrote `status: superseded by ADR-NNN`, which breaks the README's stated `accepted | superseded` vocabulary. Fixed: status becomes `superseded` and the successor pointer is a body line, so no frontmatter field is added beyond the design's six.

**Deviations:**
- **`005-review-topology.md` also records the pre-execution disposition checkpoint.** The Recorded Rulings row covers only the collapsed round critic. The checkpoint is `[OWNER 2026-08-25]` from `spec.md` and the epic's Product-Lens, and it is part of the review topology a reader of this record needs; filing the topology without it would contradict `GOAL_RUNBOOK.md` in Phase 2. It is written inline with its own owner grade and source, and the record's frontmatter grade stays the copied `[AGENT]` inference. Nothing was invented — the text is the spec's.
- `test_register_is_coherent` globs `*.md` and filters on the `NNN-slug` name pattern rather than the stencil's `[0-9][0-9][0-9]-*.md` glob, so `README.md`, `INDEX.md`, and `template.md` are excluded by an explicit rule a reader can see.

### Phase 2 Completion
**Completed:** 2026-08-25

**Actual Changes:**
- `work/orchestration/GOAL_RUNBOOK.md` (NEW, 246 lines, unwrapped prose) — the fourteen sections in the plan's order, ending in a table citing all seven ADR records by relative path.

**Validation run:**
- `uv run python -m pytest tests/orchestration -q` → 1 passed (Phase 6 adds the runbook assertions).
- Digest verb scan (`match|compar|recomput|verif` within 80 characters of "digest"): exactly one hit, and it is the sentence that *names* the bar — "No goal procedure compares a cited digest against a stored or computed one… barred until a real run shows this reading failing". No sentence instructs the act. The load-bearing phrase "Digests are read by people" is present for Phase 6 test 5.
- All seven ADR relative links resolve from `work/orchestration/`.
- Human/agent split scan (`the agent does` / `the human does` / `if you are an agent|human`): no hits. B4 holds — no section forks by operator kind.

**Cold read against the four-question stencil:** the six procedural sections (grounding, round open/close, running a task, the checkpoint, the fresh review, resuming) each answer *what do I do* and *who checks it*, and each carries an explicit **Write:** line. Three of them did **not** answer *where does it go* on the first pass — round open/close, running a task, and the fresh review all left `trail.md` implied by the heading names. Fixed in place: each now carries a **Where:** line, and the round section states the append-only and dated-amendment rule once, for all the entries that follow it.

**Reading against the referent (`handshake-lcoe-construction.md`):** the referent is a *run record* and this is a *procedure*, so the match is on density and explicitness rather than genre — no hedging, every rule cited to its record rather than restated, vocabularies fixed and used exactly. The closer structural precedent in the repo is `.claude/skills/run-study/runbook.md`, whose "states obligations, not decisions" framing and cite-don't-restate discipline this file follows deliberately; its opening paragraph says so.

**Issues:** none.

**Deviations:** none.

### Phase 3 Completion
**Completed (partial):** 2026-08-25 — templates done, `run-goal/SKILL.md` **BLOCKED**

**Actual Changes:**
- `work/orchestration/goal-templates/goal.md` (NEW) — the ten headings in the fixed order; `Limits` restates all four numbers explicitly.
- `work/orchestration/goal-templates/trail.md` (NEW) — `## Round N — <strategy-slug>` and the eight entry headings in occurrence order, each with its named fields. Carries the two notes in place: a retry is another `### T-00N start` under the same id, not a new entry kind; each checkpoint submission is a new `rK` entry, never an amendment.
- `work/orchestration/goal-templates/learnings.md` (NEW) — `## L-00N — <claim>` with Evidence · Scope · Implication · Supersedes · Accepted by.

**BLOCKED, staged for the orchestrator:** `.claude/skills/run-goal/SKILL.md` could not be written — writes under `.claude/` require an approval this non-interactive session cannot obtain, and the block fires on the literal `.claude` path component anywhere in the path, including inside a staging directory. The finished file is staged at `.project/active/goal-harness-contract/staging/dot-claude/skills/run-goal/SKILL.md` (the `dot-claude` name is the workaround, not the target). Frontmatter parses; it points at the runbook, the templates, and the register, and restates no rule.

**Assumption under test — held.** Every template heading came from the runbook; no template needed a convention the runbook does not carry.

### Phase 4 Completion
**Completed:** 2026-08-25

**Actual Changes:**
- `tests/study/test_records.py` — join logic extracted to module-level `_ids_in_record(text, prefix)` and `_ids_in_log(text, prefix)`; `test_findings_join_the_discovery_log` now calls them and is otherwise unchanged. `_ids_in_log` keeps `line.split("|")[3]` (I9).
- Docstrings corrected: the set comparison guarantees the joined-row shape **by intent**, and `_ids_in_log`'s docstring says plainly that returning a set is load-bearing.
- Added `test_a_joined_disposition_row_is_legal`, using the same helpers the real test uses — no second parser (D9).

**Validation run:**
- `uv run python -m pytest tests/study -q` → 232 passed, 43 skipped (was 231; +1 is the new test).
- `uv run ruff check tests/study` → only the pre-existing E501 at `test_mechanical_failures.py:131`. No new findings.

**Red-check observed:** rewriting `_ids_in_log`'s set comprehension to a list turns **three** tests red, not one — `test_a_joined_disposition_row_is_legal` plus `test_findings_join_the_discovery_log` for both committed records (`20260821-power-cycle-ab`, `20260823-magnet-technology-ab`). The real records already carry a repeated id under the Record column, so the guarantee is exercised by live data as well as by the fixture. Reverted; suite green again.

### Phase 5 Completion
**Completed:** 2026-08-25. Edits 1–4 and the `run-goal` skill were applied by the orchestrator (`17e61516`) because writes under `.claude/` are blocked in this session; edits 5 and 6 and all validation are this session's.

**Re-check result (Step 0):** Item 6 had landed **none** of the four pending runbook sentences. Newest commit touching `.claude/skills/run-study/runbook.md` at re-check was `ad2fb4ea` — Item 6 *Phase 1*, not Phase 4. Each `#10` resolved to its study: study 1 (`20260821-power-cycle-ab`) `#10` = oracle-emitted predicate operand, home steps 5/7; study 2 (`20260823-magnet-technology-ab`) `#10` = re-run preflight when `axes.json` changes, home step 6. With study 1 `#11` and study 2 `#6`, the protected homes are steps 5/6/7/9 and the study-definition convention. This item touched step 14, the administrator paragraph, and § `DISCOVERY_LOG.md`. **Disjoint — the collision stop did not fire.**

**Actual Changes:**
- Test 1 written first and observed red: 5 passed, **2 failed** — both log-header assertions — with the four runbook homes already green from the applied edits 1–4. Six parametrized cases across the five homes.
- Edit 5 applied: `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3`. Cardinality clause, writer clause, and the wrong authority citation fixed together — the header had attributed the writer rule to `runbook.md § DISCOVERY_LOG.md`, which carries no writer rule; it now cites step 14.
- Edit 6 applied: `CLAUDE.md:73`. `*state*` inserted, the two existing sentences kept, the permission paragraph appended citing `.project/adr/006-goal-evidence-seam.md`.

**Validation run:**
- `uv run python -m pytest tests/orchestration -q` → 7 passed (was 2 failed before the edits).
- `uv run python -m pytest tests/study -q` → 232 passed, 43 skipped. `test_findings_join_the_discovery_log` and `test_record_is_closed` unaffected by the header rewrite.
- `grep -c '^|' …/DISCOVERY_LOG.md` → **24**, unchanged. No rows added or removed.
- Both schema tables still carry six columns in order — `Date | Kind | Record | Finding | Disposition | Home` (`DISCOVERY_LOG.md:5`, `runbook.md:300`). I9 holds.
- `CLAUDE.md` § Project Management read end to end: the permission reads as a permission, and the prohibition still prohibits mirroring — the `*state*` narrowing plus "Citing is not mirroring — never copy or restate the other system's state."

**Deviations:** the phase was split across two sessions by the permission wall, so its work sits in two commits rather than one.

### Phase 6 Completion
**Completed:** 2026-08-25

**Actual Changes:** `tests/orchestration/test_goal_contract.py` — tests 2, 4, and 5, as seven test functions (two parametrized). Test 2 is split by subject: goal-template heading order, trail entry headings in occurrence order plus the two rules a writer breaks first (I8 retry-is-not-a-new-kind, I4 checkpoint-is-never-an-amendment), learnings entry shape, the eleven runbook stages, and the skill as a door. Every assertion carries a comment or a message naming the obligation it guards.

**Validation run:**
- `uv run python -m pytest tests/orchestration -q` → **24 passed**.
- `uv run python -m pytest tests/study -q` → 232 passed, 43 skipped.
- `uv run ruff check tests/orchestration` → clean (one E501 found and fixed by wrapping the parametrize tuple).

**Three mutation checks, run and reverted:**
1. **Noise check (required).** Reworded a non-load-bearing runbook sentence ("An honest empty round is a result." → a longer paraphrase). **24 passed** — the tests do not fire on a reword.
2. **Test 5 bites.** Injected "Before reusing a citation, recompute the digest and compare it to the recorded one." into the runbook → **1 failed**. The guard catches an instruction to perform the barred act.
3. **The n1 trap is closed.** Restored "One row per finding;" in the log header → **1 failed**. A bare substring check would have passed, because "One row per finding" is a prefix of its own replacement; the negative lookahead catches it.

**Deviation, recorded:** the design's test-5 sentence reads "`GOAL_RUNBOOK.md` **and the three templates** carry I6's and I13's sentences". Implemented per the plan's stencil instead, which asserts those sentences on the **runbook only** and applies the no-crossing scan to the runbook *and* the templates. Requiring the templates to carry I6 and I13 would put one rule in four homes, which is the duplication the whole design forbids and which test 2's own cite-don't-restate check works against. The plan's stencil is the narrower and consistent reading.

### Phase 7 Completion
**Completed:** 2026-08-25

**Suite counts:** `uv run python -m pytest tests/study tests/orchestration -q` → **256 passed, 43 skipped**. `uv run ruff check tests/study tests/orchestration .project/scripts` → only the pre-existing E501 at `tests/study/test_mechanical_failures.py:131`, which is WI-030's and untouched. `tests/models` not run: needs the SYSIDE env and is not touched by this item.

**SC mapping results:**

| # | Verdict | Evidence |
|---|---|---|
| SC1 | **Met** | Seven records live at `.project/adr/` with copied grades; `test_register_is_coherent` (I12, every `grade` present, every `amends` path resolving); `test_the_amendments_are_live` (CLAUDE.md ↔ record 006, both directions); `GOAL_RUNBOOK.md` § The decisions behind this cites all seven by relative path, all resolving |
| SC2 | **Met** | Three heading tests; the round-open question answered from `trail.md` headings alone — a heading-only walk over the template returns closed when the result entry is present and open when it is not (I15/D12), demonstrated in this session; the magnet study walked through the templates on paper, below |
| SC3 | **Met** | `GOAL_RUNBOOK.md` § The two checks are distinct — one table, six rows, differing in *when*, *over what*, *asks*, *reviewer*, *on failure*, and *loops?*; `test_the_runbook_names_every_stage` asserts both stages exist as sections |
| SC4 | **Met** | `test_writer_ownership_agrees` across six parametrized cases over the five homes, present-clause plus lookahead absent-clause; `test_a_joined_disposition_row_is_legal`; and the paper walk below |
| SC5 | **Met** | One document, no human/agent fork (grep for the agent does / the human does / if you are an agent-or-human: no hits); `test_the_skill_is_a_door_and_not_a_second_copy`. **One defect found and staged** — see below |
| SC6 | **Met, with the runtime half stated as manual** | 256 passed / 43 skipped; test 5 checks the documents do not instruct the barred act and its docstring says plainly it cannot check runtime behaviour; § Non-Goals walk below |

**Paper walk — the `20260823-magnet-technology-ab` study through the amended homes.** Record § 15 and the log both carry 11 ids for that study and they join. Took real row `#3` (no coil-thickness / radial-build / stress coupling, currently `unrouted`) and wrote the disposition row a goal round would append under `GOAL_RUNBOOK.md` § The discovery log, with `model fix — task T-004, round 2` as the disposition and a work-item path as the home. Appending it **keeps the join** — a legal disposition row. Changing its id to `#99` **breaks the join**, which is I7 doing its job: a goal round may append only under an id the record already carries, and never mints one.

**§ Non-Goals walk — none entered.** No task-envelope files, no event ledger, no authority digests, no idempotency keys, no effect queries, no reconciliation operation, no denser per-stage trail events, no concurrent runs, no unattended dispatch, **no stale-authority guard** — the runbook's only mention of that machinery is the sentence declaring it absent and on the hardening path. No executable goal-agent code (`adr.sh` is the register's filing helper, per D4). No digest scheme for untracked evidence — D8's "unpinned; no native digest" wording instead. Nothing touched under `scripts/zotero_*`, research entry surfaces, or `knowledge/` (confirmed by `git status` across all commits). `exploration/phase_1a/ADR-001_csv-source-of-truth.md` unmoved — its newest commit is still `56d9fb2f`, its original.

**Cold read of `GOAL_RUNBOOK.md` against `work/orchestration/handshake-lcoe-construction.md`.** The referent is a *run record* and this is a *procedure*, so the bar transfers as density and explicitness rather than genre: no hedging, fixed vocabularies used exactly, every rule cited to its record rather than restated. Each of the six procedural sections answers what to do, what to write, where it goes, and who checks it. The honest residual is the one the design already named as a risk — it was written by the agent that built the layer, and only Item 4's cold-grounding proof tests whether a stranger can actually run it. Any finding Item 4 raises against it is an **Item 1 defect**.

**One defect found by Phase 3's manual check, staged not applied.** `SKILL.md` closes § Three roles with "An agent never fills two of these roles for the same round" — a rule the runbook owns, stated twice. It is the only such sentence in the file. The one-line replacement is staged at `.project/active/goal-harness-contract/staging/skill-edit-1.md`; the plan box stays unchecked until it lands. Low severity: the rule is correct and an operator following it does the right thing; the cost is a second home that can drift.

**Amendment 2026-08-25 — amends the paragraph above.** The claim "it is the only such sentence in the file" is **wrong** and is withdrawn. The audit found two more restatements: `SKILL.md:42` restates `GOAL_RUNBOOK.md:72` (how to tell whether a round is open) and `SKILL.md:46` restates `GOAL_RUNBOOK.md:35` ("the headings are the contract"). The check behind the claim was `grep -nE 'must|never|always|at most|only when'`, which finds normative phrasing and cannot see a restatement written as description — so the check was weaker than the claim it was used to support. Both are corrected to pointers in `staging/skill-edit-2.md` (edits 2–3), and the same correction is noted in `staging/skill-edit-1.md`. The lesson is the check, not the sentences: a restatement check has to be a read, not a keyword grep.

**Branch state:** one commit per phase — `f83a9742` (Phase 1 accepted), `586f3568` (Phase 2), `488f1d8d` (Phase 3 templates), `d36d4b0d` (Phase 4), `17e61516` (Phase 3 skill + Phase 5 edits 1–4). Nothing merged, nothing pushed. Merge, push, and item close stay owner-held (Align ruling 2).


### Audit-fix hop — 2026-08-25

Every audit finding dispositioned APPLY by the orchestrator (`a317e103`). Resolution block with authority bases appended at `product-lens.md`; **gate now CLEAR**.

**`audit-F1`** — ADR-005 frontmatter and `INDEX.md:11` now write the split grade (`[AGENT]` topology, owner may override; `[OWNER 2026-08-25]` checkpoint placement), per `README.md:45`. The body already carried the owner half; these are the two scanning surfaces.

**`audit-F2`** — `GOAL_RUNBOOK.md` gains § What "fresh" means: the owner's rule quoted at verbatim strength ("The critic is never the author's session", `goal-driven-model-development-harness.md:47`), stated as a *session* boundary rather than a work boundary; who obtains the reviewer on each path; and the agent's defined move when it cannot start one — a `### Stop` of kind `handoff` whose entry shape is given literally. Both gates now point there and both say what an agent does instead of proceeding. `handoff` joins the trail template's stop-kind vocabulary. No dispatch: building a way to start a session is the barred mechanism (ADR-003), and the prose handoff is the lean answer. `SKILL.md`'s overclaim is staged.

**Smaller findings, all applied:** three uncited runbook pointers (the `run-study` runbook by path at the seams table; a *pin* gloss with a pointer to where the study layer owns the term; the integration pattern rewritten to the honest form — no written pattern exists, so it is a `PREREQUISITE` return until epic Item 3). Two dead § Affected seams cross-refs now cite "The fresh review". `adr.sh:28` and `template.md:5` default to `[GRADE — copy from source]`. `INDEX.md`'s prior-art paragraph gains the loose-`ADR-00X` sentence. `audit-F3`: `CLAUDE.md` § Project Structure gains an `adr/` row, `modeling_project/ARCHITECTURE.md` gains a § Scope sentence. `SKILL.md:42`/`:46` staged as pointers, and the "only such sentence" over-claim corrected by a dated amendment above.

**Suites:** `uv run python -m pytest tests/study tests/orchestration -q` → **258 passed, 43 skipped** (was 256; +1 the new stage assertion, +1 `test_fresh_is_defined_at_owner_strength_with_an_agent_move`). `ruff check tests/orchestration` clean. **No test expectation was adjusted for old wording** — `test_writer_ownership_agrees` and `test_the_skill_is_a_door_and_not_a_second_copy` passed unchanged through every edit. One regex was widened at authoring time only (`session\W{0,2} boundary`), because the runbook italicises *session*.

**Two guards added beyond the brief.** `test_fresh_is_defined_at_owner_strength_with_an_agent_move` makes `audit-F2` a checked fact rather than prose that can quietly regress. And `test_register_is_coherent` now rejects the grade placeholder itself, so "cannot be left as-is" is mechanical rather than a hope — verified by minting a record from the template and observing it go red, then reverting.

**Two notes for the reader.** The prior-art sentence went into `INDEX.md`, not `README.md` — the "Prior art, outside the register" paragraph the audit meant lives there, and that is where a reader hits it. And `SKILL.md` edits are staged at `staging/skill-edit-2.md` rather than applied: writes under `.claude/` remain blocked in this session.

---

**Status**: Complete (2026-08-25) — audited, findings applied, product-lens gate CLEAR
**Next Step**: apply `staging/skill-edit-2.md`, then `/_my_close`. Merge, push, and item close stay owner-held.
