---
Verdict: FAIL
Implementation: 2ee448830c891c05532088c63e41eae46e9d893c
Created: 2026-09-11
---

# WI-049 independent native audit

## Verdict and scope

**FAIL: one new citation defect requires a bounded repair. Numerical and execution checks pass.** MR-WI049-1 through -5 pass; -7 fails the required Source-field format; -6's execution obligations pass but its positive independent-audit completion gate remains unsatisfied. No numerical repair, financial reinterpretation or study refresh is requested by this finding.

[INHERITED: parent audit brief] Scope is all seven WI-049 requirements, SV-076–078, directly affected model/source/traceability records, native IFE generation and supported consumers. Parent confirmed scope and retained routine stage authority. The author of this report is independent of spec, design and implementation. Read-only source review used registered Hawker extraction, with no fresh image-certification claim. Unchanged WI-048 source facts inherit the [positive WI-048 audit](20260911-045617_audit_WI-048_ife-operating-point-repair-r1.md); they are not claimed as fresh source-image checks.

The audit reviewed spec, design, review, plan, immutable entry baseline and implementation records, then independently executed current production and temporary generated packages. Primary changes are `models/library/analyses/ife_lcoe.sysml`, `models/designs/generic_ife/ife_plant.sysml`, their synchronized IFE copies, generated package and direct execution helpers. No production or author-artifact edits were made. This report and its [evidence directory](20260911-ife-zero-audit-evidence/) await the parent's commit.

## A01 — Required Source field contains a title

**FAIL, MR-WI049-7 and project MR-4.** At `models/designs/generic_ife/ife_plant.sysml:112` and `:122`, the two new duration comments put `Hawker, A simplified economic model for inertial fusion` in **Source**. The same lines exist in `exploration/ife_e2e/models/designs/generic_ife/ife_plant.sysml`. Project `modeling_project/REQUIREMENTS.md:49,54` requires Source to be a direct artifact path. The correct path is present in Reference, so the authority is discoverable and both numerical values are correct; that does not satisfy the mandatory Source field.

Recommendation: replace those two Source values with `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`, synchronize the twin, regenerate affected native artifacts through the supported preservation route, and independently recheck citation resolution and unchanged numerical/package semantics. The author must amend the implementation's claim of complete citation compliance. This audit does not make those repairs.

The CSV rows at `data/traceability_matrix.csv:92–94` are a separate convention: Source_Document may be a title, while Source_Location carries the resolving file locator. Those rows meet the installed matrix schema and are **not** a second defect. No missing new definition row was found. The factor and LCOE definitions have direct Source paths and references at `ife_lcoe.sysml:24–30,136–141`; the generic plant and inherited guard have current matrix rows at CSV lines 89 and 85. Inherited blank DI/PR links on the derived guard remain explicitly described in WI-048's audit; no new project requirement or insight is invented.

## Fresh numerical verification

The [audit probe](20260911-ife-zero-audit-evidence/probe.py) independently reconstructs annual physical/cost quantities in 90-digit Decimal arithmetic. It imports baseline input values and required boundary referents, not the implementation's financial oracle. Integer cost and energy are independently summed at explicit calendar dates; fractional cases use Decimal difference-of-powers algebra. The shipped sealed public evaluator supplies actual results. Every nonzero channel uses relative tolerance **1e-9**; only true zeros use absolute **1e-9** in channel units. Generic percentage audit thresholds do not weaken the item contract.

Hawker `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141–148` defines discounted annual streams and five construction/forty operation years. The following Eq. 2.2 and cost paragraphs support the separate energy and cost streams. Integer construction dates are 1 through Yc, with operation Yc+1 through Yc+Nop. For nonzero d, the implemented `-expm1(-n*log1p(d))/d` equals `(1-(1+d)^(-n))/d`. Both ratios approach their derivative limits at d=0, giving n. The operation factor includes the construction delay. Its exact-zero branch includes negative zero. No near-zero clipping or approximate-series switch exists.

