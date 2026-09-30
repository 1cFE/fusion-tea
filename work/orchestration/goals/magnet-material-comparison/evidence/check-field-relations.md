# T-014 focused independent check — the two derived field relations

Checker: fresh agent, brief `evidence/briefs/t014-check-field-relations.md`. I did none of the derivations. Every page below was rendered with PyMuPDF (`.codex-test/run python`) and viewed as an image, unless marked "text layer". Renders and scratch scripts are in the session scratchpad, outside the repository, not committed. Judgments are `[AGENT]`.

**Verdicts.** Relation 1 (Ampère floor): **PASS WITH CORRECTIONS**. The derivation and the arithmetic are right; the contract's sentence on where the floor binds is incomplete, and the contract names no consequence when it binds. Relation 2 (pack-size arm): **PASS WITH CORRECTIONS**. The three points, the fit and the linear form reproduce; the re-anchoring is arithmetic plus a slope-transfer assumption the contract must label as such; the anchor abscissa is rounded; the 25–40 flag band is not where the fit was made.

## Sources inspected

- Stellaris, Lion et al., FED 2025, `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf` (sha256 7fd72c12…): PDF p.3 Table 2; p.22 § 2.9 text; p.23 Table 8, Fig. 41 and text.
- Lion et al., Nucl. Fusion 61 (2021) 126021, session-scratchpad copy (sha256 db74f1c6d04aa505…, the prefix field-term.md names): PDF p.4 (journal p.3) § 2 scaling prescription; p.9 (journal p.8) eq. 36–39; p.16 (journal p.15) Table 2; p.17 (journal p.16) plasma–coil distance.
- Lion, PhD thesis TU Berlin 2023, session-scratchpad copy (sha256 4eafe5a7c38b39c0…): PDF p.106 (printed p.98) Table 4.1; PDF p.108–109 (text layer) set-up; PDF p.110 (printed p.102) Table 4.3.
- Model: `models/library/analyses/mfe_plasma_scaling.sysml:420-493` ('Conductor Peak Field', identical in `exploration/stellarator_e2e/models/analyses/`), `:145` (`r_coil_centre = vessel_or + coil_t/2`); `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml:246` (peak_ratio 2.7667), `:278` (a_coil_ref 3.15 m), `:286` (k_link 0.77313), `:305` (coil_t 0.30), `:447` (wp_side 0.36).

## Relation 1 — the Ampère floor: PASS WITH CORRECTIONS

### Re-derivation

1. Take one coil and cut its winding pack perpendicular to the coil's direction. The cut is a square of side `s`. Its boundary is a closed loop `Γ` of length `4s` that links the coil's current once.
2. Ampère's law (magnetostatics): `∮_Γ B·dl = μ0 × (current through any surface bounded by Γ)`. The only current through that surface is the coil's own ampere-turns `I_coil`. Current conservation makes the answer independent of which spanning surface is chosen.
3. The integrand is the tangential component `B_t = B·t̂` along `Γ`. So the mean of `B_t` around `Γ` is exactly `μ0 I_coil / (4s)`.
4. `max|B|` on `Γ` ≥ `max B_t` on `Γ` ≥ mean of `B_t` = `μ0 I_coil / (4s)` = `μ0 I_coil / (4√A_wp)`.

Assumptions, each stated:

- **Component.** The bound is on the tangential component along the loop, which is the part of B lying in the cross-section plane and tangent to the pack boundary. `|B|` can only be larger, so the bound holds for the field magnitude.
- **No straight-conductor approximation.** Ampère's circuital law is exact for any geometry. Curvature, torsion, discrete turns and a non-uniform current distribution inside the pack do not enter. The only geometric input is the perimeter of one perpendicular cut: `4s` for a square. For a rectangular pack the bound is `μ0 I / (2(t + r))`, and `μ0 I/(4√A_wp)` slightly overstates it. For field-term.md's Helias 5 row (0.634 × 0.761 m) that is 6.89 T against 6.92 T. There is no contract consequence, because the plant packs are square.
- **Steady state, non-magnetic materials.** DC flat-top (no displacement or eddy currents; the casing carries no net current), and no magnetised material in or near the pack (copper, SS316, REBCO, Nb₃Sn). With a ferromagnetic material the law would bound H, not B.
- **External field from the other coils.** Their currents do not pass through any surface bounded by `Γ`, so their field has zero circulation around `Γ`. It can move the maximum, cancel `|B|` at some points, and make the total-field maximum lower than the self-field maximum. It cannot change the mean of `B_t` around `Γ`, so it cannot pull `max|B|` below `μ0 I_coil / (4s)`.
- **Scope.** The bound holds at every cross-section, including the weakly loaded outboard side. That is why it is loose: 54–60 % of the printed peaks.

