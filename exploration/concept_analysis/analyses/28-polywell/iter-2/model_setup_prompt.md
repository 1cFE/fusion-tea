# Free-Form Model Update: Polywell (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: "No burning plasma" differentiator missing its cost implication
- **Target:** Section 7 (Cross-Concept Notes, differentiators list)
- **Category:** analysis
- **Finding:** Section 7 lists four key differentiators from a conventional tokamak, but item 3 ("No burning plasma") does not state a cost implication (Goal 3). This is actually the concept's most TEA-critical structural difference: because the Polywell never transitions to alpha-sustained burn, the 78 MW e-beam must run continuously, producing a 29% recirculating power fraction at the baseline γ=0.1 and potentially 40–45%+ at γ=0.2. By contrast, a burning-plasma MFE concept (tokamak, stellarator) recirculates only 10–20% for heating and housekeeping once ignited. The e-beam recirculating power is therefore a permanent cost penalty relative to burning-plasma MFE — and it compounds the γ uncertainty: worse γ doubles the beam power, directly degrading Q_eng. This connection (non-burning architecture → high recirculating fraction → γ sensitivity amplified in Q_eng terms) is central to understanding the Polywell's economics but is not stated in Section 7.
- **Recommendation:** Add a sentence in Section 7 under item 3 stating the cost implication: continuous e-beam injection imposes a structural recirculating power penalty (~29% at baseline, ~45%+ at γ=0.2) relative to burning-plasma concepts, making Q_eng significantly lower than Q_sci and making γ the primary lever on both net output and LCOE. Frame this as a cost penalty with a magnitude that depends on γ.
- **Priority:** important

### F-2: Section 2 does not rank challenges by LCOE sensitivity
- **Target:** Section 2 (Challenges in Capturing System Function)
- **Category:** analysis
- **Finding:** Section 2 identifies six challenges (γ, energy conversion, bremsstrahlung, tritium breeding, scaling, O&M) but presents them without ranking by LCOE leverage (Goal 4). The checklist requires Section 2 to identify the 2–3 parameters with highest LCOE sensitivity for this concept. The model output's KEY BINDING CONSTRAINTS section provides this ranking implicitly (γ/fusion power → ±10.80 ¢/kWh swing; thermal efficiency → ±2 ¢/kWh; capital cost overrides → ±1 ¢/kWh), but this does not appear in the analysis text. A reader of Section 2 alone would not know which challenge dominates the LCOE corridor. In particular, bremsstrahlung (item 3) and O&M (item 6) are important physically but have far less LCOE leverage than γ, yet they receive similar narrative weight.
- **Recommendation:** Add a brief priority statement at the top of Section 2 (or at the end of item 1) naming the 2–3 parameters with highest LCOE sensitivity for the Polywell specifically: (1) γ / Q_plasma — dominant, controls net output and recirculating power simultaneously; (2) thermal efficiency — second-order but blocks all net output calculations; (3) capital cost of SC coil and e-beam systems — reducible with engineering study. This ordering should inform which items the cost model prioritizes in sensitivity analysis.
- **Priority:** important

### F-3: Modeling approach choice (1costingfe vs. free-form) not stated in analysis
- **Target:** Section 2 or Section 7 (modeling recommendations)
- **Category:** analysis
- **Finding:** The analysis does not state whether CAS-structured (1costingfe) or free-form modeling is appropriate for the Polywell, nor does it justify the choice (Goal 4). The model output uses the 1cFE CAS-structured framework with two concept-specific overrides (C220103 SC coils, C220104 e-beam), but the analysis text contains no recommendation or rationale. Given that the Polywell substitutes an e-beam injection system and 6-sided SC coil array for the TF/PF coil set and H&CD system of a tokamak, a brief statement justifying CAS-structured modeling (with concept-specific CAS22 overrides for novel subsystems) over free-form would fulfill this requirement and help a modeling agent understand the scope of customization needed.
- **Recommendation:** Add a sentence in Section 2 or Section 7 stating that CAS-structured modeling (1costingfe) is appropriate because the Polywell shares the D-T BOP structure (buildings, turbine plant, tritium handling) with MFE concepts, and the concept-specific cost differences concentrate in two CAS22 line items: SC coil system and e-beam injection, both handled via direct override. Note that a free-form model would not improve accuracy given the current data availability level.
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/iter-2/model_setup.py`
