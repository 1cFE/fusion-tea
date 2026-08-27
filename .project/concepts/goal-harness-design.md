# Design: Goal Harness

**Status:** Proposed
**Owner:** Reid W
**Created:** 2026-08-23
**Input:** `.project/concepts/goal-driven-model-development-harness.md` (read-only). Governing frame for what a study records: `.project/concepts/study-driven-model-development.md`.

---

## Overview

The goal harness turns a question about the model base into rounds of work: run a study, read what it found, decide what to do about each finding, do it, check it landed, go again. One agent with judgment drives the rounds with continuous context. Everything that continuity depends on is written to a run directory on disk, so a different agent can pick the run up cold and the operator can replay every decision afterward.

The core insight is that every stage already exists and already produces the artifacts the loop needs. What is missing is an owner for two things: what happens to a finding after a study logs it, and where a run stands when the session is gone. The harness owns exactly those two and briefs the existing stages for everything else.

---

## Problem

The repo can run a study, change a model, regenerate the package, and research a topic. Each of those is a closed, documented procedure. Together they form a loop that has run once, by hand, over two days: a study found the model had no conductor-field limit and four values with no source; that became a model change and a research round; the research produced insights and two new sources; the package was regenerated; the study is waiting to resume. Every hop worked because the person who built the system read one artifact, decided, and started the next procedure, carrying the same message, "I need this," in a different shape each time.

Nothing owns the seam between procedures. The study files its findings and stops. The synthesis reads the study and stops. The modeling pipeline begins from a spec someone wrote; research begins from a topic someone typed. A finding is dispositioned once, in prose, and nothing checks later whether the disposition landed or whether the finding moved. The research step's last hop, bringing an outside document into the repo as something the model can cite, is a shell command and a hand-written index entry. And nothing records where a run stands: if the session ends mid-loop, the next session starts from memory.

The operator this serves did not build the repo and is not working from a pre-defined item. They have a question, expect most answers to end in "the model needs to change," and want the loop to run without them until a decision genuinely needs them.

---

## Goals

- Let an operator state a goal grounded against what the model base can actually answer, and run it without the builder present.
- Walk every finding a study produces to a verified model change or a recorded known gap, with the next step chosen at each point rather than a home assigned once.
- Bring outside information in as registered, citable sources through one operation, never through a hand-written index entry.
- Keep every run resumable from disk by a session that has never seen it.
- Put a critic between every judgment and the action it leads to, and keep the critic out of the author's session.
- Give the operator a ledger that replays every decision with its reason and its effect.
- Keep every stage runnable by hand with the same artifacts the harness uses.

## Non-Goals

- The coding pipeline and its orchestrator. They were the reference for two ideas (one judgment agent; files as memory) and nothing in this loop uses them.
- The study layer, the detectors, and the pairwise round-walk policy. The prior concept owns those; this harness runs whatever study a goal calls for.
- Insight supersession and impact propagation. Designed upstream; consumed when it lands.

---

## Design Principles

### 1. One owner per seam

The study owns what it records; the goal owns what happens to a finding after it is recorded. The modeling pipeline owns the model change; the goal owns deciding that the change is needed and checking that it landed. No two components write the same fact.

### 2. Files are the memory; sessions are disposable

Anything the next session needs is on disk before the current session moves on. State is derived from artifacts wherever it can be, so there is no second source of truth to drift; only what cannot be derived is written as state.

### 3. Brief the stage that exists

The harness never re-implements a study, a model change, or a research round. It starts a fresh session with a brief and reads the result, the way a lead hands a task to a colleague. If a stage cannot be briefed, the stage is fixed, not duplicated.

### 4. A finding is walked, not routed

Each finding carries its own history and a current state. The decision at each round is the next step and the reason, never a final destination. Research often comes first, and whether something can be modeled is usually what the research answers.

### 5. Author and critic are never the same session

Every artifact that carries a judgment (a reading, a decisions document, a research document, an execution outcome) is reviewed by a session that did not write it. The orchestrator acts only after reading both.

---

## Architectural Bets

- **A persistent orchestrator whose state is on disk.** Continuous context for judgment, file state for continuity. The alternative, a fresh session per iteration with no orchestrator, was rejected: the "which step next for this finding" call needs the whole run in view.
- **The finding is the unit of orchestration.** The queue is the set of open findings across the run, each with a history. The alternative, a per-round to-do list, loses the walk.
- **Reuse the existing synthesis as the reading.** The administrator already reads only the study folder and writes what it found and what it cannot support. The harness adds the goal-aware decisions document on top rather than replacing the synthesis with a goal-aware analysis.
- **Registration is one operation with the holdout check in code.** The alternative, keeping the index hand-written and adding a checklist, was rejected: it is the hop that broke every time.

