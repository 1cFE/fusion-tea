# Design: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Status:** Draft (revised after `design-review.md`, verdict Revise)
**Owner:** Reid W
**Created:** 2026-08-26
**Updated:** 2026-08-26
**Branch:** `feat/goal-integration-seam` (no child branch)
**Base commit:** `78e03edf`

---

## Overview

Run one real goal — `cryo-volume-basis` — through Item 1's shipped contract as a sequence of headless cold runs, and keep the input, the output, and the commit order of every one of them as the proof.

## Related Artifacts

- **Spec:** `.project/active/goal-cold-pickup-proof/spec.md` (Approved after review)
- **Spec review:** `spec-review.md`; dispositions `briefs/spec_fix.md`
- **Design review:** `design-review.md` (verdict Revise, 2026-08-26); dispositions `briefs/design_fix.md`. All four Critical and seven Major findings are incorporated in this revision.
- **Align record:** `align.md`
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 4
- **Contract under test:** `work/orchestration/GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, `.claude/skills/run-goal/SKILL.md`
- **Decision records:** ADR-001 through ADR-007 (`.project/adr/`)
- **Grounding chain for the proof goal:** `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:20`, `knowledge/KNOWLEDGE.md` DI-010, `work/completed/20260822_WI-031_research-round-item6-values/`

## The Point

Item 1 shipped a goal layer that nobody but its author has ever used. Three bets carry the epic's critical path on that layer, and all three are untested: a stranger can ground a goal and cannot start an ungrounded one; a fresh session can resume an interruption from disk; a fresh reviewer catches drift and settles the learning delta.

The obligation that makes this urgent is the owner's, and it is a bar, not a wish: **none of the five hardening mechanisms — envelope YAML, event ledger, digests, idempotency keys, reconciliation — enters the first build unless a recorded proof run demonstrates that the prose/native-facts route failed** `[OWNER]` (`goal-strategy-task-harness-design-review.md:209`, carried as the epic's Hardening rule). Concurrent runs and unattended dispatch are not on that list; ADR-003 bars them outright as premises, and no evidence this item produces can promote them.

So this run is the only admissible evidence in either direction. Without it there is nothing to promote a mechanism on, and equally nothing that justifies leaving the prose route alone. This design's job is to make the run *count* — to produce evidence an auditor who did not watch it can verify from files alone. Everything below exists for that one purpose. This item records failures; it does not repair them.

## Research Findings

**The contract under test.** `GOAL_RUNBOOK.md` § The five surfaces fixes the three goal files and their location (`:23-35`). § What "fresh" means defines the session boundary (`:37-62`). § Running one task fixes the scope → start → work → return order and the six return outcomes (`:103-134`). § Opening and closing a round gives the six close triggers (`:84-91`). § Resuming an interruption gives the four-step resume order, its two permitted writes, and "the native artifact is the truth" (`:208-219`). § The discovery log gives the round's write outside its own directory and the no-mint rule (`:232-244`). The templates carry the headings; `trail.md`'s template carries the five decision fields (`trail.md:43`).

**The cold-run mechanism.** `~/.claude/scripts/orchestrate-stage.sh` runs one stage headless as `claude -p`, returns `{session_id, result, cost, is_error}`, and writes a full stream-json transcript (`.project/research/20260822-120756_research-extraction-harness.md:81`, P7 at `:137`). A sampled log confirms the transcript is a JSON array of `system|user|assistant|result` events carrying `session_id`, `cwd`, the tool list, the initial prompt, every tool call, and the final result text. Three mechanism facts settle the design:

- There is **no cwd flag**. `claude -p` runs in the caller's working directory, so a worktree is entered by invoking the runner from it (orchestrator-resolved fact).
- `--log-dir` selects where the transcript lands; it **defaults relative to the caller's cwd**, which is why the default is unusable here (see § The freshness fence).
- **Resume by session id is real and in routine use** — `.orchestrate-logs/` already holds 74 files named `resume-<session-id>-<timestamp>.json` (verified at review).

**The grounding chain the proof goal rests on.** Discovery row `20260823-magnet-technology-ab#2` is live and `unrouted`, and its Home column already names where it belongs: "modeling item under the MFE cost modeling epic" (`DISCOVERY_LOG.md:20`). DI-010 gives the winding-pack current densities and states in its own model implications that the pack volume "should enter `vol_cold_cryo`". `work/BACKLOG.md:24` carries the epic. So the round's routing task has a real destination and a real citation chain, not a fixture.

**`add-item` rewrites the whole backlog file.** `agentic_mbse/pm/operations.py:962-995` re-serializes all of `work/BACKLOG.md` on every call. This is why the interruption's non-repetition check is row-scoped, not a file diff.

