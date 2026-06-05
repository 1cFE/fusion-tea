# Free-Form Model Update: Laser ICF Liquid-Jet Target (Cortex Fusion Systems)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\iter-2\model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one
- **Native scale only**: do NOT add or restore a `scaled_headline` dict or any
  `(p_native/1000)^(1-α)` extrapolation. Freeform models report at the
  concept's native power. If the prior model contains such code, remove it as
  part of the edit. The headline LCOE line must read
  `LCOE: <value> $/MWh   (freeform, native-scale only)` so cross-concept
  tables can flag it.


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Analysis Section 4 gold consumption estimate is 1000× too low — contradicts model's dominant cost driver
- **Target:** Section 4 (Key Materials and Supply Chain Considerations), gold nanoshell subsection
- **Category:** analysis
- **Finding:** Section 4 computes gold consumption as "~40 μg/s ≈ 0.14 g/hr ≈ 1.3 kg/year" and concludes the cost is "approximately $75,000/year in gold alone — modest." The per-shell mass (4 × 10⁻¹⁴ g) and the throughput (10¹² shells/s) are both stated correctly, but the product is 4 × 10⁻² g/s = 40 mg/s, not 40 μg/s. This is a factor-of-1000 unit conversion error. The correct annual consumption is ~933 kg/year (at 75% availability) costing ~$56M/year — matching the model output exactly. The analysis text claims gold cost is "modest" while the model correctly identifies gold nanoshells as the dominant cost driver at 80.7% of revenue requirement. This internal contradiction means the analysis narrative about cost structure (Sections 2, 4, and 7) is built on a wrong premise: the reader is told gold is negligible when it is in fact the single largest cost by far.
- **Recommendation:** Correct the unit conversion in Section 4: 4 × 10⁻¹⁴ g/shell × 10¹² shells/s = 40 mg/s ≈ 144 g/hr ≈ 933 kg/yr (at 75% availability) ≈ $56M/yr at $60,000/kg. Remove the "modest" characterization. Update the cost narrative throughout Sections 2, 4, and 7 to reflect that gold nanoshell consumption dominates LCOE unless nanoshells survive irradiation (the key unknown the model's sensitivity sweep correctly highlights).
- **Priority:** blocking

### F-2: Model lacks module-level P_native literal and three-forward helper form
- **Target:** model_setup.py module-level interface
- **Category:** model
- **Finding:** The coherence flag reports "no module-level P_native literal." The model computes net electric power from `fusion_power_MW` and `kappa` but never declares `P_native` as a named constant at module level. Additionally, the model does not expose `generic`, `native`, or `result_1gw` at module level, nor does it use the `generic_reference()` / `run_native_and_1gw()` helper form. Since the concept has no archetype (`Archetype-Fit: None`), there is no generic reference to run against, and the free-form structure is architecturally defensible. However, the pipeline's cross-artifact coherence checks expect a `P_native` literal. Adding a module-level `P_native = 0.3` constant (matching the frontmatter) and documenting that this concept cannot use the three-forward form because it has no archetype would satisfy the pipeline check and make the design-point power explicitly traceable without changing the model's computational structure.
- **Recommendation:** Add a module-level `P_native = 0.3` constant near the top of the module-level interface section, with a comment noting it matches the frontmatter value and is the inferred net electric power from the paper's 1 MW fusion × 30% conversion. If the pipeline requires `native` and `result_1gw` module-level names, alias the existing `results` dict to `native = results` and set `result_1gw = None` with a comment explaining this concept has no archetype for 1 GWe projection.
- **Priority:** important

### F-3: Section 7 family-delta discussion does not engage fixed comparables (empty list acknowledged but cost-direction analysis is absent)
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The frontmatter `Comparables: []` is empty, and Section 7 correctly acknowledges this. The section then describes how the concept differs from other IFE concepts in mechanism, scale, driver, and fuel. However, it does not assign a cost direction (advantage, penalty, neutral, unknown) to any of these differentiators as required by the analysis goals. The D-D fuel advantage (no tritium infrastructure) is noted but not tagged with a TEA consequence. The "negligible laser cost" differentiator is mentioned but not compared to a specific subsystem cost in a named comparable. The gold nanoshell cost penalty is not called out as a differentiator at all — and given Finding F-1, the analysis text at time of writing doesn't yet recognize it as the dominant cost.
- **Recommendation:** For each structural differentiator (no magnets, no tritium, negligible driver cost, novel target consumable, sub-MW scale), add an explicit cost-direction tag: advantage, penalty, neutral, or unknown. At minimum: (1) no magnets/tritium → advantage (eliminates CAS22.03, CAS22.04, breeding blanket); (2) negligible driver cost → advantage (CAS22.07 orders of magnitude below IFE norms); (3) gold nanoshell consumable → penalty (CAS80 dominates LCOE at ~$56M/yr); (4) sub-MW scale → penalty (fixed-cost floor dominates); (5) undesigned energy conversion → unknown (κ = 30% assumed, no mechanism). This makes the family-delta section actionable for the TEA rather than purely descriptive.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\analysis.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`

## Output
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\iter-2\model_setup.py`
