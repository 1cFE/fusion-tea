# WI-065 independent integrated review

**Final verdict: PASS within the validation limits below.** [AGENT REVIEW] The corrected implementation is released for native integration and study. This review does not certify either later result.

**Initial verdict: REVISE.** [AGENT REVIEW] The initial nonnegative operating-power guard suppressed existing signed negative operating-demand diagnostics in two shared current-sizing scenarios. This violated the owner's requirement to preserve failed cases. The correction below was released for implementation; its verification and final disposition are recorded in the addendum.

## Required correction

[AGENT REVIEW] Allow finite signed operating auxiliary power as well as signed required auxiliary demand. Require nonnegative total absorbed heat H and core radiation C≤H. Define power_account_valid=1 only when edge radiation E≥0 and operating auxiliary power≥0. Negative auxiliary demand then remains an invalid-physical-account diagnostic with unchanged signed output arithmetic and original predicates. Amend the original spec/domain contract to carry this correction. Cover the negative-operating corner directly and preserve both failing shared current-sizing scenarios against their entering outputs and predicates. Apply the same domain to the independent oracle.

## Evidence already checked

[AGENT REVIEW] Original source-review.md remains applicable to peaks, capture pairs, conservation, equivalent area and missing surface-radiation qualification. I inspected the native ledger, component/instance bindings, generated seventeen-output wrapper and handwritten completion, pipeline routing, independent oracle helper/call site, eight channel mappings and component/coupled tests. The peak retains the original product-then-division arithmetic. Capture changes deposited power and implied area together. No physical-area or average-flux lever is added.

[AGENT REVIEW] Independent hash checks verified all26 prior manual bodies against WI-064, the27-seed inventory, every recorded package hash, all three canonical/exploration twins and the frozen entering native-cases.json against25f9ce82. Total-power balance, viability definitions, primary-loop calculation and generic plant were byte-identical to that revision. The auto-generated special-materials change is source-line metadata only. Native pipeline outputs resolve the eight new component EXPOSEs to the ledger channels.

[AGENT REVIEW] The initial component log reports194 passes and the coupled log12 passes. The latter checks all entering outputs and all20 predicate responses for five frozen controls, plus independent oracle agreement at three controls under both source profiles. Separate paired-profile checks preserve non-divertor outputs and cost. My independent wrapper/oracle probes also agreed exactly for zero separatrix with negative edge radiation, dormant zero capture, full radiation and a negative-edge case, including signed required-demand margins. These probes passed after correcting my runtime import path; the first probe invocation failed to import simkit before executing any runtime checks.

[AGENT REVIEW] Consumer search identifies one direct ledger occurrence on the Divertor definition, its generic MFE plant occurrence and Stellaris specialization, with exploration twins. IFE/HIF is separate. The shared-consumer run revealed the operating-power defect above and a stale channel-count expectation. Its failures cannot be represented as passing evidence.

## Validation limits

[AGENT REVIEW] Native L1/L3/L4/L5 pass. L2 retains ten literal-binding warnings. L6 remains failing; the diagnostic comparison adds eight unsupported-dot EXPOSE diagnostics to inherited residue. Generated execution resolves those interfaces, but does not make the six-level static validation clean. Coupled runs retain the existing cryoplant boolean-serialization warning. Physical qualification still needs supported active source metadata, a valid power account and radiation/geometry/engineering evidence beyond this account.

## Final correction and release addendum

[AGENT REVIEW] The native contract, implementation, oracle and spec now permit signed operating demand with account-valid0. H<0 remains refused. Independent direct wrapper/oracle probes at auxiliary power −50, −400 and −401 MW verify positive-total and zero-total diagnostic handling and negative-total refusal. Updated receipt checks verify the current package and all26 preserved manual bodies. The component suite now passes198 checks. Fresh regeneration still proves exact package equality.

[AGENT REVIEW] The corrected-model shared run passes129 checks and initially fails only the two new preservation assertions. The first omitted the aggregate headline from its reference. The sized case additionally exposes an existing native/oracle floating-point sign difference at exact current closure. No threshold or predicate tolerance changed. The corrected tests compare old and new oracle scalars and derived predicates on their own basis, then compare every old native scalar and all native responses exactly against the original generated package. I verified all297 archived package files against the f76ec031951d7918fbfec2de23d298830941c121 git tree and checked the capture script uses that package. Each new entering capture contains234 scalar outputs and21 responses:20 predicates plus headline.

[AGENT REVIEW] The focused corrected rerun passes both cases; the reviewed production hashes are unchanged since the129 passing shared checks. Together these cover all131 selected shared/coupled checks, including14 divertor integration checks. Evidence is `work/active/WI-065_divertor-deposited-power-and-peak-area-account/evidence/consumer-tests-corrected-model-test-reference-failure.log`, `negative-entering-capture.log`, `negative-preservation-final.log`, `component-tests.log` and `regeneration.log`. Earlier failures remain retained. No missing test is counted as passing. The signed operating-power defect is resolved, exact entering predicate failures are preserved, and no further implementation correction is required within this bounded account.
