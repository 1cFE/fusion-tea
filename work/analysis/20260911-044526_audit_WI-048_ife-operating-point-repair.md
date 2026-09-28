---
Verdict: FAIL
Scope: WI-048_ife-operating-point-repair
Implementation: 243625b476c6761e6c74dbafa7e9413402eafe90
Created: 2026-09-11
---

# WI-048 independent model audit

The operating-point repair executes correctly, but the item does not yet satisfy its source-provenance acceptance requirement. One blocking documentation finding remains: the active plant-cost explanation still uses the corrupted 2.054 GW thermal basis without identifying it as an erroneous historical input. Retain the cost coefficient; correct its stated provenance. F02 and F03 pass independently. F01's literal transcription passes, but its current-source-claim cleanup is incomplete.

This is a fresh native audit-models work-item audit by a non-author. The parent approved scope and routine audit confirmation under `work/orchestration/ife-operating-point-repair.md`. A separate numerical reviewer checked sources and recomputed the cash flows; the audit coordinator independently inspected both required source images, reviewed the model/test/caller changes, and reran validation and execution. No production fix, source rewrite, close/archive, goal transition, commit, or residual acceptance occurred.

## Scope and evidence

The production scope is the six canonical files `models/library/analyses/{fusion_cycle,hif_economics,ife_lcoe}.sysml`, `models/designs/generic_ife/ife_plant.sysml`, and `models/designs/hif_ife/{hif_driver,hif_plant}.sysml`, their six IFE twins, the generated IFE package, affected consumers, tests and documentation. Validation materialized the eleven-file canonical IFE family with `tests/model_families.py:131`. Scope inspection against approved-plan commit `d953f12c` found no MFE, shared foundation, shared CAS, monetary-normalization, runtime, or lockfile change. The pytest marker declaration is supporting test configuration. Setup edits were preserved.

Authority read: the item spec/design/review/plan/implementation-evidence; the F01–F03 entries in `.project/reports/20260907-fusion-model-audit.md:50`; project requirements, architecture and validation matrices; SOURCE_INDEX and traceability matrix; the native audit, validation, requirements and traceability skills. No quarantined holdout was accessed. This is not certification of the historical IFE epic or F04–F20.

Fresh evidence is in [wi048-audit-evidence](wi048-audit-evidence/). The full numerical/source tables and separately calculated cash-flow results are in [numerical-review.md](wi048-audit-evidence/numerical-review.md), incorporated as this report's numerical appendix. Its tables enumerate all thirteen historical facts, current physical inputs, finance assumptions, formula coefficients, conversions, and relevant derived outputs with file/line or image-row locators. Different historical and computed bases are identified explicitly; their differences are not falsely graded as source-equality failures.

## Findings and required repair

### A01 — Blocking, medium severity: active cost provenance retains the corrupted thermal basis

`models/designs/hif_ife/hif_plant.sysml:128` retains alpha = 2000 dollars/kWe. Its explanation at lines 130–139 says it derives from Meier reactor cost about 0.73 billion dollars at **2.054 GW thermal**, scaled by 1.83 and divided by 1.0 GW electric. The same text remains in the IFE twin at `exploration/ife_e2e/models/designs/hif_ife/hif_plant.sysml:130`. The 2.054 GW value is the corrupted operating basis F01 identified; the image says 2.504 GW and the corrected computed case uses 2.30115 GW. The active doc comment labels the result estimated but does not identify that underlying basis as erroneous/historical.

This violates MR-WI048-1's requirement to correct affected source claims and distinguish facts from later assumptions. It also leaves the Phase 2/5 citation-completion claims premature. The executable alpha may remain 2000 under the approved finance scope. A documented historical estimate is legitimate; presenting the old basis as a current source derivation is not.

**Required correction:** amend the current canonical/twin doc comments to identify alpha as the retained prior modeling estimate and explain that the old 2.054/1.0 basis is historical and not an image-verified or current computed operating point. Alternatively remove the misleading numerical derivation while preserving its provenance by path. Keep the literal, dollars, finance, and physical calculations unchanged. Review the adjacent O&M estimate at lines 143–153 for the same historical/current distinction; its approximate 3.3-billion-dollar/1-GWe derivation is also inherited, not a recomputation of the corrected case. Recheck source claims and family synchronization after the bounded repair.

