# Bounded execution design

[AGENT] Source review gates these choices. Implementation corrects false source attributions and implements explicit source-conditioned scenarios with complete raw diagnostics. No new physical equation, criterion, conductor gain, cavity dimension or coolant circuit is introduced.

## Native model correction

Use the quick-model workflow for comment/doc-only changes in canonical `models/designs/stellarator_09/stellarator_plant.sysml` and its byte-identical exploration twin. Correct the HCLL attribution to a retained helium-primary alternative with source water-blanket/separate-helium-first-wall scope. Correct the generic 0.80m blanket layer's label, currently called a Stellaris thickness, to its actual external-library scenario provenance. Add exact profile values from original Fig16 as the explicit reconstruction alternative, preserving numeric defaults and historical digitization. Keep calculation definitions and all inputs unchanged. Validate unchanged comment-stripped model text and package outputs; native integration establishes whether regenerated metadata/snapshot require synchronization.

## Scenario experiment

All cases are sensitivity/attribution, never optimization. Retain legacy default and selected-current-sizing mode with1.01 inventory reserve controls. Add exact0.35/1.2 fuel/temperature profiles in both controls. Add a Table5 plasma-conditioned pair usingR12.74,a1.3,V425 andB9: volume shaping is recalculated exactly, and operational coil ampere-turns scale withR to preserve the reduced-model on-axis9T at unchanged bore. That compensating current is an agent-derived conditioning input, not a published coil prediction. Fixed magnet shape reference anchors remain historical and explicit; no source-global geometry claim. Add two off-reference cases from the exact-profile legacy baseline: R increased2% and a increased2%, individually. Keep shape factors fixed in these two scaling checks. Eight cases total; all outputs and20 predicates survive.

Any native entry-input constraint or axis gate that blocks these cases is reported before execution. A mathematically equivalent native mapping may replace a proposed key only after verified ownership/entry fan-out. Conductor selected-mode exact floating boundary is tracked separately; the existing1.01 reserve avoids counting roundoff as margin. No material scenario tuning to pass.

## Reporting

One machine-readable per-case report joins qualified predicate identities, raw verdict, scope/application (`conditional_model_scenario`, `source_unresolved`, or `source_incompatible_scenario`), reason and evidence. All20 raw diagnostics count in raw combined feasibility; source qualification is explicitly unresolved irrespective of their count. No filtered combined pass is calculated. Local pack fit is unresolved for the source; absolute conductor current is conditional construction/field-angle transfer; divertor peak is a transport surrogate at the computed load; helium loop/cycle screens belong to the deliberate coolant scenario. Other checks preserve their existing reduced-model scope and limits.

A separate source-conditioned divertor account uses500MW and90%radiation with paired (capture0.99,peak9.5,T200,diffusion1) and(capture0.97,peak5,T100,diffusion3). Deposited/uncaptured power and peak-equivalent area are derived. The peak is supplied, so this earns accounting consistency only. Source pointA/B quantities are evidence rows, not injected all-plant outputs.

Per-case costs retain native LCOE, capital, magnet procurement, heating and pump/cycle response where available. Attribute only isolated or explicitly coordinated contrasts. Water cooling hardware and local cavity/conductor qualification costs remain unpriced; source estimates and assumed tape price have differing cost bases.

## Verification and ownership

The coordinator owns this design, source-to-model/applicability decisions and final answer. A worker can own the new native study directory and execute integration/study after release. Every point is compared to the package-owned independent oracle, including raw verdicts. Independent reviewer checks scientific interpretation before execution and final implementation/numerical/source fidelity afterward. Freeze files are excluded from every mutation and checked unchanged. Study results must be committed before synthesis and remain immutable.

[AGENT review correction] Source TBR1.074 is a held result of the source water/PbLi neutronics, just as multiplication1.2 is source-case conditioned. The helium/generic-build case's breeding/fuel checks must be marked conditional transfer; retaining a satisfied rawTBR predicate does not establish source-valid breeding after coolant/geometry changes. Correct the source doc attribution and report this limitation without changing the number.

[AGENT control-fidelity correction, 2026-09-16] The existing comparison's exact selected mode uses inventory_multiplier = 1.0, as recorded in `.project/active/aries-comparison-preparation/package/selected-mode-check.json` and input-rules.json. The eight new study cases use 1.01 only in explicitly labeled reserve scenarios. Reuse the historical exact selected-mode diagnostic as a separate control: numerical model/package identity is unchanged. Preserve its 224/226 strict relative scalar matches and 19/20 predicate matches, including signed near-zero current-margin differences. It is neither a ninth parity-certified study case nor a filtered pass. The new study must pass its normal verification gates without a boundary exception.
