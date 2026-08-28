# Implementation Plan: GSTH Item 5 — Research-to-Model Round Proof

**Status:** Draft
**Created:** 2026-08-27
**Last Updated:** 2026-08-27
**Branch:** `feat/goal-research-model-proof` (base `e44498d4`; no child branch, no worktree)

## Source Documents

- **Spec (the contract):** `.project/active/goal-research-model-proof/spec.md`
- **Design:** `.project/active/goal-research-model-proof/design.md` ← component detail, session table, bets, the ten invariants, the commit sequence. Referenced throughout, restated nowhere.
- **Design review:** `design-review.md` (verdict Revise; the design revision of 2026-08-27 applies all findings)
- **Spec review:** `spec-review.md` (applied)
- **Align (owner rulings, settled):** `align.md`
- **Shape reference for this plan:** `.project/completed/20260827_goal-cold-pickup-proof/plan.md` (Item 4)

## Who executes this plan

**The orchestrator, acting as operator.** Not a subagent work order. Every step below is something the orchestrator types or commits itself. The only work delegated is what runs inside a cold headless session, and those sessions get a committed brief on stdin and nothing else.

Three consequences the executor holds onto:

- **The orchestrator never plays a role inside the round.** It writes briefs, launches runs, copies transcripts, commits, and writes the records. It never grounds the goal, never writes a trail entry, never runs the checkpoint, never reviews.
- **The owner is a real, absent participant.** Three gates park the run. At each one the plan stops with nothing further executed until a ruling arrives. The plan is resumable at each — every gate section states exactly what is on disk when the park begins and what the next phase does with the answer.
- **The orchestrator's own experience is a deliverable.** `operator-notes.md` is written after the runs from the kept transcripts, each judgment call graded `[AGENT]` and never as a contract repair (`design.md#component-overview`).

## The Point

The goal layer exists to decide what to work on next and what evidence means, across the seam where a modeling attempt runs out of evidence and has to go get some. That sequence — a bounded model task hits a wall, a critic checks the reading before anyone acts on it, evidence is acquired through a tracked procedure, modeling resumes or the round closes honestly — **has never run once.** Item 4 proved the round machinery on manual seams. Item 2 proved the research seam against fixtures, offline. Nothing has joined them.

So the obligation is not to build anything. It is to run the sequence once, on a need the repository is actually waiting on — the stellarator's `p_pump` = 1.0 MW, roughly 100× below admissible helium-primary circulator figures, understating `rec_frac` in every arm of both committed A/B studies — and to come out with a record an auditor can check against disk `[OWNER 2026-08-27]` (`align.md:7-12`).

Two things make the run worth more than a demo.

- **Criticism sits before work compounds on a misread.** `[OWNER-VERBATIM]` "Study > Analysis > Dispositions Plan / Critic looks at the analysis and plan and can push back on either/both" (`.project/concepts/goal-driven-model-development-harness.md:33`). A gate that has never bound is not evidence of anything.
- **Honest outcomes are first-class.** A queued source, a bounded negative, a strategy blocker, or a park at a reserved gate are all valid results. The item is deliberately not built so that only the positive path can succeed.

And the claim the whole run has to make checkable from `git log` alone: **the prerequisite emerged from the work rather than from the prompt.** Every mechanism in this plan — the grounding guard, the brief fence, the pre-declared covering branch, the ordering predicates — exists for that one claim.

## Implementation Strategy

**Phasing rationale.** The phases follow the design's § The commit sequence one-for-one, because that sequence *is* the evidence: the ordering predicates an auditor checks are commit ancestry, so commit order is the deliverable, not an implementation detail. Three splits are layered on top of it, all for the same reason — the run parks and cannot proceed:

