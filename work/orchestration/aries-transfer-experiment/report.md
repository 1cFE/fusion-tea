# ARIES transfer experiment: first implemented results

[AGENT] The first two increments demonstrate that some components transfer unchanged and that a missing profile relationship can be added through the existing modeling tools. They do not yet evaluate the complete ARIES plant. This is post-reveal development, with the original unsuccessful comparison preserved.

## What actually ran

| Increment | Existing definitions reused unchanged | New modeling work | Executed evidence | What remains unproved |
|---|---|---|---|---|
| Fuel flow and processing-capacity check (WI-082) | Two calculations and one constraint | One case assembly with supplied load, operating assumptions and capacity; one native completion copied with import-prefix adjustment | Five native cases; 35 exact baseline comparisons; independent energy/conservation checks; reviewer replay at a new load | Actual ARIES processing equipment, operating fractions, inventory, breeding and costs |
| Hollow finite-edge density profile (WI-081) | Existing parser, generator and TEAx route; no claim of unchanged plasma-equation reuse | One generic local-density calculation, one case assembly and a guarded typed completion | 13 supported native cases; 25 invalid-input refusals; independent polynomial oracle and supplied-choice propagation | Absolute ARIES density, profile moments, temperature/composition and coupled fusion prediction |

[AGENT] The fuel case takes the published 2436 MW fusion load as an input. With explicitly assumed 5% burn fraction and 99% recovery, exhaust is 1.6432423549621273e22 tritium atoms/s. Assumed capacity 2e22 passes; 1e22 fails. Doubling demand makes the original capacity fail without resizing it. The input load and assumed equipment are not predictions or verified ARIES hardware.

[AGENT] The density case reproduces the source equation's shape with a supplied demonstration amplitude. The source uses conflicting descriptions of the amplitude and axis density. The model therefore does not infer an absolute ARIES density. Supplying a different amplitude or shape changes the calculated local density through the generated bindings.

## How much work is still required?

[AGENT] The [change register](change-register.md) identifies 13 provisional engineering work areas. Two have partial executed evidence; neither is complete at plant level. This is not a demonstrated minimum of 13 changes, and counting source files would give a misleading reuse percentage.

- Full engineering evaluation still needs consistent plasma closure, sector/material representation, qualified magnetic-field and conductor calculations, geometry-specific breeding evidence, actual fuel equipment, maintenance assumptions, dual helium/PbLi heat transport and Brayton conversion.
- Comparable LCOE additionally needs technology-specific equipment prices, facility quantities, disjoint cost-account boundaries and matched finance conventions.
- Coil geometry/current definitions, applicable conductor evidence and new breeding response data are scientific or source dependencies. Changing input guards does not supply them.

[AGENT] The thermal inventory also found a concrete interface hazard: the published helium duty includes friction heating. Supplying that number directly as source heat to the existing loop would count recovered work twice. No such substitution was made.

## Verification and next work

[AGENT] Independent review is recorded in [implementation-review.md](evidence/implementation-review.md). The fuel case has a narrowly accepted static-check exception: L1–L5 pass, while L6 rejects three EXPOSE expressions that actual generation and native execution resolve. The density case also passes L1–L5 and has one independently accepted L6 EXPOSE exception, verified by native replay. Both complete-validator runs return exit 1; neither is a six-level pass. No full-plant regression claim follows from either isolated case. Failed attempts and repairs remain in the item evidence. All 1,383 protected original files match their baseline hashes, as recorded in [preservation-final.json](evidence/preservation-final.json).

[AGENT] Next, extend the source-supported plasma profile into explicitly defined density/temperature moments and reaction integration, after resolving the coordinate, species and normalization definitions. In parallel, develop the sector/material inventory from published geometry and recipes. Record inputs still missing before claiming source correspondence. Continue to treat field/conductor and breeding qualification as separate dependencies; do not feed published output targets into those checks to manufacture an independent prediction.

[AGENT] The first implementation round is bounded to the two registered items. The full transfer epic and both full-plant milestones remain open. The plan, inventories, native models, reproduction scripts and continuing [log](log.md) provide the starting point for further increments.

## Continued area T01: connected plasma integration

