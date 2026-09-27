# Study record — exchanger architecture

## 1. Study header

- **Study id:** 20260926-design-study-exchanger-architecture
- **Package:** unchanged aries_integrated; goal-owned record under exchanger_architecture
- **Date executed:** 2026-09-26 local time (execution completion UTC 2026-09-27)
- **Executor:** delegated native worker; reporting worker; coordinator executor synthesis
- **Mode:** execute
- **Arms:** arm-architecture

648 unique retained maps completed once. Two explicit candidate aliases resolve to those maps. There were no native refusals or execution retries. Exact command/runtime/context evidence is in results/execution-context.json and results/execution-completion.json.

## 2. Intake

> How does connecting the available heat exchangers in series versus a series-then-parallel network change the usable operating range and cost of electricity? Is there a range where the connection choice makes one design preferable, once heat removal, equipment and architecture-specific costs are accounted for?

[OWNER-VERBATIM] Intake above; full owner brief retained as owner-brief.md. [AGENT] The declared comparison uses supplied source powers at fixed deposition assumptions, 20 MW heating and unchanged hardware. It is a downstream comparison, with no claim of sustained plasma or physically closed blanket design. comparison-contract.md carries the reviewed scope. The sampled source, flow and split grid is an executor choice within that scope.

## 3. Objective and result

**Objective channels:** `aries_integrated_plant__plant_ledger__evaluate__net_electric` and `aries_integrated_plant__lifecycle_accounts__evaluate__lcoe_sum`. Complete native outputs are in results/cases.json and cases.csv. Every positive-output case is preserved, including engineering failures.

648 cases completed; 397 pass all implemented predicates and 251 fail. The 432 primary cases contain 247 native passes and 185 failures, all involving heat removal. Paired economics are restricted to common-source passing cases. The report and tables in results/reporting provide full decomposition, tested operating choices and case IDs. Neither native pass nor finite LCOE establishes scientific qualification.

## 4. Constraint outcomes

Every executing constraint is listed by qualified identity. Per-case verdicts and catalog operands remain in results/cases.json and results/constraint_catalog.json.

| constraint_id | source_local_identity | satisfied | violated | other |
|---|---|---:|---:|---:|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | 397 | 251 | 0 |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | 648 | 0 | 0 |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | 648 | 0 | 0 |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| source_mode | sensitivity | 1 calculated control; 0 supplied downstream family; no sustained plasma claim |
| source_load | search | Supplied common-load boundary; exact nominal source anchor and engineered 1650–2600 MW window |
| architecture | search | Existing series or series-then-parallel connection graph |
| cycle_flow | search | Same four supplied operating choices for both architectures; installed capacities fixed |
| branch_split | search | Supplied network operating choice; inert .85 placeholder in series |
| conductance_uncertainty | sensitivity | [AGENT] correlated 0.8/1.2 multiplier on each inherited U; shared uncertainty, no physical identity or hardware change asserted |
| pressure_loss | sensitivity | Common .02/.08 sensitivity and network .08 differential against inherited .045 series |
| pump_mode | sensitivity | [AGENT] coordinated switch to existing fixed-power mode 1 for all pumps |
| pump_power | sensitivity | [AGENT] coordinated 0.8/1.2 multiplier on each own reference power; preserves distinct powers and existing heat recovery |
| tritium_price | sensitivity | [AGENT] selected zero-price bookkeeping endpoint within owner-authorized fuel sensitivity; reprices annual purchases and initial stock; no breeding claim |

**As judged after the run:** all proposed framings retained. Search axes expose a sampled heat-removal boundary and differences in feasible operation. Sensitivities test conditional response; none establishes its own physical boundary. Source_load has a series edge bracketed by 2500 passing and 2600 failing on the offered flow grid; the network upper edge remains uncaught. The lower tested cycle flow is a domain choice, not an optimum.

## 6. Per-axis account