- Commit-sequence phase 1 splits at **gate (a)** into plan Phases 1 and 2.
- Commit-sequence phase 5 splits at **gate (b)** into plan Phases 6 and 7.
- Commit-sequence phase 6 splits at **gate (c)** into plan Phases 8 and 9 (Phase 8's park is conditional).

**Critical path.** Scaffold and declare the covering branches → ground the goal → *gate (a)* → T-001 discovers the prerequisite → fresh critic binds → operator ruling and the r2 re-submission → the seam runs → *gate (b)* → advance or close → *gate (c)* if it is a judgment → result → fresh review → flip the runbook → bookkeeping → verify against disk.

**First proof point, and it is not a run.** Phase 0's Invariant-3 self-check on the drafted grounding brief. If the brief that grounds the goal already contains the errand, criterion 1 is hollow whatever the trail later says, and no later care recovers it. That check costs a grep and it happens before anything is committed. The design names this the de-risk-first item (`design.md#next-stage-handoff`), and Phase 0 does it for both sensitive briefs, drafted verbatim below.

**Where the flex is.** The floor is seven sessions: 01, 02, 03, 04, 05, 07, 08. Three are conditional and two of those are likely rather than remote:

| Run | Condition | Cost |
|---|---|---|
| 04b (critic re-submission `C-001.r2`) | D5's ruling changes the route the critic approved — **likely**, per design M1 | one session |
| 05a/05b split | same condition (the round writes the revision, stops, then resumes after r2) | one extra resume turn |
| 06 (gate (b) turn) | the owner rules gate (b) before close — near-certain **not** to happen in time | one session |

Nine sessions plus one substantive judgment is the realistic ceiling inside the epic's 8h execute. **If the budget binds, the thing that gives is T-003's spec depth — never the checkpoint and never the review** (`design.md#potential-risks`).

**Ordering predicates are commitments.** Each phase opens with **Ancestor required**: what must be committed and reachable from `HEAD` before the phase's first run starts. Check any with:

```bash
git merge-base --is-ancestor <earlier-sha> <later-sha> && echo OK || echo VIOLATED
```

**The enumeration rule, in force from Phase 1 to the end.** *Every* run — kept, aborted, discarded, crashed — gets a `sessions/NN-<role>/` directory with whatever it produced and a row in `freshness-record.md`. There is no such thing as a run that did not happen.

**Standing per-run procedure.** Every cold run in Phases 1–10 follows the same six steps, written once here and referenced as **[RUN]** afterwards.

1. Write `sessions/NN-<role>/brief.md`.
2. Commit the brief **alone**: `git add .project/active/goal-research-model-proof/sessions/NN-<role>/brief.md && git commit -m "proof(NN-<role>): brief"`.
3. Run it directly — **never through `orchestrate-stage.sh`** (`design.md#implementation-notes`; Item 4 `operator-notes.md:48-58`):
   ```bash
   ITEM=.project/active/goal-research-model-proof
   mkdir -p ~/goal-proof-logs-item5/NN-<role>
   claude -p --output-format stream-json --verbose \
     --permission-mode bypassPermissions \
     < $ITEM/sessions/NN-<role>/brief.md \
     | tee ~/goal-proof-logs-item5/NN-<role>/transcript.jsonl
   ```
   For a continuation turn of the same session, add `--resume <session-id>`. The session id is the `session_id` field of the first event in that session's transcript.
4. Copy the transcript in **before anything else touches the tree**:
   `cp ~/goal-proof-logs-item5/NN-<role>/transcript.jsonl $ITEM/sessions/NN-<role>/transcript.jsonl`, extract the final `result` event's text to `output.md`, and write `meta.md` (session id, command, cwd, log dir, start/end, exit status, kept or discarded with reason).
5. Append the run's row to `freshness-record.md`.
6. Commit the run's output **before the next dependent run starts**.

**The allowlist block**, carried verbatim in every brief for sessions 01–08 (`design.md#the-brief-fence`):

> You may read: the goal directory `work/orchestration/goals/p-pump-basis/`, `work/orchestration/GOAL_RUNBOOK.md` and `work/orchestration/goal-templates/`, `.claude/skills/run-goal/`, `.project/adr/`, and the native repository — `models/`, `knowledge/`, `work/`, `exploration/`, `modeling_project/`.
> You may not read: `.project/active/goal-research-model-proof/`, any `.orchestrate-logs/` directory anywhere in the tree, `~/goal-proof-logs-item5/`, and `.project/backlog/epic_goal_strategy_task_harness.md`. Anything not on the "may read" list is out of scope for this exchange.

**How the Invariant-3 narrowing is implemented, and why it is not written as a denial.** The design narrows sessions 01–03 further: they may not read the research seam paths, and that narrowing lifts once T-001's return is on disk (`design.md#the-brief-fence`). Those paths cannot be *named* in a pre-T-001 brief — `research_seam`, `source_registry`, and `research-acquire` are three of Invariant 3's seven denied strings, so a denial naming them would trip the invariant it serves, and would point the session at the errand besides. **The narrowing is therefore implemented as omission from a positive allowlist**, which is why the block above closes with "anything not on the 'may read' list is out of scope." From run 05 the allowlist gains the five research-seam paths explicitly. This is an execution detail of a fixed decision, recorded here so the executor does not improvise it and so `verification_record.md` can state it plainly.

**One string that will look like a violation and is not.** The item directory is named `goal-research-model-proof`, so the word "research" appears inside the denial line of every brief. Invariant 3's denial list does not contain the bare word "research", and a path denial is not an instruction to do research. Item 4 had the same shape. Note it in `verification_record.md` § Failures rather than leaving an auditor to trip over it.

**Overall validation approach.** Each phase is checked by a command that reads files, not by the operator's recollection. Phase 13 walks the nine spec criteria, the ten invariants, and the two ancestry predicates against what the earlier phases produced and drafts `verification_record.md`. The item then goes to `/_my_audit` as a **fresh session** — the orchestrator writes the record and does not certify it.

---

## Phase 0: Scaffolding, the covering branches, and the two sensitive briefs

**Commit-sequence phase 0** (`design.md#the-commit-sequence`). Lands **C-COVER**.

### Goal

Every evidence path exists on disk and in git; `covering-branches.md` is **complete**, not a skeleton, before the round opens; and the two briefs that can silently ruin the proof are drafted and checked before anything runs.

### Assumption Under Test

That the grounding brief can carry everything R-A1 and R-A3 require — the owner's question, three evidence pointers, the invariant channel, the gates, the limits, the consumer — **without** carrying the errand. This is the item's de-risk-first assumption (`design.md#next-stage-handoff`). Phase 0 collapses it with a grep, not with a run.

### Ancestor required

None. This is the first phase.

### Test stencil (write the pass condition before the artifact)

```bash
ITEM=.project/active/goal-research-model-proof
# Invariant 3, run against every brief committed before T-001's return.
# Expected output: nothing at all, and exit status 1 from grep.
grep -nEi 'Moscato|SOFT 2018|WPBOP|research_seam|source_registry|research-acquire|not ingested' \
  $ITEM/sessions/0[123]-*/brief.md
echo "exit=$?"   # expect exit=1 (no matches)
```

### Steps

- [x] `mkdir -p .project/active/goal-research-model-proof/sessions ~/goal-proof-logs-item5`
- [x] Confirm the direct-invocation surface before committing any brief: `claude -p --help | grep -E 'resume|output-format|verbose|permission-mode'`. **If the flag spelling differs from the [RUN] block above, fix this plan's commands now** — do not improvise per-run.
- [x] Copy the three templates into place as the empty starting point:
  `mkdir -p work/orchestration/goals/p-pump-basis && cp work/orchestration/goal-templates/{goal.md,trail.md,learnings.md} work/orchestration/goals/p-pump-basis/`
- [x] **Write `covering-branches.md` in full** (`design.md#component-overview`; the design is explicit that it is finished here, not stubbed). Two tables:

  **Table 1 — the branch table.** Each honest outcome, which criteria it covers, which it leaves non-exercised, and why that is a declared stop rather than a miss (R-H4):

  | Outcome | Covers | Leaves non-exercised | Why a declared stop |
  |---|---|---|---|
  | `OPERATOR_QUEUE` → `PREREQUISITE` → gate-(b) park → close on trigger 4/5 | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | R-D6: a queued candidate is a real result, handed to the owner with its reason, not retried into a positive |
  | `BOUNDED_NEGATIVE` | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | R-D6: a bounded negative is cited by whatever was waiting on it |
  | `REGISTERED` → premise moves → `STRATEGY_BLOCKER` close on trigger 2 via gate (c) | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | R-E3, B6: a peer outcome, not a fallback. Criterion 3 is met by honest routing |
  | `REGISTERED` → premise holds → gate (b) → T-003 mints and specs | 1–9 | — | the advance path; ceiling is `spec-model` (D3) |
  | The repository answers it (T-001 returns `COMPLETE`) | 2, 5, 6, 8, 9 | 3, 4 | R-B3: a research need is never manufactured |
  | Checkpoint hits its cap → `### Stop` kind `cap` | 1, 2, 8, 9 | 3, 4 | R-C3: the cap stops the work, it never releases it |
  | Owner rules no gate before close → trigger 4 | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | near-certain per the spec; a park at a declared gate is a declared stop |

  **Table 2 — D8's seam class → goal outcome mapping**, copied from `design.md#key-decisions` D8 including the `BLOCKER` split, and stated in the file as **the item taking a judgment the runbook leaves to the round agent**, with the reason (four classes against six outcomes is exactly where an honest queue gets quietly re-graded into a blocker, and a mapping written after the return is not a mapping). The mapping is a reading of the return, never a re-grade of it — the seam's class stays verbatim in the trail beside it (R-D3).

- [x] Create the record skeletons, each with its headings and an explicit "not yet populated" line:
  - [x] `freshness-record.md` — enumeration table (run NN, role, session, brief path, transcript path, session id, kept/discarded, reason) plus the closing-statement placeholder
  - [x] `operator-notes.md` — headings only; written in Phase 12 from the kept transcripts
  - [x] `verification_record.md` — the nine-criterion table skeleton, the two ordering predicates, the ten invariant slots, § Failures, § Hardening verdict; written in Phase 13
- [x] **Draft the two sensitive briefs** into `sessions/01-grounding/brief.md` and a held draft at `sessions/05a-round-agent-t002/brief.draft.md`. Both texts are below, verbatim. The 05a brief is **drafted now and committed later** — Phase 5 commits it, only after T-001's return is on disk (`design.md#next-stage-handoff`).
- [x] **Run the self-check** from the test stencil against `sessions/01-grounding/brief.md`. Expected: no matches, exit 1. **A match stops the phase** — fix the brief, do not annotate around it.
- [x] Also grep the drafted `goal.md` starting point and the commit message you are about to use with the same pattern. The commit message is read by nobody in the round, but it is in `git log`, which is the artifact the proof's central claim is checked against.
- [x] Commit: `proof: item scaffolding — sessions/, covering-branches.md complete, record skeletons` **plus** the goal-template copies. Record the sha as **C-COVER**.

### The grounding brief — session 01, verbatim

```markdown
# Operator brief — grounding, turn 1

You are a fresh session working with an operator to ground a goal under the repository's
goal layer. You did not build that layer and you need nothing beyond what is on disk.

## What you may read

The goal directory `work/orchestration/goals/p-pump-basis/`;
`work/orchestration/GOAL_RUNBOOK.md`; `work/orchestration/goal-templates/`;
`.claude/skills/run-goal/`; `.project/adr/`; and the native repository — `models/`,
`knowledge/`, `work/`, `exploration/`, `modeling_project/`.

You may **not** read `.project/active/goal-research-model-proof/`, any `.orchestrate-logs/`
directory anywhere in the tree, anything under `~/goal-proof-logs-item5/`, or
`.project/backlog/epic_goal_strategy_task_harness.md`. These are orchestration surfaces,
not goal material. Anything not on the "may read" list above is out of scope for this
exchange.

## The operator's question

> Is `p_pump` = 1.0 MW defensible for a helium-primary loop at this plant scale, and what
> sourced value should the model carry?

## The grounding evidence the operator can point at

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a`, row `20260821-power-cycle-ab#3`
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448` § 15
- `knowledge/KNOWLEDGE.md@ffa5c54c`, DI-008

Walk these yourself, and walk whatever else in the native repository they lead you to. The
operator will not hand you paths beyond these three.

## The consumer

Discovery row `20260821-power-cycle-ab#3`. What is waiting on the answer is that open
finding in the committed A/B study. There is no work item for this.

## The channel this value travels, and the distinction that goes with it

`p_pump` → the plant thermal balance and the recirculating sum → `rec_frac` and `p_net` →
the `recirc_ok` and `net_positive` verdicts and LCOE
(`models/library/analyses/mfe_power_balance.sysml:119,135`).

- **The input shift is equal across arms.** `p_pump` is cycle-independent (DI-007) and is
  held at 1.0 MW in all four arms, so a re-based value adds the same megawatts to every
  arm's recirculating sum.
- **The effect is not equal.** `rec_frac` is the recirculating sum over `p_et`, and `p_et`
  differs by arm by construction (η 0.333 → 0.47). The arms already sit at different
  recirculating fractions at the same grid corner — 0.94 / 0.79 / 0.68 by arm
  (`record.md@881d4448:208`) — and the `recirc_ok` fence already sits at different radii:
  violated at R ≤ 8.0 m (paper), ≤ 6.5 m (upstream), ≤ 5.5 m (both η 0.47 arms), at
  a = 0.8 m against threshold 0.5 (`record.md@881d4448:56`).

State this channel and this distinction in § Invariants and **stop there**. Whether
comparison meaning survives a re-based value is not settled at grounding — that is a
judgment for a round to make on evidence it has in hand, under the checkpoint and the fresh
review. A goal that hands a round the conclusion has not grounded anything.

## The reserved gates the owner keeps

- Any model or knowledge mutation beyond this goal directory. Anything landing in `work/`,
  `models/`, or `knowledge/` is the owner's go/no-go.
- The close ruling, if the round ends on a judgment call.
- Merge, push, work-item close, and archive.

## The limits

Restate every one explicitly in `goal.md` with its number; nothing is inherited silently.
The `GOAL_RUNBOOK.md` § Limits defaults are: retry cap 2 retries (3 attempts); checkpoint
revision cap 2 revisions (3 submissions); round limit 6 rounds; tasks per round: none. The
runbook has no time-limit row — do not invent one.

## What to do

Ground this question into `work/orchestration/goals/p-pump-basis/goal.md`, per
`GOAL_RUNBOOK.md` § Grounding a goal. The three template copies are already in the goal
directory as your starting point.

This is a headless exchange: you cannot pause to ask. Fill what you can ground from the
repository and the runbook. Where a field genuinely needs the owner — the exact wording of
§ Question, the § Answered when condition, § Close rule — write the goal file as far as
honesty allows, and put your questions for the owner, numbered and specific, in your final
message. The answers arrive as your next turn.

Provenance: the operator is an agent acting under authority the owner delegated. Mark
operator-supplied content `[AGENT]`, never `[OWNER]`.

Do not run `git commit` — the operator owns commits. Do not open a round and do not start
any task: grounding is the only work of this exchange.
```

**Checked against `design.md#the-grounding-guard`.** Contains only what the may-contain list allows: the owner's value question, the three pointers by path and sha, the invariant channel and the equal-input/unequal-effect distinction, the reserved gates, the limits, the consumer. Contains none of the may-not list: no "research", "acquire", "ingest", "register", or "source registration" as an instruction; no Moscato, SOFT 2018, or WPBOP-CPR(18) 20276; no statement about DI-008's ingestion status; no reference to the seam scripts, the command, or the operator guide; and the question is a value question, not an errand.

### The T-002 resume brief — session 05a, verbatim (held; committed in Phase 5)

```markdown
# Operator resume turn — the checkpoint verdict, and one operator ruling

This is a resume turn of the round session that wrote `### T-001 scope`, `### T-001 start`,
and `### T-001 return` for round 1 of the goal at `work/orchestration/goals/p-pump-basis/`.
You are still the round agent for that round. Continue it per `GOAL_RUNBOOK.md`.

## The checkpoint verdict

`### Checkpoint C-001.r1` is on disk in `trail.md`. A fresh critic session that was not you
wrote it. Read it there. Its verdict and its findings govern what you do next.

## An operator ruling, and exactly what authority it carries

**Grade: `[AGENT]`.** This is an operator judgment. It is not a contract, not a runbook
amendment, and not something to cite as either.

`GOAL_RUNBOOK.md` § The native seams marks the `research` row "**pending native repair**",
and the bullet under that table routes a round to the WI-031 hand pattern — a modeling-PM
work item, insights into `knowledge/research/approved/`, DIs minted at close. **That row and
that bullet are stale.** The native tracked procedure shipped, and the operator's ruling is
that you use it rather than the hand pattern:

- `docs/research_seam_operator_guide.md@9637f1b7` — the procedure: forming a request,
  running an invocation, the four return classes, committing the run directory with the work
- `scripts/research_seam.py` — the request and the run record
- `scripts/source_registry.py` — the one write into `knowledge/`
- `/research-acquire` — the command that drives them

The runbook row has not been flipped, deliberately: the flip is meant to rest on a seam run
that actually happened, and that has not happened yet. This ruling stands in for the flip
until then. **Do not edit `GOAL_RUNBOOK.md` yourself.**

Whether you had already noticed that staleness before reading this is worth one sentence in
the trail either way.

## What this ruling does to your dispositions

You wrote your proposed research disposition while the runbook still routed it to the hand
pattern, and the critic read the same stale runbook. So if this ruling changes the route the
critic approved, **the revised dispositions go back to a fresh critic before the follow-up
executes.** That is `### Checkpoint C-001.r2`. It is not a waiver, and it costs one of the
goal's two declared revisions. Write the revision, write the handoff `### Stop`, and stop —
the operator obtains the critic.

If the route the critic already approved is the native one, no re-submission is needed and
you may proceed to the follow-up task directly. Say in the trail which of the two it was.

## The follow-up task, when it is authorized

One field of the request is the operator's, because it is a naming decision rather than a
research one: `consumer` is `20260821-power-cycle-ab#3`. The discovery row is what is
actually waiting, it exists now, and no work item does. Every other field of the request you
write from your own return.

Whatever the seam returns is routed as it stands. Its class — `REGISTERED`,
`OPERATOR_QUEUE`, `BOUNDED_NEGATIVE`, or `BLOCKER` — is preserved verbatim in the trail
beside your reading of it. The goal layer reads a return; it does not re-grade one. A queued
candidate goes to the owner with its reason. A bounded negative is a first-class result,
cited by whatever was waiting on it. Neither is retried into a positive by hand.

Acquisition may register sources. It may not mint or amend a domain insight — that is a
knowledge mutation beyond the goal directory, and therefore a reserved gate.

## What you may now read, added to your standing allowlist

`docs/research_seam_operator_guide.md`, `.claude/commands/research-acquire.md`,
`scripts/research_seam.py`, `scripts/source_registry.py`, and `knowledge/research/`.
Everything else on your standing allowlist, and every denial on it, is unchanged.

Do not run `git commit` — the operator owns commits.
```

**Checked for what it may name.** Every seam path, the guide, and the command appear here and **only** here and later — this brief is committed in Phase 5, after `### T-001 return` is on disk, so Invariant 3 does not reach it. It still names no Moscato, no SOFT 2018, no WPBOP, and makes no statement about DI-008's ingestion status: what to search for is T-001's return to have established, not the operator's to supply.

### Validation

- [x] `git log --oneline -1` shows the scaffolding commit; its sha recorded as **C-COVER**
- [x] `covering-branches.md` has both tables **filled**, not stubbed: `grep -c '^|' covering-branches.md` returns a two-table count, and no line contains "TBD" or "not yet populated"
- [x] The Invariant-3 self-check returns no matches on `sessions/01-grounding/brief.md`
- [x] `ls work/orchestration/goals/` shows `cryo-volume-basis` and `p-pump-basis`, nothing else

### What We Know Works After This Phase

The covering branches are declared and dated in `git log` before the round exists, so no outcome can be re-read after the fact as a failed criterion. And the brief that grounds the goal has been shown, mechanically, not to carry the errand it is supposed to discover.

---

## Phase 1: Grounding turn 1 → gate (a)

**Commit-sequence phase 1**, first half. Session **01**, new, `run-goal ground`.

### Goal

A fresh session produces `goal.md` as far as it honestly can from the repository and the runbook, and puts its remaining questions to the owner. `Status` stays `draft`, and a draft goal authorizes no task.

### Assumption Under Test

That a stranger can ground this goal from the shipped prose plus the operator's value question alone — and, on the operator's side, where the exchange stalls and what the operator has to supply that the runbook never prompts for.

### Ancestor required

**C-COVER.**

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
grep -n '^## ' $GOAL/goal.md              # every template heading present
grep -n 'Status' $GOAL/goal.md            # still `draft` after turn 1
test ! -s $GOAL/trail.md || echo "trail should be the untouched template"
```

### Steps

- [x] **[RUN] as `sessions/01-grounding/`** with the grounding brief drafted verbatim in Phase 0. Nothing is added to it at run time.
- [x] Keep the final message as `output.md`. It carries the **gate (a) questions** — this is where the ask is written, because no trail exists yet (`design.md#owner-pause-points`).
- [x] Commit brief-then-output per [RUN], with the current `goal.md` state in the output commit.
- [x] Note in a scratch file what the session asked for, what it could not find, and what the operator had to supply. Raw material for `operator-notes.md`.

### Validation

- [x] `goal.md` is `draft` and no `### Round 1` heading exists anywhere
- [x] Tool-input fence check on this transcript (command in Phase 13, Invariant 2) returns nothing
- [x] A row exists in `freshness-record.md`

### **WAIT: owner ruling — gate (a)**

**The run parks here.** On disk when it parks: `covering-branches.md` complete, the goal directory with a partial `draft` `goal.md`, session 01's brief/transcript/output committed.

**What the owner rules:** the final wording of `goal.md` § Question, the § Answered when condition, and § Close rule. Whether any limit differs from the runbook default. `goal.md` § Question stays a question about the model value — that shape is fixed (`design.md#the-grounding-guard`); the wording is the owner's.

**Resume with:** Phase 2. Nothing else executes until the ruling arrives — no round, no task, no session 03.

---

## Phase 2: Grounding turn 2 — `Status: grounded`

**Commit-sequence phase 1**, second half. Session **02** = session 01 resumed.

### Goal

The owner's answers land as a committed resume-turn brief, and the session takes the goal to `Status: grounded` with all five field classes non-hollow (R-A3).

### Assumption Under Test

That the owner's answers can be delivered as a brief without re-opening the guard — the ruling settles wording and terms, and adds nothing about acquisition.

### Ancestor required

Session 01's output commit.

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
grep -n 'grounded' $GOAL/goal.md
grep -nE '@[0-9a-f]{7,40}|unpinned; no native digest' $GOAL/goal.md   # evidence pinned or declared unpinned
grep -nE 'Retry cap|Checkpoint revision cap|Round limit|Tasks per round' $GOAL/goal.md
grep -nE 'p_pump|rec_frac|recirc_ok' $GOAL/goal.md                    # the invariant channel is there
grep -nE 'model or knowledge mutation|close ruling' $GOAL/goal.md     # gates (b) and (c) named
```

### Steps

- [ ] Write `sessions/02-grounding/brief.md`: the allowlist block; the owner's answers, numbered against session 01's questions; and the reminder that operator-supplied content is `[AGENT]` and only what the owner said is `[OWNER 2026-08-27]`.
- [ ] **Run the Invariant-3 self-check on this brief too** before committing it — it is a pre-T-001 brief and Invariant 3 binds it exactly as it binds session 01's.
- [ ] **[RUN]** as a `--resume` of session 01.
- [ ] Verify the four limits are restated with their numbers, and that no time limit was invented.
- [ ] Verify § Invariants carries the channel and the equal/unequal distinction and **stops short of any conclusion** about whether comparison meaning survives (R-A6). If it states a conclusion, that is a finding for § Failures **and** a correction to take in one more grounding turn — do not edit `goal.md` yourself.
- [ ] Verify the seam-class routing table is **not** in § Invariants (D8 homes it in `covering-branches.md`).
- [ ] Commit; the last commit of this phase carries `Status: grounded`. Record its sha as **C-GROUND**.

### Contingency

- **A heading is left empty.** Not an abort — a run to keep, a freshness row, and material for the report. Take one more turn asking the session to complete it per the runbook. Do not fill it yourself.
- **The session grounds it but writes an errand-shaped § Question.** Record it in § Failures as evidence about the guard, and take one more turn. The wording is the owner's and the shape is fixed.

### Validation

- [ ] All five check-first commands pass
- [ ] Tool-input fence check on both grounding transcripts returns nothing
- [ ] Every operator-side line in `goal.md` is `[AGENT]`; only owner rulings are `[OWNER 2026-08-27]`

### What We Know Works After This Phase

A real goal exists at `work/orchestration/goals/p-pump-basis/`, grounded on the live need, with a question about the model value and no mention of the errand anywhere in it.

---

## Phase 3: T-001 — the bounded modeling task

**Commit-sequence phase 2.** Session **03**, new, `run-goal round`. Lands **C-T001**.

### Goal

The round opens under one strategy revision, and its first task attempts to re-base `p_pump` from repository-native sources under the goal's invariants. **Either the current data answers the question, or the task returns that research is needed to establish a defensible value.**

**Framing, per Ruling 2 `[OWNER 2026-08-28]`.** T-001's return is a judgment about **the sufficiency of the repository's current data** — not the identification of one missing document. The task is graded on the work it did: did it honestly test whether an admissible, citable basis exists here, and can it evidence its answer? Criterion 1 as originally written is retired (`covering-branches.md` § Amendment 2026-08-28), so this phase no longer carries it.

### Assumption Under Test

**B1** — the repository holds no admissible, citable basis for a helium-primary circulator `p_pump` at this scale, so an honest bounded attempt runs out of evidence and returns that research is needed.

**B2 is already measured and false** (Phase 1 notes; `covering-branches.md` § Amendment 2026-08-28). It is not under test here. Blindness is not what T-001 is being graded on.

### Ancestor required

**C-COVER must be an ancestor of C-T001** (Invariant 4, R-H4). Verify before launching, and again after committing:

```bash
git merge-base --is-ancestor <C-COVER> HEAD && echo OK || echo STOP
```

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
D=$(date +%Y-%m-%d)
grep -c "^### Strategy revision" $GOAL/trail.md          # 1
grep -c "^### T-001 scope"       $GOAL/trail.md          # 1
grep -nE "^### T-001 return — $D" $GOAL/trail.md         # date-anchored, per Invariant 9
# The scope must name a modeling objective and no research task (R-B1, R-B2):
sed -n '/^### T-001 scope/,/^### T-001 start/p' $GOAL/trail.md
```

**Date-anchor every poll and grep against goal files.** The trail template ships `### T-001 return — YYYY-MM-DD` literally; an unanchored predicate false-positives immediately (Item 4 harness error 08a). Invariant 9 requires each pasted predicate to show its anchor.

### Steps

- [ ] Write `sessions/03-round-agent/brief.md`: the allowlist block (**without** the research-seam paths — Phase 0's omission rule); the goal directory; "open round 1 and run it per `GOAL_RUNBOOK.md`". The brief states the objective in modeling terms only — *re-base `p_pump` from repository-native sources under the goal's invariants* — and **lists no prerequisite and no forward task** (ADR-001, R-B1, R-B2).
- [ ] **Run the Invariant-3 self-check on this brief.** It is the last pre-T-001 brief and the one most at risk of carrying the answer.
- [ ] **[RUN].**
- [ ] Verify T-001's return carries the **five decision fields for each goal-level decision** — finding or trigger; decision and reason; tier (`execution detail | reserved gate | premise surprise`); who decided; what changed as paths, ids, commits, or `none` (R-B4, `GOAL_RUNBOOK.md:130`). A four-field decision is a **recorded prose failure, not a formatting nit**.
- [ ] Verify the return names its evidence refs and the goal-level reading of them.
- [ ] Verify the reading and proposed research/model dispositions are written, and a `### Stop` of kind `handoff` closes the run — the round agent may not run its own checkpoint (R-C5).
- [ ] Commit transcript, output, `meta.md`, the strategy revision and T-001 entries, and the freshness row. Record the sha as **C-T001**.

### Conditional branch — T-001 returns `COMPLETE` (B1 false)

The repository's current data answers the question. Lands on `covering-branches.md` **row "The repository answers it"**: covers criteria 2, 5, 6, 8, 9; leaves 3 and 4 non-exercised.

- [ ] **Do not manufacture a research need** (R-B3). This is the single rule that keeps the item honest.
- [ ] The round continues to a close on whatever trigger fits, through the checkpoint (Phase 4) and the review (Phase 10). The seam is not invoked, so Phases 5–7 are skipped and Phase 11's flip does **not** land — R-G3 requires the flip to rest on a seam run that happened.
- [ ] `verification_record.md` records that the repository's current data answered the question, with T-001's return as the evidence. The seam is not invoked, criteria 3 and 4 go non-exercised under the declared branch, and the item ships the smaller proof.

### Validation

- [ ] `git merge-base --is-ancestor <C-COVER> <C-T001>` → OK, output pasted for Phase 13
- [ ] `### T-001 scope` names no research task and lists no future tasks
- [ ] Tool-input fence check on session 03's transcript returns nothing. **If it shows a read of `.project/backlog/epic_goal_strategy_task_harness.md`, that is not a run to discard** — it is recorded in § Failures. What T-001 is graded on is the work it did: whether it honestly tested the sufficiency of the repository's current data and can evidence its answer (Ruling 1, `[OWNER 2026-08-28]`).
- [ ] Every goal-level decision carries all five fields

### What We Know Works After This Phase

A real bounded modeling task has either answered the `p_pump` question from the repository or returned that research is needed to establish a defensible value — with its reasoning and evidence on the trail — and `git log` shows the covering-branch declaration predates the task that produced the outcome.

---

## Phase 4: The checkpoint — a fresh critic binds

**Commit-sequence phase 3.** Session **04**, new and fresh, `run-goal checkpoint`. Spec criterion 2.

### Goal

A fresh non-author critic reviews the reading and the proposed dispositions **before any semantic follow-up executes**, and its verdict is recorded as `### Checkpoint C-001.r1`.

### Assumption Under Test

That the checkpoint written into `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint actually binds a live round. It has never been exercised.

### Ancestor required

**C-T001.** The checkpoint reads T-001's return; it cannot precede it.

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
D=$(date +%Y-%m-%d)
grep -nE "^### Checkpoint C-001\.r1 — $D" $GOAL/trail.md
grep -nE "^(PASS|FINDINGS|Verdict)" $GOAL/trail.md | tail -5
```

### Steps

- [ ] Legality check before launching: session 04 authored no part of the round. It is not session 01/02 (grounding) and not session 03 (`design.md#sessions`, ADR-002, § What "fresh" means).
- [ ] Write `sessions/04-checkpoint/brief.md`: the allowlist block (**still without** the research-seam paths — the critic must read the same repository the round agent read, including the stale runbook row); the goal directory; run the checkpoint per the runbook. It is **not** told what verdict is wanted, and it is not told the runbook row is stale.
- [ ] Run the Invariant-3 self-check on this brief. It is committed before `### T-001 return` reaches the checkpoint's own reading, so it stays inside Invariant 3's window in spirit; run it regardless — the cost is a grep.
- [ ] **[RUN].**
- [ ] Verify `### Checkpoint C-001.r1` names the reviewer, the reading, the dispositions, the verdict, and what the author changed (R-C6). A previous entry is never amended.
- [ ] Commit transcript, output, `meta.md`, the checkpoint entry, the freshness row.

### Conditional branches

- **Verdict is `FINDINGS` and the author must revise.** The round agent (session 03 resumed) revises and re-submits as `C-001.r2` to a fresh session 04b. This consumes one of the two declared revisions — the same budget the route-change re-submission in Phase 5 draws on. **If both fire, the cap is reached at r3.**
- **The cap is reached (r3 does not pass).** The round writes `### Stop` of kind `cap` naming the unresolved dispositions and what the owner must decide, and **stops**. Execution is not permitted past an unpassed checkpoint (R-C3). Lands on `covering-branches.md` **row "Checkpoint hits its cap"**: covers 1, 2, 8, 9; leaves 3 and 4 non-exercised. The item goes to Phase 10 (review), Phase 12 and Phase 13 from there; no flip.
- **The critic notices the stale runbook row unprompted.** Record it — it is the more valuable result, and it is exactly what § Failures is for.

### Validation

- [ ] `C-001.r1` present, dated, with a verdict
- [ ] The critic session is not the author session (session ids compared in `meta.md`)
- [ ] Tool-input fence check on session 04's transcript returns nothing
- [ ] No T-002 entry exists anywhere in `trail.md` yet:
      `grep -c '### T-002' $GOAL/trail.md` → 0

### What We Know Works After This Phase

Criterion 2 has its evidence: a fresh critic bound a live round before any follow-up executed, and the disagreement — if there was one — is on disk as a sequence of submissions rather than an amended entry.

---

## Phase 5: The operator ruling, the r2 re-submission, and the seam run

**Commit-sequence phase 4.** Sessions **05a** (03 resumed), **04b** (new critic, likely), **05b** (03 resumed). Lands **C-SEAM**. Spec criterion 3.

### Goal

D5's ruling reaches the round after — never before — the checkpoint; the revised dispositions go back to a fresh critic if the route changed; and the Item 2 seam is then invoked natively with its return routed as it stands.

### Assumption Under Test

**B4** — the seam's four return classes cover what this need actually produces, so the goal layer never has to invent or re-grade a class. And R-C1's real guarantee: **what executes is what the critic approved.**

### Ancestor required

A **passing** `### Checkpoint C-001.rK` entry, committed. And for C-SEAM specifically: the passing checkpoint that covers **the route actually executed** (`design.md#the-commit-sequence`, row 4).

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
D=$(date +%Y-%m-%d)
# The seam's own evidence, after the run:
ls knowledge/research/requests/
cat knowledge/research/requests/REQ-PPUMP-01.json
find knowledge/research -name 'return.json' -newermt '2026-08-27' -print
uv run python -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('class'), d.get('queued'))" <return.json>
# The class is preserved verbatim in the trail beside the reading (R-D3):
grep -nE "REGISTERED|OPERATOR_QUEUE|BOUNDED_NEGATIVE|BLOCKER" $GOAL/trail.md
```

### Steps

- [ ] **Commit the 05a brief now, and not before.** Move `sessions/05a-round-agent-t002/brief.draft.md` to `brief.md` — the text is the one drafted verbatim in Phase 0 — and confirm `### T-001 return` is on disk first:
      ```bash
      grep -nE "^### T-001 return — 2026-[0-9]{2}-[0-9]{2}" work/orchestration/goals/p-pump-basis/trail.md
      ```
      **If that returns nothing, stop.** Committing this brief earlier puts the seam paths inside Invariant 3's window and breaks the proof's central claim.
- [ ] **[RUN] 05a** as a `--resume` of session 03. It reads the checkpoint verdict, absorbs the ruling, and either revises the dispositions and stops for `C-001.r2`, or proceeds directly if the approved route was already the native one. Commit its output.
- [ ] **Branch A — the route changed (likely, per design M1).**
  - [ ] Write `sessions/04b-checkpoint-r2/brief.md`: the allowlist block **with** the five research-seam paths added (the critic must be able to read what it is being asked to approve); the goal directory; run the checkpoint per the runbook on `C-001.r2`.
  - [ ] Legality check: session 04b is new and fresh, and is neither session 03 nor session 04.
  - [ ] **[RUN] 04b.** Commit its transcript and the `### Checkpoint C-001.r2` entry **before the seam runs.** This is the ordering R-C1 exists for.
  - [ ] If r2 does not pass, r3 is the last submission; past it, `### Stop` kind `cap` and the Phase 4 cap branch applies.
- [ ] **Branch B — the route did not change.** Record in the trail and in `operator-notes.md` that the critic had already approved the native route, skip 04b, and say so in § Failures beside the staleness entry — it is evidence the round or the critic caught the stale row unprompted.
- [ ] **[RUN] 05b** as a further `--resume` of session 03: T-002 executes. The round writes the request, runs `open` → `log` → `register --run` → `close --adequacy` per `docs/research_seam_operator_guide.md`, and routes what comes back.
- [ ] Verify the request is at `knowledge/research/requests/REQ-PPUMP-01.json` with `consumer` = `20260821-power-cycle-ab#3` (D7) and the shape the design fixes (`design.md#the-seam-invocation`).
- [ ] Verify **nothing under `knowledge/SOURCE_INDEX.md`, `knowledge/MANIFEST.jsonl`, or `knowledge/sources/` was hand-edited** — every change there is `source_registry.py`'s (Invariant 6, R-D1). Check the diff before committing, not after.
- [ ] Commit transcript, output, `meta.md`, the T-002 trail entries, and **everything under `knowledge/research/requests/`** — the request, the run directory, the receipts, the return, any bounded negative (R-D4). Record the sha as **C-SEAM**.

### Conditional branches, by return class

Each names the `covering-branches.md` row it lands on. The mapping is D8's, declared before the round opened.

- [ ] **`REGISTERED`.** T-002 is `COMPLETE`. The round then does the analytic work B6 makes likely: read the registered band against the arms' recirculating fractions and the `recirc_ok` fence radii, and decide whether the A/B comparison still means what it meant. **This is real work in this session, not a park** — it is the item's one substantive judgment. It resolves to either the gate (b) park (Phase 6, advance) or the gate (c) park (Phase 8, `STRATEGY_BLOCKER`), and neither is the fallback of the other. Rows: **"`REGISTERED` → premise holds"** or **"`REGISTERED` → premise moves"**.
- [ ] **`OPERATOR_QUEUE`.** T-002 returns `PREREQUISITE` per D8. The queued candidate goes to the owner at the gate (b) park with its reason. **Not retried into a positive, not re-graded as a blocker** (R-D6). Row: **"`OPERATOR_QUEUE` → `PREREQUISITE` → gate-(b) park"**.
- [ ] **`BOUNDED_NEGATIVE`.** A first-class result, cited by whatever was waiting on it. Row: **"`BOUNDED_NEGATIVE`"**.
- [ ] **`BLOCKER`, split per D8.**
  - **Fix leaves the request key unchanged** (unwritable registry, broken environment, a `limits` or `priority` change): `MECHANICAL_FAILURE`, retried under the same `T-002` id with a second `### T-002 start` recording the operational correction, within the cap of 2 retries.
  - **Fix changes any key field** (`question`, `consumer`, `gap_type`, sorted `where_to_look`): by the seam's definition it is a different request, so by the runbook's definition it is a **different task**. It gets a **new `T-00N`** with its own scope inside the same round, and the trail says why the request changed. **It is not a retry and is not written as one** — writing it as one is exactly what the fresh reviewer's retry-classification check catches (`GOAL_RUNBOOK.md:169`).
  - Past the retry cap, the blocker closes the round.

### Known upstream defect to watch for

`pm approve-research` refuses an empty insight list (`agentic_mbse/pm/operations.py:664-668`). A source-only round produces one. It is filed upstream and is **not this item's to fix** — if it bites, record it in `verification_record.md` § Failures and route around it (`design.md#implementation-notes`).

### Validation

- [ ] The seam's return class appears verbatim in `trail.md` beside the round's reading of it (R-D3)
- [ ] `git diff <C-T001>..HEAD --stat -- knowledge/` shows changes only under `knowledge/research/` and — if `REGISTERED` — under paths `source_registry.py` wrote
- [ ] The passing checkpoint entry covering the executed route is an ancestor of C-SEAM
- [ ] Tool-input fence check on sessions 04b, 05a, 05b returns nothing
- [ ] `git log --oneline -- knowledge/research/requests/` shows the request committed with the round, not separately after

### **WAIT: owner ruling — gate (b)** *(the park itself is Phase 6)*

Phase 6 writes the park. Phase 5 ends when C-SEAM is committed.

### What We Know Works After This Phase

Criterion 3 has its evidence: the Item 2 seam was invoked natively, its return routed as it stands, and no hand-written `SOURCE_INDEX.md` entry, manifest row, or source directory appears anywhere in the path.

---

## Phase 6: The gate (b) park

**Commit-sequence phase 5**, first half. Session 03 resumed, or already parked at the end of 05b.

### Goal

The round writes the owner gate where the layer natively keeps it — a `trail.md` `### Stop`, Kind `owner gate` — naming what the seam returned and what the owner must decide. Nothing about the gate is mirrored into the item directory.

### Assumption Under Test

None. This is the designed park (R-A4, R-E2). Its only risk is being skipped.

### Ancestor required

**C-SEAM.**

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
D=$(date +%Y-%m-%d)
grep -nA8 "^### Stop — $D" $GOAL/trail.md   # Kind: owner gate; names the return and the decision
grep -c 'owner gate' $GOAL/trail.md
```

### Steps

- [ ] If session 05b has not already written it, resume session 03 with a one-paragraph brief asking it to write the gate per the runbook. Do not write the entry yourself.
- [ ] Verify the `### Stop` names: the seam's return class verbatim, what it returned (the registered source, or the queued candidate **with its reason**), and the specific decision the owner must make — mint and advance the work item, or close.
- [ ] Commit.

### Validation

- [ ] The park is in `trail.md`, dated, Kind `owner gate`
- [ ] `freshness-record.md` cites the trail entry **by heading and date**, and mirrors no goal state (R-F5, `design.md#owner-pause-points`)
- [ ] No work item exists yet: `grep -c 'p_pump' work/BACKLOG.md` → 0

### **WAIT: owner ruling — gate (b)**

**The run parks here.** On disk when it parks: the goal grounded, round 1 open with a strategy revision, T-001 and T-002 complete with the seam's evidence committed, at least one passing checkpoint, and a dated owner-gate `### Stop`.

**What the owner rules:** whether to mint and advance the modeling work item on what the seam returned, or to close the round on the return as it stands.

**Resume with:** Phase 7 on a go; Phase 8 on a no-go or a close.

**Near-certain outcome, and it is covered.** The spec says this round parks at least once by construction and the owner will most likely not rule before close. That closes the round on trigger 4, leaves criterion 4 non-exercised, and lands on the `covering-branches.md` row **"Owner rules no gate before close"** — a declared stop, not an unmet criterion.

---

## Phase 7: T-003 — mint and spec the work item (advance path only)

**Commit-sequence phase 5**, second half. Session **06** = session 03 resumed. Spec criterion 4.

### Goal

On the owner's go, the round records a new bounded modeling task that mints the work item through the modeling PM's own operations and carries it to `spec-model` — **and stops there** (D3).

### Assumption Under Test

**B6, in its surviving half** — that a registered `p_pump` value moves the number without moving the premise, so the R-E1 advance is available. If the round has already read the evidence as moving the premise, T-003 is **never scoped** and this phase does not run.

### Ancestor required

The gate (b) park commit and the owner's ruling brief commit, in that order.

### Check first

```bash
grep -n 'p_pump\|circulator' work/BACKLOG.md          # exactly one new row
ls work/active/                                        # one new WI-0NN_ directory with spec.md
grep -nE '@[0-9a-f]{7,40}' work/active/WI-0NN_*/spec.md   # cites the registered source directly
```

### Steps

- [ ] Write `sessions/06-round-agent-gate-b/brief.md`: the allowlist block (with the research-seam paths); the owner's ruling verbatim; and the **ceiling, stated plainly** — `pm add-item` mints the item and `/spec-model` writes its `spec.md`. Design, plan, implement, regeneration, and pin promotion are out: they are the `integrate` seam and Item 6's (R-E4, D3). A round reaching them returns `PREREQUISITE` naming the seam.
- [ ] **[RUN].**
- [ ] Verify the new `spec.md` cites the registered source directly as its MR-4 basis. **No DI is minted and DI-008 is not amended** — that is a knowledge mutation beyond the goal directory and therefore its own reserved gate (R-D5).
- [ ] Verify the spec states the comparison-meaning reading the round arrived at, since criterion 4 asks that the advance "preserves comparison meaning."
- [ ] Verify no goal state is mirrored into `work/` and no modeling-PM state is mirrored into the goal directory (R-F5, ADR-006). Evidence is cited `<path>@<commit-sha>`.
- [ ] Commit transcript, output, `meta.md`, the T-003 trail entries, `work/BACKLOG.md`, and the new work item directory.

### Conditional branch — T-003 returns `PREREQUISITE` naming `integrate`

Expected and fine (R-E4). The round records it and goes to Phase 8. Criterion 4 is still met if the item was minted and specced before the prerequisite surfaced; if it was not, the round closes on the prerequisite and criterion 4 is non-exercised under the declared branch.

### Validation

- [ ] `uv run agentic-mbse status` parses cleanly and shows the new item
- [ ] No `design.md`, `plan.md`, or model file exists under the new work item — the `spec-model` ceiling held
- [ ] Tool-input fence check on session 06's transcript returns nothing

### What We Know Works After This Phase

Criterion 4 has its evidence: a newly authorized modeling task advanced a native work item under the same strategy, on evidence the seam registered, with the comparison-meaning reading stated.

---

## Phase 8: Findings dispositions, and the gate (c) park if the close is a judgment

**Commit-sequence phase 6**, first half. Session 03 resumed. Spec criterion 5.

### Goal

Every discovery row the round's evidence touched gets a joined disposition row, and — if the close turns on the R-E1-versus-R-E3 judgment — the round parks at gate (c) rather than deciding it alone.

### Assumption Under Test

That the round can tell the difference between a finding it must route to the discovery log and a finding of its own, which goes to `learnings.md`, the work item, or an ADR with the trail citing it (R-F2).

### Ancestor required

Phase 6's park at minimum; Phase 7's commits if the advance path ran.

### Check first

```bash
LOG=exploration/stellarator_e2e/studies/DISCOVERY_LOG.md
grep -n '20260821-power-cycle-ab#3' $LOG          # first-sighting row plus one joined row
grep -nE '20260821-power-cycle-ab#(1|2|5)' $LOG   # read-but-untouched accounting
git diff <base>..HEAD -- $LOG                      # appended rows only, no edits above
uv run python -m pytest tests/study/test_records.py -q
```

### Steps

- [ ] Verify row `20260821-power-cycle-ab#3` has a joined disposition row appended **under the same id**, with kind, status, responsible task, and what changed or the concrete next reference (R-F1, ADR-004). **No `unrouted`.**
- [ ] Verify the first-sighting row is **untouched** and **no id is minted** (Invariant 7). The study executor remains the first-sighting writer.
- [ ] Verify rows `#1`, `#2`, `#5` are accounted for: a joined row if this round's evidence touched them, and otherwise the recorded reasoning for leaving them, where the reviewer can check it (Item 4's read-but-untouched pattern).
- [ ] Verify findings the round discovered itself are **not** log rows.

