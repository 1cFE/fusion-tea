# Review: Planar Coil Stellarator

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 4 files

---

## Citation Verification

### CV-1: "first awardee company" — DOE certification claim
- **Source cited:** thea-energy-doe-certification-jan2026.md §Key Facts
- **Status:** FOUND
- **Actual text:** "Thea Energy is the **first awardee company** to receive DOE certification of its pilot plant design under the Milestone-Based Fusion Development Program"
- **Notes:** Exact match.

### CV-2: "World's first tokamak-like X-point divertor for an optimized stellarator" (Section 2, block quote)
- **Source cited:** thea-energy-doe-certification-jan2026.md §Three Technical Innovations Highlighted
- **Status:** NOT FOUND
- **Actual text (in cited source):** "Stellarator 'divertor' exhaust system capable of fusion power operations (world's first)"
- **Notes:** The cited DOE cert source does not contain the phrase "tokamak-like X-point divertor." That exact phrasing comes from thea-energy-helios-arxiv-2512-08027.md §Divertor: "Type: Novel tokamak-like X-point divertor (first for optimized stellarator)". The analysis uses block-quote formatting, implying a direct verbatim quote from the cited file — but neither the phrasing nor the word "tokamak-like" appears in the cited DOE cert source. See PA-1.

### CV-3: "10× better neutral compression than island divertor" (Section 2, footnote [2])
- **Source cited:** thea-energy-doe-certification-jan2026.md §Three Technical Innovations Highlighted
- **Status:** NOT FOUND in cited source
- **Actual text (in cited source):** No mention of "10x" or "neutral compression." Source covers three innovation bullets (software coils, divertor, sector maintenance) without this quantitative claim.
- **Notes:** The 10× compression claim is found in thea-energy-helios-arxiv-2512-08027.md §Divertor: "10x better neutral compression than island divertor". The citation points to the wrong source. See PA-2.

### CV-4: "Closed loop field control to within 1% of predicted field" (Section 3, block quote)
- **Source cited:** thea-energy-canis-prototype-arxiv-2503-18960.md §Key Validation Results
- **Status:** FOUND
- **Actual text:** "Closed loop field control to within 1% of predicted field"
- **Notes:** Exact match.

### CV-5: ISS04 enhancement factor 1.4 (reference), 1.33 (gyrokinetic)
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration
- **Status:** FOUND
- **Actual text:** "ISS04 enhancement factor: 1.4 (reference), 1.33 (gyrokinetic)"
- **Notes:** Exact match.

### CV-6: Power balance numbers — 958 MW, 1,094 MW, 438 MWe, 390 MWe, ~48 MWe
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Power Balance
- **Status:** FOUND
- **Actual text:** "Fusion power: 958 MW / Total thermal power: 1,094 MW / Gross electric: 438 MWe / Net electric to grid: 390 MWe / Auxiliary/facility power: ~48 MWe"
- **Notes:** All five values match exactly.

### CV-7: Thermal efficiency ~40.2%; Steam Rankine, 635°C, three-stage turbines
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Energy Conversion
- **Status:** FOUND
- **Actual text:** "Efficiency: ~40.2% / Steam temperature: 635°C superheated / Three-stage turbines"
- **Notes:** Exact match.

### CV-8: Operational ECRH = 1 MW; startup ECRH = 10 MW at 170 GHz; total budget = 2.5 MW
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Heating
- **Status:** FOUND
- **Actual text:** "Startup: 10 MW ECRH at 170 GHz / Ignited operation: 1 MW ECRH for impurity control / Total ECRH budget: 2.5 MW (1 MW operational + overhead)"
- **Notes:** Exact match.

### CV-9: Capacity factor 88%; maintenance cycle 84 days biennial
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Operations
- **Status:** FOUND
- **Actual text:** "Capacity factor: 88% / Maintenance cycle: 84 days biennial"
- **Notes:** Exact match.

