# WI-052 independent implementation audit

[AGENT] **NOT CERTIFIED — prerequisite and documentation corrections required.** The tested numerical repair is sound. The final plan gate is unmet because 22 new downstream regression nodes remain unresolved. Four newly added Source fields also fail the project's direct-path format, and one unrelated fuel comment incorrectly describes its execution mode. These are separate findings; none demonstrates an error in the tested financial values.

## Scope and authority

Fresh auditor `/root/financial_audit`, 2026-09-12, isolated worktree `/tmp/fusion-mfe-financial-rate-limits`. Implementation/evidence inspected at immutable `75d21061b608bc9cad472f68b951f5cdf7847abe`, production commit `75bb4824`. Dispatch authority is main-checkout `work/orchestration/goals/fusion-audit-remediation/evidence/T-031_implementation/audit-brief.md@5b3732ad`. The installed audit-models skill, native spec/design/review/plan, alignment, consumer handoff, requirements and architecture control this audit. Parent already approved scope.

The audited calculations are IDC Closed-Form Cost and Levelized Annual Cost in `models/library/analyses/mfe_account_costs.sysml:645`, LCOE DCF in `models/library/analyses/mfe_lcoe_dcf.sysml:4`, and Lifecycle Calendar in `models/library/analyses/mfe_lifecycle.sysml:4`, their family mirrors and native execution. Existing native equations are the mathematical baseline. External citations remain inherited, without fresh adoption or numerical-source verification. No changed physical parameter needs a new source baseline: all 246 input defaults remain exactly equal. Construction-duration zero remains parked.

Evidence paths below use `I = work/active/WI-052_mfe-financial-rate-limits`, `E = I/implementation`, and `A = I/audit-evidence`, relative to the isolated worktree. These abbreviations identify actual artifacts, not additional state.

## Findings and prerequisites

**F1 — unresolved new regression failures; certification blocker.** Independent parsing of raw entering/candidate JUnit records confirms all 108 inherited study failures and the inherited skip retain the identical node, status and message. Exactly 22 formerly passing nodes now fail or error. `A/checks.json` records every new identity; `E/new-downstream-failures.json` enumerates their downstream classifications. Twenty-one arise from the stale current manifest generation; one is the current radius consumer's exact frozen-finance comparison. The strict final gate in `I/plan.md` forbids certification while any new failure remains unresolved. Deferring consumer work does not waive this gate. MR-WI052-6's native structural/interface subclaims pass, but its completion gate remains unmet; SV-092 stays pending.

The 21 manifest consequences span `test_integrate_lineage.py`, `test_integrate_rerun.py`, `test_integrate_stock_route.py`, `test_integrate_success.py`, `test_preflight_gates.py` and `test_preflight_negatives.py`. Retained preflight receipts at `E/downstream-manifest/*-preflight_results.json:74` explicitly refuse `manifest_currency`: manifest executable `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c` differs from repaired package `fa52a2996d8c1b7c969f0628e812063e0f95d5a5f88b4032df95d857c112e64d`. A separately authorized task must review and re-declare current baseline, ties, oracle and objective catalog against the repaired package, validate the current oracle/adapter at zero/equal/near rates and rerun affected consumer checks. Preserve historical records. Any integration promotion remains subject to its own authority and gate. A fingerprint substitution alone is insufficient evidence.

The additional node is `tests/study/test_major_radius.py::test_current_radius_controls_match_frozen_model_and_independent_oracle`. Its helper `.project/active/mfe-major-radius-study-package/implementation/check_controls.py:33` demands exact baseline CAS71 equality to frozen pre-repair finance. The native ledger attributes a relative movement of `1.873133217044486e-16`; physical outputs remain exact. A separately authorized current-caller correction should retain the historical float as historical evidence and compare current finance against an independent reference at the agreed tolerance. Preserve exact physical expectations. The fresh native audit does not grant permission to change historical expectations.

**F2 — four new Source fields are prose, not paths; required citation-format correction.** At `models/library/analyses/mfe_account_costs.sysml:666` and `:712`, `models/library/analyses/mfe_lcoe_dcf.sysml:32`, and `models/library/analyses/mfe_lifecycle.sysml:83`, the new Source value is “native equation retained above” or “native calendar equations above.” Project MR-4 requires a direct file path in Source. Existing inherited Source paths remain, and the adjacent Ref resolves to the design derivation, so this is a field-format defect rather than an absent mathematical derivation. Replace the supplemental Source value with the actual repository-relative native authority path and put the equation locator in Ref; preserve the honest external-inheritance qualification. Synchronize mirrors and regenerate required native metadata. MR-WI052-7 is partial until corrected. No new source adoption is needed.

**F3 — wrong fuel execution description; required bounded documentation correction.** `models/library/analyses/mfe_account_costs.sysml:759` now says “Output-only Real declarations select typed native manual completion” inside DT Fuel Cost. Its `annual_raw`, `burn_correction` and `annual_fuel` remain executable SysML expressions at `:785`, `:790`, and `:793`. This unrelated comment was changed by WI-052's replacement of the shared annual-cost description. Restore the accurate generated-arithmetic description for DT Fuel Cost, including its family copy and derived documentation. This is a content error distinct from F2's Source-field format. Fuel arithmetic itself is unchanged.