### Conditional branch — the close is a judgment call

If the close turns on whether the registered evidence preserves the premise or moves it (R-E1 advance versus R-E3 `STRATEGY_BLOCKER`):

- [ ] The round writes `trail.md` `### Stop — <date>`, Kind `owner gate`, naming the judgment and the evidence on both sides. Commit.

### Validation

- [ ] `git diff <base>..HEAD -- $LOG` shows appended lines only
- [ ] `tests/study/test_records.py` passes
- [ ] No touched row returns `unrouted`

### **WAIT: owner ruling — gate (c)** *(conditional)*

**The run parks here only if the close is a judgment call.** On disk when it parks: everything from Phase 6, plus the seam's return routed, plus the joined discovery rows, plus a dated owner-gate `### Stop` naming the judgment.

**What the owner rules:** advance (R-E1) or close `STRATEGY_BLOCKER` on trigger 2 (R-E3).

**Resume with:** Phase 9.

**If the close is not a judgment call** — the return was `OPERATOR_QUEUE` or `BOUNDED_NEGATIVE`, or the owner never ruled gate (b) — there is no gate (c). Go straight to Phase 9.

---

## Phase 9: `### Round 1 result`

**Commit-sequence phase 6**, second half. Session **07** = session 03 resumed. Spec criterion 6, first half.

