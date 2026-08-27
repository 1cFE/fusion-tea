# Design Review: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Design:** `.project/active/goal-cold-pickup-proof/design.md`
**Spec:** `.project/active/goal-cold-pickup-proof/spec.md` (approved after `spec-review.md`)
**Review File:** `.project/active/goal-cold-pickup-proof/design-review.md`
**Date:** 2026-08-26
**Reviewer:** fresh design_review session (did not author the design)

---

## The Point

Item 1 shipped a goal layer — `GOAL_RUNBOOK.md`, three templates, the `run-goal` skill, ADRs 001–007 — written entirely by the person who designed it, and used by nobody else. `work/orchestration/goals/` does not exist. Three bets carry the epic's critical path on that layer and none has ever been tested: a stranger can ground a goal and cannot start an ungrounded one; a fresh session can resume an interruption from disk without repeating the completed native effect; a fresh reviewer catches drift and settles the learning delta.

What makes this urgent is the owner's bar, and it is a bar, not a preference: **none of the five hardening mechanisms — envelope YAML, event ledger, digests, idempotency keys, reconciliation — enters the first build unless a recorded proof run demonstrates that the prose/native-facts route failed** `[OWNER]` (`goal-strategy-task-harness-design-review.md:209`, carried as the epic's Hardening rule). Concurrent runs and unattended dispatch are not on that list; ADR-003 bars them as premises and no evidence here can promote them.

So this run is the only admissible evidence in either direction. Without it there is nothing to promote a mechanism on, and equally nothing that justifies leaving the prose route alone. The design's job is to make one real run *count* — evidence an auditor who did not watch it can verify from files alone. This item records failures; it does not repair them.

---

## Fundamental Assessment

**Sound, with four must-fix defects.**

The approach is right and I would not rework it. The core move — carry the ordering of ten cold runs on git commit ancestry rather than on anyone's account of what happened — is the correct answer to the spec's hardest constraint, that an auditor has files and not a clock. Three hard problems each get exactly one mechanism (five per-class probes, a real process kill, a drift planted upstream of the writer), and each mechanism exists to make evidence checkable rather than to make the run smoother. That is the right instinct for a proof item. The choice to run one honest round on one real question with a real grounding chain — rather than a fixture — is what makes the evidence worth anything, and D2 (evidence in the item directory, never the goal directory) correctly protects Criterion 3 from its own proof.

I found no over-engineering. The design adds no tooling, no script, and no template, which is the point: the shipped prose is the only mechanism under test. Complexity is proportional — nine sessions is a lot, but each one is forced by ADR-002 or § What "fresh" means, and the legality argument at `design.md:93` holds when I check it.

**Product lens.** I ran the lens inline rather than spawning the subagent, because this brief is a non-interactive stage invocation and the orchestration context does not authorize spawning agents. Reading the durable product statements (`epic_goal_strategy_task_harness.md` § Item 4, ADR-001–007, `GOAL_RUNBOOK.md`) against the design's **The Point**: the design's framing and the epic's converge, and I derive the same point independently — this is the gate on the owner's hardening rule and nothing else in the epic can supply it. No **DON'T** finding at owner or `[HARD]` authority. One `[HARD]`-adjacent contradiction did fire, and it is Critical C-3 below, escalated into this judgment rather than parked in the rubric.

**The two structural smells.** One fires.

- *A consumer compensating for a producer or platform guarantee* — **fires.** The design's freshness fence is a single instruction ("do not read `.project/active/goal-cold-pickup-proof/`") compensating for the fact that the platform leaves every prior session's full transcript sitting in `./.orchestrate-logs/` at the repo root, outside that path. The consumer (the brief) is patching a gap the runner creates. See C-1. This is the reason the verdict is Revise and not Approve.
- *A solution that changes who owns an invariant without saying so* — does not fire. The design is careful to keep every native mutation inside its owning system's own operations, and Integration Strategy states it plainly.

Neither of these makes the work wrong. Both are fixable inside the current shape, which is why I recommend **Revise**, not Rework.

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

