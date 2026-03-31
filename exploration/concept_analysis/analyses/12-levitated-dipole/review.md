# Review: Levitated Dipole (D-T)

**Iteration:** 1
**Date:** 2026-03-30
**Files reviewed:** analysis.md, model_setup.py
**Source documents:** 5 files (arxiv-2602-20564 [iter-01 and iter-02 variant], arxiv-2508-17691, openstar-prototype-roadmap, openstar-2026-funding-tahi-timeline)

---

## Citation Verification

### CV-1: "preliminary results from this model which are subject to change" (Section 1)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Discussion
- **Status:** FOUND (wrong section)
- **Actual text:** "OpenStar is currently in the process of developing a model for estimating the overnight capital cost and LCOE for levitated dipole fusion power plants which will be the topic of future work. This study uses preliminary results from this model which are subject to change as the model is developed."
- **Notes:** Located in §3.3 Optimization Constraints, not §Discussion. The quote is accurate; the section attribution is wrong. §Discussion (§5) does not contain this passage.

---

### CV-2: "The assumption that these reactors will be Q_sci = 15 is only valid if a smaller demonstration device...displays adequate plasma performance." (Section 2)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Discussion
- **Status:** FOUND
- **Actual text:** "The assumption that these reactors will be $Q_{sci} = 15$ is only valid if a smaller demonstration device, which we will call Tahi, displays adequate plasma performance."
- **Notes:** Section attribution to §Discussion is correct (§5 Discussion, line 758). Quote is accurate. The bracketed editorial "[the next prototype, ~2028, target 20 T]" is correctly marked as analyst synthesis, not quotation.

---

### CV-3: "Intrinsic decoupling of the confining magnetic field-generating REBCO magnets and the vacuum vessel offer unparalleled accessibility and maintainability." (Section 2)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Introduction
- **Status:** FOUND
- **Actual text:** "The intrinsic decoupling of the confining magnetic field-generating REBCO magnets and the vacuum vessel offer unparalleled accessibility and maintainability, allowing for high plant duty factors and theoretically low electricity prices." (Abstract)
- **Notes:** The exact quote is in the Abstract, not §Introduction. The introduction contains the same concept in paraphrase. Minor attribution imprecision; no substantive concern.

---

### CV-4: "The physics defining an upper bound on the value of p_lcfs is not well understood as no dipole experiments have yet had enough heating power to generate edge conditions applicable to fusion power plants." (Section 2)
- **Source cited:** arxiv-2602-20564-plasma-state-clarification.md §2.1.4
- **Status:** FOUND
- **Actual text:** "The physics defining an upper bound on the value of $p_{lcfs}$ is not well understood as no dipole experiments have yet had enough heating power to generate edge conditions applicable to fusion power plants."
- **Notes:** Section attribution §2.1.4 (Plasma Edge Conditions) is correct. Exact text match confirmed in both iter-01 and iter-02 source files.

---

### CV-5: "Tungsten will undergo recrystallization and it is possible that the onset of degraded mechanical properties can be delayed until other forms of damage dominate." (Section 3)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §4.3 Neutron Transport
- **Status:** PARTIAL MATCH
- **Actual text:** "...the tungsten tiles in Reactor A reach a maximum steady state temperature of 1950 K which is well below the design constraint of 2500 K, but above the recrystallization temperature... As long as the shield is maintained at these elevated temperatures it is possible that the onset of the degraded mechanical properties can be delayed until other forms of damage dominate."
- **Notes:** The first clause of the analysis quote ("Tungsten will undergo recrystallization") does not appear verbatim in the source. The source describes the tiles as operating "above the recrystallization temperature" — the analysis has converted this into a declarative sentence. The second half of the analysis quote is a close paraphrase of the actual source text. Section attribution §4.3 is correct. The blockquote presentation implies a single continuous passage; it is a composite of two separated sentences. Severity: minor — meaning is faithfully captured.

---

### CV-6: "greatest magnetic stored energy delivered by an HTS flux pump to date" (Section 3 / parameter table)
- **Source cited:** arxiv-2508-17691-junior-design-results.md §Flux Pump Results
- **Status:** FOUND
- **Actual text:** "...charged to ~600 A which is ~42% of its design current achieving the greatest magnetic stored energy delivered by an HTS flux pump to date." (§4 Initial Results)
- **Notes:** Located in §4 Initial Results, not a separately titled §Flux Pump Results. The claim is confirmed; section name is approximate but unambiguous.

