# 1costingfe Model Update: MagLIF (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/iter-10/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/iter-10/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: eta_th standardization to 0.35 ignores the sourced combined-cycle category and discards a peer-reviewed Z-IFE value
- **Target:** `model_setup.py` lines 110–114 (`ETA_TH = 0.35`); related power balance discussion in `analysis.md` Section 2 (Power Conversion) and Section 5 (Parameters).
- **Category:** model
- **Finding:** The model sets `ETA_TH = 0.35` with the comment "standardized from 0.42 per scoring_framework.md (Energy Capture: Thermal (unspecified))". This mapping is the wrong category, and the consequence is a non-trivial LCOE distortion:
  1. **The cited source is a combined cycle, not unspecified thermal.** `z-ife-sand2006-7148-thermal-cycles.md §3.2` (named in the inline comment, lines 112–114) describes a Combined Brayton-Rankine cycle with steel-chamber outlet conditions targeting ~42%, with a stated path to ~50% via C-C composite chambers. This is a *specific* cycle architecture with a *peer-reviewed published efficiency*, not a TBD/unknown.
  2. **The scoring_framework.md table has the right row already** (line 316): `"Thermal (combined cycle, Brayton-Rankine) | 0.50 | Best thermal achievable"`. The Z-IFE 0.42 is conservative within this published-cycle category — well above the 0.35 default for unspecified steam.
  3. **The category dispatch logic for "unspecified" defaults to 0.35** (line 317 of the framework: "Default to superheated steam unless concept specifies"). Z-IFE has specified the cycle — applying the "unspecified" canonical violates the framework's own conditional ("unless concept specifies"). This is a category-assignment error, not a deviation question.
  4. **LCOE consequence is direct:** dropping eta_th from 0.42 to 0.35 increases the required fusion power per net MWe by ~20%, which propagates into CAS22/24 (chamber, driver scaling) and inflates LCOE for a concept that already has marginal Q_eng.
  This is the inverse failure mode of 06-magnetic-mirror: 06 standardized *upward* away from its physics carve-out; 07 standardized *downward* away from a published source it cites in its own comment.
- **Recommendation:**
  1. Re-classify the energy capture as "Thermal (combined cycle, Brayton-Rankine)" and apply the matching canonical of 0.50, OR retain the published 0.42 as a justified deviation citing the steel-chamber regime explicitly. The inline comment should read: `# DEVIATION (justified): Energy capture = Thermal (combined cycle, Brayton-Rankine); canonical 0.50. Using 0.42 per z-ife-sand2006-7148-thermal-cycles.md §3.2 (steel-chamber near-term regime; 0.50 requires C-C composite chambers not yet commercial).`
  2. Add a scenario branch / sensitivity sweep in the model: eta_th ∈ {0.42 steel, 0.50 C-C composite}. Report LCOE under both. The C-C scenario should be labeled "advanced material assumption" so downstream comparisons can isolate the material-readiness assumption from the architectural one.
  3. Update Section 2 (Power Conversion) in `analysis.md` to: (a) state the cycle architecture explicitly (Combined Brayton-Rankine, steel chamber baseline), (b) name the canonical category match from `scoring_framework.md`, (c) justify the steel-vs-composite scenario choice. Currently the analysis silently absorbs the 0.35 standardization without engaging the source it cites.
  4. Cross-check whether ETA_PIN=0.60 (LTD driver, line 116) and the IMG ~90% wall-plug claim (lines 119–121) interact with eta_th in a way that the current single-point model masks. The combined sensitivity matters more than either alone for Z-IFE-class LCOE.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mif_mag_target.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/iter-10/model_setup.py`