I walked all nine criteria against the run sequence and the commit table. Seven are backed by a run that produces the evidence. Two are not.

| Criterion | Producing run | Disk evidence | Ordering | Verdict |
|---|---|---|---|---|
| 1. Cold grounding | 01 + 02 | `goal.md` grounded at C05; transcripts | — | backed |
| 2. Gate reach, per class | 03–07 | `gate-probe-record.md` at C12 | C12 ancestor of C14 ✓ | backed, construction under-specified (M-4) |
| 3. Goal directory stands alone | **none** | — | — | **not produced (C-2)** |
| 4. Interrupted resume | 08 → 09 | `interruption-state.md`, C14 trail state | C14 ancestor of C16 ✓ | backed, but rests on an unstated bet (C-4) and an unverified kill mechanic (M-1) |
| 5. Bounded closure | 09 | `### Round 1 result` at C16 | — | backed only if C-4 resolves the design's way |
| 6. Judgment replays from trail | 09 | five-field decisions in T-001/T-002 returns and the result | — | backed, thin (m-3) |
| 7. Discovery-row accounting | 09 | appended row under `…-ab#2` | — | backed for `#2`; silent on other touched rows (m-4) |
| 8. Fresh review catches the seed | 10 | `### Round 1 review`, `seed-record.md` at C13 | C13 ancestor of C17 ✓ | backed |
| 9. Failures are recorded | orchestrator | `verification_record.md` at C20 | — | backed |

The three ordering predicates the spec names (`spec.md:35`) all resolve to real ancestry pairs in the commit table, and I could check each with `git merge-base --is-ancestor`. That part is clean.

**Capture-fidelity check.** The design carries the spec's provenance faithfully in the places I checked. `[OWNER]` items — branch, operator role, operator-notes artifact, the hardening bar — survive at their emphasis. The `[AGENT] (ratified by owner)` items (the question, the reserved gates) are treated as challengeable rather than settled, which is correct. The owner's referent for the operator-notes artifact ("what the grounding dialogue asked, where it stalled, what the operator had to supply that the runbook did not prompt for", `spec.md:89`) is carried verbatim into the component list at `design.md:151` — but the mechanism the design picks can barely produce it. See M-6. No `[INFERRED]`/`[INHERITED]` item is silently promoted to a fixed constraint.

### 2. Pattern Consistency
**Assessment:** Pass

The design uses the repository's own patterns rather than inventing any: `orchestrate-stage.sh` for headless stages (the same runner every other stage in this epic used), the worktree naming convention from memory (`../fusion-tea-gate-pN`, parallel to the repo), `agentic-mbse pm add-item` as the modeling PM's own operation, and citation-only crossing of the `.project/` ↔ `work/` seam per ADR-006. Nothing new is introduced where something existing works.

### 3. Abstraction Quality
**Assessment:** Pass

There is essentially one abstraction — the `sessions/NN-<role>/` quad of brief, transcript, output, meta — and it earns its place: it is the unit the freshness record enumerates and the unit ancestry is asserted over. Removing it would make Criterion 4 and Criterion 8 unbacked. The five records (`freshness-record.md`, `gate-probe-record.md`, `seed-record.md`, `interruption-state.md`, `operator-notes.md`) each map to a distinct spec obligation with no overlap I could find, and `verification_record.md` correctly collapses the report and the epic's record into one document per `spec.md:90`.

### 4. Duplication Avoidance
**Assessment:** Pass

Non-Goals and Required Invariants (especially invariant 7) hold the line against restating or repairing Item 1's contract. The design cites the runbook by section and line throughout instead of copying rules, which is the same discipline the runbook demands of the goal layer itself. `interruption-state.md` scopes its unit to the minted row rather than duplicating `work/BACKLOG.md` — correct, and it is what keeps invariant 4 checkable.

### 5. Data Structure Clarity
**Assessment:** Concerns

The commit table and the run table are the design's two load-bearing structures and both are legible. Two units are under-specified:

