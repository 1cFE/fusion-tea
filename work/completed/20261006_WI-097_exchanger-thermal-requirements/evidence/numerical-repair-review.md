# WI-097 independent numerical repair review

2026-09-27. [AGENT] Continuing independent reviewer. Reviewed [numerical-repair-investigation.md](numerical-repair-investigation.md), its probe/code and retained failure captures. Reused the accepted physical design, source review and implementation integration coverage. The preserved Round 3 attempt is recorded at `ca25c49c`; Round 4 is the authorized final repair round.

**Verdict: PASS. Implement the proposed stable denominator and restrict the analytic equality branch to exact `Cr == 1`.** This is a numerical evaluation repair of the accepted counterflow equation. It does not change the thermal contract, equipment, controller meaning, independent oracle or verification tolerances. Regenerated native execution and the exact 1277-map replay remain acceptance work after implementation.

## Mathematical equivalence and scope

Let `r=C_min/C_max`, `n=UA/C_min` and `L=1-exp(-n*(1-r))`. The original denominator is identically `1-r*exp(-n*(1-r))=(1-r)+r*L`. Computing `L` with `-expm1(...)` and summing the nonnegative denominator terms avoids subtracting nearly equal numbers. It preserves the same effectiveness `L/((1-r)+r*L)` and installed conductance.

As `r` approaches one, `L` approaches `n*(1-r)`, so effectiveness approaches `n/(1+n)`. The exact-equality branch implements this analytic limit. Applying that limit throughout `abs(1-r)<1e-10` instead approximates unequal capacities and introduces a small discontinuity. Removing that approximation restores the intended continuous equation within floating-point precision. No physical tolerance or admissible operating region is widened.

Both observed execution failures occur outside the old equality cutoff. The retained adjacent bypass endpoints have spurious native residual signs caused by denominator cancellation. Fixing the denominator addresses those failures. The separate near-equality fixtures show why retaining the approximate-equality branch would leave another defect: it can refuse a root or report apparent convergence whose independently calculated heat residual exceeds the native stopping requirement.

The proposed repair leaves the 1e-10 MW bypass residual target, 100 iterations, cycle residual contract and finite-state behavior unchanged. It does not accept a stalled midpoint, clip a temperature, change accepted duty, alter a requirement, resize equipment or mask a failed predicate. The legacy calculation remains a separate unchanged implementation.

## Independent numerical checks

I loaded the original body into a separate Python module and replaced only its local conductance function in memory. I independently evaluated the energy/LMTD conductance identity at 120 decimal digits, rather than using the proposed epsilon denominator as the reference. No production file was modified by these checks.

- For captured trial `c0621`, the repaired bypass's independently calculated duty residual is −4.994166e-12 MW.
- For captured trial `c1085`, the corresponding residual is −6.166469e-11 MW.
- All nine independently constructed near-equality root fixtures satisfy the unchanged 1e-10 MW target. Their maximum absolute high-precision residual is 4.502001e-11 MW.
- Across 510 conductance points spanning UA 0.002–2000 MW/K, secondary heat-capacity rates 0.1–20 MW/K and capacity ratios on both sides of equality, the maximum relative discrepancy against the separate high-precision LMTD identity is 3.16e-16. Included offsets approach equality to 1e-15 and bracket the former cutoff.
- The retained in-memory full-pipeline replays for both failed input maps each report 35 satisfied predicates. These are development probes; their old package fingerprint does not certify a rebuilt executable.
- I checked the probe's original generated-body and failed-store SHA-256 values against the current files. Both remain unchanged at review time.

The author's paired 80/120-digit calculations and captured false-bracket signs are consistent with this independent check. The repair is within the existing equations and delegated implementation scope. No new scientific choice or owner gate is required.

## Implementation and execution release

Change only the new controlled body's conductance evaluation, add the focused failure/equality regressions and regenerate the isolated package. Preserve the Round 3 executable and failed study. Retain the separate legacy body, original inputs, model interface, physical predicates, cost bindings and independent oracle.

Before the Round 4 comparison is accepted, require the rebuilt two-case native replay and unchanged-oracle verification; existing legacy, accounting and failure-state regressions; fresh package identity and integration; and native execution/independent verification of all 1277 original maps. Compare the 1275 previously completed cases' verdicts and explain any changes through the unchanged equations and oracle. A near-threshold rounding difference must be investigated rather than hidden by changing comparison classes or predicate thresholds.

This verdict releases implementation of the numerical repair. It does not certify the repaired package before regeneration, accept an architecture ranking or close the goal.

## Rebuilt implementation recheck — 2026-09-27

**Verdict: PASS. The committed implementation matches the approved remedy and may proceed to integration and exact-map Round 4 replay.** Reviewed commit `bf1fae9feb6bd71dde03b59169e3757536254d29`, the fresh native controls and repair verification/preservation evidence. The new executable fingerprint is `668b903599f995fd6e9038d61a2401144d79f1db13f221b4a663df7cb24a2a23`.

The commit changes exactly three files: the original controlled body, its generated copy and the generated package contract. Both bodies contain only the approved equality condition and stable denominator replacement. The package contract updates the associated body hash and executable identity. No model interface, predicate, purchased equipment, cost binding, legacy body or solver tolerance changed. The retained build report records successful regeneration to a fixed point.

I reran the 27 kept repair regressions: all passed. They cover fifteen high-precision conductance points, nine near-equality roots, both captured failing trial roots and the complete native preservation check. The author's separate fresh validation reports 56 passing tests in total; these counts overlap and are not additive.

I independently checked the twenty-row rebuilt native receipt and compared the seven legacy cases' complete output dictionaries and effective input maps against their original receipts: all are exact. The two repaired cases use the exact original failed study maps and now each satisfy all 35 native predicates. The regression also confirms every original development case retains its predicate set and every purchase output remains exact.

[repair-oracle-verification.json](repair-oracle-verification.json) reports PASS for all twenty fresh native rows on the complete 435-channel and 35-predicate catalog. I directly compared its tolerance declarations with the pre-repair receipt: all 44 absolute classes and the `1e-9` relative rule are unchanged. The seven independently implemented oracle source hashes in [repair-oracle-preservation.json](repair-oracle-preservation.json) match current source bytes. This establishes unchanged verification semantics for the repaired controls.

The numerical implementation prerequisite is resolved. Fresh integration/preflight and complete verification of the identical 1277-map Round 4 replay remain required before accepting study comparisons. The preserved Round 3 failure remains part of the evidence trail.
