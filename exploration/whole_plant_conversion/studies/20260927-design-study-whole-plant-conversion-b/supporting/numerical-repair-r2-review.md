# Round 2 numerical correction review

Date: 2026-09-27. Reviewer: independent boundary reviewer. Verdict: **PASS for the bounded correction below**. This releases implementation of the oracle convergence and four diagnostic-spacing changes. It does not release economic results or certify the replacement study.

## Reviewed proposal and scope

[AGENT] The exact submitted proposal is [numerical-repair-r2-proposal.md](numerical-repair-r2-proposal.md), SHA256 `d54e4192f05f3f6ffb9f4bb315112844e4d642888d8e0067412d653b96fe0da1`. The approved edits are:

- In `exploration/whole_plant_conversion/oracle_thermal.py`, retain the independent water-temperature integration, Brent method, physical equations, root bracket and maximum iteration count; change the cooler root convergence to `xtol=5e-324` (the smallest positive binary64 value) and `rtol=4*epsilon`, or their exact programmatic equivalents.
- In `exploration/whole_plant_conversion/studies/scan_catalog.py`, change only the four cryogenic diagnostic offsets from `±0.00001` to `±0.01 W/m³` about the same calculated threshold. Retain the source cases, equipment offers, capacity, demand equations and failed-side points.
- Preserve the native executable, source model, physical assumptions, comparison rules and acceptance tolerances. Preserve the failed original study and its reviews.

The unchanged oracle source inspected before implementation has SHA256 `5d77285a3c816f8ce88a6da83b0b7f1ef98eefc7cdd06186c05fe6cbe360b417`. A changed oracle source identity must be recorded even though the native executable remains unchanged.

## Independent numerical adjudication

The full [forensic census](verification-failure-r1/discrepancies.json) accounts for all 11 scalar discrepancies over five of 2,496 cases, with zero predicate mismatches. The cooler accounts for three discrepancies; the four cryogenic points account for eight. These are separate causes.

I inspected the native adjacent-float bisection, the oracle's independent segment integration and Brent stopping rule, and the [high-precision reference implementation](verification-failure-r1/high_precision_cooler.py). The reference transcribes the enthalpy and heat-transfer equations with Decimal arithmetic and uses the existing property table. It does not import the native cooler body. Its native and oracle operand maps are identical. The 60-digit and 80-digit calculations agree to a maximum absolute difference of approximately `4.23e-42` across the recorded outputs; this is numerical adjudication of the accepted equations, not new physical validation.

The [reference result](verification-failure-r1/high-precision-cooler.json) places the outlet at `39.11820057461559871919686 °C`. Native differs by about `2.20e-14 K`, while the original oracle differs by about `−1.94e-12 K`. At this small approach, the outlet error is amplified in conductance. The native root already has adjacent binary64 endpoints; a native iteration increase would not resolve the discrepancy. The evidence supports repairing the oracle's stopping accuracy.

The [focused Brent experiment](verification-failure-r1/brent-precision-probe.json) retains the independent algorithm, returns a UA residual of approximately `−2.835e-11 MW/K`, and passes all 1,192 scalar and 125 predicate comparisons for the exact retained cooler case. I inspected its code and checked the receipt counts and empty failure lists. The unchanged gas net export remains negative, so the correction does not erase the case's engineering failure.

For cryogenics, the [conditioning probe](verification-failure-r1/conditioning-probe.json) traces the discrepancy to roundoff in subtracting nearly equal quantities. The proposed offsets give approximately `±3.0726 W` cold-capacity margins at `75.42260142820312` and `75.44260142820313 W/m³`, around the unchanged `75.43260142820313 W/m³` threshold. All four proposed diagnostic calculations retain opposite margin signs and pass the unchanged comparison rule; the largest relative discrepancy across both affected margin outputs is approximately `4.74e-12`. This provides a resolved bracket for the stated study question. Native execution of those four changed inputs remains required.

## Required implementation and integration evidence

1. Inspect the actual diff against this bounded scope and capture the changed oracle/scanner identities. Keep the native/package and acceptance identities unchanged unless a separately reviewed change is needed.
2. Recheck the original 2,496 inputs with the corrected oracle. The expected result is exactly the eight retained cryogenic scalar discrepancies and zero other scalar or predicate mismatches. The original four close points remain recorded failures; they are not relabelled as passing.
3. Execute and stock-verify all four replacement cryogenic inputs natively. Recheck the 498 legacy controls under the corrected independent oracle.
4. Freeze the new study input set and comparison identity before its main run. The 2,492 unchanged inputs plus four declared replacement points must all pass stock scalar and predicate verification in the new 2,496-case record before any economic result is released.

No blocking finding remains for implementing this exact correction. Full integration and final study review remain outstanding. The original [final results review](final-results-review.md) remains FINDINGS, and the [Round 1 closure review](round-1-review.md) remains limited to closure and finding routing.
