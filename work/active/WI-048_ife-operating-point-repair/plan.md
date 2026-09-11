---
Status: approved
Created: 2026-09-10
Updated: 2026-09-10
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-048 implementation plan

## Authority and source documents

[AGENT] This plan sequences the parent-accepted [design](design.md), including the accepted R-001 correction in [review.md](review.md), under the [alignment](../../orchestration/ife-operating-point-repair.md). Routine plan approval belongs to the parent. [spec.md](spec.md), MR-WI048-1–8 and SV-073–075, is the acceptance contract; the [IFE epic](../../backlog/epic-ife-cost-modeling.md) supplies inherited context. Return source conflicts, monetary/finance comparison-basis conflicts, scope changes and other reserved gates to the parent before dependent writes.

## Design summary

Use authoritative beam energy, efficiency and rate to drive one computed physical balance shared by Hawker and Meier pricing. Preserve historical Osiris facts separately; retain the closed-form finance arithmetic and use one typed handwritten guarded quotient with a named strict-positive net-generation assertion.

## Prototype baseline and sequencing

`prototype/build.py`, `prototype/models/`, `prototype/execute.py`, `prototype/price_impl.py`, `prototype/execution.json` and `review-boundary-evidence.json` prove structure and public execution. The source retains stale comments and the handwritten prototype is untyped; refine production files against the design rather than copying the probe wholesale. `prototype/validation.txt` records Levels 1–5 PASS and Level 6 FAIL with 34 reported issues, including EXPOSE/static-extraction limitations; exact public generation succeeded separately. Phase 1 completes library documentation, Phase 2 completes source distinctions and bindings, Phase 3 proves typed completion/regeneration, and Phase 5 attributes every remaining L6 issue without declaring it clean.

[INHERITED: parent entry runs, 2026-09-10] Model tests passed 63 with 13 skipped; the two public IFE suites passed 20. Evidence: `work/orchestration/goals/fusion-audit-remediation/evidence/{entry-model-tests,entry-ife-tests}.txt`. The initial public-suite setup failure was missing TEAx on PYTHONPATH; the documented rerun passed without dependency changes.

The five phases follow dependencies: library definitions, plant wiring, executable package, consumers and acceptance, final integration. Execute serially because each phase changes a coupled surface; this plan has no batch of three independent production files. Mark each checkbox when completed and record the commands and deviations here or in `implementation-evidence.md`.

## Validation commands and environment

Use `.codex-test/run` per `.project/codex-test-setup.md`; never synchronize or modify the shared runtime. For public TEAx execution, add this repository and `$STOP_PARSER_TEAX_ROOT/packages/teax-simkit` to PYTHONPATH and set `STUDY_REQUIRE_TEAX=1` as documented in `docs/integration_seam_operator_guide.md`. Resolve the existing configured root rather than inventing another checkout; do not print credentials.

Create a temporary canonical IFE subset with the existing `tests.model_families.materialize_canonical_subset` helper and its declared IFE family mapping. Call that directory `IFE_CHECK_DIR` below. Re-materialize after each model change; it includes imports and excludes unrelated families. The installed validation skill prefers the wrapper over standalone `syside check`; Level 1 supplies parser verification.

- **V1–3:** `.codex-test/run agentic-mbse validate --level=1 "$IFE_CHECK_DIR"`, then the same command with `--level=2` and `--level=3`. Require no parser errors, blocking structure errors or dependency cycles; inspect names, imports, Real units and pure EXPOSE bindings.
- **V1–6:** `.codex-test/run agentic-mbse validate --complete "$IFE_CHECK_DIR"`; also run `.codex-test/run agentic-mbse validate --complete models/` for separately attributed whole-tree findings.
- **Models:** `.codex-test/run python -m pytest tests/models/ -v`.
- **IFE public:** with the environment above, `.codex-test/run python -m pytest tests/test_codegen_teax_acceptance.py tests/test_occurrence_mutation_teax.py -v`.

These named commands are invoked explicitly by each phase checklist. A command that fails or skips remains recorded; numerical output or a sealed package cannot erase a failed quality level.

## Phase 1 — Library contracts and source-backed arithmetic

**Design reference:** “Research findings and source facts,” “Proposed elements and equations,” and “Cost basis and corrected baseline.” Existing definitions contain the original arithmetic; prototype copies demonstrate output and constraint shapes. Refine canonical library definitions first, preserving monetary coefficients and finance conventions.

**Files and work:**

