# Run-goal prompt: fuel inventory and startup requirement

Use $run-goal to close the stellarator model’s fuel-inventory and startup gap.

Work in `/home/reid/1cfe/fusion-tea`. Read project instructions, the Codex adapter and runtime setup, then the run-goal skill and `work/orchestration/GOAL_RUNBOOK.md`.

## Goal

Use the slug `fuel-inventory-and-startup`.

Question: Can we calculate the tritium held throughout the fuel system, the stock needed to start operation, and the processing throughput from explicit operating and fuel-system assumptions?

The purpose is to meet the existing R10.P2 rubric target before the ARIES comparison. I authorize research, model implementation, package generation, targeted studies and independent review needed for this goal. Ground the goal from this prompt and proceed through the necessary rounds. Ask only when a material scientific or scope decision requires my judgment.

## Starting evidence

- `.project/active/demo-depth-rubric/rubric.md`, revision `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`.
- `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and its companion `.cells.json`.
- `work/orchestration/goals/plant-closure/` and its fuel-cycle research and implementation references.
- `work/orchestration/goals/pre-reveal-feasible-neighborhood/` and its linked study.
- Current fuel-flow, recovery, required-breeding and maintenance-calendar implementations, located through those records.

The September 18 assessment grades fuel physics P1 against a P2 target. Burn, injection, exhaust and annual fuel flows already have calculations. Startup stock and operating inventory are missing. More throughput calculations alone do not meet the full target. Confirm current implementation and any subsequent changes before planning work.

The exact target is: “Tritium inventory, startup requirement, and processing throughput forward-computed, verified.” Inventory means an amount of fuel held in equipment or storage; throughput means an amount processed per unit time. Keep those quantities distinct.

## Required result

1. Define the fuel-system boundary and streams. Identify fuel injection, plasma burn, exhaust, recovery, processing, storage and any represented blanket extraction. Distinguish tritium from total hydrogen-isotope flow and other species where relevant. Trace existing calculations before adding new ones.

2. Establish consistent fuel accounting. Define burn fraction, recycling, recovery efficiency, permanent loss, retention, decay and reserve assumptions. Specify which stream each fraction applies to. A quantity must not be counted both as circulating stock and as permanently consumed fuel. Report unresolved interpretation of existing assumptions.

3. Calculate operating inventory. Derive fuel held in each represented stage from justified residence times, working volumes, process hold-up or other supported physical relationships. Residence time means how long material remains in a stage. Identify minimum operating stock and any separately assumed reserve. Do not substitute an unexplained total inventory figure for the calculation.

4. Calculate startup requirements. Define the startup condition and account for filling the system, delays before recycled or bred fuel becomes available, early consumption and any declared reserve. Distinguish an initial external supply from recurring makeup fuel. Avoid counting the same system fill or reserve twice. State the level of startup timing represented; a simple verified model is preferable to unsupported transient detail.

5. Calculate processing throughput consistently with the inventories and operating point. Distinguish peak/operating flow from annual totals and calendar averages. Annual availability must not incorrectly reduce equipment’s required running capacity. Use the existing maintenance calendar where appropriate and explain treatment of shutdown inventory and decay.

6. Integrate these quantities into the model and executable package. Expose named outputs with units and definitions for the fuel-processing cost goal. Demonstrate response to supported changes in fusion power, burn fraction, recovery, residence times and reserves. Preserve the existing required-breeding calculation unless a justified correction is separately recorded.

7. Verify conservation, units, numerical limits and representative operating/startup cases. Use independent hand calculations or reference cases, not just a second copy of the implementation. Check physically meaningful limiting cases and invalid inputs. Report existing and new regression failures separately.

8. Run a focused study showing inventory, startup stock, processing demand and losses across justified assumptions. Identify the main drivers and whether source uncertainty prevents a useful estimate. A computed inventory is not proof that external tritium supply is available or that the plant breeds enough fuel.

9. Obtain a fresh independent R10.P grade against the unchanged rubric. Success requires all three outputs—inventory, startup requirement and throughput—to be calculated and verified. P2 does not require a complete self-sufficient fuel-cycle design.

## How to proceed

Start by drawing a simple fuel-flow and storage diagram and checking existing equations against it. Research admissible internal sources first; use native research and source-registration procedures for additional sources. Have a fresh reviewer check stream definitions, loss semantics, inventory/startup accounting and validation before substantial implementation.

Coordinate with `computed-tritium-breeding` and `throughput-based-fuel-processing-costs` if those goals exist. Breeding owns achieved tritium production; this goal owns inventory/startup and its throughput interface. Agree on shared equations and file ownership. A stated breeding scenario may be used for a bounded inventory calculation, but must not be presented as a prediction of adequate breeding.

Use native modeling, integration and study workflows. Record decisions and progress in the goal trail. Use `.codex-test/run` for Python and modeling commands. Preserve unrelated work.

## Limits and reserved decisions

- Keep ARIES sealed and follow `knowledge/holdout/aries-cs/PROTOCOL.md`. Do not read barred material or the excluded `.project/concepts/stellarator-mbse-demo.md`.
- Preserve the published r2 archive and historical results. Identify new model versions and studies separately.
- Do not lower rubric requirements or adjust recovery, losses or reserves merely to obtain self-sufficiency or a small startup stock.
- Do not expand this into closing calculated breeding, fuel-processing capital costs or the P3 full self-sufficiency target. Include only dependencies needed to make P2 quantities coherent.
- Material changes to existing loss/recovery interpretations must be surfaced with evidence and consequences before dependent conclusions proceed.
- Reveal, replacement of the frozen comparison, major scope or plant-concept changes and formal goal closure remain my decisions. No merge or push.

If P2 cannot be supported, identify the missing process/residence-time evidence, approaches investigated and concrete next step. A documented blocker is not closure of the gap.

## Deliverables

Produce native goal records, the fuel-flow/storage diagram, source and assumption register, verified calculations and study, an explicit throughput interface for costing, independent reviews and a fresh R10.P grade. Explain how much fuel is held, how much is needed at startup, what determines processing capacity, whether P2 is met and what remains uncertain.

Write for an engineer without project background. Define terms, use plain headings and show actual results and gaps.
