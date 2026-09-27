---
Status: implementation verified; integration review pending
Created: 2026-09-27
Updated: 2026-09-27
Related Artifacts:
  Spec: spec.md
  Design: design.md
  Configuration: configuration.md
  Plan: plan.md
---

# WI-098 whole-plant comparison implementation

The isolated native package now calculates complete declared plant power and lifecycle cost for the same supplied reactor inventory with steam and helium Brayton conversion. The retained matched offers at 2500 and 2800 MW source pass all 125 implemented predicates. These are development controls, not the final catalog comparison. Main-study execution remains behind independent integration review.

The source is conditional. The altered 48 kA magnet geometry has no reconstructed plasma-sustainment or global manufactured-fit claim. Source, nuclear-transport and global-construction qualification remain zero. The effective hot-source multiplier excludes cryogenic deposition; uncertain cold heating is an explicit independent demand scenario. These qualifications remain part of the result, even when every implemented equipment check passes.

## Implemented boundary

- `models/designs/whole_plant_conversion/plant.sysml` retains the repaired conversion calculations and binds one selected source to primary heat/flow, fusion, fuel and both branches. Seven old input keys retire into one source and shared finance owners. The coordinator-owned migration rejects unequal duplicates.
- `models/library/analyses/whole_plant_conversion_accounts.sysml` declares ten new calculation interfaces, the concrete costed-account part and numerical predicates. [Interface contracts](evidence/calc-interfaces.json) and [domain/diagnostic conventions](evidence/interface-domains.md) describe every formal and output. The existing complete fuel-inventory implementation is reused.
- Readable costed parts retain major reactor purchases and branch purchases. Rebuilt contingency, indirect services, freight, spares, tax, insurance and commissioning use the reviewed exact membership sets. Derived account leaves directly expose their calculated values; their generated interface has no disconnected wrapper factor inputs.
- Whole-plant electricity subtracts primary circulation, deposited-heating wall supply, magnet drive, refrigeration, fuel/vacuum, cooling, controls, house and declared residual loads once. The separately rated auxiliary sink receives its declared heat. Coil-drive heat is already in the extracted cold/intercept heat and is not added twice.
- Separate D/T/Li-6 purchase streams, selected startup stock, operating imports, magnet/blanket/primary/other replacement events, outage budgets and terminal costs enter one native cashflow calculation. Construction finance applies once to initial spending. The main default is 5% real discount, 30 integer years, 8 construction years and 0.80 availability.
- Selected cryoplant ratings and quote belong to `cryogenic_offer`. Heating demand changes refrigeration power, auxiliary heat, margins and economics while keeping hardware and price fixed. Explicit smaller/larger hypothetical offers exercise the separate procurement role. Captured 40/60 kW results remain reference evidence.

## Package identity and generation

| Item | Value |
|---|---|
| Package |`exploration/whole_plant_conversion/whole_plant_conversion_tea` |
| Executable fingerprint |`6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f` |
| Semantic fingerprint |`bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3` |
| Snapshot SHA256 |`b62054b5ae3bf73f715ea4468ef4a7292d2b732da01191973fb6ed33a829f8d1` |
| Native interface |637 complete numeric inputs; 1196 scalar outputs, of which 1192 independently verified and 4 inherited solver-iteration diagnostics excluded from numerical equality |
| Executable predicates |125 |
| Generation scope |16 source files; 39 handwritten installation receipts; two successive preserved-body generation passes yield identical package trees |

[Build hashes](evidence/build/build-hashes.json) retain the complete source, staged-file, installed-body, package and snapshot identities. [Conversion body reuse](evidence/conversion-body-reuse.json) proves all seven local repaired predecessor body copies differ only by package namespace. Ten new bodies implement the reviewed upstream/ledger equations; the other reused implementations retain their reviewed arithmetic and documented typed adapters. No new physical root solver was added.

## Exact magnet capture

[Capture report](evidence/magnet-capture/report.md) links complete full-system inputs, outputs, predicates and package identity. The selected 48 kA offer has 23.904 T peak field, positive local fit/current margins, 399.36 MPa winding stress and 0.0013312 strain. At the assumed 35.5 W/m³ reference demand, cold/intercept duties are 27.7303/41.1895 kW against selected 40/60 kW. Requoted magnet procurement isUSD 2025 2.614323602 billion. No failed 50 kA probe was overwritten.

The altered full-plasma native run produces 2748.353599 MW fusion and 3258.804491 MW hot source, with retained sustainment, wall, fuel, primary and conversion failures. Those are not presented as passed supplied-source operating points. The new assembly instead evaluates its declared 2500/2800 MW source conditions and carries unresolved transport/construction qualification explicitly.

The first independent numerical review found that the captured stress margin used 650 MPa, the reference calibration, instead of the selected 800 MPa allowable. The source body was corrected to 800 MPa. [First development receipts](evidence/development/native/cases.json) and [first findings](evidence/independent-verification/first-native-findings.md) retain the old executable evidence. The final package and receipts below verify the correction without changing tolerance or hardware.

## Development and independent verification

