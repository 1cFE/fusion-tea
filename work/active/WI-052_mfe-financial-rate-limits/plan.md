---
Status: active
Created: 2026-09-12
Updated: 2026-09-12
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
  Review: ./review.md
---

# WI-052 implementation plan

## Authority and start gate

[INHERITED: implementation/baseline.md] The historical production hold is satisfied. The parent recorded plant-closure completion and authorized T-031 through the committed implementation brief at `93abdf4d`. All six implementation phases are authorized in this isolated checkout; the separate fresh audit remains required.

[AGENT] The six phases below implement spec.md@050054bd and design.md@239ca68e, independently reviewed PASS in review.md@1131d6bc. The coordinator's planning brief accepts the reviewed design for planning. Its historical draft/pending language is not an implementation approval. Review R1 is an accepted agent recommendation: add Last Updated verification dates with Source/Ref/Basis documentation. Checkboxes below record executed evidence; the independent audit owns its verdict.

Source documents: [design](design.md), [spec](spec.md), [review](review.md), [alignment](../../orchestration/mfe-financial-rate-limits.md), [routing](stage-provenance/spec-routing.md), [production hold](stage-provenance/production-hold.md), [MFE epic](../../backlog/epic-mfe-cost-modeling.md). Construction-duration zero remains parked. Source conflicts, scope changes, large baseline deviations, premise surprises and reserved decisions go to the parent before dependent work continues. Current study oracle/adapter migration and integration promotion are separately scoped downstream tasks.

## Design summary

Keep the existing four calculation interfaces and plant wiring. Complete the three finance definitions through native typed manual bodies and a shared stable financial helper; change only finance arithmetic in the existing calendar body. See design §§ Elements and interfaces and Numerical method and justification for the methods and their derivation.

## Prototype baseline and feasibility

The retained prototype consists of `prototype/factors.py`, `check_factors.py`, `build.py`, `execute.py`, `differential.py`, its materialized `models/` and native `generated/` package. Its output-only declarations, actual wrapper return order, shared-helper preservation and native wiring already satisfy design discovery. The [language](stage-provenance/external-language-expert.md) and [mathematical](stage-provenance/external-math-expert.md) consultations and four independent review standards notes satisfy the existing discovery obligations; no new language structure is proposed here.

| Recorded result, not rerun during planning | Required refinement |
|---|---|
| 6,421 independent 90-digit factor/PV checks; maximum error 7.802128119577708e-15 | Phase 3: retain tests against actual public production routes and the full spec grid |
| Native normal/smart preservation passes; ten full evaluations; 72 calendar checks | Phases 4–5: exhaustive boundary classes, independent energy ratio, all public fields, complete native ledger |
| L1/L3 pass; L2 ten warning identities unchanged | Phases 1–6: recapture current entering baseline and require no new scoped structural/dependency issues |
| L4/L5 pass; normative comments still incomplete | Phase 2: Source/Ref/Basis, timing, numerical method and Last Updated; Phase 6: traceability review |
| L6 has 229 findings, inheritance not certified | Phases 1 and 6: match every issue by identity and report changes; counts alone do not pass |

Definitions remain in library analyses with existing Real formals. No new model dependency, calculation definition, design input or output is needed. Generation must use the explicit MFE family in `tests/model_families.py`, not the whole heterogeneous canonical tree. Numerical probes certify their stated window only; overflow, subnormal underflow and other untested domains receive no acceptance credit.

## Execution conventions and validation strategy

All commands run with explicit workdir `/tmp/fusion-mfe-financial-rate-limits`. All Python/tool invocations use `.codex-test/run`, whose local launcher points to this isolated worktree and uses the retained runtime without synchronization. Read helper bodies and imports before execution. Restrict inventories to explicit model/package/test paths; no source/quarantine traversal, historical study/pin mutation, installation, or external-checkout writes.

Paths below are relative to that workdir. `I` denotes `work/active/WI-052_mfe-financial-rate-limits`; `G` denotes `exploration/stellarator_e2e/generated`. These are document abbreviations, not pre-existing shell variables. New implementation scripts must expose the commands specified below and write evidence only under `I/implementation/` or a fresh temporary destination. Do not execute prototype/build.py against production by changing its hard-coded root.

