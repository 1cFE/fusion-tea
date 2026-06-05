VERDICT: FINDINGS

### F-1: p_input value inconsistent between analysis Section 5 and model_setup.py
- **Target:** Section 5 (Design Point Parameters table), p_input row
- **Category:** analysis
- **Finding:** The analysis parameter table records p_input as "~0 MW (ignited)" with high confidence, while model_setup.py uses p_input=5.0 MW with a well-reasoned justification (minimal burn-control/impurity-management power in an ignited stellarator, analogized to Thea Energy Helios at 0.5–0.64% of P_native). The model's value is the more defensible engineering choice — a true 0 MW input ignores real burn-control needs and may cause numerical edge cases — but the analysis text does not reflect this. Cross-artifact coherence requires the analysis parameter table and the model spec to agree on the same number.
- **Recommendation:** Update the analysis Section 5 p_input row to state 5 MW (or whatever value the model uses) with a note explaining: "Design point is ignited (Q = ∞); 5 MW is a conservative estimate for residual burn-control and impurity-management power (see model_setup.py for derivation)." Change confidence from "high" to "medium" given the value is analyst-estimated rather than published.
- **Priority:** important
