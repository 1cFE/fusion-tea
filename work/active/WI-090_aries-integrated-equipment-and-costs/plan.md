---
Status: proposed
Created: 2026-09-22
Updated: 2026-09-22
---

# WI-090 implementation plan

Related Artifacts: spec.md; design.md; ../../orchestration/goals/aries-integrated-equipment-costs/trail.md

## Preparation and review

- [x] Inspect existing assembly ownership, source-budget, constituent, capacity, fuel, costed-component and facilities interfaces; record precise reuse limits in design.
- [x] Capture requirements, equations, proposed binding roles, public-input migration, account boundaries and new assumptions.
- [x] Incorporate `work/orchestration/goals/aries-integrated-equipment-costs/evidence/source-basis.md`; preserve source27 as heat rejection and material parent-child discrepancies as unallocated differences, with separate nominal and source replacement schedules.
- [ ] Fresh independent review of source interpretation/equations, MR-7 roles, thermal/cost coupling and disjointness; record findings and revise before implementation.

## Native implementation after review

- [ ] Author additive `models/library/analyses/integrated_equipment_costs.sysml` and `models/library/structure/integrated_equipment_parts.sysml`; reuse inspected existing definitions. Add finite/domain guards and quantitative citations to the accepted design/source record.
- [ ] Extend `models/designs/aries_cs_integrated/plant.sysml` with selected inventory/cost owners and the exact proposed binding table. Migrate only declared UA/pump entries; retain explicit source modes, eight existing selected ratings and scientific support flags.
- [ ] Extend `exploration/aries_integrated/build.py`, native completions and case definitions through the established generator. Redirect all evidence writes from archived WI-089 to this WI-090 directory before invoking build/test commands. Coordinator owns package generation and `tests/model_families.py` source-family registration unless reassigned.
- [ ] Export native inventories, cost leaf/parent outputs, source reconciliation, overnight/classification channels, annual fuel/O&M/consumables and replacement event interfaces. Generate machine-readable input-key migration and full four-case maps.
- [ ] Replace the study oracle's unknown-predicate fallback with explicit operand mappings for every added predicate; reject unknown names. Follow the coordinator's `evidence/study-preparation.md` for full native input-axis groups.

## Validation and acceptance evidence

| Requirement | Check and expected observation | Basis | Status |
|---|---|---|---|
|R1,R6| Four inherited scenarios replay through new package; nominal reproduces423.106794 MW, literal scenarios retain failure verdicts and residuals. | Unchanged equations/nominal operating powers and UA mapping; archived WI-089 evidence. | Pending |
|R2| Density amplitude5e20→5.15e20 at fixed hardware changes heat/margins/net/annual fuel; every selected inventory and upfront leaf cost remains exact. | MR-7 fixed-design contract. | Pending |
|R2| HX area5000/75000 m² at fixedU reproduces formerUA5/75 behavior, changes area cost; independent U sweep changes thermal results without area/capital change. | UA physical identity and existing insufficient/sufficient thermal evidence. | Pending |
|R2| Every eight rated machine/branch/fuel quantity has insufficient/sufficient checks; actual demand unchanged, selected quantity and corresponding cost change. Pump-flow rating low/high adds capacity tests. | MR-7 chosen-inventory contract. | Pending |
|R2,R7| Pump operating-flow perturbation changes proxy electricity/friction and thermal transfer while purchased rating/cost fixed; literal fixed-power mode reproduces source inputs. | Reviewed proxy equation and source modes. | Pending |
|R3,R4| Independent recomputation of all leaf/parent sums; source eight-parent total2619.572 MUSD2004; explicit rounding residuals; source1.93 multiplier only in inclusive comparison. | Original images/source review; disjoint account map. | Pending |
|R3| Initial T and LiPb purchase once; replacement event0 absent, permanent coils/shield absent from blanket replacement, LiPb replacement only selected makeup fraction. | Declared account scope. | Pending |
|R5| Replacement events just before/at/after plant lifetime; event at lifetime excluded; availability change rescales calendar interval and fuel productive time, calendar decay uses full year. | Independent schedule construction and dimensional arithmetic. | Pending |
|R5| Negative net output retained with import channel; no negative annual energy masquerading as sales, no auxiliary electricity double charge. | Plant export convention and financial boundary. | Pending |
|R6| Principal thermal sensitivity completed and interpreted before ranking; fixed inventories/costs in uncertainty sweeps, all adverse outcomes retained. | Owner quote and design sensitivity scope. | Pending |
|R7| Unsupported magnet/breeding/material/hydraulic flags stay0 in every source substitution; numerical domain refusal distinct from failed adequacy. | Scientific evidence limits. | Pending |
|R8| Focused parse/structural checks then six-level complete validation, typed native generation/fixed-point/census and integrated execution; any L6 exceptions identified by actual diagnostics and execution evidence. | Established model-validation guidance. | Pending |
|R1,R8| Original Stellaris/transfer/frozen evidence digest comparison at increments, plus separately scoped isolated Stellaris behavioral regression by coordinator. | Preservation contract; hashes and behavior are different evidence. | Pending |

- [ ] Independent reviewer traces executed demand and selected-area/rating perturbations through actual generated dependencies, not only formula mirrors. Record MR-7 verdict and scope.
- [ ] Coordinator promotes at most one package and commits at most one study per goal round. Study ordering and identities live in native goal/study records.
- [ ] Deliver model report, exact package/case identities, replay commands, assumption-ranked cost range and financial handoff. Update this checklist as phases finish; formal closure remains owner-held.

## Current handoff

Preparation only. No model/package files or frozen evidence changed. The reviewed source record is incorporated; independent design review remains before implementation. Coordinator owns PM registration, source research, goal trail, source-family registration and generation. Author ownership is currently this WI-090 directory only.