### Goal

The round closes on exactly one of the six triggers, with a result whose stop reason is **derived** from the last semantic outcome plus the goal's limits — not a second status enum (R-F3).

### Assumption Under Test

**B5** — one round is enough, because the runbook bounds tasks per round at "none", so `model → research → model` is three tasks under one strategy rather than three rounds.

### Ancestor required

Phase 8's commits, and the gate (c) ruling brief if one was needed.

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
D=$(date +%Y-%m-%d)
grep -nE "^### Round 1 result — $D" $GOAL/trail.md
sed -n '/^### Round 1 result/,$p' $GOAL/trail.md
# learnings.md must NOT have gained its entry yet — that lands only in the reviewer's commit:
git log --oneline -- $GOAL/learnings.md
```

### Steps

- [ ] If a gate (c) ruling was needed, write and commit `sessions/07-round-agent-close/brief.md` carrying it verbatim, then **[RUN]** as a resume of session 03. Otherwise resume with a brief that simply asks the round to close per the runbook.
- [ ] Verify the result carries: intent met/unmet, the task sequence, the last semantic outcome, the **derived** stop reason, the evidence refs, the **proposed** learning delta, and the finding dispositions (R-F3).
- [ ] Verify the close trigger is named and is one of the six.
- [ ] Verify `learnings.md` has **not** gained the entry — it lands only in the reviewer's commit (R-F4).
- [ ] Commit transcript, output, `meta.md`, the result, the freshness row.

### Validation

- [ ] The stop reason is derived, and the derivation is legible
- [ ] `learnings.md` is unchanged since the template copy
- [ ] Tool-input fence check on session 07's transcript returns nothing

### What We Know Works After This Phase

The round is closed and reviewable, on a trigger the covering-branch table already named before it opened.

---

## Phase 10: The fresh review

**Commit-sequence phase 7.** Session **08**, new and fresh, `run-goal review`. Spec criterion 6, second half.

### Goal

A fresh reviewer reads the round end to end, returns `PASS` / `FINDINGS` / `OWNER_GATE`, and accepts, corrects, or rejects the learning delta before it is appended to `learnings.md` — in the reviewer's commit and nowhere else.

### Assumption Under Test

**B3** — that `trail.md` is the round's real record rather than a record of the harness. The reviewer is the test: it was not there, and it has only what is on disk.

### Ancestor required

Phase 9's result commit.

### Check first

```bash
GOAL=work/orchestration/goals/p-pump-basis
D=$(date +%Y-%m-%d)
grep -nE "^### Round 1 review — $D" $GOAL/trail.md
git log --oneline -1 -- $GOAL/learnings.md   # must be the reviewer's commit
```

### Steps

- [ ] Legality check: session 08 authored no part of the round — it is not 01/02, 03, 04, 04b, 05a/05b, 06, or 07.
- [ ] Write `sessions/08-reviewer/brief.md`: the allowlist block **including** the research-seam paths and the whole trail — its job is the round end to end. Plus the one thing the design requires it to be told (`design.md#sessions`):

  > After a pass, the runbook has you either recommend the owner-held close or write the next strategy revision, which opens round N+1. **This item wants the close recommendation; opening round 2 is out of scope for this run.** The verdict itself — `PASS`, `FINDINGS`, or `OWNER_GATE` — and every finding are yours.

