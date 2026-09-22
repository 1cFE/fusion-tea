# T03–T05: work that needs additional scientific inputs

[AGENT] Sequential disposition after T02, 2026-09-21. These are open transfer areas, not completed models or engineering failures. The reviewed profile and constituent increments do not provide the inputs listed below. This uses the existing audit evidence; no new acquisition search or numerical experiment is claimed.

## T03: magnetic field and mechanical loads

[INHERITED: physics-inventory.md; existing field-qualification/capability-contract.md] A qualified calculation requires identified three-dimensional coil paths, signed current families, selected turns/pack dimensions, an axis definition and independently checked field/peak conventions. Current scalar radii/current and a calibration factor do not supply that configuration. Finite packs matter for conductor peak field; point-filament self-field is singular.

[AGENT] Disposition: retain as requiring a new qualified field/mechanical treatment and authenticated design data. Do not retune the scalar calibration to the published field. The prior archive search concerned named Stellaris files; it is not evidence that every ARIES geometry source has been searched. Actual ARIES configuration acquisition/reconstruction and verification remain work, not a small input-range repair. [Required evidence](../../../.project/active/aries-comparison-preparation/field-qualification/capability-contract.md), [prior acquisition limits](../../../.project/active/aries-comparison-preparation/geometry-acquisition/report.md).

## T04: conductor performance

[INHERITED: physics-inventory.md and alternative-point-screen/evidence/domain-rules.json] The current performance model is REBCO at 20 K over its documented field interval. The reference uses low-temperature superconducting technology. A wider numerical interval would not turn one technology's performance relation into the other.

[AGENT] Disposition: retain as requiring an applicable Nb3Sn performance model, operating temperature/strain/product assumptions and explicit winding/current definitions. A generic published superconducting curve alone does not identify the selected ARIES conductor. Source peak-field values can be reported as source results, but do not establish calculated field or current adequacy. No extrapolation or new performance claim was implemented.

## T05: tritium breeding

[INHERITED: physics-inventory.md and current mfe_tritium_breeding implementation] The current response dataset fixes major/minor radius and several geometry/material coordinates. WI-084 supplies a constituent accounting representation, not a neutron transport response. Its source recipes cannot establish tritium production.

[AGENT] Disposition: retain as requiring geometry/material-specific transport calculations or a validated response dataset with an applicable interpolation domain. Existing definedness/interpolation interfaces may transfer, but source TBR inserted as an input would be a supplied result, not independently predicted breeding. No guard widening or source-output substitution was performed.

## Continue independent work

[AGENT] These dependencies prevent supported whole-plant engineering evaluation. They do not prevent testing the implemented plasma producer against unchanged downstream fuel balances or testing accounting under explicitly supplied boundaries. Advance to T06 while keeping all three scientific areas open in the change register. This is a documented implementation choice under the owner's instruction to continue area by area, not a claim that the missing work is impossible.
