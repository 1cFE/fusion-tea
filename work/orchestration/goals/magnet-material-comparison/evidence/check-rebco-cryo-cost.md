# Independent check B: REBCO, cryogenics, cost (T-004)

Checker: fresh agent, no authorship of the checked work. Brief: `evidence/briefs/t004-check-rebco-cryo-cost.md`. Originals were rendered or read from each PDF's own page or text layer (PyMuPDF), not from the author's summaries. Scripts and renders stayed in the session scratch directory.

## Overall verdict: FINDINGS

The source readings and arithmetic hold up. Two things must change before modeling:

1. **Refrigerator input-power equivalence (claim 4b): write the factor so its direction is unambiguous.** A 20 K rating becomes a 4.5 K-equivalent rating by multiplying by the ratio of Carnot specific power, 14.0/65.7 = 0.213. The brief writes this as `COP_Carnot,20K / COP_Carnot,4.5K`. With the usual definition COP = Q/W, that ratio is 4.69, which is inverted. The evidence (`cryo.md:24`, "specific power ... ratio 4.69") uses W/W, where the factor comes out right. The model and contract should state `R_equiv = rating × (300−20)/20 ÷ (300−4.5)/4.5 = 0.213 × rating` explicitly. Getting it inverted gives a 22× error in rating (4.69²).
2. **Price-per-metre provenance (claim 6).**
   - The Nb₃Sn reference of 8 USD/m is supported by the per-kg sources, not by Chislett-McDonald's 8.0 USD/kA·m. Those are different units. At 6 T and 4.2 K the Chislett value converts to about 5 USD/m.
   - State both ranges in 2021 USD.
   - Label REBCO's 30 USD/m reference as Chislett's *target* price. The 2021 market price is about 70–90 USD/m.

## Per-claim verdicts

### 1. REBCO 20 K field shape: confirmed

**Inspected:** Molodyk 2021 `raw.pdf` p.3. I extracted Fig. 1 as an embedded image (xref 64, 1805×858 px) and calibrated the axes on the gridlines: x₀ = 141 px, 23.24 px/T; y₀ = 660.5 px, 0.3578 px/A. The 1000 A/mm² dashed line lands at 225 A, which checks the calibration. I located marker centres by colour segmentation.

**Geneva 20 K open circles:** 8 T 475 A, 10 T 418 A, 12 T 366 A, 15 T 303 A, 20 T 226 A.

**Ic(B)/Ic(20 T), mine against the author's:**

| Field | Mine | Author |
|---|---|---|
| 8 T | 2.10 | 2.11 |
| 10 T | 1.85 | 1.85 |
| 12 T | 1.62 | 1.61 |
| 15 T | 1.34 | 1.33 |

All agree within 1%.

**Second sample.** The Tohoku 20 K squares (Ic(20 T) ≈ 275 A) give 2.17, 1.87, 1.64 and 1.35. The NHMFL 20 K data stop at about 15 T.

**Anchor.** The normalized shape agrees within 3% across two samples whose absolute Ic differs by 22%. That supports transferring the shape to the production average. The average itself is 1.13 × 175 A = 198 A (`output.md:77`, `:137`). I checked that 175 A applies to 4 mm tape: 1.86 MA/cm² × 2.35 µm × 4 mm = 175 A. So the anchor is defensible.

**Caveat.** Part of the production 20 T data were extrapolated from 0–12 T (`output.md:153`).

**B∥c worst orientation: confirmed.** The Fig. 2 caption (p.3) says: "Within the accuracy of measurement, the minimum value of Ic for all field orientations is at B//c." The 20 K curves are flat from −40° to +20°.

### 2. REBCO temperature law: confirmed

**Inspected:** Senatore `raw.pdf` p.6.

- **Eq. (1).** The form Jc(T,B) = Jc(0,B)·exp(−T/T*) is as printed. It holds to about 50 K at θ = 0°, with error below 2%.
- **Orientation.** θ = 0° means field normal to the tape, which is B∥c (`output.md:60`).
- **Fig. 3 at θ = 0°, 8–19 T, read by me:** T* spans 17–33 K.

| Maker | T* at 8 T → 19 T |
|---|---|
| AMSC | 29 → 25.5 K |
| Bruker | 27 → 24 K |
| Fujikura | 33 → 28.5 K (15 T) |
| SuNAM | 24.5 → 18.5 K |
| SuperOx | 25 → 17 K |
| SuperPower | 28.5 → 23.5 K |

