# Design review r3: WI-095 loop return control (fresh, focused)

Verdict: FINDINGS. One `correct-before-implementation`; the rest `note`. The physics in § 1–§ 2 holds; the return check as defined does not test what the design says it tests.

## Q1: requirement and arrangement B

The requirement is the loop's. From the definition's own equations, `q_ihx = q_source + w_fluid = mdot·cp·(T_out − T_comp_in)/1e6`, so "return at `T_comp_in`" is exactly "take the whole duty from a stream entering at `T_out`" (matches the doc line). The mixed-return identity holds for any `f < 1`: `f·T_out + (1−f)·(T_out − q/((1−f)C_h)) = T_out − q/C_h = T_comp_in`, with constant-cp mixing consistent with the loop's premise.

`note`: monotonicity holds but § 2's argument for the `C_h(f) < C_c` regime is incomplete (ε rises there while `C_min` falls). The product still falls: with `u = UA/C_h(f) − UA/C_c`, capability `= UA·ΔT / (u/(1−e^{−u}) + UA/C_c)`, and `u/(1−e^{−u})` increases in `u`. Capability is strictly decreasing and tends to 0 as `f → 1`, so the root is unique. Put this in the body's guard doc.

## Q2: cycle side unchanged

Correct for the closure. In `network_heat_driven_closure_impl.py` `stage()` returns `secondary + q/cs` with `q = min(available, cap)`; the turbine bisection sees only the summed `q`. Primary temperatures enter only through `cap`, which binds only when infeasible. The pre-change replay is a valid control.

## Q3: checks — `correct-before-implementation`

'Return Condition Held' is tautological when feasible. § 3 defines `exchanger_return` from `duty`, so `mixed_return = T_out − duty/C_h` to roundoff for any `f`, whatever the bisection returned. The 1e-6 K tolerance is therefore not a root-solve closure, and no output or check carries `|capability(f) − duty|`. Fix: define `exchanger_return = T_out − capability(f)/C_h(f)` in both branches (`f = 0` when infeasible). Then `residual = (duty − capability(f))/C_h`: about 1e-10 K at the 1e-9 MW solve (`C_h` ≈ 10–20 MW/K), the physical deficit when infeasible, one formula. State that bisection exhaustion and the monotonicity guard raise rather than return a value. No physical allowance is introduced either way.

`note`: the identity also needs `he_cp = loop_cp` (declared twice in the assembly, both 5193.0). A 1e-6 relative divergence fails the check by ~2e-4 K. Bind to one or assert equality.

## Q4: MR-7

Roles are right: UA, cycle flow, ratio chosen; `f` an operating setting, not capacity; nothing sized. The `f = 0` family is legitimate: the ratio search lives in the oracle as a study policy, separately identifiable, and each located point executes with the ratio as a chosen input. § 6's feasible/infeasible pair meets MR-7's acceptance test. MR-7 compliant for this scope, subject to the Q3 fix.

`note`: `max_bypass = 1.0` makes 'Bypass Within Limit' vacuous (`f < 1` always). The answer must say so.

## Q5: disclosure

`note`: § 6's expected `f` (0.188, 0.060) are the check file's linear equivalents `residual/(T_out − he_return)`, which assume the exchanger outlet is unchanged by the reduced flow. The ε-NTU root will differ; that difference is the owner's "can change its performance" point. Do not use them as acceptance values.

`note`: the closure's `he_hot`, `he_return` and terminal differences now describe the uncontrolled floating state, not arrangement B's exchanger (hot terminal at `T_out`, cold terminal `exchanger_return − he_secondary_in`). Say so.

`note`: the unmodeled bypass loss feeds `T_comp_in` itself through `dp_loop → r_comp`, not only cost; and the exchanger outlet leg runs below `T_comp_in`, outside the loop's held window, though the mixed return preserves the density premise. Nothing double-counted: `q_ihx` is unchanged and `w_fluid` is recovered once.

## Missing evidence / uncertainty

- "Cycle unchanged" is verified only for the closure's stage arithmetic (impl lines 15–105); the downstream electrical parts were not read.
- Nothing was executed; the numeric `f` values and the bit-exact replay are implementation claims that § 6's control must show.
- § 7 tooling (R6) is outside the five questions and was not assessed.
- The `duty = 0` edge lies outside the stated domain (`mdot = 0`) and was not analyzed.