- The interruption unit is "the minted row's text and its SHA-256." `add-item` parses `work/BACKLOG.md` and re-serializes the whole file (`agentic-mbse/src/agentic_mbse/pm/operations.py:933`), so a later PM operation can normalize unrelated rows without touching the minted one. Invariant 4 is right to scope to the row, but the design should say explicitly that a whole-file diff is not the check. (m-4)
- "Field class" is used as a probe unit without a mapping to template headings. "Answer contract" plausibly means § Answered when, but § Question and § Consumer are adjacent. The plan cannot build five variants without that mapping. (M-4)

### 6. Route Safety
**Assessment:** Concerns

Read as evidence routing rather than HTTP routing: the design has one catch-all that masks a real leak. The brief's prohibition names exactly one path, `.project/active/goal-cold-pickup-proof/`. Everything else in the repository is permitted, and the runner's own output directory sits at the repo root outside that path. See C-1. There is no wildcard-safe framing of what a cold session may read — it is an allowlist stated as a single denial, and the denial is incomplete.

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

The five stated bets are genuine claims about reality, each with an honest "if false → what fails," and none is a mechanism choice in disguise. B3 is stated as a bet with a stated taint consequence and is explicitly flagged rather than assumed away (`design.md:192`), which is the right posture. The nine decisions each name the rejected alternative and why; D4 and D6 in particular are argued rather than asserted.

**On B3 specifically, as the brief asks.** The design's reading of the goal's own reserved gate is correct on the plain wording. The gate reads "any model or knowledge mutation beyond the goal directory needs owner sign-off." In this repository "model" means SysML under `models/` and "knowledge" means `knowledge/`; `work/BACKLOG.md` is PM state and is neither. Minting through the PM's own operation is exactly the pattern `GOAL_RUNBOOK.md:244` contemplates for a finding that is work. That reading holds, and the design keeps it honest by naming the taint if a reviewer or the owner reads it the other way.

But B3 tests the wrong rule. The binding constraint is not the goal's reserved gate; it is `GOAL_RUNBOOK.md:234`. See C-3.

**Hidden bets I surfaced** (none of these is stated in the design):

- **The resumer finishes the interrupted task's remaining work.** The design has session 09 append the disposition row "which is what completes the routing" (`design.md:111`). § Resuming an interruption authorizes writing a return or a `### Stop`, not continuing the work. This is C-4 and it is the most expensive unstated bet in the design.
- **The kill preserves session 08's transcript.** Every "the session was not told" claim and D8's whole justification rest on a stream that a terminated process may never have flushed. M-1.
- **`orchestrate-stage.sh` resumes a session by id.** Asserted in D1 and load-bearing for run 02. I verified this one for you: `.orchestrate-logs/` already contains 74 files whose names are `resume-<session-id>-<timestamp>.json`, so resume-by-id is real and in routine use. Bet confirmed; no action needed.
- **The round agent will agree it may mint.** If it reads `GOAL_RUNBOOK.md:234` the way I do, it refuses, no native effect lands, and there is no interruption to resume. Folded into C-3.

### 8. Reader Comprehension
**Assessment:** Pass

Strong. "The Point" states the obligation and the stakes in three paragraphs a tired engineer can read once. "Core Concept" gives the mental model — ordering carried by commits, not by anyone's account — before any mechanism, and the three hard parts are each introduced with the plain problem before the solution. The two tables (ten runs, twenty commits) are where an auditor will actually live, and both are self-contained. I did not find voice that blocks the model.

---

## Issues by Severity

### Critical

**C-1. The freshness fence has a hole at `./.orchestrate-logs/`, and it is live today.**
*Dimension: Route Safety, Spec Compliance (Criteria 2, 4, 8).*

The design's enforcement is one instruction: "do not read `.project/active/goal-cold-pickup-proof/`" (`design.md:95`). `orchestrate-stage.sh` writes its full stream-json transcript to `--log-dir`, which defaults to `./.orchestrate-logs` relative to the caller's working directory — the repo root. That directory is not under the prohibited path, so the fence does not cover it.

