# 1costingfe Model Update: Heavy Ion Beam ICF (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Driver efficiency sensitivity is inverted — contradicts the central HIF economic argument
- **Target:** model_setup.py / model_output.txt (sensitivity section and driver efficiency scenario sweep)
- **Category:** model
- **Finding:** The model shows **positive** elasticity for `eta_pin` (+0.148), meaning higher driver efficiency increases LCOE. The scenario sweep confirms this: eta_pin = 0.25 gives LCOE = $91.9/MWh while eta_pin = 0.45 gives $92.7/MWh. The laser ICF reference (eta_pin = 0.10) produces LCOE = $91.4/MWh — *lower* than HIF's base case at 0.35. This directly contradicts the analysis narrative's claim (Section 7) that "This is the foundational HIF economic argument" against laser ICF. Physically, higher driver wall-plug efficiency should reduce recirculating power and lower LCOE (consistent with `q_eng` having negative elasticity of -0.32 as expected). The sign inversion suggests `eta_pin` is either not correctly wired to recirculating power in the IFE model path, or the 1costingfe framework's `eta_pin` parameter (designed for tokamak heating efficiency) is semantically mismatched with HIF driver efficiency and enters a cost sub-model in the wrong direction.
- **Recommendation:** Diagnose whether `eta_pin` in the framework drives Q_eng (and thus net power) in the correct direction for IFE. If `eta_pin` connects only to a cost sub-model that scales driver CAPEX upward with efficiency rather than reducing recirculating power, the wiring is wrong for HIF. The driver efficiency scenario sweep should show LCOE *decreasing* as eta_pin rises from 0.10 (laser ICF) to 0.35–0.40 (HIF range). Fix the parameterization so the model correctly demonstrates HIF's structural efficiency advantage, or if the framework cannot represent this pathway, document the limitation explicitly and use a manual scenario (e.g., "if recirculating power fraction were reduced to X% by driver efficiency, LCOE would be $Y").
- **Priority:** blocking

### F-2: Availability is the top LCOE lever but is not treated as a key challenge
- **Target:** Section 2 (Challenges) and Section 5 (Parameters)
- **Category:** analysis
- **Finding:** The model's top sensitivity parameter is `availability` (elasticity -0.958), roughly 3× the magnitude of the next parameter (`q_eng` at -0.32). Yet Section 2 has no challenge entry addressing availability for HIF. For a rep-rated IFE concept at 5–15 Hz, availability is determined by: (a) accelerator uptime across hundreds of induction cells, (b) liquid wall system cycling reliability, (c) target injection system reliability, and (d) chamber vacuum re-establishment between shots. None of these is characterized quantitatively or framed as an LCOE-critical challenge. The analysis correctly notes "no published HYLIFE-II availability target" in the Section 5 missing-parameters table, but does not discuss *why* HIF availability might be higher or lower than analogous IFE concepts or what the LCOE consequence of a 5-percentage-point availability swing (~0.95 × $5/MWh per point) would be.
- **Recommendation:** Add a Section 2 challenge entry (or expand an existing entry) explicitly treating availability as the primary LCOE lever for HIF. Discuss the three availability-driving subsystems (accelerator, liquid wall, target factory) with at least an order-of-magnitude framing of what availability range is plausible (e.g., 70–90%). Note that the high rep rate (6 Hz) means any per-shot failure mode is magnified, but also that individual shot failures may not require full plant shutdown. Add an availability range (70–90%) to the Section 5 parameters table as a medium-confidence analogue estimate. This reframing better aligns the analysis narrative with the model's quantitative findings.
- **Priority:** important

### F-3: No modeling approach decision stated; key hypotheses not formulated as testable propositions
- **Target:** Section 2 (or a dedicated modeling approach section)
- **Category:** analysis
- **Finding:** The analysis does not state whether 1costingfe or free-form modeling is appropriate for HIF, or why. HIF deviates structurally from the 1costingfe reference concept (no plasma-confining magnets; driver replaces magnet system as dominant CAPEX; per-shot target costs create a variable OPEX stream with no MFE analog), raising the question of whether the tokamak-centric cost accounting structure adequately captures HIF's cost shape. Additionally, the analysis frames key uncertainties as open questions (e.g., "whether DT ice-layer targets...can be produced at this cost is unknown") rather than testable hypotheses. A TEA model should be organized around propositions of the form: "HIF achieves LCOE < $100/MWh if and only if driver CAPEX is reduced to $X by modular manufacturing AND target cost is < $Y per shot AND availability exceeds Z%."
- **Recommendation:** Add a brief modeling approach statement identifying: (1) whether 1costingfe or freeform is being used and the key framework gaps for HIF (especially driver cost sub-account, target factory OPEX, no blanket replacement CAPEX), and (2) 2–3 key hypotheses stated as explicit if-then propositions that the sensitivity sweeps are designed to test. For example: "H1: Modular induction linac manufacturing reduces driver CAPEX from $1.4B to $0.7B (NOAK), enabling LCOE < $80/MWh — tested in the driver capital sweep." This gives the model a clear purpose and makes it auditable against the analysis claims.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_heavy_ion.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/iter-2/model_setup.py`
