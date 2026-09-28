# Record: 20260925-aries-flow-scaling-check

## 1. Study header

- **Study id:** `20260925-aries-flow-scaling-check`
- **Package:** `aries_integrated` (WI-092 package, unchanged since round 2; executable `f739dbce…`, semantic `78dd23bf…`; integration candidate `…/evidence/integration-attempt2/integration_return.json` reused)
- **Date executed:** `2026-09-25`
- **Executor:** Claude coordinator of goal `aries-reference-heat-electricity-reconciliation` (round 3, T-002); executor reporting.
- **Mode:** execute
- **Arms:** single arm, `arm-diagnostic`

## 2. Intake

[OWNER-VERBATIM] From `…/evidence/owner-supplement-r3.md`: "The unresolved question is now much narrower: why does our heat-delivery and cycle model produce a lower turbine-inlet temperature and efficiency than the published calculation?" and, from the owner brief: "Any missing input that prevents that interpretation must have its influence investigated rather than merely be listed."

[AGENT] The round-3 thermal-cycle review (`…/evidence/q1-thermal-cycle-review.md`, finding 2) found that the reference-case contract's cross-paper mapping scales Raffray's duties to Lyon's 2436 MW by 1.030 while holding the primary flows at Raffray's 2365 MW values, so the PbLi return needed for full transfer (447 °C) falls below the cycle-side inlet at 1600 kg/s (452 °C); part of the 56 MW PbLi shortfall of the revised case is that artefact. This study quantifies it by scaling the three primary flows (and the helium and PbLi pump offered capacities, carried along so the mapping does not trip a pump screen by construction) with the duties, all together and one loop at a time, and adds 1650 kg/s points to narrow the cycle-flow threshold the round-2 review left unbracketed. Scaled flows and capacities are declared values of the mapping, never derived from demand. Controls: C1, C2, C3 (series), the round-2 network case and the round-2 1700 kg/s resized case, retained verbatim.

## 3. Objective and result

- **Objective channels:** as in the round-2 record § 3, plus `heat_exchangers__evaluate__pbli_return`, `__pbli_cold_terminal_difference`, `__he_hot_terminal_difference`.
- **Result.** At 1600 kg/s and split 0.85, scaling all three flows with the duties changes unremoved heat by -14.195 MW (PbLi -34.285, helium 20.091) and net by 12.757 MW (`network-c3-scaledflows-0.85`: unmet 95.681, net 892.449, turbine inlet 651.9 °C). The PbLi flow alone accounts for it (unmet -13.936, PbLi -35.360, helium 21.423); the helium flow alone changes unmet heat by -0.274 MW. So ≈ 34 MW of the 56 MW PbLi shortfall is the mapping artefact, but ≈ 20 MW of it migrates to the helium stage (whose limit is the 456 °C hot inlet and rises with the heater inlet), so the total shortfall falls by only ≈ 14 MW. At split 0.90 with scaled flows: unmet 92.369, net 895.426.
- **Threshold.** At 1650 kg/s with the rating raised to 1650 MW the network leaves 42.715 MW unremoved (all PbLi; 26.314 with scaled flows), not steady; at 1700 kg/s all heat is removed in both, and the plant-ledger outputs are the same to -9.3e-04 MW (the PbLi pump proxy at scaled flow). The threshold lies between 1650 and 1700 kg/s for both mappings.
- **Against the reference:** no change to the best tested steady case (net 891.003); the not-steady 1600 kg/s case improves to net 892.449 with scaled flows and remains not steady.

## 4. Constraint outcomes

Every generated constraint identity appears below; no indeterminate statuses.

| `constraint_id` | Status | Note |
|---|---|---|
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | satisfied / violated | Violated in 10 of 12: every case except the two 1700 kg/s resized cases. |
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | satisfied | All 12 (the 1650 and 1700 cases carry their declared ratings). |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180`, `__pbli_pump__…`, `__divertor_pump__…` | satisfied | All 12 (capacities carried with the scaled flows; divertor capacity 500 kg/s exceeds 291.5). |
| the nine other capacity screens and `balances_ok` | satisfied | All 12. |

Two cases satisfy every evaluated check: `resized-compressor-1700-network-0.85` and `resized-compressor-1700-network-scaledflows-0.85`. Exact predicates in `results/constraint_catalog.json`.

## 5. Framing

All 25 axes sensitivity-framed as declared (round-2 axes unchanged; `he_primary_flow`, `pbli_primary_flow` operating; `he_pump_capacity`, `pbli_pump_capacity` purchased, carried with the mapping). No reframing; no case filtered.

## 6. Per-axis account

#### `pbli_primary_flow` — observed response

26,860 → 27,666 kg/s at C3 network 1600 kg/s: PbLi unmet 56.4 → 21.0 MW, helium unmet 53.5 → 74.9, total 109.9 → 95.9; PbLi return 457.9 → 459.3 °C; PbLi cold terminal difference 5.5 → 6.7 K. Sensitivity only.

#### `he_primary_flow` — observed response

3261 → 3359 kg/s alone: total unmet −0.3 MW (helium 53.5 → 52.2, PbLi 56.4 → 57.4). The helium stage is bounded by its hot inlet, not by its capacity rate. Sensitivity only.

#### `divertor_primary_flow`, `he_pump_capacity`, `pbli_pump_capacity` — observed response

Divertor 283 → 291.5 kg/s changes no unmet heat (divertor stream never limiting here). The capacities change only their screens (satisfied in all cases). Sensitivity only.

#### `cycle_flow`, `compressor_rating` — observed response

1650 kg/s: unmet 42.7 (unscaled) / 26.3 (scaled) MW; 1700: 0 / 0. Bracket only; the threshold was not located more finely.

#### the other 19 axes

Varied only to compose the retained controls; responses as in the round-1 and round-2 records.

## 7. Axis groups

`axes.json` declares 25 single-key groups, disjoint, every key a package input. The preflight sibling scan warns as in round 2 plus the divertor pump capacity and the other `selected_flow_capacity` keys; deliberate.

## 8. Indicators and rulings

`indicators.json`: every axis `constraints_reachable` (`he_primary_flow`, `pbli_primary_flow`: 10 of 14 constraints; the two pump capacities: 1 of 14, their own screens). No ruling required. Model-development findings: the primary flows have no hydraulic or MHD law (round-1 `…reconciliation#3`); the pump capacities are scalar screens (`…flow-scaling-check#3`).

