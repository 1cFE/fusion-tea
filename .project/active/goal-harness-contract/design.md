# Design: Lean Goal Contract and Operator Runbook

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-25
**Updated:** 2026-08-25
**Branch:** `feat/run-study-first-consumer` @ `3cb2a125`
**Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` — Item 1
**Spec:** `.project/active/goal-harness-contract/spec.md`

## Overview

Put the approved goal layer on disk as four things: a decision register that gives the seven approved rulings a home, three prose templates plus a shared operator runbook that a human and an agent both work from, the six edits that make the discovery log admit joined disposition rows, and a small set of tests that stop those surfaces from drifting apart.

## Related Artifacts

- **Spec:** `.project/active/goal-harness-contract/spec.md` — the contract; provenance grades load-bearing
- **Align:** `.project/active/goal-harness-contract/align.md` — owner rulings, 2026-08-25
- **Product-lens:** `.project/active/goal-harness-contract/product-lens.md`
- **Spec review:** `.project/active/goal-harness-contract/spec-review.md`
- **Required Reading (background, not re-derived here):** `.project/concepts/goal-strategy-task-harness-design.md`; its two reviews § Resolutions; `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words and Success Criteria; `work/orchestration/handshake-lcoe-construction.md` (`[REFERENT]` prose bar); `CLAUDE.md`; `.claude/skills/run-study/runbook.md` and `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header
- **Decision records:** `.project/adr/INDEX.md` does not exist. Creating it is this item's first deliverable, so the setup skim found nothing to contradict.

## The Point

Item 1 puts the goal layer on disk so someone who did not build it can operate it.

The owner's words are the bar: `[OWNER-VERBATIM]` "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human," run by an operator who `[OWNER-VERBATIM]` "shouldn't have to be me (who built this and therefore is mostly familiar)" (`.project/concepts/goal-driven-model-development-harness.md` § Owner's Words). That ladders up to the epic's critical success factor — a non-builder resumes and completes a real goal round from the goal directory and native records alone, every touched study finding dispositioned, no completed native work repeated.

Concretely this item owes four obligations. The seven approved decisions become live records with their recorded grades intact, and the live project guidance one of them contradicts (`CLAUDE.md:73`) gets amended. The three lean files get conventions detailed enough that current goal state is derivable without mirroring native stage state. The five textual homes that still forbid a goal round from appending a disposition row get amended so that no touched finding is left `unrouted`. And one shared `GOAL_RUNBOOK.md` describes the same artifacts, gates, returns, and reviews whether a human or an agent operates the loop. All of it under the owner's lean-first rule: no hardening mechanism without a recorded observed failure of the prose-and-native-facts route.

Everything after this item reads it. Items 4–6 test the cold grounding, the resume, and the closure against exactly these documents.

## Research Findings

**No ADR home exists, but the toolchain already expects one.** `.project/adr/` is absent, as is `.project/scripts/adr.sh`. The only script in `.project/scripts/` is `get-metadata.sh`. Yet the globally installed `/_my_design` command instructs every future design stage to skim `.project/adr/INDEX.md` at setup and to file records with `.project/scripts/adr.sh new <slug>` at acceptance, adding "If the script is missing, note the gap; don't hand-mint ids." Today that branch fires every time. The convention the repo is missing is one the tooling is already written against.

**The modeling register is scoped to models, not orchestration.** `modeling_project/ARCHITECTURE.md:3` states its own charter: "Structural decisions about how the domain is decomposed into model packages." AD-001–AD-007 are all SysML typing, library layout, and calc-def shape. The concept-design already checked and recorded the same finding (`goal-strategy-task-harness-design.md:215`: "modeling decisions AD-001–AD-007 contain no orchestration decision").

**One stray record exists in a third style.** `exploration/phase_1a/ADR-001_csv-source-of-truth.md` — YAML frontmatter (`status`/`date`/`deciders`), Context / Decision / Rationale / Consequences / Open. It is a good record and it already owns the id `ADR-001`.

**The run-study skill is the fusion-tea-owned precedent for an entry surface.** `.claude/skills/run-study/` is a real committed directory (SKILL.md + runbook.md + record-template.md); every other entry in `.claude/skills/` is a symlink into `~/1cfe/agentic-mbse`, and every file in `.claude/commands/` is agentic-mbse's. `SKILL.md` is deliberately thin — "This file is the entry point and nothing else. It captures intake, picks the mode, names the record path, and points onward."

**The discovery-log test parses by column index.** `tests/study/test_records.py:60` reads the `Record` column as `line.split("|")[3]`. Adding or reordering a column in the log's schema table would silently break the join. The same test compares *sets*, which is why a second row under an existing id passes today.

**The runbook edits do not collide with Item 6's pending findings.** Item 6 Phase 4 lands sentences for findings `#6` (export `case_id` in `points.csv`), `#10` (re-run preflight after any `axes.json` change), and `#11` (stores beside the record directory) — homes at runbook steps 6, 7/9, and the study-definition convention (`.project/active/run-study-first-consumer/plan.md:309,323`). This item touches step 14, the administrator section, and § `DISCOVERY_LOG.md`. Disjoint.

