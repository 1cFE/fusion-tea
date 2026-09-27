# Selected steam offer versus tested Brayton offers

**Blocked at numerical verification.** This sealed attempt preserves executed evidence; it is not a released economic comparison. Formal goal and work-item closure remain owner-held.

## 1. Study header

- **Study id:** `20260926-design-study-component-alternatives`
- **Package:** `component_alternatives_tea`
- **Date executed:** 2026-09-26
- **Executor:** Goal coordinator `/root`
- **Mode:** execute; stopped at verification
- **Arm:** `arm-matched-offers`

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


## 3. Objective and result

The native objectives are `component_alternatives__plant__steam_ledger__evaluate__cost_per_net_MWh` and `component_alternatives__plant__gas_ledger__evaluate__cost_per_net_MWh`, in USD2025 per net MWh. These include the conversion subsystem and its connecting equipment, with common finance and source conditions.

All 498 distinct points completed; 83 pass every implemented predicate. Full numerical verification failed. Six cases disagree beyond predeclared tolerances, including two otherwise-passing efficiency sensitivities. Native output and cost plots are diagnostic, unreleased results. They cannot establish a completed economic ranking.

`results/cases.json` and `results/cases.csv` retain every input, output and predicate. `results/verification-diagnostics.json` identifies the numerical qualifications by case. No failed point was deleted.

## 4. Constraint outcomes

All 84 executing checks are listed below. Counts refer to the 498 native cases. Zero indeterminate verdicts occurred. Independent diagnostic re-derivation agrees with every predicate, but that does not override six numerical failures. Case attribution is in `results/constraint-summary.json`.

