# Fresh interface and accounting review

**Verdict: PASS for the bounded interface/account trace.** [AGENT] The WI-069 producer supplies a verified conditional running isotope-load interface for a potential aggregate exhaust processor. This verdict does not approve a costing source, technology, equipment design or implementation, and does not grade R10.S2.

The implementation computes inlet U=B/f−B before outlet recovery, then exports T mass and equal-atom-rate D+T mass separately. Availability enters annual amounts only. Gross and extracted T are isotope rates, not carrier throughput. These statements agree with the upstream throughput-interface.md and the actual implementation at exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/fuel_inventory_impl.py:49 and :90. The stellarator activates inventory and retains conditional recovery and extraction assumptions at models/designs/stellarator_09/stellarator_plant.sysml:1380 and :1405. Undefined breeding preserves diagnostic carriers; production-dependent outputs require the applicability flag.

The accounting statements are supported:

- Combined cleanup/separation is a stock representation, with loss at its outlet; it is not a specified process train (models/library/structure/mfe_plant_systems.sysml:513). Purification should be understood only as the trace’s functional interpretation of cleanup, not verified technology or purchased scope.
- C220500 remains the $120 million net-power proxy labeled processing plus containment. It enters CAS22 once. The installation subtotal includes power-core and remote-handling capital, excluding this fuel account (models/designs/generic_mfe/mfe_plant.sysml:463 and :500). Shipping, tax, insurance and indirect charges respond downstream; source-installed pricing therefore needs a scope reconciliation.
- The 30×20×8 m values are equipment envelopes, not final building dimensions (stellarator_plant.sysml:1556). The layout adds clearances, includes the fuel building in controlled ventilation, and selects the new civil account instead of the grouped legacy building allowance; the legacy HVAC constants visible in the instance are not an additional active charge (generated/handwritten/mfe_facilities/facility_layout_impl.py:195 and :220; facility_account_selection_impl.py:10, under exploration/stellarator_e2e/).
- Vacuum Pumping has gas-load arithmetic but no pumping-train price (mfe_plant_systems.sysml:566). Vessel cost does not establish pump coverage. Replacing the full C220500 allowance cannot imply retained containment coverage.
- CAS50 startup purchase remains power-scaled, separate from computed stock; CAS80 remains reaction-priced recurring fuel (models/library/analyses/mfe_account_costs.sysml:647; generic_mfe/mfe_plant.sysml:650, under models/designs/).

I independently checked an empty tracked-file diff against 956444b5 for the producer paths listed in inspect_entry.py, inspected the retained 144-pass/13-warning log and relevant native/oracle tests. I did not rerun those tests or certify untracked-file absence. Existing static-validation limitations remain.

No blocking correction to current-trace.md is required. Cost scope, feed composition, purity, pressure, reference price/year, scale law, redundancy, installation and safety coverage remain unresolved. The interface establishes isotope load, not complete gas-processing capacity.
