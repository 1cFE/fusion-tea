# WI-097 bypass convergence investigation

2026-09-27. [AGENT] Bounded author investigation for the Round 3 prerequisite and proposed Round 4 numerical repair. The failed native store and executable were read without modification. This document proposes a repair for independent review; no production package change has been made.

## Finding and proposed repair

Two distinct floating-point defects affect the same counterflow conductance evaluator:

1. The denominator `1 − Cr * exp(−NTU*(1−Cr))` loses significant digits when the heat-capacity ratio Cr approaches one. This creates noisy duty residuals and false bypass-root brackets. It caused both observed native execution failures.
2. The branch `abs(1−Cr) < 1e-10` substitutes the exactly equal-capacity formula for unequal capacities. Its discontinuity can cause a separate root refusal or apparent convergence with a true residual above the unchanged target.

Use the algebraically equivalent expression below, selecting the analytic equal-capacity limit only when the floating-point ratio is exactly one:

```python
if ratio == 1.0:
    epsilon = ntu / (1.0 + ntu)
else:
    loss = -math.expm1(-ntu * (1.0 - ratio))
    epsilon = loss / ((1.0 - ratio) + ratio * loss)
```

This preserves the counterflow effectiveness-NTU equation and its continuous equal-capacity limit. It changes its numerical evaluation, not an engineering requirement or an equipment choice. The bypass root keeps its 1e-10 MW residual target and 100-iteration budget. The cycle residual contract, independent oracle, verification tolerances, operating domains, all 1277 declared input maps, offers and predicates remain unchanged. Legacy mode dispatches to a separate unchanged body and must remain bit-exact.

## Exact failed cases

The store is `exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison/results/native/20260927-exchanger-thermal-comparison.db`. Both failed cases use offer B and supplied fusion 1835.4512830147435 MW. Their complete stored inputs, failure records, exception locals and intermediate cycle states are retained in [numerical-repair-probe.json](numerical-repair-probe.json).

| Quantity | c0621 | c1085 |
|---|---:|---:|
| Scenario / cycle flow / split | 15 K approach / 1403.0517578125 kg/s / 0.8 | Main 30 K / 1259.78515625 kg/s / 0.7 |
| Failing branch | Divertor | Blanket He |
| Delivered duty, MW | 304.31769245221153 | 896.545166140189 |
| Installed UA, MW/K | 2 | 18 |
| Full primary heat-capacity rate, MW/K | 2.5965 | 16.934373 |
| Secondary heat-capacity rate, MW/K | 1.457209555664062 | 6.54206431640625 |
| Required source hot temperature, K | 963.35303965038 | 703.7660697027395 |
| Trial secondary inlet, K | 602.3581508460094 | 516.914479209307 |
| Trial turbine temperature, K | 786.3694435479078 | 859.3709063462677 |
| `1−Cr` near stalled bypass root | 1.21167e-6 | 5.33864e-6 |

These failures occur at intermediate cycle evaluations. Their ratios are outside the approximate equality cutoff; the observed cause is denominator cancellation.

### The brackets are numerically false

For c0621, the final bypass endpoints are 0.438779976889842 and 0.43877997688984205. Native residuals have opposite signs: +5.737832e-9 and −4.634785e-9 MW. At 120 decimal digits, using the exact recorded float arguments, both residuals are negative: approximately −3.951495e-9 and −3.951522e-9 MW. There is no physical root between those endpoints.

For c1085, the endpoints are 0.6136834005808492 and 0.6136834005808494. Native residuals are +1.567514e-9 and −9.036967e-10 MW. High-precision residuals are both positive: approximately +1.091175e-9 and +1.091086e-9 MW. This is another false bracket. At this floating-point resolution, further bisection repeats an endpoint instead of improving the residual.

The 80- and 120-digit conductance calculations agree to better than 4.3e-79 MW for the retained endpoint tests. Small last-digit differences from the independent oracle author's reconstruction reflect where rounded drive/capacity arithmetic is introduced; both calculations establish the same sign and scale. The independent source confirms finite LMTD roots at these exact trial conditions in [oracle-failure-check.json](oracle-failure-check.json).

## Why the equality cutoff also needs correction

The probe evaluates 15 nearby capacity-ratio fixtures with UA 18 MW/K and secondary heat-capacity rate 6 MW/K. The maximum conductance error against high precision is 3.055067e-9 MW/K for the original expression, 1.687326e-10 MW/K after fixing only the denominator, and 8.881784e-16 MW/K after also restricting the equality branch to `Cr == 1`.

Nine root fixtures independently construct the duty for an active primary heat-capacity rate just below, at or above the secondary rate. They use unchanged native bypass solving, full primary capacity 12 MW/K, secondary capacity 6 MW/K, UA 18 MW/K and a 300 K inlet drive. All inputs and outcomes are retained in the probe JSON.

- The original evaluator refuses four of nine fixtures. Some apparent successes have independent physical duty residuals as large as 5.066002e-8 MW despite its 1e-10 MW stopping target.
- A denominator-only change still refuses the fixture at relative capacity offset +5e-11. Other apparent successes retain independent residuals around 2.53e-8 MW because the equality approximation is still active.
- The continuous candidate evaluates all nine. The maximum independently checked duty residual is 4.502002e-11 MW, within the unchanged 1e-10 MW target.

Removing the near-equality substitution is therefore necessary for a stable evaluation of the already intended equation. Keeping it would repair the two sampled failures while leaving a demonstrated defect in the same operating domain.

## Candidate replay evidence

[numerical-repair-probe.py](numerical-repair-probe.py) loads each exact failed input map through the existing native graph, captures the original exception with frame tracing, and then substitutes only the candidate conductance function in memory. The original body and database hashes are identical before and after the probe. Scratch executions are under the recorded `/tmp/wi097-numerical-repair-*` directory.

Both candidate full-pipeline replays complete and satisfy all 35 predicates. At the previously failing intermediate branch states, the new bypass solution's independently checked residual is −4.994166e-12 MW for c0621 and −6.166469e-11 MW for c1085. These are development replays of an in-memory formula substitution; the old package fingerprint does not certify them as repaired native evidence. Regeneration and a new executable identity are required before Round 4.

Reproduce with:

```bash
.codex-test/run bash -c 'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/active/WI-097_exchanger-thermal-requirements/evidence/numerical-repair-probe.py'
```

## Minimal implementation and acceptance scope

After independent approval, change only `conductance()` in the new controlled closure body and rebuild its isolated generated package. Retain the archived Round 3 executable and failed study. The separate legacy implementation, SysML interface, purchased quantities, cost adapters, controller semantics and physical constraints do not change.

Add regressions for both captured trial states, both exact failed full input maps, the nine near-equality root fixtures and the 15 high-precision conductance points. Keep analytical equal-capacity, full-UA saturated-terminal, zero/inadequate-UA and native failure-state tests. Re-run existing legacy preservation and accounting tests. The two repaired full input maps must complete under the rebuilt executable and pass the unchanged independent oracle.

Round 4 must execute the same 1277 maps, preserve their complete-map identities and compare every previously completed case's engineering verdict against Round 3. Numerically compare changed controlled outputs under the unchanged verification classes rather than requiring bit equality across a floating-point repair. Verify every repaired native case independently, regenerate integration receipts and retain any unexpected new refusal as evidence. Increased iteration limits, relaxed residuals and accepting a stalled midpoint are unnecessary and would not repair the false physical bracket.