**source_mode — sensitivity:** the original calculated N control reproduces all 551 historical outputs and 14 predicates; the supplied-source counterpart reproduces 549 downstream outputs and all predicates, differing only in two source-mode labels. No plasma sustainment claim is introduced.

**source_load — search:** all loads 1650–2500 MW have passing tested points in both arrangements; at 2600 MW only the network has passing tested points. This is a sampled extension on the four-flow grid. The network upper boundary is not located.

**architecture — search:** equal source, cycle operation and fully accepted heat give equal modeled output. At source loads 2200, 2300, 2350, 2450 and 2500 MW the network accepts all heat at a tested flow 100 kg/s below the best passing series flow, gaining about 68.361 MW. Six other common loads tie. Unpriced topology differences remain absent.

**cycle_flow — search:** the same four chosen flows are evaluated in both graphs with unchanged installed hardware. The best passing tested flow depends on heat removal; all selected equipment checks pass throughout the primary grid. The discrete switches between flows are grid effects, not continuous optimum claims.

**branch_split — search:** network passing subsets are bounded by the competing PbLi and divertor duties. Earlier failure at supplied split .85 is not an architecture-wide failure. All tied passing splits within .01 MW are retained in reporting; choosing a representative never hides the tied alternatives.

**conductance_uncertainty — sensitivity:** correlated U ×0.8/1.2 at unchanged area preserves the best-tested power advantage at both 2200 and 2300 MW. It changes terminal diagnostics and some passing subsets. No changed hardware or purchasable U improvement is claimed.

**pressure_loss — sensitivity:** at 2200 MW common .08 loss removes the best-tested network advantage; at 2300 MW common .02 removes it. Higher network-only loss can change preference among passing modeled cases. The fixed preselected network controls also fail heat removal under .08; they are retained separately from reselection among already tested cases.

**pump_mode and pump_power — sensitivities:** existing fixed-power mode is tested at ×0.8/1.2 of each pump’s own reference power, with recovered friction heat coupled through the native source. At 2200 MW ×1.2 removes the best-tested advantage; at 2300 MW ×0.8 removes it. Neither pump law establishes a hydraulic map or split achievability.

**tritium_price — sensitivity:** the zero-price bookkeeping endpoint reprices native initial stock and annual purchases at unchanged thermal behavior. The paired sign at gain points survives but shrinks from roughly 58–68 USD2004/MWh to 4.4–5.8. This endpoint is agent-selected, not a source-supported fuel-supply design or market assumption.

## 7. Axis groups

The complete 16 qualified entry keys and their fan_out/tie provenance are in axes.json; the proposed roles and windows are in axis-plan.json. Ties are declared in the local manifest. U multipliers are a shared uncertainty across three distinct exchangers; pump power multipliers scale each pump’s own reference power; mode switches select the existing fixed-power calculation. These are coordinated scenarios, not claims that distinct hardware has identical physical quantities. Every composed complete point is checked for exact public-key coverage, finite values and changes only within declared groups. Identical full maps are represented by aliases, never executed twice.

## 8. Indicators and rulings

All ten groups have `no_constraint_response=false` in indicators.json. These are possible graph paths, not observed constraint response. No group has the sound-negative no_constraint_response indicator that requires an owner framing ruling before execution; indicators do not themselves mechanically gate a study. The oracle selection and later native outcomes must establish actual behavior.

[AGENT] Tritium price is economically unresisted: no market, breeding, extraction or sustainable supply model constrains its chosen endpoint. The zero-price endpoint is AGENT-selected within the owner’s explicit instruction to test consequential fuel assumptions (owner-brief.md, common requirement 6 and class-specific economics). It is a bookkeeping sensitivity that also reprices initial stock, never an optimization or achievable breeding scenario. Pressure loss, pumping and conductance likewise remain assumption sensitivities with their missing hydraulic/material/transport evidence recorded in the contract. No additional owner ruling is inferred from graph reachability.

