# Operator notes — the orchestrator's own side of the exchange

**Status:** headings only, opened 2026-08-27 at Phase 0. Written at Phase 12 from the kept transcripts.

Every judgment call here is graded `[AGENT]` and **never** written as a contract repair. Where a session got something wrong, the correction was another turn of that session, not the operator's pen.

## The D5 ruling as an operator judgment

What it overrode, why it was delivered after the checkpoint rather than before, and that it was `[AGENT]`-graded in the brief itself so the round agent knew it was reading an operator judgment rather than a contract.

## The Invariant-3 narrowing, implemented as omission rather than denial

## The stated limit of this evidence

A headless run cannot pause mid-run to ask and receive an answer, so every owner round-trip costs one run. A limit of the mechanism, not a finding about the runbook.

## Mechanism notes

### The Item 4 log-teeing mechanism became unavailable mid-run (2026-08-28)

`[AGENT]` — operator judgment, execution-detail tier. **Authorized by the orchestrator; not a contract repair and not a design change.**

The design and the plan's [RUN] block both require every cold session to be teed to `~/goal-proof-logs-item5/NN-<role>/`, outside the repository — Item 4's measured mechanism (`.project/completed/20260827_goal-cold-pickup-proof/operator-notes.md:48-58`). Session 01 ran exactly that way on 2026-08-27.

On resuming after gate (a), the session sandbox had tightened and every write outside `/home/reid/1cfe/fusion-tea` was refused. Both probes, quoted:

> `mkdir` in '/home/reid/goal-proof-logs-item5/02-grounding' was blocked. For security, Claude Code may only create directories in the allowed working directories for this session: '/home/reid/1cfe/fusion-tea'

> `touch` in '/home/reid/goal-proof-logs-item5/02-grounding-transcript.jsonl' was blocked. For security, Claude Code may only create or modify files in the allowed working directories for this session: '/home/reid/1cfe/fusion-tea'

The second probe used a flat file under the already-existing log root, so it was not the directory creation that was refused — it was any write outside the repository.

**The decision.** Tee each cold run directly to `sessions/NN-<role>/transcript.jsonl`, which is where [RUN] step 4 copies the file anyway. The operator did not take this adaptation unilaterally: it was surfaced as a `BLOCKED` return and the orchestrator ruled it, execution-detail tier, on the ground that the sandbox change was outside both parties' control this run.

**What is given up, stated precisely.** Only the copy outside the tree. Kill-recoverability is **not** lost — `tee` and shell redirection both write incrementally, so a killed run still leaves its partial transcript at the in-repo path. (The operator's first framing of this was wrong and said kill-recoverability was lost; the orchestrator corrected it, and the correction is recorded rather than the original.)

**What is unchanged.** Invariant 1's brief-ancestry check and Invariant 2's fence sweep both read the same files they always would. Cold sessions still may not read the item directory, the denial is still in every brief, and the sweep still targets tool-call *inputs*. A transcript being written into the item directory during a run is not a session read of it.

**Status: authorized; exercised from session 02 onward (see Post-run notes below).** At the time of this entry no cold run had used it — the `claude` binary was blocked before session 02 could start (see the run's blocked return). The first run to use it should confirm the transcript lands complete and well-formed.

## Post-run notes — 2026-08-28 (Phase 12)

All graded `[AGENT]`; none is a contract repair.

- **The operator role split mid-run.** The implement-stage subagent ran Phases 0–1, then its sandbox degraded in three steps (git writes → home-directory writes → invoking `claude` at all), each refusal quoted in § Mechanism notes. The orchestrator session absorbed the operator role from Phase 2 on: it ran every cold session, made every commit, and resumed nothing of the subagent. Same operator discipline, different pair of hands; the briefs, transcripts, and commit ordering are unchanged in kind.
- **D5 was never delivered.** The stale-runbook-row override was designed for the T-002 resume brief. T-001 returned `COMPLETE`, the seam never ran, and the ruling was never issued. The stale row (`GOAL_RUNBOOK.md:256,264`) remains stale on `main` and in this branch — the flip (R-G) has no seam run to rest on and correctly did not land. The hazard the round actually met was goal.md:130 carrying the same stale instruction; it never bit because no task needed the seam.
- **What the runbook prompted for unprompted:** session 01 verified citation liveness, ran an order-of-magnitude check, and found the DI-008 band discrepancy — none of it asked for by the brief. Session 07 read three new ARIES-ACT lines at round close and found the divertor-relative misread. The contract's "walk whatever the evidence leads you to" wording is doing real work.
- **Stalls:** none. Eight runs, zero retries, zero aborted sessions. The only round-trips above the design's floor were the r2 checkpoint cycle (designed for) and the three unblock turns the sandbox degradation cost the subagent.
- **Judgment calls by the orchestrator-as-operator:** committing on the subagent's behalf at its exact two-commit specification; authorizing the in-repo tee (recorded above, with the kill-recoverability correction); running Phases 8+9 as one resume (the commit sequence puts their outputs in one row, so one session turn is the same shape); freshness row 02 recorded one phase late (a prose failure, in § Failures).
- **The headless limit stands as Item 4 stated it:** a cold run cannot pause mid-run to ask; every owner round-trip costs one run. Limit of the mechanism, not a finding about the runbook.
