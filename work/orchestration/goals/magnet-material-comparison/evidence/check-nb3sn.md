# T-004 independent check A — Nb₃Sn

Checker: fresh agent, brief `evidence/briefs/t004-check-nb3sn.md`. Pages were rendered with PyMuPDF from the stored PDFs and viewed as images unless marked "text layer". My law implementation was written and run before I opened `evidence/screen/`. Scratch script: outside the repository (session scratchpad), not committed.

**Overall verdict: FINDINGS.** The law, its parameters, the strain units, the Ic evaluations and the Demattè arithmetic are all confirmed, and the screen reproduces my numbers exactly. Four items must change before modeling (listed at the end): the steel base value, the insulation-fraction basis statement, the Nb₃Sn protection-copper density, and the wording of the Nb₃Sn support claim at 8–12 T.

## 1. Law form and parameters — confirmed

- Inspected: Tsui & Hampshire 2012, raw.pdf PDF p.8 (printed p.7), eq. (6)–(7) and the text below them; PDF p.9 (printed p.8), Table 5(c); PDF p.3 Table 1 and PDF p.5 (text layer) for the criterion and Jc basis.
- Eq. (6): Jc = (C/B)·s(εI)(1−t^1.52)(1−t²)b^p(1−b)^q. Eq. (7) is the ITER strain function. Tc(ε) = Tc(0)[s(ε)]^(1/3) and Bc2(T,ε) = Bc2(0,0)s(ε)(1−t^1.52). All as the note states.
- Table 5(c) BEAS II: p 0.489, q 1.618, C 2.227×10¹⁰ A T m⁻², Ca1 226.93, Ca2 203.86, ε0,a 0.187 %, εM −0.366 %, Bc2*(0,0) 30.28 T, Tc*(0) 16.02 K, RMS 2.5 A. All nine values match.
- The basis is engineering Jc over the whole strand at 10 µV/m. Independent confirmation: the right-hand Ic axis of Fig. 9 equals Jc × 0.528 mm², which is the whole area of a 0.82 mm strand (for example 350 A ↔ 6.6×10⁸ A m⁻²).

## 2. Strain units and meaning — confirmed, with a sign correction to the brief's conversion and one bounded assumption

