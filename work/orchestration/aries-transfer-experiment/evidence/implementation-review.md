# Independent bounded implementation review

[AGENT] 2026-09-21. WI-082 accepted for its conditioned tritium-flow and supplied-capacity proof. WI-081 implementation and the combined reporting claim remain pending. This is a focused `audit-models` review, not whole-plant qualification.

## WI-082: accepted within its declared scope

[AGENT] Primary Table VII, printed p716, visually confirms the 2436 MW reference fusion load. The case treats it as a supplied subsystem boundary. Burn fraction, recovery and hardware rating remain labeled scenario assumptions. The actual `fuel_reuse.sysml` bindings connect the fuel-system exhaust to the processing occurrence; the generated pipeline preserves that dependency and sends its calculated margin and definedness to the existing executable constraint. Hardware rating remains a public independent input.

[AGENT] Reused author evidence in `work/active/WI-082_aries-existing-component-transfer-proof/evidence/` establishes five native cases, 35 exact comparisons with the prior seven-output fuel implementation, conservation checks and the under/over-capacity outcomes. Independently inspected the generated body and original-preserving capacity completion. The review script verifies current source hashes against the generation receipt and confirms that the capacity body differs only in package import prefix.

[AGENT] Independent replay addresses the concrete uncertainty that the three L6 EXPOSE errors might mask lost native dependency edges. `review-native.py` loads the actual sealed package and executes a new 3000 MW case and an unsupported case through TEAx. At 3000 MW, independent decimal arithmetic gives exhaust `2.023697481480452e22` T atoms/s; execution agrees within `2e-15` relative tolerance, keeps the rating at `2e22`, and violates the capacity constraint. Unsupported conditions produce definedness zero and no adequacy credit. Package fingerprint and outputs are in `review-native.json`.

[AGENT] Accept the narrow L6 exception for `exhaust_atoms_s`, `margin_atoms_s` and `evaluation_defined`: generated bindings resolve each dotted expression, exported filenames retain the EXPOSE labels, and native execution verifies the downstream effect. Retain the validator's exit 1 and L1–L5 passes; do not describe this as six-level validation passing. No exception is granted for unrelated expressions or future packages.

[AGENT] The current report correctly distinguishes undefined capability from a physical shortage, and excludes raw breeding channels, total D+T equipment qualification, cost and plant claims. Independent hashing verifies all 1,383 entries in the experiment baseline remain unchanged, including original library definitions and protected comparison evidence. This is no broad-regression claim.

## Pending scope

[AGENT] WI-081 final code, native domain refusal, amplitude propagation and source-polynomial checks remain to be reviewed. The combined report and 13-area transfer register remain to be reviewed when available. No combined completion verdict is issued yet.