| Quantity / location | Model or result | Independent source/reference | Discrepancy / status |
|---|---|---|---|
| Construction default, `ife_plant.sysml:109` | 5.0 years, Real | Hawker extraction `:148`, 5 years | 0%; numerical PASS; A01 citation format FAIL |
| Operation default, `ife_plant.sysml:119` | 40.0 years, Real | Hawker extraction `:148`, 40 years | 0%; numerical PASS; A01 citation format FAIL |
| Rate input and varied durations, `ife_lcoe.sysml:143–145` | Required signed rates and six duration pairs | Spec acceptance/design window; test-specific, not new source defaults | PASS; no new domain policy |
| Construction factor, `ife_lcoe.sysml:146` | A(Yc,d); zero limit Yc | Independent dated sums or fractional powers | PASS across 268 cases |
| Operation factor, `ife_lcoe.sysml:147` | Delayed A(Nop,d); zero limit Nop | Independent dated sums or fractional powers | PASS across 268 cases |
| Discounted cost, `ife_lcoe.sysml:122` | Zero baseline about 58,111,257,843.81798 dollars | Independently summed construction and operation costs | PASS, checked separately |
| Discounted energy, `ife_lcoe.sysml:123` | Zero baseline about 274,751,655.9428571 MWh | Independently summed dated generation | PASS, checked separately including signed/zero energy |
| Eligible price, guard at `ife_lcoe.sysml:150` | Zero baseline about 211.5046682590476 dollars/MWh | Independent cost/energy quotient for generators | PASS; exact invalid zero otherwise |
| Thirty inherited 8% output channels | All names retained, plus two factors | Immutable `entry-baseline/baseline_result.json` | Maximum relative change 1.421702266930599e-16; both verdicts exact; PASS |
| Unchanged annual/power/cost constants | 31557600 seconds for shots; 8760 hours for energy; original replacement and Meier expressions | Inherited WI-048 source verification plus fresh unchanged-expression diff and source-oracle regressions | PASS for preservation; mixed dollar basis remains unresolved |

Full actual/reference numbers and per-channel errors for every case are in [numerical.json](20260911-ife-zero-audit-evidence/numerical.json). All **268 cases pass**, maximum residual **5.995204332975845e-15**. They cover the three required operating points, 14 rates, required 5/40 and 5.5/40.5 durations, four additional duration pairs, generating ±50% cases and four positive neighbors. The finite window exercises subannual and long durations without claiming arbitrary-Real representability. Existing extreme overflow/underflow limits remain.

## Requirement and completion gates

| Requirement | Status | Evidence |
|---|---|---|
| MR-WI049-1 | PASS | Fresh zero and signed-rate integer date sums, independent cost/energy reconstruction; probe and numerical.json. |
| MR-WI049-2 | PASS | All five checked numerical channels finite and individually below 1e-9; 268 cases. Retained tests also reject separate-channel cancellation and inappropriate absolute floors. |
| MR-WI049-3 | PASS | Real inputs/defaults and shared bindings at plant lines 109–169; fractional power oracle, six duration pairs, signed zero and both sides of the sole zero branch. Duration mutation tests execute. |
| MR-WI049-4 | PASS | Exact net verdicts, both flags and invalid sentinels checked across required cases. Zero/negative diagnostics complete. Four +2.5 W neighbor cases remain eligible. Both supported consumer functions and direct module path execute in fresh tests. |
| MR-WI049-5 | PASS | All thirty immutable 8% channels and two verdicts preserved. Fresh physical/source-oracle tests and source diff show unchanged cost streams, time constants, replacement charges, Meier, labels and power balance. |
| MR-WI049-6 | INCOMPLETE | All execution/validation obligations pass at their specified scope; positive independent audit gate blocked by A01. No new execution defect found. |
| MR-WI049-7 | FAIL | A01: two new duration Source fields fail project MR-4. Factor derivation, dates, financial interpretation and matrix locators otherwise resolve. |

Plan Phase 1's numerical/structural work passes, but its complete citation gate does not. Phase 2's execution, migrations and native regeneration pass. Phase 3's numerical, regression and diagnostic-attribution gates pass; final independent acceptance awaits A01 repair. Checked implementation boxes are delivery evidence, not grounds to override this failed gate.

SV-076, SV-077 and SV-078 remain **passing**: this audit independently reproduces their numerical/behavioral checks. Their existing Test pointers resolve to retained acceptance tests and implementation evidence. No native PM status update is needed; these rows do not certify MR-WI049-7 or the entire work item.

## Execution and six-level validation

All Python/model commands used `.codex-test/run`; executable tests used `PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1`. Fresh command: `python -m pytest tests/models/ tests/test_ife_consumer_eligibility.py -q` within that launcher/environment. Result: **376 passed, 13 skipped** in 20.92 seconds. Skips are the inherited example customization and twelve missing-foundation tests; every WI-049 acceptance test executed. The historical independent integer cross-check also succeeds and retains its explicit separation from computed Osiris.

Fresh native validation ran `agentic-mbse validate --complete --verbose` on both the IFE twin and `models/`. Logs are in the evidence directory.

