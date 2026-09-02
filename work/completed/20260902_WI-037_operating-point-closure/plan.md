---
Status: complete
Created: 2026-09-01
Updated: '2026-09-02'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-037 Plan: Operating-Point Sustainment

Phased implementation of design D1–D8. Validation after each phase; L1 = `uv run syside check` on touched files, full sweep at the end. Both trees (`models/` and `exploration/stellarator_e2e/models/`) stay byte-identical.

## Phase 1 — Library: sustainment calc + limit
- [x] `models/library/analyses/mfe_plasma_sustainment.sysml` — `'Plasma Sustainment'` calc def per D1/D2: manual interface (outs without expressions), normative executable semantic in the doc (closed-form ISS04, A.3 balance, A.5/A.6 damped ash fixed point, composed radiation, discretization contract N=200,000 / floor 1e-6 keV / damping ½ / tol 1e12 m⁻³ / cap 200 / fail-loud), full Source/Ref/Basis.
- [x] `models/library/analyses/mfe_viability.sysml` — `'Sustainment Limit'` constraint def (p_aux_required ≤ p_aux_installed).
- [x] L1 both files.

## Phase 2 — Generic plant wiring
- [x] `models/designs/generic_mfe/mfe_plant.sysml` — new held-fact attributes (iota_23, f_ren, f_alpha_fast, tau_ratio_ash, f_suppr_ash, Z_eff_core, f_W_core, Ti_over_Te; R_w_sync/kappa_sync defaulted); `calc sustain : 'Plasma Sustainment'` wired from levers, geom, and `magnet.B`; fusion and beta rebound to `sustain.{n_D0,n_T0,n_He0,T_e0}` by reference redefinition; plant attributes n_D0/n_T0/n_He0/T_e0 retired (deleted; the calc-def defaults cover the 0D-bypass dormant path).
- [x] L1.

## Phase 3 — Instance
- [x] `models/designs/stellarator_09/stellarator_plant.sysml` — retire `:>> n_D0/n_T0/T_e0/n_He0` bindings (retirement note at the site, WI-035 pattern); bind the held facts with image-verified citations (iota_23 = 0.92, f_ren = 1.0, f_alpha_fast = 0.95, tau_ratio_ash = 8.0, f_suppr_ash = 0.5, Z_eff_core = 1.20, f_W_core = 7.76e-6, Ti_over_Te = 0.95); correct the `p_input` doc (plasma-coupled, Table 2); assert `sustainment_ok`.
- [x] L1.

## Phase 4 — Twins
- [x] Copy the four touched files byte-identically into `exploration/stellarator_e2e/models/`; verify with `diff -r`.

## Phase 5 — Handwritten impl
- [x] `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py` — pure-Python float64 realization of the doc semantic, `AUTO_IMPLEMENTED = False`, identical Bosch-Hale/profile-integral code and contract as `dt_fusion_power_impl.py`, faithful Albajar port; plus `__init__.py`.
- [x] Spot-run the impl standalone against the round-1 prototype numbers (τ_E 1.458, p_rad 228.7, n_He0 5.80e19, p_aux_required 89.6 at point-A levers).

## Phase 6 — Validation + record
- [x] Full L1 sweep both trees; offender list unchanged vs HEAD baseline.
- [x] `uv run python -m pytest tests/models` — green; census re-derived per suite instructions if it flags the entry-point changes.
- [x] Implementation record appended below.

## Implementation record — 2026-09-01

