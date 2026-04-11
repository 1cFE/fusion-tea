# Review: Magnetic Mirror (D-T)

**Iteration:** 2
**Date:** 2026-03-29
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 11 files

---

## Citation Verification

### CV-1: Hammir pilot plant targets — Qe > 1, Pe,out > 50 MWe, ≥3 hours continuous
- **Source cited:** aps-dpp-2025-sutherland.md §Hammir Facility (Pilot Plant)
- **Status:** FOUND
- **Actual text:** "Target: electric gain Qe > 1, net electricity Pe,out > 50 MWe, for at least 3 hours continuously"
- **Notes:** Exact match. Section heading "### Hammir Facility (Pilot Plant)" exists in source.

---

### CV-2: Q > 5 at 50-meter center cell
- **Source cited:** arxiv-2411-06644-confinement-predictions.md §Hammir Design
- **Status:** FOUND
- **Actual text:** Abstract: "a fusion gain Q > 5"; Table 3: Q = 5.8 (Optimum), Q = 5.0 (Alternate) at 50 m center cell
- **Notes:** Q > 5 confirmed. However, no section called "§Hammir Design" exists in the paper — it uses numbered sections (§1–§5). "§Hammir Design" is an informal descriptor not traceable to a specific section. See PA-2.

---

### CV-3: "Longer center cell → Q > 10+"
- **Source cited:** arxiv-2411-06644-confinement-predictions.md §Hammir Design (analysis.md §1 block quote; model_setup.py L85)
- **Status:** NOT FOUND in cited source
- **Actual text (arXiv):** The arXiv paper demonstrates Q = 5.8 at 50 m center cell and shows Q scales with length, but contains no statement that "Q > 10" is achievable. The phrase "Q > 10" does not appear in the paper body.
- **Notes:** The Q > 10 claim appears in the introduction of the **Fusion Report interview** (fusion-report-interview-realta.md): "longer center cells can produce Q>10 energy gain results." This is the interview author paraphrasing the arXiv paper — it is not a direct arXiv finding. The analysis and model_setup.py both attribute this claim to the arXiv paper rather than the interview. Misattribution — see PA-1.

---

### CV-4: ~7 MW per meter scaling law; input power constant with length; 500 MW Q=20 scenario
- **Source cited:** fusion-report-interview-realta.md §Performance Scaling
- **Status:** FOUND
- **Actual text:** "this increases by roughly 7 MW per meter. Interestingly, the input power does not change, even as the center cell gets longer. There is a scenario where you could get 500 MW out of a Q=20 system."
- **Notes:** Content confirmed. No section "§Performance Scaling" exists in the source; this is in the interview Q&A body text. Informal section descriptor — see PA-2.

---

### CV-5: Dual energy conversion — thermal blanket captures neutron energy; DEC captures alpha energy; "lowers the Q required to reach net-electric"
- **Source cited:** fusion-report-interview-realta.md §Energy Conversion
- **Status:** FOUND
- **Actual text:** "while the neutron's energy can be captured through a typical thermal blanket approach (which also produces new tritium from the lithium in the thermal blanket), the energy in the 'ash' (in this case a charged helium nucleus) can be captured as well as it is expelled from the fusion chamber, and use direct energy conversion to generate electricity. Using direct energy conversion lowers the Q required to reach net-electric while still using DT fuel for first generation systems."
- **Notes:** Content confirmed. No section "§Energy Conversion" exists; the text is in "What is a Tandem Magnetic Mirror?" See PA-2.

---

### CV-6: "$50 million in REBCO tape alone for WHAM++"
- **Source cited:** realta-fusion-hub-spotlight.md §Magnet Specifications
- **Status:** FOUND
- **Actual text:** "$50 million in REBCO tape alone for WHAM++, although that is expected to be the majority of the cost"
- **Notes:** Content confirmed. No section "§Magnet Specifications" exists in the source — the claim appears in the general introductory text before any subheadings. See PA-2.

