## 1. Study header

- **Study id:** `20260910-ife-operating-point`
- **Package:** `ife_tea`
- **Date executed:** 2026-09-10
- **Executor:** Codex fusion-audit-remediation round 1
- **Mode:** execute
- **Arms:** single arm: `arm-ife`

## 2. Intake

[OWNER-VERBATIM]

> I have this audit report of modeling issues: .project/reports/20260907-fusion-model-audit.md

> I'd like you to $run-goal to address these.

> yes ground and proceed

[AGENT] The grounded round selects the corrected IFE operating point, beam/rate sensitivity and the audited non-generation counterexamples. `protocol.md` records the executor's proposed framing and execution choices separately from the owner's words. T-005 stopped at indicator preparation; T-007 resumes the same unexecuted draft after the shared producer correction.

## 3. Objective and result

The two price channels are `hif_plant_pkg__hif_plant__hawker_price__price` (mixed-basis $/MWh) and `hif_plant_pkg__hif_plant__meier_price__price` (1988 cents/kWh). Their distinct finance and dollar-year interpretations are retained. Values below come from `results/points.csv`; full qualified outputs, inputs and eligibility flags are in `results/cases.json`.

| Role | Net electric MW | Hawker mixed-basis $/MWh | Meier 1988 cents/kWh | Price eligible |
|---|---:|---:|---:|---|
| baseline | 871.231786 | 240.666461 | 5.589992 | yes |
| beam-4.0 | 696.985429 | 290.031012 | 6.257484 | yes |
| beam-6.0 | 1045.478143 | 207.756760 | 5.125380 | yes |
| rate-3.6 | 681.833571 | 244.405964 | 6.773097 | yes |
| rate-5.6 | 1060.630000 | 238.272338 | 4.806524 | yes |
| counterexample | -46.000000 | invalid sentinel | invalid sentinel | no |
| zero | 0.000000 | invalid sentinel | invalid sentinel | no |

Increasing either ordinary axis lowered each price interpretation over the sampled points while increasing net generation. That observed response establishes no optimum, physical capacity or common financial comparison.

## 4. Constraint outcomes

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `hif_plant_pkg__hif_plant__net_positive__1d299cceab19c61c` | net_positive | satisfied / violated | Satisfied on all five ordinary cases; violated on counterexample and zero. |
| `hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b` | viability | satisfied | Satisfied on every case, including both non-generating diagnostics. |

All seven cases completed. The five ordinary cases satisfy both emitted checks. Both diagnostics fail model feasibility and price eligibility despite satisfying the heuristic. This finite constraint set does not establish engineering completeness. No indeterminate verdict occurred; exact zero fails the strict net-positive comparison.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| beam_energy_mj | sensitivity | Possible net-power path, held gain and conversion assumptions; no sourced capacity boundary. |
| frequency | sensitivity | Possible net-power path, held gain and conversion assumptions; no sourced capacity boundary. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| beam_energy_mj | sensitivity | no | All ordinary beam cases generate; outputs and both price interpretations respond without a verdict flip. |
| frequency | sensitivity | no | All ordinary rate cases generate; outputs and both price interpretations respond without a verdict flip. |

The fixed negative/zero diagnostics are outside the response window and test the audited gate, not a newly swept axis. The all-feasible ordinary sensitivity window does not invoke the search-framed feasible-fraction bar.

## 6. Per-axis account

#### beam_energy_mj — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### beam_energy_mj — observed response (sensitivity framing)

**Applies:** yes.

The three ordinary beam points in `results/points.csv` show increasing fusion and net power, increasing procurement, and decreasing each separately denominated price as beam energy rises at the held rate and gain. Both constraints are satisfied. No boundary claim is made. This response does not establish that gain or engineering capacity could stay fixed in a real beam-energy change.

#### frequency — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### frequency — observed response (sensitivity framing)

**Applies:** yes.

The three ordinary rate points show increasing net power and decreasing each price interpretation at held beam energy and gain. Both constraints are satisfied. No boundary claim is made. No repetition-rate ceiling is established by these points.

The only net violations are the named fixed `counterexample` and `zero` roles with complete coordinated overrides in `results/proposals.json`. They are not ordinary beam/rate response points. The negative case yields approximately -46 MW; the exact-zero case yields 0 W. Both retain zero price sentinels and zero generating flags, and neither is eligible.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| beam_energy_mj | `hif_plant_pkg__hif_plant__driver__beam_energy_mj` | fan_out | One authoritative design input after WI-048; downstream bindings are structural. |
| frequency | `hif_plant_pkg__hif_plant__frequency` | fan_out | One authoritative design input after WI-048; downstream bindings are structural. |

`axes.json` carries the complete declaration. No external identity ties.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| beam_energy_mj | constraints_reachable | Not required: no_constraint_response is false. | Swept as sensitivity; reaches net generation, not the held heuristic. |
| frequency | constraints_reachable | Not required: no_constraint_response is false. | Swept as sensitivity; reaches net generation, not the held heuristic. |

**Not derivable, disclosed in every record.** Indicators cannot establish monotonicity or response sign, identity across differing key names, or intra-module operand dependency. A reachable constraint is a possible path, never a statement that it responds. `unresisted` would be an agent judgment, not tool output.