**T* derived from Molodyk at 20 T, my digitization:**

- Geneva: 15.8 K / ln(458.4/226.4) = 22.4 K.
- Tohoku: 15.8 K / ln(577/275) = 21.4 K.

So T* ≈ 22 K is confirmed, and the 17 and 33 K sensitivities bracket the source range.

### 3. REBCO construction and degradation: confirmed

- **Stellaris Table 7** (`page_021_table_0.png`): 9 / 35 / 12 / 36 / 8 %, exactly as stated.
- **SPC Table I** (`knowledge/raw/wpmag16576.pdf` p.5, printed p.3): TF conductor is 60 kA, 12 T, 4.5 K inlet, 100 A/mm² in copper (the CS value is 120).
  - Note: this is a 4.5 K requirement extrapolated from the Nb₃Sn DEMO design. Applying it at 20 K is a transfer, not a stated 20 K rule.
- **SPC cycling** (`output.md:101`): "about 10% for the Superpower conductor and 20% for the SuperOx conductor." The SuperOx loss is tied to strand bending damage (`:103`).
- **VIPER** (`knowledge/raw/viper2020.pdf` text layer):
  - p.3: fabrication loss from the ideal design Ic is below 5%.
  - p.4: cycling loss asymptotes at 2.0–4.1%.
  - Combined, the retained fraction is about 0.91–0.98.

**Is 0.90 fair?** Yes. The 0.90 reference sits at the worst end of VIPER and equals SPC-SuperPower. The 0.80 sensitivity equals SPC-SuperOx, and 0.95 is a mid-VIPER value.

**Limit.** Neither test reached the matched duty's field or I×B load. VIPER went to 10.9 T and 382 kN/m per stack.

### 4. Refrigerator efficiency and capital: (a) confirmed; (b) corrected (factor direction, finding 1)

**Green 2015** (`knowledge/raw/green2015_iop_publisher.pdf`, PDF p.3):

- Eq. (1): C(M$) ≈ 3.1 R(kW)^0.65. It is 2015 dollars (2007 costs escalated by 20%), for refrigerators above 100 W.
- Eq. (2): η(%) = 15.5 R(kW)^0.23.
- Both fits use only 4.2/4.5 K plants. The Fig. 1 and Fig. 2 data span about 0.01–35 kW, with no machines built after 2007.

**Strobridge 1974** (`knowledge/raw/nbstechnicalnote655.pdf`):

- Fig. 1 (PDF p.11, printed p.5) plots percent of Carnot against refrigeration capacity, with one curve for every temperature band.
- PDF pp.10 and 12 say the 10–30 K data "refute" the idea that higher-temperature refrigerators are more efficient: "the losses relative to ideal are proportionally the same."
- Eq. (3) (PDF p.15, printed p.9): C = 6000 P^0.7 dollars, where P is installed input power in kW, for 1.8–90 K. The text adds: "Adjustments have not been made for the change in value of the dollar."

**(a) One η law for both temperatures, evaluated at cooling capacity.** Defensible. It is Strobridge's own presentation.

- Condition: keep the stage capacity inside Green's roughly 0.1–35 kW data range.
- Caveat: Strobridge notes that 30–90 K units at 10–1000 W are more efficient.

**(b) Costing a 20 K plant by input-power equivalence.** Defensible in concept, because Strobridge's cost law is in input power across 1.8–90 K. It needs two changes or disclosures:

- The factor must be 0.213 (finding 1).
- Green's laws imply cost ∝ P^(0.65/0.77) = P^0.84, while Strobridge gives P^0.7. That difference and the size-dependent η(R) make the equivalence approximate. The capacity-basis sensitivity bounds this.

### 5. Cold loads: confirmed

**Ballarino** (`knowledge/raw/T005-ballarino.pdf` pp.1–2, Table 1): conduction-cooled leads carry 47 W/kA at 4.2 K and 45 W/kA at 77 K. The minimum-heat-leak (Wiedemann–Franz) form Q/I = √(L₀(T_h² − T_c²)), with L₀ = 2.45×10⁻⁸ W·Ω/K², reproduces both table values and gives the 20 K value:

