---
Status: approved
Created: 2026-09-11
Updated: 2026-09-11
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
  Review: ./review.md
---

# WI-049 implementation plan

[AGENT] Parent approved all three implementation phases on 2026-09-11 after review of the accepted design and plan. Routine stage approvals are covered by the grounded goal. The implementer returns evidence for fresh independent audit; it does not certify its own work.

## Authority and source documents

[AGENT] This plan refines the accepted prototype under the parent's stage authority. Requirements remain those in [spec.md](spec.md); architecture comes from [design.md](design.md), accepted after [review.md](review.md) PASS at `3a2bc1e5`. The related epic is [IFE Cost Modeling](../../backlog/epic-ife-cost-modeling.md). The parent owns routine stage acceptance, commits and the fresh independent audit. Return semantic conflicts or missing shared capabilities to the parent before dependent work.

## Design summary

A typed native completion evaluates the two present-value factors using `log1p`/`expm1` and the exact-zero limit. The existing IFE calculation combines those factors with its existing annual quantities; the plant supplies shared Real durations to both calculations. See design sections **Elements and dataflow**, **Evaluation and numerical argument** and **Interfaces and deferred impact** for equations and interface decisions.

## Prototype baseline and phasing

[INHERITED: design.md, Prototype and validation] `prototype/build.py` materializes the eleven-file IFE family; only `prototype/models/analyses/ife_lcoe.sysml` and `prototype/models/designs/generic_ife/ife_plant.sysml` differ from production. `prototype/factors_impl.py` and `prototype/execute.py` implement and exercise the typed completion. Production refinement must change the package import from `wi049_probe` to its native package identity.

[INHERITED: prototype/execution.json, positive-neighbor.json, validation.txt] All 264 sealed evaluations pass independent 80-digit references, with maximum relative error `6.026965908260528e-15`. Four positive-neighbor cases also pass numerically. Preservation and preservation-plus-smart regeneration are byte-stable. Levels 1–5 pass; Level 6 reports 50 static/EXPOSE issues. Equality of counts is not attribution: Phase 3 compares individual issues against the pre-change family. Phase 1 completes the L5 comment follow-through; Phase 3 reviews L4 coverage and L6 debt.

The parent retained the complete pre-change 30-output/two-verdict baseline in [entry-baseline/](entry-baseline/), captured from production revision `f4bf57cf` and committed with stage evidence at `3a2bc1e5`. Treat those files and prototype evidence as immutable inputs. Use a new `implementation/` directory for implementation evidence.

Three phases follow dependencies: source definitions and wiring; native package and caller migration; full numerical/integration certification. Work is small and coupled, so execute sequentially. Mark each checkbox and record evidence immediately after completion. Every phase ends with Levels 1–3 passing; final validation covers Levels 1–6. Optional parent review can occur after Phase 1 or before audit, without an owner approval request.

## Phase 1 — Refine production definitions and wiring

**Design reference:** **Elements and dataflow**, **Evaluation and numerical argument**, **Prototype and validation**; review finding **Production documentation follow-through**. The validated prototype already supplies the executable shape. This phase ports it and completes its comments before regeneration.

**Files:** REFINE `models/library/analyses/ife_lcoe.sysml`, `models/designs/generic_ife/ife_plant.sysml`, `exploration/ife_e2e/models/analyses/ife_lcoe.sysml`, `exploration/ife_e2e/models/designs/generic_ife/ife_plant.sysml`, `data/traceability_matrix.csv`; NEW `tests/models/test_ife_zero_discount_repair.py`, `implementation/` evidence under this item.

