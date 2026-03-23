# Review: Levitated Dipole (D-T)

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 5 files

---

## Citation Verification

### CV-1: D-T fuel cycle quote
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Fuel
- **Status:** FOUND (near-match)
- **Actual text:** "DT required for rapid deployment due to lower plasma triple product requirements"
- **Notes:** Analysis paraphrases as a block quote: "In order to achieve rapid deployment…due to its lower required plasma triple products." The prose in the source note matches in substance; the block-quote framing implies a verbatim extract from the HTML preprint, but only the sense is captured in the source file. No material inaccuracy.

### CV-2: Reactor A power figures (667 MW / 208 MWe)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Reactor Performance
- **Status:** FOUND
- **Actual text:** "Reactor A (conservative Bohm scaling): ~667 MW fusion, ~208 MW net electric"
- **Notes:** Exact match. Section 5 parameter table and model_setup.py both use these values correctly.

### CV-3: Junior prototype specifications (coils, field, mass, stored energy)
- **Source cited:** arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs
- **Status:** FOUND
- **Actual text:** "14 non-insulated (NI) solder impregnated HTS coils in series / Design field: 5.63 T max at windings; achieved 2.35 T (at 42% of design current) / Design current: 1.44 kA; achieved 600 A / Floating mass: 550 kg / Stored energy achieved: 0.095 MJ (record for flux pump delivery)"
- **Notes:** All figures match. Analysis states "1.44 kA design / 600 A achieved" — cross-check: 42% × 1.44 kA = 605 A ≈ 600 A; 42% × 5.63 T = 2.365 T ≈ 2.35 T. Internally consistent.

### CV-4: Junior built for <$10M in under 2 years
- **Source cited:** arxiv-2508-17691-junior-design-results.md §Key Notes
- **Status:** FOUND
- **Actual text:** "Built in under 2 years for less than $10M USD"
- **Notes:** Exact match.

### CV-5: LDX high-beta quasi-steady discharges
- **Source cited:** openstar-prototype-roadmap.md §Lab Experiments
- **Status:** FOUND
- **Actual text:** "High-beta (20%) quasi-steady discharges >20 seconds / Inward turbulent pinch observed (Nature Physics)"
- **Notes:** Analysis states "β up to ~20%, >20 seconds" — matches source. Analysis also claims LDX operated "at keV plasma temperatures" (Section 2 body) — this specific claim is **not supported by any extracted source**. LDX electron temperatures were typically hundreds of eV, not keV. See PA-1.

### CV-6: February 2026 levitated plasma milestone
- **Source cited:** openstar-2026-funding-tahi-timeline.md §February 2026 Milestone
- **Status:** FOUND
- **Actual text:** "Junior prototype achieved plasma at ~300,000°C lasting 20 seconds in a 5.2m vacuum chamber"
- **Notes:** Analysis says "achieving plasma at ~300,000°C for 20 seconds" — exact match. Cross-check: 300,000°C = 300,000 K / 11,605 eV·K⁻¹ ≈ 25.9 eV ≈ 26 eV as stated. Correct.

### CV-7: NZ government funding amounts and fund name
- **Source cited:** openstar-prototype-roadmap.md and openstar-2026-funding-tahi-timeline.md (§NZ Government Funding)
- **Status:** PARTIAL MATCH — fund name discrepancy
- **Actual text (roadmap):** "Total raised by 2024: NZD 20M / Feb 2026: NZD 35M from NZ Regional Development Fund"
- **Actual text (timeline source):** "NZD 35 million (~USD 21 million) from **Regional Infrastructure Fund** for Tahi development"
- **Notes:** The analysis uses "NZ Regional Development Fund." The two source files disagree: roadmap says "Regional Development Fund," timeline source says "Regional Infrastructure Fund." The timeline source cites specific news outlets (Bloomberg, RNZ, World Nuclear News) and is more likely to be accurate on the fund name. See PA-2.

