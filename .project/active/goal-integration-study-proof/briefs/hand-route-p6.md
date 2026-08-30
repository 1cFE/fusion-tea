# Brief — hand operator — route equivalence (GSTH Item 6, Phase 6)

You are the HAND OPERATOR: a fresh session playing a human who follows
`work/orchestration/GOAL_RUNBOOK.md` literally, step by step. You have no memory of the
agent route. You operate ENTIRELY in the isolated worktree:

    /home/reid/1cfe/fusion-tea-route-equiv        (detached at the round's closing commit)

`cd` there first; verify with `pwd` and `git rev-parse HEAD`. **Never write to
`/home/reid/1cfe/fusion-tea`** — reading main-tree paths is permitted only for the two
gitignored env files named below. No git commits anywhere, worktree included.

## The exercise — the same contract goal `p-pump-fence` round 1 ran, isolated

1. **Grounding walk** (§ Grounding a goal): perform the five-class check on
   `work/orchestration/goals/p-pump-fence/goal.md` by hand as the runbook instructs.
   Record whether a hand operator reaches the same `grounded` verdict and where the
   instructions were ambiguous.
2. **`integrate` — invoke for real** per `docs/integration_seam_operator_guide.md`,
   `--out-dir` inside the worktree (outside the package tree). ADR-009 makes a re-run
   return the same identity: expect the agent route's pin `20c2c364d6c7…` and fingerprints
   `f08daa7b…` / `f97f0848…`. Any difference is a finding, not a nuisance.
3. **`study.execute` — fixture-substituted (the declared limit).** Do not run points. Walk
   runbook steps 1–6 obligations by hand against the committed record
   `exploration/stellarator_e2e/studies/20260829-p-pump-fence/`: re-derive what you would
   declare (axes, groups), compare to its `axes.json`; read its `indicators.json` as the
   step-3 deposit; confirm the recorded protocol rulings answer step 4; check the step-6
   preflight deposit. The committed record stands in for execution. State this limit
   plainly in your report.
4. **`study.read` — run for real, by hand**: administer the committed record per the
   runbook's administer contract, record-directory-only, writing YOUR OWN
   `synthesis-hand.md` into the worktree's copy of the record directory. Compare your
   reading class and headline numbers to the committed `synthesis.md` only AFTER writing
   yours.
5. **Checkpoint and review walk (read-only)**: as a hand reader of
   `work/orchestration/goals/p-pump-fence/trail.md`, verify the checkpoint entries and the
   round review meet the runbook's stated contract (fresh sessions, caps, append-only).

## Environment

`uv run` everything, from the worktree root. The two env files are gitignored and absent in
the worktree — reference them read-only from the main tree:
`--env-file /home/reid/1cfe/fusion-tea/.venv/integration.env` and
`/home/reid/1cfe/agentic-mbse/.env` (plus `set -a; source …; set +a` where a test needs it).
Sealed wheels live outside both trees and resolve normally.

## Report (your final message)

For each of the five comparison dimensions — required artifact set, native end states,
gates, return classes, reviewer-visible evidence — what the hand route produced/observed vs
the agent route's kept evidence, and whether the SAME CONTRACT was met (textual identity
not required). Every divergence with its reason. Every place the runbook needed an
operator-kind carve-out (that is a finding). The declared limit stated. Full list of files
you wrote (all must be inside the worktree).
ARTIFACT: (your final message)
