# Integrated ARIES heat/electricity study

## 1. Study header

- **Study id:** `20260922-integrated-heat-electricity`
- **Package:** `aries_integrated`
- **Date executed:** 2026-09-22
- **Executor:** Codex study executor, coordinated under the integrated ARIES goal.
- **Mode:** execute
- **Arms:** single arm, `combined-sensitivity`; fourteen declared points.

[AGENT] Execution, numerical verification and record preparation are complete. This record is ready for the coordinator's immutable commit. Native candidate evidence is copied in `results/integration/`; the execution checkout is `a8912fa4cb9356f14dc18bee4eec841792f544a8`.

## 2. Intake

[OWNER-VERBATIM] “I would like to continue working until we get to an integrated ARIES model, making the best assumptions we can as needed along the way.”

[OWNER-VERBATIM, issued brief] “Include sufficient/insufficient fixed-equipment cases and at least one supported demand perturbation with hardware held constant. Retain adverse points; never filter failures to manufacture a feasible region.”

[INHERITED: copied owner and execution briefs under results/sources/work/orchestration/goals/aries-integrated-heat-electricity/evidence/] Run one connected source/calculated-mode study with distinct literal reconstructions, native identities, explicit assumptions and no changes to original Stellaris evidence.

[AGENT] The fourteen-point list combines four canonical configurations and bounded density, offered-rating, compression-ratio and conductance perturbations. No point or hardware value was changed during execution.

## 3. Objective and result

LCOE objective and result: not applicable; this thermal/electrical study contains no cost model. The calculated nominal delivers **423.106794 MW net**, accepts **2240.389047 MW heat**, has zero unmet duty and satisfies all ten scalar predicates. Its source is **1835.451283 MW** from supplied plasma profiles. This is a conditional integrated calculation, not a reconstruction of the published plant or qualification of its unsupported physics.

All fourteen points complete. Eight satisfy all ten predicates; six retain engineering violations. Exact floats, all 211 native numeric outputs and all ten verdicts are in `results/cases.json` and SQLite. The declared CSV contains 187 output columns. The table rounds display values only.

| Case | Selected fusion MW | Accepted heat MW | Unmet heat MW | Net electricity MW | Predicates satisfied |
|---|---:|---:|---:|---:|---:|
| nominal-calculated | 1835.451283 | 2240.389047 | 0.000000 | 423.106794 | 10/10 |
| nominal-source-assumed | 2436.000000 | 2759.082152 | 158.725848 | 796.005288 | 9/10 |
| literal-Lyon-source-input | 2436.000000 | 2518.899476 | 398.908524 | 807.016660 | 9/10 |
| literal-Raffray-accounting | 2365.000000 | 2517.615798 | 502.134202 | 805.910865 | 8/10 |
| density-low | 1486.715539 | 1847.015128 | 0.000000 | 140.230696 | 10/10 |
| density-high | 2220.896052 | 2675.170747 | 0.000000 | 735.759323 | 10/10 |
| fuel-rating-low | 1835.451283 | 2240.389047 | 0.000000 | 423.106794 | 9/10 |
| fuel-rating-high | 1835.451283 | 2240.389047 | 0.000000 | 423.106794 | 10/10 |
| helium-rating-low | 1835.451283 | 2240.389047 | 0.000000 | 423.106794 | 9/10 |
| helium-rating-high | 1835.451283 | 2240.389047 | 0.000000 | 423.106794 | 10/10 |
| compressor-ratio-low | 1835.451283 | 2240.389047 | 0.000000 | 470.897994 | 10/10 |
| compressor-ratio-high | 1835.451283 | 2240.389047 | 0.000000 | 366.692730 | 10/10 |
| helium-ua-low | 1835.451283 | 2193.270440 | 47.118607 | 389.195517 | 9/10 |
| helium-ua-high | 1835.451283 | 2240.389047 | 0.000000 | 423.106794 | 10/10 |

The calculated nominal's native gross generation is 655.354927 MW, 597.645073 MW below the Lyon gross reference. Its net difference is -576.893206 MW against the published 1000 MW basis. These native comparison channels are not an accuracy pass: profiles, topology and equipment assumptions differ. The source-conditioned and literal cases remain thermally inadequate despite positive computed export.

