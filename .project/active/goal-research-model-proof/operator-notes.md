# Operator notes — the orchestrator's own side of the exchange

**Status:** headings only, opened 2026-08-27 at Phase 0. Written at Phase 12 from the kept transcripts.

Every judgment call here is graded `[AGENT]` and **never** written as a contract repair. Where a session got something wrong, the correction was another turn of that session, not the operator's pen.

*Not yet populated.*

## What the runbook prompted for unprompted, and what the operator had to supply

## Where the exchange stalled, and what each stall cost in turns

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

**Status: authorized, not yet exercised.** No cold run has used it — the `claude` binary was blocked before session 02 could start (see the run's blocked return). The first run to use it should confirm the transcript lands complete and well-formed.