This is not hypothetical. `./.orchestrate-logs/` exists right now and holds 74 files, including the transcripts of this item's own spec, spec-review, and design stages. A cold session run today at the repo root can read the entire pipeline — the spec, the seeded drift once it is written into a brief, the orchestrator's reasoning — while honestly obeying the one instruction it was given. Sessions 08, 09, and 10 all run at the canonical path.

Criteria 2, 4, and 8 rest on the freshness record (`spec.md:87`), and the record's closing statement would be false in a way the transcript check cannot even detect, because a `Read` of `.orchestrate-logs/` is not a read of a prohibited path.

*Resolution:* pass an explicit `--log-dir` outside the repository tree for every cold session (for example `~/goal-proof-logs/NN/`), copy the transcript into `sessions/NN-<role>/` from there, and state the prohibition as an allowlist — the goal directory, the runbook and templates, and the native repository — plus explicit denials for `.project/active/goal-cold-pickup-proof/` and any orchestration log directory. Add the log-directory read to the transcript check in Validation Approach and to Required Invariant 2.

**C-2. Criterion 3 has no producing run, and adding one breaks the closed enumeration.**
*Dimension: Spec Compliance.*

Criterion 3 requires that a reader given only `work/orchestration/goals/cryo-volume-basis/` plus the repository — no spec, no item directory, no operator transcript — names the active strategy, the one task, the gate/limit state, and the native evidence (`spec.md:43`). The design's Validation Approach acknowledges this needs "its own check" (`design.md:205`), but no run in the ten-run table performs it, no commit in the twenty-commit table carries its output, and `freshness-record.md` states that "these ten runs are all the runs there were" (`design.md:147`).

So the design is in a bind it has not noticed: either the check never happens and Criterion 3 is unbacked, or an eleventh cold session performs it and the freshness record's closure statement is false as written.

The reviewer session 10 is not a substitute. It reads the goal directory in review mode against the runbook's eight review checks, which is a different question from "does this directory stand alone," and it has already been handed the round's material.

*Resolution:* add run 11 as a standalone-reader session with its own brief, its own commit pair, and its own row in the freshness record; state its output as the Criterion 3 evidence. It runs after session 10 so it cannot contaminate the review, and its brief hands it the goal directory and the repository with the same allowlist. Update the run count everywhere it appears (Core Concept, the run table, `freshness-record.md`, the commit table).

**C-3. Minting the work item is a second write outside the goal directory, and the runbook says there is exactly one.**
*Dimension: Bets & Decisions Integrity; capture-fidelity rule 4 (surfacing).*

`GOAL_RUNBOOK.md:234` states flatly: "A goal round has exactly one write outside its own directory, and this is it" — the discovery log. The design's native target for the interruption is `uv run agentic-mbse pm add-item`, which writes `work/BACKLOG.md`. That is a second write outside the goal directory, and the design's B3 analysis never reaches it. B3 tests only the goal's own reserved gate, and passes.

There is a genuine counter-reading ten lines further down the same section: "A finding the round discovers itself... has a home, and the trail cites it: ... a native work item through the owning PM if it is work" (`GOAL_RUNBOOK.md:244`). So the runbook contradicts itself, and this proof is precisely the run that would expose it.

Two consequences, and the second is the expensive one:

1. Per capture-fidelity rule 4, a premise conflict of this kind is surfaced, not resolved silently in either direction. The design resolves it silently — by not seeing it.
2. If the round agent reads `:234` the way I do, it refuses to mint, no native effect lands, and there is no interruption to resume. The design has no fallback for a round agent that declines the native target, and this failure mode burns a cold session.

*Resolution:* surface the conflict explicitly in the design (a named entry, not a parenthetical), and choose one of two postures deliberately. Either (a) keep the mint, record the `:234` vs `:244` conflict as a predicted prose failure in the same register the spec uses for the grounding-gate prediction (`spec.md` § A predicted prose failure), and treat the round agent's own reading as part of the measurement — with a stated contingency if it refuses; or (b) pick a native target whose legality is unambiguous. Note that the design already rejected the obvious (b) candidate — the disposition row — for a good reason (D4), so (a) is probably right. Either way, B3 must be restated to be about `:234`, not about the reserved gate.

