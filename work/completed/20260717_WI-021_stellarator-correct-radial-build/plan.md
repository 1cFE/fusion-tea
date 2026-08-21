---
Status: complete
Created: 2026-07-17
Updated: '2026-07-17'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-021 Plan: Stellarator-Correct Radial-Build Volumes

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. Radial-build formulas from 1costingFE @ `0254385` (admissible lineage exception, §3).

Owner ruling (2026-07-17): **Option 1** (torus shells, no material shape factor — six values unchanged); yes to wall_area, r_coil, special_materials rebind; Option 2 deferred to the epic; proceed on the uncommitted WI-020 base.

**Central closure risk (design D5):** the handshake injects 1costingFE's material volumes directly; making them computed removes those injection points. Phase 5 must verify `rb` reproduces 1cfe's `geo` values and that SV-025/026 stay byte-identical, with the D5 fallback ready.

## Phase 1 — Library: `'MFE Radial Build'` calc def

- [x] Add the `'MFE Radial Build'` calc def to `models/library/analyses/mfe_plasma_scaling.sysml` (full def in design.md "Proposed Design"): 15 inputs (R, a, kappa, pi-default, 11 thicknesses), cumulative-radii + torus-coefficient + per-layer intermediates, 6 outputs (blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil).
- [x] `diff` the analyses file canonical vs staged (`exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml`) to confirm byte-identity, then apply the identical edit to the staged copy.
- [x] Validate L1 (0 errors) on canonical `models/`. Watch `**`/precedence and name resolution across the ~13 intermediates.

## Phase 2 — Generic plant: thickness attrs + `rb` block + output wiring

- [x] `models/designs/generic_mfe/mfe_plant.sysml`: add 11 `attribute <layer>_t : Real default <RadialBuild default>;` (vacuum_t 0.10, firstwall_t 0.05, blanket_t 0.70, reflector_t 0.20, ht_shield_t 0.20, structure_t 0.15, gap1_t 0.10, vessel_t 0.10, coil_t 0.30, gap2_t 0.10, lt_shield_t 0.15 — cite geometry.py:19-40).
- [x] Add `calc rb : 'MFE Radial Build' { in R = R; in a = a; in kappa = kappa; in <each>_t = <each>_t; }` next to the `geom` block.
- [x] Wire outputs into the parts (sibling-calc pattern): `part blanket { … :>> blanket_vol = rb.blanket_vol; }` and likewise shield/structure/vessel; `part magnet { … :>> r_coil = rb.r_coil; }`.
- [x] Mirror into the staged plant copy.
- [x] Validate L1.

## Phase 3 — Instance: bind thicknesses, wire wall_area, rebind special_materials, delete constants

- [x] `models/designs/stellarator_09/stellarator_plant.sysml`: bind all 11 thicknesses near the geometry inputs (~277), each cited — blanket_t=0.80/ht_shield_t=0.20/structure_t=0.15/vessel_t=0.10 → `steady_state_stellarator.yaml:39-42`; the other 7 → `RadialBuild` defaults `geometry.py:19-40`.
- [x] `wall_area`: change `attribute wall_area : Real = 802.201;` (line ~507) to `= rb.wall_area;`; rewrite the doc to the forward computation (drop the "802.201 constant" wording).
- [x] Rebind `special_materials_capital` (line ~445): `:>> special_materials_capital = blanket.blanket_vol * 0.50 * 9400.0 * 5.0;`; update the doc (now computed from blanket_vol; value ≈ 26.289 M$ unchanged). If codegen rejects the expression (D6), fall back to the literal with the derivation kept in the doc.
- [x] **Delete** the six injected constants: `blanket_vol` (145), `shield_vol` (158), `structure_vol` (169), `vessel_vol` (180), `r_coil` (117); rewrite each part's doc comment to describe the rb forward computation instead of the copied value. (`wall_area` handled above.)
- [x] Mirror into the staged instance copy.
- [x] Validate L1–L6 on canonical `models/`; compare to the WI-020 baseline (L1=0, L2=3, L6=105) — expect zero new issues.

## Phase 4 — Oracle, regen, runner