## 4. Constraint outcomes

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied in all 14 | No observed violation |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied in all 14 | No observed violation |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | violated in 1; satisfied otherwise | fuel-rating-low |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied in all 14 | No observed violation |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | violated in 1; satisfied otherwise | helium-rating-low |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied in all 14 | No observed violation |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | violated in 1; satisfied otherwise | literal-Raffray-accounting |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | violated in 4; satisfied otherwise | nominal-source-assumed, literal-Lyon-source-input, literal-Raffray-accounting, helium-ua-low |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied in all 14 | No observed violation |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied in all 14 | No observed violation |

All ten exact IDs are preserved. Local name `capacity_ok` is reused by eight occurrences; names alone do not identify those predicates. Unsupported scientific flags remain zero and do not become passed science checks merely because these ten scalar predicates pass.

## 5. Framing

Proposed and judged framing: **sensitivity** for every declared group; unchanged after execution. Density, ratings, conductance and compression show the expected kinds of response. The producer/source/heat-mode groups distinguish explicit scenarios; changes bundled in a source reconstruction are not attributed to one axis alone. No search, constrained optimum, monotonicity theorem or feasible-region boundary is claimed.

## 6. Per-axis account

#### density_amplitude — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### density_amplitude — observed response (sensitivity framing)

**Applies:** yes. Low/high density give fusion 1486.715539/2220.896052 MW and net electricity 140.230696/735.759323 MW. Fuel exhaust, three branch duties, turbine temperature/work and fuel-variable electric demand respond. All 121 other public inputs remain equal to nominal, including every hardware choice. Neither point violates a predicate. No boundary or optimum is claimed.

#### fuel_rating — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### fuel_rating — observed response (sensitivity framing)

**Applies:** yes. The lower offered processing rating fails only the fuel-capacity predicate; the higher rating passes. Physical outputs and demand remain unchanged. No boundary or optimum is claimed.

#### helium_rating — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### helium_rating — observed response (sensitivity framing)

**Applies:** yes. The lower offered thermal rating fails only helium capacity; the higher rating passes. Physical outputs and demand remain unchanged. No boundary or optimum is claimed.

#### compressor_stage_1_ratio — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### compressor_stage_1_ratio — observed response (sensitivity framing)

**Applies:** yes. The lower/higher first-stage ratios give net electricity 470.897994/366.692730 MW. Stages two and three and all other hardware remain fixed. All ten predicates pass both points. No boundary or optimum is claimed.

#### helium_exchanger_ua — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### helium_exchanger_ua — observed response (sensitivity framing)

**Applies:** yes. Lower conductance gives 47.118607 MW unmet heat and net electricity 389.195517 MW, failing heat removal. Higher conductance gives no unmet heat and unchanged nominal net electricity 423.106794 MW. Other hardware choices are fixed. No boundary or optimum is claimed.

#### producer_mode — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### producer_mode — observed response (sensitivity framing)

**Applies:** yes. Source-conditioned nominal uses the published 2436 MW input and fails heat removal by 158.725848 MW; calculated nominal uses supplied profiles and closes thermal removal. This is a named mode comparison, not independent agreement with the published source. No boundary or optimum is claimed.

#### source_fusion — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### source_fusion — observed response (sensitivity framing)

**Applies:** yes. The 2365 MW Raffray reference occurs only in the separately labeled literal accounting scenario. Its simultaneous source-accounting changes prevent attributing the difference to source power alone. No boundary or optimum is claimed.

#### heat_accounting_mode — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### heat_accounting_mode — observed response (sensitivity framing)

**Applies:** yes. Literal Raffray accounting retains supplied deposition and exchange, 502.134202 MW unmet heat and 182.03 MW source-energy discrepancy. It fails heat removal and balances; it is not combined silently with the nominal partition. No boundary or optimum is claimed.

#### recuperator_effectiveness — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### recuperator_effectiveness — observed response (sensitivity framing)

**Applies:** yes. The literal Lyon scenario changes source-conditioned recuperation from nominal 0.8 to 0.95 and gives 398.908524 MW unmet heat with 807.016660 MW net. Source duty is retained; the larger export does not establish thermal adequacy. The Raffray case also uses 0.95 but has additional source changes. No boundary or optimum is claimed.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| density_amplitude | `aries_cs_plasma_integration__plasma__amplitude` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| fuel_rating | `aries_integrated_plant__fuel_capacity__selected_rating` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| helium_rating | `aries_integrated_plant__he_capacity__selected_rating` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| compressor_stage_1_ratio | `aries_integrated_plant__compressor_1__selected_ratio` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| helium_exchanger_ua | `aries_integrated_plant__heat_exchangers__he_ua` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| producer_mode | `aries_integrated_plant__source__producer_mode` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| source_fusion | `aries_integrated_plant__source__reference_fusion_mw` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| heat_accounting_mode | `aries_integrated_plant__deposition__heat_mode` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |
| recuperator_effectiveness | `aries_integrated_plant__cycle__recuperator_effectiveness` | fan_out | One actual public source attribute; downstream fan-out is model-owned. |

