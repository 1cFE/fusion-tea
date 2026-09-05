---
Status: approved
Created: 2026-09-05
Updated: 2026-09-05
Related Artifacts:
  Spec: ./spec.md
---

# WI-042 Design — the helium-ash profile from the source's own rule, electrons by quasi-neutrality, one pressure integral

Designed under goal `stored-energy-basis`, round 2, task T-001. The spec's five open decisions are settled here with their reasoning and cost, because the round review reads this file to check that the increment stayed inside the owner's ruling — the ash shape and the electron closure change; the W integral form, the fuel and temperature exponents and the peaks do not — and that no number was tuned.

## Overview

Today the sustainment calc integrates power-law profiles for the stored energy and gives the helium ash the fuel's flat exponent (0.33), while the beta calc carries a second copy of the same pressure average. The paper the model cites for the ash *amount* also states the ash *shape*: the ash follows the fusion-rate profile times a fixed particle-to-energy confinement ratio (Appendix A, Eq. A.5, applied pointwise; p. 9). This design puts that rule inside the sustainment calc — the ash profile is the fusion-rate shape scaled to the converged peak, the electrons are the ions' charge, and W is the same 1.5 ⟨p⟩ V over the derived profiles — retires the bound electron exponent, has the beta calc read the one ⟨p⟩ the sustainment calc computes, and makes every reader of the electron profile inside the chain (the ISS04 line average, the bremsstrahlung and line-radiation integrals, the synchrotron fit's profile parameter) take the derived profile. Nothing is bound at point A; the shape is computed from the rule at every lever point, which is what the owner's "scales up for larger stellarators" asks for.

At the baseline the two violated verdicts both flip to satisfied — sustainment by 0.9 MW, the wall by the fusion power falling 2.7 % as the ash re-closes — and LCOE rises 2.8 %. Those are the rule's consequences, disclosed here and never tuned; the sustainment margin is inside the paper's own 2.7 % residual, so the design point stays on the boundary.

## Research findings

**The rule, from the pages** (rendered from `raw.pdf`, never the extraction). p. 9: "Helium ash profiles are obtained using a fixed ratio of particle-to-energy confinement time." p. 32, A.5: n_He / τ*_α = n_D n_T ⟨σv⟩_T with τ*_α = ρ* τ_E, ρ* ~ 8 ("ρ* shall not be confused with the normalized minor radius"); A.6: n'_He = f_suppr n_He, f_suppr = ½. The paper defines p ≡ ⟨p⟩_V ≡ ∫_V p dV / V and closes the balance with P = W/τ_E (A.7–A.8). Nothing on the pages makes τ* depend on ρ; the pointwise reading with τ* uniform is the only one the text supports, and it reproduces the printed n_e0 (5.04 vs 5.06) and ⟨n_e⟩ (3.16 vs 3.17) and the plotted ash curve of Fig. 16(a) (goal L-002, L-003).

**What the rule gives at any lever point.** With n_D = n_T = n_D0 u^α_n (u = 1 − ρ²), T_i = T_i0 u^α_T, and the ash amount n_He0 from the same fixed point as today, the ash profile is n_He(ρ) = n_He0 · S(ρ) with S(ρ) = u^(2α_n) ⟨σv⟩(T_i0 u^α_T) / ⟨σv⟩(T_i0); S(0) = 1 by construction, so the peak and the shape are one equation. The electrons are n_e(ρ) = 2 n_D0 u^α_n + 2 n_He0 S(ρ), with n_e(0) = 2 n_D0 + 2 n_He0 = n_e0 — the lever is untouched. The pressure average splits into a closed-form fuel term and an ash-weighted integral: ⟨p⟩ = e [ 2 n_D0 (T_e0 + T_i0) / (1 + α_n + α_T) + n_He0 (2 T_e0 + T_i0) I_W ], I_W = ⟨S(ρ) u^α_T⟩_V = ∫₀¹ 2ρ u^(2α_n + α_T) ⟨σv⟩(T_i0 u^α_T) dρ / ⟨σv⟩(T_i0). The line average that enters ISS04 is n̄ = ∫₀¹ n_e(ρ) dρ = 2 n_D0 I_line(α_n) + 2 n_He0 I_line(S), so the ISS04 prefactor now depends on the ash and sits inside the fixed-point iteration. The volume average ⟨n_e⟩ = 2 n_D0 / (1 + α_n) + 2 n_He0 ⟨S⟩_V gives the effective electron exponent n_e0 / ⟨n_e⟩ − 1 — the very relation that bound 0.596 from the printed pair.

**What it does at the baseline** (the oracle-side prototype, `prototype/proto_qn_chain.py`, the full plant computation with the quasi-neutral chain substituted; every number a prediction the implementation checks): W 551.444 → 519.914 MJ; τ_E 1.4499 → 1.5573 s; n̄ 38.343 → 37.777; n_He0 5.781e19 → 6.044e19; n_D0 1.9519e20 → 1.9256e20; p_fus 2725.36 → 2652.56 MW; p_rad 228.61 → 219.72 MW; p_aux_required 90.605 → 49.080 MW (installed coupled 50 → **satisfied by 0.92 MW**); wall peak 4.0880 → 3.9788 (**satisfied**); β from the one ⟨p⟩ 2.684 % → 2.531 %; CAS72 131,494,480 → 126,649,656; LCOE 313.513 → 322.318; effective electron exponent 0.5953 (the bound 0.596; ⟨n_e⟩ 3.172e20 vs printed 3.17); effective ash exponent 4.05 at 14.63 keV.

**The shape scales.** The effective ash exponent is a function of T_i0 through the reactivity's temperature dependence — 4.73 at 10 keV, 4.41 at 12, 4.05 at 14.63, 3.66 at 18, 3.46 at 20 (α_n 0.33, α_T 1.19) — and of nothing bound at point A. Across the geometry window the committed studies sweep, W_new / W_old is not a constant: 0.99 at (R 17.2, a 1.3), 0.93 at (R 11.2, a 1.3), 0.84 at (R 14.2, a 2.2), 0.77 at (R 11.2, a 2.2), following the ash fraction the rule gives at each geometry (larger τ_E → more ash → a larger share of the old family's off-axis over-count). The closure's fuel guard fires at (R 11.2, a 2.2, T 18, 1.1×) under both chains (`prototype/window_corners.json`).

