# WI-048 implementation evidence

[AGENT] Implementation under the approved plan. Independent audit remains pending.

## Phase 1

Library calculations expose physical balance, bank energy, discounted and annualized cost/energy, and the shared Real 0/1 guarded price contract. The strict net-generation assertion is separate from the retained economic heuristic. Meier Eq. 5 and the Osiris table images were visually inspected; no transcription conflict occurred.

V1–3 passed with 11 canonical library/shared files and matching prototype design usages during the interface transition (zero parser warnings, structural issues or cycles). See `phase1-level{1,2,3}.txt`. New structural test: 1 passed. Typed generation and canonical plant validation follow in later phases.

Native `pm trace-element` rejected duplicate existing element/file rows and offers no update operation. Added qualified current element rows with MR/SV/source locators through the native operation, preserving historical unqualified rows. No registry was hand-edited.

## Phase 2

The HIF driver derives bank energy from beam/efficiency; procurement rate binds plant frequency. Both price chains consume computed thermal/net powers. All thirteen historical table facts survive as separately named attributes. The six changed family twins match canonical bytes; shared files and MFE models were untouched. V1–3 passed on the canonical subset (see `phase2-level{1,2,3}.txt`), with zero parser warnings, structural issues or cycles; source/structure tests: 2 passed. The old 23/18 entry census remains temporarily stale until phase 3 re-derives it.

## Phase 3 — Executable contract

The shipped `ife_tea` package generates from the canonical IFE subset with pinned `GenerationConfig`/`run_codegen`. One handwritten implementation contains only the strict-positive final quotient. It retains the generated `Generating_Electricity_PriceInput -> tuple[float, float]` signature. The generator backlog is a static template with two unchecked rows for the two usages of this one completed definition; execution and regeneration tests establish completion. Both native `preserve_handwritten=True` and `smart_regen=True` preserve it and all package bytes; see `phase3-regeneration.txt` and `test_typed_handwritten_quotient_survives_supported_regeneration`. Live and captured-snapshot packages are completed from that same implementation before execution comparisons. All 20 original public tests passed after deliberate expectation migration (`phase3-public-tests.txt`); four regeneration cases and eight source/boundary cases were subsequently added.

Final interface: 19 entry points = 16 design attributes + 3 library defaults, versus 23 = 18 + 3 + 2 usage literals before repair. The independent `driver__energy`, `driver__pulse_rate_ref`, `thermal_power_gw` and `net_electric_power_gw` keys retire. The old usage-literal keys `meier_reactor_cost_calc__num_units` and `meier_capital_calc__target_factory_cost` retire; named design keys `reactor_units` and `target_factory_direct_cost_billions` replace them. All keys have the `hif_plant_pkg__hif_plant__` prefix. Historical reference attributes are not entry points. The exact sets are asserted in `tests/models/test_model_family_spines.py`; all 13 family tests pass (`phase3-family-tests.txt`).

The final package has 30 numeric channels plus two constraint-evaluation channels and the constraint report, versus seven numeric channels plus one evaluation and its report before repair. `lcoe_calc__lcoe` and `meier_coe_calc__coe_cents_kwh` retire. Guarded `hawker_price__price` and `meier_price__price` each have `__generating`. Added outputs expose bank energy; both cost numerators/denominators; beam/yield; all powers and fractions; annual shots, lifetime, driver capital and replacement cost. The exact 33-channel set is asserted in `tests/test_codegen_teax_acceptance.py`.

[AGENT] Parent approved six additional intermediate outputs during implementation to make SV-074 directly observable: energy on target, yield per shot, annual shots, driver lifetime, driver capital and annual replacement cost. The last two name existing inline expressions without changing their arithmetic order or assumptions. This is an interface observability change, not a new physics or finance model. V1–3 passed after the additions (`phase3-level*.txt`). The generator's temporary backup of the earlier IFE output signature was moved outside the shipped package, then native regeneration rebuilt seals; no seal was edited by hand.

