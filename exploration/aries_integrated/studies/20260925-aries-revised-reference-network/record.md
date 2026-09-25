# Record: 20260925-aries-revised-reference-network

## 1. Study header

- **Study id:** `20260925-aries-revised-reference-network`
- **Package:** `aries_integrated` (WI-092 increment: `Network Heat Driven Closure`; executable `f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4`, semantic `78dd23bf4c4a2d431ce8223d973db08e955e6f378175623ced8b976db4231f93`; integration candidate `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json`)
- **Date executed:** `2026-09-25`
- **Executor:** Claude coordinator of goal `aries-reference-heat-electricity-reconciliation` (round 2, T-004); executor reporting, not an independent administrator reading.
- **Mode:** execute
- **Arms:** single arm, `arm-diagnostic`

## 2. Intake

[OWNER-VERBATIM] From `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/owner-brief.md`:

> Integrate the supported corrections. Retain the original failing case. Produce a separately named revised reference case and show exactly what changed and why. Recheck balances, temperatures, capacity margins, support status and power under the actual native graph.

> Do not enlarge equipment solely until the run passes and call that reference reproduction. A deliberately resized alternative may be studied separately, with its purpose and changed hardware explicit.

[AGENT] Executor additions: this study is the first on the WI-092 package, whose reviewed increment represents the published exchanger network (Raffray Fig. 12: blanket-helium stage, then PbLi and divertor-helium stages in parallel on a supplied cycle-flow split) as network mode 1, with mode 0 reproducing the series closure bit-exactly. It retains the original failing case, the literal Lyon variant, the calculated baseline and the round-1 series cases C1, C2, C3 and the series steady point verbatim; adds the network at each position of the change order (original, C1, C2, C3) to measure order interaction; sweeps the supplied split at C3 (0.50–0.98); tests the steady candidates at 0.8 recuperation; brackets cycle flow at 1700 and 1800 kg/s on the inherited 1600 MW compressor rating; and adds the separately named resized-compressor alternative (rating raised to 1700 or 1800 MW alongside the same flow), labelled as a declared hardware change and never as a reference reproduction. Nothing is tuned to the published output.

## 3. Objective and result

- **Objective channels:** `aries_integrated_plant__plant_ledger__evaluate__net_electric` and `__gross_electric` (MW); `aries_integrated_plant__heat_exchangers__evaluate__unmet_heat`, `__he_unmet`, `__pbli_unmet`, `__divertor_unmet`, `__accepted_heat`, `__turbine_temperature`, `__he_secondary_out`, `__pbli_stream_out`, `__divertor_stream_out`; `aries_integrated_plant__plant_ledger__evaluate__thermal_efficiency` and `__compressor_demand`. The package's LCOE channel remains the manifest headline for the baseline gate and is not this study's objective.
- **Result.** The published network removes the series-order PbLi limit but not all of the unremoved heat at the source-supported inputs. At C3 (0.95 recuperation, 1600 kg/s, 283 kg/s divertor flow, Lyon auxiliaries, source-informed partition) the network with the design-default split 0.85 gives net 879.693 MW, gross 1131.703 MW, thermal efficiency 0.4019 and 109.876 MW unremoved (helium 53.514, PbLi 56.362), against the series C3 values 842.732 / 1094.742 / 0.3945 / 151.002 (all PbLi). The residual is a helium-stage bound: the whole cycle flow enters the blanket-helium stage at 308.6 °C (0.95 recuperation) and leaves at 452.4 °C against the 456 °C helium hot inlet, so the stage carries 1195.054 of its 1248.568 MW duty and no split between the parallel stages removes the rest (107.234 MW at 0.90, 113.678 at 0.80; 246.223 at 0.50 when the PbLi stream starves; 168.484 at 0.98 when the divertor stream starves).
- **Steady all-checks cases.** Seven of 27 points satisfy every evaluated check: the calculated baseline; the 0.8-recuperation cases at 1600 kg/s in either arrangement (`c3-minus-recuperator`, `network-c3-eps0.8-0.70`, `network-c3-eps0.8-0.85`: net 759.886, gross 1011.896, efficiency 0.3459, turbine inlet 606.2 °C, identical because with all heat removed the turbine inlet follows from the energy balance alone); and the declared resized-compressor alternatives `resized-compressor-1700-network-0.85` (net 891.003, gross 1143.013, efficiency 0.3907, turbine inlet 628.2 °C, compressor demand 1667.033 MW on a 1700 MW rating) and `resized-compressor-1800-series` / `-network-0.85` (net 803.563, gross 1055.573, efficiency 0.3608, 580.8 °C). With the network, complete removal at 0.95 recuperation needs 1700 kg/s where the series arrangement needs 1800 (`resized-compressor-1700-series` leaves 40.013 MW unremoved). The same flows on the inherited 1600 MW rating (`network-c3-1700-0.85`, `network-c3-1800-0.85`) remove all heat and fail the compressor screen; they are retained as adverse points.
- **Against the reference (1253 gross / 1000 net / 708 °C).** No point reaches the reference; the best steady point is 109.98 MW gross and 108.997 MW net short, entirely the thermal-efficiency shortfall (0.3907 against 0.43) at a heat-limited turbine inlet (628 against 708 °C). Net 1000 is reached nowhere in the studied space; the largest net anywhere is 916.263 MW (`network-c1-0.85`, 82.769 MW unremoved). Interaction: the input corrections alone give +46.727 MW net, the network alone at the original inputs +29.409 MW, the combination +83.687 MW (order interaction +7.552 MW); the network step is +29.4 to +44.0 MW net depending on its position in the order (`results/attribution.md`).

