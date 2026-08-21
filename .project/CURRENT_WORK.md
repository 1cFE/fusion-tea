# Current Work

**Last Updated**: 2026-08-20

---

## Where `main` stands (2026-08-20)

- **Stop-parser shipment merged** — PR #102 (`5338db5f`). fusion-tea now pins agentic-mbse / sysml-codegen / 1costingfe to sealed git SHAs; `tests/test_dependency_provenance.py` verifies the chain. The shipment record (every gate and deviation) is in sysml-codegen: `.project/completed/20260820_stop-parser-pr-shipment/plan.md`. Tags `stop-parser/*` must not move.
- **CONSTRAINT-EXEC fusion-side items done** — Item 8 (IFE package regenerated with the embedded constraint catalog, hand-built catalog script deleted), Item 9 (stock multi-channel bridge, wrappers deleted), Item 14 Appendix C (IFE viability acceptance). All committed 2026-07-20 and on `main`. Record: `work/active/20260713_constraint-exec-acceptance/brief.md`. The `item8-fusion-embedded-catalog` branch was deleted 2026-08-20; it had no commits of its own.
- **Explorer** — UX v3 Phase 1 + Themes A/B1/F merged; 1costingfe v0.1.0 migration done 2026-06-28 (`reports/2026-06-28_1costingfe-v0.1.0-migration.md`). Web hosting merged (#97). OOM Layers 1–2 merged (#98), JAX pre-warm (#99), deploy switched to numpy-only 1costingfe v0.1.1 (#100).
- **Working tree** — cleaned 2026-08-20: stale `uv.lock` edit discarded (`main`'s lock is current, `uv lock --check` passes), IFE run residue and `_bridged` scratch dirs deleted, stranded `.project/` docs committed.

## Next up

### Whole-plant regeneration on the elaborate-first route

Fusion-tea's half of sysml-codegen's ELABORATE-FIRST Item 8. Owner-decided order (2026-08-15): codegen's scope scrub first (A), then fusion-tea whole-plant regeneration (B). Branch off `main`. Context and premises: sysml-codegen `.project/CURRENT_WORK.md` ("2026-08-15: Item 8 sequencing"). The Stellarator model is split out of this item (lives in `~/1cfe/fusion-tea-stellarator-mbse-demo`).

### Explorer UX v3 — Phase 2

Pick the next item by leverage; D1 (per-account override decomposition) is the top candidate. Epic: `.project/backlog/epic_explorer_ux_v3.md`. Small loose ends listed there: concept 27 stale data, FR-SO1 test's stale `>5%` assertion, re-extract 37 & 39.

## Open decisions

- **`feat/compute-concurrency-semaphore`** (1 commit, unmerged, off an old `main`). It caps concurrent JAX `forward()` calls, but #100 made the deploy numpy-only, so the memory profile it guards against may be gone. Decide: land it or delete the branch. Background: `.project/reports/2026-07-03-1114-status-report.md`.
- **`run_analysis.py` CLI step semantics** — a real bug with a paused spec (`.project/active/run-analysis-cli-step-semantics/spec.md`, BACKLOG row). `analyze` and `model-setup` look like peers but overlap; `regenerate-concept` chains them so the weaker path overwrites the loop's output. Schedule or drop.

## Paused / deferred

- `batch-pipeline-run` — plan drafted, unblocked since 2026-04-11, not started.
- `traceability-system` — spec + plan, awaiting prioritization.
- `loop-dry-run-symmetry` — spec only; `archive/fix-feedback-data-leak-2026-04-13` tag holds the implementation work.

## Housekeeping owed

- **`.project/active/` archival pass.** ~50 item dirs, most finished but never moved to `completed/`. Last archival was 2026-04-11 (`.project/completed/CHANGELOG.md`).
- **Branch / worktree tidy.** Local branches already merged: `chore/retire-pipeline-truth-workarounds` (#101), `feat/explorer-web-hosting` (#97), `stop-parser-fusion-r2` (#102), `self-binding-replacement` (in `main`). Unmerged: `epic/pipeline-derisk-demo`, `feat/compute-concurrency-semaphore`, `stop-parser-verification`. Worktrees: `fusion-tea-portfolio-audit-stage` (detached), `fusion-tea-self-binding`, `fusion-tea-stellarator-mbse-demo` (active), plus `/tmp/stop-parser.QVJIIP/*` and `/tmp/ft-main` (prunable). Each deletion needs owner sign-off. Earlier cleanup record: `.project/reports/2026-05-22-branch-cleanup.md`.
- **Merge flow reminder.** Branch protection needs a review the author can't self-provide; agent pushes + opens the PR, owner merges with `! gh pr merge <n> --repo 1cFE/fusion-tea --merge --admin`. Use a merge commit for anything a downstream pin depends on.

## Stellarator demo + run-study capability (landed from `feat/stellarator-mbse-demo`)

- **Run-Study Capability epic** (`.project/backlog/epic_run_study_capability.md`): Items 1–5 complete and audited 2026-08-20. Delivered: `.claude/skills/run-study/`, `scripts/study/` (indicators, manifest, identity, preflight, verify), `exploration/stellarator_e2e/studies/` (manifest, era adapter, oracle seam, ANNEX), `tests/study/` (273). **Item 6 (first A/B consumer) runs after the model migration** `[OWNER 2026-08-21]`, on the stock teax route.
- **Stellarator MBSE Demo epic** (`epic_stellarator_mbse_demo.md`): On Hold by owner (2026-08-19). Items 1–4 done (handshake to 1costingFE: LCOE 275.264220, 5/5 verdicts). Proof-of-life design search (948-point grid) in `exploration/stellarator_e2e/study/`.
- **Package state**: sealed 2026-07-25 on codegen `06d95f8`, `runtime_contract_version 1.0.0`; runs only on the era teax worktree (`/home/reid/1cfe/teax-v1-era` @ `fa0e06a`) through `era_adapter.py`. Current teax main refuses it by design.
- **MFE models live only in the staged twin** `exploration/stellarator_e2e/models/` for now (owner decision Q1 → A): main's spine test generates the whole `models/` tree and the MFE models cannot generate on the pinned codegen yet (94 self-named bindings + three further refusal classes). See `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § 2–3.
- **Next**: the model-migration item (D-5 rename, scalar-function rewrites, unit-comment and positional-binding fixes, regenerate at 2.0.0, retire the adapter). Landing plan: `.project/active/stellarator-demo-landing/plan.md`.