Final identities are recorded in `final-package-identity.json`: semantic `8b7a76a631e6e55dbd45cf617a68fae87def408e4f8494015e40c0c8aac585dd`, executable `930738720555969d2ddb283fb73c8a31173a3851d5c94e3acb9c3cff92e0fefd`, quotient SHA256 `67bc0ed6241856920c8380b4ddcc0293d41f6d6fa131abc6c97b6cc74d1d9377`. `ProvisionalPackageLoader` accepted the final seal. Prepared execution and CandidateBridge supply the baseline/mutation evidence.

## Phase 4 — Independent numerical acceptance

`tests/ife_oracle.py` derives the physical balance directly from beam energy and the source inputs, computes Meier Eqs. 1–5, and sums individual annual capital/operation/energy cash flows over calendar years 1–45. It neither imports generated finance nor copies the closed-form PV factors. `capture_execution.py` also rebuilds the old model files at approved-plan commit `d953f12c` into a temporary package and checks the old baseline independently using its explicitly separate bank and power inputs. Run `.codex-test/run python work/active/WI-048_ife-operating-point-repair/capture_execution.py`. Full inputs, outputs, named verdicts and independent expected values are in `execution-evidence.json`; `capture-execution.txt` records maximum relative residual `9.642452298033805e-16` across baseline and three mutations.

| Quantity | Before repair | Corrected computed case | Cause |
|---|---:|---:|---|
| Beam energy used by Hawker (MJ) | 5.0001 | 5 | Removes independently rounded bank input |
| Bank energy (MJ) | 14.286 | 17.8571428571 | Derives beam/0.28 instead of holding bank independently |
| Gain; operating rate (Hz) | 80; 3.5 | 87; 4.6 | Image-verified source inputs |
| Computed yield (MJ) | 400.008 | 435 | Corrected beam and gain; printed 432 remains historical |
| Computed fusion power (MW) | 1400.028 | 2001 | Corrected yield and rate |
| Computed thermal power (MW) | 1610.0322 | 2301.15 | Same retained blanket multiplier 1.15 |
| Computed gross power (MW) | 692.313846 | 1035.5175 | Corrected conversion efficiency 0.45 |
| Driver and other power, each (MW) | 50.001 | 82.1428571429 | Derived bank and common rate; retained equal cooling allowance |
| Computed net power (MW) | 592.311846 | 871.231785714 | Gross minus driver and other |
| Meier thermal/net denominator basis (GW) | 2.054 / 1.0 held | 2.30115 / 0.871231785714 computed | Both price paths now share one physical case |
| Driver procurement (billion 1988 dollars) | 0.9749584 | 0.98452224 | Rate factor changes from 3.5 to 4.6 Hz |
| Gamma (dollars/J bank) | 68.247088 | 55.13324544 | Same procurement divided by authoritative bank joules |
| Reactor cost (billion 1988 dollars) | 0.730444258781 | 0.772264159550 | Computed thermal power replaces fixed denominator |
| Total Meier capital (billion 1988 dollars) | 3.303886865568 | 3.397919111177 | Reactor and driver changes; factory and 1.83 multiplier held |
| Hawker price (dollars/MWh) | 270.1211779380445 | 240.66646063955096 | Corrected net output and coherent shots, capital and replacement inputs |
| Meier price (1988 cents/kWh) | 4.735403549076959 | 5.589991561584082 | Greater annualized capital and lower net denominator than the old held 1 GW |

Hawker retains 8% discount, five construction years, forty operation years, mixed inherited 1988-derived plant/driver coefficients and generic target cost. Meier retains 8.3% fixed charge plus 3% O&M, a 1.83 capital multiplier and 1988 cents/kWh. Both use availability 0.90 and computed net 0.871231785714 GW. Shot accounting uses 31557600 seconds/year; energy accounting uses 8760 hours/year. The historical 5.6 in 1992 cents/kWh is a reference fact, not a validation target for either current price. No currency normalization or financial convention was changed.

SV-074 independently verifies all 30 public numeric outputs at baseline, beam 5→10 MJ, efficiency 0.28→0.35 and rate 4.6→5 Hz. Beam doubling doubles bank/yield and changes procurement by exactly the source factor 1.5789473684210527 within relative 1e-9. Efficiency reduces bank demand inversely while beam/yield stay fixed. Rate scales every power and annual shots by 5/4.6, scales lifetime inversely, and changes procurement by the independently calculated Meier rate factor. Gamma×bank equals direct driver dollars; those dollars equal Hawker driver capital and drive annual replacements. Tests compare numeric identities at relative 1e-9; absolute 1e-6 W applies only to power arithmetic near zero, never eligibility.

