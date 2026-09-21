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