---

### CV-7: Parameter table — Fusion power 667 MW / Net electric 208 MWe / Gross electric ~296 MWe
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Table 6 and §Table 9
- **Status:** FOUND
- **Actual text:** Table 6: "Fusion power: 667 MW" (Reactor A); Table 9: "Net Electric Power: 208 MW", "Total Electrical Power: 296 MW" (Reactor A)
- **Notes:** All three values confirmed exactly in Tables 6 and 9.

---

### CV-8: Parameter table — REBCO tape 4,320 km cited to §Table 7
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Table 7
- **Status:** FOUND (wrong table)
- **Actual text:** Table 5 (mass/component breakdown): "REBCO Tape: 4,320 km" (Reactor A)
- **Notes:** The 4,320 km value appears in Table 5 (mass table), not Table 7 (core magnet design parameters: peak field, inductance, float time, etc.). This is a citation error — wrong table number. The value itself is correct.

---

### CV-9: Parameter table note — "+~1.2 km top magnet" REBCO tape
- **Source cited:** Not explicitly cited in the parameter table; marked "dossier"
- **Status:** NOT FOUND (in any primary power plant source)
- **Actual text:** Not present in Simpson et al. (2602.20564). The 1.2 km figure appears in the Junior top magnet Table 2 (arxiv-2508-17691): "Tape length: 1.2 km."
- **Notes:** Simpson et al. explicitly states "the details of the levitation coil have not been considered" for the power plant. The analyst has applied the Junior prototype top magnet tape length as an estimate for the Reactor A top magnet. This analogue is invalid: the power plant core magnet operates at ~29.4 kA (Table 7) vs. ~700 A for the Junior top magnet — a 42× current difference. The power plant top magnet tape content would be on the order of tens of km, not 1.2 km. This is a factual concern in the notes column.

---

### CV-10: Parameter table — Plant duty cycle 90.1%, Plant availability 96%
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §3.2.5 and §Table 7
- **Status:** FOUND
- **Actual text:** Combined parameter table (near Table 5 in §4): "Core magnet duty cycle: 90.1% (Reactor A)"; "Plant availability factor: 96%"
- **Notes:** Both values confirmed in source. The duty cycle appears in the reactor overview table alongside Table 5 data, not exclusively in §Table 7 (magnet design parameters). Values are correct.

---

### CV-11: Parameter table — Energy confinement times 3.5 s (A), 5.9 s (B)
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Table 6
- **Status:** FOUND
- **Actual text:** Table 6: "Energy confinement time: 3.5 s (Reactor A), 5.9 s (Reactor B)"
- **Notes:** Exact match.

---

### CV-12: Parameter table — Cryogenic load "14.1 kW deposited, 1.31 MW wall plug"
- **Source cited:** arxiv-2602-20564-dt-dipole-power-plants.md §Table 9
- **Status:** PARTIAL MATCH
- **Actual text:** Table 9 Core Magnet section: total heating = 16.4 kW (neutron 13.5 + photon 0.59 + electrical 1.3 + conductive 1.0 = 16.4 kW); Table 9 Plant: "Cryogenic Cooling: -1.31 MW"
- **Notes:** The analysis states "14.1 kW deposited" as a single value. The source does not tabulate 14.1 kW as an explicit line item; the nearest interpretation is neutron + photon = 13.5 + 0.59 = 14.09 kW ≈ 14.1 kW (excluding electrical and conductive heating). The 1.31 MW wall-plug is confirmed directly in Table 9. The 14.1 kW figure is a partial subtotal not stated as such in the source — minor documentation gap.

---

### CV-13: Junior prototype cost <$10M, built in under 2 years (Section 1 / parameter table)
- **Source cited:** arxiv-2508-17691-junior-design-results.md §3
- **Status:** FOUND
- **Actual text:** "The Junior system described in this article was designed and built in under 2 years at a cost of < $10M USD" (§3 Experiment Overview)
- **Notes:** Exact match.

---

### CV-14: Parameter table — Tama Nui commercial range 50–200 MWe
- **Source cited:** openstar-2026-funding-tahi-timeline.md
- **Status:** FOUND
- **Actual text:** "the fourth-gen model, Tama Nui, may produce 50 to 200 megawatts of electricity"
- **Notes:** Exact match (Bloomberg source).

