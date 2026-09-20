---
Status: implementing
Created: 2026-09-19
Updated: 2026-09-19
Related Artifacts: spec.md, design.md, interface-inventory.md
---

# WI-073 implementation and verification plan

[AGENT] This is the persistent plan for the reviewed design candidate. Source/prototype work and the structural probe are complete. Canonical implementation was released by the fresh corrected design PASS at goal `evidence/round2/cycle-design-review.md`. Mark each item when its evidence exists; do not mark review, integration or archive work complete from an author check.

## Phase 0 — research and design release

- [x] Preserve the original proposal, six-case prototype/results and native research runs. Independent source/math review is `evidence/round2/cycle-physical-review.md` under the current comparison goal.
- [x] Apply its three findings in versioned `cycle-proposal-v2.md`: no invented moisture fence, unresolved 3% allowance overlap, guarded conditional cooling water. Save through the native operation as `knowledge/research/pending/20260919-203209_comparison-matched-rankine-cycle-v2-final.md`; no DI adoption is implied.
- [x] Record additive manual mode/entry-point probe and specialization failures in `structure-options.md` and its evidence. Select the additive route and exact interfaces in `interface-inventory.md`.
- [x] Fresh independent design review covers scientific applicability, structural bindings, mode/current check inventory, held-efficiency seam, tolerances and phases below. Resolve material findings before canonical implementation. Coordinator records release without conflating it with owner replacement adoption.

## Phase 1 — source asset and guarded solver

Scientific author owns new `models/library/analyses/mfe_matched_steam_cycle.sysml`, canonical `models/library/data/matched_steam_properties.json`, and the corresponding handwritten modules under `exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/`. Use the installed generator and existing manual-stage mechanism, not a second production implementation hidden in tests.

- [x] Extract the three original NIST tables into the canonical physical asset, retaining full precision, separate phases, both saturation endpoints, query/reference-state metadata and hashes. Retain the erroneous SatT capture separately; it is never an asset source.
- [x] Implement the exact `Matched Steam Cycle`, `Cooling Water Rejection` and `Cycle Mode Selection` contracts. Guard enable before property lookup. Add precise finite/domain/phase refusals and explicit inactive/UA-unavailable semantics. No extrapolation or moisture acceptance fence.
- [x] Implement analytic piecewise profile minima/UA, extraction mass/energy closure, distinct turbine/pump/generator work and rejection. Keep gross and cycle-net meanings distinct. Record output inventory and every input's model owner.
- [x] Preserve source/staged asset identity and source hashes across stock generation. Negative checks reject tampered or mismatched asset bytes. No runtime network lookup or new external property dependency.
- [x] Run focused author checks against the retained six-case source arithmetic and domain/mode edge cases. Record precise commands/receipts and preserve failures. These are not independent oracle evidence.

## Phase 2 — structure and native wiring

Scientific author owns `models/library/structure/mfe_steam_cycle_components.sysml`, extensions to `mfe_interfaces.sysml`, `mfe_plant_systems.sysml`, `models/designs/generic_mfe/mfe_subsystems.sysml`, `mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml`, and additive power-balance inputs in `mfe_power_balance.sysml`. Preserve other agents' changes. Coordinator supplies one package-generation window.

- [x] Add the named SG/turbine/heater/reheater/condenser/pump/generator occurrences, functional descriptions, water/heat/shaft/electric connections, and actual state/work/duty aliases. Keep unsupported condensate-pump outlet T/s absent. Trace components and calculations to WI-073 requirements and source/assumption comments.
- [x] Expose existing heat-transport producers through pure aliases. Bind `salt_flow*ihx_count`, with `ihx_count=n` and `salt_pump_count=2n`; never double the salt heat by using installed pump count. Existing source and pumping equations remain unchanged.
- [x] Keep raw legacy fit argument feeding the old cooling diagnostic. Bind the new matched solver downstream of cooling. Prove the actual generated graph acyclic and verify producer ordering. Confirm no state/property output becomes a free entry point.
- [x] Generic matched/CW modes default off; current stellarator selects both reference scenarios. Preserve old fit/direct modes. Record raw legacy checks with explicit mode applicability, and execute actual matched source-domain/admission/CW checks for current mode. Never turn old failed values into true values to obtain a pass.
- [x] Add each new electric pump demand once to recirculation. Verify `p_the=matched gross`, equal heat bases, unchanged 3% formula, explicit loss accounting and cost drivers. Preserve legacy zero-load arithmetic under original test policies.
- [x] Parse/validate the affected model and regenerate once through the stock workflow. Record actual commands, semantic/executable identities and canonical/staged asset equality. Classify existing static failures without claiming a clean check from skips.

