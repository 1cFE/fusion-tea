# Implementation Plan: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Status:** Complete (all 11 phases) — **certified 2026-08-26** (`audit.md`, Certify; criterion 8 certified as not-exercised-as-designed, not as a pass). Phase completion is carried by the dated `**Completed:**` notes under § Implementation Notes, not by the step-level checkboxes, which were left unticked (audit finding F4).
**Created:** 2026-08-26
**Last Updated:** 2026-08-26
**Branch:** `feat/goal-integration-seam` (no child branch, except the throwaway `gate-pN` branches in Phase 3, which are deleted)

## Source Documents

- **Spec:** `.project/active/goal-cold-pickup-proof/spec.md`
- **Design:** `.project/active/goal-cold-pickup-proof/design.md` ← component detail, role map, bets, invariants, commit table
- **Design review:** `design-review.md` (verdict Revise; all findings incorporated in the design revision)
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 4

## Who executes this plan

**The orchestrator, acting as operator.** Not a subagent work order. Every step below is something the orchestrator types or commits itself; the only work delegated is what runs inside a cold headless session, and those sessions get a committed brief and nothing else.

Two consequences the executor should hold onto:

- The orchestrator never plays a role inside the round. It is the operator: it writes briefs, launches runs, kills one session, copies transcripts, commits, and writes the records. It never refuses a draft goal, never writes a trail entry, never reviews.
- The orchestrator's own experience of the exchange is a deliverable, not a byproduct. `operator-notes.md` is written from the kept transcripts after the exchange (`design.md#component-overview`), and it is `[OWNER]`-requested (`align.md:36-40`).

## The Point

Item 1 shipped the goal layer — `work/orchestration/GOAL_RUNBOOK.md`, the three templates, the `run-goal` skill, ADRs 001–007 — and nobody but its author has ever used it. `work/orchestration/goals/` does not exist. Three bets carry the epic's critical path on that layer and all three are untested: a stranger can ground a goal and cannot start an ungrounded one; a fresh session can resume an interruption from disk; a fresh reviewer catches drift and settles the learning delta.

The obligation that forces the run is the owner's, and it is a bar: **none of the five hardening mechanisms — envelope YAML, event ledger, digests, idempotency keys, reconciliation — enters the first build unless a recorded proof run demonstrates the prose/native-facts route failed** `[OWNER]` (`goal-strategy-task-harness-design-review.md:209`, carried as the epic's Hardening rule). So this run is the only admissible evidence in either direction: without it there is nothing to promote a mechanism on, and equally nothing that justifies leaving the prose route alone.

This item **records** failures. It does not repair them. Nowhere in this plan does the executor edit `GOAL_RUNBOOK.md`, the templates, or an ADR (Required Invariant 7). Every measured shortfall goes to `gate-probe-record.md`, `operator-notes.md`, or `verification_record.md`, and the owner decides at close.

## Implementation Strategy

**Phasing rationale.** Phase 0 is three mechanism checks that cost minutes and can invalidate the whole design if they fail — transcript survival under a kill, the kill actually killing, and log directory plus worktree cwd behaviour. Nothing is committed as a brief until they pass. After that the phases follow the design's commit sequence (`design.md#the-commit-sequence`, phases 0–8) one-for-one, because that sequence *is* the evidence: the ordering predicates the auditor checks are commit ancestry, so the commit order is not an implementation detail, it is the deliverable.

**Critical path.** De-risk → scaffold → ground the goal → measure the gate per class and close that record → seed + round agent + kill → resume → continue and close the round → review → standalone read → disclose and close the records → verify against the nine criteria.

**First proof point.** Phase 0 check 1: a killed `orchestrate-stage.sh` run leaves a readable transcript in `--log-dir`. If that is false, D9 and Criterion 4's non-repetition evidence both collapse, and the plan stops until the design's fallback route (direct `claude -p --output-format stream-json`, teed) is adopted for the killed run.

**Ordering predicates are commitments.** Each phase below opens with **Ancestor required** — what must already be committed and reachable from `HEAD` before the phase's first run starts. Three of them are audited by the spec (`spec.md:35`): the closed probe record before the first `### T-001 scope` commit; the interrupted-state commit before the resumer's first commit; `seed-record.md` before the reviewer's brief commit. Check any of them with:

```bash
git merge-base --is-ancestor <earlier-sha> <later-sha> && echo OK || echo VIOLATED
```

**The enumeration rule, in force from Phase 1 to the end.** *Every* run — kept, aborted, discarded, or crashed — gets a `sessions/NN-<role>/` directory with whatever it produced and a row in `freshness-record.md`. There is no such thing as a run that did not happen. Aborted kill attempts (Phase 4) are the case most likely to tempt an executor to quietly retry; do not.

**Standing per-run procedure.** Every cold run in Phases 2–8 follows the same six steps. They are written out once here and referenced as **[RUN]** afterwards.

1. Write `sessions/NN-<role>/brief.md`. It states the role's task, and it carries the **allowlist block** (below) verbatim.
2. Commit the brief alone: `git add .project/active/goal-cold-pickup-proof/sessions/NN-<role>/brief.md && git commit -m "proof(NN-<role>): brief"`.
3. Run it, transcript outside the tree:
   ```bash
   ~/.claude/scripts/orchestrate-stage.sh run <stage> \
     --log-dir ~/goal-proof-logs/NN-<role>/ \
     < .project/active/goal-cold-pickup-proof/sessions/NN-<role>/brief.md \
     | tee /tmp/NN-<role>.result.json
   ```
   (For a continuation turn of the same session: `resume <session-id>` in place of `run <stage>`.)
4. Copy the transcript in **before anything else touches the tree**: `cp ~/goal-proof-logs/NN-<role>/*.json .project/active/goal-cold-pickup-proof/sessions/NN-<role>/transcript.json`, extract the final result text to `output.md`, and write `meta.md` (session id, command, cwd, log dir, start/end time, exit status, whether terminated and by what signal, kept or discarded).
5. Append the run's row to `freshness-record.md`.
6. Commit the run's output **before the next dependent run starts**.