| `constraint_id` | `source_local_identity` | Satisfied | Violated |
|---|---|---:|---:|
| `component_alternatives__plant__water_ic1__evaluation_defined_ok__49d1611637350e3c` | `evaluation_defined_ok` | 333 | 165 |
| `component_alternatives__plant__water_ic1__flow_margin_ok__2ca46da8d6c9fc06` | `flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__water_ic1__duty_margin_ok__ae893105fd8169d4` | `duty_margin_ok` | 498 | 0 |
| `component_alternatives__plant__water_ic1__power_margin_ok__ceac76348e0eb2b6` | `power_margin_ok` | 498 | 0 |
| `component_alternatives__plant__salt_flow_capacity__capacity_requirement__1f3f2b5125f26aed` | `capacity_requirement` | 451 | 47 |
| `component_alternatives__plant__steam_feed_flow_capacity__capacity_requirement__f522084f390b88ed` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__gas_boundary__bypass_flow_margin_ok__840f5556c962fa45` | `bypass_flow_margin_ok` | 495 | 3 |
| `component_alternatives__plant__gas_boundary__controller_capacity_ok_ok__3c7a992b7ef572ac` | `controller_capacity_ok_ok` | 495 | 3 |
| `component_alternatives__plant__gas_boundary__bypass_fraction_margin_ok__7197bb376c493e60` | `bypass_fraction_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_boundary__pressure_margin_ok__023a9033fbabc01f` | `pressure_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_boundary__total_flow_margin_ok__e4fcc2a2f41664a0` | `total_flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_boundary__exchanger_flow_margin_ok__586a84274fb7f1fb` | `exchanger_flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_boundary__added_dp_margin_ok__daebd77c6cb6ed86` | `added_dp_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_boundary__temperature_margin_ok__b9e59d1aa293995e` | `temperature_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_boundary__source_adequate_ok__dd6d7a3461399330` | `source_adequate_ok` | 281 | 217 |
| `component_alternatives__plant__water_ic2__duty_margin_ok__8546438198d8a311` | `duty_margin_ok` | 498 | 0 |
| `component_alternatives__plant__water_ic2__evaluation_defined_ok__06ab6aea3f7f761b` | `evaluation_defined_ok` | 333 | 165 |
| `component_alternatives__plant__water_ic2__power_margin_ok__9155c8131175c99b` | `power_margin_ok` | 498 | 0 |
| `component_alternatives__plant__water_ic2__flow_margin_ok__a1238658a4279d69` | `flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_ledger__net_positive__7be67634b73dc5d3` | `net_positive` | 498 | 0 |
| `component_alternatives__plant__steam_ledger__balance__79e79cd29079c8e8` | `balance` | 498 | 0 |
| `component_alternatives__plant__recuperator_duty_capacity__capacity_requirement__37716788614d63a8` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__steam_condensate_electric_capacity__capacity_requirement__7f87933904cdde5d` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_hp_flow_capacity__capacity_requirement__7d80da68d49ab07e` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__he_capacity__capacity_ok__3993dc4f00da3840` | `capacity_ok` | 498 | 0 |
| `component_alternatives__plant__gas_loss_duty_capacity__capacity_requirement__3f4fdc86d64b5036` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__salt_electric_capacity__capacity_requirement__d0a6e35468ded9cc` | `capacity_requirement` | 451 | 47 |
| `component_alternatives__plant__steam_lp_shaft_capacity__capacity_requirement__145e6e0999fc7f4f` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_gross_capacity__capacity_requirement__4252a99565636ed5` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_rejection_capacity__capacity_requirement__ed5a57ebe998f809` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__steam_condenser_capacity__capacity_requirement__67922fb363412df0` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_lp_flow_capacity__capacity_requirement__704e61a5a8c7bf24` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__gas_loss_electric_capacity__capacity_requirement__6a158987313c84e0` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__steam_reheat_ua_capacity__capacity_requirement__ff5775187764fbbd` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_boundary__source_adequate_ok__eaa371ee289234f1` | `source_adequate_ok` | 474 | 24 |
| `component_alternatives__plant__steam_boundary__exchanger_flow_margin_ok__b6c20f51b00f7b9c` | `exchanger_flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__added_dp_margin_ok__f0c716d635261219` | `added_dp_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__bypass_flow_margin_ok__8f1459a694a0757a` | `bypass_flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__total_flow_margin_ok__e80a0efbac0d3f57` | `total_flow_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__controller_capacity_ok_ok__d8dd67a24704a1c0` | `controller_capacity_ok_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__temperature_margin_ok__39291a564826dd0f` | `temperature_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__bypass_fraction_margin_ok__32cff09a266a19fc` | `bypass_fraction_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_boundary__pressure_margin_ok__177980a50b09bf98` | `pressure_margin_ok` | 498 | 0 |
| `component_alternatives__plant__steam_hp_shaft_capacity__capacity_requirement__08512b73f01b2ff4` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_water_flow_capacity__capacity_requirement__f3bfd573273dc22e` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__gas_loss_flow_capacity__capacity_requirement__8a2d8de72c5b2880` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__turbine_capacity__capacity_ok__0178c1184c793932` | `capacity_ok` | 498 | 0 |
| `component_alternatives__plant__steam_condensate_pressure_capacity__capacity_requirement__d523b96c0c76de1b` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_water__cooling_approach_ok_required__c8a5d75f54ded9d6` | `cooling_approach_ok_required` | 498 | 0 |
| `component_alternatives__plant__generator_capacity__capacity_ok__ee0395479decdfc2` | `capacity_ok` | 498 | 0 |
| `component_alternatives__plant__salt_shaft_capacity__capacity_requirement__419a029d2df87f3c` | `capacity_requirement` | 451 | 47 |
| `component_alternatives__plant__source_checks__flow_ok__d77445a069dcb805` | `flow_ok` | 498 | 0 |
| `component_alternatives__plant__source_checks__pressure_ok__aa0a62a144e9c75d` | `pressure_ok` | 498 | 0 |
| `component_alternatives__plant__gas_loss_water__cooling_approach_ok_required__6112b029bb4ede08` | `cooling_approach_ok_required` | 498 | 0 |
| `component_alternatives__plant__rejection_capacity__capacity_requirement__8eab7ec16a8b759e` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__steam_feed_electric_capacity__capacity_requirement__02f57441b4cf6746` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_water_electric_capacity__capacity_requirement__79eb129457bf9d3d` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__compressor_capacity__capacity_ok__e8c94ef170d28993` | `capacity_ok` | 468 | 30 |
| `component_alternatives__plant__salt_fill_capacity__capacity_requirement__0d36a52c336754e3` | `capacity_requirement` | 498 | 0 |
| `component_alternatives__plant__steam_feed_pressure_capacity__capacity_requirement__2b0a04222feb552b` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_main_ua_capacity__capacity_requirement__c2efdc04c52106da` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_condensate_flow_capacity__capacity_requirement__a06233d7139b47ec` | `capacity_requirement` | 474 | 24 |
| `component_alternatives__plant__steam_transport__motor_factor_ok_required__eed87936beb69817` | `motor_factor_ok_required` | 474 | 24 |
| `component_alternatives__plant__steam_transport__design_motor_factor_ok_required__4a9e97f942584206` | `design_motor_factor_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__design_pump_size_ok_required__39419b9b933c2a99` | `design_pump_size_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__design_pump_type_ok_required__86fcc6e00c250519` | `design_pump_type_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__pump_type_ok_required__a1706d503ff60f4c` | `pump_type_ok_required` | 464 | 34 |
| `component_alternatives__plant__steam_transport__pump_size_ok_required__b3af0a8e326050b1` | `pump_size_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__ihx_capacity_ok_required__a8ade32d723ec9f2` | `ihx_capacity_ok_required` | 474 | 24 |
| `component_alternatives__plant__steam_transport__salt_head_ok_required__9049eef128641767` | `salt_head_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__design_motor_base_ok_required__34d2455206f46357` | `design_motor_base_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__salt_flow_regime_ok_required__6e2b05d56b7bbfaf` | `salt_flow_regime_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_transport__motor_base_ok_required__238e695ccdaf5ebf` | `motor_base_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_conditions__supported_required__92a5d05764f5fff9` | `supported_required` | 474 | 24 |
| `component_alternatives__plant__water_pre__power_margin_ok__d793d504da406d97` | `power_margin_ok` | 492 | 6 |
| `component_alternatives__plant__water_pre__flow_margin_ok__129a83656acb8a06` | `flow_margin_ok` | 489 | 9 |
| `component_alternatives__plant__water_pre__evaluation_defined_ok__bc4741b386520ff5` | `evaluation_defined_ok` | 211 | 287 |
| `component_alternatives__plant__water_pre__duty_margin_ok__80af75533d32b208` | `duty_margin_ok` | 498 | 0 |
| `component_alternatives__plant__gas_ledger__net_positive__ee25ae39167c9ad3` | `net_positive` | 497 | 1 |
| `component_alternatives__plant__gas_ledger__balance__a530b58ca455c8b8` | `balance` | 176 | 322 |
| `component_alternatives__plant__steam_cycle__main_ua_available_required__6cdb52b3bf9953e0` | `main_ua_available_required` | 498 | 0 |
| `component_alternatives__plant__steam_cycle__reheat_admission_ok_required__e88f7416d91d86fd` | `reheat_admission_ok_required` | 498 | 0 |
| `component_alternatives__plant__steam_cycle__reheat_ua_available_required__1e1158ef6871602d` | `reheat_ua_available_required` | 498 | 0 |
| `component_alternatives__plant__steam_cycle__main_admission_ok_required__dbbd20ff9c7f4317` | `main_admission_ok_required` | 498 | 0 |

## 5. Framing

[AGENT] Proposed framings are retained as judged; none changed after execution. Search means selection from the finite explicit catalog, not continuous optimization. Sensitivities remain hypothetical scenarios. Thirty-nine attributes varied; four traced directions remained declined.

| Axis | Proposed | Judged | Executed variation |
|---|---|---|---|
| `blanket_source_q_source` | sensitivity | sensitivity | yes |
| `cycle_selected_flow` | search | search | yes |
| `compressor_1_selected_ratio` | search | search | yes |
| `compressor_1_efficiency` | sensitivity | sensitivity | yes |
| `compressor_2_selected_ratio` | search | search | yes |
| `compressor_2_efficiency` | sensitivity | sensitivity | yes |
| `compressor_3_selected_ratio` | search | search | yes |
| `compressor_3_efficiency` | sensitivity | sensitivity | yes |
| `cycle_turbine_efficiency` | sensitivity | sensitivity | yes |
| `water_ic1_ua` | search | search | yes |
| `water_ic2_ua` | search | search | yes |
| `water_pre_ua` | search | search | yes |
| `recuperator_hardware_ua` | search | search | yes |
| `steam_transport_n_loops` | search | search | yes |
| `steam_transport_salt_pumps_per_circuit` | search | search | yes |
| `steam_transport_selected_salt_design_flow_kg_s` | search | search | yes |
| `steam_boundary_bypass_flow_rating` | sensitivity | sensitivity | yes |
| `steam_ledger_controller_capital` | sensitivity | sensitivity | yes |
| `steam_ledger_annual_service_fraction` | sensitivity | sensitivity | yes |
| `steam_ledger_replacement_fraction` | sensitivity | sensitivity | yes |
| `steam_ledger_common_source_pv` | sensitivity | sensitivity | yes |
| `gas_boundary_bypass_flow_rating` | sensitivity | sensitivity | yes |
| `gas_ledger_controller_capital` | sensitivity | sensitivity | yes |
| `gas_ledger_annual_service_fraction` | sensitivity | sensitivity | yes |
| `gas_ledger_replacement_fraction` | sensitivity | sensitivity | yes |
| `gas_ledger_common_source_pv` | sensitivity | sensitivity | yes |
| `compressor_equipment_price_factor` | sensitivity | sensitivity | yes |
| `turbine_equipment_price_factor` | sensitivity | sensitivity | yes |
| `generator_equipment_price_factor` | sensitivity | sensitivity | yes |
| `he_hx_price_factor` | sensitivity | sensitivity | yes |
| `he_duty_equipment_price_factor` | sensitivity | sensitivity | yes |
| `conversion_services_price_factor` | sensitivity | sensitivity | yes |
| `heat_rejection_equipment_price_factor` | sensitivity | sensitivity | yes |
| `gas_ledger_capital9` | sensitivity | sensitivity | yes |
| `steam_ledger_capital3` | sensitivity | sensitivity | yes |
| `steam_ledger_capital4` | sensitivity | sensitivity | yes |
| `steam_transport_costscale` | sensitivity | sensitivity | yes |
| `steam_cycle_eta_hp` | sensitivity | sensitivity | yes |
| `steam_cycle_eta_lp` | sensitivity | sensitivity | yes |
| `steam_cycle_steam_temperature_C` | sensitivity | sensitivity | declined |
| `steam_cycle_reheat_temperature_C` | sensitivity | sensitivity | declined |
| `steam_cycle_condenser_temperature_C` | sensitivity | sensitivity | declined |
| `steam_transport_secondary_head` | sensitivity | sensitivity | declined |

## 6. Per-axis account

`results/axis-assessment.json` records every tested value, its case identities and the number satisfying all implemented checks. The following compact account uses the same order as those values. Coordinated offers vary several attributes together; grouped counts do not identify an isolated causal effect. The comparison and sensitivity figures use matched cases and carry the verification block.

| Axis | Tested values | Predicate-passing / evaluated at each value | Account |
|---|---|---|---|
| `blanket_source_q_source` | 2500, 2800, 3000 | 35/166, 26/166, 22/166 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `cycle_selected_flow` | 1500, 1750, 2000, 2250, 2500 | 0/75, 28/116, 54/157, 1/75, 0/75 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `compressor_1_selected_ratio` | 1.2, 1.35, 1.5, 1.65, 1.8 | 0/75, 0/75, 29/116, 23/116, 31/116 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `compressor_1_efficiency` | 0.86, 0.89, 0.92 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `compressor_2_selected_ratio` | 1.2, 1.35, 1.5, 1.65, 1.8 | 0/75, 0/75, 29/116, 23/116, 31/116 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `compressor_2_efficiency` | 0.86, 0.89, 0.92 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `compressor_3_selected_ratio` | 1.2, 1.35, 1.5, 1.65, 1.8 | 0/75, 0/75, 29/116, 23/116, 31/116 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `compressor_3_efficiency` | 0.86, 0.89, 0.92 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `cycle_turbine_efficiency` | 0.9, 0.93, 0.96 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `water_ic1_ua` | 25, 30, 40 | 83/348, 0/75, 0/75 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `water_ic2_ua` | 25, 30, 40 | 83/348, 0/75, 0/75 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `water_pre_ua` | 20, 25, 40, 50, 60 | 2/75, 81/198, 0/75, 0/75, 0/75 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `recuperator_hardware_ua` | 60, 80 | 83/423, 0/75 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `steam_transport_n_loops` | 10, 11, 12, 14 | 19/36, 21/36, 5/18, 38/408 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `steam_transport_salt_pumps_per_circuit` | 2, 3, 4 | 0/24, 22/42, 61/432 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `steam_transport_selected_salt_design_flow_kg_s` | 225, 250 | 43/72, 40/426 | Discrete catalog evidence only. Coordinated changes in other attributes prevent interpreting grouped counts as an isolated causal effect. |
| `steam_boundary_bypass_flow_rating` | 500, 2000 | 3/3, 80/495 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_ledger_controller_capital` | 5e+06, 8e+06, 1e+07, 1.5e+07 | 6/6, 3/3, 68/483, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_ledger_annual_service_fraction` | 0.01, 0.02, 0.03 | 3/3, 77/492, 3/3 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_ledger_replacement_fraction` | 0.1, 0.2, 0.3 | 3/3, 77/492, 3/3 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_ledger_common_source_pv` | 0, 5e+08, 2e+09 | 77/492, 3/3, 3/3 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `gas_boundary_bypass_flow_rating` | 500, 2000 | 0/3, 83/495 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `gas_ledger_controller_capital` | 5e+06, 8e+06, 1e+07, 1.5e+07 | 6/6, 0/3, 71/483, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `gas_ledger_annual_service_fraction` | 0.01, 0.02, 0.03 | 3/3, 77/492, 3/3 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `gas_ledger_replacement_fraction` | 0.1, 0.2, 0.3 | 3/3, 77/492, 3/3 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `gas_ledger_common_source_pv` | 0, 5e+08, 2e+09 | 77/492, 3/3, 3/3 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `compressor_equipment_price_factor` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `turbine_equipment_price_factor` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `generator_equipment_price_factor` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `he_hx_price_factor` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `he_duty_equipment_price_factor` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `conversion_services_price_factor` | 0.5, 1, 1.25, 1.5 | 6/6, 71/336, 0/75, 6/81 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `heat_rejection_equipment_price_factor` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `gas_ledger_capital9` | 4.29665e+07, 8.5933e+07, 1.289e+08 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_ledger_capital3` | 1.23732e+08, 2.47464e+08, 3.71197e+08 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_ledger_capital4` | 5.79698e+07, 1.1594e+08, 1.73909e+08 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_transport_costscale` | 0.5, 1, 1.5 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_cycle_eta_hp` | 0.87, 0.9, 0.93 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_cycle_eta_lp` | 0.87, 0.9, 0.93 | 6/6, 71/486, 6/6 | Hypothetical scenario response at selected anchors; no boundary claim. Coordinated attribute changes are identified in proposed-points.json. |
| `steam_cycle_steam_temperature_C` | 445 | 83/498 | Declined under the held steam offer; no varied native point or boundary claim. |
| `steam_cycle_reheat_temperature_C` | 445 | 83/498 | Declined under the held steam offer; no varied native point or boundary claim. |
| `steam_cycle_condenser_temperature_C` | 42 | 83/498 | Declined under the held steam offer; no varied native point or boundary claim. |
| `steam_transport_secondary_head` | 40 | 83/498 | Declined under the held steam offer; no varied native point or boundary claim. |

