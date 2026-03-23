# Review: Laser ICF - Liquid Jet Target (D-D)

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 4 listed (iter-01/sources/) + dossier.md (found at phase_1a/research/03-laser-icf-liquid-jet-target/dossier.md — cited but not in review prompt's listed sources)

---

## Citation Verification

### CV-1: IP notice quote
- **Source cited:** arxiv-2503-nanoshell-paper.md §IP Notice
- **Status:** PARTIAL MATCH
- **Actual text:** "Systems, methods, and underlying principles...are the intellectual property of Cortex Fusion Systems, Inc."
- **Notes:** Analysis inserts "for nuclear fusion using plasmonic field enhancement" between "principles" and "are" (inside the quoted span). This phrase does not appear in the source extraction; the source just has "..." for the elided portion. The core meaning is preserved but the interpolated clause is unverified. Minor concern.

### CV-2: "Many practical challenges exist"
- **Source cited:** arxiv-2503-nanoshell-paper.md §What's NOT Addressed
- **Status:** FOUND
- **Actual text:** "Many practical challenges exist — acknowledged but not detailed"
- **Notes:** Exact match.

### CV-3: Cambridge kHz baseline ~10^5 n/s
- **Source cited:** kHz-liquid-sheet-fusion-paper.md §Key Technical Details
- **Status:** FOUND
- **Actual text:** "D-D fusion neutron production verified, ~10^5 neutrons/second"
- **Notes:** Exact match. Analysis correctly identifies this as a different apparatus from Cortex.

### CV-4: "currently building the first electricity-producing fusion reactor"
- **Source cited:** cortex-fusion-website.md §Status
- **Status:** FOUND
- **Actual text:** "Claims to be 'currently building the first electricity-producing fusion reactor'"
- **Notes:** Exact match.

### CV-5: "Energy per D-D fusion: 3333 MeV"
- **Source cited:** arxiv-2503-nanoshell-paper.md §Fusion Parameters
- **Status:** FOUND
- **Actual text:** "Energy per D-D fusion: 3333 MeV (note: this seems high — standard D-D is 3.27 MeV for D+D→He3+n or 4.03 MeV for D+D→T+p; paper may be calculating something differently or including secondary reactions)"
- **Notes:** The source extraction itself flags this as anomalous. Correctly reported.

### CV-6: "Sub-micrometer scale target is extremely stable and can operate at kHz or above"
- **Source cited:** kHz-liquid-sheet-fusion-paper.md §Key Technical Details
- **Status:** FOUND
- **Actual text:** "Sub-micrometer scale target is extremely stable and can operate at kHz or above"
- **Notes:** Exact match.

### CV-7: Cambridge laser specs "1-kHz Ti:sapphire laser, 8 mJ, 40 fs pulses; Intensity: ~5×10^18 W/cm²"
- **Source cited:** kHz-liquid-sheet-fusion-paper.md §Key Technical Details
- **Status:** FOUND
- **Actual text:** "Laser: 1-kHz Ti:sapphire laser, 8 mJ, 40 fs pulses; Intensity: ~5×10^18 W/cm²"
- **Notes:** Exact match.

### CV-8: "1 MHz rep rate, 1 million nanoshells ignited per pulse"
- **Source cited:** arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters
- **Status:** FOUND
- **Actual text:** "1 MHz rep rate, 1 million nanoshells ignited per pulse"
- **Notes:** Exact match.

### CV-9: Neutron flux projection and "nine orders of magnitude" qualifier
- **Source cited:** arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters
- **Status:** FOUND
- **Actual text:** "Neutron flux: ~10^19 n/s ('exceeds current devices by nine orders of magnitude')"
- **Notes:** Verified. The analysis correctly quotes this as "nine orders of magnitude" when attributing the paper's own claim, while independently calculating "14 orders of magnitude" for the Cambridge-to-Cortex gap — these use different baselines and are both correct (see Consistency Check).

### CV-10: "Target repetition frequency for reactor: 1 MHz"
- **Source cited:** arxiv-2503-nanoshell-paper.md §Laser Specifications
- **Status:** FOUND
- **Actual text:** "Target repetition frequency for reactor: 1 MHz"
- **Notes:** Exact match.

### CV-11: Q~100 with "30% conversion efficiency, 3 kW laser consumption"
- **Source cited:** arxiv-2503-nanoshell-paper.md §Projected Reactor Parameters
- **Status:** FOUND
- **Actual text:** "Q-factor: ~100 (with 30% conversion efficiency, 3 kW laser consumption)"
- **Notes:** Exact match.

### CV-12: Fusion rate per nanoshell ~10^7 s⁻¹ and ~1 μW power
- **Source cited:** arxiv-2503-nanoshell-paper.md §Fusion Parameters
- **Status:** FOUND
- **Actual text:** "Fusion rate per nanoshell: ~10^7 s^-1; Power per nanoshell: ~1 μW"
- **Notes:** Exact match. Note: these two numbers from the source are internally inconsistent — 10^7 s⁻¹ × 3333 MeV ≈ 0.5 mW (not 1 μW). This is a source-level inconsistency, not an analysis error.

### CV-13: "Typical radius: ~100 nm or larger" and thin-shell regime
- **Source cited:** arxiv-2503-nanoshell-paper.md §Target Design
- **Status:** FOUND
- **Actual text:** "Typical radius: ~100 nm or larger; Inner radius R1, outer radius R2 (thin-shell regime: thickness ≤ skin depth)"
- **Notes:** Exact match. Analysis derives δ ≈ 25 nm from "thickness ≤ skin depth at optical frequencies" — this is a reasonable physical estimate (skin depth of gold at ~1 μm ≈ 20–30 nm) but the source does not give an explicit numerical value for δ. The derivation is labelled [inferred].

### CV-14: Website kHz rep rate claim
- **Source cited:** cortex-fusion-website.md §Technology Description
- **Status:** FOUND
- **Actual text:** "Repetition rate: 'thousands of pulses per second' (kHz regime)"
- **Notes:** Exact match.

### CV-15: dossier.md §Energy Capture citation
- **Source cited:** dossier.md §Energy Capture
- **Status:** FOUND (file exists; not in review prompt's listed sources)
- **Actual text (dossier §Energy Capture Notes):** "No disclosed energy conversion method."
- **Notes:** dossier.md exists at `phase_1a/research/03-laser-icf-liquid-jet-target/dossier.md` and was generated by the Phase 1a pipeline. The citation is accurate. The file is not listed among the review prompt's 4 source documents — an omission in the review brief, not an error in the analysis.

### CV-16: dossier.md §Neutron Management citation
- **Source cited:** dossier.md §Neutron Management
- **Status:** FOUND
- **Actual text (dossier §Neutron Management Notes):** "Not addressed by any Cortex source. D-D neutrons are 2.45 MeV (not 14 MeV)... the paper claims 10^19 n/s neutron flux, which would require substantial shielding infrastructure if achieved."
- **Notes:** Exact match for the paraphrased claim. Analysis correctly attributes this to dossier inference, not primary source.

### CV-17: Levitt 2023 paper "framework paper, no reactor engineering"
- **Source cited:** arxiv-2308-levitt-quantum-control.md §Summary
- **Status:** FOUND
- **Actual text:** "No specific reactor engineering details"
- **Notes:** The analysis's characterization matches the source.

---

## Calculation Verification

### CALC-1: Mass per nanoshell
- **Claimed:** m ≈ ρ_Au × 4π × R² × δ ≈ 19,300 × 4π × (100×10⁻⁹)² × 25×10⁻⁹ ≈ **6 × 10⁻¹⁸ kg**
- **Re-derived:**
  - Volume = 4π × R² × δ = 4π × (10⁻⁷ m)² × (2.5×10⁻⁸ m)
  - = 12.566 × 10⁻¹⁴ × 2.5×10⁻⁸ = 3.14 × 10⁻²¹ m³
  - m = 19,300 kg/m³ × 3.14×10⁻²¹ m³ = **6.06 × 10⁻¹⁷ kg**
- **Status:** MISMATCH
- **Notes:** The arithmetic is off by exactly 10×. The result stated in the analysis is 6×10⁻¹⁸ kg; the correct value is ~6×10⁻¹⁷ kg. This error propagates through the entire gold consumption chain (see CALC-2, CALC-3, CALC-4).

### CALC-2: Gold mass per pulse
- **Claimed:** "~6 × 10⁻⁶ g of gold per pulse" (10^6 nanoshells/pulse × mass per nanoshell)
- **Re-derived:**
  - Using analysis's own stated value: 6×10⁻¹⁸ kg × 10⁶ = 6×10⁻¹² kg = 6×10⁻⁹ g/pulse
  - Using correct per-nanoshell mass: 6.06×10⁻¹⁷ kg × 10⁶ = 6.06×10⁻¹¹ kg = 6.06×10⁻⁸ g/pulse
- **Status:** MISMATCH
- **Notes:** The stated 6×10⁻⁶ g/pulse is inconsistent with the stated per-nanoshell mass by 1000×, and inconsistent with the correct per-nanoshell mass by 100×. The per-pulse figure appears to have an additional undocumented jump. The correct per-pulse mass is ~6×10⁻⁸ g, not 6×10⁻⁶ g.

### CALC-3: Annual gold consumption
- **Claimed:** "~6 g/s at 1 MHz" → "roughly 190 tonnes of gold per year"
- **Re-derived:**
  - Correct mass flow: 6.06×10⁻¹⁷ kg/shell × 10⁶ shells/pulse × 10⁶ pulses/s = 6.06×10⁻⁵ kg/s = **60 mg/s**
  - Annual: 0.06 g/s × 3.156×10⁷ s/yr = **~1.9 tonnes/year**
  - Using analysis's claimed 6 g/s: 6 g/s × 3.156×10⁷ s/yr = ~190 tonnes/year (internally consistent with stated 6 g/s, but the 6 g/s is wrong)
- **Status:** MISMATCH
- **Notes:** The "190 t/yr" figure is consistent with the stated 6 g/s flow rate, but 6 g/s is itself 100× too large. The correct annual consumption is ~1.9 t/yr — still non-trivial but not "~5% of world production" (it would be ~0.05%). The directional concern (recycling is critical) remains valid; the magnitude is overstated by ~100×.

### CALC-4: Gold cost per hour
- **Claimed:** "~$0.5M/hour" for unrecovered gold at "6 g/s" and "~$80,000–90,000/kg (early 2026)"
- **Re-derived:**
  - 6 g/s × 3,600 s/hr = 21,600 g/hr = 21.6 kg/hr
  - 21.6 kg × $85,000/kg = **~$1.84M/hr** (not $0.5M/hr)
  - At correct 60 mg/s: 216 g/hr × $85/g = **~$18,400/hr**
- **Status:** MISMATCH
- **Notes:** The $0.5M/hr figure is inconsistent with the stated 6 g/s flow rate and the stated $80–90k/kg price — it would require a price of roughly $23/g ($23,000/kg, circa 2022). The cost estimate appears to use an outdated gold price. Neither the stated flow rate nor the stated gold price, taken together, yields $0.5M/hr. At the correct mass flow and current gold price the hourly cost is ~$18k/hr — serious but not $0.5M/hr.

### CALC-5: 14 orders of magnitude (Cambridge to Cortex)
- **Claimed:** "The closest independent experimental analogue achieves 10^5 n/s... 14 orders of magnitude below the projected flux [10^19 n/s]"
- **Re-derived:** 10^19 / 10^5 = 10^14 → 14 orders of magnitude.
- **Status:** MATCH
- **Notes:** Arithmetic correct. Distinct from the paper's own "nine orders" claim, which uses a different baseline (see CV-9, Consistency Check).

### CALC-6: D-D average energy per reaction
- **Claimed:** "approximately 1000× the standard value of ~3.65 MeV"
- **Re-derived:**
  - D+D → He-3 + n: 3.27 MeV (50%)
  - D+D → T + p: 4.03 MeV (50%)
  - Average: 3.65 MeV ✓
  - 3333 MeV / 3.65 MeV ≈ 913× (analysis says "approximately 1000×")
- **Status:** MATCH (within stated approximation)
- **Notes:** "Approximately 1000×" is an acceptable rounding of 913×.

### CALC-7: Power balance (model_setup.py comment)
- **Claimed:** p_fus ≈ 1000 / (0.35 - 0.10) ≈ 4000 MW; p_implosion ≈ 40 MW; Q_eng ≈ 3.5
- **Re-derived:**
  - P_fus = NET_ELECTRIC / (η_th − 1/(Q_plasma × η_pin)) = 1000 / (0.35 − 1/10) = 1000/0.25 = 4000 MW ✓
  - P_laser_output = P_fus / Q = 4000/100 = 40 MW ✓
  - P_laser_electric = P_laser_output / η_pin = 40/0.10 = 400 MW
  - P_gross = 4000 × 0.35 = 1400 MW
  - Q_eng = 1400/400 = 3.5 ✓
- **Status:** MATCH
- **Notes:** Power balance is internally self-consistent.

---

## Model Setup Audit

### MSA-1: NET_ELECTRIC_MW = 1000.0
- **Value:** 1000.0 MW
- **Source:** analysis.md §Section 5 — "~1 MW" projected for single unit; 1 GWe is framework reference scale
- **Status:** TRACED
- **Notes:** Correctly flagged as "REFERENCE ONLY / not a validated commercial target." The distinction is clearly documented.

### MSA-2: AVAILABILITY = 0.40
- **Value:** 0.40
- **Source:** analysis.md §Section 5 Missing Params — "truly-unknown, blocking"
- **Status:** TRACED
- **Notes:** Conservative proxy appropriate for TRL 1. Well-documented.

### MSA-3: P_IMPLOSION_MW = 40.0
- **Value:** 40.0 MW
- **Source:** analysis.md §Section 5 "Laser input power at Q~100: ~3 kW" scaled to 1 GWe
- **Status:** TRACED
- **Notes:** Derivation (3 kW → 1 MW fusion, scale to 1 GWe) is correct per CALC-7. Flagged as uncertain.

### MSA-4: P_IGNITION_MW = 0.0
- **Value:** 0.0 MW
- **Source:** analysis.md §Section 3 — single femtosecond OAM beam serves as both driver and igniter
- **Status:** TRACED
- **Notes:** Correct for this concept. Override from YAML default of 0.1 MW is justified.

### MSA-5: ETA_TH = 0.35
- **Value:** 0.35
- **Source:** analysis.md §Section 2 Challenge 1 — "No energy capture architecture disclosed"
- **Status:** TRACED
- **Notes:** Correctly flagged as BLOCKING UNCERTAIN / placeholder. Reduced from YAML default (0.46).

### MSA-6: ETA_PIN1/2 = 0.10
- **Value:** 0.10
- **Source:** analysis.md §Section 4 — Ti:sapphire 5–10%, Yb-fiber up to 30%
- **Status:** TRACED
- **Notes:** 0.10 is the upper bound for Ti:sapphire and conservative for Yb-fiber. Consistent with YAML default.

### MSA-7: MN = 1.05
- **Value:** 1.05
- **Source:** analysis.md §Section 2 Challenge 4 — neutron management unaddressed; no breeding blanket
- **Status:** TRACED
- **Notes:** Reduced from YAML 1.1. Rationale is clear.

### MSA-8: P_CRYO = 0.0
- **Value:** 0.0 MW
- **Source:** analysis.md §Section 3 — "No magnets... no cryogenics"
- **Status:** TRACED
- **Notes:** Correct for D-D liquid jet concept. Override from YAML 0.5 MW.

### MSA-9: P_TRIT = 0.0
- **Value:** 0.0 MW
- **Source:** analysis.md §Section 4 — "No tritium supply or breeding required"
- **Status:** TRACED
- **Notes:** Correct for D-D fuel cycle. Override from YAML 10.0 MW is well-justified.

### MSA-10: P_TARGET = 2.0
- **Value:** 2.0 MW
- **Source:** analysis.md §Section 4 — "Gold nanoshell synthesis at industrial scale is not characterized"
- **Status:** TRACED
- **Notes:** Doubled from YAML 1.0 MW. Rationale (nanoshell synthesis unknowns) is documented. Caveated as uncertain.

### MSA-11: C220103 (coils/magnets) = $0.0 M
- **Value:** $0.0 M
- **Source:** analysis.md §Section 7 — "No external magnets... fundamentally different from MFE concepts"
- **Status:** TRACED
- **Notes:** Appropriate. No superconducting or resistive coils in concept.

### MSA-12: C220108 (divertor) = $0.0 M
- **Value:** $0.0 M
- **Source:** No divertor applicable to IFE pulsed concept
- **Status:** TRACED
- **Notes:** Appropriate for any IFE concept. Not MFE-specific.

### MSA-13: C220112 (isotope separation) = $0.0 M
- **Value:** $0.0 M
- **Source:** analysis.md §Section 4 — D2O from CANDU; no Li-6 enrichment needed
- **Status:** TRACED
- **Notes:** Correct for D-D cycle. Well-justified.

### MSA-14: Radial build (PLASMA_T, BLANKET_T, etc.)
- **Value:** 4.0 m / 0.80 m / 0.25 m / 0.15 m / 0.10 m (all YAML defaults)
- **Source:** "No Cortex chamber design has been disclosed"
- **Status:** TRACED
- **Notes:** All correctly flagged as DEFAULT/PLACEHOLDER. Comment explicitly notes no chamber architecture exists.

### MSA-15: NOAK = False (FOAK)
- **Value:** False → 10% contingency
- **Source:** analysis.md §Section 3 — TRL 1 concept with no experimental results
- **Status:** TRACED
- **Notes:** FOAK is correct for a TRL 1 concept. Appropriate choice.

---

## Consistency Check

**Section 5 vs. Section 2 narrative:** All parameter table values in Section 5 are consistent with claims made in Section 2. The confidence ratings ("low" for all projected parameters) align with the blocking challenges described. The "high" confidence rating for Neutron energy (2.45 MeV) is correct — this is standard D-D physics, not a Cortex-specific claim.

**TRL ratings vs. challenges:** Section 3 TRL assignments are consistent with Section 2. Energy Capture is TRL 0 (no architecture) — consistent with Challenge 1 (blocking). Plasmonic Nanoshell Fusion is TRL 1 — consistent with Challenge 2 (no experimental validation). The liquid jet target at TRL 2–3 correctly uses the Cambridge paper as the partial analogue while noting Cortex's specific implementation is undisclosed.

**Model setup vs. parameter table:** All model parameters that appear in both the analysis and model_setup.py are consistent. P_IMPLOSION scaled correctly from the "3 kW → 1 MW" ratio. ETA_TH, ETA_PIN, MN all consistent with analysis text. Zero overrides all justified by analysis.

**"Nine orders" (paper) vs. "14 orders" (analysis):** Both figures are cited correctly — they use different baselines. The paper's "nine orders" refers to 10^19 n/s vs. "current devices" (likely large fission neutron sources at ~10^10 n/s). The analysis's "14 orders" refers to 10^19 vs. the Cambridge kHz experiment (10^5 n/s). Neither is wrong. A clarifying note would help readers who might conflate them.

**Q ambiguity (engineering vs. plasma Q):** The paper's Q~100 is an engineering Q (electrical output / electrical laser input), derived from: 1 MW fusion × 30% η_th = 300 kW output / 3 kW laser input = Q_eng = 100. The plasma Q (P_fusion / P_laser_optical) would be ~333 (assuming η_pin = 0.10: P_optical = 0.3 kW, Q_sci = 1000/0.3 ≈ 3333). The model_setup.py applies Q=100 as Q_plasma in the power balance. This makes the model conservative relative to what the paper implies — the model assumes more recirculating power than the paper's own Q_eng = 100 claim would require. The direction is defensible (conservative), and the uncertainty is flagged extensively.

**Gold consumption concern direction:** Despite the arithmetic errors in CALC-1 through CALC-4, the directional finding is correct: gold recycling is essential, and unrecovered gold consumption would be prohibitive at any physically plausible mass flow rate. The concern stands; only the quoted magnitudes need correction.

---

## Proposed Actions

### PA-1: Arithmetic error in per-nanoshell gold mass
- **Category:** calculation-error
- **Severity:** important
- **Location:** analysis.md §Section 4, Gold for Nanoshells (inline formula and footnote [2])
- **Finding:** The thin-shell mass formula gives ~6 × 10⁻¹⁷ kg per nanoshell, not 6 × 10⁻¹⁸ kg as stated. The exponent is off by one.
- **Proposed Fix:** Correct the formula result to "≈ 6 × 10⁻¹⁷ kg" and update all downstream values (per-pulse mass, g/s flow rate, annual consumption, % of world production, and the cost-per-hour estimate). See PA-2, PA-3, PA-4.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: Per-pulse gold mass inconsistent with per-nanoshell mass
- **Category:** calculation-error
- **Severity:** important
- **Location:** analysis.md §Section 4, Gold for Nanoshells — "~6 × 10⁻⁶ g of gold per pulse"
- **Finding:** "6 × 10⁻⁶ g per pulse" is inconsistent with the stated per-nanoshell mass even before correcting PA-1. Using the (wrong) 6×10⁻¹⁸ kg/shell × 10⁶ shells/pulse = 6×10⁻¹² kg = 6×10⁻⁹ g/pulse. The correct value (from corrected PA-1) is ~6×10⁻⁸ g/pulse.
- **Proposed Fix:** Replace "~6 × 10⁻⁶ g of gold per pulse" with "~6 × 10⁻⁸ g of gold per pulse" once PA-1 is corrected.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: Annual gold consumption overstated ~100×
- **Category:** calculation-error
- **Severity:** important
- **Location:** analysis.md §Section 4, Gold for Nanoshells — "~6 g/s" and "roughly 190 tonnes of gold per year" and "~5% of annual production"
- **Finding:** The correct mass flow rate is ~60 mg/s (not 6 g/s), giving ~1.9 t/yr (not ~190 t/yr) and ~0.05% of world production (not ~5%). The concern about recycling remains valid but the magnitude claimed is 100× too large.
- **Proposed Fix:** Update to: "~60 mg/s at 1 MHz → roughly 1.9 tonnes of gold per year if not recovered — ~0.05% of world annual production (~3,500 t/yr). Viable but not negligible. Recovery fraction is still the critical constraint."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: Gold cost/hour inconsistent with stated flow rate and gold price
- **Category:** calculation-error
- **Severity:** important
- **Location:** analysis.md §Section 4 — "~$0.5M/hour" and model_setup.py KEY ASSUMPTIONS SUMMARY
- **Finding:** At the stated 6 g/s and $80–90k/kg (early 2026), the cost is ~$1.84M/hr. $0.5M/hr implies ~$23k/kg gold price (circa 2022 pricing). At the correct 60 mg/s and current gold price, the cost is ~$18k/hr. The dollar figure appears to use an old gold price that was not updated when current market prices were cited in the same paragraph.
- **Proposed Fix:** After correcting PA-3, update the cost estimate to: "At 60 mg/s (unrecovered) and ~$85k/kg: ~$18,000/hr — economically punishing but not the $0.5M/hr stated." Also update the KEY ASSUMPTIONS SUMMARY in model_setup.py if the gold consumption figure appears there.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-5: IP quote contains unverified interpolated clause
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 1, opening block quote
- **Finding:** The quoted text inserts "for nuclear fusion using plasmonic field enhancement" in the middle of the IP notice. The source extraction (arxiv-2503-nanoshell-paper.md) shows "..." at that position; the interpolated clause is not verified in the source.
- **Proposed Fix:** Remove the interpolated clause or mark it as paraphrased: "Systems, methods, and underlying principles [for nuclear fusion using plasmonic field enhancement —paraphrase] are the intellectual property of Cortex Fusion Systems, Inc." Or keep the original "..." to match the source.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-6: dossier.md omitted from review source list
- **Category:** improvement
- **Severity:** minor
- **Location:** Review prompt / analysis.md §Section 2 footnotes [1] and [5]
- **Finding:** analysis.md cites "dossier.md" twice (§Energy Capture and §Neutron Management). The dossier exists at `phase_1a/research/03-laser-icf-liquid-jet-target/dossier.md` and citations check out. The review prompt listed only 4 iter-01 source files and omitted dossier.md. This is a review configuration gap, not an analysis error.
- **Proposed Fix:** Add dossier.md to the source list in future review prompts for any concept that cites it.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-7: "Nine orders" vs. "14 orders" — clarify baselines
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §Section 2 Challenge 2 and §Section 3 Challenge 5
- **Finding:** Both figures are arithmetically correct but use different reference baselines. The paper's "nine orders" compares to high-flux fission-based devices (~10^10 n/s); the analysis's "14 orders" compares to the Cambridge kHz paper (10^5 n/s). A reader may conflate these or assume an error. The analysis correctly uses the Cambridge paper as the closest experimental analogue for this specific concept, which is the appropriate comparison.
- **Proposed Fix:** Add a parenthetical in §Section 2 Challenge 2: "...14 orders of magnitude below the projected flux (note: the paper itself claims 'nine orders' compared to high-flux fission devices at ~10^10 n/s; the Cambridge kHz result at 10^5 n/s is used here as the closest experimental analogue)."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-8: Source-level inconsistency in nanoshell power — note in analysis
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §Section 5 parameter table — "Power per nanoshell: ~1 μW" and "Fusion rate per nanoshell: ~10^7 s⁻¹"
- **Finding:** These two source values are internally inconsistent. 10^7 s⁻¹ × 3333 MeV ≈ 0.5 mW; 10^7 s⁻¹ × 3.65 MeV ≈ 6 μW. Neither matches "~1 μW." The ~1 μW figure would require ~0.6 MeV per event. The inconsistency originates in arXiv:2503.15531 and compounds the existing anomaly of the 3333 MeV figure. The analysis already flags the 3333 MeV anomaly; the power inconsistency adds weight to that concern.
- **Proposed Fix:** Add a note to the parameter table row for "Power per nanoshell: ~1 μW" — something like: "Note: internally inconsistent with the same paper's 10^7 s⁻¹ fusion rate × 3333 MeV/event (which would give ~0.5 mW); compounds the 3333 MeV anomaly (see §Section 2, Challenge 2)."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 17
- **Citations verified:** 16
- **Citations not found:** 0
- **Citations partial match / minor discrepancy:** 1 (CV-1 — interpolated clause in IP quote)
- **Calculations checked:** 7
- **Calculations matched:** 3 (CALC-5, CALC-6, CALC-7)
- **Calculations mismatched:** 4 (CALC-1 through CALC-4 — all in the gold consumption chain)
- **Model parameters audited:** 15
- **Model parameters with issues:** 0 (all TRACED; model is internally consistent and well-documented)
- **Proposed Actions:** 8 (blocking: 0, important: 4, minor: 4)
- **Overall:** HAS ISSUES

**Assessment:** The analysis and model are structurally sound and well-documented. Citations check out. The model setup is exemplary — every parameter is traced, flagged, and justified. The four calculation errors (PA-1 through PA-4) all concern the gold consumption estimate in §Section 4 and form a single interconnected chain from a factor-of-10 arithmetic error in the thin-shell mass formula. The directional conclusion (gold recycling is essential; unrecovered consumption is prohibitive) remains correct. The magnitude is overstated by ~100× for consumption and ~25–100× for cost, depending on which error is the primary driver. These should be corrected before the analysis is used as a reference for supply chain or operating cost arguments.