---

### CV-7: WHAM — 17 T in-bore HTS magnets, world record for magnetically confined plasma, CFS-built REBCO
- **Source cited:** wham-experiment-details.md §Magnet System
- **Status:** FOUND
- **Actual text:** "At 17 Tesla, these magnets set a world record in magnetic field strength for magnetically confined plasmas." / "Two mirror coils will be constructed using REBCO high temperature superconducting material by CFS (17 T mirrors)."
- **Notes:** Content confirmed. No section "§Magnet System" exists; the source is a single narrative. See PA-2.

---

### CV-8: WHAM magnets ">20 T on conductor"
- **Source cited:** wham-experiment-details.md §Magnet System (implied by analysis.md §S3 claim)
- **Status:** NOT FOUND
- **Actual text:** Not found in wham-experiment-details.md or any other ingested source. Both sources confirm 17 T in-bore; no "20 T on conductor" language appears in any ingested document.
- **Notes:** The ">20 T on conductor" spec may originate from the Endrizzi et al. 2023 WHAM physics paper (not ingested). The claim is physically plausible for REBCO at this field level but lacks a traceable source in the current ingested set. See PA-5.

---

### CV-9: D-T physics — 80% of fusion energy in 14.1 MeV neutrons, 20% in 3.5 MeV alphas
- **Source cited:** realta-fusion-hub-spotlight.md §Fuel & Reaction; analysis.md
- **Status:** FOUND
- **Actual text (spotlight):** "Fusion reactors with DT fuel cycles will produce 80% of their output energy in the form of neutrons which then produce heat energy via their collisions in the reactor blanket." (appears in §Target Markets)
- **Notes:** Content confirmed. No section "§Fuel & Reaction" exists — relevant text is under §Target Markets within "Realta's Go-to-Market Strategy." The 20%/80% split is fundamental D-T nuclear physics and is unambiguously correct. See PA-2.

---

### CV-10: DCLC and Alfvén ion cyclotron instabilities; stabilization via sloshing ions + vortex flows
- **Source cited:** arxiv-2411-06644-confinement-predictions.md §Key Technical Details; realta-fusion-hub-spotlight.md §Stabilization
- **Status:** FOUND (both sources, different section names)
- **Actual text (spotlight):** "Important kinetic instabilities... are the drift cyclotron loss cone (DCLC) instability and Alfven Ion Cyclotron (AIC) instability. Realta is proposing to use 'sloshing ions' to help stabilize such micro-instabilities." (§Kinetic Stability) / "Realta is also proposing to use vortex stabilization to mitigate MHD instability." (§MHD Stability)
- **Actual text (arXiv):** DCLC extensively discussed; sloshing ions used for DCLC stabilization; Bayesian ML optimization described in §4.
- **Notes:** Content confirmed from both sources. Spotlight sections are "§Kinetic Stability" and "§MHD Stability", not "§Stabilization"; arXiv has no section "§Key Technical Details". See PA-2.

---

### CV-11: $9.5M SVB growth capital, February 2026
- **Source cited:** realta-svb-funding-feb2026.md §Key Details
- **Status:** FOUND
- **Actual text:** "Silicon Valley Bank... has provided a growth capital facility of $9.5 million to fusion energy startup Realta Fusion"
- **Notes:** Content confirmed. No section "§Key Details" in source (single press release text). See PA-2.

---

## Calculation Verification

### CALC-1: D-T alpha energy fraction = 20%
- **Claimed:** "D-T physics: 80% of fusion energy in neutrons, 20% in alphas → f_dec = 0.20" (model_setup.py L170–175; analysis.md §S2.4)
- **Re-derived:** D + T → ⁴He (3.52 MeV) + n (14.07 MeV) = 17.59 MeV total. Alpha fraction = 3.52/17.59 = 20.01%.
- **Status:** MATCH
- **Notes:** Exact. Physical constant, not empirical.

---