### CV-8: Flux pump and current leads
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Driver Technology; openstar-prototype-roadmap.md §Key Milestones
- **Status:** FOUND
- **Actual text:** "On-board superconducting transformer-rectifier ('flux pump') power supply / Flux pump needs only 10 W to maintain magnet indefinitely"
- **Notes:** Both "on-board superconducting transformer-rectifier" and "10 W continuous" confirmed. The ~10 W figure is in the roadmap §Key Milestones, not §Driver Technology of the arXiv note — minor citation specificity issue.

### CV-9: ICRH wall-plug efficiency ~70%
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Heating (also §Primary Heating in Section 5 table)
- **Status:** NOT FOUND in extracted source
- **Actual text:** Source extract shows only: "Ion-cyclotron resonance heating (ICRH) as baseline / Also evaluated ECRH and NBI"
- **Notes:** The 70% wall-plug efficiency figure does not appear in the extracted arxiv-2602-20564 source document. The model_setup.py comments correctly attribute this to "JET, EAST" demonstrations (general ICRH literature) and state it's the "stated reason OpenStar selected ICRH over ECRH." If the full arXiv PDF states 70% explicitly, this would be FOUND — but the extracted source does not support it. See PA-3.

### CV-10: Two-section sacrificial coil (~20%, ~1 yr lifetime)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Magnet
- **Status:** FOUND
- **Actual text:** "Two-section coil: sacrificial section (~20% of coil, ~1-year neutron damage lifetime) + semi-permanent section (decade-scale)"
- **Notes:** Exact match for both the 20% fraction and ~1-year lifetime.

### CV-11: Neutron intercept fraction (~25%)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management
- **Status:** FOUND
- **Actual text:** "Only ~25% of fusion neutrons pass through core magnet region due to geometry"
- **Notes:** Exact match. The analysis uses "~25% of fusion neutrons intercept the core magnet" and the source says "pass through core magnet region" — equivalent wording.

### CV-12: Two-temperature shield values (>2000 K, ~600°C)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Neutron Management
- **Status:** FOUND
- **Actual text:** "Two-temperature shield: hot shield (>2000 K) and warm shield (~600°C)"
- **Notes:** Exact match. 92% radiated heat figure also FOUND: "92% of heat deposited in neutron shield radiated to first wall."

### CV-13: TBR 1.1 with Li₂O ceramic blanket
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Tritium Breeding
- **Status:** FOUND
- **Actual text:** "Li₂O ceramic blanket / Target TBR: 1.1 / 10B(n,α)³H reaction in B₄C shield also produces tritium"
- **Notes:** All confirmed. B₄C secondary tritium source noted in analysis.md is supported.

### CV-14: Local plasma β₀ ~ 3 optimal
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Plasma Physics
- **Status:** FOUND
- **Actual text:** "Local β₀ ~ 3 optimal"
- **Notes:** Exact match.

### CV-15: Tahi target field 20 T and Lawson criterion goal
- **Source cited:** openstar-2026-funding-tahi-timeline.md §Tahi Specifications
- **Status:** FOUND
- **Actual text:** "Magnetic field: up to 20 T (4x stronger than Junior's ~5.6 T) / Goal: Place dipole on Lawson criterion curve (nTτ)"
- **Notes:** 20 T and Lawson criterion goal confirmed. Note: source claims "4× stronger than Junior's ~5.6 T" but 4 × 5.6 = 22.4 T ≠ 20 T. This is an internal inconsistency within the source document itself (not an analysis error). The analysis correctly quotes "20 T" from the source.

### CV-16: Flux pump stored energy record — value discrepancy
- **Source cited:** arxiv-2508-17691-junior-design-results.md §Junior Core Magnet Specs and openstar-prototype-roadmap.md §Key Milestones
- **Status:** PARTIAL MATCH — two sources give different values
- **Actual text (arXiv):** "Stored energy achieved: 0.095 MJ (record for flux pump delivery)" = 95 kJ
- **Actual text (roadmap):** "170 kJ stored energy via flux pump (record)"
- **Notes:** Analysis §Section 1 uses 0.095 MJ (95 kJ) citing the arXiv paper, then §Section 3 mentions "Subsequent milestone noted 170 kJ stored energy delivery in the dossier." The "subsequent milestone" framing implies 170 kJ is a later achievement not in the Junior paper. This is plausible but not explicitly stated. The two figures are cited to different sources and likely represent different points in time. The analysis should clarify this explicitly. See PA-4.

