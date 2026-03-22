# Review: Magnetic Mirror (D-T)

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 6 files

---

## Citation Verification

### CV-1: "End plug: HTS magnets + modern neutral beams → classical tandem mirror pilot plant with Q > 5"
- **Source cited:** arxiv-2411-06644-confinement-predictions.md §Key Technical Details
- **Status:** FOUND
- **Actual text:** "End plug: HTS magnets + modern neutral beams → classical tandem mirror pilot plant with Q > 5"
- **Notes:** Exact match.

### CV-2: "Primary objective: demonstrate stable sustainment of end-plug plasma conditions required for tandem mirror pilot plant"
- **Source cited:** aps-dpp-2025-sutherland.md §Anvil Device (Next Step)
- **Status:** FOUND
- **Actual text:** "Primary objective: demonstrate stable sustainment of end-plug plasma conditions required for tandem mirror pilot plant"
- **Notes:** Exact match.

### CV-3: "Dual approach 'lowers the Q required to reach net-electric while still using DT fuel'"
- **Source cited:** fusion-report-interview-realta.md §Energy Conversion
- **Status:** FOUND
- **Actual text:** "Dual approach "lowers the Q required to reach net-electric while still using DT fuel""
- **Notes:** Single vs. double quote difference only; content exact match.

### CV-4: "~7 MW per meter as center cell lengthens. Input power remains constant despite increased output."
- **Source cited:** fusion-report-interview-realta.md §Performance Scaling
- **Status:** FOUND
- **Actual text:** Two separate bullets: "~7 MW per meter as center cell lengthens" and "Input power remains constant despite increased output"
- **Notes:** The analysis and model_setup.py join these as a single sentence; the composite is accurate.

### CV-5: "Requires stabilization against MHD and trapped particle modes"
- **Source cited:** arxiv-2411-06644-confinement-predictions.md §Key Technical Details
- **Status:** FOUND
- **Actual text:** "Requires stabilization against MHD and trapped particle modes"
- **Notes:** Exact match.

### CV-6: "$50 million in REBCO tape alone for WHAM++"
- **Source cited:** realta-fusion-hub-spotlight.md §Magnet Specifications
- **Status:** FOUND
- **Actual text:** '"$50 million in REBCO tape alone for WHAM++"'
- **Notes:** Exact match including the internal quotation marks in the source.

### CV-7: "80% of output energy in neutrons" (parameter table footnote [3])
- **Source cited:** realta-fusion-hub-spotlight.md §Fuel & Reaction
- **Status:** FOUND
- **Actual text:** "80% of output energy in neutrons → heat via collisions in reactor blanket"
- **Notes:** Exact match (truncated at →, but the claimed portion is correct).

### CV-8: Parameter table — Hammir pilot targets (>50 MWe, Qe > 1, ≥3 hours)
- **Source cited:** aps-dpp-2025-sutherland.md §Hammir Facility
- **Status:** FOUND
- **Actual text:** "Target: electric gain Qe > 1, net electricity Pe,out > 50 MWe, for at least 3 hours continuously"
- **Notes:** All three values appear in the single source line; parameter table correctly splits them into separate rows.

### CV-9: Parameter table — "50-meter center cell → Q > 5" and "Longer center cell → Q > 10+"
- **Source cited:** arxiv-2411-06644-confinement-predictions.md §Hammir Design; fusion-report-interview-realta.md §Performance Scaling
- **Status:** FOUND
- **Actual text:** arxiv: "50-meter center cell → Q > 5" / "Longer center cell → Q > 10+"; fusion-report: "Longer center cells: Q > 10 possible"
- **Notes:** Both cited sources support the values. Dual citation is appropriate.

### CV-10: Parameter table — "Theoretical output (Q=20 variant) | 500 MWt"
- **Source cited:** fusion-report-interview-realta.md §Performance Scaling
- **Status:** PARTIAL MATCH
- **Actual text:** "Theoretical: 500 MW from Q=20 system"
- **Notes:** Source says "500 MW" without a thermal/electric qualifier. The analysis labels this "500 MWt" (thermal). In context, 500 MW is almost certainly thermal fusion power (consistent with ~7 MWt/m × ~71m cell), so the thermal interpretation is physically reasonable — but the source does not explicitly state MWt. See PA-1.

