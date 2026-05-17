# 1costingfe Model Update: Laser ICF - Fast Ignition (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Rep rate sweep is flat — H3 cannot be tested by the current model
- **Target:** Section 2 (Modeling Approach, Hypothesis H3) and model repetition rate sweep
- **Category:** model
- **Finding:** The model's repetition rate sweep produces only ~0.4 $/MWh variation across 5–25 Hz (67.8 → 67.4 $/MWh, <0.6%), but the analysis asserts H3: "10 Hz is a sub-optimal rep rate for COE minimization; the 10 Hz constraint imposes approximately +4% COE penalty." The model's f_rep elasticity is -0.0040, confirming 1costingfe treats rep rate as nearly inconsequential to LCOE. The Meier 2006 result (+4% at 10 Hz, +16% at 5 Hz relative to the 20–25 Hz optimum) arises from rep-rate-dependent cost amortization — specifically, per-shot driver capital and optics maintenance costs spread over more shots at higher rep rate. The 1costingfe framework does not capture this structure. H3 as written cannot be tested.
- **Recommendation:** Either (a) implement a rep-rate-dependent capital amortization overlay in model_setup.py so that increasing f_rep reduces effective per-shot driver capital, allowing the Meier +4%/+16% penalties to emerge at lower rep rates; or (b) remove H3 from the testable hypotheses list and add a note explaining that 1costingfe does not capture rep-rate-dependent cost amortization, that this effect requires a Meier-class systems model, and cite the Meier 2006 result as an external constraint rather than a model output. Do not leave H3 as a stated testable hypothesis when the model demonstrably cannot evaluate it.
- **Priority:** important

### F-2: 17a-laser-icf-hybrid-drive absent from nearest-neighbor section; no numeric FI vs. CHS comparison
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 7 names 04-laser-icf (HB11, p-B11 fast ignition) as the "most direct parallel," but for TEA purposes the structurally closest comparator is 17a-laser-icf-hybrid-drive (Xcimer HDD: D-T fuel, DPSSL driver class, ~sub-Hz rep rate, steam cycle, same IFE economic framework). The p-B11 FI concept shares the fast ignition physics step but has a completely different fuel cycle, blanket cost structure, and gain requirement — making it TEA-dissimilar despite the physics analogy. Xcimer data is used throughout Sections 2–4 but is not formally listed in Section 7 as a nearest neighbor. More critically, the section does not attempt the central TEA question: given the model's baseline LCOE of 67.6 $/MWh (with the dual-driver cost lower-bounded), at what ignitor cost premium does FI become more expensive than a CHS D-T direct-drive analog? The ignitor premium sweep (67.6 → 70.0 $/MWh at +65%) is in the model output but never interpreted against a CHS LCOE reference.
- **Recommendation:** In Section 7, add 17a-laser-icf-hybrid-drive as the first-named nearest neighbor for TEA comparisons (same fuel, driver class, and economic framework), followed by 26-laser-icf-indirect-drive for cost benchmarks, with 04-laser-icf noted as a physics-parallel but TEA-dissimilar concept. Add a closing paragraph that uses the ignitor premium sweep to bound the answer: state the approximate CHS D-T IFE LCOE reference (from Meier 2006 CI result or 17a analysis), identify the premium threshold at which FI stops being cheaper than CHS, and flag whether the Focused Energy scenario falls above or below that threshold.
- **Priority:** important

### F-3: "Ranked by sensitivity" claim inconsistent with model output
- **Target:** Section 2 (Modeling Approach, Top three LCOE levers)
- **Category:** analysis
- **Finding:** The analysis states the top-3 LCOE levers are "ranked by sensitivity" as: (1) availability, (2) q_eng, (3) driver capital. However, the model's sensitivity output shows construction_time_yr (+0.2601) and eta_th (-0.2460) each have higher elasticity than driver_laser_per_mw (+0.0638). A reader who cross-checks the model output against the ranking will find the claim inconsistent. The ranking is defensible on uncertainty-weighted grounds — eta_th is fixed at 0.40 (confirmed by company) and construction time is constrained by project planning, while driver capital is highly uncertain — but the analysis says "by sensitivity" when it means "by uncertainty-weighted leverage."
- **Recommendation:** Change "ranked by sensitivity" to "ranked by uncertainty-weighted leverage" and add one sentence clarifying that eta_th and construction time have higher raw sensitivity but are treated as near-fixed for this concept (Rankine cycle confirmed, construction time constrained), making driver capital the most consequential modeled uncertainty despite its lower elasticity value.
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-3/model_setup.py`