### CV-17: Bohm-like confinement and conservative design point
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Plasma Physics
- **Status:** FOUND
- **Actual text:** "Bohm-like confinement scaling (conservative baseline)"
- **Notes:** Matches analysis claim.

### CV-18: RT-1 (University of Tokyo) peaked density profiles
- **Source cited:** (no citation given in Section 1 body text)
- **Status:** FOUND in source but uncited in analysis
- **Actual text (roadmap §Lab Experiments):** "RT-1 (University of Tokyo): Similar design, 1st-gen HTS (Bi-2223) magnet / Also observed peaked density profiles"
- **Notes:** The claim appears in analysis.md body text without an inline citation. The supporting content is in openstar-prototype-roadmap.md. Should add citation. See PA-5.

### CV-19: Plasma state clarification (sustained, not ignited)
- **Source cited:** arxiv-2602-20564-plasma-state-clarification.md §Evidence
- **Status:** FOUND
- **Actual text:** "Power balance equation (Eq. 9): τe = Up/(fsh·fα·Pfus + Paux − Prad) — Paux (auxiliary power) is an essential term... Fixed Qsci assumption... Section 2.2.7 discusses ICRH, ECRH, and NBI as heating options that are 'required'"
- **Notes:** Analysis correctly describes the sustained (non-ignited) plasma state with supporting evidence.

### CV-20: 1 MW-year/m² fluence threshold applied to sacrificial coil
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Magnet; dossier.md §Neutron Management
- **Status:** PARTIAL MATCH — threshold is for tungsten shield in the extracted source, not explicitly for the coil outer section
- **Actual text:** "1 MW-year/m² neutron fluence threshold for tungsten replacement" (under §Neutron Management)
- **Notes:** The analysis applies this threshold to justify the sacrificial coil ~1 year replacement interval. The source states this threshold under "Neutron Management" for tungsten, and the arXiv source extract's §Magnet section is not separately extracted. The two-section coil design explicitly targets a ~1-year lifetime for the sacrificial outer section (confirmed in CV-10), so the claim is supported, but the specific fluence threshold tied to the coil section vs. shield tungsten is ambiguous in the available extracts. See PA-6.

---

## Calculation Verification

### CALC-1: Net plant electrical efficiency
- **Claimed:** ~31% = [208 MWe / 667 MW]
- **Re-derived:** 208 / 667 = 0.3118 ≈ 31.2%
- **Status:** MATCH
- **Notes:** Straightforward ratio. Correctly labeled as net-to-fusion (not thermal efficiency).

### CALC-2: Gross electric inference range
- **Claimed:** ~255–290 MWe [from 667 MW fusion at 35–40% thermal efficiency and ~1.1 energy multiplication]
- **Re-derived:**
  - P_neutron = 0.80 × 667 = 533.6 MW; P_alpha = 0.20 × 667 = 133.4 MW
  - Thermal power (excluding Paux for simplicity): 1.10 × 533.6 + 133.4 = 720.4 MW
  - At 35%: 0.35 × 720.4 = 252.1 MWe
  - At 40%: 0.40 × 720.4 = 288.2 MWe
- **Status:** MATCH (within stated range; analysis notes Paux also contributes as heat, slightly raising the floor)
- **Notes:** Conservative: ignoring Paux contribution to thermal power slightly underestimates gross electric, so actual range is modestly higher. The stated "255–290 MWe" is a reasonable band.

### CALC-3: Recirculating power inference
- **Claimed:** ~50–80 MWe [gross electric minus 208 MWe net]
- **Re-derived:** 252–288 MWe gross − 208 MWe = 44–80 MWe
- **Status:** MATCH (minor: floor is ~44 not ~50, but within stated uncertainty)
- **Notes:** The "~50–80 MWe" band is slightly conservative at the low end, which is appropriate.