**C-4. The design assumes the resumer finishes T-001's unfinished work; the runbook does not authorize that.**
*Dimension: Bets & Decisions Integrity; Spec Compliance (Criteria 5, 6, 7, 8).*

§ Resuming an interruption gives the resumer four ordered steps and exactly two possible writes at step 4: "the missing return — if the native evidence shows the task reached an outcome — or `### Stop` of kind `interruption`" (`GOAL_RUNBOOK.md:217`).

T-001's objective is to *route* discovery row `…-ab#2` — mint the item **and** append the joined disposition row. At the kill, only the mint has landed. So the native evidence does not show the task reached an outcome, and a correct resumer following the runbook literally writes `### Stop — interruption`, not a return. The design instead has session 09 append the disposition row itself, "which is what completes the routing" (`design.md:111`), then scope T-002 and close the round.

D6 addresses whether the resumer *inherits the round*. It does not address whether the resumer may *finish the interrupted task's work*, which is the load-bearing assumption. That is an unstated bet.

If session 09 writes the Stop instead — which is the reading I would defend — the run produces no `### Round 1 result`, so Criteria 5 and 6 have no evidence, Criterion 7 leaves `…-ab#2` still `unrouted`, and session 10 has nothing to review, so Criterion 8's seeded drift is never tested. Four of nine criteria, on a single-shot run, with no contingency stated.

*Resolution:* state this as a sixth key bet with its own "if false" line, and give the design an explicit contingency. The cheapest honest one: if session 09 stops rather than returns, that is a first-class measured result (the runbook's silence on who completes an interrupted task's objective is a real prose gap, and it is arguably the most valuable finding the run could produce) — and then a further fresh session, enumerated in advance, opens the next task and closes the round. Deciding this in the design costs a paragraph; discovering it mid-run costs the proof.

### Major

**M-1. Session 08's transcript may not survive the kill, and the kill may not stop the writer.**
*Dimension: Bets & Decisions Integrity.*

Two mechanics, both load-bearing, neither verified:

- *Transcript survival.* If `orchestrate-stage.sh` streams `claude -p --output-format stream-json` to the log file as it runs, a terminated process leaves a truncated but usable transcript. If it buffers and writes on completion, the kill destroys session 08's transcript entirely — and with it D8's justification, B5's evidence, and the freshness claim for the one session that matters most.
- *Kill target.* Terminating the wrapper script does not necessarily terminate the `claude` child. If the child survives, it writes `### T-001 return` after the orchestrator has already committed C14, which is precisely the clean-boundary state the spec excludes (`spec.md:44`, `epic:329`) — and the contamination would be invisible until someone reads the trail.

*Resolution:* add both to the design's **De-risk first** list alongside the cwd fact. Verify the streaming behavior with one throwaway session before C02, and specify that the kill targets the process group (`kill -TERM -<pgid>`) with a post-kill verification that no `claude` process remains before the C14 commit. If the transcript does not survive termination, D8 needs a different mechanism for session 08 — for example running `claude -p` directly with the stream teed to a file the orchestrator owns.

**M-2. The kill-window failure modes are covered asymmetrically.**
*Dimension: Spec Compliance (Criterion 4).*

Implementation Notes cover one failure — the kill lands late, a return is already written, discard and re-run with a tighter poll (`design.md:183`). Two others are uncovered:

- *The start line is not on disk at kill.* Criterion 4 requires the write-ahead `### T-001 start` present, the native artifact present, and no return (`spec.md:44`). If the round agent mints before writing the start line — which is exactly the runbook compliance under test — the kill leaves a minted row with no write-ahead, and Criterion 4 is unprovable. This is a genuine measured prose failure worth recording, but it also means the interruption must be re-run, and the design should say so rather than leaving the orchestrator to improvise.
- *The mint and the return are emitted in one assistant turn.* Nothing prevents an agent from issuing the `add-item` Bash call and the trail Write in the same turn, or immediately back to back. B1's "before the session writes six more lines" assumes sequencing that is not guaranteed. The mitigation offered ("a brief that puts the minting call late in the task") does not address it.