---

### CV-15: Neon hydrogen backup quote (Section 3)
- **Source cited:** Analysis Section 3 narrative (not explicitly block-quoted)
- **Status:** FOUND
- **Actual text:** "However if procuring and maintaining a supply of neon proves challenging it would be a viable alternative." (arxiv-2602-20564 §3.2.5, discussing hydrogen as alternative cryogen; source also states hydrogen "needs ~5 times the volume to store the same amount of energy")
- **Notes:** Analysis correctly states the source proposes hydrogen as backup requiring a 5× larger reservoir. Confirmed in source §3.2.5 (Cryogenic Cooling subsection narrative).

---

## Calculation Verification

### CALC-1: Recirculating power fraction ~30%
- **Claimed:** [inferred: (296 − 208)/296 from Table 9 gross vs. net electric] ~30%
- **Re-derived:** (296 − 208) / 296 = 88 / 296 = 29.73% ≈ 30%
- **Status:** MATCH
- **Notes:** Table 9 gross electric = 296 MW and net = 208 MW confirmed. Calculation is correct.

---

### CALC-2: ICRH wall-plug power 63.6 MW from Q_sci = 15 at 70% efficiency
- **Claimed:** P_plasma = 667/15 = 44.5 MW; P_icrh_grid = 44.5/0.70 = 63.6 MW
- **Re-derived:** 667/15 = 44.47 MW; 44.47/0.70 = 63.52 MW ≈ 63.6 MW
- **Status:** MATCH
- **Notes:** Both values confirmed exactly in Table 6 (44.5 MW auxiliary heating) and Table 9 (−63.6 MW plasma heating wall power). Derivation chain is self-consistent and independently verified.

---

### CALC-3: Annual sacrificial tape replacement ~864 km/yr
- **Claimed:** ~20% of 4,320 km core magnet tape = ~864 km/yr
- **Re-derived:** 0.20 × 4,320 = 864.0 km exactly
- **Status:** MATCH
- **Notes:** Source Table 5 confirms 4,320 km REBCO tape (Reactor A). Source §Abstract and §4.3 confirm ~20% sacrificial section. Derivation is exact.

---

### CALC-4: "30-year cumulative tape ~31,000 km, roughly 5× the initial inventory" (Section 4)
- **Claimed:** "cumulative tape consumption approaches ~31,000 km per Reactor A — roughly 5× the initial inventory"
- **Re-derived:** 4,320 + (30 × 864) = 4,320 + 25,920 = 30,240 km; 30,240 / 4,320 = 7.0× (not 5×)
- **Status:** MISMATCH
- **Notes:** Two errors:
  1. The "5×" multiplier is wrong relative to the core magnet tape inventory of 4,320 km (correct is 7.0×). The 5× figure is only approximately correct if the denominator includes an estimated top magnet tape (~1,200 km, per Junior analogue), giving 30,240 / 5,520 ≈ 5.5× — but this requires using an unvalidated analogue as the denominator without stating so.
  2. The cumulative figure of "~31,000 km" slightly overstates the calculated 30,240 km (rounds to ~30,000 more naturally).
  Additionally, the model uses a 40-year lifetime (see CALC-5) while the narrative says "30-year plant life" — the two are inconsistent.

---

### CALC-5: Plant lifetime inconsistency — analysis text vs. model
- **Claimed:** Section 4 narrative says "30-year plant life"; model_setup.py uses plant_lifetime_years = 40.0
- **Re-derived:** Not arithmetic — a consistency check.
- **Status:** MISMATCH (internal inconsistency)
- **Notes:** Section 4 explicitly uses "30-year plant life" for the supply chain narrative. The economic model uses 40 years (1costingfe default). This inconsistency means the LCOE is calculated for a 40-year plant while the supply chain analysis is framed for a 30-year plant. At 40 years, the cumulative tape consumption would be 4,320 + (40 × 864) = 38,880 km (≈9× initial). The lifetime assumption should be harmonized.

---

