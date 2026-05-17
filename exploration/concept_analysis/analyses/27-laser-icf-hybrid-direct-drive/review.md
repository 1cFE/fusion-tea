# Review: Laser ICF - Hybrid Direct Drive (D-T)

**Iteration:** 1
**Date:** 2026-03-31
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 8 files

---

## Citation Verification

### CV-1: "Most significantly, Xcimer must demonstrate that this laser architecture, never before built at MJ-scale, can deliver on the performance, cost and other advantages."
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer's Novel Laser Architecture (analysis.md §2.1 block quote)
- **Status:** FOUND
- **Actual text:** "Most significantly, Xcimer must demonstrate that this laser architecture, never before built at MJ-scale, can deliver on the performance, cost and other advantages as outlined in this paper." (XEC §Next Steps, line ~1084)
- **Notes:** Quoted text is accurate but the source section cited in analysis.md is slightly wrong. The quote appears in the §Next Steps section of XEC, not in §Xcimer's Novel Laser Architecture. Minor discrepancy in section attribution.

---

### CV-2: "An Nth of a kind system producing 250 target gain (Qsci) with a 7% laser efficiency"
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Challenge 3: Cost and Economics (analysis.md §2.2 block quote)
- **Status:** FOUND
- **Actual text:** "An Nth of a kind system producing 250 target gain (Qsci) with a 7% laser efficiency will have a recirculating power fraction in the range of 11% to 13%." (XEC §Next Steps, line ~1077)
- **Notes:** The quote is accurate but again appears in §Next Steps, not §Challenge 3 as cited. The same claim is echoed throughout the document (Challenge 3 discusses the 7% efficiency need); the substance is correct but section attribution is imprecise.

---