- [ ] Before edits, retain a complete verbose validation report for the current IFE twin under `implementation/validation-before.txt`: `.codex-test/run agentic-mbse validate --complete --verbose exploration/ife_e2e/models`. Preserve diagnostic identities, not only totals.
- [ ] REFINE canonical `ife_lcoe.sysml`: add `'IFE Present Value Factors'` with the three Real inputs and two output-only Real factors from the prototype. Document dimensionless rate and years for durations/factors, integer payment dates, fractional algebra and exact-zero limits. Include resolving **Source**, **Reference**, **Ref**, **Basis** and **Last Updated** fields pointing to registered Hawker `output.md:141–148` and the derived identity in this design.
- [ ] REFINE `'IFE LCOE'` in that file: add `pvf_construction` and `pvf_operation` inputs before intermediate/output features, remove the subtractive factor definitions, and replace the obsolete introductory description. Preserve all physical, annual-cost and discounted-product expressions, input Real types and `'Generating Electricity Price'` behavior.
- [ ] REFINE canonical generic plant: add `construction_duration` and `operational_duration` with Real defaults 5.0 and 40.0, units stated in comments and resolving Hawker citations. Add `pv_factors` usage and bind rate/durations; bind the same durations and named factor outputs into `lcoe_calc` exactly as the design binding table specifies. Preserve the guard and existing constraints.
- [ ] REFINE both corresponding IFE twins through the mapping in `tests/model_families.py`; verify byte equality to their canonical sources. No other family source needs modification.
- [ ] REFINE `data/traceability_matrix.csv` through native trace operations where supported: add the factor definition and direct duration bindings, and update the affected LCOE row. Carry the Hawker source, derived numerical basis and relevant MR-WI049-1/3/7 links without inventing a new approved insight or source interpretation. Inspect `.codex-test/run agentic-mbse pm trace-element --help` before invocation; preserve the existing CSV schema.
- [ ] NEW `tests/models/test_ife_zero_discount_repair.py`: add structural checks for the library factor definition, Real duration inputs and shared instance bindings, with no calc definition introduced in designs. Check that the two factors reach the cost/energy inputs and the strict guard still receives actual net power.
- [ ] Run `.codex-test/run python -m pytest tests/models/test_ife_zero_discount_repair.py -q` for the structural tests written so far.
- [ ] Run `.codex-test/run agentic-mbse validate --level=1 exploration/ife_e2e/models`, then the same command with `--level=2` and `--level=3`; retain outputs. The L1 command supplies the parser checkpoint over the complete import closure. Manually check naming, imports, types, binding direction and citation resolution.

**Completion gate:** structural tests and Levels 1–3 pass; canonical/twin equality holds; both new definitions/bindings have complete comments and trace rows. Record remaining inherited L4–6 concerns for Phase 3. Package/caller migration follows next; do not claim full execution certification here.

## Phase 2 — Regenerate the native package and migrate execution callers

**Design reference:** **Elements and dataflow**, **Interfaces and deferred impact**, **Risks and acceptance**. The prototype proves the typed completion and native sealing. Production and temporary packages still need both manual functions, revised keys and the two new output channels.

**Files:** REFINE native generated tree `exploration/ife_e2e/generated/` through codegen, including NEW `handwritten/ife_lcoe/ife_present_value_factors_impl.py`; REFINE `exploration/ife_e2e/eligibility.py`, `tests/ife_execution.py`, `tests/ife_oracle.py`, `tests/models/test_model_family_spines.py`, `tests/test_ife_consumer_eligibility.py`, `tests/models/test_ife_zero_discount_repair.py`; NEW `implementation/migration.md`.