---

## ADR Candidates

### The finding lifecycle is the unit of orchestration
- **Proposed decision:** A finding has one current state (`open`, `researching`, `modeling`, `regenerating`, `verifying`, `closed`, `known-gap`) and a history; the decisions document assigns the next step, never a final home.
- **Why it may need a record:** A future agent will reach for "route each finding to one of three homes" because the discovery log's `Home` column suggests it.
- **Affected seams:** study record §15, discovery log, goal ledger, the modeling and research briefs.
- **Provenance:** `[OWNER]` (2026-08-23: "those 3 outcomes should not be treated as perfectly parallel … run research, then decide if they can model something").
- **Alternative rejected:** one-shot routing to model / research / seam.

### Who writes a finding's state after the study logs it — **PARKED, owner ruling required**
- **Conflict:** the prior concept settled `[OWNER]` that the discovery log carries "finding → disposition → what changed, across rounds" (criterion 4); the runbook makes the executor its sole writer. A goal-side state store beside the log would give two readers two answers.
- **Option (a):** the log gains an append-only *transition* row type (same `<study-id>#<n>` id, written by the goal orchestrator); §15 `Home` becomes "first step"; finding state derives from the log. **Option (b):** the log is declared an index of first sightings; criterion 4 is amended; state derives from the goal ledger.
- **Affected seams:** runbook step 14, record §15, `DISCOVERY_LOG.md`, goal ledger.
- **Provenance:** `[AGENT]` recommendation for (a); decision `[OWNER]` pending.

### The round verdict drives the stops
- **Proposed decision:** Every round's decisions document opens with a verdict against the goal's "what answered means": `answered`, `not yet`, or `not answerable on this package`; the third is a premise surprise and stops the run.
- **Why it may need a record:** Without it a run ends on critic PASS and per-finding steps with no statement about the question.
- **Affected seams:** `goal.md`, `decisions.md`, stop rules.
- **Provenance:** `[INHERITED: goal-driven-model-development-harness.md` Key Concept 3]`.
- **Alternative rejected:** verdict only at run end.

---

## Core Model

### Goal (`goal.md`)
The operator's question, its consumer, what "answered" means, the kind (`task` or `general`), stop rules (`surprise`, `reserved-gate`, `checkpoint`, `blocker`, plus `time`/`iterations` for general), the reserved gates, and grounding evidence: package and manifest, candidate axes with their indicators, discovery-log rows and insights already touching the question. Names the research question (RQ-1..5 in `modeling_project/OVERVIEW.md`) it serves. Written in `ground` mode with the operator. Not responsible for any decision after the run starts.

### Run directory (`work/orchestration/goals/<goal>/`)
- `goal.md` — above.
- `trail.md` — the prose narrative: rulings, graded inputs, dated stage log. Inherits the stage-log variant of the existing orchestration briefs (e.g. `work/orchestration/handshake-lcoe-construction.md`), not the immutable no-log variant.
- `ledger.md` — one entry per decision: finding ids, critic finding, decision, reason, tier (`execution-detail` / `reserved-gate` / `premise-surprise`), decider, what changed (paths, ids, commits), and the session id of any stage it dispatched. The only writer of finding state in the run; open findings, parked gates, and live sessions are all derived from it.
- `rounds/<n>/` — `decisions.md`, `critic-*.md`, `briefs/`, `audit.md`. The synthesis is cited by path and digest from `decisions.md`.

### Orchestrator (`goal` skill: `SKILL.md`, `runbook.md`, templates)
Same shape as the run-study skill. Modes: `ground`, `run`, `resume`, `status`. `run` and `resume` execute the round loop; `status` derives where the run stands from the directory and must read a hand-run directory identically. It dispatches stages and reads results; it writes only into the run directory. Not responsible for executing a study, a model change, or a research round itself.

### Dispatch (`scripts/goal/dispatch.py`)
Starts a fresh headless session with a brief and a short non-interactive preamble (stop with questions; end with the artifact path), returns `{session_id, result, cost}`, and can resume a session by id. Logs raw output under the run directory. Mechanism only; no routing. Imports `exploration/concept_analysis/scripts/lib/claude.py` (`invoke_claude`, resume by session id, retry decision); not a copy.

### Round
1. **Study** — brief the run-study skill in execute mode. The step-4 ruling on any `no_constraint_response` axis is taken at `ground`: the goal file already carries candidate axes with their indicators, so the operator rules there and the brief carries the ruling. A dispatched study stops with questions only when it proposes an axis the goal did not pre-rule; that is the exception, not the path.
2. **Reading** — brief the run-study skill in administer mode; the synthesis is the reading. Unchanged.
3. **Decisions** — the orchestrator writes `decisions.md`. It opens with the round verdict against the goal (`answered` / `not yet` / `not answerable on this package`); then, for every open finding (new §15 rows plus carried ones), the next step and the reason, in the proposed-action shape with a Decision slot. Steps: `research`, `model`, `regenerate`, `known-gap`. One modeling item may carry several finding ids.
4. **Checkpoint critic** — a fresh session reviews synthesis and decisions together, emits the feedback schema; loop until PASS or the goal's cap.
5. **Execute** — per finding, dispatch the step's existing stage: `research` → `/research` in acquisition mode; `model` → `pm add-item` then the modeling pipeline; `regenerate` → the package regeneration and manifest re-pin; `known-gap` → ledger entry plus the caveat the next record carries.
6. **Audit critic** — a fresh session checks that each step *landed*: the claimed artifacts exist and the mechanical checks ran against them. Whether the finding *moved* is judged by the next round's reading on the new fingerprint, not here. Then ledger entries are written and the run continues or stops.

### Finding
Three states, derived from the ledger, plus the step in flight:
```text
open ──(research)──► open, now known enough? ──(model → regenerate)──► next reading: moved? ──yes──► closed
  │                        └─ not modelable / nothing found ─────────────────────────────────────► known-gap
  └──(model → regenerate, known enough already)──────────────────────────────┘ no ──► open (reopened)