- **Units.** Strains enter as fractions. With ε0,a = 0.00187, 1 − Ca1·ε0,a = 0.5756 > 0. Entering 0.187 would give −41.4.
- **The law takes intrinsic strain directly.** s(εI) has its maximum s = 1 exactly at εI = 0 (checked numerically; εsh = 0.00382), so εI is strain measured from the Jc peak.
- **εM is not needed when εI is supplied.** It only converts applied strain on the measurement spring into εI.
- **Sign convention (correction to the brief's wording).** The Durham law (eq. 5, PDF p.7, text layer) defines εI = εA − εM, where εM is the applied strain at the peak. BEAS II Durham εM is +0.369 % (Table 4c). The ITER Table 5(c) prints −0.366 %, the same magnitude with the opposite sign. So the ITER-table value must be used as εI = εA + εM(table) = εA − 0.366 %. That convention puts the peak at εA ≈ +0.37 %, which matches Fig. 9. Plugging the signed table value into εI = εA − εM instead puts the peak at εA = −0.366 %, which contradicts the figure: it gives 47 A at εA = 0 against about 170 A measured.
- **SULTAN/EU DEMO effective strain.** It is in the same coordinate (intrinsic, zero at the peak). Breschi 2017 (PDF p.14, text layer) defines it as the strain "applied to the corresponding strand to obtain the same E–J characteristics measured on the full-size conductor". So it is a lumped degradation parameter tied to the strand parameterization used to extract it. The DEMO values (−0.27 %, Sedlak PDF p.3 viewed; ≈ −0.33 %, Bruzzone 2015 PDF p.6 text layer) were not extracted with BEAS II parameters.
- The same strain degrades the three available parameter sets differently. s(−0.30 %) is 0.951 for BEAS II, 0.946 for Breschi Kiswire (taking ε0a = 0.0044 as a fraction) and 0.931 for ITER-2008. At −0.60 % the values are 0.861, 0.834 and 0.809.
- Applying a DEMO effective strain to the BEAS II law is therefore a bounded assumption `[AGENT]`, not an identity. The contract's "(check)" should say so.

## 3. Independent evaluation — confirmed; no discrepancy with the screen

Implementation: eq. (6)–(7) with Table 5(c), strains as fractions, strand area π/4 × 0.82² = 0.5281 mm².

| Point | Ic_strand (A) | Jc_eng (A/mm²) |
|---|---|---|
| 12 T, 4.2 K, εI = 0 | 201.85 | 382.2 |
| 12 T, 4.22 K, εI = 0 | 201.30 | 381.2 |
| 12 T, 5.2 K, −0.3 % | 152.95 | 289.6 |
| 12 T, 6.7 K, −0.3 % | 106.83 | 202.3 |
| 8 T, 6.7 K, −0.3 % | 238.93 | 452.4 |
| 12 T, 6.7 K, −0.6 % | 73.11 | 138.4 |

- **ITER TF specification.** The spec is > 190 A at 12 T, 4.22 K and 10 µV/m (Table 1, PDF p.3). At the strain peak the law gives 201.3 A, which is 6 % above the spec.
- **Figure comparison.** Fig. 9(a), BEAS II at 4.2 K (zoomed at 330 dpi): the 12 T curve peaks at about 3.73×10⁸ A m⁻², or about 197 A, at εA ≈ +0.37 %. With εI = εA − 0.366 %, the law gives 201.9 A. At 8 T the law gives 2.10×10⁸ A m⁻² at εA = −1.09 % (read about 1.95×10⁸) and 6.36×10⁸ at εA = 0.0 % (read about 6.08×10⁸). The law runs 3–8 % above the data at 8 T, consistent with the dotted ITER-fit line in the figure.
- **Screen comparison.** `contract-screen.json` gives, at 6.7 K / 5.2 K: 8 T 238.93 / 305.43 A and 12 T 106.83 / 152.95 A. I also computed 9–11 T: 197.54/258.10, 162.50/217.79 and 132.56/183.08 A. Every value matches to 0.01 A.
- **Screen strand counts.** The reference offers imply Tcs = 6.758 K at 8 T (n = 68) and 6.707 K at 12 T (n = 226). Both are consistent with the Tcs ≥ 6.7 K rule.
- **Grade gap (informational).** Converted to non-Cu (× 2), BEAS II at 12.04 T, 6.5 K, −0.3 % gives 425 A/mm². Demattè's sizing implies 673 A/mm² (104 950 A / 155.9 mm²) with its Kiswire strand and an undisclosed C. The BEAS II choice is therefore about 37 % below the DEMO design strand. It is a conservative grade choice, and worth a strand-grade sensitivity.

## 4. EU DEMO construction arithmetic — inputs confirmed; derived values need two corrections

- Inspected: Demattè raw.pdf p.2 (§III text, Fig. 1, Table I), p.3 (eq. 1 and sizing text), p.4 (§V and Fig. 5–6). All pages rendered and viewed.
- **Confirmed inputs.** 104.95 kA, 12.04 T, −0.3 %, 6.5 K "for 2 K temperature margin"; 19 × 21 = 399 strands of 1 mm, Cu:non-Cu 1; 20 % void; cos θ = 0.97; 68 × 37.9 mm; Cu 1123.7 mm² (J_Cu 93.4 A/mm²); steel 982.7 mm²; pack 1296 × 411 mm; 142 turns (14.903 MA per coil).
- **Arithmetic checks.** 104 950 / 1123.7 = 93.40 A/mm². 1123.7 − 156.7 (strand Cu) = 967.0 = 2 × 483.5, so 1123.7 mm² is total copper. Cable plus steel is 2600.9 mm², 0.9 % above the 2577.2 mm² envelope.
- **Steel 9.36 mm²/kA: arithmetic confirmed (9.364), basis corrected.** Layer 1 uses the 5 mm jacket that Demattè sets as the "minimum jacket thickness … for manufacturing" (p.2 §IV). Its steel is sized by fabrication, not by stress: the layer-1 membrane stress is about 435 MPa against a 667 MPa limit (Fig. 3). In the source, steel per turn rises toward the low-field layers as stress accumulates: layer 8 is 16.24 mm²/kA and the pack average is 12.66 mm²/kA. Steel therefore does not follow local B inside the source pack.
- **Is linear B scaling defensible?** Scaling steel per kA with B is defensible as a first-order force scaling at fixed geometry: Lorentz load goes as I·B, and I ∝ B. But it is a bounded assumption `[AGENT]`, and the tokamak TF is only a proxy for a 48-coil stellarator.
- **Better basis.** Use the pack-average 12.66 mm²/kA as the reference. Carry 9.36 (layer 1, manufacturing minimum) and 16.24 (layer 8) as bounds.
- **This is consequential.** At 8 T the pack average adds 35.3 mm² of steel, or 46.3 mm² gross. The screen's Nb₃Sn fit margin goes from +44.0 to about −2 mm², so the fit verdict flips. REBCO on the same basis stays positive (about +16 mm²).
- **Insulation fraction 0.237: value confirmed, formula corrected.** 1 − 142 × 68 × 37.9 / (1296 × 411) = 0.313, not 0.237. The 0.237 (0.2368) comes only from the actual per-layer conductor areas: Σ = 406 531 mm², fill 0.763. The contract's source cell ("EU DEMO layer 1") should say pack-wide, per-layer areas.
- **Protection copper 93.4 A/mm²: confirmed in source, but the contract uses I/100 A/mm² (SPC HTS requirement) for basis P.** For Nb₃Sn this understates copper by 6.6 % against the Demattè value it cites. At 8 T that is 11.4 mm² of copper, or 14.9 mm² gross. Use 93.4 A/mm² for Nb₃Sn on basis P, or state the substitution as `[AGENT]`.

## 5. Temperature budget — confirmed

- Inspected: Sedlak 2020 PDF p.3, rendered. The requested Tcs is 6.7 K, "based on 4.5 K inlet temperature, 0.7 K for nuclear heat load, and 1.5 K temperature margin".
- **Why 5.2 K with Tcs ≥ 6.7 K is right.** Tcs depends on (B, I, ε), not on the operating temperature. The rule Tcs ≥ 6.7 K is identical to n·Ic(B, 6.7 K, ε) ≥ I, which is what the screen uses, and to Tcs − 5.2 K ≥ 1.5 K. The 5.2 K point only sets the reported operating fraction; for example Ic(6.7 K)/Ic(5.2 K) = 0.698 at 12 T, −0.3 %.
- **How Demattè's 6.5 K relates.** Sizing at I = Ic(6.5 K) is the same as requiring Tcs = 6.5 K. Demattè states no inlet temperature. Reading the 2 K as margin above a 4.5 K inlet, with nuclear heating included, is inferred.
- Demattè's rule is 0.2 K less strict than Sedlak's. Using it as the sensitivity is correct.

## 6. Range — mostly fair; the support claim is corrected

- **Bruzzone 2015** (efcp150901.pdf PDF p.3 rendered, pp.5–6 text layer). Design point confirmed: 82.4 kA at 13.50 T with a 1.5 K margin. DC tests ran at I ≤ 70 kA (12.35 T background, so Beff ≈ 12.94 T). The "13 T edge" label is fair.
- **BEAS II measured domain** (Fig. 9, zoomed at 300–330 dpi):
    - 4.2 K: 8–14.5 T over the full strain range. The 8 T curve stops at εA ≈ 0.0 %, which is εI ≈ −0.37 %.
    - 8 K: 8–14.5 T, but only up to about 55 A. The 8 T data exist only at εA ≤ −0.67 % (εI ≤ −1.04 %). The 12 T data stop at εA ≈ −0.17 % (εI ≈ −0.54 %). Near εI = −0.3 %, 8 K data exist only at about 13.5 T and above.
    - 10 K: 7.5–14.5 T. 12 K: 6.5–11 T.
    - No data between 4.2 K and 8 K.
- **What this means for 8–12 T.** Every contract point at 5.2–6.7 K and −0.3 % is a temperature interpolation, with no measured neighbour above 4.2 K at those (B, ε). 8 T is the weakest point: no 5–8 K data at any strain with Ic above 55 A, and a slight strain extrapolation even at 4.2 K.
- **Correction to the wording.** The contract's "measured over 8–14.5 T at 4.2 and 8 K" overstates coverage. Say "inside the fitted field range; law interpolation in temperature, with 8 T the weakest point". 8 T can stay "supported" only with that qualifier.
- The 14 T "law-only" label and the above-14.5 T "unsupported" label are fair.

## Must change before modeling

1. **Steel base.** Replace or bound 9.36 mm²/kA. It is layer 1's manufacturing-minimum jacket. Use the pack average, 12.66 mm²/kA, with 9.36–16.24 as the sensitivity. Label B-scaling as `[AGENT]` bounded. This flips the screen's 8 T Nb₃Sn fit verdict.
2. **Insulation fraction.** State 0.237 as the pack-wide, per-layer value, not "layer 1" and not the 142 × 68 × 37.9 formula (which gives 0.313).
3. **Nb₃Sn protection copper.** Use 93.4 A/mm² (the Demattè source value) instead of 100 A/mm², or mark 100 A/mm² as an `[AGENT]` substitution.
4. **Support claims.** Reword the Nb₃Sn support claim per claim 6, and mark the effective-strain transfer to BEAS II as a bounded assumption per claim 2. If any code converts applied strain, it must use εI = εA + εM(table).

Recommended, not blocking: a strand-grade sensitivity, because BEAS II non-Cu Jc is about 37 % below Demattè's design strand at the DEMO point.

## Recheck r2

Scope: my four required changes, the new construction-P calibration and the new reference strand. Inspected: `comparison-contract.md` r2 §§ 2–4 and § 11; Breschi 2017 raw.pdf PDF p.24 (Table III, rendered at 200 dpi); Tsui Fig. 7 caption (PDF p.8, viewed earlier); Demattè Table I and p.4 (viewed earlier). The numbers come from my own re-implementation.

**Overall verdict r2: FINDINGS (small).** All four required items are resolved, and the OST reference strand is confirmed. Two small corrections remain: the calibration residual, and the support and validity wording for the new reference strand. Neither blocks the design.

### Required items

1. **Steel base — resolved.** The reference is the pack average, 12.66 mm²/kA. The variants are 9.36 and 16.24 mm²/kA and a no-scaling case. Field scaling is labelled a bounded assumption, and layer 1's value is attributed to the manufacturing-minimum jacket.
2. **Insulation fraction — resolved.** It is stated as pack-wide: 1 − 406,531/532,656 = 0.2368.
3. **Nb₃Sn protection copper — resolved.** It is 93.4 A/mm² for Nb₃Sn, and the 100 A/mm² used for REBCO is labelled.
4. **Wording and strain — resolved for BEAS II.** The effective-strain transfer is labelled a bounded assumption, and εI = εA + εM(table) is recorded. The support wording now needs two updates for the new reference strand:
    - **(a) OST field coverage.** OST has no 4.2 K data below 10 T (Tsui Fig. 7(a): "10 to 14.5 T at 4.2 K"). At 8 K the 8 T data sit only at εA ≲ −0.7 % and Ic ≲ 60 A (Fig. 7(b)). With OST as the reference, 8–9.5 T at 5.2–6.7 K is interpolation with no 4.2 K anchor. Say so in the text.
    - **(b) Strain validity range.** The range "εI in [−1.0, +0.5] %" is Tsui's applied-strain range. In intrinsic terms it is about [−1.28, +0.22] % for OST and [−1.37, +0.13] % for BEAS II. The evaluated strains (−0.3 % and −0.6 %) are inside both, so no result changes.

### New items

5. **Calibration residual 1.049 mm²/kA — corrected.**
    - Layer-1 inputs: 399 strands of 1 mm (313.37 mm²), so the cable is 313.37 / 0.97 / 0.8 = 403.83 mm². Stabilizer = (104,950 / 93.4 − 156.69) / 0.9 = 1074.42 mm². Steel = 982.7 mm². Envelope = 68 × 37.9 = 2577.2 mm².
    - The residual is 116.25 mm² (1.1077 mm²/kA) if it includes the 0.2 × 30.3 = 6.06 mm² steel strip. It is 110.19 mm² (1.0499 mm²/kA) if the strip is excluded.
    - The contract puts the strip inside the residual, but its 1.049 is the strip-excluded value. As written, the rules give 2571.04 mm², 6.16 mm² short of layer 1, so the "reproduces exactly" test fails. Fix: use 1.1077 mm²/kA, or add an explicit strip term.
    - The test must also pin the steel at 982.7 / 104.95 = 9.3635 mm²/kA. Rounded 9.36 misses by 0.37 mm², and the reference 12.66 gives 2917 mm².
    - Calibrating to the envelope rather than to Table I's cable space (1618.2 mm²) is the right choice, given the 0.9 % inconsistency in Table I.
6. **Reference strand OST — confirmed, with a stronger justification.**
    - **Direct match.** Breschi Table III includes Tsui's OST set verbatim as ITER TF production sample TFEU9: p, q, Ca1, Ca2, ε0a, Bc0 and Tc0 are identical. Its C1 = 28,622.88 A·T equals Tsui's C × 0.528 mm² to within 0.02 %.
    - **ε0a unit resolved.** TFEU9's 0.00207 equals Tsui's 0.207 %, so the column's "[%]" label is wrong and the values are fractions.
    - **Kiswire cross-check.** Treating ε0a as a fraction, Kiswire gives 138.28 A at (12 T, 6.7 K, −0.3 %). OST gives 138.94 A and BEAS II gives 106.83 A, which confirms the coordinator's arithmetic. Reading ε0a as a percentage gives 105.3 A.
    - **Where OST sits in the production range.** Across the ten Table III production sets the value spans 111.98–138.92 A, with a median of 127.2 A. OST is the highest and Kiswire the second highest. BEAS II (106.8 A) sits about 5 % below the lowest production set (BEAS TFEU10–12, 112.0 A).
    - Recommendation: keep OST as the reference because it matches Kiswire, the strand Demattè names. Label it the upper end of ITER TF production, and consider the production median (≈127 A) as a middle sensitivity.

### Advisory (outside scope, not blocking)

Anchor D is not self-consistent at its own design point. At 104.95 kA and 12.04 T, with Demattè's own 399 strands and the reference steel, the rules give 2917 mm² bare and 3823 mm² gross, which exceeds the 3751.1 mm² envelope by 72 mm². OST strands (n = 756, 399 mm² element area) would exceed it by more. Nb₃Sn fit near 12 T on anchor D is therefore decided by the stated no-grading and pack-average-steel assumptions. Report it that way, not as a material result.

## Recheck r3

Scope: contract r3 §§ 2–5 and § 12. I re-rendered Breschi raw.pdf PDF p.24 (Table III) at 300 dpi in two crops and re-read Breschi pp.5, 11 and 19 from the text layer. The numbers come from my own implementation.

**Overall verdict r3: PASS**, with one advisory about the −0.6 % strain case.

### Recheck r2 items

1. **Residual — resolved.** The contract gives 1.1077 mm²/kA including the strip; the exact value is 116.2513 mm², or 1.10768 per kA. The anchor test (399 × 1 mm strands, 93.4 A/mm², steel 9.3635 mm²/kA, residual 1.1077 mm²/kA) gives 2577.2011 mm², a relative error of 4.3e−7. That is inside the stated 1e−6 tolerance.
2. **OST wording — resolved.** "No 4.2 K data below 10 T", and the Breschi fitted domain is labelled unstated, a bounded assumption. Breschi p.5 says only "dedicated measurements … as a function of magnetic field, temperature and strain [11], [12]".
3. **Strain domain — resolved.** The intrinsic range [−1.0, +0.2] % is conservative for OST and BEAS II at the compressive end. The evaluated strains, −0.3 % and −0.6 %, are inside it. Wording nit, not a finding: "shifted by about −0.3 %" would give −1.3 at the lower end, not −1.0.
4. **N2 statement — confirmed.** With pack-average steel and the new residual, Demattè's own layer-1 construction needs 3831.2 mm² gross against 3751.1 mm² available, 2.1 % over.
5. **Common J_Cu of 93.4 A/mm² for both materials.** This is the design reviewer's call. It is consistent with the anchor calibration.

### New reference strand

6. **Transcription — confirmed.**
    - The WST TFCN5–6 row matches the rendered table exactly: 0.578, 2.211, 47.52, 0, 0.00218, 34.22, 16.26, 20823.
    - I also checked the ChMP, Hitachi, Kiswire, Luvata and OST TFUS5R–7R rows against the rendered table. All match.
    - All ten coordinator Ic values at (12 T, 6.7 K, −0.3 %) match mine to 0.01 A.
7. **Ranking and median — confirmed.** The order is BEAS TFEU10–12 111.98 < OST TFUS 121.25 < Luvata 121.41 < Jastec 125.83 < ChMP 126.99 < WST 127.31 < Hitachi 129.11 < OST TFEU11–13 136.87 < Kiswire 138.28 < OST TFEU9 138.92 A. The median is 127.15 A. WST is the upper of the two middle sets, 0.25 % from ChMP, so either is defensible.
8. **Form and units of C1 — confirmed.**
    - Breschi p.11 says the meaning of the parameters is in [11], which p.19 identifies as Bottura & Bordini 2009, the ITER Nb₃Sn production parameterization. That is the same form Tsui cites.
    - C1 is per-strand Ic in A·T. Evidence: TFEU9 reproduces Tsui Table 5(a) with C1 = 28,622.88 A·T, which equals Tsui's C × 0.528 mm² (0.82 mm strand) to within 0.02 %.
    - With Ca2 = 0 the form reduces cleanly (εsh = 0, peak at εI = 0).
    - The ε0a column is fractions, as established in r2.
9. **WST at 6 T, 4.2 K, εI = 0 — confirmed.** Ic = 680.48 A. It is correctly labelled a price conversion outside the supported field.

### Advisory (not blocking)

WST is the production median only near the reference strain. It ranks 5th of 10 at (8 T, 6.7 K, −0.3 %) and 7th at 13 T. But at (12 T, 6.7 K, −0.6 %) it ranks 3rd of 10: 61.2 A against a production median of 73.1 A, a range of 58.0–81.4 A. Its strain sensitivity (Ca2 = 0) is stronger than most sets. So the −0.6 % sensitivity case mixes a strain effect with a strand-grade effect. Report the production spread at −0.6 % alongside it, or state that "median" is defined at the reference point.
