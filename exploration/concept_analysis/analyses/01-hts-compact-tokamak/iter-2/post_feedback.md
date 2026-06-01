VERDICT: FINDINGS

The analysis is strong on override discipline, family-delta concreteness, and
data-gap honesty, and the cross-artifact P_native / override-count / provenance
checks all hold. One design-point coherence gap in the model is worth one pass.

### F-1: Native run uses the library-default thermal efficiency (~40%), not the named design point's 46%
- **Target:** model_setup.py `spec` dict (add `eta_th`)
- **Category:** model
- **Finding:** The named design point is explicitly the ARC 2015 *conservative-Pilot*
  phase — 233 MWe net **at η_th ≈ 46%** (1100 K blanket outlet), which is what
  distinguishes it from the FNSF phase (190 MWe at ~40%). Section 5 records
  η_th = 46% as the design-point value. But `model_setup.py` leaves `eta_th` to
  the library default in the native forward, and the eta_th sweep confirms the
  headline native point is computed at 0.40 (`eta_th=0.40 → LCOE 199.0`, which
  equals the reported "Native LCOE = 199.0"; the 0.46 case is 194.6). So the
  native reference number that propagates downstream describes the FNSF-material
  operating point, not the 233 MWe conservative-Pilot point the dossier selected.
  The docstring defends this by analogy to override discipline ("aspirational
  published efficiency is not grounds to override the archetype default"), but
  η_th is a design-point physics *spec* parameter that defines this plant's
  operating point — not a cost-account override. Leaving it at the library
  default silently substitutes a different phase of the machine while still
  labeling it 233 MWe.
- **Recommendation:** Set `eta_th=0.46` in the `spec` dict so the native forward
  computes the named conservative-Pilot point (Section 5's stated value), and
  keep the existing 0.40–0.50 sweep with 0.40 labeled as the demonstrated-material
  FNSF floor. The LCOE impact is small (~2%), but it makes the native headline
  describe the one plant the dossier names rather than a lower-efficiency phase.
- **Priority:** important
