# Feedback — design revision — from design-review.md (verdict Revise)

Fix all four Critical and seven Major findings (Minors too where cheap). Orchestrator
dispositions where a call was needed:

1. **C1 (freshness hole)** — as the reviewer says: every cold run gets `--log-dir` at a path
   outside the repository tree; immediately after each run the orchestrator copies the
   transcript into `sessions/NN-<role>/` and commits it before the next dependent run.
   Reframe session read-rules as an allowlist (what the session MAY read), and the
   freshness/transcript check must cover reads of any log path. The pre-existing repo-root
   `.orchestrate-logs/` is treated as forbidden territory for all cold sessions.
2. **C2 (Criterion 3)** — add the standalone-reader run as its own enumerated cold session.
   Closure of the freshness record means *complete enumeration with a closing statement*,
   not a fixed count; update the run table and count everywhere.
3. **C3 (mint vs `GOAL_RUNBOOK.md:234`)** — surface, then proceed under a recorded reading.
   The design states the contradiction (`:234` "exactly one write outside its own directory"
   vs `:244` minting through the owning PM) as measured Item 1 evidence for the run summary
   and the proof report. It then adopts, loudly and as `[AGENT]`: `:234` binds the goal
   layer's own pen (goal dir + discovery log); a task invoking the owning PM's own operation
   (`agentic-mbse pm add-item`) is native work by the native workflow, which is the layer's
   stated purpose (runbook § What this is). Challenge path recorded. Contingency: if the
   cold round agent reads `:234` restrictively and refuses to mint, that refusal is itself
   recorded prose-ambiguity evidence, and the operator resolves it in-session (a kept,
   transcripted operator clarification), after which the task proceeds. No silent
   resolution in either direction. Bet B3 (PM state vs the goal's reserved gate) stays
   flagged as before — it is a distinct question and the reviewer confirmed it passes on
   plain wording.
4. **C4 (resumer authorization)** — restructure: the resumer does exactly what
   § Resuming an interruption authorizes — inspect native facts, append the correct
   return or `### Stop`, no more. Either outcome satisfies Criterion 4; which one it picks
   is measured evidence. A separate fresh **round-continuation session** then picks up from
   the trail, runs T-002 to the unresolved-owner-gate close, and writes the round result
   (drift already planted in the Round 1 strategy revision, so it survives). The ADR-002
   one-agent-per-round tension this creates is recorded as measured evidence of the
   contract under interruption, not patched. Update criteria mapping and the run table.
5. **Majors** — M-1: kill must terminate the child process group and the transcript must be
   copied from the external log dir regardless of kill timing; state the mechanics. M-2:
   the poll gates the kill on both the `### T-00N start` line and the native artifact being
   observable; define the abort-and-rerun rule if the session batches start+effect+return
   into one observation window (an aborted attempt is enumerated in the freshness record
   with its transcript — nothing is hidden). M-3: probes pass `--log-dir` outside, their
   transcripts are copied before teardown, variant drafts live only in the worktree and the
   probe briefs/outputs are committed in the item directory — nothing probe-related commits
   on the branch except briefs and kept outputs. M-4: state the expected refusal shape per
   field class given the template's `Status:` coupling (`GOAL_RUNBOOK.md:72`), so the one
   predicted-pass class is separated from the four predicted-failure classes. M-5: reword
   D6 so the run measures the silence and the operator's response is recorded as operator
   judgment, not as a contract repair. M-6: the grounding exchange may span several
   resumes of the same session (one session, several turns, all kept); the operator-notes
   artifact is written by the orchestrator after the exchange, from the transcript, and is
   graded `[AGENT]`. M-7: fix the closure statement wording so it cannot contradict itself.
6. The reviewer verified: resume-by-id naming is real; `add_item` re-serializes the whole
   `work/BACKLOG.md` file — so say explicitly that the non-repetition check for the mint is
   row-scoped (the WI row exists once), not a whole-file diff.

Update `design.md` in place; keep the criteria→run→evidence mapping consistent after the
restructure. End with `ARTIFACT: <path>`.
