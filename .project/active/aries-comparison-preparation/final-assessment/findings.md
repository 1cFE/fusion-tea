# Final assessment findings log

This continues [F019–F021](../geometry-acquisition/findings.md). Findings are recorded as the checks finish. This is a post-reveal comparison of the retained selected design, not a fresh blind test or a reconstruction of every ARIES design choice.

## Work started

[OWNER] Authorized execution and regular commits. [AGENT] Structural and cost review run in parallel; the coordinator checks field-independent quantities and reporting. Original models, input selection, source evidence and numerical attempts are preserved. The final report will distinguish a matched function, comparable calculation, descriptive difference and unavailable comparison.

## F022 — Pack area agreement does not establish geometry agreement

[AGENT] Source inspection identifies ARIES coil dimensions as winding-pack dimensions; internal-sheet/insulation scope still needs correspondence. Model/reference nominal dimension ratios are 1.856 and 0.497, both within the old factor-of-three band. The dimension products differ by only about 8%, but the selected model is nearly square while the reference is elongated. The model's own radial clearance remains −0.120 m. This is a selected-design comparison, not an independent geometry prediction. [Quantity review](quantities.md).

## F023 — Field-independent does not mean reference-comparable

[AGENT] All 35 field-independent calculated quantity rows were checked. Geometry definitions, material inventories, selected capacities or reference aggregation prevent independent numerical validation with the inspected evidence. In particular, 55 MW of plant-plus-cryogenic power cannot be assigned entirely to the model's cryogenic electricity account. [Row dispositions and source checks](evidence/quantity-rows.json).

## F024 — Structural comparison now has explicit verdicts

[AGENT] The radial-order checklist passes at its stated qualitative level. The subsystem checklist fails because the selected plant lacks the separate PbLi heat-removal branch shown in the ARIES engineering design. Complete account coverage remains unresolved despite recognizable cost families. These verdicts are submitted for independent review. [Structural evidence and mapping](structure.md).

## F025 — Component prices can be compared descriptively, but not scored as accuracy passes

[AGENT] All 35 field-independent calculated cost rows are reviewed, including 21 source-value pairs checked against primary images. Eight nominal ratios are inside the original band, three below and ten above, with excluded C220107 among the eight. Different money years, technologies and account boundaries prevent scientific pass/fail. Values are now visible with individual reasons rather than a generic field blocker. [Cost review](costs.md).

## F026 — Selected purchases and source numbering affect apparent agreement

[AGENT] Turbine and heat-rejection amounts are supplied purchases; several other accounts price selected equipment classes. They do not validate achieved plant output. Source papers also number heat rejection and special materials differently, so an account-number-only join can compare the wrong equipment. The semantic crosswalk preserves each paper's actual meaning. [Frozen producer evidence](evidence/cost-frozen-excerpts.json), [crosswalk](structure.md).

## F027 — The original comparison can be concluded without another plant run

[AGENT] The reviewed evidence supports a structural failure from missing ARIES heat-removal correspondence, a qualitative radial-order pass, and unresolved full account equivalence. Numerical accuracy remains unestablished, with descriptive geometry and price differences preserved. The original full comparison therefore does not pass. The result does not require changing the field, selecting new equipment or discarding unavailable rows. [Integrated report](report.md), [all 276 rows](evidence/comparison-rows.csv).

## Completion and verification

[AGENT] Fresh independent review accepts the completed reporting scope with no material findings outstanding. Exact replay preserves all 276 original rows; all 52 frozen model files and 1,322 protected files remain unchanged. This is acceptance of the assessment's accuracy and completeness within its declared scope, not an engineering or numerical-comparison pass. [Review and pinned evidence](evidence/review.md). Checkpoints: plan 2b8341ce, structural/quantities 85c1b470, costs 5f8658b6; final reviewed reporting is committed separately.