- [ ] Regenerate from `exploration/ife_e2e/models` using `GenerationConfig` and `run_codegen`, package name `ife_tea`, output `exploration/ife_e2e/generated`, following the existing family/prototype invocation. Run every Python invocation through `.codex-test/run`. Let native generation emit modules, schemas, contracts, manifests, entry JSON, pipeline and generated tests.
- [ ] NEW typed factor completion: adapt `prototype/factors_impl.py` to the emitted `IFE_Present_Value_FactorsInput` import and native tuple signature; return operation then construction. Use only the approved stable factors and exact `rate == 0.0` branch, including negative zero. Do not add epsilon clipping or input bounds.
- [ ] Preserve the existing typed `generating_electricity_price_impl.py`. Reseal via supported generation with `preserve_handwritten=True`; retain signature/loader evidence. Inspect the regenerated LCOE signature and confirm its two factor inputs are required and named correctly.
- [ ] REFINE `tests/ife_execution.py` so `complete_ife_package` installs both shipped typed completions, rewrites package-qualified imports for temporary packages, and regenerates seals. Assert preservation of both functions; update helper documentation.
- [ ] REFINE `tests/ife_oracle.py` current entry keys from `lcoe_calc__construction_years`/`lcoe_calc__operational_years` to `construction_duration`/`operational_duration`. Preserve its independent annual arithmetic. Add a separate clearly labeled Decimal fractional-algebra reference for Phase 3, keeping explicit integer dated sums distinct and never importing the production factor function.
- [ ] REFINE IFE entry census and documentation in `tests/models/test_model_family_spines.py`: two duration keys move from library defaults to plant design attributes. Assert exact sets and Real defaults; retain the unchanged total entry count. Add/check the two factor output channels and preserve all thirty original names in the response census.
- [ ] REFINE `exploration/ife_e2e/eligibility.py` direct caller `module_balance` and its input assembly: evaluate the native factor module first and pass its named outputs to the core. REFINE `tests/test_ife_consumer_eligibility.py` to verify this path, which also serves `run_anchors.py`. No caller duplicates the factor formula. Search current `tests/`, `scripts/` and IFE executable code for other direct callers/old keys and record the actual migrated set in `implementation/migration.md`; generated callers are regenerated, not hand-edited.
- [ ] REFINE `tests/models/test_ife_zero_discount_repair.py` with a temporary generated-execution fixture using the revised helper. Assert sealed loading, named factor outputs, exact entry/output census and successful baseline/zero/fractional smoke cases. Exercise mutations of each plant duration to prove they reach both factors and the cost calculation.
- [ ] Add retained repeat-regeneration checks for full package byte equality, excluding runtime caches: first `preserve_handwritten=True`, then `preserve_handwritten=True, smart_regen=True`. Validate both typed completions and public loader after each route. Smart mode alone with overwrite is not the accepted preservation route.
- [ ] Run `.codex-test/run python -m pytest tests/models/test_ife_zero_discount_repair.py tests/models/test_model_family_spines.py tests/models/test_ife_operating_point_repair.py tests/test_ife_consumer_eligibility.py -q` with the configured sealed TEAx import environment. Use `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest ...'` when needed, replacing `...` with these exact paths. Capture outcomes and investigate new failures.
- [ ] Run the Phase 1 three validation commands again over `exploration/ife_e2e/models`; retain reports and manually inspect generated factor-to-core pipeline bindings.
- [ ] NEW `implementation/migration.md`: identify deferred study entry snapshots, channel metadata, manifests and package pins, including `exploration/ife_e2e/studies/study_route.py`, its manifest and `20260910-ife-operating-point/results/context/`. `tests/study/test_ife_native_route.py` expects the study route's old channel set/pin and may fail closed after regeneration. Record this separately from production regressions; do not refresh study metadata, alter immutable records, re-pin or run a study in this item.

**Completion gate:** sealed current and temporary packages load and execute; two typed completions survive both regeneration routes; direct callers and current censuses migrate; scoped non-study tests and Levels 1–3 pass. Only the identified study refresh remains deferred. Return any additional integration dependency to the parent.

## Phase 3 — Retain acceptance tests and certify integration

**Design reference:** **Evaluation and numerical argument**, **Prototype and validation**, **Implementation and verification checklist**; spec **Acceptance cases**; review **Final acceptance assertions**. Prototype numerical evidence must become retained tests against production execution, with stronger verdict and consumer assertions.

**Files:** REFINE `tests/models/test_ife_zero_discount_repair.py`, `tests/ife_oracle.py`, `tests/test_ife_consumer_eligibility.py`, `modeling_project/VALIDATION_MATRIX.md`; NEW `implementation/validation.md` and machine-readable results where useful. Fresh reviewer owns NEW `audit.md` after implementation.