**Who reads the electron exponent today** (`grep alpha_n_e`): the sustainment calc (four readers inside: W, n̄, the two radiation integrals, the Albajar parameter), the beta calc (`p_e`), the generic plant attribute and two bindings, the instance binding at `stellarator_plant.sysml:602`, the census (a design attribute), `oracle_entry.py:78` (an entry key), `verify_stellaris.py` (`IN["alpha_n_e"]` and the beta mirror at `:596`), `tests/models/test_beta_peak_field.py:21-24` (the beta calc's formal list, asserted in order), and one committed record's prose. No study definition and no `run_stellaris_single.py` guard case reads it.

**The codegen envelope** (migration ledger; WI-039/WI-041 designs): arithmetic only inside calc defs (`+ − × ÷ **`), no function invocation on the exact route, every binding a bare reference or a calc output, defaulted formals declared last, a manual stage's handwritten impl preserved across regeneration only while its interface matches (otherwise re-stencilled — restore by hand, delete `handwritten/backup/`, regenerate again).

## Design decisions

### D1 — The rule lives inside 'Plasma Sustainment'; the bound electron exponent retires; four derived quantities become outputs. `[AGENT]`

**The decision.** `alpha_n_e_in` is removed from the sustainment calc's formals; the ash profile, the electron closure, the ash-weighted integrals and the derived line and volume averages are computed inside the calc (a manual stage already); four outputs are added — `p_avg` (the volume-averaged thermal pressure [Pa], the one pressure integral), `n_e_volav` (⟨n_e⟩ [m⁻³]), `alpha_n_e_eff` (n_e0/⟨n_e⟩ − 1 [1]) and `alpha_He_eff` (the ash shape's effective power-law exponent [1], a diagnostic). The generic plant attribute `alpha_n_e` and the instance binding `alpha_n_e = 0.596` are deleted; the printed pair 3.17 / 5.06 stays in the instance as the cross-check the derived `alpha_n_e_eff` is compared with (0.5953).

**Why retire rather than rebind.** Keeping a formal bound to a computed quantity would make the calc take as input something it computes itself. Retiring it is what "the shape is computed from the rule at any geometry, never bound as an exponent digitized at point A" means for the electrons.

