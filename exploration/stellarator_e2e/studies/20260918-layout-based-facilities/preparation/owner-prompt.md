# Run-goal prompt: facilities sized from the plant layout

Use $run-goal to close the stellarator model’s facilities gap.

Work in `/home/reid/1cfe/fusion-tea`. Read project instructions, the Codex adapter and runtime setup, then the run-goal skill and `work/orchestration/GOAL_RUNBOOK.md`.

## Goal

Use the slug `layout-based-facilities`.

Question: Can we derive the size and cost of plant buildings and maintenance facilities from the equipment they contain and the maintenance work they must support?

The purpose is to meet the existing R9.S3 rubric target before the ARIES comparison. I authorize research, model implementation, package generation, targeted studies and independent review needed for this goal. Ground the goal from this prompt and proceed through the necessary rounds. Ask only when a material scientific or scope decision requires my judgment.

## Starting evidence

- `.project/active/demo-depth-rubric/rubric.md`, revision `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`.
- `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and its companion `.cells.json`.
- `work/orchestration/goals/plant-closure/`.
- `work/orchestration/goals/pre-reveal-feasible-neighborhood/` and its linked study.
- Current building, site, maintenance, component-replacement and cost-account implementations, located through the assessment’s references.

The September 18 assessment grades facilities S2 against an S3 target. Existing building estimates follow grouped plant-power relationships. They do not derive building volumes, shielded maintenance capacity or component-handling space from a plant layout. Confirm the current implementation and check for work completed after that assessment before planning changes.

The exact target is: “Building set sized by volume/function from layout drivers, incl. hot cell and remote-handling facilities.” A hot cell is a shielded facility for working on radioactive components. Remote handling means moving and servicing those components without direct human access.

## Required result

1. Define the facilities and accounting boundaries. Identify existing building/site accounts and what they include. Separate building structures, shielding, installed services and handling equipment where the evidence supports doing so. Identify overlap with reactor shielding, cooling equipment, maintenance costs and decommissioning. State which existing estimates will be replaced and which missing costs will be added.

2. Establish an explicit conceptual layout. Derive facility requirements from equipment dimensions, component removal envelopes, access paths, assembly and servicing space, and justified separation or clearance requirements. Identify which dimensions are calculated, source-supported or assumed. A parameterized layout is acceptable; unsupported geometric precision is not.

3. Calculate maintenance-facility capacity. Use component sizes, replacement quantities and schedules to estimate receipt, storage, processing and handling requirements. State assumptions for processing times, simultaneous work and storage duration. Size the hot cell and handling spaces from these requirements. Do not invent logistics merely to reproduce a previous building cost.

4. Connect facility dimensions and functions to costs. Use applicable sourced estimates for building volume/area, shielding and facility services, with explicit purchased/installed boundaries. Preserve currency, price year, scope and uncertainty. Do not cost the same shielding, equipment or installation twice. Replacing a power multiplier with an equally arbitrary volume multiplier does not establish a source basis.

5. Integrate the calculations into the model and executable cost hierarchy. Changes in supported reactor dimensions, component envelopes or maintenance requirements must change facility size and cost. Preserve interfaces to the maintenance calendar; do not silently change plant availability. If a proposed layout cannot support the assumed replacement schedule, report that conflict rather than concealing it.

6. Verify dimensions, capacity, costs and account totals. Compare with admissible source examples where available, check implementation independently and run relevant regression checks. Distinguish a plausible conceptual layout from a qualified construction or maintenance design.

7. Run a focused study showing how facility sizes and costs respond to equipment size and maintenance demand. Use matched cases to distinguish adding missing scope from changing the design. Report plant-cost and electricity-cost consequences, important assumptions and infeasible layouts. Do not optimize on unsupported clearance or throughput assumptions.

8. Obtain a fresh independent R9.S grade against the unchanged rubric. The reviewer must inspect the actual layout-driven building set, hot-cell and remote-handling provisions, source basis and executed response. Meeting S3 does not require lowering cost.

## How to proceed

Start with an inventory of existing facilities accounts and the equipment and maintenance information available to size them. Research admissible internal sources first; use native research and source-registration procedures for additional sources. Choose the simplest defensible conceptual layout method. Have a fresh reviewer examine layout assumptions, maintenance-capacity logic and accounting boundaries before substantial implementation.

If the cooling-equipment goal or other work is active, agree on the equipment-envelope interface and file ownership. Use clearly identified provisional assumptions when upstream dimensions are unavailable. Do not overwrite another goal’s implementation or silently present placeholders as calculated dimensions.

Use native modeling, integration and study workflows. Record decisions and progress in the goal trail. Use `.codex-test/run` for Python and modeling commands. Preserve unrelated work.

## Limits and reserved decisions

- Keep ARIES sealed and follow `knowledge/holdout/aries-cs/PROTOCOL.md`. Do not read barred material or the excluded `.project/concepts/stellarator-mbse-demo.md`.
- Preserve the published r2 archive and historical results. Identify new model versions and studies separately.
- Keep the existing rubric and physical requirements. Do not reduce maintenance needs or remove facility functions to obtain a passing grade.
- This goal is conceptual facility sizing and costing, not a licensed site design, detailed seismic analysis or a complete remote-handling machine design. Include only necessary interfaces to other subsystems.
- Reveal, replacement of the frozen comparison, major scope or plant-concept changes and formal goal closure remain my decisions. No merge or push.

If S3 cannot be supported, identify the missing layout or maintenance evidence, approaches investigated and concrete next step. A documented blocker is not closure of the gap.

## Deliverables

Produce native goal records, a facility/account boundary map, conceptual layout and sizing evidence, model/study results, independent reviews and a fresh R9.S grade. Explain what determines each facility’s size, what is assumed, what costs are included, what changed in total plant cost, whether S3 is met and what remains unresolved.

Write for an engineer without project background. Define terms, use plain headings and show actual results and gaps.