- [ ] The brief does **not** script the verdict and does not tell the reviewer what to find.
- [ ] **[RUN].**
- [ ] Verify the review covers every touched discovery row and the retry classification — whether a `BLOCKER` fix that changed a request key was written as a retry when D8 makes it a different task (`GOAL_RUNBOOK.md:169`).
- [ ] Commit the reviewer's transcript, output, `meta.md`, `### Round 1 review`, and the `learnings.md` entry **in the same commit** (R-F4).

### Contingency

- **The reviewer returns `FINDINGS`.** That is a result, not a failure. Record the findings in `verification_record.md`. Do not re-run the reviewer to replace a verdict.
- **The reviewer writes a strategy revision anyway**, opening round 2. Record it as a measured prose failure — the brief said the close recommendation was wanted, and the runbook's two-sequel wording is what produced the divergence. **Do not execute round 2** (D2, non-goal).

### Validation

- [ ] `### Round 1 review` present with a verdict
- [ ] `learnings.md` gained its entry only in this commit
- [ ] Every touched discovery row accounted for in the review
- [ ] Tool-input fence check on session 08's transcript returns nothing

### What We Know Works After This Phase

Criterion 6 has its evidence: the round closed through `RoundResult` and a fresh `RoundReview`, with no modeling-PM state mirrored, and the learning delta landed only after a session that was not the author settled it.

