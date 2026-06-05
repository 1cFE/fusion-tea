VERDICT: FINDINGS

### F-1: CAS80 override is not taking effect — fuel cost unchanged from generic
- **Target:** model_setup.py overrides list (CAS80 entry)
- **Category:** model
- **Finding:** The analysis specifies a CAS80 override of $0.5M/yr (raw fuel is earth-abundant p-B11, target fabrication cost allocated to C220108). The model_setup.py dutifully includes this override with `"value": 0.5, "enabled": True`. However, the model output shows CAS80 = 154.5 for both generic and native — identical values, meaning the override is not being applied. At the 1 GWe projection CAS80 doubles to 309.0 (pure power-scaling of the generic default), confirming the override has no effect. This inflates LCOE by carrying a DT-scale fuel cost that the analysis explicitly argues is inapplicable. The fuel cost at $154.5M for a concept using industrial-commodity boron and hydrogen (no tritium) is implausible on its face.
- **Recommendation:** Investigate whether the CostModel framework supports CAS80 overrides through the standard override mechanism. If CAS80 is a top-level annual cost that routes differently from CAS22 sub-accounts, the override may need to be applied via the `spec` dict or a different parameter. Confirm the override takes effect in the output (native CAS80 should differ from generic CAS80 when the override is enabled) and re-run the model.
- **Priority:** blocking

### F-2: CAS70 override appears ineffective — O&M cost unchanged from generic
- **Target:** model_setup.py overrides list (CAS70 entry)
- **Category:** model
- **Finding:** The same pattern as CAS80: the analysis specifies CAS70 at 50% of generic ($0.50 * generic.costs.cas70`), and the model_setup.py includes this override, but the model output shows CAS70 = 38.6 for both generic and native — identical. The 1 GWe value (52.8) is consistent with pure power-scaling of generic, not a 50% reduction. The analysis narrative emphasizes that elimination of neutron-activated component replacement is a major economic advantage of the p-B11 fuel cycle; the model does not reflect this. Both CAS70 and CAS80 are likely top-level cost accounts that the override mechanism doesn't reach, which means two of the nine overrides are silently ineffective, and the LCOE is overstated relative to the analysis intent.
- **Recommendation:** Same root cause as F-1 — determine how CAS70 and CAS80 are handled in the cost model framework and apply the reductions through the correct mechanism. If these accounts cannot be overridden via the standard list, document this as a framework limitation and adjust the native LCOE commentary accordingly.
- **Priority:** blocking

### F-3: CAS21 override appears ineffective — buildings cost unchanged from generic at 1 GWe
- **Target:** model_setup.py overrides list (CAS21 entry)
- **Category:** model
- **Finding:** The CAS21 override is set to `0.50 * generic.costs.cas21` and the native output does show CAS21 = 139.9 vs. generic 279.9 — the override takes effect at native scale. However, at 1 GWe the CAS21 value is also 139.9, identical to native, while most other accounts scale upward from native to 1 GWe (e.g., CAS22: 677.9 → 1307.6, CAS23: 131.8 → 263.5). This suggests the 1 GWe projection is carrying the native CAS21 value without applying power-law scaling, or the override's absolute value is being carried forward as a constant rather than scaling with plant size. This inconsistency means the 1 GWe LCOE may undercount buildings cost relative to the scaling convention applied to other accounts, or the framework intentionally holds CAS21 constant — either way, it should be verified and documented.
- **Recommendation:** Verify whether CAS21 is expected to scale with plant power in the 1 GWe projection. If it should scale (as CAS22, CAS23, CAS24, CAS25, CAS26 all do), the override value expression may need to reference the 1 GWe generic rather than the native generic. If CAS21 is intentionally held constant (site-dependent, not power-dependent), add a comment in model_setup.py explaining this behavior.
- **Priority:** important
