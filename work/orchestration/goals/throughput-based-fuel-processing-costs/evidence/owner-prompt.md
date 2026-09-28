# Run-goal prompt: fuel-processing costs driven by throughput

Use $run-goal to close the stellarator model’s fuel-processing cost gap.

Work in `/home/reid/1cfe/fusion-tea`. Read project instructions, the Codex adapter and runtime setup, then the run-goal skill and `work/orchestration/GOAL_RUNBOOK.md`.

## Goal

Use the slug `throughput-based-fuel-processing-costs`.

Question: Can we make the cost of the fuel-processing plant follow its calculated processing demand, using applicable cost sources and explicit equipment boundaries?

The purpose is to meet the existing R10.S2 rubric target before the ARIES comparison. I authorize research, model implementation, package generation, targeted studies and independent review needed for this goal. Ground the goal from this prompt and proceed through the necessary rounds. Ask only when a material scientific or scope decision requires my judgment.

## Starting evidence

- `.project/active/demo-depth-rubric/rubric.md`, revision `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`.
- `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and its companion `.cells.json`.
- `work/orchestration/goals/plant-closure/` and its fuel-cycle implementation and cost references.
- `work/orchestration/goals/pre-reveal-feasible-neighborhood/` and its linked study.
- The `fuel-inventory-and-startup` goal, if created, and its declared throughput outputs.

The September 18 assessment grades fuel-processing costs S1 against an S2 target. Annual fuel purchases and an existing fuel-handling power-based estimate do not establish a processing-plant cost that responds to calculated throughput. Confirm current implementation and subsequent work before planning changes.

The exact target is: “Processing-plant cost follows computed throughput with source basis.” Throughput is the amount processed per unit time. S2 permits a justified aggregate cost relationship; it does not require S3 decomposition into a complete set of independently sized process equipment.

## Required result

1. Define the processing and accounting boundaries. Identify which functions are represented: for example, exhaust treatment, isotope separation, purification, storage/delivery and blanket-fuel extraction where applicable. Select functions from the actual fuel-system architecture, not from an assumed complete plant. Distinguish processing equipment from fuel purchases, startup fuel stock, vacuum pumping, fueling hardware, buildings and safety systems already costed elsewhere.

2. Establish the capacity-driving quantity for each cost relationship. Trace it to a verified fuel-flow calculation. Distinguish tritium mass, total isotope flow, total gas flow and process composition. Determine whether the source relationship depends on throughput, inventory, duty cycle or another quantity. Do not substitute one for another merely because both scale with plant power.

3. Obtain an applicable cost basis. Check process technology, feed/product composition, capacity range, pressure/temperature where relevant, redundancy, currency, price year and included equipment. Distinguish purchased from installed cost and capital from operating expenses. Retain raw source values and justify any scaling or conversion. Do not invent a universal scaling exponent or assume a small experimental facility scales directly to a power plant.

4. Implement a cost model driven by computed throughput. A source-supported aggregate process-plant estimate is acceptable for S2 if its scope and applicability are clear. Preserve necessary capacity margins as explicit assumptions. Costs must respond to fuel-processing demand rather than an unrelated plant-power proxy.

5. Integrate the estimate into plant costs and electricity cost. Explicitly replace overlapping existing estimates. Separate recurring fuel purchases and startup stock from processing-plant capital. Include operating, replacement or installation terms only where their scope and source basis justify them; disclose missing terms rather than fabricating completeness. Verify that no existing cost has been counted twice.

6. Verify the throughput-to-cost chain. Reproduce source reference cases, check scaling limits, units, capacity conventions and cost-account totals. Confirm that annual availability does not incorrectly reduce required running capacity. Verify generated execution and run relevant regression checks, distinguishing existing failures from new ones.

7. Run a focused study. Show how supported changes in burn fraction, recovery, operating power or other actual drivers affect processing demand, capital cost and electricity cost. Separate throughput effects from source-price uncertainty and process assumptions. Preserve failed plant cases and do not interpret a low process cost as proof of breeding self-sufficiency.

8. Obtain a fresh independent R10.S grade against the unchanged rubric. The reviewer must trace the cost from actual computed throughput through an applicable source relationship into the plant total. A new account name or annual fuel bill is not sufficient evidence for S2.

## Dependencies and execution

Start by checking whether the existing fuel calculations already provide the required verified throughput. The inventory/startup goal may add or correct that interface, but not all costing research has to wait for it. Research and cost-boundary work can proceed independently. Final integration and the grade must identify the exact producer and tested version of every consumed quantity.

If `fuel-inventory-and-startup` is active, agree on quantity definitions, operating versus annual units, file ownership and a stable interface. Do not duplicate its mass-balance calculation inside the cost model or quietly adopt a conflicting loss interpretation. Record a real dependency if the needed quantity is unavailable.

Research admissible internal sources first; use native research and source-registration procedures for additional sources. Have a fresh reviewer check source applicability, capacity mapping and accounting boundaries before substantial implementation. Use native modeling, integration and study workflows, record progress in the goal trail and use `.codex-test/run` for Python and modeling commands. Preserve unrelated work.

## Limits and reserved decisions

- Keep ARIES sealed and follow `knowledge/holdout/aries-cs/PROTOCOL.md`. Do not read barred material or the excluded `.project/concepts/stellarator-mbse-demo.md`.
- Preserve the published r2 archive and historical results. Identify new model versions and studies separately.
- Keep the existing rubric and fuel-system requirements. Do not simplify the required process or change fuel-loss assumptions to obtain a favorable cost.
- Do not expand S2 into a detailed process-plant design, the breeding gap, facilities sizing or full fuel self-sufficiency. Include only necessary interfaces.
- Reveal, replacement of the frozen comparison, major scope or process-technology changes and formal goal closure remain my decisions. No merge or push.

If no admissible source supports the required process/capacity, report the missing evidence, methods investigated and concrete next step. An unsupported cost number or documented blocker does not close the gap.

## Deliverables

Produce native goal records, the process/account boundary map, cost-source applicability assessment, integrated model/study evidence, independent reviews and a fresh R10.S grade. Explain what processing is included, what determines required capacity, how that capacity determines cost, what was replaced, effects on plant/electricity cost, whether S2 is met and what remains unpriced.

Write for an engineer without project background. Define terms, use plain headings and show actual results and gaps.
