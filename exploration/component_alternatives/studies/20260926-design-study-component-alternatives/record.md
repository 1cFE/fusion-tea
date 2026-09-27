# Selected steam offer versus tested Brayton offers

Draft study record. Preparation is authorized; native execution awaits implementation validation and independent integration review. This is a conversion-subsystem comparison at matched source conditions.

## 1. Study header

- **Study id:** `20260926-design-study-component-alternatives`
- **Package:** `component_alternatives_tea`
- **Date executed:** Not executed
- **Executor:** Goal coordinator `/root`
- **Mode:** execute
- **Arms:** single arm

Arms are variants of the same question, run to be compared. Two studies asking different questions of the same package are two records, not two arms of one.

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

- **Conversion-subsystem cost-per-net-MWh objective channel(s):** `<qualified channel name(s)>`
- **Conversion-subsystem cost-per-net-MWh result:** `<value with units, and what point or region it belongs to>`

`<one or two sentences: what the objective did over the studied space>`

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `<qualified id>` | `<local identity>` | `<satisfied \| violated \| indeterminate>` | `<where and why, one line>` |

A short display name is not a qualified identity. If the executed artifacts carry only the short name, the qualified identity was dropped on export and recovering it is part of this section, not optional.

## 5. Framing

[AGENT] Proposed framing, before the oracle window scan and native study. Coordinated offer selections remain explicit choices.

| Axis | Framing proposed | Why |
|---|---|---|
| `blanket_source_q_source` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `cycle_selected_flow` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `compressor_1_selected_ratio` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `compressor_1_efficiency` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `compressor_2_selected_ratio` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `compressor_2_efficiency` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `compressor_3_selected_ratio` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `compressor_3_efficiency` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `cycle_turbine_efficiency` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `water_ic1_ua` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `water_ic2_ua` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `water_pre_ua` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `recuperator_hardware_ua` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `steam_transport_n_loops` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `steam_transport_salt_pumps_per_circuit` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `steam_transport_selected_salt_design_flow_kg_s` | search | Test operating and installed-offer choices in the declared discrete catalog. |
| `steam_boundary_bypass_flow_rating` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_ledger_controller_capital` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_ledger_annual_service_fraction` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_ledger_replacement_fraction` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_ledger_common_source_pv` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `gas_boundary_bypass_flow_rating` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `gas_ledger_controller_capital` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `gas_ledger_annual_service_fraction` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `gas_ledger_replacement_fraction` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `gas_ledger_common_source_pv` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `compressor_equipment_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `turbine_equipment_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `generator_equipment_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `he_hx_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `he_duty_equipment_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `conversion_services_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `heat_rejection_equipment_price_factor` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `gas_ledger_capital9` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_ledger_capital3` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_ledger_capital4` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_transport_costscale` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_cycle_eta_hp` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_cycle_eta_lp` | sensitivity | Describe a response at matched source conditions; no boundary claim. |
| `steam_cycle_steam_temperature_C` | sensitivity | Declared and traced, then declined because the held steam offer does not support the changed condition. |
| `steam_cycle_reheat_temperature_C` | sensitivity | Declared and traced, then declined because the held steam offer does not support the changed condition. |
| `steam_cycle_condenser_temperature_C` | sensitivity | Declared and traced, then declined because the held steam offer does not support the changed condition. |
| `steam_transport_secondary_head` | sensitivity | Declared and traced, then declined because the held steam offer does not support the changed condition. |

As judged after the run: pending execution.

## 6. Per-axis account

One pair of subsections per axis. Both ship present; the `**Applies:**` line discharges the one the axis's framing does not owe.

#### `<axis>` — feasible structure (search framing)
**Applies:** `<yes \| not applicable — this axis is sensitivity-framed>`

`<which constraint is active, where the boundary sits, whether a constrained optimum was found and where>`

#### `<axis>` — observed response (sensitivity framing)
**Applies:** `<yes \| not applicable — this axis is search-framed>`

`<the observed response; an explicit statement that no boundary claim is made; and, for any constraint that goes violated anywhere in the sweep, where in the swept space it does — locating a violation is a fact about the run, not a boundary claim>`

## 7. Axis groups

Each group is the complete emitted key set for one SysML attribute. Multi-attribute equipment offers are coordinated proposals, with each constituent attribute declared separately. No additional physical identity is inferred.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
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

The stock indicator run covers all 43 declared groups, including all four declined directions. Every group is valid and `constraints_reachable`; there are no suffix-sibling warnings. No group reports `no_constraint_response`, so that indicator creates no pending owner gate.

| Axis | Indicator | Ruling / disposition |
|---|---|---|
| `blanket_source_q_source` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `cycle_selected_flow` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `compressor_1_selected_ratio` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `compressor_1_efficiency` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `compressor_2_selected_ratio` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `compressor_2_efficiency` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `compressor_3_selected_ratio` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `compressor_3_efficiency` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `cycle_turbine_efficiency` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `water_ic1_ua` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `water_ic2_ua` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `water_pre_ua` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `recuperator_hardware_ua` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `steam_transport_n_loops` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `steam_transport_salt_pumps_per_circuit` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `steam_transport_selected_salt_design_flow_kg_s` | `constraints_reachable` | Search as proposed; execution awaits review/integration. |
| `steam_boundary_bypass_flow_rating` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_ledger_controller_capital` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_ledger_annual_service_fraction` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_ledger_replacement_fraction` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_ledger_common_source_pv` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `gas_boundary_bypass_flow_rating` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `gas_ledger_controller_capital` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `gas_ledger_annual_service_fraction` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `gas_ledger_replacement_fraction` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `gas_ledger_common_source_pv` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `compressor_equipment_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `turbine_equipment_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `generator_equipment_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `he_hx_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `he_duty_equipment_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `conversion_services_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `heat_rejection_equipment_price_factor` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `gas_ledger_capital9` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_ledger_capital3` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_ledger_capital4` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_transport_costscale` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_cycle_eta_hp` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_cycle_eta_lp` | `constraints_reachable` | Sensitivity as proposed; execution awaits review/integration. |
| `steam_cycle_steam_temperature_C` | `constraints_reachable` | Declined: held offer does not support this direction. |
| `steam_cycle_reheat_temperature_C` | `constraints_reachable` | Declined: held offer does not support this direction. |
| `steam_cycle_condenser_temperature_C` | `constraints_reachable` | Declined: held offer does not support this direction. |
| `steam_transport_secondary_head` | `constraints_reachable` | Declined: held offer does not support this direction. |

