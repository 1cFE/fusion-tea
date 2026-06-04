# 1costingfe Model Update: Magnetized Target Inertial Fusion - MTIF (D-D)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Navy railgun cancellation absent from TRL and viability framing
- **Target:** Section 3 (Plasma-Armature Railgun Driver subsystem block)
- **Category:** analysis
- **Finding:** The analysis presents defense hypervelocity railgun programs (U.S. Navy, BAE Systems, General Atomics EML) as the primary technology analogue for NearStar's driver, and uses them to support the TRL 3-4 rating. The Wikipedia railgun source documents that the U.S. Navy canceled all railgun R&D in its 2021 budget after spending approximately $500M over 17 years, citing unresolved technical challenges including rail durability and rate-of-fire. This cancellation is the most authoritative external signal about whether even defense-scale railgun development — which has far less demanding duty-cycle requirements than commercial fusion (10 shots/minute vs. 1 Hz continuous, months of campaign vs. 30-year plant life) — can be brought to operational viability. The analysis does not mention the program cancellation, leaving the impression that the defense programs are ongoing proof-of-concept efforts rather than programs that have been terminated for the same reasons that threaten NearStar's concept.
- **Recommendation:** In the Section 3 "Plasma-Armature Railgun Driver" subsection, add a note that the U.S. Navy terminated railgun R&D funding in 2021 (~$500M, 17 years) after concluding that barrel durability and rate-of-fire targets could not be met. Frame this as the strongest available external signal on railgun maturity: the defense programs represent the best-resourced analogue effort, with much less demanding operational requirements than NearStar, and they did not achieve the engineering thresholds needed. Adjust the TRL framing accordingly — TRL 3-4 remains correct but the "on the path to higher TRL" implication should be removed given program termination.
- **Priority:** important

### F-2: Rail lifetime characterization is optimistic relative to documented evidence
- **Target:** Section 2 (Challenge 3: Railgun wear and replacement rate) and Section 3 (Plasma-Armature Railgun Driver, "On paper only" / "Missing at scale" bullets)
- **Category:** analysis
- **Finding:** Section 2 states that "Rail lifetimes in defense hypervelocity research programs are typically measured in hundreds to a few thousand shots at these velocities." The Wikipedia railgun source provides more specific and more pessimistic documentation: initial designs achieved only 12 full-power shots before requiring service; the Navy's most recent milestone as of 2014 was "over 400 shots" with the caveat that ONR would not confirm these were full-power shots; the Navy's stated development goal was 3,000 shots at 6 rounds/minute, which was never demonstrated before program cancellation. The analysis's "hundreds to a few thousand" characterization is on the optimistic end of the documented range and does not capture the contested nature of even the 400-shot milestone. The O&M note in Section 3 also uses 10^5 shots as the hypothetical floor for rail-replacement frequency ("if rails last 10^5 shots, replacement required every ~28 hours") — this is six to seven orders of magnitude above what defense programs actually achieved, making the already-alarming O&M calculation conservative in the wrong direction.
- **Recommendation:** Update Section 2, Challenge 3 to replace "hundreds to a few thousand shots" with a more precise characterization: documented defense program rail life ranges from ~12 shots (early systems) to a contested ~400 shots at unconfirmed full power, with a development target of 3,000 shots that was not achieved before program cancellation. Update the O&M note in Section 3 to replace 10^5 with 400 as the "historically optimistic" upper bound from documented defense programs — this makes the replacement cadence calculation (~2 hours instead of ~28 hours) far more alarming and better reflects actual evidence.
- **Priority:** important

### F-3: IFE capsule fabrication cost benchmarks absent from Section 5 gap discussion
- **Target:** Section 5 (Missing Parameters — capsule fabrication cost per shot row) and Section 6 (Gap 7)
- **Category:** analysis
- **Finding:** Section 5 identifies per-shot capsule fabrication cost as an important missing parameter, noting that "IFE target fabrication literature provides lower bound" without giving any numbers. The National Academies IFE Chapter 5 source provides concrete benchmarks: conventional ICF target fabrication currently costs thousands of dollars per target; power plant economics require a target cost of $0.25–$0.50 per shot; achieving this requires approximately a 10,000× reduction from current research-scale costs, and factory-model projections from the chemical batch-processing industry suggest 17–35 cents per target is achievable at mass-production scale. NearStar's capsule design (50 g, pre-magnetized, cryogenic fuel geometry, must survive Mach 30 launch) is substantially more complex than conventional ICF pellets, so these numbers are a lower bound rather than a direct estimate. At 28 million shots/year, even $0.50/capsule yields $14M/year in capsule cost — a non-trivial operating cost line that deserves quantitative context.
- **Recommendation:** Update the Section 5 "capsule fabrication cost per shot" row to cite the NAS IFE benchmark: ICF targets must reach $0.25–$0.50/shot for power plant viability (currently at ~$1,000+/target, requiring ~10,000× reduction). Note that NearStar's capsule is structurally more complex than ICF pellets (pre-magnetized, 50 g, must survive railgun launch), so $0.25–0.50 is a lower bound and NearStar's target will need to be substantially cheaper per-unit relative to its complexity. Update Section 6, Gap 7 similarly to replace the vague "IFE target fabrication literature provides lower bound" with the specific NAS figures.
- **Priority:** minor

---

## Source Notes

