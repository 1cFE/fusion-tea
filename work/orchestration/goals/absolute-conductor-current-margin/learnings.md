# Learnings: Absolute conductor-current margin

Accepted findings are appended after independent coverage and round review.

## L-001 — An absolute-current check adds independent information

[AGENT; independently accepted 2026-09-15] Source-derived normalization gives reference critical current 29.65 kA against 50 kA operation under the default perpendicular/ideal-retention scenario. The selected field ceiling passes while current margin fails; a native counterexample shows the reverse. Retain both predicates. The reference-conductor estimate is distinct from set-average capacity and weakest-coil qualification. Evidence: `answer.md`, `evidence/final-review.md`, frozen study `e1f5516b`.

## L-002 — Orientation and retention determine conditional passes

[AGENT; independently accepted 2026-09-15] All twelve entering nineteen-predicate passes fail under default current assumptions. Orientation factor 3 recovers twelve combined passes at the sixteen anchors; with three retention factors of 0.9, one remains. These assumed scalar gains do not supply a field-angle map, cable qualification or supplier price/performance relation. Evidence: frozen study `results/analysis.json@e1f5516b`, `answer.md`, `evidence/final-review.md`.

## L-003 — Physical lengths separate parallel capacity from series turns

[AGENT; independently accepted 2026-09-15] Tape/conductor length gives effective parallel tapes. Distinct coil-current and winding-pack-volume distribution factors convert the set estimate to the reference conductor. Fixed-ampere-turn repartition changes turn current and parallel capacity proportionally, leaving operating fraction and physical tape procurement unchanged. Apply the selected allowance once to independently normalized capacity; do not resize inventory merely to force a pass. Evidence: `evidence/interface-assessment.md`, native WI-062 design, frozen study turn-repartition cases and `evidence/final-review.md`.