Each phase ends with an explicitly logged checkpoint: `.codex-test/run agentic-mbse validate --complete exploration/stellarator_e2e/models`. This includes parser, structure and dependency checks and records L4–L6. L1/L3 must pass and the scoped L2 delta must be clean; the spec's identity-matched inherited findings exception controls the generic clean-family rule. Preserve raw diagnostics, severity, element/file, message and exit code; normalize only root prefixes and unstable line positions, retaining original locations. Do not normalize away meaningful differences. Final validation also runs against a freshly materialized canonical family and the full canonical source tree for regression attribution.

Use the spec's relative error ≤1e-9 for every nonzero independent expectation, with no absolute floor; true zero uses absolute error ≤1e-9 in stated units. This overrides generic percent-level model-validation thresholds. Compare ordinary physical channels and verdicts exactly; financial differences require an independent reference and a named explanation. Log actual binary64 operands and both absolute/relative financial deltas. An entering singular financial result can be an expected repair, but is never an acceptable numerical reference.

## Phase 1 — Release hold and capture the entering state

**Overview and design reference:** Establish a reproducible baseline before mutation. Read design §§ Prototype and validation, Bindings and consumer handoff, Risks and stage state; spec §§ Acceptance cases and Scope and downstream handoff.

**Prototype baseline:** Prototype records describe an earlier source/package state. They do not establish the state after concurrent plant-closure work.

**Files:** NEW `I/implementation/capture.py`, `I/implementation/entering/`, `I/implementation/commands.md`, `I/implementation/baseline.md`; REFINE `I/plan.md` progress only.

- [x] Obtain the parent's recorded timing confirmation and implementation authorization; record its exact reference in baseline.md.
- [x] Inspect current status, commit, explicit family files, current package, runtime identity and direct-call routes. Compare them with the design baseline. If concurrent work changed them, recapture everything below before editing; route semantic conflicts or significant baseline changes to the parent.
- [x] Create capture.py and baseline.md. Capture read-only source/package byte inventories, full input keys/defaults, producer graph, every scalar, complete constraint responses/report and all verdict names. Record live and held ordinary cases before any mutation.
- [x] Capture native zero-discount, equal-rate and near-zero cases in both modes, recording entering errors as errors. Use the same fixed operating inputs for later comparisons; record overrides explicitly.
- [x] Inspect test imports and helper side effects before running. Identify current regressions versus historical fixture replays, particularly WI-050's four-body assertion and WI-051's fixed four-seed hashes. Do not execute broad preservation/source walkers.
- [x] Run `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/implementation/capture.py` after implementing and inspecting it. It must collect individual issue identities and test node IDs, raw logs and exit codes, not only counts.
- [x] Run `.codex-test/run agentic-mbse validate --complete models` and the phase checkpoint; retain all six levels for comparison. Materialize the MFE subset through `materialize_canonical_subset(MFE, destination)` for family-specific baseline validation.
- [x] Run `.codex-test/run python -m pytest tests/models/ -v` and `.codex-test/run python -m pytest tests/study/ -v` after side-effect inspection, saving node-level failures/skips. If a test would violate quarantine or historical-write restrictions, record its exact node and blocker instead of executing it; do not call that test passing.

**Test requirements and gate:** Baseline artifacts cover every input/scalar/verdict and retain individually identifiable failures. Unexplained baseline drift or inaccessible required checks blocks dependent certification. No production mutation until baseline capture and parent release are recorded.


## Phase 2 — Document and complete reusable finance

**Overview and design reference:** Refine library definitions before mirroring/generation. Read design §§ Elements and interfaces and Numerical method and justification, review § Findings R1.

**Prototype baseline:** Three output-only declarations and helper formulas work; prototype comments are not final normative documentation. Existing manual calendar still states verbatim financial identity.