*Resolution:* extend the discard-and-re-run rule to cover the missing-start-line case, and record it as a measured finding when it happens. For the batching risk, consider a brief that names the expected artifact explicitly in the start line, which makes the write-ahead a described precondition of the mint rather than an adjacent step — and accept that the mitigation is probabilistic, which B1 already concedes.

**M-3. The worktree probe mechanics do not survive the resolved cwd fact.**
*Dimension: Spec Compliance (Criterion 2), Data Structure Clarity.*

Taking the orchestrator's resolution as fact — no cwd flag, `claude -p` runs in the caller's working directory, `--log-dir` defaults relative to that cwd — D3 works but the design's evidence flow around it does not. Three things break:

- *The transcript lands in the worktree and dies with it.* `../fusion-tea-gate-pN/.orchestrate-logs/` is inside the throwaway tree. C07–C11 require "transcript, output, `gate-probe-record.md` row" per probe. Unless the transcript is copied out — or `--log-dir` points outside the worktree — probe evidence does not survive teardown, and D8's rule ("every cold session's full transcript is committed") fails for five of ten sessions.
- *A worktree cannot check out the branch the main tree has.* The design says the variant "is committed inside its own worktree" and the probe's kept output is "committed on the branch" (`design.md:99`). Those are two different branches. The variant commit necessarily lands on a throwaway branch, and the kept output must be copied to the main tree and committed there. The commit table (C06–C11) reads as if everything is on `feat/goal-integration-seam`.
- *Teardown is not clean by default.* `git worktree remove` refuses a tree with modifications, and the throwaway branch persists after removal. The invariant "leave nothing behind" (`design.md:68`) needs `--force` plus an explicit branch delete.

*Resolution:* specify per probe: create the worktree on a throwaway branch, run with `--log-dir` pointing outside both trees, copy transcript and output into `sessions/NN-gate-pN/` in the main tree, commit there, then `git worktree remove --force` and delete the throwaway branch. Correct the C06–C11 rows to say the variants are kept as fixtures under the item directory (which they must be anyway, for Required Invariant 3), not at the canonical path on the branch.

**M-4. The grounding-evidence probe's construction decides whether the one predicted refusal means anything.**
*Dimension: Spec Compliance (Criterion 2), Data Structure Clarity.*

The five variants each hollow "exactly one field class," and the design predicts one refusal — grounding evidence, per `GOAL_RUNBOOK.md:72`. But § Grounding evidence and § Status are coupled by the template: "Empty means `draft`" (`goal-templates/goal.md`), and the shipped rule is that *a draft goal authorizes no task*. So P1 has two possible constructions and the design does not say which:

- Hollow § Grounding evidence and set `Status: draft` — then the refusal is triggered by the status flag, and the probe measures whether a session reads a one-word field, not whether the gate reaches the grounding-evidence class.
- Hollow § Grounding evidence and leave `Status: grounded` — then the file is internally inconsistent in a way no real goal would be, B2 is strained for this variant specifically, and a refusal may name the inconsistency rather than the missing class.

Criterion 2 requires the session to name the missing class *unprompted* (`spec.md:40`), so which construction is used changes what the one predicted pass actually establishes.

The other four variants have a related but smaller problem: the design does not map "field class" to template headings. "Answer contract" is presumably § Answered when, but § Question and § Consumer are adjacent and a plan cannot build the variant without the mapping.

*Resolution:* state the heading-to-class mapping for all five, and for P1 pick the second construction (grounded status, hollow evidence) with the reasoning recorded — it is the only one that tests the gate's reach rather than the status flag, and `gate-probe-record.md` can carry a column noting the tell. Alternatively run P1 both ways as P1a/P1b and record both, which costs one session and settles it.

**M-5. D6 risks patching the silence it claims to measure.**
*Dimension: Spec Compliance (contract fidelity).*

