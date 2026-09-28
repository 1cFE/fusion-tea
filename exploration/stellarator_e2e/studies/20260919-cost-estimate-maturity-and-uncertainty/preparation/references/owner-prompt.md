# Run-goal prompt: cost-estimate maturity and uncertainty

Use $run-goal to close the stellarator model’s integrated cost-estimate quality gap.

Work in `/home/reid/1cfe/fusion-tea`. Read project instructions, the Codex adapter and runtime setup, then the run-goal skill and `work/orchestration/GOAL_RUNBOOK.md`.

## Goal

Use the slug `cost-estimate-maturity-and-uncertainty`.

Question: Can we state how well developed the plant cost estimate is, expose the functional accounts where cost is concentrated, and quantify the uncertainty that the available evidence supports?

The purpose is to meet the existing R12.S3 rubric target before the ARIES comparison. I authorize research, model implementation, package generation, targeted studies and independent review needed for this goal. Ground the goal from this prompt and proceed through the necessary rounds. Ask only when a material scientific or scope decision requires my judgment.

## Starting evidence

- `.project/active/demo-depth-rubric/rubric.md`, revision `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`.
- `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and its companion `.cells.json`.
- `work/orchestration/goals/plant-closure/`.
- `work/orchestration/goals/magnet-manufacturing-cost-completeness/` and its account ledger.
- `work/orchestration/goals/pre-reveal-feasible-neighborhood/` and its linked study.
- Current cost-account hierarchy, financing, replacement and electricity-cost implementations, located through those records.

The September 18 assessment grades integrated cost-estimate quality S2 against an S3 target. Existing account arithmetic, financing, contingency and electricity costs are computed, but estimate maturity and uncertainty are not established. Verify current implementation and subsequent cost-model work before planning changes.

The exact target is: “3-digit functional subaccounts where cost concentrates, plus a stated estimate class and uncertainty treatment.” The project’s Cost Account Structure groups costs hierarchically; the target requires meaningful functional detail beneath broad totals where major costs occur. An uncertainty chart alone does not satisfy all parts of S3.

## Required result

1. Establish what estimate is being assessed. Identify the exact model/executable version, design inputs, cost scope, price-year/currency conventions, financing and maintenance assumptions. Keep estimates for different designs separate. Distinguish capital cost, operating cost, financing and levelized cost of electricity—the estimated lifetime cost per unit of electricity generated.

2. Review functional cost detail. Identify where costs concentrate, inspect existing subaccounts and determine whether they meet the rubric’s three-digit functional-account requirement. Preserve disjoint account boundaries and trace each significant amount to its producer. Add missing functional detail needed for this criterion, supported by engineering quantities and sources. Renaming a lump or splitting it into arbitrary percentages does not add estimate quality.

3. State estimate maturity using a justified method. Select an applicable estimate-class or maturity framework, explain its meaning and assess the actual degree of design definition and cost evidence. Do not equate software completion or a model-depth score with a mature engineering cost estimate. If different accounts have different maturity, expose that difference instead of assigning an unsupported uniform accuracy claim.

4. Build an uncertainty register for the significant costs and electricity-production assumptions. Distinguish uncertain source prices and scaling relationships from deliberate design choices, future scenarios, structural model limitations and entirely missing equipment. State the basis for each range or distribution. Do not apply an arbitrary common percentage or treat missing scope as a zero-cost random variable.

5. Define and implement a defensible uncertainty calculation. Choose bounded scenarios, probabilistic propagation or another justified method based on the evidence. Probability distributions are not mandatory, and unsupported probability claims are unacceptable. Preserve known shared drivers and dependencies; do not create artificial precision by treating related quantities as independent. If probabilities cannot be justified, report conditional ranges rather than confidence or percentile claims.

6. Treat financial conventions and contingency consistently. Identify overlap between existing contingency and modeled uncertainty. Explain whether the reported result includes contingency and prevent double counting. Keep raw monetary bases. If price-year normalization is justified for the new estimate, implement it transparently and separately from the unchanged frozen comparison rules. Disclose unresolved mixed-year inputs.

7. Propagate uncertainty to cost totals and electricity cost. Include relevant effects on the electricity denominator, such as availability, where supported. Preserve engineering failures and invalid calculations. Report their counts and causes rather than silently dropping them. If a distribution is conditional on passing designs, state the conditioning and population explicitly.

8. Verify the calculations and run a focused study. Check account sums, units, deterministic limiting cases and source-range reproduction. For sampling methods, retain seeds, sampling design and sufficient convergence evidence. Explain which assumptions dominate the result and which missing costs are outside the numerical range. A parameter sensitivity ranking is not, by itself, a quantified uncertainty estimate.

9. Obtain a fresh independent R12.S grade against the unchanged rubric. The reviewer must assess functional subaccounts, maturity classification and uncertainty treatment together. A contingency percentage, an unsupported estimate class or an unweighted sensitivity plot is not sufficient for S3.

## Dependencies and execution

Check whether cooling, facilities and fuel-processing cost goals are active or complete. Their results can materially change both cost concentration and uncertainty. Begin with account review and method selection, but do not present an assessment of an earlier cost model as the final assessment of their revised model.

Agree on account interfaces and file ownership. Integrate completed upstream changes before the final study and grade, or explicitly bound the deliverable to the current revision and identify the required follow-up. Do not duplicate equipment-cost implementations or overwrite other agents’ work.

Research admissible internal sources first; use native research and source-registration procedures for additional sources. Have a fresh reviewer check the maturity framework, range/distribution evidence, dependencies, missing-cost treatment and contingency policy before substantial implementation or sampling. Use native modeling, integration and study workflows, record progress in the goal trail and use `.codex-test/run` for Python and modeling commands.

## Limits and reserved decisions

- Keep ARIES sealed and follow `knowledge/holdout/aries-cs/PROTOCOL.md`. Do not read barred material or the excluded `.project/concepts/stellarator-mbse-demo.md`.
- Preserve the published r2 archive, its monetary-comparison rules and historical results. Identify new versions and studies separately.
- Keep rubric targets and physical requirements. Do not choose ranges or distributions to produce a reassuring price or feasible fraction.
- Target S3, not a fully engineered S4 project risk estimate. Include correlation or schedule assumptions only to the extent necessary for an honest chosen method, with limitations stated.
- Material revisions to accounting scope, financial policy or the plant concept must be surfaced before dependent conclusions proceed.
- Reveal, replacement of the frozen comparison, major scope changes and formal goal closure remain my decisions. No merge or push.

If the evidence cannot support S3, identify which required element is missing, what was investigated and the concrete next step. A numerical interval with an invented basis does not close the gap.

## Deliverables

Produce native goal records, a functional account map, estimate-maturity assessment, uncertainty register and method, reproducible study/results, independent reviews and a fresh R12.S grade. Explain what the estimate includes, how well it is supported, what its reported range means, its major drivers, what is excluded, whether S3 is met and what remains unresolved.

Write for an engineer without project background. Define terms, use plain headings and show actual results and gaps.