### CALC-6: Thermal efficiency back-calculation (model_setup.py comment)
- **Claimed:** "at η_th=0.38 the model yields p_et ≈ 291 MWe (~2% low); at 40% the model gives p_et ≈ 306 MWe (~3% high)"
- **Re-derived:**
  - Model thermal power = 1.10×(0.80×667) + 0.20×667 + 667/15 = 586.96 + 133.4 + 44.47 = 764.83 MW
  - At 38%: 0.38 × 764.83 = 290.6 MW (model says ~291 MW — MATCH)
  - At 40%: 0.40 × 764.83 = 305.9 MW (model says ~306 MW — MATCH)
  - Root cause: published thermal power (Table 9) = 741 MW; at 40% = 296.4 MW = published 296 MW. The model thermal power is ~24 MW higher than published because it does not capture endothermic tungsten shield losses (−14 MW) and other effects.
- **Status:** MATCH (model comment arithmetic is correct)
- **Notes:** The η=0.38 calibration is reasonable and documented. The comment accurately describes the tradeoff.

---

### CALC-7: Model net electric vs. published 208 MWe
- **Claimed:** Model should be close to published 208 MW net electric
- **Re-derived:**
  - p_et (model at 38%) = 290.6 MW
  - p_icrh_wallplug = 44.47/0.70 = 63.52 MW
  - p_aux = 5.0 + 4.0 + 5.0 + 1.0 = 15.0 MW
  - p_net = 290.6 − 63.52 − 15.0 = 212.1 MW (vs. published 208 MW; +2.0%)
- **Status:** MATCH (within first-pass tolerance)
- **Notes:** The 4 MW overestimate arises because the model budgets ~15 MW for non-ICRH auxiliary loads while Table 9 implies ~23 MW (= 88 MW total recirc − 63.6 MW ICRH − 1.31 MW cryo). The ~8 MW unaccounted auxiliary load explains the p_net gap. Acceptable for first-pass modeling; the gap and its magnitude should be documented (see PA-7).

---

### CALC-8: Confinement time extrapolation ratio (Section 2)
- **Claimed:** "τ_e = 3.5 s — roughly 240× longer" than LDX 14.5 ms
- **Re-derived:** 3.5 / 0.0145 = 241.4×
- **Status:** MATCH
- **Notes:** "240×" is the correct rounded figure. Confirmed against source τ_e = 14.5 ms (cited in §Discussion, line 762) and Reactor A τ_e = 3.5 s (Table 6).

---

### CALC-9: Cryogenic annotation unit error — "1.13 kW wall plug" (model_setup.py)
- **Claimed:** [inline annotation] "14.1 kW / 0.0125 efficiency = 1.13 kW wall plug"
- **Re-derived:** 14,100 W / 0.0125 = 1,128,000 W = 1.128 MW
- **Status:** MISMATCH (unit error in annotation)
- **Notes:** The annotation says "1.13 kW" but the result is 1.13 MW. This is a unit error in the docstring comment only; the model parameter (p_cryo_MW = 5.0) is independently estimated and not directly derived from this formula, so the model output is unaffected. The published 1.31 MW is ~16% higher than 1.128 MW, attributable to fixed cryoplant overhead as noted in the comment.

---

### CALC-10: Combined capacity factor
- **Claimed:** plasma_duty_cycle × plant_availability = 0.901 × 0.96 = 0.865
- **Re-derived:** 0.901 × 0.96 = 0.86496 ≈ 0.865
- **Status:** MATCH

---

## Model Setup Audit

### MSA-1: p_fus_MW = 667.0 MW
- **Value:** 667.0 MW
- **Source:** analysis.md §Section 5; arxiv-2602-20564 Table 6
- **Status:** TRACED
- **Notes:** Exact match to source Table 6.

---

### MSA-2: thermal_efficiency = 0.38
- **Value:** 0.38 (paper states 40%; model uses 38% as calibration anchor)
- **Source:** Documented derivation in model comment; arxiv-2602-20564 §3.2.5 / §4.4
- **Status:** TRACED
- **Notes:** Calibration rationale is fully documented (CALC-6). The choice is intentional and well-explained; flagged HIGH UNCERTAINTY.

---

### MSA-3: qsci = 15.0
- **Value:** 15.0
- **Source:** arxiv-2602-20564 §3.3 (design constraint), §Discussion
- **Status:** TRACED
- **Notes:** Q_sci = 15 confirmed as hard optimization constraint (Table 4 constraints; §3.3 narrative). Validation derivation (P_plasma = 44.5 MW, P_icrh = 63.6 MW) matches Table 6 and Table 9 exactly.