**The referent's prose shape.** `work/orchestration/handshake-lcoe-construction.md` is 49 unwrapped lines: a header naming the governing frame and pipeline, Align rulings as a numbered list, "Decision-carrying inputs, graded" with every bullet carrying an explicit `[OWNER]`/`[INHERITED]`/`[AGENT]` grade, owner gate rulings as their own dated section, and a reverse-chronological stage log where each entry is one dense dated paragraph. That is the bar for `GOAL_RUNBOOK.md` and the templates.

## Core Concept

The goal layer is a set of *documents with fixed shapes*, not a program. What makes a fresh operator able to run it is that every question they can have has exactly one place to look: what am I trying to answer (`goal.md`), what has happened (`trail.md`), what do we now know (`learnings.md`), how do I do the next thing (`GOAL_RUNBOOK.md`), and why is it this way (`.project/adr/`). Nothing is duplicated between them, so nothing can disagree.

The key insight is that the contract is enforced by *shape*, not by machinery. A task return is a heading with six named lines under it. A round result is a heading with seven. Because each entry has a fixed shape, a fresh reader knows immediately whether an entry is complete, and a test can check that the templates still carry that shape — without any of it becoming a control plane. The three prose files plus git give the whole thing replay: git supplies history, native artifacts supply truth, and the trail supplies only the judgment that lives nowhere else.

This is the right approach because the alternative was tried and ruled out. The owner's lean-first ruling (`[OWNER]` 2026-08-23) bars envelopes, ledgers, and idempotency machinery until prose is *observed* to fail. Templates and a runbook are the smallest thing that can be operated, reviewed, and proven wrong.

The design composes with existing pieces rather than paralleling them. `run-study` keeps the study contract and the discovery log — this item amends five sentences in it and adds nothing. The two PM systems keep their own state and operations — the goal layer cites them. `pytest` under `tests/` keeps drift detection, in the same doc-consistency style `tests/study/test_no_retired_identifiers.py` and `tests/study/test_record_template.py` already use. The only genuinely new surface is the ADR register, and it is new only because it does not exist yet.

## Key Bets

- **B1.** A fixed-shape prose entry is enough for a non-builder to reconstruct a round: what was authorized, what happened, what it meant, where each finding went. *If false → the resume and closure proofs (Items 4–6) fail, and the hardening path opens with a recorded failure. That is the designed outcome of being wrong, not a surprise — but the round trip costs Items 4–6.*
- **B2.** Freshness plus a written scope catches scope drift without preventing it. Nothing stops a same-round agent exceeding its recorded scope; the fresh reviewer sees it afterwards. *If false → drift lands silently in native artifacts and the goal layer records a fiction.*
- **B3.** An evidence-citation digest and the barred authority digest are different mechanisms that share a word. A citation digest is *read by a person*; an authority digest is *compared by a procedure to decide whether work is still authorized*. *If false → the Goal Evidence Seam record and the hardening bar genuinely collide, and D8's re-derivation has to go back to the owner.* See D8.
- **B4.** One document with two doors (skill for the agent, direct read for the human) keeps them on the same contract. *If false → the doors drift and the "same artifacts, gates, returns, reviews" criterion fails at exactly the seam it was written to protect.*

## Key Decisions