**Files:** REFINE `models/library/analyses/mfe_account_costs.sysml`, `models/library/analyses/mfe_lcoe_dcf.sysml`, `models/library/analyses/mfe_lifecycle.sysml`; REFINE their same-named files under `exploration/stellarator_e2e/models/analyses/`; NEW `G/handwritten/mfe_account_costs/financial_factors.py`; REFINE `G/handwritten/mfe_account_costs/idc_closed_form_cost_impl.py`, `G/handwritten/mfe_account_costs/levelized_annual_cost_impl.py`, `G/handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py`, `G/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py`; REFINE `data/traceability_matrix.csv` through native PM operations where rows need updating.

- [x] Refine 'IDC Closed-Form Cost' in mfe_account_costs.sysml: preserve all three input names/Real types and cost output; replace evaluated intermediates with normative equation documentation and output-only cost.
- [x] Refine 'Levelized Annual Cost' in the same file: preserve five Real inputs, crf and levelized output names; document construction escalation and first-payment timing; retain output-only declarations.
- [x] Refine 'LCOE DCF' in mfe_lcoe_dcf.sysml: preserve seven Real inputs and lcoe; document CRF and the distinct midpoint construction factor.
- [x] Refine 'Lifecycle Calendar' in mfe_lifecycle.sysml: preserve input/output groups and eleven declarations; amend the obsolete verbatim-finance description while retaining event/physical semantics.
- [x] Complete Source/Ref/Basis and Last Updated for each of those four definitions and corresponding changed manual bodies. Cite scoped native equations and design derivation; distinguish inherited external citations from sources actually verified now.
- [x] Implement financial_factors.py with typed pure crf, annuity_pv, idc and periodic_pv functions using the reviewed methods; retain exact limits, Real durations and the justified IDC numerical switch. Add module citations and unit/timing descriptions.
- [x] Refine run_idc_closed_form_cost, run_levelized_annual_cost and run_lcoe_dcf with typed input classes and AUTO_IMPLEMENTED=False. Verify emitted annuity return order `(levelized, crf)`.
- [x] Refine calendar `_crf`, held PV/annualization, live dated PV and dated-energy discount weights only. Preserve `_clip`, mode/domain validation, interval walk, counts, event dates, terminal treatment, energy-bin overlaps and accumulation order.
- [x] Copy each of the three canonical files to its named family mirror and prove byte equality. Inspect existing generic/stellarator bindings; no edit is expected. Route any unexpectedly required interface change before proceeding.
- [x] Inspect/update the four relevant traceability rows using `.codex-test/run agentic-mbse pm trace-element` with verified existing identifiers; record resolved citations and avoid duplicating rows or inventing a new DI.
- [x] Run the phase validation checkpoint and inspect names, imports, Real types and unchanged formals/output inventory. Log the exact scoped delta.

**Test requirements and gate:** No new definition-count/interface/structural/dependency failures. Typed body compilation and imports will be exercised after native completion in Phase 3; do not treat these edited handwritten files as an executable package until then. Documentation fully explains the retained equations and accepted R1 date field.

## Phase 3 — Native completion and independent factor/public tests

**Overview and design reference:** Make generation and direct public modules exercise the repaired methods. Read design §§ Elements and interfaces, Numerical method and justification, Prototype and validation.

**Prototype baseline:** build.py proves preserved manual/helper regeneration; check_factors.py supplies independent 90-digit references. Current regression helpers still assume four manual bodies and can silently miss the extra helper or reject the new inventory.

**Files:** NEW `I/implementation/regenerate.py`, `I/implementation/reference_finance.py`, `tests/models/test_mfe_financial_rate_limits.py`; REFINE current-package caller portions of `tests/models/test_mfe_operating_heating.py` and `tests/models/test_mfe_major_radius.py` as needed to use the new helper; REFINE generated family artifacts under `G/` through native generation only.

