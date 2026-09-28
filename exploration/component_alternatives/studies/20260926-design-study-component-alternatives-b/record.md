# Selected steam offer versus tested Brayton offers — numerical repair replay

**Sealed, numerically verified conditional comparison.** Full numerical verification and independent economic review pass. The repaired executable completed the unchanged 498-point list. This record reports conditional matched conversion results and preserves failed offers. Formal closure remains owner-held.

## 1. Study header

- **Study id:** `20260926-design-study-component-alternatives-b`
- **Package:** `component_alternatives_tea`
- **Date executed:** 2026-09-26
- **Executor:** Goal coordinator `/root`; record author `/root/brayton_audit`
- **Mode:** execute, bounded numerical-repair replay
- **Arms:** `arm-matched-offers`

## 2. Intake

[OWNER-VERBATIM] Original brief, retained in full below.

> # Run-goal prompt: a matched comparison of alternative conversion components
>
> Goal slug: design-study-component-alternatives
>
> ## The engineering question
>
> For the same supported reactor heat source, how do the modeled steam and helium Brayton conversion options differ in net electricity, required equipment and conditional LCOE? Can the alternatives developed around different plants support a meaningful choice between components?
>
> This is a categorical component/subsystem choice. It is not a comparison between the complete published Stellaris and ARIES plants, whose many simultaneous differences prevent attribution.
>
> ## Class-specific strategy
>
> - First inspect the compatibility map and identify a common, physically supportable heat-source boundary. Candidate starting points are the Stellaris helium source used in C-1, or the ARIES divertor helium source identified as C-3-compatible with the steam path. Do not assume their interfaces are interchangeable merely because both carry heat in MW.
> - Prefer the largest useful common boundary that can be evaluated with existing definitions and modest justified integration work. If only an isolated source loop supports a fair comparison, state that scope and calculate the cost per net MWh of that conversion subsystem. Do not label an isolated subsystem metric whole-plant LCOE. A full-plant comparison must include the remaining heat paths and common plant accounts explicitly.
> - Fix source heat duty, temperatures, return requirements and upstream costs consistently. Specify whether each alternative includes its required intermediate exchanger, salt loop, cooling system and machinery. Necessary connecting equipment belongs inside the compared conversion subsystem and must be costed. Do not force one topology onto incompatible technology or grant one branch free heat transfer.
> - Build both branches using the applicable existing definitions. Audit fixed steam temperature/rated-condition assumptions and the Brayton source matching. Do not alter guards or use a lumped efficiency fit to impersonate a missing physical component. Reuse the existing alternatives where supported; record any required new relationship as an extension, not demonstrated unchanged reuse.
> - Supply explicit equipment inventories and cost bases for both choices. Give both branches the same opportunity for a bounded operating-parameter study and explicit offered-equipment selections. Do not compare one tuned branch with an arbitrarily poor default of the other. Report common-design and branch-specific choices separately.
> - Keep reactor/fuel assumptions and financial conventions matched. Resolve relevant auxiliary and heating accounting before computing net electricity. Explain differences through temperature matching, conversion performance, internal power consumption and purchased equipment.
> - Evaluate a small set of common source operating points within the overlap of supported ranges, not just one favorable point. Test whether the relative result survives uncertainty in prices and component efficiencies. Unsupported extrapolation is not evidence of an economic crossover.
> - If steam/Brayton cannot support a fair comparison within this goal's budget, report the specific missing interface or cost requirement. You may evaluate another genuine physical component/material alternative only if the evidence shows it answers the owner's expanded-library question. Comparing two price correlations for the same equipment or two numerical settings does not satisfy this class.
>
> ## Figures and result required
>
> Show the two assemblies and their common comparison boundary in a simple diagram. Provide matched net-output and cost-contribution comparisons and a delta-LCOE or subsystem cost-per-MWh plot over the supported common source range, with uncertainty and failed cases visible. Answer which option performs better under which assumptions, or explain why the evidence supports no recommendation. Pure execution/reuse evidence is not sufficient completion.
>
> ## Purpose and authority
>
> Use the run-goal workflow. The owner requests a study that demonstrates how the expanded Stellaris/ARIES component library helps evaluate engineering choices. We need an understandable design question, a named starting configuration, a credible comparison and an explained result. A parameter sweep that merely produces numbers is insufficient.
>
> The question is not how closely we can reproduce ARIES. It is what alternative design choices the expanded library lets us evaluate, what changes in performance and LCOE, and why. Do not make an arbitrary fixed tritium-supply threshold the central result. Do not manufacture novelty, a ranking reversal or a positive result. An explained absence of advantage, a bounded applicability limit or an inadequate-model result is legitimate; report unmet completion criteria honestly.
>
> Read AGENTS.md, CLAUDE.md, .agentic-mbse/codex.md, .project/codex-test-setup.md, the run-goal skill and native runbook. Use native goal templates and the prescribed runtime. Read MR-7 and follow the modeling workflow for changes. The slug below is supplied by this prompt; use it without another naming confirmation. Preserve this prompt as the owner brief. Specific study strategies below are proposed starting approaches, not required findings.
>
> ## Grounding records
>
> - docs/write-up/sysml-codegen-model-evaluation.md, section 1.1: the distinction between parameters, component/material alternatives and architecture.
> - docs/write-up/aries-model-transfer-outline.md: the reader's question; editorial context, not authoritative numerical evidence.
> - work/orchestration/goals/design-space-combinations/{goal,trail,learnings,answer}.md and evidence/choice-inventory.md, compatibility-map.md.
> - The WI-093 combination-assemblies report and evidence; locate its current active/completed path through native tracking. Its cross-plant assemblies prove partial reuse, not full plant qualification.
> - work/orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md.
> - work/orchestration/goals/aries-reconciled-alternative-economics/answer.md.
> - exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/ and its verified results.
>
> Known issues to check when relevant: the steam path expects a salt-loop interface and has fixed temperature assumptions; the hybrid plasma assembly omits its own calculated heating requirement from the electrical balance; one peaked-profile case reports a negative sustainment requirement that was not interpreted; blanket source temperature is not fully coupled to duty and flow; pump-law assumptions can change conclusions; recuperator and cycle-side costs lack complete equipment support. These are specific prerequisites or limitations to resolve, not a mandate to repair every model.
>
> ## Common execution and comparison requirements
>
> 1. Ground a persistent goal contract and bounded round plan. Start by inspecting existing evidence, then run a small recorded screening study if needed. State the original design point in plain engineering terms: which components, selected equipment, operating settings, calculated outputs and inherited assumptions. Explain why it is a useful starting point. Do not introduce an unexplained 423 MW or 891 MW baseline.
> 2. Before the main study, write a comparison contract: independent choices, quantities held equal, calculated consequences, permitted equipment reselections, accounting boundary, failure conditions, scientific support and materiality/tolerances. Have the risky interface and comparison assumptions independently reviewed. Routine scope choices within this prompt do not require another owner approval.
> 3. Reuse existing equations and cost machinery. Small, justified interface/accounting repairs or additive alternatives are authorized through the modeling workflow and applicable independent review. An adapter may map units or names but must not conceal new physics. Retain the pre-repair replay and identify changed behavior. If a credible comparison requires a major new physical model, surface that dependency and report partial completion rather than substituting an unsupported calculation.
> 4. Preserve design choices: no silent equipment sizing, demand-derived purchases or automatic constraint satisfaction. If selecting alternative equipment, enumerate explicit offered ratings and prices before execution, account for them, and report that selection as a separate design decision. Performance changes requiring different hardware must carry its costs or be labeled unsupported performance sensitivities.
> 5. Track the complete relevant energy and cost boundaries, including pumps, compressors, external heating, generator losses, heat rejection, purchased equipment, replacements and operating expense. Do not count a load twice or leave it out to make branches comparable. Do not insert reference net electricity into a claimed prediction.
> 6. Use consistent currency, finance, lifetime, availability and fuel conventions across each matched comparison. Show capital, nonfuel operation, fuel and electricity-denominator contributions separately. Fuel supply remains conditional unless modeled and supported. Test whether reasonable fuel assumptions change a recommendation; do not equate absent breeding qualification with an established market-purchase scenario. If absolute LCOE is too assumption-dependent, provide paired delta-LCOE and cost contributions, with the absolute figures explicitly conditional.
> 7. Separate numerical execution, passing implemented engineering checks and scientific qualification. A case that cannot remove its heat or exceeds selected equipment is not an LCOE winner. Preserve failed cases; distinguish them in every plot and ranking. Missing checks must remain visible even if all existing checks pass.
> 8. Explain at least one decision relationship using matched cases and an energy/cost decomposition. Check it against consequential modeling assumptions. Do not search only for dramatic outcomes; retain the screened questions and explain why the selected one teaches something useful.
> 9. Use subagents for bounded source/interface/cost audits and fresh independent reviews, with explicit ownership and preservation instructions. Keep a findings log, failed attempts, a changed/reused inventory and replay commands. Commit coherent increments using explicit paths; never sweep the shared index into a goal commit. Preserve owner write-up edits and other agents' work.
> 10. Work in goal-owned study/model/package locations. Preserve the existing Stellaris and ARIES packages, historical studies and their behavior; create isolated variants where needed. These three study prompts may be run by different agents: coordinate shared changes rather than concurrently editing or repinning the same library or manifest. No push, merge, external messages or purchases. Respect source-access restrictions and the scope of existing exceptions.
>
> ## Deliverables and stopping conditions
>
> Produce answer.md, a complete candidate ledger, sealed study evidence, independent review and exact replay instructions. Include publication-ready SVG/PNG figures, their source data and a reproducible rendering script in the goal evidence directory. Do not edit the owner's article. Supply a short proposed passage explaining: starting design, changed decision, measured consequence, mechanism and practical limit. Every plotted point must trace to a case identity and its check status.
>
> Completion requires an executed and verified comparison that answers the class-specific question below, consistent performance/cost accounting, a causal explanation, and a sensitivity check on the assumptions that could change the conclusion. Running cases or demonstrating reusable interfaces alone does not complete an economic comparison. If the goal remains blocked by missing physics, incompatible interfaces or unsupported costs, name the exact gap and assess partial/unmet completion. Do not call it met because an illustrative plot exists.
>
> Use a maximum of four rounds, with retry limits from the runbook. Begin with a bounded screen, then select one primary question rather than collecting unrelated studies. Formal goal and work-item closure remain with the owner.