[Final proposals](evidence/development-final/proposals.json) and [native receipts](evidence/development-final/native/cases.json) contain 35 cases: 32 evaluated cases and 3 expected domain refusals. Each evaluated receipt includes the complete effective input map, native executable fingerprint, all scalar outputs, response verdicts, structured native constraint report and provenance.

[Independent final numerical check](evidence/independent-verification/native-check-final.json) compares all 1192 required scalar outputs and 125 predicates on each evaluated case. All pass. [Independent behavior checks](evidence/independent-verification/native-behaviors-final.json) contain 88 passed checks, including:

- Matched 2500/2800 MW pairs pass all implemented checks. 3000 MW retains the selected primary-pressure and divertor failures.
- Same-hardware 50 W/m³ and 10 kW extra-cold scenarios pass cryogenic capacity; 80 W/m³ and 13 kW extra-cold scenarios fail it. Native electrical, sink and economic consequences agree with the independent equations.
- Explicit 20/30 kW cryoplant offer fails both stages; 60/90 kW offer passes with unchanged demand and its independently supplied quote. Source-demand-only cases preserve installed inventory and initial purchases.
- Insufficient/sufficient stock, processing, primary pressure and auxiliary rejection offers behave as declared. Capture-identity and selected primary path-count mismatches cannot rank.
- Nonpositive operating export, import-dominated annual energy, excessive availability/outage budget and actual exchanger crossover retain violated predicates. Failed economics has finite zero LCOE plus a failing admission flag; it cannot rank.
- Unsupported water properties, negative cold heating and fractional operational years refuse evaluation. Zero discount and fuel price/recovery/extraction/breeding scenarios preserve the defined accounting conventions.

| Retained development pair | Steam net MW | Brayton net MW | Steam USD 2025/MWh | Brayton USD 2025/MWh |
|---|---:|---:|---:|---:|
|2500 MW supplied source |663.969189|285.883396|408.163805|875.312561|
|2800 MW supplied source |746.644668|204.460262|370.701372|1230.283623|

These values use retained matched offers, the declared hypothetical common procurement/service assumptions and 0.80 availability. They do not establish optimized catalog minima or validated market costs. At 2500 MW, initial totals areUSD 2025 18.406924374 billion steam and 16.962956122 billion Brayton; both include the same selected source accounts and their applicable branch overheads. Source/fuel/finance price dependence belongs in the subsequent reranked study.

## Structural validation and preservation

The [complete validator log](evidence/validation.log) reports L1 syntax, L3 dataflow, L4 executable constraint coverage and L5 documentation passing. L2 reports 72 literal bindings and L6 reports 1174 alias/readiness diagnostics; the aggregate validator exits 1. This report does not call that a static validation pass.

[Detailed disposition](evidence/validation-detail.json), produced by [the retained source-to-native checker](evidence/validation-detail.py), records every diagnostic identity and resolves it against authored bindings, generated metadata and executed evidence. It finds zero unresolved items: 45 cross-part aliases, 1129 output aliases and 72 inherited Boolean-screen literals. The 2766 additional all-path completeness diagnostics are classified by input/output/internal/abstract-member role. The 18 logical adapters are checked against their actual native predicates, including failed cases. This is executed translation evidence for the reviewed pattern, not suppression of validator findings.

[Source registration tests](evidence/source-registration-tests.log) pass 3 checks. [Preservation receipt](evidence/preservation.json) confirms 528 original model/full-system files and 207 predecessor conversion files are unchanged. The added source collection is registered in `tests/model_families.py`; no existing model/package, sealed study, source evidence or article was rewritten.

Some generated descriptive CAS labels are incorrect. Use the exact inventory and account membership in [configuration.md](configuration.md) for traceability. Those labels do not drive executable totals; the native bindings and reviewed membership sets do.

## Replay

```bash
.codex-test/run python exploration/whole_plant_conversion/author_model.py
.codex-test/run python exploration/whole_plant_conversion/build.py
.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/development_cases.py
.codex-test/run agentic-mbse validate --complete exploration/whole_plant_conversion/input_models
.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/validation-detail.py --reuse-api
```

Keep the recorded native receipts before rerunning development execution. The complete source/default map is [development-final/complete-defaults.json](evidence/development-final/complete-defaults.json). The strict runner consumes complete new-package maps only; legacy migration is owned by `exploration/whole_plant_conversion/studies/migrate_controls.py`.

## Retained controls and whole-plant study

All 498 retained conversion controls passed under the frozen final identity, with original case labels and legacy finance. The [conversion comparison](evidence/conversion-controls/comparison.json) checks 872 inherited channels and 84 predicates per case; the largest numerical difference is exactly zero. The [independent whole-plant control summary](evidence/independent-verification/controls-summary.json) reports all 498 cases passing the 1192-channel and 125-predicate check. Independent integration review and the complete 2,496-case native catalog/sensitivity study have passed. The verified [whole-plant answer](../../orchestration/goals/design-study-whole-plant-conversion/answer.md) reports the supported conditional steam preference, the combined-assumption Brayton reversal and unsupported 3,000 MW source. [Final independent review](../../orchestration/goals/design-study-whole-plant-conversion/evidence/final-results-review-r2.md) checks the actual reranking, complete declared boundary and remaining assumptions. Formal item closure remains with the owner.
