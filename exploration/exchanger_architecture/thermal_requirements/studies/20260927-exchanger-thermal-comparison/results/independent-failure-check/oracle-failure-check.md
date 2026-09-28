# Independent check of the two failed Round 3 native cases

2026-09-27. [AGENT] Both failed maps are valid finite cases under the unchanged equations and pass all 35 independently derived predicates. Their native bypass-solver failures do not establish physical infeasibility. This assessment supplies a numerical-repair baseline; it is not a native completion or a passing-study claim.

## Evidence and independence

The exact input maps were read from `results/native/20260927-exchanger-thermal-comparison.db` under `exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison/`. Both maps exactly equal their exported maps. The database SHA-256 is unchanged after the read. [oracle-failure-check.json](oracle-failure-check.json) retains the maps, all 435 independent outputs, all 35 re-derived predicates and branch diagnostics. The oracle/equipment/lifecycle file hashes match the earlier development-verification receipt. No oracle equation or tolerance was changed.

The existing independent log-LMTD controller and Brent cycle root converge on both maps. A separate 80/160-digit passive LMTD calculation using each reconstructed active stream agrees between precisions for all six branch states. Its largest difference from the independent accepted branch duty is `2.2737367544323206e-13 MW`. Cycle heat residual magnitudes are `4.547473508864641e-13 MW` in both cases.

## Case results

Both cases use the exact supplied N load, 1835.4512830147435 MW, offer B and network topology. They belong to declared requirement sensitivities; their passing verdicts apply to those supplied requirements.

| Case | Scenario | Cycle flow, kg/s | PbLi split | Independent net, MW | Independent LCOE, USD2004/MWh | Predicates |
|---|---|---:|---:|---:|---:|---|
| `c0621` / `case-00621` | 15 K actual-terminal requirement | 1403.0517578125 | 0.8 | 421.0205823161955 | 1124.9548961663454 | 35/35 satisfied |
| `c1085` / `case-01085` | Alternative post-pump return boundary | 1259.78515625 | 0.7 | 518.9590464166228 | 912.6522964264473 | 35/35 satisfied |

Both accept the full duties He 896.5451661401889 MW, PbLi 1039.5261886482301 MW and divertor 304.31769245221153 MW. All six branch states are defined, required hot states remain below supplied caps, and calculated mixed returns match their supplied targets within `1.14e-13 K`.

| Case / branch | Required bypass fraction | Actual hot terminal, K | Actual cold terminal, K | Active-primary / secondary capacity ratio |
|---|---:|---:|---:|---:|
| c0621 He | 0.7538926526079363 | 109.27793778877322 | 17.208671839311194 | 0.5720074511697174 |
| c0621 PbLi | 0.3429857846966682 | 146.6865587870716 | 15.000376305347913 | 0.5752443657376085 |
| c0621 divertor | 0.43631455994943147 | 151.70273123303923 | 152.6158745522248 | 1.0043917426991635 |
| c1085 He | 0.6136677655289906 | 49.80565752241296 | 49.810472126284935 | 1.0000351332604152 |
| c1085 PbLi | 0.00004313484862927819 | 46.88416709685828 | 70.18080117958357 | 1.114366444333765 |
| c1085 divertor | 0.2313088662081355 | 150.869508339939 | 153.45550909741155 | 1.0169606168933671 |

The limiting requirement for c0621 is its 15 K PbLi cold terminal, with a positive margin of 0.000376305347913 K. The c1085 helium exchanger is close to equal heat-capacity rates.

## Independent check of the exact native failure locations

The native author captured the original intermediate exceptions in [numerical-repair-probe.json](numerical-repair-probe.json). Only the captured stage inputs and original stalled endpoints were used here; candidate repair outputs were not used in independent arithmetic. The failures occur in c0621's divertor at secondary inlet 602.3581508460094 K and c1085's helium stage at 516.914479209307 K. Both have adequate no-bypass capability and a finite full-duty bypass solution.

The original native expression reports opposite residual signs at adjacent floating-point endpoints, but 80/160-digit LMTD evaluations show the endpoints have the same true sign. The c0621 endpoint residuals are −3.951470262109069e-9 and −3.95152710552793e-9 MW. The c1085 endpoint residuals are +1.0911662684520707e-9 and +1.091052581614349e-9 MW. Thus neither stalled pair brackets the true root. This independently confirms numerical evaluation noise, rather than absent thermal capability, as the cause of these two failures.

The unchanged independent log-LMTD controller gives bypass fractions 0.4387799768646484 and 0.6136834005821314 at those respective trial states. Their high-precision duty residuals are −5.684341886080802e-14 and −1.1368683772161603e-13 MW. The oracle's auxiliary binary64 passive-capability diagnostic at these exceptional near-equal-capacity trial states has errors of approximately 1.2e-8 and 2.5e-9 MW, within its previously declared 1e-7 MW comparison class. This diagnostic roundoff does not enter the log-LMTD controller root. No oracle change or tolerance amendment is required by these observations.

## Audit of the completed failed-attempt rows

At the coordinator's explicit request, the unchanged stock verifier was run against the preserved attempted store with `--sample-size 1277`. [verification-attempt.json](../../../../exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison/results/verification-attempt.json) and its adjacent log report 1,277 total cases, 1,275 completed cases and all 1,275 completed cases sampled. Every completed row passes 435 channel comparisons and all 35 exact predicate derivations. The relative tolerance remains `1e-9` with the same 44 declared absolute classes. No additional completed-row mismatch was found.

The stock verifier samples completed cases, so its pass applies only to those 1,275 rows. The two native execution failures remain unverified as native outputs and the overall attempted study remains incomplete. No final `verification_summary.json` was written. A repaired package must replay the same 1,277 maps and pass complete native verification before dependent reporting can resume.