[OWNER-VERBATIM] Continuation and cap extension, retained in full below.

> # Owner direction: one additional design submission
>
> 2026-09-26. [OWNER-VERBATIM] The following message extends the cap for WI-096's next design submission only.
>
> > Authorize one additional design revision and its independent review. This extends the exhausted revision cap by one submission; it does not waive the modeling requirements or handwritten-solver limits.
> >
> > Before implementation:
> >
> > 1. Explain each required physical equality in plain engineering terms. Identify the independently chosen inputs, calculated operating states, and checks.
> >
> > 2. Move required coupled physical calculations into the model. Preserve MR-7: do not silently derive source power, pressure ratio or purchased equipment merely to make the branches match. Where a designer-selected combination is inconsistent, report the failure. If a controller or a change in variable roles is necessary, document the engineering rationale and obtain the applicable review.
> >
> > 3. State whether the proposed additions still fit the authorized bounded scope. The current work includes cooler, pumping and recuperator behavior as well as closure calculations; do not classify all of that as interface wiring.
> >
> > 4. Keep the comparison fair and accurately named: the selected steam offer versus tested Brayton offers at matched source conditions, using conversion-subsystem cost per net MWh. Do not claim equally optimized technologies or whole-plant LCOE.
> >
> > If the revised design passes the required review and remains within scope, continue autonomously through implementation, integration, the matched study and final review. Preserve the failed diagnostic cases and existing evidence.
> >
> > If it still fails review, or requires a major new physical model or a policy exception, stop with the exact unresolved requirement. Do not open another round to bypass the cap.
> >
> > Formal closure remains mine. Commit only your files; no push or merge.

[AGENT] The executable comparison will use the independently reviewed fourth design. Its chosen source powers, direct pressure-ratio grid and declared equipment offers define an engineered test window. Feasible points may support conditional comparisons; numerical execution alone does not establish equipment qualification. The selected steam offer and tested Brayton offers have different operating freedoms. Their metric is conversion-subsystem cost per net MWh.



[OWNER-VERBATIM] Bounded numerical-repair continuation:

> # Owner direction: bounded numerical repair
> 
> 2026-09-26. [OWNER-VERBATIM]
> 
> > Authorize one bounded numerical-repair continuation of this goal, including the necessary new executable and revalidation. Extend the applicable cap only for this repair; do not waive verification tolerances.
> >
> > 1. Isolate all six numerical failures. Do not attribute the unresolved bypass-flow and temperature-margin mismatches to the cooler without evidence.
> >
> > 2. Repair confirmed native numerical defects. Use convergence criteria or numerically stable formulations that control the required output accuracy, not merely a local residual. Preserve the independent oracle and existing tolerances.
> >
> > 3. Add focused regression checks for the demonstrated failures and nearby sensitive cases. Preserve the original failed executable, cases and diagnostics.
> >
> > 4. Re-execute and verify the complete matched study on the repaired identity. Update the rankings, sensitivity results and figures from that verified record.
> >
> > 5. Distinguish equipment failures from unsupported cooler-property ranges. State how these exclusions limit the comparison; do not expand the physical domain merely to obtain more passing candidates.
> >
> > Keep the current comparison scope and explicit equipment offers. No new technology branch or broad physics expansion. If a failure requires a substantive physical-model change, surface that dependency before proceeding.
> >
> > Obtain independent review of the repair and final economic conclusions. Formal closure remains mine. Commit only task files; no push or merge.

## 3. Objective and result

The native objectives are `component_alternatives__plant__steam_ledger__evaluate__cost_per_net_MWh` and `component_alternatives__plant__gas_ledger__evaluate__cost_per_net_MWh`, in USD2025 per net MWh. They include conversion equipment, required connecting equipment, included auxiliaries, rejection, service and replacements under matched source and financial assumptions. Source fuel, common upstream circulation and other plant accounts are excluded equally.

All 498 distinct points completed and pass numerical verification; 83 satisfy every implemented engineering predicate and 415 fail at least one. The selected steam offer produces more net electricity at all three matched source scenarios. Its larger capital and recurring costs offset that output advantage. Choosing among explicit connecting-equipment offers changes the comparison substantially; the fixed 14-circuit steam curve remains separate.

| Selected source heat MW | Selected steam connector | Steam net MW | Tested gas net MW | Fixed 14-circuit steam cost | Selected steam cost | Tested gas cost | Steam minus gas cost |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2500 | 10 circuits, 4 pumps/circuit, 225 kg/s design | 937.579 | 559.493 | 45.309 | 33.762 | 33.768 | -0.006 |
| 2800 | 11 circuits, 4 pumps/circuit, 225 kg/s design | 1060.283 | 518.099 | 40.065 | 32.406 | 36.466 | -4.060 |
| 3000 | 14 circuits, 3 pumps/circuit, 250 kg/s design | 1144.003 | 682.834 | 37.133 | 37.114 | 27.669 | +9.446 |

All costs in the table are conditional USD2025 per net MWh. The 2500 and 2800 MW gaps lie inside the predeclared 5 USD/net MWh materiality band; the 3000 MW nominal gas advantage exceeds it. The net-output differences exceed the separate 5 MW band. Tested branch quote scenarios reverse cost signs at every source point. Efficiency changes move the 3000 MW gap from about 4.007 to 13.104 USD/net MWh, crossing materiality without reversing its sign. Equal positive source-service PV charges favor the larger steam electricity denominator; about 1.831 BUSD of common added PV erases the 3000 MW nominal gap. These are sensitivity scenarios, not qualified fuel prices or procurement quotations.

`results/cases.json` and `.csv` retain native values, inputs and predicate identities. `results/replay-comparison.json` proves exact old/new input correspondence and zero predicate changes. The [verified comparison report](results/report/report.md), [exact plot data](results/report/plot-data.json) and [summary](results/report/matched-study-summary.json) provide energy/cost decompositions, case identities and native K/E correction frontiers. The [assembly boundary](results/report/reviewed-comparison-boundary.svg), [output comparison](results/report/matched-output.svg), [cost decomposition](results/report/matched-cost.svg) and [sensitivities](results/report/matched-sensitivity.svg) have PNG counterparts and retained renderers. Independent review accepts this conditional economic interpretation; no global optimum, equally optimized technology comparison or whole-plant LCOE is claimed.

## 4. Constraint outcomes

All 84 executing checks are listed below for the 498 fresh native cases. Every predicate was independently rederived with zero disagreement; there are no indeterminate verdicts. `results/constraint-summary.json` names every violated case. Passing numerical verification does not make an engineering-failed case admissible.

