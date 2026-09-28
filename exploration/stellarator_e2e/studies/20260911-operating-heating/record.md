## 1. Study header

- **Study id:** 20260911-operating-heating
- **Package:** stellarator_tea
- **Date executed:** 2026-09-11
- **Executor:** Native T-019 execution agent, under parent authorization recorded in preparation/dispositions.md.
- **Mode:** execute; final review dispositioned, findings registered, evidence finalized for parent commit.
- **Arms:** arm-reserve, arm-retained-alpha, arm-density, arm-signed-bracket.

## 2. Intake

[OWNER-VERBATIM]

> I have this audit report of modeling issues: .project/reports/20260907-fusion-model-audit.md

> I'd like you to $run-goal to address these.

> yes ground and proceed

[AGENT] Under T-019 scope at 167785f0 and Round 4, test whether reserve changes at fixed plasma and efficiencies leave operation unchanged while procurement responds, and whether supported demand changes at fixed heating installation propagate coherently without repricing installed heating. The specific study question, engineered cases and expectations are agent-originated. Preserve historical evidence, held finance/efficiencies and design-point sizing conventions.

The record uses the single T-018 candidate copied in `context/integration_return.json`; no new pin is created. Model audit at 55456198 and package certificate at 07c33fee are copied in `context/`. Their conclusions are inherited bounded evidence, not new study execution.

## 3. Objective and result

The study separates installed heating reserve from operating demand. At fixed plasma, increasing installed electrical capacity from 100 to 120 MW changes heating procurement from $264,145,000 to $316,974,000 while leaving all checked operating flows and annual energy unchanged. Headline LCOE rises from **224.269233 to 225.413073 $/MWh**, on sealed executable fingerprint a9514eb6505dea1589f47cb20bd004e480d61b3be98e7d793bf195b1b2d773b0 with the captured runtime in `results/runtime.json` (no era adapter/pin). The increase is entirely capital attribution under the retained finance convention.

At fixed heating installation, raising retained-alpha fraction from 0.95 to 0.96 reduces signed operating coupled demand from 49.079601 to 43.769169 MW and headline LCOE to 222.326284 $/MWh. Installed heating procurement stays fixed. Density changes also alter fusion, ash, confinement, radiation, equipment sizing and calendar outcomes; their economic changes are not an isolated auxiliary-heating intervention.

**Zero of fifteen cases is fully feasible.** Every case violates the existing divertor target screen. Finite LCOE at negative demand is an invalid burn-hold diagnostic, never an improvement. The lowest displayed LCOE is not an optimum claim.

All fifty previously audited cost, annual, calendar and finance modules have their actual inputs, outputs and baseline deltas in `results/cost-operands.json`. Installed delivered power drives heating procurement. Held heating procurement in demand cases coexists with legitimate changes in retained design-point turbine, heat-rejection, electric and indirect accounts; replacement amounts and annual accounts can change with those priced components. These are modeled sizing consequences, not repricing purchased heating or a pure running-expense change. The current bindings and classifications are copied in `context/inherited-cost-operand-coverage.json`.

Both objective channels, `stellarator_09__stellaris__lcoe_calc__lcoe` and `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe`, are exported in `results/points.csv`. All fifteen case identities, inputs, 141 numeric channels and verdicts are in `results/cases.json`; actual capital numerators, annual accounts, energy and both additive LCOE bridges are in `results/additional-verification.json`. Baseline controls at proposal indices 2, 6 and 8 have identical outputs and remain separately labeled with their actual native candidate IDs.

For the 0.95→0.96 retained-alpha case, the headline change is −1.942948499 $/MWh: capital +0.014242582, annual accounts +0.025110437, energy −1.982301518. The comparison change is −1.905635676: capital +0.013934861, annual +0.025110437, energy −1.944680974. Both bridges use the measured numerator operands, never an LCOE-derived numerator. Reserve adds +1.143840050 headline and +1.119126564 comparison, with zero annual and energy contributions.

The historical pre-repair headline 224.609524728→224.269232884 $/MWh is a copied audit comparator. Its −0.340291844 change has capital +0.002479292, annual +0.004380321 and energy −0.347151457 contributions. The historical comparison change is −0.333756416, with +0.002425725 capital, +0.004380321 annual and −0.340562462 energy. `results/inherited-bridge-reconstruction.json` carries the actual historical and current numerators/energy and `context/inherited-baseline-attribution.json` carries the full source ledger. The old package was not rerun.