### Arithmetic

All six Stellaris coils were checked against Table 8 (PDF p.23, viewed zoomed), using μ0 = 4π×10⁻⁷.

| Coil | I (MA) | side (m) | floor (T) | Table 8 peak (T) | Fig. 41 surface max (T) | peak / floor |
|---|---|---|---|---|---|---|
| 0 | 15.4 | 0.360 | 13.44 | 24.6 | 24.70 | 1.83 |
| 1 | 14.6 | 0.360 | 12.74 | 23.1 | 23.33 | 1.81 |
| 2 | 13.8 | 0.340 | 12.75 | 22.0 | 22.02 | 1.73 |
| 3 | 12.9 | 0.340 | 11.92 | 21.0 | 20.90 | 1.76 |
| 4 | 12.5 | 0.320 | 12.27 | 21.4 | 21.37 | 1.74 |
| 5 | 11.2 | 0.300 | 11.73 | 19.5 | 20.19 | 1.66 |

- The claim reproduces: coil 0 gives 13.44 T against 24.6 T, and coil 5 gives 11.73 T against 19.5 T.
- The printed rows are consistent with each other. Turns × turn current equals I (324 × 47.6 kA = 15.42 MA), and I/side² equals the printed j_WP to rounding (118.8 against 119 A/mm²). So the Table 8 "I (total Amp-turns)" row is one coil's ampere-turns, and the side is the current-carrying square.
- Table 2 (PDF p.3) prints 24.9 T peak conductor field and 15.4 MA peak coil current. That is 1.85 × the coil-0 floor.
- Observation, no action needed: Fig. 41's surface maxima and Table 8's peaks differ by up to 0.69 T (coil 5). The text (p.23) gives 24.59 T "inside the winding pack" for coil 0. This is within-paper spread and is immaterial to a floor at 12–13 T.

### Which B_peak the bound applies to

The floor applies to both definitions, and the difference does not matter for a floor:

- The model's `B_peak` is the "peak magnetic field on the winding pack" (`mfe_plasma_scaling.sysml:422`), anchored to Table 2's peak conductor field.
- Lion 2021's `B_max` is the maximum over position of the total field, "on the coil surface" (eq. 38, PDF p.9).
- The loop `Γ` lies on the pack surface. B is continuous across it (no surface current). So the maximum over the pack (interior plus boundary) ≥ the surface maximum ≥ the floor.
- Suppose `B_peak` were read strictly as the peak over tape-stack positions only, which sit about half a turn width inside the surface. The same argument on the loop through the outermost turn centres, with uniform current, gives a floor lower by the factor `(s − w)/s`. With the 20 mm turn that factor is 0.944 (12.69 T at coil 0), still far below the peak.

### Where the floor binds: check of the contract sentence

In the plant model, `B_axis = μ0 k_link N I/(2πR)` and `B_peak = B_axis × ratio × bn`, where `bn` is the normalised bore factor. Dividing by the floor gives:

`B_peak / floor = (2 k_link N/π) × bn × ratio / (R/s) = 23.63 × bn × ratio / (R/s)` (k_link 0.7731, N 48; equals 1.853 at the reference).

I evaluated `bn` over the § 5 grid using `a_coil = a + 1.70 + coil_t/2` with coil_t 0.30–0.70 m. It lies between 0.90 and 1.08.

| Geometry cell | Floor binds when R/s exceeds | Examples |
|---|---|---|
| anchored (ratio 2.7667) | 65.4 × bn | R 22 / a 2.2: 0.99 at s 0.36 m, 0.83 at s 0.30 m |
| HELIAS-class (ratio 2.12, k_link 0.773) | 50.1 × bn | R 15, s 0.30: 0.98; R 18, s 0.36: 0.95; R 22, s 0.36: 0.76 |
| HELIAS-class, k_link 0.95 variant | 61.5 × bn | R 18, s 0.30: 0.97; R 22, s 0.36: 0.93 |
| pack-size arm | never | `23.63 × bn × (0.064 + 0.508/(R/s)) ≥ 1.51 × bn ≥ 1.36` on the grid |

