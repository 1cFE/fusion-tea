VERDICT: FINDINGS

### F-1: Analysis YAML uses wrong anchor for Class-U relative overrides
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** The Section 5b YAML for C220101, C220102, and C220106 anchors relative overrides to `generic.costs.C220101`, `generic.costs.C220102`, and `generic.costs.C220106` respectively. Per policy, CAS22 reactor-island sub-accounts (C2201xx) live under `generic.cas22_detail["C2201xx"]`, not `generic.costs`. The model_setup.py already uses the correct anchor (`generic.cas22_detail["C220101"] * 0.70`, etc.) — the analysis YAML does not match. As written, the analysis YAML would fail or produce incorrect values if evaluated directly.
- **Recommendation:** Update the three override YAML entries in Section 5b to use `generic.cas22_detail["C220101"]`, `generic.cas22_detail["C220102"]`, and `generic.cas22_detail["C220106"]` as the anchor, matching model_setup.py exactly.
- **Priority:** important

### F-2: Frame audit incorrectly states CAS70 "scales correctly"
- **Target:** Section 5b (Override Candidates) — frame audit paragraph
- **Category:** analysis
- **Finding:** The Section 5b frame audit reads: "Relative overrides (C220101, C220102, C220106, CAS21, CAS70) are anchored to the generic reference and scale correctly." This is false for CAS70. The model_setup.py explicitly acknowledges the opposite: "NOTE: CAS70 overrides are silently dropped by the framework today (1cFE/1costingfe#106) — this entry has no effect on the headline." The model output confirms it: native CAS70 is 20.8 M$ (above the generic 13.3 M$, driven by elevated CAPEX), proving the 0.80× override has zero effect. The analysis's O&M narrative — claiming a 20% advantage from aneutronic operation — does not flow through to the modelled LCOE, and the frame audit hides this.
- **Recommendation:** Correct the frame audit to remove CAS70 from the "scales correctly" list. Add a note explicitly stating that the CAS70 override is silently dropped per the framework (1costingfe#106) and that the modelled LCOE does not reflect the claimed O&M advantage. The override may remain in the registry as documented intent (matching what model_setup.py already does), but the analysis must not claim it has effect.
- **Priority:** important

### F-3: CAS27 model_setup.py comment misstates expected framework behavior
- **Target:** model_setup.py — CAS27 override comment
- **Category:** model
- **Finding:** The CAS27 override comment states "framework multiplies by n_mod → fleet total $5M," implying the $0.5M absolute value will be multiplied by n_mod=10 at the 1 GWe scale. The model output shows the opposite: CAS27 stays at $0.5M at both native and 1 GWe scales. CAS27 is Class-P (power-proportional) and an absolute override is held flat by the framework; the n_mod multiplication does not apply to absolute overrides on this account. The comment's expected behavior ($5M fleet) never materialises, and the stated rationale class ("Class P, power-proportional") is a partial mismatch with how the override actually behaves. The financial impact is negligible (<0.01% of CAPEX), but the comment would mislead anyone verifying the scale behaviour.
- **Recommendation:** Replace the CAS27 comment's "framework multiplies by n_mod → fleet total $5M" with a note that absolute overrides on CAS27 are held flat — native = 1 GWe = $0.5M — and update the class description accordingly so the documented expectation matches the output.
- **Priority:** minor
