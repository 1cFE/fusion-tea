# Design: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-26
**Updated:** 2026-08-26
**Branch:** `feat/goal-integration-seam` (no child branch)
**Base commit:** `78e03edf`

---

## Overview

Run one real goal — `cryo-volume-basis` — through Item 1's shipped contract in ten headless cold runs across nine distinct sessions, and keep the input, the output, and the commit order of every one of them as the proof.

## Related Artifacts

- **Spec:** `.project/active/goal-cold-pickup-proof/spec.md` (Approved after review)
- **Spec review:** `.project/active/goal-cold-pickup-proof/spec-review.md`; dispositions `briefs/spec_fix.md`
- **Align record:** `.project/active/goal-cold-pickup-proof/align.md`
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 4
- **Contract under test:** `work/orchestration/GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, `.claude/skills/run-goal/SKILL.md`
- **Decision records:** ADR-001 through ADR-007 (`.project/adr/`)
- **Grounding chain for the proof goal:** `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:20`, `knowledge/KNOWLEDGE.md` DI-010, `work/completed/20260822_WI-031_research-round-item6-values/`

## The Point

Item 1 shipped a goal layer that nobody but its author has ever used. Three bets carry the epic's critical path on that layer, and all three are untested: a stranger can ground a goal and cannot start an ungrounded one; a fresh session can resume an interruption from disk; a fresh reviewer catches drift and settles the learning delta.

The obligation that makes this urgent is the owner's, and it is a bar, not a wish: **none of the five hardening mechanisms — envelope YAML, event ledger, digests, idempotency keys, reconciliation — enters the first build unless a recorded proof run demonstrates that the prose/native-facts route failed** `[OWNER]` (`goal-strategy-task-harness-design-review.md:209`, carried as the epic's Hardening rule). Concurrent runs and unattended dispatch are not on that list; ADR-003 bars them outright as premises, and no evidence this item produces can promote them.

So this run is the only admissible evidence in either direction. Without it there is nothing to promote a mechanism on, and equally nothing that justifies leaving the prose route alone. This design's job is to make the run *count* — to produce evidence an auditor who did not watch it can verify from files alone. Everything below exists for that one purpose. This item records failures; it does not repair them.

## Research Findings

**The contract under test.** `GOAL_RUNBOOK.md` § The five surfaces fixes the three goal files and their location (`:23-35`). § What "fresh" means defines the session boundary and gives the agent its move when it cannot start a session (`:37-62`). § Running one task fixes the scope → start → work → return order and the six return outcomes (`:103-134`). § Opening and closing a round gives the six close triggers (`:84-91`). § Resuming an interruption gives the four-step resume order and "the native artifact is the truth" (`:208-219`). § The discovery log gives the round's one write outside its own directory and the no-mint rule (`:232-244`). The three templates at `work/orchestration/goal-templates/` carry the headings; `trail.md`'s template also carries the five decision fields (`trail.md:43`).

**The cold-session mechanism.** `~/.claude/scripts/orchestrate-stage.sh` runs one stage headless as `claude -p`, returns `{session_id, result, cost, is_error}`, and writes a full stream-json transcript to `.orchestrate-logs/` (`.project/research/20260822-120756_research-extraction-harness.md:81`, P7 at `:137`). Inspecting a real log confirms the transcript is a JSON array of `system|user|assistant|result` events carrying `session_id`, `cwd`, the tool list, the initial prompt, every tool call, and the final result text. `.orchestrate-logs/` is gitignored (`.gitignore:54`), so nothing kept there is evidence until it is copied into the item directory and committed.

**The grounding chain the proof goal rests on.** Discovery row `20260823-magnet-technology-ab#2` is live and `unrouted`, and its Home column already names where it belongs: "modeling item under the MFE cost modeling epic" (`DISCOVERY_LOG.md:20`). DI-010 (`knowledge/KNOWLEDGE.md`) gives the winding-pack current densities and states in its own model implications that the pack volume "should enter `vol_cold_cryo`". `work/BACKLOG.md:24` carries the epic — "MFE Cost Modeling — Tokamak & Stellarator". So the round's routing task has a real destination and a real citation chain, not a fixture.

