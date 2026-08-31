# Current Work

**Updated 2026-08-30 (magnet-closure: goal measured at target — three owner rulings pending).**

## Where things stand

- **Goal `magnet-closure` round 2 closed** (`work/orchestration/goals/magnet-closure/trail.md`, close commit `0cf0cf41`): the fresh non-author Row-3 re-grade at the frozen `rubric.md@dc0f0b6d` reads **R3.P = 3 (was 1), R3.S = 3 (was 2)** — the goal's § Answered when target, the demo epic Item 10 chain's first measured maturation delta. Deposit: `.project/active/demo-depth-rubric/grading-r3-regrade.md`.
- **Three owner rulings pending** (trail § Round 2 Stop): (1) the § Answered when "affected studies re-run clean" reading (new study clean + the restated non-reproducible B-axis comparand — or re-run something first); (2) the goal close itself; (3) the routing proposal for `20260830-stress-fence#1`/`#2` — one modeling item, the winding-pack sizing chain, MFE Cost Modeling epic.
- **A fresh session should review round 2** (`GOAL_RUNBOOK.md` § The fresh review) before or at close.
- WI-035 at `work/active/` awaits item close; merge/push owner-held; `magnet-ab#4` stays behind the Rung C gate. Baseline: LCOE 304.482, total capital $14.574B, seven verdicts satisfied.

---

## Previous status
**Last Updated**: 2026-08-30

---

## Active work

- **demo-depth-rubric** (`.project/active/demo-depth-rubric/`, Stellarator MBSE Demo — maturation phase) — spec in progress 2026-08-30. Concept: `.project/concepts/stellarator-demo-maturation.md` (new 2026-08-30: no reveal; clean-room split; 1costingFE anchor closed).

## Where `main` stands (2026-08-30)