- [x] Create regenerate.py using explicit current normative seeds, including the three new manual finance bodies, calendar, unchanged unrelated manual bodies and financial_factors.py. Reject nonfresh temporary destinations, missing/extra/mismatched seeds and symlink seeds. Inspect all helper imports before running.
- [x] Provide a current-package completion route independent of historical four-body fixtures. Adapt actual current regression callers to it while retaining historical fixture replay and refusal tests on their original evidence. Preserve WI-050/WI-051 frozen expectations and old implementation evidence; replace current assumptions at the caller rather than rewriting historical records.
- [x] Generate from a fresh materialized canonical MFE subset, install explicitly inventoried bodies, and inspect all four public wrappers. Record generated signatures, output order and package import locations.
- [x] Create reference_finance.py using at least 60-digit arithmetic (retain 90 digits or more): explicit dated integer cash-flow sums and independently evaluated fractional powers/IDC expressions. Do not import production factors or the current study oracle to calculate expectations.
- [x] Create SV-090 tests in test_mfe_financial_rate_limits.py for each helper and each public module: separate CRF, stream PV, levelized charge, tiny IDC factor and currency cost, midpoint multiplier, DCF numerator and price. Retain the $1M equal-rate annuity and $1B/$10M zero-discount DCF regression referents with recomputed high-precision expectations.
- [x] Cover rates 0, 0.02, 0.08 and both signs of 1e-4, 1e-8, 1e-12, 1e-16, 1e-18; equality at 0, 0.02, -0.02; either rate zero; both signs of requested differences around 0 and 0.02. Record rounded equality using actual operands.
- [x] Cover N=30/30.5, T=8/8.5 and the justified duration window 0.25, 0.5, 1 and its binary64 neighbors, 100.5 and 200.5. Test exact and adjacent signed IDC switch cases, exact one-year zero and inherited subannual negative IDC.
- [x] Run `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/implementation/regenerate.py` with its safe scratch default; run `.codex-test/run python -m pytest tests/models/test_mfe_financial_rate_limits.py -v`; run the phase checkpoint.

**Test requirements and gate:** All factor and public-route cases pass the spec tolerance without skipping the native path. Actual native return order and imports are proven. No current helper omits the extra module or carries stale generated arithmetic; no historical expectation was rewritten to force a pass.

## Phase 4 — Calendar boundary and energy tests

**Overview and design reference:** Verify the calendar independently of prices. Read design §§ Numerical method and justification and Risks and stage state; spec § Acceptance cases SV-091.

**Prototype baseline:** 72 public calendar checks independently verified PV/annualization and physical invariance; exhaustive boundary classes and independent dated-energy ratio remain missing.

**Files:** NEW `tests/models/test_mfe_financial_calendar.py`; REFINE `I/implementation/reference_finance.py`, `tests/models/test_lifecycle_calendar.py`; REFINE calendar body only if a scoped numerical defect is demonstrated.

- [x] Create SV-091 public-wrapper tests asserting exactly eleven named outputs in emitted order: availability, coil_life_margin_fpy, replacement_pv, planned_downtime_yr, terminal_downtime_yr, unplanned_downtime_yr, productive_fpy, dated_energy_ratio, cas72_annual, n_replacements, physical_life_fpy.
- [x] Independently derive held event dates/counts and live event dates/online intervals. Verify event diagnostics too, although events are not exported scalars. Use exact representable fixtures to distinguish arithmetic rounding from changed event semantics.
- [x] Cover held wall-load floor at 1e-6, lifetime floor 0.5, cap N*A including cap below floor, integer N/interval count transitions, zero/multiple events, and positive fractional horizons. For each threshold test exact and adjacent representable inputs on both sides; record actual operands and whether the represented branch really changes.
- [x] Cover live q_n=0 infinite physical life, no events, multiple events, zero outage, run ending exactly at N, completion t_k+d exactly at N and adjacent sides, retirement inside outage, and terminal downtime. Include nonzero unplanned fraction and noninteger N.
- [x] Cross every boundary class with zero, ordinary and signed nearby rates from SV-090. Compare all eight physical outputs and event sequences exactly against entering execution at identical inputs and across finance-only rate changes. Preserve legitimate infinity only in physical life.
- [x] Independently calculate dated replacement PV and CRF annualization at high precision; check each separately, including zero-event and zero-cost cases. Do not use their quotient to certify them.
- [x] Implement an independent dated-energy reference from interval intersections with commissioning year bins and discounted year lengths. Cover integer/fractional horizons, boundaries near ceil(N-1e-12), segment starts/ends at year boundaries and adjacent values, terminal downtime, zero interest and signed nearby rates. Check numerator and denominator as well as ratio; held ratio remains exactly 1. Preserve the existing bin rule, including its epsilon, without interpreting it as new timing policy.
- [x] Refine the existing held-finance identity regression in test_lifecycle_calendar.py to independent numerical expectations under the approved routing; keep exact physical comparisons. Leave verify_stellaris.py and study adapters unchanged.
- [x] Run `.codex-test/run python -m pytest tests/models/test_mfe_financial_calendar.py tests/models/test_lifecycle_calendar.py -v` and the phase checkpoint. Record each boundary class and actual branch, not only a case count.