| Cold end | Q/I |
|---|---|
| 4.2 K | 46.95 W/kA |
| 20 K | 46.85 W/kA |
| 77 K | 45.4 W/kA |

**Končar** (`knowledge/raw/koncar17578.pdf` p.3, Eq. 1): Q = σ·A_c·ε_r·(T_h⁴ − T_c⁴).

- With an 80 K shield: (80⁴ − 20⁴)/(80⁴ − 4⁴) = 0.9961.
- With a 77 K shield against 4.5 K: 0.9955.
- The 0.996 figure is derived, not printed in the paper.

**NIST 316 fit** (`raw.html` checked against `output.md`): coefficients a–i as tabulated; data range 4–300 K; fit error 2%. Integrating the conductivity:

| Range | ∫k dT |
|---|---|
| 4.5 → 77 K | 326.0 W/m |
| 20 → 77 K | 307.4 W/m |
| Ratio (20 K / 4.5 K) | 0.943 |

Spot values: k(4.5 K) = 0.32, k(20 K) = 2.17, k(77 K) = 7.92 W/m·K.

### 6. Prices: corrected (see finding 2)

**Sources, as found:**

- **Chislett-McDonald** (`knowledge/raw/chislett2022.pdf` p.17): "8.0 $/kA m (6 T, and 4.2 K) for Nb3Sn strands [138] (in 2021 costs). Currently, REBCO tapes are priced at ≈80 $/kA m (6 T, 4.2 K) with the aim to reduce this to 30". The 30 is repeated as "expected" on p.33.
- **Cooley & Pong** (PDF p.3): $80/m for 100 A (77 K, self-field) and 400 A at 20 T, 4.2 K. That is $200/kA·m for a 4 mm × 0.25 mm tape including 100 µm steel and 100 µm Cu.
- **PROCESS:** `s_cref[17] = 526.0e6`, "ITER Nb3Sn SC strands cost (2014 $)". It scales with `s_kref = 210.0e3` kg of "total mass of Nb3Sn".

**Nb₃Sn, per metre of 0.82 mm strand.** Area is 0.528 mm². At an assumed density of 8.9 g/cm³ that is 4.70 g/m.

| Source reading | USD/m (source year) | USD/m (2021) |
|---|---|---|
| PROCESS, 210 t taken as whole-strand mass (2505 USD/kg) | 11.8 (2014) | 13.5 |
| PROCESS, 210 t taken as non-Cu mass, strand ≈ 420–500 t (1052–1252 USD/kg) | 4.9–5.9 (2014) | 5.7–6.7 |
| Cooley & Pong, 1500–2000 USD/kg | 7.0–9.4 (2016) | 7.9–10.6 |
| Chislett 8.0 USD/kA·m × Ic(6 T, 4.2 K) | — | ≈4.4–5.2 |

- The non-Cu reading of the 210 t is consistent with ITER's 384–500 t of TF strand.
- **The Chislett row needs an Ic value.** It needs the strand Ic at 6 T and 4.2 K. My estimate of about 0.55–0.65 kA is only a Kramer-type ratio of about 2.9 applied to an assumed Ic(12 T) of 190–230 A. That is not a registered-source value. The model must compute it from the Tsui & Hampshire law at a stated strain.
- **Verdict on the range.** 5–11 USD/m (2021) is a fair reading under the non-Cu interpretation. The reference of 8 comes from Cooley & Pong per-kg, not from Chislett.

**REBCO, per metre of 4 mm × 56 µm tape.** Chislett's prices need the tape Ic at 6 T and 4.2 K (B∥c). From my Fig. 1a digitization:

- Geneva: 978 A.
- Scaled to the production average (× 198/226): about 856 A.
- Tohoku: about 1.25 kA.

Converted to per-metre prices:

| Chislett price | USD/m |
|---|---|
| 80 USD/kA·m (2021 market) | 69–100 |
| 30 USD/kA·m (target) | 26–38 |
| 10 USD/kA·m (further reduction) | 8.6–12.5 |

Cooley & Pong's price needs no Ic if taken per metre: 80 USD/m (2016) → 90 USD/m (2021). If converted per kA·m at 20 T and 4.2 K instead, the production tape carries about 401 A, which gives the same value.

**Verdict on the range.** 10–100 USD/m is fair. The 30 USD/m reference is the aim price, so label it that way and treat the present price (about 80 USD/m) as a named case.