## Requirement verdicts

| Requirement | Verdict | Evidence |
|---|---|---|
| MR-WI052-1 | PASS within stated scope | Exact limits and original $1M equal-rate/$1B zero-discount public counterexamples pass; distinct midpoint and reported IDC retained. `A/focused.xml`; helper and three typed bodies. |
| MR-WI052-2 | PASS within tested window | Nonzero relative tolerance ≤1e-9 without absolute floor; true-zero absolute tolerance ≤1e-9. Independent 100-digit references, fresh additional 110-digit checks and retained full-native factor reconstruction. |
| MR-WI052-3 | PASS within tested window | Real formals and fractional continuations retained; durations 0.25–200.5, one-year neighbors, signed exact/adjacent IDC switches. `I/design.md`, numerical derivation; `A/focused.xml`. |
| MR-WI052-4 | PASS | Thirty-seven calendar fixtures × thirteen rates; all eleven public outputs, independent event dates/PV/annualization/year-bin energy and exact eight physical fields/events. `tests/models/test_mfe_financial_calendar.py`; fresh focused run. |
| MR-WI052-5 | PASS within native cases | Fresh ten-case native output equals author output exactly; 246 inputs, 158 scalars per case, exact physical/report/verdict comparisons and attributed finance. `A/native-absolute/native.json`, `A/checks.json`, `E/scalar-ledger.json`. |
| MR-WI052-6 | PARTIAL; final gate unmet | Canonical/mirror/public/native paths, wrapper order and fresh family generation pass. No new structural/dependency issue. Twenty-two new downstream nodes remain unresolved: F1. |
| MR-WI052-7 | PARTIAL | Four definitions have inherited citations, native derivations, dates and matrix rows; complete scalar/producer handoff distinguishes independent and propagated checks. New supplemental Source format needs F2 correction. |

Phases 1–5 numerical/native acceptance is substantiated. Phase 6's unchecked final gate remains unchecked in author records. This audit supplies the requested fresh audit, but is not a positive completion verdict. No plan or author evidence was rewritten.

## Numerical verification and preservation

The native retained equations in `E/entering/models/analyses/` and calendar implementation are the baseline. The independent reference in `E/reference_finance.py:1` constructs Decimal from represented float operands, explicitly sums integer cash flows and evaluates fractional analytic powers. It imports no production factor or study oracle. The calendar reference derives the event schedule separately and reconstructs productive time from interval intersections before dated-energy comparison. Actual rate differences and boundary branch selections are retained in JUnit properties, including requests that round to equality.

| Quantity/constant | Production locator and method | Baseline/reference | Result |
|---|---|---|---|
| CRF | `generated/handwritten/mfe_account_costs/financial_factors.py:21`; exact 1/N at zero | Dated unit-flow sum or high-precision retained Real extension | PASS |
| Shared PV and levelized charge | Same helper `:25`; first payment after construction escalation | Independent dated sum; equal-rate PV=A1*N/(1+i), both zero gives annual charge=annual cost | PASS |
| Reported IDC | Same helper `:34`; zero branch and binomial/factored evaluation | Retained `((1+i)^T-1)/(i*T)-1`, 100/110 digits | PASS, including tiny nonzero and subannual negative IDC |
| IDC switch 0.125, relative stop 1e-17, cap 100 terms | Same helper `:37` | Design-derived ratio/tail bound; these are numerical choices, not physical parameters | PASS at exact/adjacent signed switches; no new economic constants |
| Midpoint multiplier, annual capital, numerator, energy, price | `generated/handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py` | Independent `(1+i)^(T/2)`, CRF and retained 8760-hour denominator | PASS separately before final division |
| Held/live PV and annualization | `generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py` | Explicit dated events, independent CRF | PASS, including no events and zero cost |
| Dated-energy numerator/denominator/ratio | Same calendar body, `_dated_energy_ratio` | Independent Decimal interval/year-bin overlap with retained ceil epsilon | PASS; held ratio exactly 1 |
| All input defaults, physical scalars, verdicts | Native package and fresh ten-case results | Entering package at identical physical inputs | Exact preservation; original divertor violation remains |

Here `generated/` has prefix `exploration/stellarator_e2e/`. Complete additional numerical actual/expected/error rows are in `A/checks.json`; broader represented operands are in `A/focused.xml`, and native finance expected values are in `E/independent-native.json`. The author-observed maximum ordinary finance movement is `4.740682057829581e-15`; independent native reference error is at most `2.477131275755007e-15`. Fresh native equality establishes these retained candidate values were reproduced, while formula/test inspection establishes the independent reference's meaning. Downstream CAS70/CAS90/comparison-LCOE reconstruction explicitly uses native operands and is not mislabeled as independent upstream physics.