| `constraint_id` | `source_local_identity` | Satisfied | Violated | Indeterminate |
| --- | --- | ---: | ---: | ---: |
| `component_alternatives__plant__water_ic1__evaluation_defined_ok__49d1611637350e3c` | `evaluation_defined_ok` | 333 | 165 | 0 |
| `component_alternatives__plant__water_ic1__flow_margin_ok__2ca46da8d6c9fc06` | `flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__water_ic1__duty_margin_ok__ae893105fd8169d4` | `duty_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__water_ic1__power_margin_ok__ceac76348e0eb2b6` | `power_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__salt_flow_capacity__capacity_requirement__1f3f2b5125f26aed` | `capacity_requirement` | 451 | 47 | 0 |
| `component_alternatives__plant__steam_feed_flow_capacity__capacity_requirement__f522084f390b88ed` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__gas_boundary__bypass_flow_margin_ok__840f5556c962fa45` | `bypass_flow_margin_ok` | 495 | 3 | 0 |
| `component_alternatives__plant__gas_boundary__controller_capacity_ok_ok__3c7a992b7ef572ac` | `controller_capacity_ok_ok` | 495 | 3 | 0 |
| `component_alternatives__plant__gas_boundary__bypass_fraction_margin_ok__7197bb376c493e60` | `bypass_fraction_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_boundary__pressure_margin_ok__023a9033fbabc01f` | `pressure_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_boundary__total_flow_margin_ok__e4fcc2a2f41664a0` | `total_flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_boundary__exchanger_flow_margin_ok__586a84274fb7f1fb` | `exchanger_flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_boundary__added_dp_margin_ok__daebd77c6cb6ed86` | `added_dp_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_boundary__temperature_margin_ok__b9e59d1aa293995e` | `temperature_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_boundary__source_adequate_ok__dd6d7a3461399330` | `source_adequate_ok` | 281 | 217 | 0 |
| `component_alternatives__plant__water_ic2__duty_margin_ok__8546438198d8a311` | `duty_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__water_ic2__evaluation_defined_ok__06ab6aea3f7f761b` | `evaluation_defined_ok` | 333 | 165 | 0 |
| `component_alternatives__plant__water_ic2__power_margin_ok__9155c8131175c99b` | `power_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__water_ic2__flow_margin_ok__a1238658a4279d69` | `flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_ledger__net_positive__7be67634b73dc5d3` | `net_positive` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_ledger__balance__79e79cd29079c8e8` | `balance` | 498 | 0 | 0 |
| `component_alternatives__plant__recuperator_duty_capacity__capacity_requirement__37716788614d63a8` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_condensate_electric_capacity__capacity_requirement__7f87933904cdde5d` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_hp_flow_capacity__capacity_requirement__7d80da68d49ab07e` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__he_capacity__capacity_ok__3993dc4f00da3840` | `capacity_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_loss_duty_capacity__capacity_requirement__3f4fdc86d64b5036` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__salt_electric_capacity__capacity_requirement__d0a6e35468ded9cc` | `capacity_requirement` | 451 | 47 | 0 |
| `component_alternatives__plant__steam_lp_shaft_capacity__capacity_requirement__145e6e0999fc7f4f` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_gross_capacity__capacity_requirement__4252a99565636ed5` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_rejection_capacity__capacity_requirement__ed5a57ebe998f809` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_condenser_capacity__capacity_requirement__67922fb363412df0` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_lp_flow_capacity__capacity_requirement__704e61a5a8c7bf24` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__gas_loss_electric_capacity__capacity_requirement__6a158987313c84e0` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_reheat_ua_capacity__capacity_requirement__ff5775187764fbbd` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_boundary__source_adequate_ok__eaa371ee289234f1` | `source_adequate_ok` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_boundary__exchanger_flow_margin_ok__b6c20f51b00f7b9c` | `exchanger_flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__added_dp_margin_ok__f0c716d635261219` | `added_dp_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__bypass_flow_margin_ok__8f1459a694a0757a` | `bypass_flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__total_flow_margin_ok__e80a0efbac0d3f57` | `total_flow_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__controller_capacity_ok_ok__d8dd67a24704a1c0` | `controller_capacity_ok_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__temperature_margin_ok__39291a564826dd0f` | `temperature_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__bypass_fraction_margin_ok__32cff09a266a19fc` | `bypass_fraction_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_boundary__pressure_margin_ok__177980a50b09bf98` | `pressure_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_hp_shaft_capacity__capacity_requirement__08512b73f01b2ff4` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_water_flow_capacity__capacity_requirement__f3bfd573273dc22e` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_loss_flow_capacity__capacity_requirement__8a2d8de72c5b2880` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__turbine_capacity__capacity_ok__0178c1184c793932` | `capacity_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_condensate_pressure_capacity__capacity_requirement__d523b96c0c76de1b` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_water__cooling_approach_ok_required__c8a5d75f54ded9d6` | `cooling_approach_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__generator_capacity__capacity_ok__ee0395479decdfc2` | `capacity_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__salt_shaft_capacity__capacity_requirement__419a029d2df87f3c` | `capacity_requirement` | 451 | 47 | 0 |
| `component_alternatives__plant__source_checks__flow_ok__d77445a069dcb805` | `flow_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__source_checks__pressure_ok__aa0a62a144e9c75d` | `pressure_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_loss_water__cooling_approach_ok_required__6112b029bb4ede08` | `cooling_approach_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__rejection_capacity__capacity_requirement__8eab7ec16a8b759e` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_feed_electric_capacity__capacity_requirement__02f57441b4cf6746` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_water_electric_capacity__capacity_requirement__79eb129457bf9d3d` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__compressor_capacity__capacity_ok__e8c94ef170d28993` | `capacity_ok` | 468 | 30 | 0 |
| `component_alternatives__plant__salt_fill_capacity__capacity_requirement__0d36a52c336754e3` | `capacity_requirement` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_feed_pressure_capacity__capacity_requirement__2b0a04222feb552b` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_main_ua_capacity__capacity_requirement__c2efdc04c52106da` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_condensate_flow_capacity__capacity_requirement__a06233d7139b47ec` | `capacity_requirement` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_transport__motor_factor_ok_required__eed87936beb69817` | `motor_factor_ok_required` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_transport__design_motor_factor_ok_required__4a9e97f942584206` | `design_motor_factor_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__design_pump_size_ok_required__39419b9b933c2a99` | `design_pump_size_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__design_pump_type_ok_required__86fcc6e00c250519` | `design_pump_type_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__pump_type_ok_required__a1706d503ff60f4c` | `pump_type_ok_required` | 464 | 34 | 0 |
| `component_alternatives__plant__steam_transport__pump_size_ok_required__b3af0a8e326050b1` | `pump_size_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__ihx_capacity_ok_required__a8ade32d723ec9f2` | `ihx_capacity_ok_required` | 474 | 24 | 0 |
| `component_alternatives__plant__steam_transport__salt_head_ok_required__9049eef128641767` | `salt_head_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__design_motor_base_ok_required__34d2455206f46357` | `design_motor_base_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__salt_flow_regime_ok_required__6e2b05d56b7bbfaf` | `salt_flow_regime_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_transport__motor_base_ok_required__238e695ccdaf5ebf` | `motor_base_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_conditions__supported_required__92a5d05764f5fff9` | `supported_required` | 474 | 24 | 0 |
| `component_alternatives__plant__water_pre__power_margin_ok__d793d504da406d97` | `power_margin_ok` | 492 | 6 | 0 |
| `component_alternatives__plant__water_pre__flow_margin_ok__129a83656acb8a06` | `flow_margin_ok` | 489 | 9 | 0 |
| `component_alternatives__plant__water_pre__evaluation_defined_ok__bc4741b386520ff5` | `evaluation_defined_ok` | 211 | 287 | 0 |
| `component_alternatives__plant__water_pre__duty_margin_ok__80af75533d32b208` | `duty_margin_ok` | 498 | 0 | 0 |
| `component_alternatives__plant__gas_ledger__net_positive__ee25ae39167c9ad3` | `net_positive` | 497 | 1 | 0 |
| `component_alternatives__plant__gas_ledger__balance__a530b58ca455c8b8` | `balance` | 176 | 322 | 0 |
| `component_alternatives__plant__steam_cycle__main_ua_available_required__6cdb52b3bf9953e0` | `main_ua_available_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_cycle__reheat_admission_ok_required__e88f7416d91d86fd` | `reheat_admission_ok_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_cycle__reheat_ua_available_required__1e1158ef6871602d` | `reheat_ua_available_required` | 498 | 0 | 0 |
| `component_alternatives__plant__steam_cycle__main_admission_ok_required__dbbd20ff9c7f4317` | `main_admission_ok_required` | 498 | 0 | 0 |

Cooler validity is separate from equipment adequacy. Of 375 gas-catalog points, 14 pass all checks; 39 have solved coolers but fail equipment or source/coupling checks. The other 322 have at least one no-root cooler: 233 exceed an upper bracket, 78 lie below a lower bracket, and 11 have mixed bounds across coolers. These categories retain overlapping failed predicates. Undefined cooler outputs can trigger the conversion balance check; that is not an independently established hardware deficit.