### 7. Currency: confirmed

**Inspected:** Minneapolis Fed CPI extraction (`output.md`). It has 114 annual rows covering 1974 through 2022.

| Year | CPI | Factor to 2021 USD |
|---|---|---|
| 1974 | 49.3 | ×5.50 |
| 1990 | 130.7 | ×2.07 (Chislett uses 2.13) |
| 2014 | 236.7 | ×1.145 |
| 2015 | 237.0 | ×1.143 |
| 2016 | 240.0 | ×1.129 |
| 2021 | 271.0 | — |

**Caveats.**

- Strobridge's Eq. 3 dollars are unadjusted, mixed-year data (p.15), so the 1974 conversion is nominal.
- Green's "2015 dollars" are 2007 costs × 1.2.

## Recheck r2

Scope: `comparison-contract.md` r2, § 6, § 7, § 11 and the § 4 copper line. I rechecked each item against the original pages.

### Required changes

**Finding 1, the 20 K input-power factor: resolved.** § 6 now writes out R_equiv = rating × (300 − 20)/20 ÷ (300 − 4.5)/4.5 = 14.00/65.67 = 0.2132. I recomputed 0.21319. The direction is correct. The same factor is used for the η(R_equiv) sensitivity, and the capacity basis (R_equiv = rating) is kept as the other sensitivity.

**Finding 2, price labels: resolved.** All prices are now stated in 2021 USD.

- **Nb₃Sn reference 8 USD/m.** It is now attributed to the Cooley & Pong per-kg price (7.9–10.6 USD/m).
- **REBCO reference 80 USD/m.** It is now labelled the 2021 market price, with target 30 and volume 10. The Chislett-McDonald text supports these labels (PDF p.17–18): "aim to reduce this to 30 $/kA m ... in the near future. Increased demand could reduce this even further to 10 $/kA m."
- **CPI factors.** 1974 ×5.50, 1990 ×2.07 and 2014 ×1.145 match the series. The manufacturing allowance converts correctly: 985 × 1.145 = 1128 USD/m.

Advisory, not blocking: the Nb₃Sn lower bound of 4.4 USD/m is my rough estimate for a bronze-route strand. It is not a value computed from the law. r2 changes the reference strand to OST, and OST has higher Ic at 6 T and 4.2 K than a bronze-route strand. The Chislett conversion should therefore be recomputed from the law's Ic for OST, as § 7 already says. It will likely come out near 6 USD/m.

### New in r2, within this check's area

**Lead cold ends: resolved.** The form is f_lead × n_leads × I × √(L₀(77² − T²)). It is the same minimum-heat-leak expression that reproduces Ballarino Table 1 (47 W/kA at 4.2 K, 45 W/kA at 77 K), applied to the 77 K → T segment. I recomputed 12.03 W/kA at 4.5 K and 11.64 W/kA at 20 K, as stated. Two further checks:

- The anchor S inventory sums to 21.94 kW, against the stated 21.93 kW.
- The nuclear term is 35.5 × 136.56 = 4.85 kW, as stated.

Note: this form is a resistive-lead optimum. An HTS lower section would carry a smaller load. The form is applied equally to both materials.

**Carnot at the supply temperature: resolved.** The specific power is 65.67 W/W at 4.5 K and 14.00 W/W at 20 K. Refrigerator work is set by the temperature at which the heat is removed, so this is the right basis.

**SPC 100 A/mm² copper at 20 K: resolved.** § 4 states that the value is given at 4.5 K and labels its use at 20 K a bounded assumption.

**Anchor D cold loads: resolved.** The source is Končar Table 1, base case with 80 K shields and 4 K magnets, rendered from PDF pp.4–5:

| Term | Load |
|---|---|
| Radiation | 1.3 kW |
| Thermal-anchor conduction | 4.4 kW |
| VVTS-support conduction | 0.2 kW |
| Magnet total | 5.9 kW |

So the contract's 4.6 kW is 4.4 + 0.2. The table covers the whole DEMO magnet system, and r2 labels attributing it all to the TF coils as an upper assumption. Scaling the thermal-anchor term by the 316 stainless conductivity integral (ratio 0.943) assumes a 316-like anchor path. That is a small effect.

### Overall verdict on r2: PASS

Both required changes are resolved. One advisory remains: recompute the Nb₃Sn lower price bound from the law for the OST strand.