### CV-11: Parameter table — "$9.5M SVB facility (Feb 2026)"
- **Source cited:** realta-svb-funding-feb2026.md §Key Details
- **Status:** FOUND
- **Actual text:** "$9.5M growth capital facility from Silicon Valley Bank (Feb 17, 2026)"
- **Notes:** Exact match on amount and month; analysis correctly does not claim this adds technical data.

### CV-12: Parameter table — "17 T in-bore; >20 T on-conductor" and "Mirror ratio 10+"
- **Source cited:** wham-experiment-details.md §Magnet System; realta-fusion-hub-spotlight.md §Magnet Specifications
- **Status:** FOUND
- **Actual text:** wham: "17 Tesla in bore, >20 T on the magnets themselves"; spotlight: "Mirror ratio of 10 or higher (vs historical max of ~2)"
- **Notes:** Exact matches.

### CV-13: model_setup.py comment — "$50M in REBCO tape alone for WHAM++ (pre-commercial device)"
- **Source cited:** realta-fusion-hub-spotlight.md §Magnet Specifications
- **Status:** FOUND
- **Actual text:** '"$50 million in REBCO tape alone for WHAM++"'
- **Notes:** Exact match.

### CV-14: model_setup.py comment — "ECH gyrotrons (110 GHz on WHAM): ~45–55% wall-plug efficiency"
- **Source cited:** analysis.md §S3 NBI+ECH subsystem
- **Status:** FOUND (in analysis.md)
- **Actual text:** "ECH gyrotron efficiency improvements toward 50–60% wall-plug efficiency (current generation: ~45–55%)" in analysis.md §S3
- **Notes:** Model cites analysis.md, which cites the general ECH literature (not directly a Phase 1a source). The efficiency range is correct for 110 GHz gyrotrons but is not directly traceable to the wham-experiment-details.md source (which only confirms 110 GHz usage, not efficiency values). This represents a chain of inferences, all internally consistent.

### CV-15: model_setup.py — WHAM REBCO magnets operating temperature
- **Source cited:** wham-experiment-details.md §Magnet System
- **Status:** FOUND (partially)
- **Actual text:** Source states "REBCO HTS magnets from Commonwealth Fusion Systems, 17 Tesla in bore, >20 T on the magnets themselves." The comment adds "(REBCO at 20 K)" as operating temperature.
- **Notes:** The source does not explicitly state 20 K. REBCO typically operates at 10–30 K, and 20 K is the standard CFS operating temperature for REBCO magnets, but this temperature is not in the cited source file. Minor — the value is physically correct and uncontroversial.

---

## Calculation Verification

### CALC-1: f_dec = 0.20 (alpha energy fraction in D-T fusion)
- **Claimed:** "D-T physics: 80% of fusion energy in neutrons, 20% in alpha particles → f_dec = 0.20" (model_setup.py, analysis.md §S2)
- **Re-derived:** D + T → ⁴He (3.52 MeV) + n (14.07 MeV) = 17.59 MeV total. Alpha fraction = 3.52 / 17.59 = 20.01%. Neutron fraction = 80.0%.
- **Status:** MATCH
- **Notes:** Exact. This is a physics constant, not an empirical estimate.

### CALC-2: p_input=100 MW justification — claimed Q~10 → 1000 MWt
- **Claimed:** model_setup.py comment: "for commercial scale Q~10, P_input ~100 MW is consistent with 1000 MWt fusion power target"
- **Re-derived:** If chamber_length=70m and center-cell power scaling = ~7 MWt/m (from fusion-report-interview-realta.md §Performance Scaling), then P_fusion ≈ 70 × 7 = 490 MWt. At P_input=100 MW, implied Q_plasma = 490/100 = **4.9 ≈ 5**, not ~10. For Q~10 at P_input=100 MW, P_fusion would need to be ~1000 MWt, requiring chamber_length ≈ 1000/7 ≈ **143 m** — twice the modeled 70m cell.
- **Status:** MISMATCH
- **Notes:** The comment contains an internal inconsistency. The 70m chamber length is consistent with Q~5 (which is the minimum for the Hammir design point), not Q~10. The 1000 MWt figure is inconsistent with both the 70m cell length and the ~7 MWt/m scaling. The *parameter value* (p_input=100 MW) may still be reasonable — it is an uncertain estimate for a commercial machine — but the *justification in the comment* is wrong: it claims Q~10 and 1000 MWt where the model geometry implies Q~5 and ~490 MWt. See PA-2.