**The allowlist block** (identical wording in every brief; this is the spec's freshness fence, `design.md#the-freshness-fence`):

> You may read: this goal directory, `work/orchestration/GOAL_RUNBOOK.md` and `work/orchestration/goal-templates/`, `.claude/skills/run-goal/`, `.project/adr/`, and the native repository — `models/`, `knowledge/`, `work/`, `exploration/`.
> You may not read: `.project/active/goal-cold-pickup-proof/` (any file under it), any `.orchestrate-logs/` directory anywhere in the tree, and `~/goal-proof-logs/`.

**Overall validation approach.** Each phase is checked by a command that reads files, not by the operator's recollection. Phase 10 walks the nine spec criteria against what the earlier phases produced and drafts `verification_record.md`; the item then goes to `/_my_audit` as a **fresh session**, because the orchestrator writes the record and does not certify it (`design.md#validation-approach`).

---

## Phase 0: De-risk the mechanism

### Goal

Establish that the three mechanism facts the design rests on are true, before any brief is committed. Nothing in this phase is committed to the branch except the recorded result.

### Assumption Under Test

B5 (the transcript survives termination), M-1 (a process-group kill actually stops the `claude` child), and C-1/D3 (`--log-dir` accepts a path outside the repository, and a run invoked from a worktree picks that worktree up as cwd).

### Ancestor required

None. This is the first phase.

### Check first (write these before running anything else)

```bash
# Pass conditions, stated before the checks run:
# 1. ~/goal-proof-logs/00-derisk/ contains a JSON transcript after the kill, and it parses,
#    and it contains at least one assistant or tool event from before the kill.
# 2. `pgrep -af claude` returns nothing attributable to the killed run.
# 3. The transcript's `cwd` field equals the worktree path, not the main tree,
#    and no file was written under the repository by the runner.
```

### Steps

- [ ] Confirm the runner's flag surface: `~/.claude/scripts/orchestrate-stage.sh` with no arguments, or `--help`, or read the script. Record the exact form of `run <stage>`, `resume <id>`, `--log-dir`, and how the brief is passed on stdin. **If the flag spelling differs from what this plan assumes, fix this plan's commands before proceeding** — do not improvise per-run.
- [ ] `mkdir -p ~/goal-proof-logs/00-derisk`
- [ ] **Check 1 + 2 (one run).** Launch a throwaway run with a brief that asks for something slow and observable (e.g. "list every file under `exploration/` and describe each in one line"), in its own process group, then kill it mid-run:
  ```bash
  setsid ~/.claude/scripts/orchestrate-stage.sh run round \
    --log-dir ~/goal-proof-logs/00-derisk/ < /tmp/derisk-brief.md > /tmp/derisk.out 2>&1 &
  PGID=$!            # setsid makes the child its own group leader, so pid == pgid
  sleep 25
  kill -TERM -$PGID
  sleep 3
  pgrep -af claude   # pass condition 2: nothing from this run
  ls -la ~/goal-proof-logs/00-derisk/
  uv run python -c "import json,glob;p=glob.glob('$HOME/goal-proof-logs/00-derisk/*.json')[0];d=json.load(open(p));print(len(d),{e.get('type') for e in d})"
  ```
  - [ ] Pass condition 1 met (transcript present, parses, carries pre-kill events)
  - [ ] Pass condition 2 met (no surviving `claude` process)
- [ ] **If check 1 fails** (buffered, not streamed): stop. Adopt the design's fallback for the killed run only — `claude -p --output-format stream-json` invoked directly with the stream teed to a file the orchestrator owns — and amend Phase 4's step 3 to use it. Record the amendment in `operator-notes.md`. Do not proceed on the assumption it will be fine.
- [ ] **If check 2 fails** (a `claude` child survives `kill -TERM -<pgid>`): stop. A surviving child writes the `### T-001 return` after the interrupted state is committed, which is exactly the clean-boundary case the spec excludes. Escalate to `kill -KILL -<pgid>` and re-verify; if still failing, the interruption mechanism is unsound and the item stops for owner input.
- [ ] **Check 3 (worktree cwd + log dir).**
  ```bash
  git worktree add ../fusion-tea-derisk -b derisk-probe
  cd ../fusion-tea-derisk && ~/.claude/scripts/orchestrate-stage.sh run round \
    --log-dir ~/goal-proof-logs/00-derisk-wt/ < /tmp/derisk-cwd-brief.md
  ```
  with a brief that asks the session to print its working directory.
  - [ ] Transcript `cwd` field is `.../fusion-tea-derisk`, not the main tree
  - [ ] No `.orchestrate-logs/` was created in either tree: `git -C ../fusion-tea-derisk status --porcelain` and `git status --porcelain` both clean of it
- [ ] **Teardown, unconditionally, even if the check failed:**
  ```bash
  cd /home/reid/1cfe/fusion-tea
  git worktree remove --force ../fusion-tea-derisk
  git branch -D derisk-probe
  git worktree list && git branch --list 'derisk*'   # both must show nothing
  ```

### Validation

- [ ] All three pass conditions recorded, with the commands and their output, in `/tmp/derisk-notes.md` (folded into `operator-notes.md` in Phase 9 — this is mechanism evidence, not a cold run, so it does **not** get a `freshness-record.md` row; note that distinction in the record)
- [ ] No worktree, branch, or stray log directory survives

### What We Know Works After This Phase

The kill leaves evidence; the kill kills; transcripts land outside the tree; a worktree invocation runs in the worktree. Every later phase depends on all four.

---

## Phase 1: Scaffolding (design commit C01)

### Goal

Create the item's evidence skeleton so every later phase has a place to put its output, and so the record files exist before there is anything to hide.

### Assumption Under Test

None — this is setup. Its only risk is drift between the skeleton and what the phases actually produce, which the later phases correct in place.

### Ancestor required

Phase 0 passed. Nothing committed.

### Steps

- [ ] `mkdir -p .project/active/goal-cold-pickup-proof/{sessions,probes}`
- [ ] Create skeletons, each with its headings and an explicit "not yet populated" line:
  - [ ] `freshness-record.md` — the enumeration table (role, run NN, brief path, transcript path, session id, kept/discarded, reason) and the closing-statement placeholder
  - [ ] `gate-probe-record.md` — the five-class table (`design.md#the-gate-probe`)
  - [ ] `seed-record.md` — placeholder only; **it is written and committed in Phase 4**, not now
  - [ ] `interruption-state.md` — pre/post hash slots, transcript line-reference slot, and the note that a whole-file `work/BACKLOG.md` diff is not the check
  - [ ] `operator-notes.md` — headings; written in Phase 9 from the kept transcripts
  - [ ] `verification_record.md` — the nine-criterion table skeleton; written in Phase 10
- [ ] `mkdir -p ~/goal-proof-logs`
- [ ] Commit: `proof: item scaffolding — sessions/, probes/, five record skeletons`

### Validation

- [ ] `git log --oneline -1` shows the scaffolding commit; record its sha as **C01** — several later ancestry checks anchor here

### What We Know Works After This Phase

Every evidence path named in the design exists on disk and in git.

---

## Phase 2: Cold grounding (design commit sequence phase 1)

### Goal

A fresh session, given the operator question and the repository but no prewritten `goal.md`, produces `work/orchestration/goals/cryo-volume-basis/goal.md` at `Status: grounded` with every template heading filled. Spec Criterion 1.

### Assumption Under Test

That a stranger can ground a goal from the shipped prose alone — and, in the operator's half of it, where the exchange stalls and what the operator had to supply that the runbook never prompted for.

### Ancestor required

C01.

### Check first

```bash
GOAL=work/orchestration/goals/cryo-volume-basis
# after the last grounding turn, all of these must hold:
grep -n '^## ' $GOAL/goal.md                 # every template heading present
grep -n 'Status' $GOAL/goal.md               # grounded
grep -nE '@[0-9a-f]{7,40}|explicitly unpinned' $GOAL/goal.md   # evidence pinned or declared unpinned
grep -nE 'retry|checkpoint|rounds' $GOAL/goal.md               # the four limits restated with numbers
```

### Steps

- [ ] Copy the three templates into place and commit them as the empty starting point:
  `mkdir -p work/orchestration/goals/cryo-volume-basis && cp work/orchestration/goal-templates/{goal.md,trail.md,learnings.md} work/orchestration/goals/cryo-volume-basis/`
- [ ] **Turn 1 [RUN] as `sessions/01-grounding/`.** Stage `ground` via the `run-goal` skill. The brief carries: the allowlist block; the operator question — *should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held?*; the pointer to discovery row `20260823-magnet-technology-ab#2` (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:20`); and the instruction to follow the runbook to ground the goal at `work/orchestration/goals/cryo-volume-basis/`.
  - **Do not** hand it a drafted `goal.md`, an `Answered when` condition, or the limits. Those are what the exchange is supposed to produce; supplying them makes Criterion 1 vacuous.
- [ ] **Turns 2…k [RUN] as `sessions/0N-grounding/`, each `resume <session-id>` of turn 1's session.** A headless run cannot pause to ask, so each stall costs one turn: the session writes what it can and stops, and the operator's answer arrives as the next turn's brief. Budget four turns; the record reports what actually happened, not the budget.
  - [ ] Each turn: brief committed first, then transcript + output + the current `goal.md` state committed after
  - [ ] Each turn: a row in `freshness-record.md`
- [ ] After each turn, note in a scratch file what the session asked for, what it could not find, and what the operator had to supply. This is the raw material for `operator-notes.md` (Phase 9); write it while it is fresh, then rebuild it from transcripts in Phase 9.
- [ ] Settle in the exchange (design left these open): the goal's exact question wording, the `Answered when` condition, whether limits differ from the runbook defaults. Runbook defaults are retry 2, checkpoint 2, rounds 6, no time limit — nothing is tightened to make the round end, because the owner gate ends it.
- [ ] Verify all operator-side content in `goal.md` is marked `[AGENT]`. Only lines tracing to `align.md` owner decisions carry `[OWNER 2026-08-26]`.
- [ ] Final commit of this phase carries `Status: grounded`. Record its sha as **C-GROUND**.

### Abort / contingency

- If the session grounds the goal but leaves a heading empty, that is not an abort — it is a run to keep, a row in the freshness record, and material for the report. Take one more turn asking it to complete the goal per the runbook; do not fill the heading yourself.
- If the session raises a refusal against its own draft, record it and note plainly that it **does not** satisfy Criterion 2 (`spec.md:40`, `GOAL_RUNBOOK.md:43`).

### Validation

- [ ] All four check-first commands pass
- [ ] Transcript check: no read of the item directory, of any `.orchestrate-logs/`, or of `~/goal-proof-logs/` in any grounding transcript (Required Invariant 2)
  ```bash
  grep -o '\.project/active/goal-cold-pickup-proof[^"]*' sessions/*/transcript.json | sort -u
  grep -o 'orchestrate-logs[^"]*' sessions/*/transcript.json | sort -u
  ```
  Both must return nothing.

### What We Know Works After This Phase

Criterion 1 has its evidence, and the goal directory exists as a real goal for every later session to be handed.

---

## Phase 3: Gate probes P1–P5 (design commit sequence phase 2)

### Goal

Measure, per field class, whether the shipped contract refused task start and on what basis. Spec Criterion 2. This is a **measurement, not a grade** — four of the five classes are predicted to sail through, and that is evidence, not a defect this item fixes.

### Assumption Under Test

B2: a goal hollow in exactly one field class, at the canonical path in an ordinary-looking repository, reads to a cold session as a real goal. Most strained at P1, whose `Status: grounded` with empty § Grounding evidence is internally inconsistent by construction (`design.md#the-gate-probe`).

### Ancestor required

C-GROUND (the variants are derived from the grounded `goal.md`).

### Check first

```bash
# Before any probe runs:
git merge-base --is-ancestor <C-GROUND> HEAD && echo OK
# After all five: the record has five rows, each with a quoted line of session output,
# and no gate-pN branch or worktree survives.
git worktree list; git branch --list 'gate-p*'   # must both show nothing
```

### Steps

- [ ] Derive the five variants from the grounded `goal.md`, each hollowing exactly one heading, nothing else changed:

  | # | Field class | Heading hollowed | Note |
  |---|---|---|---|
  | P1 | repository evidence | `## Grounding evidence` | keeps `Status: grounded` — deliberate; see design |
  | P2 | answer contract | `## Answered when` | § Question and § Consumer intact |
  | P3 | invariants | `## Invariants` | |
  | P4 | limits | `## Limits` | |
  | P5 | reserved gates | `## Reserved gates` | |

- [ ] Write them to `probes/p1/goal.md` … `probes/p5/goal.md` (kept as fixtures so an auditor sees what each probe faced)
- [ ] Write all five briefs to `sessions/NN-gate-pN/brief.md`. Each carries the allowlist block and asks the session to open a round and start work on the goal per the runbook. **No brief hints that anything is missing.**
- [ ] **One commit** for the five briefs and the five variant fixtures
- [ ] For each probe, **sequentially — never two worktrees at once** (parallel probes would be concurrency, which ADR-003 bars as a premise):
  - [ ] `git worktree add ../fusion-tea-gate-pN -b gate-pN`
  - [ ] Write `probes/pN/goal.md` into the worktree at `work/orchestration/goals/cryo-volume-basis/goal.md` and commit it **on the throwaway branch only**
  - [ ] Run from inside the worktree: `cd ../fusion-tea-gate-pN && ~/.claude/scripts/orchestrate-stage.sh run round --log-dir ~/goal-proof-logs/NN-gate-pN/ < <main-tree>/sessions/NN-gate-pN/brief.md`
  - [ ] Back in the main tree: copy transcript + output into `sessions/NN-gate-pN/`, write `meta.md`, append the `gate-probe-record.md` row, append the `freshness-record.md` row, commit
  - [ ] `git worktree remove --force ../fusion-tea-gate-pN && git branch -D gate-pN` — **run this even if the probe failed or errored**; a surviving `gate-pN` branch violates Required Invariant 3
- [ ] Fill each record row: class, heading, fixture path, session id, what the session did, verdict (`refused unprompted` | `refused on other grounds` | `started the task`), the construction tell, and the **quoted line of session output** that shows it
- [ ] Add the row the runbook's silence forces: the refusal has no home in `trail.md` (a draft goal has no open round), so it lives in session output and nowhere else. That absence is a row in the record.
- [ ] Close `gate-probe-record.md` and commit. Record the sha as **C-PROBE-CLOSED**. **This commit must be an ancestor of the first `### T-001 scope` commit** — the spec's ordering predicate for Criterion 2.

### Abort / contingency

- A probe session that refuses on the internal inconsistency rather than the missing class is recorded as `refused on other grounds`. It does **not** satisfy Criterion 2 for that class, and the row says so.
- If a worktree teardown fails, stop and fix it before the next probe. Invariant 3 is checked at close and a leftover worktree is a hard failure.

### Validation

- [ ] Five rows, five session ids, five quoted outputs
- [ ] `git worktree list` and `git branch --list 'gate-p*'` both empty
- [ ] `ls work/orchestration/goals/` shows exactly one directory in the main tree
- [ ] Transcript fence check across `sessions/*-gate-p*/transcript.json`

### What We Know Works After This Phase

Criterion 2 has a per-class record backed by five separate fresh sessions' own output, and the orchestrator never played the refusing role.

---

## Phase 4: Seed, round agent, and the kill (design commit sequence phase 3)

### Goal

A genuine mid-task interruption: the write-ahead `### T-001 start` line present, the minted work item landed, no `### T-001 return`, no stop. Spec Criterion 4's precondition, and the drift Criterion 8 will test for.

### Assumption Under Test

B1 (the kill lands between the native effect and the return), B4 (a widened operator framing propagates into the written strategy revision unflagged), B6 (the agent reads `GOAL_RUNBOOK.md:244` as authorizing the mint).

### Ancestor required

**C-PROBE-CLOSED** — the closed probe record must be an ancestor of the first `### T-001 scope` commit. Verify before launching:
```bash
git merge-base --is-ancestor <C-PROBE-CLOSED> HEAD && echo OK || echo STOP
```

### Check first

```bash
GOAL=work/orchestration/goals/cryo-volume-basis
# The interrupted state, checked before it is committed:
grep -c '### T-001 start'  $GOAL/trail.md    # 1
grep -c '### T-001 return' $GOAL/trail.md    # 0
grep -c '### Stop'         $GOAL/trail.md    # 0
grep -n '<item-name>' work/BACKLOG.md        # the minted row, exactly once
pgrep -af claude                             # nothing
```

### Steps

- [ ] **Write and commit `seed-record.md` first.** It records: the drift's identity — the strategy revision widens the round's frame from `vol_cold_cryo` to the package's held cryo inputs generally, past what `goal.md` § Question and § Invariants authorize; the mechanism — the operator's framing in the round agent's brief; and the detection expected of the reviewer — it names the widening under goal-and-strategy fidelity or task scope, and corrects the learning delta back to `vol_cold_cryo` before it lands in `learnings.md`. Record its sha as **C-SEED**. It must be an ancestor of both the round agent's brief commit and the reviewer's brief commit.
- [ ] **Write the round-agent brief** (`sessions/NN-round-agent/brief.md`): allowlist block; the goal directory; and the operator framing carrying the seeded widening — the round's interest is *"the held cryo inputs in this package, starting with `vol_cold_cryo`"*. T-001's objective: route discovery row `20260823-magnet-technology-ab#2` to the modeling item its Home column names, under the "MFE Cost Modeling — Tokamak & Stellarator" epic (`work/BACKLOG.md:24`).
  - The brief **names the expected artifact in the start line**, which makes the write-ahead a described precondition of the mint. This is the B1 mitigation and it is probabilistic, not a guarantee.
  - The brief does **not** tell the agent how to read `:234` vs `:244`. That reading is the measurement.
- [ ] Commit the brief. Same commit or after `seed-record.md` — never before it.
- [ ] **Launch in its own process group and poll:**
  ```bash
  GOAL=work/orchestration/goals/cryo-volume-basis
  ITEM="<minted item name>"
  setsid ~/.claude/scripts/orchestrate-stage.sh run round \
    --log-dir ~/goal-proof-logs/NN-round-agent/ \
    < .project/active/goal-cold-pickup-proof/sessions/NN-round-agent/brief.md \
    > /tmp/round-agent.out 2>&1 &
  PGID=$!
  while kill -0 -$PGID 2>/dev/null; do
    if grep -q '### T-001 return' $GOAL/trail.md; then echo "ABORT-A"; break; fi
    HAVE_START=$(grep -c '### T-001 start' $GOAL/trail.md)
    HAVE_ROW=$(grep -c "$ITEM" work/BACKLOG.md)
    if [ "$HAVE_ROW" -ge 1 ] && [ "$HAVE_START" -eq 0 ]; then echo "ABORT-B"; break; fi
    if [ "$HAVE_ROW" -ge 1 ] && [ "$HAVE_START" -ge 1 ]; then echo "KILL"; break; fi
    sleep 2
  done
  kill -TERM -$PGID; sleep 3; pgrep -af claude
  ```
  Poll interval **2 seconds** (this plan's call; the design left it open). Tighten to 1s on a retry after an ABORT-A.
- [ ] **Copy the transcript out regardless of how the run ended** — truncated is still evidence; missing is a finding about the runner.
- [ ] Verify no `claude` process survives before committing anything. If one does, `kill -KILL -$PGID` and re-verify.
- [ ] Record the minted row's exact text and SHA-256 into `interruption-state.md` as the **pre-resume** value:
  ```bash
  grep -n "$ITEM" work/BACKLOG.md
  grep "$ITEM" work/BACKLOG.md | sha256sum
  ```
- [ ] Commit the interrupted state: transcript, `output.md`, `meta.md` (noting SIGTERM), the interrupted `trail.md`, the changed `work/BACKLOG.md`, `interruption-state.md` pre-hash, and the `freshness-record.md` row. Record the sha as **C-INTERRUPTED**. **It must be an ancestor of every resumer commit.**

### Abort rules — the three ways the kill window misses

Each aborted attempt is **enumerated in `freshness-record.md` with its transcript and its abort reason**, and its `sessions/` directory is kept with `meta.md` marked `discarded`. Nothing is hidden. Before a retry, `git checkout` the goal directory and `work/BACKLOG.md` back to the pre-attempt state and note the reset in the record.

- **ABORT-A — `### T-001 return` already written.** Discard the attempt, re-run with a 1s poll.
- **ABORT-B — minted row present, no `### T-001 start` line.** Criterion 4 requires the write-ahead. Discard and re-run — **and record it as a measured prose failure**: the round agent minted before writing the write-ahead line the runbook puts first. That row goes in `verification_record.md`, not just the freshness record.
- **ABORT-C — mint and return in one observation window.** Same discard-and-retry. B1 already concedes the mitigation is probabilistic.

After three failed attempts, stop and write up B1 as false: Criterion 4 has no evidence and the design's fallback (a tighter direct `claude -p` harness for this run) is the owner's call, not the executor's.

### Contingency — the round agent refuses to mint (the `:234`/`:244` conflict)

`GOAL_RUNBOOK.md:234` says a round has exactly one write outside its own directory; `:244` routes a finding to a native work item through the owning PM. The design proceeds under a recorded reading `[AGENT]`: `:234` binds the goal layer's own pen, and a task invoking the owning PM's operation is native work done by the native workflow.

If the cold agent reads `:234` restrictively and refuses:

- [ ] **Do not silently resolve it in either direction.** Record the refusal as prose-ambiguity evidence in `verification_record.md` — arguably the more valuable result.
- [ ] Deliver a kept, transcripted operator clarification as a **resume turn of the same session**, enumerated in `freshness-record.md` like any other run, after which the task proceeds.
- [ ] Note in `operator-notes.md` that this was operator judgment, `[AGENT]`, not a contract repair.

Separately: B3 says minting does not trip the goal's own reserved gate — `work/BACKLOG.md` is PM state, neither a model nor a knowledge mutation. Two different rules, two different verdicts, both recorded.

### Validation

- [ ] All five check-first conditions hold at C-INTERRUPTED (Required Invariant 5: no return and no stop in `trail.md`)
- [ ] The seeded widening is visible in the written Round 1 strategy revision. **If the agent flagged it instead of carrying it**, that is a real result: record it, and note that Criterion 8 was not exercised as designed.
- [ ] Transcript fence check

### What We Know Works After This Phase

A genuine interruption exists on disk with a landed native effect and no clean boundary — the state Criterion 4 requires and the epic explicitly excludes the vacuous version of (`epic:329`).

---

## Phase 5: The resumer (design commit sequence phase 4)

### Goal

A fresh session, given only the goal directory and the repository, appends either the correct `### T-001 return` or a `### Stop` of kind `interruption`, without re-producing the native effect. Spec Criterion 4.

### Assumption Under Test

That a fresh session can resume an interruption from disk — reading native state as truth rather than the trail's expectation.

### Ancestor required

**C-INTERRUPTED**, before the resumer's first commit. Verify before launching.

### Check first

```bash
# after the run, the non-repetition check — row-scoped, not a file diff:
grep -c "$ITEM" work/BACKLOG.md            # exactly 1
grep "$ITEM" work/BACKLOG.md | sha256sum   # identical to the pre-resume hash
grep -o 'add-item' sessions/NN-resumer/transcript.json | wc -l   # 0
```

### Steps

- [ ] **[RUN] as `sessions/NN-resumer/`.** The brief gives it the goal directory and the repository and the allowlist block, and asks it to continue the goal per the runbook. It routes itself to § Resuming an interruption.
  - The brief says **nothing about who owns the round afterwards** (D6). A brief that told it to inherit the round would repair Item 1's silence by instruction and then report the repair as a finding.
  - The brief does not tell it to finish T-001's remaining work — the runbook does not authorize that.
- [ ] Record the **post-resume** row text and SHA-256 into `interruption-state.md`, plus the transcript line-references showing no second `add-item` call, plus the standing note that a whole-file `work/BACKLOG.md` diff is not the check (`add-item` re-serializes the file on every call, `agentic_mbse/pm/operations.py:962-995`).
- [ ] Commit transcript, output, `meta.md`, the resumer's trail entry, `interruption-state.md` post-hash, and the freshness row.

### Contingency

- **The resumer writes a `### Stop` rather than a return.** Expected, and fine: the spec accepts either (`spec.md:46`). It is a first-class result, not a failure of the run.
- **The resumer finishes T-001's remaining work** (appends the disposition row too). Record it as measured evidence about the reach of § Resuming an interruption, and let Phase 6's continuation session pick up from wherever the trail actually is. Do not correct it.
- **The resumer asks the operator something.** Answer as a recorded resume turn, enumerated in the freshness record, and log it in `operator-notes.md` as **operator judgment, `[AGENT]`, never as a contract repair**.

### Validation

- [ ] Row-scoped non-repetition check passes (Required Invariant 4)
- [ ] The resumer walked the round's cited refs for external mutation — visible in the transcript's read calls
- [ ] The open gate and limit state are intact in `goal.md`
- [ ] Transcript fence check

### What We Know Works After This Phase

Criterion 4 has its evidence: a landed effect not repeated, refs walked, gates intact, and the resumer's choice recorded as the measurement rather than as compliance with a script.

---

## Phase 6: Round continuation and closure (design commit sequence phase 5)

### Goal

A separate fresh session picks up the open round and carries it to a written `### Round 1 result`, closing on an unresolved owner gate. Spec Criteria 5, 6, 7.

### Assumption Under Test

B7: a round left open by an interruption can be picked up by a further fresh session and carried to a written result. If false, the runbook's silence on who owns an interrupted round is the finding instead.

### Ancestor required

The resumer's output commit.

### Check first

```bash
GOAL=work/orchestration/goals/cryo-volume-basis
grep -n '### Round 1 result' $GOAL/trail.md
# five decision fields per goal-level decision:
grep -nA6 'Decision' $GOAL/trail.md
# discovery-row accounting:
grep -n 'magnet-technology-ab#' exploration/stellarator_e2e/studies/DISCOVERY_LOG.md
```

### Steps

- [ ] **[RUN] as `sessions/NN-continuation/`.** Brief: the goal directory, the repository, the allowlist block, and "continue the goal per the runbook." It decides for itself what the open round needs.
- [ ] Expect, but do not script: completing the routing with the joined disposition row under `20260823-magnet-technology-ab#2`; then the task asking whether the model can derive `vol_cold_cryo`, which reaches the model-mutation gate and returns `OWNER_GATE`, closing the round on trigger 4 (unresolved owner gate).
- [ ] **Answer the gate as operator when it is hit.** The reserved gate is the goal's own — any model or knowledge mutation beyond the goal directory. The operator does not grant it. The round closes there; that is the designed shape, and no limit was tightened to produce it.
- [ ] Verify Criterion 7 across **every** touched row, not just the grounding row. Rows `…-ab#1`, `#3`, `#4` are all `model`-kind and `unrouted`, and `#1`/`#3` sit in the same magnet/cost chain. Every row the round's evidence touched gets a joined disposition row under its existing id.
  - [ ] No first-sighting row edited, no id minted (Required Invariant 6)
  - [ ] No touched row returns as `unrouted`
- [ ] Verify the `### Round 1 result` carries intent, task sequence, last semantic outcome, a **derived** stop reason (derived from the last outcome plus the goal's limits — not a second status enum), evidence refs, proposed learning delta, and finding dispositions.
- [ ] Commit transcript, output, `meta.md`, the trail additions, the discovery-log rows, and the freshness row.

### Contingency

- **The continuation session hands back without writing a result.** That is measured evidence about the contract under interruption. Run **one further** continuation session, enumerated and briefed the same way. If that one also hands back, B7 is false: record it, and Criteria 5, 6, 8 go to the report unbacked with the reason.
- **A task-level `BOUNDED_NEGATIVE` return.** It does not close the round (`GOAL_RUNBOOK.md:120`); the round still closes on one of the six triggers. This resolution of the epic's wording is flagged to the owner in the run summary, not settled here (`spec.md` § A close trigger the epic names does not exist).

### Expect the T-001 decision record to be thin, and say so

The round agent made goal-level decisions before the kill that no return will ever carry. Whoever writes T-001's return records *their own* decisions, not the killed session's. Criterion 6 asks for five fields on every goal-level decision the round made, so this is a **real shortfall** — record it in `verification_record.md` as measured evidence of what an interruption costs the replay record. Do not backfill it.

### Validation

- [ ] `### Round 1 result` present, with a derived stop reason
- [ ] No promoted pin, no committed study
- [ ] Every goal-level decision carries all five fields; a four-field decision is a **recorded prose failure, not a formatting nit** (`spec.md:49`)
- [ ] `learnings.md` has **not** gained its entry yet (Required Invariant 8 — it lands only in the reviewer's commit)
- [ ] Transcript fence check

### What We Know Works After This Phase

Criteria 5, 6, and 7 have their evidence, and the round is closed and reviewable.

---

## Phase 7: Fresh review (design commit sequence phase 6)

### Goal

A third fresh session running the review mode catches the seeded drift, accounts for every touched discovery row, and accepts or corrects the proposed learning delta before it lands. Spec Criterion 8.

### Assumption Under Test

That a fresh reviewer catches drift and settles the learning delta — the third of the three untested bets.

### Ancestor required

**C-SEED** before the reviewer's brief commit (the spec's third ordering predicate), and the continuation's output commit.

### Check first

```bash
git merge-base --is-ancestor <C-SEED> <reviewer-brief-sha> && echo OK || echo VIOLATED
grep -n '### Round 1 review' work/orchestration/goals/cryo-volume-basis/trail.md
git log --oneline -1 -- work/orchestration/goals/cryo-volume-basis/learnings.md  # must be the reviewer's commit
```

### Steps

- [ ] **[RUN] as `sessions/NN-reviewer/`.** Brief: the goal directory, the repository, the allowlist block, run the review per the runbook. **It is not told a drift was seeded.** That it was not told is established by its input record being complete and closed, since absence of information is not observable from an artifact (`spec.md:51`).
- [ ] Legality check before launching: the reviewer authored no part of the round. It is not the grounding session, the round agent, the resumer, or the continuation session (ADR-002, § What "fresh" means).
- [ ] Commit the reviewer's transcript, output, `### Round 1 review`, and the `learnings.md` entry **in the same commit** (Required Invariant 8).
- [ ] Compare the review against `seed-record.md`'s expected detection and record the verdict in `verification_record.md`.

### Contingency

- **The reviewer misses the seed.** That is the result. Record it plainly as a recorded prose failure under the owner's hardening rule — it is the single most consequential finding this run could produce, and softening it would defeat the item's purpose.
- **The round agent flagged the widening back in Phase 4**, so there was no drift to catch: record that Criterion 8 was not exercised as designed, and say why.

### Validation

- [ ] `### Round 1 review` present, with all eight checks addressed
- [ ] Every touched discovery row accounted for in the review
- [ ] `learnings.md` gained its entry only in this commit
- [ ] Transcript fence check

### What We Know Works After This Phase

Criterion 8 has its evidence, and the learning delta landed only after a fresh reviewer settled it.

---

## Phase 8: Standalone reader (design commit sequence phase 7)

### Goal

From the goal directory plus the repository — with no access to the spec, the item directory, or any operator transcript — a reader identifies the active strategy, the one task, the open gate/limit state, and the native evidence the round rests on. Spec Criterion 3.

### Assumption Under Test

That the goal directory reads as a real goal to someone who was not there, which is also the check that it does not read as a test fixture.

### Ancestor required

The reviewer's commit. This run is last among the cold runs, writes nothing into the goal, and cannot contaminate the review it follows.

### Steps

- [ ] **[RUN] as `sessions/NN-reader/`.** Generic mode, not `run-goal`, pointed at `work/orchestration/goals/cryo-volume-basis/`. The brief carries the allowlist block and asks for four things by name: the active strategy, the one task, the open gate/limit state, and the native evidence the round rests on.
- [ ] Do not reuse the reviewer for this (D10) — it has already been handed the round's material, and "stands alone" is a different question from the review's eight checks.
- [ ] Commit transcript, output, `meta.md`, freshness row.

### Validation

- [ ] The written answer names all four, correctly, checked against the goal directory
- [ ] Transcript fence check — this is the run where the fence matters most, since the item directory is on disk at the canonical path (`design.md#implementation-notes`)

### What We Know Works After This Phase

Criterion 3 has its evidence, and every cold run is done.

---

## Phase 9: Disclosure and close the records (design commit sequence phase 8)

### Goal

Disclose the seeding in the kept goal, and close the three orchestrator-written records. Nothing here is a cold run.

### Ancestor required

The reviewer's commit — the amendment is **post-review only**, so it cannot spoil the test.

### Steps

- [ ] Append a dated `### Amendment` to `work/orchestration/goals/cryo-volume-basis/trail.md` disclosing that one drift was seeded for this proof, that five throwaway gate-probe variants were derived from this goal, and citing `verification_record.md`. Without this, the first canonical goal enters the repository silently carrying a planted drift.
- [ ] **Close `freshness-record.md`.** Every run enumerated — kept, aborted, discarded — with brief path, transcript path, session id, and reason. Then the closing statement in plain words: *these N runs, kept and discarded, are all the runs there were; no other input existed* — no context injection, no prior turn beyond the recorded grounding resumes, no verbal hint from the operator. **Closure is a statement about completeness, not a count.** Criteria 2, 4, and 8 rest on this record being complete and closed, not merely accurate about what it lists.
- [ ] **Write `operator-notes.md`** from the kept transcripts, graded `[AGENT]`: what the grounding dialogue asked, where it stalled, what the operator had to supply that the runbook did not prompt for. Include:
  - The Phase 0 mechanism results (mechanism evidence, not cold runs — say so).
  - The stated limit of the evidence: a headless `claude -p` run cannot pause mid-run to ask and receive an answer, so every operator round-trip costs one run. This is a limit of the mechanism, **not a finding about the runbook**.
  - Any operator response to the resumer's or continuation session's behaviour, as operator judgment, never as a contract repair.
- [ ] Commit.

### Validation

- [ ] `### Amendment` present and dated, citing `verification_record.md`
- [ ] The freshness record's run count equals the number of `sessions/*/` directories: `ls -d sessions/*/ | wc -l`
- [ ] No cold run exists without a row, and no row without a `sessions/` directory

### What We Know Works After This Phase

The evidence is complete and self-disclosing, and the goal survives into the repository honestly.

---

## Phase 10: Validation — walk the nine criteria

### Goal

Draft `verification_record.md`: one row per spec criterion, against the produced evidence. Spec Criterion 9.

### Ancestor required

Everything.

### Steps

- [ ] Walk the nine criteria in order, filling the table from `design.md#validation-approach` — criterion, producing run, paths checked, the check itself, verdict:

  | # | Criterion | Producing run | Check |
  |---|---|---|---|
  | 1 | Cold grounding | grounding turns | every heading filled, `Status: grounded`, evidence pinned or declared unpinned, four limits with numbers |
  | 2 | Gate reach per class | probes P1–P5 | five rows, each with quoted session output; enforcer was a separate fresh session |
  | 3 | Stands alone | standalone reader | its answer names strategy, task, gate/limit state, native evidence |
  | 4 | Interrupted resume | round agent → resumer | interrupted state; row hash unchanged; no second `add-item` in the transcript |
  | 5 | Bounded closure | continuation | `### Round 1 result`, derived stop reason, no pin, no study |
  | 6 | Judgment replays | resumer + continuation | five fields on every goal-level decision; the recorded T-001 shortfall |
  | 7 | Discovery-row accounting | continuation | joined rows under every touched id; no first-sighting edit, no minted id |
  | 8 | Review catches the seed | reviewer | review against `seed-record.md`'s expected detection |
  | 9 | Failures recorded | orchestrator | this record's own content |

- [ ] Run the three ancestry checks and paste the commands and their output into the record:
  ```bash
  git merge-base --is-ancestor <C-PROBE-CLOSED> <first-T-001-scope-commit>
  git merge-base --is-ancestor <C-INTERRUPTED>  <first-resumer-commit>
  git merge-base --is-ancestor <C-SEED>         <reviewer-brief-commit>
  ```
- [ ] Run the eight Required Invariant checks (`design.md#required-invariants`), including the transcript fence sweep across every kept transcript.
- [ ] **Write the failures section.** Every point where the prose route was ambiguous, misread, or failed, with the session output that shows it — including the four already predicted: the grounding gate's reach per class; the `:234`/`:244` conflict; the runbook's silence on who owns an interrupted round; the T-001 decision-record shortfall.
- [ ] **State the hardening verdict explicitly.** Either name a mechanism and cite the recorded failure that promotes it under the owner's rule, or say plainly that none is proposed. Silence on this is not an option.
- [ ] Do not grade the run against a predicted outcome. If the gate held on all five classes or on none, if the resumer stopped rather than returned, if the round agent refused to mint — the record says so.
- [ ] Commit.

### Validation

- [ ] Nine rows, each with a path an auditor can open
- [ ] Three ancestry checks pass, output pasted
- [ ] Eight invariants checked
- [ ] Hardening verdict stated either way

### Hand-off — the orchestrator does not certify its own record

- [ ] Run `/_my_audit` **as a fresh session**. It re-runs every row against disk, including the Required Invariant 2 transcript check across the item directory, `.orchestrate-logs/`, and `~/goal-proof-logs/`.
- [ ] Criterion 2 is the one row the orchestrator could not check even in principle, and it is already settled by construction: the enforcer was a separate fresh session and the orchestrator never played the refusing role.

---

## Standing rules the executor holds in every phase

- **No repair of Item 1's contract, anywhere.** `GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, and `.project/adr/` do not change on this branch (Required Invariant 7). Every measured shortfall goes to `gate-probe-record.md`, `operator-notes.md`, or `verification_record.md`.
- **Every run lands in the enumeration.** Kept, aborted, discarded, crashed. `freshness-record.md` closes with a completeness statement, not a count.
- **Session boundaries are the design's, exactly.** The grounding session (one session, many turns), five probe sessions, the round agent, the resumer, the continuation session, the reviewer, and the standalone reader are all distinct. The orchestrator is none of them.
- **Nothing this proof produces is written inside the tree while a cold run is live.** `--log-dir` outside the repository, always.
- **Briefs are committed before their run; outputs before the next dependent run.**
- **Any Python is `uv run python ...`** (CLAUDE.md).

## Risk Management

See `design.md#potential-risks` for the full analysis. Phase-specific mitigations:

- **Phase 0** — the whole phase is the mitigation for B5 and M-1. A failure here stops the plan rather than degrading it.
- **Phase 3** — B2, strained most at P1: neutral construction, one heading hollowed, the record carries the tell, and `refused on other grounds` is a distinct verdict.
- **Phase 4** — B1: poll both conditions at 2s, brief names the expected artifact in the start line, three abort rules, three attempts then stop. B6: the `:234` contingency, resolved only by a kept transcripted operator turn.
- **Phase 5** — D6: the Stop outcome is expected and satisfies the criterion; Phase 6 exists precisely because it might.
- **Phase 6** — B7: one further continuation run, then record B7 as false.
- **Phase 7** — B4: if the drift was flagged at the writer, Criterion 8 was not exercised as designed; record it rather than re-running.

## Implementation Notes

[TO BE FILLED DURING EXECUTION]

### Phase 0 Completion
**Completed:** 2026-08-26 — All three mechanism checks passed; runner amendment recorded (direct claude -p stream-json for cold runs) before any brief was committed. Evidence: operator-notes.md § Mechanism notes, ~/goal-proof-logs/00-derisk*/.

### Phase 1 Completion
**Completed:** 2026-08-26 — C01 = 0a7008a0. sessions/, probes/, five record skeletons.

### Phase 2 Completion
**Completed:** 2026-08-26 — Two turns (budget four). C-GROUND = c3e47e11. Premise gap found by the session unprompted. Fence clean (tool-input check).

### Phase 3 Completion
**Completed:** 2026-08-26 — Five probes sequential in throwaway worktrees; C-PROBE-CLOSED = 1ea90295. Measured reach: 2 of 5 classes. Deviations: probe p2 attempt 04a discarded (harness timeout); fixture commit message neutralized from p3.

### Phase 4 Completion
**Completed:** 2026-08-26 — C-SEED = e626b901; C-INTERRUPTED = a6caab37. Attempt 08a discarded (template-placeholder poll false-positive; polls date-anchored after). Kill landed start(74)<mint(77)<kill; seed did not propagate (B4 false, recorded).

### Phase 5 Completion
**Completed:** 2026-08-26 — Resumer 4464c354: Stop(interruption)+completed scoped remaining half+COMPLETE return; row hash identical; zero add-item.

### Phase 6 Completion
**Completed:** 2026-08-26 — Continuation 2e257062: T-002 spec'd WI-032 via PM, OWNER_GATE. Operator ruling (run 11, resumed session): round closed trigger 4, result 57129cb9.

### Phase 7 Completion
**Completed:** 2026-08-26 — Review 328d437b: FINDINGS; learnings settled+appended same commit; organic drift caught (finding 1); seed had been neutralized at writer.

### Phase 8 Completion
**Completed:** 2026-08-26 — Reader 0c03d923: four answers correct from the goal directory alone.

### Phase 9 Completion
**Completed:** 2026-08-26 — Disclosure amendment d36009e8; freshness record closed (13 kept/2 discarded/12 sessions); operator-notes.md written.

### Phase 10 Completion
**Completed:** 2026-08-26 — verification_record.md drafted; three ancestry checks pasted OK; eight invariants checked; hardening verdict: nothing promoted. Next: /_my_audit as a fresh session.

---

**Status**: Draft → In Progress → Complete