- **D1. The ADR home is `.project/adr/`, a register separate from `modeling_project/ARCHITECTURE.md`.** *Rejected: extending the `AD-XXX` convention in `ARCHITECTURE.md` — its stated charter is model-package decomposition, its seven entries are all SysML, and CLAUDE.md's two-system rule puts orchestration and tooling decisions on the coding-PM side. Also rejected: a goal-harness-specific register — the register is for repository decisions generally, and a third one-purpose home is what produced the stray.* The separation is deliberate and stated in the register's README: `modeling_project/ARCHITECTURE.md` owns model-architecture decisions (`AD-XXX`); `.project/adr/` owns repository, orchestration, and tooling decisions (`ADR-NNN`).

- **D2. Record form: one file per decision, `.project/adr/NNN-<slug>.md`, plus `INDEX.md`.** Frontmatter `status` / `date` / `deciders` / `grade` / `supersedes`, then Context, Decision, Rationale, Rejected alternatives, Affected seams, Consequences. This is the stray record's shape plus a `grade` field for capture-fidelity provenance and an explicit rejected-alternatives heading, because the seven candidates already carry both. *Rejected: a single append-only `DECISIONS.md` — seven records at ~60 lines each is a file no one reads, and per-file records give each decision a citable path for the runbook and CLAUDE.md to name.*

- **D3. The stray `ADR-001` is not renumbered or moved.** `INDEX.md` lists it under "Prior art, outside the register" with a one-line note. *Rejected: renumbering it, or starting the register at ADR-002 — the first breaks its inbound citations for cosmetic tidiness and is outside this item's scope; the second leaves an unexplained hole.* Ids are register-scoped, and the register's own test asserts no two *register* files claim the same id.

- **D4. A minimal `.project/scripts/adr.sh` ships with the register (`new`, `supersede`, `list`).** *Rejected: README-procedure only.* The globally installed `/_my_design` command tells every future design stage not to hand-mint ids when the script is missing — so a register with no script is a register nothing will file into. This is a judgment call past the spec's `[INFERRED]` list of deliverables ("records, conventions, documentation, templates, and the consistency tests"), taken because the epic's own Current State names the missing "filing mechanism", and recorded here rather than buried. The script mints the next id, copies the template, and appends the index row; roughly 40 lines of `bash`, no logic beyond that. It is not goal-agent code.

- **D5. The ADR home is the first deliverable, landing in its own commit before any other work in this item.** Item 2 is running now in a parallel worktree and files into it "once it exists" (Align ruling 3). The commit carries `README.md`, `INDEX.md`, `adr.sh`, the template, and the seven records — a partial home is worse than none, because Item 2 would file against a convention that then changes.

- **D6. Templates are separate files at `work/orchestration/goal-templates/`, beside the runbook.** *Rejected: sections embedded in `GOAL_RUNBOOK.md` — a human copying a template should copy a file, not extract prose from a document. Also rejected: templates inside the skill (the run-study precedent) — here the runbook itself lives in `work/orchestration/`, and making a human operator reach into `.claude/` for their own working files puts agent configuration on the human path.*

- **D7. The goal-agent entry surface is a thin fusion-tea-owned skill, `.claude/skills/run-goal/SKILL.md`, that restates nothing and points at `GOAL_RUNBOOK.md`.** *Rejected: a slash command — every file in `.claude/commands/` is an agentic-mbse symlink; a fusion-tea command there is tool-owned territory and gets clobbered. Rejected: plain instructions with no entry surface — the agent then has no discoverable trigger, and the human and the agent enter through different doors.* One document, two doors: the skill captures intake, picks the mode, names the goal directory, and hands off. Same shape as `run-study/SKILL.md`.

- **D8. The evidence-citation digest is carried as `<path>@<commit-sha>`, and the `[INFERRED]` reconciliation is re-derived rather than surfaced.** Git already supplies a content digest for every repository artifact, so the owner's "by path and digest" term is satisfied with zero new mechanism. The re-derivation: the barred row is "immutable task envelope and **authority** digests… promote when unattended dispatch needs a stale-authority guard" (`goal-strategy-task-harness-design.md:186`) — a digest a *procedure compares* to decide whether work is still authorized. A citation digest is read by a person to see which version of an artifact was cited. Different function, same word; no genuine collision, so nothing is parked. **Invariant I6 keeps them apart**: no goal procedure compares a cited digest. If a later item wants that comparison, it is the barred mechanism and needs the owner.