The gas catalog has 14 passing cases of 375, below the policy H1 search band of 5–95%. This is a negative result for that hypothesis, not evidence of an equality over chosen source/ratio inputs. Cooler property/root validity and source/capacity requirements account for the failures. Steam connector offers pass in 21 of 72 scans. The 54 sensitivity/controller proposals yield 51 passing cases; three undersized gas bypass offers fail. All scan cases evaluated, and only three exact duplicates were removed from native execution with aliases retained.

## 7. Axis groups

Every axis is a single SysML attribute with its complete emitted entry-key group. `axes.json` retains all 43 groups and provenance. Equal compressor ratios and common financial choices are coordinated scenario selections, not inferred physical identities.

| Axis | Complete key | Provenance |
|---|---|---|
| `blanket_source_q_source` | `component_alternatives__plant__blanket_source__q_source` | fan_out |
| `cycle_selected_flow` | `component_alternatives__plant__cycle__selected_flow` | fan_out |
| `compressor_1_selected_ratio` | `component_alternatives__plant__compressor_1__selected_ratio` | fan_out |
| `compressor_1_efficiency` | `component_alternatives__plant__compressor_1__efficiency` | fan_out |
| `compressor_2_selected_ratio` | `component_alternatives__plant__compressor_2__selected_ratio` | fan_out |
| `compressor_2_efficiency` | `component_alternatives__plant__compressor_2__efficiency` | fan_out |
| `compressor_3_selected_ratio` | `component_alternatives__plant__compressor_3__selected_ratio` | fan_out |
| `compressor_3_efficiency` | `component_alternatives__plant__compressor_3__efficiency` | fan_out |
| `cycle_turbine_efficiency` | `component_alternatives__plant__cycle__turbine_efficiency` | fan_out |
| `water_ic1_ua` | `component_alternatives__plant__water_ic1__ua` | fan_out |
| `water_ic2_ua` | `component_alternatives__plant__water_ic2__ua` | fan_out |
| `water_pre_ua` | `component_alternatives__plant__water_pre__ua` | fan_out |
| `recuperator_hardware_ua` | `component_alternatives__plant__recuperator_hardware__ua` | fan_out |
| `steam_transport_n_loops` | `component_alternatives__plant__steam_transport__n_loops` | fan_out |
| `steam_transport_salt_pumps_per_circuit` | `component_alternatives__plant__steam_transport__salt_pumps_per_circuit` | fan_out |
| `steam_transport_selected_salt_design_flow_kg_s` | `component_alternatives__plant__steam_transport__selected_salt_design_flow_kg_s` | fan_out |
| `steam_boundary_bypass_flow_rating` | `component_alternatives__plant__steam_boundary__bypass_flow_rating` | fan_out |
| `steam_ledger_controller_capital` | `component_alternatives__plant__steam_ledger__controller_capital` | fan_out |
| `steam_ledger_annual_service_fraction` | `component_alternatives__plant__steam_ledger__annual_service_fraction` | fan_out |
| `steam_ledger_replacement_fraction` | `component_alternatives__plant__steam_ledger__replacement_fraction` | fan_out |
| `steam_ledger_common_source_pv` | `component_alternatives__plant__steam_ledger__common_source_pv` | fan_out |
| `gas_boundary_bypass_flow_rating` | `component_alternatives__plant__gas_boundary__bypass_flow_rating` | fan_out |
| `gas_ledger_controller_capital` | `component_alternatives__plant__gas_ledger__controller_capital` | fan_out |
| `gas_ledger_annual_service_fraction` | `component_alternatives__plant__gas_ledger__annual_service_fraction` | fan_out |
| `gas_ledger_replacement_fraction` | `component_alternatives__plant__gas_ledger__replacement_fraction` | fan_out |
| `gas_ledger_common_source_pv` | `component_alternatives__plant__gas_ledger__common_source_pv` | fan_out |
| `compressor_equipment_price_factor` | `component_alternatives__plant__compressor_equipment__price_factor` | fan_out |
| `turbine_equipment_price_factor` | `component_alternatives__plant__turbine_equipment__price_factor` | fan_out |
| `generator_equipment_price_factor` | `component_alternatives__plant__generator_equipment__price_factor` | fan_out |
| `he_hx_price_factor` | `component_alternatives__plant__he_hx__price_factor` | fan_out |
| `he_duty_equipment_price_factor` | `component_alternatives__plant__he_duty_equipment__price_factor` | fan_out |
| `conversion_services_price_factor` | `component_alternatives__plant__conversion_services__price_factor` | fan_out |
| `heat_rejection_equipment_price_factor` | `component_alternatives__plant__heat_rejection_equipment__price_factor` | fan_out |
| `gas_ledger_capital9` | `component_alternatives__plant__gas_ledger__capital9` | fan_out |
| `steam_ledger_capital3` | `component_alternatives__plant__steam_ledger__capital3` | fan_out |
| `steam_ledger_capital4` | `component_alternatives__plant__steam_ledger__capital4` | fan_out |
| `steam_transport_costscale` | `component_alternatives__plant__steam_transport__costscale` | fan_out |
| `steam_cycle_eta_hp` | `component_alternatives__plant__steam_cycle__eta_hp` | fan_out |
| `steam_cycle_eta_lp` | `component_alternatives__plant__steam_cycle__eta_lp` | fan_out |
| `steam_cycle_steam_temperature_C` | `component_alternatives__plant__steam_cycle__steam_temperature_C` | fan_out |
| `steam_cycle_reheat_temperature_C` | `component_alternatives__plant__steam_cycle__reheat_temperature_C` | fan_out |
| `steam_cycle_condenser_temperature_C` | `component_alternatives__plant__steam_cycle__condenser_temperature_C` | fan_out |
| `steam_transport_secondary_head` | `component_alternatives__plant__steam_transport__secondary_head` | fan_out |