### CALC-4: Qsci range inference
- **Claimed:** ~12–19 [from Paux 35–55 MW at 70% ICRH wall-plug efficiency]
- **Re-derived:**
  - If recirc = 50–80 MW and ~15 MW is non-ICRH aux, then P_icrh_grid ≈ 35–65 MW
  - P_plasma = 0.70 × P_icrh_grid = 24.5–45.5 MW
  - Qsci = 667 / 24.5 to 667 / 45.5 = 14.7 to 27.2
  - Alternatively (as in analysis): treating Paux as plasma power directly: 667/55 = 12.1; 667/35 = 19.1
- **Status:** MATCH for the stated derivation, but note the derivation conflates P_plasma_heating with total recirculating power
- **Notes:** The Qsci range of 12–19 is self-consistent if Paux refers to plasma heating power (not total recirc). The analysis is slightly ambiguous about this. The range is plausible but the upper bound may be optimistic given non-ICRH aux loads. Using model defaults (Qsci=15), this is within the stated band.

### CALC-5: Model power balance with default parameters
- **Claimed:** "Baseline 38% is consistent with published p_fus=667 MW / p_net=208 MWe pair at assumed Qsci=15" (model_setup.py thermal_efficiency docstring)
- **Re-derived with defaults (qsci=15, η_th=0.38, aux loads as specified):**
  - P_plasma = 667/15 = 44.47 MW
  - P_icrh_grid = 44.47/0.70 = 63.53 MW
  - P_th = 1.10 × 533.6 + 133.4 + 44.47 = 764.87 MW
  - P_et = 0.38 × 764.87 = **290.65 MWe**
  - P_aux (non-ICRH) = 5 + 4 + 5 + 1 = 15 MW
  - P_recirc = 63.53 + 15 = 78.53 MW
  - P_net = 290.65 − 78.53 = **212.1 MWe** (not 208 MWe)
  - For P_net = 208 MWe: η_th needed = (208 + 78.53) / 764.87 = **37.5%**
- **Status:** MISMATCH — model with η_th=0.38 gives P_net = 212 MWe, not 208 MWe
- **Notes:** The ~4 MWe discrepancy (2%) is small in absolute terms but the docstring claim that 38% is "consistent" with the published pair is not exactly correct. Setting η_th = 0.375 would give the exact match. See PA-7.

### CALC-6: REBCO energy scaling (Section 4 narrative)
- **Claimed:** Power plant coil "would store roughly 16× more energy per unit volume (energy ∝ B²)" vs. Junior
- **Re-derived:** B_ratio = 23 T / 5.63 T = 4.085; B² ratio = 4.085² = 16.69 ≈ "roughly 16×"
- **Status:** MATCH
- **Notes:** Correct application of B² scaling for magnetic energy density.

### CALC-7: Tritium startup cost
- **Claimed:** ~1 kg at ~$35,000/g → ~$35M
- **Re-derived:** 1 kg × 1000 g/kg × $35,000/g = $35,000,000 = $35M
- **Status:** MATCH

### CALC-8: Blanket energy multiplication derivation comment
- **Claimed (model_setup.py comment):** "Li-6 + n → T + He + 4.8 MeV adds ~10% to neutron energy deposited" — used to justify M = 1.10 via TBR = 1.1
- **Re-derived:** If TBR = 1.1, then 1.1 tritium atoms produced per D-T event → 1.1 × 4.8 MeV = 5.28 MeV extra energy per event. Fraction of neutron energy: 5.28 / 14.1 = **37.4%**, not ~10%. The physically correct M from TBR = 1.1 should be ~1.37, not 1.10.
- **Status:** MISMATCH — the stated derivation is incorrect
- **Notes:** M = 1.10 is the standard 1costingfe D-T assumption (separately cited in the parameter docstring), and this value may be defensible as a conservative first-pass estimate. However, the comment linking M = 1.10 to the TBR = 1.1 calculation is physically wrong. The two figures (TBR and M) are independent parameters. The 10% energy multiplication likely comes from the 1costingfe default, not from the TBR via the stated formula. If M = 1.37 were used instead, P_th would increase by ~(1.37 − 1.10) × 533.6 = +144 MW (+19%), substantially changing all downstream outputs. See PA-8.