- The arm result holds because its slope 0.064 exceeds 0.042/bn. A slope below about 0.047 would let the floor bind at large R/s.
- Equal-duty REBCO designs at large R carry small packs. For example, about 15 MA at 120 A/mm² gives s ≈ 0.36 m, so R/s ≈ 61 at R 22. Those designs land in the binding region of both constant-ratio cells.

### Corrections required to the contract text

1. § 3.2: "it can bind on the anchored cells at large R and small pack, never under the arm" → "it can bind on both constant-ratio cells, anchored (R/s > 65 bn) and HELIAS-class (R/s > 50 bn, or > 62 bn with k_link 0.95), at large R and small pack; under the arm it cannot bind while the arm slope exceeds 0.042/bn (it is 0.064)."
2. § 7 names the floor margin only as a carried flag. A design with `B_peak` below the floor has a physically impossible peak field. Its conductor status, acceptance, strain, stress and tape count are then evaluated at too low a field, which favours small packs at large R, usually REBCO. The contract must name a consequence. `[AGENT]` recommendation: a named check `ampere_floor_ok` whose violation files the design as `failed`, so it cannot be a best supported design. The alternative is to evaluate the conductor at `max(B_peak, floor)`; that is the larger change.
3. State once that the floor bounds `max|B|` over the pack, surface included, for a square pack carrying the coil's full ampere-turns. `pack_area_ok` guarantees the current lies inside `wp_side²`, which is all the floor needs.

### Not checked

- The COMSOL values themselves.
- Any tighter self-field bound for a square bar (not asked).
- The `bn` values the policy will actually supply (I used a coil_t 0.30–0.70 m illustration).

## Relation 2 — the pack-size arm: PASS WITH CORRECTIONS

### (a) The three points, reproduced from the pages

| Row | Page | B_max (T) | Tor. B (T) | R (m) | WP toroidal × radial (m) | A_wp (m²) | R/√A_wp | ratio | implied coils | k_link |
|---|---|---|---|---|---|---|---|---|---|---|
| Lion 2021 Helias 5 | PDF p.16 (journal p.15) Table 2 | 14.5 | 7.07 | 20.7 | 0.634 × 0.761 | 0.4825 | 29.80 | 2.0509 | 50.02 (printed 50) | 0.957 |
| Thesis advanced | PDF p.110 (printed p.102) Table 4.3 | 12.7 | 5.86 | 12.5 | 0.362 × 0.434 | 0.1571 | 31.54 | 2.1672 | 49.93 | 0.959 |
| Thesis conservative | same | 11.6 | 5.81 | 17.1 | 0.541 × 0.649 | 0.3511 | 28.86 | 1.9966 | 49.94 | 0.957 |

- **A_wp is the whole pack cross-section.** The total coil current divided by (j_WP × toroidal × radial thickness) gives 50 coils in all three rows. So "total coil current" sums 50 coils, and A_wp is the full rectangular pack (toroidal × radial) under j_WP.
- **The ratio's numerator** is Lion 2021's `B_max`, the maximum field on the coil surface (eq. 38, PDF p.9).
- **The ratio's denominator** is the printed "Tor. B-field". The tables do not say it is the axis average; eq. 36 uses ⟨B_t⟩. I assume the same basis as Stellaris's axis-averaged 9.0 T; not verified.
- **k_link** is my arithmetic, `B_t 2πR/(μ0 I_coil N)`.
- Page locations: field-term.md places Lion 2021 Table 2 at "p. 13–15"; it is journal p.15. The thesis page is as stated.

### (b) Refit and uncertainty

