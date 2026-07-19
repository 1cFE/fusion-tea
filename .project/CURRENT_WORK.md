# Current Work

**Last Updated**: 2026-07-18

---

## Active Work

### Stellarator MBSE Demo — demo epic written; tracking recovered to the concept's frame (2026-07-18)

**Status**: The demo now has a tracking home: **`.project/backlog/epic_stellarator_mbse_demo.md`** (Ready — epic home and the criterion-3 bar owner-ratified 2026-07-18: coding PM is the home base, modeling items created in `work/`; the Anchor-A bar is *explaining* remaining discrepancies and closing any errors, not closing the full gap). The governing frame is `.project/concepts/stellarator-mbse-demo.md` — every demo done-ness assessment runs against its 8 criteria, not any other epic's items. Criterion status mapped honestly: 1 done (model end-to-end, WI-025 headline), 3 partial (Anchor A — tolerance spec never written, −31% structural gap via injected values), 2 not met (constraints don't execute in the pipeline), 4–7 not started, 8 stretch. 9 items decomposed (~10–14d): anchor acceptance spec → account scopes (CAS22 tail, LCOE construction) ∥ constraint execution → studies → visualization → owner-triggered reveal/comparison → write-up. The MFE epic's Next Action now points here for demo work; it keeps only its own non-demo residuals (tokamak — a demo Non-Goal, sweep, WI-009/010/018 disposition rulings). Verified along the way: the upstream constraint-execution epic **completed 2026-07-13** (IFE acceptance 2294/2301 in this repo) — Stage 4's gate is now the P0 PR-wave remediation churn + CE-F1/F2, handled by per-item commit pinning, not a missing capability.

**Next**: Item 1 (anchor acceptance spec — smallest item, three others judged against it); Item 2 (constraint execution) can start in parallel.

### Stellarator MBSE Demo — WI-025 STALE-BASIS pass-through recompute DONE: audited PASS, closed, committed (2026-07-18, `7ba3cd70`)

**Status**: WI-025 complete — implemented, audit PASS (`work/analysis/20260718-220847_audit_WI-025_stale-basis-recompute.md`), owner-closed (`work/completed/20260718_WI-025_stale-basis-pass-through-recompute/`), committed at `7ba3cd70`. PROTOCOL.md respected throughout; orchestration brief at `work/orchestration/stale-basis-recompute.md`.

**What moved**: the last three pass-through cost accounts are now **forward-computed functions of the model's computed powers**, and all three STALE BASIS annotations are retired (grep-zero). Three new library calc defs in `models/library/analyses/mfe_account_costs.sysml` — `'Buildings Cost'` (CAS21, exact 6-term grouped collapse of the 1cfe 18-building DT loop, tracking p_fus/p_the/p_th/p_et), `'Preconstruction Cost'` (CAS10 pre-contingency subtotal, tracking p_net), `'Annual OM Cost'` (CAS70 unlevelized, tracking p_net) — wired in the generic plant (8 concept-input attributes + 3 calc usages) and bound by the Stellaris instance (all $-conversions of pinned 1costingFE constants; DT/FOAK/n_mod = 1 frozen as documented constants). Conventions preserved: CAS10 pre-contingency (CAS29 applies once), CAS21 raw, CAS70 unlevelized (CAS71/72 remain Stage-3).

**Executed headline (bit-exact vs oracle rel 1e-9, incl. the three new account channels)**: CAS21 **$640,475,006.17** (was $613.65M at pre-WI-019 powers), CAS10 **$34,391,496.77** (was $33.896M at p_net 575.3), CAS70 **$52,517,269.06/yr** (was $41.641M/yr) → direct $9,247,944,633.47, total **$12,638,857,665.74** (+0.296%), **LCOE $203.647152/MWh** (+$2.1751). Denominator invariant: p_net 915.081088, q_eng 6.606662, rec_frac 0.151362, magnet $6,323,469,946.33 (50.03%) — all unchanged to the cent. SV-032 passing with the executed record; handshake byte-identical under the standing successor bar (injection-map-only edit — om_ref zeroed, 1cfe annual O&M via the om_direct identity path); IFE anchors unchanged; pytest tally unchanged (11/18/14/0); L1–L6 offender list = the 6 pre-existing (mfe_plant lines shifted only); WI-022 handwritten impl content-hash survived regen.