**Where the runbook is silent, measured before the run.** A draft goal has no open round, so `trail.md` has no heading under which a refusal could be written; the runbook names no home for one. § Resuming an interruption tells the resumer what to write but not whether it inherits the round afterwards, while ADR-002 says a round is one agent's. Both gaps are recorded as evidence, not repaired here (spec § A predicted prose failure).

## Core Concept

The proof is a **stack of cold runs whose order is carried by git commits, not by anyone's account of what happened.** Ten runs across nine distinct sessions — run 02 is a recorded resume of session 01, and nothing else resumes anything. Each run gets exactly one brief, that brief is committed before the run starts, the run's full transcript and final output are committed after, and the freshness record enumerates all ten and closes the enumeration. An auditor checks ordering with `git merge-base --is-ancestor` and checks content by reading files. Nothing rests on the orchestrator's word.

The run those sessions execute is one honest round on one real question: should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`? The round routes the discovery row that raised it by minting the modeling work item the row's Home column already names — genuine native work, inside round authority — then tries to look at the model, hits the owner's model-mutation gate, and closes on an unresolved owner gate. No pin, no study, finding unsolved. That is a legitimate empty round, and it is exactly the shape the proof needs.

The three hard parts each get one mechanism, and each mechanism exists to make the evidence checkable rather than to make the run smoother:

- **Per-class gate measurement needs five drafts, not one.** A single draft hollow in all five field classes can only tell you which class a session noticed first. So five probes run, each against a goal hollow in exactly one class, each in a throwaway worktree so the canonical goals directory never holds a fixture.
- **A genuine interruption cannot be instructed.** A session told to stop will write the handoff stop the runbook tells it to write, and a recorded stop fails Criterion 4. So the round agent is killed after its native effect lands and before its return.
- **A seeded drift must be planted upstream of the writer.** The orchestrator plays the operator; the drift rides in the operator's framing of the round, and the round agent carries it into the strategy revision in good faith.

## Key Bets

- **B1.** The kill can be landed between the native effect and the return — the minting call is observable on disk the moment it completes, and a short poll catches it before the session writes six more lines. *If false → no genuine interruption; Criterion 4 is unprovable without repeated re-runs, and each re-run burns a fresh session.*
- **B2.** A goal hollow in exactly one field class, sitting at the canonical path in an ordinary-looking repository, reads to a cold session as a real goal. *If false → the per-class record measures the fixture's tells, not the shipped contract, and Criterion 2 is contaminated.*
- **B3.** Minting a modeling work item through the modeling PM is inside the round's authority — it is PM state, not a model or knowledge mutation, so it does not trip the goal's reserved gate. *If false → the round crossed a reserved gate to produce its interruption, and the interruption evidence is tainted at the root.*
- **B4.** An operator framing one notch wider than `goal.md` propagates into the round agent's written strategy revision without the agent flagging it. *If false → no drift is planted, and Criterion 8 has nothing to catch.*
- **B5.** The stream-json transcript records tool calls in enough detail to show that the resumer did not re-invoke the minting command. *If false → "no second invocation" rests on the artifact hash alone, which is weaker evidence than the spec asks for.*

## Key Decisions

- **D1. Cold sessions run headless through `orchestrate-stage.sh run`, one `run` per session.** A fresh session per `run`, resumable by id, is exactly the boundary § What "fresh" means requires, and the runner already produces a session id and a full transcript. *Rejected: interactive sessions (no kept input record, and the session boundary would rest on the operator's word).*
- **D2. All cold-session evidence lives in the item directory, never the goal directory.** `.project/active/goal-cold-pickup-proof/sessions/NN-<role>/`. The goal directory must survive into the repository as the first real goal, readable as a goal and not as a test fixture. *Rejected: an `evidence/` subdirectory under the goal (Criterion 3 would fail on its own artifact).*
- **D3. Five gate probes, one field class each, in throwaway git worktrees.** Per-class measurement is the criterion; one draft cannot produce it. Worktrees (`../fusion-tea-gate-p1` … `-p5`, per the repo's worktree convention) put each variant at the canonical path in a normal repository, run sequentially, and leave nothing behind. *Rejected: one draft hollow in all five classes (measures only the first class noticed); five draft goal directories committed at the canonical path (junk in `work/orchestration/goals/`, which Criterion 3 reads).*
- **D4. The interrupted task's native effect is a modeling work item minted through the modeling PM; the joined discovery row is the resumer's to append.** The row's own Home column names the modeling item, so minting it is the honest routing rather than a fixture write. The spec already scopes "byte-identical" to the interrupted artifact alone and says the discovery log legitimately gains rows during a correct resume (`spec.md:46`) — this split is what that sentence describes. *Rejected: the disposition row as the interrupted artifact (the resumer has a legitimate reason to append rows, so the unit and the noise would be the same file); a model or knowledge file (crosses the reserved gate).*
- **D5. The round runs two tasks and closes on an unresolved owner gate.** T-001 routes the row; T-002 asks whether the model can derive `vol_cold_cryo`, reaches the point where a model file would have to change, and returns `OWNER_GATE`. *Rejected: one task carrying both the interruption and the closure (the close trigger would have to be manufactured); closing on a declared limit (a limit tightened to make the round close is a fixture, and the owner gate is already real).*
- **D6. The resumer inherits the round and closes it.** § Resuming an interruption says what the resumer writes and stops there; ADR-002 says one agent per round. The interruption is precisely the case that breaks that, and the runbook does not say who continues. The design picks inheritance and **records the silence as a measured prose gap**. *Rejected: an eleventh session to close the round (three agents in one round, further from ADR-002, and it would hide the gap rather than record it).*
- **D7. The seeded drift is a widened strategy frame, planted in the operator's brief to the round agent.** `goal.md` binds the goal to `vol_cold_cryo`; the operator brief frames the round's interest as "the held cryo inputs in this package, starting with `vol_cold_cryo`". *Rejected: a comparison-meaning drift (the round commits no study, so comparison meaning is thin ground); planting it by the orchestrator editing the trail after the fact (the round's written material must be the round agent's).*
- **D8. Every cold session's full stream-json transcript is committed, not just its final output.** Criterion 4's "no second invocation" and every "the session was not told" claim are visible only in the tool-call record. *Rejected: keeping the final result text alone (cheaper, but it makes the two hardest criteria unbacked).*
- **D9. The round agent is a different session from the grounding session.** The grounding session must survive to be resumed for its second turn; the round agent must be killed. *Rejected: one session doing both (the kill would destroy the grounding session's resumability).*

## Architecture

### The goal

`work/orchestration/goals/cryo-volume-basis/` — `goal.md`, `trail.md`, `learnings.md`, copied from the templates. Question: should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held? Limits are restated explicitly in `goal.md` at the runbook defaults (retry 2, checkpoint 2, rounds 6) with no time limit — nothing is tightened to make the round end, because the owner gate ends it. Reserved gates: merge, push, item close, archive, plus any model or knowledge mutation beyond the goal directory. All operator-side content is marked `[AGENT]` — orchestrator-operationalized — never as owner intent (`align.md:36-40`).

### The ten runs and their roles

| # | Session | Mode / command | Given | Produces |
|---|---|---|---|---|
| 01 | Ground, turn 1 | `run-goal` skill, `ground` | question + consumer + repository | `goal.md` at `Status: draft` |
| 02 | Ground, turn 2 | resume of 01 | grounding evidence, invariants, limits, gates | `goal.md` at `Status: grounded` |
| 03–07 | Gate probes P1–P5 | `run-goal`, `round` | a goal hollow in one class, at the canonical path in a worktree | a refusal, or a started task |
| 08 | Round agent | `run-goal`, `round` | goal directory + repository + widened operator framing | strategy revision, T-001 scope, T-001 start, minted work item |
| 09 | Resumer | `run-goal` (sees start-without-return, routes to § Resuming an interruption) | goal directory + repository only | T-001 return, discovery row, T-002, `Round 1 result` |
| 10 | Reviewer | `run-goal`, `review` | goal directory + repository | `Round 1 review`, accepted learning delta |

Legality against ADR-002 and § What "fresh" means: session 10 authored no part of the round. Session 01/02 authored `goal.md` but not the round. Session 09 authored part of the round, so it cannot be 10. Sessions 03–07 wrote only into discarded worktrees.

**What a cold session may read.** Its brief names the goal directory, the runbook, and the repository, and states plainly: do not read `.project/active/goal-cold-pickup-proof/`. Enforcement is by instruction; **verification is by transcript** — every `Read` and `Grep` call is in the kept stream, so an auditor can check the prohibition held rather than take it on trust.

### The gate probe

Five variants are derived from the grounded `goal.md`, each hollowing exactly one field class: repository evidence, answer contract, invariants, limits, reserved gates. Each is committed inside its own worktree, and the probe session is asked to follow the runbook and start the first task. Whatever it does is the measurement: a refusal naming the missing class unprompted means the contract holds for that class; a started task — a `### T-001 scope` written into the worktree trail — is a recorded prose failure. The prediction is one refusal (grounding evidence, `GOAL_RUNBOOK.md:72`) and four pass-throughs. The probe's brief and its kept output are committed on the branch; the worktree is removed.