### A02 — Warning: retained Hawker locators overstate the source support

`hif_plant.sysml:47,69,123` cites Hawker Table 1 for target cost, the blanket assumption, and an 8% default discount. Table 1 in `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:106` is the technology comparison. Table 2 at line 155 lists parameter names; sampling ranges are at lines 443–469. Neither renaming Table 1 to Table 2 nor citing a range establishes an exact 10-dollar target cost, 1.15 blanket multiplier, or 8% source default. Generic plant parameter comments at `models/designs/generic_ife/ife_plant.sysml:39,47,57,65,76,86,94` repeat the incorrect table locator.

These claims predate most of this repair, but line 69 was rewritten here. Correct the relevant locators and identify retained selected values as modeling assumptions where the source provides only a range or parameter definition. Do not reparameterize the model to fix citation prose. This warning is separate from the blocking 2.054-GW provenance defect.

### T01 — Traceability limitations, separately reported

Every definition in the six-file scope has a doc comment with an authority path or source context. The new/changed core definitions have current source locators and update dates. Existing `Recirculating Power Fraction`, `Meier Reactor Cost`, and `Meier Total Capital Cost` comments lack the skill's explicit Last Updated field; their existing sources remain readable. L5's 29/29 documentation score checks presence and does not establish full citation correctness (A01/A02).

The seven calc definitions and four part/constraint definitions in scope have authority comments; nine of those eleven definitions have matrix rows. The plant usage has its own row. `Recirculating Power Fraction` and `Viability Threshold` have no matrix row. These are inherited omissions, including the heuristic whose explanatory text changed here. Both cite DI-001 in their model context; adding qualified rows using native trace-element is a bounded follow-up, not a reason to invent a new insight or requirement.

The eight appended qualified rows at `data/traceability_matrix.csv:82` carry current authority/MR/SV locators. Five link existing DI-004 or DI-005; Meier COE, Generating Electricity Price and Positive Net Generation have empty DI/PR cells and direct authority/derived-rule context. No applicable current promoted PR-XXX exists to fill those cells. Historical Meier rows carry ephemeral MR-WI008 identifiers rather than current PR links. These are limitations against the generic skill's desired DI/PR chain, not missing numerical authority. Native trace-element is add-only: qualified current rows coexist with legacy unqualified rows; this audit does not claim supersession or rewrite historical metadata.

## Numerical findings and cost basis

Both reviewers personally read `knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png` and `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/images/page_004_eq_0.png`. All thirteen stored Osiris facts at `hif_plant.sysml:233` match their image rows exactly, including gain 87, yield 432 MJ, thermal 2504 MW, and 5.6 in 1992 cents/kWh. The executable choice of gain 87 makes 5 × 87 = 435 MJ; preserving 432 separately is correct. The historical identity 432 × 4.6 = 1987.2 MW differs from printed 1987 by rounding. Nothing is fitted to erase that difference.

The independently expressed annual sum places one fifth of initial capital in years 1–5 and constant operation cost/energy in years 6–45, discounted at 8%. It agrees with the closed-form implementation. Tests additionally compare all 30 numeric channels for baseline, beam 10 MJ, efficiency 0.35 and frequency 5 Hz at relative 1e-9. The absolute 1e-6 W allowance applies only to near-zero arithmetic, not to the source literals or predicates. The skill's source-comparison thresholds (PASS ≤1%, WARN 1–5%, FAIL >5%) apply only to comparable bases; image transcriptions here require exact equality under the spec.