A lower-bound exclusion is below the supported UA bracket near the infinite-water-flow limit. An upper-bound exclusion exceeds the finite outlet-temperature bracket; when that bracket is capped by 60 °C, the retained water-property range limits the model. Every one of the 464 upper-bound cooler occurrences in this record hits the 60 °C property ceiling, rather than the hot-gas terminal cap. These are cooler occurrences, not 464 distinct cases. Neither exclusion licenses physical extrapolation or ranking. A solved cooler may still exceed selected water-flow, power or duty ratings. The connector catalog has 21 passing and 51 failed proposals. Three of six smaller controller offers fail on the gas branch; the three steam offers pass. All 48 efficiency/price/recurring/source-cost sensitivity proposals pass their engineering checks.


## 5. Framing

[INHERITED] Proposed framing is retained after the fresh run, with no changes. Search is selection from the finite explicit catalog; sensitivities remain scenarios. Thirty-nine attributes varied and four directions stayed declined under the fixed steam offer. The gas catalog has 14 passing combinations out of 375 (3.73%), below the policy’s 5–95% H1 search band. That hypothesis is falsified for this window; it is not permission to derive chosen source/ratio inputs or expand property domains.

| Axis | Proposed | Judged | Changed? | Executed variation |
| --- | --- | --- | --- | --- |
| `blanket_source_q_source` | sensitivity | sensitivity | no | yes |
| `cycle_selected_flow` | search | search | no | yes |
| `compressor_1_selected_ratio` | search | search | no | yes |
| `compressor_1_efficiency` | sensitivity | sensitivity | no | yes |
| `compressor_2_selected_ratio` | search | search | no | yes |
| `compressor_2_efficiency` | sensitivity | sensitivity | no | yes |
| `compressor_3_selected_ratio` | search | search | no | yes |
| `compressor_3_efficiency` | sensitivity | sensitivity | no | yes |
| `cycle_turbine_efficiency` | sensitivity | sensitivity | no | yes |
| `water_ic1_ua` | search | search | no | yes |
| `water_ic2_ua` | search | search | no | yes |
| `water_pre_ua` | search | search | no | yes |
| `recuperator_hardware_ua` | search | search | no | yes |
| `steam_transport_n_loops` | search | search | no | yes |
| `steam_transport_salt_pumps_per_circuit` | search | search | no | yes |
| `steam_transport_selected_salt_design_flow_kg_s` | search | search | no | yes |
| `steam_boundary_bypass_flow_rating` | sensitivity | sensitivity | no | yes |
| `steam_ledger_controller_capital` | sensitivity | sensitivity | no | yes |
| `steam_ledger_annual_service_fraction` | sensitivity | sensitivity | no | yes |
| `steam_ledger_replacement_fraction` | sensitivity | sensitivity | no | yes |
| `steam_ledger_common_source_pv` | sensitivity | sensitivity | no | yes |
| `gas_boundary_bypass_flow_rating` | sensitivity | sensitivity | no | yes |
| `gas_ledger_controller_capital` | sensitivity | sensitivity | no | yes |
| `gas_ledger_annual_service_fraction` | sensitivity | sensitivity | no | yes |
| `gas_ledger_replacement_fraction` | sensitivity | sensitivity | no | yes |
| `gas_ledger_common_source_pv` | sensitivity | sensitivity | no | yes |
| `compressor_equipment_price_factor` | sensitivity | sensitivity | no | yes |
| `turbine_equipment_price_factor` | sensitivity | sensitivity | no | yes |
| `generator_equipment_price_factor` | sensitivity | sensitivity | no | yes |
| `he_hx_price_factor` | sensitivity | sensitivity | no | yes |
| `he_duty_equipment_price_factor` | sensitivity | sensitivity | no | yes |
| `conversion_services_price_factor` | sensitivity | sensitivity | no | yes |
| `heat_rejection_equipment_price_factor` | sensitivity | sensitivity | no | yes |
| `gas_ledger_capital9` | sensitivity | sensitivity | no | yes |
| `steam_ledger_capital3` | sensitivity | sensitivity | no | yes |
| `steam_ledger_capital4` | sensitivity | sensitivity | no | yes |
| `steam_transport_costscale` | sensitivity | sensitivity | no | yes |
| `steam_cycle_eta_hp` | sensitivity | sensitivity | no | yes |
| `steam_cycle_eta_lp` | sensitivity | sensitivity | no | yes |
| `steam_cycle_steam_temperature_C` | sensitivity | sensitivity | no | declined |
| `steam_cycle_reheat_temperature_C` | sensitivity | sensitivity | no | declined |
| `steam_cycle_condenser_temperature_C` | sensitivity | sensitivity | no | declined |
| `steam_transport_secondary_head` | sensitivity | sensitivity | no | declined |


## 6. Per-axis account

Each table locates passing and failed cases by tested value, using `results/axis-assessment.json`. Its complete case IDs join directly to `results/cases.json` verdicts and the qualified checks in §4; `results/constraint-summary.json` provides the inverse check-to-case mapping. The cost-gap range includes only cases satisfying all implemented checks, in USD2025/net MWh. Coordinated offers and different source scenarios coexist at a level, so these grouped ranges do not isolate a causal effect. Matched-case decomposition and sensitivities provide that interpretation. No continuous feasible boundary is inferred.

#### `blanket_source_q_source` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `blanket_source_q_source` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 2500 | 35/166 | 104 | -36.950 to 33.759 |
| 2800 | 26/166 | 108 | -38.496 to 30.376 |
| 3000 | 22/166 | 110 | -22.946 to 41.837 |

#### `cycle_selected_flow` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 1500 | 0/75 | 72 | No passing case |
| 1750 | 28/116 | 49 | -38.496 to 30.376 |
| 2000 | 54/157 | 59 | -36.950 to 41.837 |
| 2250 | 1/75 | 67 | -6.657 to -6.657 |
| 2500 | 0/75 | 75 | No passing case |


#### `cycle_selected_flow` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `compressor_1_selected_ratio` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 1.2 | 0/75 | 60 | No passing case |
| 1.35 | 0/75 | 64 | No passing case |
| 1.5 | 29/116 | 64 | -33.771 to 33.759 |
| 1.65 | 23/116 | 68 | -22.946 to 41.837 |
| 1.8 | 31/116 | 66 | -38.496 to 30.376 |


#### `compressor_1_selected_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `compressor_1_efficiency` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `compressor_1_efficiency` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.86 | 6/6 | 0 | -21.832 to 5.140 |
| 0.89 | 71/486 | 322 | -38.496 to 41.837 |
| 0.92 | 6/6 | 0 | 3.466 to 13.104 |

#### `compressor_2_selected_ratio` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 1.2 | 0/75 | 60 | No passing case |
| 1.35 | 0/75 | 64 | No passing case |
| 1.5 | 29/116 | 64 | -33.771 to 33.759 |
| 1.65 | 23/116 | 68 | -22.946 to 41.837 |
| 1.8 | 31/116 | 66 | -38.496 to 30.376 |


#### `compressor_2_selected_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `compressor_2_efficiency` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `compressor_2_efficiency` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.86 | 6/6 | 0 | -21.832 to 5.140 |
| 0.89 | 71/486 | 322 | -38.496 to 41.837 |
| 0.92 | 6/6 | 0 | 3.466 to 13.104 |

#### `compressor_3_selected_ratio` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 1.2 | 0/75 | 60 | No passing case |
| 1.35 | 0/75 | 64 | No passing case |
| 1.5 | 29/116 | 64 | -33.771 to 33.759 |
| 1.65 | 23/116 | 68 | -22.946 to 41.837 |
| 1.8 | 31/116 | 66 | -38.496 to 30.376 |


#### `compressor_3_selected_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `compressor_3_efficiency` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `compressor_3_efficiency` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.86 | 6/6 | 0 | -21.832 to 5.140 |
| 0.89 | 71/486 | 322 | -38.496 to 41.837 |
| 0.92 | 6/6 | 0 | 3.466 to 13.104 |

#### `cycle_turbine_efficiency` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `cycle_turbine_efficiency` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.9 | 6/6 | 0 | -21.832 to 5.140 |
| 0.93 | 71/486 | 322 | -38.496 to 41.837 |
| 0.96 | 6/6 | 0 | 3.466 to 13.104 |

#### `water_ic1_ua` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 25 | 83/348 | 173 | -38.496 to 41.837 |
| 30 | 0/75 | 74 | No passing case |
| 40 | 0/75 | 75 | No passing case |


#### `water_ic1_ua` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `water_ic2_ua` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 25 | 83/348 | 173 | -38.496 to 41.837 |
| 30 | 0/75 | 74 | No passing case |
| 40 | 0/75 | 75 | No passing case |