---

## Phase 11: The runbook flip

**Commit-sequence phase 8.** Lands **C-FLIP**. Spec criterion 7. No cold run.

### Goal

`GOAL_RUNBOOK.md` § The native seams stops telling the next round to hand-write what the seam now does — and the change rests on a seam run that actually happened.

### Assumption Under Test

None. The ordering is the point (R-G3), and it is checked by commit ancestry.

### Ancestor required

**C-SEAM must be an ancestor of C-FLIP** (Invariant 5). **If the seam never ran** — T-001 returned `COMPLETE`, or the checkpoint capped — **this phase does not run at all.** R-G3 has nothing to rest on, and criterion 7 goes non-exercised with the reason recorded.

### Check first

```bash
git merge-base --is-ancestor <C-SEAM> HEAD && echo OK || echo STOP
git diff HEAD -- work/orchestration/GOAL_RUNBOOK.md   # must touch exactly four spots
```

### Steps — four edits, all in § The native seams

- [ ] **R-G1, `:256`** — the `research` row loses "— **pending native repair**"; its Native return column becomes the four classes (registered sources, a queued candidate, or a bounded negative). The goal-level question column is unchanged.
- [ ] **R-G4, `:262`** — "**Two seams are not repaired yet**, and a goal round may not silently absorb either repair" becomes **one** seam, naming `integrate`.
- [ ] **R-G2, `:264`** — the WI-031 hand-pattern bullet is replaced by a pointer to `docs/research_seam_operator_guide.md`, `scripts/research_seam.py`, `scripts/source_registry.py`, and `/research-acquire`. **Leaving it would tell the next round to hand-write what the seam now does.**
- [ ] **R-G4, `:267`** — "The repairs have their own owners and their own failure contracts" is made singular.
- [ ] **The `integrate` row at `:258` and its bullet at `:265` are not touched** (R-G1). Verify byte-unchanged.
- [ ] Commit alone: `flip(GOAL_RUNBOOK): research seam is native`. Record the sha as **C-FLIP**.

### Validation

- [ ] `git merge-base --is-ancestor <C-SEAM> <C-FLIP>` → OK, output pasted for Phase 13
- [ ] `git diff <C-FLIP>~1..<C-FLIP> -- work/orchestration/GOAL_RUNBOOK.md` shows four hunks and nothing under the `integrate` row or its bullet (Invariant 8)
- [ ] `grep -n 'WI-031' work/orchestration/GOAL_RUNBOOK.md` → nothing in § The native seams
- [ ] `grep -n 'pending native repair' work/orchestration/GOAL_RUNBOOK.md` → one match, the `integrate` row

### What We Know Works After This Phase

The run compounds: the next goal round that needs evidence is told to use the seam, and `git log` shows the instruction rests on a seam invocation rather than on a shipment.

---

## Phase 12: Bookkeeping — the close list, the freshness record, the operator notes

**Commit-sequence phase 9**, first half. No cold run.

### Goal

Nothing stale is left behind for a Phase 4 operator to trip over, every run is enumerated, and the orchestrator's own side of the exchange is written down.

### Assumption Under Test

None. This is the correction discipline: a correction shrinks or amends, it never accretes (capture-fidelity Rule 3).

### Ancestor required

Phase 10's review commit. Phase 11's flip if it ran.

### Steps

- [ ] **The `CURRENT_WORK.md` edit — a removal, not an annotation** (R-A7, R-A7a; `[OWNER 2026-08-27]`, `align.md`). Today `.project/CURRENT_WORK.md:22`'s Phase 4 close list reads "…the runbook sentences (#10/#11 from study 2; #6/#10/#11 from study 1), **the `p_pump` re-source item**, WI-030's DI note". **Delete the bolded member** and close the sentence with one pointer:

  > the `p_pump` re-source is not on this list — it runs under `work/orchestration/goals/p-pump-basis/`

  That single clause is R-A7a's record of where it went. **Leaving the member standing with a note beside it would be accretion, not correction.** No modeling-PM or goal state is mirrored — a pointer only.
- [ ] **Close `freshness-record.md`.** Every run enumerated — kept, aborted, discarded, crashed — with brief path, transcript path, session id, and reason. Then the closing statement in plain words: *these N runs, kept and discarded, are all the runs there were; no other input existed* — no context injection, no prior turn beyond the recorded resume turns, no verbal hint from the operator. **Closure is a statement about completeness, not a count.**
- [ ] **Write `operator-notes.md`** from the kept transcripts, every judgment call graded `[AGENT]` and never as a contract repair. Include at minimum:
  - What the runbook prompted for unprompted, and what the operator had to supply.
  - Where the exchange stalled, and what each stall cost in turns.
  - **The D5 ruling as an operator judgment** — what it overrode, why it was delivered after the checkpoint rather than before, and that it was `[AGENT]`-graded in the brief itself so the round agent knew what it was reading.
  - The stated limit of the evidence: a headless run cannot pause mid-run to ask and receive an answer, so every owner round-trip costs one run. **A limit of the mechanism, not a finding about the runbook.**
  - The Invariant-3 narrowing implemented as omission rather than denial, and why (Phase 0).
- [ ] Commit.

### Validation

- [ ] `grep -n 'p_pump re-source item' .project/CURRENT_WORK.md` → nothing (the member is gone)
- [ ] `grep -n 'p-pump-basis' .project/CURRENT_WORK.md` → exactly one pointer
- [ ] The freshness record's run count equals the number of session directories: `ls -d sessions/*/ | wc -l`
- [ ] No cold run exists without a row, and no row without a `sessions/` directory

### What We Know Works After This Phase

The evidence is complete and closed, and the owner's removal ruling is applied as a removal.

---

## Phase 13: Verification — nine criteria, ten invariants, two predicates

**Commit-sequence phase 9**, second half. Spec criteria 8 and 9. No cold run.

### Goal

`verification_record.md` settles every criterion against disk, pastes every predicate with its output, records every prose failure, and states the hardening verdict either way.

### Assumption Under Test

None. This is the record. Its only failure mode is asserting rather than checking.

### Ancestor required

Everything.

### Steps — the nine criteria

- [ ] Walk them in order, one row each: criterion, producing run(s), the path/commit/return file that settles it, verdict.

  | # | Criterion | Producing run(s) | What settles it |
  |---|---|---|---|
  | 1 | Real `PREREQUISITE`, no predicted task list | 03 | `### T-001 scope` and `### T-001 return` in `trail.md`; the ambient-hint note |
  | 2 | Fresh critic before any follow-up | 04 (+04b) | `### Checkpoint C-001.rK` entries; session ids differ from the author's |
  | 3 | Seam invoked natively, return routed as it stands | 05b | `knowledge/research/requests/REQ-PPUMP-01.json`, the run dir, `return.json`; the class verbatim in the trail |
  | 4 | Modeling task advances the native item | 06 | `work/BACKLOG.md` row + `work/active/WI-0NN_*/spec.md`, **or** the covering-branch row that leaves it non-exercised |
  | 5 | Joined dispositions; learning cites the evidence | 07, 08 | `DISCOVERY_LOG.md` diff; `learnings.md` entry in the reviewer's commit |
  | 6 | `RoundResult` + fresh `RoundReview`, no mirroring | 07, 08 | `### Round 1 result`, `### Round 1 review` |
  | 7 | Runbook `research` row flipped, later than the seam run | orchestrator | `git merge-base --is-ancestor C-SEAM C-FLIP`; the four-hunk diff |
  | 8 | Every prose ambiguity, misread, and failure recorded | orchestrator | § Failures, entries resolving to real run artifacts |
  | 9 | No hardening mechanism without a recorded failure | orchestrator | § Hardening verdict; the keyword sweep plus the whole-diff read |

