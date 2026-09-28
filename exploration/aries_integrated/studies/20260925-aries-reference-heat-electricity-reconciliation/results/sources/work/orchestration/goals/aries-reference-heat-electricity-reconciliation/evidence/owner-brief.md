# Run-goal: explain the ARIES heat-to-electricity discrepancy

Use `$run-goal`. Proposed goal directory: `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/`.

## Objective and authority

[OWNER] We want to evaluate the published ARIES operating point as far as the available evidence permits and explain the important differences from our model. Previous goals established an integrated model under assumptions; that is not sufficient completion for this goal.

[AGENT, execution proposal adopted when this prompt is issued] Pursue this question: **when supplied the published ARIES fusion power, why does our model calculate approximately 796 MW net instead of the reported 1,000 MW, and why can it not remove all the heat?**

Treat my issuance of this prompt as authorization to ground and execute this goal, use retained ARIES sources, make justified ARIES-specific model changes, run diagnostic studies, delegate bounded work and independent review, and commit locally. Do not stop after a plan or a list of gaps. Routine engineering assumptions are allowed, but documenting an assumption does not explain a discrepancy: quantify its effect and support its range.

Preserve the original Stellaris model and its behavior, all frozen studies and historical comparison results. Preserve unrelated workspace changes. No push, merge, external messages or formal goal/item closure. Do not fit inputs to obtain 1,000 MW. Automatic equipment sizing is not authorized.

## Starting evidence

Read current project instructions and state, including AGENTS.md, CLAUDE.md, .agentic-mbse/codex.md, .project/codex-test-setup.md, modeling_project/REQUIREMENTS.md (especially MR-7), MODELING_PROCESS.md, the run-goal skill and GOAL_RUNBOOK.md. Use the prescribed `.codex-test/run` environment and actual native CLI interfaces.

The current integrated model and package are:

- `models/designs/aries_cs_integrated/plant.sysml`
- `exploration/aries_integrated/aries_integrated/`

Read these records selectively, following their exact identity/replay references:

- `work/orchestration/goals/aries-integrated-heat-electricity/answer.md`
- `work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md`
- `work/orchestration/goals/aries-integrated-equipment-costs/answer.md`
- `work/orchestration/goals/aries-integrated-lcoe/answer.md`
- `work/orchestration/goals/aries-integrated-design-studies/answer.md`

The historical thermal record reports:

| Case | Fusion MW | Accepted heat MW | Unmet heat MW | Gross electricity MW | Net electricity MW |
|---|---:|---:|---:|---:|---:|
| Assumed calculated-plasma baseline | 1835.451283 | 2240.389047 | 0 | 655.354927 | 423.106794 |
| Lyon source-conditioned, assumed equipment | 2436 | 2759.082152 | 158.725848 | 1028.658530 | 796.005288 |
| Literal Lyon source-input variant | 2436 | 2518.899476 | 398.908524 | 1039.669902 | 807.016660 |
| Published Lyon comparison | 2436 | Establish exact matching heat boundary | — | 1253 | 1000 |

Reproduce the relevant source-conditioned cases against the actual current package before adopting these as the new baseline. Verify effective-input differences; do not assume similarly named scenarios are otherwise identical. The 796-MW result describes the removable-heat subset of a thermally inadequate scenario. It is not a valid steady reference operating point. Thermal MW cannot be added directly to electrical MW.

ARIES source reading is authorized post-reveal. Prefer retained primary papers/page images and reviewed source records. The historical quarantine warning does not prohibit this authorized investigation; do not rewrite shared policy or bypass acquisition safeguards. Any additional acquisition follows the prescribed research route. The earlier hold-out result remains unchanged.

## Define the comparison before changing the model

Use the Lyon systems reference as the primary target unless primary evidence shows a different clearly identified source configuration is required. Distinguish it from Raffray's engineering case. Do not silently combine their different powers, temperatures or heat boundaries.

Create a concise reference-case contract specifying:

- Supplied fusion power and any other deliberately supplied source boundary values.
- Calculated outputs to compare: deposited/recovered heat by circuit, heat delivered to conversion, gross generation, individual auxiliary loads and net export.
- Exact source definitions, units, case/revision and confidence for each comparison.
- Every inherited approximation affecting those outputs and whether it is source-supported, independently justified, assumed or unresolved.

Directly check governing tables, figures and equations against primary page images. A published output supplied to isolate a downstream subsystem is legitimate, but earns no prediction credit for that supplied quantity. Keep source-conditioned and predictive paths separate.

This goal does not require reconstructing every ARIES input or qualifying every subsystem. It does require enough correspondence to interpret the heat/electricity differences. Any missing input that prevents that interpretation must have its influence investigated rather than merely be listed.

## Work to pursue

The following are investigation questions, not a predetermined sequence of run-goal tasks. Follow the evidence across bounded rounds.

