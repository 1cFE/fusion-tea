# 1costingfe Model Update: Laser ICF - Fast Ignition (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: FI cost advantage contingent on ignitor laser cost assumption — not modeled
- **Target:** Section 2 (Challenge 2) and Section 5 (Parameter Table)
- **Category:** analysis
- **Finding:** The analysis identifies the dual-laser capital cost as a differentiator and states the combined driver cost will be "higher than a single-driver DPSSL plant" (Challenge 2), but does not model the counter-balancing gain advantage or articulate the trade-off quantitatively. The Meier 2006 systems study (OSTI purl-1438678) provides precisely this: FI achieves 15% lower COE than central hot spot ignition at 10 Hz operation (5.9¢/kWeh FI vs. 6.1¢/kWeh CI) — but only under the assumption that the ignitor laser adds zero incremental $/J to the driver capital cost. The analysis correctly identifies ignitor laser cost as a "blocking" gap (Gap #3 in Section 6) but does not connect this to the published economic model that assumes it away. The analysis should make this conditional structure explicit: the FI economic advantage exists in the literature only under the "free ignitor" assumption, and any realistic ignitor cost erodes it.
- **Recommendation:** In Section 2 Challenge 2, add a paragraph noting that the Meier 2006 study is the primary published reference for FI COE advantage and that its core finding (15% lower COE) explicitly assumes no added capital cost for the ignition laser. State that the analysis's inability to constrain ignitor laser cost (Gap #3) therefore makes the sign of the FI economic advantage unresolved — FI may be cheaper or more expensive than CI depending on this parameter. In Section 5, add a row for "FI COE advantage over CI (Meier 2006)" with value "15% assuming zero ignitor cost premium" at low confidence, citing osti-servlets-purl-1438678.
- **Priority:** blocking

### F-2: Gain competitiveness threshold materially higher than stated viability threshold
- **Target:** Section 2 (Challenge 3) and Section 5 (Parameter Table)
- **Category:** analysis
- **Finding:** The analysis states the commercial viability threshold as η_wp × G > 10, yielding G > 100 at 10% wall-plug efficiency, and notes that Focused Energy targets G = 50–100. The analysis treats G > 100 as the minimum commercial requirement. However, the Hawker 2020 LCOE framework study (PMC-7658748) finds that gain > 400 is required for cost competitiveness with mid-range economic parameters — 4× higher than the analysis's threshold. The analysis does not distinguish between the energetics viability threshold (G > 100, breakeven condition) and the economic competitiveness threshold (G > 400, competitive LCOE condition). Focused Energy's gain target of 50–100 falls below both thresholds. This distinction matters materially for Goals 3 and 5: the physics risk is not just failing to achieve ignition gain, but achieving ignition gain well below the level required for competitive economics.
- **Recommendation:** In Section 2 Challenge 3, add a sentence distinguishing the two thresholds: (1) the energetics breakeven threshold G > 100 (from osti-purl-2561299, the η_wp × G > 10 condition) and (2) the economic competitiveness threshold G > 400 (from Hawker 2020 LCOE model, PMC-7658748). Note that Focused Energy's G = 50–100 commercial target falls below both, and that achieving ignition at G = 50–100 would still leave the concept economically uncompetitive without further gain improvements. In Section 5, update the "η_wp × G minimum for viability" row to distinguish viability (G > 100) from competitiveness (G > 400 per Hawker 2020), and add osti-servlets-purl-1438678 and pmc-articles-pmc7658748 as additional references.
- **Priority:** important

### F-3: Optimal rep rate from systems modeling is 20–25 Hz, not 10 Hz
- **Target:** Section 5 (Parameter Table) and Section 2 (Challenge 2)
- **Category:** model
- **Finding:** The analysis treats 10 Hz as the commercial plant target (from Focused Energy disclosures) without noting that IFE systems modeling finds a different optimum. The Meier 2006 study (OSTI purl-1438678) finds that COE is minimized at 20–25 Hz for both CI and FI configurations, with a +4% COE penalty for being limited to 10 Hz and a +12% penalty for being limited to 5 Hz. This framing is absent from the analysis: 10 Hz is presented as the design point, but Meier establishes it as a sub-optimal rep rate chosen under engineering constraints, not as the economic optimum. This affects the sensitivity sweep design for the model.
- **Recommendation:** In Section 5, update the repetition rate row to note that 10 Hz is Focused Energy's disclosed target and that systems studies (Meier 2006) find 20–25 Hz minimizes COE, with the 10 Hz constraint imposing approximately +4% COE penalty. Add rep rate as an explicit sensitivity parameter in the model, sweeping from 5 Hz to 25 Hz to quantify the rep rate economic leverage. This is a model-level change: add a rep_rate sensitivity sweep to model_setup.py with the Meier 2006 baseline as justification.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Petawatt ignition laser cost excluded from model
- **Target:** Model (model_setup.py / CAS22 driver sub-account)
- **Category:** model
- **Finding:** The model's Key Assumption 2 explicitly states the petawatt ignition laser adds "~35–50% more driver capital vs. a single DPSSL system" but then labels the CAS22 result a "LOWER BOUND on the true dual-driver cost." The dual-laser structure is the defining structural cost differentiator of fast ignition over every other laser IFE concept — it is the primary reason the concept carries a cost premium over CHS direct drive — yet it is absent from the model's CAS22 computation. The LCOE of 67.6 $/MWh is structurally understated by an unquantified but analysis-acknowledged 35–50% driver capital gap. The sensitivity sweep does not include a parameter for the ignition laser cost premium, so there is no way to bracket the result against this known omission.
- **Recommendation:** Add a petawatt ignition laser cost parameter to model_setup.py (e.g., `ignition_laser_cost_premium_frac` defaulting to 0.40, with sensitivity range 0.25–0.65) and apply it as a multiplier on the driver sub-account of CAS22. Include this parameter in the sensitivity sweep. This does not require resolving the proprietary cost — it should be modeled parametrically with the range derived from the 35–50% estimate already stated in the model assumptions.
- **Priority:** blocking

### F-2: Fast ignition viability not captured as scenario branch
- **Target:** Model (sensitivity sweep and scenario structure)
- **Category:** model
- **Finding:** Section 2 (Challenge 1) correctly identifies proton coupling efficiency (η_coup) as "the dominant LCOE uncertainty" and recommends bracketing LCOE "between optimistic (30%) and pessimistic (5%) coupling." Section 2 (Challenge 3) further notes that if fast ignition physics falls short, the required laser energy "rises steeply" — and Key Assumption 1 in the model output states that "If G = 50 (Focused Energy minimum target), q_eng < 1," which is a commercially non-viable regime. However, the model only performs local sensitivity sweeps around q_eng = 4.0, which cannot capture this step-change risk. The sensitivity elasticity of -0.26 for q_eng is computed near a baseline that may itself be unreachable, and the near-zero-gain scenario (fast ignition not achieving gain > 1) is not modeled as a scenario branch at all. This is the concept's primary risk and the analysis explicitly calls it out — the model needs to reflect that.
- **Recommendation:** Add a pessimistic scenario branch to the model where η_coup = 0.05 propagates into an effective q_eng < 1, with the LCOE reported as "non-viable" or computed under a hypothetical rescue-by-laser-energy-scaling scenario. Additionally, sweep η_coup directly (range 0.05–0.30) as a named sensitivity parameter rather than only sweeping q_eng, so the physical chain described in the analysis (η_coup → effective gain → q_eng) is explicit in the model output.
- **Priority:** blocking

### F-3: Section 2 lacks explicit LCOE parameter ranking and modeling-approach declaration
- **Target:** Section 2 (Challenges) and Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Two analysis checklist criteria are not addressed. (a) Section 2 discusses challenges narratively but does not produce an explicit ranked list of the 2–3 parameters with highest LCOE sensitivity for this concept — the model output reveals the top drivers (availability, interest_rate, q_eng, eta_th) but the analysis text does not state this ranking, making it unclear whether the six challenges are in LCOE-leverage order or narrative order. (b) The analysis never states whether 1costingfe or free-form modeling is appropriate for this concept and why — this is a required modeling-approach declaration. Additionally, Section 7's nearest-neighbor discussion names only one concept (26-laser-icf-indirect-drive); concept 04-laser-icf (HB11, p-B11 fast ignition) shares the fast ignition physics step and dual-laser architecture, making it the most structurally relevant comparator for the proton coupling and dual-driver cost questions, yet it is not mentioned.
- **Recommendation:** Add a brief "Modeling Approach" paragraph to Section 2 that (1) states that 1costingfe is used because the concept is D-T with a thermal steam cycle, with the dual-laser driver as an additive cost overlay; (2) explicitly lists the top 3 LCOE levers in ranked order (matching the model sensitivity output: availability, q_eng, driver capital); and (3) frames each of the top-3 as a testable proposition rather than an open challenge (e.g., "H1: Achieving η_coup ≥ 15% is necessary for q_eng > 4.0 at the stated laser energies"). In Section 7, add concept 04-laser-icf as a named nearest neighbor and note the structural parallel (dual-laser, fast ignition physics step) alongside the key differences (fuel cycle, laser technology class).
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-2/model_setup.py`
