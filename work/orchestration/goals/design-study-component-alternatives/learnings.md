# Learnings: Matched steam and helium Brayton component alternatives

The following agent interpretations were accepted for faithful partial-result reporting after round 1 review. Numerical study verification remains failed.

## L-001 — Model-owned controls preserve chosen design inputs

[AGENT] Accepted at round 1 final assurance. The reviewed assembly keeps source heat, compressor ratios and equipment offers as chosen inputs. Existing bypass controls calculate operating splits and retain deficient transfer; the finite cooler computes required water flow under purchased ratings. This establishes the reviewed role pattern, not scientific qualification of the imposed hydraulics. Evidence: fourth design review, implementation review and WI-096 at `29dcb5d8`.

## L-002 — Local convergence does not guarantee downstream accuracy

[AGENT] Accepted at round 1 final assurance. In independently diagnosed case c0206, a small water temperature rise amplifies cooler outlet error into flow/pump error beyond the scalar verification requirement, despite meeting the local UA residual stopping rule. Development verification and integration PASS did not establish accuracy over the wider study. Six cases fail numerical verification in total; this diagnosis does not establish a common cause for all six. Evidence: `evidence/verification-failure-review.md`, the sealed blocked study at `49c20e69`, and its cause-attribution addendum.

## L-003 — Connecting-equipment choices affect the diagnostic comparison

[AGENT] Accepted at round 1 final assurance as an unreleased diagnostic interpretation. Selecting steam exchanger/pump offers from the declared catalog reduces lower-duty cost per net MWh relative to holding all 14 circuits. The turbine offer stays fixed, so this does not establish equal optimization. Native nominal differences and price sensitivities remain conditional; failed numerical verification prevents releasing the economic comparison. Evidence: `evidence/matched-results-draft.md`, case-linked plot data and final assurance review.
