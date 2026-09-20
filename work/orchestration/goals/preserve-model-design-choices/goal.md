# Goal: Preserve model design choices

## Status

`grounded` — [OWNER] Execution of the deposited prompt authorizes grounding with this slug, 2026-09-20.

## Question

Can the stellarator model and shared dependencies evaluate and cost supplied designs without silently selecting different hardware, while preserving supported physical relationships and validity limits?

## Consumer

[OWNER] The project owner needs an MR-7-compliant evaluation model and independently checked evidence of its supported design choices.

## Answered when

[OWNER] The scoped whole-model inventory is complete; every confirmed violation is repaired through native model, generated interfaces and consumers; applicable behavioral/regression/integration checks pass; independent review supports compliance. Unverified or deferred violations remain open, with concrete blockers. See evidence/owner-prompt.md for the full acceptance contract.

## Invariants

- [INHERITED: modeling_project/REQUIREMENTS.md] MR-1 through MR-7 apply. MR-7 separates physical relationships, chosen hardware, requirements and selection policy. Preserve intended choices of winding geometry/inventory, facility allocation, processing capacity and supported cooling equipment; investigate directional operating closures and demand-matched proxies without inventing performance data.
- [OWNER] Preserve conductor validity limits, physical relationships, historical packages/studies and reference evidence. No reference-derived tuning, reference-paper/request/observation reads, new comparison or replacement freeze. This is post-reveal repair from pre-reveal code.
- [OWNER] Work on fix/modeling-intent-after-reveal; preserve unrelated staged/unstaged work and enforcement commits. Only explicit-file local commits are authorized; no push/merge.
- [AGENT] Each round promotes at most one package and commits at most one study. Numerical improvement and whole-plant feasibility are not success criteria.

## Grounding evidence

- modeling_project/REQUIREMENTS.md@0223c73785713400633b857183e6a7f5f103aa95 — MR-7 authority and evidence.
- modeling_project/MODELING_PROCESS.md@0223c73785713400633b857183e6a7f5f103aa95 — native stages and independent review.
- .project/active/modeling-intent-enforcement/spec.md@0223c73785713400633b857183e6a7f5f103aa95 — owner intent and enforcement.
- .project/active/demo-depth-rubric/application-policy.md@0223c73785713400633b857183e6a7f5f103aa95 — depth versus design-choice compliance.
- .project/active/aries-comparison-preparation/current-readiness/revealed-results/post-reveal-repair-results-note.md@0223c73785713400633b857183e6a7f5f103aa95 — disclosed repair basis.
- work/analysis/20260920-184131_design-choice-assignment-audit.md — unpinned; no native digest; initial nonexhaustive audit.
- evidence/owner-prompt.md — unpinned; no native digest; exact executed owner instruction.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | None |
| Tasks per round | None |

## Reserved gates

[OWNER] Genuinely unresolved intended variable freedoms, new physical approximations and unsupported source interpretation require the owner before dependent work. Formal goal closure, archival, merge/push and any future comparison remain owner-held. Routine implementation and verified fixes are authorized.

## Close rule

[OWNER] Only the owner formally closes the goal after reviewing technical completion evidence or a bounded negative result.

## Amendments

None.