### CALC-2: DEC thermodynamic contribution ≈ 11% of plant thermal output
- **Claimed:** "~54% DEC efficiency × 20% alpha fraction = 0.20 × 0.54 ≈ 11% of the thermal output" (analysis.md §S2.4)
- **Re-derived:** 0.20 × 0.54 = 0.108 ≈ 10.8% ≈ 11%
- **Status:** MATCH

---

### CALC-3: 7 MW/m × 70 m → ~490 MWt
- **Claimed:** "at ~7 MWt/m → ~490 MWt fusion power" (model_setup.py L87)
- **Re-derived:** 7 × 70 = 490
- **Status:** MATCH

---

### CALC-4: Q_plasma ≈ 7 at p_input=70 MW and ~490 MWt
- **Claimed:** "At 70 MW input and ~490 MWt fusion power: Q_plasma ≈ 7" (model_setup.py L135)
- **Re-derived:** Q = 490/70 = 7.0
- **Status:** MATCH

---

### CALC-5: arXiv Table 3 — implied total input heating power for Hammir pilot (50 m design)
- **Claimed:** analysis.md §S5 lists "NBI + ECH total input power" as a blocking gap with "40–100 MW" range from prior analyses. model_setup.py uses 70 MW (midpoint).
- **Re-derived from primary source:** arXiv Table 3 gives P_fusion = 175 MW (Optimum), Q = 5.8 → **P_input = P_fusion/Q = 175/5.8 ≈ 30.2 MW**. Alternate case: 200 MW / 5.0 = **40.0 MW**. End plug NBI power alone is listed at 15 MW (Optimum) / 20 MW (Alternate).
- **Status:** MISMATCH
- **Notes:** The arXiv paper's Table 3 directly implies total system input power ≈ 30–40 MW for the 50 m pilot design — at the very low end of or below the "40–100 MW" uncertainty range stated in the analysis. The Fusion Report "constant input power" thesis further implies this value may apply at commercial length (70 m) as well. The model uses 70 MW, which may be 1.75–2.3× the arXiv-implied value. This is the single largest tractable discrepancy between the model and the primary source data. See PA-3.

---

### CALC-6: LCOE unit conversion — $/MWh to ¢/kWh via ÷10
- **Claimed:** `lcoe_ckwh = float(c.lcoe) / 10` (model_setup.py L205)
- **Re-derived:** 1 MWh = 1000 kWh; $X/MWh = X/1000 $/kWh = X/1000 × 100 ¢/kWh = X/10 ¢/kWh
- **Status:** MATCH

---

## Model Setup Audit

### MSA-1: ConfinementConcept.MIRROR, Fuel.DT
- **Value:** `CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)`
- **Source:** Concept rationale docstring; analysis.md §S1
- **Status:** TRACED
- **Notes:** Correct concept type. Rationale is clearly stated.

---

### MSA-2: PLASMA_T = 1.5 m — labeled DEFAULT, comment "no Hammir plasma radius published"
- **Value:** 1.5 m
- **Source:** model_setup.py comment: "UNCERTAIN: no Hammir plasma radius published. Keeping framework default." Cites "mfe_mirror.yaml default"
- **Status:** INCORRECT PREMISE
- **Notes:** The arXiv paper (Table 3) gives Hammir central cell plasma radius as **0.54 m (Optimum)** or **0.78 m (Alternate)**. The comment "no Hammir plasma radius published" is factually incorrect — a primary source exists. Using 1.5 m (2–3× the published value) affects plasma volume (scales as r²), fusion power density, blanket surface area, and reactor building volume. This is likely the largest unacknowledged error in the model. See PA-4.

---

### MSA-3: CHAMBER_LENGTH = 70.0 m — extrapolated from 50 m pilot + "Q > 10" projection
- **Value:** 70.0 m
- **Source:** arxiv Table 3 (50 m pilot point); fusion-report-interview-realta.md (Q > 10 for longer cells)
- **Status:** TRACED (inferred extrapolation; 70 m not stated in any source)
- **Notes:** The Q > 10 claim that motivates going beyond 50 m is from the Fusion Report interview, not the arXiv paper — see CV-3/PA-1. The extrapolation logic (7 MW/m) is sound. UNCERTAIN flag present.

