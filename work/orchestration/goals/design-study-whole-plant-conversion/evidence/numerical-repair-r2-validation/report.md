# Reviewed numerical correction: validation

[AGENT] The exact correction released by [numerical-repair-r2-review.md](../numerical-repair-r2-review.md) passes its bounded regression requirements. The replacement main study has not been prepared or executed. All readers and native validation processes completed before the coordinator was released to rerun integration.

## Changes and identities

The [actual diff](reviewed-changes.diff) contains two one-line changes: the independent cooler's Brent stopping precision, and the scanner's cryogenic diagnostic offsets. The generated native package, public model, physical equations, manifest, acceptance tolerances, and failed original native receipts remain unchanged. Before/after hash comparison identifies only `oracle_thermal.py` among the scanned execution inputs as changed. The original failed record remains failed.

| Artifact | SHA256 |
|---|---|
| Original independent thermal oracle | `5d77285a3c816f8ce88a6da83b0b7f1ef98eefc7cdd06186c05fe6cbe360b417` |
| Corrected independent thermal oracle | `ab1442e237fa90d5fa540703da2568e22082a10809194a42778743133c219b67` |
| Corrected scanner | `8392dd2ee5eb9a34e13b3e4dac5c7184ff9cf41d1fd997d2cd28f41ea9635e12` |
| Unchanged native executable | `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f` |
| Unchanged semantic fingerprint | `bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3` |
| Unchanged indicator input pin | `89acea93750da8794f74883315fb0ff658d6213d0d4b2ffcaf2b1edb320deeae` |

## Completed checks

| Retained or new evidence | Result | Scalar comparisons | Predicate comparisons |
|---|---|---:|---:|
| Original 2,496 study cases | Exactly eight expected scalar failures on the four original cryogenic points; all 2,492 other cases pass; zero predicate mismatches or evaluation errors | 2,975,232 | 312,000 |
| 498 retained controls | All pass under stock rules | 593,616 | 62,250 |
| 35 retained development cases | 32 pass and three domain refusals remain independently consistent | 38,144 | 4,000 |
| Four new cryogenic points | Native execution and stock verification of every scalar/predicate pass | 4,768 | 500 |
| Total checked | Expected failures preserved; no unexpected differences | 3,611,760 | 378,750 |

The original study regression continues the stock verifier's unchanged comparison and predicate derivation rules after each discrepancy so every case is checked. Its [complete discrepancy file](original2496/discrepancies.json) retains the eight original cryogenic failures. The controls and development regression calls the stock `check_case` function directly. The four new points use the existing `execute_study`/`StudyRunner` lifecycle and the stock verifier CLI with sample size four. See [validation-summary.json](validation-summary.json), [controls-development-summary.json](controls-development-summary.json), and [cryo-native-summary.json](cryo-native-summary.json).

## Native cryogenic bracket

At each of the 2,500 and 2,800 MW source loads, the lower heat input is 75.42260142820312 W/m³ and the upper is 75.44260142820313 W/m³. Only the mean nuclear heating input changed from each original complete point. Hardware, ratings, source load, and zero extra structural heat remain fixed.

The lower native cold margin is +3.072599999992235 W and all 125 predicates pass. The upper margin is −3.072600000006787 W and exactly the cold-capacity predicate fails. Every reported scalar and predicate on both sides agrees with the corrected independent oracle under the unchanged acceptance rules. These points bracket the engineering capacity boundary; they do not establish a nuclear heating uncertainty range.

## Remaining gate

The coordinator must rerun integration with the changed independent-source identity, then release preparation of the replacement record. Its complete-point set and aliases must be compared with the sealed original before freezing; the intended input change is limited to the four cryogenic points. Native execution, full stock verification, and final study review remain required before publishing the replacement ranking.
