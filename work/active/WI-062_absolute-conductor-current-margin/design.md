# WI-062 design for source/interface review

Status: proposed; normalization remains subject to T-001 source research and independent review.

## Scientific basis and qualification

[AGENT] Use a source-derived 20 K, perpendicular-field, 4 mm tape reference current at20T, with linear transfer to6mm width at fixed56µm full composite construction. Tentative200A is rounded from a published175A lot-average77K self-field current times1.13 fitted lift. It is a statistical manufacturing scenario, not a directly measured56µm specimen value. Reference sample and production spread scenarios must remain distinct; the completed research report owns the evidence and may replace this provisional normalization before release.

[AGENT] Use Ic_tape=Ic_ref*(width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor. This is a supported simple empirical approximation within inspected field measurements, with explicitly opted-in extrapolation outside their field extent. No temperature fit is inferred. Width transfer, same product family and layer construction, ideal sharing and uniform field application are assumptions, not qualification. Normalization, its construction transfer and exact field domain require independent source review.

[AGENT] Source caveat: the existing source's graded80% criterion is not proof that the ungraded reference pack was sized at80%. Preserve the existing reference density and relative-envelope sizing as inherited inventory scenarios. Apply allowable_fraction exactly once, to the margin, never to Ic or tape quantity. Explain any discrepancy with the source's ungraded operating fractions through different product, homogenization and field-angle treatment; no parameter fitting to reproduce their passes.

## Inventory mapping and outputs

[AGENT] Use the measured actual peak field, inventory temperature and actual tape dimensions. Reconstruct N_set=tape_length/conductor_length and N_ref=N_set*f_set/f_wp_vol. Both are continuous effective parallel-tape counts. The reference-conductor critical current is N_ref*Ic_tape*cabling_factor*degradation_factor*sharing_factor; expose the corresponding set-average value separately. Compare the common modeled turn_current with each. The named predicate screens the reference-conductor estimate. No claim that reference density bounds every actual coil is made. Series lengths cancel in the ratio and cannot multiply capacity.

[AGENT] Report at least: N_set, N_ref, tape_Ic, Ic_reference, Ic_set, operating_fraction_reference, operating_fraction_set, allowable_current=allowable_fraction*Ic_reference, margin_fraction=allowable_fraction-operating_fraction_reference, margin_A=allowable_current-turn_current and field_extrapolated(0/1). Predicate is margin_fraction>=0, accepting exact boundary without a hidden tolerance. Margin is a fraction of critical current, not a percentage of operating current. All factors and allowances are public named inputs, with provenance.

## Controls and unsupported inputs

[AGENT] Proposed nominal controls: material_factor=1, orientation_factor=1(perpendicular), cabling_factor=1, degradation_factor=1, sharing_factor=1(ideal upper-limit assembly transfer), allowable_fraction=0.8. The three retention factors each lie in(0,1]; they have distinct named mechanisms and are not additional operating allowances. Sensitivities may combine them, with no calibrated physical stress law implied. Material and orientation multipliers are positive assumed scenarios, not fitted angular predictions.

[AGENT] Temperature must match20K, full composite thickness56µm, and width4–6mm under the declared linear-width transfer. Reject nonfinite/invalid inputs and intermediate/output overflow/underflow. Tape/conductor lengths, distribution factors and turn current must be positive. Actual field must be positive. Out-of-measurement-domain fields require an explicit allow_field_extrapolation switch; emit field_extrapolated. The model should never silently call extrapolated values measured. Use nominal allow_field_extrapolation=1 to evaluate entering24.9–30.18T cases under the owner-requested explicit extrapolation assessment. Exact field-support interval is finalized from the source report.

## Native ownership and interface

[AGENT] Add one material-specific reusable analysis definition to `models/library/analyses/mfe_conductor_current.sysml`, using the established typed manual-completion pattern for validation and arithmetic. Add inputs to Winding Pack in `mfe_magnet_parts.sysml`. Magnet System in `mfe_power_core.sysml` owns the calc, binds procurement tape/conductor lengths through exposed producer attributes and exposes the result. Source-derived scenario values live in stellarator design. Define the fraction-margin constraint in the library and assert it with bindings-only in the stellarator design. Existing generic MFE definition inherits additional inputs; enumerate this consumer and preserve prior equations. Canonical MFE twin must match exactly.

[AGENT] Retain all nineteen entering predicate expressions, including peak_field_ok. It remains the declared demand<=selected sizing-envelope requirement; the new estimate depends independently on actual field, tape quantity and material/assembly evidence. Neither predicate implies the other. Demonstrate independent outcomes by low/perpendicular performance within envelope and high/oriented performance outside it. The latter remains rejected by the full predicate set.

[AGENT] Existing generated manual bodies stay byte-identical. Add one reviewed body, fresh-generate using explicit seed inventory, refresh contract fingerprints, census and snapshot through native producers. Extend independent oracle equations and entry/output/operand mappings. No caller-side current calculation fills missing model behavior.

## Verification and study handoff

[AGENT] Test analytic synthetic examples and actual-reference values; exact boundary, each side, invalid temperature/construction/extrapolation flag/factors and arithmetic; inventory identity, turn repartition invariance, actual-field response, density/envelope/tape propagation; retention/allowance separation; field-envelope independence. Compare all212 prior native scalar outputs and19 prior verdicts at reference; compare all196 entering oracle-mapped channels at matching study coordinates. Candidate study must evaluate reference, three former nominal eighteen-predicate passes, twelve entering nineteen-predicate passes and historical cases as named references. Material, angle and retention sensitivities are bounded engineering scenarios, not search or qualification.

[AGENT] Required independent release covers source normalization/applicability, inventory units, reference-versus-set interpretation, implicit allowance, domain behavior and predicate independence. Postimplementation review checks consequential bindings, native/generated/oracle behavior, preservation and study findings; reuse the same fresh non-author reviewer.
