# Free-Form Model Update: Dense Plasma Focus (p-B11)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Enriched decaborane fuel cost now has a concrete anchor
- **Target:** Section 4 (Boron-11 isotopically enriched decaborane), Section 5 (Missing Parameters — Variable O&M enriched decaborane fuel cost), Section 6 (Gap #11)
- **Category:** analysis
- **Finding:** The analysis correctly flags enriched decaborane cost as "not-yet-sourced" in Sections 5 and 6. The LPPFusion p-B11 fuel source (lppfusion-proton-boron-p11b-fuel-arrives.md) provides a concrete 2019 procurement price: $600/gram for isotopically pure decaborane (99.9999% chemical purity, 99.9% B-11), with 93 grams purchased for hundreds of experimental shots. The source explicitly states commercial mass production would reduce the per-gram price "many hundred-fold" (implying ~$0.60–$6/gram at scale). This fills gap #11 and provides the per-shot fuel cost input needed for O&M sensitivity modeling.
- **Recommendation:** Update Section 4 to add the $600/gram reference cost under the B-11 decaborane paragraph. Move the enriched decaborane row in the Section 5 Missing Parameters table to the Available Parameters table with value "$600/gram (2019 lab procurement), ~$0.60–$6/gram projected at commercial scale" and confidence "low" (commercial projection unverified). Update gap #11 in Section 6 to reflect that a laboratory-scale anchor now exists and the remaining gap is commercial-scale pricing. Also update Section 2's O&M cost structure paragraph to note that fuel cost per shot is now estimable given a consumption rate of ~93g per hundreds of shots, pending commercial-scale pricing.
- **Priority:** important

### F-2: Geopolitical supply chain risk for enriched decaborane not captured
- **Target:** Section 4 (Boron-11 isotopically enriched decaborane), Section 7 (Cross-Concept Notes — Key divergence from all D-T concepts)
- **Category:** analysis
- **Finding:** Section 4 frames the B-11 supply challenge purely as isotopic purity at scale ("isotopic purity at scale is the bottleneck"). The LPPFusion fuel source reveals that 2019 procurement required two specialized overseas facilities: isotopic purification in Russia and decaborane compound synthesis in the Czech Republic, described as "hand-produced as custom laboratory items." This geographic concentration represents a geopolitical supply risk that is qualitatively distinct from total supply availability and is not currently mentioned in the analysis. This matters for Goal 5 (Risks and Assumptions) because supply chain concentration in adversarial or single-source geographies is a risk category the TEA should flag, particularly given the analysis already highlights the supply chain simplicity of p-B11 as a differentiator (Section 7).
- **Recommendation:** Add a sentence in Section 4 under B-11 decaborane noting that current isotopic enrichment relies on Russian and Czech suppliers (single-source for each process step), creating supply concentration risk at commercial scale. Add a corresponding entry in the Section 6 gap inventory noting that domestic or diversified isotopic enrichment supply has not been analyzed. In Section 7, qualify the "supply chain simplification" claim for p-B11 with a note that the isotopic enrichment step currently has geographic concentration risk absent from natural-boron supply chains.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Modeling approach (1costingfe vs. free-form) not stated
- **Target:** Section 2 (Modeling Recommendations)
- **Category:** analysis
- **Finding:** The analysis never states whether 1costingfe or free-form modeling is appropriate for this concept, nor explains why. This is a Goal 4 requirement. For a concept with no blanket, no turbine, no external magnets, and a novel dual-path DEC replacing the entire thermal cycle, the choice of free-form with zeroed CAS accounts is non-obvious and should be explicitly justified.
- **Recommendation:** Add a modeling approach statement (can be a short paragraph or a labeled field in Section 2 or a new modeling note section) stating: free-form modeling is appropriate because the DPF cost structure cannot be mapped to 1costingfe defaults — CAS22.01, CAS22.03, CAS22.04, and CAS23 are structurally zero, and the dominant capital item (DEC) has no library analogue. State which CAS accounts are zeroed and why.
- **Priority:** important

### F-2: Section 2 challenge ranking conflates physics difficulty with TEA leverage — DEC efficiency is the primary LCOE sensitivity parameter
- **Target:** Section 2 (Challenges) and Section 5 (LCOE-Relevant Parameters)
- **Category:** analysis
- **Finding:** Section 2 ranks challenges by physics difficulty: (1) yield gap, (2) QMF, (3) DEC, (4) rep-rate, (5) O&M. For TEA modeling purposes this ordering misframes the concept: DEC efficiency is the single highest-leverage parameter once the physics challenges are conditionally assumed to succeed. The model shows that η_dec < 0.65 drives net power negative (plant impossible), and there is NO thermal cycle fallback — underperformance of DEC eliminates the concept entirely. This is structurally different from, say, Q_sci uncertainty, which sets whether any LCOE exists; DEC efficiency determines the shape of the LCOE surface given that net energy is achieved. The analysis conflates these two distinct risk axes (feasibility vs. sensitivity) in a single ordering, which obscures the TEA modeling priority (Goal 4).
- **Recommendation:** In Section 2 or Section 5, add an explicit statement distinguishing two risk axes: (a) physics feasibility risks that determine whether any LCOE exists (yield gap, QMF — if these fail, LCOE is undefined), and (b) TEA sensitivity parameters that determine the LCOE value conditional on physics success (DEC efficiency, rep-rate, electrode cost). Flag DEC efficiency as the top-ranked TEA sensitivity parameter: the model's Q_sci sweep shows that even achieving net energy at Q ≈ 1.72 leaves 82% of gross electric recirculating back to the driver, making the net power balance extremely sensitive to DEC path losses. Add this recirculating fraction figure to the Section 5 parameter table as a derived quantity.
- **Priority:** important

### F-3: High recirculating power fraction (~82% at baseline) not surfaced as a DPF-unique structural constraint
- **Target:** Section 5 (LCOE-Relevant Parameters) and Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** At the baseline physics target (Q_sci = 1.72, just above breakeven of 1.41), the model computes 82% recirculating fraction — meaning only 18% of gross electric becomes net output per module. This is a DPF-specific structural characteristic not shared by any MFE, IFE, or MIF concept in the landscape: tokamaks and stellarators typically recirculate 10–25% of gross electric; mirror devices 15–30%; IFE concepts 20–35%. The DPF's high recirculating fraction arises because the driver (capacitor bank) must receive back nearly all the stored energy to sustain 200 Hz operation at 115 kJ/shot, leaving only the fusion surplus as net electric. This constraint means Q must substantially exceed breakeven (≥ 2.5 for viable ~57% recirculation at NOAK) — a non-obvious design requirement that is nowhere stated in the analysis. Section 7 claims the aneutronic fuel cycle eliminates "30–40% of a D-T tokamak's capital cost structure" but does not acknowledge that the high recirculating fraction imposes a compensating penalty: the plant must be grossly oversized relative to net output, driving high specific capital ($/kWe).
- **Recommendation:** Add recirculating fraction as a named parameter in Section 5 (derived value: gross electric minus driver recirculation, as a fraction of gross). Add a paragraph in Section 7 noting that while D-T blanket/tritium costs are eliminated, the DPF's 80%+ recirculating fraction at near-breakeven Q means the plant must produce ~5× the net electric output as gross fusion power, driving capital intensity in ways that partially offset the structural cost advantage. State the Q target needed for commercially viable recirculating fraction (roughly Q ≥ 2.5 for ≤ 60% recirculation).
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/iter-2/model_setup.py`