- **D9. Consistency tests split by subject, not by owner.** The joined-row shape goes in `tests/study/test_records.py` beside the existing join test, reusing its `RECORDS` parametrization and parsing. The document-agreement tests go in a new `tests/orchestration/test_goal_contract.py`. *Rejected: one new file holding both — the joined-row assertions would duplicate `test_records.py`'s log parser, and two parsers of the same table is exactly the drift these tests exist to catch.*

- **D10. Numeric caps: 2 retries, 2 checkpoint revisions, 6 rounds.** See § Default limits for the grounding. *Rejected: 3/3/10 — larger caps mean a failing loop burns more before anyone sees it, and the referent run shows the smaller numbers are enough.*

## Architecture

Five surfaces, each with one job, joined only by citation.

```text
.project/adr/                     why the layer is shaped this way    (7 records + index)
work/orchestration/
├── GOAL_RUNBOOK.md               how to operate it                   (shared, one copy)
├── goal-templates/{goal,trail,learnings}.md
└── goals/{goal}/                 one live goal
    ├── goal.md    fixed          question, answer contract, limits, gates, evidence
    ├── trail.md   append-only    strategy, tasks, checkpoints, results, reviews
    └── learnings.md  append-only accepted cross-round meaning
.claude/skills/run-goal/SKILL.md  the agent's door onto GOAL_RUNBOOK.md
tests/orchestration/ + tests/study/test_records.py   drift detection
```

**Data flow, one round.** The operator and a goal agent co-develop `goal.md`; it stays `draft` until § Grounding evidence is non-empty, and a draft goal authorizes no task. A round opens with one `StrategyRevision` appended to `trail.md`. For each task: append the six-line scope, then the one-line write-ahead start, then do the work through the *native* workflow (which keeps its own stage records), then append the return with its six-value outcome and five decision fields. When a study reading produces proposed dispositions, a fresh non-author checkpoint reads them and the author revises through it before any semantic follow-up task starts. The round closes with a mandatory `RoundResult`, then a fresh `RoundReview` that accepts or corrects the learning delta, accounts for every touched discovery row, and either recommends owner-held closure or writes the next strategy.

**Integration points.** `trail.md` cites native artifacts by path or native id (`work/active/WI-0NN/…`, `exploration/<pkg>/studies/<study-id>/`, `.project/active/<item>/…@<sha>`) and never restates their content. A goal round's only *write* outside its own directory is the joined disposition row it appends to `exploration/<pkg>/studies/DISCOVERY_LOG.md`.

**The two checks are distinct and the runbook says so in one table.** The pre-execution disposition checkpoint runs *before* any semantic follow-up executes, over *the study reading and its proposed dispositions*. `RoundReview` runs *after* the round closes, over *the whole round* — scope, retry classification, touched-finding dispositions, learning delta, carry-forward — and it is where owner criterion 5's post-execution audit obligation lives: it accounts for every touched row and what changed.

## Required Invariants

- **I1.** A goal with an empty § Grounding evidence is `draft` and authorizes no task.
- **I2.** At most one task is active in `trail.md`; every successor carries its own six-line scope, written before work begins.
- **I3.** Every task with a write-ahead start has either a return or an interruption stop entry. An invocation with no return is an interruption, resolved by inspecting native artifacts as truth.
- **I4.** No prior `trail.md` or `learnings.md` entry is edited. Corrections are dated amendment entries.
- **I5.** Routine native stage progress appears only in native artifacts; goal entries cite rather than restate.
- **I6.** No goal procedure compares a cited digest. Digests are read by people. (The hardening boundary, made testable.)
- **I7.** Every discovery row a round's evidence touches carries a joined `<study-id>#<n>` disposition row; no touched row returns as `unrouted`.
- **I8.** A first-sighting row is never edited. A disposition update is delivered as an appended row under the same id. A row's kind is positional: for an id, the earliest row in file order is the sighting; later rows are disposition updates. No column marks it.
- **I9.** The discovery log's schema table keeps its six columns in order — `Date | Kind | Record | Finding | Disposition | Home`. `tests/study/test_records.py:60` reads `Record` by column index.
- **I10.** Every closed round has exactly one `RoundResult` and one `RoundReview` by a non-author.
- **I11.** Mechanical failures produce no learning.
- **I12.** Every register ADR id resolves to exactly one file under `.project/adr/`, and every file appears in `INDEX.md`.