### CALC-3: LCOE unit conversion — `lcoe_ckwh = float(c.lcoe) / 10`
- **Claimed:** Converts $/MWh to ¢/kWh by dividing by 10
- **Re-derived:** 1 MWh = 1000 kWh. $X/MWh = $X/1000 kWh = $(X/1000)/kWh × 100 ¢/$ = X/10 ¢/kWh. So $/MWh ÷ 10 = ¢/kWh. ✓
- **Status:** MATCH
- **Notes:** Conversion is correct.

---

## Model Setup Audit

### MSA-1: ConfinementConcept.MIRROR with Fuel.DT
- **Value:** `CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)`
- **Source:** Concept rationale in docstring + analysis.md §S1 ("axisymmetric tandem magnetic mirror")
- **Status:** TRACED
- **Notes:** Correct concept type for an axisymmetric linear mirror. The rationale section clearly explains the choice.

### MSA-2: NET_ELECTRIC_MW = 500.0
- **Value:** 500.0 MWe (commercial assumption)
- **Source:** Comment cites aps-dpp-2025-sutherland.md §Hammir Facility (pilot: >50 MWe); commercial value is an explicit assumption
- **Status:** TRACED
- **Notes:** The source provides only the pilot target (>50 MWe). The 500 MWe is an acknowledged assumption for commercial relevance. The UNCERTAIN flag and explanation are present and adequate.

### MSA-3: chamber_length = 70.0 m
- **Value:** 70.0 m
- **Source:** arxiv §Hammir Design + fusion-report §Performance Scaling
- **Status:** TRACED
- **Notes:** 50m is the published Hammir design point; 70m is inferred as a Q~8–10 commercial extension. UNCERTAIN flag present. The inference is reasonable but note that the comment's Q~10 claim is inconsistent (see CALC-2, PA-2).

### MSA-4: p_input = 100.0 MW
- **Value:** 100.0 MW NBI+ECH
- **Source:** analysis.md §S5 Missing Parameters (proprietary)
- **Status:** TRACED (parameter acknowledged as UNCERTAIN; source citation self-referential)
- **Notes:** The parameter value may be reasonable but the comment's Q~10/1000 MWt justification is internally inconsistent with chamber_length=70m. See PA-2.

### MSA-5: eta_th = 0.40 — docstring claims "elevated to 0.40 (from 0.40 default)"
- **Value:** 0.40
- **Source:** dossier.md §Key Sources (MARS study); analysis.md §S5 Missing Parameters
- **Status:** INCORRECT (in docstring description)
- **Notes:** The docstring says "eta_th elevated to 0.40 (from 0.40 default)" — if the default is 0.40, the parameter has not been elevated; it is unchanged. The MARS baseline was ~36% = 0.36. One of two things is wrong: (a) the stated default value "0.40" in the docstring is incorrect and the actual mfe_mirror.yaml default is lower (perhaps 0.36), making 0.40 a genuine elevation; or (b) the default is 0.40 and the description should say "retained at 0.40" rather than "elevated." Either way the docstring is misleading. See PA-3.

### MSA-6: f_dec = 0.20
- **Value:** 0.20
- **Source:** realta-fusion-hub-spotlight.md §Fuel & Reaction + D-T physics
- **Status:** TRACED
- **Notes:** Correctly derived from D-T physics (20% alpha energy fraction). Citation and derivation chain both present.

### MSA-7: eta_de = 0.54
- **Value:** 0.54 (MARS 1983 gridless DEC efficiency)
- **Source:** dossier.md §Key Sources (MARS study, Logan 1983) + analysis.md §S2, §S3
- **Status:** TRACED (via dossier.md, not in review scope)
- **Notes:** The value is well-established in the analysis narrative and appropriately labeled as a historical lower-bound. Dossier.md is outside the available Phase 1a sources but is a registered project document. No factual concern.

