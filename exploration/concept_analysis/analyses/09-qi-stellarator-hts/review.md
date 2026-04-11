# Review: QI Stellarator - HTS

**Iteration:** 1
**Date:** 2026-04-06
**Files reviewed:** analysis.md, model_setup.py, model_output.txt
**Source documents:** 11 files

---

## Strategic Assessment

### 1. Modeling Approach

The modeling approach is structurally sound and notably conservative in the right direction. The decision to flag C220103 (3D non-planar HTS coils) as an explicit lower bound — and then to sweep the multiplier from 1.0× to 5.0× rather than picking a point estimate — is the correct response to a genuinely unbounded uncertainty. The coil cost is not just an important unknown; it is the number that determines whether Stellaris is competitive at all, and treating it as a range is more honest than most analyses at this TRL.

The H4 hypothesis branch (ignited vs. sustained ECRH) is also well-structured. Carrying both Scenario A ($110.8/MWh replacement-inclusive) and Scenario B ($114.7/MWh) as co-equal outputs correctly refuses to bet on an unvalidated physics outcome. The $3.9/MWh gap between them is informative: the H&CD advantage of ignition is real but not the dominant factor — which means the coil premium is still the make-or-break variable regardless of which branch materializes.

The H2a scenario (CIEMAT-QI4X 4% beta) is appropriately scoped as a forward-state physics branch, not a Stellaris v1 variant. This matters for how TEA readers should interpret it. The label "Higher-Beta QI (4% Beta, R0 ≈ 11.6 m, Smaller Machine)" is adequate but could be lost in a cross-concept comparison table where only scenario names appear. The risk is that H2a gets treated as a Stellaris range rather than a different design family.

The replacement-inclusive LCOE being surfaced as the primary comparison figure (iter-6 update) is the right call. The magnet replacement liability ($4.5–$22/MWh depending on multiplier) is a structural cost element not shared by any tokamak reference, and demoting it to a footnote would have artificially flattered the headline number.

CAS mapping choices are defensible. The decision to track coils at C220103 within CAS22 (rather than CAS21) follows ARIES convention and is internally consistent. The geometry derivation — plasma volume from power density, then R0 from assumed aspect ratio R0/a ≈ 10 — is the right approach given that major radius is not published, and the ±10% uncertainty is explicitly noted.

One structural modeling concern: the ARIES-CS reference is used to calibrate the stellarator cost baseline, but ARIES-CS studied quasi-axisymmetric (QA) configurations while Stellaris is quasi-isodynamic (QI). The analysis acknowledges this in Section 1 ("carries an additional structural assumption that QA and QI stellarators of similar size and field strength have comparable cost structures, which may not hold, particularly in the CAS21 coil account where different magnetic symmetry classes imply different coil topologies") — but this caveat does not propagate forward into the CAS-level delta table or the model assumptions list. A reader looking only at the model output and assumptions would not know the baseline calibration carries a structural topology mismatch.

### 2. Strategic Positioning

The concept is correctly positioned as a near-term commercial stellarator competitor to HTS compact tokamaks, not a long-shot or exotic concept. The framing — "harder to design, easier to operate" — captures the core trade correctly, and the analysis doesn't overstate the disruption-free advantage (it treats it as a capacity factor input, not a physics trump card).