The production helper's exact limits and algebra agree with the retained equations. Held clipping/count and live event logic are retained. Fresh family-spine tests regenerate source and snapshot packages; retained `E/regeneration.json` additionally records repeated ordinary/smart byte preservation with eight seeds. Historical WI-050/WI-051 records were not changed by this implementation; current test callers were deliberately migrated to the new completion route. The entering-to-candidate diff preserves the historical four-seed drivers and receipts.

## Validation and regression evidence

| Surface | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| Canonical, retained raw records re-compared | PASS | 10 retained warnings; CLI level fails | PASS | PASS | PASS | 279 retained findings; fails |
| Materialized family, retained raw records re-compared | PASS | 10 retained warnings; CLI level fails | PASS | PASS | PASS | 229 retained findings; fails |
| Native mirror, fresh CLI plus raw identity comparison | PASS | 10 retained warnings; CLI level fails | PASS | PASS | PASS | 229 retained findings; fails |

`A/validation-identities.json` independently re-compares all six levels' raw issue multisets and warning arrays using the inspected logical-file normalization, which removes documentation line shifts but retains diagnostic text and logical file. No new issue exists. Placeholder warnings concern ref_power/alpha in waste, fuel_handling, other_rpe, inc_cost and owner. No new unbound/undefined/self binding, unused definition or cycle exists. L6 still contains real inherited architecture/codegen findings; they are not waived globally. The two invalid validation-matrix Type warnings (`rel dev`, `rel dev\`) remain inherited.

| Suite | Entering | Candidate | Audit |
|---|---|---|---|
| Models | 428 pass, 13 skip | 539 pass, 13 skip | Raw statuses/messages individually compared; all 13 skips identical; no new failure |
| Study | 656 pass, 108 fail, 1 skip | 634 pass, 115 fail, 15 errors, 1 skip | 108 failures and skip identical; 22 new nodes retained explicitly |
| Focused numerical/calendar/family | — | Fresh 139 pass | `A/focused.log`, 25.16 seconds |
| Extra audit numerical grid | — | Fresh 282 pass | `A/check.py`, `A/checks.json`; 110-digit independent analytic equations |

Broad model/study suites and repeated smart regeneration were inspected from immutable evidence, not rerun merely to duplicate it. Fresh direct/full-native execution and family generation suffice for the checked claims. This is not an integration-stage return or a new study.

## Project standards and traceability

PR-1/PR-2 concern taxonomy/concept-analysis preparation; this repair adds no taxonomy or concept and preserves the existing scoped structure. PR-3 passes through the reviewed prototype/design and fresh family execution. PR-4 passes through explicit reporting of the unresolved consumer contradiction. PR-5 passes for the committed native phase chain and this owned audit artifact. Project MR-1/MR-2 account/component structure, MR-3 library separation, MR-5 output contract and MR-6 prior pattern preparation remain preserved. Project MR-4 has F2's new format defect. F3 is an additional inaccurate documentation claim.

AD-001 passes: numeric formals stay Real. AD-004 passes: definitions remain library analyses. AD-006's parameter/calculation separation is preserved. AD-002 metadata, AD-005 CAS types and AD-007 magnet ownership are unchanged; no new applicable deviation. AD-003 specifically addresses Hawker IFE DCF and adds no MFE requirement here. Existing global L6 findings remain separately recorded.

All four audited definitions have matrix rows; none lacks a doc comment or a matrix entry. The current matrix has empty Knowledge/Requirement cells on these rows. This is inherited on the three existing rows; the new LCOE row links native equations directly. The local project MR-4 explicitly supersedes matrix-based provenance with structured path citations, so no invented DI/PR mapping is required. The bounded Calendar Assumptions cell correction is accurate and its other cell values are unchanged. IDC/annuity rows are retained; LCOE was added through native PM. No PM tool repair occurred.

SV-090/091 remain passing on fresh evidence. SV-092 remains pending under the spec/final gate. No status mutation was needed; no positive item audit, close/archive or residual acceptance is issued.

## Execution notes and limits

All runtime commands used the isolated `.codex-test/run`; no synchronization, installation, production repair, historical mutation, source acquisition or quarantined traversal occurred. Native-probe invocation initially used relative paths and failed to import the package, then encountered the resulting existing scratch symlink on retry. A fresh absolute-path destination succeeded; both failure logs are retained under A. These are audit invocation errors, not candidate failures.

The first extra audit grid accidentally included nextafter(0), a subnormal outside the stated tested window. Its 110-digit power-difference reference was insufficient for ~1e-324 operands, so that result cannot establish production accuracy or a defect. The retained initial log records the rejected probe; the final grid uses specified-scale zero neighbors ±1e-18. Subnormal underflow, extreme overflow, arbitrary rates near minus one and untested durations remain unverified as already declared by the native spec/design. No new supported-domain restriction is inferred.

Return F1 for separately authorized consumer work and F2/F3 for bounded author corrections, then obtain fresh verification of the changed evidence and unresolved final gate. This audit makes no production, manifest, source, integration-promotion or merge decision.
