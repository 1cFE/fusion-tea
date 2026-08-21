# Spec: Parallel Subprocess Dispatch + Archive + Status Stats (Concept-Analysis Rework, Item 11)

**Status:** Implementation Complete (Phase 1 parallel runner + Phase 2 bulk archive + Phase 3 status stats)
**Owner:** Reid W
**Created:** 2026-05-31
**Complexity:** LOW
**Branch:** `concept-analysis-rework`
**Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 11

---

## Work Item Summary

Item 11 in the epic is framed as "bulk regeneration." In practice the operator does **not** want a run-all-31 orchestrator — the infra already exists and the operator hand-picks small batches of concepts. This item delivers the one capability that's actually missing plus two small conveniences: (1) a **parallel subprocess runner** that fans out `analyze` (with `--max-passes`) and `model-critic` over an explicit, operator-supplied concept list; (2) an **archive step** that `git mv`s a concept's old pipeline artifacts into `archive/` before it's regenerated, retaining git history; (3) three **stats columns** (`P_native`, native LCOE, `result_1gw` LCOE) added to the existing `status` subcommand. The regeneration workflow stops after `model-critic` — a human checkpoint, not the full chain.

## Why This Matters Now

The per-concept primitives already exist and are correct: `analyze --max-passes N` runs `analyze → model-setup → assess` in-loop (model_setup is inside each iteration), and `model-critic <concept>` is the standalone Item 9 review. The only thing the operator can't do today is run those across a handful of concepts **in parallel** — `run_scoring_pipeline.py` already has the `ProcessPoolExecutor` pattern, but it's hardwired to the scoring stages. Generalizing it is a few lines. The archive habit and the status stats are quality-of-life: the operator wants old artifacts retained for reference (only concept 01 is on the new pipeline; the other 30 are old-pipeline and worth keeping) and wants to see plant size / native / 1 GWe LCOE at a glance while iterating.

## Key Bets / Constraints

- **Constraint — no new orchestrator, no run-all default.** The runner operates on an **explicit concept list** the operator passes. There is no "all concepts" mode and no full-chain (review/synthesize/score/approve) automation in this item.
- **Constraint — reuse, don't reinvent.** Parallel dispatch reuses `run_scoring_pipeline.py`'s `run_for_concept` / `run_parallel_stage` / `ProcessPoolExecutor` machinery. Stats reuse the existing `status` subcommand and the explorer's module-loading approach for LCOE values. `git mv` is plain git.
- **Constraint — stop after the critic.** A batch run is `analyze --max-passes N` then `model-critic`, then it stops for human review. No downstream stages.
- **Constraint — `regenerate-concept` is not used.** That subcommand (Item 6, commit `9cc9675`) runs the full chain through `approve`; it is the wrong tool for this checkpoint-driven phase and is left untouched.
- **Constraint — archive is `git mv` only.** Old artifacts are moved to `archive/`, history retained. No comparison/diff tooling is built (the operator uses git/manual diff).
- **Non-goal:** A bulk "regenerate everything" command, progress dashboards beyond the `status` columns, old→new LCOE delta tooling, and touching freeform concepts (`fit_grade=None` or no-`P_native`) — all out.

---

## Business Goals

### Why This Matters

The operator drives regeneration in small, hand-selected batches with a human checkpoint after the critic — deliberately, because running 31 concepts unattended "is not going to turn out well." The missing capability is purely throughput: running a chosen batch concurrently instead of one at a time. The archive and status conveniences keep the iteration loop legible without adding process.

### Success Criteria

- [ ] The operator can pass an explicit list of concept IDs and run `analyze --max-passes N` for all of them in parallel (`--workers N`), then `model-critic` for all of them in parallel, with per-concept pass/fail output.
- [ ] A concept's old pipeline artifacts are retained in `archive/` with git history intact before it's regenerated.
- [ ] `status` shows, per concept, the design reference plant size (`P_native`), native LCOE, and 1 GWe (`result_1gw`) LCOE alongside the existing iteration count.

### Priority

