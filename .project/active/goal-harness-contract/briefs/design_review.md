# Brief: design_review stage — goal-harness-contract

**From**: orchestrator (Fable), `/_my_orchestrate`, 2026-08-25. Fresh session — you did not author the design.

**Review target**: `.project/active/goal-harness-contract/design.md`
**Contract it must satisfy**: `.project/active/goal-harness-contract/spec.md` (provenance grades are load-bearing). Also read `align.md`, `spec-review.md`, and the epic Item 1 section in `.project/backlog/epic_goal_strategy_task_harness.md`.

## Context

Item 1 of epic GSTH: file seven approved decisions in a new ADR home, define the goal.md/trail.md/learnings.md contract, amend five writer-ownership homes + CLAUDE.md:73, and ship GOAL_RUNBOOK.md + templates + consistency tests. Epic Items 4–6 will test this contract with fresh non-builders; Item 2 runs in parallel and files ADRs into the home this design creates.

## What to check hardest

1. **Spec coverage** — every [NEED]/[HARD]/[INHERITED] requirement has a design home; every spec Open Question is settled or explicitly surfaced. Flag silent omissions hardest of all.
2. **Hardening boundary** — no control-plane mechanism (envelopes, event ledger, digests-as-authority, idempotency, reconciliation, concurrency, dispatch) enters by the back door. Check `adr.sh` and the digest handling (`<path>@<commit-sha>`, invariant I6) specifically: the design claims both stay inside the boundary — verify the claims, don't take them.
3. **The six amendment edits** — verify each against the live files (runbook step 14 at :221, :270, :290-296 schema table, DISCOVERY_LOG.md:3 header, CLAUDE.md:73). Do the edits actually reconcile writer ownership AND one-row-per-finding cardinality? Do they truly leave room for Item 6's pending findings #6/#10/#11 (check `.project/active/run-study-first-consumer/plan.md:309,323`)?
4. **Test design** — does the joined-row coverage plan actually turn the set-comparison accident at `tests/study/test_records.py:41` into a stated guarantee without breaking existing records? Check the positional-column gotcha (`:60` reads Record by index).
5. **Operability at the owner's bar** — could a non-builder actually run the loop from GOAL_RUNBOOK.md + templates as designed? The referent bar is `work/orchestration/handshake-lcoe-construction.md`. Distinct timing/responsibility of the pre-execution checkpoint vs RoundReview must survive into the designed conventions.
6. **ADR-home choice** — is the rejection of extending `modeling_project/ARCHITECTURE.md` sound, and is the "lands first, one complete commit" sequencing real (Item 2 depends on it)?

Return must-fix findings vs. nits with the sources you checked. Do not edit the design yourself.
