# Transfer change register

[AGENT] This is a provisional decomposition into 13 engineering work areas. It is not 13 completed code changes or a proved irreducible minimum. Areas combine shared causes to avoid counting a new input, its binding and its downstream consumer three times. Full source sufficiency may split an area; the log must record why. The counted target is the original ARIES-CS reference, not a chosen easier alternative.

| ID | Responsibility | Existing behavior that can carry over | Required adaptation or evidence | Current experiment |
|---|---|---|---|---|
| T01 | Plasma profiles and operating closure | D-T reaction kernel, basic pressure/energy relations | Hollow finite-edge density; compatible temperature/species/geometry integration and confinement | WI-081 local profile plus reviewed WI-083 forward integration (14 supported cases, 25 refusals); reused density/kernel/beta. Actual reference profiles, geometry measure and closure remain open |
| T02 | Radial sectors and constituent inventory | Geometry/mass identities | Full/tapered coverage, material constituents and their actual volumes; uniform shells do not encode this | WI-084 reviewed: 3 reference regions/9 material children execute; 4 new generic definitions. Actual midpoint geometry and mean taper remain missing |
| T03 | Magnetic field and mechanical loads | Explicit current/turn and pack arithmetic | Independent coil geometry/current-family inputs; qualified field/force/stress treatment | Missing scientific inputs; scalar rebinding insufficient |
| T04 | Conductor performance | Capability-versus-demand pattern | Nb3Sn product/temperature/strain performance and winding definitions | Source qualification required; do not expand REBCO interval |
| T05 | Breeding response | Guard/interface/interpolation pattern | Geometry/material/source-specific transport dataset and validation | New dataset required; current table has fixed geometry |
| T06 | Fuel handling | Burn, injection, exhaust and conservation balances | Matched burnup/recovery/inventory/processing inputs; full breeding coupling | WI-082 reuse plus reviewed WI-085 calculated plasma→fuel→fixed-capacity integration (six cases, 35 exact comparisons), no new physics. Actual equipment/inventory/breeding remain open |
| T07 | Maintenance and availability | Calendar and replacement arithmetic | Source-supported component clocks, maintenance operations or explicitly supplied availability boundary | Conditional use possible; prediction of actual reliability remains unestablished |
| T08 | Helium and PbLi heat transport | Thermodynamic balances, some helium relationships | Separate branches and interfaces; applicable hydraulics/MHD/properties; prevent friction-heat double counting | WI-086 reviewed two-branch heat accounting with one transfer and fixed capacity checks; hydraulics/MHD/properties, divertor circuit and equipment qualification remain open |
| T09 | Power conversion | Generic energy bookkeeping | Recuperated helium Brayton components/states/capabilities instead of Rankine | WI-087 reviewed nominal ideal-gas Brayton assembly: six new definitions, nine native cases and 306 comparisons. Real-fluid, shaft split, electrical and primary-exchanger matching remain open |
| T10 | Installed equipment costs | Selected-purchase and account-addition patterns | Correct technology inventories and dated prices; current salt/cooling assumptions do not represent PbLi equipment | WI-084 source-rate constituent arithmetic and WI-088 supplied budgets execute; actual equipment-specific purchase/install estimates remain open |
| T11 | Facilities and handling | Civil commodity pricing | Source-supported takeoff/layout and maintenance relations | Quantity data missing for actual facility prediction |
| T12 | Cost boundaries and rollup | Generic sum, contingency and annual-account arithmetic | Disjoint source/model scope mapping including vacuum, manifolds, installation and parent accounts | WI-088 aggregates eight disjoint source parents without descendants; full model/source subaccount correspondence remains open |
| T13 | Finance and LCOE convention | CRF, interest and annual-energy arithmetic | Overnight versus financed capital; calendar versus full-power years; annual versus lifetime costs | WI-088 native partial budget allocation executes under literal and inferred FPY/calendar conventions; source77.6 reconciliation and complete annual costs remain open |

Source evidence and exact current producers are in [physics inventory](physics-inventory.md) and [thermal/cost inventory](thermal-cost-inventory.md). These reports distinguish reusable equations from applicable source data. Eight native increments provide bounded evidence; they do not close all 13 areas.

## Measurement rule

[AGENT] For every executed increment report: existing definitions instantiated unchanged, shared definitions changed, new definitions, new case bindings, copied native implementations versus newly authored equations, and verification of each. Count equation copying or a fork as a copy, not unchanged shared-code reuse. Count a typed-import prefix adaptation separately from mathematical changes. Keep validation scope explicit: native execution, equation correctness, source correspondence and full-plant applicability are different claims.

[AGENT] Configuration is work even when no equation changes. A selected capacity check can pass or fail without design resizing. A source-supplied load is not predicted; an agent-assumed operating parameter remains an assumption. No reuse fraction will be reported across arbitrary file or definition counts.

## Sequencing

First implement WI-081 and WI-082 as independent native cases. Their outputs test representation and reuse without requiring missing coil geometry or transport simulations. Review their source and execution claims, then update this register with observed results. Extend plant closure only where the remaining input and scientific dependencies are established; do not wire a partial module into the original plant and present it as a qualified ARIES model.