## Component Overview

**`.project/adr/`** — the register. `README.md` states the charter, the separation from `modeling_project/ARCHITECTURE.md`, the record form, the grade vocabulary, and the procedure. `INDEX.md` is the one-line-per-record index the `/_my_design` setup skim reads, plus the "Prior art, outside the register" line for the stray. `template.md`. Records `001`–`007`, one per approved candidate, each carrying its recorded grade unchanged from `goal-strategy-task-harness-design.md` § Recorded Rulings: 001 strategy-and-task `[AGENT]` ratified by owner; 002 round-boundary `[OWNER]` purpose + `[AGENT]` mechanism; 003 lean-first-persistence `[OWNER]` 2026-08-23 + `[AGENT]` separate-`learnings.md` mechanism; 004 finding-disposition `[OWNER]` 2026-08-23; 005 review-topology `[AGENT]`, owner may override; 006 goal-evidence-seam `[OWNER]` 2026-08-23; 007 supersession, split into its `[AGENT]` task-as-authority half and its owner-ruled finding-obligation half. Record 006 names `CLAUDE.md:73` as the surface it amends. Filing, not re-deciding.

**`.project/scripts/adr.sh`** — `new <slug>` mints the next id, copies the template, appends the index row; `supersede <old> <new>` flips status and cross-links; `list` prints the index. No other logic.

**`work/orchestration/GOAL_RUNBOOK.md`** — the shared operator deliverable, written to the referent's bar. Sections: what the layer is and what it is not; the five surfaces and which question each answers; grounding a goal; opening a round; running one task (scope → write-ahead → native work → return); the disposition checkpoint; closing a round; the fresh review; resuming an interruption; the limits table; the native seams table, with `research` and `integrate` labelled **pending native repair** and naming the interim hand patterns (documented WI-031 hand pattern; current manual integration pattern) with the standing rule that a goal round may not silently absorb either repair. It cites the seven records and restates none of them.

**`work/orchestration/goal-templates/`** — `goal.md`, `trail.md`, `learnings.md`, each a copyable skeleton whose headings are the contract. See § Section conventions.

**`.claude/skills/run-goal/SKILL.md`** — frontmatter (name, description with triggers, `allowed-tools`, `user-invocable: true`), then: the three roles (operator; round agent; fresh reviewer), pick the mode (`ground | round | checkpoint | review`), name the goal directory, then "go here" → `GOAL_RUNBOOK.md`, the templates, the ADR register. Restates no rule.

**`tests/orchestration/test_goal_contract.py`** and the addition to `tests/study/test_records.py`. See § Validation Approach.

## Section conventions

Shared across all three files: unwrapped prose, newest entry last, ISO dates, no entry ever edited in place. A correction is `### Amendment YYYY-MM-DD — amends <entry heading>` stating what changed and why.

**`goal.md`** — fixed, revised rarely, headings in order: Status (`draft | grounded`) · Question · Consumer · Answered when · Invariants (package and comparison) · Grounding evidence · Limits · Reserved gates · Close rule · Amendments. `Limits` carries the four numbers (retry cap, checkpoint revision cap, round limit, and any time/iteration limit) so a fresh reader finds them without leaving the file; defaults come from the runbook and are restated here explicitly, never inherited silently.

**`trail.md`** — `## Round N — <strategy-slug>`, and under it these entry headings in the order they occur:

