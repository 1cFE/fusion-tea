# Current supplied-design interface migration

[AGENT] This is a versioned current evaluator interface. Frozen packages and their historical replay meanings remain unchanged. The current public-input delta is enumerated independently in WI-075/evidence/interface-delta.json and checked against generated contracts: 511 entering inputs, 12 retirements and 98 additions, yielding 597 current inputs. All names below are below `stellarator_09__stellaris__`.

| Path | Before | Current supported choice |
|---|---|---|
| `magnet` | Current/current density, field grade and inventory policy selected pack geometry and conductor quantities; support/casing masses followed energy/radius policies. | Supply `winding_pack__wp_side`, `coil__reference_turns`, `coil__turn_current`, `m_support` and `casing__m_casing`. Current density and ampere-turns are identities. Existing current, fit and stress screens evaluate the chosen design. |
| `buildings` | Calendar demand selected allocated storage, package segmentation and building envelopes. | Supply room dimensions, package counts, storage positions and parcel dimensions. `parcel_origin_x_offset/y_offset` are signed metres relative to the documented entering coordinate frame. Absolute parcel minima are derived coordinate identities; no demand-dependent translation occurs. |
| `fuel_cycle` | `processing_capacity_margin` multiplied running exhaust and selected installed capacity/price. | Supply `processing_capacity_kg_s` per module. Demand sets a signed margin; price follows supplied capacity. Source applicability remains separate. |
| `heat_transport` | Current duty selected machine price points and coolant procurement; calibration flow also acted as offered flow ceiling. | Supply helium/salt machine price design points and purchased coolant masses. `mdot_loop_rated` is independent of calibration `mdot_loop_ref`. Operating energy still follows heat-balanced demand. |

Retired selection inputs have no live aliases. A historical design-construction policy may be run separately against its original package, then its resulting hardware choices can be supplied to this evaluator. That is an explicit migration, not numerical equivalence of arbitrary old proposals. Library selection helpers remain optional analyses outside the mandatory evaluator.

The entering winding side/turns/masses, facility dimensions and cooling purchase/design points were copied from the entering model's own evaluated design. Processor capacity is the independently stated 0.00015 kg D+T/s per-module engineering assumption. The resulting processor-price difference is explained by that supplied rating. No external reference outputs selected these values.

Machine off-design performance, support/casing structural qualification, arbitrary facility topology and independently offered fuel-buffer/tank stocks remain outside supported evaluation. Fuel residence/coverage/startup policies and operating heat/mass closures retain their declared directions. Aggregate cost proxies remain explicitly labeled assumptions; they do not certify installed equipment capacity. See residual-dispositions.md and the independent implementation review for the precise boundaries.