**Test requirements and gate:** Every eleven-output boundary case has independent financial checks and exact physical/event preservation. Any apparent boundary movement is investigated against the entering represented-input behavior before changing code. No final-price or existing-oracle parity substitutes for energy-ratio independence.

## Phase 5 — Full native attribution and repeat regeneration

**Overview and design reference:** Establish production-wide preservation and public execution. Read design § Bindings and consumer handoff and spec § Acceptance cases SV-092.

**Prototype baseline:** Ten native runs were smoke checks, not a complete before/after census. Fresh-generation support now exists from Phase 3.

**Files:** NEW `I/implementation/execute.py`, `I/implementation/scalar-ledger.json`, `I/implementation/native-results.json`, `I/implementation/regeneration.json`; REFINE `tests/models/test_mfe_financial_rate_limits.py`; REFINE `exploration/stellarator_e2e/stellarator.snapshot.json` and `tests/models/data/mfe_census.json` only if the current native contract requires refresh, deriving them from generation rather than hand-editing fingerprints.

- [x] Create execute.py to run entering and candidate native packages in separate import contexts at identical fixed inputs: ordinary baseline, zero discount, equal rates and signed tiny rates, each held and live. Compare complete named verdict outcomes/responses/reports; retain any pre-existing violated engineering gate.
- [x] Assert input key/default, public output name/order and producer-edge preservation. Create a full scalar ledger with entering/candidate values, exact/relative deltas, producer, consumers, classification and independent-reference coverage. Classify every scalar as changed finance, unchanged physical/other or newly added (expected none).
- [x] Check every physical scalar exactly, including availability feeding fuel and both energy denominators. Explain each changed financial scalar through independently checked factor/PV arithmetic or marked downstream propagation. Bound ordinary changes by the spec tolerance against independent reconstruction; stop on unexplained changes.
- [x] Identify CRFs and charges for CAS71/CAS80, reported IDC, all calendar outputs, CAS70, comparison CAS90, headline DCF and comparison LCOE using actual `stellarator_09__stellaris__` names. Include internal factors in test evidence even if not exported.
- [x] Repeat native generation with preserve_handwritten=True, then with preserve_handwritten=True and smart_regen=True. Verify the complete package tree, helper and unrelated manual bytes survive; rerun public and native cases on the regenerated result.
- [x] Verify the three canonical/mirror pairs byte-for-byte and refresh any native snapshot/census only through inspected current generation. Recheck the entering production inventory immediately before replacing production outputs; concurrent drift requires baseline recapture and parent routing if material.
- [x] Run `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/implementation/execute.py`; rerun both new scoped test files and the phase checkpoint. Preserve raw native results and regeneration inventories.

**Test requirements and gate:** Complete scalar and verdict accounting, no new exposed scalar, no unexplained financial delta, exact physical preservation and successful regenerated public/full-native execution. Native family regeneration is within the item after release; integration-seam promotion remains downstream.

## Phase 6 — Integration, validation and independent audit handoff

**Overview and design reference:** Close acceptance evidence, then hand it to a fresh auditor. Read design §§ Implementation checklist and Risks and stage state, review §§ Evidence and limitations and Accepted changes and next step.

**Prototype baseline:** L6 issue inheritance, full regression identities, normative citations and complete consumer handoff are not certified by the design evidence.

