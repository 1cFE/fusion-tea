---
Status: active
Created: 2026-09-22
Updated: 2026-09-22
---

# WI-090 implementation plan

Related Artifacts: spec.md; design.md; ../../orchestration/goals/aries-integrated-equipment-costs/trail.md

## Preparation and review

- [x] Inspect existing assembly ownership, source-budget, constituent, capacity, fuel, costed-component and facilities interfaces; record precise reuse limits in design.
- [x] Capture requirements, equations, proposed binding roles, public-input migration, account boundaries and new assumptions.
- [x] Incorporate `work/orchestration/goals/aries-integrated-equipment-costs/evidence/source-basis.md`; preserve source27 as heat rejection and material parent-child discrepancies as unallocated differences, with separate nominal and source replacement schedules.
- [x] Fresh independent review of source interpretation/equations, MR-7 roles, thermal/cost coupling and disjointness; record findings and revise before implementation.
- [x] Address review R1 in the proposed design: selected kg converts to atoms for the existing required-breeding calculation, with shared mass/decay constants and explicit dormant-stock input migration. Same-reviewer corrective acceptance is recorded at coordinator checkpoint1043ca8f.

## Native implementation after review

- [x] Author additive `models/library/analyses/integrated_equipment_costs.sysml` and `models/library/structure/integrated_equipment_parts.sysml`; reuse inspected existing definitions. Add finite/domain guards and quantitative citations to the accepted design/source record.
- [x] Extend `models/designs/aries_cs_integrated/plant.sysml` with selected inventory/cost owners and the exact proposed binding table. Migrate only declared UA/pump entries; retain explicit source modes, eight existing selected ratings and scientific support flags.
- [x] Extend `exploration/aries_integrated/build.py`, native completions and case definitions through the established generator. Redirect all evidence writes from archived WI-089 to this WI-090 directory before invoking build/test commands. Author owns generation under T-003; coordinator owns `tests/model_families.py` source-family registration.
- [x] Export native inventories, cost leaf/parent outputs, source reconciliation, overnight/classification channels, annual fuel/O&M/consumables and replacement event interfaces. Generate machine-readable input-key migration and full four-case maps.
- [x] Replace the study oracle's unknown-predicate fallback with explicit operand mappings for every added predicate; reject unknown names. Follow the coordinator's `evidence/study-preparation.md` for full native input-axis groups.

## Validation and acceptance evidence

| Requirement | Check and expected observation | Basis | Status |
|---|---|---|---|
|R1,R6| Four inherited scenarios replay through new package; nominal reproduces423.106794 MW, literal scenarios retain failure verdicts and residuals. | Unchanged equations/nominal operating powers and UA mapping; archived WI-089 evidence. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R2| Density amplitude5e20→4.75e20/5.25e20 at fixed hardware changes heat/margins/net/annual fuel; every selected inventory and upfront leaf cost remains exact. | MR-7 fixed-design contract. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R2| HX area5000/75000 m² at fixedU reproduces formerUA5/75 behavior, changes area cost; independent U sweep changes thermal results without area/capital change. | UA physical identity and existing insufficient/sufficient thermal evidence. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R2| Every eight rated machine/branch/fuel quantity has insufficient/sufficient checks; actual demand unchanged, selected quantity and corresponding cost change. Pump-flow rating low/high adds capacity tests. | MR-7 chosen-inventory contract. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R2,R7| Pump operating-flow perturbation changes proxy electricity/friction and thermal transfer while purchased rating/cost fixed; literal fixed-power mode reproduces source inputs. | Reviewed proxy equation and source modes. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R3,R4| Independent recomputation of all leaf/parent sums; source eight-parent total2619.572 MUSD2004; explicit source residuals; source1.93 multiplier only in inclusive comparison. | Original images/source review; disjoint account map. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R3| Initial T and LiPb purchase once; replacement event0 absent, permanent coils/shield absent from blanket replacement, LiPb replacement only selected makeup fraction. | Declared account scope. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R5| Replacement events just before/at/after plant lifetime; event at lifetime excluded; availability change rescales calendar interval and fuel productive time, calendar decay uses full year. | Independent schedule construction and dimensional arithmetic. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R2,R5,R7| Change selected tritium stock10→20kg at fixed source power, burn/recovery fractions and availability. Initial stock cost and calendar decay double; required breeding increases by `lambda_T*(10kg/atom_mass)/(eta_extract*burn_rate)`. Burn/exhaust/loss and heat/net electricity remain unchanged; breeding support stays0. Inspect generated `I_total_in` and annual-decay bindings for one selected-stock owner, no independent dormant-atoms entry or duplicated mass/decay constants. | Design-review R1; unchanged `Fuel Cycle Flows` equation and independent dimensional calculation. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R5| Negative net output retained with import channel; no negative annual energy masquerading as sales, no auxiliary electricity double charge. | Plant export convention and financial boundary. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R6| Principal thermal sensitivity completed and interpreted before ranking; fixed inventories/costs in uncertainty sweeps, all adverse outcomes retained. | Owner quote and design sensitivity scope. | Passed64-point frozen study494c329e and independent thermal-study-review.md before Round2 economics. |
|R7| Unsupported magnet/breeding/material/hydraulic flags stay0 in every source substitution; numerical domain refusal distinct from failed adequacy. | Scientific evidence limits. | Passed native66-case development checks; independently accepted in goal evidence/implementation-review.md. |
|R8| Focused parse/structural checks then six-level complete validation, typed native generation/fixed-point/census and integrated execution; any L6 exceptions identified by actual diagnostics and execution evidence. | Established model-validation guidance. | Native generation/fixed-point/execution pass; complete validator L1/3/4/5 pass, L2/L6 diagnostics retained and independently accepted as scoped limitations. |
|R1,R8| Original Stellaris/transfer/frozen evidence digest comparison at increments, plus separately scoped isolated Stellaris behavioral regression by coordinator. | Preservation contract; hashes and behavior are different evidence. |8752protected files unchanged; isolated1352-output/68-response Stellaris replay exact. |

- [x] Independent reviewer traces executed demand and selected-area/rating perturbations through actual generated dependencies, not only formula mirrors. Record MR-7 verdict and scope.
- [x] Coordinator promoted one package in Round1 and reused it in Round2; one study per round is frozen at494c329e and8d322312. Study ordering and identities live in native goal/study records.
- [x] Deliver model report, exact package/case identities, replay commands, assumption-ranked cost range and financial handoff in the goal answer and two native studies. Final independent goal-interpretation review passes; formal closure remains owner-held.

## Current handoff

The accepted design is implemented and canonical cases run through the generated package. Initial63-case evidence is preserved in `evidence/checkpoint-a24f9080/`; the corrective native source comparisons and stock adequacy cases pass final66-case verification (`evidence/verification.json`), with54evaluated and12expected refusals. All new writes target WI-090 evidence. Independent integrated review and all ten native promotion gates pass; the64-point thermal study is frozen at494c329e and independently accepted. Round2 cost uncertainty is frozen at8d322312, with all113points independently verified numerically and final interpretation review passing. Both rounds preserve source failures and unsupported scientific qualifications; their reports and the exact financial handoff complete the authored delivery. Coordinator owns PM registration, source research, goal trail, source-family registration and commits; the study worker owns study interfaces. No frozen predecessor evidence was changed.