### Steps — the two ordering predicates, output pasted verbatim

```bash
git merge-base --is-ancestor <C-COVER> <C-T001> && echo OK || echo VIOLATED   # Invariant 4
git merge-base --is-ancestor <C-SEAM>  <C-FLIP> && echo OK || echo VIOLATED   # Invariant 5
```

### Steps — the ten invariant checks, each with its command and expected shape

```bash
ITEM=.project/active/goal-research-model-proof
GOAL=work/orchestration/goals/p-pump-basis
BASE=e44498d4

# 1 — one committed brief per cold session, its commit an ancestor of that session's output commit.
for d in $ITEM/sessions/*/; do
  n=$(basename $d)
  b=$(git log -1 --format=%H -- $d/brief.md)
  o=$(git log -1 --format=%H -- $d/transcript.jsonl)
  printf '%s brief=%s out=%s ' "$n" "${b:0:8}" "${o:0:8}"
  git merge-base --is-ancestor $b $o && echo OK || echo VIOLATED
done
# Expected: one line per session directory, all OK, and every brief= non-empty.

# 2 — fence sweep against tool-call INPUTS, not raw transcript text.
#     (Every brief embeds its own denial list, so a raw grep self-matches.)
for f in $ITEM/sessions/*/transcript.jsonl; do
  uv run python - "$f" <<'PY'
import json,sys,re
DENY = re.compile(r'\.project/active/goal-research-model-proof|orchestrate-logs|goal-proof-logs-item5|epic_goal_strategy_task_harness')
hits=[]
for line in open(sys.argv[1]):
    try: e=json.loads(line)
    except Exception: continue
    for blk in (e.get("message") or {}).get("content") or []:
        if isinstance(blk,dict) and blk.get("type")=="tool_use":
            s=json.dumps(blk.get("input"))
            if DENY.search(s): hits.append((blk.get("name"),s[:200]))
print(sys.argv[1], "CLEAN" if not hits else hits)
PY
done
# Expected: every line ends CLEAN.

# 3 — no pre-T-001 brief names the errand.
grep -nEi 'Moscato|SOFT 2018|WPBOP|research_seam|source_registry|research-acquire|not ingested' \
  $ITEM/sessions/0[1234]-*/brief.md
# Expected: no output, exit 1. (Sessions 01, 02, 03, 04 are all committed before T-001's
# return reaches the seam. 05a onward are outside the window by construction.)

# 4, 5 — the two predicates above.

# 6 — every knowledge/ write is source_registry.py's.
git diff --stat $BASE..HEAD -- knowledge/SOURCE_INDEX.md knowledge/MANIFEST.jsonl knowledge/sources/
uv run python scripts/source_registry.py verify
# Expected: the diff shows only what a registration writes (or nothing, on a queue/negative
# return), and verify reports zero faults.

# 7 — no first-sighting row edited, no id minted.
git diff $BASE..HEAD -- exploration/stellarator_e2e/studies/DISCOVERY_LOG.md | grep '^-' | grep -v '^---'
uv run python -m pytest tests/study/test_records.py -q
# Expected: no removed lines at all (appends only); the suite passes.

# 8 — the runbook diff touches only the four spots.
git diff $BASE..HEAD -- work/orchestration/GOAL_RUNBOOK.md
# Expected: four hunks, all in § The native seams; the `integrate` row and its bullet absent
# from the diff entirely.

# 9 — every predicate this record pastes shows its date anchor.
grep -nE '###.*—.*YYYY-MM-DD' $ITEM/verification_record.md
# Expected: no output. A predicate quoted with the literal placeholder, or with no anchor at
# all, is itself the audit finding.

# 10 — no hardening mechanism entered without a recorded failure.
git diff $BASE..HEAD --stat -- $ITEM
git diff $BASE..HEAD -- $ITEM | grep -niE 'envelope|event ledger|digest|idempoten|reconcil|dispatch'
# Expected: the grep returns nothing — AND the record states that the check was a keyword
# sweep PLUS a read of the whole item diff, because a dispatcher need not call itself one.
# Do not claim mechanical completeness.
```

**Before any `tests/models` run:** `set -a; source ~/1cfe/agentic-mbse/.env; set +a` (the file does not export the key).

### Steps — § Failures

- [ ] **Three entries are known before the run and are written whatever else happened:**
  1. **The stale `research` seam row.** The shipped runbook instructed a hand-write that Item 2 had already replaced, and only an operator ruling stopped it. Record whether the round agent or the critic noticed the staleness **before** the ruling arrived — from T-001's return and the checkpoint transcript, either way.
  2. **The `:140` trigger-phrase tension (R-C2).** The runbook phrases the checkpoint trigger as "after a study reading produces proposed dispositions." This round executed no study; it read committed study evidence. The reading this run acted on: the checkpoint fires on **the reading**, and a reading of committed study evidence is a reading — basis, the epic's own Item 5 scope step 2, which names no freshly executed study (`epic:389`) and which the owner ratified with the decomposition. **Recorded as an orchestrator execution-detail decision, loudly, in this section and in the run summary that goes to the owner.** If the owner reads `:140` narrowly, it is that runbook sentence that gets amended, not this item's checkpoint.
  3. **The recorded gap is the readable gap — bet B2 measured false, and criterion 1 retired.** The full write-up is `covering-branches.md` § Amendment 2026-08-28 and the Phase 1 completion note; § Failures carries it as a measured prose failure with its general result: a need selected because it is documented has a prerequisite legible to anyone who reads the documentation, so a deliberately chosen need cannot yield blind discovery. State that the brief fence held (Invariants 2 and 3 clean) and that the leak came through evidence R-A1 requires. Record the owner's ruling and characterization verbatim. Add the "research" string in the item-directory denial line (Phase 0), the `research_seam_operator_guide.md` strings in `covering-branches.md` (Phase 0 note), and any transcript showing a session reached `.project/backlog/` anyway.
- [ ] Add everything else that actually happened: aborted runs, the `pm approve-research` empty-insight refusal if it bit, harness errors, anything the executor had to decide in the moment.
- [ ] **State the hardening verdict explicitly.** Either name a mechanism and cite the recorded run failure that promotes it under the owner's rule, or say plainly that none is proposed. **Silence is not an option.**
- [ ] Do not grade the run against a predicted outcome. If the seam queued, if the premise moved, if T-001 returned `COMPLETE` — the record says so, and `covering-branches.md` already said which criteria that outcome covers.
- [ ] Run the honest-outcome test: whatever the round closed on, confirm `covering-branches.md` predates it in `git log` **and already lists it**. An outcome the branch table does not list is a **finding for § Failures, not a reason to edit the table.**
- [ ] Commit.

### Validation

*Verified by the fresh audit, 2026-08-28 (`audit.md`, POSITIVE).*

- [x] Nine criterion rows, each with a path an auditor can open — all nine re-run against disk; one citation points at the wrong row of the right table (`audit.md` Finding 3)
- [x] Two ancestry predicates, output pasted — both re-run: `e02ce403 → 71d2abe8` OK, `08af1532 → 71d2abe8` OK; Invariant 5 correctly non-exercised
- [x] Ten invariant checks, each with its command and output — all ten re-run, every figure reproduced exactly (fence sweep 8/8 CLEAN over 174 tool calls; `0 fault(s), 3 legacy`; 7 passed; 261 passed / 84 skipped; 0-line runbook diff)
- [x] § Failures has at least its three known entries — eight entries, all resolving to real artifacts; a ninth is owed
- [x] Hardening verdict stated either way — stated, and it survives a sweep wider than this battery's

### Hand-off — the orchestrator does not certify its own record

- [x] Run `/_my_audit` as a **fresh session**. It re-runs every row against disk, including the Invariant 2 tool-input sweep. — done 2026-08-28, `audit.md`, verdict **POSITIVE** with five findings; every row re-run, none overturned.
- [ ] **Still owed at close, outside the design:** the `product-lens.md` ledger entry the spec marks "to be created at close; not yet run" (`spec-review.md:30`, finding **L1-5** — this line and `verification_record.md:88` both cite it as "A9", a label that does not appear in the review). The audit did not clear this gate.

---

## Standing rules the executor holds in every phase

- **Never invoke a cold session through `orchestrate-stage.sh`.** It composes `/_my_<stage>` plus an orchestrator preamble, and its buffered output does not survive a kill. Direct `claude -p --output-format stream-json --verbose`, teed to `~/goal-proof-logs-item5/`, outside the tree.
- **Date-anchor every poll and grep against goal files.** The templates ship `YYYY-MM-DD` literally.
- **Fence sweeps target tool-call inputs, never raw transcript text.**
- **Briefs are committed before their run; outputs before the next dependent run.**
- **Every run lands in the enumeration** — kept, aborted, discarded, crashed.
- **The orchestrator writes no trail entry, grounds no goal, runs no checkpoint, and reviews nothing.** Where a session got something wrong, the correction is another turn of that session, not the operator's pen.
- **Nothing new is built.** The item's only executable inputs are the two Item 2 scripts, the modeling PM's CLI, and `claude -p` (spec § Non-Goals).
- **Any Python is `uv run python ...`** (CLAUDE.md).
- `set -a; source ~/1cfe/agentic-mbse/.env; set +a` before `tests/models`.

## Risk Management

See `design.md#potential-risks` for the full analysis. Phase-specific mitigations:

- **Phase 0** — the whole phase is the mitigation for the staged-discovery risk. The Invariant-3 self-check is mechanical and costs a grep; a match stops the phase rather than degrading it.
- **Phase 3** — B1 false is not mitigated, by design (R-B3). The covering-branch row for it was written in Phase 0, so the outcome is covered rather than salvaged.
- **Phase 4** — the cap is a designed outcome, not a failure of the item. It stops the work; it never releases it.
- **Phase 5** — R-C1 is protected by ordering, not by intent: the `C-001.r2` entry is committed **before** the seam runs, and Phase 13's check is that the passing checkpoint covering the executed route is an ancestor of C-SEAM. The `BLOCKER` split is where the reviewer's retry-classification check will bite if it is blurred.
- **Phases 6 and 8** — the owner not ruling is near-certain and already covered. The risk to guard is the operator ruling *for* the owner; the parks are written into `trail.md` by the round, not by the orchestrator.
- **Phase 11** — the flip does not run if the seam did not. R-G3 has nothing to rest on, and criterion 7 goes non-exercised with the reason recorded.
- **Budget** — nine sessions plus one substantive judgment is the ceiling. If it binds, T-003's spec depth gives. **Never the checkpoint and never the review.**

