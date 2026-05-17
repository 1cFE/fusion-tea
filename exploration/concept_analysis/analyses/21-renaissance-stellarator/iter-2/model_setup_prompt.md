# 1costingfe Model Update: Compact Liquid-Wall HTS Stellarator

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

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
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-2/model_setup.py`