### MSA-8: p_coils = 10.0 MW — cited to wham-experiment-details.md §Magnet System
- **Value:** 10.0 MW (elevated from 5 MW default)
- **Source:** wham-experiment-details.md §Magnet System
- **Status:** PARTIALLY TRACED
- **Notes:** The cited source describes magnet field strength and materials (REBCO, 17 T, 20 K) but does not state a coil power value. The elevation from 5 MW to 10 MW is a reasonable inference for a larger commercial REBCO array, but the citation does not support the specific 10 MW figure — it supports the *rationale* (larger magnet set, HTS material) without providing a number. This is acceptable given the UNCERTAIN flag, but the citation is loose. See PA-4.

### MSA-9: cost_overrides = {}
- **Value:** No overrides
- **Source:** Justified in docstring and inline comment: "Realta has published zero plant-level cost data"
- **Status:** TRACED
- **Notes:** The explicit statement that no override data exists, with the specific explanation that the $50M REBCO proxy cannot be extrapolated, is thorough and accurate. The approach is correct.

### MSA-10: R0 = 0.0 (no toroidal axis offset)
- **Value:** 0.0
- **Source:** Physical reasoning (cylindrical geometry, not toroidal)
- **Status:** TRACED
- **Notes:** Correct. A linear mirror has no major radius. The note is adequate.

---

## Consistency Check

**Section 2 narrative vs. Section 5 parameters:**
All Section 5 parameter values are consistent with Section 2 narrative claims. The 50m/Q>5 design point appears in both. The DEC efficiency of ~54% (MARS) is flagged as historical in both. The f_dec=0.20 (alpha fraction) is derived from the same 80% neutron energy fraction cited in §S2 Challenge 2 and §S3 DEC subsystem. No conflicts found.

**TRL ratings vs. challenges:**
- DEC (TRL 2–3) is the lowest-rated subsystem, consistent with §S2 Challenge 2 calling it "undefined." ✓
- Tandem mirror confinement with HTS (TRL 3–4) correctly reflects that WHAM demonstrates simple mirror but not tandem configuration. §S2 Challenge 1 emphasizes this gap. ✓
- NBI+ECH (TRL 6–8) rated high, consistent with §S2 treatment as a scaling issue rather than a fundamental gap. ✓
- Tritium blanket (TRL 2–3) correctly reflects zero Realta-specific blanket data, consistent with §S1 and §S5 gap inventory. ✓

**Model setup vs. parameter table:**
- chamber_length=70m is not in the parameter table (50m is the published design point). The 70m is a model-setup inference, clearly flagged UNCERTAIN. Consistent.
- p_input=100 MW matches §S5 Missing Parameters listing "NBI + ECH auxiliary power for Hammir | proprietary | blocking." Consistent.
- eta_th=0.40 is consistent with §S5 "~36% overall" for MARS with stated modern improvement allowance. Consistent.
- The **Q-value inconsistency** in the p_input comment (Q~10 claimed, Q~5 implied by geometry) is an internal inconsistency between the model_setup.py comment and the scaling data in §S5 / the arxiv source. See PA-2.

**One cross-concept reuse concern:**
The model_setup.py docstring mentions "MARS 1983 baseline ~36%" and cites `dossier.md §Key Sources` throughout. The dossier.md is a project-internal document not included in the Phase 1a source set. Values attributed to it (MARS TBR=1.15, plant efficiency ~36%, DEC ~54%) are well-established historical numbers consistent with the open literature, and their use is appropriate — but they cannot be verified against the provided source files.

---

## Proposed Actions