```
`known-gap` is terminal with a reason and re-openable only by a later goal's decisions document. Regeneration and verification are package events recorded in the ledger, not finding states.

### Research stage
A fusion-tea-owned command wraps the upstream `/research` (a tool-owned symlink, never edited in place) and adds an acquisition mode: input is a research request (value or question, consumer finding id, gap kind, priority, where to look); protocol is search → triage (fetch-and-summarize is relevance-only, never content) → capture → register; output is the research document plus `research_output.json` (searched, found, captured, failed, queued). Registration is `scripts/register_source.py` (new), built on `process_local_pdf` and `append_source_index_entry` in `scripts/zotero_ingest.py` rather than a second writer: URL or PDF → extraction with saved raw artifact → `knowledge/sources/<slug>/` → index block with source URL, raw and extract hashes, and use-for text (the writer today writes no URL and leaves use-for blank) → manifest row carrying a content hash beside the Zotero key (a schema migration; rows are keyed on Zotero key only today). The holdout check runs before any write against a machine-readable blocklist derived from `PROTOCOL.md` § 3 (barred paths, titles, URLs); a path or title hit refuses and logs; a content hit (ARIES-CS design or cost data in the fetched text) queues the source for the operator with the matched rule, since bibliographic mentions are exempt and the principle needs a human. A research critic reviews provenance, holdout disclosures, paraphrase absence, and conflicts with existing insights. The approval gate stays.

### Critics and schemas
Feedback schema: `VERDICT: PASS | FINDINGS` then ≤3 `### F-N` blocks (Target, Category, Finding, Recommendation, Priority), adopted unchanged; Category names the artifact the fix lands in (`reading | decisions | research | execution`). Decision schema: `PA-N` rows (Category, Severity, Location, Finding, Proposed Fix, Decision, User Notes), repurposed from the review's small-fix list to the round's per-finding decisions: Decision takes the step vocabulary, User Notes carries the reason. Parsers: the proposed-action parser exists (`exploration/concept_analysis/scripts/lib/sources.py`); only a verdict-line parser exists for F-N, so a field parser is new. Lenses per critic: reading (faithful to the record; nothing unsupported), decisions (goal fit; step choice; evidence for "known enough to model"), research (above), audit (landed; moved). Backpressure before any stage is marked done: preflight gates, verification, family regression tests, parse check, trace audit, holdout blocklist.

---

## Prior Art

None relevant — `.project/adr/` does not exist (0 entries). Prior concepts: `study-driven-model-development.md` (record, detectors, log; built through Run-Study Items 1–5), `autonomous-source-acquisition.md` (the research step this stage lifts), `run-study-skill.md` and its design.

---

