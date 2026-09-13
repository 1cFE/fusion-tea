# Goal: fusion-audit-remediation

Grounded 2026-09-10. [OWNER-VERBATIM] "yes ground and proceed" approves the proposed slug and grounding contract. Agent proposals remain [AGENT] (ratified by owner, 2026-09-10).

[OWNER-VERBATIM] "I have this audit report of modeling issues: .project/reports/20260907-fusion-model-audit.md" and "I'd like you to $run-goal to address these." The audit findings remain agent judgments. All proposed decisions below are [AGENT] unless marked otherwise; owner ratification does not change their origin.

## Status

`grounded` — 2026-09-10 on the owner ruling above. Grounding evidence, answer contract, invariants, limits, and reserved gates are populated.

## Question

Can the current IFE and MFE models resolve all 20 audit findings with independently checked corrections, while making every remaining source, engineering, and comparison limitation explicit and enforceable within each model's supported use?

## Consumer

[OWNER] The project owner requested remediation through `run-goal`.

[AGENT] The answer should support decisions about which model predictions can be trusted, which comparisons are meaningful, and what further evidence is needed.

## Answered when

- Every finding F01–F20, including distinct subissues, has a current-revision assessment and evidence-linked final disposition. Later work receives credit only for what it demonstrably resolves.
- Reproducible source, dependency, arithmetic, domain, citation, and documentation defects within the supported scope are corrected through audited native work items. Verification covers original counterexamples and independent source checks or identities, with changed baselines explained.
- Accounting, reuse, and comparison findings have implemented contracts appropriate to the supported scope. Choosing a monetary/finance basis or narrowing supported scope requires an owner ruling. Naming a follow-up item alone does not resolve a defect.
- Any finding that cannot be fully resolved from available evidence has a concrete research result or limitation, an explicit effect on permitted model use, and an owner-accepted residual disposition. Missing evidence does not become an invented physical relation; an open research request alone does not count as resolution.
- Fresh review verifies the final assessment against native artifacts and relevant execution evidence. Syntax, translation parity, independent numerical/source validation, and engineering coverage are reported separately. Existing failures and skips are distinguished from new regressions.

## Invariants

- [INHERITED: modeling_project/REQUIREMENTS.md] Preserve quantitative traceability, library/design separation, and the cost/interface obligations in MR-1 through MR-6.
- Source corrections may change outputs. Historical reproductions and normalized comparisons remain distinguishable; each change must be attributable. A lower LCOE is not itself success.
- Source images govern transcription corrections. Preserve the original audit as historical evidence and retain its F identifiers in subsequent assessments.
- At most one promoted pin and one committed study per round. Preserve each comparison's declared physical, financial, and accounting interpretation. Changed comparison meaning closes the round.
- The existing `plant-closure` round has T-007 complete and no T-008 start or round result. Preserve its pin and historical evidence. Before changing shared MFE artifacts, assess the effect on that pending round and obtain the owner ruling below. Initial IFE work can proceed independently of that decision.
- [INHERITED: CLAUDE.md] Preserve source quarantine, coding/modeling ownership, native PM operations, and research/integration procedures. Use the documented `.codex-test/run` runtime launcher.

## Grounding evidence

- [INHERITED] `.project/reports/20260907-fusion-model-audit.md@e341dc3449b968125d11dc6162e3112bb9c5c169` and its adjacent evidence directory at that revision: 20 findings and retained counterexamples. The audited model was `b244abd8baf463dbad447935f86d0da5278ee751`, earlier than the current worktree.
- [INHERITED] `models/designs/generic_mfe/mfe_plant.sysml@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909`: source heat and power balance still read installed heating; primary loop and cycle are now calculations; the lifecycle calendar supplies availability and replacement cost. These are current code observations, not fresh numerical certification.
- [INHERITED] `models/designs/stellarator_09/stellarator_plant.sysml@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909`: the independent magnet-radius literal remains, supporting continued investigation of F06.
- [INHERITED] `work/orchestration/goals/plant-closure/goal.md@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909` and `work/orchestration/goals/plant-closure/trail.md@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909`: scope and T-001–T-007 outcomes. WI-045/046/047 carry later evidence relevant to F12/F13/F15; assess their records before claiming any finding closed.
- [INHERITED] `modeling_project/REQUIREMENTS.md@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909` and `modeling_project/OVERVIEW.md@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909`: modeling and comparison obligations.
- [INHERITED] `.project/codex-test-setup.md` — unpinned; no native digest. Runtime instructions and setup checks. The current conversation exposes all 30 project skills and five expert roles; no expert spawn or model baseline was executed during this grounding preparation.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds, then owner re-grounding or close |
| Time or iteration limit | No additional time cap; round boundaries and reserved gates apply |

## Reserved gates

- [OWNER-VERBATIM 2026-09-10] "yes ground and proceed" resolves the slug and grounding gate for this contract.
- Owner decides monetary/finance comparison changes, supported concept/module scope changes, project requirement changes, and acceptance of residual findings. Routine evidence-supported corrections proceed through native workflows.
- Owner decides how to preserve, finish, or supersede the pending `plant-closure` comparison before shared MFE changes invalidate its current-artifact assumptions. Reading and citing its evidence may proceed.
- [INHERITED: work/orchestration/GOAL_RUNBOOK.md] Merge, push, work-item close/archive, and goal close remain owner-held. Source/research approval follows its native workflow.
- [INHERITED: .agentic-mbse/codex.md] Native stages may use installed experts and fresh non-author agents with self-contained briefs. Goal checkpoint and round reviews must meet the runbook's fresh-session boundary. If the host cannot provide a qualifying session, write the required handoff and stop at that gate.

## Close rule

The owner closes after fresh review supports every Answered when condition, or redirects at a round boundary. A limit or unresolved gate stops work without certifying completion.

## Amendments

None.