- [ ] Retain all 264 design cases through sealed generated public evaluation: durations `(5,40)`, `(5.5,40.5)`, `(0.25,0.5)`, `(1,1)`, `(20,100)`, `(50.5,200.5)`; baseline, exact-zero-net and negative-net points; zero, 8%, and both signs of `1e-4`, `1e-8`, `1e-12`, `1e-14`, `1e-16`, `1e-18`; add ±50% for generating cases. Also assert signed-zero factor limits.
- [ ] SV-076: independently reconstruct annual quantities with 80-digit Decimal arithmetic and explicitly sum integer payment dates. Assert finite cost, signed/zero energy and eligible price separately; assert each factor as an additional diagnostic. Use relative error ≤`1e-9` for every nonzero reference and absolute error ≤`1e-9` only for true-zero channels. Ensure the tests would reject the original zero exception and separate-channel cancellation even when their quotient agrees.
- [ ] SV-077: use separately labeled high-precision difference-of-powers fractional references and exact `A(n,0)=n`; cover the full design window and both sides of the exact-zero branch. Do not cast production durations to integer or turn test bounds into supported-domain policy.
- [ ] SV-078: for every applicable generated case assert exact named `net_positive` verdict, exact generating flags and exact zero invalid prices. Assert the inherited named viability verdict where expected. Cost and signed/zero energy diagnostics must still complete for non-generators. Exercise both Hawker and Meier supported eligibility consumers using actual generated outputs/verdicts.
- [ ] Harden the four WI-048 positive-neighbor cases at zero, ±`1e-12` and 8% into retained assertions: actual net power >0, exact satisfied net verdict, generating=1, positive price, supported consumer eligibility and independently accurate cost/energy/price with the same strict relative tolerance. This prevents passing by suppressing all prices.
- [ ] Compare every one of the thirty inherited numerical output names against `entry-baseline/baseline_result.json` at 8%, preserving both exact named verdicts and eligibility. Assert exactly two added factor channels. Independently verify ordinary baseline arithmetic; preserve Meier, power balance, annual time constants, dollar bases, replacement charges and comparison labels. Investigate any unexpected movement before proceeding.
- [ ] Run final regression `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/models/ tests/test_ife_consumer_eligibility.py -v'`. This includes live/snapshot family equality, mutation propagation, WI-048 regressions and retained WI-049 cases. Report passed/failed/skipped counts and reasons; no required IFE acceptance case may be silently skipped. Run `.codex-test/run python scripts/verify_ife_lcoe.py` as the existing independent integer cross-check.
- [ ] Run `.codex-test/run agentic-mbse validate --complete --verbose exploration/ife_e2e/models` and `.codex-test/run agentic-mbse validate --complete --verbose models/`; retain full reports. Levels 1–3 must pass for the scoped IFE family. Attribute wider-model results separately, including inherited Level 2 placeholder failures recorded by WI-048; do not require unrelated MFE repairs or report a blanket pass. Review IFE L4 constraint coverage and L5 comments/citations. Confirm canonical/twin equality and no new calculation definition in designs.
- [ ] NEW `implementation/validation.md`: match each of the 50 reported IFE L6 diagnostics to the pre-change issue by file, element, rule and message, accounting for moved lines; classify retained, resolved and new issues. Compare with WI-048/prototype reports as supporting evidence. Resolve introduced scope-relevant problems; return new shared blockers to the parent. Record wider-model inherited debt separately. A matching total alone cannot certify no regression.
- [ ] Complete directly affected trace rows and citation checks; record that source interpretation is unchanged. Document actual execution identity, command environment, test results, regeneration evidence, baseline comparison and the deferred stale study route in `implementation/validation.md`.
- [ ] Update only SV-076, SV-077 and SV-078 in `modeling_project/VALIDATION_MATRIX.md` through `.codex-test/run agentic-mbse pm update-validation SV-076 --status passing` and analogous commands for SV-077/SV-078 after their retained tests pass. Add direct evidence pointers as supported by the native format. Historical certifications remain intact.
- [ ] Hand off to the parent for a fresh independent item audit into `audit.md`, supplying the seven MR rows, this plan, retained tests/results and before/after identities. This checkbox records delivery for audit only. The parent owns the audit verdict and later acceptance; the implementer resolves findings and reruns affected checks when returned, without marking a self-certification.

**Explicit acceptance matrix:** all seven rows must have concrete evidence in the final report and independent audit.

| Requirement | Completion evidence |
|---|---|
| MR-WI049-1 | SV-076 exact-zero and dated integer streams, separate cost/energy checks. |
| MR-WI049-2 | SV-076/077 finite independent numerical channels meeting strict per-channel tolerance. |
| MR-WI049-3 | SV-077 Real durations, fractional algebra, zero limit and justified design-window tests. |
| MR-WI049-4 | SV-076/078 exact flags, verdicts, sentinels and supported consumer eligibility, including positive neighbor. |
| MR-WI049-5 | SV-078 all thirty old outputs, both verdicts, ordinary independent baseline and preserved Meier/annual/physical semantics. |
| MR-WI049-6 | Native and temporary package execution, twin equality, typed signatures, both preservation routes, scoped regression, IFE L1–3 PASS, attributed L4–6 and wider-model findings, and positive fresh audit. |
| MR-WI049-7 | Resolving model comments and trace rows for limits/derivation/defaults, inspected by audit. |

**Completion gate:** all seven requirements and SV-076–078 have retained passing evidence, required checks pass, inherited debt is individually attributed and the fresh audit is positive. Parent decides the next goal-stage action. Close/archive, study refresh, financial normalization, source rulings and MFE changes remain outside this item.

## Feasibility and risk handling

The accepted prototype resolves the pinned renderer limitations; preserve its output-only factor definition, input ordering and direct shared-duration bindings. Tuple order is easy to reverse, so test named factor outputs and verify the emitted signature. Old keys may survive in current callers; use a scoped census and distinguish immutable historical evidence from executable consumers. The Decimal oracle must reconstruct annual quantities independently so shared wrong arithmetic cannot pass. Extreme floating-point representability remains a design limitation, not a reason to add rate/duration policy. Surface any requirement/source conflict or new shared-tool prerequisite to the parent before changing scope.
