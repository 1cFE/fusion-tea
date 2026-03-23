# Review: Laser ICF - p-B11 Fast Ignition

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 7 files

---

## Citation Verification

### CV-1: "10× more fusion reactions than previous results at same facility using 'pitcher-catcher' geometry"
- **Source cited:** hb11-osaka-experiment-2022.md §Key Results
- **Status:** FOUND
- **Actual text:** "10× more fusion reactions than previous results at same facility using 'pitcher-catcher' geometry"
- **Notes:** Exact match.

### CV-2: Alpha yield ~10^10 alpha/sr; "~4 orders of magnitude below the breakeven threshold"
- **Source cited:** hb11-osaka-experiment-2022.md §Key Results and §Significance
- **Status:** FOUND
- **Actual text:** "Measured alpha particle flux: ~10^10/sr" (§Key Results); "Still ~4 orders of magnitude away from net energy gain" (§Significance)
- **Notes:** Both values confirmed. Analysis says "~10,000× (4 orders of magnitude)" which is consistent with the source.

### CV-3: "energy per reaction: ~1 GJ (~280 kWh)"
- **Source cited:** hb11-patent-reactor-design.md §Performance Targets
- **Status:** FOUND
- **Actual text:** "Energy per reaction: ~1 GJ (~280 kWh)"
- **Notes:** Exact match. This is the number at the center of the internal inconsistency analysis in Section 2, Challenge 3.

### CV-4: "no need for a heat exchanger or steam turbine generator" (New Atlas, 2020)
- **Source cited:** hb11-newatlas-article.md §Energy Conversion — DIRECT
- **Status:** FOUND
- **Actual text:** "with no need for a heat exchanger or steam turbine generator"
- **Notes:** Exact match. Confirms the pre-2025 direct conversion baseline.

### CV-5: "conventional steam cycle generator" (2025 website)
- **Source cited:** hb11-technology-page-2025.md §Energy Conversion
- **Status:** FOUND
- **Actual text:** "The energy released drives a conventional steam cycle generator."
- **Notes:** Exact match. Also confirmed in the earlier hb11-technology-page.md (2024 fetch): "Power generation: 'Conventional steam cycle generator'."

### CV-6: Direct electrostatic conversion at −1.4 MV, Faraday cage, 714 A output
- **Source cited:** hb11-patent-reactor-design.md §Energy Conversion — Direct Electrostatic
- **Status:** FOUND
- **Actual text:** "Bias voltage: Reaction chamber at -1.4 MV relative to outer spherical wall"; "Faraday cage: Between reaction chamber and outer wall"; "Output: 714 Amperes discharge current via HVDC transmission"
- **Notes:** All three values confirmed exactly.

### CV-7: A$8.2M Adelaide USPL partnership; >10% wall-plug efficiency target
- **Source cited:** hb11-recent-developments-2024-2025.md §Adelaide Laser Partnership (2025)
- **Status:** FOUND
- **Actual text:** "$8.2M collaboration with University of Adelaide DualTech-USPL Group"; "Target: demonstrate >10% wall-plug efficiency"
- **Notes:** Confirmed. Note: Section 5 parameter table attributes the A$8.2M to §FusionXInvest Profile, which is incorrect — that section only lists A$8.2M as "Defence Trailblazer" in the funding table but the specific Adelaide partnership context comes from §Adelaide Laser Partnership (2025). See PA-4.

### CV-8: ps laser energy example ~30 kJ; ps laser duration <5 ps; ps laser peak power >1 PW; intensity ≥10^17 W/cm²
- **Source cited:** hb11-patent-reactor-design.md §Laser Specifications (Fusion Laser)
- **Status:** FOUND
- **Actual text:** "Duration: <5 ps"; "Power: >1 petawatt"; "Intensity: >=10^17 W/cm²"; "Energy per pulse example: 30 kJ (= 30 PW for 1 ps)"
- **Notes:** All four values confirmed exactly.

### CV-9: ns laser energy >100 J; duration <20 ns
- **Source cited:** hb11-patent-reactor-design.md §Laser Specifications (Magnetic Field Laser)
- **Status:** FOUND
- **Actual text:** "Duration: <20 ns"; "Energy: >100 J"
- **Notes:** Exact match.