## 8. Indicators and rulings

All 43 proposed axes, including the four declined directions, were traced. Every result is `constraints_reachable`; no `no_constraint_response` axis exists, no subset was used, and no new owner ruling is required. `indicators.json` preserves exact paths and evidence.

Not derivable: monotonicity, identity of the same physical quantity across differing names, and intra-module operand dependency. A reachable constraint is a possible graph path, not evidence that it responds. Financial assumptions remain sensitivity-framed under the owner's requested price/fuel sensitivity. Their missing procurement qualification is a finding, even though the graph reports reachability.

## 9. Preflight results

All gates ran on the promoted package. `preparation/package_identity.json` and `preparation/baseline_result.json` are local copies of the exact gate inputs; their digests are in `preparation/preflight_results.json`. `preparation/integration_return.json` preserves all ten integration gates.

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 43 declared keys across 43 groups, all package inputs |
| sibling_scan | pass | warnings: 12 |
| identity | pass | kind sealed, digest 14dddcfe3b0af047b18064f7c284b6739a633f20777558b304c37f6637a372a3 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | component_alternatives__plant__gas_ledger__evaluate__cost_per_net_MWh reproduces at relative deviation 0.000e+00; 36/36 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The suffix scan has 12 advisory warnings. They are different attributes (inactive branch UA, primary loop count and controller-loss ratings), not missing fan-out copies. The declared groups map the actual authored attributes; no sweep key was silently tied to those siblings.

