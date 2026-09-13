# WI-052 consumer handoff

[AGENT] The financial implementation executes at zero interest, equal rates and the tested nearby signed rates. Its numerical and native evidence passes. Repair certification remains blocked by the current study manifest's old executable fingerprint and the separate fresh audit. No manifest, study adapter, oracle, pin, source-adoption or economic decision was changed here.

## Current producer contract

The emitted occurrence prefix is `stellarator_09__stellaris__`. All 246 input keys/defaults, 158 scalar names and their order, producer bindings, 18 authored assertion responses and the aggregate response are preserved. Native ordinary live/held reports are exactly equal to entering reports; the existing divertor violation remains. The full per-case [scalar ledger](implementation/scalar-ledger.json) records each scalar, producer, consumer, entering/candidate values, delta and coverage. No scalar was added.

| Exact emitted channel | Consumers and evidence |
|---|---|
| `stellarator_09__stellaris__cas71_calc__crf` | Comparison CAS90. Independent CRF, stream PV and public annual-cost tests. |
| `stellarator_09__stellaris__cas71_calc__levelized` | CAS70 O&M. Independent construction-escalated annual stream and levelized charge. |
| `stellarator_09__stellaris__cas80_calc__crf` | Public fuel CRF diagnostic; retained in scalar ledger even without a consuming module. Independent CRF. |
| `stellarator_09__stellaris__cas80_calc__levelized` | CAS70 annual total and comparison LCOE. Independent annual stream and levelized charge. |
| `stellarator_09__stellaris__idc__cost` | Comparison CAS90; remains distinct from headline midpoint construction finance. Tiny nonzero factor and currency amount are checked separately. |
| `stellarator_09__stellaris__calendar__replacement_pv` | Public dated replacement PV; independent dated-event sums. |
| `stellarator_09__stellaris__calendar__cas72_annual` | CAS70 replacement account. Independent PV and CRF annualization. |
| `stellarator_09__stellaris__calendar__dated_energy_ratio` | Public dated-energy diagnostic. Independent interval/year-bin numerator, denominator and ratio; remains exactly one in held mode. |
| `stellarator_09__stellaris__cas70_calc__cas70` | Comparison LCOE. Reconstructed rollup at native operands; its upstream finance quantities are independently checked. |
| `stellarator_09__stellaris__cas70_calc__annual_total` | Headline DCF annual cost. Reconstructed rollup at native operands; its upstream finance quantities are independently checked. |
| `stellarator_09__stellaris__cas90_1cfe_calc__cas90` | Comparison LCOE. Reconstructed from overnight capital, reported IDC and independently checked CRF. |
| `stellarator_09__stellaris__lcoe_calc__lcoe` | Headline annual-equivalent price. Independent CRF, midpoint multiplier, annual capital, numerator, energy denominator and price at native operands. |
| `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` | Comparison price. Reconstructed from CAS70/CAS80/CAS90 and existing energy terms; does not substitute for factor/PV verification. |

`stellarator_09__stellaris__calendar__availability` continues feeding the fuel quantity and both price denominators. All eight physical calendar outputs, event dates, live event walk, strict restart condition, held wall-load floor, floor-then-cap order and event count remain exact against entering execution. The remaining scalar channels are exhaustively covered by the ledger's exact entering physical/other comparisons.

## Direct execution and preservation

The shared helper is `generated/handwritten/mfe_account_costs/financial_factors.py` under `exploration/stellarator_e2e/`. The three finance manual bodies and existing calendar use it; three unrelated manual bodies remain byte-identical. The current completion route is [regenerate.py](implementation/regenerate.py), with eight explicit seed paths and hashes. It rejects nonfresh destinations, symlink/missing/mismatched seeds and extra manual seeds. Source generation, snapshot generation, ordinary preserved regeneration and smart preserved regeneration produce identical package bytes.

The annuity wrapper returns `(levelized, crf)`. The calendar wrapper returns `(availability, coil_life_margin_fpy, replacement_pv, planned_downtime_yr, terminal_downtime_yr, unplanned_downtime_yr, productive_fpy, dated_energy_ratio, cas72_annual, n_replacements, physical_life_fpy)`. The kept tests execute these public wrappers without native skips. Historical WI-050/051 four-seed evidence remains frozen; current regression callers use the new completion route.

## Required downstream prerequisite

The current study manifest pins executable `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c`; the repaired package carries `fa52a2996d8c1b7c969f0628e812063e0f95d5a5f88b4032df95d857c112e64d`. Integration tests that previously reached later gates now correctly stop at the manifest-generation freshness check (`manifest_currency`). Twenty-one new regression nodes have this freshness consequence. Their baseline headline still reproduces at relative deviation `1.267e-16`, and all 18 pinned verdicts match. These are new downstream failures, not inherited failures or numerical mismatches.

One additional new node is the current radius-consumer check at `tests/study/test_major_radius.py:84`, which calls `.project/active/mfe-major-radius-study-package/implementation/check_controls.py:33`. It still requires exact baseline equality to frozen pre-repair CAS71 finance; the measured relative delta is `1.873133217044486e-16`. Its physical values remain exact. This assertion also belongs to the deferred current-consumer task.

A separately scoped consumer task must review and re-declare the current manifest's baseline, ties, oracle and objective catalog against the repaired package. It must address current oracle/adapter zero/equal/near-rate behavior and promote an integration pin only through its authorized gate. Existing study and pin history stays unchanged. The complete failure-node differential and receipts are linked in the [validation report](implementation/validation-report.md). The fresh auditor should assess this bounded implementation and its unmet final gate explicitly; this handoff does not approve downstream promotion or claim repair completion.

## Numerical limits

The tested window covers all specified rates, Real/fractional durations, one-year neighbors and both IDC switch sides. It preserves inherited subannual negative IDC. Construction-duration zero remains parked. Subnormal underflow, extreme overflow, arbitrary rates near minus one and untested durations receive no acceptance credit and are not silently declared unsupported.
