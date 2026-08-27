# Operator notes — how the exchange worked from the operator's chair

Written by the orchestrator-as-operator after the runs, from the kept transcripts and the
per-turn scratch notes. Owner-requested at Align (`align.md`); everything here is `[AGENT]`.

## What the runbook prompted for on its own

More than the grounding gate enforces. The written gate defends one field class (empty
grounding evidence → draft → no task), but the *co-development direction* of § Grounding a
goal surfaced all five: turn 1's session came back with six numbered questions covering the
premise, consumer, answer contract, limits, reserved gates, and close rule — unprompted, and
before any operator answer existed. The procedure asks for the fields even where the gate
would not refuse their absence. The gate probes measured the refusal side separately
(`gate-probe-record.md`): two classes refuse, three sail through.

## What the operator had to supply unprompted

- The question itself, and the discovery-row pointer — by design.
- Rulings, not facts: which of three derivation routes the goal may take (answer: choosing
  is the goal's own work), consumer confirmation, close rule, gate confirmations. The
  session found every repository fact itself, including the premise gap the operator's own
  question rested on (the 27–41 % arithmetic gap) — the operator supplied judgment only.
- The continue-vs-close ruling at the T-001 handoff, and the gate-2 ruling that closed the
  round. Both are decisions the runbook explicitly routes to the operator; both were
  delivered as committed, transcripted resume turns.

## Where the exchange stalled, and why

It did not stall. Two turns of a budgeted four: turn 1 wrote everything groundable and
queued precise questions; turn 2 finished on the answers and set `grounded`. The headless
bound (a session cannot pause mid-turn to ask) cost nothing here, because the runbook's
grounding shape — write what you can, surface what you cannot — matches the turn boundary.

## Operator judgment calls (each `[AGENT]`, never a contract repair)

1. Gate-2 ruling: not granted in-round (owner absent; operator does not hold the owner's
   authority). Closed the round on trigger 4. The gate goes to the owner in the run summary.
2. Continue-vs-close at the handoff: continue, per the design's shape for this proof.
   The continuation session correctly noted the runbook itself does not say who decides.
3. The `:234`/`:244` contingency never fired — the round agent read minting through the
   owning PM as native work without prompting, matching the recorded `[AGENT]` reading.
4. Probe fixture commit message: "probe fixture pN" was a construction tell (p1 read it in
   history); switched to a neutral message for p3–p5 mid-run, recorded in the record's tell
   column. p2 kept the telling message — its script copy was already executing.

## Mechanism notes (Phase 0 de-risk results and the runner amendment)

- The three de-risk checks all passed: a `stream-json` transcript survives a mid-run
  process-group kill (39 events kept); `kill -TERM -<pgid>` leaves no survivors (claude +
  two MCP children); a worktree invocation runs in the worktree and writes no
  `.orchestrate-logs/` into either tree. Raw outputs: `~/goal-proof-logs/00-derisk*/`,
  summarized in the freshness record's closing statement.
- Runner amendment, recorded before any brief was committed: `orchestrate-stage.sh run
  <stage>` composes `/_my_<stage>` plus an orchestrator preamble — the wrong frame for a
  cold non-builder, and its buffered `--output-format json` does not survive a kill. Every
  cold run therefore invoked `claude -p --output-format stream-json --verbose` directly,
  teed to `~/goal-proof-logs/NN-<role>/` outside the tree. The script remains right for
  genuine `/_my_*` stages (the audit).
- Two orchestrator harness errors, both enumerated as discarded attempts, neither hidden:
  04a (a batch script hit the Bash tool's own wall-clock cap mid-probe) and 08a (the kill
  poll matched the trail *template's* placeholder `### T-001 return — YYYY-MM-DD` and
  killed the round agent at ~2 s). The 08a lesson generalizes: any disk predicate against
  goal files must distinguish template scaffold from real entries — date-anchored greps.
  The plan's own Phase 4 check-first greps carried the same latent flaw.
- Fence checks must run against tool-call *inputs*, not raw transcript text: every brief
  embeds the denial list, so raw grep self-matches (first seen on run 01; rechecked clean).

## What a headless bound could and could not show

Shown: the whole loop — grounding, gate refusals, a real mid-task kill, resume from disk,
round close, fresh review, standalone read — ran headless with committed briefs as the only
inputs, and the transcripts carry every read. Not shown: a live human co-editing `goal.md`
in-session (the exchange was turn-based by construction), and any behavior under
interactive permission prompts (cold runs ran `acceptEdits`/`bypassPermissions`; a denied
tool call mid-round was never observed). Neither gap touches what this item proves.
