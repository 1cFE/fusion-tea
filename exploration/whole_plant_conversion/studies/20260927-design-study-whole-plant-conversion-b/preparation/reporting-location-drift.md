# Reporting bracket location comparison

[AGENT] Rebuilding every preparation stage with the corrected independent cooler oracle preserves all 2,651 aliases, all nominal and performance anchors, all scenario catalogs, and the strict economic zero-crossing bracket. The resulting suite still contains 2,496 complete points and has zero oracle refusals.

The exact complete-point comparison finds 60 changed input maps: the four reviewed cryogenic replacements and 56 maps from the four ±5 USD2025/MWh reporting-band endpoint scenarios. The latter carry 60 aliases. The secant estimate of the +5 threshold shifts `t` by `1.7208456881689926e-15`; the −5 estimate shifts by `1.6653345369377348e-15`. Only the previously declared quote inputs change, by at most `1.362641504513456e-15` relative. These are floating-point changes caused by recomputing the reporting locations from slightly more accurate oracle outputs.

| Target gap, USD2025/MWh | Endpoint | Original t | Recomputed t |
|---:|---|---:|---:|
| +5 | Lower | 0.4824365396331414 | 0.48243653963314315 |
| +5 | Upper | 0.48245653963314145 | 0.48245653963314317 |
| −5 | Lower | 0.6330429567194699 | 0.6330429567194715 |
| −5 | Upper | 0.6330629567194698 | 0.6330629567194714 |

Both sets retain about 0.000664 USD2025/MWh separation on each side of the target. The original reporting-point inputs were included among the 2,492 unchanged native receipts that passed the corrected oracle regression. The independent recommendation is to retain those original sampled locations explicitly, preserving the reviewed four-point input change. The coordinator selected retention of the original engineered reporting locations, and the [focused disposition review](../../../../../work/orchestration/goals/design-study-whole-plant-conversion/evidence/final-results-review-r2/reporting-location-disposition.md) passed that selection. The replayable `retain_reporting_locations.py` helper restored exactly those 56 quote maps and their 60 aliases, recomputed the oracle responses, and rechecked both reporting brackets. Selection provenance is in `reporting-location-selection.json`.

The exact initial comparison and recomputed proposal list are preserved under `recomputed-reporting-locations/`. The final comparison is in `original-point-comparison.json`. Its proposed-point SHA256 is `5817ba5d4dafa0ee97c64910bcd6d1a0bdf08c7a879233f764cee617caf93405`.