## Required Invariants

### Run directory
- Only mechanical conditions stop the loop (missing key, fingerprint mismatch, failed verification, barred source); an interpretive result is recorded and argued. *(inherited from the study policy)*
- Every stage deposits a fixed-name artifact; `status` derives the current stage from those artifacts and the ledger alone, for hand-run and dispatched directories alike. *(intended)*
- Every decision the orchestrator makes has a ledger entry before the next stage starts. *(intended)*
- Every stop has a ledger entry with its reason. *(intended)*

### Finding
- A finding's state is `open | closed | known-gap`, derived from ledger entries; nothing stores it. *(intended; pending the parked ADR on whether the log also carries transition rows)*
- `closed` requires a reading on a package whose fingerprint differs from the one that opened the finding, showing the indicator or verdict moved. *(intended)*
- `known-gap` requires a reason; from a research step it carries the negative result. *(intended)*

### Seams
- A study executor is the sole writer of the discovery log; the administrator reads only the record directory; no goal edits a record or the log. *(true today; preserved)*
- `decisions.md` references findings only by `<study-id>#<n>`. *(intended)*
- A research session never writes a source file by hand; every registered source carries URL, raw hash, extract hash, and a recorded holdout result. *(true in concept analysis today; intended for `/research`)*
- Registration refuses a blocklist path or title hit and logs it; a content hit is queued to the operator with the matched rule and nothing is written. *(intended)*
- A dispatched stage either ends with an artifact path or stops with questions; it never ends silently. *(adopted from the reference runner's preamble)*
- The critic's session id differs from the author's, and the orchestrator acts on an artifact only after a verdict for it exists in the round directory. *(intended)*

---

## How It Works

### The Item 6 trace, through the harness
Today: align prose → research doc → design table → two work items minted by hand → `/research` → hand ingest → regeneration → study waits. Through the harness: `ground` captures "what does an Nb3Sn arm need, and what resists it" with indicators on the magnet axes. Round 1 study runs; the executor stops at step 4 with the `no_constraint_response` ruling; the orchestrator raises the reserved gate, the operator rules, the study resumes and commits. Reading produces the synthesis. Decisions: `#peak-field` → `model` (known enough: the constraint form is in the paper); `#f_carnot`, `#vol_cold` → `research`; `#availability` → `known-gap` (out of this goal's scope, reason recorded). Critic passes on pass 2 (it asked for the evidence behind "known enough"). Execute: research round registers two sources via `register_source.py` and proposes insights; the model item runs spec → implement; regeneration and re-pin. Audit confirms the constraint id resolves and the two values now cite repo paths. Round 2 study runs on the new fingerprint; `#peak-field` verified moved → `closed`.

Further scenarios (resume after a dead session; a general goal at its limit; research that finds nothing) are in Appendix A.

---

## Edge Cases and Failure Modes

- **Critic never passes.** At the goal's cap the open findings are written to the ledger; the goal file says whether the orchestrator proceeds (execution detail) or stops (reserved gate).
- **Package regenerated under a run.** Each round records the package fingerprint; a round on a changed fingerprint re-grounds. Two goals on one package serialize at `regenerate`: the second waits or re-grounds.
- **Model change does not land.** The audit marks the step failed with the modeling item's own audit as evidence; retry count increments; past the cap, `blocker`.
- **Dispatched session dies mid-stage with side effects** (source captured, not registered). The research stage's output file lists captures; `resume` registers or discards them before anything else. The modeling pipeline's own state files carry its half-done state. The session id to resume is on the ledger entry that dispatched it.
- **Research surprises.** A contradiction with an existing insight goes to a reserved gate with both cited (supersession is not available). A holdout trip refuses registration, logs the URL and rule, and the stage continues; the refusal reaches the critic.
- **The study's own reviews.** Runbook step 12 has the executor deposit §14 review lenses, and step 4 already owes an external critique. One runbook sentence admits a critic-deposited lens; the record is immutable after step 15, so no transcription step exists.

---

## Vocabulary

- `goal`: the operator's grounded question and its stop rules; the outer loop.
- `finding`: a model gap a study recorded, with a state and a history.
- `step`: the next action for a finding (`research`, `model`, `regenerate`, `known-gap`).
- `known-gap`: a finding parked with a reason; re-openable only by a later goal.
- `critic`: a fresh session that reviews an artifact and emits the feedback schema.
- `ledger`: the replay log, one entry per decision; `trail`: the narrative log.

---

## System Confidence

**Boundary obligations.** The study guarantees a committed record with §15 filled; the goal assumes nothing outside it. The reading guarantees a synthesis citing only the record. Decisions guarantee every open finding has a next step and a reason. Each executed step guarantees an artifact path or a stop-with-questions. Registration guarantees a citable path, hashes, and a holdout result, or a logged refusal.

**Route agreement.** A stage run by hand and a stage run by dispatch must leave the same end state (same artifacts at the same paths, same ledger facts); `status` must read both identically. A finding closed by the harness and a finding closed by hand must satisfy the same `closed` invariant.

**Dangerous combinations, never exercised together.** Regeneration while a run has a dispatched study in flight. Resume onto a dead session that had captured but not registered a source. Two goals on one package. **Unowned proofs.** (1) The loop closes end-to-end on an operator-chosen goal with no hand step. (2) Resume mid-stage with side effects loses nothing and duplicates nothing. (3) Hand-run and dispatched stages are equivalent. No single component's tests establish these.

## Validation Strategy

- A fixture replay of the Item 6 trace must reach the same end state the hand run produced.
- Resume tests kill a run at each stage boundary and once mid-research; registration tests cover URL and PDF paths, hash fields, manifest keying, and holdout refusal.
- Full list in Appendix B.

---

## Next-Stage Handoff

**Settled here:**
- The cycle and its five kinds of work; nothing from the coding pipeline inside it.
- Finding lifecycle as the unit; walked, not routed; `known-gap` terminal with reason.
- Reading = existing synthesis; decisions document is the new artifact; checkpoint critic reviews both.
- Run directory = `goal.md`, `trail.md`, `ledger.md`, `rounds/<n>/`; finding state derived, never stored; step-4 rulings taken at `ground`.
- Research stage = a fusion-tea wrapper over `/research` with acquisition mode + `register_source.py` on the existing writer + holdout blocklist with operator queue; approval gate kept.
- Critic schemas from concept analysis: the feedback schema unchanged; the proposed-action row repurposed as the per-finding decision row.

**Spec/design detail still needed next:**
- `goal.md` template and the grounding prompt: which checks are computed (indicators per candidate axis group, log and insight lookups) and which are asked.
- `decisions.md` field list; ledger entry format and the state-derivation rules `status` applies.
- Dispatch preamble, per-stage brief templates, the research request shape, and the critic lens checklists.
- The blocklist derivation from `PROTOCOL.md` and the operator queue format.

**First risk to de-risk:**
- Can a dispatched run-study session execute the runbook to a committed record from a brief that carries pre-taken rulings, and stop cleanly when it meets an axis the goal did not pre-rule? `/_my_spike` with one study on the current package.

**Proof obligations:**
- End-to-end closure on an operator-chosen goal; resume mid-side-effect; hand-vs-dispatch equivalence. Each is an epic item with its own deliverable.

---

## Summary

The harness adds two owners the loop lacks, one for a finding's life after it is logged and one for a run's state after the session is gone, and briefs the existing stages for everything else. Findings are walked step by step with a critic at each judgment, research becomes a stage that ends in registered sources, and the run directory makes the whole thing resumable and replayable.

---

## Appendix A — Further scenarios

### Resume after a dead session
`resume` reads the run directory: `status` finds round 2's decisions present, critic verdict absent. The ledger entry that dispatched the critic carries its session id; dispatch resumes it. If it is dead, a new critic runs; the ledger records the restart. No completed stage re-runs.

### A general goal reaching its limit
"Find a magnet technology that lowers LCOE" with `iterations: 4`. Round 4 ends with two findings `researching`; the stop is logged as `limit`, the findings stay open in the run directory, and the trail says what a continuation would do first.

### Research that finds nothing
The research session returns `research_output.json` with zero captures and the queries tried; the critic confirms the search was adequate; decisions move the finding to `known-gap` with the negative result; a later goal touching the same value sees it at grounding.

## Appendix B — Validation details

- `dispatch.py --dry-run` prints the composed brief; a golden brief per stage is kept and diffed.
- A replay of the Item 6 trace as a fixture run: the harness must reach the same artifacts the hand run produced.
- A resume test that kills a run at each stage boundary and once mid-research, then resumes.
- `register_source.py` tests: URL and PDF paths, hash fields present, manifest row keyed on content hash, holdout blocklist refusal.
- Parser tests: the proposed-action parser is reused from concept analysis; the F-N field parser is new and gets its own tests.
- `status` derived from a hand-built run directory matches the expected stage.
