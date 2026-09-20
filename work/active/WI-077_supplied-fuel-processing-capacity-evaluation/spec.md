---
Status: active
Scale: standard
Owner: codex
Created: 2026-09-20
Updated: 2026-09-20
---

# Supplied fuel-processing capacity

[NEED] Evaluate and cost a supplied processor throughput without binding its capacity to exhaust demand. Source: preserve-model-design-choices/evidence/owner-prompt.md; MR-7. Preserve source applicability separately from capacity adequacy and preserve historical replay packages.

## Proposed exact binding plan

[AGENT] Replace public Fuel Cycle `processing_capacity_margin` [1] with `processing_capacity_kg_s` [kg D+T/s per module]. Replace calculation formal `capacity_margin_in` with `capacity_in`. In `models/library/structure/mfe_plant_systems.sysml`, processing_cost binds `in capacity_in = processing_capacity_kg_s`. Keep `in flow_in = dt_processing_flow` as running demand. The source model is `models/library/analyses/mfe_fuel_cycle.sysml`, with parallel canonical twin under exploration/stellarator_e2e/models/analyses/.

[AGENT] In the normative handwritten implementation, active capacity must be finite and positive; demand finite and nonnegative; n_mod a positive integer. Set capacity_kg_s to supplied capacity, plant_capacity_kg_s=n_mod*capacity and price scale=(capacity/reference_flow)^exponent. Add plant_demand_kg_s=n_mod*flow, capacity_margin_kg_s=n_mod*(capacity-flow), and capacity_evaluation_defined=1 for active inventory/processing. Dormant mode keeps legacy price and capacity_evaluation_defined=0; it does not claim capacity adequacy. Preserve defined_flag as source-price applicability, independent of capacity. Zero running demand does not erase installed price.

[AGENT] Expose the defined flag and signed margin on Fuel Cycle. Add a library `Fuel Processing Capacity` constraint that requires capacity_evaluation_defined >= 1 and margin >= 0; assert it on the active stellarator instance, not on dormant generic plants. Bind each formal to the owner EXPOSE. Existing exhaust_processor capital/equipment/installation bindings continue to consume processing_cost outputs, now solely determined by supplied capacity and price settings.

[AGENT] Replace the stellarator margin literal with independently supplied 0.00015 kg D+T/s per module. This is a round engineering assumption for interface demonstration, not an adequacy guarantee or fitted result. Document [ASSUMED] provenance to this spec. Tests deliberately exercise capacities below and above demand; baseline pass is not required. Costs will differ from the entering demand-matched price because a different explicit rating is supplied.

[AGENT] No automatic selection remains in the evaluation route. A caller wishing to reproduce the old policy can explicitly calculate old demand×margin once, persist the resulting rating, then evaluate it. The retired input must be rejected by the new study contract. Frozen study packages and WI-070 records/seeds remain unchanged. Update only live oracle consumer(s) and current tests; add new WI-077 seed and regeneration provenance rather than changing WI-070 evidence.

## Acceptance checklist

- [x] Fresh non-author approval of actual bindings and source-price interpretation before implementation.
- [x] Current native package executes below-demand and above-demand supplied ratings, retains each rating and returns the expected capacity predicate.
- [x] At fixed capacity and prices, varying exhaust demand changes margin but not processing price; zero demand preserves price.
- [x] Multiple identical modules scale demand/capacity/prices together without changing per-module margin sign.
- [x] Source-condition false remains undefined pricing while preserving diagnostic values; cannot be reported as a certified price.
- [ ] Invalid capacity/fractions fail explicitly, and native generated public names/migration are checked.
- [ ] Affected regressions and independent integration review recorded.