---

### MSA-4: p_input = 70.0 MW — midpoint of 40–100 MW uncertainty range
- **Value:** 70.0 MW
- **Source:** analysis.md §S2 Challenge 3, §S5 Missing Parameters (prior model runs)
- **Status:** PARTIALLY TRACED
- **Notes:** The 40 MW and 100 MW bounds come from two prior model runs, not from any primary source. The arXiv paper implies ≈30–40 MW for the pilot design (see CALC-5). The 70 MW midpoint may be 1.75–2.3× the arXiv-implied value, and the model comment does not acknowledge the arXiv data point. See PA-3.

---

### MSA-5: eta_th = 0.38 — MARS analogue (36% baseline + modest improvement)
- **Value:** 0.38
- **Source:** analysis.md §S5 (MARS analogue); MARS study not ingested as primary source
- **Status:** TRACED to analysis.md only
- **Notes:** MARS study is not an ingested source. Value is labeled UNCERTAIN and physically reasonable. The deviation from the 36% MARS baseline to 0.38 is a modest improvement assumption; adequately justified.

---

### MSA-6: eta_de = 0.54 — MARS 1983 gridless DEC efficiency
- **Value:** 0.54
- **Source:** analysis.md §S5, §S2 Challenge 4; MARS study not ingested
- **Status:** TRACED to analysis.md only
- **Notes:** MARS study not ingested. Moir & Barr 1973 venetian-blind reference appears in the arXiv bibliography (line 407), confirming the citation exists. Value is well-labeled as historically analogous but concept-mismatched (gridless ≠ venetian blind). Acceptable.

---

### MSA-7: f_dec = 0.20 — D-T alpha fraction
- **Value:** 0.20
- **Source:** realta-fusion-hub-spotlight.md (§Target Markets); D-T nuclear physics
- **Status:** TRACED and CORRECT
- **Notes:** CALC-1 confirms. The additional caveat (fraction of alphas actually captured at electrodes is a further unknown) is appropriately noted in the comment.

---

### MSA-8: NET_ELECTRIC_MW = 500.0 — commercial assumption
- **Value:** 500.0 MWe
- **Source:** Fusion Report interview — "50–500 MW of power" range; APS DPP pilot target >50 MWe
- **Status:** TRACED
- **Notes:** 500 MWe is the upper bound of the published range. UNCERTAIN flag present. Appropriate for cross-concept LCOE comparison.

---

### MSA-9: p_coils = 10 MW, p_cryo = 2 MW — inferred elevations
- **Value:** 10 MW, 2 MW
- **Source:** wham-experiment-details.md §Magnet System (qualitative REBCO reference only)
- **Status:** PARTIALLY TRACED
- **Notes:** The cited source describes material and field strength but contains no power draw figures. Both values are inferences from magnet scale, labeled UNCERTAIN. p_cryo reasoning (REBCO at ~20 K vs. LTS at 4 K → reduced cryo load) is physically sound but the 2 MW figure is unsourced. Acceptable given data absence and explicit uncertainty flag.

---

### MSA-10: cost_overrides = {} — no overrides
- **Value:** Empty dict
- **Source:** Docstring: "Realta has published zero plant-level cost data"
- **Status:** TRACED
- **Notes:** Correct and well-justified. The $50M REBCO proxy is correctly identified as non-extrapolatable to a commercial CAS22 estimate.

---

## Consistency Check

**Section 5 parameter table vs. Section 2 narrative:** All parameter table values are consistent with Section 2 narrative claims. The Q > 5 / Q > 10 distinctions, 50 m pilot vs. commercial length, and input power uncertainty are consistently presented throughout.