**Why `alpha_He_eff` as an output.** MR-WI042-10 has the study read the effective ash exponent at every executed point; a channel is the only way a study reads it. Its definition is stated so it is reproducible: the least-squares slope of ln S(ρ_k) against ln u_k over the 1,700 nodes ρ_k = k/2000, k = 1..1700 (ρ ≤ 0.85, the round-1 attribution's window). Nothing downstream reads it.

**What it costs.** One entry point retired (`stellarator_09__stellaris__alpha_n_e`, a design attribute); four channels added; the handwritten impl's interface changes (re-stencil expected; the recorded recovery); the oracle's `IN` and channel dict; `oracle_entry.py`'s entry-key map; the census; the six known-answer fixtures.

### D2 — 'Volume-Averaged Beta' reads the one ⟨p⟩ and computes only β = 2 μ0 ⟨p⟩ / B². `[AGENT]`

**The decision.** The beta calc's nine profile formals (`n_e0_in`, `T_e0_in`, `n_D0_in`, `n_T0_in`, `n_He0_in`, `T_i0_in`, `alpha_n_in`, `alpha_n_e_in`, `alpha_T_in`) and its intermediates (`p_e`, `p_fuel`, `p_He`, `p_avg`) are removed; it takes `in attribute p_avg_in : Real` (the volume-averaged thermal pressure [Pa]) and `in attribute B_in : Real`, keeps `mu0` (declared last, defaulted), and computes `beta = 2 μ0 p_avg_in / B_in²`. The generic plant binds `p_avg_in = sustain.p_avg`. `e_keV` retires with the pressure arithmetic.

**The alternative, and why it loses.** Keeping the closed-form body and adding a bypass would need a conditional the exact route does not admit (no conditional expression exists anywhere in the library), or a second manual stage recomputing the profile integral — a second copy of exactly the thing MR-WI042-4 forbids. Reading the one ⟨p⟩ makes "W and β can never disagree" true by construction: β B² 1.5 V / (2 μ0) = W_th to float precision.

**Concept-agnostic use preserved.** Every MFE instance is the generic plant and carries the sustainment chain (WI-037 made the chain generic: "every MFE concept binds them from source"), so every instance has a ⟨p⟩ to read. The former closed form — Σ_s n_s0 T_s0 / (1 + α_n,s + α_T) — is recorded in the beta calc's doc as the no-ash special case the sustainment calc reproduces (D7), not as an executable path.

**What it costs.** `tests/models/test_beta_peak_field.py`'s formal list and intermediate list are restated from this design; one library-default entry point retires (`beta_calc__e_keV`); the beta calc is regenerated as an expression module (not manual). The `beta_ok` operand binding (`beta_calc__beta`) does not move.

### D3 — The ISS04 density is the chord average of the derived profile, and the ISS04 prefactor moves inside the fixed-point iteration. `[AGENT]`

n̄ = ∫₀¹ n_e(ρ) dρ = 2 n_D0 I_line(α_n) + 2 n_He0 I_line(S), with I_line(α_n) = ∫₀¹ u^α_n dρ and I_line(S) = ∫₀¹ S(ρ) dρ computed once per evaluation (they do not depend on n_He0), and C = 0.134 f_ren a^2.28 B^0.84 ι^0.41 n̄^0.54 R^0.64 re-evaluated at every iterate. The fixed-point contract (damped half-step from 0, tolerance 1e12 m⁻³, cap 200, fail-loud) is unchanged; at the baseline it converges as before. This is the reader the constant-scale counterfactual could not move (`NOTES.md` § 6) and the reason the baseline lands at 49.1 MW rather than the counterfactual's 51.4.

### D4 — The synchrotron fit's density-profile parameter is the derived effective exponent. `[AGENT]`

Albajar's formula (radiation.py:180-241) is a fit parameterized by profile exponents; it cannot take a profile. The parameter is `alpha_n_e_eff` = n_e0/⟨n_e⟩ − 1, the same relation that bound 0.596 — at the baseline it reads 0.5953 and the synchrotron term moves 14.2615 → 14.2626 MW (+0.008 %). Stated in the calc doc; the alternative (a log fit of the derived profile, as for the ash) would be a second fit for no gain.

### D5 — The ash-weighted integrals share the fusion integral's contract. `[AGENT]`

I_W, I_line(S) and ⟨S⟩_V are trapezoid sums on the same grid as the fusion integral (N = 200,000 intervals in ρ, temperature floor 1e-6 keV, pure-Python float64), with the same Bosch–Hale reactivity, so the ash shape is by construction the same reactivity profile that gives p_fus. The oracle mirrors them exactly (bit-exact bar).

### D6 — Dormant-safe by the ash amount, not by a switch. `[AGENT]`

An instance that binds τ*/τ_E = 0 or f_suppr = 0 converges to n_He0 = 0 at the first iterate; then n_e ≡ 2 n_D0 u^α_n, the ash-weighted terms vanish, W and ⟨p⟩ reduce to the fuel-only closed form, and `alpha_n_e_eff` = α_n. No new inputs, no bypass; the generic plant's semantics for a no-ash concept are stated in the calc doc.

### D7 — The doc-text corrections ride this regeneration. `[AGENT]`

A doc-text change re-pins the package, so the stale comments this item touches are corrected here: the WI-030 beta-referent block in the instance (`stellarator_plant.sysml:583-604`, which bound the exponent and recorded "helium on the electron exponent would give −3.3 %"); the `sustainment_ok` comment (`:1250-1258`, "the disclosed W-form delta (+9.2 %, never tuned)" → the new disclosed reading); the sustainment calc's own doc (the CHAIN block and the cross-check line "n_He0 +3.6 %"); the beta calc's doc.

### D8 — The reference calculation and the window table are deposited under the item. `[AGENT]`

`prototype/proto_qn_chain.py` with `baseline_old_new.json` and `window_corners.json` (this session's scratch run, copied verbatim; the WI-022 `prototype/digitize_fig16.py` precedent) is the design's reference calculation for the baseline moves and the scaling table. The point-A identity (MR-WI042-8) reuses the round-1 script `evidence/w_counterfactual/attribution_sourced_definition.py` at `5cc30ac0` unchanged — its "model exponents but A.5 ash and QN electrons" row (524.5 MJ) is the number the implementation's SV row reproduces at the printed peaks.

## Proposed design

### Changed: `calc def 'Plasma Sustainment'` — `models/library/analyses/mfe_plasma_sustainment.sysml` (prototyped)

The doc's CHAIN block is rewritten to the equations in § Research findings (the ash shape S(ρ), the electron closure, n̄ over the derived profile, ⟨p⟩ as the closed-form fuel term plus the ash-weighted integral, W = 1.5 ⟨p⟩ V, the radiation integrals over n_e(ρ)², the Albajar parameter, the two effective exponents), with the Source/Ref lines adding p. 9 (the ash-profile sentence) and A.5 applied pointwise, and the cross-check line updated to what the rule gives at point A. The interface:

| quantity | kind | units | change |
|---|---|---|---|
| `alpha_n_e_in` | in | 1 | **removed** (D1) |
| every other formal | in | — | unchanged, same order; the three defaulted formals still last |
| `p_avg` | out | Pa | **new** — the volume-averaged thermal pressure, the one pressure integral |
| `n_e_volav` | out | m⁻³ | **new** — ⟨n_e⟩_V of the derived profile |
| `alpha_n_e_eff` | out | 1 | **new** — n_e0 / ⟨n_e⟩ − 1 |
| `alpha_He_eff` | out | 1 | **new** — the ash shape's effective exponent (D1's definition) |
| the thirteen existing outputs | out | — | unchanged names and meanings; values re-close |

Handwritten impl `generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py`: `alpha_n_e` gone; `S(u)`, `I_line_fuel`, `I_line_S`, `I_W_S`, `I_vol_S` computed once before the loop; `state()` computes n̄ and C per iterate (D3) and ⟨p⟩ per the split; the radiation integrals take `n_e(u)`; the Albajar call takes `alpha_n_e_eff`; the return tuple gains the four outputs in the regenerated caller's unpack order (read from the stencil after regeneration).

### Changed: `calc def 'Volume-Averaged Beta'` — `models/library/analyses/mfe_plasma_scaling.sysml` (prototyped)

`in attribute p_avg_in : Real;` (volume-averaged thermal pressure [Pa]); `in attribute B_in : Real;`; `in attribute mu0 : Real default 1.25663706212e-6;` (last); `out attribute beta : Real = 2.0 * mu0 * p_avg_in / (B_in ** 2);`. The doc says where ⟨p⟩ comes from, records the former closed form as the no-ash special case, keeps the printed 2.76 % as the cross-check with L-002's caveat (the printed β is inconsistent with the printed W at 9.0 T; the model's 2.53 % is from the same ⟨p⟩ as its W).

