# 1costingfe Model Update: Spherical Tokamak - CS-free p-B11 (p-B11)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: DEC-failure scenario branch missing — the concept's central economic hypothesis is untested
- **Target:** model_setup.py (sensitivity sweep / scenario branches)
- **Category:** model
- **Finding:** The analysis identifies direct energy conversion failure as potentially fatal to the economic case (Section 2, item 2: "without this advantage, a p-B11 plant needs ~10–30× higher plasma performance... while capturing energy at lower efficiency than a D-T thermal plant — making it economically untenable"). The model sweeps eta_de ±10% around the 0.8 base case, but because the model holds net output fixed at 500 MWe, this sweep shows elasticity of only −0.044 — dramatically understating DEC's economic importance. What is actually needed is a scenario branch that substitutes fallback thermal efficiency (eta_th = 0.35) for DEC efficiency (eta_de = 0.8) across the DEC power fraction (f_dec = 0.85). This would show the true LCOE cost of DEC failure, which the analysis predicts is catastrophic. The model currently does not test the primary hypothesis of this concept.
- **Recommendation:** Add a scenario branch labeled "DEC_failure" that sets eta_de = 0.0 and routes the full DEC power fraction (f_dec × P_fusion) through the fallback thermal cycle (eta_th = 0.35). Report the resulting LCOE, net output, and Q_eng alongside the base case. This single scenario branch is the most informative output the model can produce for this concept.
- **Priority:** blocking

### F-2: Section 2 states physics challenges but does not identify top LCOE leverage parameters or testable model propositions
- **Target:** Section 2 (Challenges in Capturing System Function) and modeling approach framing
- **Category:** analysis
- **Finding:** Section 2 thoroughly documents why p-B11 ignition is uncertain and why direct conversion is speculative, but it does not translate those challenges into the two deliverables Goal 4 requires: (a) the 2–3 parameters with the highest LCOE sensitivity for this specific concept, and (b) the key hypotheses stated as testable model propositions rather than open questions. The model sensitivity results show availability (−0.99) and construction time (+0.41) dominate the LCOE, while DEC efficiency shows only −0.044 due to the fixed-net-output model structure — a result that appears to contradict the analysis narrative but is actually a modeling artifact. The analysis never resolves this tension or states what the model is actually testing. Hypotheses like "if DEC efficiency ≥ 70%, the LCOE is competitive with D-T HTS concepts at ~X $/MWh" or "if ECRH recirculating power exceeds 30% of gross output, Q_eng drops below break-even" are implied by the narrative but never stated as propositions the model should evaluate.
- **Recommendation:** Add a paragraph at the end of Section 2 (or a brief Section 2.5 / Modeling Hypotheses block) that: (1) names the 2–3 highest-leverage LCOE parameters for the TEA model (note that availability and capital cost structure dominate because this is a capital-intensive concept with no demonstrated design point, and that DEC efficiency matters most as a scenario branch rather than a sensitivity parameter), and (2) states 2–3 key hypotheses in testable form — e.g., "Hypothesis H1: The DEC-enabled case achieves LCOE ~X $/MWh; the DEC-failure (fallback thermal) case yields LCOE ~Y $/MWh, making p-B11 economically untenable." Also state that 1costingfe with speculative placeholder parameters is used because no published plant study exists, and what that implies for confidence in the LCOE number.
- **Priority:** important

### F-3: Model ECRH recirculating power assumption (200 MW) is inconsistent with the analysis narrative (30–50% of gross output)
- **Target:** model_setup.py (p_input = 200 MW parameter) and Section 2 (CS-free challenge)
- **Category:** model
- **Finding:** Section 2, item 3 states "the recirculating power could represent 30–50% or more of any gross electrical output" from ECRH non-inductive current drive. The model uses p_input = 200 MW, which is approximately 13% of gross electrical output (1488 MWe gross). This is 2–4× below the range the analysis identifies as the concern scenario. The model parameter is labeled [UNCERTAIN — CS-free current drive] but is not swept over the range identified in the analysis. The sensitivity of p_input is +0.134, meaning at the upper bound of the concern range (ECRH ≈ 600–750 MW), LCOE would increase by roughly 25–35% above the base case — a meaningful penalty that is not reflected in the reported sensitivity results. The model and analysis are citing the same concern about ECRH recirculating power but using incompatible numbers.
- **Recommendation:** Either (a) add a sensitivity sweep for p_input over the range implied by the analysis concern (e.g., 200 MW → 700 MW, representing 13% → 47% of gross), reporting LCOE at each endpoint, or (b) add a note in the Key Assumptions table explaining why 200 MW was chosen as the base case (e.g., "represents a successful ECRH efficiency scaling scenario; upper concern bound is 600–700 MW") and include the upper-bound LCOE in the model output. This aligns the model's ECRH assumptions with the uncertainty range the analysis documents.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/iter-2/model_setup.py`