| Quantity and calculation basis | Before repair | Current | Cause/evidence |
|---|---:|---:|---|
| Beam energy used by Hawker, MJ | 5.0001 | 5 | Correct authoritative beam/bank identity; `hif_economics.sysml:39`, `hif_driver.sysml:87` |
| Bank energy, MJ | 14.286 | 17.857142857143 | 5/0.28, replacing independent bank literal |
| Gain; rate Hz | 80; 3.5 | 87; 4.6 | Exact image inputs |
| Yield MJ; fusion MW | 400.008; 1400.028 | 435; 2001 | Beam × gain × rate |
| Thermal MW; gross MW | 1610.0322; 692.313846 | 2301.15; 1035.5175 | Retained 1.15 multiplier; corrected 0.45 conversion |
| Driver and cooling, each MW | 50.001 | 82.142857142857 | Bank × common frequency; retained equal cooling allowance |
| Net MW | 592.311846 | 871.231785714286 | Gross minus driver minus cooling |
| Meier thermal/net GW | 2.054 / 1 held | 2.30115 / 0.871231785714286 | `hif_plant.sysml:161` now binds common computed powers |
| Driver procurement, billion 1988 dollars | 0.9749584 | 0.98452224 | Eq.5 rate factor; coefficients unchanged |
| Gamma, dollars/J bank | 68.247088 | 55.13324544 | Direct driver dollars divided by coherent bank joules |
| Meier reactor, billion 1988 dollars | 0.730444258781 | 0.772264159550 | Eq.3 thermal input changes |
| Meier total, billion 1988 dollars | 3.303886865568 | 3.397919111177 | Driver/reactor change; 0.1 factory and 1.83 multiplier retained |
| Hawker, dollars/MWh | 270.1211779380445 | 240.666460639551 | Changed net output, procurement and replacement/shot inputs |
| Meier, 1988 cents/kWh | 4.735403549076959 | 5.589991561584084 | Increased annualized capital and reduced denominator versus old held 1 GW |

Old values above were checked against the committed before/after execution record and its reconstruction script; this coordinator freshly reconstructed/validated the old model subset but did not independently rerun its generated price package. Current values were independently recalculated by the numerical reviewer and freshly executed in the public tests and anchors. This distinction prevents treating an inherited old execution log as a fresh experiment.

Hawker retains a mixed inherited monetary basis: 1988-dollar-derived plant/driver coefficients, generic target costs, 8% discount, 5 construction years and 40 operating years. Meier retains 1988 cents/kWh, 8.3% fixed charge plus 3% O&M, and 1.83 total/direct capital. Both use 0.90 availability and the same computed net power. Shot accounting deliberately retains 31557600 seconds/year, versus Hawker's printed 365-day expression; energy retains 8760 hours/year. These inherited approximations are reported, not accepted as a new convention. The historical 5.6 in 1992 cents/kWh is not a common-dollar validation target. No source conflict requires changing those numbers.

## Fresh programmatic validation

All Python/model commands used `.codex-test/run`. Public execution additionally set `PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"` and `STUDY_REQUIRE_TEAX=1`. Runtime provenance tests passed. Fresh logs retain failures; no failed quality level is relabeled clean.

| Scope | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| Current canonical IFE, 11 files | PASS, 0 errors/warnings | PASS, 0 issues | PASS, 0 cycles | PASS, 2 admitted numerical/2 | PASS, 29/29 docs | FAIL, 50 |
| Old IFE at d953f12c, fresh reconstruction | PASS | FAIL, 2 literal placeholders | PASS | PASS | PASS, 28/28 docs | FAIL, 26 |
| Current whole tree | PASS | FAIL, 10 unrelated placeholders | PASS | PASS | PASS, 103/103 docs | FAIL, 277 |

Commands were `agentic-mbse validate --complete` on `/tmp/wi048-fresh-audit`, `/tmp/wi048-audit-old`, and `models/`; outputs are `ife-validation.txt`, `old-ife-validation.txt`, and `whole-validation.txt`. Whole-tree validation is context, not the item blocking-family gate.

Fresh native L6 API results in `level6-comparison.json` reproduce every one of the old 26 and current 50 issue identities in the implementation's JSON after temporary roots/source-line shifts are normalized. Old IFE = 18 abstract missing defaults + 4 unsupported-dot aliases + 4 unextractable static aliases. Current IFE = 18 + 15 + 15 + 2 derived thermal/net references. The exact increase is 24: eleven additional EXPOSE aliases counted twice, plus two derived references. The prototype's recorded 34 = 18 + 7 + 7 + 2; the eight later plant aliases account for the final additional sixteen. The whole-tree rise from recorded old 253 to fresh 277 is the same 24. The actual live/snapshot generator and execution succeed on these bindings. This identifies the limitations; it does not waive Level 6 or accept unrelated residue.

