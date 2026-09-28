# WI066 validation diagnostic comparison

The full validation remains failed at Levels2 and6. Levels1,3,4 and5 pass. Do not describe all failures as inherited: a same-scope Level6 comparison identifies32 new diagnostic identities.

## Published logs have different scopes

WI065 `native-validation.log` checked canonical `models/`:41 files,13 analyzed documents,22 numerical constraint usages,126 documented elements,78 calc definitions,88 usages,533 bindings,209 design attributes. Its Level6 summary reports267 issues,94 incomplete attributes and81 unextractable attributes.

WI066 `validation.log` checks the MFE exploration twin:34 files,8 analyzed documents,20 numerical constraint usages,110 documented elements,72 calc definitions,81 usages,514 bindings,177 design attributes. Its Level6 summary reports336 issues,83 incomplete attributes and77 unextractable attributes. Comparing267→336 alone cannot attribute69 new issues to WI066 because scope and capture time differ.

Both logs show the same10 placeholder-binding warnings and no unbound calc inputs, undefined bindings, circular dependencies or malformed numerical constraints. The visible warnings concern literal `ref_power`/`alpha` inputs for waste, other_rpe and inc_cost. Both logs show inherited capital-cost derived-expression diagnostics at generic-plant lines386,392,476 and608. The log excerpts truncate the remaining issues and cannot prove their identities.

## Same-scope comparison

Re-executed only the Level6 validator against the current MFE twin, saved in `L6-current-comparison.json`. Compared diagnostic identities against WI065 `L6-candidate.json`, stripping source-path/line suffixes and retaining multiplicity. Exact delta:304→336 issues,32 added,0 removed. Full identities are in `L6-diagnostic-comparison.json`.

- 14 added unsupported-dot diagnostics:6 Transport Calculated Blanket outputs (`tbr_li6`, `tbr_li7`, `tbr_std_error`, `interpolation_allowance`, `tbr_lower`, `breeding_defined`);5 Stellaris adequacy aliases (`breeding_requirement`, `breeding_design_margin`, `breeding_fuel_margin`, `breeding_numerical_margin`, `breeding_adequacy_defined`);3 Fuel Cycle outputs (`loss_rate`, `tbr_required`, `tbr_margin`).
- 7 added missing-value/binding diagnostics on subtype attributes `breeding_R`, `breeding_a`, `breeding_kappa`, `breeding_ht_shield_t`, `breeding_structure_t`, `breeding_gap1_t`, `breeding_vessel_t`.
- 11 added numeric-default extraction diagnostics for the6 blanket and5 adequacy aliases above.

These new diagnostics need disposition against occurrence-level bindings and generated dynamic dataflow. Successful generation or runtime checks can establish those behaviors but cannot make this validator pass retroactively. This report supplies no blanket waiver and changes no production model.

## Concrete binding disposition for independent review

`L6-binding-disposition.json` records all32 diagnostics across21 attributes, the inspected successful probe pipeline/contract hashes, exact parameter bindings and generated output channels. This is a new-diagnostic disposition, not an inherited waiver. Every checked channel exists in the probe contract. All7 geometry attributes resolve to existing owner parameters; none becomes a duplicate independent input. The instance bindings are at `models/designs/stellarator_09/stellarator_plant.sysml:567` on the specialized blanket occurrence; the subtype's intentionally unbound definitions are at `models/designs/generic_mfe/mfe_subsystems.sysml:104`.

| Subtype formal | Breeding calc input | Concrete parameter suffix |
|---|---|---|
| `breeding_R` | `R_in` | `plasma__R` |
| `breeding_a` | `a_in` | `plasma__a` |
| `breeding_kappa` | `kappa_in` | `plasma__kappa` |
| `breeding_ht_shield_t` | `ht_shield_t_in` | `shield__ht_shield_t` |
| `breeding_structure_t` | `structure_t_in` | `structure__structure_t` |
| `breeding_gap1_t` | `gap1_t_in` | `vessel__gap1_t` |
| `breeding_vessel_t` | `vessel_t_in` | `vessel__vessel_t` |

The6 blanket aliases each have two static diagnostics and resolve to the response calc outputs. The5 adequacy aliases each have two and resolve to adequacy calc outputs. Fuel Cycle's3 aliases each have one and resolve to fuel calc outputs. Exact per-alias mappings are in the disposition JSON. The11 numeric-default failures are expected for dynamic computed outputs: inserting constants to quiet them would disconnect the computation. The14 dot-operator warnings likewise concern dynamic aliases that this successful native probe resolves. No missing concrete wire was found in this32-diagnostic set. Runtime numerical behavior and physical adequacy still require their separate tests and independent audit; this inspection does not claim the static validator now passes.