SV-075 retains the negative-net eta=0.1, gain=100, blanket=0.6, thermal efficiency=0.3 counterexample. Its heuristic passes and named net verdict fails. The 5 Hz boundary is exactly 0 W; thermal efficiencies 0.199999999 and 0.200000001 give exactly −2.5 and +2.5 W. Both prices/validities are zero for non-generators; positive neighbors have finite positive prices and validity one. At 4.6 Hz, the same nominal boundary produces +5.960464477539063e−8 W and correctly passes the literal strict predicate. Neither a tolerance nor a clamped power changes that result. Every case executes through live and snapshot public routes; the separate consumer tests reject ineligible prices for both Hawker and Meier ranking and anchors.

### Runnable consumers

The migrated callers are `scripts/verify_ife_lcoe.py`, `scripts/verify_hif_costs.py`, `exploration/ife_e2e/{run_anchors,sweep_ife,plot_sweep}.py` and `exploration/ife_e2e/study/{run_viability_study,bench_prepare_once,prove_catalog_seam}.py`. `eligibility.py` shares validity-plus-named-verdict checks. Historical module scenarios remain labeled and separate from the corrected whole-plant case. Named generated output wrappers replace tuple-order assumptions. Price outputs for invalid points are excluded from ranking and exported as missing values in legacy sweep/study tables.

All nine bounded smoke commands passed, with exact commands and compact output under `caller-evidence/`. Verification scripts pass their independent source/identity checks. Anchors reproduce historical module scenarios and the corrected whole-plant prices to relative 1e-9. The historical-module sweep executed 11,505 points, with 10,440 generation-eligible, 8,755 heuristic-viable and 7,419 attractive points; invalid zero never qualifies. The bounded 2×2 study includes an exact-zero row with violated net verdict and blank price; the catalog proof and two-point prepare/rebuild benchmark pass. Plotting reads bounded temporary output. Output-local package aliases avoid the old global temporary link accidentally pointing at another checkout. No native-study infrastructure was added and no historical outputs were rewritten. V1–3 passed (`phase4-level*.txt`).

## Phase 5 — Validation and audit handoff

Final regression command: `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/models/ tests/test_codegen_teax_acceptance.py tests/test_occurrence_mutation_teax.py tests/test_ife_consumer_eligibility.py tests/test_dependency_provenance.py -v'`. Result: **122 passed, 13 skipped** (`final-regression.txt`), comprising 75 model tests, 32 public IFE tests, 12 consumer tests and 3 dependency-provenance tests. Entry counts were 63 model passes/13 skips and 20 public passes; there are twelve new model passes, twelve new public passes and twelve consumer passes. No old test disappeared and no new skip was introduced. The thirteen inherited skips are the existing example-template skip and twelve tests targeting absent legacy foundation files; their individual names remain in the log.

Runtime: `/home/reid/1cfe/fusion-tea/.venv/bin/python3`, agentic-mbse 0.1.3, sysml-codegen 0.1.1, SysIDE 0.8.4, under the retained sealed dependency identities. Tests verify immutable wheel/source provenance; versions alone are not the identity. Implementation was performed on `d953f12c72d7311e446741b0c8f47d307a7b6d11` plus the reviewed working-tree changes. Shared runtime and lockfiles were not modified.

| Validation scope | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| Final canonical IFE subset | PASS, zero warnings | PASS, zero issues | PASS, zero cycles | PASS, 2/2 admitted numerical | PASS, 29/29 documented | FAIL, 50 issues |
| Whole tree before repair at d953f12c | PASS | FAIL, 12 placeholders | PASS | PASS | PASS | FAIL, 253 issues |
| Final whole tree | PASS | FAIL, 10 placeholders | PASS | PASS | PASS | FAIL, 277 issues |