Fresh regression command: `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/models/ tests/test_codegen_teax_acceptance.py tests/test_occurrence_mutation_teax.py tests/test_ife_consumer_eligibility.py tests/test_dependency_provenance.py -q'`. Result: **122 passed, 13 skipped in 27.28 seconds**. The inherited skips are the example template and twelve absent legacy-foundation tests, as individually identified in the implementation's verbose final-regression log. No new skip or removed preexisting test was found in the diff.

The suite exercises 19 entries, 30 numeric channels, two constraint-evaluation channels and their report. Live and snapshot packages execute both costs and the named verdicts. `test_typed_handwritten_quotient_survives_supported_regeneration` executes both preserve-only and smart-regeneration routes, verifies the typed implementation signature, checks zero changed package bytes and reloads/executes the seal. The shipped handwritten file contains only the final guarded quotient; all finance and physical arithmetic stays in SysML. Its two usages share one implementation. The generated unchecked backlog rows are template output, not evidence of a missing implementation.

Fresh `verify_ife_lcoe.py`, `verify_hif_costs.py`, and `run_anchors.py --output-dir /tmp/wi048-audit-anchors` pass; logs are retained. The remaining bounded sweep/study/plot/benchmark/catalog command records were inspected as implementation evidence, not rerun by this auditor. Consumer inspection confirms explicit eligibility in sweep, plot, anchors and viability-study selection. Twelve fresh consumer tests reject zero sentinels, missing/contradictory verdicts and non-finite prices for rankings/anchors. Benchmark/catalog paths measure or demonstrate execution rather than selecting a winning price.

## F01, F02 and F03 dispositions

| Historical finding | Verdict | Evidence |
|---|---|---|
| F01, source fidelity | PARTIAL; A01 blocks closure | All thirteen exact source facts and executable 87/4.6/0.28/0.45 pass. Historical/current separation exists in stored facts and price channels. Active alpha derivation still cites old corrupted 2.054 basis without qualification. |
| F02, disconnected operating point | PASS | Bank=beam/efficiency; driver frequency=plant frequency; Meier powers bind Hawker outputs. Beam doubling gives 2× bank/yield and procurement factor 1.5789473684210527. Efficiency mutation gives 0.8× bank with fixed beam/yield. Rate mutation gives 5/4.6× power/shots and inverse lifetime; Eq.5 procurement changes by 1/0.99648. Gamma×bank equals capital and feeds replacements. |
| F03, non-generation accepted | PASS | Actual priced net binds strict net_positive. Counterexample heuristic passes but net=-0.2×driver power fails. Exact zero at 5 Hz fails; -2.5 W fails; +2.5 W passes. At 4.6 Hz, +5.960464477539063e-8 W is positive and passes. Both invalid prices/indicators are zero; eligible consumers also require the satisfied named verdict. Driver and total fractions equal their respective powers/gross. |

## Item requirements and completion gates

| Requirement | Status | Specific result |
|---|---|---|
| MR-WI048-1 | FAIL | Exact transcription/rounding choice pass; current provenance cleanup incomplete (A01). |
| MR-WI048-2 | PASS | Bank identity and capital/replacement outputs verified at baseline and beam/efficiency mutations; `hif_economics.sysml:39`, `ife_lcoe.sysml:92`. |
| MR-WI048-3 | PASS | One rate reaches procurement, shots, power and lifetime; `hif_plant.sysml:38`, `ife_plant.sysml:123`. |
| MR-WI048-4 | PASS | Both current prices use computed powers; independent annual sum and Meier source arithmetic agree; monetary/finance bases declared above. A01 qualifies retained coefficient provenance, not executable denominators. |
| MR-WI048-5 | PASS | Named strict net predicate and two guarded prices execute at negative, exact-zero, ±2.5 W and roundoff-positive fixtures. |
| MR-WI048-6 | PASS | All physical powers and both fractions verified against independent arithmetic and boundary balance. |
| MR-WI048-7 | PASS | Canonical/twin equality, live/snapshot execution, sealed loading, typed regeneration, mutations and consumer tests pass. |
| MR-WI048-8 | PASS for technical/reporting obligations | IFE L1–3 pass, L4–6 honestly reported, exact entry/channel changes accounted for. This fresh audit remains negative due to MR-WI048-1. |