[AGENT] WI-083 adds one forward integration calculation and case. It reuses the accepted density component, copies the existing reaction helper unchanged, and feeds calculated thermal pressure into the unchanged beta definition. Fourteen native supported cases pass and 25 invalid or numerically unresolved cases refuse. Independent review accepts the bounded result and nine named static EXPOSE exceptions; aggregate validation still exits 1 with L1–L5 passing.

[AGENT] The selected scenario calculates 1835.451283 MW fusion power and 5.60649% thermal beta. Density amplitude, temperature sensitivity shape, local species and volume measure are explicit supplied choices, not fitted to reference outputs. This establishes a connected forward calculation; it does not establish actual ARIES profiles, confinement closure or numerical agreement with the reference. [Implementation and exact evidence](../../active/WI-083_aries-supplied-profile-plasma-integration/implementation.md), [independent review](evidence/plasma-integration-review.md).

## Continued area T02: reference constituent inventory

[AGENT] WI-084 adds four elementary calculation/aggregation definitions and one assembly with three reference regions and nine material children. Five native cases pass 230 independent comparisons; 14 invalid inputs refuse, including inconsistent coverage at zero volume. Independent review accepts the repaired model and 39 named static EXPOSE exceptions; L1–L5 pass and aggregate validation remains exit 1.

[AGENT] Supplied geometry now drives constituent volume, known non-helium mass and an unmapped USD2004 source-rate subtotal. No unchanged physical-definition reuse is claimed for this increment. Existing blanket-cost proxies do not express these constituent semantics. Actual midpoint areas, taper distribution and helium mass/price remain missing; source LiPb accounting also prevents calling the combined subtotal installed blanket cost. [Result and reproduction](../../active/WI-084_aries-sector-constituent-inventory/report.md), [review](evidence/constituent-review.md).

## Continued area T06: calculated plasma power reaches fuel equipment checks

[AGENT] WI-085 adds one assembly and no new physical definitions. It imports the reviewed plasma case and binds its calculated fusion-power output into existing fuel balances and then into the fixed-capacity check. Six native cases and 35 exact fuel-output comparisons pass. Independent review's separate doubled-volume test also increases demand enough to fail unchanged supplied capacity. The integrated fuel case has no public source-power input. [Implementation](../../active/WI-085_aries-calculated-plasma-to-fuel-integration/implementation.md), [review](evidence/plasma-fuel-review.md).

[AGENT] The result demonstrates cross-component reuse and supplied-choice preservation. Burn/recovery fractions and processing rating remain scenario assumptions; actual ARIES inventory, equipment cost and breeding are unqualified. L1–L5 pass, with twelve narrowly accepted L6 EXPOSE exceptions and aggregate exit 1 retained.

## Continued area T08: two blanket heat branches

[AGENT] WI-086 adds two generic heat-accounting definitions and an assembly with a single shared transfer, two branch owners and unchanged capacity screens. Seven native scenarios pass 42 heat comparisons; eleven refusal tests include both physical-domain and generated-input-schema checks. Independent review accepts the repaired interface and six named static EXPOSE exceptions (L1–L5 pass; aggregate exit 1).

[AGENT] The Raffray engineering case reconstructs 1192 MW helium and 1444 MW PbLi removal from supplied source-derived boundaries. Internal conservation is zero; comparison to the printed deposited-heat total retains a -1 MW residual. This is a separate engineering source case, not a connection to the Lyon or WI-083 plasma point. Hydraulics, MHD, the omitted divertor circuit, actual exchangers and electrical pumping remain unqualified. [Report](../../active/WI-086_aries-dual-blanket-heat-accounting/report.md), [review](evidence/heat-transport-review.md).

## Nominal Brayton component execution (T09)

[AGENT] WI-087 adds six ideal-gas component/ledger definitions and a connected nominal cycle using three unchanged capacity screens and constraints. Nine scenarios, 306 independent comparisons and 21 refusals pass independent review. Selected flow and three compressor ratios remain independent inputs; equipment ratings stay fixed. Nominal net shaft work is 831.790186675 MW, not plant electricity. Real-fluid accuracy, primary heat-exchanger matching, source shaft split, electrical losses and installed equipment remain open. [Result](../../active/WI-087_aries-nominal-brayton-component-cycle/report.md).