---

## Model Setup Audit

### MSA-1: p_fus_MW = 667.0
- **Value:** 667.0 MW
- **Source:** analysis.md §Section 5; arxiv-2602-20564 §Reactor Performance
- **Status:** TRACED
- **Notes:** Directly published value.

### MSA-2: blanket_energy_multiplication = 1.10
- **Value:** 1.10
- **Source:** "TBR 1.1 confirmed by analytic model for OpenStar geometry"; 1costingfe costing_constants.yaml
- **Status:** TRACED (value defensible; derivation comment incorrect — see CALC-8)
- **Notes:** The value is from 1costingfe standard D-T assumption and is plausible. The comment's claim that it derives from TBR = 1.1 via Li-6 breeding is wrong (would give M ≈ 1.37). PA-8 addresses this.

### MSA-3: thermal_efficiency = 0.38
- **Value:** 0.38
- **Source:** UNPUBLISHED; noted as HIGH UNCERTAINTY
- **Status:** TRACED (as assumed)
- **Notes:** Properly flagged. For exact match to published P_net = 208 MWe, η_th = 0.375 would be needed (see CALC-5). The 0.5% discrepancy from 0.375 to 0.38 is minor but the claim of consistency should be qualified.

### MSA-4: qsci = 15.0
- **Value:** 15.0
- **Source:** INFERRED; analysis.md §Section 5 (range 12–19)
- **Status:** TRACED
- **Notes:** Within stated range. Central estimate is reasonable.

### MSA-5: icrh_wall_plug_efficiency = 0.70
- **Value:** 0.70
- **Source:** "Multi-MW ICRH systems demonstrated at ~70% wall-plug efficiency on JET, EAST" AND cited to arxiv-2602-20564 §Heating
- **Status:** PARTIAL — JET/EAST basis is sound general ICRH literature; citation to specific OpenStar arXiv source not verified (see CV-9)
- **Notes:** The 70% ICRH wall-plug efficiency is a well-established figure from the community; model_setup.py correctly credits JET/EAST. Citing it additionally to the arXiv §Heating section is unverified but the underlying physics is correct.

### MSA-6: p_cryo_MW = 5.0
- **Value:** 5.0 MW
- **Source:** ASSUMED; "ITER He cryoplant is ~35 MW for 4 K; neon at 24.6 K less demanding"
- **Status:** TRACED (as estimate)
- **Notes:** Thermodynamic basis is sound (24.6 K neon << 4 K helium in cryogenic demand). ITER cryoplant power (~35 MW) is a known reference. Estimate is reasonable; the MODERATE UNCERTAINTY tag is appropriate.

### MSA-7: duty_cycle = 0.95
- **Value:** 0.95
- **Source:** arxiv-2602-20564 §Operation Mode (">95% duty cycle achievable")
- **Status:** TRACED
- **Notes:** Using 0.95 as the exact value when the source says ">95%" is a slight conservative choice (could be 0.96–0.98). Acceptable for first-pass.

### MSA-8: vessel_inner_radius_m = 3.5 m
- **Value:** 3.5 m
- **Source:** ASSUMED; "No vessel geometry published for OpenStar Reactor A"
- **Status:** TRACED (as estimate)
- **Notes:** Correctly labeled HIGH UNCERTAINTY. The first-wall loading argument is reasonable but geometry-dependent costs are acknowledged to be minor vs. coil/ICRH.

### MSA-9: hts_coil_system_cost_M_USD = 250.0
- **Value:** $250M
- **Source:** ASSUMED; CFS SPARC REBCO TF coil set analogue; analysis.md §Section 2
- **Status:** TRACED (as assumed with basis)
- **Notes:** Correctly identified as the single most uncharacterized CAPEX item. HIGH UNCERTAINTY tag appropriate. The CFS SPARC analogue is reasonable given no OpenStar-specific cost data.

### MSA-10: sacrificial_section_fraction = 0.20
- **Value:** 0.20
- **Source:** arxiv-2602-20564 §Magnet — "~20% of coil"
- **Status:** TRACED
- **Notes:** Matches source exactly.