---

### MSA-4: icrh_wall_plug_efficiency = 0.70
- **Value:** 0.70
- **Source:** arxiv-2602-20564 §4.4 Power Balance ("The total efficiency of the auxiliary heating systems is assumed to be 70%")
- **Status:** TRACED
- **Notes:** Confirmed in source §4.4 narrative. Published value.

---

### MSA-5: p_cryo_MW = 5.0 MW (ASSUMED)
- **Value:** 5.0 MW; published anchor = 1.31 MW (Table 9)
- **Source:** arxiv-2602-20564 Table 9 (1.31 MW published); analyst estimate for total cryoplant load
- **Status:** TRACED (partially)
- **Notes:** Published 1.31 MW correctly cited. The upward revision to 5.0 MW for fixed cryoplant infrastructure is labeled MODERATE UNCERTAINTY and is physically reasonable. No direct source for the additional ~3.7 MW.

---

### MSA-6: plasma_duty_cycle = 0.901
- **Value:** 0.901
- **Source:** arxiv-2602-20564 combined parameter table (§4 overview)
- **Status:** TRACED
- **Notes:** Confirmed in source. Correct value.

---

### MSA-7: plant_availability = 0.96
- **Value:** 0.96
- **Source:** arxiv-2602-20564 combined parameter table
- **Status:** TRACED
- **Notes:** Confirmed in source ("Plant availability factor: 96%").

---

### MSA-8: hts_coil_system_cost_M_USD = 250.0 M$ (OVERRIDE)
- **Value:** $250M; no published cost
- **Source:** CFS ARC analogue from 01-hts-compact-tokamak analysis; analysis.md §Section 2
- **Status:** TRACED (analogue-based)
- **Notes:** No primary source for power plant levitated coil cost. CFS ARC $200–500M for 18 TF coils is the documented analogue. Single-coil scaling rationale is explicitly described. Flagged HIGH UNCERTAINTY. Best available basis given the data gap.

---

### MSA-9: icrh_system_cost_M_USD = 150.0 M$ (OVERRIDE)
- **Value:** $150M; no published cost
- **Source:** ITER ICRH analogue (~$200–250M for 20 MW system, FOAK)
- **Status:** TRACED (analogue-based)
- **Notes:** No primary source for dipole-specific ICRH cost. ITER analogue scaling is documented. Flagged MODERATE UNCERTAINTY. Note: ICRH coupling in a dipole geometry is undemonstrated (analysis Section 3), adding conceptual uncertainty beyond the parameter uncertainty.

---

### MSA-10: rh_scale_factor = 1.50 (C220110, OVERRIDE)
- **Value:** 1.50× standard DT remote handling base ($150M at 1 GWe)
- **Source:** 1costingfe costing_constants.yaml (base); analysis.md §Section 2 (novel coil docking challenge)
- **Status:** TRACED (override)
- **Notes:** Analyst judgment, well-documented, labeled HIGH UNCERTAINTY. Base cost source is documented. The 1.5× multiplier is an expert estimate with no direct analogue; appropriate for first-pass.

---

### MSA-11: sacrificial_section_fraction = 0.20
- **Value:** 0.20
- **Source:** arxiv-2602-20564 §Abstract, §2.2.1, §4.3
- **Status:** TRACED
- **Notes:** Source states "About 20% of the coil is designated as sacrificial" in multiple places. Confirmed.

---

### MSA-12: sacrificial_section_material_cost_M_USD = 45.0 M$/yr (ASSUMED)
- **Value:** $45M/yr; no published cost
- **Source:** REBCO tape price analogue (864 km/yr × $50–100/kA-m); analysis.md §Section 2, §Section 4
- **Status:** TRACED (analogue-based)
- **Notes:** Derivation is documented. The $45M/yr central estimate sits near the optimistic end of current-price scenarios ($52–103M/yr at current tape prices). Labeled HIGH UNCERTAINTY. The $10M/yr NOAK scenario is highly optimistic for tape costs projected 10–15 years out; this may understate the pessimistic bound.

---