Nothing session 01 or 02 says about its own draft counts here, however apt — reviewing your own work is not a check (`GOAL_RUNBOOK.md:43`, `spec.md:40`). Such a remark is recorded in the probe record as context and marked as not satisfying the criterion.

`gate-probe-record.md` carries one row per class: class, variant path, session id, what the session did, verdict (`refused unprompted` | `refused on other grounds` | `started the task`), and the quoted line of session output that shows it. Because the runbook names no home for a refusal, the refusal lives in session output and nowhere else — that absence is itself a row in the record.

### The interruption

T-001's objective: route discovery row `20260823-magnet-technology-ab#2` to the modeling item its Home column names, under the "MFE Cost Modeling — Tokamak & Stellarator" epic. The round agent writes the scope, writes the write-ahead start line, and mints the item through `uv run agentic-mbse pm add-item`. The orchestrator runs session 08 in the background, polls `work/BACKLOG.md` for the new row, and terminates the process as soon as it appears.

State at the kill, committed before session 09 runs: the `### T-001 start` entry present, the minted row present in `work/BACKLOG.md`, no `### T-001 return`, no `### Stop`. The **unit** for Criterion 4 is the minted row's text and its SHA-256, recorded in `interruption-state.md` — not `work/BACKLOG.md` as a file, and not `DISCOVERY_LOG.md`, which the resumer has a legitimate reason to append to.

