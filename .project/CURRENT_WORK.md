# Current Work

**Last Updated**: 2026-07-14

---

## Active Work

### Stellarator MBSE Demo — first item implemented (aries-cs-holdout)

**Status**: `aries-cs-holdout` implemented and committed (`8939d9dc` + ratification follow-up), pending `/_my_audit`. Quarantine live at `knowledge/holdout/aries-cs/` (4 PDFs + manifest + README + PROTOCOL.md, plus one CLAUDE.md line); all leak-surface verifications passed. Owner ratified (2026-07-13) the two ingestion-time barred-list additions (the `knowledge/sources` Helios extraction and a concept-36 ARIES-CS stub). Note: ARIES mirrors are all dead — PDFs came from Wayback snapshots of the canonical URLs, recorded in PROTOCOL §7. Concept at `.project/concepts/stellarator-mbse-demo.md`. On branch `feat/stellarator-mbse-demo`.

### Stellarator MBSE Demo — Stage 3 item 1 DONE: WI-019 faithful power balance (2026-07-14, uncommitted)

**Status**: WI-019 implemented, validated, handshake-verified — **uncommitted in the worktree**, pending review/commit. Spec → owner checkpoint (approved, order 3→4→1→2 confirmed) → design → plan → implement, all same-day. PROTOCOL.md respected; sourcing 1costingFE @ `0254385` only.

**What changed**: `'MFE Power Balance Calc'` now computes the faithful thermal power `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump` — the collapsed form of 1costingFE physics.py steps 4–7 (p_rad cancels algebraically at f_dec=0; no radiation model needed). `p_pump` is 1costingFE's absolute input (fpcppf trap resolved), alpha fraction exact (3.52/17.58). Consumers rebound (generic plant, concept-09 instance, staged e2e copies, oracle); pipeline regenerated; handshake re-run.

**Results**: **SV-025 passing** — all six power channels match 1costingFE at ≤6.3e-8 (float32 floor; tolerance was 1e-5). **SV-026 passing** — all 12 power-scaled accounts end-to-end ≤1e-7 (was −8.6…−16.4%). Net electric at the 1 GWe point now exact. **New Stellaris headline: p_net 786 MW (was 575), q_eng 3.87, total $10.09B, LCOE $189/MWh (was 251).** LCOE handshake gap moved −13%→−31% *by design*: the old figure was two errors partly cancelling (understated capital vs understated denominator); the −31% is the honest structural distance (unmodeled CAS22 tail + CAS40/50/60 + LCOE construction) and is the measured target for the remaining account-scope items.

**Surfaced at close (owner attention)**:
1. Three pass-throughs (`buildings_capital`, `preconstruction_capital`, `annual_om`) were derived at the old p_net=575; annotated STALE BASIS in the instance files. Recomputing them (Stage-3 account-scope item) will move capital/LCOE again.
2. SV-016's "Q_eng ~10–40" band predates the fix; measured 3.87 (Stellaris) / 8.84 (1cfe 1 GWe). Needs owner adjust/annotate.
3. Pre-existing broken test `tests/models/test_power_balance.py` (targets pre-WI-009 layout; fails at HEAD) — candidate small backlog item.

**Next**: owner review + commit; then demo item 4 (stellarator-correct geometry) per the approved 3→4→1→2 order — new `/spec-model` + owner checkpoint.

### Stellarator MBSE Demo — Stage 2 (initial model) BUILT + committed (2026-07-13, `c3f3089e`)

**Status**: The full Stage-2 initial-model chain is built, validated, end-to-end-run, and committed at `c3f3089e`. All demo model-development sessions respected the ARIES-CS blocklist. (Stage-2 headline numbers below are pre-WI-019; see the Stage-3 entry above for current.)