Complete changed and held values live in `proposed-points.json` and stored case inputs. `results/propagation-and-input-preservation.json` proves exact agreement for all fourteen point maps. External ties: none; the similarly named ratings and stage ratios belong to different chosen hardware attributes.

## 8. Indicators and rulings

All nine native groups report `constraints_reachable`; no proposed group was declined. The complete report is `indicators.json`. No `no_constraint_response` case arose, so its conditional owner ruling and missing-pushback finding are not applicable here.

[OWNER-VERBATIM, issued brief] “For this prompt, I authorize explicitly labeled diagnostic/sensitivity-only sweeps of declared assumptions even when no modeled constraint resists them. Record the missing constraint response and development finding before execution.”

Indicators do not establish monotonicity, same-quantity identity across differently named keys or within-module operand dependency. Reachability denotes a possible path; observed response is supported separately by stored values. `unresisted` remains an executor judgment, not an indicator output.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Native integration | PASS | All ten gates in `results/integration/integration_return.json`; sole promoted candidate |
| Declared-group key validation | PASS | Nine keys in nine full groups |
| Suffix-sibling scan | PASS with 14 warnings | Independent equipment ratings and compressor-stage ratios share suffixes; they are separate attributes, not omitted members of a tie |
| Sealed identity | PASS | Recomputed sealed identity in `results/integration/package_identity.json` |
| Manifest / package fingerprint match | PASS | Actual executable and semantic identities match |
| Baseline headline | PASS | Exact headline match; two uniquely named baseline predicates match |
| Package cleanliness | PASS | Checked before and after study; `results/preflight_results.json` |
| Baseline file-read coverage | PASS within stated scope | `results/integration/read_coverage.json`; baseline Python-observable reads only |

The integration's pre-execution baseline/preflight evidence was reused for this same manifest, complete groups and package. A study-local preflight reconfirmed all six checks after execution. The fourteen suffix warnings list twelve independently chosen capacity ratings and two other compressor-stage ratios. They do not authorize tying those choices. The baseline gate's two local-name predicates do not individually certify the eight repeated capacity names; the store and verifier check every full ID.

## 10. Execution route and why

**Route:** study-local direct API using `PreparedEvaluator`, `PreparedListStrategy`, `StudyRunner`, `StudyStore` and `StudyQuery`. The list coordinates named scenarios and single-choice perturbations without an unnecessary Cartesian grid. Integration proved the strict stock route before the study ran. All advertised physical quantities come from the generated graph.

**Glue ledger: none.** No caller-side physical adapter or oracle value enters runtime. Package-owned typed completion adapters are part of the sealed native calculation package. Route/checker/tool sources are copied under `results/sources/`. Replay commands in `replay.md` use a fresh temporary directory and never invoke the author script that overwrites baseline evidence.

## 11. Study definition and window provenance

The engineered windows were chosen after the retained independent development scan, not tuned after native results. Density changes create a visible upstream response while holding hardware fixed. Offered-rating pairs test inadequate and sufficient scalar capacity. Conductance includes an inadequate transfer choice; ratio perturbations leave other stages fixed. All adverse source reconstructions remain in the list. Exact windows and held values are in the snapshot and point maps. The scan is a numerical planning check under declared assumptions, not source validation or a physical boundary search.

## 12. Cross-fingerprint correlation and what it means

**Single study fingerprint; no cross-arm correlation needed.** All fourteen stored points use `cebe17fd3ca0dae4c5102365b384cc40635406b3c470c29dd7f55c086b9657bd`. Earlier development receipts retain their old executable identity. T-007's normalized package has separate parity and checker receipts; the older receipts were not relabeled as this study's executions.

## 13. Verification

**PASS:** every one of the fourteen stored cases was sampled across all five observed verdict combinations. Verification checks thirty selected channels per case (**420 scalar comparisons**) and independently rederives all ten exact verdicts (**140 comparisons**), with zero verdict mismatch.

The relative rule remains 1e-9 except for the explicitly reviewed residual-only 1e-7 MW absolute allowance. The actual worst relative discrepancy, 18619, remains reported for that near-zero residual; it is not hidden by the passing absolute check. Original relative-only refusals and the reviewed correction are retained. The model's engineering balance tolerance is unchanged.