## 10. Execution route and why

The study-local direct API uses stock `StudyRunner` and `PreparedListStrategy` because the list combines explicit coordinated equipment offers with selected-anchor sensitivities. The strict package loader, evaluator, store and query retain the native lifecycle. The matching physical calculations live in the model. Glue ledger: none; no runtime adapter.

The first launch lacked the documented TEAx import root and stopped before creating a native store. `preparation/execution-attempt1/` preserves that attempt. Retry 1 used the documented environment with the same 498 points and package. `results/execution-context.json` records exact commands and revision. No physical or metadata change was needed for the retry.

## 11. Study definition and window provenance

The window is engineered, not a qualified equipment envelope. `proposals.py` in the archived sources composes independently chosen inputs without a physical root or equipment sizing calculation. Core, steam and sensitivity oracle scans all completed before native execution. Every evaluated offer, including engineering failures, entered the native list; three exact duplicate points have explicit aliases in `window.json`. No body refusal occurred in these scans. Earlier development property refusals remain in the WI-096 evidence.

The best tested passing gas offer at each source anchored the steam connector scan. The least-cost passing connector then anchored the sensitivities. This is discrete offer selection; it does not establish equal optimization of the technologies. The common 14-circuit steam curve remains visible separately. The scan fixes a finite list, not a continuous feasible boundary or global optimum. Every tested value and generating choice is retained in the proposal files and snapshot window.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint: no cross-arm correlation needed. Every native case uses the same executable identity and model contract. Earlier development diagnostics and prior goal studies are historical evidence; none is merged into this store or treated as a matched main-study observation.