### CV-10: First wall lifetime 15 full-power years; magnet lifetime 40+ years
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §First Wall; §Magnets
- **Status:** FOUND
- **Actual text:** "Lifetime: 15 full-power years" (§First Wall); "Designed lifetime: 40+ years (with shielding)" (§Magnets)
- **Notes:** Exact match.

### CV-11: LCOE targets $150/MWh → $60/MWh
- **Source cited:** thea-energy-website-and-press.md §Helios
- **Status:** FOUND
- **Actual text:** "LCOE target: $150/MWh initially → $60/MWh at scale"
- **Notes:** Exact match.

### CV-12: Alpha particle loss fraction 6.6%; code ASCOT5
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Energetic Particle Confinement
- **Status:** FOUND
- **Actual text:** "Alpha loss: 6.6% of fusion product energy / Code: ASCOT5"
- **Notes:** Exact match.

### CV-13: Startup tritium 1–2 kg; Li-6 enrichment 65%; LiPb blanket thickness 50 cm; TBR idealized 1.3, required 1.1
- **Source cited:** thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding
- **Status:** FOUND
- **Actual text:** "Startup tritium: 1-2 kg / Li-6 enrichment: 65% / Blanket thickness: 50 cm / Idealized TBR: 1.3 / Required TBR: 1.1"
- **Notes:** All four values confirmed.

### CV-14: W7-X H_ISS04 ≈ 1.3–1.4 in QI configuration (Section 1 and Section 2)
- **Source cited:** None — no footnote provided for this claim
- **Status:** UNVERIFIABLE from available sources
- **Actual text:** Not present in any of the four source documents.
- **Notes:** The claim appears in Section 1 experimental heritage and in Section 2 Challenge 1 without a citation. It is broadly accurate per the stellarator community literature, but it is not traceable to any of the four ingested sources. See PA-5.

### CV-15: Eos daily tritium production ~0.2 g/day (70 g/year); first plasma 2030
- **Source cited:** thea-energy-website-and-press.md §Key Machines
- **Status:** FOUND
- **Actual text:** "Tritium production: ~0.2 g/day (70 g/year) via D-D / First plasma target: 2030"
- **Notes:** Exact match.

### CV-16: Total Thea Energy funding — $20M Series A, DOE milestone participation
- **Source cited:** thea-energy-website-and-press.md §Funding
- **Status:** FOUND
- **Actual text:** "Series A: $20M (September 2024) — Prelude Ventures lead / DOE Milestone-Based Fusion Development Program: Selected May 2023"
- **Notes:** Match. The analysis correctly notes no separate ARPA-E grant is claimed.

### CV-17: Canis field error — EOS1: 0.56%, EOS2: 0.60%
- **Source cited:** thea-energy-canis-prototype-arxiv-2503-18960.md §Key Validation Results (via §Magnets note in parameter table)
- **Status:** FOUND
- **Actual text:** "EOS1 patch: 0.56% RMS field error / EOS2 patch: 0.60% RMS field error"
- **Notes:** Exact match.

---

## Calculation Verification

### CALC-1: Plasma gain Q ≈ 958
- **Claimed:** "~958 (effectively ignited)" — derivation: 958 MW fusion / 1 MW operational ECRH
- **Re-derived:** Q = P_fusion / P_heating = 958 MW / 1 MW = 958
- **Status:** MATCH
- **Notes:** Correct. "Effectively ignited" is an appropriate qualifier.

### CALC-2: Blanket breeding thermal bonus ~135 MW
- **Claimed:** "~135 MW" — derivation: 1,094 MW total thermal − 958 MW fusion − ~1 MW heating
- **Re-derived:** 1,094 − 958 − 1 = 135 MW
- **Status:** MATCH
- **Notes:** Correct. The bonus arises from Li-6(n,α)T exotherms captured in the LiPb blanket.