### MSA-13: C220112 = 0.0 (Isotope Separation — no Li-6 enrichment)
- **Value:** $0
- **Source:** arxiv-2602-20564 §Conclusions ("TBR in excess of 1.1 without the use of expensive molten salts and neutron multipliers")
- **Status:** TRACED
- **Notes:** Natural Li₂O confirmed as blanket material; no enrichment required. $0 assignment appropriate.

---

### MSA-14: C220108 = 0.0, C220109 = 0.0 (Target Factory, Direct Energy Converter)
- **Value:** Both $0
- **Source:** Conceptual: continuous MFE with no targets; closed-field topology precludes DEC
- **Status:** TRACED
- **Notes:** Both eliminations are conceptually correct. Appropriate.

---

### MSA-15: vessel_inner_radius_m = 3.5 m (ASSUMED)
- **Value:** 3.5 m; actual first-wall radius = 20.6 m (from Table 5 overview)
- **Source:** Analyst estimate from mass data; no published geometry for cost-model geometry
- **Status:** UNTRACED (approximation)
- **Notes:** The actual Reactor A first-wall radius is 20.6 m (Table 5 overview). The 3.5 m is a rough approximation for the concentric-shell geometry model — it is the analyst's geometric placeholder for cost volume scaling. The comment flags this as HIGH UNCERTAINTY. Given that cost is dominated by HTS coil and ICRH overrides (not geometry-scaled accounts), the impact on total LCOE is minor. Acceptable for first-pass with explicit uncertainty flagging.

---

### MSA-16: blanket_thickness_m = 0.80 m (ASSUMED — derived from mass)
- **Value:** 0.80 m
- **Source:** arxiv-2602-20564 Table 5 (3,490 t Li₂O mass); ITER HCPB TBM analogue
- **Status:** TRACED (derived)
- **Notes:** Derivation: 3,490 t / 2.01 t/m³ = 1,737 m³; at r_i = 3.5 m spherical shell → thickness ≈ 0.7–0.9 m. Reasonable. Dependent on the uncertain 3.5 m inner radius.

---

### MSA-17: shield_thickness_m = 0.60 m (ASSUMED)
- **Value:** 0.60 m
- **Source:** arxiv-2602-20564 §4.3 (475 mm W/B₄C/W shield depth); Table 5 (1,760 t tungsten)
- **Status:** TRACED (partially)
- **Notes:** Source gives 475 mm for the neutron-attenuating shield. The model adds ~0.12 m for outer structure to reach 0.60 m. Reasonable interpretation. Acceptable.

---

### MSA-18: ConfinementConcept / model architecture
- **Value:** Standalone parameterized dataclass; no inherited ConfinementConcept base
- **Source:** Model design
- **Status:** TRACED
- **Notes:** The model does not import from a ConfinementConcept base class. It reuses 1costingfe scaling constants by value, with explicit documentation of which accounts are overrides. The three-layer approach (power balance → geometry → CAS22 overrides) is appropriate for a novel concept without a valid reference concept to adapt. No base concept mismatch issue.

---

## Consistency Check

**Section 5 parameters vs. Section 2 narrative:** Clean. Fusion power (667 MW), net electric (208 MWe), auxiliary heating (44.5 MW), duty cycle (90.1%), plant availability (96%), cryo efficiency (1.25%), and confinement times (3.5 s / 5.9 s) are all consistent across Sections 2, 3, and 5. The Section 2 discussion of Reactor B requiring "better-than-Bohm" scaling is consistent with Section 5 showing Reactor B requires τ_e = 5.9 s vs. 3.5 s for Reactor A.

**TRL ratings vs. Section 2 challenges:** All consistent. D-T fusion at Q_sci = 15 (TRL 2) aligns with Impact: Critical for confinement scaling. Annual sacrificial coil replacement (TRL 2–3) aligns with Impact: High and documented lack of activation demonstration. REBCO HTS general (TRL 6–7) aligns with the mature commercial backdrop despite the 23 T / levitated-coil-specific gap. Balance of Plant (TRL 8–9) aligns with the thermal cycle as Impact: Moderate.

**model_setup.py vs. Section 5 parameter table:** All key parameters align (p_fus, Q_sci, η_ICRH, duty cycle, availability, sacrificial fraction, tape quantity). The η_th discrepancy (model: 0.38, paper: 40%) is an intentional calibration documented in both the model and the analysis; not an inconsistency.

