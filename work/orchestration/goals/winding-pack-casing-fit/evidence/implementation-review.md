# Independent WI-061 implementation review

Date: 2026-09-15. Verdict: **PASS for the bounded implementation; no material implementation finding.** Final author receipt checkpoint: `b69616b3`. Code candidate: `ece3a7ed11bc6830fc56573502fe7d11f7116b0a`. Semantic fingerprint: `d61aff71c088a81d1c12da1817511b7aede938df05a34d5a6bd278c56ec55386`. Executable fingerprint: `c9c9f4c962e8b3d7c06652a22541411ec643d2f44385dee0ed5b145027b820f6`.

## Independence and scope

This reviewer is `geometry_research`, not the continuation of `fit_reviewer` named in the original implementation brief. I authored `geometry-research.md` and explicitly exclude independent certification of that report and its source recommendations. I did not author the implementation, generated package, oracle, model tests or consumer repairs. Source/design acceptance relies on the separate fresh non-author review in [design-review.md](design-review.md), which inspected the original figures and accepted the conditional scenario before implementation. This review checks implementation against that accepted design. The separate source reviewer could not resume because the coordinator encountered the agent thread limit.

The reviewed route has seventeen numeric fit outputs, seven added scenario inputs, one additional mapping for existing `coil_t`, and one new predicate. Counts in the initial review brief referring to sixteen outputs are superseded by the explicit minimum-margin output. The complete live contract has 299 inputs, 212 numeric outputs and nineteen predicates; the oracle maps 196 numeric outputs.

## Code and mathematical findings

No material implementation defect identified. The source definition in `models/library/analyses/mfe_winding_pack_fit.sysml`, magnet bindings in `models/library/cost_structure/mfe_power_core.sysml`, physical owners in `models/library/structure/mfe_magnet_parts.sysml` and concrete scenario/constraint in `models/designs/stellarator_09/stellarator_plant.sysml` implement the reviewed dimensions and orientation. Pack demand comes from the existing live `wp_side`; cavity x comes from independently held `coil_t-2*wall`, and cavity y from an independent input. No dependency grows the cavity automatically with demand.

The manual completion in `exploration/stellarator_e2e/generated/handwritten/mfe_winding_pack_fit/winding_pack_casing_fit_impl.py` checks all inputs for finite sign domains, checks doubled allowances and positive cavity geometry, rejects nonfinite or destructively underflowed dimensions, and preserves signed finite negative margins as valid results. Ground insulation and assembly clearance each enter twice, once for each opposing face. Additional internal build enters through the independently reviewed axis fractions. No fit geometry feeds a new procurement or support charge. The old thermal and stress proxies remain explicitly limited.

The completion returns fields in the generated schema's actual order. I checked its order against the wrapper unpacking and reconstructed all seventeen fields independently in execution. The native predicate uses `minimum_margin >= 0`, mathematically equivalent to the two-axis conjunction for the finite margins admitted by the completion. Exact equality passes without a tolerance. The standalone generated predicate remains part of the normal runtime constraint machinery; geometric domain validity belongs to its producing calculation.

The oracle in `exploration/stellarator_e2e/verify_stellaris.py:702` reconstructs nominal area from current, reference density and purchased field envelope, without consuming generated fit outputs. New input/output/operand mappings in `studies/oracle_entry.py` cover all added dimensions and the predicate operand. Existing conductor-domain checks run upstream of the new oracle helper on the public compute route. Direct calls to the private helper are not a replacement for the whole oracle's conductor-domain contract.

## Independently executed evidence

All reviewer commands used `.codex-test/run` and made no production changes.