- **PR #110 merged** (`66bbdb81`, 2026-08-30): WI-033 (`p_pump` 1.0 → 195.0 MW re-base + regenerated sealed package), GSTH Item 6, the GSTH epic close, four-digit ADR register, product ledger entry 0001. Gate report: `.project/reports/2026-08-30-pre-pr-wi033-gsth-epic-close.md` (READY, battery 574/14/0).
- **Stellarator demo landing merged** — PR #104 (`d0e4398d`): run-study skill and tools (`.claude/skills/run-study/`, `scripts/study/`, `tests/study/` 273), proof-of-life design search (`exploration/stellarator_e2e/study/`), before-migration record. The certified migration is archived at `.project/completed/20260821_stellarator-model-migration/`.
- **Stop-parser shipment merged** — PR #102 (`5338db5f`). fusion-tea pins agentic-mbse / sysml-codegen / 1costingfe to sealed git SHAs; `tests/test_dependency_provenance.py` verifies the chain. Shipment record in sysml-codegen: `.project/completed/20260820_stop-parser-pr-shipment/plan.md`. Tags `stop-parser/*` must not move.
- **CONSTRAINT-EXEC fusion-side items done** — Items 8, 9, 14 Appendix C committed 2026-07-20. Record: `work/active/20260713_constraint-exec-acceptance/brief.md`.
- **Explorer** — UX v3 Phase 1 + Themes A/B1/F merged; 1costingfe v0.1.0 migration 2026-06-28; web hosting (#97; operator runbook `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`); OOM Layers 1–2 (#98), JAX pre-warm (#99), numpy-only deploy on 1costingfe v0.1.1 (#100).
- **`.project/` archival pass done 2026-08-21** (on this branch): 56 item dirs and 6 epics moved to `completed/` with the `20260821_` prefix, 3 empty dirs deleted, live path references rewritten. `active/` now holds 5 dirs. Record: `.project/completed/CHANGELOG.md`, report `.project/reports/2026-08-21-1339-status-report.md`.

## GSTH — epic closed (2026-08-30)

- **The epic is closed and archived** to `.project/completed/20260830_epic_goal_strategy_task_harness.md` — all six items closed 2026-08-27 → 2026-08-30, all eleven epic success criteria ticked (per-criterion evidence: `.project/completed/20260830_goal-integration-study-proof/epic_evidence.md` § 2), product-lens gate CLEAR. Product ledger entry **0001** ("A non-builder runs a goal round from the runbook and native records alone") filed at close; `ADR-0010` records the oracle-carry ruling (the "pending owner yes/no" is discharged). Every seam `GOAL_RUNBOOK.md` lists is native.
- **PR #110 is merged** (2026-08-30, `66bbdb81`) — WI-033 + Item 6 + the epic close shipped as one PR (spec § Align ruling 2), gate READY. Nothing GSTH remains owner-held. Three fully-merged branches remain on origin and can be deleted: `feat/goal-integration-seam`, `feat/goal-research-model-proof`, `feat/wi033-p-pump-rebase`.
- **Live follow-up: `WI-034`** ("CAS10 land-term guard", MFE Cost Modeling epic, `work/BACKLOG.md`, status `backlog`), minted at `5d740688`. One defect, two sightings: `net_positive` cannot read violated because CAS10's land term takes `sqrt(p_net)` and fails first. Four recorded hardening candidates (`epic_evidence.md` § 4): F-1/F-2 fixed at close as documentation, F-3/F-4 recorded with fix homes; no mechanism promoted, per epic SC 7.

## Next up (in order, 2026-08-21)

0. **Run-study end-to-end explainer** (`.project/active/run-study-e2e-explainer/`, new run-study epic Item 7) — spec approved 2026-08-23 (product-lens DISPOSED); story outline drafted 2026-08-23 (`story-outline.md`, html-explainer Step 1, owner review pending — **caution: the file is not in `.project/active/run-study-e2e-explainer/` and is in no branch's history**; either recover it or re-draft, per the 2026-08-30 09:00 status report finding 3); next `/_my_design`; gates Item 6 Phase 4. Deep HTML explainer of the two A/B studies for an outside reader, to live in `exploration/stellarator_e2e/studies/`.
1. **RUN-STUDY Item 6** (first A/B consumer + policy cutover) on the stock route — unblocked by the archived stellarator migration certification (`.project/completed/20260821_stellarator-model-migration/audit.md`). Owner Align held 2026-08-21 (`.project/active/run-study-first-consumer/align.md`: policy ratified, comparison left to design research, oracle for this demo only); spec drafted 2026-08-21 (`spec.md`, Draft): two studies (REBCO vs Nb3Sn magnets after a `work/` modeling item; Rankine vs sCO2 on the current package), research round in `work/` first; research at `.project/research/20260821-141439_item6-ab-candidates.md`. Design drafted 2026-08-21 (`design.md`: two studies, definitions in the record dir, one store per study, two `work/` prerequisites). Modeling PM: **WI-030** (computed beta + peak-field limit; spec at `work/completed/20260822_WI-030_computed-beta-peak-field/spec.md`, SV-036 pending) and **WI-031** (research round for the four unsourced second-arm values; `work/completed/20260822_WI-031_research-round-item6-values/spec.md`) minted. Plan drafted (`plan.md`: Phase 1 today off `main`, Phases 2–3 gated on the migration/WI-031/WI-030). **WI-030 designed 2026-08-21** (`work/completed/20260822_WI-030_computed-beta-peak-field/design.md`, prototype PASS on the pinned codegen; research approved at `knowledge/research/approved/20260821-152108_wi030-computed-beta-peak-field.md`). Four `/_my_ask_me` rulings in the design: calc-then-compare shape for the peak-field constraint (the pinned codegen compiles arithmetic in a predicate, but `scripts/study/indicators.py:469` / `verify.py:193` cannot parse it — BACKLOG Flagged row), `magnet__peak_ratio` / `magnet__B_max` on the library Magnet System, DI deferred to close, design written before the merge (now moot: PR #107 merged). Spec amended: `peak_ratio = 2.766666666666