### MSA-11: sacrificial_section_material_cost_M_USD = 45.0
- **Value:** $45M/year
- **Source:** ASSUMED; "20% × $250M × material fraction"
- **Status:** TRACED (as assumed)
- **Notes:** Derived from hts_coil_system_cost_M_USD, which is itself assumed. Properly flagged HIGH UNCERTAINTY. 40-year cumulative of $1.8B is a material OPEX driver.

### MSA-12: C220108 (Target Factory) = $0
- **Value:** $0
- **Source:** "Continuous MFE operation; no targets"
- **Status:** TRACED
- **Notes:** Correct elimination. Not applicable to continuous MFE.

### MSA-13: C220109 (Direct Energy Converter) = $0
- **Value:** $0
- **Source:** "Closed-field levitated dipole; no directed ion exhaust for DEC"
- **Status:** TRACED
- **Notes:** Correct elimination. Consistent with analysis.md §Section 7 cross-concept note on FRC DEC.

### MSA-14: rh_scale_factor = 1.50 (C220110 Remote Handling)
- **Value:** 1.5× multiplier on standard DT base
- **Source:** ASSUMED; novel coil docking rationale
- **Status:** TRACED (as assumed)
- **Notes:** Rationale is sound (annual coil replacement with no tokamak precedent). Properly flagged HIGH UNCERTAINTY.

### MSA-15: C220107 power supplies — 0.5× reduction
- **Value:** 0.50 × standard scaling
- **Source:** "On-board flux pump (~10 W continuous) eliminates conventional power supply"
- **Status:** TRACED
- **Notes:** The flux pump eliminating the main confinement coil power supply is a genuine simplification. The 50% reduction relative to standard tokamak scaling is reasonable given only ICRH, cryogenic, and auxiliary supplies remain. Could be argued to be lower (since the dominant supply in a tokamak is the main coil supply, which is entirely absent here).

### MSA-16: ConfinementConcept — bespoke class (no standard base)
- **Value:** LevitatedDipolePlantParams (standalone, not inheriting standard concept)
- **Status:** TRACED
- **Notes:** Appropriate. The levitated dipole has no close analogue in standard cost bases. The model correctly identifies and overrides the three concept-specific accounts (C220103, C220104, C220110) and eliminates two inapplicable accounts (C220108, C220109). The inheritance decision (custom class) is well-motivated.

---

## Consistency Check

**Section 5 parameters vs. Section 2 narrative:** All directly cited values in the Section 5 parameter table are consistent with the Section 2 narrative. The 667 MW / 208 MWe pair, >95% duty cycle, ~25% neutron intercept, TBR 1.1, 23 T field, 20% sacrificial section, and ~1-year replacement interval all appear consistently in both sections.

**TRL ratings vs. Section 2 challenges:** TRL assignments are internally consistent with the described challenge levels. Plasma exhaust at TRL 1 (Section 2: "not addressed in any published document") is appropriate. D-T confinement at TRL 2 (Section 2: "26 eV vs. 10–20 keV required") is appropriate. Sacrificial coil at TRL 3 (Section 2: described in paper but never fabricated) is appropriate.

**Model vs. analysis values:**
- qsci = 15 (model) is within the 12–19 range (analysis §Section 5) ✓
- duty_cycle = 0.95 (model) consistent with ">95%" (analysis §Section 5) ✓
- sacrificial_section_fraction = 0.20 (model) consistent with "~20%" (analysis §Section 5) ✓
- thermal_efficiency = 0.38 (model) consistent with "35–40% range" in analysis §Section 2 ✓
- P_net = 212 MWe (model output) vs. P_net = 208 MWe (published) — minor 2% inconsistency (PA-7)

**Missing parameter treatment:** All 14 rows of the §Section 6 data gap inventory are reflected in model parameter documentation (ASSUMED, INFERRED, or UNPUBLISHED tags). No gap is silently ignored.

