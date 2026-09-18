# Computed tritium breeding

The model now calculates tritium production from a supported blanket configuration and makes inadequate breeding fail a design constraint. The current 0.80 m blanket fails the declared numerical adequacy screen. Increasing thickness improves breeding but raises cost and, in the studied cases, violates the peak magnetic-field limit. No case in this study is a feasible whole plant.

**The fresh independent grade is R2c.P3**, against the unchanged rubric. P2 is met because TBR is computed from blanket configuration and verified; P3 is met because computed adequacy changes the accepted blanket/build choices. This meets the modeling target, not physical plant qualification. Formal goal closure remains the owner's decision.

## What is calculated

The tritium breeding ratio (TBR) counts tritium atoms produced in the blanket per fusion neutron. In deuterium–tritium fusion, one tritium atom is burned and one neutron is emitted per reaction, so this is also production per tritium atom burned.

An isolated OpenMC neutron-transport calculation follows neutrons through the retained conceptual helium-cooled lead–lithium blanket and surrounding radial layers. It uses explicit isotope inventories and evaluated nuclear data. Five direct transport calculations supply a narrow, independently checked interpolation in breeder thickness. The generated plant executable evaluates that interpolation; the previous manually assigned TBR 1.074 input has been removed.

Supported breeder thickness is 0.60–1.00 m at fixed major radius 12.7 m, minor radius 1.3 m, circular cross section, other radial layers, 70% lithium-6 enrichment and a declared material/source/opening scenario. The breeder contains 80% lead–lithium, 10% steel and10% helium by volume. One 10.8-degree missing-breeder window is represented explicitly. These are documented conceptual assumptions, not actual stellarator port geometry. Thickness changes also propagate through the existing volume, coil-bore, magnetic-field and cost calculations. Other geometry changes make breeding explicitly undefined; the model does not extrapolate or silently retain a pass.

The executable also calculates gross production, extracted supply, breeder-extraction loss, exhaust-recycle loss, radioactive decay, stock growth and net fuel balance separately. At the current baseline, mean gross production is 1.1283×10²¹ atoms/s against burn 9.4175×10²⁰ atoms/s and assumed recycle loss 1.7893×10²⁰ atoms/s. Unity extraction and zero inventory/stock growth leave no extraction, decay or growth demand in that particular scenario.

## Which requirement applies

The existing 1.05 floor is retained as a design policy. The fuel balance requires 1.190 under the existing 5% burn fraction, 99% exhaust recovery, 100% breeder extraction and zero inventory/growth assumptions. Burning only 5% means much more tritium circulates than burns; losing 1% of that exhaust adds 19% to the replacement requirement. The original cost-derived 99% factor is not validated isotope-recovery evidence.

The constraint uses the stricter requirement: `max(1.05, calculated fuel requirement)`. It checks a numerical lower estimate, `mean TBR − 2 Monte Carlo standard errors − 0.01 interpolation allowance`, and requires valid applicability. This numerical screen is not a physical confidence bound. Even the 0.60 m case exceeds the old 1.05 floor but falls well short of the fuel requirement. The baseline mean exceeds 1.190, but its lower estimate does not. The model therefore does not claim established self-sufficiency.

## Actual study results

| Breeder thickness | Mean TBR | Numerical lower estimate | Breeding screen | Blanket cost | Electricity cost |
|---:|---:|---:|---|---:|---:|
| 0.60 m | 1.09145 | 1.07820 | Fail | $551.36M | $134.13/MWh |
| 0.80 m | 1.19807 | 1.18615 | Fail | $718.41M | $144.75/MWh |
| 0.825 m | 1.20630 | 1.19458 | Pass | $740.30M | $146.12/MWh |
| 0.90 m | 1.23096 | 1.21730 | Pass | $807.27M | $150.29/MWh |
| 1.00 m | 1.25245 | 1.23915 | Pass | $899.68M | $156.00/MWh |

The study retains ten supported cases and three deliberately unsupported cases. The 0.825–1.00 m samples pass breeding but fail the peak-field limit. Every case also retains divertor, winding-pack-fit and conductor-current failures. This is a sensitivity study, not a claim of an optimum or a precise feasibility boundary. The 0.55 m, 1.05 m and altered-major-radius cases fail breeding applicability; their zero numerical carriers are not interpreted as physical zero production.

Costs retain the existing blanket-account volume convention, which includes first-wall/reflector regions and differs from the actual neutron-transport breeder inventory. The neutron-energy multiplier remains held at 1.2; no new heat-production or plant-efficiency prediction is inferred from the tritium tally. These limitations are disclosed rather than repaired beyond this goal's scope.

## How it was checked

**Physical evidence:** approximate independent reconstructions of published lithium and lead/lithium sphere experiments give 0.69786 versus measured 0.685±0.03836, and 0.50413 versus 0.530±0.03180. Missing exact casing/penetrations limit that comparison. One adverse density sensitivity fails the declared diagnostic and remains in the record; no correction factor was fitted. Geometry, source sampling, isotope inventories, tally normalization/covariance and neutron balance have separate checks. All six withheld thickness calculations pass the predeclared interpolation test; the worst conservative discrepancy is 0.00932 against the 0.01 allowance.

**Software evidence:** independent interpolation and fuel-conservation implementations agree with the generated executable. The focused study passes 3,185 scalar comparisons and 260 independently derived constraint comparisons across all 13 cases. Generic study verification also passes. Native integration passes all ten gates. Static model validation remains failed at Levels 2/6; the independent audit maps all 32 new diagnostics to actual generated bindings and explicitly records the tool limitations.

## What remains uncertain

Material fractions, neutron-source shape, actual three-dimensional stellarator geometry, ports and omitted outer-component details can change physical breeding adequacy. At baseline thickness, declared material sensitivities span approximately 1.069–1.254 TBR. A peaked-source pilot also changes the result. Those variations are separate scenarios, not a justified probability distribution or plant uncertainty band. Better Monte Carlo precision alone will not resolve them.

A defensible next physical step is to replace the declared material/port/source assumptions with an engineering inventory and representative shaped geometry, then repeat transport and independent benchmark/data-library checks. Physical exhaust recovery and breeder extraction also need evidence before treating the conditional fuel requirement as demonstrated operating performance. Full fuel inventory and processing costs remain outside this goal.

## Evidence and identity

- [Independent final review and grade](evidence/round2/final-review-and-grade.md), with [machine-readable R2c.P assessment](evidence/round2/final-grade.cells.json).
- [Native study and complete results](../../../../exploration/stellarator_e2e/studies/20260918-computed-tritium-breeding/record.md).
- [Transport calculations and withheld checks](evidence/round2/transport/table-report.md), [independent physical release](evidence/round2/table-release-review.md), and [implementation audit](../../../active/WI-066_computed-tritium-breeding/audit.md).
- Audited model commit `d2e29237`; immutable study commit `5347d5a3`; [native integration receipt](evidence/round2/integration/integration_return.json). The package is separately identified from the published r2 comparison.
- [Goal trail](trail.md) records research, rejected surrogate transfer, decisions and native execution. [Archive preservation](evidence/round2/archive-preservation.json) confirms unchanged r2 bytes and historical study records. ARIES remains sealed; no reveal, frozen-comparison replacement, merge or push occurred.