## Implementation Notes

[TO BE FILLED DURING EXECUTION]

### Phase 0 Completion
**Completed:** 2026-08-27. **C-COVER = `e02ce403`.**

**Changes made:**
- Created `covering-branches.md` in full — Table 1 (seven honest outcomes against the nine criteria) and Table 2 (D8's seam-class mapping with the `BLOCKER` split), plus the statement that the item is taking a judgment the runbook leaves to the round agent.
- Created `freshness-record.md`, `operator-notes.md`, `verification_record.md` as skeletons with their headings and explicit "not yet populated" lines.
- Copied the three templates to `work/orchestration/goals/p-pump-basis/`.
- Drafted both sensitive briefs verbatim: `sessions/01-grounding/brief.md` and `sessions/05a-round-agent-t002/brief.draft.md`.

**The Invariant-3 self-check — the phase's proof point — passed.** Run against `sessions/01-grounding/brief.md`, the `goal.md` starting point, and the commit message: no match on any of `Moscato|SOFT 2018|WPBOP|research_seam|source_registry|research-acquire|not ingested`, exit 1 on each.

**Flag check.** `claude -p --help` confirms `--resume`, `--output-format`, `--verbose`, and `--permission-mode` all exist with the spellings the [RUN] block uses. No plan command needed fixing.

**Execution details, recorded so they are not improvised later:**
- **Both briefs were extracted from `plan.md` by line range (`sed -n '163,251p'` and `sed -n '259,328p'`) rather than retyped**, so "verbatim" is true by construction rather than by care. 89 and 70 lines.
- **`sessions/01-grounding/brief.md` is deliberately NOT in the C-COVER commit.** [RUN] step 2 says commit the brief *alone*, immediately before its run; Phase 1 does that. Invariant 1 (brief commit an ancestor of the output commit) holds either way, and this reading honours [RUN] literally. C-COVER carries the four item records and the three template copies.
- **`sessions/05a-round-agent-t002/brief.draft.md` stays untracked until Phase 5**, per the design's de-risk-first instruction. Committing it now would put the five seam paths inside Invariant 3's window and break the proof's central claim. Consequence for the executor: **every `git add` from here to Phase 5 must name explicit paths — never `git add -A`.**

**For § Failures (Phase 13):** `covering-branches.md` contains the strings `research_seam_operator_guide.md` and `docs/research_seam_operator_guide.md:108` in the `BLOCKER` split, and it is committed at C-COVER — before T-001. This is not an Invariant-3 violation: Invariant 3 binds *briefs*, and `covering-branches.md` is inside the item directory that every session is denied from reading. Recorded here so an auditor grepping the whole item diff for those strings does not trip over it.

**No deviations from plan.**

### Phase 1 Completion
**Completed:** 2026-08-27. Session 01 kept. Parked at gate (a).

**The run.** `b56a1223-b046-4341-a0f3-366c4598286d`, exit 0, 26 turns, 25 tool calls, $2.31, 21:31–21:36Z. Brief on stdin, direct `claude -p --output-format stream-json --verbose`, teed to `~/goal-proof-logs-item5/01-grounding/`. Never through `orchestrate-stage.sh`.

**Commits:** `554e86db` (brief, alone) → `7b2f3a30` (transcript, output, meta, freshness row, `goal.md` state). Invariant 1 holds: `git merge-base --is-ancestor 554e86db 7b2f3a30` → OK.

**What it produced.** `goal.md` at `Status: draft` with four of the five field classes filled and three owner-held headings parked (§ Question wording, § Answered when, § Close rule). `trail.md` and `learnings.md` verified byte-identical to the templates — no round opened. No commit by the session.

**Validation, all passing:** `goal.md` is `draft`; no dated `### Round 1` entry; fence sweep CLEAN across 25 tool calls; freshness row present.

**Harness error 08a reproduced, exactly as the plan predicted.** The unanchored check `grep -rn '### Round 1'` returned two hits — both the trail template's literal `### Round 1 result — YYYY-MM-DD` placeholders. Re-run date-anchored (`— 2026-08-27`) it returns nothing, and `diff -q` against the template confirms `trail.md` is byte-identical. **A live instance of the failure Invariant 9 exists to catch.** For § Failures.

**The session did work the brief did not ask for, and it was right to.** It verified all three cited shas were still current, ran an arithmetic check off the study's own oracle scan (the re-basing is of the same order as the entire existing recirculating sum, so "negligible, leave it held" is not available without measuring), and stated plainly what that does *not* establish. It also found a **band discrepancy nobody had recorded**: DI-008 says ~60–190 MW; the research file it was minted from says the same three sources bracket 30–190 MW. It recorded it rather than resolving it, correctly — amending a DI is a reserved gate.

---

#### PREMISE SURPRISE — design bet B2 is measured and false

**What B2 claimed.** Row `#3`'s ambient text tells a reader that re-sourcing is the shape of the work, "but not which prerequisite blocks it, not that DI-008's strongest primary is un-ingested, and not whether the gap is satisfiable from what is already here. *If false → the discovery is staged before the run and criterion 1's word 'real' is hollow, whatever the trail says.*"

**What happened.** Walking the three evidence pointers R-A1 *requires* the brief to give it, session 01 established all three of those on its own and wrote them into `goal.md` § Grounding evidence:

- **Moscato et al., SOFT 2018, EUROfusion WPBOP-CPR(18) 20276**, by name and report number — "**Open PDF, not ingested.** This is the only source in the set that is a helium-primary *pumping-system design* rather than a single reported figure, and it is the one not in the repository."
- **Cismondi 2017 and Kessel/ARIES-ACT are ingested but unregistered** in `SOURCE_INDEX.md`, with the exact dossier paths and line numbers, verified.
- **The `research` seam is unrepaired**, and registering a source runs the WI-031 hand pattern.

**Why this is structural, not a mishap.** DI-008 *is* one of the three required grounding pointers, and DI-008's own model implication points one hop to the un-ingested primary. **You cannot ground this goal honestly without the grounding session finding the gap.** Re-grounding on a narrower evidence set would violate R-A1 and would not help.

**The general result.** The recorded gap *is* the readable gap. A need selected because it is documented is a need whose prerequisite is legible to anyone who reads the documentation. So a deliberately chosen need cannot yield blind discovery — not for this need, and not for any other. That is the item's finding about the goal layer, and it is worth more than the check it defeats.

**Ruled at gate (a), `[OWNER 2026-08-28]`.** Criterion 1 is **retired as unreachable by construction**. The owner's characterization of the retired check, recorded as given: it was **"a stupid test to begin with and was never going to work."** It tested the wrong thing.

**The framing this run carries from here (Ruling 2, `[OWNER 2026-08-28]`).** The workflow intent is not "the agent notices a specific source is missing." It is: *the agent recognizes that the repository's current data cannot answer the question and returns "research is needed"; a bounded, open-ended research round then runs through the seam — search, evaluate, register what is admissible, or return a bounded negative.* T-001's expected return is therefore **"research is needed to establish a defensible value"**, a judgment about the sufficiency of the current data. No artifact frames T-002 as fetching a known document; the request stays a question with `where_to_look` and limits, and any particular paper is one candidate a search may surface. T-001 still runs as a real bounded task and is graded on the work it does, not on blindness.

**What is NOT broken.** Invariant 3 binds *briefs*, and no brief contains any denied string — the mechanical fence held, and the self-checks passed. Invariant 2 held. § Question is a proper value question, not an errand, so the Phase 2 contingency for an errand-shaped question does not apply. § Invariants carries the channel and stops short of the comparison-meaning conclusion, as R-A6 requires. The guard did everything it was designed to do; the leak came through required evidence, which no fence on the brief could have closed.

**Not resolved by the operator.** Capture-fidelity Rule 4: a premise surprise is surfaced, never absorbed in either direction. Deleting a true finding from `goal.md` to protect a proof would be backwards, and the operator writes no goal file in any case. Parked for the owner at gate (a).

### Phase 2 Completion
**Completed:** **NOT STARTED — blocked before session 02 could run.**

**The block.** After the gate (a) resume, the session sandbox tightened twice. First, every write outside `/home/reid/1cfe/fusion-tea` was refused, which took away the `~/goal-proof-logs-item5/NN-<role>/` teeing the [RUN] block requires. That was surfaced and the orchestrator authorized the in-repo tee (below). Then the `claude` binary itself became unavailable — `claude -p …` and even `claude --version` return "This command requires approval". **No cold session can be launched**, so Phases 2–10 cannot proceed.

**Authorized deviation, recorded but not yet exercised — the in-repo tee.** `[AGENT]`, orchestrator-ruled, execution-detail tier. Each cold run tees directly to `sessions/NN-<role>/transcript.jsonl` instead of to `~/goal-proof-logs-item5/NN-<role>/`. That is where [RUN] step 4 copies the transcript anyway.

- **Given up:** only the copy outside the tree.
- **Not given up:** kill-recoverability. `tee` and shell redirection write incrementally, so a killed run still leaves its partial transcript at the in-repo path. (The operator's first framing said kill-recoverability was lost; that was wrong, and this corrected statement replaces it.)
- **Unchanged:** Invariant 1's brief-ancestry check and Invariant 2's fence sweep read the same files either way. Cold sessions still may not read the item directory, the denial stays in every brief, and the sweep still targets tool-call *inputs*. A transcript written into the item directory during a run is not a session read of it.
- Full write-up with the sandbox refusal text quoted: `operator-notes.md` § Mechanism notes. Belongs in `verification_record.md` § Failures at Phase 13 as a measured harness failure.

**On disk at the block.** HEAD `0e69a043`. Session 02's brief is written and committed, Invariant-3 self-check passed. `goal.md` is untouched since `7b2f3a30` and still `Status: draft`, so it authorizes no task. `trail.md` and `learnings.md` are still byte-identical to the templates — no round has opened. `sessions/05a-round-agent-t002/` is still deliberately untracked. Nothing is half-applied and no transcript is stranded.

**To resume:** restore the ability to invoke `claude`, then run session 02 as `--resume b56a1223-b046-4341-a0f3-366c4598286d` with `sessions/02-grounding/brief.md` on stdin, teed per the authorized deviation. Phase 2's validation and contingencies are unchanged.

### Phase 3 Completion
**Completed:**

### Phase 4 Completion
**Completed:**

### Phase 5 Completion
**Completed:**

### Phase 6 Completion
**Completed:**

### Phase 7 Completion
**Completed:**

### Phase 8 Completion
**Completed:**

### Phase 9 Completion
**Completed:**

### Phase 10 Completion
**Completed:**

### Phase 11 Completion
**Completed:**

### Phase 12 Completion
**Completed:**

### Phase 13 Completion
**Completed:**

---

**Status**: Draft → In Progress → Complete
