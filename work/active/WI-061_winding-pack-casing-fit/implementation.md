---
Status: implementation-validation
Created: 2026-09-15
Updated: 2026-09-15
Related Artifacts: spec.md; design.md; plan.md; evidence/contract-migration.json
---
# WI-061 implementation

The native model now compares its nominal current-density-sized pack envelope, explicit internal sheet pitch, external ground insulation and assembly allowance with an independently allocated local casing cavity. The reference fails radially by 0.120 m and passes transversely by 0.021 m under the reviewed conditional scenario. Its procurement, thermal, support and economic outputs remain unchanged at held old inputs; baseline LCOE is $144.73830113443233/MWh.

The radial cavity is the existing coil-layer allocation minus two independent wall allowances. Sweeping that allocation retains all existing radial-build consequences. The transverse cavity is an independent assumption. The model distinguishes nominal envelope, additional internal build, pack, ground-insulated pack, required assembly envelope, casing interior and exterior. The source does not resolve whether its published pack envelope already includes the pancake sheets; the nominal excluded-sheet fraction 0.025 and included-sheet alternative zero explicitly retain that uncertainty.

## Execution and evidence

- Independent design release: goal evidence/design-review.md. Its remaining editorial corrections are applied, including centered alignment and nominal-envelope terminology.
- Fresh generation: evidence/generation-indicator-repair.log and regenerate.py establish two fresh package inventories identical to production, preserving all twenty-two inherited manual bodies and adding one reviewed fit completion. The first attempt's new-seed tuple signature mismatch is retained in generation.log/generation-debug.log and rejected-signature-seeds.json. No inherited body changed.
- Predicate representation: native execution supports the original conjunction, but the indicator producer rejects its nested comparisons. The implemented equivalent checks minimum_margin=min(margin_x,margin_y)≥0. Both axis margins remain public. This coordinator-approved representation repair is recorded in design.md and has native equality/each-axis equivalence tests.
- ABI: seven new public scenario inputs; existing coil_t gains its missing oracle mapping; seventeen numeric fit outputs; one new predicate. The complete contract has 299 inputs, 212 numeric channels and nineteen predicates. evidence/contract-migration.json proves every original predicate expression unchanged and no prior inputs/outputs removed.
- Baseline receipt and metadata: evidence/repin-final.log/baseline.json compare all 196 oracle-mapped native channels. Native producers refresh manifest fingerprints, census and tracked structural snapshot. The live runner and study route recognize nineteen predicates; the manifest records reference fit failure.
- Native validation: evidence/validate-final.log passes L1/L3/L4/L5 and fails L2/L6. Compared with WI-060, the ten literal-binding warnings and all 267 scanner diagnostics remain unchanged; only the new file/definition/usage and binding counts differ. This is not an all-levels pass.
- Traceability and validation: native PM registered the calculation's scenario basis and SV-108. The PM command retains existing validation-matrix parser warnings for two unrelated malformed Type values. SV-108 remains pending until the final retained tests pass.

## Validation still running

The original affected-consumer batch retained in evidence/consumers-initial.log reported 409 passes, 31 failures and 37 errors. These exposed stale cardinalities, historical adapter assumptions and the conjunction grammar limitation. Current repairs preserve frozen records and explicitly adapt only added channels/predicate at consumer boundaries. Final focused and full-model results will be appended after completion. Coordinator-owned independent implementation review, native integration and bounded study remain outstanding.

## Supported claim

This is a conditional centered, aligned rectangular local screen at one representative station. The 0.30 m coil allocation is an inherited default, not a measured casing dimension; its incompatibility with the 0.36 m nominal pack is reported without tuning. Thermal surface and stress remain prior approximations; wall mass, added insulation procurement, cold deformation, fillets, offsets, insertion path, conductor-current margin and three-dimensional coil interference are not qualified by this screen.