### CV-10: Magnetic field strength ≥1 kT (examples: 4.5 kT, 10 kT)
- **Source cited:** hb11-patent-reactor-design.md §Magnetic Field Generation
- **Status:** FOUND
- **Actual text:** "Field strength: >=1 kT (kilotesla); examples cite 4.5 kT and 10 kT"
- **Notes:** Exact match.

### CV-11: Fuel pellet 1 cm length × 0.2 mm diameter; ~5 µm silver cover layer; quartz fiber positioning
- **Source cited:** hb11-patent-reactor-design.md §Reactor Geometry
- **Status:** FOUND
- **Actual text:** "Solid-state cylindrical HB11 body, 1 cm length x 0.2 mm diameter"; "Fuel positioning: Held along magnetic field axis via quartz fibers"; "Cover layer: Material with atomic weight >100 (e.g., silver), thickness ~5 microns"
- **Notes:** All confirmed. Analysis says "~5 µm high-Z material (e.g., silver)" — consistent.

### CV-12: Outer vessel spherical stainless steel, ≥1 m diameter, 10 mm thick
- **Source cited:** hb11-patent-reactor-design.md §Reactor Geometry
- **Status:** FOUND
- **Actual text:** "Outer vessel: Stainless steel spherical wall, 10 mm thick, diameter >= 1 m"
- **Notes:** Exact match.

### CV-13: Energy gain target >500 (enhanced: >1000)
- **Source cited:** hb11-patent-reactor-design.md §Performance Targets
- **Status:** FOUND
- **Actual text:** "Energy gain: >500 (enhanced: >1000) per laser energy expended"
- **Notes:** Exact match.

### CV-14: 12 experiments at international laser facilities; Osaka, Belfast, Prague
- **Source cited:** hb11-recent-developments-2024-2025.md §Experimental Progress
- **Status:** FOUND
- **Actual text:** "12 experiments at international laser facilities"; "Osaka LFEX (2022)"; "Belfast TARANIS laser"; "PALS laser facility, Prague (2024)"
- **Notes:** All confirmed.

### CV-15: Neutron fraction <1% of fusion energy
- **Source cited:** hb11-technology-page.md §Key Technical Details
- **Status:** PARTIAL MATCH
- **Actual text:** The technology page states the reaction "creates three helium ions (alpha particles) releasing 8.7 MeV" — it does not explicitly state a neutron fraction of <1%. The <1% figure is well-established nuclear physics for p-B11 side reactions.
- **Notes:** The source is correctly associated with the concept but the specific <1% figure is an established physical constant, not a verbatim claim from this source. Low concern given the physics is uncontested, but the citation is imprecise. See PA-5.

---

## Calculation Verification

### CALC-1: 30 kJ × 500 gain = 15 MJ; 1 GJ / 15 MJ ≈ 67× inconsistency
- **Claimed:** "The 15 MJ implied by 30 kJ × 500 gain is inconsistent with the 1 GJ electrical output claim by a factor of ~67."
- **Re-derived:** 30 kJ × 500 = 15,000 kJ = 15 MJ. 1 GJ / 15 MJ = 66.7×. Analysis says "factor of ~67."
- **Status:** MATCH
- **Notes:** Correct.

### CALC-2: 1 GW at 35% thermal efficiency requires ~2.9 GJ/shot; implies gain ~97,000 from 30 kJ
- **Claimed:** "requires ~2.9 GJ fusion energy per shot — implying a gain of ~97,000 from 30 kJ"
- **Re-derived:** 1 GJ electrical / 0.35 = 2.857 GJ fusion/shot ≈ 2.9 GJ ✓. Required gain = 2,857,000 kJ / 30 kJ = 95,233 ≈ ~97,000 (close; difference from rounding the 2.9 GJ figure).
- **Status:** MATCH
- **Notes:** Minor rounding difference; the order of magnitude and framing are correct.

### CALC-3: Scenario math — p_fusion, p_implosion, wall-plug draw, Q_eng
- **Claimed:** "P_fusion = 1000 / 0.35 ≈ 2857 MW; Laser energy/shot = 2857 MJ / 500 = 5.71 MJ → p_implosion = 5.71 MW; Wall-plug = 5.71 / 0.10 = 57.1 MW; Q_eng ≈ 1000 / 57.1 ≈ 17.5"
- **Re-derived:** 1000 / 0.35 = 2857.14 MW ✓; 2857.14 / 500 = 5.714 MW ≈ 5.71 MW ✓; 5.71 / 0.10 = 57.1 MW ✓; 1000 / 57.1 = 17.51 ✓
- **Status:** MATCH
- **Notes:** All four steps verify exactly.

