# Independent numerical verification

**Independent numerical verification: PASS.** The final 35-case development battery agrees with the independent oracle. Its 32 evaluated cases each pass 1,192 scalar comparisons and 125 predicate checks. Three invalid cases are consistently refused. Another 88 checks verify behavior across native cases. All 498 retained conversion replay cases also pass 1,192 scalar and 125 predicate comparisons each. Across both batteries, 631,760 scalar values and 66,250 predicate results agree, with no outstanding numerical discrepancy. The executable fingerprint is `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f`.

## Authority and independence

The original source, fuel and lifecycle equations follow the accepted design/configuration at 81423599. Dynamic cryogenic demand and auxiliary rejection follow the corrected design approved in `work/orchestration/goals/design-study-whole-plant-conversion/evidence/capture-boundary-review-r2.md`. Selected cryoplant ratings and price follow `cryoplant-offer-review.md` in that directory.

The new oracle imports no production numerical body. It independently enumerates common account membership, branch equipment/freight/spares/tax bases and replacement dates. It uses explicit annual discount sums. The retained conversion oracles and startup-inventory oracle preserve their prior independent arithmetic. Authored SysML supplies wiring; generated metadata identifies predicate operands. Those bindings do not supply numerical equations or expected totals.

The exact 48 kA capture passes 93 separately derived geometry, material, procurement, current, stress, strain and refrigeration comparisons. One integration discrepancy was found and corrected: the native captured stress margin initially subtracted stress from the 650 MPa source peak calibration rather than the retained 800 MPa allowable. `first-native-findings.md` and `native-check-first.json` preserve that finding; the final receipt verifies its correction.

## Coverage

| Evidence | Result |
|---|---|
| `capture-check.json` | 93 selected-magnet comparisons pass |
| `semantic-checks.json` | 69 equation checks pass, including all common leaf and branch-slot memberships |
| `authored-checks.json` | 48 independent wiring and perturbation checks pass |
| `native-check-final.json` | 38,144 scalar and 4,000 predicate comparisons pass; three consistent refusals |
| `native-behaviors-final.json` | 88 native behavior checks pass |
| `controls-summary.json` and `controls/batch-*.json` | All 498 replay cases pass; 593,616 scalar and 62,250 predicate comparisons |

Four native solver iteration outputs remain diagnostic-only. Every other emitted scalar is independently compared. Relative agreement is 1e-9. The new dimensionless isotope residuals use 1e-12 absolute tolerance; cost cancellation residuals use 1e-4 USD2025 and power residuals use 1e-9 MW. All component values are compared separately, and capacity predicates receive no added tolerance. Existing conversion solver tolerances are retained.

## Required behavior

- Matched 2,500 MW and 2,800 MW points satisfy every applicable predicate. The 3,000 MW point fails primary pressure and divertor loading.
- Source-only and heating-demand-only changes preserve installed capital. Fusion, primary work and fuel respond to source heat. Cryogenic uncertainty leaves the separately defined hot source and fuel inversion unchanged.
- Mean nuclear heating of 80 W/m³ and extra cold heat of 13 kW exceed the baseline cold rating. The smaller 20/30 kW offer fails both cryogenic stages. The baseline 40/60 kW and larger 60/90 kW offers pass at reference demand. Changing ratings and quotes leaves demanded heat, refrigeration and export unchanged while changing capital.
- Refrigerator electricity reaches operating export and standby imports. Refrigerator electricity plus extracted heat reaches auxiliary rejection; lead/joint heat is counted once. Primary motor losses also reach the auxiliary sink.
- Insufficient stock, processing, primary pressure and auxiliary capacity fail their checks. Nonpositive export, import-dominated annual delivery, excessive outage demand, a mismatched capture identity and a changed primary path count are excluded.
- A water-property violation, negative extra cryogenic heating and fractional operating lifetime are refused. Actual exchanger crossover fails the actual cold-end approach predicate.
- Lower extraction raises purchased tritium without reducing lithium replenishment. Lower recovery raises deuterium purchases. Zero tritium price retains deuterium and lithium costs. A branch quote changes that branch's capital without changing the other branch or common purchases.
- End-of-life replacement events are excluded. Zero-discount finance and energy sums agree. Outage allowance is checked without changing selected availability.

## Supported conditional development points

These points establish integration support, not an optimized ranking. The 2,800 MW row uses its matched conversion offer; it is distinct from the demand-only perturbation used to prove capital invariance.

| Source MW | Branch | Net export MW | Initial capital USD2025 billion | LCOE USD2025/MWh |
|---:|---|---:|---:|---:|
| 2,500 | Steam | 663.969189 | 18.406924 | 408.163805 |
| 2,500 | Brayton | 285.883396 | 16.962956 | 875.312561 |
| 2,800 | Steam | 746.644668 | 18.721604 | 370.701372 |
| 2,800 | Brayton | 204.460262 | 16.962956 | 1,230.283623 |

Source, nuclear-transport and global-construction qualification remain zero. These calculations do not establish plasma sustainment or a validated reactor build. The selected nuclear-heating scenario is an uncertain demand, not a proven transport bound. The effective hot-source multiplier excludes cryogenic deposition by the reviewed regional accounting assumption.

## Reproduction

Run `check_capture.py`, `check_semantics.py` and `check_authored.py` in this evidence directory with `.codex-test/run python`.

For native agreement: `.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/check_native.py work/active/WI-098_whole-plant-conversion-comparison/evidence/development-final/native/cases.json --out work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/native-check-final.json`.

For cross-case checks, use the same arguments with `check_native_behaviors.py` and output `native-behaviors-final.json`. Each receipt records the exact native source-file hash. The oracle files, capture inputs and source/binding files are retained alongside their provenance manifests.

For all retained controls: `.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/check_controls.py`. The batch verifier requires exactly 498 cases and records each native-file hash plus the oracle/source identity. It reports numerical and predicate agreement for retained physically failed cases without turning them into supported cases. The coordinator separately owns comparison against predecessor receipts and study ranking.