#### `water_ic2_ua` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `water_pre_ua` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 20 | 2/75 | 60 | -36.950 to -6.747 |
| 25 | 81/198 | 38 | -38.496 to 41.837 |
| 40 | 0/75 | 75 | No passing case |
| 50 | 0/75 | 74 | No passing case |
| 60 | 0/75 | 75 | No passing case |


#### `water_pre_ua` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `recuperator_hardware_ua` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 60 | 83/423 | 247 | -38.496 to 41.837 |
| 80 | 0/75 | 75 | No passing case |


#### `recuperator_hardware_ua` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `steam_transport_n_loops` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 10 | 19/36 | 0 | -33.771 to 33.759 |
| 11 | 21/36 | 0 | -38.496 to 30.376 |
| 12 | 5/18 | 0 | -1.509 to 5.770 |
| 14 | 38/408 | 322 | -36.950 to 41.837 |


#### `steam_transport_n_loops` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `steam_transport_salt_pumps_per_circuit` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 2 | 0/24 | 0 | No passing case |
| 3 | 22/42 | 0 | -22.946 to 41.837 |
| 4 | 61/432 | 322 | -38.496 to 33.759 |


#### `steam_transport_salt_pumps_per_circuit` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `steam_transport_selected_salt_design_flow_kg_s` — feasible structure (search framing)

**Applies:** yes.

The following levels delimit tested discrete offers. Other selected attributes vary jointly; no continuous boundary or global optimum is established.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 225 | 43/72 | 0 | -38.496 to 33.759 |
| 250 | 40/426 | 322 | -36.950 to 41.837 |


#### `steam_transport_selected_salt_design_flow_kg_s` — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### `steam_boundary_bypass_flow_rating` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_boundary_bypass_flow_rating` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 500 | 3/3 | 0 | -4.083 to 9.424 |
| 2000 | 80/495 | 322 | -38.496 to 41.837 |

#### `steam_ledger_controller_capital` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_ledger_controller_capital` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 5e+06 | 6/6 | 0 | -38.496 to -9.112 |
| 8e+06 | 3/3 | 0 | -4.083 to 9.424 |
| 1e+07 | 68/483 | 322 | -36.950 to 23.280 |
| 1.5e+07 | 6/6 | 0 | 12.143 to 41.837 |

#### `steam_ledger_annual_service_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_ledger_annual_service_fraction` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.01 | 3/3 | 0 | -2.457 to 9.287 |
| 0.02 | 77/492 | 322 | -38.496 to 41.837 |
| 0.03 | 3/3 | 0 | -5.663 to 9.604 |

#### `steam_ledger_replacement_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_ledger_replacement_fraction` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.1 | 3/3 | 0 | -2.457 to 9.287 |
| 0.2 | 77/492 | 322 | -38.496 to 41.837 |
| 0.3 | 3/3 | 0 | -5.663 to 9.604 |

#### `steam_ledger_common_source_pv` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_ledger_common_source_pv` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0 | 77/492 | 322 | -38.496 to 41.837 |
| 5e+08 | 3/3 | 0 | -8.371 to 6.867 |
| 2e+09 | 3/3 | 0 | -21.306 to -0.870 |

#### `gas_boundary_bypass_flow_rating` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `gas_boundary_bypass_flow_rating` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 500 | 0/3 | 0 | No passing case |
| 2000 | 83/495 | 322 | -38.496 to 41.837 |

#### `gas_ledger_controller_capital` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `gas_ledger_controller_capital` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 5e+06 | 6/6 | 0 | 14.173 to 41.837 |
| 8e+06 | 0/3 | 0 | No passing case |
| 1e+07 | 71/483 | 322 | -36.950 to 28.003 |
| 1.5e+07 | 6/6 | 0 | -38.496 to -4.389 |

#### `gas_ledger_annual_service_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `gas_ledger_annual_service_fraction` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.01 | 3/3 | 0 | -2.457 to 9.287 |
| 0.02 | 77/492 | 322 | -38.496 to 41.837 |
| 0.03 | 3/3 | 0 | -5.663 to 9.604 |

#### `gas_ledger_replacement_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `gas_ledger_replacement_fraction` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.1 | 3/3 | 0 | -2.457 to 9.287 |
| 0.2 | 77/492 | 322 | -38.496 to 41.837 |
| 0.3 | 3/3 | 0 | -5.663 to 9.604 |

#### `gas_ledger_common_source_pv` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `gas_ledger_common_source_pv` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0 | 77/492 | 322 | -38.496 to 41.837 |
| 5e+08 | 3/3 | 0 | -8.371 to 6.867 |
| 2e+09 | 3/3 | 0 | -21.306 to -0.870 |

#### `compressor_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `compressor_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/486 | 322 | -36.950 to 28.003 |
| 1.5 | 6/6 | 0 | -38.496 to -4.389 |

#### `turbine_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `turbine_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/486 | 322 | -36.950 to 28.003 |
| 1.5 | 6/6 | 0 | -38.496 to -4.389 |

#### `generator_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `generator_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/486 | 322 | -36.950 to 28.003 |
| 1.5 | 6/6 | 0 | -38.496 to -4.389 |

#### `he_hx_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_hx_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/486 | 322 | -36.950 to 28.003 |
| 1.5 | 6/6 | 0 | -38.496 to -4.389 |

#### `he_duty_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_duty_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/486 | 322 | -36.950 to 28.003 |
| 1.5 | 6/6 | 0 | -38.496 to -4.389 |

#### `conversion_services_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `conversion_services_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/336 | 173 | -36.950 to 28.003 |
| 1.25 | 0/75 | 74 | No passing case |
| 1.5 | 6/81 | 75 | -38.496 to -4.389 |

#### `heat_rejection_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_rejection_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | 14.173 to 41.837 |
| 1 | 71/486 | 322 | -36.950 to 28.003 |
| 1.5 | 6/6 | 0 | -38.496 to -4.389 |

#### `gas_ledger_capital9` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `gas_ledger_capital9` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 4.29665e+07 | 6/6 | 0 | 14.173 to 41.837 |
| 8.5933e+07 | 71/486 | 322 | -36.950 to 28.003 |
| 1.289e+08 | 6/6 | 0 | -38.496 to -4.389 |

#### `steam_ledger_capital3` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_ledger_capital3` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 1.23732e+08 | 6/6 | 0 | -38.496 to -9.112 |
| 2.47464e+08 | 71/486 | 322 | -36.950 to 23.280 |
| 3.71197e+08 | 6/6 | 0 | 12.143 to 41.837 |

#### `steam_ledger_capital4` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_ledger_capital4` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 5.79698e+07 | 6/6 | 0 | -38.496 to -9.112 |
| 1.1594e+08 | 71/486 | 322 | -36.950 to 23.280 |
| 1.73909e+08 | 6/6 | 0 | 12.143 to 41.837 |

#### `steam_transport_costscale` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_transport_costscale` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.5 | 6/6 | 0 | -38.496 to -9.112 |
| 1 | 71/486 | 322 | -36.950 to 23.280 |
| 1.5 | 6/6 | 0 | 12.143 to 41.837 |

#### `steam_cycle_eta_hp` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_cycle_eta_hp` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.87 | 6/6 | 0 | -20.842 to 10.579 |
| 0.9 | 71/486 | 322 | -38.496 to 41.837 |
| 0.93 | 6/6 | 0 | -4.984 to 12.045 |

#### `steam_cycle_eta_lp` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_cycle_eta_lp` — observed response (sensitivity framing)

**Applies:** yes.

The observed conditional ranges below describe the tested scenarios. No boundary claim. Failed cases are counted at their actual levels and retained by identity.

| Tested value | All checks pass / evaluated | Any undefined cooler | Passing steam-minus-gas cost range |
| ---: | ---: | ---: | ---: |
| 0.87 | 6/6 | 0 | -20.842 to 10.579 |
| 0.9 | 71/486 | 322 | -38.496 to 41.837 |
| 0.93 | 6/6 | 0 | -4.984 to 12.045 |

#### `steam_cycle_steam_temperature_C` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_cycle_steam_temperature_C` — observed response (sensitivity framing)

**Applies:** yes.

Declined under the held steam offer; no varied response is claimed. Existing offered conditions do not support this temperature/head move. The fixed value remains in the input record; no boundary claim.

#### `steam_cycle_reheat_temperature_C` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_cycle_reheat_temperature_C` — observed response (sensitivity framing)

**Applies:** yes.

Declined under the held steam offer; no varied response is claimed. Existing offered conditions do not support this temperature/head move. The fixed value remains in the input record; no boundary claim.

#### `steam_cycle_condenser_temperature_C` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_cycle_condenser_temperature_C` — observed response (sensitivity framing)

**Applies:** yes.