### CALC-4: Patent parameters → ~5.25 MWe net (model_setup.py docstring note)
- **Claimed:** "Patent example (30 kJ laser, gain 500): p_fus = 0.03 MW × 500 = 15 MW — insufficient by a factor of ~190 for a 1 GW plant."
- **Re-derived:** 30 kJ/shot × 1 Hz = 30 kW = 0.030 MW laser avg. 0.030 × 500 = 15 MW fusion. 15 MW × 0.35 = 5.25 MWe net. 1000 / 5.25 = 190.5 ✓
- **Status:** MATCH

### CALC-5: Section 5 table — "Net plant electrical output (estimated)" value column
- **Claimed:** "[estimated: ~300–500 MWe at 1 Hz, if gain = 500, laser energy ~30 kJ, η_thermal = 35%]"
- **Re-derived:** 30 kJ × 500 gain = 15 MJ fusion. 15 MJ × 0.35 = 5.25 MJ electrical. At 1 Hz: 5.25 MW net. The same table cell's derivation column independently shows: "30 kJ × 500 gain × 0.35 thermal = 5.25 MJ/shot × 1 Hz = 5.25 MW."
- **Status:** MISMATCH — the value column states "~300–500 MWe" but the correct result is ~5 MWe. The two halves of the same table cell contradict each other by a factor of ~60–95×.
- **Notes:** The derivation in the source column is correct (5.25 MW). The value/range column is wrong. This appears to be a labeling error — "~300–500 MWe" may have been a copy-paste from a different concept or scenario (possibly corresponding to a much larger laser energy input). See PA-1.

### CALC-6: CAS21 buildings override arithmetic
- **Claimed:** "Framework default for LASER_IFE/PB11 at 1 GWe ≈ $511M... Adjustments: remove cryogenics ($15/kW × 1000 = −$15M); reduce hot cell by 50% (aneutronic, −$47M); reduce heat exchanger (thin blanket, −$6M). Net reduction ≈ −$68M → ~$420M."
- **Re-derived:** $511M − ($15M + $47M + $6M) = $511M − $68M = $443M. The stated result is $420M. Discrepancy: $443M − $420M = $23M.
- **Status:** MISMATCH — the arithmetic gives $443M, not $420M.
- **Notes:** Either the stated deductions are understated (the actual reductions applied sum to $91M, not $68M) or the $511M baseline or the override value ($420M) is wrong. The $420M is used in the actual `model.forward()` call. See PA-2.

### CALC-7: 31.5M pellets/year at 1 Hz
- **Claimed:** "31.5M units/year" (docstring, multiple references)
- **Re-derived:** 365.25 days × 24 hr × 3600 s = 31,557,600 s/yr ≈ 31.56M. "31.5M" is correct to three significant figures at 100% availability; at 70% availability it would be 22.1M but the reference is for production capacity, so 31.5M is the right ceiling figure.
- **Status:** MATCH

### CALC-8: p_ignition rounding — 100 W physical → 0.1 MW in model
- **Claimed:** "At 1 Hz: average power = 100 J × 1 Hz = 100 W = 0.0001 MW. Rounded to 0.1 MW to avoid numerical zero."
- **Re-derived:** 100 J × 1 Hz = 100 W = 0.0001 MW ✓. The model uses 0.1 MW — a 1,000× upward rounding.
- **Status:** MATCH (the arithmetic in the comment is correct; the rounding itself is flagged below as a concern)
- **Notes:** The 100 W → 0.1 MW rounding is 3 orders of magnitude. At 0.1 MW vs. p_implosion=5.71 MW, the ns laser is 1.7% of the ps laser power — the impact on LCOE is negligible, but the rounding should be stated as an approximation order rather than just "to avoid numerical zero." See PA-3.

---

## Model Setup Audit

### MSA-1: ConfinementConcept.LASER_IFE
- **Value:** `ConfinementConcept.LASER_IFE`
- **Source:** docstring rationale (pulsed laser driver → target shot → heat capture → steam cycle; two-laser architecture maps to p_implosion / p_ignition)
- **Status:** TRACED
- **Notes:** Correct base concept. The HB11 architecture is IFE even with the non-standard fuel and fast ignition geometry.