The Helios analogue choice is well-justified. Helios (Thea Energy) is the closest public comparator in optimization class, fuel type, and commercial intent, and the analogue use is transparent throughout: capacity factor (88%), thermal efficiency (40%), and ignited ECRH (1 MW) are all borrowed from Helios and labeled as such. The scale mismatch (Helios 390 MWe vs. Stellaris 1,000 MWe) is noted but not resolved — scaling from a 390 MWe design to a 1,000 MWe plant is not trivial, and the thermal efficiency assumption in particular (using Helios's 40% as the high-end while modeling 38% for Stellaris) may underestimate efficiency improvement possible at larger scale.

The W7-X heritage connection is used appropriately: as a validation basis for the island divertor and QI physics, not as a cost reference (W7-X was not a power plant study).

Comparison with the HTS compact tokamak reference is present in §7 as a CAS-level delta table, which is the right framing given that neither analysis has a finalized approved LCOE yet. The delta table is qualitative (direction + magnitude category), not numerical, which is appropriate for this stage. A side-by-side numerical comparison is premature until the tokamak reference is approved.

Type One Energy is correctly categorized as an HTS stellarator with less public data, and the decision not to benchmark against it is appropriate — there is no published plant study.

### 3. Risk and Uncertainty Framing

Risk framing is the strongest dimension of this analysis. Three blocking uncertainties are correctly identified and kept visible throughout: coil manufacturing cost (C220103 lower bound), alpha confinement under burning plasma conditions (H4 validation gap), and machine geometry (R0 unpublished). All three are explicitly labeled as blocking gaps in §6.

The magnet replacement risk is handled with unusual rigor: the analysis derives a lifecycle cost contribution ($4.5–$22/MWh), models it separately from initial-build LCOE, and designates the replacement-inclusive figure as the primary output. This is the right treatment for a non-standard O&M liability that no tokamak reference carries.

The TBR margin assessment (1.074 post-correction, 70% Li-6 enrichment required) is honest about margin adequacy: "close to the typical minimum engineering requirement." The acknowledgment that stellarator geometry creates more blanket penetrations than a tokamak is a physically grounded concern, not boilerplate.

The capacity factor assumption (88%, from Helios analogue) is the risk that receives the least quantified treatment given its importance. The sensitivity analysis shows availability elasticity of −0.89 — the strongest single engineering lever in the model — and the published range (85–95%) is stated in §5. But the analysis never applies that range to produce an LCOE bound: at 85% availability (the low end), the LCOE impact is approximately +4% relative to the 88% base case, which would add ~$4–5/MWh to Scenario A. This is comparable to the H4 branching effect ($3.9/MWh) and should be visible in the output, not only derivable by a reader who multiplies elasticity by the range width. The Proxima unpublished capacity factor target is correctly listed as a gap, but the downstream LCOE consequence of the range uncertainty should be surfaced explicitly.

Economic and supply chain risks are adequately covered: REBCO tape demand, Li-6 enrichment supply chain, and construction time premium for 3D coil fabrication are all noted. Regulatory risk is thin — the analysis mentions the Alpha demo and Stellaris roadmap but does not address first-of-kind regulatory pathways for a stellarator in Germany, which will differ from tokamak licensing precedents.

TRL assessment: The analysis does not include an explicit TRL rating, but the implicit placement (burning plasma unvalidated, Alpha demo ~2031, commercial plant 2030s) is consistent with TRL 3–4 for the integrated system. The framing is appropriate.

### 4. Data Sufficiency

Data sufficiency is the weakest dimension, but the analysis is honest about it. The five blocking gaps in §6 are correctly identified as blocking (capital cost, major radius, coil manufacturing cost) or important (thermal efficiency, capacity factor target). The analysis does not overreach: it uses analogues transparently, labels lower bounds as lower bounds, and structures the model to show consequences of the uncertainty rather than hiding it in a point estimate.

The stellaris-design-details.md source (337 KB) is the primary engineering reference and provides more depth than most private fusion company publications. The fact that it is paywalled means the analysis is working from an extracted text of the full paper rather than a summary, which gives reasonable confidence in the parameter values cited.

The ARIES-CS sources are appropriately thin (3 KB each in extracted form) — these are abstract-level references used only to establish the historical stellarator cost baseline, not primary data sources for Stellaris parameters. The limitation is acknowledged.

The Helios comparison source (176 KB) is the most valuable gap-filling resource, and it is used correctly. The arXiv preprint status of Helios (December 2024) is a minor concern — the analysis treats it as authoritative before peer review is complete — but this is acceptable given the level of technical detail provided and the Proxima-adjacent authorship (Thea Energy/Max Planck provenance).

No critical gap should trigger an additional research iteration before proceeding. The blocking gaps (coil cost, major radius) are not resolvable from open sources — they require either the full paywalled paper, proprietary Proxima disclosure, or the 2027 SMC demo data. Sending stage1 back to research would not close them.

### 5. Cross-Concept Consistency

This is the first analysis reviewed, so cross-concept consistency cannot be fully evaluated against a prior baseline. The analysis positions Stellaris relative to HTS compact tokamaks and Helios in a way that is internally consistent and physically grounded. The framing — large coil premium partially offset by H&CD savings and capacity factor advantage — is the correct structure for this comparison.

The assumption set (88% capacity factor, 38% thermal efficiency, 8-year construction, NOAK financials at 7% discount rate) will serve as an implicit reference point for subsequent analyses. If other concepts use different financial assumptions, the comparison becomes inconsistent. The analysis does not explicitly state that it follows a common assumption protocol — this is a cross-analysis governance gap, not specific to this concept, but worth noting.

The coil replacement lifecycle treatment is concept-specific and not present in the tokamak reference. This is correct modeling (stellarators have this cost, tokamaks largely do not), but it means the LCOE comparison will require careful explanation: the stellarator replacement-inclusive LCOE is the right comparison figure, while the tokamak initial-build LCOE likely does not carry this term. If the comparison table shows both at initial-build LCOE, Stellaris will appear better than it is.

---

## Verdict

VERDICT: PROCEED

This analysis is strategically sound. The hypothesis-driven framework, explicit lower bounds on the dominant uncertainty (C220103 coil cost), conservative scenario branching (H4 true/false, multiplier sweep), and honest gap inventory demonstrate appropriate analytical rigor for a pre-Alpha concept. The data gaps are real but expected at this TRL, and the model is structured to show consequences of uncertainty rather than masking it. Minor fixes are noted below.

---

## Minor Fixes (PROCEED only)

### PA-1: Surface capacity factor LCOE range in model output
- **Category:** improvement
- **Severity:** minor
- **Location:** model_output.txt and model_setup.py (Scenario A output block)
- **Finding:** The sensitivity analysis shows availability elasticity of −0.89, and §5 states the published range is 85–95%. But the output never applies this range to show an LCOE bound. A reader must manually multiply elasticity × range width to get the ~±$4–5/MWh consequence. The H4 branching effect ($3.9/MWh) is shown explicitly; the capacity factor range effect (comparable magnitude) is not.
- **Proposed Fix:** Add a brief sensitivity row to the model output alongside the coil multiplier sweep: "Capacity Factor Range: 85% → $X/MWh | 88% → $110.8/MWh | 95% → $Y/MWh (replacement-inclusive, Scenario A, 1.0× coil)." Three numbers, not a full table.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: Propagate QA→QI cost structure assumption into model assumptions list
- **Category:** inconsistency
- **Severity:** minor
- **Location:** analysis.md §1 (last paragraph of ARIES-CS discussion) and model_setup.py (Key Assumptions, #11)
- **Finding:** The analysis correctly notes in §1 that ARIES-CS is a QA study and that the cost extrapolation to QI "carries an additional structural assumption that may not hold, particularly in the CAS21 coil account." But this caveat does not appear in the model_setup.py assumptions list or model_output.txt summary. A reader of the model artifacts alone would not know the ARIES baseline carries a topology mismatch.
- **Proposed Fix:** Add a 13th assumption to model_setup.py: "Framework calibration: ARIES-CS baseline (QA stellarator) applied to QI configuration — topology difference may affect C220103 coil account; direction of bias unknown."
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-3: Clarify H2a scenario scope in any summary or table header
- **Category:** improvement
- **Severity:** minor
- **Location:** model_output.txt (Scenario H2a header) and any downstream comparison tables
- **Finding:** Scenario H2a is correctly described in the body as "CIEMAT-QI4X 4% beta branch for next-generation QI designs, NOT a Stellaris v1 variant" in model_setup.py assumptions. But the scenario header in model_output.txt reads "Scenario H2a: Higher-Beta QI (4% Beta, R0 ≈ 11.6 m, Smaller Machine)" without the "not Stellaris v1" qualifier. In a cross-concept comparison table where only scenario labels appear, this could be read as a Stellaris design range.
- **Proposed Fix:** Append " [next-gen QI, not Stellaris v1]" to the H2a scenario header in model_output.txt.
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