## 13. Verification

**Failed; dependent completion stopped.** The stock verifier requested all 498 cases and stopped at its first numerical disagreement. `results/verification-attempt1-failure.json` retains the exact case and outputs. `results/verification-blocker.json` records the disposition. There is no successful `verification_summary.json` for this study.

Post-failure diagnostics compared 872 channels and independently re-derived all 84 predicates in each case. Six cases exceed unchanged predeclared tolerances; zero predicates disagree. These diagnostics inventory the failure and do not replace the stock verifier's release gate. Four solver iteration counts are diagnostic-only and excluded. Chosen inputs, assumed prices, imposed pressure service and supplied property data are common premises, not independently validated scientific facts.

The independent reviewer used a 60-digit cooler calculation at the exact native gas tuple. It agrees with the oracle; the native cooler's residual stopping rule permits amplified flow and pump error at a small water temperature rise. No oracle error was demonstrated. Required native numerical repair/new executable revalidation or new tolerance authority is outside this continuation. No model, tolerance or case selection was changed after the failure.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Fourth design, continuing independent reviewer | PASS | Reviewed physical roles, MR-7, five substantive bodies and one newly written iterative cooler family; scope authorized. |
| Implemented integration, same non-author reviewer | PASS at WI-096 `29dcb5d8` | Reused exact implementation, 17-case numerical and predicate evidence; this does not cover all main-study points. |
| Stock integration seam | CANDIDATE, ten gates pass | Exact promoted identity retained. |
| Full study verification | FAIL | Six numerical mismatch cases identified; none removed. |
| Independent failure assessment | FINDINGS / stop | Accurate independent cooler root identifies native numerical accuracy dependency. |

