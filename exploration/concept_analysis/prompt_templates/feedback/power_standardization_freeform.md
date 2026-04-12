VERDICT: FINDINGS

### F-1: Add post-hoc scaling headline for 1000 MWe cross-concept comparison

- **Category:** model
- **Severity:** high
- **Description:** For cross-concept comparability, add a `scaled_headline` dict at
  module level with LCOE and overnight $/kW normalized to 1000 MWe using
  economy-of-scale post-hoc scaling.

  Required changes:
  1. Do NOT change `results` or any physics parameters — keep all computations at
     the concept's native power level. Do NOT change p_fus, rep_rate, n_mod, Q_sci,
     or any plasma physics parameters.
  2. After the existing `results` computation, add a scaling block:
     ```python
     # Post-hoc scaling to 1000 MWe (cross-concept comparison)
     _ALPHA = 0.6  # economy-of-scale exponent
     _p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
     _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
     _overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native  # $/kW native

     scaled_headline = {
         "p_net_mw": 1000.0,
         "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
         "overnight_per_kw": _overnight * _factor,
     }
     ```
  3. Add a brief print line showing the scaled headline values for reference.
  4. Do NOT rename `results`, do NOT add `results_native`.
  5. `params` should remain the native physics parameters (unchanged).