| Level | IFE family | Wider tree |
|---|---|---|
| 1 syntax | PASS, 11 files, zero errors/warnings | PASS |
| 2 structure | PASS, zero issues | FAIL, 10 inherited MFE placeholders |
| 3 dataflow | PASS, zero cycles | PASS |
| 4 constraints | PASS, 2/2 admitted numerical, 100% executable | PASS |
| 5 documentation | PASS, 30/30 documented | PASS |
| 6 architecture/readiness | FAIL, 50 retained issues | FAIL, 277 issues |

L5 checks documentation presence and does not contradict manual finding A01. A fresh structured native L6 inventory was compared against the retained preimplementation inventory by a multiset of file, element, rule and message, allowing only moved line numbers: **50 retained, zero new, zero resolved**. See [attribution.py](20260911-ife-zero-audit-evidence/attribution.py), [l6-current.json](20260911-ife-zero-audit-evidence/l6-current.json) and attribution.txt. The unchanged wider findings match prior WI-048 evidence; no blanket project pass or inherited-debt acceptance is claimed.

The typed factor function returns operation then construction at `generated/handwritten/ife_lcoe/ife_present_value_factors_impl.py:5–15`, matching generated named outputs. Both completions are copied and import-adjusted by `tests/ife_execution.py:16–27`. Public sealed execution succeeds on the shipped package; fresh temporary packages execute duration mutations, zero/fractional cases and both regeneration routes. A disposable byte-for-byte copy of the shipped package also reproduces all **55 files** under preservation and preservation-plus-smart generation. Production was not rewritten by this audit. The exact 19-entry census preserves Real 5/40 defaults with the accepted two duration-key migrations; 32 outputs retain all thirty previous names.

## Project requirements, architecture and deferred impact

| Obligation | Scoped disposition |
|---|---|
| Project MR-1 / MR-2 | Inherited F08 CAS/interface gap remains separately open, as in WI-048 audit; this factor repair adds no cost-bearing component and does not certify the broader project. |
| Project MR-3 | PASS for new scope: reusable factor definition in library analyses, plant values/usages in designs; no new design calc definition. Existing generic-IFE placement is inherited. |
| Project MR-4 | FAIL A01; new factor and directly affected matrix references otherwise resolve. |
| Project MR-5 | PASS for preserved comparison outputs; standard cross-concept schema remains historically unspecified and monetary normalization remains unresolved. |
| Project MR-6 / PR-3 | PASS: committed design, early prototype and fresh design review precede implementation. |
| PR-1 | Existing IFE repair inherits established taxonomy/selection; no new concept admission. |
| PR-2 | Existing shared/divergent decomposition retained; no new cross-concept decomposition. |
| PR-4 | PASS: actual renderer limitations and migration tradeoff were surfaced; this citation finding returns for correction. |
| PR-5 | Prior phase artifacts committed through audited HEAD. This independent report is ready for parent commit. |

AD-001 is respected through Real values and stated units; AD-004 through library placement; AD-006 through independent arithmetic inputs and parameter bindings. AD-003's single-calc wording has a bounded departure explicitly accepted by the parent and design review at `3a2bc1e5`: stable factors are a separate typed completion, while the closed-form financial interpretation is unchanged. AD-002 metadata and AD-005 CAS structures are unchanged inherited scope, not recertified. AD-007 concerns MFE and does not apply to this repair.

Deferred study impact is concrete: `exploration/ife_e2e/studies/study_route.py` and its manifest retain old channels/pin; `tests/study/test_ife_native_route.py:46,90` expects 30 channels. The study oracle imports the newly migrated BASE but its duration checks at `oracle_entry.py:22` still use old suffixes. Immutable prior context retains old entry names and identity. The implementation's separate **10 failed / 7 passed** study-route run is inherited evidence, not rerun or repaired here. Study readiness and pin promotion are outside this numerical acceptance contract.

## Frozen identity and return

Audited HEAD: `2ee448830c891c05532088c63e41eae46e9d893c`. Native semantic fingerprint: `8596c899df17f763bbce6eb50a18c1b5bca83080c40233e40bc01a7bb1aa1888`. Native executable fingerprint: `2810897c4ef9db8cb646aec5616884de42963c41e3b92ac20c2947450ffcbfd7`. These match the inspected sealed contracts and successful public execution.

Return **FAIL A01** to the parent for a fresh bounded author repair and re-audit. Monetary normalization, remaining MFE F05, inherited validation debt and study refresh remain unresolved separate work. No source approval, residual acceptance, requirement promotion, commit, close/archive, merge/push or goal close occurred.
