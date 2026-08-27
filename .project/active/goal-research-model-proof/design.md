# Design: GSTH Item 5 — Research-to-Model Round Proof

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-27
**Updated:** 2026-08-27
**Branch:** `feat/goal-research-model-proof` (at `147adf5b`)
**Complexity:** HIGH

---

## Overview

How one live goal round is structured, sessioned, evidenced, and kept honest so that a bounded modeling task discovers a source prerequisite by itself, a fresh critic binds before any follow-up executes, and the Item 2 research seam is invoked natively with whatever it returns routed as it stands.

## Related Artifacts

- **Spec (the contract):** `.project/active/goal-research-model-proof/spec.md` — revised 2026-08-27
- **Align (owner rulings, settled):** `.project/active/goal-research-model-proof/align.md`
- **Spec review:** `.project/active/goal-research-model-proof/spec-review.md`
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md@83d6fc6c` § Item 5
- **Operating contract, cited never restated:** `work/orchestration/GOAL_RUNBOOK.md@1d43dc5b`
- **Item 2 (the seam):** `.project/completed/20260827_goal-research-seam/`; `docs/research_seam_operator_guide.md@9637f1b7`; `scripts/research_seam.py`; `scripts/source_registry.py`; `.claude/commands/research-acquire.md`
- **Item 4 (the working pattern this extends):** `.project/completed/20260827_goal-cold-pickup-proof/` — `design.md` § The runs and their roles, `operator-notes.md` § Mechanism notes, `verification_record.md`
- **Decision records read:** ADR-001 (no forward task list), ADR-002 (one agent per round), ADR-003 (lean-first; the hardening bar), ADR-004 (joined disposition rows), ADR-005 (review topology), ADR-006 (goal cites `.project/` by path and digest), ADR-008 (source identity). No decision here contradicts one; no new record is filed.
- **The live need:** `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a` row `20260821-power-cycle-ab#3`; `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448` § 15; `knowledge/KNOWLEDGE.md@ffa5c54c` DI-008

## The Point

The goal layer exists to decide what to work on next and what evidence means, across the seam where a modeling attempt runs out of evidence and has to go get some. That sequence — a bounded model task hits a wall, a critic checks the reading before anyone acts on it, evidence is acquired through a tracked procedure, modeling resumes or the round closes honestly — has never run once. Item 4 proved the round machinery on manual seams. Item 2 proved the research seam against fixtures, offline. Nothing has joined them. `[INHERITED: epic § Item 5 Current State]`

The obligation is therefore not to build anything. It is to run the sequence once, on a real need the repository is actually waiting on — the stellarator's `p_pump` = 1.0 MW, roughly 100× below admissible helium-primary circulator figures, understating `rec_frac` in every arm of both committed A/B studies — and to come out the other side with a record an auditor can check against disk. `[OWNER 2026-08-27]`, `align.md:7-12`.

Two things make the run worth more than a demo. First, criticism sits *before* work compounds on a misread — `[OWNER-VERBATIM]` "Study > Analysis > Dispositions Plan / Critic looks at the analysis and plan and can push back on either/both" (`.project/concepts/goal-driven-model-development-harness.md:33`). A gate that has never bound is not evidence of anything. Second, honest outcomes are first-class: a queued source, a bounded negative, a strategy blocker, or a park at a reserved gate are all valid results, and the item is deliberately not built so that only the positive path can succeed. `[OWNER]`, spec § Problem.

## Research Findings

