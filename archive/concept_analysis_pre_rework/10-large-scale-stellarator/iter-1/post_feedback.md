VERDICT: FINDINGS

### F-1: FOAK-to-NOAK cost ratio not modeled as a sensitivity parameter
- **Target:** Model sensitivity sweep (model_setup.py / Section 2 Challenge #1)
- **Category:** model
- **Finding:** The analysis explicitly calls the FOAK-to-NOAK cost transition "the single most important modeling gap" and the key assumptions state "NOAK may be 40–60% of FOAK" — a factor-of-2 uncertainty range. Despite this, the model sensitivity sweep contains no parameter for a NOAK learning factor or FOAK-to-NOAK multiplier. The current model output ($11,461/kWe overnight, 148.6 $/MWh LCOE) represents a single point in this range with no quantification of the uncertainty band. The top engineering sensitivities are availability and construction time, both of which are secondary to capital cost uncertainty for a concept in this position.
- **Recommendation:** Add a `noak_fraction` parameter (range 0.40–0.70, representing NOAK as a fraction of FOAK) to the sensitivity sweep. The FOAK-implied capital cost ($16,000–20,000/kWe) should be the reference from which this parameter scales the model's overnight cost. This allows the analysis to answer whether the stellarator can reach competitive LCOE under plausible learning scenarios — the central TEA question for this concept.
- **Priority:** blocking

### F-2: Conventional large-scale tokamak absent as reference concept in Section 7
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 7 compares the large-scale stellarator only to the spherical tokamak (ST-E1). The conventional large-aspect-ratio tokamak (e.g., DEMO or ARIES-AT class) is mentioned throughout the body of the analysis but never appears as a structured comparison point. For a D1+ analysis of a large-scale MFE stellarator, the conventional tokamak is the primary reference from which differentiators should be measured — not the spherical tokamak, which is itself a non-mainstream variant. As written, the nearest-neighbor framing is incomplete: only one of the required 2-3 comparison concepts is present, and it is not the most natural reference.
- **Recommendation:** Add a comparison block for a conventional large-scale tokamak (DEMO or ARIES-AT class) as the primary reference concept in Section 7. Structure it the same way as the ST-E1 comparison: shared elements, key divergences, and TEA implications. The 5 divergences already identified in the narrative (steady-state, no current drive, blanket geometry, machine scale, disruption-free) should be reorganized as differentiators from the conventional tokamak first, with the ST-E1 comparison serving as a secondary near-neighbor. Identify the 2-3 nearest neighbors by name in the section header.
- **Priority:** important

### F-3: Key uncertainties not stated as testable hypotheses
- **Target:** Section 2 (Challenges) and cross-reference to Section 5 parameters
- **Category:** analysis
- **Finding:** Section 2 identifies challenges with LCOE impact ratings but frames them as narrative descriptions rather than testable propositions. The checklist requires hypotheses the cost model should test. Three critical uncertainties identified in Section 2 — blanket type (HCPB vs. DCLL causes ~20–25% LCOE swing), FOAK-to-NOAK learning, and the steady-state capacity factor advantage — are each stated as open gaps but none is converted into a falsifiable modeling proposition with a stated decision boundary. Without this, the model's sensitivity sweep and the analysis's framing are not connected: the reader cannot tell which model outputs would confirm or challenge the analysis's conclusions.
- **Recommendation:** Add a "Key Hypotheses" subsection at the end of Section 2 (or at the start of Section 5) with 3–4 propositions in the form: "H1: If NOAK capital cost reaches X% of FOAK, LCOE falls below competitive threshold (≤ $100/MWh). H2: HCPB vs. DCLL blanket choice shifts LCOE by ~20–25% via thermal efficiency. H3: Steady-state operation at ≥85% availability reduces LCOE by ~15% relative to an equivalent pulsed tokamak at 75%." Each hypothesis should map to at least one parameter in the Section 5 table and one sensitivity parameter in the model. This also satisfies the checklist requirement for Section 2 to identify the 2–3 parameters with highest LCOE sensitivity for this concept.
- **Priority:** important