| Check | Observed result |
|---|---|
| `python -m pytest tests/models/test_winding_pack_fit.py -q` | 92 passed, 11 existing Boolean serialization warnings. Includes binary-exact contact, each-axis failure, arithmetic domains, public native/oracle agreement, all 195 old baseline numeric values and eighteen old responses. |
| `python -m pytest tests/models/test_structure_translation.py tests/study/test_operand_bindings.py -q` | 24 passed. Confirms live ledger and operand mappings after the structured fit-evaluation addition. |
| Independent deterministic random reconstruction, seed 6109, 100 rectangles | All seventeen wrapper fields match separately constructed geometric identities; native predicate matches both signed margins. Inputs span varying side, aspect, both internal fractions, ground, clearance, wall and independent cavity dimensions. The first attempt lacked the simkit import path; the corrected invocation used the documented runtime environment's `STOP_PARSER_TEAX_ROOT/packages/teax-simkit` and passed. |
| Independent native demand perturbations | Increasing current 20%, reducing reference density 20%, and raising purchased envelope to 30 T each increase pack demand and reduce radial margin. Resulting margins: −0.15436024140371957, −0.1624922359499621 and −0.14069666566094308 m. |
| Independent native allowance perturbations | Setting internal x fraction to .1, external ground to .01 m, and assembly allowance to .015 m independently matched all 196 mapped oracle values while preserving all old numeric outputs exactly. |
| Direct catalog comparison against `d64aea81` | All eighteen old predicate IR strings unchanged; exactly one predicate added. |
| Direct SHA256 and byte comparisons | All 22 inherited manual implementations unchanged; all 32 canonical/twin model pairs equal; all 284 package receipt files match their recorded hashes. |

The baseline failure remains the reviewed result: radial margin −0.120 m and transverse margin +0.021 m. The independent executions establish implementation behavior under the assumptions, not manufactured cavity dimensions.

## Author evidence inspected and limits

I inspected the fresh-generation recipe, its exact-repeatability receipt and package inventory. It seeds the reviewed manual bodies, generates two fresh packages and compares full inventories. I independently verified current receipt hashes; I did not regenerate the package during review. The one changed inherited `special_materials_capital_impl.py` is auto-generated and changes source-location comments only; the twenty-two manual bodies are unchanged.

Current census, structural snapshot, manifest provenance, explicit ABI additions and historical comparison adapters were inspected. Adapters remove only the new predicate from old eighteen-check comparisons and explicitly extend current channel/parameter sets. Frozen historical work records are not rewritten. Indicator expected JSON changes represent new live dependency/catalog output, not changed historical physics expectations.

The final affected model batch recorded 205 passes and one stale ledger failure; the repaired ledger passes all seven tests, independently rerun as part of the review's 24-test check. The clean study batch recorded 210 passes, one skip and two stale predicate-set expectations. `final-corrected-consumers.log` records both repaired tests passing; `remaining-consumers-final.log` records another 48 passes. I inspected the repairs: they explicitly add `wp_fit_ok` and its one computed operand, and retain all old expected verdicts. The earlier full model run is not a final green full-suite result, and no such claim is made.

Native complete validation reports L1/L3/L4/L5 pass and L2/L6 fail. Direct diff against WI-060 shows the same ten placeholder-binding warnings, L6 category counts and printed first five diagnostics, with expected new file/definition/usage/binding counts. The log elides 262 L6 identities, so this review does not certify identity-level equality for all 267 diagnostics. That limit is now stated correctly in the implementation report.

This bounded review leaves coordinator native integration and the 72-point matched entering/candidate study separate. It does not certify study conclusions, whole-design feasibility, real casing dimensions, local stress, thermal-surface accuracy, insulation procurement, cold deformation or three-dimensional assembly.

## Final checkpoint acceptance

Final author receipt `b69616b3` was inspected before this verdict. Its changes are the reviewed consumer expectation repairs, runner label, validation status and documentation/receipts; native source and generated package remain unchanged from `ece3a7ed`. The final implementation report accurately states the passing focused reruns and incomplete full-suite/all-diagnostic-identity coverage. The plan evidence table still labels several already demonstrated implementation obligations Pending; the native audit below supplies their bounded dispositions without changing coordinator-owned off-design/study obligations. This is a documentation bookkeeping lag, not a code defect.