**Model-development findings.** Neither axis reports no_constraint_response, so the associated mandatory owner-ruling condition does not bind. The held-gain and missing source-backed engineering-capacity limitations are nevertheless recorded as finding #2; successful net generation does not discharge them. The fresh framing critique confirmed that this sensitivity protocol needs no additional owner ruling.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 2 declared keys across 2 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest 045417b231573653d754b68c8e26eec26fcec72fdc3814df27e504416639fe63 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | hif_plant_pkg__hif_plant__hawker_price__price reproduces at relative deviation 0.000e+00; 2/2 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The preflight read `results/baseline/package_identity.json` and `results/baseline/baseline_result.json`. All six gates ran. `results/post-run-clean.json` confirms the package remained clean after execution. The full indicator pass also ran the read-set coverage assertion absent from the historical integration manifest gate; this does not rewrite that earlier report.

## 10. Execution route and why

- **Route:** study-local direct-API.
- **Why this route:** The baseline/preflight exercised the stock route successfully. The planned union of one-factor points and coordinated fixed diagnostics is a prepared list, not a Cartesian grid. `execute.py` calls the package's `StudyRunner` route without a hand-written evaluator loop.

**Glue disclosure:** glue ledger: none. No adapter on this route. The typed final price quotient is inside the sealed generated package and is preserved by regeneration; it is a disclosed package implementation dependency, not harness-supplied physics.

## 11. Study definition and window provenance

The independent oracle scan in `results/oracle-scan.json` covered broad candidate beam and rate values with every other ordinary input held at the audited baseline. All outputs were finite and net generation stayed positive. At both ends of each candidate scan the generating edge was not caught; neither the fixed heuristic nor this finite scan establishes a source-backed beam/rate capacity boundary.

The executor fixed the narrower ordinary-response window recorded in `results/window.json` after that scan. It brackets the baseline at modest one-factor changes and avoids presenting extrapolated low prices as optima. Provenance is engineered, not sourced. No validity mask drops cases. The two fixed WI-048 diagnostics are retained outside that response window with their complete overrides and role names; they test non-generation, not a new sensitivity axis. The scan supports the pre-reviewed framing, so no re-critique was needed.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. There is one arm and one study store. The preflight baseline store is auxiliary validation evidence, not a second arm.

## 13. Verification

Native verification passed for all seven stored cases, all thirty numerical channels and both independently re-derived predicates. `results/verification_summary.json` records the sample and worst relative deviation; every observed verdict combination was covered. The independent oracle computes source power identities and explicit annual cash flows rather than generated closed-form arithmetic.

A direct 1costingFE comparison verifies the applicable bank-energy and driver-draw identities for all seven cases. `results/reference-applicability.md` explains why different thermal, auxiliary, costing and finance conventions prevent whole-plant net-power or LCOE equality from being a like-for-like claim here. The copied reference excerpts and JSON result make that distinction inspectable.

Verification shares selected source facts and held assumptions with the audited model. It does not independently establish source correctness, real gain/capacity response, engineering feasibility or normalized finance. The annual-cash-flow oracle supports positive integral year counts; all study points stay in that domain. Both oracle files and the sealed handwritten price quotient are copied in `results/context/`. No empirical performance validation is claimed.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique | PASS | Fresh `ife_study_critique` review in `pre-execution-review.md`; all six execution dispositions carried into scan, case roles, reference comparison and reporting. |
| Correctness, honesty and readability | PASS | Fresh `ife_study_review` review in `post-execution-review.md`; all result/store/hash, interpretation and discovery joins checked, with no corrective findings. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260910-ife-operating-point#1` | model | The corrected IFE chain responds coherently, and non-generation is rejected despite the satisfied heuristic. | model fix — WI-048 independently audited; this study verifies the retained repair over named points. | `results/context/WI048-audit.md` and `results/cases.json` |
| `20260910-ife-operating-point#2` | model | Held gain and absent sourced beam/rate capacity checks prevent engineering-boundary claims. | declared seam — unresolved engineering coverage; no residual acceptance. Source/engineering work and owner disposition remain required. | `results/context/ANNEX.md` sections Oracle and Validity masks |
| `20260910-ife-operating-point#3` | model | The two price interpretations retain incompatible historical bases. | declared seam — separate labels enforced; normalized comparison and residual acceptance remain owner-held. | `results/context/ANNEX.md` section Baseline pin and `results/reference-applicability.md` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** 3edebbe53943050eba7de55102f8773e21b09db8cf3b2c2b5dd92c5e2103179e
- **Schema version:** 1

## 17. What this record does not contain

This record contains no full source-image re-audit, validated engineering capacity envelope, gain-versus-beam relation, hardware performance measurement or normalized cost comparison. It does not supply an optimum or a source-backed feasibility boundary. Those missing model/evidence claims remain explicit findings rather than accepted residuals.

The immutable context contains the oracle, execution route, manifest, model contract, relevant audit reports, handwritten quotient and reference excerpts. The complete generated package and full external 1costingFE checkout are identified by revision/fingerprints rather than copied in full. Execution results, effective inputs, all named outputs/verdicts, scan and reference checks are carried inside this record; interpretation does not require retrieving those external source trees.