## 9. Preflight results

From `preparation/preflight_results.json`: all six gates pass (25 declared keys; sibling warnings deliberate; identity `f739dbce…` recomputed; fingerprints match; LCOE headline reproduces at relative 0 with 2/2 pinned verdicts; package byte-untouched).

## 10. Execution route and why

Same route as round 2 (`revised_reference_support.py` over the round-2 canonical replay receipt and the predecessor executor); the round-2 integration candidate is reused because the package identity and the manifest pin are unchanged. Glue ledger: none.

## 11. Study definition and window provenance

Oracle scan 12 of 12 evaluated, none refused. Windows: scaled flows are Raffray's printed flows × 2436/2365 (sourced values under the contract's mapping); 1650 kg/s is an engineered bracket point; capacities carried with flows.

## 12. Cross-fingerprint correlation and what it means

single fingerprint — no cross-arm correlation needed.

## 13. Verification

All 12 stored cases verified against the package-owned independent oracle (`scripts/study/verify.py`, sample size 12): 364 numeric channels per case at relative 1e-9 or the six declared absolute tolerances, 14 predicates re-derived exactly; outcome `pass`. Largest relative deviation 4.31e+04 at `residual_magnitude` in `20260925-aries-flow-scaling-check:c0006`, a near-zero channel passing its declared absolute tolerance. One attempt; no retries.

## 14. Review outcomes

- Q1 thermal-cycle review (fresh): `…/evidence/q1-thermal-cycle-review.md` (SURVIVES; finding 2 motivates this study).
- Round-3 review of this reading: pending at the round result.

## 15. Findings

| Id | Kind | Finding | Proposed disposition |
|---|---|---|---|
| `20260925-aries-flow-scaling-check#1` | model | Scaling the primary flows with the duties (cross-paper mapping correction) changes the 1600 kg/s network case's unremoved heat by -14.195 MW (PbLi -34.285, helium 20.091) and net by 12.757 MW; the PbLi flow alone accounts for it. ≈ 34 MW of the 56 MW PbLi shortfall is the artefact; ≈ 20 MW migrates to the helium stage. | Bounded correction of the mapping; contract § 8 rule amended to scale flows with duties; ledger. |
| `…#2` | model | Cycle-flow threshold for complete removal with the network at 0.95 recuperation lies between 1650 kg/s (42.7 / 26.3 MW unremoved) and 1700 kg/s (0) for both mappings; the 1700 kg/s steady case's plant outputs are invariant to the flow scaling to 1e-3 MW. | Bracket narrowed; not located more finely. |
| `…#3` | model | Pump offered capacities carried with the scaled flows are declared mapping values; scalar screens only, no pump map. | Declared seam. |
| `…#4` | process | Second study on the same package identity reused the round-2 canonical receipt and integration candidate without re-pin. | Process note. |

## 16. Snapshot

`snapshot.json` (sha256 `342d97318902abfb7803559d4fca7e5ee1dabd688f1344bb146904df5c2ca471`): package `exploration/aries_integrated/aries_integrated` at `812b79bf`, fingerprints unchanged from round 2, the manifest content used (six absolute tolerances), arm `arm-diagnostic`, 228 hashed artifacts, 12 cases with [551] numeric outputs, 364 verified channels and 14 exact verdicts per case, 2 all-checks cases. `sealed-package.tar.gz` and `results/sources/` as in round 2.

## 17. What this record does not contain

No reproduction of the ARIES operating point; no threshold located more finely than 1650–1700 kg/s; no hydraulic statement; no cost conclusion for the scaled flows or ratings; no prediction credit for supplied values; no change to any model, package, manifest or frozen record.