- [ ] REFINE `models/library/analyses/hif_economics.sysml`: `Meier HIF Driver Cost` exposes bank joules derived from beam MJ/efficiency; keep the Eq. 5 procurement and gamma normalization. `Meier COE` exposes annualized-cost numerator and energy denominator in place of its raw quotient; retain `Meier Reactor Cost` and `Meier Total Capital Cost` arithmetic. Complete affected definition/output docs with Meier equation-image citations and units.
- [ ] REFINE `models/library/analyses/ife_lcoe.sysml`: `IFE LCOE` keeps its 14 inputs, construction/operation defaults and closed-form DCF; exposes fusion, thermal, gross, driver, equal cooling/other and net powers, GW conversions, driver/total fractions, discounted cost and discounted energy. Preserve annual shots, lifetime, driver capital and replacement dependencies and the distinct 31557600-second/8760-hour conventions. Document Hawker equations and channel units.
- [ ] REFINE the same file: add `Generating Electricity Price`, with numerator, denominator and actual net W inputs and price/Real 0-or-1 generating outputs; document strict-positive behavior and invalid zero sentinel. Keep manual scope to the conditional final quotient.
- [ ] REFINE `models/library/analyses/fusion_cycle.sysml`: add `Positive Net Generation` with `net_power > 0.0`; retain and label `Viability Threshold` as a heuristic. Keep existing recirculation definition compatibility as needed.
- [ ] NEW `tests/models/test_ife_operating_point_repair.py`: structural tests for new output directions/types, strict net predicate and one bank derivation; exact source/independent arithmetic tests will be added in Phases 2 and 4.
- [ ] REFINE `data/traceability_matrix.csv`: add/update rows for the three changed calculations and two new definitions with current Hawker/Meier image or equation sources and MR/SV references, using the existing schema. Inspect applicable equation images before changing arithmetic; return a real transcription conflict to the parent.
- [ ] Run V1–3 on a temporary subset with the matching prototype usages while library ports are transitioning; record this interim scope. Run the new structural tests with `.codex-test/run python -m pytest tests/models/test_ife_operating_point_repair.py -v`.

**Gate:** Library definitions and new constraint are valid, documented and structurally tested. Temporary matching usages are only a transition validation fixture; Phase 2 must validate canonical usages before generation.

## Phase 2 — One plant operating point and preserved historical facts

**Design reference:** “Overview and decisions,” “Bindings and channel contract,” and “Cost basis and corrected baseline.” Production HIF currently contains independently adjustable bank/rate/power inputs and corrupted source literals. Prototype bindings pass Levels 1–3 but need production citations and historical facts.

- [ ] REFINE `models/designs/hif_ife/hif_driver.sysml`: `HIF Driver`/existing instance uses efficiency 0.28, authoritative beam and exposed Meier bank energy; remove the fixed independent bank value and correct current citations.
- [ ] REFINE `models/designs/generic_ife/ife_plant.sysml`: `IFE Power Plant` instantiates `hawker_price`, exposes its price plus required powers/fractions, keeps the documented driver-only `recirculating_fraction` alias and asserts `net_positive` against actual priced net W. Label the retained eta-gain assertion honestly.
- [ ] REFINE `models/designs/hif_ife/hif_plant.sysml`: plant baseline frequency 4.6, gain 87 and thermal efficiency 0.45; bind driver rate to frequency and both Meier power denominators to computed thermal/net GW. Instantiate `meier_price` and retain the public `meier_coe` alias. Name reactor units=1 and target factory direct cost=0.1 billion 1988 dollars instead of anonymous usage literals.
- [ ] REFINE the same plant: preserve all 13 table facts from spec “Source record and assumptions” as clearly named historical reference attributes or a named reference part, with the verified Osiris image citation. Separate historical yield 432 from computed 435 MJ, historical 2504/1000 MW from computed thermal/net powers, and historical 1992 cents/kWh from computed cost conventions. Explain 1.15 blanket multiplier, 0.90 availability and equal driver/cooling as later assumptions.
- [ ] REFINE `tests/models/test_ife_operating_point_repair.py`: exact source literal assertions for all table facts, baseline input corrections, authoritative energy/rate bindings, common computed denominators and historical/computed separation; no broad tolerances for transcription.
- [ ] REFINE `data/traceability_matrix.csv` for HIF driver/plant and generic plant changes; REFINE `models/README.md` with the operating-point and historical reference distinction and output contract.
- [ ] REFINE six IFE twin files through the existing `tests/model_families.py` mapping: `exploration/ife_e2e/models/analyses/{hif_economics,ife_lcoe,fusion_cycle}.sysml` and `exploration/ife_e2e/models/designs/{generic_ife/ife_plant,hif_ife/hif_driver,hif_ife/hif_plant}.sysml`. Synchronize canonical bytes only; preserve the shared foundation/cost hierarchy files and all MFE files.
- [ ] Re-materialize the canonical IFE subset and run V1–3 plus `.codex-test/run python -m pytest tests/models/test_ife_operating_point_repair.py -v`; verify twin bytes via the existing family tests, recording temporarily stale census expectations for Phase 3.

**Gate:** Canonical family parses without cycles and independently settable bank/rate/Meier-power inputs are gone. Exact historical facts survive visibly and both cost channels consume one computed balance.