P0 within the epic's Phase 2, but small. Gated on Item 10 (explorer adapter + pilot) and the three-forward contract landing, since regenerated artifacts use the three-forward shape and the stats read `native` / `result_1gw`.

---

## Problem Statement

### Current State

- `run_scoring_pipeline.py` has a working `ProcessPoolExecutor` runner (`run_for_concept`, `run_parallel_stage`, `--workers`, default 3) that spawns `run_analysis.py <stage> <cid>` subprocesses — but its `STAGES` list is hardwired to `synthesize → extract-scores → calibrate → heatmap`. There is no parallel path for `analyze` or `model-critic`.
- `analyze` and `model-critic` accept multiple concept IDs but iterate **sequentially** (`for c in targets`).
- The `status` subcommand prints per-concept state + iteration count (`I{N}`) but no cost/size stats.
- Regenerating a concept overwrites/extends its directory in place; old-pipeline artifacts are lost on regeneration with no retained copy.

### Desired Outcome

A small parallel runner the operator points at a chosen concept list to fan out `analyze`/`model-critic` subprocesses; a documented `git mv` archive step run before regenerating; and three extra columns on `status`. Nothing more.

---

## Scope

### In Scope

- Parallel subprocess dispatch for `analyze` (passing `--max-passes`) and `model-critic` over an explicit concept list, reusing the `run_scoring_pipeline.py` pool machinery. (Whether this is a generalization of that script or a sibling is a design call.)
- An archive step — documented procedure and/or a thin helper — that `git mv`s a concept's old **pipeline-produced** artifacts to `archive/concept_analysis_pre_rework/{cid}/`, leaving inputs/hand-written content (`design-points/` trace, human-authored `review.md`) in place.
- Three columns on the existing `status` subcommand: `P_native`, native LCOE, `result_1gw` LCOE.

### Out of Scope

- Any "regenerate all concepts" orchestration or default.
- The full downstream chain (review / address-review / synthesize / score / approve) — this item stops after `model-critic`.
- `regenerate-concept` (full-chain) — untouched.
- Old→new comparison / diff / delta tooling.
- Freeform concepts (`fit_grade=None`; `fit_grade≠None` but no `P_native`) — not regenerated, not archived here.
- Item 12 (native-scale projection).

### Edge Cases & Considerations

- **Cross-concept reads under parallelism.** Stages that read the shared approved pool / landscape context could race when several concepts run at once. Since this item stops after the critic (no synthesize/approve), the analyze landscape read is the main exposure — design should note whether it matters at batch sizes the operator actually uses, and not over-engineer if it doesn't.
- **Per-stage flag differences.** `run_for_concept` currently hardcodes `--force` and a synthesize-only `--skip-review-gate`; `analyze` needs `--max-passes` (and `--force` semantics that cold-start cleanly), `model-critic` takes neither. Design handles the per-stage flag set.
- **Archive vs. regeneration ordering.** If a path is `git mv`'d away, a subsequent `analyze` cold-starts cleanly into the now-empty path — confirm this is the intended interaction and that `design-points/` (a regen input) is never moved.
- **Status LCOE source.** Native / 1 GWe LCOE come from the three-forward `native` / `result_1gw` forwards. Mechanism (load the module like the explorer vs. parse `model_output.txt`) is a design call; `model_output.txt` format changes under the three-forward contract, so design should pick the robust source.

---

## Requirement Selection Notes

The normative requirements below cover only what must be true for the three deliverables to work and to stay minimal. Mechanism choices (generalize the existing script vs. a sibling; module-load vs. text-parse for LCOE; helper vs. documented-procedure for the archive step) are deferred to design — the spec fixes *what*, not *how*.

---

## Requirements

### Functional Requirements

