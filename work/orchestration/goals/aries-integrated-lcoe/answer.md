# Conditional integrated ARIES LCOE

[AGENT] Work in progress. Native development verification is complete; independent integration review and the declared lifecycle study remain pending. This is not a final goal-met assessment.

## Delivered boundary and interpretation

The evolving native assembly is `models/designs/aries_cs_integrated/plant.sysml`, package `exploration/aries_integrated/aries_integrated/`. The 423.106794 MW case remains the **assumed integrated baseline**. Equipment choices are supplied independently of demand; scientific magnet, breeding, deposition, hydraulics, materials and machine-map qualifications remain unsupported.

The financial convention uses constant USD2004, an assumed 5% real rate, six-year construction represented by midpoint spending, 40 calendar operating years and 85% availability. The generated graph charges overnight capital with construction financing once; annual O&M, fuel, consumables and imports; dated blanket replacements; an explicit other-equipment overhaul allowance; and terminal decommissioning/disposal less declared salvage. Availability includes downtime. The alternative replacement reserve is excluded. See [assumptions and ownership](../../../active/WI-091_aries-integrated-lifecycle-cost/design.md).

“No breeding credit” means no credit for new usable tritium supply. Internal exhaust recycling remains in the modeled fuel loop. The inherited recovery input represents NEW usable T feed outside that loop, after extraction losses, in kg per calendar year. It must never include exhaust that was already credited through the permanent-loss calculation. The named 100 kg/year scenario includes a separate assumed 30 million USD2004/year supply-service charge. That charge and feed are independent scenario assumptions; they do not qualify breeding or define a recovery-equipment performance/cost law. They are not optimization controls.

## Verification still to complete

The accepted source/math/design review and 34-case native development receipt are retained. Final executed integration review, one sealed study, final source-comparison table, sensitivity reading, exact replay and prompt-04 handoff will complete this answer. Formal closure remains owner-held.