### MSA-2: NET_ELECTRIC_MW = 1000.0
- **Value:** 1000.0 MW
- **Source:** hb11-technology-page-2025.md §Energy Conversion; comment confirmed
- **Status:** TRACED
- **Notes:** Source says "Target: 1 GW baseload power." ✓

### MSA-3: AVAILABILITY = 0.70
- **Value:** 0.70
- **Source:** No primary source cited — analyst assumption
- **Status:** UNTRACED (analyst judgment, documented)
- **Notes:** Adequately explained in comment (rep-rated petawatt laser at 1 Hz is undemonstrated; lower than standard 85%). Appropriate to flag as an assumption.

### MSA-4: blanket_t = 0.05 m
- **Value:** 0.05 m
- **Source:** "hb11-technology-page.md §Key Technical Details"
- **Status:** PARTIAL
- **Notes:** The technology page describes the fuel reaction but does not specify blanket thickness. The value is a modeling choice derived from the concept being aneutronic. Same issue as CV-15 — the citation is imprecise. The ht_shield_t=0.05 self-cites "analysis.md §Section 4" which is acceptable but is a second-order reference.

### MSA-5: p_implosion = 5.71 MW
- **Value:** 5.71 MW
- **Source:** Derived from SCENARIO MATH (gain=500, 1 GW target, 35% thermal efficiency)
- **Status:** TRACED
- **Notes:** Derivation verified in CALC-3. Correctly marked UNCERTAIN. ✓

### MSA-6: p_ignition = 0.1 MW
- **Value:** 0.1 MW
- **Source:** hb11-patent-reactor-design.md §Laser Specifications (Magnetic Field Laser)
- **Status:** TRACED (with concern — see CALC-8)
- **Notes:** Physical value is 0.0001 MW (100 W). Model uses 0.1 MW (1000×). Impact on LCOE is negligible. Comment arithmetic is correct. Rounding should be labeled as ~3 OOM approximation. See PA-3.

### MSA-7: mn = 1.0
- **Value:** 1.0 (no neutron multiplication)
- **Source:** hb11-technology-page.md §Key Technical Details
- **Status:** TRACED (same caveat as CV-15)
- **Notes:** Correct for aneutronic fuel — no breeding blanket, mn=1.0 is appropriate.

### MSA-8: eta_th = 0.35
- **Value:** 0.35
- **Source:** hb11-technology-page-2025.md §Energy Conversion (steam cycle); Z-IFE/LIFE analogues
- **Status:** TRACED
- **Notes:** Appropriate. The steam cycle pivot is documented; 35% is a defensible estimate for pulsed IFE with thermal buffer.

### MSA-9: eta_pin1 = 0.10, eta_pin2 = 0.10
- **Value:** 0.10 each
- **Source:** eta_pin1 → hb11-recent-developments-2024-2025.md §Adelaide Laser Partnership (2025); eta_pin2 → assumed same
- **Status:** TRACED (eta_pin1); UNTRACED (eta_pin2 — explicit assumption)
- **Notes:** eta_pin2 assumption is correctly flagged. Adequate.

### MSA-10: p_trit = 0.0, p_cryo = 0.0
- **Value:** 0.0 each
- **Source:** p_trit → hb11-technology-page.md §Key Technical Details; p_cryo → hb11-patent-reactor-design.md §Magnetic Field Generation
- **Status:** TRACED
- **Notes:** Correct for p-B11 aneutronic concept with no permanent magnet system. ✓

### MSA-11: C220103 = $0.0 (no permanent coils)
- **Value:** $0M
- **Source:** hb11-patent-reactor-design.md §Magnetic Field Generation
- **Status:** TRACED
- **Notes:** Correct. Patent confirms transient capacitor-coil generation with no standing magnet infrastructure.

### MSA-12: C220104 = $0.0 (no NBI)
- **Value:** $0M
- **Source:** Concept type reasoning (laser IS the driver for IFE)
- **Status:** TRACED
- **Notes:** Correct. NBI heating doesn't apply to IFE.