- **en-wiki-railgun.md**: Material. Provides specific rail lifetime data (12–400 shots documented), system efficiency anchor (~20% overall for naval planning), program history including Navy cancellation in 2021, and rate-of-fire achievements (5 Hz demonstrated at 185 g/shot in 1995, 0.167 Hz for heavy rounds). Directly relevant to Sections 2, 3, 5, 6.
- **iopscience-10-1088-1741-4326-ac2dbe.md**: Not usable. File contains only a CAPTCHA/access denial page — no scientific content was extracted. Cannot assess.
- **nationalacademies-read-18289-chapter-5.md**: Partially material. Contains no MTIF or magnetized target fusion content; exclusively covers conventional IFE (laser direct/indirect, heavy-ion, Z-pinch). Provides IFE economic benchmarks (5–10 ¢/kWh COE target, $0.25–$0.50/shot target fabrication goal, 70–80% capacity factor target) useful as comparative context but not as direct inputs to the NearStar analysis.

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Rail replacement O&M captured only as availability loss, not as an explicit cost
- **Target:** Model (CAS70 / O&M), cross-referenced to Section 2 (Challenge 3) and Section 5 (missing parameters table, "Rail lifetime and replacement cost — blocking")
- **Category:** model
- **Finding:** The analysis correctly identifies rail replacement as the dominant OPEX differentiator (Section 2.3: every ~28 hours at 10^5-shot rail life). The model's CAS70 shows only $25.2 M$/year O&M for 200 MWe — consistent with a generic fusion O&M scaling, not a concept where the primary consumable is replaced every day. The rail replacement penalty enters the model only through reduced availability (0.40), which reduces energy production; but the actual replacement labor, materials, and downtime cost appears to have no explicit cost line. At 1 Hz, even a modest rail unit cost creates a per-year replacement bill that would dominate O&M and should be a top-sensitivity parameter. Instead, `om_cost_dd` (elasticity +0.19) is the only O&M lever and it follows D-D generic scaling rather than a rail-replacement-specific formulation.
- **Recommendation:** Add a per-shot rail consumable cost parameter to the model (analogous to `target_factory_base` for capsule fabrication but representing rail erosion material and replacement labor). Run a sensitivity sweep over rail unit replacement cost and rail lifetime shots to produce a two-dimensional cost map. Update Section 2.3 with the implied O&M range from the sweep, stating the breakeven rail life (shots per replacement) at which O&M becomes economically tractable.
- **Priority:** blocking

### F-2: Driver capital cost calibrated for pneumatic pistons, not railgun
- **Target:** Model (CAS22 driver sub-account, `driver_mag_target_per_mw`), cross-referenced to Section 2 (Challenge 3) and Section 7 (comparison to General Fusion concept 14)
- **Category:** model
- **Finding:** The model output explicitly acknowledges this: "`driver_mag_target_per_mw` default ($3 M$/MW_driver, pneumatic piston calibration) — likely underestimates railgun capital." The railgun driver is the primary architectural differentiator from General Fusion's pneumatic approach and is the novel capital system in this concept. Using a pneumatic piston calibration understates a key cost penalty: plasma-armature railguns at 10 km/s operate far outside the regime of pneumatic actuators (different energy storage topology, pulsed-power infrastructure, high-current switching, precision firing circuits). Railgun capital costs in defense programs are measured in $10s–100s M$ per installation at much lower duty cycles than required here. The current calibration may underestimate driver CAS22 contribution by a factor of several.
- **Recommendation:** Add a railgun driver cost scenario branch with a multiplier range relative to the pneumatic piston baseline (e.g., 2×, 5×, 10× of `driver_mag_target_per_mw`). Anchor the lower bound using defense electromagnetic launcher program cost data (Navy/DARPA EML programs), which provide at least order-of-magnitude capital estimates for pulsed-power railgun systems. Report the LCOE sensitivity to this multiplier explicitly in the model output.
- **Priority:** important

### F-3: Highest-sensitivity parameters not stated as testable propositions with breakeven thresholds
- **Target:** Section 2 (Modeling Approach / Challenges) and the analysis's framing of key hypotheses
- **Category:** analysis
- **Finding:** The sensitivity analysis shows `availability` (elasticity −0.994) and `q_eng` (elasticity −0.334) as by far the dominant LCOE levers. The analysis narrative in Section 2 identifies the correct physical challenges (D-D ignition, energy balance, rail wear) but does not connect them to these parameters as breakeven conditions. There is no statement of the form: "At availability = 0.40, LCOE is ~190 $/MWh; a commercially viable LCOE (~50–80 $/MWh) requires availability ≥ 0.80, which requires rail lifetime ≥ N shots — approximately X orders of magnitude beyond the demonstrated defense program data." Without this framing, the analysis identifies risks but does not structure them as testable propositions that the cost model can evaluate.
- **Recommendation:** Add a paragraph in Section 2 (or a new modeling-recommendation sub-section) that (a) names availability and Q_eng as the two dominant LCOE levers from the sensitivity analysis, (b) states the breakeven availability and Q_eng values required for LCOE below a target threshold (e.g., 80 $/MWh), and (c) converts those breakeven values into physical requirements (rail shots per replacement, minimum fusion gain) that can be compared directly to the state of the art. This converts narrative challenges into testable modeling hypotheses.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mif_mag_target.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/iter-2/model_setup.py`
