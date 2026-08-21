---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-022 Plan: Predictive Confinement — Profile-Integrated D-T Reactivity

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read.

Owner rulings: Rung-B handwritten-stage approach (2026-07-17); Option-1 anchor-derived referents + errata fold-in (a = 1.3, V ≈ 425) + WI-023 for magnet B (2026-07-18). Decision A honest-physics; Decision B bypass/flat handshake closure; Decision C resolved referents (spec).

Note (WI-020 lesson): generated params bake *instance* bindings — the handshake must inject every value whose 1cfe reference differs. Existing injections already cover this item: `fusion__sigma_v` (> 0 → bypass), `fusion__n_e`, `geom__a`, `geom__f_shape = 1.0`. The handshake's internal `n_e = 3.37e20` is a self-consistent back-solve pair with its computed sigma_v (not a Stellaris citation) — untouched.

## Phase 1 — Library: profile-integrated `'DT Fusion Power'`

- [x] `diff` canonical vs staged `mfe_plasma_scaling.sysml` — confirm byte-identity before editing.
- [x] Edit `'DT Fusion Power'` per design D4/D5: 5 profile inputs (`n_D0`, `n_T0` default 0.0; `T_i0` default 1.0; `alpha_n`, `alpha_T` default 0.0), `sigma_v` gains `default 0.0`, Bosch-Hale intermediates (`theta`, `xi`, `sigv_peak` — e-power form, `RealFunctions::sqrt` routing trigger), `p_fus` peak-form expression, normative doc (mode rule, integral contract, discretization, citations).
- [x] Mirror identically into the staged copy.
- [x] Validate L1 (0 errors) on canonical `models/`.

## Phase 2 — Plant: thread the profile inputs

- [x] `mfe_plant.sysml`: 5 plant attributes (defaults mirroring the calc def), bindings in the `fusion` block; `sigma_v` attribute gains `default 0.0`.
- [x] Mirror into the staged plant copy (shared regions only — staged carries codegen adaptations).
- [x] Validate L1.

## Phase 3 — Instance: referent bindings + errata rebind + doc rewrites

- [x] Geometry (MR-WI022-8): `:>> a = 1.3` (Table 2 image cite); `:>> f_shape = 1.0031566` (V = 425, Table 5 image cite); rewrite the WI-020 shaping note (delete the empirical-0.7943 framing; record the amended owner ruling 2026-07-18 and the ≈0.3% residual shaping meaning).
- [x] Fusion: `:>> sigma_v = 0.0` + MAPPING-TRAP/doc rewrite (MR-WI022-3 — 0D limitation closed by this item; garbled-text history compressed); bind `n_D0 = 1.96e20`, `n_T0 = 1.96e20`, `T_i0 = 14.63`, `alpha_n = 0.33`, `alpha_T = 1.19` with image/digitization citations (MR-WI022-2).
- [x] Corrections: `:>> n_e = 3.17e20` (Table 5 image; doc: handshake/reference-only in profile mode); `wall_load_limit = 4.05` (Table 2 image); re-point the `mfe_viability.sysml` 4.95 doc reference.
- [x] Refresh the instance headline doc block to the expected re-baselined values (final numbers from Phase 5 execution).
- [x] Mirror into the staged instance copy (shared regions).
- [x] Validate L1–L6 on canonical `models/`; compare to the WI-021 baseline (L1 = 0; L2 = 2 pre-existing IFE; L6 = 5 pre-existing) — zero new offenders.

## Phase 4 — Codegen: manual_required routing + handwritten impl

- [x] `bridge_v11_generate.py`: add `preserve_handwritten=True` to `GenerationConfig` (MR-WI022-4).
- [x] Regenerate: snapshot over staged models → V11 bridge. Verify: `'DT Fusion Power'` routed `manual_required`; package emits; V11 offenders stay exactly 3; `IMPLEMENTATION_BACKLOG.md` lists the one handwritten function.
- [x] Fill `handwritten/.../dt_fusion_power_impl.py` with the design-D3 impl (bypass branch + trapezoid integral, N = 200,000, T-floor 1e-6, pure-Python `math`), adopting the generated stub's exact signature.
- [x] Regen **again**; confirm the filled impl survives (MR-WI022-4 acceptance).

## Phase 5 — Oracle, runner, execution

- [x] `verify_stellaris.py`: mirror `_sigv_dt` + the identical integral (same op order); update IN params (`a = 1.3`, `f_shape = 1.0031566`, `n_e = 3.17e20`, `sigma_v = 0.0`, profile set).
- [x] `run_stellaris.py`: update headline asserts — V 448 → 425 (tol 2), p_fus 2144.5 → computed (≈2748), cascaded p_th / p_net / q_eng / rec_frac / total / LCOE to executed values; magnet capital moves (coil bore from a = 1.3) — record it.
- [x] Run `run_stellaris.py` — bit-exact vs oracle at rel 1e-9 on every channel/account/LCOE; record the full re-baselined headline and the residual vs 2700.

## Phase 6 — Handshake (closure proof) + regressions

- [x] Re-run `handshake_1costingfe.py` — **zero edits to the script**; SV-025 six power channels and SV-026 account gap byte-identical to the WI-021 records (D2 closure proof: injected `fusion__sigma_v > 0` takes the exact bypass path).
- [x] IFE regression SV-023 (no IFE files touched) — unchanged.
- [x] Viability asserts: beta_ok (0.0276 < 0.05), wall_load_ok (≈3.1 < 4.05), tbr_ok — all pass at re-baselined power.

## Phase 7 — Close

