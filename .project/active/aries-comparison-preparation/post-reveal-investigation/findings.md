# Findings from the post-reveal magnetic-field investigation

This is a working evidence log for the write-up. Entries distinguish recorded facts from interpretations and proposed changes. The original comparisons remain unchanged; this investigation is post-reveal.

## F-001 — The latest attempt reached unsupported conductor conditions

Status: observed. Evidence: `../post-reveal-results/post-reveal-v1/report.md` and its retained first-forward result.

The conductor calculation received 56.61785714285713 T at 20 K, outside the represented 20–32 T approximation. The attempt returned no completed numeric outputs or engineering verdicts. All 67 predicates are unevaluated, all 276 comparison rows are blocked and LCOE is unavailable. This is an evaluation refusal, not proof of physical impossibility.

## F-002 — The attempted point retained most of the existing design

Status: observed. Evidence: `../post-reveal-results/post-reveal-v1/request.json` and `input-evidence/held-input-inventory.json` in that result directory.

Three reference scalars were supplied. The other 701 inputs remained held, including 308 reference-coil turns and 50,000 A per turn. The field was calculated rather than supplied from the reference. The attempted point is not a fully reconstructed reference plant. F-005 records the completed audit of the transferred field approximation.

## F-003 — Published reference fields were already in the source record

Status: source review complete. Evidence: [source review](source-review/source-review.md), [field candidates and provenance](source-review/field-candidates.json), Lyon printed p708 Table IV, Ku p677, Najmabadi p669 and the retained historical source-value inventory under `../post-reveal-results/post-reveal-v1/source-evidence/`.

Lyon reports 5.70 T on axis and 15.08 T maximum field on the coils. Ku describes approximately 15 T maximum on the winding pack for 5.7 T on axis. The 15.08 T peak already appeared in the historical source-value transcription; the retained source table also contains the 5.70 T axis value. Failed native execution, not an absent reference peak, blocked the comparison. The source describes Nb3Sn magnets, with a roughly 4 K operating condition in the overview. Those are different conductor technology and temperature choices from the held model's REBCO/20 K assumptions.

The field values are comparison evidence, not permission to assign the model's calculated field to the published value or change conductor limits to make the run pass. The source-review record preserves exact quantity definitions, design-revision distinctions and page-image provenance. The 16 T number in the source is a design limit, not its achieved operating field.

## F-004 — The recorded field is reproducible arithmetic

Status: isolated arithmetic independently reproduced. Evidence: [reconstruction script](field-audit/reconstruct.py), [receipt](field-audit/receipt.json) and [independent audit review](source-review/field-audit-review.md), which bind the exact adopted archive and retained failed request.

| Intermediate quantity | Reconstructed value | Meaning |
|---|---:|---|
| Axis field | 14.7484 T | Calculated from held coil count, turns, current and linkage factor at the supplied major radius. |
| Coil-centre minor radius | 3.55 m | Supplied plasma size plus held radial-build layers. |
| Inboard clearance | 4.20 m | Major radius minus coil-centre minor radius. |
| Normalized geometric multiplier | 1.38756 | Model's bore correction relative to its calibration geometry. |
| Peak field | 56.61786 T | Axis field times held peak/axis factor times the geometric multiplier. |

Displayed values are rounded; the receipt preserves exact floating-point results. These values reconstruct the frozen equations; they are not newly published outputs of the failed native attempt. No arithmetic implementation discrepancy has been found in this chain. Arithmetic reproduction does not establish that its geometry approximation applies to the attempted design.

## F-005 — Scientific support is missing before the conductor calculation

Status: independently reviewed audit finding. Evidence: [field audit](field-audit/audit.md), [source provenance](field-audit/source-evidence.json) and [cross-review](source-review/field-audit-review.md), including direct inspection of Lion 2021 Equation 39.

The peak-field approximation retains one calibrated field ratio and a bore correction. Its source equation also includes a configuration-dependent winding-pack term. The implementation intentionally omits the changing contribution of that term because the required coefficients were not available. A calibration at one geometry cannot establish how the omitted contribution changes at another geometry.

The attempted transfer shrinks major radius while increasing coil-centre minor radius. It also retains coil count, current distribution and geometry-transfer factors. This is not uniform scaling of the original coil design. The audit identifies a scientific applicability gap in both axis and peak field transfer, rather than a demonstrated coding error or proof of an impossible reactor.

Conductor-independent results are not necessarily field-independent. The axis field feeds plasma calculations and downstream power/economic calculations. Restoring arithmetic after a conductor exception therefore does not establish scientifically supported LCOE at this point. Execution availability, model-definedness and scientific applicability must stay distinct.

## F-006 — Native execution discards independent diagnostic results