1. **FR-1**: The operator MUST be able to run `analyze` with a chosen `--max-passes` across an **explicit, operator-supplied list** of concept IDs as parallel subprocesses, with a configurable worker count (`--workers`, default consistent with the existing runner).
2. **FR-2**: The operator MUST be able to run `model-critic` across an explicit concept list as parallel subprocesses, same mechanism.
3. **FR-3**: Parallel dispatch MUST reuse the existing `run_scoring_pipeline.py` pool machinery (`run_for_concept` / `run_parallel_stage` / `ProcessPoolExecutor`) rather than introduce a second parallel framework, and MUST emit per-concept pass/fail output like the existing runner.
4. **FR-4**: There MUST be **no** run-all-concepts default and **no** automation of stages after `model-critic`.
5. **FR-5**: An archive step MUST move a concept's old **pipeline-produced** artifacts (e.g. `analysis.md`, `model_setup.py`, `model_output.txt`, `synthesis.md`, `iter-*/`, `prompts/`, prior `critic_review_*`) to `archive/concept_analysis_pre_rework/{cid}/` using `git mv` so history is retained.
6. **FR-6**: The archive step MUST NOT move regeneration **inputs** or hand-written content — specifically `design-points/` and human-authored `review.md` stay at the live path.
7. **FR-7**: The `status` subcommand MUST display, per concept, `P_native`, native LCOE, and `result_1gw` LCOE, alongside the existing iteration/state columns.

### Non-Functional Requirements

- None — batch sizes are small (operator-selected), so runtime/cost is not a constraint.

---

## Acceptance Criteria

### Core Functionality

- [ ] FR-1/FR-2/FR-3: Passing 2–3 concept IDs runs them concurrently for `analyze --max-passes N` and for `model-critic`, with `[i/total] cid: OK|FAILED` output; the underlying pool is the reused `run_scoring_pipeline.py` machinery.
- [ ] FR-4: There is no path that defaults to all concepts and no invocation of review/synthesize/score/approve from this item's runner.
- [ ] FR-5/FR-6: After the archive step on a concept, `git log --follow` on a moved artifact shows pre-move history; `design-points/` and `review.md` remain at the live path untouched.
- [ ] FR-7: `status` prints the three new columns; native LCOE and `result_1gw` LCOE resolve from the regenerated three-forward `model_setup.py` and `P_native` from frontmatter.

### Quality & Integration

- [ ] Existing `exploration/concept_analysis/scripts/` tests continue to pass.
- [ ] The existing scoring pipeline (`run_scoring_pipeline.py`) still works if its runner is generalized.

---

## Next-Stage Handoff

**Settled in this spec:**
- The parallel runner operates on an explicit concept list, covers `analyze` (with `--max-passes`) and `model-critic`, reuses the existing pool machinery, and stops after the critic.
- Archive is `git mv` to `archive/concept_analysis_pre_rework/{cid}/`, preserving `design-points/` and human `review.md`.
- `status` gains `P_native` / native LCOE / `result_1gw` LCOE columns.

**Design must figure out:**
- Whether to generalize `run_scoring_pipeline.py` (add `analyze` / `model-critic` to its stage handling + accept an explicit concept list) or add a thin sibling that imports its helpers; and the per-stage flag set (`--max-passes` for analyze, none for critic).
- The archive step's form: a documented procedure, a tiny helper script, or a `status`-adjacent subcommand — and the exact artifact include/exclude list.
- The robust source for native / `result_1gw` LCOE in `status` (module-load like the explorer vs. parsing `model_output.txt`, given the three-forward format change).
- Whether cross-concept landscape reads need any freezing at the batch sizes the operator uses (default: don't, unless evidence says otherwise).

**Watch-outs for design:**
- Depends on Item 10 + the three-forward contract being landed — regenerated artifacts and the stats assume `generic`/`native`/`result_1gw`.
- Don't let the archive step move `design-points/` (a regen input) or clobber human-authored `review.md`.
- Keep the existing scoring pipeline working if its runner is generalized.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 11
- **Parallel pattern to reuse:** `exploration/concept_analysis/scripts/run_scoring_pipeline.py`
- **Per-concept primitives:** `run_analysis.py` `analyze` (`--max-passes`, in-loop model-setup) + `model-critic`
- **Upstream deps:** Item 10 ([`concept-rework-explorer-pilot`](../concept-rework-explorer-pilot/spec.md)), three-forward contract ([`concept-rework-three-forward-contract`](../concept-rework-three-forward-contract/spec.md))
- **Design:** `.project/active/concept-rework-bulk-regeneration/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