## 4. Constraint outcomes

Every generated constraint identity appears below; there are no indeterminate statuses. "Satisfied" means the evaluated scalar check passes, not scientific feasibility.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied / violated | Violated in `network-c3-1700-0.85` (demand 1667.033 MW) and `network-c3-1800-0.85` (1765.094 MW) on the inherited 1600 MW rating; satisfied in the four resized-compressor cases whose rating was raised to the flow. |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied | All 27 (the literal Raffray accounting case is not in this study). |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | satisfied / violated | Violated in 18 of 27: every source-conditioned case at 0.95 recuperation and 1600 kg/s in either arrangement, the original and literal Lyon controls, `network-c3-eps0.8-0.95` (divertor stream starved, 65.110 MW) and `resized-compressor-1700-series` (40.013 MW). |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied | All 27. |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied | All 27. |

Seven cases satisfy every evaluated check: `nominal-calculated`, `c3-minus-recuperator`, `network-c3-eps0.8-0.70`, `network-c3-eps0.8-0.85`, `resized-compressor-1700-network-0.85`, `resized-compressor-1800-series`, `resized-compressor-1800-network-0.85`. Exact predicates and operand provenance are in `results/constraint_catalog.json`.

## 5. Framing

**As proposed at intake.** [AGENT] Every axis is sensitivity-framed: the study measures response to declared input changes and to the declared arrangement; it searches for no boundary and no optimum. The split sweep is a sensitivity, not an optimisation, and the 0.85 default is reported as it was fixed at design time.

| Axis | Framing proposed | Why |
|---|---|---|
| `network_mode` | sensitivity | source-derived arrangement; no branch hydraulic balance or header law resists it. |
| `pbli_split` | sensitivity | operating input; no valve, header or branch hydraulic model responds to it. |
| `compressor_rating` | sensitivity | purchased input; scalar offered-capacity screen only; the resized alternative is a declared hardware change. |
| the 18 round-1 axes | sensitivity | as in the round-1 record § 5; the diagnostic conductance axes (`he_u`, `pbli_u`, `divertor_u`) are declared for composition parity and not varied here. |

**As executed.** Unchanged. No axis was reframed; no case was filtered.

## 6. Per-axis account

#### `network_mode` — feasible structure (search framing)

Not searched. Two values (0 series, 1 network) at fixed hardware.

#### `network_mode` — observed response (sensitivity framing)

At the original inputs the network moves the 158.726 MW PbLi shortfall to the divertor stream (117.863 MW unremoved, net 825.414); at C1 and C2 it removes 43.6 and 48.9 MW of the shortfall (net +39.2 and +44.0); at C3 it removes 41.125 MW (unmet 151.002 → 109.876, net +36.961) and the residual splits between the helium stage (53.514) and the PbLi stream (56.362). Once all heat is removed (0.8 recuperation at 1600 kg/s; 1800 kg/s) the arrangement has no effect on any plant output. Direction only; no monotonicity claim.

#### `pbli_split` — feasible structure (search framing)

Not searched. Eight values at C3 (0.50–0.98), three at 0.8 recuperation (0.70, 0.85, 0.95).

#### `pbli_split` — observed response (sensitivity framing)