**Files:** NEW `I/implementation/validation-differential.json`, `I/implementation/regression-differential.json`, `I/implementation/validation-report.md`, `I/consumer-handoff.md`; REFINE `modeling_project/VALIDATION_MATRIX.md` through native PM; NEW `I/audit.md` and audit evidence owned exclusively by the fresh auditor.

- [x] Run `.codex-test/run agentic-mbse validate --complete exploration/stellarator_e2e/models`, the fresh materialized canonical MFE family and `.codex-test/run agentic-mbse validate --complete models`. Match each L1–L6 issue to the entering record by identity; classify retained, repaired and new issues. No count-only L6 acceptance.
- [x] Run `.codex-test/run python -m pytest tests/models/ -v` and `.codex-test/run python -m pytest tests/study/ -v` after the same side-effect inspection as Phase 1. Match failing/skipped node IDs and reasons individually. New failures require fixes or explicit unresolved blockers; a downstream unstable-oracle mismatch is reported as current, never mislabeled inherited.
- [x] Review all four changed definitions' citations and dates, helper/body method documentation, canonical/mirror equality, complete traceability rows and unchanged binding architecture. Verify no new design-layer calc or cycle.
- [x] Write validation-report.md with commands, exits, six-level issue details, regression identity differences, residual limitations and links to numerical/native evidence. Complete SV-090, SV-091 and SV-092 evidence; update each passing status through `.codex-test/run agentic-mbse pm update-validation SV-090 --status passing` and corresponding SV-091/SV-092 commands only when that entry is actually proven. Unrelated invalid-Type warnings remain individually recorded.
- [x] Write consumer-handoff.md from the actual pipeline and exhaustive scalar ledger. Include the producer edges in design § Bindings and consumer handoff, exact emitted names, changed finance channels, unchanged physical channels, factor/PV independence versus propagated evidence, and the separately pending current oracle/adapter and integration promotion tasks.
- [x] Verify MR-WI052-1: all exact identities and both original counterexamples pass with distinct finance conventions preserved.
- [x] Verify MR-WI052-2: each nonzero factor, PV, charge and price meets ≤1e-9 relative error; true zeros meet stated absolute tolerance.
- [x] Verify MR-WI052-3: Real/fractional duration cases and numerical switch boundaries pass with documented method/window justification.
- [x] Verify MR-WI052-4: live/held zero and nearby rates, zero events, all boundary classes and eleven outputs preserve physical/calendar semantics.
- [x] Verify MR-WI052-5: unchanged operating inputs, exact physical/verdict comparison, retained account/currency/timing meaning and every financial delta attributed.
- [x] Verify MR-WI052-6: canonical/mirror/native/direct routes, preserved signatures/order, repeated generation, no new scoped structural/dependency issues and individual inherited-failure matching.
- [x] Verify MR-WI052-7: resolvable citations, complete scalar/producer handoff and clearly identified independent coverage.
- [x] Request a fresh non-author audit-models stage through the parent with spec, design, review, this checked plan and all implementation evidence. Record actual dispatch/session receipts. The implementing author does not write or predeclare the audit verdict.

**Final gate:** All scoped numerical/native acceptance checks pass; every remaining six-level/regression issue is individually explained without falsely claiming a clean full suite. Any unresolved new failure prevents repair certification. Positive fresh independent audit is the completion boundary; source adoption, residual acceptance, study execution, integration promotion and close/archive remain outside this item.


## Feasibility concerns and coordination

[AGENT] Execute production mutations serially. The canonical edits, helper interface and native generation share dependencies and do not form three independent file tasks; no parallel write batch is required. A parent may delegate independent test-reference work with explicit disjoint ownership, but integration and baseline capture remain one owner's responsibility.

The main risks are stale preserved autogenerated bodies, historical four-body helper assumptions, tuple-order errors, branch cases rounded to equality, tiny IDC errors hidden by final prices and concurrent baseline drift. The explicit seed inventory, current-caller adaptation, public-wrapper tests, actual-operand logs, separate references and pre-replacement inventory check address those risks. If evidence reveals a domain/timing conflict, park dependent conclusions and return it to the parent; this plan authorizes no new economic interpretation.