**TRL ratings vs. challenges:** TRL assignments are calibrated against described capability gaps. DEC (TRL 4–5) is appropriate given 1970s lab demonstrations but no fusion-condition operation. End-plug confinement (TRL 3–4) reflects WHAM operation of simple mirror but no tandem or Anvil results. Blanket (TRL 2–3) correctly reflects zero Realta-specific design data. NBI/ECH (TRL 6–7) correctly reflects commercial availability with scale caveats.

**model_setup.py vs. analysis.md:** All model parameters trace to explicit analysis.md sections. No parameter is absent from the analysis narrative. The model docstring's "Key Deviations from mfe_mirror.yaml Defaults" matches the analysis discussion.

**arXiv MHD/trapped-particle claim:** Section 2.1 states the arXiv paper "explicitly acknowledges that 'stabilization against MHD and trapped particle modes' is required." More precisely, the arXiv conclusions state these topics "have not been addressed here and will be the topic of a future publication" — the paper assumes MHD stability rather than analyzing it. The analysis's characterization is slightly overstated but directionally correct.

**Internal Q consistency:** At p_input = 70 MW and ~490 MWt (7 MW/m × 70 m), Q_plasma = 7, which is consistent with the arXiv Q ≈ 5.8 at 50 m design point extrapolated to 70 m. This is internally consistent.

**MARS-derived values (eta_th, eta_de, LCOE ~7 ¢/kWh 1983$):** The MARS study is not ingested as a Phase 1a source; these values are routed through the handwritten exemplar. The analysis correctly flags them as analogues and documents this limitation in §S8.

---

## Proposed Actions

### PA-1: Q > 10 claim is misattributed to arXiv paper
- **Category:** citation-error
- **Severity:** important
- **Location:** analysis.md §S1 block quote; model_setup.py L85
- **Finding:** "Longer center cell → Q > 10+" is cited as from `arxiv-2411-06644-confinement-predictions.md §Hammir Design`. The arXiv paper does not state Q > 10 anywhere. The Q > 10 claim appears in the Fusion Report interview introduction (fusion-report-interview-realta.md): "longer center cells can produce Q>10 energy gain results" — the interview author paraphrasing the arXiv results. The arXiv demonstrates Q = 5.8 at 50 m.
- **Proposed Fix:** Change the citation for the "Q > 10" claim from the arXiv paper to `fusion-report-interview-realta.md`. Add a note that this is a secondary-source characterization of the arXiv paper's scaling behavior, not a direct arXiv result. Update model_setup.py L85 accordingly.
- **Decision:** alternative
- **User Notes:** Cite both sources with correct attribution: arXiv demonstrates Q = 5.8 at 50 m (primary); Fusion Report interview extrapolates "Q > 10 possible" for longer center cells (secondary). Call out the nuance rather than dropping one citation.

---

### PA-2: Systematic invented section headings in citations
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §§1,2,3,4,5; model_setup.py passim
- **Finding:** Multiple citations use informal section descriptors that don't correspond to actual section headings in the source documents:
  - `§Hammir Design` → arXiv uses numbered sections (§1–§5); no matching heading
  - `§Performance Scaling` → Fusion Report has no such heading; in interview Q&A body
  - `§Energy Conversion` → Fusion Report has no such heading; in "What is a Tandem Magnetic Mirror?"
  - `§Magnet Specifications` → Fusion Hub Spotlight has no such heading; in intro text
  - `§Fuel & Reaction` → Spotlight has no such heading; content in §Target Markets
  - `§Stabilization` → Spotlight uses §Kinetic Stability and §MHD Stability
  - `§Key Technical Details` → arXiv uses numbered sections
  - `§Magnet System` → wham-experiment-details.md has no section headings
  - `§Key Details` → realta-svb-funding-feb2026.md has no section headings
  - **Correctly cited:** §Hammir Facility (Pilot Plant), §Anvil Device (Next Step), §WHAM Experiment in aps-dpp-2025-sutherland.md