**Cross-concept claims (Section 7):** All factual claims in Section 7 that reference other analyses (01-hts-compact-tokamak, 08-frc-w-direct-conversion, 11-magnetic-mirror, 21-spherical-tokamak-hts) are clearly attributed and no verification against those analysis files was required for this review. The contrast claims are logically grounded in the concept architectures.

---

## Proposed Actions

### PA-1: LDX plasma temperature claim unsupported
- **Category:** factual-concern
- **Severity:** important
- **Location:** analysis.md §Section 2 (Confinement Scaling challenge, first paragraph)
- **Finding:** Analysis states "LDX demonstrated quasi-steady confinement with Bohm-level energy confinement times in hydrogen isotopes at keV plasma temperatures." No extracted source document supports the "keV plasma temperatures" claim. LDX literature indicates electron temperatures were typically in the hundreds of eV range, not keV. The sentence is ambiguous — it may intend to say LDX operated at temperatures approaching keV, but as written it implies keV was achieved.
- **Proposed Fix:** Qualify or remove the temperature claim for LDX. Replace with "at sub-keV plasma temperatures (hundreds of eV)" or simply remove the temperature qualifier, since the key point is that LDX did not reach fusion-relevant nTτ, not that it specifically achieved keV temperatures.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: NZ government funding source name inconsistency
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 1 (Company transparency paragraph)
- **Finding:** Analysis states "NZD 35M in February 2026 from the NZ Regional Development Fund." The openstar-2026-funding-tahi-timeline.md (sourced from Bloomberg, RNZ, World Nuclear News) says "Regional Infrastructure Fund." The openstar-prototype-roadmap.md says "NZ Regional Development Fund." The news-outlet-sourced file is more likely to reflect the official fund name.
- **Proposed Fix:** Update to "NZ Regional Infrastructure Fund" (per the news-sourced iter-02 source, which cites Bloomberg/RNZ directly).
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: ICRH 70% wall-plug efficiency — citation to arXiv source not verified
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 5 parameter table (ICRH wall-plug efficiency row); model_setup.py icrh_wall_plug_efficiency docstring
- **Finding:** Both analysis.md and model_setup.py cite arxiv-2602-20564-dt-dipole-power-plants.md §Heating as the source for the 70% wall-plug efficiency. The extracted source document does not contain this figure — only lists ICRH as the baseline heating choice. The figure is from JET/EAST experience, which model_setup.py also credits correctly. If the full arXiv PDF (not HTML extract) contains the 70% figure, the citation is correct.
- **Proposed Fix:** Either (a) confirm the figure appears in the full arXiv PDF and note it may not be in the HTML version, or (b) change the citation to reference JET/EAST published literature as the primary source, with the arXiv paper as the context for OpenStar's selection of ICRH over ECRH.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: Flux pump stored energy record — ambiguous dual values
- **Category:** inconsistency
- **Severity:** minor
- **Location:** analysis.md §Section 1 (0.095 MJ) and §Section 3 (170 kJ)
- **Finding:** The Junior arXiv paper (arxiv-2508-17691) gives 0.095 MJ = 95 kJ as the record, while openstar-prototype-roadmap.md gives 170 kJ. Analysis labels 170 kJ as a "subsequent milestone" citing "dossier.md" (not a source file in this analysis set). The two values are not reconciled explicitly.
- **Proposed Fix:** Clarify the timeline: state explicitly that 95 kJ was the record at the time of the Junior paper publication (arXiv 2508.17691, 2025) and that a subsequent milestone of 170 kJ was achieved later (per the prototype roadmap). If the dossier.md source for 170 kJ is from a later date, state that date.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-5: RT-1 peaked density profiles claim lacks inline citation
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 1 (Experimental heritage paragraph)
- **Finding:** "The University of Tokyo RT-1 device corroborated peaked density profiles in a similar geometry using Bi-2223 HTS" — no citation. The claim is supported by openstar-prototype-roadmap.md §Lab Experiments ("RT-1 (University of Tokyo): Similar design, 1st-gen HTS (Bi-2223) magnet / Also observed peaked density profiles") but the source is not cited inline.
- **Proposed Fix:** Add inline citation: [openstar-prototype-roadmap.md §Lab Experiments].
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-6: Neutron fluence threshold applied to coil lifetime — source specificity
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 2 (Sacrificial Coil section) and §Section 5 (parameter table, sacrificial coil replacement interval)
- **Finding:** The analysis cites "1 MW-year/m² fluence threshold" for the sacrificial coil ~1-year replacement interval from §Neutron Management and §Magnet. The extracted source file lists the 1 MW-year/m² threshold under §Neutron Management for tungsten shield replacement, not explicitly for the coil outer section. The two-section coil design (CV-10) does confirm ~1-year lifetime for the sacrificial section, so the claim is plausible, but the specific fluence figure may apply to the shield rather than directly to the coil.
- **Proposed Fix:** Qualify the statement to note that the 1 MW-year/m² threshold is stated for tungsten shield replacement, and the ~1-year coil replacement cycle is derived from the coil's design lifetime in the same neutron environment. Alternatively, confirm that §Magnet in the full PDF explicitly states the fluence limit for the coil section.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-7: Model thermal efficiency claim slightly inconsistent with published P_net
- **Category:** model-bug
- **Severity:** minor
- **Location:** model_setup.py, thermal_efficiency parameter docstring; line ~88–92
- **Finding:** Docstring states "Baseline 38% is consistent with published p_fus=667 MW / p_net=208 MWe pair at assumed Qsci=15." Independent calculation shows η_th=0.38 with Qsci=15 and the model's aux loads gives P_net = 212.1 MWe, not 208 MWe. Exact match requires η_th ≈ 37.5%.
- **Proposed Fix:** Either (a) update the docstring to say "approximately consistent, gives P_net ≈ 212 MWe vs. published 208 MWe; exact match requires η_th ≈ 37.5%," or (b) change the default to η_th = 0.375. Option (a) is preferred since 38% is a round number within the cited uncertainty band.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-8: Blanket energy multiplication comment — incorrect derivation from TBR
- **Category:** model-bug
- **Severity:** important
- **Location:** model_setup.py, blanket_energy_multiplication parameter docstring; line ~74–81
- **Finding:** The comment states "Li-6 + n → T + He + 4.8 MeV adds ~10% to neutron energy deposited" as the derivation for M = 1.10 from TBR = 1.1. The physically correct calculation is: extra energy per D-T event = TBR × 4.8 MeV = 1.1 × 4.8 = 5.28 MeV; fraction of 14.1 MeV neutron energy = 5.28/14.1 = 37.4%, giving M ≈ 1.37. The "~10%" stated in the comment is incorrect.
  - The value M = 1.10 appears to come from the 1costingfe default (also cited in the docstring) rather than from the TBR derivation.
  - If M should be 1.37 instead of 1.10, P_th increases by ~(0.27 × 533.6) = +144 MW (+19%), materially affecting LCOE output.