Session 09 gets the goal directory and the repository. Following § Resuming an interruption it reads native state as truth, sees the item already minted, walks the cited refs for external mutation, and appends the `### T-001 return` — plus the joined disposition row under `20260823-magnet-technology-ab#2`, which is what completes the routing. It then scopes T-002, hits the model-mutation gate, returns `OWNER_GATE`, and writes the `### Round 1 result`, deriving the stop reason from the last outcome plus the goal's limits.

### The seed

`seed-record.md`, committed before session 08 runs (and therefore before session 10): the drift's identity — the strategy revision widens the round's frame from `vol_cold_cryo` to the package's held cryo inputs generally, past what `goal.md` § Question and § Invariants authorize — the mechanism (the operator's framing in session 08's brief), and the detection expected of the reviewer: it names the widening under goal-and-strategy fidelity or task scope, and corrects the learning delta back to `vol_cold_cryo` before it lands in `learnings.md`.

After session 10 completes, a dated `### Amendment` is appended to the kept `trail.md` disclosing that one drift was seeded for this proof and that five throwaway gate-probe variants were derived from this goal, citing `verification_record.md`. Post-review only, so it cannot spoil the test.

## The commit sequence

Every ordering predicate in the spec is carried here. An auditor checks each with `git merge-base --is-ancestor <earlier> <later>`.

| # | Commit | Carries |
|---|---|---|
| C01 | item scaffolding: `sessions/`, `freshness-record.md`, `operator-notes.md`, `verification_record.md` skeletons | — |
| C02 | session 01 brief | before 01 runs |
| C03 | session 01 transcript + output; `goal.md` at draft | — |
| C04 | session 02 brief | before 02 runs |
| C05 | session 02 transcript + output; `goal.md` grounded; operator-notes entry | — |
| C06 | session 03–07 briefs; the five variants as kept fixtures | before any probe runs |
| C07–C11 | one commit per probe: transcript, output, `gate-probe-record.md` row | — |
| C12 | `gate-probe-record.md` closed, five verdicts | **before any `### T-001 scope`** |
| C13 | `seed-record.md`; session 08 brief | **before 08 and before 10** |
| C14 | session 08 transcript + output; interrupted trail state; minted row; `interruption-state.md` with the pre-resume hash | **ancestor of every session-09 commit** |
| C15 | session 09 brief | before 09 runs |
| C16 | session 09 transcript + output; T-001 return, discovery row, T-002, round result; post-resume hash | — |
| C17 | session 10 brief | before 10 runs |
| C18 | session 10 transcript + output; `### Round 1 review`; `learnings.md` entry | — |
| C19 | post-review `### Amendment` in `trail.md` | after 10 |
| C20 | `freshness-record.md` closed; `operator-notes.md` complete; `verification_record.md` | — |