**What was built (WI-009 → WI-010 → WI-018 → codegen → handshake):**
- **WI-009 MFE cost-structure library** (`models/library/`, 7 files): enum `mfe_divergent`, MFE CAS22 sub-accounts + `'Magnet System'`, and the plasma-scaling / power-balance / magnet-cost / LCOE-DCF / viability calc+constraint defs. Sourced purely from **1costingFE @ `0254385`** (clean; ARIES-CS anchor dropped, barred citations re-pointed — see contamination note below). AD-007 registered; SV-019/020/021/022 passing.
- **WI-010 generic MFE plant** (`models/designs/generic_mfe/`): composes subsystems, wires the physics→cost→LCOE spine, asserts viability. The two untested wiring constructs (cross-calc binding, part-level `assert constraint`) are **validated and survive extraction** (SV-024). Forward-pass fix: WI-009 power balance now exposes `p_th`/`p_the`/`p_et`.
- **WI-018 concept-09 "Stellaris" instance** (`models/designs/stellarator_09/`): Stellaris design point — physics/geometry from the admissible Stellaris sources, cost/engineering params from 1costingFE stellarator defaults. Viability (beta, wall load, TBR) all pass. Mapping traps documented (r_coil, sigma_v, B-vs-b_center).
- **Codegen → teax** (`exploration/stellarator_e2e/`): the chain **closed** — every executed channel bit-exact vs the pure-Python oracle. Headline: V=564 m³, fusion 2700 MW, net 575 MWe, **LCOE $250.95/MWh, total $9.783B**, magnet-dominated (44.9%). Via snapshot+V11-bridge (canonical `models/` untouched; codegen-adapted copies staged in `stellarator_e2e/`).
- **Anchor A handshake** (`exploration/stellarator_e2e/HANDSHAKE_REPORT.md`): fed 1costingFE's solved 1 GWe point into the generated model. **Machinery validated: formula-isolation matches every account to ~1e-8** (magnet 5.4e-10). End-to-end LCOE −13%, total capital −44% — entirely documented model-scope simplifications, not codegen error.

**Success criteria**: SC-1 (runs end-to-end, LCOE + full CAS) ✓; SC-2 (viability as modeled constraints) — DEFINED, execute at Stage 4 per owner decision (constraint-exec epic); SC-3 (1costingFE handshake) ✓ machinery bit-exact, discrepancies itemized.

**Stage-3 backlog (from the handshake, ranked by leverage):**
1. **Power balance fidelity** (top): SysML 0D `p_th` omits alpha/wall + radiation power to the blanket (~547 MW, 19%) → −16.4% p_th cascading into every power-scaled account. Align with `physics.py`.
2. **CAS22 reactor-plant tail** (~1093 M$): remote handling, installation, coolant, cryoplant, waste, fuel handling, I&C. Plus CAS40 owner / CAS50 supplementary.
3. **LCOE construction**: add CAS70 levelized O&M + CAS80 fuel; reconcile IDC treatment (SysML folds into DCF vs 1costingFE CAS60 line).
4. Vessel gas-load pump sub-term; 0D reactivity/volume (sigma_v tuned to design power; torus-volume 564 vs Stellaris 448); ISS04 confinement-consistency constraint (deferred at Stage 2).

**Codegen findings** (`exploration/stellarator_e2e/CODEGEN_FINDINGS.md`, file upstream): #8 EXPOSE-alias wires by consumer-input name (V11 blind spot, teax rejects; harness glue closes); #9 strict-mode `assert constraint` now aborts on plain design-attribute actuals (constraints commented in staged copies — Stage-4 scope).

**Contamination note**: the pre-quarantine WI-009 `design.md` carried an ARIES-CS ~$9700/kW anchor + barred-doc citations; logged in PROTOCOL §5/§6 (2026-07-13), demo build re-sourced to 1costingFE only. No barred file was read by any build session.

**Next**: owner review + commit; then Stage 3 (start with the power-balance fix — highest leverage). Every demo work item lists PROTOCOL.md as Required Reading.

### EXPLORER-UX-V3 — Phase 1 verified; migration complete; pick next Phase-2 item

**Status**: Phase 1 + Themes A/B1/F all merged to `main`; 1costingfe v0.1.0 migration complete and Phase 1 re-verified. **Next: pick the next Phase-2 item by leverage (top candidate D1).**
**Epic**: `.project/backlog/epic_explorer_ux_v3.md` (see its "Post-merge status" + "1costingfe v0.1.0 migration" sections)

What's merged:
- **Phase 1** — Item 1 (slider/tornado/headline coherence), Item 2 (override-inspection surface), FU1 (CAS header hint). Override-overlay UX = PR #52; built on rework infra #44.
- **Theme A** — identity & shared spine. PR #58. **Theme B1** — ontology matrix home page. PR #59. **Theme F1** — cost landscape page. PR #64.

**1costingfe v0.1.0 migration (2026-06-28) — done.** Library on `1costingfe@0254385`; all explorer data regenerated (Option A: re-enable the gated solvers from the fusion-tea side). FR-SO1 holds for 33/33 served concepts; tests 19/20. The "concept 01 override moves the headline only 1.26%" scare is **resolved and benign** — the override behaves as designed; the recalibration raised the bare baseline under a frozen-by-design override (~19% at native scale, ~1.26% at the 1 GWe headline). Nothing broke. Full writeup: `reports/2026-06-28_1costingfe-v0.1.0-migration.md`.