- [x] `verify_stellaris.py`: replace the six geometry constants in `IN` with the rb computation (cumulative radii → torus-shell volumes → wall_area/r_coil), mirroring the calc def. Add the 11 thicknesses.
- [x] Regenerate: `sysml-codegen snapshot` over the staged models → `bridge_v11_generate.py` (env from `~/1cfe/fusion-tea/.env`). Confirm no new rollup offenders beyond the known 3.
- [x] `run_stellaris.py`: headline unchanged under Option 1 — re-confirm the existing asserts pass (V 448, p_fus 2144.5, net 578.0, LCOE 247.34, total $9.683B). Update only if a value moves (it shouldn't).
- [x] Run `run_stellaris.py` — bit-exact vs the updated oracle; **verify the six geometry outputs = the pre-item-1 constants** (1118.695 / 552.140 / 219.979 / 157.933 / 802.201 / 3.20).

## Phase 5 — Handshake (closure proof)

- [x] **Verify `rb` reproduces 1cfe `geo`** (D5 precondition): confirm the generated `rb` outputs equal the handshake's `geo["blanket_vol"]`/`shield_vol`/`structure_vol`/`vessel_vol`/`r_coil_vessel_or` before removing injections. If any differs → surface it (real geometry inconsistency), do not absorb.
- [x] Remove the 5 direct injections in `handshake_1costingfe.py` (`blanket__blanket_vol`, `shield__shield_vol`, `structure__structure_vol`, `vessel__vessel_vol`, `magnet__r_coil` — lines ~232/238/242/248/261). Confirm the `geom__a=1.8` override does not leak into `rb` (per-calc params: `rb__a` stays 1.5).
- [x] Re-run `handshake_1costingfe.py`; confirm SV-025 (six power channels) and SV-026 (power-scaled account gap) **numerically unchanged** vs the WI-020 result. If closure breaks, apply the D5 fallback (inject `rb__*` inputs = 1cfe's radial build).
- [x] IFE regression: re-run SV-023 anchors (no IFE files touched) — still passing.
- [x] Confirm all three viability asserts (beta, wall load, TBR) pass (wall_load unchanged).

## Phase 6 — Close

- [x] `pm update-validation SV-028 --status passing`.
- [x] Record the (unchanged) headline + the six now-forward-computed values in this plan's Implementation Record and `.project/CURRENT_WORK.md`; note the six-constants fidelity gap closed and Option 2 deferred in the epic.
- [x] `pm close-item WI-021`.

## Implementation Record

**Completed 2026-07-17.** All six phases landed; SV-028 passing. Option 1 (torus shells, no material shape factor) — the six geometry values are unchanged; the headline is unchanged. Fidelity/traceability win: six injected constants → forward-computed arithmetic.

**Model change:**
- `mfe_plasma_scaling.sysml`: new `'MFE Radial Build'` calc def — 15 inputs (R, a, kappa, pi-default, 11 thicknesses), ~13 intermediate `attribute` locals (cumulative radii, torus coefficient C, per-layer volumes), 6 outputs (blanket/shield/structure/vessel volumes, wall_area, r_coil). Uses the multi-output/intermediate pattern proven by WI-019's `'MFE Power Balance Calc'`; compiled `fully_compilable`.
- `mfe_plant.sysml`: 11 thickness attributes (RadialBuild defaults) + `calc rb` block; the four cost calcs and the magnet cost read `rb.<vol>` / `rb.r_coil` **directly** (the `in V = geom.V` idiom) — see codegen note below; part attributes also mirror rb (`:>> blanket_vol = rb.blanket_vol` etc.) for the costed-component structure.
- `stellarator_09/stellarator_plant.sysml`: 11 thicknesses bound explicitly with citations (4 → steady_state_stellarator.yaml, 7 → RadialBuild defaults); `wall_area` bound directly into `wall_load_calc` as `rb.wall_area` (dropped the standalone top-level attribute — see L6 note); `special_materials_capital` rebound to `rb.blanket_vol * 0.50 * 9400 * 5.0`; the six injected constants deleted; six doc comments rewritten to the forward computation.
- Staged e2e copies mirrored (analyses file byte-identical; plant/instance carry the pre-existing codegen adaptations).

**Two codegen findings (design D3/D5 realized):**
1. **L6 / V11 offender on `wall_area`.** A top-level design attribute with a derived expression referencing a calc (`attribute wall_area = rb.wall_area`) is an L6 "derived-expression-references-design-attributes" offender (the same class the V11 bridge chokes on). Fixed by binding `rb.wall_area` directly into `wall_load_calc` (the `in V = geom.V` idiom) and dropping the standalone attribute — forward-computed everywhere, zero new L6 offenders.
2. **V11 bridge abort on the cost-calc volume inputs.** Reading `blanket.blanket_vol` (a now-derived cross-part attribute) leaves `blanket_cost__blanket_vol` uncovered → V11 abort. Fixed by wiring the cost calcs to read `rb.<vol>` directly (sibling-calc output, V11-coverable). After the fix, only the 3 pre-existing rollup closures are bridged (same as WI-020).

**Handshake (D5 fallback — the notable result):** the handshake's Anchor A is 1costingFE's OWN reference reactor at **R0=5.5** (not the Stellaris R0=12.7), and it injected 1cfe's material volumes directly as leaf params. Those params vanish once the volumes are computed, so closure required the D5 fallback: the emitter (`emit_1cfe_point.py`) now emits 1cfe's radial-build inputs, and the handshake feeds them into `rb__*` (separate params from `geom__*`, so the `geom__a=1.8` plasma-path override does not leak). Verified `rb` reproduces 1cfe's geo exactly (blanket 884.59, shield 419.06, structure 168.06, vessel 119.86, r_coil 3.50, wall_area 660.08). The 5 direct volume/r_coil injections were removed. **This makes the handshake stronger** — it now exercises the SysML radial-build math against `compute_geometry`, not just volume pass-through.

**Validation:**
- L1 = 0; L2 = 2 (pre-existing IFE); L6 = 5 errors (3 pre-existing MFE rollups + 2 pre-existing IFE) — **zero new offenders** from WI-021.
- Codegen: snapshot + V11 bridge regenerated; `MFE_Radial_Build` compiled fully_compilable; 3 known rollup closures bridged, no new offenders.
- `run_stellaris.py`: **ALL CHECKS PASSED** — every physics channel, per-account cost, rollup, and LCOE bit-exact vs the updated oracle at rel 1e-9; the six geometry outputs reproduce the pre-item-1 constants (1118.695 / 552.140 / 219.979 / 157.933 / 802.201 / 3.20); WI-020 headline reproduced.
- **Handshake closure**: SV-025 six power channels +0.000%, SV-026 accounts +0.00% end-to-end, worst formula-isolation structure −7.63e-08 — **byte-identical to the WI-020 result**. The −30.87% LCOE / −41.9% total remain the documented structural gaps (unmodeled CAS tail), unchanged.
- IFE regression SV-023: no IFE/HIF files touched → unaffected by construction.
- Viability: wall_load 2.14 < 4.95 (computed wall_area 802.201), beta 0.0276 < 0.05, TBR 1.074 > 1.05 — all pass, unchanged.

**Headline (unchanged, Option 1):** V 448 m³, p_fus 2144.5 MW, net 578.0 MW, q_eng 3.16, total **$9,683,350,944** (was $9,683,350,490 — +$454 from the special_materials refinement, invisible at $9.68B), **LCOE $247.34/MWh**, magnet $4.392B (45.4%). The only numeric movement is `special_materials` 26,289,000 → 26,289,332.

**Deviation from design:** `wall_area` bound directly into `wall_load_calc` rather than kept as a standalone instance attribute (D3 assumed a design attribute; the L6/V11 offender forced the cleaner `in V = geom.V` idiom). Cost calcs read `rb.<vol>` directly (design left the exact binding to implement). Both are within the design's codegen-envelope intent.

**Surfaced (owner attention):**
1. SV-016 band ("Q_eng ~10–40") still reads low at q_eng 3.16 — carried open from WI-019/020, unaffected by item 1.
2. Option 2 (material shape factor) recorded as deferred in the epic — revisit if a sourced conformal-volume basis appears.
3. Next: item 2 (predictive confinement).