SV-073's exact source-fact and numerical-baseline tests, SV-074 mutations, and SV-075 generation semantics are each **passing**. The auditor invoked native `pm update-validation SV-073/074/075 --status passing`; existing statuses remained unchanged. SV-073's passing numerical criterion is narrower than MR-WI048-1's current-source-claim cleanup, so it does not erase A01. No other historical SV status changed.

| Plan phase completion gate | Audit result |
|---|---|
| 1, library contracts/arithmetic | PASS executable/structural gate; citation limitations are reported above. |
| 2, coherent plant and historical facts | PASS bindings/facts; current-source documentation incomplete under A01. |
| 3, supported generation/interfaces | PASS; 19 entries/33 total channels, typed quotient, zero-byte regeneration and seals. |
| 4, independent acceptance/consumers | PASS numerical/mutation/net and consumer execution obligations; source-cleanup acceptance remains subject to A01. |
| 5, integration and audit handoff | Fresh audit handoff accomplished; positive certification/closure gate FAIL because MR-WI048-1 is incomplete. |

## Project standards and architecture

| Project obligation | Assessment |
|---|---|
| MR-1 CAS hierarchy | Inherited IFE gap remains outside repair (F08); no CAS redesign or new cost-bearing subsystem introduced. No project-wide pass claimed. |
| MR-2 costed-component interface | Inherited IFE subsystem limitation remains (F08). The changed computations do not repair or worsen that interface. |
| MR-3 library/design split | New reusable price/constraint definitions are in library analyses; numerical plant choices stay in HIF design. Existing generic-IFE type placement is unchanged, as scoped. |
| MR-4 quantitative traceability | FAIL for A01; A02/T01 describe further inherited locator/metadata limitations. Exact source literals and formula coefficients otherwise verified. |
| MR-5 standard metadata | Existing parameter metadata container retained; project fields remain TBD. No new metadata standard claimed. |
| MR-6 documented patterns first | PASS for this change: design prototype, independent review and plan precede implementation; typed completion/EXPOSE patterns tested. |
| PR-1 taxonomy first | Existing-concept repair; inherits the established IFE selection, no new concept admission. |
| PR-2 shared/divergent analysis | Existing IFE framework preserved; no new cross-concept decomposition. |
| PR-3 documented patterns first | PASS scoped as MR-6; accepted design and prototype supply repair patterns. |
| PR-4 iteration | PASS: generator conditional failure was surfaced and the bounded manual route reviewed; A01 returned for correction. |
| PR-5 artifacts at each phase | Committed spec/design/review/plan and implementation evidence present at audited HEAD. This audit is a review artifact for the parent to commit, not falsely described as already committed. |

The current project uses MR-1–6 and PR-1–5; the archived PR-001–007 are not silently reinstated. AD-001 (Real units), AD-004 (library directories), and AD-006 (separate parameter metadata/arithmetic) are respected. AD-002's parameter metadata structure is retained; this repair does not certify every historical usage against that decision. AD-003's single-calc wording has a bounded, explicitly accepted departure in `design.md:27`: the unchanged closed-form DCF core supplies one shared handwritten guarded quotient. The implementation matches that exception and introduces no duplicate finance formula. AD-005's shared CAS hierarchy is unchanged; AD-007 concerns MFE and is outside this item. L6's references to repository ADR-002 are distinct from model AD-002 and remain reported above.

## Return to parent

Apply A01's bounded documentation correction, address A02's directly affected claims during that repair, and obtain a fresh audit of the repaired revision. Preserve the fixed coefficients, conventions and all historical artifacts. The exact-source transcription and numerical/execution work can be carried as evidence; it does not excuse the remaining provenance defect. T01 is a separately visible inherited traceability limitation. Owner-held residual acceptance, requirement changes, research approval, merge/push, item close/archive and goal close remain reserved.