- **Proposed Fix:** Update section citations to match actual source structure. For sources without section headings, cite by document title only. For arXiv, cite by section number (§3 POPCON, §4 Table 3) or describe the specific table/figure.
- **Decision:** reject
- **User Notes:** The section headings exist in the extracted .orig.md source files (created by the extraction agent). Citations are correct against the ingested sources, which is the relevant standard for this pipeline.

---

### PA-3: p_input = 70 MW doesn't incorporate arXiv-implied pilot design input power
- **Category:** factual-concern
- **Severity:** important
- **Location:** analysis.md §S2 Challenge 3; §S5 Missing Parameters; model_setup.py L129–L136
- **Finding:** The model uses p_input = 70 MW as "midpoint of 40–100 MW uncertainty range" derived from two prior model runs. However, arXiv Table 3 provides a direct published data point: P_fusion = 175 MW, Q = 5.8 → **P_input ≈ 30 MW** (Optimum); P_fusion = 200 MW, Q = 5.0 → **P_input = 40 MW** (Alternate). These are the only published operating points for any Hammir-class design. Combined with the "constant input power with length" claim from the Fusion Report interview, this implies the 70 m commercial design may use ≈30–40 MW, not 70 MW. At 30 MW input with ~490 MWt fusion power, Q_plasma ≈ 16 — substantially better than the modeled Q ≈ 7, with lower recirculating fraction and better LCOE. The current model likely underestimates Q and overestimates LCOE.
- **Proposed Fix:** (1) Add the arXiv-derived p_input ≈ 30–40 MW to the §S5 parameter table as a "medium" confidence data point, citing arXiv Table 3. (2) Update the model comment to flag 30–40 MW as the arXiv-anchored estimate vs. 40–100 MW from prior model runs. (3) Consider running the model at p_input = 35 MW (arXiv-midpoint extrapolation) to provide an optimistic LCOE bracket alongside the current 70 MW conservative case.
- **Decision:** agree
- **User Notes:** Verified: arXiv Table 3 data (P_fusion=175 MW, Q=5.8, P_input≈30 MW) is present in the full extraction output.md but was lost in the .orig.md summary. The data has been in our sources all along.

---

### PA-4: PLASMA_T = 1.5 m ignores published Hammir central cell plasma radius
- **Category:** model-bug
- **Severity:** important
- **Location:** model_setup.py L78–L79
- **Finding:** The model comment states "no Hammir plasma radius published. Keeping framework default." This is factually incorrect. The arXiv paper (Table 3) gives the Hammir central cell plasma radius as **0.54 m (Optimum)** or **0.78 m (Alternate)**. The model uses 1.5 m — 2–3× the published values. Plasma radius directly affects calculated plasma volume (scales as r²), and propagates into fusion power density, blanket surface area, reactor building volume, magnet quantities, and CAS22/CAS21 costs. Using a radius 2–3× too large likely inflates capital cost significantly.
- **Proposed Fix:** Update PLASMA_T to a value consistent with the arXiv data. For the 70 m commercial design, a radius modestly larger than the 50 m pilot's 0.54–0.78 m is defensible; a range of 0.6–1.0 m is reasonable. Set PLASMA_T = 0.75 as a central estimate and update the comment: "arXiv Table 3 gives 0.54 m (Optimum) to 0.78 m (Alternate) for the 50 m pilot. Using 0.75 m as a central estimate for a 70 m commercial design; commercial radius may be modestly larger if power density is maintained. Source: arxiv-2411-06644 Table 3."
- **Decision:** agree
- **User Notes:** Verified: arXiv Table 3 gives 0.54 m (Optimum) / 0.78 m (Alternate). Data present in full extraction output.md. The model comment "no Hammir plasma radius published" is factually wrong.

---