Not derivable from indicators: channel monotonicity, physical identity across different key names, or intra-module operand dependency. The price-authority correction is recorded in preparation-authority-correction.json; earlier indicator/preflight outputs remain under attempt1 names.

## 9. Preflight results

All six gates pass in preparation/preflight_results.json: declared keys, sibling scan, sealed identity, manifest currency, exact pinned headline and git-clean package. preparation/baseline_result.json and package_identity.json are emitted by the native stock route. preparation/control-replay.json verifies the historical calculated N exactly on 551 outputs and 14 verdicts, then the exact supplied-power replay on 549 downstream outputs and all verdicts. Only selected_mode and net_result_producer_mode change. Assertions: baseline pressure loss 0.045, calculated source mode 1, supplied source mode 0, exact source 1835.4512830147435 MW.

## 10. Execution route and why

**Route:** study-local direct API using unchanged `StudyRunner` and `PreparedListStrategy`, through the stock strict ARIES loader. The coordinated operating grid, paired uncertainty blocks, explicit control aliases and oracle-selected bookkeeping endpoints require a finite list of complete maps. The route has loaded successfully for the pinned baseline and control replays. `exploration/exchanger_architecture/execute_study.py` binds the local manifest and reuses the historical exact-full-map exporter unchanged.

**Glue ledger: none.** The wrapper supplies no physical arithmetic, constraints or model outputs. The goal-owned preparation composer preserves full-map validation and declared-key checks while allowing honest search/sensitivity framing; it does not invoke the sensitivity-only reconciliation composer.

## 11. Study definition and window provenance

The engineered window was inspected with the independent package-owned oracle before main execution. It contains 12 supplied powers from 1650 to 2600 MW including exact 1835.4512830147435, four flows 1300–1600 kg/s and eight network splits; series gets one inert split at every matching power/flow. All 432 main points remain, including engineering failures. The 192 paired uncertainty points cover source powers 2200 and 2300 MW, four flows, series plus splits 0.65/0.75/0.85, with U ×0.8/1.2, pressure loss 0.02/0.08 or fixed primary pump power ×0.8/1.2.

The original calculated N adds one unique control; exact supplied N aliases a main point. oracle-selection.json retains every tie within 0.01 MW and explicitly selects the lowest flow, then lowest split among ties for follow-up controls. Eleven loads have a passing tested pair, so 22 zero-price maps are added. No series case passes at 2600 MW, so no paired zero-price map is invented there. Two topology-specific 0.08 network-loss controls compare against inherited 0.045 series: the 2300 MW control aliases an existing uncertainty case, while 2200 MW adds one unique case.

The full candidate ledger therefore has 648 unique retained maps and two aliases. Every point executes in the oracle with positive net power; no numerical validity mask or refusal exclusion was needed. `oracle-initial-scan.json` preserves the 625 initial maps; `oracle-window-scan.json` contains all 648. This does not remove any engineering failure. The series upper passing edge is sampled between 2500 and 2600 MW; the network upper edge is not caught by the supplied window. The lower flow edge is an imposed tested window, not a discovered optimum. Frozen native execution may change a finding only through recorded verification evidence.

## 12. Cross-fingerprint correlation and what it means

Single unchanged package fingerprint; no cross-package correlation needed. Series/network are selectable existing graphs within the same package and complete maps are stored for every candidate.

## 13. Verification

**PASS, every retained point:** results/verification_summary.json compares all 648 rows, 364 scalar channels and all 14 independently rederived predicates, using the unchanged relative tolerance 1e-9 and named absolute tolerances. No mismatch, numerical window change or relaxed tolerance was used. All 551 native outputs are retained. results/execution-completion.json summarizes the checks and clean-package result.

The largest relative discrepancy involves a near-zero energy residual: native 2.6177531253779307e-9 MW is within the existing 1e-7 MW absolute tolerance. Primary hot/return temperatures and six terminal differences are native diagnostic outputs outside the current independent oracle catalog. The source-specific 30 K reporting screen is not a native predicate; return requirements remain absent. Numerical parity does not supply scientific qualification.