### CALC-3: Alpha particle wall loading ~12.7 MW
- **Claimed:** "~12.7 MW deposited on first wall/divertor"
- **Re-derived:** P_alpha = 958 MW × 20% = 191.6 MW alpha power; 6.6% loss × 191.6 = 12.65 MW ≈ 12.7 MW
- **Status:** MATCH
- **Notes:** Rounding to one decimal; consistent.

### CALC-4: Total facility recirculating fraction ≈ 11%
- **Claimed:** "48/438 = 11% covers all facility loads"
- **Re-derived:** 48 / 438 = 10.96% → rounds to 11%
- **Status:** MATCH
- **Notes:** Correct.

### CALC-5: Carnot COP at 20 K ≈ 0.07
- **Claimed:** "Carnot COP at 20 K ≈ 0.07" (Section 5 Missing Parameters note)
- **Re-derived:** COP_Carnot = T_cold / (T_hot − T_cold) = 20 K / (300 − 20) K = 20/280 = 0.0714
- **Status:** MATCH
- **Notes:** Correct.

### CALC-6: LiPb blanket plasma-facing surface area ~870 m²
- **Claimed:** "500 m³ plasma volume / 1.8 m a → surface area ~870 m²" (Section 5 Missing Parameters derivation note)
- **Re-derived:** Standard torus surface area: A = 4π²Rr = 4π² × 8.0 m × 1.8 m = 4 × 9.870 × 14.4 = 568 m². The formula used in the analysis (V / a × π ≈ 500 / 1.8 × π ≈ 874 m²) has no standard physical basis for a torus.
- **Status:** MISMATCH
- **Notes:** The analysis value of ~870 m² is ~53% above the standard torus formula result of ~568 m². Downstream estimate for blanket volume propagates: ~435 m³ claimed vs. ~284 m³ by correct formula; LiPb mass ~4.2M kg claimed vs. ~2.7M kg re-derived. This is confined to the "derivable / nice-to-have" row of the Missing Parameters table, so the impact on the main analysis or model setup is zero. See PA-3.

---

## Model Setup Audit

### MSA-1: NET_ELECTRIC_MW = 390.0
- **Value:** 390.0 MWe
- **Source:** analysis.md §Section 5; arxiv §Power Balance
- **Status:** TRACED
- **Notes:** Direct match to source: "Net electric to grid: 390 MWe."

### MSA-2: AVAILABILITY = 0.88
- **Value:** 0.88
- **Source:** analysis.md §Section 5; arxiv §Operations
- **Status:** TRACED
- **Notes:** Direct match: "Capacity factor: 88%."

### MSA-3: LIFETIME_YR = 40
- **Value:** 40 years
- **Source:** analysis.md §Section 5; arxiv §Magnets
- **Status:** TRACED
- **Notes:** Source says "40+ years"; using 40 as the design point value is appropriate.

### MSA-4: R0 = 8.0; PLASMA_T = 1.8; ELON = 1.0
- **Value:** 8.0 m, 1.8 m, 1.0
- **Source:** analysis.md §Section 5; arxiv §Plasma & Configuration
- **Status:** TRACED (R0, PLASMA_T) / APPROPRIATE DEFAULT (ELON)
- **Notes:** R0 and PLASMA_T directly match source. ELON=1.0 is a reasonable assumption for a QA configuration (approximately circular cross-section); not published in Helios sources but correctly noted as a default.

### MSA-5: BLANKET_T = 0.50
- **Value:** 0.50 m
- **Source:** comment says "[A/C] inferred from plasma-to-coil gap 1.2 m [B §Magnets]"
- **Status:** TRACED (but comment is misleading)
- **Notes:** The blanket thickness of 50 cm is directly stated in the source (thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding: "Blanket thickness: 50 cm") and does not need to be inferred from the coil gap. The comment implies it was derived when a direct authoritative value exists. See PA-4.

