# Owner request — 2026-09-17

The following task text is copied from the owner's initiating request. It carries owner authority, not agent scientific recommendations.

Ground and pursue a new goal: reconcile the Stellaris reference plasma power balance and explain the difference between published ignition and the model’s required auxiliary heating.

## Owner intent

Complete one final, tightly bounded scientific reconciliation before selecting a new pre-reveal comparison freeze. We want to recover the published plasma result through justified modeling where possible, or quantify and explain the remaining discrepancy. Do not force ignition or a feasible plant.

## The problem

The completed Stellaris reference reconciliation found that exact published profile inputs reduce modeled auxiliary heating and divertor heat, but do not reproduce the paper’s Point-A ignition.

The Table 5 plasma-conditioned case computes approximately:

- Fusion power: 2,603.4 MW versus published 2,700 MW.
- Stored energy: 513.0 MJ versus published 504.65 MJ.
- Confinement time: 1.5774 s versus published 1.46 s.
- Required operating auxiliary heating: 44.0038 MW.

These are potentially consequential differences in a balance between large terms. Determine which equations, definitions, normalizations and assumptions account for the auxiliary-heating residual. First confirm that the cited source quantities describe the same operating point and use compatible power-balance conventions.

## Starting context

- work/orchestration/goals/stellaris-reference-reconciliation/answer.md
- Its reconciliation table, original-page source review, study and final review.
- work/orchestration/goals/divertor-peak-heat-load/answer.md
- Relevant operating-point-closure, stored-energy-basis, burn-control and plasma-profile work.
- Current fusion, alpha heating, stored-energy, confinement, radiation, sustainment and divertor-ledger calculations.
- .project/active/aries-comparison-preparation/package/readiness.md
- The existing frozen comparison package and input-selection rules.

Read current project instructions and the quarantine protocol before source work. Use clean original sources and independently admitted evidence. Respect the recorded mixed-source-note exclusion and coordinator-handoff restrictions. Do not open the excluded note or recover its contents through history or summaries.

## The question

Can the model reproduce the published Stellaris ignition balance using a coherent source-defined operating point? If not, how much of the discrepancy is attributable to identifiable differences, and what remains unexplained?

## Phase 1 — reconstruct the source balance

Identify the exact source equations, definitions and operating point underlying the ignition claim. Verify original pages, tables and figures.

Establish whether the published fusion power, stored energy, confinement time, radiation and heating values are:

- Inputs or independently calculated outputs.
- From the same point, profile convention and configuration.
- Rounded table values or quantities from a separate calculation.
- Sufficient to reconstruct the claimed balance.

Explicitly distinguish:

- Total fusion power and alpha-particle power.
- Alpha power retained as plasma heating.
- Electron and ion thermal stored energy and their profile/species conventions.
- Absorbed plasma heating versus installed or electrical auxiliary power.
- Radiation channels and the boundary across which each leaves.
- Transport loss, confinement power and any subtraction already included in the confinement convention.
- Ignition, external-heating demand and any signed burn-control diagnostic.

Do not assume that P_loss = W/tau and a separate radiation term can be combined without checking the source’s definitions. Avoid double counting radiation or alpha losses.

If the publication does not supply enough information for a closed reconstruction, identify the missing terms precisely.

## Phase 2 — construct a term-by-term comparison

Write the source balance and model balance explicitly, with units and sign conventions. Build a table for each term showing:

- Physical meaning and control-volume boundary.
- Source equation/value and original evidence.
- Current model equation/value and producer.
- Supplied versus predicted status.
- Known convention or input differences.
- Contribution to the auxiliary-heating discrepancy where attribution is possible.

Investigate at least:

- Fuel and temperature profile integration.
- Electron/ion/fuel/ash density definitions and quasi-neutrality.
- Fusion reactivity, dilution and retained alpha heating.
- Stored-energy species, temperature and volume conventions.
- Confinement scaling, units, normalization factors and heating-power definition.
- Bremsstrahlung, line and synchrotron radiation, including overlap or omission.
- Installed-to-coupled heating conversion and signed auxiliary-power treatment.

Inspect existing explanations before redoing research. Do not reopen established choices without evidence that they contribute to this discrepancy.

