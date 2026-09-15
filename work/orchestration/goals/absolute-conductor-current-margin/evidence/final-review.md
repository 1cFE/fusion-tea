# Independent final current-margin review

Date: 2026-09-15. Reviewer: `/root/current_reviewer`, non-author of model implementation, study and answer. **PASS. The bounded technical objective is complete; recommend owner-held formal closure and item archival.** No further model or study work is required to answer the stated conditional question. This review does not close or archive either record.

## Scope and examined identities

Reused `source-design-review.md` and `implementation-review.md`. Their scope remains valid: copied source interpretation and oracle files are byte-identical to their reviewed counterparts, and the admitted Molodyk PDF retains SHA-256 `2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b`. No barred source was read.

- Model/package implementation: `09178a90310c6a973b1097fe94bd960ce1b6f80b`; final consumer checkpoint reviewed previously: `2f4c2efcd3cd35da17d9089f075e92847bf16ac3`.
- Semantic fingerprint: `f1340dda1471f65942e804579adc14b21344f9e1e4f26f04e8567214483c2ed8`; executable fingerprint: `c0a7ef4a259082952bece2bf40b5a7cfaa570c317ae8f1dd4026fc33bdae46be`.
- Native integration pin: `855a3a3b88c277e169aa3265db273c3d24686a6d762d7bd8437c0fd987c6160f`. All ten implemented gates report PASS and match the study identity. Independently recomputed the live package's 289 contract artifact hashes; all match.
- Frozen study: `e1f5516b077c85f557ba979aeb1fe2cf8c5b4e8b`; snapshot SHA-256 `7980b775611fd1b7855a8b69c8f6dfede2c2ec996aa2f3aef7aae2efa0bf75f4`.
- Round result/answer/dispositions: `ce229522`, with answer precision/link corrections and explicit entering-predicate enumeration at `fccc80da`. Those corrections do not alter frozen evidence.

## Independent integrity and numerical checks

Read-only checks used `.codex-test/run`, with the documented simkit path for executable oracle checks. No author checker that rewrites frozen files was run.

1. Recomputed all **445 snapshot artifact hashes**. Verified all **453 required retained files** exist in the freeze commit and remain byte-identical to that commit. Checked each of the 296 report aliases against its canonical native inputs; they resolve to exactly 295 unique cases.
2. Opened both SQLite stores read-only. The baseline store contains one completed case; the study store contains **295 completed cases and 295 valid proposals**. Independently joined every study case's input, content-addressed artifact digest, outputs, twenty verdicts and complete report coverage to the exported native row. No exported case lacks a native witness.
3. Recomputed the retained all-point oracle comparisons: **61,065 scalar comparisons and 5,900 predicate comparisons**, all agreeing at the declared tolerance. Maximum relative difference is `2.474163829169531e-12`. All eleven new outputs are mapped; the sixteen older unmapped outputs are explicitly disclosed.
4. Independently reconstructed all **eleven current outputs at all 295 cases** from physical tape/conductor lengths, distinct current/volume distribution factors, actual field, tape dimensions, source normalization, material/orientation factors, retention factors and one allowable fraction. The fraction predicate agrees everywhere. This calculation was separate from the author analysis script and oracle helper.
5. Recomputed entering attribution: **22,932 prior-channel comparisons and 2,223 old-predicate comparisons** over 117 aliases. The complete entering nineteen-entry predicate catalog is unchanged. Recomputed **177 performance-only pairs**, covering **37,524 old-output and 3,363 old-predicate comparisons**; all agree. The separately captured reference covers all 212 prior numeric outputs. This does not claim off-reference native execution of an older package.
6. Freshly evaluated five representative points through the independent oracle: reference, cheapest entering pass, its orientation-3 case, its mixed-retention orientation case, and the predicate-independence example. Each agrees on 207 mapped channels. Rechecked both turn repartitions: tape quantity/cost stay fixed and operating fractions are invariant. Fresh oracle evaluation also refuses the sole out-of-domain endpoint at **32.09058362175721 T**; it has no native proposal or predicate-failure claim.

## Answer and source assessment

All scenario counts in the answer reproduce from native verdicts. The reference has **29,646.755 A** critical current against **50,000 A** operation, fraction **1.686525**, and allowable-current margin **−26,282.596 A**. Nominal fit remains failed. All twelve entering nineteen-predicate passes fail the current predicate under default performance. The thirteen combined passes require orientation factor 3; twelve use ideal retention and one uses three factors of 0.9. Material-only scenarios recover none of the sixteen anchors.

The answer correctly distinguishes statistical normalization from exact-construction measurements, approximate empirical prediction from extrapolation, and reference-conductor capacity from set-effective or worst-coil capacity. It preserves source ungraded-versus-graded allowance interpretation and does not tune normalization, geometry or prices to pass. Independent selected-envelope and current predicates remain justified. The unchanged price of improved-performance scenarios is explicitly a missing supplier cost/performance relation, not an economic optimum.

Two answer-only precision issues were corrected during review: the distribution ratio now names distinct coil-current and winding-pack-volume factors; the accounting sketch now shows the executable fraction-margin predicate. The corrected public-interface link and every other local answer link resolve. No frozen artifact required correction.

## Goal and finding dispositions

The four task returns and Round 1 result precede this review. The trail records one promoted pin and one frozen study. Import-path corrections and numeric export normalization are mechanical execution corrections: native proposals, package identity and scientific assumptions did not change. They do not require a semantic retry. No additional semantic work is released by the answer.

All **fifteen incoming plus nine new findings** appear exactly once in the current goal's joined discovery-log dispositions. Their partial-fix and remaining-seam language preserves open qualification, geometry and cost limitations. Proposed L-001, L-002 and L-003 accurately summarize the independent-predicate result, conditional orientation/retention result and series/inventory/allowance identities. They are suitable for acceptance as scoped findings; none establishes conductor qualification.

## Remaining limits

This PASS covers numerical consistency and an evidence-supported conditional estimate. Exact product/lot construction, a common high-field criterion, local angle/temperature distribution, cable sharing/degradation and weakest-location performance remain unqualified. The 32 T cutoff is an engineering scenario bound. There is no continuous feasible-boundary, manufacturing-price or optimized-machine claim.

Native L2/L6 remain non-green; the previously reviewed ten placeholder warnings and twelve added EXPOSE diagnostics are not erased. The integration manifest gate expressly omits `assert_read_set_covered`, with no replacement coverage claimed. The unavailable historical-store verifier skip and sixteen unmapped old channels remain limitations. No broad-suite rerun or independent reconstruction of all old physics is claimed. Source quarantine and owner-held merge/push/closure boundaries remain intact.
