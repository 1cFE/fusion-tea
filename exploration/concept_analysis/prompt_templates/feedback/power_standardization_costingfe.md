VERDICT: FINDINGS

### F-1: Add post-hoc scaling headline for 1000 MWe cross-concept comparison

- **Category:** model
- **Severity:** high
- **Description:** For cross-concept comparability, add a `scaled_headline` dict at
  module level with LCOE and overnight $/kW normalized to 1000 MWe using
  economy-of-scale post-hoc scaling.

  Required changes:
  1. Do NOT change `result = model.forward(...)` — keep it at the concept's native
     power level with all existing parameters and cost_overrides untouched.
  2. After the existing `result` computation, add a scaling block:
     ```python
     # Post-hoc scaling to 1000 MWe (cross-concept comparison)
     _ALPHA = 0.6  # economy-of-scale exponent
     _p_native = float(result.power_table.p_net)
     _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

     scaled_headline = {
         "p_net_mw": 1000.0,
         "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
         "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
     }
     ```
  3. Add a brief print line showing the scaled headline values for reference.
  4. Do NOT rename `result`, do NOT add `result_native`, do NOT duplicate forward().
  5. If the model has FOAK/NOAK scenario branches, only the primary `result` needs
     a `scaled_headline`. Scenario branches (e.g., `result_foak`) are informational.