- **Proposed Fix:** Remove or correct the sentence linking M = 1.10 to TBR = 1.1 via the stated formula. Replace with: "M = 1.10 is the 1costingfe standard D-T assumption (conservative); note TBR and M are independent parameters — full blanket energy multiplication accounting would give M ≈ 1.15–1.30 depending on breeding zone geometry." Consider adding a note that this value may underestimate P_th by ~10–20%, which is one reason the LCOE should be treated as a lower bound on required capital recovery.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 20
- **Citations verified (FOUND or FOUND near-match):** 15
- **Citations partial match (value found, source specificity or name discrepancy):** 4 (CV-7, CV-16, CV-9, CV-20)
- **Citations not found in extracted source:** 1 (CV-9 — ICRH 70% efficiency; may be in full PDF)
- **Calculations checked:** 8
- **Calculations matched:** 6
- **Calculations mismatched:** 2 (CALC-5: P_net 212 vs. 208 MWe; CALC-8: blanket energy multiplication derivation)
- **Model parameters audited:** 16
- **Proposed Actions:** 8 (blocking: 0, important: 2, minor: 6)
- **Overall:** HAS ISSUES — no blocking errors; two important issues (PA-1 LDX temperature claim, PA-8 blanket multiplication derivation) should be resolved before synthesis; six minor items are clean-up level.