A separate delivery replay of all 648 complete maps into a fresh temporary store reproduced every one of the 551 native outputs, all input maps and all 14 predicates exactly. results/delivery-replay-comparison.json records zero differences. This tests reproducibility; it does not extend independent oracle coverage.

## 14. Review outcomes

Independent pre-execution review initially found capture errors in pressure loss and source-mode labels. The corrected contract, exact input-map assertions, framing and six passing gates were accepted before main execution. See reviews/comparison-review.md, comparison-review-r2.md and comparison-execution-release.md. Coordinator T-002 released the exact reviewed numerical proposal only after the stated record conditions were filled.

**Independent post-execution integration/answer audit: PASS**, reviews/final-review.md. The reviewer independently checked all 648 maps and the complete verification sample, original control, every primary purchase output, passing selection, nominal/zero-price/asymmetric pairs, energy and cost arithmetic, break-even endpoints, failed cases and aliases. All four figures were visually inspected; seventeen regenerated figures/data artifacts matched byte for byte. The reviewer accepts the conditional comparison and partial completion. Documentation corrections were applied before sealing. This is independent coverage; the coordinator’s record completion is not a self-certification.

Remaining closure coverage is the final native seal and goal disposition. The goal trail records that check, reusing this audit rather than repeating scientific review.

## 15. Findings

| ID | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260926-design-study-exchanger-architecture#1` | model | Split and common flow freedom change the sampled heat-removal range; equal passing operation gives equal output. | Recorded conditional architecture result and correction of earlier B3 branch explanation. | results/reporting/results-reading.md |
| `20260926-design-study-exchanger-architecture#2` | model | Native topology purchases/losses are invariant; pressure-loss uncertainty can erase or reverse a passing comparison. | Declared seam; report annual-extra-cost/power break-even allowance, not a detailed estimate or unconditional preference. | results/reporting/results-reading.md |
| `20260926-design-study-exchanger-architecture#3` | model | Primary return requirements and finite minimum approach are not implemented; all primary native passes fail the separate source-specific 30 K screen. | Declared seam; physical architecture selection remains unqualified and completion partial. | results/reporting/results-reading.md |
| `20260926-design-study-exchanger-architecture#4` | model | Source sustainment is absent and fuel price has no actual engineering resistance despite conservative graph reachability. | Supplied-source downstream comparison; agent-selected price endpoint within authorized sensitivity; no plasma or supply qualification. | comparison-contract.md |
| `20260926-design-study-exchanger-architecture#5` | process | Oracle covers 364 of 551 native outputs and all predicates; terminal/return diagnostics are outside that catalog. | Explicit verification limit at diagnostic claims; preserved native data for future extension. | results/verification_summary.json |

## 16. Snapshot

snapshot.json and sealed-package.tar.gz seal the completed report and native evidence. The snapshot resolves every declared fingerprint, native store, tool identity and result artifact digest. The native package itself is unchanged. Retained route/oracle/support sources and complete input maps support replay without reconstructing the assumptions from conversation.

## 17. What this record does not contain

No plasma sustainment/heating solution; no fully coupled blanket duty/flow/temperature model; no required primary-return constraints; no engineering minimum approach enforced by native predicates; no validated pump/branch hydraulic or machine maps; no priced split-controller/manifold inventory or validated topology-specific pressure-loss law; no tritium breeding/supply qualification; no global optimum or located network upper boundary. No alternative inventory was selected because fixed hardware already supports the declared conditional range in at least one arrangement; any future inventory alternative requires its own offered ratings/prices and reviewed study.

The record preserves native failed cases and oracle candidate ledger; no numerical refusals occurred. Source and equipment adequacy beyond the implemented predicates is unverified. Diagnostic temperature channels are retained without independent numerical certification. Existing studies, model files, generated package and the owner’s article are unchanged.
