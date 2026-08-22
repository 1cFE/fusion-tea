# Current Work

**Last Updated**: 2026-08-21

---

## Where `main` stands (2026-08-21)

- **Stellarator demo landing merged** — PR #104 (`d0e4398d`): run-study skill and tools (`.claude/skills/run-study/`, `scripts/study/`, `tests/study/` 273), proof-of-life design search (`exploration/stellarator_e2e/study/`), before-migration record. The certified migration is archived at `.project/completed/20260821_stellarator-model-migration/`.
- **Stop-parser shipment merged** — PR #102 (`5338db5f`). fusion-tea pins agentic-mbse / sysml-codegen / 1costingfe to sealed git SHAs; `tests/test_dependency_provenance.py` verifies the chain. Shipment record in sysml-codegen: `.project/completed/20260820_stop-parser-pr-shipment/plan.md`. Tags `stop-parser/*` must not move.
- **CONSTRAINT-EXEC fusion-side items done** — Items 8, 9, 14 Appendix C committed 2026-07-20. Record: `work/active/20260713_constraint-exec-acceptance/brief.md`.
- **Explorer** — UX v3 Phase 1 + Themes A/B1/F merged; 1costingfe v0.1.0 migration 2026-06-28; web hosting (#97; operator runbook `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`); OOM Layers 1–2 (#98), JAX pre-warm (#99), numpy-only deploy on 1costingfe v0.1.1 (#100).
- **`.project/` archival pass done 2026-08-21** (on this branch): 56 item dirs and 6 epics moved to `completed/` with the `20260821_` prefix, 3 empty dirs deleted, live path references rewritten. `active/` now holds 5 dirs. Record: `.project/completed/CHANGELOG.md`, report `.project/reports/2026-08-21-1339-status-report.md`.

## Next up (in order, 2026-08-21)

1. **RUN-STUDY Item 6** (first A/B consumer + policy cutover) on the stock route — unblocked by the archived stellarator migration certification (`.project/completed/20260821_stellarator-model-migration/audit.md`). Owner Align held 2026-08-21 (`.project/active/run-study-first-consumer/align.md`: policy ratified, comparison left to design research, oracle for this demo only); spec drafted 2026-08-21 (`spec.md`, Draft): two studies (REBCO vs Nb3Sn magnets after a `work/` modeling item; Rankine vs sCO2 on the current package), research round in `work/` first; research at `.project/research/20260821-141439_item6-ab-candidates.md`. Design drafted 2026-08-21 (`design.md`: two studies, definitions in the record dir, one store per study, two `work/` prerequisites). Modeling PM: **WI-030** (computed beta + peak-field limit; spec at `work/completed/20260822_WI-030_computed-beta-peak-field/spec.md`, SV-036 pending) and **WI-031** (research round for the four unsourced second-arm values; `work/completed/20260822_WI-031_research-round-item6-values/spec.md`) minted. Plan drafted (`plan.md`: Phase 1 today off `main`, Phases 2–3 gated on the migration/WI-031/WI-030). **WI-030 designed 2026-08-21** (`work/completed/20260822_WI-030_computed-beta-peak-field/design.md`, prototype PASS on the pinned codegen; research approved at `knowledge/research/approved/20260821-152108_wi030-computed-beta-peak-field.md`). Four `/_my_ask_me` rulings in the design: calc-then-compare shape for the peak-field constraint (the pinned codegen compiles arithmetic in a predicate, but `scripts/study/indicators.py:469` / `verify.py:193` cannot parse it — BACKLOG Flagged row), `magnet__peak_ratio` / `magnet__B_max` on the library Magnet System, DI deferred to close, design written before the merge (now moot: PR #107 merged). Spec amended: `peak_ratio = 2.7666666666666666` (2.7667 reads violated at the design point), LTS check at 4.69 T (4.70 is violated). Design approved and planned 2026-08-21 (`plan.md`, five phases, draft pending owner approval); WI-030 stays on this branch `[OWNER 2026-08-21]`; Item 6's design table (bare `B_max`/`peak_ratio`, 4.70 T) is settled up at the end — the model is the source of truth `[OWNER 2026-08-21]`. **WI-030 implemented 2026-08-21, commit `ba5c9945`** (all five plan phases; SV-036 passing, record at `work/completed/20260822_WI-030_computed-beta-peak-field/verification_record.md`): package 173/75/6 at semantic `1ca93d0c…` / executable `7447efea…`, headline unchanged to the cent, six verdicts, beta 0.026834 (A) / 0.028691 (B) bit-exact vs the oracle, preflight 6/6, verify pass, `tests/study` 262 / `tests/models` 48 green. Item 6 resumes on this package: keys `magnet__B`, `magnet__B_max` (=24.9 HTS / 13.0 Nb3Sn), `magnet__peak_ratio`, `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`; LTS on-axis ceiling 4.6988 T (use 4.69); `beta` objective in the manifest. **WI-030 audited and closed 2026-08-22**: audit POSITIVE (`work/analysis/20260821-171229_audit_WI-030_computed-beta-peak-field.md`; one WARN — L6 `DESIGN_ATTR_INCOMPLETE` 98 → 102 from the four no-default plant attributes, by design D10, so the next validator baseline is 102; one record nit — Point B override was the exact 0.636580, not 0.6366), archived to `work/completed/20260822_WI-030_computed-beta-peak-field/`, DI-011 minted (`knowledge/KNOWLEDGE.md`). Next: Item 6 `/_my_implement` Phase 1 and the design-table settle-up. Environment note: `tests/test_dependency_provenance.py::test_installed_artifacts…` needs `STOP_PARSER_WHEEL_TARGET` exported. Owed upstream filing: agentic-mbse `pm approve-research` refuses an empty insight list (`pm/operations.py:664-668`); the WI-030 report was moved to `approved/` by hand.
2. **Upstream filings to sysml-codegen** — three rows written 2026-08-21 by the archived migration (scalar-function vocabulary, unit-scrape byte offset, plus the unit-scrape defect); they sit uncommitted in `/home/reid/1cfe/sysml-codegen/.project/backlog/BACKLOG.md` for the owner's commit.
3. **IFE whole-plant regeneration on the elaborate-first route** — fusion-tea's half of sysml-codegen's ELABORATE-FIRST Item 8, step B after codegen's scope scrub A (owner order 2026-08-15). Context: sysml-codegen `.project/CURRENT_WORK.md` ("2026-08-15: Item 8 sequencing").
4. **Explorer UX v3 — Phase 2**: pick by leverage, D1 top candidate. Epic: `.project/backlog/epic_explorer_ux_v3.md`.

## Recently Completed

### 2026-08-21: Stellarator Model Migration

- Regenerated and sealed the stellarator package at runtime contract 2.0.0 on stock teax with numerical identity across the baseline, 948-point grid, and 19-point sweep.
- Promoted the MFE models into `models/`, preserved both family regression spines, closed the CAS27 verification gap, and retired the primary era adapter whole.
- Made study publication and the single-point evidence command fail closed; all SC1–SC11 criteria were certified. Archive: `.project/completed/20260821_stellarator-model-migration/`.

## Open decisions

- **`feat/compute-concurrency-semaphore`** (1 commit, unmerged, off an old `main`). It caps concurrent JAX `forward()` calls, but #100 made the deploy numpy-only, so the memory profile it guards against may be gone. Decide: land it or delete the branch. Background: `.project/reports/2026-07-03-1114-status-report.md`.
- **`run_analysis.py` CLI step semantics** — a real bug with a paused spec (`.project/active/run-analysis-cli-step-semantics/spec.md`, BACKLOG row). `analyze` and `model-setup` look like peers but overlap; `regenerate-concept` chains them so the weaker path overwrites the loop's output. Schedule or drop.
- ~~Rework design-point gate never signed~~ — accepted as-is `[OWNER 2026-08-21]`; BACKLOG Flagged row.
- **Delete `.project/completed/` folders before a cutoff date, keep `CHANGELOG.md`** `[OWNER 2026-08-21]` — not yet; a later pass. Cutoff date still to be chosen. Git history keeps everything; the changelog stays as the index. Live citations into the deleted folders (`ingest_design_point_proposals.py:32`, `test_validators.py:547`, `.claude/skills/run-study/record-template.md`, `knowledge/holdout/aries-cs/PROTOCOL.md`) will need repointing in that pass.

## Paused / deferred

- `traceability-system` — spec + design + plan (2026-03-02), never started; still the citation-format reference for CLAUDE.md / MR-4.
- `loop-dry-run-symmetry` — spec only; the gap is still live at `exploration/concept_analysis/scripts/lib/loop.py:620`.
- ~~`demo-study-parameterization-policy/policy.md`~~ — ratified and moved to `modeling_project/STUDY_POLICY.md` 2026-08-21 (Item 6 Phase 1).

## Housekeeping owed

- **Branch / worktree tidy.** Local branches already merged: `chore/retire-pipeline-truth-workarounds` (#101), `feat/explorer-web-hosting` (#97), `stop-parser-fusion-r2` (#102), `self-binding-replacement` (in `main`). Unmerged: `epic/pipeline-derisk-demo`, `feat/compute-concurrency-semaphore`, `stop-parser-verification`. Remote `fix/eta-th-double-count` is dead (PR #31 closed; fixed in 1costingFE YAMLs instead). Worktrees: `fusion-tea-portfolio-audit-stage` (detached), `fusion-tea-self-binding`, `fusion-tea-stellarator-mbse-demo`, `/home/reid/1cfe/teax-v1-era` (unused since the migration), plus `/tmp/stop-parser.QVJIIP/*` and `/tmp/ft-main` (prunable). Each deletion needs owner sign-off. Earlier cleanup record: `.project/reports/2026-05-22-branch-cleanup.md`.
- **Merge flow reminder.** Branch protection needs a review the author can't self-provide; agent pushes + opens the PR, owner merges with `! gh pr merge <n> --repo 1cFE/fusion-tea --merge --admin`. Use a merge commit for anything a downstream pin depends on.

## Stellarator demo + run-study capability

- **Run-Study Capability epic** (`.project/backlog/epic_run_study_capability.md`): Items 1–5 complete and audited 2026-08-20 (dirs archived under `completed/20260821_run-study-*`). Item 6 is unblocked after the certified model migration `[OWNER 2026-08-21]`, on the stock teax route.
- **Stellarator MBSE Demo epic** (`epic_stellarator_mbse_demo.md`): On Hold by owner (2026-08-19). Items 1–4 done (handshake to 1costingFE: LCOE 275.264220, 5/5 verdicts). The ARIES-CS barred/admissible lists live in `completed/20260821_aries-cs-holdout/spec.md` (pointer updated in `knowledge/holdout/aries-cs/PROTOCOL.md`).
- **Package state**: regenerated 2026-08-21 on the pinned codegen `8a758e92`, `runtime_contract_version 2.0.0`, runs on stock teax (`744745f`) with no adapter. MFE models live in `models/` with `exploration/stellarator_e2e/models/` as the byte-identical twin; `tests/models/test_model_family_spines.py` generates each family from its own canonical subset.