## Phase 3 — Supported generation, typed completion and interfaces

**Design reference:** “Bindings and channel contract,” “Prototype and validation report,” and “Risks and approval.” The prototype seals only after native handwritten completion; its untyped function is unsuitable for smart regeneration.

- [ ] REFINE `exploration/ife_e2e/generated/` using pinned `GenerationConfig`/`run_codegen` from the canonical IFE subset; regenerate contracts, manifests, schemas, inputs, modules and pipeline together. Do not hand-edit seals or generated arithmetic.
- [ ] NEW `exploration/ife_e2e/generated/handwritten/ife_lcoe/generating_electricity_price_impl.py`: implement only the guarded quotient using the generated typed input and return signature. Nonpositive net returns price=0, generating=0; positive net divides and returns generating=1. Both plant instances use this same definition implementation.
- [ ] REFINE `tests/models/test_model_family_spines.py`: derive and record the exact new IFE entry/channel census, retire bank/rate/thermal/net entry keys and old raw price channels, account for named literals and new outputs/assertion. Update IFE beam/gain dependency expectations while distinguishing direct input consumers from downstream execution reach. Preserve MFE expectations.
- [ ] REFINE `tests/test_codegen_teax_acceptance.py` and `tests/test_occurrence_mutation_teax.py`: complete generated temporary IFE packages with the shipped typed implementation through the supported handwritten workflow. Replace old channel/default assumptions and keep live/snapshot stencil parity; complete both packages before comparing executed results.
- [ ] Verify native regeneration with `preserve_handwritten=True` retains implementation bytes and seals; exercise the supported smart regeneration route with the typed signature and prove it is not replaced by a stub. Record actual behavior and return an unresolved route failure to the parent rather than weakening preservation tests.
- [ ] Verify sealed loading with `ProvisionalPackageLoader`, `PreparedEvaluator` and `CandidateBridge`, baseline execution, strict net assertion channel and both validity outputs. Add meaningful preservation/signature and temporary-package execution tests alongside the public acceptance tests.
- [ ] Run V1–3, `.codex-test/run python -m pytest tests/models/test_model_family_spines.py -v`, and IFE public commands. Record exact retired/new keys and channel counts in NEW `implementation-evidence.md`.

**Gate:** Shipped and temporary packages execute through public APIs, typed handwritten code survives supported regeneration, seals validate and migrated IFE interface tests pass. No generator/exporter/runtime patch is needed.

## Phase 4 — Independent acceptance and runnable consumers

**Design reference:** “Cost basis and corrected baseline,” “Implementation and acceptance work,” and “Risks and approval”; spec “Success criteria and verification contract.” Prototype numerical results are expectations to check, not the independent oracle.

- [ ] REFINE `tests/models/test_ife_operating_point_repair.py` and the two public TEAx suites: independently derive source-based baseline bank/yield/powers/fractions, Meier procurement/reactor/capital/COE, and Hawker DCF using a separately expressed discounted cash-flow sum. Compare actual generated execution at relative 1e-9 and documented absolute 1e-6 W near zero. Record old→new values and causes, units, year-dollar basis, finance, availability and denominators for both channels in `implementation-evidence.md`.
- [ ] Add beam 5→10 MJ, efficiency 0.28→0.35 and rate 4.6→5 Hz public mutations holding other independent inputs fixed. Verify bank identity, beam doubling of bank/yield, procurement ratio 1.5789473684210527, efficiency inverse bank demand with unchanged beam/yield, and rate-proportional power/shots. Independently check the Meier rate factor, gamma×bank=direct driver dollars, driver capital, annual shots, lifetime years and annual replacements in each case (SV-074).
- [ ] Add public SV-075 cases: retained eta=0.1/G=100/M=0.6/t=0.3 negative-net counterexample; exact-zero 5 Hz fixture from review evidence; matching −2.5 W and +2.5 W neighbors. Require exact zero where intended, passing heuristic, violated named net verdict for net≤0 and satisfied for positive net. Both prices/indicators are zero for non-generators and finite/valid for the positive neighbor. Separately record the 4.6 Hz +5.960464477539063e−8 W rounding case; do not alter strict predicate semantics.
- [ ] Add consumer-level tests that feed zero-price invalid results and prove they cannot be selected as attractive, a minimum, or a valid generating anchor. Require validity=1 and satisfied named net-generation verdict before ranking either cost; translation parity alone does not certify this.
- [ ] REFINE `scripts/verify_ife_lcoe.py` and `scripts/verify_hif_costs.py`: correct current HIF expectations and expose independent source/identity checks; distinguish historical/module parameter scenarios from the computed plant and old mirror/range checks. Keep their standalone command paths runnable.
- [ ] REFINE `exploration/ife_e2e/run_anchors.py` and `exploration/ife_e2e/sweep_ife.py`: migrate the split DCF/quotient module interface and actual channels/entry keys; require generation eligibility for anchors/ranking. Retain explicitly named historical/module scenarios without presenting them as the corrected plant.
- [ ] Inspect `exploration/ife_e2e/{plot_sweep.py,study/run_viability_study.py,study/bench_prepare_once.py,study/prove_catalog_seam.py}` and REFINE affected runnable callers for retired interfaces and generation eligibility. Keep this to compatibility changes and small checks; historical study records/results remain evidence. Record the actual changed caller list in `implementation-evidence.md`.
- [ ] Run `.codex-test/run python scripts/verify_ife_lcoe.py`, `.codex-test/run python scripts/verify_hif_costs.py`, and `.codex-test/run python exploration/ife_e2e/run_anchors.py` with the documented package alias/environment. Exercise each affected sweep/study/plot caller on bounded temporary data/output; record exact commands and sentinel-exclusion result without overwriting historical outputs.
- [ ] Run V1–3, new model tests and IFE public tests. Record independent oracle results separately from model/translation parity in `implementation-evidence.md`.