### PA-1: Clarify "500 MWt" unit in parameter table
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §S5 parameter table, row "Theoretical output (Q=20 variant)"
- **Finding:** Source (fusion-report-interview-realta.md) says "500 MW from Q=20 system" without specifying thermal or electric. The analysis labels this "500 MWt." The interpretation is physically reasonable (500 MWt ÷ 7 MWt/m ≈ 71m center cell, consistent with Q=20 at modest P_input) but the unit qualifier is not in the source.
- **Proposed Fix:** Add a parenthetical note: "500 MW (interpreted as thermal fusion power; source does not specify unit)" or add a confidence note explaining the unit inference.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: Fix p_input comment — Q~10 claim is inconsistent with chamber_length=70m
- **Category:** inconsistency
- **Severity:** important
- **Location:** model_setup.py line 110–113 (p_input comment)
- **Finding:** The comment states "for commercial scale Q~10, P_input ~100 MW is consistent with 1000 MWt fusion power target." However, with chamber_length=70m and ~7 MWt/m scaling (from the cited source), P_fusion ≈ 490 MWt, which implies Q_plasma ≈ 4.9 at P_input=100 MW — consistent with the Hammir Q>5 design point, not Q~10. For Q~10 at P_input=100 MW, the center cell would need to be ~143m. The stated Q~10/1000 MWt justification is wrong for the chosen chamber_length.
- **Proposed Fix:** Revise the comment to: "Estimated for commercial scale Q~5 (consistent with 70m center cell at ~7 MWt/m ≈ 490 MWt); P_input=100 MW is consistent with this fusion power target. If Q~10 were targeted, chamber_length would need to be ~140m and/or P_input reduced. Source: arxiv §Hammir Design (50m→Q>5); fusion-report §Performance Scaling (~7 MWt/m)." If the intent is to model Q~10, either increase chamber_length to ~140m or reduce p_input to ~50 MW.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: Fix eta_th docstring — "elevated to 0.40 (from 0.40 default)" is self-contradictory
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py lines 22–24 (Concept Choice Rationale / Key Deviations docstring)
- **Finding:** The docstring reads "eta_th elevated to 0.40 (from 0.40 default; consistent with MARS 1983 baseline ~36% with modest allowance for modern steam-cycle improvement)." If the default is 0.40, the value has not been elevated — it is unchanged. If the actual mfe_mirror.yaml default for a mirror is less than 0.40 (e.g., 0.36 matching MARS), then the docstring incorrectly states the default as 0.40. Either way, the sentence is misleading.
- **Proposed Fix:** Check mfe_mirror.yaml to determine the actual default for eta_th. If the default is 0.36 (MARS baseline), correct the docstring to "eta_th elevated to 0.40 (from 0.36 MARS-analogous default; modern steam cycle allows modest improvement)." If the default is genuinely 0.40, change "elevated" to "retained": "eta_th retained at framework default of 0.40 (MARS 1983 overall plant efficiency was ~36%; 0.40 reflects modest modern improvement)."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: Strengthen p_coils citation — wham source doesn't provide a power number
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py line 144–149 (p_coils comment)
- **Finding:** The citation `wham-experiment-details.md §Magnet System` is listed as supporting p_coils=10 MW. The source describes field strength and materials (REBCO, 17 T) but contains no coil power figure. The 10 MW value is an inference from magnet scale, not a directly sourced number.
- **Proposed Fix:** Revise the comment to make clear this is an inferred value, not a cited one: "UNCERTAIN: no coil power published for Hammir or any mirror-scale HTS system. Elevated from mfe_mirror.yaml default (5 MW) based on inference: larger commercial REBCO array (end plugs ≥ WHAM scale + 70m center-cell solenoids) will draw more cooling and control power than the default. Source for rationale: wham-experiment-details.md §Magnet System (REBCO material and scale). No quantitative source exists."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 15
- **Citations verified:** 14
- **Citations not found:** 0
- **Partial matches:** 1 (CV-10: "500 MW" without thermal/electric qualifier; CV-15: REBCO 20 K operating temperature not in source)
- **Calculations checked:** 3
- **Calculations matched:** 2 (f_dec, LCOE conversion)
- **Calculations mismatched:** 1 (p_input comment claims Q~10/1000 MWt; geometry implies Q~5/490 MWt)
- **Model parameters audited:** 10
- **Parameters fully traced:** 7
- **Parameters partially traced:** 2 (p_coils, eta_th docstring)
- **Parameters with incorrect description:** 1 (eta_th "elevated from 0.40 default")
- **Proposed Actions:** 4 (blocking: 0, important: 1, minor: 3)
- **Overall:** HAS ISSUES
