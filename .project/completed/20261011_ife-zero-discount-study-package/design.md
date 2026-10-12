# Package refresh design

[AGENT] Reuse the existing stock loader, evaluator, study store, verifier and metadata producer. Extend the route's channel catalog with the two audited factor channels. Update the adapter's explicit duration-key check; continue using `tests/ife_oracle.py` for all arithmetic. That oracle already publishes the new factors as independently summed payments.

The metadata producer declares the one discount-rate axis needed by round 2 and refreshes fingerprints, baseline, census and instance snapshot natively. Window selection and the indicator's interpretation belong to a later study task. Update the annex to describe the audited stable factors, changed keys and retained oracle-coverage limit.

No new execution abstraction, arithmetic implementation, compatibility alias or fallback is needed. Validate actual cases through the current route and then regenerate metadata to a fixed point. The owner retains financial interpretation and study framing rulings; a discount-rate axis does not itself claim an engineering bound.