### MSA-6: p_input = 1.0 MW
- **Value:** 1.0 MW
- **Source:** analysis.md §Section 5; arxiv §Heating
- **Status:** TRACED
- **Notes:** "Ignited operation: 1 MW ECRH for impurity control." Correct.

### MSA-7: eta_th = 0.40
- **Value:** 0.40
- **Source:** analysis.md §Section 5; arxiv §Energy Conversion (40.2%)
- **Status:** TRACED
- **Notes:** Slight rounding down from 40.2%; conservative and appropriate.

### MSA-8: p_cryo = 15.0 MW (UNCERTAIN)
- **Value:** 15.0 MW (upper bound)
- **Source:** Estimated from Carnot COP analysis; analysis.md §Section 5 Missing Parameters gap #14
- **Status:** UNTRACED (appropriately flagged)
- **Notes:** Correctly marked UNCERTAIN. The estimate range "5–15 MWe" is internally derived (no Helios-published figure). Using the upper bound and flagging with UNCERTAIN is the right approach.

### MSA-9: p_coils, p_cool, p_pump, p_house (various auxiliary loads)
- **Values:** 2.0, 8.0, 3.0, 5.0 MW
- **Source:** all marked UNCERTAIN, with rationale citing analysis sections
- **Status:** UNTRACED (appropriately flagged)
- **Notes:** No Helios-published breakdown of 48 MWe facility load exists. Each auxiliary component is flagged as UNCERTAIN with a qualitative rationale. This is the correct approach given data availability.

### MSA-10: p_trit = 10.0 MW (DEFAULT)
- **Value:** 10.0 MW
- **Source:** DEFAULT from framework (mfe_stellarator.yaml); noted as consistent with DT baseline
- **Status:** TRACED to default / appropriate
- **Notes:** Analysis notes ~300 g/day tritium at 958 MW fusion with 5% burn fraction. The 10 MW default is consistent with DT blanket tritium processing requirements.

### MSA-11: noak = False
- **Value:** False (FOAK)
- **Source:** analysis.md §Section 5; website "LCOE target (first plant): $150/MWh"
- **Status:** TRACED
- **Notes:** Correct. Analysis explicitly models the first-plant scenario.

### MSA-12: ConfinementConcept.STELLARATOR
- **Value:** STELLARATOR
- **Source:** Helios is a steady-state quasi-axisymmetric stellarator
- **Status:** TRACED
- **Notes:** Correct base concept. The rationale in the docstring is well-argued and accurate.

### MSA-13: f_dec = 0.0
- **Value:** 0.0 (no direct energy conversion)
- **Source:** analysis.md; pure steam Rankine, no DEC
- **Status:** TRACED
- **Notes:** Correct. Helios uses steam Rankine only; no ion direct conversion or other DEC pathway.

### MSA-14: "1costingfe" in docstring (lines 4 and 173)
- **Value:** N/A (documentation text)
- **Source:** N/A
- **Status:** N/A
- **Notes:** The docstring on line 4 reads "1costingfe STELLARATOR/DT concept" and line 173 reads "model result above is the 1costingfe parametric estimate." The leading "1" in "1costingfe" appears to be a typo — the package name used in the imports is `costingfe`. See PA-6.

---

## Consistency Check

**Section 5 ↔ model_setup.py**: All primary parameter values in §Section 5 Available Parameters are correctly reflected in model_setup.py: R0=8m, a=1.8m, eta_th=0.40, P_net=390 MWe, availability=0.88, lifetime=40yr, P_input=1 MW, p_cryo=15 MW, noak=False. No inconsistencies found.

**TRL ratings ↔ Section 2 challenges**: The TRL ratings in Section 3 are internally consistent with the challenge descriptions in Section 2. The QA X-point divertor is correctly rated TRL 1–2 (no hardware precedent), consistent with being flagged as the highest-impact LCOE challenge in Section 2. ECRH is rated TRL 7–8, consistent with the "shallowest development challenge" characterization.