**Plant lifetime inconsistency (important):** Section 4 supply chain narrative uses "30-year plant life" while model_setup.py uses plant_lifetime_years = 40 (1costingfe default). This is a genuine inconsistency. At 40 years, the correct cumulative tape consumption is 38,880 km (~9× core inventory). The 30-year figure used in the narrative is not sourced from either the primary literature or from the model itself.

**Neon cryogen operating temperature (consistent):** Section 3 describes neon slush at 24.6 K (melting point); Table 7 gives 30 K operating temperature. These are consistent: the slush provides thermal absorption at 24.6 K to maintain the coil at 30 K (with margin). No inconsistency.

---

## Proposed Actions

### PA-1: Correct citation — "preliminary results" quote is in §3.3, not §Discussion
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 1, first direct quote attribution
- **Finding:** The quote "preliminary results from this model which are subject to change" is attributed to §Discussion. It appears in §3.3 Optimization Constraints (not §5 Discussion).
- **Proposed Fix:** Change "§Discussion" to "§3.3 Optimization Constraints."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-2: Correct citation — REBCO tape 4,320 km is in Table 5, not Table 7
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 5 parameter table, "REBCO tape requirement (A)" row
- **Finding:** Citation reads "§Table 7" for the 4,320 km tape value. The value appears in Table 5 (mass/component breakdown). Table 7 contains core magnet design parameters (peak field, inductance, float time) but not tape quantity.
- **Proposed Fix:** Change citation from "§Table 7" to "§Table 5."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-3: Correct calculation — "roughly 5×" should be "roughly 7×" for REBCO cumulative tape
- **Category:** calculation-error
- **Severity:** important
- **Location:** analysis.md §Section 4, REBCO supply chain paragraph
- **Finding:** "roughly 5× the initial inventory" is arithmetically incorrect. Re-derived: 4,320 + (30 × 864) = 30,240 km = 7.0× the core magnet tape inventory (4,320 km). The 5× figure is only approximately correct if the denominator includes ~1,200 km of estimated top magnet tape (5,520 km total), but the power plant top magnet tape is unpublished and unknown — using the Junior top magnet tape as a power plant analogue is not valid (42× current difference).
- **Proposed Fix:** Change to "roughly 7× the initial core magnet tape inventory (4,320 km)" and note that the top magnet tape quantity is unknown at power plant scale, so total initial inventory is higher than 4,320 km by an unquantified amount.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-4: Resolve plant lifetime inconsistency — harmonize Section 4 narrative with model's 40-year assumption
- **Category:** inconsistency
- **Severity:** important
- **Location:** analysis.md §Section 4 (supply chain narrative) vs. model_setup.py plant_lifetime_years = 40.0
- **Finding:** Section 4 says "Over a 30-year plant life..." while the economic model uses 40 years. This produces a narrative/model inconsistency. The cumulative tape consumption for 40 years = 38,880 km (~9× core inventory), not ~31,000 km or ~7× as implied by the 30-year narrative.
- **Proposed Fix:** Preferred: Update Section 4 to use "40-year plant life" (consistent with model). Note this is the 1costingfe default and is not sourced from OpenStar. If 30 years is the preferred assumption, update model_setup.py plant_lifetime_years to 30, noting departure from 1costingfe default.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-5: Fix unit error in cryogenic annotation in model_setup.py
- **Category:** calculation-error
- **Severity:** minor
- **Location:** model_setup.py p_cryo_MW docstring, annotation line "14.1 kW / 0.0125 efficiency = 1.13 kW wall plug"
- **Finding:** The annotation says "1.13 kW wall plug" but the correct result is 1.13 MW wall plug (14,100 W / 0.0125 = 1,128,000 W = 1.128 MW). The model parameter value (5.0 MW) is unaffected by this annotation error.
- **Proposed Fix:** Change "= 1.13 kW wall plug" to "= 1.13 MW wall plug" in the docstring.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-6: Correct the composite misquotation of tungsten recrystallization (Section 3)
- **Category:** citation-error
- **Severity:** minor
- **Location:** analysis.md §Section 3, Layered W-B₄C-W Neutron Shield blockquote
- **Finding:** The blockquote presents "Tungsten will undergo recrystallization and it is possible that the onset of degraded mechanical properties can be delayed until other forms of damage dominate" as a single passage. The source does not contain the first sentence verbatim; it describes tiles as operating "above the recrystallization temperature." The second half is a close paraphrase. Presenting a synthesis as a direct quotation is misleading.
- **Proposed Fix:** Reconstruct as: paraphrase the first part, then directly quote the second: "The neutron shield tungsten tiles reach 1,950 K — above the recrystallization temperature. The paper notes that at these temperatures, 'it is possible that the onset of the degraded mechanical properties can be delayed until other forms of damage dominate.'"
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-7: Flag and correct the "+~1.2 km top magnet" tape note as invalid analogue
- **Category:** factual-concern
- **Severity:** minor
- **Location:** analysis.md §Section 5 parameter table, "REBCO tape requirement (A)" notes column
- **Finding:** The "+~1.2 km top magnet" figure is drawn from the Junior prototype top magnet (arxiv-2508-17691 Table 2). The power plant top magnet tape is explicitly out of scope in Simpson et al. The Junior top magnet operates at ~700 A; the power plant core magnet operates at ~29.4 kA (42× higher current). The power plant top magnet tape would be substantially larger — likely tens of km, not 1.2 km.
- **Proposed Fix:** Replace "+~1.2 km top magnet" in the notes column with "+top magnet tape [unknown; out of scope in Simpson et al.; Junior top magnet analogue (1.2 km) is invalid at power plant scale due to 42× current difference — treat as unknown and not included in the total]."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