**Gate:** SV-073 source fidelity and cost movements, SV-074 dependency mutations and SV-075 named verdict/eligibility are independently demonstrated; supported IFE callers run with current channels. No undefined or nonpositive generation is accepted as a low-cost winner.

## Phase 5 — Integration, traceability and independent audit handoff

**Design reference:** “Prototype and validation report” and “Implementation and acceptance work.” Final validation must distinguish the old L6 residue from new failures and public generation success.

- [ ] Run V1–3 on the final canonical IFE subset, then V1–6 for the subset and whole tree. Record each level's actual verdict and issue categories in `implementation-evidence.md`; compare L6 findings with prototype/baseline, identify legacy EXPOSE/static extraction and deliberate manual calculation separately, and return any unresolved new blocking issue or residual-acceptance decision to the parent.
- [ ] Run Models and IFE public commands; run `.codex-test/run python -m pytest tests/test_dependency_provenance.py -v`. Record commands, environment identity, revisions, pass/fail/skip totals and reasons. Compare the 63/13 and 20 entry baselines without silently accepting a lost test or new skip.
- [ ] Recheck IFE twin equality, source citations on all affected/new definitions, complete `data/traceability_matrix.csv`, and final generated contracts/seals and handwritten preservation evidence. Inspect the diff for shared MFE changes and accidental historical-output rewrites.
- [ ] Complete the acceptance matrix in `implementation-evidence.md`: MR-WI048-1 exact source/historical facts; -2 bank/gamma/capital/replacement identities; -3 authoritative rate effects; -4 computed common denominators and independently explained cost bases; -5 negative/zero/positive named generation verdicts; -6 balance/fractions; -7 public execution, synchronization, consumer migration and regeneration; -8 all validation levels, interface accounting and independent audit status. Link SV-073, SV-074 and SV-075 to concrete test names and result files.
- [ ] Update SV-073–075 evidence/status in `modeling_project/VALIDATION_MATRIX.md` through the installed supported PM operation where available; preserve historical certifications. Record implementation verification honestly, without claiming an independent audit has occurred.
- [ ] Mark completed phase checkboxes and design implementation checkboxes with evidence; return to the parent for a fresh `$audit-models` stage. That non-author audit must evaluate F01, F02 and F03 separately against the spec. Item close/archive, goal close and merge/push remain reserved.

**Gate:** All blocking IFE checks pass, all eight requirements and three SV entries have evidence, and the parent has a concrete package for the mandatory fresh audit. Implementation completion does not self-certify the item.

## Feasibility and bounded hazards

- The typed handwritten signature is required for regeneration. Keep one shipped implementation and complete temporary packages from it; do not patch the pinned compiler or duplicate finance arithmetic in Python.
- Existing direct consumers use positional outputs and old channels. Search remaining references to retired channels and entry keys after migration; distinguish archived evidence from runnable callers before editing.
- Exact-zero cancellation depends on the fixture. Use the review's 5 Hz boundary and explicit neighbors; approximate equality is for arithmetic checks, never predicate eligibility.
- Derived output bindings can be misclassified by static L6 even when exact generation succeeds. Report both observations and their provenance; a new unexplained failure returns to the parent.
- Source literals, printed gain/yield rounding, dollar-year distinctions, equal cooling allowance and the unchanged finance/day-count conventions are the contract. Changed cost baselines are expected; tuning them to the old result would defeat the repair.

## Parent approval — 2026-09-10

[AGENT] Approved all five phases for execution under the owner-approved alignment. The R-001 correction is incorporated in the accepted design. Keep caller changes limited to compatibility and eligibility; a missing native study seam is reported separately rather than repaired inside this model item. Production verification and fresh independent audit remain required.