Declined under the held steam offer; no varied response is claimed. Existing offered conditions do not support this temperature/head move. The fixed value remains in the input record; no boundary claim.

#### `steam_transport_secondary_head` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `steam_transport_secondary_head` — observed response (sensitivity framing)

**Applies:** yes.

Declined under the held steam offer; no varied response is claimed. Existing offered conditions do not support this temperature/head move. The fixed value remains in the input record; no boundary claim.



## 7. Axis groups

Every axis names one authored SysML attribute and its complete emitted entry-key group. `axes.json` retains all groups. Equal compressor ratios and matched financial scenarios are coordinated input choices, not inferred physical identities.

| Axis | Entry key | Provenance | Note |
| --- | --- | --- | --- |
| `blanket_source_q_source` | `component_alternatives__plant__blanket_source__q_source` | fan_out | SysML attribute component_alternatives::plant::blanket_source::q_source. Chosen common source heat scenarios; no matching solve. |
| `cycle_selected_flow` | `component_alternatives__plant__cycle__selected_flow` | fan_out | SysML attribute component_alternatives::plant::cycle::selected_flow. Chosen gas operating flow at held installed ratings. |
| `compressor_1_selected_ratio` | `component_alternatives__plant__compressor_1__selected_ratio` | fan_out | SysML attribute component_alternatives::plant::compressor_1::selected_ratio. Independent stage choice. The proposal catalog coordinates the three choices at equal values; no physical identity is inferred. |
| `compressor_1_efficiency` | `component_alternatives__plant__compressor_1__efficiency` | fan_out | SysML attribute component_alternatives::plant::compressor_1::efficiency. Hypothetical performance sensitivity. |
| `compressor_2_selected_ratio` | `component_alternatives__plant__compressor_2__selected_ratio` | fan_out | SysML attribute component_alternatives::plant::compressor_2::selected_ratio. Independent stage choice. The proposal catalog coordinates the three choices at equal values; no physical identity is inferred. |
| `compressor_2_efficiency` | `component_alternatives__plant__compressor_2__efficiency` | fan_out | SysML attribute component_alternatives::plant::compressor_2::efficiency. Hypothetical performance sensitivity. |
| `compressor_3_selected_ratio` | `component_alternatives__plant__compressor_3__selected_ratio` | fan_out | SysML attribute component_alternatives::plant::compressor_3::selected_ratio. Independent stage choice. The proposal catalog coordinates the three choices at equal values; no physical identity is inferred. |
| `compressor_3_efficiency` | `component_alternatives__plant__compressor_3__efficiency` | fan_out | SysML attribute component_alternatives::plant::compressor_3::efficiency. Hypothetical performance sensitivity. |
| `cycle_turbine_efficiency` | `component_alternatives__plant__cycle__turbine_efficiency` | fan_out | SysML attribute component_alternatives::plant::cycle::turbine_efficiency. Hypothetical performance sensitivity. |
| `water_ic1_ua` | `component_alternatives__plant__water_ic1__ua` | fan_out | SysML attribute component_alternatives::plant::water_ic1::ua. Installed capability selected from an explicitly priced coordinated service offer. |
| `water_ic2_ua` | `component_alternatives__plant__water_ic2__ua` | fan_out | SysML attribute component_alternatives::plant::water_ic2::ua. Installed capability selected from an explicitly priced coordinated service offer. |
| `water_pre_ua` | `component_alternatives__plant__water_pre__ua` | fan_out | SysML attribute component_alternatives::plant::water_pre::ua. Installed capability selected from an explicitly priced coordinated service offer. |
| `recuperator_hardware_ua` | `component_alternatives__plant__recuperator_hardware__ua` | fan_out | SysML attribute component_alternatives::plant::recuperator_hardware::ua. Installed capability selected from an explicitly priced coordinated service offer. |
| `steam_transport_n_loops` | `component_alternatives__plant__steam_transport__n_loops` | fan_out | SysML attribute component_alternatives::plant::steam_transport::n_loops. Selected salt/IHX equipment offer. Here n_loops counts offered IHX circuits; upstream primary loop count remains held at 14. |
| `steam_transport_salt_pumps_per_circuit` | `component_alternatives__plant__steam_transport__salt_pumps_per_circuit` | fan_out | SysML attribute component_alternatives::plant::steam_transport::salt_pumps_per_circuit. Selected salt/IHX equipment offer. Here n_loops counts offered IHX circuits; upstream primary loop count remains held at 14. |
| `steam_transport_selected_salt_design_flow_kg_s` | `component_alternatives__plant__steam_transport__selected_salt_design_flow_kg_s` | fan_out | SysML attribute component_alternatives::plant::steam_transport::selected_salt_design_flow_kg_s. Selected salt/IHX equipment offer. Here n_loops counts offered IHX circuits; upstream primary loop count remains held at 14. |
| `steam_boundary_bypass_flow_rating` | `component_alternatives__plant__steam_boundary__bypass_flow_rating` | fan_out | SysML attribute component_alternatives::plant::steam_boundary::bypass_flow_rating. Full or deliberately undersized purchased controller offer. |
| `steam_ledger_controller_capital` | `component_alternatives__plant__steam_ledger__controller_capital` | fan_out | SysML attribute component_alternatives::plant::steam_ledger::controller_capital. Hypothetical controller quote paired with its declared flow rating; also subject to branch quote sensitivity. |
| `steam_ledger_annual_service_fraction` | `component_alternatives__plant__steam_ledger__annual_service_fraction` | fan_out | SysML attribute component_alternatives::plant::steam_ledger::annual_service_fraction. Hypothetical recurring-cost sensitivity. Separate salt event schedule remains explicit. |
| `steam_ledger_replacement_fraction` | `component_alternatives__plant__steam_ledger__replacement_fraction` | fan_out | SysML attribute component_alternatives::plant::steam_ledger::replacement_fraction. Hypothetical recurring-cost sensitivity. Separate salt event schedule remains explicit. |
| `steam_ledger_common_source_pv` | `component_alternatives__plant__steam_ledger__common_source_pv` | fan_out | SysML attribute component_alternatives::plant::steam_ledger::common_source_pv. Illustrative common upstream present-value charge, coordinated equally across branches; no fuel price model. |
| `gas_boundary_bypass_flow_rating` | `component_alternatives__plant__gas_boundary__bypass_flow_rating` | fan_out | SysML attribute component_alternatives::plant::gas_boundary::bypass_flow_rating. Full or deliberately undersized purchased controller offer. |
| `gas_ledger_controller_capital` | `component_alternatives__plant__gas_ledger__controller_capital` | fan_out | SysML attribute component_alternatives::plant::gas_ledger::controller_capital. Hypothetical controller quote paired with its declared flow rating; also subject to branch quote sensitivity. |
| `gas_ledger_annual_service_fraction` | `component_alternatives__plant__gas_ledger__annual_service_fraction` | fan_out | SysML attribute component_alternatives::plant::gas_ledger::annual_service_fraction. Hypothetical recurring-cost sensitivity. Separate salt event schedule remains explicit. |
| `gas_ledger_replacement_fraction` | `component_alternatives__plant__gas_ledger__replacement_fraction` | fan_out | SysML attribute component_alternatives::plant::gas_ledger::replacement_fraction. Hypothetical recurring-cost sensitivity. Separate salt event schedule remains explicit. |
| `gas_ledger_common_source_pv` | `component_alternatives__plant__gas_ledger__common_source_pv` | fan_out | SysML attribute component_alternatives::plant::gas_ledger::common_source_pv. Illustrative common upstream present-value charge, coordinated equally across branches; no fuel price model. |
| `compressor_equipment_price_factor` | `component_alternatives__plant__compressor_equipment__price_factor` | fan_out | SysML attribute component_alternatives::plant::compressor_equipment::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `turbine_equipment_price_factor` | `component_alternatives__plant__turbine_equipment__price_factor` | fan_out | SysML attribute component_alternatives::plant::turbine_equipment::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `generator_equipment_price_factor` | `component_alternatives__plant__generator_equipment__price_factor` | fan_out | SysML attribute component_alternatives::plant::generator_equipment::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `he_hx_price_factor` | `component_alternatives__plant__he_hx__price_factor` | fan_out | SysML attribute component_alternatives::plant::he_hx::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `he_duty_equipment_price_factor` | `component_alternatives__plant__he_duty_equipment__price_factor` | fan_out | SysML attribute component_alternatives::plant::he_duty_equipment::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `conversion_services_price_factor` | `component_alternatives__plant__conversion_services__price_factor` | fan_out | SysML attribute component_alternatives::plant::conversion_services::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `heat_rejection_equipment_price_factor` | `component_alternatives__plant__heat_rejection_equipment__price_factor` | fan_out | SysML attribute component_alternatives::plant::heat_rejection_equipment::price_factor. Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer. |
| `gas_ledger_capital9` | `component_alternatives__plant__gas_ledger__capital9` | fan_out | SysML attribute component_alternatives::plant::gas_ledger::capital9. Selected cycle-transport quote in USD2004; physical scope held. |
| `steam_ledger_capital3` | `component_alternatives__plant__steam_ledger__capital3` | fan_out | SysML attribute component_alternatives::plant::steam_ledger::capital3. Selected steam conversion or rejection aggregate quote in USD2025; physical scope held. |
| `steam_ledger_capital4` | `component_alternatives__plant__steam_ledger__capital4` | fan_out | SysML attribute component_alternatives::plant::steam_ledger::capital4. Selected steam conversion or rejection aggregate quote in USD2025; physical scope held. |
| `steam_transport_costscale` | `component_alternatives__plant__steam_transport__costscale` | fan_out | SysML attribute component_alternatives::plant::steam_transport::costscale. Existing salt-connector cost multiplier; no physical equipment sizing. |
| `steam_cycle_eta_hp` | `component_alternatives__plant__steam_cycle__eta_hp` | fan_out | SysML attribute component_alternatives::plant::steam_cycle::eta_hp. Hypothetical performance sensitivity on the selected steam offer. |
| `steam_cycle_eta_lp` | `component_alternatives__plant__steam_cycle__eta_lp` | fan_out | SysML attribute component_alternatives::plant::steam_cycle::eta_lp. Hypothetical performance sensitivity on the selected steam offer. |
| `steam_cycle_steam_temperature_C` | `component_alternatives__plant__steam_cycle__steam_temperature_C` | fan_out | SysML attribute component_alternatives::plant::steam_cycle::steam_temperature_C. Declared but declined: held steam offer does not establish an off-design temperature envelope. |
| `steam_cycle_reheat_temperature_C` | `component_alternatives__plant__steam_cycle__reheat_temperature_C` | fan_out | SysML attribute component_alternatives::plant::steam_cycle::reheat_temperature_C. Declared but declined: held steam offer does not establish an off-design temperature envelope. |
| `steam_cycle_condenser_temperature_C` | `component_alternatives__plant__steam_cycle__condenser_temperature_C` | fan_out | SysML attribute component_alternatives::plant::steam_cycle::condenser_temperature_C. Declared but declined: held steam offer does not establish an off-design temperature envelope. |
| `steam_transport_secondary_head` | `component_alternatives__plant__steam_transport__secondary_head` | fan_out | SysML attribute component_alternatives::plant::steam_transport::secondary_head. Declared but declined: altered operating salt head changes the captured steam return condition. |

