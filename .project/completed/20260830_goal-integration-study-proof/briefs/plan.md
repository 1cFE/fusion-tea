# Brief — plan stage — GSTH Item 6 (goal-integration-study-proof)

You are the plan stage for a lean-shape orchestrated run of GSTH Item 6. Author
`.project/active/goal-integration-study-proof/plan.md` — phased, checkboxed, per /_my_plan
conventions. Do NOT git commit; the orchestrator applies commits. Do not edit any other file.

## Read first (in this order)

1. `.project/active/goal-integration-study-proof/spec.md` — Align rulings, incl. reserved gates and the lean-shape ruling (no design.md; YOUR plan carries the route-equivalence isolation design).
2. `.project/backlog/epic_goal_strategy_task_harness.md` § Item 6 (~line 439) — Scope 1–5, Success Criteria 1–7, Out of Scope. This is the governing spec.
3. `.project/concepts/goal-strategy-task-harness-design.md` § Native seams, Round Semantics, Findings and Learning, Review Pattern, Validation and Handoff.
4. `work/orchestration/GOAL_RUNBOOK.md` — the loop the round follows; note the `integrate` rows (~:258, :262, :265) still say "pending native repair" — flipping them (mirroring C-FLIP `9f0019e8` for research, `git show` it for the recipe) is part of this item, AFTER the seam runs live.
5. `work/completed/20260828_WI-033_p-pump-rebase/verification_record.md` and `.project/pre_pr/2026-08-28-pre-pr-wi033-p-pump-rebase.md` — the audited input and the 21 designed battery reds this item is expected to turn green.
6. The integrate seam: `scripts/integrate.py`, its ADR (ADR-009, `.project/adr/`), and its tests `tests/study/test_integrate_*` — learn invocation, gates, return classes (CANDIDATE pin/fingerprint vs named BLOCKER).
7. `.claude/skills/run-study/SKILL.md`, `.claude/skills/run-study/runbook.md`, `modeling_project/STUDY_POLICY.md` — study execute/administer contract.
8. `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` rows for `20260821-power-cycle-ab#3` (:9, :33, :35) — the open tail the new goal answers: "where the `recirc_ok` fence moves and what LCOE does".
9. `work/orchestration/goals/p-pump-basis/` goal.md + trail.md § "Constraints carried into round 2" — the closed predecessor; its constraints inform the new round.

## Provenance you must respect (owner-grade, do not re-decide)

- New successor goal, owner's wording for § Question / § Answered when — RESERVED GATE; plan must sequence grounding before the round opens and mark the gate.
- One PR ships WI-033 + Item 6 from `feat/wi033-p-pump-rebase`; push/PR/merge owner-held.
- Adverse/inconclusive reading closes the round, no self-repair; any ruling it requests is owner-held.
- Out of scope: second pin, second committed study, concurrency, optimizer policy, unattended dispatch, reopening `p-pump-basis`, any research registration, auto-close/archive of native work, push/PR.

## Phase sketch — `[AGENT]` orchestrator suggestion; refine where the artifacts say otherwise

- P0 Ground the successor goal (owner wording arrives via orchestrator), open round 1, StrategyRevision, task T-001 scope written before work.
- P1 Integrate: invoke the seam on the audited WI-033 work → exactly one CANDIDATE pin+fingerprint or named blocker; commit the regenerated package; verify the 21 battery reds go green here.
- P2 Study execute: one bounded study against the exact pin contract; commit its record.
- P3 Administer: FRESH session reads the committed record only → synthesis + findings.
- P4 Close: joined dispositions for every touched/new discovery row; learning delta; fresh RoundReview (fresh session); round closes on the reading whatever it says.
- P5 Runbook `integrate` row flip (post-live-proof), research row byte-untouched.
- P6 Route equivalence: hand-operated session follows GOAL_RUNBOOK step-by-step vs the goal-agent route's kept evidence; YOUR isolation design goes here — compare artifact set, native end states, gates, return classes, reviewer-visible evidence, with no duplicate external effects and no second committed study/pin (fixtures or isolated targets — e.g. scratch worktree/dir; decide and specify). Output `route_equivalence.md`.
- P7 Epic evidence: `epic_evidence.md` mapping every epic success criterion to evidence, incl. the honest limit (spec criterion 8: `research_seam.py` bookkeeper never ran end-to-end); full regressions (canonical battery both env files, `tests/models` with `set -a; source ~/1cfe/agentic-mbse/.env; set +a`, `tests/research`).
- P8 Verification record for the item; audit prep.

## Constraints and gotchas

- `uv run` for everything Python; never bare python/pip. Validation via `uv run agentic-mbse validate models/` (never bare `syside check`).
- The regeneration fence from WI-033 is now INVERTED: Item 6 IS the authorized regeneration; committed prior studies stay reproducible at their pins — do not touch their pinned dirs.
- Goal artifacts cite native state, never restate it (cite-don't-mirror; two-PM rule).
- Each phase needs a validation step and a commit point marked for the orchestrator.
- Keep plan.md concise — a tired engineer reads it once mid-task.

End your final message with `ARTIFACT: .project/active/goal-integration-study-proof/plan.md`.