D6 says "The design picks inheritance and **records the silence as a measured prose gap**" (`design.md:71`). Those two clauses pull in opposite directions and the design does not say which wins in session 09's brief.

If the brief tells session 09 to inherit the round and close it, the design has repaired Item 1's silence by instruction, and the "measured evidence" is the orchestrator's own note about a gap it then filled — which is not measurement. If the brief is silent and session 09 decides for itself, the behavior *is* the measurement, and whichever way it goes is a real result.

The Non-Goals are explicit that this item records and does not repair (`design.md:170`), so the second reading must be the intent. The design has to say so, because the plan will otherwise write the brief the easy way.

*Resolution:* state plainly that session 09's brief names the goal directory, the repository, and nothing about who owns the round afterwards; that whatever it does is the measurement; and that `operator-notes.md` records the gap as observed rather than as anticipated. Fold C-4's contingency into the same paragraph — they are the same question asked at two grains.

**M-6. Headless one-shot sessions cannot produce the operator-notes artifact the owner asked for.**
*Dimension: Spec Compliance, capture-fidelity rule 2 (compression).*

`spec.md:89` is `[NEED]` `[OWNER 2026-08-26]`: the orchestrator's notes on **how the operator exchange actually works** — "what the grounding dialogue asked, where it stalled, what the operator had to supply that the runbook did not prompt for." The design carries that referent verbatim into the component list (`design.md:151`) and adds "written turn by turn as the run proceeds, never reconstructed at the end." Good.

But the mechanism gives grounding two turns: run 01 produces a draft, run 02 resumes and produces a grounded goal. That is exactly **one** operator round-trip. A headless `claude -p` session cannot pause mid-run to ask the operator a question and receive an answer. So "where the dialogue stalled" has at most one opportunity to be observed, and the design's own handoff note that session 01 "co-develops with the operator rather than receiving" (`design.md:211`) overstates what two turns can deliver.

This is not fatal and it is not the design's fault — it is a property of the runner. But it is an owner-graded requirement whose evidence the mechanism thins, and shrinking an owner referent silently is what capture-fidelity rule 2 exists to stop.

