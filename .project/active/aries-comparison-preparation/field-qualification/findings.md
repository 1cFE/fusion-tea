# Write-up findings: field qualification

Continuation of [F-001–F-009](../post-reveal-investigation/findings.md) and [F-010–F-014](../partial-assessment/findings.md). This investigation follows exposure of the reference comparison. It makes no clean-holdout claim and supplies no new reference-point prediction.

## F-015 — Scalar tables do not define the published current paths

[OBSERVATION] The primary Stellaris paper specifies six coil families within its 48-coil, four-period set. It gives different family currents, turns and pack sides. The inspected local material supplies no executable centreline curves, pack frames or axis coordinates. The paper's data-availability statement says the data are available on request. [Evidence and inspected source images](evidence/local-inventory.md).

[INTERPRETATION] Aggregate radii, coil count and maximum current do not identify a configuration-specific magnetic field. A different turn/current pair yielding the same ampere-turns also does not reconstruct the published winding. This narrows the missing-data problem; it does not establish that the data do not exist.

## F-016 — The missing pack response cannot be inferred from one calibration

[OBSERVATION] The source peak-field relation contains two configuration-specific coefficients. Eight exact rational checks show that two positive coefficient pairs can match one normalized reference point and disagree when pack size is varied. Common current scaling and complete geometric similarity have the same relative response in both examples. [Executable proof](evidence/identifiability.py), [result](evidence/identifiability.json), [independent reproduction](evidence/reviewer-proof-receipt.json).

[INTERPRETATION] The omitted term is not identifiable from the single calibration. The illustrative coefficients are neither physical bounds nor candidate Stellaris parameters. The six published family columns cannot supply the missing controlled pack sweep because coil geometry and currents also differ. Scientific support requires configuration-matched magnetic calculations or equivalent independent data.

## F-017 — A newer author script names the missing baseline inputs

[OBSERVATION] A registered author script at revision `a79006b0bc1e6df8ab48de284e3457d39a49b995` loads `tests/test_files/input.stellaris` and `tests/test_files/coils.stellaris`, then separately constructs and optimizes alternative coils. The boundary is described as available on request. Neither required input file was acquired. The associated Zenodo archive remains an unresolved lead. [Focused follow-up](evidence/external-followup.md).

[INTERPRETATION] The exact input names make further acquisition concrete. Public software and an optimization script are not themselves the original geometry. An optimized alternative must not silently replace the published baseline. The investigation cannot conclude that there is no public geometry from an uninspected archive or a filename search.

## F-018 — Qualification stops at a real data dependency

[OBSERVATION] The acquired material does not establish finite-pack placement, the precise vacuum/finite-pressure axis convention, a matching reference field map or a validated pack-size response. One newer paper was rejected by the source-registry hold-out screen; that acquisition failure is retained separately from scientific evidence. No rejected paper was adopted or cropped around the rejection. [Search records](evidence/external-inventory.md), [follow-up](evidence/external-followup.md), [capability contract](capability-contract.md).

[INTERPRETATION] The current approximation remains unqualified. The required next inputs are identifiable; inventing a geometry or fitted coefficients would not close this gap. The scope of completed work is the support assessment, not a repaired field model. The [data-request draft](data-request-draft.md) has not been sent.

## Citation correction

[OBSERVATION] Independent review identified the coil-method section in Lion 2021 as §3.7, not §3.5 as stated in the earlier field-audit prose. The equation identity, inspected Eq. 39 image and substantive findings are unchanged. The new contract uses the correct section; historical audit bytes are preserved. [Independent review](evidence/review.md).