### MSA-13: C220108 = $400M (target factory)
- **Value:** $400M
- **Source:** Scaled from framework default ($244M) by ~1.6× for dual-component requirement
- **Status:** UNTRACED (no primary source for either $244M default or 1.6× scale factor)
- **Notes:** The estimate is appropriately flagged UNCERTAIN. The dual-component rationale (HB11 pellet + capacitor-coil assembly at 31.5M units/year) is well-reasoned. No primary source for $244M default or 1.6× multiplier. Acceptable given the acknowledged uncertainty, but should note the framework default source explicitly.

### MSA-14: CAS21 = $420M (buildings, adjusted)
- **Value:** $420M
- **Source:** Framework default (~$511M) minus deductions ($68M total)
- **Status:** INCORRECT — see CALC-6
- **Notes:** $511M − $68M = $443M ≠ $420M. The arithmetic as documented does not produce the value used. See PA-2.

### MSA-15: Docstring header typo
- **Value:** "1costingfe model setup" (line 1 of docstring)
- **Source:** N/A
- **Status:** Minor — appears to be a typo for "1cfe"
- **Notes:** See PA-6.

---

## Consistency Check

**Section 5 table vs. Section 2 narrative:** The patent inconsistency analysis in Section 2, Challenge 3 is rigorous and well-calculated. However, the Section 5 parameter table has an internal contradiction in the "Net plant electrical output (estimated)" row: the Value/Range column states "~300–500 MWe" while the Source/derivation column independently computes the correct value as "5.25 MW." These two halves of the same cell are inconsistent by a factor of ~60–95×. The derivation is correct; the value/range label is wrong. This is the most significant issue in the analysis (PA-1).

**TRL ratings vs. Section 2 challenges:** The TRL ratings in Section 3 are well-aligned with the challenges described in Section 2. TRL 1 for the avalanche mechanism is consistent with Challenge 1 (zero experimental confirmation). TRL 2–3 for the kT field and rep-rated laser are consistent with Challenges 2 and 5. No inconsistencies found.

**Section 5 parameters vs. model_setup.py:** The model setup correctly uses values from Section 5 (gain=500, eta_pin=10%, steam cycle at 35%, ns laser >100 J). The p_implosion=5.71 MW derivation in the model matches the scenario math in Section 5 exactly. The main discrepancy is the CAS21 arithmetic (PA-2) and the Section 5 table value error (PA-1) — neither is a model-setup/analysis conflict per se, as the model uses $420M directly, independent of the explanation arithmetic.

**Energy conversion pivot documentation:** Both Section 2 (Challenge 4) and the model setup docstring consistently document the 2018 patent → 2020 New Atlas → 2025 website pivot from direct electrostatic to steam cycle. The two source documents are correctly cross-referenced and quoted. Consistent.

**Section 7 cross-concept references:** The cross-references to analyses 07-maglif and 08-frc-w-direct-conversion are analytically sound. The capacitor cost benchmark ($5/J current, <$0.50/J target) is cited to "handwritten exemplar for concept 26 §Key Materials" — this is a second-order citation to another concept's analysis rather than a primary source (TRUMPF/LLNL report). Acceptable for context but could be strengthened with a direct primary source.

---

## Proposed Actions

