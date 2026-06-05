VERDICT: FINDINGS

### F-1: C220104 override value is $960M (FOAK) in analysis but $560M (NOAK) in model — cross-artifact drift
- **Target:** Section 5b (Override Candidates) — C220104 entry
- **Category:** analysis
- **Finding:** The analysis Section 5b YAML sets `value: 960.0` using the FOAK upper bound ($120/J × 8 MJ), while `model_setup.py` uses `value: 560.0` (NOAK midpoint $70/J × 8 MJ). Both carry `provenance: direct`. The model comment explains the switch ("cost_basis must be 'noak'"), but the analysis YAML — which is the canonical override registry — still records the FOAK figure. A reader comparing the two artifacts sees a $400M discrepancy on the single largest cost account with no reconciliation in the analysis text.
- **Recommendation:** Change the analysis Section 5b C220104 `value` to the NOAK figure (560.0) to match the model, or add a second `value_noak` field and note that the model uses the NOAK value. The rationale already contains the NOAK range ($60–$80/J); make the `value` field consistent with what the model actually uses. Keep `provenance: direct` — the NOAK range is also company-published.
- **Priority:** important

### F-2: Q_eng spec value (8.2) describes NOAK performance, not the Athena pilot at its native 5% WPE
- **Target:** model_setup.py spec dict and Section 5 parameter table
- **Category:** model
- **Finding:** The spec uses `q_eng=8.2`, which the model comments acknowledge is the "NOAK target" at 7% laser WPE and 250 target gain. But Athena is a pilot-demonstrator with stated 5% WPE, which the analysis itself estimates would yield Q_eng ~5–6. Using 8.2 in the spec inflates the net-to-gross conversion: the plant produces more net electricity per unit fusion power than the actual Athena design can deliver, making both the native and 1 GWe LCOE appear more favorable than they should. The analysis Section 5 table correctly flags this ("Athena with ~5% eff would be lower") but the model does not use the native-consistent value. This is a design-point coherence issue — the spec claims to describe Athena at native scale but uses a physics parameter that Athena cannot achieve.
- **Recommendation:** Use a Q_eng value consistent with Athena's stated 5% WPE (approximately 5.5–6, derived from the whitepaper's recirculating-power-fraction formula at 5% efficiency). If the intent is to model the NOAK-maturity version of this architecture at 400 MWe, the Design-Point-Maturity field should say so; otherwise, the spec should match the pilot-demonstrator's actual performance. Add a sensitivity sweep over Q_eng = [5.5, 6.5, 8.2] to show the LCOE impact of the WPE assumption.
- **Priority:** blocking