At C3 the unremoved heat falls from 246.223 (0.50, all PbLi) to 107.234 MW (0.90) and rises to 139.926 (0.95) and 168.484 (0.98) as the divertor stream starves; net follows (757.153 → 882.067 → 827.020); the PbLi stream outlet falls from 731.4 to 627.9 °C and the divertor stream outlet rises from 479.1 to 700.0 °C (its hot-inlet bound) across the sweep. At 0.8 recuperation the split has no effect between 0.70 and 0.85 (all heat removed) and starves the divertor stream at 0.95 (65.110 MW unremoved). The 0.85 default is not the best sampled value. Sensitivity only.

#### `compressor_rating` — feasible structure (search framing)

Not searched. 1600 (inherited), 1700 and 1800 MW alongside the same cycle flow.

#### `compressor_rating` — observed response (sensitivity framing)

Changes only the compressor screen verdict and the purchase, cost and price channels; no thermal output moves (the 1700 and 1800 kg/s pairs are otherwise channel-identical to their inherited-rating counterparts). Sensitivity only; the alternative's cost consequences are outside this goal.

#### `recuperator_effectiveness`, `cycle_flow`, `divertor_primary_flow`, the auxiliary-load and pump-mode axes, `radiation_fraction`, `exchange_fraction` — feasible structure and observed response

Not searched. Varied only to compose the retained round-1 cases C1, C2, C3 and the steady point (whose values reproduce the round-1 record bit-exactly, `work/active/WI-092_aries-parallel-exchanger-network/evidence/migration-report.json`) and to bracket cycle flow at 1700 and 1800 kg/s. At 0.95 recuperation the network needs 1700 kg/s for complete removal (series: 1800); at 0.8 recuperation 1600 kg/s suffices in either arrangement. Responses are as in the round-1 record § 6; nothing new is claimed for these axes.

#### `he_u`, `pbli_u`, `divertor_u`

Declared, not varied.

## 7. Axis groups

`axes.json` declares 21 single-key groups, disjoint, every key a package input. The three new groups are `aries_integrated_plant__heat_exchangers__network_mode` (code), `aries_integrated_plant__heat_exchangers__pbli_split_fraction` (dimensionless) and `aries_integrated_plant__compressor_capacity__selected_rating` (MW). The preflight sibling scan warns that the seven other `*__selected_rating` keys and the PbLi pump keys are undeclared siblings; deliberate (only the compressor rating is a declared alternative).

## 8. Indicators and rulings

`indicators.json` reports every declared axis as `constraints_reachable` (`network_mode`, `pbli_split`: 6 of 14 executing constraints and 122 of 364 objective channels on a possible path; `compressor_rating`: the compressor screen and downstream cost channels). No axis is `no_constraint_response`, so no user ruling is required before execution. The owner's authorisation of explicitly labelled assumption-sensitivity studies without modelled constraint response applies to the split, the arrangement and the rating as stated below.

**Not derivable, disclosed:** monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path and never a statement that a constraint responds.

**Model-development findings.**

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `network_mode` | No branch hydraulic balance, header or pressure-loss law; the arrangement is a supplied representation of Raffray Fig. 12. | `20260925-aries-revised-reference-network#9` |
| `pbli_split` | No valve, header or branch hydraulic model; a starved stream reports unmet heat, nothing redistributes flow. | `20260925-aries-revised-reference-network#4` |
| `compressor_rating` | No compressor map or purchase response beyond the scalar screen and the linear cost account. | `20260925-aries-revised-reference-network#8` |
| the 18 round-1 axes | as in the round-1 record § 8 (`…reconciliation#1`–`#6`). | round-1 ids |

## 9. Preflight results

From `preparation/preflight_results.json` (run on the amended manifest; see § 13).

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 21 declared keys across 21 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass, warnings | PbLi pump keys and the seven other `selected_rating` keys are undeclared siblings; deliberate |
| Identity | pass | sealed digest `f739dbce…` recomputed; every sealed artifact matches |
| Manifest / package fingerprint match | pass | both recorded fingerprints match the package on disk (`preparation/package_identity.json`) |
| Baseline gate against the pinned headline | pass | `aries_integrated_plant__lifecycle_price__evaluate__lcoe` reproduces at relative deviation 0; 2/2 pinned verdicts match (`preparation/baseline_result.json`) |
| Package cleanliness | pass | package tree byte-untouched |

## 10. Execution route and why