### PA-1: Section 5 table — "Net plant electrical output (estimated)" value is wrong
- **Category:** calculation-error
- **Severity:** blocking
- **Location:** analysis.md §Section 5, parameter table row "Net plant electrical output (estimated)", Value/Range column
- **Finding:** Value/Range column states "~300–500 MWe at 1 Hz, if gain = 500, laser energy ~30 kJ, η_thermal = 35%." The correct calculation — shown in the adjacent Source column of the same cell — gives 5.25 MW (not MWe ×60–95). The derivation (30 kJ × 500 × 0.35 × 1 Hz = 5.25 MW) is correct. The "~300–500 MWe" range is wrong by ~2 orders of magnitude, likely a copy-paste from a scenario with a much larger laser energy input.
- **Proposed Fix:** Replace "~300–500 MWe at 1 Hz, if gain = 500, laser energy ~30 kJ, η_thermal = 35%" with "~5 MWe at 1 Hz, if gain = 500, laser energy ~30 kJ, η_thermal = 35% (far below 1 GW company target by ~190×)."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: CAS21 buildings override — arithmetic doesn't produce the stated value
- **Category:** calculation-error
- **Severity:** important
- **Location:** model_setup.py, CAS21 cost_overrides comment (lines 219–226)
- **Finding:** Comment states: "Framework default ≈ $511M. Adjustments: −$15M cryogenics, −$47M hot cell, −$6M heat exchanger. Net reduction ≈ −$68M → ~$420M." But $511M − $68M = $443M, not $420M. The discrepancy is $23M. The actual override used in the model is $420M, which is inconsistent with the documented arithmetic.
- **Proposed Fix:** Either (a) correct the override value to $443M, (b) adjust the stated deductions to total $91M (e.g., add a fourth deduction or increase existing ones), or (c) revise the baseline framework default if $511M is incorrect. Add a note explaining the basis for whichever number is chosen.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: p_ignition=0.1 MW is 1000× the physical value — rounding comment understates magnitude
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py, line 139 and accompanying comment (lines 134–139)
- **Finding:** The comment correctly computes 100 J × 1 Hz = 100 W = 0.0001 MW, then rounds to 0.1 MW "to avoid numerical zero." This is a 1,000× (3 orders of magnitude) upward approximation. The comment does not convey the magnitude of the rounding. Impact on LCOE is negligible (ns laser is ~1.7% of ps laser power), but a reader could misinterpret the model as treating the ns laser as 0.1 MW of average load rather than ~0.1 kW.
- **Proposed Fix:** Change comment to: "Rounded up by ~1000× from 0.0001 MW (100 W physical) to avoid numerical zero in framework. Impact on results negligible (<0.01% of total driver power)."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: Funding table citation — A$8.2M sourced to wrong section
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 5, parameter table row "Total company funding," Source column
- **Finding:** The A$8.2M Defence Trailblazer figure is attributed to "hb11-recent-developments-2024-2025.md §FusionXInvest Profile." But §FusionXInvest Profile only contains the outdated $3.57M USD total; the A$8.2M is in §Adelaide Laser Partnership (2025). The FusionXInvest profile predates the Defence Trailblazer grant, so it cannot be the source of that figure.
- **Proposed Fix:** Change source citation to "hb11-recent-developments-2024-2025.md §Adelaide Laser Partnership (2025); §FusionXInvest Profile."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-5: Neutron fraction <1% cited to technology page that doesn't state it
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 5 table, "Neutron fraction" row; model_setup.py blanket_t and mn comments
- **Finding:** Both locations cite hb11-technology-page.md §Key Technical Details for the "<1% neutron fraction" figure. The technology page describes the p-B11 reaction as producing three alpha particles releasing 8.7 MeV, but does not explicitly state a neutron fraction. The <1% figure is established nuclear physics for p-B11 side reactions, not a direct source claim.
- **Proposed Fix:** Add "[established nuclear physics — p-B11 primary reaction is aneutronic; neutrons only from secondary reactions (D-D, n-B11, etc.)]" as a note or change the Source to "[nuclear physics constant]" rather than implying the technology page asserts this value.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-6: Docstring header typo ("1costingfe" → "1cfe")
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py, line 1: `"""Laser ICF — p-B11 Fast Ignition (HB11 Energy): 1costingfe model setup.`
- **Finding:** "1costingfe" appears to be a typo for "1cfe" (project name) or possibly a garbled "costingfe" (framework name).
- **Proposed Fix:** Correct to "1cfe model setup" or "costingfe model setup" as appropriate.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 15
- **Citations verified:** 14
- **Citations not found:** 0
- **Citations partial match (citation imprecise but data correct):** 1 (CV-15: neutron fraction)
- **Calculations checked:** 8
- **Calculations matched:** 6
- **Calculations mismatched:** 2 (CALC-5: Section 5 table value; CALC-6: CAS21 arithmetic)
- **Model parameters audited:** 15 (distinct parameter groups)
- **Parameters fully traced:** 10
- **Parameters partially traced or untraced (with documentation):** 4 (AVAILABILITY, eta_pin2, C220108, ht_shield_t)
- **Parameters with arithmetic error:** 1 (CAS21)
- **Proposed Actions:** 6 (blocking: 1, important: 1, minor: 4)
- **Overall:** HAS ISSUES

The analysis is otherwise of high quality: all direct quotes verified against source documents, the challenge framing is rigorous, TRL ratings are internally consistent, and the scenario math in the model setup is correct. The two calculation errors (Section 5 table value and CAS21 arithmetic) are the priority fixes before this analysis is marked approved.