All figures depend on the single sealed identity in `results/package_identity.json`, the runtime in `results/runtime.json`, and unchanged empirical, cost, calendar and finance assumptions. These are modeled design-point economics, not a plant feasibility certificate.

## 4. Constraint outcomes

Every native case completed. All eighteen assertions are retained by both qualified constraint ID and source local identity.

| constraint_id | source_local_identity | Status | Note |
|---|---|---|---|
| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | satisfied: 0/15, violated: 15/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | satisfied: 13/15, violated: 2/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | satisfied: 9/15, violated: 6/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | satisfied: 13/15, violated: 2/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | satisfied: 9/15, violated: 6/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |
| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | satisfied: 15/15, violated: 0/15, indeterminate: 0/15 | Exact case locations in results/report-summary.json. |

No verdict was suppressed or reclassified. Divertor violations occur in all fifteen cases; sustainment additionally fails at installed-80 and alpha-0.94. Wall and loop-capacity screens fail for density multipliers 1.1–1.4 and both signed-bracket cases. Burn hold fails at density-1.4 and negative-near-zero. All other native checks are satisfied throughout.

## 5. Framing

**As proposed at intake.** Installed capacity, retained-alpha fraction and density were sensitivity-framed interventions. Temperature was proposed as sensitivity, then declined because the preliminary candidate range did not provide the signed-demand diagnostic. All four indicators remain in the record.

**As judged after the run.** All three executed axes retain sensitivity framing. Reserve isolates procurement from operation; retained alpha changes operating demand with compensating divertor heat; density changes the coupled plasma solution. The negative brackets locate diagnostic signs, not an engineering boundary. Temperature remains declined and unjudged by execution. None of these observations supports a search optimum, a caught feasible-region edge, or an engineering operating window. Policy H1's search feasible-fraction bar does not apply to these sensitivities; the actual 0/15 feasibility is still reported.

## 6. Per-axis account

#### p_wallplug_heat — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### p_wallplug_heat — observed response (sensitivity framing)

**Applies:** yes.

Reserve leaves operating heat, source/loop/net/divertor channels and calendar availability unchanged. Procurement and downstream capital/IDC increase. Installed-80 fails sustainment; the exact baseline-derived equality case satisfies it. Every reserve case violates divertor heat. No physical boundary claim is made.

#### f_alpha_fast — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### f_alpha_fast — observed response (sensitivity framing)

**Applies:** yes.

At baseline density, increasing retained fraction from 0.94 to 0.96 changes demand 54.390032→43.769169 MW. Alpha-0.94 also violates sustainment; all three violate divertor heat. Retained alpha plus demanded auxiliary heat exactly compensates within floating tolerance, so divertor absorbed heat and target peak stay fixed while source heat and electricity change. At density 6.578e20 the two coordinated brackets give +0.008164627807332181 and −0.008164627807559555 MW; the negative case fails burn hold, and both fail divertor, wall and loop capacity. No physical boundary claim is made.

#### n_e0 — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### n_e0 — observed response (sensitivity framing)

**Applies:** yes.

Density multipliers 1.0→1.4 change demand 49.079601→−15.308579 MW, net power 1013.931933→1596.518763 MW and target peak 10.517842→16.316537 MW/m². Multipliers 1.1–1.4 fail wall and loop capacity; 1.4 also fails burn hold. Divertor heat fails everywhere. Fusion, ash, confinement, radiation and calendar changes prevent attribution solely to heating. No physical boundary claim is made.

#### T_i0 — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed and declined.

#### T_i0 — observed response (sensitivity framing)

**Applies:** not applicable — declined.

Not applicable: declined before execution. Preliminary temperature probes remain available; no executed response is claimed. No physical boundary claim is made.

## 7. Axis groups