1. **Establish the energy boundaries.** Reconcile fusion, neutron multiplication, charged-particle deposition, auxiliary heating, transferred heat and recovered pumping work. Explain source-case residuals without inserting balancing heat. Separate coolant deposition from heat reaching the power cycle, and distinguish thermal rejection from unremoved heat.
2. **Inspect the actual thermal arrangement.** Compare the implemented sequential exchangers with the published network. Identify whether component connections, branch allocation, recuperation or temperature assumptions cause the mismatch. Reuse applicable definitions; add alternatives only where their meaning is insufficient. An architecture correction is permitted and must be reviewed before implementation.
3. **Check equipment assumptions.** Review selected flows, conductances/areas, temperature limits, pressures, pressure losses and machine efficiencies. Replace arbitrary inherited values with independently supported values where available. Where an input is missing, determine a justified interval or alternative and measure its effect. Do not enlarge equipment solely until the run passes and call that reference reproduction. A deliberately resized alternative may be studied separately, with its purpose and changed hardware explicit.
4. **Explain conversion and auxiliaries separately.** Trace thermal input to turbine/compressor work, generator losses, gross electricity and net export. Reconcile definitions of gross/net output and which pumps/compressors are included. Check primary pumping, heating, cryogenics, fuel processing and other loads for omissions or duplicate subtraction.
5. **Integrate the supported corrections.** Retain the original failing case. Produce a separately named revised reference case and show exactly what changed and why. Recheck balances, temperatures, capacity margins, support status and power under the actual native graph.

Do not start by tuning the plasma profile. Published fusion power is deliberately supplied here to isolate downstream performance. Independent reproduction of 2436 MW from plasma inputs is a separate goal. Full magnet/conductor and breeding qualification are also outside this goal except where a missing relationship materially prevents the stated thermal comparison. Financial optimization is outside scope.

## Required discrepancy accounting

Maintain one evolving table:

**Source quantity → original model result → revised result → difference → identified cause → supporting evidence → remaining uncertainty.**

Before refinement studies, declare a materiality budget in MW for net electricity and for branch heat balance, based on source precision and the assessment's purpose. State its rationale in the goal record and obtain focused independent review. Do not choose or relax it afterward to accept the observed residual. Source ambiguity must remain explicit rather than disappear inside an inflated tolerance.

Use controlled cases to quantify causes. Change one justified assumption or model feature at a time where meaningful, then run the combined corrected case. Attribution in a nonlinear model can depend on change order: identify that order, measure consequential interactions and ensure the final ledger accounts for the combined difference. Do not simply add unrelated sensitivity effects.

Every material discrepancy must end in one of these states:

- Corrected through an evidence-supported input, definition or connection change, with before/after execution.
- Explained by a quantified difference in physical or accounting meaning.
- Bounded by an evidence-supported missing-input range, including its effect on net electricity and thermal adequacy.
- Unresolved because the necessary evidence or model is absent. This remains unfinished reconciliation; it does not become success merely because the assumption is documented.

## Studies and engineering discipline

Use `$run-study`, sealed identities and immutable native records. Start with targeted diagnostic comparisons rather than a broad optimization sweep. Needed evidence includes original-case replay, isolated cause tests, material assumption ranges and the combined revised case. One round may promote at most one package and commit at most one study; group compatible cases or use successive rounds.

I authorize explicitly labeled assumption-sensitivity studies without modeled constraint response. Record that absence before execution. This does not authorize optimizing those assumptions or treating an endpoint as an engineering optimum.

MR-7 remains binding. Flow, hardware geometry, ratings and purchase choices are supplied; operating states and demand are calculated. Any change in variable roles requires explicit reasoning and design review. No hidden resizing, clipping that conceals unmet demand, target-output substitution in a claimed prediction, or automatic passing of unsupported checks. Preserve engineering-failed, unsupported and undefined results separately. Keep derived outputs in the generated native graph; reporting scripts must not manufacture a replacement plant result.

Reuse machinery and valid earlier evidence. Add ARIES-specific assemblies or isolated generic alternatives without changing definitions consumed by Stellaris. Record entry preservation hashes and replay the applicable Stellaris baseline in isolation at delivery. Freeze prior ARIES evidence even if its live assembly evolves.

## Execution, review and limits

Ground the named goal using native templates and actual commit-pinned evidence before opening a round. Limits: two retries per failed task, two checkpoint revisions, six rounds, no additional wall-clock cap. Do not extend caps silently. A negative task result does not complete the positive goal; continue other useful work until the question is answered or a real gate/limit prevents progress.

Use continuing authors and fresh non-author reviews with bounded briefs. Parallelize independent source-boundary and implementation investigations where useful. Assign file ownership; workers are not alone and must preserve each other's edits. Integrate shared model/package changes sequentially. Review new source interpretations, equations and architecture before they compound; independently replay the consequential final behavior. Avoid duplicate reviews of unchanged evidence.

Keep goal trail/learnings, the reference-case contract and discrepancy table current. Commit meaningful implementation and study checkpoints. Preserve failed attempts and explain corrections plainly.

## Completion condition

The goal is answered only when the report can explain, numerically and by subsystem, why the revised source-conditioned case does or does not reproduce the reported heat balance, gross generation and net electricity within the predeclared materiality budget.

The 159-MW unmet-heat problem must be resolved by a supported correction, or traced and bounded as a specific discrepancy. A case with unremoved heat is not accepted as a steady operating reconstruction merely because it has finite electrical output. If a material discrepancy cannot be explained or bounded, report the goal unmet or partially answered, name the exact missing evidence and the useful next action. Do not substitute the successful 423-MW assumed baseline as completion.

Agreement with 1000 MW is neither guaranteed nor a tuning target. A well-supported disagreement is a valid scientific result; an unexplained difference is not a completed reconciliation.

Deliver `answer.md` with the source case definition, baseline and revised heat/electricity tables, quantitative discrepancy attribution, remaining uncertainty, engineering statuses, reuse/model changes, independent review, Stellaris preservation and exact replay instructions. Include a short plain-language explanation suitable for the write-up. Reserve formal goal/item closure for me.