## Phase 3 — attribute the discrepancy

Use a small, deliberate set of diagnostic evaluations:

1. Reproduce the entering forward reference.
2. Reproduce the exact-profile and Table 5-conditioned cases.
3. Substitute compatible source terms individually or in physically necessary groups to isolate the residual.
4. Evaluate the fully source-conditioned balance only where its terms are mutually compatible.

Keep these diagnostics separate from forward predictions. A supplied source value earns no independent prediction credit.

Report interactions and order dependence. Do not imply that a list of isolated changes sums exactly to the total discrepancy unless demonstrated. Where exact additive attribution is unavailable, retain an explicit interaction/residual term.

Use uncertainty or rounding bounds when supported by the source. Do not choose a tolerance merely because it encloses the discrepancy. Distinguish numerical precision from source/model uncertainty.

## Phase 4 — correct only what is justified

Classify each discrepancy before implementation:

- Transcription, units or binding error.
- Inconsistent physical definition or double counting.
- Different source case or boundary.
- Deliberate alternative assumption.
- Reduced-model approximation.
- Missing source information.

Implement bounded corrections supported by evidence and independent review. Preserve historical results and explain every reference change.

Do not tune confinement multipliers, profile exponents, alpha retention, radiation fractions or other coefficients to obtain zero auxiliary demand. Do not silently replace a forward equation with a held published output.

Preserve signed power-balance diagnostics. If the reconstruction exposes that the existing sustainment or burn-hold predicate misinterprets ignition or negative auxiliary demand, review that semantic issue explicitly before changing it. No predicate may be removed or relaxed simply to recover a pass.

## Success criteria

- The source ignition claim and the current model balance have explicit, compatible definitions—or their incompatibility is demonstrated.
- The approximately 44 MW auxiliary-heating discrepancy is decomposed as far as the evidence permits.
- Known contributions, interactions, rounding uncertainty and unexplained residual are separately reported.
- Any corrected reference result follows from justified equations or inputs, not calibration to pass.
- Source-conditioned reproduction and integrated forward prediction remain distinct.
- Changed calculations agree across the native model, generated package and independent oracle.
- A few targeted off-reference checks verify that corrections behave coherently beyond the anchor.
- Downstream effects on divertor power, sustainment, thermal/electrical balance, LCOE and predicate verdicts are reported where affected.
- Independent review checks source fidelity, accounting boundaries, numerical attribution and the final interpretation.
- The final answer states whether ignition is reproduced, whether its deviation is adequately explained, or which specific missing evidence prevents resolution.

## Scope

This is a plasma power-balance reconciliation, not another feasible-region search or a full Stellaris redesign.

Keep pack/casing geometry, local conductor field-angle qualification, coolant-system redesign, manufacturing completeness and new divertor transport models outside scope. Their existing failures and applicability limits remain visible. Recovering plasma ignition would not establish whole-plant feasibility.

Use a bounded evaluation plan with expected responses and stopping rules before expensive execution. Reuse existing studies and source inspections. Do not add a general solver, performance surface or new subsystem unless it is essential to resolving a demonstrated discrepancy.

## Comparison freeze and ARIES boundary

Preserve the existing comparison archive unchanged. Do not reveal ARIES, seek equivalent holdout information elsewhere, or use reference-specific knowledge to select assumptions.

At completion, recommend the plasma profile/geometry convention and execution mode for a replacement pre-reveal freeze, with evidence and remaining limitations. Identify exactly which mappings, applicability records, tests and frozen artifacts need updating.

Do not silently choose the mode that makes a future comparison look best. Any source-conditioned mode must retain its supplied-input classification. Do not claim that the previous freeze represents corrected model behavior.

## Execution

Ground the goal and use the native modeling, integration, study and independent-review workflows at an appropriate scale.

Continue autonomously until the bounded reconciliation is implemented where justified, verified, independently reviewed and answered. Research missing evidence when it can materially resolve the question; otherwise use engineering judgment and record assumptions with their provenance. Do not stop for routine decisions or expand the scope indefinitely.

A quantified, well-supported unresolved residual is an acceptable outcome. A tuned ignition point is not.

Do not merge, push or reveal the holdout.
