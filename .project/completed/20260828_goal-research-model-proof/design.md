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
- **B6.** A registered `p_pump` value moves the number without moving the premise the strategy rests on, so `REGISTERED` leaves the R-E1 advance available. *If false → T-002 or T-003 returns `STRATEGY_BLOCKER` through gate (c), criterion 4 goes non-exercised under the declared branch, and criterion 3 is still met by honest routing.* **This bet is the weakest one here, and the design's own evidence leans against it:** DI-008's band is ~60–190 MW for Stellaris against 1.0 MW held; the arms sit at `rec_frac` 0.94 / 0.79 / 0.68 at the same grid corner and `recirc_ok` already fails at R ≤ 8.0 / 6.5 / 5.5 m by arm (`record.md@881d4448:208,56`). Adding tens of megawatts equally to arms already at and past the fence plausibly changes what the A/B comparison means. So `REGISTERED → advance` and `REGISTERED → STRATEGY_BLOCKER` are **peer outcomes**, not a main line and a fallback. The design does not predict which — R-A6 stops short of the conclusion on purpose, and the judgment belongs to the round, made on the registered evidence under the critic checkpoint and the fresh reviewer.

## Key Decisions

- **D1. The goal slug is `p-pump-basis`**, at `work/orchestration/goals/p-pump-basis/`. It names the model value in question, matching the shape of the closed `cryo-volume-basis` goal, and it says nothing about acquisition, sourcing, or research. *Rejected: `p-pump-resource` and anything containing "source" or "research" (smuggles the errand into the directory name, which every session reads first, R-A2a). The final wording of the goal's § Question is the owner's at gate (a); this decision fixes only the slug the operator proposes with it.*
- **D2. This item covers exactly round 1, and no round 2 is opened.** The goal itself declares the runbook's default round limit of 6, because it is a real goal that outlives this item — the item's bound is not the goal's limit. `model → PREREQUISITE → checkpoint → research → model` runs as T-001…T-003 under one strategy revision. The item ships when round 1 has a `### Round 1 result` and a fresh `### Round 1 review`, on any of the six close triggers. *Rejected: declaring a round limit of 1 in `goal.md` (cripples a real goal to suit a proof item's budget, and would make an honest continuation look like a limit breach). Rejected: opening round 2 to chase criterion 4 (the epic budgets 8h execute; the spec's floor already declares round 1 shippable).*
- **D3. If the round advances, the follow-up work item is carried to `spec-model` and stops there.** This decision bounds one of two peer sequels to a registered source (B6); it does not assume that sequel. Should the round instead read the registered evidence as moving the premise, T-003 is never scoped and the round goes to gate (c) and `STRATEGY_BLOCKER` — the ceiling below simply does not apply. On the advance path, T-003's authorized ceiling, once the owner rules gate (b), is: `pm add-item` mints the item, and `/spec-model` writes its `spec.md` citing the registered source directly. Design, plan, implement, and every regeneration or pin are out — R-E4 already puts them in the `integrate` seam, and they do not fit the budget. Criterion 4's "advances the native work item under the same strategy" is met by a minted, specced item whose spec carries the new sourced basis and states the comparison-meaning reading. *Rejected: carrying through `/design-model` (needs SysML prototyping and validation; blows the budget and drags the item into Item 6's territory). Rejected: stopping at the mint (a bare backlog row advances nothing and cites no evidence).*
- **D4. One session carries the whole round, resumed across owner turns; only the critic and the reviewer are separate fresh sessions.** ADR-002 puts one agent on one round; Item 4 needed several only because a kill was staged. Owner rulings arrive as committed resume-turn briefs, exactly as they did in Item 4's grounding. *Rejected: a fresh session per task (breaks one-agent-per-round and re-pays the read-in cost three times for no measured gain).*
- **D5. At T-002 the operator overrides the runbook's stale `research` row with a committed ruling naming the native route.** The row still says "pending native repair" and its bullet routes to the WI-031 hand pattern; following it would violate R-D1 and criterion 3, and flipping it first would violate R-G3. So the T-002 resume brief states, as an operator ruling, that Item 2 shipped the native procedure at `docs/research_seam_operator_guide.md@9637f1b7` and that the runbook row is stale pending this item's own flip. It is delivered *after* T-001's return and after the checkpoint, so it stages nothing. *Rejected: flipping the runbook before the round (R-G3 — the flip must rest on the run). Rejected: letting the round follow the hand pattern (R-D1, criterion 3).*
- **D6. The covering branch is a committed file, `covering-branches.md`, whose commit is an ancestor of the strategy-revision commit.** *Rejected: a section inside `spec.md` (already committed, so its ancestry proves nothing about when the branches were declared relative to the round). Rejected: a trail entry (the trail is the round's record; the declaration is the item's, and it must predate the round opening).*
- **D7. The seam request's `consumer` is `20260821-power-cycle-ab#3`.** The discovery row is what is actually waiting, it exists at request time, and the work item does not — it is minted at T-003, after the gate. *Rejected: waiting to mint the WI first so the consumer could be `WI-0NN` (inverts the sequence the item exists to prove, and gate (b) has not been ruled at that point).*
- **D8. Seam class → goal outcome is a fixed reading, declared in `covering-branches.md` before the round opens and applied by the round.** Say plainly what this is: **the item is taking a judgment the runbook leaves to the round agent.** The runbook gives the round the six outcomes and lets it read a return; this design fixes the reading in advance, because four classes against six outcomes is exactly where an honest queue gets quietly re-graded into a blocker, and because a mapping written after the return is not a mapping. The mapping is a reading of the return, never a re-grade of it — the seam's class is preserved verbatim in the trail beside it (R-D3).

  | Seam class | Goal outcome | Note |
  |---|---|---|
  | `REGISTERED` | `COMPLETE` | Both sequels stay open (B6) |
  | `OPERATOR_QUEUE` | `PREREQUISITE` | Then a separate park at gate (b). The trail writes both steps so the reviewer sees the gate, not a missing one |
  | `BOUNDED_NEGATIVE` | `BOUNDED_NEGATIVE` | A first-class result; cited by whatever was waiting (R-D6) |
  | `BLOCKER` | see below | Split by whether the fix changes the request key |

  **`BLOCKER` splits in two, because the runbook's retry rule is strict.** A retry is permitted only when the task, its inputs, its scope, and its meaning are all identical (`GOAL_RUNBOOK.md:132`). The seam's request key is a hash of `question`, `consumer`, `gap_type`, and sorted `where_to_look` (`research_seam_operator_guide.md:108`).

  - **Fix leaves the key unchanged** — unwritable registry, a broken environment, a `limits` or `priority` change: `MECHANICAL_FAILURE`, retried under the same `T-00N` id with a second `### T-00N start` recording the operational correction, within the cap of 2.
  - **Fix changes any key field:** by the seam's own definition it is a different request, so by the runbook's definition it is a **different task**. It gets a new `T-00N` with its own scope, inside the same round, and the trail says why the request changed. It is not a retry and is not written as one.

  Getting this wrong is precisely what the fresh reviewer checks (`GOAL_RUNBOOK.md:169`), so it would surface as a review finding if left blurred.

  *Rejected: leaving the mapping to the round agent in the moment (see above). Rejected: `goal.md` § Invariants as its home — that field class has a defined contract, "the invariants a comparison must preserve" (`:68`), and it is one of the five R-A3 checks an auditor reads for a different purpose. A routing table there pollutes it. `covering-branches.md` is already the item's pre-declared-readings artifact and already commits at C-COVER, ahead of C-T001, so it carries the same ancestry guarantee.*

## Architecture

### The goal

`work/orchestration/goals/p-pump-basis/` — `goal.md`, `trail.md`, `learnings.md`, copied from `work/orchestration/goal-templates/`. All five field classes non-hollow at grounding (R-A3), and all four of the runbook's limits restated explicitly with their default numbers per R-A5/R-C3a: retry cap 2 retries (3 attempts); checkpoint revision cap 2 revisions (3 submissions); round limit 6; **tasks per round: none** (`GOAL_RUNBOOK.md:227-230`). The runbook has no time-limit row, so none is invented. § Invariants carries the `p_pump` → recirculating sum → `rec_frac`/`p_net` → `recirc_ok`/`net_positive`/LCOE channel and the equal-input/unequal-effect distinction, stopping short of any conclusion about whether comparison meaning survives (R-A6) — and nothing else. The seam-class routing table is not an invariant and lives in `covering-branches.md` (D8). § Reserved gates names gate (b) — any model or knowledge mutation beyond the goal directory — and gate (c) — the close ruling on a judgment call — plus merge, push, item close, archive. Every operator-side sentence is graded `[AGENT]`; only what the owner said at gate (a) is `[OWNER]`.

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

Every return carries the outcome, the evidence refs, the goal-level reading of them, and **the five decision fields for each goal-level decision** — the finding or trigger, the decision and its reason, the tier (`execution detail | reserved gate | premise surprise`), who decided, and what changed as paths, ids, commits, or `none` (R-B4, `GOAL_RUNBOOK.md:130`). T-001's return is the item's primary evidence, so its decision blocks are what an auditor reads first.

Between T-001 and T-002 sits `### Checkpoint C-001.r1` — the reading (row `#3` and record § 15 and DI-008, together with T-001's return) plus the proposed research and model dispositions, handed to a fresh `run-goal checkpoint` session. Revisions are `r2`, `r3`; at the cap the round writes `### Stop` of kind `cap` and stops (R-C3).

**A route change to a passed disposition costs a new submission.** R-C1's guarantee is that a fresh critic approved the dispositions *before* the follow-up executed — so what executes has to be what the critic approved. Session 03 writes its proposed research disposition while the runbook still routes it to the WI-031 hand pattern, and the critic reads the same stale runbook, so C-001.r1 may well pass on the wrong route. When D5's ruling then changes the route, **the revised dispositions go back as `### Checkpoint C-001.r2` before T-002 executes.** The cap still holds: r2 and r3 are the two revisions the goal declares, and a third disagreement is a `### Stop` of kind `cap`, not a waiver. The alternative — delivering the ruling before the checkpoint — is worse, because it colors the critic's judgment on exactly the question the checkpoint exists to test. One conditional critic session (04b) is budgeted for this and it is the likely case, not the unlikely one.

The round can end before T-003 and still be complete. Two shapes are roughly as likely as each other. If DI-008's strongest primary stays un-ingested, T-002 returns `OPERATOR_QUEUE` → `PREREQUISITE` → the queued candidate goes to the owner → the round closes on trigger 4 or 5. If a source registers, the round faces the comparison-meaning judgment (B6) and closes either by advancing through T-003 or, through gate (c), on trigger 2 as `STRATEGY_BLOCKER`.

**Reading this section against § Sessions:** the two tables cut the same run two ways. T-001 happens in session 03; the checkpoint in 04 (and 04b on the r2 above); T-002 in session 05, which is session 03 resumed; T-003 and the close in 06 and 07, also session 03.

### The stale runbook row

The round agent reads `GOAL_RUNBOOK.md` § The native seams, which today tells it the `research` seam is unrepaired and routes it to the WI-031 hand pattern (`:256`, `:264`). This is the one place the shipped contract actively points the run at the wrong route. D5 resolves it with an operator ruling in the T-002 brief. Two things follow.

It is a **measured prose failure** and it goes in `verification_record.md` § Failures as one: the runbook instructed a hand-write that Item 2 had already replaced, and only an operator ruling stopped it. Whether the round agent notices the staleness by itself *before* the ruling arrives is worth recording either way, from the T-001 return and the checkpoint transcript.

It is also the evidence R-G3 wants: the flip lands after the seam actually ran, so the runbook change rests on the run.

The T-002 brief carries the ruling with its `[AGENT]` grade **in the brief itself**, not only in `operator-notes.md`, so the round agent knows it is reading an operator judgment rather than a contract.

### The other surfaced conflict: the checkpoint's trigger phrase

`GOAL_RUNBOOK.md:140` phrases the checkpoint trigger as "after a study reading produces proposed dispositions." This round executes no study — it reads already-committed study evidence — and the spec parked this for loud surfacing rather than silent absorption (R-C2, capture-fidelity Rule 4).

The reading this run acts on is the spec's: the checkpoint fires on **the reading**, and a reading of committed study evidence is a reading; its basis is the epic's own Item 5 scope step 2, which names no freshly executed study (`epic:389`) and which the owner ratified with the decomposition. That reading is recorded as an orchestrator execution-detail decision, loudly, in **two named places**: `verification_record.md` § Failures, beside the seam-row staleness, and the run summary that goes to the owner. If the owner reads `:140` narrowly, it is that runbook sentence that gets amended — not this item's checkpoint. Nothing in the run depends on the owner ruling either way before close.

### The brief fence

Two mechanisms, and the second is the one Invariant 2 checks.

**Delivery.** A brief is passed to `claude -p` **on stdin**. The file at `sessions/NN-<role>/brief.md` is the committed *record* of what was passed — it is never the session's read, and no brief instructs a session to open it. This is Item 4's mechanism (`.project/completed/20260827_goal-cold-pickup-proof/plan.md:100`), and stating it is what keeps Invariant 2 from reading as self-contradictory: a session receives its brief without ever touching the item directory.

**An allowlist, then the denials** — Item 4's shape (`design.md:72`), stated once here and copied into every brief for sessions 03–08.

*May read:* `work/orchestration/goals/p-pump-basis/`, `work/orchestration/GOAL_RUNBOOK.md` and `work/orchestration/goal-templates/`, `.claude/skills/run-goal/`, `.project/adr/`, and the native repository — `models/`, `knowledge/`, `work/`, `exploration/`, `modeling_project/`. From run 05 on, also `docs/research_seam_operator_guide.md`, `.claude/commands/research-acquire.md`, `scripts/research_seam.py`, `scripts/source_registry.py`, and `knowledge/research/`.

*May not read:* `.project/active/goal-research-model-proof/` (this item's own directory, including every brief and record), any orchestration log directory — `.orchestrate-logs/` anywhere in the tree and `~/goal-proof-logs-item5/` — and `.project/backlog/epic_goal_strategy_task_harness.md`.

Two role-specific narrowings sit on top. Sessions 01–03 additionally may not read the research seam paths listed above; that is Invariant 3's fence, and it lifts once T-001's return is on disk. Session 08, the reviewer, reads everything on the allowlist including the whole trail — its job is the round end to end.

**The `.project/backlog/` denial is new relative to Item 4** and it is there for a reason worth naming: the epic's § Item 5 states the intended `model → research → model` sequence and the native-research-seam criterion. It names no `p_pump`, Moscato, or WPBOP, so the leak would be the *shape* of the errand rather than its content — but it is a leak, and the cheap fix is to deny it. As with row `#3`'s Home column, if a transcript shows a session reached it anyway, that is recorded in `verification_record.md` as a second ambient hint and criterion 1 is judged on the work T-001 actually did.

**Verified by transcript.** Every `Read`, `Grep`, `Glob`, and `Bash` call is in the kept stream, so an auditor checks the fence held rather than taking it on trust.

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

**Session 08's brief must say which of the reviewer's two sequels the item wants**, without scripting the verdict. After a pass the runbook has the fresh reviewer either recommend the owner-held close or write the next strategy revision, which opens round N+1 (`:181`). D2 says no round 2 opens here, so the brief states that the item wants the close recommendation and that opening round 2 is out of scope for this run. The verdict itself — `PASS`, `FINDINGS`, or `OWNER_GATE` — and every finding stay the reviewer's.

Run 06 is conditional, and run 04b is likely rather than conditional (the route-change re-submission above). The freshness record enumerates whatever actually happened, kept and discarded, and closes with the completeness statement — these were all the runs there were, and no other input existed (Item 4's shape).

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

**The paths, end to end.** The search names Moscato et al., SOFT 2018, WPBOP-CPR(18) 20276 as the strongest candidate. Two outcomes are roughly as likely as each other, and a third sits inside the first.

If the PDF is reachable and extracts, `register --run` writes the source directory, manifest row, and index block together and the return is `REGISTERED` — T-002 is `COMPLETE`. **The round then has to do the analytic work this item's evidence makes likely** (B6): read the registered band against the arms' recirculating fractions and the `recirc_ok` fence radii, and decide whether the A/B comparison still means what it meant. That judgment goes through the checkpoint's already-passed dispositions and is checked by the fresh reviewer. It resolves one of two ways, and neither is the fallback of the other:

- *The premise holds.* The round parks at gate (b), and on the owner's go T-003 mints and specs the work item citing the registered source directly (R-D5: a registered source is sufficient MR-4 basis; no DI is minted, which would itself be gate (b) material). Criterion 4 is exercised.
- *The premise moves.* The round parks at gate (c) with the reading, and on the owner's ruling closes `STRATEGY_BLOCKER` on trigger 2 (R-E3). Criterion 4 goes non-exercised under the declared covering branch; criterion 3 is still met by honest routing. **The round does not force the positive path**, and T-003 is never scoped.

If the candidate is behind the IDM or a publisher wall, the agent records `log --failure <url> --reason "<the wall>"` with the default disposition, the candidate lands in `queued[]`, no bounded negative is written (`:155`), and the return is `OPERATOR_QUEUE`. T-002 then returns `PREREQUISITE` per D8, the queued candidate goes to the owner at the gate-(b) park with its reason, and the round closes on it. **It is not retried into a positive and not re-graded as a blocker** (R-D6).

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

**R-A7 and R-A7a**, in the same neighbourhood but not the same commit. The owner ruled a **removal**, so the edit to `.project/CURRENT_WORK.md:22` strikes the list member rather than annotating beside it. The Phase 4 close list today reads "…the runbook sentences (#10/#11 from study 2; #6/#10/#11 from study 1), **the `p_pump` re-source item**, WI-030's DI note". The bolded member is deleted and the sentence closes with one pointer: the `p_pump` re-source is not on this list — it runs under `work/orchestration/goals/p-pump-basis/` (`align.md`, `[OWNER 2026-08-27]`). That single clause is R-A7a's record of where it went. Leaving the member standing with a note appended beside it would be accretion, not correction (capture-fidelity Rule 3). No modeling-PM or goal state is mirrored — a pointer only.

## The commit sequence

Ordering predicates an auditor checks with `git merge-base --is-ancestor`.

| # | Commits | Ordering it carries |
|---|---|---|
| 0 | Item scaffolding: `sessions/`, `covering-branches.md`, `freshness-record.md` and `verification_record.md` as skeletons | `covering-branches.md` complete here — **C-COVER** |
| 1 | Per grounding turn: brief, then transcript + output + `goal.md` state | brief before its run; last commit carries `Status: grounded` |
| 2 | Round-agent brief; then transcript, strategy revision, T-001 entries — **C-T001** | **C-COVER is an ancestor of C-T001** (R-H4) |
| 3 | Critic brief(s); then transcript(s) and each `### Checkpoint C-001.rK` | brief before its run; a passing checkpoint entry precedes any T-002 commit |
| 4 | T-002 resume brief (carrying D5's ruling, `[AGENT]`-graded); if the ruling changes the approved route, the `C-001.r2` brief and its entry land **before** the seam runs; then transcript, the request, run directory, receipts, return, any registration — **C-SEAM** | the checkpoint pass that C-SEAM rests on is the one covering the route actually executed (R-C1) |
| 5 | Gate-(b) park; the owner's ruling brief; then T-003 entries and any `work/` artifacts | park before ruling before T-003 |
| 6 | The joined `DISCOVERY_LOG.md` row(s); `### Round 1 result` | |
| 7 | Reviewer brief; then transcript, `### Round 1 review`, `learnings.md` entry | brief before its run; result before review |
| 8 | The runbook flip — **C-FLIP** | **C-SEAM is an ancestor of C-FLIP** (R-G3) |
| 9 | The `CURRENT_WORK.md` Phase 4 list removal; `freshness-record.md` closed; `operator-notes.md`; `verification_record.md` | |

## Component Overview

Under `.project/active/goal-research-model-proof/` unless stated.

- **`sessions/NN-<role>/`** — `brief.md` (the one committed input), `transcript.jsonl` (copied from `~/goal-proof-logs-item5/`), `output.md` (final result text), `meta.md` (session id, command, cwd, log dir, start/end, exit status, kept or discarded with reason).
- **`covering-branches.md`** — two pre-declared tables, committed at phase 0 and an ancestor of C-T001. First, the branch table: each honest outcome — `OPERATOR_QUEUE` and the gate park, a bounded negative, a `STRATEGY_BLOCKER` close (including the `REGISTERED → STRATEGY_BLOCKER` case, B6), and the no-prerequisite case — with which criteria it covers, which it leaves non-exercised, and why that is a declared stop rather than a miss (R-H4). Second, D8's seam-class → goal-outcome mapping including the `BLOCKER` split, stated as the item taking a judgment the runbook leaves to the round.
- **`freshness-record.md`** — one row per run, kept and discarded, closing with the completeness statement.
- **`operator-notes.md`** — the orchestrator's notes on its own side: what the runbook prompted for unprompted, what the operator had to supply, where the exchange stalled, and each operator judgment call graded `[AGENT]` and never as a contract repair. Written after the runs, from the kept transcripts. Item 4's file is the shape.
- **`verification_record.md`** — the nine criteria against disk, one row each: criterion, producing run(s), the path/commit/return file that settles it, verdict. Then the ordering predicates with commands and pasted output; then the Required Invariant checks; then **§ Failures** — every point where the prose route was ambiguous, misread, or failed, whether or not it promoted anything. Three entries are known before the run and are written whatever else happens: the stale `research` seam row that pointed the round at the WI-031 hand pattern; the `:140` trigger-phrase tension and the reading this run acted on (R-C2); and any ambient hint a session reached that the fence could not remove. Then **§ Hardening verdict** naming what was promoted and why, or that nothing was.
- **`work/orchestration/goals/p-pump-basis/`** — the goal, which stays.
- **`knowledge/research/requests/REQ-PPUMP-01.json`, its run directory, receipts, `return.json`** — the seam's committed evidence.
- **Whatever `source_registry.py` wrote**, if the return was `REGISTERED`: source directory, manifest row, index block. Nothing here is hand-authored.
- **One joined row** in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under `20260821-power-cycle-ab#3`, plus any other touched id.
- **One modeling work item** in `work/BACKLOG.md` with `work/active/WI-0NN_.../spec.md`, if gate (b) opened.

## Required Invariants

1. Every cold session has exactly one committed brief, and its commit is an ancestor of the commit carrying that session's output.
2. No cold session's tool-call *inputs* read `.project/active/goal-research-model-proof/`, any `.orchestrate-logs/`, `~/goal-proof-logs-item5/`, or `.project/backlog/epic_goal_strategy_task_harness.md`. Swept against tool inputs, not raw transcript text. Briefs arrive on stdin, so receiving one is not a read of the item directory (§ The brief fence).
3. No brief committed before T-001's return contains: `Moscato`, `SOFT 2018`, `WPBOP`, `research_seam`, `source_registry`, `research-acquire`, or `not ingested`.
4. `git merge-base --is-ancestor C-COVER C-T001` holds.
5. `git merge-base --is-ancestor C-SEAM C-FLIP` holds.
6. No commit hand-edits `knowledge/SOURCE_INDEX.md`, `knowledge/MANIFEST.jsonl`, or anything under `knowledge/sources/`. Every change there is `source_registry.py`'s, and `uv run python scripts/source_registry.py verify` reports zero faults at close.
7. No first-sighting `DISCOVERY_LOG.md` row is edited and no id is minted; `tests/study/test_records.py` passes.
8. `git diff` on `GOAL_RUNBOOK.md` touches only the four spots in R-G1–G4. The `integrate` row and its bullet are byte-unchanged.
9. Every predicate command `verification_record.md` reports is pasted verbatim, and each one that reads a goal file shows its date anchor in the pasted text. A predicate quoted without its anchor is itself the audit finding. (The underlying discipline — never poll a goal file on an unanchored pattern, because the templates ship `YYYY-MM-DD` literally — is in Implementation Notes; this invariant is the checkable trace of it.)
10. No task envelope, event ledger, digest comparison, idempotency layer, reconciliation pass, or dispatcher appears in the item's diff without a recorded run failure promoting it (R-H1). The check is a keyword sweep **plus a read of the whole item diff** — a dispatcher need not call itself one — and `verification_record.md` states it that way rather than claiming mechanical completeness.

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
- **The seam returns `BLOCKER`.** Split per D8: if the fix leaves the request key unchanged it is a `MECHANICAL_FAILURE` retry within the cap, and past the cap a blocker that closes the round; if the fix changes a key field it is a new task with its own scope, not a retry. Writing the second case as a retry is what the fresh reviewer's retry-classification check catches.
- **The registered source moves the premise (B6 false).** Then the round does the comparison-meaning judgment and closes `STRATEGY_BLOCKER` through gate (c). Not a risk to mitigate — a peer outcome to budget for, which is what makes it a risk to the *schedule* rather than to the item.
- **The owner does not rule gate (b) or gate (c) before the item closes.** Near-certain per the spec; the round closes on trigger 4 and criterion 4 ships non-exercised under the declared branch.
- **Budget, honestly.** The floor path is seven sessions — 01, 02, 03, 04, 05, 07, 08 — which fits the 8h execute estimate on Item 4's measured shape. Two things eat the margin and both are likely rather than remote: the `C-001.r2` re-submission M1 requires (one more session, run 04b), and the comparison-meaning judgment if a source registers, which is real analytic work in session 05 or 06 rather than a park. Nine sessions plus one substantive judgment is the realistic ceiling. Mitigation: D2 (one round) and D3's `spec-model` ceiling are the two bounds that keep it inside; if the budget binds, the thing that gives is T-003's spec depth, never the checkpoint or the review.

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

**Fixed for the plan:** the slug `p-pump-basis` (D1); one round only (D2); the `spec-model` ceiling on the advance path (D3); one session per round plus two fresh reviewers (D4); the D8 class mapping and its `BLOCKER` split, homed in `covering-branches.md`; the request shape with `consumer` = `20260821-power-cycle-ab#3` (D7); the route-change rule that sends a changed disposition back as `C-001.r2`; brief delivery on stdin with the allowlist and denials of § The brief fence; the commit sequence and its two ordering predicates; the ten Required Invariants; the grounding brief's may/may-not lists; the `CURRENT_WORK.md` edit as a removal.

**Open, and correctly so:** the goal's § Question wording and its "answered when" terms — the owner's at gate (a). The exact T-001 scope wording, which the round agent writes. Which seam class comes back. Whether a registered value preserves the premise or moves it (B6) — the round's judgment, under the critic and the reviewer. Whether the round reaches T-003 at all.

**Still owed at close, outside this design:** the `product-lens.md` ledger entry the spec marks "to be created at close; not yet run" (review A9).

**De-risk first:** the T-002 operator ruling (D5) and the `C-001.r2` it triggers. The ruling is the one place a committed brief has to override the shipped contract; getting its wording wrong either stages the errand (too early, too specific) or leaves the round following the stale hand-pattern bullet. Draft both in the plan, review the ruling against Invariant 3's fence, and commit it only after T-001's return is on disk. The r2 brief is the thing that keeps R-C1 intact — what executes must be what the critic approved.

---
Next Step: After approval → `/_my_design_review`, then `/_my_plan`.
