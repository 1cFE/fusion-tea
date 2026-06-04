# 1costingfe Model Update: Compact Liquid-Wall HTS Stellarator

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: ISS04 confinement scaling coefficients enable plasma design point closure
- **Target:** Section 6 (Gap #7) and model_setup.py
- **Category:** model
- **Finding:** The analysis correctly identifies ISS04 as the right confinement scaling to use for plasma parameter estimation (Gap #7) but does not include the formula. The UKAEA PROCESS source provides the full ISS04 expression with all fitted coefficients:

  τ_E = 0.134 · R₀^0.64 · a_p^2.28 · n̄₂₀^0.54 · B₀^0.84 · P^-0.61 · ī^0.41

  where ī is the rotational transform (≡ 1/q). This is the currently recommended scaling in PROCESS for stellarator studies. With R₀ ≤ 4 m, a_p ≈ 1 m, B₀ = 10 T, and a target rotational transform of ī ≈ 0.25–0.5 (typical QI stellarators), this formula can close the Q=∞ design point and produce first-principle estimates for missing parameters: plasma density, confinement time, and by extension the achievable Lawson product. The analysis currently treats these as unresolvable from available sources, but they are derivable from the ISS04 formula applied to the published machine geometry. Four alternative scalings (LHD, gyro-reduced Bohm, Lackner-Gottardi, ISS95) are also available for bounding analysis.
- **Recommendation:** Add the ISS04 formula to model_setup.py as the basis for estimating plasma confinement time, density design point, and Lawson criterion closure. Run the design point calculation with the published geometry (R₀ = 4 m, a_p ≈ 1 m, B₀ = 10 T) across a range of rotational transform values and check Q=∞ feasibility. Use the four alternative scalings as a sensitivity envelope. Cite the UKAEA PROCESS stellarator documentation as the source. Update Gap #7 in Section 6 from "not-yet-sourced" to a derived estimate with stated uncertainty.
- **Priority:** important

### F-2: Beta = 5% hard limit and Sudo density limit define the plasma operating envelope — not discussed in analysis
- **Target:** Section 2 (Challenge #3: Ignited stellarator plasma) and Section 5 (Missing Parameters)
- **Category:** analysis
- **Finding:** The analysis discusses the ignited stellarator plasma risk (Challenge #3) in terms of the gap to W7-X and the lack of stellarator burning-plasma precedent, but does not state the physical constraints that define the feasible operating space. The UKAEA PROCESS source establishes two binding constraints for stellarators:

  1. **Beta limit: β ≤ 5%**, based on 3-D MHD stability calculations for stellarators (hard constraint in PROCESS). This directly bounds the plasma pressure achievable at a given field and density.
  2. **Sudo density limit**: n_max = 0.25(PB₀ / R₀a_p²)^0.5 (in units of 10²⁰ m⁻³). This radiation-based limit applies to stellarators and is noted as having "unclear extrapolation to reactor parameters" at high power.

  Neither constraint is mentioned in the analysis. For the Renaissance Fusion design point (B₀ = 10 T, R₀ ≈ 4 m, a_p ≈ 1 m), the beta limit directly constrains whether Q = ∞ is achievable at the stated field: a compact stellarator at high field and high β approaches this 5% ceiling. The Sudo limit constrains the maximum plasma density, which feeds back into the Lawson criterion. The analysis also identifies ECRH-critical-density as not applicable (NNBI heating), but the Sudo limit still applies regardless of heating method.
- **Recommendation:** Add a paragraph to Section 2, Challenge #3 (Ignited Stellarator Plasma) stating: the stellarator beta limit of 5% (3-D MHD) and the Sudo density limit (n_max ∝ (PB₀/R₀a_p²)^0.5) define the feasible plasma operating space and should be evaluated at the Renaissance Fusion design point as part of the Q=∞ feasibility check. State whether the published design point operates comfortably within these limits or approaches them. Add both constraints to the Section 5 Missing Parameters table with gap type "derivable" — they can be evaluated from published machine geometry using established stellarator physics.
- **Priority:** important

### F-3: PROCESS reference pumping power (200 MW conventional) anchors the unexplained recirculating power gap
- **Target:** Section 2 (Challenge #5: Net efficiency gap) and Section 6 (Gap #3)
- **Category:** analysis
- **Finding:** The analysis correctly identifies the 32% recirculating power gap (cycle efficiency 50% vs. net efficiency 34%) as unexplained, noting that liquid metal circulation pump power is the likely dominant contributor (Gap #3). The UKAEA PROCESS stellarator model parametrizes conventional solid-blanket cooling at: blanket coolant pump 120 MW, first-wall coolant pump 56 MW, divertor coolant pump 24 MW — totaling 200 MW of mechanical pumping power for a stellarator of comparable scale using a conventional solid blanket. This provides a quantitative lower bound: if conventional solid-blanket cooling for this machine class requires ~200 MW mechanical power (before electrical conversion losses in pumping drives), then the Renaissance Fusion liquid metal wall at 25 MW/m² wall loading — more than 5× the wall loading of typical solid blanket designs — would plausibly require substantially higher pumping power. At ~1.47 GWe gross output (inferred), 200 MW is already ~14% recirculating fraction; the elevated liquid metal pumping could account for a significant part of the unexplained 16-percentage-point gap (from 14% conventional to 32% observed).
- **Recommendation:** Add the PROCESS 200 MW reference number to the Section 2, Challenge #5 paragraph and to Gap #3 in Section 6. Frame it as: conventional solid-blanket cooling for a stellarator of this class costs ~200 MW; the Renaissance Fusion liquid metal system at 25 MW/m² is expected to exceed this, and the excess is a major contributor to the unexplained 32% recirculating fraction. Use this as the lower bound when deriving the first-principles pump power estimate recommended in Gap #3. Cite the UKAEA PROCESS stellarator documentation as the source for the 200 MW reference.
- **Priority:** minor

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Key differentiators from conventional tokamak not explicitly listed
- **Target:** Section 7 (Cross-Concept Notes) or a dedicated framing subsection
- **Category:** analysis
- **Finding:** The checklist requires key differentiators from a conventional tokamak to be explicitly listed, not merely implied in the narrative. The analysis discusses differentiators dispersed across Sections 2, 3, and 7 but never enumerates them as a structured list. A TEA pipeline auditor checking Goal 2 coverage cannot confirm completeness without hunting through the full text. The concept has a rich, clearly understood differentiator set — no current drive/CS required, no disruptions, 3D non-planar coil geometry, flowing liquid metal wall (vs. solid PFC), laser-patterned HTS film (vs. wound tape), sCO₂ Brayton-Rankine (vs. steam Rankine), ignited Q=∞ target (vs. externally heated burning plasma), startup-only NNBI (vs. continuous heating system) — that would benefit from explicit enumeration against a conventional tokamak baseline. Section 7 focuses on comparison with peer stellarators; the conventional tokamak baseline comparison required by Goal 2 is absent as an explicit list.
- **Recommendation:** Add a short bulleted list of 6–8 key differentiators from a conventional tokamak (e.g., SPARC/CFS class) at the top of Section 7 or as a dedicated sub-section. For each differentiator, tag it as: novel (unique to Renaissance Fusion), borrowed (shared with all stellarators), or shared (D-T fusion universal). This list anchors the CAS-level cost implication mapping already performed later in Section 7 and makes Goal 2 coverage explicit and auditable.
- **Priority:** important

### F-2: b_max sensitivity absent from key sensitivity discussion despite being 4th-largest engineering lever
- **Target:** Section 2 (top LCOE sensitivity parameters) and model sensitivity sweep
- **Category:** model
- **Finding:** The model sensitivity output shows b_max (peak coil field) at elasticity +0.38 — the 4th largest engineering lever after availability (0.94), r_coil (0.77), and construction_time (0.54). The analysis explicitly lists "top LCOE sensitivity parameters" at the end of Section 2 and stops at three, omitting b_max entirely. This is a meaningful gap: Section 3 extensively discusses the 15–40 T peak coil field range as a key technical uncertainty (REBCO Jc degrades sharply above ~20 T at 20 K), yet the analysis never connects this physics/TRL risk to its LCOE sensitivity magnitude. The b_max lever is distinct from r_coil: r_coil captures manufacturing cost uncertainty (how much does the film process cost per unit), while b_max captures physics-driven field requirement uncertainty (how large must the coil cross-section be to achieve the required field given the Jc limit). Both are real uncertainties and should be swept independently.
- **Recommendation:** Add b_max to the top-sensitivity list at the end of Section 2 as the 4th engineering lever (elasticity +0.38), with a note explaining the mechanism: peak field drives coil cross-section at a fixed Jc, directly scaling C220103. Extend the model to include a b_max scenario sweep over the published 15–40 T design envelope to characterize the LCOE range attributable to peak field uncertainty, independent of the r_coil scenario branches already implemented. This connects the Section 3 REBCO Jc risk narrative to a quantified LCOE sensitivity.
- **Priority:** important

### F-3: Net efficiency gap labeled "Impact: High" inconsistent with pump power's actual LCOE elasticity
- **Target:** Section 2, Challenge 5 impact label
- **Category:** analysis
- **Finding:** Section 2 states that challenges are "ranked by LCOE impact." Challenge 5 (net efficiency gap / unexplained recirculating power) is labeled "Impact: High" — the same tier as ignited stellarator plasma (Challenge 3) and liquid metal wall (Challenge 4). However, the model sensitivity shows p_pump elasticity of only +0.058, meaning a ±50% error in pump power estimate (the stated model uncertainty) changes LCOE by only ~3%. This is an order of magnitude below r_coil (0.76) and substantially below construction_time (0.54). The pump power gap is a genuine physics transparency issue, but it is not a first-order LCOE lever. Labeling it "High" overstates its economic significance relative to the coil cost and availability findings, and may cause downstream analysts to over-invest in characterizing recirculating power vs. the dominant uncertainties.
- **Recommendation:** Revise the impact label for Challenge 5 from "High" to "Moderate." Add a one-sentence note citing the model result: the pump power uncertainty (±50%) contributes ~3% LCOE sensitivity, compared to ~77% for coil cost multiplier uncertainty. Retain the full discussion of why the gap is important for physics transparency (closing the engineering Q budget, verifying the 34% net efficiency claim), but distinguish between "important to understand" and "high LCOE impact."
- **Priority:** minor

---

<!-- Prior pass findings (iter-1 → iter-2 source integration) — addressed in iter-2 analysis -->

### F-1: TBR = 1.60 is explicitly stated in JNM 599 — blocking gap is resolved
- **Target:** Section 1 (Data Availability), Section 5 (Parameter Table), Section 6 (Gap Inventory)
- **Category:** analysis
- **Finding:** The analysis treats the tritium breeding ratio as an unresolved blocking gap (Section 6, Gap #4: "TBR not directly confirmed in available documents"; Section 5 missing parameters table: "truly-unknown, blocking"). The full JNM 599 (2024) 155239 paper explicitly reports TBR = 1.60 for the optimized Pb (10 cm) + Li-LiH (22 cm) configuration. This directly resolves the gap the analysis flags — the claim that "fm ≠ TBR and TBR is unconfirmed" is no longer accurate once the full paper is read. The recommendation in Gap #4 ("Read JNM 599 directly — TBR may be stated explicitly") turns out to be correct; the paper does state it.
- **Recommendation:** In Section 5, move TBR from the Missing Parameters table to the Available Parameters table with value 1.60, source JNM 599 (2024) 155239, confidence high. In Section 6, close Gap #4 and reduce its criticality to resolved. In Section 1, update the data availability narrative to note that TBR = 1.60 is confirmed and the fm/TBR confusion noted in the original dossier is now resolved. Add the design requirement context: TBR ≥ 1.15 was the design requirement; TBR = 1.60 provides a margin of ~35% above threshold, intended to cover port coverage losses and fuel cycle inefficiencies in the 3D geometry.
- **Priority:** blocking

### F-2: Analysis incorrectly asserts Li-6 enrichment is likely required
- **Target:** Section 4 (Materials and Supply Chain), Section 6 (Gap Inventory, Gap #10)
- **Category:** analysis
- **Finding:** Section 4 states: "Achieving TBR > 1 with the Li-LiH blanket geometry likely requires moderate-to-significant Li-6 enrichment." Section 6 Gap #10 lists Li-6 enrichment requirement as an "important" derivable gap. The JNM paper shows the baseline optimized design uses non-enriched natural Li-LiH and achieves TBR = 1.60 — well above the 1.15 minimum. Enrichment to 90% Li-6 is explored in the paper as an option that reduces required breeding layer thickness (from 18 cm to 16 cm), but it is presented as an optional trade-off with higher cost, not a requirement. The assertion in Section 4 that enrichment is "likely required" is directly contradicted by the source paper and affects the supply chain risk framing (Li-6 enrichment supply constraints are incorrectly elevated in the analysis narrative).
- **Recommendation:** Revise Section 4 to state that the baseline design uses non-enriched natural Li-LiH and meets TBR requirements without enrichment. Reframe the Li-6 enrichment discussion as an optional trade-off (reduces blanket thickness by ~2 cm, enables a modest cost reduction, at higher enrichment cost) rather than a likely requirement. In Section 6, downgrade Gap #10 from "important" to "nice-to-have" and add a note that the JNM baseline design achieves TBR = 1.60 without enrichment; enrichment is a cost optimization lever, not a physics necessity.
- **Priority:** important

### F-3: fm = 1.24 labeling is ambiguous — conflicts with blanket energy multiplication factor of 1.07
- **Target:** Section 5 (Parameter Table), Section 1 (Data Availability)
- **Category:** analysis
- **Finding:** The analysis lists "Neutron energy multiplication factor (fm) = 1.24" in the Section 5 parameter table, citing JNM 599 (2024) 155239. The full JNM paper reports the blanket energy multiplication factor as 1.07 (ratio of total energy deposited in blanket to incident neutron energy; meets the design requirement of ≥1.0). The 1.24 figure cited in the analysis appears to be the Pb-layer-specific neutron number multiplication (secondary neutrons produced per primary neutron via (n,2n) reactions in Pb), which is a distinct quantity from the blanket energy multiplication factor. The label "neutron energy multiplication factor" conflates these two different metrics. Using 1.24 where the blanket energy multiplication is 1.07 will create confusion in downstream TEA work — particularly in estimating total thermal power available from the blanket relative to the 2 GW fusion power output.
- **Recommendation:** In Section 5, split the parameter into two rows: (a) Blanket energy multiplication factor = 1.07 (ratio of total blanket thermal power to incident fusion neutron power; per JNM 599), and (b) Pb pebble neutron multiplication (n,2n contribution) = 1.24 if this value appears in the JNM paper, with a clarifying note that these are distinct quantities. Verify the 1.24 value against the source — if it is not present in the full JNM paper, remove it and note the original dossier may have conflated the two metrics. Also update Section 1 to note that the confirmed blanket energy multiplication factor is 1.07.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Section 2 does not identify the top LCOE-sensitive parameters, and the narrative priority conflicts with the model
- **Target:** Section 2 (challenge ranking) and Section 7 (cross-concept notes, "most significant LCOE lever")
- **Category:** analysis
- **Finding:** The checklist requires Section 2 to name the 2–3 parameters with highest LCOE sensitivity for this concept (Goal 4). The analysis ranks challenges by qualitative "LCOE impact" labels (Critical/High/Moderate) but never states which specific parameters dominate the LCOE sensitivity. The model output makes this concrete: `availability` (elasticity −0.94), `r_coil` (+0.77), and `construction_time` (+0.54) are the three largest engineering levers — not thermal efficiency. Yet Section 7 describes the sCO₂ 15-point efficiency premium as "the concept's most significant LCOE lever on the cost side," and `eta_th` carries elasticity of only 0.11 in the model. Availability is treated as a one-line footnote in Section 2 despite being the top engineering sensitivity driver.
- **Recommendation:** Add a short paragraph at the end of Section 2 that names the 3 highest-LCOE-sensitivity parameters by name and quantifies their elasticity from the model: availability (~−0.9), coil cost multiplier/r_coil (~+0.8), and construction time (~+0.5). Correct the Section 7 framing — the sCO₂ efficiency premium is a favorable architectural feature, but it is not the dominant LCOE lever; coil cost uncertainty and availability dominate. State that coil cost uncertainty and plant availability are the parameters the cost model should be designed to test.
- **Priority:** blocking

### F-2: Modeling approach (1costingfe vs. free-form) is never stated
- **Target:** Section 7 (cost model architecture recommendation)
- **Category:** analysis
- **Finding:** The analysis checklist requires the analysis to state whether 1costingfe or free-form modeling is appropriate and why (Goal 4). Section 7 correctly identifies that the Renaissance Fusion concept "requires an independent cost model that cannot be derived by adapting any existing tokamak or stellarator template," listing four CAS accounts that need novel treatment (magnet, first wall, heating, power conversion). But the analysis stops short of explicitly answering the modeling approach question — 1costingfe (adapted with overrides) or a free-form model built from scratch? This ambiguity leaves the pipeline without actionable modeling guidance.
- **Recommendation:** Add a one-paragraph statement in Section 7 that explicitly answers: "This concept should be modeled using [1costingfe with coil/blanket overrides / free-form]." Given the unique architecture (laser-patterned magnets with no tape-winding analogue, liquid-metal first wall replacing a distinct CAS sub-account structure, startup-only heating, sCO₂ rather than steam Rankine), the recommendation should likely be 1costingfe with explicit scenario branches for the two highest-uncertainty accounts (C220103 coil cost, C220101 liquid metal wall cost), rather than full free-form — but this decision should be stated and justified.
- **Priority:** blocking

### F-3: Coil cost stub does not quantify the LCOE uncertainty band it introduces
- **Target:** Model (C220103, r_coil sensitivity) and Section 2 / Section 6 gap inventory
- **Category:** model
- **Finding:** The model computes C220103 (coil cost) = $2.26B using a tape-winding framework that is explicitly flagged as inapplicable ([UNCERTAIN x3-10]). The analysis correctly identifies that the laser-patterned film has no manufacturing cost analogue, but neither the analysis nor the model quantifies what the 3–10× uncertainty range means for LCOE. With `r_coil` elasticity of +0.77, a 10× variation in coil cost corresponds to roughly a +660% shift in the coil-cost contribution to LCOE — the largest single structural uncertainty in the model. Using a single stub value (even flagged) obscures this and does not allow the pipeline to test the concept's key hypothesis. The current output presents a false-precision LCOE of 128 $/MWh for a concept whose dominant cost account is a placeholder.
- **Recommendation:** Replace the single C220103 computation with a three-scenario coil cost branch: (low) 0.3× the tape-winding analogue, (mid) 1× (current), (high) 10×. Report the LCOE range across scenarios rather than a single number. Add a note in Section 6 (gap #2) that quantifies the LCOE swing from the coil cost uncertainty: "If coil cost is 10× the tape-winding analogue, LCOE increases by approximately X $/MWh; if 0.3×, it decreases by Y $/MWh." This makes the key modeling uncertainty tractable for the TEA pipeline.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-3/model_setup.py`