- **Route:** study-local direct-API (stock `StudyRunner` with `PreparedListStrategy` over complete declared input maps, through `revised_reference_support.py`, which reuses the round-1 composer `reconciliation_support.proposals` and the retained predecessor executor `20260922-aries-integrated-lcoe/execute_study.py`).
- **Why this route:** the declared cases are named full maps composed on canonical bases and on each other; the strict loader, fingerprints, store lease and full-map exporter are reused unchanged. Canonical bases come from `canonical-replay-receipt.json`, the mode-0 replays of the four canonical maps executed on this package (WI-092 development receipt), because the predecessor's receipt carries the earlier package identity and lacks the two new entry keys.

**Glue disclosure.** glue ledger: none. No adapter on this route, so nothing is harness-supplied.

## 11. Study definition and window provenance

The candidate range was scanned with the package-owned independent oracle (`oracle-window-scan.json`, 27 of 27 evaluated, none refused). Windows are declared per axis in `axis-plan.json`: the network mode is sourced (Raffray Fig. 12); the split window 0.50–0.98 is engineered (no source states it; the Raffray duty shares imply ≈ 0.89 for equal branch rises); the compressor rating 1700/1800 MW is engineered (set equal to the flow-implied demand rounded up, as a declared alternative); the round-1 windows are unchanged.

## 12. Cross-fingerprint correlation and what it means

single fingerprint — no cross-arm correlation needed.

## 13. Verification

All 27 stored cases were verified against the package-owned independent oracle (`scripts/study/verify.py`, sample size 27, stratified over the three observed verdict combinations): 364 numeric channels per case at relative 1e-9 or a declared absolute tolerance, and all 14 predicates re-derived exactly (`results/verification_summary.json`, outcome `pass`). Six absolute tolerances apply: the two inherited (`residual_magnitude` 1e-7 MW, `idc` two ULP) and four declared for this study on the unmet-heat channels (`unmet_heat`, `he_unmet`, `pbli_unmet`, `divertor_unmet`; 1e-7 MW each). The largest relative deviation reported is 4.1e+04 at `aries_integrated_plant__plant_ledger__evaluate__residual_magnitude` in `network-c1-0.85` (c0008), a near-zero residual channel that passes its declared absolute tolerance, as in the round-1 record.