**Where the runbook is silent or self-contradicting, measured before the run.** A draft goal has no open round, so `trail.md` has no heading under which a refusal could be written; the runbook names no home for one. § Resuming an interruption tells the resumer what to write but not who owns the round afterwards, while ADR-002 says a round is one agent's. And `:234` says a round has exactly one write outside its own directory while `:244` routes a finding to a native work item through the owning PM. All three are recorded as evidence, not repaired here.

## Core Concept

The proof is a **stack of cold runs whose order is carried by git commits, not by anyone's account of what happened.** Each run gets exactly one brief, that brief is committed before the run starts, the run's full transcript and final output are committed after and before the next dependent run starts, and the freshness record enumerates every run that happened — kept and discarded — and closes the enumeration with a statement. Closure is a *statement about completeness*, not a fixed count: the run count is not sacred and moves with what the exchange needs. An auditor checks ordering with `git merge-base --is-ancestor` and checks content by reading files.

The run those cold sessions execute is one honest round on one real question: should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`? The round routes the discovery row that raised it by minting the modeling work item the row's Home column already names, then tries to look at the model, hits the owner's model-mutation gate, and closes on an unresolved owner gate. No pin, no study, finding unsolved. That is a legitimate empty round, and it is the shape the proof needs.

Four hard parts each get one mechanism, and each exists to make evidence checkable rather than to make the run smoother:

- **The freshness fence has to be structural, not a single denial.** Every cold run writes its transcript outside the repository tree, and what a session may read is stated as an allowlist.
- **Per-class gate measurement needs five drafts, not one.** A draft hollow in all five field classes only tells you which class a session noticed first. Five probes run, each against a goal hollow in exactly one class, each in a throwaway worktree.
- **A genuine interruption cannot be instructed.** A session told to stop writes the handoff stop the runbook tells it to write, and a recorded stop fails Criterion 4. The round agent is killed after its native effect lands and before its return.
- **Nothing downstream of the kill is told what to do.** The resumer does exactly what § Resuming an interruption authorizes and no more; a separate continuation session picks up after it. Whatever each one chooses is the measurement, not a step the brief scripted.

And one seeded drift rides upstream of the writer: the orchestrator plays the operator, and the drift is in the operator's framing of the round.

## The freshness fence

The runner writes its transcript to `--log-dir`, defaulting to `./.orchestrate-logs` relative to the caller's cwd — the repository root. That directory exists today and holds 74 transcripts, including this item's own spec, spec-review, and design stages. A cold session run at the repo root could read the spec, the seeded drift, and the orchestrator's reasoning while honestly obeying an instruction that named only the item directory. The fence must therefore be two things at once.

**Structural.** Every cold run passes `--log-dir` to a path **outside the repository tree** — `~/goal-proof-logs/NN-<role>/`. Immediately after each run the orchestrator copies the transcript from there into `sessions/NN-<role>/` and commits it before the next dependent run starts. Nothing this proof produces is ever written inside the tree a later cold session can read.

**An allowlist, not a denial.** Each brief states what the session **may** read: the goal directory, `GOAL_RUNBOOK.md` and the templates, `.claude/skills/run-goal/`, `.project/adr/`, and the native repository — models, knowledge, `work/`, `exploration/`. Then it names the explicit denials: `.project/active/goal-cold-pickup-proof/` and **any orchestration log directory**, including `.orchestrate-logs/` anywhere in the tree and `~/goal-proof-logs/`. The pre-existing `.orchestrate-logs/` at the repo root is forbidden territory for every cold session.

**Verified by transcript.** Every `Read`, `Grep`, `Glob`, and `Bash` call is in the kept stream, so an auditor checks the fence held rather than taking it on trust. Required Invariant 2 covers both denials.

## The surfaced conflict: one write outside the goal directory, or two?

`GOAL_RUNBOOK.md:234` states flatly that "A goal round has exactly one write outside its own directory, and this is it" — the discovery log. Ten lines later, `:244` routes a finding that is work to "a native work item through the owning PM." The proof's native target is `uv run agentic-mbse pm add-item`, which writes `work/BACKLOG.md`. Under `:234` that is a second write and is barred; under `:244` it is the prescribed home. **The runbook contradicts itself, and this run is the one that finds it.**

Per capture-fidelity rule 4 this is surfaced, not resolved silently. It is recorded as measured Item 1 evidence in the orchestrator's run summary and in `verification_record.md`, in the same register the spec uses for the grounding-gate prediction (`spec.md` § A predicted prose failure).

The design then proceeds under a recorded reading, `[AGENT]`: **`:234` binds the goal layer's own pen** — the goal directory plus the discovery log are the only files the round writes *as the goal layer*. A task that invokes the owning PM's own operation is native work done by the native workflow, which is what the layer exists to do (§ What this is: "The goal layer decides what to work on next and what the evidence means. It does not do the work"). Challenge this reading by re-deriving against those two sections, not by asking the owner.

**Contingency, stated in advance.** If the cold round agent reads `:234` restrictively and refuses to mint, that refusal is itself recorded prose-ambiguity evidence — arguably the more valuable result. The operator then resolves it in-session: a kept, transcripted operator clarification delivered as a resume turn of the same session, enumerated in the freshness record like any other run, after which the task proceeds. **No silent resolution in either direction**, and no brief pre-empts the agent's reading.

This is distinct from the goal's own reserved gate, which is B3 below. The reserved gate reads "any model or knowledge mutation beyond the goal directory"; `work/BACKLOG.md` is PM state and is neither, so the gate passes on plain wording. Two different rules, two different verdicts, both recorded.

## Key Bets

- **B1.** The kill can be landed between the native effect and the return — the write-ahead line and the minted row are both observable the moment they complete, and a short poll catches the window before the session writes its return. *If false → no genuine interruption; Criterion 4 needs repeated re-runs, each burning a cold session.*
- **B2.** A goal hollow in exactly one field class, sitting at the canonical path in an ordinary-looking repository, reads to a cold session as a real goal. *If false → the per-class record measures the fixture's tells, not the shipped contract, and Criterion 2 is contaminated.*
- **B3.** Minting a modeling work item through the modeling PM does not trip the *goal's reserved gate* — it is PM state, not a model or knowledge mutation. *If false → the round crossed a reserved gate to produce its interruption, and the interruption evidence is tainted at the root.*
- **B4.** An operator framing one notch wider than `goal.md` propagates into the round agent's written strategy revision without the agent flagging it. *If false → no drift is planted, and Criterion 8 has nothing to catch.*
- **B5.** The stream-json transcript survives process termination and records tool calls with arguments, so "the session was not told" and "the resumer made no second minting call" are both readable. *If false → D8's justification and Criterion 4's non-repetition evidence both collapse to the artifact hash alone.*
- **B6.** The cold round agent reads `GOAL_RUNBOOK.md:244` as authorizing the mint, so the native effect lands. *If false → no interruption to resume; the run falls to the § surfaced conflict contingency and costs one operator round-trip.*
- **B7.** A round left open by an interruption can be picked up by a further fresh session and carried to a written result. *If false → Criteria 5 and 6 have no evidence, and the runbook's silence on who owns an interrupted round is the finding instead.*

## Key Decisions

- **D1. Cold sessions run headless through `orchestrate-stage.sh run`, one `run` per turn, resumed by session id where a role needs several turns.** A fresh session per `run` is exactly the boundary § What "fresh" means requires, and the runner produces a session id and a full transcript. Resume-by-id is verified in routine use. *Rejected: interactive sessions (no kept input record; the session boundary would rest on the operator's word).*
- **D2. All cold-run evidence lives in the item directory, never the goal directory, and never inside the repository while a cold run is live.** `sessions/NN-<role>/`, with `--log-dir` outside the tree. The goal directory must survive as the first real goal, readable as a goal and not as a test fixture. *Rejected: an `evidence/` subdirectory under the goal (Criterion 3 would fail on its own artifact); the runner's default log directory (C-1's leak).*
- **D3. Five gate probes, one field class each, in throwaway worktrees on throwaway branches.** Per-class measurement is the criterion; one draft cannot produce it. *Rejected: one draft hollow in all five classes; five draft goal directories committed at the canonical path on the branch (junk in `work/orchestration/goals/`, which Criterion 3 reads).*
- **D4. The interrupted task's native effect is a modeling work item minted through the modeling PM.** The row's own Home column names the modeling item, so minting it is honest routing rather than a fixture write. *Rejected: the disposition row as the interrupted artifact (a later session has a legitimate reason to append rows, so the unit and the noise would be the same file); a model or knowledge file (crosses the reserved gate).*
- **D5. The round runs to an unresolved owner gate.** The task after the routing asks whether the model can derive `vol_cold_cryo`, reaches the point where a model file would have to change, and returns `OWNER_GATE`. *Rejected: closing on a declared limit (a limit tightened to make the round close is a fixture, and the owner gate is already real).*
- **D6. The resumer does exactly what § Resuming an interruption authorizes, and its brief says nothing about who owns the round afterwards.** Inspect native facts, walk cited refs, append the correct return **or** a `### Stop` of kind `interruption`. Either outcome satisfies Criterion 4; which one it picks is the measurement. The brief does not tell it to inherit the round, because a brief that did would repair Item 1's silence by instruction and then report the repair as a finding. If the operator has to respond to what the resumer does, that response is recorded in `operator-notes.md` as **operator judgment**, `[AGENT]`, never as a contract repair. *Rejected: instructing inheritance (fills the gap it claims to measure); leaving the outcome unplanned (costs four criteria if the resumer stops).*
- **D7. A separate fresh round-continuation session picks up from the trail and closes the round.** It receives the goal directory and the repository and is asked to continue the goal per the runbook; it decides for itself what the open round needs. The ADR-002 one-agent-per-round tension this creates — three agents inside one round — is **recorded as measured evidence of the contract under interruption, not patched**. *Rejected: the resumer continuing (D6's reason); leaving the round unclosed (Criteria 5, 6, 8 unbacked).*
- **D8. The seeded drift is a widened strategy frame, planted in the operator's brief to the round agent.** `goal.md` binds the goal to `vol_cold_cryo`; the operator brief frames the round's interest as "the held cryo inputs in this package, starting with `vol_cold_cryo`". It lands in the Round 1 strategy revision, so it survives the interruption and is still there for the reviewer. *Rejected: a comparison-meaning drift (no study, so comparison meaning is thin ground); planting it by editing the trail after the fact (the round's written material must be the agents').*
- **D9. Every cold run's full stream-json transcript is committed, not just its final output.** Criterion 4's non-repetition and every "the session was not told" claim are visible only in the tool-call record. *Rejected: keeping the final result text alone (cheaper, but it makes the two hardest criteria unbacked).*
- **D10. The round agent, the resumer, the continuation session, the reviewer, and the standalone reader are five different sessions.** Forced by § What "fresh" means, by the kill, and by Criterion 3's "no operator transcript" condition. *Rejected: reusing the reviewer as the standalone reader (it has already been handed the round's material, and "stands alone" is a different question from the review's eight checks).*

## Architecture

### The goal

`work/orchestration/goals/cryo-volume-basis/` — `goal.md`, `trail.md`, `learnings.md`, copied from the templates. Question: should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held? Limits are restated explicitly at the runbook defaults (retry 2, checkpoint 2, rounds 6) with no time limit — nothing is tightened to make the round end, because the owner gate ends it. Reserved gates: merge, push, item close, archive, plus any model or knowledge mutation beyond the goal directory. All operator-side content is marked `[AGENT]` — orchestrator-operationalized — never as owner intent (`align.md:36-40`).

### The runs and their roles

Runs are numbered `NN` in execution order. The grounding role takes as many turns as the exchange needs; every turn is its own run with its own committed brief and kept transcript. The count is not fixed in advance and the freshness record enumerates whatever happened.

| Run | Role | Session | Mode / command | Given | Produces |
|---|---|---|---|---|---|
| 01…0k | Grounding, turns 1…k | one session, resumed | `run-goal`, `ground` | the operator question, then whatever the exchange calls for | `goal.md` from `draft` to `grounded` |
| next 5 | Gate probes P1–P5 | five fresh | `run-goal`, `round` | a goal hollow in one class, at the canonical path in a worktree | a refusal, or a started task |
| next | Round agent | fresh | `run-goal`, `round` | goal directory, repository, widened operator framing | strategy revision, T-001 scope, T-001 start, minted work item — then killed |
| next | Resumer | fresh | `run-goal` (routes itself to § Resuming an interruption) | goal directory and repository only | a `### T-001 return` **or** a `### Stop — interruption` |
| next | Round continuation | fresh | `run-goal` | goal directory and repository only | remaining tasks, the discovery row(s), `### Round 1 result` |
| next | Reviewer | fresh | `run-goal`, `review` | goal directory and repository | `### Round 1 review`, accepted learning delta |
| last | Standalone reader | fresh | generic, pointed at the goal directory | **only** `work/orchestration/goals/cryo-volume-basis/` and the repository | a written answer naming strategy, task, gate/limit state, native evidence |

Legality against ADR-002 and § What "fresh" means: the reviewer authored no part of the round. The grounding session authored `goal.md` but not the round. The round agent, resumer, and continuation session each authored part of the round, so none of them can review it. The standalone reader runs last, writes nothing into the goal, and cannot contaminate the review it follows.

### The gate probe

Five variants are derived from the grounded `goal.md`, each hollowing exactly one field class. The mapping to template headings is fixed here so the plan can build them:

| # | Field class | Heading hollowed | Everything else |
|---|---|---|---|
| P1 | repository evidence | § Grounding evidence | filled, **including `Status: grounded`** |
| P2 | answer contract | § Answered when | filled, § Question and § Consumer intact |
| P3 | invariants | § Invariants | filled |
| P4 | limits | § Limits | filled |
| P5 | reserved gates | § Reserved gates | filled |

**P1's construction is a deliberate choice.** The template couples § Grounding evidence to § Status ("Empty means `draft`"), and the shipped rule is that a draft goal authorizes no task (`GOAL_RUNBOOK.md:72`). If P1 also carried `Status: draft`, the refusal would be triggered by a one-word flag and the probe would measure whether a session reads `Status`, not whether the gate reaches the grounding-evidence class. So P1 leaves `Status: grounded` with the evidence section empty. The file is internally inconsistent in a way no real goal would be — that strains B2 for this variant specifically, and `gate-probe-record.md` carries a column for the tell. A refusal that names the inconsistency rather than the missing class is recorded as `refused on other grounds`, which does not satisfy Criterion 2.

**Expected shapes.** P1 is the one predicted pass — the only class the shipped gate defends. P2–P5 are four predicted failures: nothing in the runbook refuses a goal for a missing answer contract, missing invariants, missing limits, or missing reserved gates. A prediction is not a grade; whatever the five sessions do is the record.

**Mechanics per probe**, given that the runner has no cwd flag and its log directory defaults relative to cwd:

1. `git worktree add ../fusion-tea-gate-pN -b gate-pN` from the branch head.
2. Write the variant into the worktree at the canonical path and commit it **on the throwaway branch**.
3. Run the probe from inside the worktree with `--log-dir ~/goal-proof-logs/NN-gate-pN/` — outside both trees.
4. Copy transcript and output into `sessions/NN-gate-pN/` in the **main** tree; commit there.
5. `git worktree remove --force ../fusion-tea-gate-pN` and `git branch -D gate-pN`.

Nothing probe-related is committed on `feat/goal-integration-seam` except the briefs, the kept outputs, and the variant drafts as fixtures under `probes/pN/goal.md`. Required Invariant 3 depends on this. Probes run **sequentially**, one worktree at a time — parallel probes would be concurrency, which ADR-003 bars as a premise.

`gate-probe-record.md` carries one row per class: class, heading, fixture path, session id, what the session did, verdict (`refused unprompted` | `refused on other grounds` | `started the task`), the construction tell, and the quoted line of session output that shows it. Because the runbook names no home for a refusal, the refusal lives in session output and nowhere else — that absence is itself a row in the record. Nothing the grounding session says about its own draft counts here, however apt; reviewing your own work is not a check (`GOAL_RUNBOOK.md:43`, `spec.md:40`).

### The interruption

T-001's objective: route discovery row `20260823-magnet-technology-ab#2` to the modeling item its Home column names, under the "MFE Cost Modeling — Tokamak & Stellarator" epic. Routing is two steps — mint the item, then append the joined disposition row — and only the first has landed at the kill. That is deliberate: it leaves the resumer a genuine judgment call rather than a formality.

**The kill.** The orchestrator runs the round-agent session in the background and polls for **both** conditions: the `### T-001 start` line present in `trail.md`, and the minted row observable in `work/BACKLOG.md`. On seeing both it sends `kill -TERM -<pgid>` to the child **process group** — terminating the wrapper alone does not necessarily stop the `claude` child, and a surviving child would write the return after C14 is committed, producing exactly the clean-boundary state the spec excludes. After the signal the orchestrator verifies no `claude` process remains before committing anything. The transcript is copied out of `~/goal-proof-logs/` **regardless of kill timing** — a truncated transcript is still evidence, and a missing one is a finding about the runner.

**Three abort rules**, because the kill window has three ways to miss:

- *A `### T-001 return` is already written.* Abort the attempt, discard it, re-run with a tighter poll.
- *The minted row is present but no `### T-001 start` line is.* Criterion 4 requires the write-ahead. Abort and re-run — **and record it as a measured prose failure**: the round agent minted before writing the write-ahead line the runbook puts first.
- *The mint and the return arrive in one observation window.* Nothing stops an agent issuing the `add-item` call and the trail write in one turn. Same abort rule. The mitigation — a brief that names the expected artifact in the start line, making the write-ahead a described precondition of the mint — is probabilistic, which B1 already concedes.

Every aborted attempt is enumerated in the freshness record with its transcript and its abort reason. Nothing is hidden.

**The unit.** For Criterion 4 the unit is the minted row's text and its SHA-256, recorded in `interruption-state.md` before and after the resume. `add-item` re-serializes the whole of `work/BACKLOG.md` on every call, so **a whole-file diff is not the check and a whole-file change does not violate Required Invariant 4.** The check is row-scoped: the work item's row exists exactly once, with unchanged text and hash, and the transcript shows no second `add-item` invocation.

### After the kill

**The resumer** gets the goal directory and the repository and nothing else. Following § Resuming an interruption it reads native state as truth, sees the item already minted, walks the cited refs for external mutation, and writes one of the two things that section authorizes: the missing return, or a `### Stop` of kind `interruption`. It does not finish T-001's remaining work, because the runbook does not authorize that, and its brief says nothing about who owns the round afterwards.

The likely outcome is the Stop — the native evidence shows the mint landed but the routing objective unmet — and that is a first-class result, not a failure of the run. Either way Criterion 4 is satisfied: the spec asks for "either the correct return or a `### Stop` of kind `interruption`" (`spec.md:46`).

**The continuation session** then picks up the open round from the trail. It decides what the round needs: completing the routing with the joined disposition row under `…-ab#2`, then the task that asks whether the model can derive `vol_cold_cryo`, which reaches the model-mutation gate and returns `OWNER_GATE`, closing the round on trigger 4. It writes the `### Round 1 result`, deriving the stop reason from the last outcome plus the goal's limits. If its reading also touches rows `…-ab#1`, `#3`, or `#4` — all `model`-kind, all `unrouted`, and `#1` and `#3` sit in the same magnet/cost chain — each touched row gets its own joined disposition row. Criterion 7 covers every touched row, not just the grounding row, and the reviewer will check for them.

*Contingency:* if the continuation session hands back without writing a result, that is measured evidence about the contract under interruption, and one further continuation run is enumerated and briefed the same way. The design does not script the outcome; it budgets for the honest ones.

**Expect the T-001 decision record to be thin, and say so.** The round agent made goal-level decisions before the kill that no return will ever carry — its return was never written. Whoever writes T-001's return records *their own* decisions, not the killed session's. Criterion 6 asks that every goal-level decision the round made carries five fields (`spec.md:49`), so this is a real shortfall, and it is itself measured evidence about what an interruption costs the replay record.

### The seed

`seed-record.md`, committed before the round-agent run and therefore before the review run: the drift's identity — the strategy revision widens the round's frame from `vol_cold_cryo` to the package's held cryo inputs generally, past what `goal.md` § Question and § Invariants authorize — the mechanism (the operator's framing in the round agent's brief), and the detection expected of the reviewer: it names the widening under goal-and-strategy fidelity or task scope, and corrects the learning delta back to `vol_cold_cryo` before it lands in `learnings.md`.

After the review completes, a dated `### Amendment` is appended to the kept `trail.md` disclosing that one drift was seeded for this proof and that five throwaway gate-probe variants were derived from this goal, citing `verification_record.md`. Post-review only, so it cannot spoil the test.

## The commit sequence

Every ordering predicate the spec names (`spec.md:35`) is carried here. An auditor checks each with `git merge-base --is-ancestor <earlier> <later>`. Phases with a variable number of runs commit one brief and one output commit per run.

| Phase | Commits | Carries |
|---|---|---|
| 0 | C01 item scaffolding: `sessions/`, `probes/`, the five records as skeletons | — |
| 1 | per grounding turn: brief commit, then transcript + output + `goal.md` state | brief before its run; last commit carries `Status: grounded` |
| 2 | one commit for all five probe briefs and the five variant fixtures; then one commit per probe (transcript, output, record row); then `gate-probe-record.md` closed | briefs before any probe runs; **record closed before any `### T-001 scope` commit** |
| 3 | `seed-record.md` + round-agent brief; then round-agent transcript, interrupted trail state, minted row, `interruption-state.md` pre-hash | seed before the round agent **and** before the review; **the interrupted-state commit is an ancestor of every resumer commit** |
| 4 | resumer brief; then resumer transcript, output, its trail entry, post-resume hash | brief before its run |
| 5 | continuation brief; then continuation transcript, remaining tasks, discovery rows, `### Round 1 result` | brief before its run |
| 6 | reviewer brief; then reviewer transcript, `### Round 1 review`, `learnings.md` entry | brief before its run |
| 7 | standalone-reader brief; then its transcript and written answer | brief before its run; runs after the review |
| 8 | post-review `### Amendment` in `trail.md`; then `freshness-record.md` closed, `operator-notes.md`, `verification_record.md` | — |

## Component Overview

All under `.project/active/goal-cold-pickup-proof/` unless stated.

- **`sessions/NN-<role>/`** — `brief.md` (the one committed input), `transcript.json` (copied from `~/goal-proof-logs/NN-<role>/`), `output.md` (final result text), `meta.md` (session id, command, cwd, log dir, start and end times, exit status, whether the run was terminated and by what signal, and whether it was kept or discarded).
- **`freshness-record.md`** — one row per run: role, brief path, transcript path, session id, kept or discarded with its reason. It closes with a statement in plain words: *these N runs, kept and discarded, are all the runs there were; no other input existed* — no context injection, no prior turn beyond the recorded grounding resumes, no verbal hint from the operator. Completeness is the claim; the count is just what the enumeration happened to reach. Criteria 2, 4, and 8 rest on this.
- **`probes/pN/goal.md`** — the five variant fixtures, kept so an auditor can see exactly what each probe faced.
- **`gate-probe-record.md`** — the five-class table described above.
- **`seed-record.md`** — drift identity, planting mechanism, expected detection.
- **`interruption-state.md`** — the minted row's text and SHA-256 before and after the resume, the transcript line-references showing no second `add-item` call, and the note that a whole-file `work/BACKLOG.md` diff is not the check.
- **`operator-notes.md`** — the orchestrator's notes from its own side of the exchange, `[OWNER]`-requested (`align.md:36-40`): what the grounding dialogue asked, where it stalled, what the operator had to supply that the runbook did not prompt for. Written by the orchestrator **after the exchange, from the kept transcripts**, and graded `[AGENT]`. It states plainly what the headless mechanism could and could not show (see below), and it records any operator response to the resumer's or continuation session's behavior as operator judgment, not as a contract repair.
- **`verification_record.md`** — the epic's verification record and the proof report under one name. Concise, reads as a verdict.
- **`work/orchestration/goals/cryo-volume-basis/`** — the goal itself, which stays.
- **One new modeling work item** in `work/BACKLOG.md`, minted by the round agent, which stays.
- **Joined disposition rows** in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under every id the round's evidence touched, at minimum `20260823-magnet-technology-ab#2`.

### What the grounding exchange can and cannot show

The owner asked for notes on **how the operator exchange actually works** (`spec.md:89`, `[NEED]` `[OWNER]`). A headless `claude -p` run cannot pause mid-run to ask a question and receive an answer, so every operator round-trip costs one run: the session writes what it can, stops, and the operator's answer arrives as the next resume turn's brief.

The design's response is to **buy the turns rather than shrink the artifact**. Grounding runs as one session over as many recorded resume turns as the exchange needs — each a run, each with a committed brief and kept transcript — so "where the dialogue stalled" has as many opportunities to be observed as the exchange actually produces. Four turns is the working budget; the record reports what happened, not the budget. `operator-notes.md` states the bound the mechanism imposes as a stated limit of the evidence, not as a finding about the runbook.

## Required Invariants

1. Every cold run has exactly one brief, and its commit is an ancestor of the commit carrying that run's output.
2. No cold run's transcript contains a read of `.project/active/goal-cold-pickup-proof/`, of any `.orchestrate-logs/` directory, or of `~/goal-proof-logs/`.
3. `work/orchestration/goals/` contains exactly one directory when the item closes, and no `gate-pN` branch or worktree survives.
4. The minted work item's row text and SHA-256 are identical before and after the resumer run, and its row appears exactly once. A whole-file change to `work/BACKLOG.md` is not a violation.
5. No `### T-00N return` and no `### Stop` exists in `trail.md` at the interrupted-state commit.
6. No first-sighting row in `DISCOVERY_LOG.md` is edited, and no id is minted.
7. Nothing under `work/orchestration/GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, or `.project/adr/` changes on this branch.
8. `learnings.md` gains its entry only in the reviewer's commit, in the same commit as the review that accepted it.

## Non-Goals

- Repairing the runbook, the templates, or the ADRs. Measured shortfalls are evidence under the owner's hardening rule, and the repair is Item 1's.
- Solving the `vol_cold_cryo` finding. The round mints the item and stops at the gate.
- Using Item 2's research seam or Item 3's integration seam.
- Any dispatch, concurrency, or hardening machinery. ADR-003 bars the first two as premises; the third is what this run is evidence about.
- Grading the proof against a predicted outcome. If the gate holds on all five classes or on none, if the resumer stops rather than returns, if the round agent refuses to mint — the record says so.

## Implementation Notes

- A transcript is not evidence until it is copied into `sessions/NN-<role>/` and committed. Copy it in the same step that runs the run, before anything else touches the tree, and commit before the next dependent run starts.
- Transcripts are large — sampled logs run 60 KB to 1.7 MB, and this design's runs number roughly a dozen. **Expect 8–20 MB of committed transcript** in a repository that otherwise carries text. That weight is accepted deliberately under D9; briefs should keep runs tight.
- Probes run sequentially, one worktree at a time. `git worktree remove` refuses a tree with modifications, so use `--force`, and delete the throwaway branch explicitly.
- The kill is a process-group termination, not an instruction, and is followed by a check that no `claude` process remains before the interrupted-state commit.
- The reviewer and the standalone reader run at the canonical path with the item directory on disk. The fence there is allowlist plus transcript check, which the spec explicitly accepts (`spec.md:51`). Running them in a worktree with the item directory removed would make the claim structural rather than verified — considered and not adopted, because it adds the worktree mechanics to the two runs whose transcripts are easiest to audit, and the transcript check already answers the question.
- Operator-side content in `goal.md` is `[AGENT]`. Only lines tracing to `align.md` owner decisions carry `[OWNER 2026-08-26]`.

## Potential Risks

- **The kill misses the window (B1).** Mitigation: poll on both conditions, short interval, a brief that names the expected artifact in the start line. Fallback: the three abort rules, each enumerated and disclosed.
- **The transcript does not survive termination (B5).** If the runner buffers rather than streams, the killed session's transcript is lost — and it is the one that matters most. Mitigation: verify streaming behavior with one throwaway run before anything else. Fallback: run `claude -p --output-format stream-json` directly for that run with the stream teed to a file the orchestrator owns.
- **The round agent refuses to mint (B6).** Covered by the § surfaced conflict contingency: recorded as prose-ambiguity evidence, resolved by a kept operator clarification, then the task proceeds.
- **The resumer stops rather than returns (D6).** Expected, and covered: the continuation session picks up the open round.
- **The continuation session leaves the round unclosed (B7).** Covered: one further continuation run, enumerated and briefed.
- **A probe session reads the fixture as a fixture (B2), most acutely at P1.** Mitigation: neutral construction, one heading hollowed, nothing else changed; the record carries the tell, and a refusal on other grounds is recorded as such.
- **The round agent flags the widened frame instead of carrying it (B4).** A real result: the contract resisted the drift at the writer rather than the reviewer. Record it and note that Criterion 8 was not exercised as designed.
- **Minting is judged to cross the reserved gate (B3).** The reading is that PM state is neither a model nor a knowledge mutation, and the review confirmed it holds on plain wording. If the owner reads it the other way, the interruption evidence is tainted and the run needs a different native target. Flagged, not assumed away.

## Integration Strategy

The goal directory, the minted work item, and the appended discovery rows are permanent. They enter their own systems through their own operations: the modeling PM mints its item through `agentic-mbse pm add-item`, and the goal round appends disposition rows under existing ids. Nothing crosses the `.project/` ↔ `work/` seam except by citation (ADR-006). The proof adds no tooling, no script, and no template — the whole point is that the shipped prose was the only mechanism.

## Validation Approach

`verification_record.md` carries one row per spec criterion: the criterion, the run that produced its evidence, the paths checked, the check itself, and the verdict.

| Criterion | Producing run | Evidence |
|---|---|---|
| 1. Cold grounding | grounding turns | `goal.md` at `Status: grounded`; transcripts |
| 2. Gate reach, per class | probes P1–P5 | `gate-probe-record.md`, five rows, each with quoted session output |
| 3. Goal directory stands alone | standalone reader | its written answer naming strategy, task, gate/limit state, native evidence |
| 4. Interrupted resume | round agent → resumer | interrupted-state commit; `interruption-state.md` row hashes; resumer transcript |
| 5. Bounded closure | continuation | `### Round 1 result` with a derived stop reason |
| 6. Judgment replays from trail | resumer + continuation | five-field decision blocks; the recorded T-001 shortfall |
| 7. Discovery-row accounting | continuation | joined rows under every touched id |
| 8. Fresh review catches the seed | reviewer | `### Round 1 review` against `seed-record.md` |
| 9. Failures are recorded | orchestrator | `verification_record.md` |

Two rules keep the record honest.

- **Ordering criteria are checked by ancestry, never by mtime or file order.** Criterion 2 → the closed probe record before the first `### T-001 scope` commit. Criterion 4 → the interrupted-state commit before the resumer's first commit. Criterion 8 → `seed-record.md` before the reviewer's brief commit.
- **The orchestrator writes the record; it does not certify it.** A fresh audit session re-runs every row against disk, including the transcript check for Required Invariant 2 — item directory, `.orchestrate-logs/`, and `~/goal-proof-logs/`. Criterion 2 is the one row the orchestrator could not check even in principle, and it is already settled: the enforcer is a separate fresh session, and the orchestrator never plays the refusing role.

Criterion 9 is the report's own content — every ambiguity, misreading, and failure with the session output that shows it, including the four already predicted (the grounding gate's reach, the `:234`/`:244` conflict, the runbook's silence on who owns an interrupted round, and the T-001 decision-record shortfall) — and either a named hardening mechanism with the recorded failure that promotes it, or a plain statement that none is proposed.

## Next-Stage Handoff

**Fixed.** The role map and the freshness fence, including `--log-dir` outside the tree and the allowlist briefs. Evidence in the item directory, never the goal directory. Five per-class probes in worktrees with the heading mapping and P1's construction. The minted work item as the interrupted artifact, with the `:234`/`:244` conflict surfaced and its contingency. The resumer's authority bounded to § Resuming an interruption, with a separate continuation session after it. The seeded drift's identity. The phased commit sequence and its three ancestry predicates.

**Open for the plan.** The goal's exact question wording and `Answered when` condition, which the grounding session co-develops rather than receives. The minted work item's name and scale. The poll interval and the number of grounding turns actually needed. The exact allowlist wording shared across briefs.

**De-risk first, before any brief is committed.** Three mechanism checks, each cheap, each load-bearing:

1. **Transcript survival under termination** — does the runner stream to `--log-dir` or buffer to completion? B5 and D9 rest on it.
2. **Process-group kill** — does `kill -TERM -<pgid>` stop the `claude` child, and does no process survive? M-1's contamination risk rests on it.
3. **`--log-dir` outside the tree** — does the runner accept an absolute path outside the repository, and does the worktree invocation pick up the worktree as cwd? C-1 and D3 rest on it.

If check 1 fails, D9 needs the direct `claude -p` route for the killed run before the plan is written.

---

**Next Step:** After design review → `/_my_plan`.