### PA-8: Document the ~8 MW auxiliary load gap vs. Table 9 in the analysis
- **Category:** improvement
- **Severity:** minor
- **Location:** analysis.md §Section 5 parameter table, "Recirculating power fraction" row; model_setup.py _compute_power()
- **Finding:** Table 9 implies total recirculating = 296 − 208 = 88 MW. Of that, 63.6 MW (ICRH) + 1.31 MW (cryo) = 64.9 MW is explicitly published. The remaining ~23 MW is not itemized in the source. The model budgets 15 MW for non-ICRH auxiliary loads, giving p_net ≈ 212 MW vs. published 208 MW (+2%). The ~8 MW gap is within first-pass tolerance but the discrepancy source is undocumented.
- **Proposed Fix:** Add a note to the Section 5 "Recirculating power fraction" row: "Table 9 implies ~23 MW of unitemized auxiliary loads beyond ICRH (63.6 MW) and cryo (1.31 MW); model assumes ~15 MW for these loads, yielding p_net ≈ 212 MW vs. published 208 MW (+2%)." This documents the gap without overstating its significance.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

---

## Summary

- **Total citations checked:** 15
- **Citations fully verified:** 10
- **Citations with section/table attribution errors:** 2 (CV-1: §Discussion → §3.3; CV-8: §Table 7 → §Table 5)
- **Citations with content issues:** 2 (CV-5: composite misquotation; CV-9: unsourced/invalid analogue)
- **Citations partial match:** 1 (CV-12: "14.1 kW" subtotal not explicit in Table 9)
- **Calculations checked:** 10
- **Calculations matched:** 8
- **Calculations with errors:** 2 (CALC-4: "5×" should be "7×"; CALC-9: unit error "1.13 kW" → "1.13 MW" in annotation)
- **Internal inconsistencies:** 1 (CALC-5: 30-year Section 4 narrative vs. 40-year model)
- **Model parameters audited:** 18
- **Parameters fully traced:** 15
- **Parameters traced via analogue (no primary source):** 3 (MSA-8: HTS coil cost; MSA-9: ICRH cost; MSA-12: sacrificial coil material cost)
- **Parameters with traceability concerns:** 1 (MSA-15: vessel_inner_radius is a rough approximation, flagged appropriately)
- **Proposed Actions:** 8 (blocking: 0, important: 2, minor: 6)
- **Overall:** HAS ISSUES — no blocking errors; no findings that invalidate the LCOE model or misrepresent primary sources. The two important issues (PA-3: incorrect 5× multiplier; PA-4: 30-year/40-year inconsistency) should be corrected before synthesis. The critical data gaps (no published capital cost, no sacrificial coil cost, no thermal cycle specification) are correctly identified and propagated as HIGH UNCERTAINTY parameters. The model's calibration approach (η_th = 0.38 back-solved from published power balance) is well-reasoned.