**Attempt history (finding #7).** Attempt 1 executed all 27 points and its all-point verification refused `he_unmet` in `network-c2-0.85` (store 2.028448680648353 MW, oracle 2.0284486773855406 MW, relative 1.609e-9 against the 1e-9 rule, absolute 3.3e-9 MW, no absolute tolerance declared). The unmet-heat channels are differences of order-1000 MW duties fixed by a root solve terminating at 1e-8 MW, so two correct solvers agree on them only to that order; the largest store-versus-oracle difference on the four channels over the 27 points is 4.84e-9 MW. An absolute tolerance of 1e-7 MW on exactly those four channels, the same allowance as the reviewed `residual_magnitude` precedent, was declared (`…/evidence/unmet-tolerance-declaration.md`), independently reviewed (`…/evidence/unmet-tolerance-review.md`: PASS, notes only; verdict parity confirmed on the stored data) and added to the live and record manifests; indicators and preflight were rerun on the amended manifest; the 27 points were re-executed into fresh `results/` (attempt 1 retained under `results-attempt1/`, with its refused verification log at `…/evidence/t004-verify-attempt1.log`), and `results/attempt-comparison.json` shows every one of the 14,877 stored channels, every input and every verdict identical between the attempts. `preparation-provenance.json` keeps the manifest sha256 from before the amendment; `indicators.json` and `results/manifest_used.json` carry the amended manifest.

## 14. Review outcomes

- Design review of the WI-092 increment (fresh, r1 FINDINGS → r2 PASS, MR-7 compliant): `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/design-review.md`.
- Implementation review of the executed increment (fresh, PASS with four notes, MR-7 compliant on executed evidence): `…/evidence/implementation-review.md`; dispositions in `work/active/WI-092_aries-parallel-exchanger-network/evidence/implementation-review-notes.md`.
- Tolerance declaration review (fresh): `…/evidence/unmet-tolerance-review.md` (see § 13).
- Round-2 review of this reading: pending at the round result.

## 15. Findings

| Id | Kind | Finding | Proposed disposition |
|---|---|---|---|
| `20260925-aries-revised-reference-network#1` | model | The published network removes the series-order PbLi limit (41.125 MW of the 151.002 MW C3 shortfall at the same hardware) but at 1600 kg/s and 0.95 recuperation the blanket-helium stage binds (cycle helium leaves 3.6 K below the 456 °C helium hot inlet), leaving 107–114 MW unremoved at every split from 0.80 to 0.90. | Structural result on the reviewed increment; ledger mechanism 2. |
| `…#2` | model | With the network, complete removal at 0.95 recuperation needs 1700 kg/s (series: 1800); the compressor demand 1667 MW exceeds the assumed 1600 MW rating (A6). The declared resized alternative (rating 1700 MW) is the best steady all-checks point: net 891.003, gross 1143.013, efficiency 0.3907, turbine inlet 628.2 °C. | Bounded result; a declared hardware change, never a reproduction; ledger and answer. |
| `…#3` | model | Once all heat is removed the arrangement has no effect on any plant output (identical channels at 0.8 recuperation / 1600 kg/s and at 1800 kg/s in both modes): the turbine inlet then follows from the energy balance alone. | Declared property; write-up. |
| `…#4` | model | The split has a broad low between 0.80 and 0.90 at C3 (unmet 113.7–107.2 MW, net 876–882); below 0.60 the PbLi stream starves (246 MW at 0.50), above 0.95 the divertor stream starves (88–149 MW). Nothing redistributes flow; the 0.85 default is not the best sampled value. | Declared seam (no branch hydraulic balance); sensitivity only, no optimum claimed. |
| `…#5` | model | The order interaction between the input corrections and the network is +7.552 MW net (sum 76.135, combined 83.687) and −0.263 MW unmet; the network step is +29.4 to +44.0 MW net by position. | Recorded; the ledger accounts for the combined difference. |
| `…#6` | model | The best steady point is 108.997 MW net and 109.987 MW gross short of the reference, entirely the efficiency shortfall at the heat-limited turbine inlet (628 against 708 °C); with the published duties the network cannot reach 708 °C at any split (PbLi stream at most 731 °C when starving the divertor, 655 °C at 0.85, mixed with the cooler divertor stream). | Explained difference in meaning; quantifies Q1 in the model; owner-visible premise carried in the answer. |
| `…#7` | process | All-point verification refused one unmet-heat channel by 1.609e-9 relative (3.3e-9 MW on 2.03 MW): solver-tolerance class on a difference channel. An absolute tolerance of 1e-7 MW on the four unmet channels was declared, independently reviewed and applied; the points were re-executed and compared bit-for-bit with attempt 1. | Process note; tooling seam (relative-only rule on difference channels). |
| `…#8` | model | `compressor_rating`: no compressor map or purchase response beyond the scalar screen and the linear cost account; the resized alternative's cost consequences are outside this goal. | Declared seam. |
| `…#9` | model | `network_mode`: no branch hydraulic, header or pressure-loss law; the arrangement is a supplied representation of Raffray Fig. 12 with adiabatic mixing. | Declared seam (WI-092 assumptions N2, N3). |

## 16. Snapshot

`snapshot.json` (sha256 `c6551b7172a567db1fac5c43f14f7cbdc8169283ffa6b47d73c4f0fe4025a738`) records the package identity (`exploration/aries_integrated/aries_integrated` at repo commit `4f5991a5`, git-clean), the three fingerprints (indicator inputs `06e0627ca37475e7…`, executable `f739dbce…`, semantic `78dd23bf…`), the amended manifest content used (six absolute tolerances), the single arm `arm-diagnostic` with its store compatibility tuple, the verification command and tool digest, 273 hashed record artifacts (attempt-1 results included), the TEAx revision `8d877460…` through the integration return, 27 cases with [551] numeric outputs each, 364 verified channels and 14 exact verdicts per case, and 7 cases with every scoped check satisfied. `sealed-package.tar.gz` holds the executed package bytes; `results/sources/` retains the tools, route, support and reporting modules, the WI-092 record and evidence, the goal evidence and the model files at freeze.

## 17. What this record does not contain

- No claim that any case reproduces the ARIES operating point: the best steady point is ≈ 110 MW gross short and outside the ±15 MW budget; the source-conditioned network case at the 1600 kg/s convention still leaves 109.876 MW unremoved and is not a steady operating point.
- No optimum for the split, the cycle flow or the recuperation; no monotonicity claim.
- No hydraulic, pressure-loss or control-law statement for the parallel branches; no compressor map; no cost conclusion for the resized alternative.
- No prediction credit for the supplied fusion power (2436 MW), the supplied arrangement or the supplied split.
- No change to the Stellaris model, its package or any frozen record; the original series closure remains bound as mode 0 and reproduces bit-exactly.