## 8. Indicators and rulings

The fresh indicator artifact traces all 43 groups, including four declined directions; no subset is used. Every group is valid and has reachable constraints. There are no `no_constraint_response` axes, so the condition requiring a new owner ruling and a missing-response finding does not arise.

| Axis | Indicator | Ruling | Note |
| --- | --- | --- | --- |
| `blanket_source_q_source` | constraints_reachable | No additional ruling required | Executed |
| `compressor_1_efficiency` | constraints_reachable | No additional ruling required | Executed |
| `compressor_1_selected_ratio` | constraints_reachable | No additional ruling required | Executed |
| `compressor_2_efficiency` | constraints_reachable | No additional ruling required | Executed |
| `compressor_2_selected_ratio` | constraints_reachable | No additional ruling required | Executed |
| `compressor_3_efficiency` | constraints_reachable | No additional ruling required | Executed |
| `compressor_3_selected_ratio` | constraints_reachable | No additional ruling required | Executed |
| `compressor_equipment_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `conversion_services_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `cycle_selected_flow` | constraints_reachable | No additional ruling required | Executed |
| `cycle_turbine_efficiency` | constraints_reachable | No additional ruling required | Executed |
| `gas_boundary_bypass_flow_rating` | constraints_reachable | No additional ruling required | Executed |
| `gas_ledger_annual_service_fraction` | constraints_reachable | No additional ruling required | Executed |
| `gas_ledger_capital9` | constraints_reachable | No additional ruling required | Executed |
| `gas_ledger_common_source_pv` | constraints_reachable | No additional ruling required | Executed |
| `gas_ledger_controller_capital` | constraints_reachable | No additional ruling required | Executed |
| `gas_ledger_replacement_fraction` | constraints_reachable | No additional ruling required | Executed |
| `generator_equipment_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `he_duty_equipment_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `he_hx_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `heat_rejection_equipment_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `recuperator_hardware_ua` | constraints_reachable | No additional ruling required | Executed |
| `steam_boundary_bypass_flow_rating` | constraints_reachable | No additional ruling required | Executed |
| `steam_cycle_condenser_temperature_C` | constraints_reachable | No additional ruling required | Declined under fixed steam offer |
| `steam_cycle_eta_hp` | constraints_reachable | No additional ruling required | Executed |
| `steam_cycle_eta_lp` | constraints_reachable | No additional ruling required | Executed |
| `steam_cycle_reheat_temperature_C` | constraints_reachable | No additional ruling required | Declined under fixed steam offer |
| `steam_cycle_steam_temperature_C` | constraints_reachable | No additional ruling required | Declined under fixed steam offer |
| `steam_ledger_annual_service_fraction` | constraints_reachable | No additional ruling required | Executed |
| `steam_ledger_capital3` | constraints_reachable | No additional ruling required | Executed |
| `steam_ledger_capital4` | constraints_reachable | No additional ruling required | Executed |
| `steam_ledger_common_source_pv` | constraints_reachable | No additional ruling required | Executed |
| `steam_ledger_controller_capital` | constraints_reachable | No additional ruling required | Executed |
| `steam_ledger_replacement_fraction` | constraints_reachable | No additional ruling required | Executed |
| `steam_transport_costscale` | constraints_reachable | No additional ruling required | Executed |
| `steam_transport_n_loops` | constraints_reachable | No additional ruling required | Executed |
| `steam_transport_salt_pumps_per_circuit` | constraints_reachable | No additional ruling required | Executed |
| `steam_transport_secondary_head` | constraints_reachable | No additional ruling required | Declined under fixed steam offer |
| `steam_transport_selected_salt_design_flow_kg_s` | constraints_reachable | No additional ruling required | Executed |
| `turbine_equipment_price_factor` | constraints_reachable | No additional ruling required | Executed |
| `water_ic1_ua` | constraints_reachable | No additional ruling required | Executed |
| `water_ic2_ua` | constraints_reachable | No additional ruling required | Executed |
| `water_pre_ua` | constraints_reachable | No additional ruling required | Executed |

Monotonicity, identity of the same physical quantity across different names and intra-module operand dependency are not derivable from these indicators. Reachability identifies a possible graph path; it does not establish response or scientific resistance. Financial axes remain sensitivity-framed even where a constraint is reachable.

## 9. Preflight results

Fresh stock integration returns `CANDIDATE` with all ten gates passing on the repaired executable. `preparation/integration_return.json` records their exact scope and producer. The six mechanical preflight gates also pass. `preparation/package_identity.json` and `preparation/baseline_result.json` are local copies of the exact identity and baseline documents read by the gates; their digests are retained in `preparation/preflight_results.json`.

| Gate | Outcome | Detail |
| --- | --- | --- |
| `declared_keys` | pass | 43 declared keys across 43 groups, all package inputs |
| `sibling_scan` | pass | warnings: 12 |
| `identity` | pass | kind sealed, digest 36f653faacc301e76132a9364c1b1024e6d0b3d28742138fcc4759aeef7b3986 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| `manifest_currency` | pass | both recorded package fingerprints match the package on disk |
| `baseline_headline` | pass | component_alternatives__plant__gas_ledger__evaluate__cost_per_net_MWh reproduces at relative deviation 0.000e+00; 36/36 pinned verdicts match |
| `package_clean` | pass | package tree is byte-untouched (git clean) |

The suffix scan has 12 advisory warnings. They refer to separate attributes: inactive branch UA, primary-loop count, controller-loss ratings, branch-specific capital slots and cooling-service conditions. These are not omitted fan-out copies. No declared axis is silently tied to one of them.

| Integration gate | Outcome | Checked scope |
| --- | --- | --- |
| `pinned-packages` | pass | the pinned package revisions and installed wheel artifacts |
| `teax-revision` | pass | the teax checkout's revision against the expected one |
| `regeneration` | pass | regeneration in place moves no package byte |
| `handwritten-preservation` | pass | the handwritten implementations survive regeneration byte for byte |
| `census-snapshot` | pass | the recaptured snapshot and the re-derived entry-point census |
| `model-family-spine` | pass | the canonical tree, the family twins and the tracked census |
| `manifest` | pass | the manifest's schema, package identity and recomputed pin |
| `preflight` | pass | the six mechanical gates a study passes |
| `verification` | pass | oracle parity and re-derived verdicts over an executed store |
| `lineage` | pass | the live fingerprints against the lineage the request named |

