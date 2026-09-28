# Learnings: Matched steam and helium Brayton component alternatives

The first three interpretations preserve the accepted round-1 partial reading. Round-2 entries update that reading after the authorized repair and verified replay; they do not alter the original failed evidence.

## L-001 — Model-owned controls preserve chosen design inputs

[AGENT] Accepted at round 1 final assurance. The reviewed assembly keeps source heat, compressor ratios and equipment offers as chosen inputs. Existing bypass controls calculate operating splits and retain deficient transfer; the finite cooler computes required water flow under purchased ratings. This establishes the reviewed role pattern, not scientific qualification of the imposed hydraulics. Evidence: fourth design review, implementation review and WI-096 at `29dcb5d8`.

## L-002 — Local convergence does not guarantee downstream accuracy

[AGENT] Accepted at round 1 final assurance. In independently diagnosed case c0206, a small water temperature rise amplifies cooler outlet error into flow/pump error beyond the scalar verification requirement, despite meeting the local UA residual stopping rule. Development verification and integration PASS did not establish accuracy over the wider study. Six cases fail numerical verification in total; this diagnosis does not establish a common cause for all six. Evidence: `evidence/verification-failure-review.md`, the sealed blocked study at `49c20e69`, and its cause-attribution addendum.

## L-003 — Connecting-equipment choices affect the diagnostic comparison

[AGENT] Accepted at round 1 final assurance as an unreleased diagnostic interpretation. Selecting steam exchanger/pump offers from the declared catalog reduces lower-duty cost per net MWh relative to holding all 14 circuits. The turbine offer stays fixed, so this does not establish equal optimization. Native nominal differences and price sensitivities remain conditional; failed numerical verification prevents releasing the economic comparison. Evidence: `evidence/matched-results-draft.md`, case-linked plot data and final assurance review.

## L-004 — The six failures had distinct numerical paths

[AGENT] Accepted by independent numerical-repair review. Four cases were sensitive to cooler root accuracy; two shared heater-network root error with a smaller bypass-solver contribution. Continuing the three existing brackets to adjacent floating-point endpoints resolved the demonstrated early stops without changing equations, equipment, variable roles, oracle or tolerances. All 15 focused assembled cases, nine high-precision local checks and the complete 498-case study pass. This demonstrates accuracy over the recorded inputs, not arbitrary near-zero outputs outside them. Evidence: `evidence/numerical-repair-review.md`, WI-096 numerical-repair report, repaired study verification and replay comparison.

## L-005 — The verified comparison remains conditional on offers and coverage

[AGENT] Accepted at the initial independent economic review for round 2; final seal assurance follows in the same review. The original selected anchors remain exact minima within their tested passing catalogs. Selecting steam connecting equipment materially lowers its lower-duty cost; its nominal advantage at 2500/2800 MW is inside the 5 USD/net MWh materiality band. The 3000 MW nominal Brayton advantage exceeds that band but quote scenarios reverse it. Only 14 of 375 gas offers pass all checks. Cooler-root/property exclusions and overlapping equipment/coupling failures limit that tested catalog; all 464 individual upper-root exclusions hit the 60°C property ceiling. Numerical repair resolves the prior release block without qualifying quotations, hydraulics, machine maps or equal optimization. Evidence: `evidence/verified-comparison/report.md`, exact plot data and `evidence/repaired-results-review.md`.