```text
### Strategy revision            approach · assumptions · abandonment conditions ·
                                 intended model increment · intended study question
### T-00N scope                  Objective · Why now · Scope · Inputs · Done when · Stop when
### T-00N start — YYYY-MM-DD     one line: task · native target · expected artifact
### T-00N return — YYYY-MM-DD    Outcome (one of six) · Evidence · Reading ·
                                 Decision: trigger · decision + reason · tier · decided by · what changed
### Checkpoint C-00N — YYYY-MM-DD   reviewer · reading reviewed · dispositions reviewed ·
                                 verdict PASS | REVISE · revision N of 2
### Round N result — YYYY-MM-DD  intent met/unmet · task sequence · last semantic outcome ·
                                 stop reason · evidence refs · learning delta · finding dispositions
### Round N review — YYYY-MM-DD  reviewer · PASS | FINDINGS | OWNER_GATE · the seven checks ·
                                 next: closure recommended | next strategy
### Stop — YYYY-MM-DD            kind (interruption | limit | cap | owner gate) · what is true on disk · what the owner must see
```

The six-value outcome vocabulary is `COMPLETE | BOUNDED_NEGATIVE | PREREQUISITE | STRATEGY_BLOCKER | OWNER_GATE | MECHANICAL_FAILURE`. Decision tier is `execution detail | reserved gate | premise surprise`; `what changed` resolves to paths, ids, commits, or `none`. A `RetryCheck` is not a new entry kind — it is a `### T-00N start` under the same task id, carrying the line "retry N of 2; task, inputs, scope, and meaning identical" and the operational correction.

**`learnings.md`** — `## L-00N — <one-line claim>`, fields: Evidence · Scope · Implication · Supersedes (`L-00M` or `none`) · Accepted by (round review + date). Appended only after a `RoundReview` accepts or corrects the proposed delta.

## Default limits

| Limit | Default | Grounding |
|---|---|---|
| Retry cap (`MECHANICAL_FAILURE` → `RetryCheck`) | **2 retries** (3 attempts) | Smallest cap that admits a genuine correct-and-retry plus one more. The referent run fired zero retries across nine implement gates (`handshake-lcoe-construction.md:46`); a third identical mechanical failure is a signal, not noise. |
| Checkpoint revision cap | **2 revisions** (3 submissions) | The referent's design cleared an independent review in one revise cycle, and its pre-execution study critique cleared in one ("PROCEED WITH CHANGES, all five changes applied"). Two leaves room for a second miss and then stops. |
| Round limit (general goals) | **6 rounds** | One round carries at most one pin and one study; six is roughly one epic's worth of evidence before the question itself should be re-grounded. Task-scoped goals declare none and stop on their rules. |
| Tasks per round | **none** | Already bounded by one pin, one study, and mandatory close after a valid reading. A second cap would be a mechanism with nothing to catch. |

Every default is restated in the goal's own `Limits` section; a goal may declare tighter or looser values, and the runbook says the declared value wins. **Hitting the checkpoint cap does not permit execution.** It writes `### Stop — kind: cap` in `trail.md`, naming the unresolved dispositions and what the owner must decide, and the round stops there. Hitting the retry cap ends the task as `MECHANICAL_FAILURE` past cap, which is a blocker.

## Amendment text plan

Six edits. Exact replacement text lands in the plan; these are the sentences and their shape.

1. **`runbook.md:221` (step 14).** "The executor is the sole writer of the log." → "The executor is the sole writer of first-sighting rows. A goal round may later append a joined disposition row under the same `<study-id>#<n>` id; it never edits a first-sighting row (`work/orchestration/GOAL_RUNBOOK.md`)."
2. **`runbook.md:270` (administrator).** Keep the existing sentence; append: "The goal round's joined disposition append is not an administrator act — the administrator stays read-only."
3. **`runbook.md:290-292` (§ `DISCOVERY_LOG.md` prose).** "one row per finding, never a second copy of the finding's account" → "one row per finding *sighting*, plus any joined disposition rows a goal round later appends under the same id — never a second copy of the finding's account." The "never a second copy of the account" rule is untouched: a disposition row carries a disposition, not a restatement.
4. **`runbook.md:294-296` (schema table).** **No column change** (I9). One sentence under the table: "A row is either a first sighting, written by the executor at step 14, or a joined disposition update, written by a goal round. `Disposition` and `Home` carry that row's own state; for an id with more than one row, the newest row is its current state."
5. **`DISCOVERY_LOG.md:3` (header).** Rewrite the cardinality clause and the writer clause together, and fix the authority citation — the header currently attributes the writer rule to "`runbook.md § DISCOVERY_LOG.md`", which carries no writer rule; the sentence is at step 14 (`:221`). New: "One row per finding sighting; a goal round may append joined disposition rows under the same id. The finding's account lives in its record's § 15 and is never copied here. `Record` joins to that section by the same `<study-id>#<n>` id. A study's executor is the sole writer of first-sighting rows (`.claude/skills/run-study/runbook.md` step 14); a goal round writes joined disposition rows (`work/orchestration/GOAL_RUNBOOK.md`); an administrator never appends."
6. **`CLAUDE.md:73`.** "**CRITICAL: Do not cross-reference between them.**" → "**CRITICAL: Do not cross-reference *state* between them.**" followed by the existing two sentences, then: "Each system is mutated only through its own operations. Reading across is permitted as evidence: a goal artifact under `work/orchestration/goals/` may cite a `.project/` artifact by path and digest (`<path>@<commit-sha>`), and the reverse. Citing is not mirroring — never copy or restate the other system's state. See `.project/adr/006-goal-evidence-seam.md`."