- **Item 4's session mechanism works and its two failure modes are known.** Cold sessions run as direct `claude -p --output-format stream-json --verbose`, teed outside the repository; `orchestrate-stage.sh` is wrong for them (it composes `/_my_<stage>` plus an orchestrator preamble, and its buffered output does not survive a kill) — `.project/completed/20260827_goal-cold-pickup-proof/operator-notes.md:48-58`. Any disk predicate against goal files must be date-anchored, because the trail template carries the literal placeholder `### T-001 return — YYYY-MM-DD` (same file, `:59-64`; harness error 08a). Fence sweeps run against tool-call *inputs*, not raw transcript text, because every brief embeds its own denial list.
- **`run-goal` has exactly the four modes this run needs** — `ground`, `round`, `checkpoint`, `review` (`.claude/skills/run-goal/SKILL.md:36-40`). The critic and the reviewer are separate modes, so neither needs an improvised prompt.
- **The seam's CLI is `open` → `log` → `register --run` → `close`, and the return class is computed from disk, not from what the agent says** (`docs/research_seam_operator_guide.md:116-156`). `queued[]` is fed both by refused registrations and by `log --failure`; a queued candidate suppresses the bounded negative (`:155`).
- **The request key is a hash of `question`, `consumer`, `gap_type`, and sorted `where_to_look`** (`:108`). `consumer` accepts a study finding as `<study-id>#<n>` (`:106`) — which is what R-D2 needs, since no work item exists at request time.
- **`knowledge/research/requests/` does not yet exist in the tree.** This run creates it, through the seam, as committed evidence (`:142`).
- **`GOAL_RUNBOOK.md` currently instructs a round to hand-write the research pattern.** Its `research` row reads "**pending native repair**" (`:256`) and its bullet routes to the WI-031 hand pattern (`:264`). That is stale as of Item 2 and it is a live hazard for this run — see Architecture § The stale runbook row.
- **DISCOVERY_LOG row `#3`'s Home column already says "re-sourcing is a separate modeling item; item not yet minted."** This is ambient repository evidence the round will read. It is not the same as the prerequisite — see B2 and the grounding guard.

## Core Concept

This item runs **one goal round on a real modeling question, under one strategy, as a sequence of bounded tasks — and the operator's job is to keep every input to that round about the model, never about the errand.**

The goal asks whether `p_pump` = 1.0 MW is defensible and what sourced value the model should carry. Its first task is a modeling objective: re-base `p_pump` from repository-native sources under the goal's invariants. When the task finds that the band's only strong authority is not in the repository, that is a `PREREQUISITE` return it discovered, not one anybody predicted. The reading of that return, plus the committed study evidence behind it, goes to a fresh critic before anything acts on it. Only then does the research seam get invoked, natively, with the discovery row as its consumer — and whatever class it returns is routed as it stands. If a source lands, a second modeling task advances a native work item; if a candidate queues, the round hands it to the owner and closes on that.

The key insight is that **the proof lives in what the run was never told.** Every mechanism here — the grounding guard, the brief fence, the pre-declared covering branch, the ordering predicates — exists to make one claim checkable from `git log` alone: the prerequisite emerged from the work rather than from the prompt. Nothing new is built. The goal layer's own five surfaces carry the run, the two Item 2 scripts do every write into `knowledge/`, the modeling PM mints and specs its own work item, and the item directory holds only briefs, transcripts, and records about the run.

## Key Bets

- **B1.** The repository does not contain an admissible, citable basis for a helium-primary circulator `p_pump` at the Stellaris scale, so a bounded modeling task honestly attempting to re-base the value runs out of evidence. *If false → T-001 returns `COMPLETE`, criterion 1 goes unmet and is owner-visible, and the item ships a smaller proof. R-B3 governs; no prerequisite is manufactured.*
- **B2.** Row `#3`'s ambient text tells a reader that re-sourcing is the shape of the work, but not which prerequisite blocks it, not that DI-008's strongest primary is un-ingested, and not whether the gap is satisfiable from what is already here. A task that establishes those itself has made a real discovery. *If false → the discovery is staged before the run and criterion 1's word "real" is hollow, whatever the trail says.*
- **B3.** A headless session with one committed brief carries a goal round's judgment faithfully enough that `trail.md` is the round's real record rather than a record of the harness. *If false → the run measures `claude -p`, not the contract. Item 4 is the standing evidence for this bet.*
- **B4.** The seam's four return classes cover what this need will actually produce, so the goal layer never has to invent or re-grade a class at the routing step. *If false → R-D3 is unsatisfiable as written, and the item stops at a surfaced contract gap rather than routing around it.*
- **B5.** One round is enough to reach every criterion the run can honestly reach, because the runbook bounds tasks per round at "none" — `model → research → model` is three tasks under one strategy, not three rounds (`GOAL_RUNBOOK.md:230`). *If false → the positive path needs a round 2 this item does not budget, and criterion 4 ships non-exercised under the declared covering branch.*

## Key Decisions