**Coil count notation**: The analysis correctly distinguishes 324 shaping coils (individually addressable) from 336 total coils (12 encircling + 324 shaping) across all sections. The model_setup.py comment on line 113 ("336 REBCO coils at 20 K") uses the total count, which is correct for the cryo load context. The Key Assumptions print block itemizes "12 encircling + 324 shaping." Consistent throughout.

**Section 1 data availability claim**: Section 1 states "All 12 differentiation columns were filled with high confidence after two research iterations" [5], cited to `dossier.md §Remaining Gaps`. The dossier file is referenced but not part of the provided source set — citation cannot be independently verified, though the claim is plausible given the richness of the Helios arxiv paper.

**W7-X H_ISS04 claim**: The claim that W7-X has demonstrated H_ISS04 ≈ 1.3–1.4 appears in both Section 1 (Experimental Heritage) and Section 2 (Challenge 1) without a traceable citation to any of the four ingested source files. This is an externally known fact that is broadly accepted in the stellarator community, but it lacks a verifiable source pointer within the project. See PA-5.

**LCOE narrative and model congruence**: The analysis clearly states that Thea has not published a bottom-up cost account, and the model_setup.py correctly uses framework defaults throughout with no cost_overrides. The Key Assumptions print in model_setup.py restates this accurately: "Framework defaults throughout (ARIES-CS analogue structure) — Thea Energy has NOT published a bottom-up capital cost breakdown." This is consistent and honest about modeling limitations.

---

## Proposed Actions

