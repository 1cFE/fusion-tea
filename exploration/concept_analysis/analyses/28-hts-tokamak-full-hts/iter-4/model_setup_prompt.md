# 1costingfe Model Update: HTS Tokamak - Full HTS

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/iter-4/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/iter-4/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Primary structure and vacuum vessel thicknesses are unjustified and mislabeled "DEFAULT"
- **Target:** `model_setup.py` — `STRUCTURE_T` (line 119), `VESSEL_T` (line 120), and the corresponding analysis text covering CAS22 primary structure / vacuum vessel sizing.
- **Category:** model
- **Finding:** The model sets `STRUCTURE_T = 0.15 m` and `VESSEL_T = 0.15 m`, both labeled `# DEFAULT`. Neither value matches any framework YAML default: the `steady_state_tokamak.yaml` default is 0.20 / 0.20, and the only family with 0.15 m thicknesses (`steady_state_stellarator.yaml`) uses 0.15 / 0.10 — not 0.15 / 0.15. The only rationale offered is a single inline comment ("slightly below default reflecting compact geometry") which is not a load-path argument; compactness in an HTS tokamak typically *increases* structural demand (higher field-on-coil forces, tighter disruption load tolerances, ARC-class arguments for thicker primary structure). The vessel_t deviation has no rationale at all. Compared with sibling tokamak concepts (01, 21, 29, 33, 34, all at 0.20 / 0.20), concept 28 silently understates structure and vessel shell volumes — biasing CAS22 capital cost downward by a small but systematic amount, and breaking apples-to-apples comparability across the tokamak peer group. The cost driver isn't trivial: structure/vessel volumes feed CAS22 directly via per-m³ cost coefficients (~$0.15M/m³ structure, ~$0.72M/m³ vessel).
- **Recommendation:** Treat structure_t and vessel_t as researched parameters, not defaults. Specifically:
  1. Investigate published HTS-tokamak primary-structure and vacuum-vessel thickness disclosures for the closest analogs — Energy Singularity HH70 / HH170 / HH380, SPARC, ARC, CFETR — and cite the specific source(s) used (analysis.md §Section 2 already flags HH170/HH380 disclosure gaps; lean on those).
  2. Distinguish three regimes in the rationale: (a) primary structure thickness driven by TF coil out-of-plane loads and disruption EM loads; (b) vacuum vessel thickness driven by atmospheric pressure + disruption halo current + neutron shielding margin; (c) any concept-specific deviation (e.g., compact HTS magnet support arguments). If no disclosure exists for HH170/HH380, anchor to SPARC/ARC published values and explicitly flag as `UNCERTAIN: ±X%` rather than `DEFAULT`.
  3. If after research the right values turn out to be the framework tokamak default (0.20 / 0.20), update both values and re-label the comments as `DEFAULT: matches steady_state_tokamak.yaml; no compact-tokamak-specific disclosure justifies deviation`. If a defensible concept-specific value emerges from the literature, use it and cite the source inline in the kwarg comment block, matching the rationale style already used for `BLANKET_T` and `R0_BASE` in this file.
  4. Add a 2–4 sentence paragraph to the relevant analysis section (likely Section 2 Challenge 2 "blanket/structure undisclosed" or Section 4 "engineering parameters") covering the structure/vessel sizing argument and the resulting LCOE sensitivity. The current analysis silently passes over these two parameters; they deserve at least the same treatment as `BLANKET_T`.
  5. Confirm the cost impact via a small sensitivity check: sweep structure_t and vessel_t over [0.10, 0.15, 0.20, 0.25] m at fixed everything-else and report LCOE deltas. If the sensitivity is genuinely negligible (≤1% LCOE swing across the range), say so in the analysis and the mislabeling becomes documentation-only; if it's non-negligible, the values need a proper source.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/iter-4/model_setup.py`