**Next**: done — audited, closed, committed. SV-016 still `pending` (q_eng did not move this item); demo work continues from the demo epic (top entry).

### Stellarator MBSE Demo — WI-024 recirculating-power derivation IMPLEMENTED (2026-07-18, uncommitted — awaiting audit → owner close → commit)

**Status**: WI-024 implemented and validated (`work/active/WI-024_recirc-power-derivation/` — plan Implementation Record filled). NOT closed, NOTHING committed (owner-held / orchestrator-held). PROTOCOL.md respected throughout; orchestration brief at `work/orchestration/recirc-power-derivation.md`.

**What moved**: p_cryo is now a **computed chain output**, not a bound constant. New library calc def `'Cryoplant Electrical Power'` (`models/library/analyses/mfe_cryo_plant.sysml`): winding-pack nuclear heating 35.5 W/m³ (Table 6 image) × 136.56 m³ winding volume (COMPUTED — Table 8 cross-sections × 8-fold symmetry × 25 m circumference) + 7.5 kW joint losses (§2.9), at 20 K through a 0.20-of-Carnot cryoplant (THE assumption, design D4; T_amb 300 K assumption; f_uplift 1.0 explicit lower-bound seam, D6) → **p_cryo = 0.8643516 MW** wall-plug. The 1cfe generic default 0.8 retired (D2, double-counting resolution); p_tf rescoped from deferral stopgap to **modeled zero** (SC coils, 1cfe's own `recirc_power_factor = 0`); p_tfcool 15.0 kept with a documented disjoint reading.

**Executed headline (bit-exact vs oracle rel 1e-9, incl. the new derived-p_cryo channel)**: p_net **915.081 MW**, rec_frac **0.151362**, q_eng **6.6067**, **LCOE $201.472/MWh**; V 425 / p_fus 2748.1 / p_th 3238.1 / gross 1078.3 unchanged; total **$12,601,519,645.07** and magnet **$6,323,469,946.33 (50.2%)** unchanged to the cent. SV-031 passing with executed values; handshake byte-identical under the Ruling-3 successor bar (injection-map edit only, `handshake_comparison.json` diff empty); IFE anchors unchanged; L1–L6 offender list = the 6 pre-existing, zero new; WI-022 handwritten impl content-hash survived regen.

**Flagged for owner**: SV-016 stays `pending` — q_eng 6.609 → 6.6067 at the derived parasitic power, still below the ~10–40 band; the derived value is a documented lower bound (unprinted cryo loads excluded, f_uplift seam). Band untouched per MR-WI024-6.

**Next**: `/audit-models` → owner `pm close-item WI-024` → commit; then the STALE-BASIS pass-through recompute (sequenced after WI-024 per the owner's Option B ruling — recompute at the settled p_net 915.081; register at pick-up).

### Stellarator MBSE Demo — WI-023 magnet-field errata DONE: audited, closed, committed (2026-07-18, `adc43cda`)

**Status**: WI-023 complete — implemented, independent audit **POSITIVE** (report: `work/analysis/20260718-105435_audit_WI-023_magnet-field-errata-B9.md`), owner-closed (`work/completed/20260718_WI-023_magnet-field-errata-B9/`), committed at `adc43cda`. PROTOCOL.md respected throughout; orchestration brief at `work/orchestration/magnet-field-errata-B9.md`.

**What moved**: two phantom-row corrections in the concept-09 instance, owner-ratified. `magnet.B` 5.86 → **9.0 T** (the 5.86 cited a Table 3 text row that does not exist — the Table 2/5 images and the published paper print axis-averaged B₀ = 9.0; magnet cost is linear in B). `pb.p_tf` 111 → **0.0** (the "conduction power to coils = 111 MW" row does not exist; 111 is the stored magnetic energy in GJ; the paper defers parasitic electricity — no-fallbacks, [OWNER] option b). The published Stellaris PDF was found in the repo (admissible iter-02 companion dir) and confirms both phantoms outright; registered in `SOURCE_INDEX.md`.

**Executed headline (audit-reproduced, bit-exact vs oracle rel 1e-9)**: V 425, p_fus 2748.1 MW, p_th 3238.1, gross 1078.3, **net 915.1 MW**, rec_frac 0.151, **q_eng 6.61**, total **$12.6015B**, **LCOE $201.46/MWh**, magnet **$6.3235B (50.2%)** — magnet exactly ×9.0/5.86 on the WI-022 baseline. SV-030 passing; SV-025/026 handshake byte-identical; IFE SV-023 unchanged; zero new validation offenders; WI-022 handwritten reactivity impl survived regen.

**Owner rulings at close (2026-07-18)**: **SV-016** (Q_eng ~10–40 band) stays `pending` until WI-024 — q_eng 6.61 is knowingly optimistic at p_tf = 0, so the band is not adjusted to fit a provisional value. **Sequencing: WI-024 (recirculating-power derivation model) runs BEFORE the STALE-BASIS pass-through recompute** (Option B — recompute at a settled p_net; the pass-throughs are now ~59% off their p_net = 575.3 basis). Both recorded in `work/backlog/epic-mfe-cost-modeling.md` (WI-024 entry + Deferred Decisions).

**Next**: WI-024 (`/spec-model` + owner checkpoint) → STALE-BASIS pass-through recompute (register at pick-up) → structural handshake-gap account items (−31%) → hold-out comparison stage (owner-triggered ARIES-CS reveal, PROTOCOL §6).

### Stellarator MBSE Demo — Stage 3 item 2 DONE: WI-022 predictive confinement (2026-07-18, uncommitted)

**Status**: WI-022 implemented, validated, handshake-verified, closed — uncommitted in the worktree, stacked on `7f0b19ea` (which committed WI-019/020/021; the "uncommitted" notes on the entries below are stale). Last demo-deepening item (order 3→4→1→2) — the demo model is now complete pending the account-scope / hold-out stages. PROTOCOL.md respected throughout.

**The headline story**: the 2144-vs-2700 "0D gap" is **closed as sourced physics, no tuning**. Fusion power is now computed by integrating the Bosch-Hale reactivity over the Stellaris source's own profiles — n(ρ)=n₀(1−ρ²)^0.33, T(ρ)=T₀(1−ρ²)^1.19, peak fuel 1.96e20/side, T_i0 14.63 keV, every parameter fixed from the source's Fig. 16 panels and printed tables **blind to the power** — giving **2748.1 MW, +1.8% vs the 2700 MW design point**. The physics executes at the **handwritten codegen stage** (first Rung-B item: SysML calc routed manual_required via a transcendental; `preserve_handwritten=True`; oracle mirrors the integral exactly, runner asserts rel 1e-9).

**Extraction-errata sweep (the session's second story)**: image-verifying the tables exposed that the text extraction's Tables 2/3/4/5 are corrupted reconstructions (garbled AND invented rows). Owner-ratified fold-in: **a = 1.3** (was 1.5 — artifact), **V = 425** (was 448 — artifact; the WI-020 f_shape 0.7943 reconciled two artifacts, now 1.0031567 ≈ true ~0.3% QI shaping), **n_e = 3.17e20** (was 3.37), **wall_load_limit = 4.05** (the "4.95" was a phantom row), T_i0 14.63 (doc said 24.6). The extracted Fig.-16 caption exponents (α_n=1.2, α_T=3.0) were refuted by digitizing the figure itself (would give 1165 MW). **WI-023 queued**: magnet B = 5.86 T cites a phantom Table-3 row; the images print axis-averaged 9.0 T (magnet = 43% of capital). **Parked for owner**: p_tf = 111 MW also cites a phantom row (111 is the stored magnetic energy in GJ).

**Re-baselined headline (executed, bit-exact vs oracle)**: V 425, **p_fus 2748.1 MW**, p_th 3238, gross 1078, **net 804.1 MW**, rec_frac 0.254, q_eng 3.93, total **$9.586B**, **LCOE $176.07/MWh**, magnet **$4.117B (42.9%)**. SV-029 passing; **SV-025/026 handshake byte-identical** (sigma_v>0 bypass = exact legacy 0D path, zero handshake edits); IFE SV-023 unchanged; L1=0, zero new L2/L6 offenders; viability passes (wall load 3.13 < 4.05). SV-016 band still reads low (q_eng 3.93 vs "~10–40") — awaiting owner adjust/annotate. Record: `work/completed/` WI-022 (spec/design/plan + `prototype/` digitization evidence).

### Stellarator MBSE Demo — first item implemented (aries-cs-holdout)

**Status**: `aries-cs-holdout` implemented and committed (`8939d9dc` + ratification follow-up), pending `/_my_audit`. Quarantine live at `knowledge/holdout/aries-cs/` (4 PDFs + manifest + README + PROTOCOL.md, plus one CLAUDE.md line); all leak-surface verifications passed. Owner ratified (2026-07-13) the two ingestion-time barred-list additions (the `knowledge/sources` Helios extraction and a concept-36 ARIES-CS stub). Note: ARIES mirrors are all dead — PDFs came from Wayback snapshots of the canonical URLs, recorded in PROTOCOL §7. Concept at `.project/concepts/stellarator-mbse-demo.md`. On branch `feat/stellarator-mbse-demo`.

### Stellarator MBSE Demo — Stage 3 item 1 DONE: WI-021 stellarator-correct radial build (2026-07-17, uncommitted)

**Status**: WI-021 implemented, validated, handshake-verified, closed — **uncommitted in the worktree** (stacked on the uncommitted WI-020), pending review/commit. Spec → owner checkpoint → design → plan → implement, same-day. PROTOCOL.md respected; radial-build formulas from 1costingFE @ `0254385` (admissible ARIES/Starfire-lineage exception, §3); R/a/kappa from the Stellaris source.

**What changed**: the six injected geometry constants (blanket/shield/structure/vessel volumes, first-wall area, coil-bore radius) are replaced by a new `'MFE Radial Build'` calc that forward-computes them from the radial-build layer thicknesses (cumulative radii → torus-shell volumes → torus surface area), reproducing `costingfe.geometry.compute_geometry(STELLARATOR)`. **Owner ruled Option 1** (pure torus shells, no material shape factor — matches 1costingFE); Option 2 (shaping the material volumes) deferred to the epic. `special_materials_capital` (CAS27) rebound to the computed blanket_vol.

**Results**: **SV-028 passing** — the six values reproduce the pre-item-1 constants (1118.695 / 552.140 / 219.979 / 157.933 / 802.201 / 3.20), generated pipeline bit-exact vs oracle at 1e-9. **Headline unchanged** (fidelity/traceability win, not a re-baseline): V 448, p_fus 2144.5, net 578.0 MW, q_eng 3.16, total $9.683B, LCOE $247.34/MWh, magnet $4.39B (45.4%). Only numeric movement: `special_materials` 26,289,000 → 26,289,332 (+$332, from the rebind; invisible at headline precision). Viability all pass (wall_load 2.14 < 4.95).

**Handshake (notable)**: the closure test's Anchor A is 1costingFE's OWN reference reactor at R0=5.5 (not Stellaris R0=12.7) and it injected 1cfe's material volumes directly — those params vanish once volumes are computed. Closed via the emitter now exposing 1cfe's radial-build inputs, fed into `rb__*` (separate params from `geom__*`, so the plasma-path override doesn't leak); verified `rb` reproduces 1cfe's geo exactly. **SV-025/026 byte-identical to WI-020** (worst formula-isolation −7.63e-08). The handshake is now *stronger* — it exercises the rb math vs `compute_geometry`. Two codegen offenders fixed along the way (wall_area as a top-level derived attr → bound into wall_load_calc; cost calcs read `rb.<vol>` directly instead of the cross-part part attribute). L1=0, zero new L2/L6 offenders. No IFE files touched (SV-023 unaffected).

**Next**: item 2 (predictive confinement) per the 3→4→1→2 order. Record: `work/completed/20260717_WI-021_stellarator-correct-radial-build/` (spec/design/plan).

### Stellarator MBSE Demo — Stage 3 item 4 DONE: WI-020 stellarator-correct geometry (2026-07-17, uncommitted)

**Status**: WI-020 implemented, validated, handshake-verified, closed — **uncommitted in the worktree**, pending review/commit. Spec → owner checkpoint → design → plan → implement, same-day. PROTOCOL.md respected; geometry sourced from the admissible Stellaris source, engineering from 1costingFE @ `0254385`.

**Owner ruling at checkpoint (2026-07-17)**: Decision B = **B1** (target the Table-2 plasma volume 448 m³ at the model's R=12.7 → shape factor 0.7943). Decision A = **do NOT re-solve sigma_v** — "make sure the model is accurate. We can test various inputs at the codegen phase." So fusion power is a computed output, not pinned.

**What changed**: `'Plasma Geometry'` gained a shape/packing factor `f_shape` (default 1.0 = pure torus); the Stellaris instance binds `f_shape = 0.794259`, correcting plasma volume from the torus over-prediction 564 m³ to the source's 448 m³. sigma_v unchanged, so fusion power falls to a computed **2144.5 MW** (was pinned 2700), re-baselining the headline. Also deleted the prior cross-check note that mis-diagnosed the gap as "R/a rounding" (arithmetically wrong: torus at R=12,a=1.5 = 533, not 448); rewrote the sigma_v doc to make the 2145-vs-2700 gap visible (the 0D single-temperature limitation, target of item 2).

**Results**: **SV-027 passing** — V = 448.0 m³, pipeline bit-exact vs oracle at 1e-9. **New Stellaris headline: p_fus 2144.5, net 578.0 MW, q_eng 3.16, total $9.68B, LCOE $247.34/MWh, magnet $4.39B (45.4%, unchanged — power-independent).** Net electric and LCOE land near the pre-WI-019 range: WI-019's power-balance gain and this volume correction nearly cancel. All viability constraints pass (wall load 2.14 < 4.95). The old 2700 MW / $189 headline is exactly recoverable at sigma_v = 7.535e-23 (sensitivity table in the plan) — a visible input choice, not baked in.

**Handshake**: the closure test caught a real bug first — the generated params carry the instance's f_shape=0.7943, so the handshake's 1cfe torus point was shrunk 20%. Fixed by explicitly injecting `geom__f_shape = 1.0` in `handshake_1costingfe.py`. Re-run: SV-025/026 **byte-identical to WI-019** — the structural −31% LCOE gap is unchanged (item 4 doesn't touch it). IFE regression SV-023 unchanged. L1=0, L2=3, L6=105 (WI-019 baseline; zero new issues).

**Surfaced (owner attention)**:
1. **SV-016** "Q_eng ~10–40" band reads low at q_eng 3.16 (carried open from WI-019; still `pending`). Needs owner adjust/annotate.
2. STALE-BASIS pass-throughs are now nearly back on their 575.3 basis (p_net 578); annotations updated, recomputation still a Stage-3 account item.
3. The 2145-vs-2700 fusion-power gap is now visible in the model — item 2 (predictive confinement) is where it closes.

**Next**: owner review + commit; then demo item 1 (radial-build volumes) per the approved 3→4→1→2 order. Record: `work/active/WI-020_stellarator-correct-geometry/` (spec/design/plan).

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