### PA-1: Block quote "World's first tokamak-like X-point divertor for an optimized stellarator" cites wrong source
- **Category:** citation-error
- **Severity:** important
- **Location:** analysis.md §Section 2, Challenge 2 block quote and attribution
- **Finding:** The block quote is attributed to `thea-energy-doe-certification-jan2026.md, §Three Technical Innovations Highlighted`. The DOE cert source does not contain the phrase "tokamak-like X-point divertor" — it says "Stellarator 'divertor' exhaust system capable of fusion power operations (world's first)". The "tokamak-like X-point divertor" phrasing originates from `thea-energy-helios-arxiv-2512-08027.md §Divertor`: "Type: Novel tokamak-like X-point divertor (first for optimized stellarator)". The block quote is also not verbatim from either source — it reads as a constructed paraphrase. Because the quote marks and attribution imply a direct quotation, this is a citation error.
- **Proposed Fix:** Replace the block quote with one of: (a) use the DOE cert's actual text verbatim, cited to doe-certification-jan2026.md, or (b) use the Helios arxiv paper's phrasing "Novel tokamak-like X-point divertor (first for optimized stellarator)", cited to thea-energy-helios-arxiv-2512-08027.md §Divertor. Option (b) is the more specific technical claim and better supports the narrative.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: "10× better neutral compression" cites wrong source (DOE cert instead of arxiv paper)
- **Category:** citation-error
- **Severity:** important
- **Location:** analysis.md §Section 2, Challenge 2, footnote [2]
- **Finding:** Footnote [2] reads "thea-energy-doe-certification-jan2026.md §Three Technical Innovations Highlighted". The "10× better neutral compression than island divertor" claim does not appear in the DOE cert source. It appears in thea-energy-helios-arxiv-2512-08027.md §Divertor: "10x better neutral compression than island divertor."
- **Proposed Fix:** Change footnote [2] to `thea-energy-helios-arxiv-2512-08027.md §Divertor`.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: LiPb blanket surface area calculation uses non-standard formula (~870 m² vs. ~568 m²)
- **Category:** calculation-error
- **Severity:** minor
- **Location:** analysis.md §Section 5 Missing Parameters, LiPb blanket inventory mass row (derivation note)
- **Finding:** The inline derivation "500 m³ plasma volume / 1.8 m a → surface area ~870 m²" uses the formula V/a × π ≈ 874 m², which has no standard physical basis for a toroidal geometry. The correct torus surface area formula is A = 4π²Rr = 4π² × 8.0 × 1.8 ≈ 568 m². The ~870 m² value is ~53% too large, propagating to an overestimate of blanket volume (~435 m³ vs. ~284 m³) and LiPb mass (~4.2M kg vs. ~2.7M kg). Impact on main analysis is nil — this is a "nice-to-have" derivable estimate in the missing parameters table, not a primary analysis input and not used in model_setup.py.
- **Proposed Fix:** Correct the surface area derivation to use A = 4π²Rr ≈ 568 m², giving blanket volume ≈ 568 m² × 0.5 m ≈ 284 m³ and LiPb mass ≈ 284 m³ × 9,600 kg/m³ ≈ 2.7M kg. Update the note accordingly.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: BLANKET_T comment overstates inference — direct source value exists
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py line 58 (BLANKET_T comment)
- **Finding:** The comment reads "[A/C] '50 cm blanket' inferred from plasma-to-coil gap 1.2 m [B §Magnets] with ~20 cm first wall + 50 cm blanket + 30 cm HT shield + structure". However, the blanket thickness of 50 cm is directly stated in thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding: "Blanket thickness: 50 cm". The value does not need to be inferred; it has a direct authoritative source.
- **Proposed Fix:** Change comment to `# [B §Blanket & Tritium Breeding] Blanket thickness 50 cm — directly stated in Helios source.` and update the citation key to `[B]` pointing to the arxiv paper's blanket section.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-5: W7-X H_ISS04 ≈ 1.3–1.4 claim lacks traceable citation
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §Section 1 (Experimental Heritage) and §Section 2 Challenge 1
- **Finding:** The claim "Wendelstein 7-X has demonstrated H_ISS04 ≈ 1.3–1.4 in some discharges" appears twice without a footnote. None of the four ingested source files contain W7-X H_ISS04 performance data. The claim is broadly consistent with the stellarator community literature (W7-X experimental record), but it is currently unverifiable within the project source set.
- **Proposed Fix:** Either (a) add a footnote referencing a specific W7-X paper (e.g., Beidler et al. 2021 or Stange et al. 2023 in Nuclear Fusion) and ingest the source, or (b) add a qualifier noting this is general stellarator community knowledge pending formal citation. Option (a) is preferred for traceability compliance.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-6: "1costingfe" typo in model_setup.py docstring
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py lines 4 and 173
- **Finding:** Line 4: "1costingfe STELLARATOR/DT concept"; line 173: "model result above is the 1costingfe parametric estimate." The package import is `from costingfe import ...` — the leading "1" in "1costingfe" is a typo. Likely a markdown list-item artifact or formatting error carried over from an intermediate draft.
- **Proposed Fix:** Replace "1costingfe" with "costingfe" on both lines.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 17
- **Citations verified:** 15
- **Citations not found (or wrong source):** 2 (PA-1: wrong source for divertor block quote; PA-2: wrong source for 10× compression claim)
- **Calculations checked:** 6
- **Calculations matched:** 5
- **Calculations mismatched:** 1 (PA-3: LiPb surface area, minor/derivable context only)
- **Model parameters audited:** 14 explicit parameters + concept choice
- **Parameters fully traced:** 11
- **Parameters appropriately uncertain/default:** 3
- **Parameters with documentation issues:** 1 (PA-4: BLANKET_T)
- **Proposed Actions:** 6 (blocking: 0, important: 2, minor: 4)
- **Overall:** HAS ISSUES — two citation errors point to the wrong source file (DOE cert cited instead of Helios arxiv paper for both the divertor innovation claim and the 10× compression figure); one minor calculation error in a derivable estimate; three minor documentation issues. No factual errors in primary analysis parameters. No model bugs. Analysis is substantively sound.
