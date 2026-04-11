VERDICT: FINDINGS

### F-1: Full HTS coil cost premium not applied in C220103
- **Target:** Model — C220103 coil sub-account in model_setup.py
- **Category:** model
- **Finding:** The model output explicitly notes "framework default does not distinguish
  full-HTS vs. partial-HTS cost penalty" for C220103 (coils, $516M). The analysis
  correctly identifies the full HTS coil scope (TF+PF+CS in REBCO vs. TF-only HTS in
  competing designs like CFS) as the primary TEA differentiator with a cost penalty
  (Goal 3), citing higher REBCO tape demand and novel CS engineering requirements. Yet
  C220103 uses framework defaults, leaving the concept's defining cost difference
  unmodeled. The base-case LCOE of 103 $/MWh may understate the full-HTS cost if the
  CS+PF tape demand meaningfully exceeds the TF-only baseline.
- **Recommendation:** Apply a cost multiplier to C220103 representing the incremental
  REBCO tape demand for PF+CS coils relative to a TF-only HTS baseline. Even a
  placeholder range of ×1.1–×1.3 with a note citing the basis (estimated additional
  tape volume for CS at 25 T, no source) is better than silence. Name the parameter
  in model_setup.py (e.g., `hts_full_coil_premium`) and include it in the sensitivity
  sweep so its LCOE impact is visible.
- **Priority:** blocking

### F-2: Major radius scenario sweep called for in analysis but absent from model
- **Target:** Model — scenario branches in model_setup.py
- **Category:** model
- **Finding:** Section 2 explicitly states "Any LCOE model must bracket this parameter
  with low / base / high scenarios (e.g., R = 1.5 m / 2 m / 2.5 m analogised from CFS
  ARC and CFETR ranges)" and names major radius the third-highest structural LCOE lever
  due to the unknown HH380 design point (Goal 4). The model runs only R=2.0m with a
  marginal sensitivity elasticity of +0.065 — which understates the structural
  uncertainty because the model holds net electric output fixed at 500 MWe. The
  analysis's concern is about an unknown design point (is HH380 a ~250 MWe machine at
  R=1.5m or an ~800 MWe machine at R=2.5m?), not marginal perturbations around a fixed
  output. The model cannot convey this uncertainty as currently structured.
- **Recommendation:** Add Scenario C (small machine: R≈1.5m, scaled net electric
  ~250 MWe) and Scenario D (large machine: R≈2.5m, scaled net electric ~800 MWe) as
  explicit scenario runs with scaled capital costs. Report LCOE for all scenarios in a
  unified table alongside Scenarios A and B so the design-point uncertainty band is
  visible alongside the technical-bet failure scenarios.
- **Priority:** important

### F-3: Full HTS cost penalty not mapped to CAS accounts in analysis narrative
- **Target:** Section 7 (Cross-Concept Notes) — differentiator table
- **Category:** analysis
- **Finding:** Section 7 correctly identifies "Full HTS coil set (TF+PF+CS in REBCO)"
  as the primary differentiator with a cost penalty (Goal 3), but the penalty is
  described only in qualitative terms ("more REBCO tape per plant, novel CS duty-cycle
  risk, higher coil fabrication cost"). The analysis does not name which CAS accounts
  are elevated or specify the comparison axis clearly — the relevant comparison is
  full-HTS vs. TF-only-HTS competitors (CFS, Tokamak Energy), not vs. the LTS baseline,
  since those are the live commercial competitors in the same field regime. Without
  CAS mapping, the model has no guidance on where to apply the premium, which is why
  C220103 falls back to framework defaults.
- **Recommendation:** Extend the full HTS row in the Section 7 differentiator table to
  state: the cost penalty falls primarily in C220103 (HTS magnet system — higher REBCO
  tape demand for CS+PF vs. TF-only) and secondarily in CAS70 O&M (CS coil
  reconditioning / replacement events in the CS coil reliability failure scenario).
  Clarify that the comparison axis is TF-only HTS competitors rather than the LTS
  baseline.
- **Priority:** important