### Changed: `models/designs/generic_mfe/mfe_plant.sysml` (prototyped)

- `attribute alpha_n_e : Real;` (`:203`) and its comment **deleted**.
- `calc sustain`: the line `in alpha_n_e_in = alpha_n_e;` **deleted**; the comment above says the electron profile is derived inside.
- `calc beta_calc`: the nine profile bindings replaced by `in p_avg_in = sustain.p_avg;` with `in B_in = magnet.B;` kept.

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml` (prototyped)

- The block `:583-604` (the WI-030 beta-referent comment and `:>> alpha_n_e = 0.596 { … }`) replaced by a comment recording the cross-check: the printed vol-av/peak pair 3.17 / 5.06 (Table 5 image) implies 0.596 for a power law; the derived profile gives 0.5953 and ⟨n_e⟩ 3.172e20 (WI-042; SV row); β from the one ⟨p⟩ reads 2.53 % against the printed 2.76 %, thermal only, with L-002's caveat.
- The `sustainment_ok` comment (`:1250-1258`) rewritten: at this lever point the verdict is EXPECTED SATISFIED by about 0.9 MW (49.1 required against 50 coupled), a margin inside the source's own 2.7 % residual on its printed stored energy — on the boundary, never tuned (WI-042; goal `stored-energy-basis` L-001, L-002).
- Nothing else in the instance changes; no binding of a reserved quantity is touched.

### Changed: `exploration/stellarator_e2e/verify_stellaris.py` and `studies/oracle_entry.py`

`_sustainment` rewritten from this design's equations (not copied from the impl): S, the four integrals, n̄ and C inside `state()`, ⟨p⟩, the radiation over n_e(u), the Albajar parameter, the two effective exponents; `IN` drops `alpha_n_e`; `compute()` reads β as `2 μ0 sust["p_avg"] / B_axis²` and returns `p_avg`, `n_e_volav`, `alpha_n_e_eff`, `alpha_He_eff` as channels. `oracle_entry.py` drops the `alpha_n_e` entry key and maps the four channels; `OPERAND_BINDINGS` is unchanged (`beta_ok` still reads `beta_calc__beta`; `sustainment_ok` still reads `sustain__p_aux_required`).

## Cross-file bindings

| consumer | input | source | change |
|---|---|---|---|
| `sustain` (generic) | `alpha_n_e_in` | — | binding deleted |
| `beta_calc` (generic) | `p_avg_in` | `sustain.p_avg` | new (replaces nine profile bindings) |
| `beta_calc` (generic) | `B_in` | `magnet.B` | unchanged |
| `fusion` (generic) | `n_D0_in`, `n_T0_in` | `sustain.n_D0`, `sustain.n_T0` | unchanged; values re-close |
| `sustainment_ok` (instance) | `p_aux_required_in` | `sustain.p_aux_required` | unchanged; verdict flips, disclosed |
| `beta_ok` (instance) | `beta_in` | `beta_calc.beta` | unchanged |

Dataflow stays unidirectional: geometry and field → sustainment (ash, electrons, ⟨p⟩, W, τ_E, radiation, required heating) → fusion, β, wall, lifetime, LCOE. No new imports.

## Expected baseline behaviour

From the prototype (D8); every number a prediction the implementation checks bit-exact against the oracle and to the prototype's precision against this table. **If anything else moves, it is a finding to derive, not a number to fit.**

| channel | today (`c1b0f0d1…`) | after | why |
|---|---|---|---|
| `sustain__W_th` | 551.444247 | 519.914214 | the ash at the rule's shape, electrons by quasi-neutrality |
| `sustain__tau_E` | 1.449909 | 1.557334 | the closed form at a lower W and a lower n̄ |
| `sustain__n_bar19` | 38.343269 | 37.776615 | the chord average of the derived profile |
| `sustain__n_He0` | 5.781097e19 | 6.043556e19 | more τ_E, more ash (+8 % vs the printed 0.56e20; was +3.6 %) |
| `sustain__n_D0`, `n_T0` | 1.951890e20 | 1.925644e20 | quasi-neutral at the peak with more ash |
| `fusion__p_fus` | 2725.363 | 2652.563 | n_D0² (−1.8 % vs the printed 2700; was +0.9 %) |
| `sustain__p_rad` | 228.612 | 219.722 | the radiation over the derived profile |
| `sustain__p_aux_required` | 90.605 | 49.080 | W/τ_E 380.3 → 333.8; p_alpha 518.3 → 504.5 |
| `sustainment_ok` | violated | **satisfied** (by 0.92 MW) | disclosed; inside the source's 2.7 % residual |
| `wall_peak_calc__wall_load_peak` | 4.088045 | 3.978845 | ∝ p_fus |
| `wall_load_ok` | violated | **satisfied** | disclosed |
| `beta_calc__beta` | 0.026840 | 0.025305 | from the one ⟨p⟩ (was a separate closed form at 0.596) |
| `sustain__p_avg` [Pa] | — | 815,545 (= 519.914e6 / (1.5 × 425.0)) | new channel |
| `sustain__n_e_volav` | — | 3.1717e20 | new channel; printed 3.17 |
| `sustain__alpha_n_e_eff` | — | 0.5953 | new channel; the bound 0.596 |
| `sustain__alpha_He_eff` | — | 4.052 | new channel |
| `cas72_calc__cost` | 131,494,480 | 126,649,656 | lifetime by the lower peak |
| `pb__p_net` | 743.910 | 716.634 | p_fus |
| `lcoe_calc__lcoe` | 313.513412 | 322.318439 | net power down 3.7 %, CAS72 down 3.7 % |
| `lcoe_1cfe` | 307.521 | 316.141 | same |
| the heating chain, the magnet chain, geometry, every capital account except through `p_fus`/`p_net` | — | unchanged in form | nothing upstream of them moved |

The printed-point cross-checks after: W +3.0 % (was +9.2 %), ⟨n_e⟩ +0.1 %, p_fus −1.8 % (was +0.9 %), τ_E +6.6 % (was −0.1 %), n_He0 +8 % (was +3.6 %), β −8 % thermal (was −2.8 %). The τ_E move is the paper's own closed form at a lower W; the printed (W, τ_E) pair does not close the paper's balance (L-002). Disclosed, not tuned.

## Validation plan

1. Parse and Levels 1–3 on the two changed library files and the two plants (the prototype below: Level 1 clean; Level 2 the 12 pre-existing placeholder literals and nothing new).
2. Codegen through the pinned generator with `--smart-regen --preserve-handwritten`; expect the sustainment impl re-stencilled (interface change) — restore from this design, delete `handwritten/backup/`, regenerate again to `Regenerated: 0`, seal clean; the beta module regenerated as an expression module; the four new channels in the contract.
3. Execute at the baseline; compare every row of the table above.
4. Point-A identity (MR-WI042-8): the round-1 script's row "model exponents but A.5 ash and QN electrons" = 524.5 MJ at the printed peaks; the impl evaluated at the printed peaks (n_He0 held at 0.56e20, no fixed point) reproduces it and ⟨n_e⟩ 3.16e20 — SV row.
5. W–β consistency: `beta × B² × 1.5 × V / (2 μ0) = W_th` to 1e-12 relative at the baseline and under every perturbation — SV row.
6. Oracle parity, written from this design: every channel bit-exact at the baseline; under T_i0 14.63 → 18.0 (the shape moves: `alpha_He_eff` 4.05 → 3.66) and τ*/τ_E 8 → 4 (the ash amount halves, the shape's weight with it) the model and the oracle move together.
7. The disclosed verdict changes with their derivation in the manifest's baseline verdicts, the SV rows and the restatement — SV row carrying the on-the-boundary reading.
8. The scaling table (MR-WI042-10): `prototype/window_corners.json` deposited; the restating study's per-point columns (`alpha_He_eff`, `W_th`) measure it on the package.
9. `tests/models` and `tests/study` green; the six fixtures re-derived by running the tool; the census re-derived from a live generation (predicted 207 → 205: `alpha_n_e` and `beta_calc__e_keV` retire, nothing minted); the beta test's formal list restated from § Proposed design.

## Risks

1. **The generator's unpack order for the four new outputs.** *Likelihood: certain, cost: minutes.* The caller's tuple order is the generator's; the impl's return order is read off the regenerated stencil, as at WI-037 and WI-041.
2. **The beta calc's interface change reaches a reader this design missed.** *Mitigation:* the grep in § Research findings; baseline parity is the backstop (β is predicted to 0.025305).
3. **A fresh reviewer reads the verdict flips as a fit.** *Mitigation:* no quantity near either fence is bound; the identity SV evaluates the chain at the printed peaks; the window table shows the correction is not a constant; the reading says the margin is inside the source's residual.
4. **The closure edge moves in the study.** *Likelihood: high, impact: low.* More ash at a higher τ_E; the prototype found the same corner failing under both chains; the restatement says the excluded set may move (row `#8`).
5. **The pinned codegen refuses the beta calc's shrunk interface or the moved bindings.** *Likelihood: low.* Same envelope as WI-041; a `MECHANICAL_FAILURE` with a retry inside the cap; the form is not changed to dodge a tool.