Review artifacts and the original design/spec are copied under `results/sources/` at sealing. Final assurance of the blocked answer is recorded in the goal trail; it cannot convert this failure into a verification pass.

## 15. Findings

First sightings are joined to `DISCOVERY_LOG.md` by the following IDs. Every finding has a retained home; future model work remains owner-held.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260926-design-study-component-alternatives#1` | model | Native cooler stopping accuracy exceeds the numerical verification tolerance in six cases, including two predicate-passing sensitivities. | Blocked; independent review confirms native accuracy dependency. No repair or waiver in this run. | `work/orchestration/goals/design-study-component-alternatives/evidence/verification-failure-review.md` |
| `20260926-design-study-component-alternatives#2` | model | Equipment prices, installed scope, service allowances and replacement costs remain conditional; hypothetical quote changes can alter the comparison. | Declared seam; withheld procurement recommendation and retained cost-correction frontier. | `work/orchestration/goals/design-study-component-alternatives/comparison-contract.md` |
| `20260926-design-study-component-alternatives#3` | model | The fixed steam turbine offer and tested gas choices have unequal supported operating freedom. | Declared seam; comparison is selected steam versus tested Brayton offers only. | `work/active/WI-096_matched-conversion-subsystems/design.md` |
| `20260926-design-study-component-alternatives#4` | model | Controller pressure service, machine efficiencies and detailed site hydraulics lack qualification. | Declared seam; modeled checks do not establish operating or procurement qualification. | `work/active/WI-096_matched-conversion-subsystems/design.md` |
| `20260926-design-study-component-alternatives#5` | model | Only 14 of 375 gas catalog combinations pass all checks (3.73%); finite-water property/root limits reject many combinations. | Declared seam; H1 search feasible-fraction hypothesis is falsified for this catalog. No continuous boundary inferred. | `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/constraint-summary.json` |
| `20260926-design-study-component-alternatives#6` | process | Direct study launch initially lacked the documented TEAx import path and stopped before evaluation. | Resolved operationally; same points and package run with the documented environment. | `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/preparation/execution-attempt1/failure.txt` |
| `20260926-design-study-component-alternatives#7` | process | Reachable-constraint indicators on financial axes do not prove physical resistance to price assumptions. | Declared seam; all financial changes remain sensitivity-framed, with no optimization claim. | `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/axis-assessment.json` |

## 16. Snapshot

- **File:** `snapshot.json`
- **Status:** blocked-at-verification evidence seal; `released: false`
- **Schema version:** 1 with explicit failed-verification fields
- **SHA256:** `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`

The snapshot preserves the actual failure. Its verification summary digest is null because no passing summary exists; the failure and full diagnostic artifacts have their own digests. This is an explicit blocked-record exception in shape, not a policy exception permitting execution or release.

## 17. What this record does not contain

There is no passing full-study verification summary, released economic recommendation, qualified procurement quotation, validated machinery map, detailed controller/site hydraulic design, reactor/fuel price model, or equally optimized technology comparison. The sealed runtime and independent oracle are included; their external licensed toolchain and Python environment must still be provided for replay.

Historical source audits, rejected designs and earlier failed native attempts remain in the goal and WI-096 history. This record copies the specific reviewed design, implementation, failure evidence and executed package needed to identify this attempt; it does not duplicate the entire project history. Formal closure is absent because the owner retains it.