## Phase 3 — independent verification and bounded integration

A fresh independent oracle author reconstructs original-property states and equations without importing production or the research prototype. Production author fixes findings; oracle author owns oracle implementation/mappings. Coordinator and coding owner agree file ownership before changing `verify_stellaris.py`, `studies/oracle_entry.py` or shared check catalogs.

- [x] Independently verify source transcription/reference states, phase boundaries, property inversion, local pump approximation and exact piecewise profiles. Record the 40°C compressed-state benchmark limitation. Do not promote interpolation resolution observations to global accuracy claims.
- [x] Map every new primitive numerical output and Boolean/status field to an independent expectation or exact source/identity rule. Include physical component bindings and all changed downstream account identities. No broad skip, expected-current snapshot or test-only duplicate call to production.
- [x] Compare baseline and reviewed diagnostic states with the existing relative1e-9/absolute1e-6 scalar policy and preserved stricter quantity-specific policies; keep justified reference-quadrature UA tolerance separate. Preserve the original Round1 minimum20K-screen/10K-failure evidence when reporting current positive-gap admission. Keep non-reheat results as adverse diagnostics without an invented failure fence. Check strict gaps and source-domain refusal boundaries independently of numeric agreement tolerance.
- [x] Execute wrong pressure, table/phase boundary, nonfinite, invalid mode, disabled invalid-property, nonpositive heat/gap/denominator, negative/zero flow and asset-tampering cases. Preserve raw refusal evidence separately from completed adverse engineering cases.
- [x] Execute a nondefault circuit-count native case and check branch mass/heat sums against actual equipment producers. Verify baseline 14-circuit versus 28-pump interpretation and all per-circuit/total units.
- [x] Produce native before/after thermal, gross efficiency, steam/CW/primary/salt pumps, net electricity, capital and LCOE comparison. Preserve other raw engineering failures. Retain the full 3% main allowance and separately report the 0/half/full pump-overlap hypotheses with fixed other loads/costs; no validated uncertainty claim.
- [x] Fresh integrated science review covers native states, component/port agreement, account boundaries, controls, source domains and limitations. Record SV-122 evidence/status through the native PM operation only when its criterion is met.

## Phase 4 — regression, comparison migration and closure evidence

Coding owner owns source-derived changed/unaffected/added/retired mappings and comparison/archive tooling. Scientific author supplies the exact final interface and assumptions. Coordinator owns native integration and final records; scientific package generation remains single-owner.

- [x] Preserve all historical fixtures and original numeric comparison policies. Derive affected partitions from changed dependencies; regenerate no expected anchors from current outputs. Run existing generic fit/direct and relevant historical replay scopes; name genuine incompatibilities precisely.
- [x] Migrate held-cycle seam atomically: disable matched and CW modes with old direct-efficiency controls. Mark new state/pump predictions unavailable and held gross/dependents conditioned. Report unsupported matched-auxiliary comparisons as incompatible; preserve formal acceptance bands and selection rules.
- [x] Refresh exact entry-point/control/read-set/quantity/predicate inventories, source-aware accounting checks, independent output coverage and reporting applicability. Preserve legacy raw check results while ensuring unused-fit domains cannot govern current matched validity. Execute grouped-seam tests and dependent-role tests.
- [x] Run affected regression suites and then the coherent agreed full scope. Classify failures against original contracts. Broaden only for changed dependencies or unresolved concerns; preserve prior run receipts.
- [x] Fresh affected-cell depth assessment against the unchanged rubric, especially R7.P/S and R8.P/S. Old identity-based 23/23 carryforward cannot certify changed scientific content.
- [x] Commit/audit exact scientific and generated lineage under coordinator ownership; run native integration including every entry-point read, independent numeric/predicate checks and account joins. Update the spec acceptance evidence and current work through the coordinator.
- [x] Hand the integrated reviewed identity to the coding owner for actual candidate refresh/freeze/restoration. This item's science evidence does not substitute for actual archive reconstruction, owner adoption or reveal authorization.

## Requirement-to-evidence map

