VERDICT: FINDINGS

### F-1: STALE marker on model_setup.py unresolved for iter-3
- **Target:** `model_setup.py` line 0
- **Category:** model
- **Finding:** The file begins with `# STALE: analysis-updated-iter-2`, indicating the model was not updated after an analysis revision in iter-2. The docstring only documents "Changes from iter-1," confirming the model is the iter-2 version. We are now generating an iter-3 assessment. If the analysis was updated in iter-2 after the last model run, the `model_output.txt` may not reflect the current analysis parameters. This violates the integrity requirement that model output reflect actual model computations (Goal 4).
- **Recommendation:** Either (a) remove the STALE marker and confirm the model reflects the current analysis state, or (b) update the model to incorporate any analysis changes made in iter-2 that were not propagated to the model, then re-run to regenerate `model_output.txt`. Document what changed and why in the docstring "Changes from iter-2" section.
- **Priority:** important

### F-2: Vessel capital cost omitted from Section 2 sensitivity framing
- **Target:** Section 2 (Conditional LCOE Framing and Testable Propositions)
- **Category:** analysis
- **Finding:** Section 2 correctly identifies plant availability (|ε| = 0.95), WACC (|ε| = 0.94), thermal efficiency (|ε| = 0.75), and Q (|ε| = 0.56) as the top LCOE drivers conditional on physics viability. However, the model's own KEY BINDING CONSTRAINTS section ranks D₂O vessel capital cost as binding constraint #2, and the elasticity table shows vessel_inner_radius_m at |ε| = 0.493 — nearly as elastic as Q. At $700/kg and 113 m³ per module, the D₂O fill alone is ~$87M/module ($348M total), a structural cost floor that does not diminish with higher Q (unlike LCOE per kWh). Section 2's framing implies vessel cost is a testable proposition rather than a binding capital lever, which is inconsistent with the model's own ranking (Goal 3 — TEA implications).
- **Recommendation:** Add vessel inner radius / D₂O capital cost to the Section 2 sensitivity summary with its elasticity value (|ε| = 0.493) and note that unlike availability or WACC, it represents a hard capital floor: a larger vessel improves power density but also raises $/kWe at fixed Q. This is the primary design-space trade-off the model reveals, and it should be stated in Section 2 alongside the other top levers.
- **Priority:** important

### F-3: Tokamak differentiator list not explicitly compiled
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** The checklist requires key differentiators from a conventional tokamak to be explicitly listed (Goal 2). The analysis correctly orients comparison toward IFE nearest neighbors (laser ICF, heavy-ion ICF, MTF) rather than MFE, and individual differences are mentioned across Sections 2, 3, 4, and 7. But there is no single compiled list. For a reader working across the full concept portfolio, it is not immediately clear which cost accounts are completely eliminated (C220103 coils → $0, C220104 supplementary heating → $0, C220109 direct energy conversion → $0, no breeding blanket) and which are replaced by acoustic-specific items (C220107 acoustic transducer array). Scattering these facts across sections makes cross-concept comparison harder (Goal 1 — concept positioning).
- **Recommendation:** Add a brief explicit list to Section 7 under a "Differentiators from conventional tokamak" heading: (1) no plasma confinement — acoustic cavitation replaces both the confinement and heating subsystems; (2) no HTS magnets or cryoplant at scale; (3) no tritium breeding blanket; (4) acoustic driver replaces both the magnet coils and the RF/NBI heating. Two to four bullet points with the CAS account mapping is sufficient. This does not require new research — the information is already present in the analysis.
- **Priority:** minor