**Room for Item 6.** Findings `#6`, `#10`, `#11` land at runbook steps 6, 7/9, and the study-definition convention. Edits 1–4 touch step 14, the administrator section, and § `DISCOVERY_LOG.md` — disjoint, and none of the three pending sentences is pre-empted or contradicted. Implementation re-checks `plan.md:309,323` before editing, and if Item 6 has landed by then, applies these edits *around* the new sentences rather than through them.

## Non-Goals

- No control-plane mechanism: no task-envelope files, machine event ledger, authority digests, idempotency keys, effect queries, reconciliation operation, denser per-stage trail events, concurrent goal runs, or unattended dispatch. The hardening boundary is absolute for this item.
- No executable goal-agent code. `adr.sh` is a filing helper for the register, not goal-agent machinery (D4).
- No touching of `scripts/zotero_*`, research entry surfaces, or `knowledge/` registry files — Item 2 owns the research seam in a parallel worktree.
- No repair of the research or integration seams; the runbook labels both pending and names the interim hand patterns.
- No proving the contract works. That is Items 4–6, which read this.
- No renumbering or relocating `exploration/phase_1a/ADR-001_csv-source-of-truth.md`.

## Implementation Notes

- **Order matters once.** The ADR home is one commit, first, complete. Everything after it may be sequenced freely.
- **Do not add or reorder columns in the discovery log's schema table** — `tests/study/test_records.py:60` reads `Record` at index 3 (I9).
- **Re-read `.project/active/run-study-first-consumer/plan.md:309,323` immediately before editing the runbook** and confirm findings #6/#10/#11 are still pending or, if landed, edit around them.
- **Grades are copied, not re-derived.** Each of the seven records carries its grade verbatim from `goal-strategy-task-harness-design.md` § Recorded Rulings, including the two split grades (002, 003) and the split candidate (007).
- **The runbook cites; it does not restate.** Following `run-study/runbook.md`'s own discipline: where a rule lives in an ADR or in `goal.md`, the runbook names it and moves on.
- **Prose convention:** unwrapped paragraphs, matching the referent and the existing `work/orchestration/` files.
- Register template frontmatter shape:

```yaml
status: accepted            # accepted | superseded
date: 2026-08-25
deciders: [Reid W]
grade: "[OWNER] 2026-08-23"  # capture-fidelity grade, copied from source
supersedes: none
amends: CLAUDE.md:73         # or none
```

## Potential Risks

- **The runbook is written by a builder and reads like one.** The stated bar is a non-builder operator, and only Item 4 tests it. *Mitigation:* write every section against one question a stranger would ask, cite the referent's shape, and treat Item 4's finding as an Item 1 defect rather than an Item 4 one.
- **Item 2 files an ADR before the home settles.** *Mitigation:* D5 — one complete commit, then tell Item 2 it exists. Do not land a partial register.
- **The stray `ADR-001` confuses a reader.** *Mitigation:* it is named in `INDEX.md` under "Prior art, outside the register", so the ambiguity is stated where a reader will hit it.
- **Item 6 lands its runbook sentences concurrently and the edits conflict.** *Mitigation:* the re-check above; both sets are small and textually disjoint.
- **The consistency tests become string-matching noise that fails on any reword.** *Mitigation:* assert on the load-bearing phrase only (`joined`, `first-sighting`, `never edits`), not on whole sentences; each assertion carries a comment naming the obligation it guards.