- **D1. The goal slug is `p-pump-basis`**, at `work/orchestration/goals/p-pump-basis/`. It names the model value in question, matching the shape of the closed `cryo-volume-basis` goal, and it says nothing about acquisition, sourcing, or research. *Rejected: `p-pump-resource` and anything containing "source" or "research" (smuggles the errand into the directory name, which every session reads first, R-A2a). The final wording of the goal's § Question is the owner's at gate (a); this decision fixes only the slug the operator proposes with it.*
- **D2. This item covers exactly round 1, and no round 2 is opened.** The goal itself declares the runbook's default round limit of 6, because it is a real goal that outlives this item — the item's bound is not the goal's limit. `model → PREREQUISITE → checkpoint → research → model` runs as T-001…T-003 under one strategy revision. The item ships when round 1 has a `### Round 1 result` and a fresh `### Round 1 review`, on any of the six close triggers. *Rejected: declaring a round limit of 1 in `goal.md` (cripples a real goal to suit a proof item's budget, and would make an honest continuation look like a limit breach). Rejected: opening round 2 to chase criterion 4 (the epic budgets 8h execute; the spec's floor already declares round 1 shippable).*
- **D3. The follow-up work item is carried to `spec-model` and stops there.** T-003's authorized ceiling, once the owner rules gate (b), is: `pm add-item` mints the item, and `/spec-model` writes its `spec.md` citing the registered source directly. Design, plan, implement, and every regeneration or pin are out — R-E4 already puts them in the `integrate` seam, and they do not fit the budget. Criterion 4's "advances the native work item under the same strategy" is met by a minted, specced item whose spec carries the new sourced basis and states the comparison-meaning reading. *Rejected: carrying through `/design-model` (needs SysML prototyping and validation; blows the budget and drags the item into Item 6's territory). Rejected: stopping at the mint (a bare backlog row advances nothing and cites no evidence).*
- **D4. One session carries the whole round, resumed across owner turns; only the critic and the reviewer are separate fresh sessions.** ADR-002 puts one agent on one round; Item 4 needed several only because a kill was staged. Owner rulings arrive as committed resume-turn briefs, exactly as they did in Item 4's grounding. *Rejected: a fresh session per task (breaks one-agent-per-round and re-pays the read-in cost three times for no measured gain).*
- **D5. At T-002 the operator overrides the runbook's stale `research` row with a committed ruling naming the native route.** The row still says "pending native repair" and its bullet routes to the WI-031 hand pattern; following it would violate R-D1 and criterion 3, and flipping it first would violate R-G3. So the T-002 resume brief states, as an operator ruling, that Item 2 shipped the native procedure at `docs/research_seam_operator_guide.md@9637f1b7` and that the runbook row is stale pending this item's own flip. It is delivered *after* T-001's return and after the checkpoint, so it stages nothing. *Rejected: flipping the runbook before the round (R-G3 — the flip must rest on the run). Rejected: letting the round follow the hand pattern (R-D1, criterion 3).*
- **D6. The covering branch is a committed file, `covering-branches.md`, whose commit is an ancestor of the strategy-revision commit.** *Rejected: a section inside `spec.md` (already committed, so its ancestry proves nothing about when the branches were declared relative to the round). Rejected: a trail entry (the trail is the round's record; the declaration is the item's, and it must predate the round opening).*
- **D7. The seam request's `consumer` is `20260821-power-cycle-ab#3`.** The discovery row is what is actually waiting, it exists at request time, and the work item does not — it is minted at T-003, after the gate. *Rejected: waiting to mint the WI first so the consumer could be `WI-0NN` (inverts the sequence the item exists to prove, and gate (b) has not been ruled at that point).*
- **D8. Seam class → goal outcome is a fixed reading, recorded once in `goal.md` § Invariants and applied by the round.** `REGISTERED` → `COMPLETE`. `OPERATOR_QUEUE` → `PREREQUISITE` (the evidence is not in the repository; a named candidate is queued for a person). `BOUNDED_NEGATIVE` → `BOUNDED_NEGATIVE`. `BLOCKER` → `MECHANICAL_FAILURE`, retryable within the cap, since the guide defines it as the seam failing rather than the search answering (`research_seam_operator_guide.md:166-168`). The seam's class is preserved verbatim in the trail alongside the mapping — the mapping is a reading of the return, never a re-grade of it (R-D3). *Rejected: leaving the mapping to the round agent in the moment (four classes × six outcomes is exactly where an honest queue gets quietly re-graded into a blocker).*

## Architecture

### The goal

`work/orchestration/goals/p-pump-basis/` — `goal.md`, `trail.md`, `learnings.md`, copied from `work/orchestration/goal-templates/`. All five field classes non-hollow at grounding (R-A3), all four limits restated with the runbook's default numbers (retry 2, checkpoint 2 revisions / 3 submissions, rounds 6, no time limit) per R-A5/R-C3a. § Invariants carries the `p_pump` → recirculating sum → `rec_frac`/`p_net` → `recirc_ok`/`net_positive`/LCOE channel and the equal-input/unequal-effect distinction, stopping short of any conclusion about whether comparison meaning survives (R-A6). § Reserved gates names gate (b) — any model or knowledge mutation beyond the goal directory — and gate (c) — the close ruling on a judgment call — plus merge, push, item close, archive. Every operator-side sentence is graded `[AGENT]`; only what the owner said at gate (a) is `[OWNER]`.

### The grounding guard

R-A2a's hazard is that the grounding exchange stages the discovery. The guard is a fence on the grounding brief and on `goal.md` itself.

**The grounding brief may contain:** the owner's question about the model value; the three grounding-evidence pointers by path and sha (`DISCOVERY_LOG.md@e891b23a` row `#3`, `record.md@881d4448` § 15, `KNOWLEDGE.md@ffa5c54c` DI-008); the invariant channel and the equal-input/unequal-effect distinction; the reserved gates; the limits; the consumer.

**The grounding brief may not contain:** the word "research", "acquire", "ingest", "register", or "source registration" as an instruction; the name Moscato, SOFT 2018, or WPBOP-CPR(18) 20276; any statement about DI-008's ingestion status; any reference to `research_seam.py`, `source_registry.py`, `/research-acquire`, or `docs/research_seam_operator_guide.md`; any phrasing of the question as an errand ("get the PDF", "find a source for") rather than as a value question.

**What the goal's § Question must look like**, at gate (a): a question about the model value — is `p_pump` = 1.0 MW defensible for a helium-primary loop at this plant scale, and what sourced value should the model carry? Final wording is the owner's.

**Surfaced honestly, not defended against.** Row `#3`'s Home column reads "re-sourcing is a separate modeling item; item not yet minted." It is grounding evidence R-A1 requires, so it cannot be withheld, and it does tell a reader that re-sourcing is the shape of the work. What it does not carry is the prerequisite's identity, DI-008's un-ingested primary, or whether the gap is satisfiable from what is already in the repository. `verification_record.md` states this ambient hint plainly and judges criterion 1 on whether T-001 actually did the work — searched repository-native sources for an admissible basis and returned a specific, evidenced gap — rather than on the absence of a hint that could not be removed.

### The round, as a task sequence

One `### Strategy revision`, no forward task list (ADR-001). Tasks are chosen from evidence in hand.

| Task | Objective | Expected outcome | What it may not say |
|---|---|---|---|
| T-001 | Re-base `p_pump` from repository-native sources under the goal's invariants | `PREREQUISITE` (B1), or `COMPLETE` if the repository answers it | Its scope names no research task and lists no prerequisite (R-B1, R-B2) |
| T-002 | Obtain an admissible `p_pump` basis through the `research` seam | Per D8's mapping | Runs only after the checkpoint passes (R-C1) |
| T-003 | Mint and spec the modeling work item on the registered basis | `COMPLETE`, or `PREREQUISITE` naming `integrate` (R-E4) | Runs only after the owner rules gate (b) (R-E2) |

Between T-001 and T-002 sits `### Checkpoint C-001.r1` — the reading (row `#3` and record § 15 and DI-008, together with T-001's return) plus the proposed research and model dispositions, handed to a fresh `run-goal checkpoint` session. Revisions are `r2`, `r3`; at the cap the round writes `### Stop` of kind `cap` and stops (R-C3).

The round can end before T-003 and still be complete. The likely shape, given DI-008's un-ingested primary, is T-002 returning `OPERATOR_QUEUE` → goal outcome `PREREQUISITE` → the queued candidate handed to the owner → round closes on trigger 4 (unresolved owner gate) or trigger 5.

### The stale runbook row

The round agent reads `GOAL_RUNBOOK.md` § The native seams, which today tells it the `research` seam is unrepaired and routes it to the WI-031 hand pattern (`:256`, `:264`). This is the one place the shipped contract actively points the run at the wrong route. D5 resolves it with an operator ruling in the T-002 brief. Two things follow.

It is a **measured prose failure** and it goes in `verification_record.md` § Failures as one: the runbook instructed a hand-write that Item 2 had already replaced, and only an operator ruling stopped it. Whether the round agent notices the staleness by itself *before* the ruling arrives is worth recording either way, from the T-001 return and the checkpoint transcript.

It is also the evidence R-G3 wants: the flip lands after the seam actually ran, so the runbook change rests on the run.

### Owner pause points

Three parks. Each is written where the layer natively keeps it, and the owner rules asynchronously by an operator resume turn whose brief is committed before the turn runs.

| Gate | Where the ask is written | Where the ruling lands |
|---|---|---|
| (a) the question and "answered when" | The grounding session's final message, kept as `sessions/01-grounding/output.md`. No trail exists yet; `goal.md` stays `draft` and authorizes no task. | Resume turn 02's brief; `goal.md` reaches `Status: grounded` |
| (b) minting or advancing the work item | `trail.md` `### Stop — <date>`, Kind `owner gate`, naming what the seam returned and what the owner must decide | The next resume turn's brief; T-003 scope follows, or the round closes |
| (c) the close ruling on a judgment call | `trail.md` `### Stop — <date>`, Kind `owner gate`, naming the judgment (R-E1 advance vs R-E3 `STRATEGY_BLOCKER`) | The resume turn's brief; `### Round 1 result` follows |

Two further stops are `handoff` kind, not owner gates: the round agent reaching the checkpoint and reaching the round review, neither of which it may perform itself (R-C5, R-F4).

Nothing about a gate is mirrored into the item directory. `freshness-record.md` cites the trail entry by heading and date.

### Sessions

Every cold session is a direct `claude -p --output-format stream-json --verbose` invocation, teed to `~/goal-proof-logs-item5/NN-<role>/` — outside the repository — never through `orchestrate-stage.sh` (Item 4, `operator-notes.md:53-58`). One committed `brief.md` per run, committed before the run; transcript and output copied into the item directory after.

| Run | Role | Session | Mode | Given | Produces |
|---|---|---|---|---|---|
| 01 | Grounding turn 1 | new | `run-goal ground` | the owner's value question, the three evidence pointers, the gates and limits | `goal.md` as far as it goes; the gate-(a) questions |
| 02 | Grounding turn 2 | 01, resumed | `run-goal ground` | the owner's answers | `Status: grounded` |
| 03 | Round agent, T-001 | new | `run-goal round` | the goal directory and the repository | strategy revision, T-001 scope/start/return, the reading and proposed dispositions, `### Stop` handoff |
| 04 | Checkpoint critic | new, fresh | `run-goal checkpoint` | the goal directory and the repository | `### Checkpoint C-001.r1`, verdict |
| 04b… | Critic re-submissions | new each time | `run-goal checkpoint` | as above | `C-001.r2`, `r3`, within the cap |
| 05 | Round agent, T-002 | 03, resumed | `run-goal round` | D5's operator ruling; the checkpoint verdict | T-002 scope/start/return; the seam run committed |
| 06 | Round agent, gate (b) turn | 03, resumed | `run-goal round` | the owner's ruling | T-003, or the close |
| 07 | Round agent, close | 03, resumed | `run-goal round` | the owner's gate-(c) ruling if needed | `### Round 1 result` |
| 08 | Round reviewer | new, fresh | `run-goal review` | the goal directory and the repository | `### Round 1 review`, the accepted learning delta |

Legality against ADR-002 and § What "fresh" means: session 03 authors the whole round, so it reviews nothing; sessions 04 and 08 authored no part of what they review. The grounding session authored `goal.md` but not the round; it is not reused as either reviewer.

Runs 04b and 06 are conditional. The freshness record enumerates whatever actually happened, kept and discarded, and closes with the completeness statement — these were all the runs there were, and no other input existed (Item 4's shape).

### The seam invocation

Request at `knowledge/research/requests/REQ-PPUMP-01.json`:

```json
{"request_id": "REQ-PPUMP-01",
 "question": "<the p_pump basis question, as the round words it>",
 "consumer": "20260821-power-cycle-ab#3",
 "gap_type": "unsourced_value",
 "priority": "P1",
 "where_to_look": ["EUROfusion IDM / WPBOP", "Fusion Engineering and Design", "SOFT 2018 proceedings"],
 "limits": {"max_searches": 4, "max_captures": 2}}
```

Then `/research-acquire` drives `open` → `log --search` / `log --candidate --triage` / `log --failure` → `register --run` → `close --adequacy`, per `docs/research_seam_operator_guide.md` §§ Forming a request, Running an invocation. Nothing here restates that procedure.

**The likely path, end to end.** The search names Moscato et al., SOFT 2018, WPBOP-CPR(18) 20276 as the strongest candidate. If the PDF is reachable and extracts, `register --run` writes the source directory, manifest row, and index block together and the return is `REGISTERED` — T-002 is `COMPLETE`, the round parks at gate (b), and on the owner's go T-003 mints and specs the work item citing the registered source directly (R-D5: a registered source is sufficient MR-4 basis; no DI is minted, which would itself be gate (b) material). If it is behind the IDM or a publisher wall, the agent records `log --failure <url> --reason "<the wall>"` with the default disposition, the candidate lands in `queued[]`, no bounded negative is written (`:155`), and the return is `OPERATOR_QUEUE`. T-002 then returns `PREREQUISITE` per D8, the queued candidate goes to the owner at the gate-(b) park with its reason, and the round closes on it. **It is not retried into a positive and not re-graded as a blocker** (R-D6).

Everything under `knowledge/research/requests/` — the request, the run record, the receipts, the return, any negative — is committed as evidence with the round (R-D4).

### Findings, closure, and the flip

Row `20260821-power-cycle-ab#3` gets a joined disposition row appended under the same id, with kind, status, responsible task, and what changed or the concrete next reference (R-F1, ADR-004). No `unrouted`. The first-sighting row is untouched and no id is minted. Rows `#1`, `#2`, `#5` are read; if the round's evidence touches one it gets its own joined row, and if not, the reasoning for leaving it is recorded where the reviewer can check it (Item 4's read-but-untouched pattern). Findings the round discovers itself are not log rows — they go to `learnings.md`, the work item, or an ADR, and the trail cites them (R-F2).

The `### Round 1 result` derives its stop reason from the last semantic outcome plus the goal's limits (R-F3). The fresh reviewer (run 08) accepts, corrects, or rejects the learning delta before it is appended to `learnings.md`, and that append happens in the reviewer's commit and nowhere else (R-F4).

**The runbook flip, after the seam-run commit** (R-G3). Four edits to `work/orchestration/GOAL_RUNBOOK.md`, all in § The native seams:

1. `:256` — the `research` row loses "— **pending native repair**"; its Native return column becomes the four classes (registered sources, a queued candidate, or a bounded negative). The goal-level question column is unchanged.
2. `:262` — "**Two seams are not repaired yet**" becomes one seam, naming `integrate`.
3. `:264` — the WI-031 hand-pattern bullet is replaced by a pointer to `docs/research_seam_operator_guide.md`, `scripts/research_seam.py`, `scripts/source_registry.py`, and `/research-acquire` (R-G2). Leaving it would tell the next round to hand-write what the seam now does.
4. `:267` — "The repairs have their own owners and their own failure contracts" is made singular (R-G4).

The `integrate` row at `:258` and its bullet at `:265` are not touched (R-G1). Ordering is checked by `git merge-base --is-ancestor <seam-run commit> <flip commit>`.

**R-A7a**, in the same neighbourhood but not the same commit: one sentence appended to `.project/CURRENT_WORK.md`'s Run-Study Item 6 Phase 4 next-up entry recording that the `p_pump` re-source has left that close list and now runs under `work/orchestration/goals/p-pump-basis/`, citing `align.md`. No modeling-PM or goal state is mirrored — a pointer only.

## The commit sequence

Ordering predicates an auditor checks with `git merge-base --is-ancestor`.

| # | Commits | Ordering it carries |
|---|---|---|
| 0 | Item scaffolding: `sessions/`, `covering-branches.md`, `freshness-record.md` and `verification_record.md` as skeletons | `covering-branches.md` complete here — **C-COVER** |
| 1 | Per grounding turn: brief, then transcript + output + `goal.md` state | brief before its run; last commit carries `Status: grounded` |
| 2 | Round-agent brief; then transcript, strategy revision, T-001 entries — **C-T001** | **C-COVER is an ancestor of C-T001** (R-H4) |
| 3 | Critic brief(s); then transcript(s) and each `### Checkpoint C-001.rK` | brief before its run; the checkpoint entry precedes any T-002 commit |
| 4 | T-002 resume brief (carrying D5's ruling); then transcript, the request, run directory, receipts, return, any registration — **C-SEAM** | checkpoint pass before C-SEAM (R-C1) |
| 5 | Gate-(b) park; the owner's ruling brief; then T-003 entries and any `work/` artifacts | park before ruling before T-003 |
| 6 | The joined `DISCOVERY_LOG.md` row(s); `### Round 1 result` | |
| 7 | Reviewer brief; then transcript, `### Round 1 review`, `learnings.md` entry | brief before its run; result before review |
| 8 | The runbook flip — **C-FLIP** | **C-SEAM is an ancestor of C-FLIP** (R-G3) |
| 9 | `CURRENT_WORK.md` note; `freshness-record.md` closed; `operator-notes.md`; `verification_record.md` | |

## Component Overview

Under `.project/active/goal-research-model-proof/` unless stated.

- **`sessions/NN-<role>/`** — `brief.md` (the one committed input), `transcript.jsonl` (copied from `~/goal-proof-logs-item5/`), `output.md` (final result text), `meta.md` (session id, command, cwd, log dir, start/end, exit status, kept or discarded with reason).
- **`covering-branches.md`** — the pre-declared branch table: each honest non-exercise outcome, which criteria it covers, which it leaves non-exercised, and why that is a declared stop rather than a miss. Committed at phase 0, ancestor of C-T001.
- **`freshness-record.md`** — one row per run, kept and discarded, closing with the completeness statement.
- **`operator-notes.md`** — the orchestrator's notes on its own side: what the runbook prompted for unprompted, what the operator had to supply, where the exchange stalled, and each operator judgment call graded `[AGENT]` and never as a contract repair. Written after the runs, from the kept transcripts. Item 4's file is the shape.
- **`verification_record.md`** — the nine criteria against disk, one row each: criterion, producing run(s), the path/commit/return file that settles it, verdict. Then the ordering predicates with commands and pasted output; then the Required Invariant checks; then **§ Failures** — every point where the prose route was ambiguous, misread, or failed, whether or not it promoted anything; then **§ Hardening verdict** naming what was promoted and why, or that nothing was.
- **`work/orchestration/goals/p-pump-basis/`** — the goal, which stays.
- **`knowledge/research/requests/REQ-PPUMP-01.json`, its run directory, receipts, `return.json`** — the seam's committed evidence.
- **Whatever `source_registry.py` wrote**, if the return was `REGISTERED`: source directory, manifest row, index block. Nothing here is hand-authored.
- **One joined row** in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under `20260821-power-cycle-ab#3`, plus any other touched id.
- **One modeling work item** in `work/BACKLOG.md` with `work/active/WI-0NN_.../spec.md`, if gate (b) opened.

## Required Invariants

1. Every cold session has exactly one committed brief, and its commit is an ancestor of the commit carrying that session's output.
2. No cold session's tool-call *inputs* read `.project/active/goal-research-model-proof/`, any `.orchestrate-logs/`, or `~/goal-proof-logs-item5/`. Swept against tool inputs, not raw transcript text.
3. No brief committed before T-001's return contains: `Moscato`, `SOFT 2018`, `WPBOP`, `research_seam`, `source_registry`, `research-acquire`, or `not ingested`.
4. `git merge-base --is-ancestor C-COVER C-T001` holds.
5. `git merge-base --is-ancestor C-SEAM C-FLIP` holds.
6. No commit hand-edits `knowledge/SOURCE_INDEX.md`, `knowledge/MANIFEST.jsonl`, or anything under `knowledge/sources/`. Every change there is `source_registry.py`'s, and `uv run python scripts/source_registry.py verify` reports zero faults at close.
7. No first-sighting `DISCOVERY_LOG.md` row is edited and no id is minted; `tests/study/test_records.py` passes.
8. `git diff` on `GOAL_RUNBOOK.md` touches only the four spots in R-G1–G4. The `integrate` row and its bullet are byte-unchanged.
9. Every disk predicate against a goal file is date-anchored, so it cannot match the template's `YYYY-MM-DD` placeholders.
10. No task envelope, event ledger, digest comparison, idempotency layer, reconciliation pass, or dispatcher appears in the item's diff without a recorded run failure promoting it (R-H1).

## Non-Goals

- Study execution, package regeneration, and pin promotion — Item 6's; a round reaching them returns `PREREQUISITE` naming the `integrate` seam.
- Repairing the `integrate` seam or flipping its runbook row.
- Reopening `cryo-volume-basis`.
- Carrying the follow-up work item past `spec-model` (D3).
- A second round.
- Any new script, wrapper, or mechanism. The item's only executable inputs are the two Item 2 scripts, the modeling PM's CLI, and `claude -p`.
- A critic per native stage — one checkpoint, placed as R-C1 says.

## Implementation Notes

- **Never invoke a cold session through `orchestrate-stage.sh`.** It composes `/_my_<stage>` plus an orchestrator preamble, and its buffered `--output-format json` does not survive a kill. Direct `claude -p --output-format stream-json --verbose`, teed outside the tree.
- **Date-anchor every poll and grep against goal files.** The trail template ships `### T-001 return — YYYY-MM-DD` literally; an unanchored predicate false-positives immediately (Item 4 harness error 08a).
- **Fence sweeps target tool-call inputs.** Every brief embeds its own denial list, so a raw-text grep self-matches.
- **Export the environment before `tests/models`:** `set -a; source ~/1cfe/agentic-mbse/.env; set +a`.
- **`pm approve-research` refuses an empty insight list.** A source-only research round produces one; the workaround is filed upstream and is not this item's to fix. If it bites, record it in § Failures.
- The plan should write `covering-branches.md` in full at phase 0 — it is a small file, and its whole value is that it was finished before the round opened.

## Potential Risks

- **The prerequisite does not emerge (B1 false).** T-001 returns `COMPLETE`. Mitigation: none, by design — R-B3 forbids manufacturing one. The item ships the smaller proof and criterion 1 goes unmet, owner-visible.
- **The grounding exchange stages the discovery anyway.** The brief fence (Invariant 3) is mechanical, but a session can still infer the errand from row `#3`'s Home column. Mitigation: the ambient hint is documented up front in `verification_record.md`, and criterion 1 is judged on the work T-001 actually did, not on the absence of a hint.
- **The checkpoint hits its cap.** Then `### Stop` of kind `cap`, the round stops, and the owner decides. This is a designed outcome, covered by the declared branch — not a failure of the item.
- **The seam returns `BLOCKER` from a malformed request.** `MECHANICAL_FAILURE` under D8, retried within the cap after fixing the request; past the cap it is a blocker and the round closes.
- **The owner does not rule gate (b) before the item closes.** Near-certain per the spec; the round closes on trigger 4 and criterion 4 ships non-exercised under the declared branch.
- **Budget.** Eight to ten sessions against an 8h execute estimate. Mitigation: D2 (one round) and D3 (spec-model ceiling) are the two bounds that keep it inside; conditional runs 04b and 06 are the flex.

## Integration Strategy

Nothing changes shape. The goal layer keeps its five surfaces; the research seam keeps its two scripts and one command; the modeling PM mints and specs its own item through its own operations. The only durable repository changes this item leaves behind are the new goal directory, the seam's committed run evidence, whatever `source_registry.py` wrote, one joined discovery row, one modeling work item, the four-spot runbook flip, and a one-sentence pointer in `CURRENT_WORK.md`. Everything else is the item's own record of the run.

The flip is what makes the run compound: after it, the next goal round that needs evidence is told to use the seam rather than to hand-write a registry entry.

## Validation Approach

- **Per criterion, against disk.** `verification_record.md` names, for each of the nine criteria, the producing run and the path, commit, or return file that settles it, and gives a verdict. Item 4's record is the shape to match.
- **Ordering predicates.** The two `git merge-base --is-ancestor` checks (Invariants 4 and 5), run with their output pasted.
- **Invariant checks.** Invariants 1–10 each get a command and its output — the brief-ancestry walk, the tool-input fence sweep, the pre-T-001 brief grep, `source_registry.py verify`, `tests/study/test_records.py`, the scoped `GOAL_RUNBOOK.md` diff, the hardening-list grep over the item's own diff.
- **Independent checks that are not ours.** The checkpoint critic checks the reading and dispositions; the fresh `RoundReview` checks the whole round including every touched discovery row and the learning delta. Neither is replaced by anything in this document.
- **The honest-outcome test.** Whatever the round closed on, `covering-branches.md` predates it in `git log` and already says which criteria that outcome covers. If the outcome is one the branch table does not list, that is a finding for § Failures, not a reason to edit the table.

## Next-Stage Handoff

**Fixed for the plan:** the slug `p-pump-basis` (D1); one round only (D2); the `spec-model` ceiling on the follow-up work item (D3); one session per round plus two fresh reviewers (D4); the D8 class mapping; the request shape with `consumer` = `20260821-power-cycle-ab#3` (D7); the commit sequence and its two ordering predicates; the ten Required Invariants; the grounding brief's may/may-not lists.

**Open, and correctly so:** the goal's § Question wording and its "answered when" terms — the owner's at gate (a). The exact T-001 scope wording, which the round agent writes. Which seam class comes back. Whether the round reaches T-003 at all.

**De-risk first:** the T-002 operator ruling (D5). It is the one place a committed brief has to override the shipped contract, and getting its wording wrong either stages the errand (too early, too specific) or leaves the round following the stale hand-pattern bullet. Draft it in the plan, review it against Invariant 3's fence, and commit it only after T-001's return is on disk.

---
Next Step: After approval → `/_my_design_review`, then `/_my_plan`.