## Prototype and validation report

**Prototype: PASS.** The four canonical model files edited in the working tree as § Proposed design states — `models/library/analyses/mfe_plasma_sustainment.sysml` (the doc contract rewritten; `alpha_n_e_in` removed; `p_avg`, `n_e_volav`, `alpha_n_e_eff`, `alpha_He_eff` added), `models/library/analyses/mfe_plasma_scaling.sysml` ('Volume-Averaged Beta' on `p_avg_in`, `B_in`, `mu0`), `models/designs/generic_mfe/mfe_plant.sysml` (the attribute and the binding retired; `beta_calc` on `sustain.p_avg`), `models/designs/stellarator_09/stellarator_plant.sysml` (the referent block and the `sustainment_ok` comment rewritten) — and validated from this worktree with `agentic-mbse validate models --complete` on the primary checkout's interpreter (SysIDE licence sourced):

- **Level 1 (syntax): 0 errors, 0 warnings across all 25 SysML files.**
- **Level 2 (structural): unused definitions 0, unbound inputs 0, undefined bindings 0; the 12 placeholder-literal warnings are the pre-existing set** in `mfe_plant.sysml` (`waste`, `fuel_handling`, `other_rpe`, …), untouched; nothing new.
- **Level 3 (dataflow): 0 circular dependencies.** Level 4: 10 constraints, 100 % executable. Level 5: 94 / 94 documented.
- **Level 6: the pre-existing residue minus one.** Against the unchanged tree on `feat/demo-maturation` (run the same minute): design attributes 208 → 207 (`alpha_n_e` retired), `L6_DESIGN_ATTR_INCOMPLETE` 105 → 104 (its row), `L6_DESIGN_ATTR_UNEXTRACTABLE` 60 → 60, bindings validated 315 → 306 (the beta calc's ten bindings → two; the sustainment calc's one retired), issues 237 → 236. Every remaining Level-6 line is the pre-existing "derived expression references design attributes" set.
- `grep alpha_n_e models/` after the edits: one hit, the retirement note.