### CV-3: "FLiBe pump and nozzle technology and redox control to prevent corrosion" are explicitly cited as development challenges.
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer's Chamber Design (analysis.md §2.4 block quote)
- **Status:** FOUND
- **Actual text:** "FLiBe pump and nozzle technology and redox control to prevent corrosion" (XEC §Xcimer's Chamber Design, line ~951)
- **Notes:** Exact verbatim match in the correct section.

---

### CV-4: "generate steam, which in turn drives turbines to produce electricity"
- **Source cited:** xcimer-science-page.md §Energy Conversion (analysis.md §2.5 narrative and model_setup.py ETA_TH_STEAM comment)
- **Status:** FOUND
- **Actual text:** "A circulating coolant absorbs and carries away the heat to generate steam, which in turn drives turbines to produce electricity." (xcimer-science-page.md line ~64)
- **Notes:** Exact verbatim match in the correct source.

---

### CV-5: Laser cost FOAK $100/J, NOAK $60–80/J on-target
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule (analysis.md §5 parameter table and model_setup.py)
- **Status:** FOUND
- **Actual text:** "Xcimer internal architecture described above can be constructed with total costs of approximately $100 to $120 / joule of laser light on-target in first-of-a-kind (FOAK) systems, and costs of $60 to $80 / joule in nth-of-a-kind (NOAK) systems" (XEC §Xcimer Laser Cost and Schedule, line ~730)
- **Notes:** Source says FOAK is "$100 to $120/J"; analysis.md consistently uses "$100/J" as FOAK and model_setup.py uses $110/J as the "midpoint" — both within the stated range. See CALC-1 below on the $110/J midpoint.

---

### CV-6: FOAK laser cost breakdown — capacitors $10/J, Marx $24/J, EB $17/J, chamber/gas $19/J, optics $12/J, seed/NLO $23/J, control $4/J
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule (analysis.md §5 parameter table)
- **Status:** FOUND
- **Actual text:** Table 1 in XEC §Xcimer Laser Cost and Schedule lists: Capacitors $10, Marx Generator $24, Electron Beam components $17, Laser Chamber & Gas Systems $19, Laser Output Windows & Optics $12, Seed Lasers / Nonlinear Optical Systems $23, Control/Diagnostics/Other $4. Total = $109/J (sums to $109, not $100).
- **Notes:** The per-line figures exactly match analysis.md. However, the sum of the line items is $10+$24+$17+$19+$12+$23+$4 = $109/J, while the table footer says "$100/J." This discrepancy exists in the source document itself (apparent rounding in the table). Analysis.md reproduces the breakdown correctly. The "$100/J FOAK" label is consistent with the source's stated total ($100–$120/J range, $100/J as the round-number floor). The $9 discrepancy between row sums and stated total is a source-side issue, not an analysis error — but worth noting.

---

### CV-7: NIF Qsci = 4.13 (April 2025 record)
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Executive Summary (analysis.md §5 parameter table)
- **Status:** FOUND
- **Actual text:** "NIF set a new record of 8.6 MJ of yield [1], for a gain (Qsci) exceeding 4" (XEC §Executive Summary); more precisely: "This resulted in a scientific gain Qsci of 8.6 / 2.08 = 4.13" (XEC §Challenge 1, line ~211)
- **Notes:** Exact match.

---

### CV-8: NIF capsule gain Qc ≈ 34 (April 2025)
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Challenge 3 (analysis.md §5 table: "NIF April 2025 record is Qsci = 4.13")
- **Status:** FOUND
- **Actual text:** "The capsule gain – the fusion yield relative to energy absorbed by the capsule – was approximately Qc = 8.6 / 0.25 = 34." (XEC §Challenge 1, line ~213)
- **Notes:** Match. The capsule gain of 34 is cited in analysis.md §5 and §2.2 correctly.

---

### CV-9: Xcimer targets Qc > 200 at 10 MJ coupling
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Challenge 3 (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** "coupling 10 MJ to a fuel capsule vs. the 250 kJ as on the NIF... suggests a capsule gain Qc of over 200 could be readily achievable with a 10 MJ laser" (XEC §Challenge 1, line ~252)
- **Notes:** The actual text appears in §Challenge 1, not §Challenge 3 as analysis.md's §5 table cites. The claim matches exactly; the section reference is slightly off.

---

### CV-10: Recirculating power fraction 11–13% at NOAK Qsci 250, 7% efficiency
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Challenge 3 (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** "An Nth of a kind system producing 250 target gain (Qsci) with a 7% laser efficiency will have a recirculating power fraction in the range of 11% to 13%." (XEC §Next Steps, line ~1077–1078)
- **Notes:** The substance matches exactly. The section source is §Next Steps, not §Challenge 3. The same claim is referenced within Challenge 3 contextually.

---

### CV-11: TBR ~1.2 (Athena, FLiBe, natural Li) and TBR ~1.05 (commercial, FLiNaK)
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer's Chamber Design (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** "The first Athena pilot plant will certainly use FLiBe providing a TBR of approximately 1.2." and "FLiNaK can be used in commercial plants in place of FLiBe... with an estimated TBR of 1.05." (XEC §Xcimer's Chamber Design, lines ~949–950)
- **Notes:** Exact match.

---

### CV-12: Tritium inventory <150 g (Athena 400 MWe) and <200 g (GWe commercial)
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer's Chamber Design (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** "analysis indicates the total tritium inventory will be less than 200 grams in the GWe-scale commercial system (and under 150 grams in Xcimer's 400 MWe 'Athena' pilot plant)" (XEC §Xcimer's Chamber Design, line ~944–945)
- **Notes:** Exact match.

---

### CV-13: Net electrical output Athena ~400 MWe
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Executive Summary (analysis.md §5 table; model_setup.py NET_ELECTRIC_MW comment)
- **Status:** FOUND
- **Actual text:** "Athena will be the first operational laser-fusion pilot power plant, producing about 400 MW electric" (XEC §Roadmap, line ~1034)
- **Notes:** The analysis also cites §Executive Summary. The 400 MWe figure actually appears in the Roadmap section, but is consistent with the overall framing of the Executive Summary. Correct value; section citation acceptable.

---

### CV-14: DPSSL long-term cost floor $700–$1,000/J
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Challenge 3 (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** "the long-term best-case cost for a DPSSL driver is about $700 - $1,000 / joule" (XEC §Challenge 3, line ~516); also repeated in §Next Steps.
- **Notes:** Exact match in the cited section.

---

### CV-15: "The entire NIF facility requires 192 beam lines and 120 tons of precision glass, with a total system cost of over $3,600,000,000."
- **Source cited:** xcimer-science-page.md (analysis.md §5 block quote, attributed to "§While there have been significant advancements")
- **Status:** FOUND
- **Actual text:** "The entire NIF facility requires 192 beam lines and 120 tons of precision glass, with a total system cost of over $3,600,000,000" (xcimer-science-page.md line ~74)
- **Notes:** Exact verbatim match.

---

### CV-16: "we've reduced the cost per joule by more than 30x compared to the National Ignition Facility (NIF)."
- **Source cited:** xcimer-energy-approach.md (analysis.md §5 block quote)
- **Status:** FOUND
- **Actual text:** "By using a gas laser architecture, we've reduced the cost per joule by more than 30x compared to the National Ignition Facility (NIF)." (xcimer-energy-approach.md line ~14)
- **Notes:** Exact verbatim match.

---

### CV-17: "Xcimer's approach utilizing a liquid first wall allows us to use readily available commercial materials that minimize activation, extend the lifetime and comply with our waste and safety goals."
- **Source cited:** xcimer-energy-approach.md (analysis.md §4 block quote)
- **Status:** FOUND
- **Actual text:** "Xcimer's approach utilizing a liquid first wall allows us to use readily available commercial materials that minimize activation, extend the lifetime and comply with our waste and safety goals." (xcimer-science-page.md line ~54)
- **Notes:** PARTIAL MATCH — The quote is correct verbatim, but the source is xcimer-science-page.md, not xcimer-energy-approach.md as cited. The analysis.md §4 citation "xcimer-energy-approach.md" is incorrect for this specific quote.

---

### CV-18: Commercial plants to use FLiNaK; "Commercial plants could switch to FLiNaK... to avoid beryllium supply chain entirely."
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer's Chamber Design (analysis.md §4 block quote)
- **Status:** PARTIAL MATCH
- **Actual text:** "FLiNaK can be used in commercial plants in place of FLiBe, avoiding beryllium supply chains." (XEC §Xcimer's Chamber Design, line ~946)
- **Notes:** Analysis.md paraphrases this as "Commercial plants could switch to FLiNaK... to avoid beryllium supply chain entirely." The source text does not use "could switch" phrasing — it says "can be used." The paraphrase is accurate in meaning but the quotation marks in analysis.md make it look like a direct quote when it is actually a paraphrase. Minor but visible misrepresentation format.

---

### CV-19: "Manufacturing complexity comparable to automotive components."
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule (analysis.md §4 block quote)
- **Status:** PARTIAL MATCH
- **Actual text:** "Manufacturing these elements involves conventional casting, fastening, surface treatment, and assembly techniques of meter-scale metal parts and assemblies with physical scale and complexity comparable to automotive components." (XEC §Xcimer Laser Cost and Schedule, line ~736)
- **Notes:** Analysis.md quotes this as "Manufacturing complexity comparable to automotive components." This is a selective excerpt from a longer sentence. The meaning is preserved but it is formatted as a standalone quote, dropping context. Acceptable as a paraphrase-quote; not materially misleading.

---

### CV-20: KrF Electra 750 J, 7% wall-plug efficiency (Section 3 and model_setup.py ETA_PIN1)
- **Source cited:** XEC §Xcimer's Novel Laser Architecture / Mehlhorn 2024 (analysis.md §3); model_setup.py cites [XEC] §Challenge 3
- **Status:** FOUND
- **Actual text:** "the 750 J Electra laser... demonstrated not only that 7% wall-plug efficiency could be achieved, but also operated continuously for 10 hours at 2.5 Hz repetition rate" (XEC §Xcimer's Novel Laser Architecture, line ~586–588)
- **Notes:** Source says Electra operated at "2.5 Hz" continuously, not "5 Hz" as stated in analysis.md §3: "NRL Electra laser demonstrated KrF excimer operation at ~750 J, 5 Hz continuous for days." The rep rate discrepancy (2.5 Hz in XEC vs. 5 Hz in analysis.md) is a factual error. The source also says "10 hours" not "days." See PA-1.

---

### CV-21: Direct drive coupling efficiency ~90% vs. 12% for NIF indirect drive
- **Source cited:** xcimer-science-page.md §In an Xcimer system (analysis.md §5 table and §7)
- **Status:** FOUND
- **Actual text:** "we'll couple over 90% of the laser energy directly to the fuel capsule, vs. only 12% coupled via the x-ray bath on the NIF." (xcimer-science-page.md line ~88)
- **Notes:** Exact match.

---

### CV-22: Athenha pilot, 8 MJ on target (roadmap table); laser energy "8–12 MJ on target"
- **Source cited:** xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Executive Summary (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** Roadmap table: "8 MJ on-target / 400 MWe output" for Athena (XEC §Roadmap, line ~978). Executive Summary: "Commercial Xcimer IFE power plants will operate at 0.25 to 1 Hz with laser energies in the range of 8 to 12 MJ" (§Roadmap line ~1042).
- **Notes:** The 8–12 MJ range is confirmed. Analysis.md uses 10 MJ as a midpoint in the parameter table (stated as the "commercial design point"); model_setup.py uses 10 MJ. This is a reasonable midpoint choice, but the Athena-specific figure is 8 MJ per the roadmap table, not 10 MJ. See PA-2.

---

### CV-23: Rep rate 0.25–1 Hz; "every couple seconds"
- **Source cited:** xcimer-energy-approach.md; xec-20260224 §Executive Summary (analysis.md §5 table)
- **Status:** FOUND
- **Actual text:** xcimer-science-page.md: "the process is repeated every couple seconds" (line ~62); XEC Roadmap: "0.25 to 1 Hz" (line ~1042); xcimer-energy-approach.md: "less than 1 Hz" (line ~22).
- **Notes:** Multiple sources confirm. Exact match.

---

### CV-24: Capacitor cost current market ~$10/J; Xcimer in-house target <$0.40/J
- **Source cited:** xec-20260224 §Xcimer Laser Cost and Schedule (analysis.md §4 and §5 table)
- **Status:** FOUND
- **Actual text:** "Current high-voltage capacitor prices are roughly $10 / joule... Cost estimates for volume production at the 3 MJ (stored) level for the first full-scale excimer amplifier module are approximately $0.85 / joule, and as volumes increase, this can be further driven down to below $0.40 / joule." (XEC §Xcimer Laser Cost and Schedule, lines ~760–765)
- **Notes:** The current price ($10/J) matches exactly. The <$0.40/J target matches exactly. The intermediate step ($0.85/J at first full-scale volume) is not mentioned in analysis.md, but its omission is not misleading.

---

### CV-25: NIF optics refurbishment >$40M/year
- **Source cited:** xcimer-science-page.md (analysis.md §4 and §7)
- **Status:** FOUND
- **Actual text:** "over $40M per year is spent on refurbishment of the optics" (xcimer-science-page.md line ~94)
- **Notes:** Exact match.

---

### CV-26: Focused Energy rep rate ~10 Hz and gain requirement 50–100
- **Source cited:** focused-energy-callahan-interview.md (analysis.md §7 cross-concept notes)
- **Status:** FOUND
- **Actual text:** "we will need to do about 900,000 shots a day – about 10 per second" (focused-energy-callahan-interview.md line ~63); "we need significantly higher gains of more like 50 to 100" (line ~33).
- **Notes:** Exact match on both counts.

---

### CV-27: Phoenix system 1–2 kJ, Q2 2026
- **Source cited:** xec-20260224 §Next Steps (analysis.md §3)
- **Status:** FOUND
- **Actual text:** Roadmap table: "Phoenix | 1-2 kJ | Q2 2026 | Denver, CO, USA" (XEC §Roadmap, line ~978); "The largest excimer amplifier in the Phoenix facility, the 'KJC,' ... will produce output energies approaching 2 kJ at 248 nm." (XEC §Next Steps, line ~984)
- **Notes:** Match.

---

### CV-28: Anvil 200 kJ on target, 2028
- **Source cited:** xec-20260224 §Next Steps (analysis.md §3)
- **Status:** FOUND
- **Actual text:** "Anvil... delivering 100 kJ in a single beamline... An identical beamline will then be constructed 180 degrees opposed to provide a 2-sided geometry with 200 kJ on-target. Anvil is expected to be completed in 2028." (XEC §Next Steps, lines ~1007–1012)
- **Notes:** Match.

---

### CV-29: Vulcan 4–12 MJ, wall-plug breakeven end 2031
- **Source cited:** xec-20260224 §Next Steps (analysis.md §3)
- **Status:** FOUND
- **Actual text:** "Initially delivering 4 MJ to target from two sides, Vulcan will be upgradeable to 12 MJ. With initial operations commencing by the end of 2030, Vulcan's goal is to achieve wall-plug breakeven by the end of 2031." (XEC §Next Steps, lines ~1029–1031)
- **Notes:** Analysis.md §3 says "targeting wall-plug breakeven by end 2031" — correct. It also states "Vulcan (4–12 MJ)" which matches.

---

### CV-30: HYLIFE-II NRL Electra rep rate demonstration
- **Source cited:** analysis.md §3 states "5 Hz continuous for days"
- **Status:** NOT FOUND (as stated)
- **Actual text from XEC:** "operated continuously for 10 hours at 2.5 Hz repetition rate" (XEC §Xcimer's Novel Laser Architecture, line ~587)
- **Notes:** This is the same factual error noted in CV-20. The XEC source says 2.5 Hz for 10 hours; analysis.md says 5 Hz for days. This needs independent sourcing to confirm; based on available sources, 2.5 Hz / 10 hours is the correct figure. See PA-1.

---

## Calculation Verification

### CALC-1: FOAK laser cost midpoint = $110/J (model_setup.py LASER_FOAK_PER_J)
- **Claimed:** model_setup.py comment states "midpoint $100–120/J" → $110/J
- **Re-derived:** XEC states FOAK range as "$100 to $120/J." Simple arithmetic midpoint = (100 + 120)/2 = $110/J.
- **Status:** MATCH
- **Notes:** The midpoint calculation is correct. The source range is $100–$120/J; analysis.md §5 and the parameter table consistently state "$100/J" as the FOAK value (rounding the lower bound). model_setup.py uses $110/J as the midpoint. These are internally consistent but slightly different characterizations; neither is wrong.

---

### CALC-2: Laser capital in M$ = $/J × MJ energy (unit verification)
- **Claimed:** model_setup.py: "M$ = $/J × MJ (unit identity: $/J × 10^6 J / 10^6 $/M$ = $/J × MJ = M$)"
- **Re-derived:** $/J × (MJ × 10^6 J/MJ) / (10^6 $/M$) = $/J × 10^6 J × (M$/10^6$) = $/J × J × M$/$ = M$. ✓
  - NOAK low: $60/J × 10 MJ = 60 × 10 = $600 M$ ✓
  - NOAK mid: $70/J × 10 MJ = $700 M$ ✓
  - NOAK high: $80/J × 10 MJ = $800 M$ ✓
  - FOAK: $110/J × 10 MJ = $1,100 M$ ✓
- **Status:** MATCH
- **Notes:** All four conversions are correct.

---

### CALC-3: FOAK laser capital contribution to $/kWe (analysis.md §5 narrative)
- **Claimed:** "10 MJ × $100/J = $1 billion in laser capex. For a 400 MWe Athena plant, this implies a laser capital cost contribution of roughly $2,500/kWe"
- **Re-derived:** $1,000 M / 400 MWe = $1,000 M / (400 × 10^3 kWe) = $1,000 × 10^6 / (400 × 10^3) = $2,500/kWe ✓
- **Status:** MATCH
- **Notes:** Arithmetic is correct.

---

### CALC-4: NOAK laser contribution to $/kWe (analysis.md §5 narrative)
- **Claimed:** "NOAK at $60–80/J reduces to $600–800M → $1,500–2,000/kWe from laser alone"
- **Re-derived:**
  - $600 M / 400 MWe = $600 × 10^6 / (400 × 10^3 kW) = $1,500/kWe ✓
  - $800 M / 400 MWe = $800 × 10^6 / (400 × 10^3 kW) = $2,000/kWe ✓
- **Status:** MATCH

---

### CALC-5: Goodin criterion — cost ceiling ~$2–3/target at 400 MWe, 0.5 Hz
- **Claimed:** "At 0.25–1 Hz, a commercial plant consumes 8–31 million targets per year." (analysis.md §2.6 and §7); model_setup.py H-4 analysis uses 0.5 Hz, 85% availability.
- **Re-derived:**
  - Shots/yr = 0.5 Hz × 86,400 s/day × 365 days/yr × 0.85 = 0.5 × 31,536,000 × 0.85 = 13,402,800 ≈ 13.4 M shots/yr (model_setup.py)
  - Low bound (0.25 Hz, 100% CF): 0.25 × 31,536,000 = 7.88 M ≈ 8 M/yr ✓
  - High bound (1 Hz, 100% CF): 1 × 31,536,000 = 31.5 M ≈ 31 M/yr ✓
  - Range stated in analysis.md §2.6 "8–31 million" is correct for the stated rep rate range.
  - Goodin criterion: targets < 10% of electricity per shot.
    Annual energy (MWh) at 400 MWe, 85% CF = 400 × 0.85 × 8,760 = 2,978,400 MWh = 2,978,400,000 kWh
    Annual energy (GWh) = 2,978.4 GWh (model: 400 × 0.85 × 8760/1000 = 2978.4 GWh ✓)
    At $2.50/target × 13.4M shots/yr = $33.5 M/yr → LCOE addition = $33.5M × 1000 / 2978.4 GWh = $11.25/MWh
    model_setup.py shows this as: annual_ms = 2.50 × 13,402,800 / 1e6 = 33.5 M$/yr → lcoe_add = 33.5 × 1000 / 2978.4 = ~$11.25/MWh
  - The $2–3/target ceiling cited from Goodin is characterised as "~10% of electricity produced per shot." The calculation is internally consistent though the Goodin source is not directly ingested (analysis.md §8, source 10: "Not ingested; cited via concept 26 handwritten exemplar").
- **Status:** MATCH (arithmetic internally consistent; Goodin primary source not verifiable from ingested files)

---

### CALC-6: Wall-plug gain Qwp = Qsci × η_wpe; claimed ~17.5 at Qsci=250, η=7%
- **Claimed:** analysis.md §5 table: "Wall-plug gain (Qwp) required ~10"; xcimer-science-page.md cited for ~10× requirement; model_setup.py comments "XEC claims ~17.5 (7% × 250)"
- **Re-derived:** Qwp = Qsci × η_wpe = 250 × 0.07 = 17.5 ✓. The claimed commercial viability threshold of ~10 is consistent with xcimer-science-page.md ("A commercial system must have a wall-plug gain of ~10").
- **Status:** MATCH

---

### CALC-7: P_IMPLOSION_MW = LASER_ENERGY_MJ × REP_RATE_HZ = 10 × 0.5 = 5 MW (model_setup.py)
- **Claimed:** 10 MJ/pulse × 0.5 Hz = 5.0 MW average optical output
- **Re-derived:** 10 × 0.5 = 5 MW ✓
- **Status:** MATCH
- **Notes:** The model comment says "Note: derived for Qsci=250 self-consistency, this gives p_implosion ≈ 4.7 MW." The small discrepancy (4.7 vs 5.0 MW) arises because at 400 MWe net output with the given efficiency assumptions, the implied Qsci is slightly below 250. This is flagged in the code comments as expected behavior.

---

### CALC-8: Shots/yr = 0.5 Hz × 86,400 × 365 × 0.85 (model_setup.py H-4)
- **Claimed:** SHOTS_PER_YEAR = REP_RATE_HZ × 86400 × 365 × AVAILABILITY
- **Re-derived:** 0.5 × 86,400 × 365 × 0.85 = 0.5 × 31,536,000 × 0.85 = 13,402,800 ≈ 13.4 M/yr
- **Status:** MATCH
- **Notes:** The H-4 table in the script prints "13.4M shots/yr at 0.5 Hz × 85% CF" — consistent.

---

### CALC-9: ANNUAL_ENERGY_GWH = NET_ELECTRIC_MW × AVAILABILITY × 8760 / 1000
- **Claimed:** 400 × 0.85 × 8760 / 1000 = 2,978.4 GWh/yr
- **Re-derived:** 400 × 0.85 × 8760 = 2,978,400 MWh = 2,978.4 GWh ✓
- **Status:** MATCH

---

### CALC-10: Analysis.md §2.2 claim that NIF April 2025 record was "Qc ≈ 34 at ~250 kJ absorbed"
- **Claimed:** Qc ≈ 34 at ~250 kJ absorbed
- **Re-derived from source:** XEC §Challenge 1: "capsule gain... Qc = 8.6 / 0.25 = 34. The capsule absorbed roughly 250 kJ." (8,600 kJ yield / 250 kJ absorbed = 34.4 ≈ 34) ✓
- **Status:** MATCH

---

### CALC-11: Analysis.md §2.3 — "only two beams" and HDD description
- **Claimed:** "Xcimer's HDD uses only two beams, relying on a ring-shaped spatial intensity profile and a brief hohlraum 'pre-pulse' to create a uniform ablation plasma before the main drive pulse."
- **Source check:** XEC §Xcimer's Hybrid Direct-Drive Target describes two-beam geometry with ring-shaped intensity profile ✓. However, the analysis.md description mentions a "hohlraum 'pre-pulse'". XEC does not describe a hohlraum pre-pulse; the HDD design uses a ring-shaped beam profile on the capsule directly (it is direct drive, not hohlraum). The word "hohlraum" here appears to be a loose description of the intensity-shaping pre-pulse, but it is technically incorrect — a hohlraum is the gold/uranium cylindrical enclosure used in NIF indirect drive. The pre-pulse in HDD creates an ablation plasma; calling it a "hohlraum pre-pulse" conflates HDD and indirect drive.
- **Status:** FACTUAL CONCERN — see PA-3.

---

## Model Setup Audit

### MSA-1: NET_ELECTRIC_MW = 400.0
- **Value:** 400 MWe
- **Source:** [XEC] §Executive Summary / §Roadmap, [an] §5 Table
- **Status:** TRACED
- **Notes:** Source confirmed at XEC §Roadmap: "producing about 400 MW electric." Citation accurate.

---

### MSA-2: AVAILABILITY = 0.85
- **Value:** 0.85 (upper scenario); 0.70 noted as lower scenario
- **Source:** [an] §Section 5 Missing Parameters (gap #3 "truly-unknown")
- **Status:** TRACED (as an assumption, not a sourced value)
- **Notes:** The code correctly marks this UNCERTAIN and labels it a "blocking gap." The value is an engineering assumption with no source citation in either the model or analysis. The code comment is honest about the uncertainty. No issue.

---

### MSA-3: LIFETIME_YR = 30
- **Value:** 30 years
- **Source:** [app] §Xcimer's approach; [an] §5 Table
- **Status:** TRACED
- **Notes:** xcimer-energy-approach.md does not explicitly state "30 years." The 30-year claim is from the XEC whitepaper §Xcimer's Chamber Design discussion of FLiBe liquid wall eliminating structural replacement. The xcimer-approach.md states the FLiBe liquid wall approach "extend[s] the lifetime" (xcimer-science-page.md, line ~54). The 30-year figure is not directly sourced to a specific sentence in the available ingested files; it is cited as HYLIFE heritage in analysis.md §1. Sourcing is by inference from liquid-wall design philosophy. Flag as weakly traced.

---

### MSA-4: LASER_ENERGY_MJ = 10.0 (midpoint of 8–12 MJ)
- **Value:** 10.0 MJ
- **Source:** [XEC] §Executive Summary
- **Status:** TRACED
- **Notes:** XEC §Roadmap specifies Athena at "8 MJ on-target." The 10 MJ midpoint is the model_setup.py choice, described as "midpoint of 8–12 MJ range." This is reasonable for scenario analysis but diverges from the specific Athena design point (8 MJ). For an Athena-focused model, 8 MJ would be more precise. See PA-2.

---

### MSA-5: REP_RATE_HZ = 0.5
- **Value:** 0.5 Hz
- **Source:** [app] §Rep Rate; [XEC] §Executive Summary; [an] §5 Table
- **Status:** TRACED
- **Notes:** Sources confirm 0.25–1 Hz range; 0.5 Hz is midpoint. Appropriate for a nominal scenario.

---

### MSA-6: ETA_PIN1 = 0.07 (laser wall-plug efficiency)
- **Value:** 7%
- **Source:** [XEC] §Challenge 3; [an] §5 Table
- **Status:** TRACED
- **Notes:** XEC §Next Steps states "7% laser efficiency" for NOAK. Electra demonstrated 7% at 750 J. Correctly flagged as not demonstrated at MJ scale.

---

### MSA-7: ETA_TH_BRAYTON = 0.45 (He Brayton thermal efficiency)
- **Value:** 45%
- **Source:** "HYLIFE-II 1994 — ~45% thermal efficiency for He Brayton at FLiBe temp"
- **Status:** UNTRACED (from ingested sources)
- **Notes:** The 45% figure is attributed to HYLIFE-II 1994 heritage, but the HYLIFE-II report is not ingested (analysis.md §8 item 8: "Not directly ingested"). The hylife-energy-conversion-notes.md ingested file contains only metadata/abstract — no thermal efficiency value appears in it. The 45% figure is a commonly cited figure for helium Brayton at FLiBe temperatures, but it is not traceable to any ingested source file. See PA-4.

---

### MSA-8: ETA_TH_STEAM = 0.33 (Steam Rankine thermal efficiency)
- **Value:** 33%
- **Source:** [sci] §Energy Conversion
- **Status:** PARTIALLY TRACED
- **Notes:** xcimer-science-page.md says "generate steam, which in turn drives turbines." It does not provide a thermal efficiency percentage. The 33% is a standard steam Rankine estimate, not extracted from the cited source. The code correctly flags this UNCERTAIN. Acceptable as industry-standard assumption, but the citation is to a source that does not specify the number.

---

### MSA-9: P_PUMP_MW = 15.0 (FLiBe pumping power)
- **Value:** 15 MW
- **Source:** [an] §2.4; [XEC] §Xcimer's Chamber Design
- **Status:** UNTRACED (explicit estimate)
- **Notes:** The code comments clearly state: "No published pumping power estimate for a thick-liquid-wall HYLIFE-scale plant. 15 MW is an order-of-magnitude estimate." The XEC source does not provide a pumping power figure. The estimate is internally flagged as UNCERTAIN. No issue with transparency; value is an engineering estimate with no external citation.

---

### MSA-10: mn = 1.1 (neutron multiplier)
- **Value:** 1.1
- **Source:** "FLiBe (⁹Be) → (n,2n) → mn ≈ 1.1; consistent with TBR ~1.2 (natural Li); [XEC] §Xcimer's Chamber Design"
- **Status:** PARTIALLY TRACED
- **Notes:** XEC §Xcimer's Chamber Design mentions TBR ~1.2 with FLiBe and natural lithium, and attributes it to (n,2n) neutron multiplication in the large capsule. However, mn = 1.1 specifically is not stated in XEC; this is an inferred value from the framework. The TBR ~1.2 figure comes from XEC, but the mn decomposition is a modeling assumption. Acceptable but not directly sourced.

---

### MSA-11: C220104 override (laser driver capital)
- **Value:** LASER_NOAK_MID_MS = $700 M (base case)
- **Source:** [XEC] §Xcimer Laser Cost and Schedule; [an] §5 Table
- **Status:** TRACED
- **Notes:** $70/J × 10 MJ = $700 M. Derivation is correct. The use of C220104 (supplementary heating / driver account) for the laser capital is acknowledged as an approximation since no standard CAS account covers a KrF excimer driver. This is appropriate given the framework limitations.

---

### MSA-12: C220103 = 0.0 override (magnets)
- **Value:** 0.0 M$
- **Source:** [app]; [an] §7 cross-concept table
- **Status:** TRACED
- **Notes:** IFE has no superconducting magnets. Override is correct and well-justified. The xcimer-energy-approach.md confirms two-beam liquid-wall geometry with no magnets.

---

### MSA-13: construction_time_yr = 5.0 (DEFAULT)
- **Value:** 5 years
- **Source:** DEFAULT: ife_laser_ife.yaml
- **Status:** UNTRACED (framework default)
- **Notes:** No Xcimer-specific construction timeline for Athena is available in ingested sources. Using the framework IFE default is reasonable. The roadmap shows Athena targeted for ~2035 from a ~2026 starting point, implying ~9 years total program time (including development), but construction of the plant itself could be shorter. Framework default of 5 years is not unreasonable but is weakly validated.

---

### MSA-14: eta_pin2 = ETA_PIN1 (same laser train, no separate ignition)
- **Value:** 0.07 (same as eta_pin1)
- **Source:** [an] §2.3: "only two beams...brief hohlraum pre-pulse"
- **Status:** TRACED (rationale correct)
- **Notes:** In HDD, there is no separate ignition laser; both "beams" are the same KrF system. Setting eta_pin2 = eta_pin1 is correct. P_IGNITION_MW = 0 is also correct for this architecture.

---

### MSA-15: eta_p = 0.5 (pumping efficiency)
- **Value:** 0.5
- **Source:** DEFAULT: ife_laser_ife.yaml
- **Status:** UNTRACED
- **Notes:** No Xcimer-specific pumping efficiency cited. Framework default used. Acceptable.

---

### MSA-16: blanket_t = 0.80 m (DEFAULT)
- **Value:** 0.80 m FLiBe blanket thickness
- **Source:** DEFAULT
- **Status:** UNTRACED
- **Notes:** Code comment notes "FLiBe liquid wall is ~1–2 m deep; default 0.8 m underestimates blanket volume slightly." XEC describes the FLiBe wall as "at least tens of centimeters" thick (§Challenge 2, line ~309). The HYLIFE heritage suggests much thicker walls. 0.8 m is below the expected range and is acknowledged as an underestimate. This affects blanket material costs and TBR calculations in the framework. Flagged in the code but no corrective override is applied. See PA-5.

---

### MSA-17: p_trit = 10.0 MW (DEFAULT: tritium extraction power)
- **Value:** 10 MW
- **Source:** DEFAULT; justified by <150 g inventory implying active in-situ extraction
- **Status:** UNTRACED
- **Notes:** No Xcimer-specific extraction power estimate. Framework default accepted. Reasonable given the low inventory design.

---

## Consistency Check

**Section 5 parameters vs. Section 2 narrative:**

The parameter table in Section 5 is largely consistent with the Section 2 narrative. Key checks:

1. Qsci ~250 at NOAK (S5 table) matches the 7% × Qsci 250 = 17.5 wall-plug gain discussion in S2.2. Consistent.
2. Recirculating power fraction 11–13% (S5 table) derived at NOAK Qsci 250 / 7% laser efficiency matches the XEC-cited range. Consistent.
3. Laser energy 8–12 MJ (S5 table) vs. "8 MJ on-target" Athena (Roadmap) and "10 MJ" used in model_setup.py. The S5 table shows the full range; model uses midpoint. Minor tension but not an inconsistency.
4. Rep rate 0.25–1 Hz (S5 table, S2 narrative). Consistent throughout.
5. Net output ~400 MWe (S5 table) matches S2 narrative and model. Consistent.

**TRL ratings vs. Section 2 challenges:**

1. KrF laser MJ-scale: TRL 2–3 in S3. S2.1 correctly describes this as "never before built at MJ-scale." S2.3 adds that two-beam HDD is also undemonstrated. These are separate subsystems but analysis groups them into separate TRL ratings. Consistent.
2. FLiBe chamber: TRL 3–4 in S3. S2.4 correctly identifies analog experiments (water/oil) but no FLiBe at fusion-relevant conditions. Consistent.
3. Target fabrication at throughput: TRL 3–4 in S3. S2.6 correctly identifies throughput (8–31 M/yr) as the core challenge. Consistent.
4. Energy conversion BOP: TRL 7–8 in S3. S2.5 identifies the cycle type ambiguity but correctly rates the underlying steam/Brayton technology as mature. Consistent.

**model_setup.py vs. analysis.md parameter table:**

All model parameters that have corresponding entries in the analysis.md §5 parameter table are consistent:
- Laser energy: 10 MJ (midpoint, per model comment) vs. "8–12 MJ" range in table ✓
- Rep rate: 0.5 Hz (midpoint) vs. "0.25–1 Hz" range ✓
- η_laser: 7% ✓
- η_th: 45% (He Brayton base) and 33% (Steam H-3 alt) — both bracketed by the analysis's "blocking gap" flag ✓
- Net output: 400 MWe ✓
- TBR via mn=1.1: consistent with TBR ~1.2 (FLiBe, natural Li) per XEC ✓
- Tritium inventory <150 g (Athena): consistent with p_trit=10 MW assumption (active extraction) ✓

One tension: model_setup.py uses `noak=False` for the FOAK scenario to apply a "10% contingency premium." Analysis.md §5 table entry for FOAK cost ($100/J) is sourced directly from XEC rather than derived from a NOAK value with a premium. The model's FOAK scenario is therefore mechanically different from the source's FOAK definition, though both produce numbers in the same range. This is a modeling approach issue worth flagging.

**Section 2 "only two beams…hohlraum pre-pulse" description:**

Analysis.md §2.3 states: "relying on a ring-shaped spatial intensity profile and a brief hohlraum 'pre-pulse' to create a uniform ablation plasma before the main drive pulse." The XEC document does not describe a "hohlraum pre-pulse" in the HDD concept — it describes a ring-shaped spatial intensity profile that achieves uniform illumination in two-beam direct drive without a hohlraum. This appears to be a technical error in the analysis text — the word "hohlraum" should not appear here. See PA-3.

---

## Proposed Actions

### PA-1: Electra rep rate stated as 5 Hz for "days" — source says 2.5 Hz for 10 hours
- **Category:** factual-concern
- **Severity:** important
- **Location:** analysis.md §Section 3, "KrF Excimer Laser at MJ Scale..." bullet "Demonstrated"
- **Finding:** Analysis.md states "NRL Electra laser demonstrated KrF excimer operation at ~750 J, 5 Hz continuous for days." The XEC whitepaper (§Xcimer's Novel Laser Architecture, line ~587) states Electra "operated continuously for 10 hours at 2.5 Hz repetition rate." The rep rate (5 Hz vs 2.5 Hz) and duration ("days" vs "10 hours") are both inconsistent with the XEC source. No other ingested source provides a different figure; the Mehlhorn 2024 paper cited in analysis.md §8 is not ingested.
- **Proposed Fix:** Correct to "~750 J, 2.5 Hz continuous for 10 hours" based on XEC source. If Mehlhorn 2024 provides a different figure (5 Hz), add that source citation. Note: the 5 Hz figure may come from Mehlhorn 2024 (not ingested) and both figures may describe different test runs — a careful reading of Mehlhorn 2024 is recommended before correcting.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-2: Model uses 10 MJ laser energy; Athena design point is 8 MJ per XEC roadmap
- **Category:** inconsistency
- **Severity:** important
- **Location:** model_setup.py LASER_ENERGY_MJ = 10.0; analysis.md §2 "Modeling Approach": "8 MJ on-target laser energy"
- **Finding:** The analysis.md §2 modeling approach correctly identifies "8 MJ on-target laser energy" as the Athena design point anchor, consistent with the XEC roadmap table (line ~978: "8 MJ on-target / 400 MWe output"). However, model_setup.py sets LASER_ENERGY_MJ = 10.0 as "midpoint of 8–12 MJ range." The result is that the model is not calibrated to the stated primary modeling target (Athena 400 MWe FOAK at 8 MJ), but rather to a commercial-range midpoint. This affects:
  - Laser capital: 10 MJ × $110/J = $1,100 M (FOAK) vs. 8 MJ × $110/J = $880 M (Athena-specific)
  - P_IMPLOSION_MW: 5.0 MW at 0.5 Hz vs. 4.0 MW at 0.5 Hz for 8 MJ
  - These differences propagate into LCOE through the power balance (Qsci, recirculating fraction) and capital cost.
- **Proposed Fix:** Either (a) change LASER_ENERGY_MJ to 8.0 for the Athena-anchored base scenario and add a 10 MJ commercial scenario, or (b) explicitly document that the primary model is a "commercial design midpoint" rather than the Athena pilot, and update analysis.md §2 "Primary modeling target" accordingly to reflect what the model actually represents. Option (a) better aligns with the stated modeling philosophy.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-3: "Hohlraum pre-pulse" in HDD description is technically incorrect
- **Category:** factual-concern
- **Severity:** important
- **Location:** analysis.md §2.3 "Two-Beam Hybrid Direct Drive Target Implosion is Undemonstrated"
- **Finding:** Analysis.md §2.3 describes Xcimer's HDD as using "only two beams, relying on a ring-shaped spatial intensity profile and a brief hohlraum 'pre-pulse' to create a uniform ablation plasma before the main drive pulse." The term "hohlraum pre-pulse" is technically incorrect. A hohlraum is the heavy-metal cylindrical enclosure used in NIF indirect drive to convert laser energy to X-rays. Xcimer's HDD does not use a hohlraum. The XEC document (§Xcimer's Hybrid Direct-Drive Target) describes two-beam direct drive with a ring-shaped spatial intensity profile to achieve symmetric implosion — it does not mention any hohlraum or hohlraum-like pre-pulse. The "Hybrid" in HDD refers to the intensity shaping technique (ring profile), not to a hybrid indirect/direct approach using a hohlraum. Using "hohlraum" here conflates HDD with indirect drive and could mislead a reader about the physics.
- **Proposed Fix:** Remove "hohlraum pre-pulse." Replace the description with: "relying on a ring-shaped spatial intensity profile to achieve symmetric two-beam direct illumination of the capsule ablator, with a shaped pre-pulse (if any) to condition the ablator plasma." Verify against XEC §Xcimer's Hybrid Direct-Drive Target and the Thomas et al. 2024 paper cited in XEC footnote 42 before finalizing the replacement text.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-4: He Brayton 45% thermal efficiency not traceable to any ingested source
- **Category:** citation-error
- **Severity:** important
- **Location:** model_setup.py ETA_TH_BRAYTON = 0.45 comment; analysis.md §2.5
- **Finding:** The 45% thermal efficiency for He Brayton is attributed to "HYLIFE-II 1994" in model_setup.py and analysis.md §2.5. The hylife-energy-conversion-notes.md ingested file contains only the OSTI abstract/metadata for UCRL-CR-105908 (the HYLIFE-II BOP cost study) — no thermal efficiency value is available in the ingested content. The HYLIFE-II report itself (Moir et al., 1994) is not ingested (analysis.md §8 item 8: "Not directly ingested"). The 45% figure cannot be verified from available sources. It is physically plausible (He Brayton at FLiBe outlet temperatures of ~600–700°C can achieve ~40–50%) but is unverified.
- **Proposed Fix:** Either (a) add "[unverified from ingested sources; HYLIFE-II 1994 is behind paywall — confirm before use]" to the model_setup.py comment and analysis.md §2.5, or (b) ingest and verify the HYLIFE-II report or an equivalent source that provides a specific thermal efficiency figure. This parameter directly affects the H-3 analysis and the LCOE difference between the two thermal scenarios.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-5: Blanket thickness 0.80 m acknowledged as underestimate; no corrective override
- **Category:** improvement
- **Severity:** minor
- **Location:** model_setup.py blanket_t = 0.80; comment "underestimates blanket volume slightly"
- **Finding:** The model uses the framework default blanket thickness of 0.80 m. The code comment acknowledges that FLiBe liquid wall is "~1–2 m deep" and that 0.80 m "underestimates blanket volume slightly." The XEC document describes the liquid wall as "at least tens of centimeters" (which 0.80 m satisfies) but HYLIFE-scale designs typically use 0.5–2 m of FLiBe. The underestimate affects: (a) FLiBe material inventory cost in CAS27/CAS50 (framework likely uses blanket_t in material cost scaling), (b) the neutron multiplication factor, and (c) TBR calculations. Since the framework's CAS27 is already flagged as "default PbLi-calibrated; likely understates FLiBe/Be cost" (model_setup.py line ~414), the double-underestimate (wrong default material × underestimated thickness) could meaningfully affect blanket cost. However, blanket cost is not among the top-3 LCOE drivers for this concept.
- **Proposed Fix:** Consider setting blanket_t = 1.0 m as a nominal midpoint of the 0.5–2 m range, with a comment noting the range. Alternatively, add a note to the analysis that blanket cost is likely understated by the framework defaults due to both wrong reference material and underestimated thickness.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-6: CV-17 — "Xcimer's approach utilizing a liquid first wall..." quoted as xcimer-energy-approach.md but text is in xcimer-science-page.md
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §4 block quote, footnote [3] xcimer-energy-approach.md
- **Finding:** The block quote "Xcimer's approach utilizing a liquid first wall allows us to use readily available commercial materials that minimize activation, extend the lifetime and comply with our waste and safety goals." is attributed to xcimer-energy-approach.md in analysis.md §4. The text is actually from xcimer-science-page.md (line ~54). xcimer-energy-approach.md contains related but different language ("We use flowing liquid lithium salt to protect the chamber's structural walls from fusion neutrons—minimizing maintenance and reducing waste" — line ~30 of approach.md).
- **Proposed Fix:** Update the citation to xcimer-science-page.md. Confirm that the xcimer-energy-approach.md citation in §4 footnote [3] is changed to xcimer-science-page.md for this specific quote.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-7: CV-18 — FLiNaK paraphrase formatted as direct quote
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §4, block quote attributed to xec-20260224 §Xcimer's Chamber Design
- **Finding:** Analysis.md §4 presents "Commercial plants could switch to FLiNaK... to avoid beryllium supply chain entirely." as a direct quotation. The actual XEC text is "FLiNaK can be used in commercial plants in place of FLiBe, avoiding beryllium supply chains." The paraphrase changes phrasing ("could switch to" vs "can be used") and adds "entirely" which is not in the source. Formatted as a block quote, this implies verbatim quotation.
- **Proposed Fix:** Either use the exact source text, or change formatting from block-quote to inline paraphrase with appropriate attribution.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-8: FOAK laser $/J interpretation: analysis.md uses $100/J; model uses $110/J midpoint
- **Category:** inconsistency
- **Severity:** minor
- **Location:** analysis.md §5 parameter table (FOAK: "~$100/J"), model_setup.py LASER_FOAK_PER_J = 110.0
- **Finding:** The parameter table in analysis.md lists FOAK at "~$100/J on-target." model_setup.py uses $110/J as "midpoint $100–120/J." The XEC source gives a range of "$100 to $120/J." Using $100 (analysis table) vs $110 (model) is a minor but visible inconsistency. The model's $110 is arguably more accurate as it represents the midpoint of the source range; analysis.md's "$100" uses the lower bound. The 10% difference on a $1B+ item (~$100M) is non-trivial.
- **Proposed Fix:** Update analysis.md §5 parameter table FOAK entry to "$100–120/J (midpoint $110/J)" to match model_setup.py and the source range, with the existing "$100/J" interpretation reserved for the lower-bound sensitivity.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-9: Section reference inconsistencies in citation footnotes (CV-1, CV-2, CV-9, CV-10)
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §2, various block quote citations
- **Finding:** Multiple block quotes are attributed to sections of XEC that are not where the text appears:
  - CV-1: "§Xcimer's Novel Laser Architecture" — actual location: §Next Steps
  - CV-2: "§Challenge 3: Cost and Economics" — actual location: §Next Steps
  - CV-9: "§Challenge 3" — actual location: §Challenge 1
  - CV-10: "§Challenge 3" — actual location: §Next Steps
  These are minor attribution errors that do not affect the content accuracy but could impede source verification.
- **Proposed Fix:** Update section references in the affected footnotes. Note: some claims are repeated in multiple sections of XEC (e.g., the 7% efficiency / Qsci 250 / 11–13% recirculating power claim appears in both §Next Steps and is discussed in §Challenge 3 context), so both attributions may be partially defensible. Prefer the most specific section where the exact text first appears.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 30
- **Citations verified:** 26 (FOUND or confirmed substance)
- **Citations not found / wrong attribution:** 4 (CV-17 wrong source file; CV-18, CV-19 paraphrases as quotes; CV-30 / CV-20 factual discrepancy in Electra data)
- **Calculations checked:** 11
- **Calculations matched:** 11 (all arithmetic verified correct)
- **Model parameters audited:** 17
- **Proposed Actions:** 9 (blocking: 0, important: 4, minor: 5)
- **Overall:** HAS ISSUES

Key findings by severity:

**Important:**
- PA-1: Electra rep rate (5 Hz / "days" in analysis vs. 2.5 Hz / 10 hours in source) — factual error requiring resolution against Mehlhorn 2024.
- PA-2: Model uses 10 MJ laser energy; stated primary modeling target (Athena) is 8 MJ per XEC roadmap — misalignment between model and stated scope.
- PA-3: "Hohlraum pre-pulse" in HDD description is technically incorrect — hohlrums are used in indirect drive (NIF), not in Xcimer's direct-drive architecture.
- PA-4: He Brayton 45% thermal efficiency cannot be verified from any ingested source; HYLIFE-II report is behind paywall.

**Minor:**
- PA-5: Blanket thickness acknowledged as underestimate with no corrective override.
- PA-6: One block quote attributed to the wrong source file.
- PA-7: Paraphrase formatted as direct quotation.
- PA-8: FOAK $/J value differs between analysis.md table ($100/J) and model ($110/J midpoint).
- PA-9: Multiple XEC section references in footnotes point to the wrong section within the document.