| Spec outcome | Required observation | Basis | Evidence/status |
| --- | --- | --- | --- |
| R1 finite heat admission | Both original-table profiles and native branch heat sums agree; raw nonpositive approaches fail strictly | Three NIST tables, preserved salt producers, analytic integration | Physical prototype reviewed; native pending Phases 1–3 |
| R2 heat/work closure | Mixing, cycle shaft/electric and cooling-water balances close; pumps counted once; gross cost drivers retained | Conservation identities; explicit component assumptions; design arithmetic tolerances | Prototype reviewed; independent native outputs/accounts pending |
| R3 source applicability | Full table transcription/hashes, explicit performance/site/cost limits, no unsupported moisture fence or T/s | Original NIST/EPA/Dostal; critic findings | V2 dispositions complete; staged identity/source review pending |
| R4 failures/domains | Domain refusals retained; inactive mode guards; raw adverse engineering values and exact predicates retained | Captured property support and original physical inequalities | Focused negative tests and native receipts pending |
| R5 physical architecture | Named component functions, meaningful bound states and connected exchanges; acyclic executable dependency graph | Structure probe, architecture/EXPOSE rules | Interface designed; actual parse/codegen/structure review pending |
| R6 independent/regression | Every new numeric/status/predicate covered, legacy policies intact, held seam conditional, before/after native effects recorded | Independent source derivation and exact input graph | Fresh oracle and coding migration pending |
| R7 bounded integration/depth | Small prescribed cases, exact integration identity, fresh affected depth grades and full affected scopes | Unchanged rubric/criteria and native integration rules | Pending after coherent implementation |
| SV-122 | Matched source-state/heat/work checks and failure evidence satisfy registered criterion | Reviewed design and numerical policy | Pending; no pass claimed |

## Implementation receipts — 2026-09-19

[AGENT] Phase1 author checks: `evidence/production/implementation.md` records184 passes and full source transcription. An initial exact-zero heat-gap failure is retained; endpoint evaluation now preserves specified temperatures without relaxing strict acceptance. Independent source/reference checks are `evidence/independent-oracle/README.md`; they do not yet certify native channel wiring.

[AGENT] Canonical physical architecture and ownership passed fresh review at goal `evidence/round2/cycle-native-structure-review.md`. Stock generation first refused mode equality under the exact-route policy; the equivalent guarded0/1-domain inequality passed. The raw first log is retained. The first seed-preserving generation found missing typed function signatures in all three new handwritten modules; no old manual seed changed. Typed signatures and tuple orders are being synchronized with the actual generated stencil before native execution. Generated readiness remains unchecked until exact repeated generation succeeds.

[AGENT] Final corrective generation is `evidence/generation-v3.log`; exact current identities and fresh baseline are in `repin-v2.log` and `baseline.json`. The independent nine native cases check9450 scalar/status values and252 strict predicates; seven native/oracle invalid cases refuse explicitly, including both inconsistent heat modes. Canonical/staged asset identity and r2 custody are `asset-and-r2-custody.json`; source-asset tamper/missing checks are part of the final author receipt. The generated-wrapper contract has21 inputs after the reviewed two-producer heat guard, with unchanged78 outputs. `result-delta.json` records the raw-default before/after and separate fixed-cost overlap hypotheses. Current model has511 free input parameters,1050 scalar/status outputs and28 engineering predicates. These counts do not certify pricing or hardware qualification.

[AGENT; 2026-09-20] The reviewed regression migration has382 focused passes,121 candidate/custody passes and one final exact-status replay pass in the coding item’s `regression-evidence/cycle-migration/`. The WI-072 historical-mode repair adds13 passing checks; the post-residual-sign independent native run repeats9450 scalar/status and252 strict predicate comparisons. Full scopes and integration remain unchecked until their final receipts exist. Earlier failing full runs are retained.

[AGENT; 2026-09-20] Final full scopes finish with3585 passes, zero failures/errors,14 ordinary skips and two strict historical CLI incompatibilities across3601 collected cases. Model scope contributes2310 passes; study/candidate contributes1275. The ordinary skips are13 unused foundation templates and one missing historical proof-of-life store. Original failure receipts remain retained. Source/node reconciliation and final independent R6 audit are the remaining documentary gate before archival admission; current source/executable identities are unchanged.

[AGENT; 2026-09-20] The fresh non-author completed R1–R7 audit PASS after independently reconciling3601 nodes and120 unchanged source hashes. All ten integration gates and the separate input-read coverage check pass. Scientific implementation and its regression obligations are complete; the exact identity is supplied to T-010 for final archived comparison preparation. Actual archive reproduction and owner adoption remain T-010/owner gates, not silently closed by this item.