*Resolution:* either budget grounding for more resume turns (each is a run, each gets a row in the freshness record and a brief commit — the run count is not sacred, and the cost is small next to the value of the owner's artifact), or state plainly in the design that the exchange is bounded to N round-trips by the headless mechanism, that `operator-notes.md` reports what that bound permitted, and that this is a stated limit of the evidence rather than a finding about the runbook. Do not leave it implicit.

**M-7. The freshness record's closure statement contradicts itself.**
*Dimension: Spec Compliance (Criteria 2, 4, 8).*

`design.md:147`: the record "states that these ten runs are all the runs there were, discarded attempts included." A discarded kill attempt (`design.md:183`) is an eleventh run. The sentence cannot be true as written the moment the mitigation it references is used.

Small wording, but the closure statement is the entire load-bearing sentence of the artifact that Criteria 2, 4, and 8 rest on (`spec.md:87`), and a record that is exact about everything it contains while incoherent about its own scope is precisely what that requirement was written to prevent.

*Resolution:* separate the count from the claim. The record enumerates every run that happened, marks each as kept or discarded with its reason, and closes with "these N runs, kept and discarded, are all the runs there were; no other input existed." Fix the count in Core Concept and the run table too if C-2 adds run 11.

### Minor

**m-1. Session 10 runs at the canonical path with `seed-record.md` on disk.** C13 commits the seed record; session 10 runs after it, at the repo root, with the item directory present. The fence is instruction plus transcript check, which the spec explicitly accepts (`spec.md:51`). Still, running session 10 in a worktree with the item directory removed would make the claim structural instead of trusted, at the cost of the M-3 mechanics. Worth one line of consideration in the design; not a must-fix.

**m-2. The five decision fields are thin at T-001.** Session 09 writes T-001's return, so its five-field decision blocks record *its own* goal-level decisions, not session 08's — which are unrecoverable, since session 08 was killed before its return. That is honest and probably the correct behavior, but Criterion 6 asks that "every goal-level decision the round made" carries five fields (`spec.md:49`), and the round made decisions in session 08 that no return will ever carry. Say explicitly that this is expected and is itself measured evidence about what an interruption costs the replay record.

**m-3. Criterion 7's scope may exceed row `…-ab#2`.** Rows `…-ab#1`, `#3`, and `#4` in `DISCOVERY_LOG.md` are all `model`-kind, all `unrouted`, all from the same study, and `#1` and `#3` both touch the magnet/cost chain that T-002's question sits in. Criterion 7 covers "every discovery row the round's evidence touched," not just the grounding row. The design commits to `#2` only. State what happens if T-002's reading touches another row — most likely a disposition row appended by session 09, which is legal, but the reviewer will check for it.

**m-4. Invariant 4's unit versus `add-item`'s whole-file rewrite.** `add_item` re-serializes all of `work/BACKLOG.md` (`agentic-mbse/src/agentic_mbse/pm/operations.py:962-995`). Invariant 4 correctly scopes to the minted row's text and hash, but the design should say in as many words that a whole-file diff of `work/BACKLOG.md` is not the check and does not violate the invariant.

**m-5. Repository weight is accepted but not sized.** D8 commits ten full stream-json transcripts, sampled at 60 KB to 1.7 MB (`design.md:179`). With C-2's eleventh run that is up to ~19 MB in a repository that otherwise carries text. The decision is deliberate and I would not overturn it, but the design should state the expected total so the owner is agreeing to a number rather than to a range.

---

## Recommendations

1. **Close the `.orchestrate-logs/` hole first (C-1).** It is one flag per session plus an allowlist rewrite of the brief, and without it the freshness record — which three criteria rest on — is false in a way its own verification cannot detect.
2. **Decide C-4 in the design, not mid-run.** Whether session 09 may finish T-001's work is the single assumption most likely to cost four criteria on a one-shot run. State it as a bet, give it a contingency, and let the resumer's actual behavior be the measurement.
3. **Surface C-3 rather than resolving it.** `GOAL_RUNBOOK.md:234` and `:244` contradict each other, and this proof is the run that finds it. Record it in the same register the spec already uses for the grounding-gate prediction, and add the contingency for a round agent that refuses to mint.
4. **Add run 11 for Criterion 3 (C-2)** and reconcile every place the run count appears, including the freshness record's closure statement (M-7).
5. **Respecify the probe mechanics against the resolved cwd fact (M-3)** — throwaway branch, external `--log-dir`, copy out before teardown, forced removal, branch delete — and correct C06–C11 accordingly.
6. **Pin the probe construction (M-4)** with a heading-to-class mapping and an explicit choice for P1's `Status` field.
7. **Make D6's brief silence explicit (M-5)** so the gap is measured rather than filled.
8. **Say what the two-turn grounding exchange can and cannot show (M-6)**, or buy more turns. This is the one owner-graded artifact whose evidence the mechanism thins.
9. **Add M-1's two mechanics to the De-risk list** — transcript survival under termination, and process-group kill — and verify both before C02, alongside the cwd check the orchestrator has already resolved.

---

## Resolutions

*(To be filled in Stage 4, when the owner engages with this review. One entry per resolved issue — this is what the design agent reads to incorporate the review.)*

---

**Overall:** Revise

The approach is right and the design is well made — I would not rework it, and most of what follows is additive rather than corrective. Four Critical findings must go back to the authoring session before the plan: the freshness leak at `./.orchestrate-logs/` (C-1), Criterion 3's missing producing run (C-2), the unsurfaced conflict between the runbook's one-write rule and the chosen native target (C-3), and the unstated bet that the resumer may finish the interrupted task (C-4). C-1 and C-4 are the two that would silently invalidate evidence rather than fail loudly, which is why they lead.

**Next Steps:** Once resolutions are recorded, return to the design-agent session (or re-run `/_my_design`) and point it at this review to incorporate. The reviewer does not edit the design. After the design is revised, `/_my_plan` — and the plan's first step remains the De-risk list, now carrying three mechanism checks instead of one.
