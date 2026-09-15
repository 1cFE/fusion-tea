---
Status: implemented
Created: 2026-09-15
Updated: 2026-09-15
Related Artifacts: spec.md; design.md; plan.md; evidence/contract-migration.json
---
# WI-061 implementation

The native model now compares its nominal current-density-sized pack envelope, explicit internal sheet pitch, external ground insulation and assembly allowance with an independently allocated local casing cavity. The reference fails radially by 0.120 m and passes transversely by 0.021 m under the reviewed conditional scenario. At reference, all 195 prior native numeric outputs and eighteen responses are checked for exact equality against the WI-060 native baseline; the coordinator study will compare the 179 shared oracle-mapped scalars off design. baseline LCOE is $144.73830113443233/MWh.

The radial cavity is the existing coil-layer allocation minus two independent wall allowances. Sweeping that allocation retains all existing radial-build consequences. The transverse cavity is an independent assumption. The model distinguishes nominal envelope, additional internal build, pack, ground-insulated pack, required assembly envelope, casing interior and exterior. The source does not resolve whether its published pack envelope already includes the pancake sheets; the nominal excluded-sheet fraction 0.025 and included-sheet alternative zero explicitly retain that uncertainty.

## Execution and evidence

- Independent design release: goal evidence/design-review.md. Its remaining editorial corrections are applied, including centered alignment and nominal-envelope terminology.
- Fresh generation: evidence/generation-indicator-repair.log and regenerate.py establish two fresh package inventories identical to production, preserving all twenty-two inherited manual bodies and adding one reviewed fit completion. The first attempt's new-seed tuple signature mismatch is retained in generation.log/generation-debug.log and rejected-signature-seeds.json. No inherited body changed.
- Predicate representation: native execution supports the original conjunction, but the indicator producer rejects its nested comparisons. The implemented equivalent checks minimum_margin=min(margin_x,margin_y)≥0. Both axis margins remain public. This coordinator-approved representation repair is recorded in design.md and has native equality/each-axis equivalence tests.
- ABI: seven new public scenario inputs; existing coil_t gains its missing oracle mapping; seventeen numeric fit outputs; one new predicate. The complete contract has 299 inputs, 212 numeric channels and nineteen predicates. evidence/contract-migration.json proves every original predicate expression unchanged and no prior inputs/outputs removed.
- Baseline receipt and metadata: evidence/repin-final.log/baseline.json compare all 196 oracle-mapped native channels. Native producers refresh manifest fingerprints, census and tracked structural snapshot. The live runner and study route recognize nineteen predicates; the manifest records reference fit failure.
- Native validation: evidence/validate-final.log passes L1/L3/L4/L5 and fails L2/L6. Compared with WI-060, the ten literal-binding warnings, L6 diagnostic counts and first five printed diagnostics match; the log elides the other 262 diagnostic identities. New file/definition/usage and binding counts differ as expected. No claim of all-identity L6 equality is made. This is not an all-levels pass.
- Traceability and validation: native PM registered the calculation's scenario basis and SV-108. The PM command retains existing validation-matrix parser warnings for two unrelated malformed Type values. SV-108 is passing based on the 92 fit checks in fit-tests-final.log and the same file in model-affected-recheck.log, including the added all-195 native baseline comparison.

## Regression checks

The original affected-consumer batch retained in evidence/consumers-initial.log reported 409 passes, 31 failures and 37 errors. These exposed stale cardinalities, historical adapter assumptions and the conjunction grammar limitation. Current repairs preserve frozen records and explicitly adapt only added channels/predicate at consumer boundaries. The next batch in consumers-recheck.log passed 526, with seven failures, one skip and ten errors. Most outstanding study checks refused the uncommitted package as required. The full model suite then passed 968, with thirteen inherited skips, four stale test failures and 46 errors from one old radius fixture. Model-affected-recheck.log records the complete affected-file rerun: 205 passed and one remaining ledger expectation failed because it omitted the new structured evaluation channel. The ledger repair passes all seven tests in ledger-final.log. No full-suite rerun is claimed. The git-clean-dependent batch in clean-study-recheck.log passed 210 with one skip and two stale expectation failures: the verifier expected-name set omitted fit, and the R14 expected violated-name set omitted its new fit failure. Both expectation sets are repaired; final-corrected-consumers.log records two passes with fresh native fixtures. Another 48 operand/domain/empty-result checks pass in remaining-consumers-final.log. Coordinator-owned independent implementation review, native integration and bounded study are the downstream handoff.

## Supported claim

This is a conditional centered, aligned rectangular local screen at one representative station. The 0.30 m coil allocation is an inherited default, not a measured casing dimension; its incompatibility with the 0.36 m nominal pack is reported without tuning. Thermal surface and stress remain prior approximations; wall mass, added insulation procurement, cold deformation, fillets, offsets, insertion path, conductor-current margin and three-dimensional coil interference are not qualified by this screen.

## Candidate identity

Owned implementation checkpoint: ece3a7ed. Semantic fingerprint: d61aff71c088a81d1c12da1817511b7aede938df05a34d5a6bd278c56ec55386. Executable fingerprint: c9c9f4c962e8b3d7c06652a22541411ec643d2f44385dee0ed5b145027b820f6. Later test/documentation receipts do not change this package. Final source hashes and full package hashes are in evidence/model-hashes.json and evidence/package-hashes.json.

## Final native return

All observed implementation/consumer failures have explicit repairs and passing focused evidence. The full model suite and first consumer failures remain retained; no clean full-suite rerun is claimed. The final two clean-native consumer corrections pass, the seven ledger checks pass, and the separate 48 operand/domain/empty-result checks pass. SV-108 is passing. Source and generated package remain unchanged from ece3a7ed; final receipts and current-test fixes are committed separately for independent review.