## Integration Strategy

For goal-driven runs, `work/orchestration/goals/{goal}/` succeeds the flat orchestration-brief pattern rather than sitting beside it. Existing briefs (`handshake-lcoe-construction.md` and its siblings) stay where they are as historical evidence and as the prose referent; nothing is migrated. `run-study` is unchanged except for the five amended sentences; the executor's step-14 obligation is untouched in substance. Both PM systems are unchanged — CLAUDE.md gains a permission, not an operation. `/_my_design`'s ADR touch points start working for the first time, for every future item, not just this one.

## Validation Approach

Tests, at the lightweight-consistency altitude only.

**`tests/study/test_records.py`** — one added test plus a docstring correction on `test_findings_join_the_discovery_log`, which currently guarantees the joined-row shape by accident (set comparison) and will say so.

The rows carry no column marking a row's kind, and this design does not add one (I9). Kind is **positional**: for a given id, the first row in file order is the sighting, and every later row under that id is a disposition update. The added test asserts, per committed record: every id in the log for that record appears in the record's § 15 (the direction the existing set equality already covers, now stated as intent rather than incidence); every id has at least one row; where an id has more than one, the extra rows follow the first in file order and none of them is the earliest row for that id; and the log is globally newest-last by `Date`, so "the newest row for an id is its current state" is well-defined. This is the `[HARD]` coverage, deliberate rather than incidental.

**`tests/orchestration/test_goal_contract.py`** — four tests:
1. *Writer ownership agrees across the five homes.* A table of (path, phrase-that-must-be-present, phrase-that-must-be-absent) covering `runbook.md` step 14, the administrator paragraph, § `DISCOVERY_LOG.md` prose, the schema-table note, and the log header. Retired wording ("sole writer of the log", "One row per finding" as a bare phrase) must be gone everywhere.
2. *The contract surfaces exist and carry their headings.* The three templates exist at the contracted paths with their contracted top-level headings in order; `GOAL_RUNBOOK.md` names every stage; `run-goal/SKILL.md` frontmatter parses and points at the runbook.
3. *The register is coherent.* Every id in `.project/adr/INDEX.md` resolves to one file; every register file is indexed; every frontmatter carries a `grade`; every non-`none` `amends` path exists.
4. *The amendments are live.* `CLAUDE.md` carries the amended cross-reference sentence and cites record 006; record 006 names `CLAUDE.md`.

**Manual verification.** Read `GOAL_RUNBOOK.md` cold against `handshake-lcoe-construction.md` and check that every stage answers "what do I do, what do I write, where does it go, who checks it." Walk one historical round on paper — the `20260823-magnet-technology-ab` study and its findings — through the templates and confirm the disposition rows it would produce are legal under the amended homes.

**Success criteria mapping.** SC1 → ADR register + edit 6 + runbook citations. SC2 → § Section conventions + § Default limits. SC3 → the runbook's checkpoint-vs-review table. SC4 → the six edits + test 1. SC5 → `GOAL_RUNBOOK.md` + `run-goal/SKILL.md` (one document, two doors). SC6 → all tests green + § Non-Goals held, with I6 as the testable form of the hardening boundary.

## Next-Stage Handoff

**Fixed.** The five surfaces and their paths. `.project/adr/` as the register and its separation from `ARCHITECTURE.md`. The seven records and their copied grades. The section conventions and entry headings. The three caps (2 / 2 / 6). The six amendment edits and their sentences. The ADR home landing first, in one commit.

**Open for the plan.** Exact prose of `GOAL_RUNBOOK.md` and the three templates — the shape is fixed, the writing is the plan's work. The exact `adr.sh` implementation. Whether `tests/orchestration/` needs its own `conftest.py` (probably one `repo_root` fixture).

**De-risk first.** Write `GOAL_RUNBOOK.md` before the templates, not after. The templates are the runbook's headings made copyable; writing them first invites a document that describes the templates instead of the operation — which is the exact failure mode B1 and the owner's bar are aimed at.

---
Next Step: After approval → `/_my_plan`