**What the prototype confirms.** The shrunk beta interface and the retired attribute parse and bind; no calc is left without a consumer; the defaulted formals stay last; the doc contract states the rule, the closure, the one pressure integral, the diagnostics' definitions and the dormant case.

**What it does not confirm**, and implementation must: codegen re-stencilling the manual stage and the second regeneration; the handwritten impl and the oracle written from § Proposed design agreeing bit-exact; the baseline table; the two perturbations; the point-A identity; the restatement before regeneration.

**The reference calculation** (D8): `prototype/proto_qn_chain.py` with `baseline_old_new.json` (every row of § Expected baseline behaviour) and `window_corners.json` (24 corners of the geometry window, one fuel-guard failure under both chains). Oracle-side; not package evidence.

**Files created:** `prototype/` (three files). **Files modified:** the four canonical model files above (twins not yet synced — the plan's phases 1–3).

## Approval

Settled by the round agent under goal `stored-energy-basis`, round 2, task T-001, on the owner's (c) ruling, which fixed the subject (the ash profile from the paper's rule, quasi-neutral electrons, scaling with geometry) and reserved the W form, the exponents and the peaks. The owner was not in session; the design is the round agent's reading of the ruling and is challenged by re-deriving against the round-1 evidence and the prototype. D1 and D2 are the load-bearing judgments: D1 retires an entry point and adds four channels; D2 changes a non-manual calc's interface and retires a library default. Both rejected alternatives are written above so the round review can challenge them by re-derivation. Approved for `/plan-model` 2026-09-05.