### PA-5: ">20 T on conductor" for WHAM magnets lacks an ingested source
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §S3 (HTS Axisymmetric Mirror Magnets section)
- **Finding:** The analysis states WHAM operates at "17 T in-bore (>20 T on conductor)." The 17 T in-bore value is confirmed in wham-experiment-details.md and aps-dpp-2025-sutherland.md. The ">20 T on conductor" spec does not appear in any ingested source. It likely originates from Endrizzi et al. 2023 (Journal of Plasma Physics, not ingested). The claim is physically plausible for REBCO at this operating point but is currently untraced in the ingested source set.
- **Proposed Fix:** Either (a) ingest Endrizzi et al. 2023 and add a proper citation, or (b) note "[unverified in ingested sources; likely from Endrizzi et al. 2023 WHAM physics basis paper]" alongside the claim.
- **Decision:** agree
- **User Notes:** Add the caveat note inline. Low priority — not cost-driving.

---

### PA-6: arXiv citation "§Hammir Design" should reference specific table/section
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §S1; model_setup.py L82–L88
- **Finding:** The arXiv paper's key quantitative results (Q = 5.8 at 50 m, central cell parameters, operating conditions) are in Table 3 (§4: "Simulation of an optimized end plug") and the abstract. "§Hammir Design" is not a navigable reference. A reviewer following the citation cannot locate the specific table without reading the full paper.
- **Proposed Fix:** Replace "§Hammir Design" with specific navigation targets: the abstract for Q > 5 claims; "§4 Table 3" for the 50 m operating point parameters (Q = 5.8, P_fusion = 175 MW, central cell radius 0.54 m); "§3 POPCON analysis" for the central cell performance requirements. This enables direct source verification.
- **Decision:** reject
- **User Notes:** Same reasoning as PA-2 — §Hammir Design exists in the extracted .orig.md. Will be addressed naturally if/when the .orig.md summary is updated to include Table 3 data.

---

## Summary

- **Total citations checked:** 11
- **Citations verified:** 9
- **Citations not found / misattributed:** 2 (CV-3: Q > 10 attributed to wrong source; CV-8: ">20 T on conductor" not in any ingested source)
- **Calculations checked:** 6
- **Calculations matched:** 5 (CALC-1 through CALC-4, CALC-6 correct)
- **Calculation mismatches:** 1 (CALC-5: arXiv-implied p_input ≈ 30–40 MW vs. model's 70 MW midpoint)
- **Model parameters audited:** 10
- **Parameters fully traced:** 7
- **Parameters with issues:** 2 (MSA-2: plasma radius ignores arXiv data; MSA-4: p_input range doesn't incorporate arXiv anchor)
- **Parameter with incorrect premise:** 1 (MSA-2: "no Hammir plasma radius published" is wrong)
- **Proposed Actions:** 6 (blocking: 0, important: 3 [PA-1, PA-3, PA-4], minor: 3 [PA-2, PA-5, PA-6])
- **Overall:** HAS ISSUES

### Key Findings Summary

**Most significant (PA-3, PA-4):** The model fails to use two quantitative parameters available in the primary arXiv source (Table 3):
- Central cell plasma radius: arXiv gives 0.54–0.78 m; model uses 1.5 m (2–3× overestimate; likely inflates capital costs)
- Total input heating power: arXiv implies ≈30–40 MW for the pilot design; model uses 70 MW (1.75–2.3× too high if "constant input power" thesis holds; likely underestimates Q and overestimates LCOE)

Both errors bias the model in the same direction: the LCOE estimate is likely too high relative to what the Hammir design data supports. This does not invalidate the structural estimate but tightens the defensible uncertainty range.

**Systematic citation style (PA-2):** Informal section descriptors are used throughout instead of actual source headings. This is a quality issue that makes citation verification difficult but does not indicate factual errors in most cases.

**Q > 10 misattribution (PA-1):** The justification for modeling a 70 m commercial design (rather than the published 50 m pilot) rests partly on the Q > 10 claim, which is in a secondary source (Fusion Report interview), not the primary arXiv paper. The arXiv shows Q = 5.8 at 50 m; Q > 10 is a secondary-source extrapolation.