- **Phase 1:** `mfe_plasma_sustainment.sysml` ('Plasma Sustainment', 21 ins / 13 outs, manual interface, normative doc semantic) and `'Sustainment Limit'` appended to `mfe_viability.sysml`. L1 clean. One syntax gotcha fixed: `tau*/tau_E` inside doc comments terminates the block comment ("tau_star/tau_E" now).
- **Phase 2:** plant wiring — `sustain` calc, eight new held-fact attributes (no defaults, the WI-030 precedent), fusion/beta rebound to `sustain.{n_D0,n_T0,n_He0,T_e0}` by reference redefinition, plant attributes n_D0/n_T0/n_He0/T_e0 retired, `mfe_plasma_sustainment` import added.
- **Phase 3:** instance — retirement notes at the four old binding sites; eight held binds with image-verified citations; `p_input` doc corrected to plasma-coupled (Table 2 image); `sustainment_ok` asserted with the expected-violation disclosure.
- **Phase 4:** twins byte-identical (`diff -r` clean on all four touched files).
- **Phase 5:** handwritten impl at N = 200,000 with the full contract; standalone spot-check against the round-1 prototype: n_bar19 38.3433, n_He0 5.80107e19, tau_E 1.4579 s, p_brems 98.367 / p_line 115.983 / p_sync 14.306 → p_rad 228.656 MW, p_aux_required **89.544 MW** at the point-A levers — every value within the refinement delta of the N=400 prototype. Return-tuple order = calc-decl order; verify against the regenerated caller at integrate (noted in the impl header).
- **Phase 6:** `tests/models` 48 passed / 13 skipped (the WI-035 green state). Two suite touches, both per the suite's own instructions: `tests/model_families.py` registers the new owned file; `tests/models/data/mfe_census.json` re-derived from the new package via the test module's own helpers (semantic fingerprint `5b9abdfc…`, entry points 186 → 193: −4 retired, +8 held facts, +3 calc-default library entries). Full L1 sweep both trees: offender set identical to the HEAD baseline (4 foundation-shadow warnings, glob artifact, present at HEAD).
- **Deferred to integrate (T-004):** package regeneration, oracle extension (mirror of the impl), runner re-baseline, caller-order verification, census freshness gate.

## MR-WI037-7 restatement — entry-point retirement and committed-study consequences (recorded before the regeneration commit, 2026-09-01)

**Retired as settable entry points:** `n_D0`, `n_T0` (quasi-neutral computed fuel), `n_He0` (converged A.5/A.6 ash), `T_e0` (held ratio from the T_i0 lever). **Replacement lever set for the operating point:** `n_e0`, `T_i0`, `p_input` (now physically consequential through `sustainment_ok`), plus the machine levers (`I_coil`, `R`, `a`, `wp_side`, …) and the held sustainment facts (`iota_23`, `f_ren`, `f_alpha_fast`, `tau_ratio_ash`, `f_suppr_ash`, `Z_eff_core`, `f_W_core`, `Ti_over_Te`) as sensitivity axes.

**Committed studies no longer reproducible as written at the new package** (all bound the retired keys as held inputs): `20260821-power-cycle-ab`, `20260823-magnet-technology-ab`, `20260829-p-pump-fence`, `20260830-stress-fence`. Their records stand as committed evidence at their own pins; re-running their protocols at the WI-037 package requires dropping the retired keys from case inputs (the computed values take over) and re-reading any finding that assumed a fixed operating point.

**Baseline movement at the printed levers (verified bit-exact against the extended oracle before pinning):** p_fus 2748.06 → 2725.36 MW (−0.83%, computed fuel 1.95189e20 vs held 1.96e20), LCOE 304.481620 → 307.087120 $/MWh (+0.86%), total capital $14.574B → $14.543B, beta 0.026834 → 0.026840; verdict set 7 → 8 with `sustainment_ok` **violated** at baseline (p_aux_required 90.605 MW vs 50 installed) — the disclosed, explained verdict change (design D6/D7); every other verdict unchanged satisfied.

**Reachability consequences (live indicator report, re-derived fixtures):** I_coil now reaches `sustainment_ok`, `net_positive`, `recirc_ok`, `wall_load_ok` and the fuel/replacement/capital objectives through the confinement chain — the structural close of `20260823-magnet-technology-ab#4`; R and a gain `beta_ok` + `sustainment_ok`; availability and interest_rate unchanged (`no_constraint_response` stands — the Row 11 finding is untouched by this item).