- **Fit.** Least squares on full-precision ratios gives `ratio = 0.1428 + 0.06415 · R/√A_wp`. On the 4-s.f. rounded inputs it gives `0.152 + 0.0638 ·` (field-term's numbers).
- **Residuals** are −0.0037, +0.0013 and +0.0024. The maximum is 0.0037, not "≤ 0.003". The rounded line `0.15 + 0.064 x` misses the 2021 point by −0.0063.
- **Formal statistics.** SE(slope) is 0.0024 with one residual degree of freedom. The 95 % t(1) = 12.71 interval is 0.034–0.095 (±47 %).
- **Rounding of the printed values.** Uniform ± half last digit on all 15 printed inputs, Monte Carlo: slope 95 % range 0.058–0.071 (extremes 0.054–0.077); intercept 95 % range −0.06 to +0.33.
- **Leave-one-out slopes:** 0.064 (drop 2021), 0.058 (drop advanced), 0.067 (drop conservative).
- **How to read it.** The rounding half-width of each ratio (0.009–0.010) exceeds every residual, so the points are consistent with an exact line.
  - If they sit on one PROCESS eq. 39 line, that line's slope is known to about ±10 %.
  - If they do not, the one-degree-of-freedom interval (±47 %) is the honest statement.
  - The intercept is undetermined either way. It does not matter after re-anchoring, which replaces it.

### (c) Do the three points share one coil set?

The evidence is consistent with one coil set, but no source states it.

For:

- Same coil count: 50 printed in 2021, 49.93 and 49.94 implied in the thesis.
- Same k_link: 0.957 / 0.959 / 0.957, within about 0.3 % rounding. This is the strongest indicator, because eq. 36's `I0(C)` normalisation is a configuration constant.
- Same pack aspect: radial/toroidal 1.200 / 1.199 / 1.200.
- Same plasma aspect: 12.3 / 12.25 / 12.30.
- The Table 4.3 caption says "a configuration … of the Helias 5 line". The Table 4.1 caption says the advanced case assumes improvements "without changing the configuration and the coils 'too much'".

Against:

- Table 4.1 also calls them "two Helias 5-like configurations".
- Neither source says the 2023 runs reuse the 2021 pre-processed `a0`, `a1`.
- The thesis rows differ in conductor (Nb₃Sn against REBCO, both at 4.5 K), blanket space (1.2 m against 0.6 m) and ε_eff. None of these enters eq. 39.

Reading: the slope is best read as PROCESS's own eq. 39 pack response along the Helias 5 coil set (`K·a1`), not a mixture. That reading depends on the unprinted shared pre-processing.

### (d) The linear form, the bore factor, and the re-anchoring

- **Linear form.** Lion 2021 § 2 (PDF p.4) says coil number and shapes are fixed and only the overall size is scaled, with "the minor plasma radius a at constant coil radius". So `a_coil/R` is fixed within a configuration. Eq. 36 gives `I ∝ ⟨B_t⟩ R`. Substituting both into eq. 39 gives `B_max/⟨B_t⟩ = [2π/(k (1 − a_coil/R))] · [a0 + a1 · R/√A_wp]`. This is linear in `R/√A_wp` at fixed bore and multiplicative in the bore factor `R/(R − a_coil)`. The brief's point (d) is confirmed.
- **No double counting.** The three Helias points carry no bore variation. The model's product `ratio_arm(x) × bore_norm` is exactly eq. 39's structure. The model and the arm therefore do not double count in form. The contract's "unestablished" can be replaced by this.
- **Re-anchoring is arithmetic plus one assumption.** Putting a line of given slope through (35.28, 2.7667) is arithmetic. Using the Helias 5 slope for Stellaris is an added assumption. `K·a1` is configuration-specific, and Stellaris differs in coil count (48 against 50), k_link (0.773 against 0.957), bore factor (1.330 against about 1.2–1.3 `[AGENT]`) and coil shapes (quasi-isodynamic against HELIAS). The implied intercepts already differ: 0.508 against 0.143. No source picks which quantity transfers. Three defensible rules `[AGENT]`:
  - Same absolute slope: 0.064 (the contract's choice).
  - Same local elasticity (0.93 at the Helias point): 0.073.
  - Same `a1`, with eq. 39's prefactor rescaled: 0.084–0.090. This assumes Helias `a_coil/R` of 0.15–0.20, which is not printed; Lion 2021 PDF p.17 gives only the 1.9 m plasma–coil distance at reference size.
  - The transfer choice alone spans +40 %, more than the fit's rounding uncertainty.
- **Anchor abscissa.** Stellaris `R/√A_wp` = 12.7/0.36 = 35.278, not 35.3. With 35.3 the arm returns 2.7653 at the reference pack instead of 2.7667, so B_peak is 24.888 T instead of 24.9 T at 9.0 T. The arm cell then does not reproduce its own anchor.
- **Sign.** Eq. 39 prints the form, not the sign of `a1`. The sign comes from the positive fitted slope. It is also forced at small packs by the Ampère floor: for Stellaris the ratio must be at least `0.042 · (R/s) / bn`.

### (e) Arm predictions at the grid extremes, and the 25–40 band

| Case | R/√A_wp | arm peak_ratio | × anchor | inside 25–40 | B_peak/floor at bn = 1 (arm; anchored) |
|---|---|---|---|---|---|
| R 10 m, 0.30 m pack | 33.33 | 2.641 | 0.955 | yes | 1.87; 1.96 |
| R 22 m, 0.36 m pack | 61.11 | 4.419 | 1.597 | no | 1.71; 1.07 |
| R 12.7 m, 0.53 m pack | 23.96 | 2.041 | 0.738 | no | 2.01; 2.73 |

- `bn` multiplies every entry: about 1.05 at R 10, 0.92 at R 22, and 1.00–1.02 at R 12.7.
- At R 22 with a 0.36 m pack, the model's `B_peak/B_axis` must be at least 2.59 by the floor. The anchored line gives about 2.55 there (below the floor). The arm gives about 4.07, well above every printed stellarator ratio in the evidence (2.0–2.8). Neither line is evidence at that corner.
- **The 25–40 band is not where the fit was made.**
  - The fit was made on the Helias 5 coil set over 28.9–31.5, a span of 2.7.
  - The Stellaris anchor (35.28) lies outside that span, on another coil set. So every arm case except the anchor itself uses a transferred slope.
  - At R 12.7, the band 25–40 corresponds to pack sides of 0.51–0.32 m, or pack areas 2.0× to 0.78× the reference. That is an `[AGENT]` tolerance around the anchor.
  - It works as a flag, provided it is described as a tolerance and not as a fitted domain.
  - The grid spans R/s from about 19 to 73, so many arm designs will carry the flag.

### Corrections required to the contract text

1. § 3.2 arm formula: write it as `peak_ratio_ref + 0.064 × (R/√A_wp − R_ref/wp_side_ref)`, with the reference abscissa computed from the same floats (35.2778), so the arm reproduces 24.9 T exactly at the reference.
2. § 3.2 evidence cell:
   - Replace "possibly mixing coil sets" with "consistent with one Helias 5 coil set (N 50, k_link 0.957, pack aspect 1.20 in all three rows); shared pre-processing not stated".
   - Replace "whether it and the model's bore factor double count is unestablished" with "no double count: the fit points are at fixed a_coil/R (Lion 2021 § 2) and eq. 39 is multiplicative in the bore factor".
   - State the slope's uncertainty: rounding 0.058–0.071; formal one-degree-of-freedom 0.034–0.095.
   - Correct the residuals to ≤ 0.004.
3. § 3.2 label: the slope is [D] on the Helias 5 coil set. Its transfer to the Stellaris coil set is an added [U] assumption; alternative transfer rules give 0.073–0.090. The row should carry both labels, so the map's weaker-of-two rule reads [U] away from the anchor.
4. § 3.2 flag: say "fit made over R/√A_wp 28.9–31.5 on Helias 5; the `arm_extrapolated` band 25–40 is an [AGENT] tolerance around the Stellaris anchor, not a fitted domain". `[AGENT]` suggestion: also report `ratio_arm / 2.7667` per case as the size of the pack-term correction.
5. § 3.2 sign sentence: "follows the printed eq. 39" → "follows the fitted Helias 5 slope (eq. 39 form with a1 > 0 there); the Ampère floor forces the same sign at small packs".

### Not checked

- Whether the 2021 and 2023 PROCESS runs share pre-processed `a0`, `a1` (unprinted).
- Whether "Tor. B-field" is the axis average.
- The Helias 5 `a_coil/R`. I used 0.15–0.20 `[AGENT]` only for the alternative-transfer illustration.
- Lion 2021 Tables 1 and 3, appendix A, and Schauer 2013.
- Any implementation: the arm is not built yet.