Coverage is thirty of 211 native numeric channels, not every output. The checker uses the same accepted equations/fit coefficients but independent adaptive integration and Brent solving. It does not independently validate nuclear data, profiles, deposition transport, assumed capacities, hydraulics, magnets, breeding, material limits or machine maps. `not_independently_verified: []` in the native summary describes its input-binding category; it does not mean universal channel or scientific coverage.

The native summary's TEAx revision field remains `unrecorded`. `results/runtime-identity.json` resolves the actual clean revision from accepted integration and the source checkout without altering the producer output.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| WI-089 source/math/ownership design review | PASS | Reused reviewed physical approximation and positive selected-power domain; copied source review |
| Native implementation and integrated behavior review | Accepted by coordinator before execution | Existing broad model review reused; no source/physical changes in this study |
| T-005 residual verification change | PASS | Copied independent review; explicit manifest declaration applied |
| Typed completion/census packaging corrections | Accepted before candidate | Existing scoped reviews reused; package identity and semantic preservation recorded |
| Executor record checks | PASS | Exact point maps, output/verdict retention, snapshot consistency and artifact digests checked |

The executor does not claim an independent cold reading of this record. The coordinator's subsequent review of the committed record is outside this executor-authored artifact.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| 20260922-integrated-heat-electricity#1 | process | Eight capacity occurrences share local name capacity_ok; the native baseline manifest cannot uniquely pin them by local name. | Retain the scoped two-predicate baseline gate; store/export and independently rederive every full predicate ID. | scripts/study/manifest.py; scripts/study/preflight.py |
| 20260922-integrated-heat-electricity#2 | process | Relative-only parity rejects negligible numerical residual differences. | Resolved by independently reviewed T-005: explicit 1e-7 MW comparison allowance on residual_magnitude alone, with exact verdict parity unchanged. Original refusals retained. | scripts/study/verify.py; .project/active/study-residual-tolerance/review.md |
| 20260922-integrated-heat-electricity#3 | model | The calculated nominal executes a connected chain with 423.106794 MW net, no unmet heat and all ten scalar predicates satisfied. | Retain as a conditional integrated result under supplied profiles and assumed equipment; no published-plant feasibility or scientific qualification claim. | work/active/WI-089_aries-integrated-heat-and-electricity/design.md |
| 20260922-integrated-heat-electricity#4 | model | The source-conditioned and both literal source scenarios fail heat removal; literal Raffray also retains a 182.03 MW source-energy discrepancy. | Keep all adverse cases and distinct source labels; use source reconciliation/thermal design refinement before stronger published-plant claims. | work/active/WI-089_aries-integrated-heat-and-electricity/design.md |
| 20260922-integrated-heat-electricity#5 | model | Density changes propagate through fuel, branch heat, cycle state, fuel electricity and net output with all hardware inputs unchanged. | Accept the fixed-hardware propagation evidence; retain supplied-profile and approximate-transport limits. | models/designs/aries_cs_integrated/plant.sysml |
| 20260922-integrated-heat-electricity#6 | model | Low independently offered fuel and helium ratings fail their own capacity predicates at unchanged physical demand and net output. | Retain insufficient/sufficient pairs; do not infer automatic sizing or actual equipment qualification. | models/designs/aries_cs_integrated/plant.sysml |
| 20260922-integrated-heat-electricity#7 | model | Lower helium UA produces unmet duty; independently changed first-stage compression changes export without resizing other equipment. | Retain bounded sensitivity results; no optimum, general monotonicity or machine-map claim. | models/library/analyses/integrated_heat_electricity.sysml |
| 20260922-integrated-heat-electricity#8 | process | The verifier summary reports TEAx revision as unrecorded despite an accepted integration revision. | Keep the producer output unchanged; snapshot records the matching integration and clean checkout revision with explicit evidence. | scripts/study/verify.py |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `e888d008f2e740129bdbb39f359a619df53a2d9d6fd789a1df40a982a2bbc4ca`
- **Schema version:** `1`

All values are resolved. The manifest content includes the residual tolerance declaration; store compatibility, source/tool digests, runtime revision and result hashes are copied into the snapshot.

## 17. What this record does not contain

This record contains no cost estimate, LCOE result, equipment purchase recommendation, independent published-plant reproduction or verified magnetic/breeding/material/machine-map capability. These are scope limits, not missing stored outputs. There is no separate independent administrator synthesis here. The archive contains the generated package and the required source/metadata/review copies; recreating its external Python environment remains a replay prerequisite identified by the recorded toolchain versions and revision.
