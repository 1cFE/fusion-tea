# Implementation review r3: WI-095 'Primary Bypass Control' (fresh reviewer, executed evidence)

**Verdict: PASS** (five notes, none correct-before-use). MR-7: **compliant** for the affected scope.

Read only: the brief's entry files. Ran nothing except read-only JSON comparisons through `.codex-test/run python -c`.

## Q1. The body is the definition

`primary_bypass_control_impl.py` computes every output as the calc def doc states. Effectiveness-NTU: `C_min/C_max`, `NTU = UA/C_min`, the `|1 − C_r| < 1e-10` branch and the counterflow form via `expm1`, capability zero when `T_out ≤ secondary_inlet` (equivalent to the doc's `max(…, 0)`). Bisection on `[0, 1 − 1e-9]` to `|g| ≤ 1e-9 MW` or interval `< 1e-15`, 200 iterations; the non-decreasing bracket and exhaustion both raise. `exchanger_return = T_out − capability(f)/((1 − f)·C_h)` in both branches with `f = 0` when infeasible; `mixed_return` and `return_residual = mixed − required_return` follow design § 3. The duty enters only `feasible` and the root target `g(f)`; nothing the design assigns to the capability is computed from the duty.

Note: a third raise exists (`bypass cannot match the duty inside [0, 1)`), firing only when `duty = 0` with `capability(0) > 0`; the doc names two raising guards. A refusal, not a value, so consistent with the design; unexercised.

## Q2. Pre-change control

`return-control-verification.json`: `passed: true`; all seven evaluated cases `compared: 245, differences: []`; `c1-flow4000-reselected-ratings` `refused_both: true`, status `refused` in both receipts. My own comparison of `c1-aries-ratios-reselected-ratings`: `net_electric` 426.57863661707336, `he_capability` 3836.4666047632377, `lcoe` 1559.4383607658922, bit-identical in WI-094 and WI-095.

## Q3. New channels and checks

Same receipt: `bypass_fraction` 0.31122, `feasible` 1, `capability_at_solution − q_ihx` = 6.2e-10 MW (< 1e-9), `return_residual_magnitude` 3.98e-11 K, `return_condition_ok` and `bypass_within_limit` both `satisfied`. `c1-ratio1.35`: `feasible` 0, `return_residual` +17.796 K, `return_condition_ok` violated, `bypass_within_limit` satisfied (margin 1.0). All eight identities true on every evaluated case; `capability_open == he_capability` bit for bit.

## Q4. MR-7

Chosen inputs unchanged: `cycle.selected_flow` 2500, `compressor_1.selected_ratio`, `he_hx.selected_area` 50000 with `assumed_u` (UA a geometry identity), `mdot_loop_rated`. `bypass_fraction` is a calculated operating setting bound only to `return_control` attributes and the two asserts; no capacity or cost consumer reads it (`he_hx` cost follows `selected_area`). `max_bypass` and `tolerance` are declared inputs graded `[ASSUMED: 1.0, no design limit declared; the owner's to set]` and `[ASSUMED: 1e-6 K, the root-solve closure]`. Sufficient (c1-aries) and insufficient (c1-ratio1.35, c1-flow1400 at +72.3 K) supplied designs exercised with the design unchanged.

Note: `primary_loop.mdot` was never a chosen input; it is calculated from duty and the chosen temperature rise, disclosed in its doc as the audited operating-point direction, untouched by WI-095.

Note: 'Bypass Within Limit' is vacuous at `max_bypass = 1.0` (f ≤ 1 − 1e-9 by construction). The assembly doc says "no design limit declared; the owner's to set" and the constraint def doc "1.0 = no design limit declared"; the word "vacuous" is not used. Adequate.

## Q5. Fixed point, registration, preservation

`build-hashes.json`: `fixed_point: true`, 13 `sources`/`staged` entries including `loop_return_control.sysml`, 25 `completions` all `prefix_only: true`. `tests/model_families.py:206` lists `analyses/loop_return_control.sysml` under `costed_loop_brayton`. `preservation-check-t010-build.json`: `passed: true`, 20973 protected files, none changed or missing.

Note: `prefix_only` is a field of the 25 bodies only; source entries are path → sha256 and carry no such flag.

## Missing evidence / uncertainty

- I did not re-execute the verifier or the receipts; I relied on the stored JSON and checked its logic by reading `verify_return_control.py`.
- I did not grep the whole assembly for every `return_control.*` consumer; lines 452-501 show only the asserts, but a reference elsewhere in the 1004-line file is unchecked.
- The loop-side identity term is zero here (`he_cp = loop_cp = 5193.0` in effective inputs); the diverging-cp failure path and the zero-duty refusal are unexercised.