## Component Overview

All under `.project/active/goal-cold-pickup-proof/` unless stated.

- **`sessions/NN-<role>/`** — `brief.md` (the one committed input), `transcript.json` (full stream copied out of the gitignored `.orchestrate-logs/`), `output.md` (final result text), `meta.md` (session id, command, cwd, start and end times, exit status, whether the session was terminated).
- **`freshness-record.md`** — one row per run with its brief path, transcript path, and session id, plus a closing statement in plain words that no other input existed: no context injection, no prior turn beyond run 02's recorded resume of session 01, no verbal hint from the operator. The enumeration is explicitly closed — it states that these ten runs are all the runs there were, discarded attempts included. Criteria 2, 4, and 8 rest on this.
- **`gate-probe-record.md`** — the five-class table described above.
- **`seed-record.md`** — drift identity, planting mechanism, expected detection.
- **`interruption-state.md`** — the interrupted artifact's identity, its text, and its SHA-256 before and after session 09; the transcript line-references showing session 09 made no second minting call.
- **`operator-notes.md`** — the orchestrator's notes from its own side of the exchange `[OWNER]`-requested (`align.md:36-40`). Per session: what the operator was asked for, what the runbook did not prompt for and the operator had to supply unasked, where the dialogue stalled, and any point where the operator had to choose between two readings of the runbook. Written turn by turn as the run proceeds, never reconstructed at the end.
- **`verification_record.md`** — the epic's verification record and the proof report under one name. Concise, reads as a verdict.
- **`work/orchestration/goals/cryo-volume-basis/`** — the goal itself, which stays.
- **One new modeling work item** under `work/BACKLOG.md`, minted by session 08 and staying.
- **One appended row** in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under `20260823-magnet-technology-ab#2`.

## Required Invariants

1. Every cold session has exactly one brief, and its commit is an ancestor of the commit carrying that session's output.
2. No cold session's transcript contains a read of `.project/active/goal-cold-pickup-proof/`.
3. `work/orchestration/goals/` contains exactly one directory when the item closes.
4. The minted work item's row text and hash are identical before and after session 09.
5. No `### T-00N return` and no `### Stop` exists in `trail.md` at C14.
6. No first-sighting row in `DISCOVERY_LOG.md` is edited, and no id is minted.
7. Nothing under `work/orchestration/GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, or `.project/adr/` changes on this branch.
8. `learnings.md` gains its entry only in C18, in the same commit as the review that accepted it.

## Non-Goals

- Repairing the runbook, the templates, or the ADRs. Measured shortfalls are evidence under the owner's hardening rule, and the repair is Item 1's.
- Solving the `vol_cold_cryo` finding. The round mints the item and stops at the gate.
- Using Item 2's research seam or Item 3's integration seam.
- Any dispatch, concurrency, or hardening machinery. ADR-003 bars the first two as premises; the third is what this run is evidence about.
- Grading the proof against a predicted outcome. If the gate holds on all five classes, or on none, the record says so.

## Implementation Notes

- `.orchestrate-logs/` is gitignored. A transcript is not evidence until it is copied into `sessions/NN-<role>/` and committed. Copy it in the same step that runs the session, before anything else touches the tree.
- Transcripts are large — the sampled logs run from 60 KB to 1.7 MB. Ten of them is real repository weight, accepted deliberately under D8. Briefs should keep sessions tight.
- Sessions 03–07 run **sequentially**, one worktree at a time. Parallel probes would be concurrency, which ADR-003 bars as a premise.
- Worktrees land beside the repo as `../fusion-tea-gate-pN`, never under `.claude/worktrees/`.
- The kill in session 08 is a process termination, not an instruction. Poll `work/BACKLOG.md`; terminate on the row's appearance; then verify the trail state matches C14's requirement before committing.
- If the kill lands late — a `### T-001 return` already written — the attempt is discarded, disclosed in `verification_record.md`, and re-run with a tighter poll. A discarded attempt is still enumerated in the freshness record.
- Operator-side content in `goal.md` is `[AGENT]`. Only lines tracing to `align.md` owner decisions carry `[OWNER 2026-08-26]`.

