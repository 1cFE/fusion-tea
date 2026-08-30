# Brief — implement stage — GSTH Item 6, Phase 1 resume (1c + 1d)

You are a **resumer round agent** for goal `p-pump-fence`, round 1. The prior round-agent
session was interrupted by a wall-clock timeout after `### T-002 start` (an invocation with no
return — `GOAL_RUNBOOK.md` § interruption). Per the runbook: inspect native artifacts as truth,
then append the missing task result. Do not redo completed work.

## State on disk (verified by the orchestrator; re-verify, don't re-derive)

- Goal grounded, round 1 open, T-001 returned PREREQUISITE (gate-2 designed refusal),
  T-002 scoped/started: `work/orchestration/goals/p-pump-fence/trail.md`, committed `67c4ff45`.
- T-002's regeneration/recapture/re-pin/fixture re-derivation is DONE and COMMITTED at
  `8099217b` (the orchestrator's commit — the seam's clean gate required it).
- Two seam runs kept as evidence: `evidence/integration-run-1/` (gate 2,
  package-not-integrated, stale package) and `evidence/integration-run-2/` (preflight clean
  gate — the tree was regenerated but uncommitted). Run 2's refusal is now discharged by
  commit `8099217b`.

## Your work — plan Phase 1c and 1d only

Instruction source: `.project/active/goal-integration-study-proof/plan.md` § Phase 1 (read it
and the spec first; § Decisions D1–D3 bind you).

1. **1c** — invoke the seam per the plan's stencil / `docs/integration_seam_operator_guide.md`,
   fresh `--out-dir /tmp/integration-run-3`, expected fingerprints = the NEW contract values
   (read them from `exploration/stellarator_e2e/generated/contracts/`). Expect exit 0,
   `class: "CANDIDATE"`. Copy the out-dir to
   `work/orchestration/goals/p-pump-fence/evidence/integration-run-3/`.
2. **1d** — canonical battery for the suite:
   `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest tests/study -q`
   Expect green (the 2026-08-28 pre_pr's 21 designed reds included). Capture the tail. Run
   pytest so YOU see the real exit code (no `| tail` pipe masking it).
3. Also run the plan's Phase-1 validation items: `uv run agentic-mbse validate models/`
   (L1 clean; L2 = the 12 known WARNs unchanged) and the two manual checks (no
   `exploration/stellarator_e2e/studies/2026*` diffs vs `8099217b^`; candidate pin equals the
   manifest's own value).
4. **Trail** — append `### T-002 return` (outcome, evidence incl. all three seam runs read as
   one arc, reading, decision with five fields). An interruption note belongs in the return:
   the task was interrupted between start and return and resumed by a fresh session from
   native facts — cite this brief and the two commits. Do NOT rewrite prior entries.
5. **Plan bookkeeping** — tick the remaining Phase 1 checkboxes that are now true; fill
   `### Phase 0 Completion` and `### Phase 1 Completion` notes (deviations: the timeout
   interruption; the run-2 clean-gate refusal, which the plan's 1a/1c did not predict as a
   separate run; the orchestrator performing the 1b commit mid-task).

## Hard rules (unchanged)

- **No git commits/pushes**; working-tree writes only; list every file you touched at the end.
- Stop and report rather than improvise if: 1c returns anything but CANDIDATE; the battery is
  not green and the cause isn't immediately diagnosable as environmental; any reserved gate.
- `uv run` everything. Cite-don't-mirror in the trail. Do not start Phase 2.

End with: T-002 return class, pin + both fingerprints, battery tail line, validation results,
grouped file list.