Baseline verification is one integration case; §13 records the separate complete-study verification gate.

## 10. Execution route and why

The inherited, previously exercised route is a study-local direct API using stock `StudyRunner` and `PreparedListStrategy`. It supports the explicit coordinated equipment list and selected-anchor sensitivities while retaining the strict loader, evaluator, store and native query lifecycle. All 498 cases completed through this route. `results/execution-context.json` retains the execution and verification commands and revision `cb9cace48efc1b29991712727996a3e0c4ef2580`. The historical missing-import-path launch failure belongs to the original sealed attempt; it is not a failure of this replay.

Glue ledger: none. No runtime adapter supplies missing physics. Model-owned heater, bypass and cooler closures calculate states; the study selects source powers, pressure ratios and declared hardware. Numerical repair changes existing root resolution only.

## 11. Study definition and window provenance

The window is engineered, not a qualified equipment envelope. The 498 complete maps and original core/steam/sensitivity proposal provenance are preserved unchanged. The original scan selected gas anchors from tested passing offers, then selected connector offers for matched sensitivities. Those selections explain the input list; they do not establish the repaired rankings. Fresh independent-oracle rescans completed for the unchanged core, connector and sensitivity proposals. `core-scan.json`, `steam-scan.json` and `sensitivity-scan.json` retain those results; `window.json` records their provenance and duplicate aliases. These scans check the list without reselection or dropping failed offers. Native execution and full verification now confirm the unchanged list; the originally selected anchors remain minima within their exact passing catalogs.

The retained proposal composer chooses inputs without a physical root or automatic sizing calculation. Three duplicate proposed maps remain explicit aliases in the new `window.json`. Every scan point evaluated; there were no body refusals. Undefined cooler roots are retained numerical outputs with failed validity predicates, so absence of a Python refusal does not mean the physical point is supported. The source points are selected operating scenarios of the unchanged loop model under an imposed total-resistance law. They do not demonstrate reactor/plasma turndown or branch-resolved hydraulic qualification. The selected steam offer has fixed rated steam and condenser conditions, so unequal supported operating freedom remains explicit.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint within this replay: no cross-arm correlation is needed. All 498 new cases use the repaired executable. The earlier sealed study remains a separate identity and store. `results/replay-comparison.json` pairs all 498 exact input maps and unchanged qualified predicate identities. It confirms identical output identities, constraint catalog and tolerances, with zero predicate changes. Numeric output changes are recorded separately; no old observation is merged into the new verified store. The unchanged semantic contract permits this bounded comparison; the repair grants no wider physical equivalence claim.

## 13. Verification

**PASS for the complete fresh study.** Stock verification covers all 498 cases and all 872 independently compared scalar channels: 434,256 comparisons. Every one of the 84 predicates is independently rederived for each case, totaling 41,832 verdict checks with zero mismatch. No declared comparison channel is left unverified. `results/verification_summary.json` is the successful release-gate receipt. The old failed record remains sealed and is not retroactively marked verified.

The independent oracle and predeclared tolerances are unchanged. Near-zero residual/fraction channels use their existing named absolute classes; the remaining channels require relative agreement below 1e-9. Four solver iteration outputs are diagnostic-only. A large reported relative deviation near zero is therefore not itself a failure when its predeclared absolute class passes. No physical/equipment predicate has been relaxed.

The earlier 15-case assembled and nine-tuple high-precision checks provide independent evidence for the numerical repair mechanism. The full replay extends acceptance to this unchanged 498-point window. It does not promise relative accuracy for arbitrary nearly zero outputs outside the evidenced inputs. Selected inputs, assumed prices, imposed pressure service, common source premises and supplied property data are not independently qualified scientific facts. Shared authored bindings and operand metadata identify what is compared; the oracle independently calculates the physical and financial channels.

## 14. Review outcomes

| Lens | Verdict | Disposition |
| --- | --- | --- |
| Fourth design, independent non-author reviewer | Inherited PASS | Physical roles, model-owned coupling, MR-7 and bounded additions remain valid because the reviewed equations, domains, roles and offers are unchanged. |
| Original implemented integration | Inherited scoped PASS | Seventeen development cases and static/native evidence remain historical support; their review does not cover fresh full-study numerical results. |
| Bounded numerical repair | PASS | Independent review of core `bf9ebfff` and final evidence committed with `9f32673f`; three local numerical variants, full focused output/predicate verification and preservation checked. |
| Fresh stock integration | CANDIDATE; all ten gates pass | Exact receipts copied under `preparation/`; baseline parity and all six preflight gates pass. This does not release the full study. |
| Full repaired study verification | PASS | All 498 cases, 872 channels and 84 predicates checked with unchanged oracle/tolerances; zero disagreements. |
| Final economic interpretation | PASS before seal | Continuing independent non-author reviewer checks complete verification, matched minima, accounting arithmetic, sensitivities, failed-case/property exclusions and figures. Scientific limitations remain explicit. |

The [archived economic review](results/sources/work/orchestration/goals/design-study-component-alternatives/evidence/repaired-results-review.md) records the pre-seal result assessment. Final hash coverage is a subsequent assurance step; it does not change the scientific interpretation. The repair changes three existing numerical roots, adds zero physical closure definitions and preserves six root occurrences. The updated census explicitly counts seven new/modified handwritten definitions across WI-096. Earlier static-validator limitations remain disclosed; review reuse does not turn that validator into a green aggregate result.

## 15. Findings

Findings below distinguish inherited scientific limits from the completed numerical repair and fresh verified results. New IDs belong to this replay; the original sealed attempt and its findings remain intact. Coordinator owns the discovery-log join.

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| `20260926-design-study-component-alternatives-b#1` | model | Six original mismatches arose in cooler, heater-network and bypass root accuracy, with downstream cancellation and amplification. | Native repair and complete 498-case verification pass. Oracle, tolerances and engineering verdicts unchanged. | [Repair report](results/sources/work/active/WI-096_matched-conversion-subsystems/numerical-repair/report.md) and [independent repair review](results/sources/work/orchestration/goals/design-study-component-alternatives/evidence/numerical-repair-review.md) |
| `20260926-design-study-component-alternatives-b#2` | model | Equipment quotes, installed scope and recurring allowances remain conditional. | Retain explicit price/recurring/common-source sensitivities and correction frontier; no procurement recommendation. | [Comparison contract](results/sources/work/orchestration/goals/design-study-component-alternatives/comparison-contract.md) |
| `20260926-design-study-component-alternatives-b#3` | model | Steam fixed rated conditions and tested gas options have unequal supported operating freedom. | Compare selected steam offer with tested Brayton offers; no equally optimized technology claim. | [Reviewed design](results/sources/work/active/WI-096_matched-conversion-subsystems/design.md) |
| `20260926-design-study-component-alternatives-b#4` | model | Pressure service, machine off-design efficiencies and site hydraulics are imposed scenarios. | Passing implemented predicates do not qualify machinery or hydraulics. | [Reviewed design](results/sources/work/active/WI-096_matched-conversion-subsystems/design.md) |
| `20260926-design-study-component-alternatives-b#5` | model | Cooler property/root validity can exclude a case separately from purchased-equipment insufficiency. | 322 gas-catalog cases have cooler no-root exclusions, 39 additional cases have solved-cooler equipment/coupling failures. Preserve overlaps; no physical-domain expansion. | [Native cases](results/cases.json), [constraint summary](results/constraint-summary.json) and [cooler classifications](results/report/plot-data.json) |
| `20260926-design-study-component-alternatives-b#6` | process | Financial axes can reach constraints without scientific resistance to hypothetical price assumptions. | Keep sensitivity framing and explicit missing cost qualification. | `indicators.json` and `axis-framing.json` |

## 16. Snapshot

- **File:** `snapshot.json`
- **Schema version:** 1
- **SHA256:** `ea6b9de7cf242c88f764a9a997aadd1b6d813560b5c0953e84e63a7aeef9928e`

## 17. What this record does not contain

Complete native results, numerical verification, the initial independent economic review and the immutable snapshot are present. The archived economic review predates the seal. Subsequent final hash assurance is recorded in the external goal review and does not alter sealed artifacts.

The comparison does not contain qualified procurement quotations, validated off-design machinery maps, detailed controller/site hydraulics, reactor/fuel price qualification, whole-plant LCOE or equal optimization of the technologies. Archived sources and runtime identify the executable, while replay still requires the licensed toolchain and specified Python environment. Earlier source audits and rejected designs remain historical evidence; this record archives the relevant inherited reviews, model sources and repair evidence. Formal closure remains absent because the owner retains it.
