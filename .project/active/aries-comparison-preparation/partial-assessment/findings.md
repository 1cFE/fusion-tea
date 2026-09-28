# Findings for the write-up: partial assessment

Continuation of [F-001–F-009](../post-reveal-investigation/findings.md). These are post-reveal findings from a separately authorized diagnostic assessment, not a clean hold-out result. Original experiment and audit records remain unchanged.

## F-010 — The conductor refusal hid independent results

[OBSERVATION] One native diagnostic evaluation of the identical 704 inputs retained 1,341 numeric outputs and 66 of 67 predicates. The conductor calculation still refused 56.61785714285713 T at 20 K. All 276 comparison rows were retained. Evidence: [result](attempts/diagnostic-1/result.json), [raw diagnostic](attempts/diagnostic-1/native-diagnostic.json), [receipt](attempts/diagnostic-1/receipt.json).

[INTERPRETATION] The earlier absence of all downstream reporting was an execution-contract limitation, not proof that every plant calculation depended on conductor performance. Diagnostic recovery does not establish scientific applicability, source correspondence or whole-plant feasibility.

## F-011 — Three selected-equipment failures are independent of the field finding

[OBSERVATION] Cold-stage cooling is short by 649.468 W; intercept-stage cooling by 375.736 W; winding-pack fit has a minimum margin of −0.120 m. Actual graph paths do not connect these checks to either field root. Evidence: [predicate report](attempts/diagnostic-1/report.json), [field qualification](attempts/diagnostic-1/field-qualification.json); cooling capacity bindings in `models/library/structure/mfe_plant_systems.sysml:486` and `:498`.

[INTERPRETATION] These are deficiencies of the held equipment under the represented assumptions. They are not claims about the actual ARIES equipment, which this three-scalar transfer does not reconstruct. No equipment was resized or replaced during the assessment.

## F-012 — Native violated and satisfied statuses need applicability context

[OBSERVATION] Native counts are 51 satisfied, 15 violated and one unavailable. Five violated checks have `defined_in=0`: breeding and four helium-equipment checks. The satisfied fuel-processing-capacity check also has an upstream module-definedness limitation. Evidence: [all-67 interpretation supplement](evidence/predicate-interpretation.json), [source script](evidence/interpret_predicates.py).

[INTERPRETATION] A failed combined “defined and adequate” predicate cannot by itself establish physical inadequacy. A satisfied predicate cannot clear an unsupported upstream calculation. The supplement retains every native status and adds interpretation without rewriting the experiment. Six conservative model-definedness guards propagate separately from field applicability; observed native predicate guards add the equipment-condition distinction.

## F-013 — Finite LCOE arithmetic remains unusable

[OBSERVATION] Raw discounted-cash-flow and other-convention LCOE carriers are 2,381.9160099583733 and 2,334.2430908879587 USD/MWh. Both depend on an unqualified field calculation and undefined upstream breeding/fuel-account interpretation. Both diagnostic values and supported predictions are null. Seventeen row values are suppressed by tracked definedness guards. Evidence: [report](attempts/diagnostic-1/report.json), [guard propagation](attempts/diagnostic-1/model-definedness.json).

[INTERPRETATION] Retained finite arithmetic must not be presented as a defensible plant-price estimate. Independent equipment purchase inputs can be retained without qualifying the economic total. Dependency propagation is conservative at module granularity; it may withhold outputs whose finer internal formulas are independent.

## F-014 — A strict numerical boundary needs separate review

[OBSERVATION] The facility-occupancy predicate reports a margin of −4.547473508864641e−13 and a violated status. No tolerance, input or equation was changed. Evidence: [predicate interpretation](evidence/predicate-interpretation.json).

[INTERPRETATION] This is a recorded strict-boundary violation, not demonstrated material occupancy shortfall. Review numerical treatment separately from field qualification and hardware changes. This assessment does not certify it as rounding error or silently turn it into a pass.

## Remaining scientific work

[AGENT] Qualify field applicability and geometry/current/pack dependence before claiming a complete magnetic or economic comparison. Breeding support, helium equipment performance away from supplied offer conditions, the selected cooling ratings and pack fit remain separate issues. The [readable assessment](report.md) connects these findings to the next decisions. No corrected magnetic field, new empirical interval or ARIES-equipment reconstruction has been inferred.