**Not derivable:** monotonicity or sign of a response, identity of a physical quantity across differently named keys, and intra-module operand dependency. A reachable constraint is a possible graph path, not proof that a constraint responds. The financial inputs reach ledger constraints at module level; this does not establish physical resistance to price or recurring-cost assumptions. Those axes remain hypothetical sensitivities under the owner brief.

The missing price qualification, installed-scope evidence and validated efficiency maps remain explicit model-development limitations even though no axis receives a sound negative from the graph indicator. The findings register will carry their observed implications after execution and review.

## 9. Preflight results

Every mechanical gate that ran, with its outcome. The identity and baseline gates read the documents the route-preparation step deposited in `results/`; name those files in the detail column so a cold reader can open what the gate read. A gate that did not run is stated as such with its condition.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | `<pass \| fail \| did not run, with the condition>` | `<detail>` |
| Suffix-sibling scan (warnings only) | `<pass \| warnings with count>` | `<the siblings found, or none>` |
| Baseline gate against the pinned headline | `<pass \| fail>` | `<expected vs observed>` |
| Manifest / package fingerprint match | `<pass \| fail>` | `<detail>` |
| Package cleanliness | `<pass \| fail>` | `<detail>` |

## 10. Execution route and why

- **Route:** `<teax-study CLI \| study-local direct-API>`
- **Why this route:** `<what about this study forced or allowed it>`

The rationale is recorded after the route was first exercised and gated, so it accounts for a route already known to load rather than predicting one.

**Glue disclosure.** What the harness supplies that the model does not, and what that means for the claims. The ledger's entries are values and live in `snapshot.json` under `glue_ledger`; this is the argument about them.

`<per rung: what it supplies, why the model cannot, and which claims it scopes — or: glue ledger: none. No adapter on this route, so nothing is harness-supplied.>`

## 11. Study definition and window provenance

`<how the window was chosen: what was scanned, with what, and what the scan showed that fixed these bounds. The bounds themselves and their engineered|sourced provenance are snapshot values under arms[].window — do not restate them here.>`

`<if engineered: state plainly that the window is engineered and what claims that costs. If sourced: name the source.>`

## 12. Cross-fingerprint correlation and what it means

`<when the arms span fingerprints: which boundary was crossed; that constraints were matched by definition qualified name plus local identity; every predicate_ir difference, disclosed; and what the correlation licenses and does not license. The compatibility tuples themselves are snapshot values under stores[]. When they do not span fingerprints, discharge the nil by naming the condition: "single fingerprint — no cross-arm correlation needed".>`

## 13. Verification

`<the outcome: what passed, what did not, and what the result licenses. The command, sampling scheme, tolerance, and summary digest are snapshot values under arms[].verification — do not restate them here.>`

`<what verification did not cover, named. A value that is identical by construction on both sides is not independently verified, and saying so here is part of the outcome.>`

## 14. Review outcomes

Each applicable lens, its verdict, and its disposition. Preserve this section when no additional review is needed: record the coordinator check, the reason, and any reused evidence with its revision/scope/environment validity. Label independent review honestly; a separate pre-execution critique is needed only when triggered.

| Lens | Verdict | Disposition |
|---|---|---|
| `<lens name, e.g. pre-execution framing critique>` | `<what it found>` | `<what was done about it>` |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` as `<study-id>#<n>`.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `<study-id>#<n>` | `<model \| process>` | `<one line>` | `<one line>` | `<home, or unrouted>` |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `<digest>`
- **Schema version:** `<snapshot_schema_version>`

No snapshot content is restated here.

## 17. What this record does not contain

`<every fact a reader might expect and will not find, stated rather than left to inference. Gaps in the record itself only — the glue disclosure belongs in §10 and a framing-conditional nil belongs in §6.>`

---

**END OF RECORD**

---

