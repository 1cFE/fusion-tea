# Brief — design_review stage — GSTH Item 4 (goal-cold-pickup-proof)

Review `.project/active/goal-cold-pickup-proof/design.md` against
`.project/active/goal-cold-pickup-proof/spec.md` (the contract; approved after
`spec-review.md`). You are a fresh reviewer; the authoring session is not yours. Epic:
`.project/backlog/epic_goal_strategy_task_harness.md` § Item 4. Align: `align.md`.

## Resolved since the design was written (take as fact)

The design flagged one unverified mechanism fact: whether `orchestrate-stage.sh` accepts a
worktree working directory. Orchestrator verified: the script has no cwd flag and runs
`claude -p` in the caller's working directory, so invoking it from a worktree works; its
`--log-dir` defaults to `./.orchestrate-logs` relative to that cwd, so worktree runs must
pass `--log-dir` (or copy logs out) for the kept-transcript evidence. Judge whether the
design's fallback and evidence flow survive this mechanic.

## What to check hardest

1. **Criterion coverage**: walk each of the spec's nine success criteria and check the
   design's run sequence actually produces the disk evidence and git-ancestry orderings each
   one demands. Look for a criterion whose evidence no run produces.
2. **The interruption's realism (Criterion 4)**: the design kills a real process on a poll.
   Check the choreography guarantees, at kill time: write-ahead `### T-00N start` on disk,
   the completed native artifact on disk, no return, and that the kill cannot instead land in
   a state the spec calls clean-boundary (or destroy the write-ahead). Also check the
   resumer's non-repetition evidence is genuinely checkable (hash/no-second-invocation).
3. **Bet B3**: the reserved gate reads "any model or knowledge mutation beyond the goal
   directory needs owner sign-off"; the design reads `agentic-mbse pm add-item` (PM state,
   `work/BACKLOG.md`) as neither. Judge that reading and whether the design keeps it
   honest — flagged, not assumed.
4. **Five per-class grounding probes**: does the probe design isolate each field class (a
   draft missing exactly one class per probe?), and is the throwaway-worktree mechanism
   sound given the cwd mechanic above? Does probe evidence survive worktree teardown?
5. **Freshness**: ten runs / nine sessions with transcript-verified reads — check nothing in
   the flow lets a later session see an earlier session's output outside its committed brief,
   and that the enumeration genuinely closes.
6. **Contract fidelity**: the design must not extend or repair Item 1's shipped contract;
   silences (e.g., resumer-inherits-round) are recorded as measured evidence, not patched.
7. **Drift plausibility**: the frame-widening drift must be one a real round could commit,
   detectable from goal.md + trail alone by a reviewer who was not told.

Findings with severities; must-fix goes back to the authoring session. Deliverable:
`.project/active/goal-cold-pickup-proof/design-review.md`. End with `ARTIFACT: <path>`.
