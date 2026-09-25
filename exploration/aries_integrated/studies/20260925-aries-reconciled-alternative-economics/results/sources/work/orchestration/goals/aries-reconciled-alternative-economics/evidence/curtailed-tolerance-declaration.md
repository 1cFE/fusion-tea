# Absolute comparison tolerance declaration — curtailed feed and external shortfall (T-004, attempt 1 refused)

[AGENT] 2026-09-25. All-point verification of the executed study (`t004-verify.log`) refused one channel: `aries_integrated_plant__lifecycle_accounts__evaluate__curtailed_feed` in `diag-L8-aligned-discount-0.08` (store 0.0, oracle 6.8e-15 kg/year, relative deviation 1.0 against the 1e-9 rule because the stored value is exactly zero; absolute error 6.8e-15 with no absolute tolerance declared). The verifier stops at the first refusal; the same difference exists on every case whose new feed equals the case's gross makeup exactly (feed 138.7304019114013 kg/year), on both the lifecycle and the source-branch twin channel.

| Case | `lifecycle_accounts__evaluate__curtailed_feed` store / oracle | `source_lifecycle_accounts__evaluate__curtailed_feed` store / oracle | absolute difference |
|---|---:|---:|---:|
| `diag-L6-fuel-self-sufficient` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `diag-L7-aligned-combined-at-1000` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `diag-L7-aligned-combined-at-our-net` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `diag-L8-aligned-discount-0.00` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `diag-L8-aligned-discount-0.03` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `diag-L8-aligned-discount-0.08` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `diag-L8-aligned-discount-0.10` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |
| `sens-feed-makeup-service30m` | 0.0 / 6.8e-15 | 0.0 / 6.8e-15 | 6.8e-15 |

**Class.** `curtailed_feed = max(new_feed − gross_makeup, 0)` and `external_shortfall = max(gross_makeup − new_feed, 0)` are differences of two equal ≈ 139 kg/year quantities at these points. The package (`annual_selected_fuel_impl.py`, `lifecycle_cashflow_accounts_impl.py`) sums burn + loss + decay in float64 and takes `max(feed − makeup, 0)`; the checker (`lifecycle_oracle.py` through `lifecycle_bindings.py`) takes the same difference of a Decimal sum, so at exact equality the package gives exactly 0.0 and the checker exposes the float64 sum's rounding error, bounded at about one ulp (2.8e-14 kg/year at 139 kg/year; observed 6.8e-15) `[r1: corrected from "different orders" on the fresh review]`. This is the numerical class of L-008 of the prior goal (a difference channel at the arithmetic's own order, where a relative-only rule cannot be satisfied), not a modelling difference: every other channel of the same cases agrees at relative ≤ 1e-9, and every verdict is identical.

**Declaration.** An absolute tolerance of 1e-9 kg/year on the four channels `lifecycle_accounts__evaluate__curtailed_feed`, `lifecycle_accounts__evaluate__external_shortfall`, `source_lifecycle_accounts__evaluate__curtailed_feed`, `source_lifecycle_accounts__evaluate__external_shortfall` (prefix `aries_integrated_plant__`). 1e-9 kg/year is 7e-12 of the makeup and one microgram of tritium per year: it cannot conceal any accounting meaning (a 1 kg/year purchase is 30 MUSD2004/year). The relative rule stays in force for every other channel; verdict re-derivation stays exact. The same allowance as the reviewed `unmet_heat` precedent (1e-7 MW on ≈ 1000 MW duties, 1e-10 relative) in spirit; smaller in absolute terms because the quantities are kilograms.

**Review.** `curtailed-tolerance-review.md` (fresh reviewer, six tool calls): FINDINGS, sound in substance; the wording above corrected as required; the `external_shortfall` entries carry their own formula; the eight-point table is the author's tabulation and the re-execution's full verification is the evidence; the equipment oracle computes `annual_external` in float64 like the package, so its channels are not of this class.

**Manifest entries** (added to the record manifest `manifest.json` and to the live `exploration/aries_integrated/studies/manifest.json` after review, so later studies carry it; the pin, fingerprints and every point are unchanged; the integration candidate obtained before the amendment is retained because the seam does not read the tolerance list):

```json
{"channel": "aries_integrated_plant__lifecycle_accounts__evaluate__curtailed_feed", "value": 1e-9, "units": "kg/year", "basis": "max(new_feed - gross_makeup, 0) at exact equality: the package sums burn + loss + decay in float64 and the checker takes the same difference of a Decimal sum, so the package gives exactly 0.0 and the checker exposes the float64 rounding error (about one ulp; 6.8e-15 kg/year observed over 8 points); 1e-9 kg/year is 7e-12 of the makeup and far below any accounting meaning; declared for 20260925-aries-reconciled-alternative-economics and independently reviewed (work/orchestration/goals/aries-reconciled-alternative-economics/evidence/curtailed-tolerance-review.md)"}
```

and the sibling entries for `source_lifecycle_accounts__evaluate__curtailed_feed` (same formula on the source branch) and for `external_shortfall` under both owners, whose formula is `max(gross_makeup - new_feed, 0)` with the same arithmetic class.

**Process.** Attempt 1's results are retained verbatim under `results-attempt1/` with the refused verification log; after the review the manifests are amended, indicators and preflight are re-run on the amended manifest, the 64 points are re-executed into fresh `results/` and compared bit-for-bit with attempt 1 (`results/attempt-comparison.json`), then verified. This consumes one T-004 retry (1 of 2): the task, inputs, scope and meaning are identical; only the verification machinery's declaration changed.