All four considered axes are declared in `axes.json` and traced, including the declined temperature candidate. The existing R/magnet-radius tie remains in the complete pinned baseline point; it is not swept.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| p_wallplug_heat | stellarator_09__stellaris__p_wallplug_heat | fan_out | Complete single-attribute entry group. |
| f_alpha_fast | stellarator_09__stellaris__f_alpha_fast | fan_out | Complete single-attribute entry group. |
| n_e0 | stellarator_09__stellaris__n_e0 | fan_out | Complete single-attribute entry group. |
| T_i0 | stellarator_09__stellaris__T_i0 | fan_out | Complete single-attribute entry group. |

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| p_wallplug_heat | constraints_reachable | No no-response ruling needed | 2/18 constraints reachable; module-level divertor reach includes the installed diagnostic, not proof of operational coupling. |
| f_alpha_fast | constraints_reachable | No no-response ruling needed | 10/18; proposed sensitivity and coordinated diagnostic. |
| n_e0 | constraints_reachable | No no-response ruling needed | 10/18; proposed sensitivity and coordinated diagnostic. |
| T_i0 | constraints_reachable | No no-response ruling needed | 10/18; declined, retained in indicators. |

**Not derivable, disclosed in every record.** Indicators cannot determine monotonicity, physical identity across different key names, or intra-module operand dependency. constraints_reachable means a possible graph path, not actual response. unresisted would be an agent judgment, not a tool result.

**Model-development findings.** No no_constraint_response axis was reported, so its special finding/ruling obligation does not apply. Broader engineering omissions remain in copied audits and the eventual findings register.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 4 declared keys across 4 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest a9514eb6505dea1589f47cb20bd004e480d61b3be98e7d793bf195b1b2d773b0 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 18/18 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

All six gates ran after exact pinned baseline execution and before the formal oracle scan. `results/preflight.json` records the gated identity and baseline documents, input digests and tool identity. `results/baseline_result.json` reproduces the pinned headline exactly and all eighteen expected verdicts. Post-run and post-verification cleanliness also pass, in their named results documents.

## 10. Execution route and why

**Route:** study-local direct-API. The baseline exercised the stock strict loader before preflight passed. A single PreparedListStrategy/StudyRunner run then executed all fifteen coordinated proposals through `study.py::run_all`, sharing one store because all arms share one fingerprint. No hand-written evaluator sweep was used.

**Glue disclosure:** glue ledger: none. There is no adapter or harness-supplied model result. `execution/run.py` exports only after validating all required outputs, exact catalog verdict membership, persisted proposal IDs, original raw proposals and actual case inputs. Labels join by the stock positional proposal ID and persisted candidate ID, never by query order. The baseline uses a separate native preparation store; it is not another study arm.

## 11. Study definition and window provenance

The fifteen executed cases are an engineered sensitivity window. `results/oracle-window-scan.json` records a fresh oracle evaluation of every candidate after all baseline/preflight gates. `results/window-freeze.json` records the window decision made before the stock sweep. It confirms the reserve equality against both generated baseline and oracle demand before freezing its unchanged value. The scan retains opposite signed brackets and reveals the density-coupled violations. There is no sourced engineering density envelope or claimed feasible anchor.

The preserved original sixteen-case proposal and preliminary probes served preparation only. Fresh critique declined the ill-conditioned algebraic center before any TEAx execution, retaining its nonzero preliminary residual and two flanks. The effective fifteen-case proposal, including metadata correction timing, is `preparation/execution-proposal.json`; `execution/corrections.md` records the correction. No result-dependent point retuning occurred. Temperature remains declined. Geometry is held at the pinned baseline and satisfies the existing radial-stack mask. No negative-demand validity mask was applied.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Copied historical model-audit comparison is an inherited ledger, not another executed arm or a rerun of an old package. No historical plant-closure study window, regrade, or engineering closure is inherited.

## 13. Verification

The stock verifier passed on every one of the fifteen completed cases: 25 objective/predicate channels and all eighteen independently re-derived predicates, covering every observed verdict combination. The additional checker passed 2,115 comparisons across all 141 required oracle channels and 566 identities, finance checks and invariance checks. The source/loop/thermal/net/divertor identities use named captured inputs and channels. Net power is independently checked against every named recirculating load. Finance uses finite discount sums and actual levelized annual accounts.

The first additional checker failed two alpha-demand-delta checks because it substituted the source-heat ratio for the distinct recorded sustainment fraction. Both failed results and checker are preserved. Parent authorized a checker-only correction to the captured sustainment input; all other verification tolerances and executed evidence stayed unchanged. `execution/corrections.md` gives the cause, timing and references. This failure is not represented as a first-pass verification success.