## Potential Risks

- **The kill misses the window (B1).** Mitigation: short poll interval, and a brief that puts the minting call late in the task. Fallback: discard and re-run, disclosed.
- **`orchestrate-stage.sh` will not run with a worktree as its working directory.** This is the one mechanism fact this design could not verify — the script is outside the session's readable paths. Mitigation: verify it in the plan's first step, before any probe. Fallback, if it will not: run the five variants sequentially at the canonical path on the branch, each committed and then removed in a disclosed cleanup commit before the round opens. Ordering is unaffected either way, because the probe's *kept output* carries the ancestry, not the variant.
- **A probe session reads the fixture as a fixture (B2).** Mitigation: neutral variant construction — hollow the class, change nothing else, keep the slug real. The transcript shows whether the session reasoned about the file being odd.
- **The round agent flags the widened frame instead of carrying it (B4).** That is a real result, not a failure of the run: it means the contract resisted the drift at the writer rather than the reviewer. Record it and note that Criterion 8 was not exercised as designed.
- **Minting the work item is judged to cross the reserved gate (B3).** The design's reading is that PM state is neither a model nor a knowledge mutation. If the reviewer or the owner reads it the other way, the interruption evidence is tainted and the run needs a different native target. This is flagged deliberately rather than assumed away.

## Integration Strategy

The goal directory, the minted work item, and the appended discovery row are permanent. They enter their own systems through their own operations: the modeling PM mints its item through `agentic-mbse pm add-item`, and the goal round appends its disposition row under an existing id. Nothing crosses the `.project/` ↔ `work/` seam except by citation (ADR-006). The proof adds no tooling, no script, and no template — the whole point is that the shipped prose was the only mechanism.

## Validation Approach

`verification_record.md` carries one row per spec criterion: the criterion, who checks it, the paths checked, the check itself (a `git merge-base` invocation, a hash comparison, a named heading, or a quoted line of session output), and the verdict. Two rules keep it honest.

- **Ordering criteria are checked by ancestry, never by mtime or file order.** Criterion 2 → C12 before the first `### T-001 scope` commit. Criterion 4 → C14 before C16. Criterion 8 → C13 before C17.
- **The orchestrator writes the record; it does not certify it.** A fresh audit session re-runs every row against disk. Criterion 2 is the one row the orchestrator could not check even in principle, and it is already settled: the enforcer is a separate fresh session, and the orchestrator never plays the refusing role.

Criteria 1, 3, 5, 6, 7 are read off the goal directory and `DISCOVERY_LOG.md`. Criterion 3 gets its own check: a reader given only `work/orchestration/goals/cryo-volume-basis/` and the repository names the strategy, the one task, the gate state, and the native evidence. Criterion 9 is the report's own content — every ambiguity, misreading, and failure, with the session output that shows it, and either a named hardening mechanism with the recorded failure that promotes it, or a plain statement that none is proposed.

## Next-Stage Handoff

**Fixed.** The ten-session map and their roles. Evidence in the item directory, never the goal directory. Five per-class probes in worktrees. The interrupted artifact is the minted work item; the discovery row is the resumer's. Two tasks, closing on an unresolved owner gate. The seeded drift's identity. The twenty-commit sequence.

**Open for the plan.** The goal's exact question wording and `Answered when` condition, which session 01 co-develops with the operator rather than receiving. The minted work item's name and scale. The poll interval for the kill. Whether session 09 needs a resume turn.

**De-risk first.** Confirm `orchestrate-stage.sh` accepts a worktree working directory and that its transcript records tool calls with arguments. Both are load-bearing — the first for D3, the second for B5 — and both are cheap to check with one throwaway session before C02.

---

**Next Step:** After design review → `/_my_plan`.