Status: synthetic native fault probe reproduced; additive implementation independently reviewed. Evidence: [probe](failure-propagation/probe.py), [probe results](failure-propagation/probe-results.json), [reviewed design](failure-propagation/design.md), [design review](failure-propagation/design-review.md) and [implementation review](failure-propagation/implementation-review.md).

At a synthetic conductor failure on the existing baseline, 111 computational modules had completed and 259 channels, including 231 numeric channels, were present in private memory. The ordinary failure contract returned none of them as model evidence. The graph identifies only three descendants of the conductor calculation: its adequacy predicate, the aggregate constraint report and the ExitPoint. Independent branches were never completed after the exception.

The selected repair is a separate native diagnostic API that continues independent branches, blocks descendants of errors and records a status for each public result. Ordinary complete-study behavior stays unchanged. Failed modules must not leak partial outputs, invalid intermediate numbers must not reach descendants, and unavailable checks must never become satisfied or violated. This is execution infrastructure; it does not resolve the field-law support gap in F-005.

## F-007 — A larger conductor interval is not the immediate scientific remedy

Status: interpretation supported by F-003 through F-005; no range change made.

The reference uses a different conductor technology and temperature, and its reported peak is below the current approximation's 20 T lower limit. The attempted model field is above its 32 T upper limit. Extending either endpoint merely to accommodate these numbers would not resolve mismatched coil geometry, technology or the field approximation. The next scientific change must be justified by the declared design family and source evidence, rather than by which guard stopped this run.

## F-008 — The current geometry representation couples plasma size and coil size

Status: audited binding and consumer behavior; no new automatic-sizing violation asserted. Evidence: the design-choice boundary section of [the field audit](field-audit/audit.md).

The radial-build representation places the coil relative to the plasma and intervening layers. Changing the plasma minor radius therefore changes the coil-centre radius and the derived circumference, which feeds material inventory and procurement calculations. Installed turns, pack side and coil thickness remain held. This is an explicit contiguous-layer geometry assumption, not an adequacy-driven sizing calculation.

The limitation matters: varying plasma size while keeping the coils physically unchanged is not represented by changing this plasma-radius input alone. Future design work must identify which geometry choices should be independently supplied and which relationships define the selected design. An audit of preserved supplied quantities does not by itself establish support for every desired design variation.

## F-009 — An additive native diagnostic path retains independent arithmetic

Status: independently reviewed and reproduced. Evidence: [implementation](failure-propagation/implementation.md), [source identity](failure-propagation/implementation-identity.json), [final synthetic receipt](failure-propagation/evidence/synthetic-v2/verification.json) and [implementation review](failure-propagation/implementation-review.md). Earlier synthetic-v1 evidence is retained separately.

The isolated native runtime now has a separate diagnostic API. On unchanged baseline inputs with an injected conductor-module exception, it retains 1,341 of 1,352 numeric outputs and 66 of 67 predicates. Every retained result exactly matches the ordinary baseline. Five retained predicates remain violated; the conductor predicate is unavailable. The aggregate constraint report stays blocked. Neither missing results nor unknown predicates are replaced with zeros or passes.

Both LCOE formulas remain numerically available in that synthetic test. The result explicitly says scientific qualification is not established. No ARIES request was executed by this diagnostic work, and none of the retained historical failures was replaced. The implementation is pinned in an isolated native-source snapshot with a portable patch; the shared runtime and adopted comparison package remain unchanged.

Fourteen focused tests and eleven existing native regression tests pass. Independent review reproduced the fourteen focused cases and the real-package synthetic fault, including exact parity of retained results. Review also verified the correction for invalid numeric fields inside structured outputs: a consumer cannot turn an infinite input into a valid-looking finite output. The collector keeps runtime errors, blocked dependencies, unavailable predicates and actual violations separate. These checks do not provide arbitrary Python side-effect rollback or scientific qualification of the model.

## Investigation record

The source review and field audit are complete and independently cross-checked. The native diagnostic design and implementation passed separate non-author reviews. Review required invalid intermediate values to block their descendants before they could produce valid-looking finite results. The ordinary complete-study contract remains unchanged. The [preservation receipt](evidence/preservation-after.json) verifies that 764 historical/model files are unchanged.

The [next-work recommendation](next-work.md) separates field applicability, configuration-specific magnetic qualification, future experiment selection and runtime adoption. These remain proposed follow-up work. This investigation did not repair or extend the magnetic-field equations, qualify the held design at reference geometry, or rerun the reference plant request.

[OWNER] Requested source-field verification, field-model audit, parallel efforts and this persistent log. [AGENT] Source review, independent field audit and failure-propagation investigation are assigned separately. No new formal reference execution or scientific range extension is authorized by the investigation plan.