The retained model uses 0.2002 for sustainment alpha and 3.52/17.58 for source heat. They are close but unequal. The checker correction respects both authored bases; it does not reconcile them or certify a single exact physical convention. Copied source files and package inputs make that difference recoverable.

Translation parity is not independent validation of source assumptions. Some copied oracle statement forms mirror historical modules, and outputs held fixed by construction are not fresh engineering verification. The study does not rerun 1costingFE; the copied audit records where direct registered-source comparison was applicable. Exact native component zero in `context/inherited-boundary-results.json` remains inherited component evidence. No full-plant exact-zero case was executed.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Fresh pre-execution framing critique | FINDINGS | F1: one shared store implemented; F2: algebraic center declined. Original named verdict preserved in preparation/pre-execution-review.md; parent dispositions authorize execution. |
| Executor correctness checks | First additional checker failed; corrected checks and stock verification pass | Failed evidence preserved; checker transcription corrected under parent authorization. This is execution verification, not independent final review. |
| Fresh correctness, honesty and readability review | FINDINGS; correctness, honesty and readability PASS within stated scope | Minor F1 corrected: executable fingerprint is accurately labeled. Parent accepted direct verification without rerun; original review preserved in execution/final-review.md and disposition in execution/finalization.md. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260911-operating-heating#1` | model | Reserve now changes procurement without changing the measured operating ledger. | Proposed: retain bounded WI-050 evidence for goal review; no engineering closure claim. | work/active/WI-050_mfe-coherent-operating-heating |
| `20260911-operating-heating#2` | model | All fifteen cases remain divertor-violating; high-density diagnostics add wall/loop violations and negative demand remains invalid. | Proposed: route remaining engineering coverage to a future scoped goal decision; no feasible-plant or optimum claim. | work/orchestration/goals/fusion-audit-remediation |
| `20260911-operating-heating#3` | model | Sustainment retains alpha fraction 0.2002 while source heat retains 3.52/17.58; verified arithmetic does not make these one physical convention. | Proposed: assess inherited basis consistency in a separately authorized modeling review; no accepted residual or source waiver. | work/orchestration/goals/fusion-audit-remediation |
| `20260911-operating-heating#4` | process | Pre-execution review caught per-arm store splitting and an ill-conditioned algebraic center. | Corrected before execution: shared store, center declined, brackets retained; named review remains FINDINGS. | preparation/dispositions.md |
| `20260911-operating-heating#5` | process | Additional checker initially conflated the two retained alpha bases. | Corrected checker only under parent authorization; failed script/results retained; fresh final review passed its stated numerical and honesty scope. | execution/corrections.md |

| `20260911-operating-heating#6` | process | Fresh final review found the executable fingerprint labeled as a candidate pin. | Corrected wording and directly verified both identities; original FINDINGS verdict preserved. | execution/finalization.md |

All six first-sighting IDs were registered by the native executor in the append-only discovery log before finalization. Proposed modeling dispositions remain subject to the later goal review. No goal disposition is executed by this record.

## 16. Snapshot

- **File:** snapshot.json
- **sha256:** 6bacec1f65669501c8f0c2a11ea0d1693ff184884ff634405549cf6f0e219f34
- **Schema version:** 1

Final snapshot resolved after fresh review, disposition and findings registration. Committed-facing result, preparation, execution and copied-context artifacts carry digests; local runtime artifacts are separately labeled. Study arms reference one complete compatibility tuple. Parent owns the final commit.

## 17. What this record does not contain

Administrator synthesis and goal dispositions are separate later work. Parent commits this finalized executor record. There is no full-plant exact-zero execution, old-package rerun, engineering operating envelope, completed historical plant-closure window, new source certification or regrade. The native databases and evidence bodies may remain local; their paths/digests and complete exported numerical cases, proposal mappings, runtime, catalog, package inputs and schemas are retained for record-only administration.

Copied audits preserve the inherited ten Level-2 findings, 227 inherited plus two accepted Level-6 diagnostic additions, legacy trace limits and excluded historical exporter failures. The package audit records 164 passes, one optional historical skip and eight publication checks; 86 excluded historical-export failures remain disclosed. These are bounded inherited audit facts, not tests rerun by T-019. Four positive/unit efficiency-domain constraints execute in this study, but the held efficiencies and engineering omissions remain assumptions. No source quarantine was bypassed.
