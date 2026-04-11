# Review: Magnetic Mirror (p-B11)

**Iteration:** 1
**Date:** 2026-03-22
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 4 files

---

## Citation Verification

### CV-1: Bremsstrahlung quote (Section 2, Challenge 1)
- **Source cited:** princeton-arpa-e-funding-2022.md §Technical Approach
- **Status:** FOUND
- **Actual text:** "at required temperatures (~150-300 keV), electrons produce x-rays (bremsstrahlung) that carry away more energy than fusion produces"
- **Notes:** Exact match.

### CV-2: Alpha channeling gain factors 2.6× and 6.9× (Section 2, Challenge 2)
- **Source cited:** technical-papers-summary.md §Lowering the reactor breakeven requirements for p-B11 fusion (2024)
- **Status:** FOUND
- **Actual text:** "Alpha channeling reduces required energy confinement time for ignition by factor of 2.6 (thermal) to 6.9 (fast proton)"
- **Notes:** Exact match. The analysis correctly attributes the 2.6× value to the Ochs & Fisch 2024 paper (#12 in presentation) and 6.9× to the 2022 hybrid scheme papers (#1 and #2). Both values appear in the same paper (§4 of technical-papers-summary.md), which is accurate.

### CV-3: "Large voltage drops with minimal dissipation" (Section 2, Challenge 4)
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Device Details (slide 6)
- **Status:** FOUND
- **Actual text:** "Large voltage drops with minimal dissipation (biased electrode)"
- **Notes:** Exact match (capitalization differs trivially).

### CV-4: "Voltage drops can be minimized near walls" (Section 2, Challenge 4)
- **Source cited:** Implied from arpa-e-2025-fisch-presentation-notes.md §Summary of Derisked Questions
- **Status:** FOUND
- **Actual text:** "Voltage drops can be minimized near walls" (item 6 in slide 19 summary)
- **Notes:** Exact match. Analysis correctly characterizes this as "derisking goal, not demonstrated result."

### CV-5: "Centrifugal drift energy is recoverable" (Section 2, Challenge 5; footnote [6])
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Summary of Derisked Questions (slide 19)
- **Status:** FOUND
- **Actual text:** "Centrifugal drift energy is recoverable" (item 5 in slide 19 summary)
- **Notes:** Exact match.

### CV-6: "One-way walls have high energy cost, so use is situational" (Section 3, Ponderomotive Barriers)
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Summary of Derisked Questions
- **Status:** FOUND
- **Actual text:** "One-way walls have high energy cost, so use is situational" (item 8 in slide 19 summary)
- **Notes:** Exact match.

### CV-7: "No tritium breeding and containment... Cheap and non-radioactive reactants" (Section 4)
- **Source cited:** arpa-e-fisch-2025-presentation.md §Why p-B11?
- **Status:** FOUND
- **Actual text:** Listed as bullet points: "No tritium breeding and containment" and "Cheap and non-radioactive reactants"
- **Notes:** The analysis quotes these as a combined block quote; they are separate bullets in the source. Not a material issue.

### CV-8: "Synchrotron radiation is manageable through reabsorption" (Section 4, footnote [5])
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Summary of Derisked Questions
- **Status:** FOUND
- **Actual text:** "Synchrotron radiation is manageable through reabsorption" (item 4 in slide 19 summary)
- **Notes:** Exact match.

### CV-9: CMFX hardware specs — 3 T / 0.3 T, mirror ratio 10, 6.7 m length, 100 kV electrode (Section 3, Section 5 table)
- **Source cited:** technical-papers-summary.md §Related: CMFX
- **Status:** FOUND
- **Actual text:** "Two LTS superconducting magnets, 3 T throat / 0.3 T midplane (mirror ratio 10)" and "6.7 m length, 0.8 m diameter, center electrode up to 100 kV"
- **Notes:** All values confirmed. The analysis correctly reports all CMFX specs.

### CV-10: 29 peer-reviewed publications (Section 1)
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Key Publication List
- **Status:** FOUND
- **Actual text:** "29 papers under ARPA-E support, 2022-2025" (in Key Publication List header)
- **Notes:** Exact match.

### CV-11: "$1.5M from ARPA-E OPEN 2021 program" (Section 1)
- **Source cited:** princeton-arpa-e-funding-2022.md §Key Facts
- **Status:** FOUND
- **Actual text:** "$1.5 million from ARPA-E OPEN 2021 program"
- **Notes:** Exact match.

### CV-12: Company pre-incorporation status, website mockup (Section 1)
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Company Status (slides 8–9)
- **Status:** FOUND
- **Actual text:** "pre-incorporation, seeking recruitment, partnerships, collaborations, investment"; website mockup shown: palebluefusion.com, "Full website coming soon"
- **Notes:** Exact match. Analysis accurately characterizes company as pre-incorporation as of July 2025.

### CV-13: Four patent applications (March–April 2025) (Section 5 table)
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Patent Applications
- **Status:** FOUND
- **Actual text:** Four patents listed: US 19/083,790 (March 19), US 19/084,168 (March 19), US 19/175,473 (April 10), US Provisional 63/794,470 (April 25)
- **Notes:** Analysis table says "4 (March–April 2025)" — correct count and date range.

### CV-14: PRX Energy 2025 paper citation (Section 1, Section 2)
- **Source cited:** arpa-e-2025-fisch-presentation-notes.md §Key Publication List
- **Status:** FOUND
- **Actual text:** "#23: Rax, Kolmes, Fisch, 'Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields', PRX Energy 4, 013007 (2025)"
- **Notes:** Journal, volume, and article number confirmed.

### CV-15: dossier.md citations (Sections 3, 4, 5)
- **Source cited:** dossier.md §Magnet Type, §Fuel, §Operation Mode, §Tritium Breeding, §Primary Heating
- **Status:** NOT FOUND (not a provided source file)
- **Actual text:** dossier.md is not among the 4 listed source documents for this review
- **Notes:** The analysis cites dossier.md in footnotes [8] in Section 3 and [1], [3], [4] in Section 4, and in the Section 5 table. This appears to be a Phase 1a artifact from the research dossier. The cited claims (no conductor specification, aneutronic fuel cycle, no tritium breeding) are consistent with the ARPA-E presentation sources and are not factually disputed — but these citations cannot be directly verified against the provided source set. Recommend confirming dossier.md exists in the Phase 1a research directory.

### CV-16: WHAM 17 T claim (Section 3, Magnet System subsection)
- **Source cited:** None (no footnote or inline citation)
- **Status:** NOT FOUND (no citation provided)
- **Actual text:** "WHAM (Realta, separate project) uses REBCO HTS magnets at 17 T as the most relevant state-of-the-art mirror magnet"
- **Notes:** This specific claim has no inline citation in Section 3. The 11-magnetic-mirror analysis is cited only in Section 7. The 17 T value for WHAM is accurate (it is sourced in the Realta analysis), but this Section 3 claim is uncited. Minor traceability gap.

---

## Calculation Verification

### CALC-1: Boron isotope natural abundances (Section 4)
- **Claimed:** "Natural boron is 80.1% boron-10 and 19.9% boron-11"
- **Re-derived:** Standard IUPAC isotopic abundances — Boron-10: 19.9%, Boron-11: 80.1%
- **Status:** MISMATCH — the percentages are reversed
- **Notes:** The analysis has the abundances exactly transposed. Boron-11 is the *major* isotope (80.1%), not boron-10. This matters for the subsequent enrichment discussion: the analysis implies that natural boron contains only ~20% of the desired isotope (requiring ~4× enrichment), whereas in reality natural boron is already ~80% B-11. The concern about enrichment being needed for fusion-grade purity is still valid — isotopic separation of trace B-10 contaminant may be required regardless — but the supply chain challenge is considerably less severe than the reversed text implies. The conclusion that "Supply chain risk is low" is in fact correct, and is consistent with B-11 being the major isotope, but the stated abundances directly contradict it. This needs correction.

### CALC-2: "Roughly a 9× higher ion temperature requirement" (Section 2, Challenge 1)
- **Claimed:** "p-B11 cross-section peaks at ~600 keV, versus ~65 keV for D-T — roughly a 9× higher ion temperature requirement"
- **Re-derived:** 600 / 65 ≈ 9.2. Cross-section peak ratio is correct. However, this is a comparison of *peak cross-section energies*, not operating temperatures. The D-T thermal plasma optimal temperature is ~13–20 keV; the p-B11 nonthermal operating range cited elsewhere in the analysis is ~150–300 keV, giving a ratio of ~8–20× by operating temperature. The "9×" from cross-section peak ratios is in the right order of magnitude but conflates peak energy with temperature.
- **Status:** MATCH (order of magnitude and narrative intent correct, methodology imprecise)
- **Notes:** The 9× characterization is standard shorthand used in the fusion literature. Not a substantive error at the concept-analysis level, but the phrasing could be tightened. The actual operating temperature requirements (150–300 keV for p-B11 vs. 10–20 keV for D-T thermal plasma) suggest a 10–20× ratio, slightly higher than 9×.

### CALC-3: LCOE unit conversion in model_setup.py (line 185)
- **Claimed:** `lcoe_ckwh = float(c.lcoe) / 10` converts $/MWh → ¢/kWh
- **Re-derived:** 1 $/MWh × (1 MWh / 1000 kWh) × (100 ¢ / $) = 0.1 ¢/kWh per $/MWh, so ¢/kWh = $/MWh ÷ 10
- **Status:** MATCH
- **Notes:** Correct unit conversion.

### CALC-4: Total conversion efficiency implied by f_dec and eta_th (model_setup.py)
- **Claimed:** f_dec=0.85, eta_de=0.70, eta_th=0.20
- **Re-derived:** Overall conversion = f_dec × eta_de + (1 − f_dec) × eta_th = 0.85 × 0.70 + 0.15 × 0.20 = 0.595 + 0.030 = 0.625 → ~62.5% total
- **Status:** MATCH (implied result internally consistent)
- **Notes:** The ~62.5% total conversion efficiency is above the 1983 MARS DEC reference of ~54% cited in Section 7, and considerably above conventional thermal cycles (~33–40%). This is plausible given physics-limit analysis in PRX Energy 2025, but is speculative. The model docstring correctly warns that eta_de=0.70 is "within range of physics limits but not validated." The Section 7 note about the MARS value should be echoed as a caveat in the model's sensitivity commentary — currently it only appears in the analysis narrative.

---

## Model Setup Audit

### MSA-1: ConfinementConcept.MIRROR, Fuel.PB11
- **Value:** `CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.PB11)`
- **Source:** analysis.md §S2, §S4 (p-B11 aneutronic fuel, cylindrical mirror geometry)
- **Status:** TRACED
- **Notes:** Well-justified in docstring. MIRROR captures cylindrical geometry and solenoid cost model. PB11 activates correct aneutronic defaults. The CHARM concept is not a classical tandem mirror but a centrifugal mirror — MIRROR is the best available analog. Appropriate choice with caveat correctly stated.

### MSA-2: NET_ELECTRIC_MW = 500.0
- **Value:** 500.0 MWe
- **Source:** analysis.md §S5 "Missing Parameters — Net electric output (plant): truly-unknown / blocking"
- **Status:** TRACED (acknowledged as assumption with no basis)
- **Notes:** Correctly flagged UNCERTAIN. Using 500 MWe as reference scale is appropriate for framework comparison given no published design point.

### MSA-3: mn=1.0 (neutron energy multiplier)
- **Value:** 1.0
- **Source:** analysis.md §S5 "Neutron energy fraction: <1%"; arpa-e-fisch-2025-presentation.md §Why p-B11?
- **Status:** TRACED
- **Notes:** Correct for near-aneutronic p-B11. No neutron multiplication expected. Setting mn=1.0 rather than mn<1.0 is conservative (no blanket neutron multiplication to subtract).

### MSA-4: p_trit=0.0
- **Value:** 0.0 MW
- **Source:** arpa-e-fisch-2025-presentation.md §Why p-B11? ("No tritium breeding and containment"); analysis.md §S4
- **Status:** TRACED
- **Notes:** Correct. p-B11 produces no tritium. Setting tritium processing power to zero is well-justified and directly source-traced.

### MSA-5: f_dec=0.85
- **Value:** 0.85
- **Source:** analysis.md §S5 "Thermal vs. direct conversion energy split: truly-unknown / important"; §S2 Challenge 1
- **Status:** TRACED
- **Notes:** Acknowledged as optimistic and UNCERTAIN. The logical basis (p-B11 puts ~99% of fusion energy into charged alphas → large DEC-available fraction, minus ~15% radiative losses) is internally consistent. The 0.85 value is speculative but physically bounded. No published estimate exists.

### MSA-6: eta_de=0.70
- **Value:** 0.70
- **Source:** analysis.md §S2 Challenge 5; §S3 "DEC: TRL 2-3"; technical-papers-summary.md §Related: Direct Energy Conversion (PRX Energy 2025)
- **Status:** TRACED
- **Notes:** Acknowledged as speculative. The PRX Energy paper establishes physics-limit upper bounds for adiabatic DEC — the model note correctly states "within range of physics limits but not validated." One additional caveat worth noting: the 1983 MARS empirical DEC value (~54%) cited in Section 7 of the analysis provides a historical anchor that is not reflected in the model comments. At eta_de=0.70, the model is ~30% above the only hardware-level DEC efficiency reference in the literature. This should be noted explicitly in the model's key assumptions printout.

### MSA-7: eta_th=0.20
- **Value:** 0.20
- **Source:** analysis.md §S2 Challenge 5; §S5 "Thermal vs. direct conversion energy split"
- **Status:** TRACED
- **Notes:** Reasonable for capturing only synchrotron and bremsstrahlung radiation in a thermal cycle. Acknowledged UNCERTAIN with appropriate range ("~15-25%") given in the model comment.

### MSA-8: p_input=60.0 MW
- **Value:** 60.0 MW (total auxiliary: RF alpha channeling ~20 MW + rotation electrode ~30 MW + misc ~10 MW)
- **Source:** analysis.md §S2 Challenge 4 "Unknown Recirculating Power"; technical-papers-summary.md §CMFX (100 kV electrode reference)
- **Status:** TRACED
- **Notes:** Well-documented as UNCERTAIN with decomposition of the estimate. The 60 MW total is plausible but completely unvalidated. At 500 MWe net and typical recirculating fractions this will drive meaningful LCOE sensitivity — correctly flagged in blocking gap inventory.

### MSA-9: chamber_length=30.0 m
- **Value:** 30.0 m
- **Source:** analysis.md §S3, §S5 "Machine size: truly-unknown / blocking"; CMFX 6.7 m reference
- **Status:** TRACED (acknowledged assumption with no published basis)
- **Notes:** 30 m is a ~4.5× upscale from CMFX (6.7 m). The comment correctly notes this is a "conservative upscale with no published basis." For a multi-chamber CHARM architecture, 30 m is in the right ballpark for a conceptual reactor. Cost sensitivity to this parameter will be high through the solenoid coil cost model; the sensitivity analysis in the script will expose this.

### MSA-10: cost_overrides={"CAS21": 200.0 M$}
- **Value:** 200 M$ for Buildings
- **Source:** analysis.md §S4 (no tritium building, no hot cell, no large remote handling facility)
- **Status:** TRACED
- **Notes:** The reduction from typical DT mirror default (~250–300 M$) to 200 M$ is qualitatively justified by the absence of tritium infrastructure and reduced remote handling requirements. The specific 200 M$ value has no quantitative basis (acknowledged). The override is reasonable and conservatively applied.

---

## Consistency Check

**Section 5 parameter table vs. Section 2 narrative:** Consistent. The ~150–300 keV proton temperature requirement in the parameter table (medium confidence, from Princeton funding article) aligns with the bremsstrahlung challenge described in Challenge 1. The alpha channeling gain factors (2.6× thermal, 6.9× fast proton hybrid) are correctly attributed and consistently presented. The "truly-unknown / blocking" classification for all plant-scale parameters in the missing parameters table correctly reflects the data gap inventory in Section 6.

**TRL ratings (Section 3) vs. challenges (Section 2):** Consistent and well-matched. CHARM multi-chamber architecture TRL 1 aligns with "never built or tested." Alpha channeling TRL 3–4 aligns with "analytical and computational models only." DEC TRL 2–3 aligns with "no prototype hardware." Centrifugal mirror TRL 3–4 aligns with CMFX having validated the confinement geometry but not at reactor-relevant conditions. These TRL characterizations are internally coherent.

**Model setup vs. analysis parameter table:** Consistent throughout. Every UNCERTAIN parameter in model_setup.py corresponds to a "truly-unknown" entry in the Section 5 missing parameters table. The power balance parameters (mn, f_dec, eta_th, eta_de) are well-matched between the model and the analysis narrative in §S2 Challenge 5. The CAS21 override is consistent with the no-tritium-infrastructure narrative in §S4. The blocking data gap warnings in the model's print statements directly reference §Section 5–6.

**One minor inconsistency:** The analysis in Section 7 explicitly notes "the 1983 MARS study value (~54% for gridless end-loss DEC)" as the only empirical DEC efficiency reference. This is not echoed in model_setup.py's comments for eta_de=0.70, which cites the PRX Energy physics-limits paper but not the MARS anchor. The model's key assumptions printout would benefit from noting that eta_de=0.70 is above the best experimental DEC efficiency ever measured.

---

## Proposed Actions

### PA-1: Boron isotope abundances reversed
- **Category:** factual-concern
- **Severity:** important
- **Location:** analysis.md §Section 4, paragraph "Boron-11 Fuel"
- **Finding:** The analysis states "Natural boron is 80.1% boron-10 and 19.9% boron-11." This is exactly wrong — natural boron is 80.1% B-11 and 19.9% B-10 (IUPAC standard values). The percentages are transposed.
- **Proposed Fix:** Correct to "Natural boron is 19.9% boron-10 and 80.1% boron-11." Then revise the subsequent enrichment discussion: since B-11 is already the *major* isotope, the enrichment challenge is much less severe than a reader of the reversed text would infer. The narrative should note that starting at 80% B-11, enrichment to fusion-grade purity (e.g., >99%) is a modest isotopic purification task, not a 5× concentration step. The conclusion that "Supply chain risk is low" is correct and should be retained — but the reasoning should flow from the correct abundances.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-2: dossier.md citations unverifiable from provided sources
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §S3 footnote [8], §S4 footnotes [1], [3], [4], §S5 table rows for "Operation mode" and "Tritium breeding requirement"
- **Finding:** analysis.md cites "dossier.md" in multiple places (§Magnet Type, §Fuel, §Operation Mode, §Tritium Breeding, §Primary Heating), but dossier.md is not included in the 4 source documents provided for this review. The cited claims are consistent with the ARPA-E presentation sources and are not factually disputed, but the citations cannot be directly verified.
- **Proposed Fix:** Confirm dossier.md exists in the Phase 1a research directory (e.g., `analyses/06-magnetic-mirror/` or the phase_1a dossier path). If it exists, no change needed — add a note to the review source list for future iterations. If it does not exist, replace dossier.md citations with direct citations to the corresponding ARPA-E presentation source files.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-3: WHAM 17 T claim uncited in Section 3
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 3, "Magnet System (Conductor Type Unspecified)" subsection
- **Finding:** The claim "WHAM (Realta, separate project) uses REBCO HTS magnets at 17 T as the most relevant state-of-the-art mirror magnet" has no inline citation. The WHAM data is established in the 11-magnetic-mirror analysis (cited in Section 7) but not cross-referenced here.
- **Proposed Fix:** Add inline citation: `[Realta Hammir: 11-magnetic-mirror analysis §Section 3]` or cite the specific source document from the Realta analysis that establishes WHAM parameters.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-4: MARS DEC reference absent from model_setup.py comments
- **Category:** inconsistency
- **Severity:** minor
- **Location:** model_setup.py line 123–129 (eta_de=0.70 comment block)
- **Finding:** The analysis in Section 7 correctly notes that the 1983 MARS empirical DEC efficiency (~54%) is the only hardware-level DEC efficiency reference in the literature, and that eta_de=0.70 in the model is ~30% above this anchor. The model comment for eta_de references the PRX Energy physics-limits paper but not the MARS value. A reader of the model without the analysis would not see this comparison.
- **Proposed Fix:** Add one line to the eta_de comment: "Historical MARS gridless DEC measured ~54% (1983 MARS study); eta_de=0.70 is above this empirical reference. See analysis.md §S7."
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

### PA-5: "9× higher ion temperature requirement" conflates cross-section peak energy with temperature
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §Section 2, Challenge 1, first paragraph
- **Finding:** The analysis states "p-B11 cross-section peaks at ~600 keV, versus ~65 keV for D-T — roughly a 9× higher ion temperature requirement." This is comparing cross-section *peak energies*, not plasma operating *temperatures*. The actual operating temperatures are cited elsewhere in the analysis (150–300 keV for p-B11 vs. 10–20 keV optimal for D-T thermal plasma), which gives a ~10–20× ratio. The 9× phrasing is standard shorthand in the field but technically conflates energy and temperature.
- **Proposed Fix:** Optionally clarify to: "...versus ~65 keV for D-T — roughly a 9× higher cross-section peak energy, translating to operating temperature requirements of ~150–300 keV vs. ~10–20 keV for D-T thermal plasmas." Alternatively, leave as-is — this level of precision is typical for concept-analysis documents and the actual operating temperatures are stated correctly later in the same footnote.
- **Decision:** agree
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 16
- **Citations verified:** 14
- **Citations not found / unverifiable:** 2 (dossier.md source not in review set; WHAM claim uncited)
- **Calculations checked:** 4
- **Calculations matched:** 3 (CALC-1 is a mismatch)
- **Model parameters audited:** 10
- **Model parameters fully traced:** 10 (all have documented basis, all marked UNCERTAIN appropriately)
- **Proposed Actions:** 5 (blocking: 0, important: 1, minor: 4)
- **Overall:** HAS ISSUES — one factual error (boron isotope abundances reversed, PA-1) requires correction before analysis is finalized; remaining issues are minor traceability and documentation improvements.