Commands: `.codex-test/run agentic-mbse validate --level=N /tmp/wi048-check` for N=1,2,3 (phase-specific `phase*-level*.txt`), then `validate --complete /tmp/wi048-check` and `validate --complete models/` (`final-ife-validation.txt`, `final-whole-tree-validation.txt`). The before-repair complete result is `entry-whole-tree-validation.txt`. The two IFE literal-placeholder issues disappeared when reactor units and target-factory cost became named attributes; ten unrelated placeholders remain.

All L6 issues are enumerated in `level6-issue-comparison.json`, with counts in `level6-category-counts.txt`. Before-repair IFE: 26 = 18 abstract-definition defaults + 4 unsupported-dot EXPOSE checks + 4 static-default extraction checks. Prototype: 34 = 18 + 7 + 7 + 2 thermal/net derived-reference checks. Final: 50 = 18 + 15 + 15 + 2. The eight new plant EXPOSE aliases add exactly sixteen instances of the same static-check limitation relative to the prototype. The whole-tree increase 253→277 is exactly the IFE increase 26→50; unrelated findings are unchanged. The deliberate handwritten quotient has declared outputs and emits no separate L6 issue. Public exact generation, sealed execution and regeneration succeed independently of this failed quality level. This evidence does not relabel L6 PASS or grant a general residual acceptance.

Native `pm update-validation SV-073/074/075 --status passing` records implementation verification only. The native command supports status but no evidence field; the existing spec reference resolves to its implementation-evidence link below. Historical certifications were preserved. Native `trace-element` appended CRLF rows; parent approved normalizing only the eight appended line endings without changing any cell or state. Native `trace-element` supplied all new qualified trace rows; it has no update/supersede operation, so historical unqualified rows remain explicitly historical metadata. Final review found no MFE/shared foundation/cost hierarchy changes and no retired IFE interface references in runnable Python callers. Remaining matching `lcoe_calc__lcoe` references are MFE channels or explicitly historical evidence.

### Acceptance matrix

| Requirement | Implementation evidence | Status |
|---|---|---|
| MR-WI048-1 | `test_osiris_exact_source_facts_and_computed_bindings`; all thirteen exact image facts; historical/computed separation in model and README | Verified, SV-073 |
| MR-WI048-2 | `test_sv073_sv074_independent_source_and_cashflow_execution`, `test_sv074_mutation_identities`; bank/gamma/capital/replacement identities in `execution-evidence.json` | Verified, SV-074 |
| MR-WI048-3 | Same tests, rate5 case; one direct frequency source reaches procurement, shots, powers and lifetime | Verified, SV-074 |
| MR-WI048-4 | Independent calendar cash-flow sum; Meier source oracle; before/after table and explicit physical, monetary, finance and availability bases | Verified, SV-073 |
| MR-WI048-5 | `test_sv075_strict_boundary_and_named_net_verdict`, public route boundary tests and both-price whole-pipeline consumer tests | Verified, SV-075 |
| MR-WI048-6 | Every power and fraction checked against the independent oracle plus all boundary power balances | Verified, SV-075 |
| MR-WI048-7 | Canonical/twin equality, live/snapshot parity, typed native regeneration, sealed loading, candidate mutations, nine runnable caller checks | Verified, SV-074/075 |
| MR-WI048-8 | L1–3 pass for IFE; all quality levels and exact interface changes reported; regression 122/13; independent audit remains the next stage | Implementation evidence complete; independent audit pending |

No source conflict, new financial convention, unexplained blocking IFE failure, or numerical tuning was introduced. The parent must arrange a fresh native `$audit-models` report evaluating F01, F02 and F03 separately. This implementation record is not that audit. Item close/archive, goal close and merge/push remain outside this stage.

## Repair attempt 1 — 2026-09-11

[AGENT] The record above describes the prior production revision. The negative independent audit identified incomplete current source claims (A01/A02) despite passing numerical checks. The bounded correction, native trace additions, synchronized generation, exact unchanged baseline and new package identity are recorded separately in [repair-1.md](repair-1.md) and [repair-1-identity.json](repair-1-identity.json). Original numerical/identity evidence remains historical and unchanged. Fresh independent re-audit is required.