## Execution notes — 2026-09-12

[AGENT] Phases 1–5 executed in the isolated worktree. Entering models: 428 passed / 13 skipped in 78.20 seconds. Entering study suite: 108 failed / 656 passed / 1 skipped in 829.56 seconds; individual results are retained. Candidate models: 539 passed / 13 skipped in 79.80 seconds. The 126 scoped finance/calendar tests pass; subsequent final documentation-only regeneration is checked by the scoped and family-spine tests. Ten native cases each expose the same 158 scalars, with exact physical outputs and complete reports/responses preserved. Ordinary finance deltas are at most 4.741e-15 relative. See `implementation/commands.md`, raw logs, JUnit files and scalar ledger.

[AGENT, parent-routed] The installed trace-element operation is add-only. The native implement-model skill §3 separately directs traceability updates. The parent authorized the minimal Calendar Assumptions cell correction and native creation of the missing LCOE row. IDC and annual-cost rows retain their existing identifiers, dates and inherited equation citations. No PM operation or tool was modified.

[AGENT] Current WI-050/051 callers now use current completion/finance tolerances while historical drivers, four-seed refusal fixtures and hash receipts remain unchanged. `test_model_family_spines.py` also required caller adaptation because it imported the historical four-seed generator. This is the same current-package completion obligation, not a historical fixture rewrite.

[AGENT, parent-routed] The final gate is unmet. The repaired executable invalidates the current study manifest generation pin, producing new `manifest_currency` failures in previously passing downstream tests. The parent directed an implementation-ready but uncertified handoff, exact failure collection and fresh audit judgment before a separately scoped consumer/manifest prerequisite. SV-090/091 pass; SV-092 remains pending. No new failure is reclassified as inherited.

[AGENT] Final study suite completed: 115 failed / 634 passed / one skipped / 15 setup errors in 743.25 seconds. The 108 inherited failures and inherited skip match exact node IDs and reasons. The 22 new nodes comprise 21 stale-manifest-generation consequences and one current-consumer exact frozen-finance assertion at a verified relative delta of 1.873e-16. Both prerequisite classes remain unresolved here. `implementation/new-downstream-failures.json` is the complete list. The final gate and SV-092 remain pending.

## Documentation repair — 2026-09-12

[INHERITED: T-032 documentation-brief.md@070fb40e] The parent authorized a fresh bounded implement-model correction of audit F2/F3. Four supplemental Source fields now name direct canonical paths with definition-specific equation locators; DT Fuel Cost accurately describes its generated arithmetic. Canonical/mirror copies and derived package/snapshot documentation were refreshed. See [repair evidence](repair-1/report.md).

[AGENT] Targeted checks pass: L1 on all 23 family files; identical source/snapshot package generation; eight manual seeds unchanged; SysML outside doc comments and Python executable ASTs unchanged; ten native cases with 158 scalars each exactly equal to the retained audit, including inputs, responses and reports. The semantic fingerprint is unchanged; documentation bytes move executable identity to `1a7c216dabff8425c279f6b3c2781629115729173fc0b406600497ac348b4340`. The historical audit verdict and evidence are preserved. F1, SV-092 and the final gate still require the separate current-consumer stage and fresh audit.

## Fresh completion audit — 2026-09-12

[AGENT] The three remaining completion boxes are now supported by the fresh non-author audit under T-032 brief `6aa5abad`, final consumer evidence `614032136b7918a47a889a73147ca51dc15511e2` and corrected model `708dddef`. See `../../analysis/20260912-wi052-financial-completion-audit.md` and `completion-audit-evidence/`. Original findings F1–F3 are resolved, all seven requirements pass within the tested window, and native PM updated SV-092 to passing. Original validation-report.md and historical negative audit remain unchanged; this completion report supplements their earlier state. Fresh 359 consumer tests, ten-case exact native reproduction and unchanged six-level issue identities pass. All broader limitations remain; no close/archive or integration promotion.