- [x] `pm update-validation SV-029 --status passing`; VALIDATION_MATRIX entry updated with executed values.
- [x] Update STALE-BASIS annotations to the new p_net.
- [x] Record headline + residual-vs-2700 + errata disposition in this plan's Implementation Record and `.project/CURRENT_WORK.md`; flag SV-016 (q_eng moves again) for owner adjust/annotate; note WI-023 (magnet B = 9.0) queued.
- [x] `pm close-item WI-022`.

## Implementation Record

**Completed 2026-07-18.** All seven phases landed; SV-029 passing.

**Model change (as designed):**
- `'DT Fusion Power'` (`mfe_plasma_scaling.sysml`) gained 5 profile inputs (n_D0, n_T0, T_i0 default 1.0, alpha_n, alpha_T), a `default 0.0` on `sigma_v` (bypass sentinel), and the model-resident Bosch-Hale intermediates (theta/xi/sigv_peak; e^x as `2.718281828459045 ** x` — the stdlib has `sqrt` but no `exp`; the `RealFunctions::sqrt` invocation is the manual_required routing trigger, spike-proven).
- `mfe_plant.sysml`: 5 plant attributes threaded into the `fusion` block; `sigma_v` defaulted 0.0.
- Instance: profile referents bound (n_D0 = n_T0 = 1.96e20, T_i0 = 14.63, alpha_n = 0.33, alpha_T = 1.19, all image/digitization-cited); errata rebind a = 1.3, f_shape = 1.0031567 (V = 425.000 exactly), n_e = 3.17e20, wall_load_limit = 4.05; sigma_v = 0.0 with the MAPPING-TRAP doc rewritten (0D gap closed as physics); headline doc + 3 STALE-BASIS notes re-baselined. `mfe_viability.sysml` 4.95 doc re-pointed to the Table-2 image 4.05.
- Staged copies mirrored (library file byte-identical; plant/instance shared regions mirrored, staged codegen adaptations preserved).

**Codegen (Rung B, first handwritten-impl item):**
- `bridge_v11_generate.py` sets `preserve_handwritten=True`. Regen routed `'DT Fusion Power'` to manual_required, emitted the package, V11 offenders stayed exactly 3 (the known rollups), backlog listed 1 function (`run_dt_fusion_power`, High).
- `handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py` filled: `_sigv_dt` (Bosch-Hale, reactivity.py:54-70 coefficients), trapezoid integral N = 200,000 in ρ, T-floor 1e-6 keV, pure-Python `math`; bypass branch reproduces the exact legacy 0D arithmetic. **Survived a second regen** (MR-WI022-4 acceptance). Gotcha for the record: the pre-WI-022 generator had auto-filled that impl file with the old 0D expression, and `preserve_handwritten` preserves by file existence — a stale auto-impl would have silently computed the old semantic. Rewritten by hand; `AUTO_IMPLEMENTED = False`.
- Oracle (`verify_stellaris.py`) carries the identical `_sigv_dt` + integral (same op order) — the runner's rel-1e-9 gate is an exact-mirror guard.

**Validation:**
- L1 = 0; L2–L5 pass; L6 = the same pre-existing offender set as the WI-021 baseline (3 MFE cross-part rollups, 2 IFE unbound attrs, 1 hif_plant binding). Zero new offenders; no diagnostic mentions any WI-022 element.
- `run_stellaris.py`: every physics channel, per-account capital, rollup, and LCOE bit-exact vs oracle at rel 1e-9; WI-022 headline check green.
- **Handshake closure (D2 proof): zero edits to `handshake_1costingfe.py`; `handshake_comparison.json` byte-identical to the committed WI-021 record** (SV-025 six channels +0.00%, worst formula-isolation −7.63e-08 = structure, same as WI-020/021). The injected `fusion__sigma_v > 0` takes the exact legacy bypass path by construction.
- IFE regression SV-023: all anchors OK (252.30 / 68.69 / 270.12; Meier 4.735 c/kWh) — unchanged.
- Viability at the re-baselined power: beta 0.0276 < 0.05; wall load 3.131 < 4.05 (corrected limit); TBR 1.074 > 1.05 — all pass.

**Re-baselined Stellaris headline (V = 425, executed):** fusion power **2748.06 MW** (profile-integrated; **+1.8% vs the 2700 MW design point — the "0D gap" closed as sourced physics, no tuning**), p_th 3238.1, gross 1078.3, **net 804.1 MW**, rec_frac 0.254, q_eng 3.93, total **$9.586B**, **LCOE $176.07/MWh**, magnet **$4.117B (42.9%** — bore shrank with a = 1.3). Prototype cross-check: 2747.7 MW (numpy trapezoid) vs 2748.06 executed (pure-Python N = 200k) — discretization-level agreement.

**Errata disposition (see spec §Surfaced extraction errata):** folded in — a 1.5→1.3, V 448→425, n_e 3.37→3.17e20, wall limit 4.95 (phantom row)→4.05, T_i0 doc 24.6→14.63. Queued — **WI-023** magnet B (Table 3 "5.86 T" row absent from the table image; Tables 2/5 images print axis-averaged 9.0 T). Parked for owner — **p_tf = 111 MW** cites a phantom "conduction power to coils" text row (the image prints 111 as stored magnetic energy [GJ]); left bound pending a real sourced value. Recorded only — the source's own 940 vs 327 m² surface-area inconsistency.

**Flags at close:** SV-016 ("Q_eng ~10–40" band) still open — q_eng moved 3.16 → 3.93, still below the band; awaiting owner adjust/annotate (unchanged status).