**Small non-blocking loose ends**: concept 27 stale data (routing-config fix); FR-SO1 test's stale `>5%` assertion; Item 2-FU (re-extract 37 & 39); spike/override-policy doc cleanup.

**Unbuilt Phase-2 candidates** (pick by leverage): **D1** (per-account override decomposition — top candidate), C1 (Design Space Viz rebrand), C2 (comparables entry), B2/B3, D2/D3, E1–E3.

### Explorer Web Hosting — separate deployment track (in progress)

**Status**: On `feat/explorer-web-hosting` (current branch). Not epic work.
**Location**: `.project/active/explorer-web-hosting/` (spec/design/plan/RUNBOOK)

Railway container deployment of the concept_explorer: slim serving manifest (`requirements-serve.txt`), `Dockerfile` + `railway.toml`, `scripts/smoke_explorer.py`, operator runbook. Plus a separate static "score explorer" published from `docs/` with a CNAME. 5 commits ahead of `main`.

### Compute OOM — debounce + cache quantization (implemented, ready to PR)

**Status**: Implemented on `feat/compute-oom-debounce-quantize` (off `feat/explorer-web-hosting`). PR back into the hosting branch to trigger the Railway rebuild.
**Location**: `.project/active/compute-oom-debounce-and-quantize/` (spec + design w/ impl notes)

Fixes the Railway OOM-kill under multi-user slider load. Layer 1 (client): `tornado.js` debounce 200→400ms + `AbortController` in `concept_page.js:onSliderChange` (at most one in-flight compute/client; abort detected via `controller.signal.aborted`, indicator-hide guarded against superseded requests). Layer 2 (server): `_quantize_sig` rounds override floats to 4 sig figs before the `_compute_cached` LRU key so nearby slider positions share a `forward()`. Verified: 15/15 compute tests, parity gate 33/33 @1e-5, browser drag (6 events→1 request, headline updates, no error flash, 0 console errors). FR-SO1 untouched (no-op path sends empty overrides → nothing to quantize). Out of scope: `forward()` semaphore.

### Batch Pipeline Run (unblocked, not started)

**Status**: Plan drafted, ready to start
**Location**: `.project/active/batch-pipeline-run/`

Run all concepts through the now-hardened pipeline to approval. Unblocked by the 2026-04-11 pipeline-hardening archival.

### Concept Explorer (merged)

**Status**: Merged and functional
**Location**: `exploration/concept_explorer/`

4-page interactive explorer (Index, Concept Profile, Comparison, Taxonomy) with FastAPI backend. Extracts data from pipeline artifacts. 140+ tests. See `exploration/concept_explorer/README.md`. The `explorer-merge` work item was archived 2026-04-11.

## Paused / Deferred

- **`traceability-system`** — Spec + plan written, on hold awaiting prioritization.
- **`loop-dry-run-symmetry`** — Spec only (2026-04-10). Small follow-up from pipeline-hardening audit. LOW complexity.

---

## Recently Completed

### [2026-04-11] Pipeline Hardening, Explorer Merge, Source Cleanup

Archived 7 items + cleaned up 2 superseded/orphan dirs. See `.project/completed/CHANGELOG.md` for details.

Key outcomes:
- Analysis pipeline hardened against silent corruption, transient API errors, and validation gaps (`pipeline-hardening`, `output-validation-retry`)
- Feedback routing now reaches model-setup agent directly instead of via analysis prose (`feedback-routing-fix`)
- Cross-concept landscape context injected into analysis prompts (`concept-landscape-context`)
- 21 NO-verdict `.orig.md` files re-sourced against real HTML (`orig-md-research`)
- `ralph/concept-explorer` merged into `design-space-explore` (`explorer-merge`)
- `source-replacement` closed out
- Deleted: `extraction-interface-gap/` (empty orphan), `step-runner-validation-retry/` (superseded by pipeline-hardening Phase 5)
- Also picked up a lingering prior-session archival of `common-output-interface/` (staged to `completed/20260407_*` but never committed)

### [2026-04-05] Analysis Pipeline Bulk Archival

Archived 13 completed items. See `.project/completed/CHANGELOG.md` for full details.

### [2026-03-29] Concept Taxonomy & Interactive Explorer
4 work items archived (2 complete, 2 superseded).

### [2026-03-06] Project Cleanup

Archived 9 active items and 4 epics.

---

## Up Next

1. Knock out `loop-dry-run-symmetry` (small, well-scoped)
2. Kick off `batch-pipeline-run` on all concepts
3. Traceability system implementation (when prioritized)
