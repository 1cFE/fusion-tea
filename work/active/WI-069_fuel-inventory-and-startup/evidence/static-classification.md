# WI-069 static diagnostic classification

The entering L2 baseline contains 10 issues. The current L2 issues have identical normalized identities: no additions or removals. L6 changes from 1,076 to 1,079 issues. Full added/removed multisets and native metrics are in `static-delta.json`; location suffixes alone are normalized because inserted declarations move lines.

All three added L6 issues report an unsupported dot in a pure EXPOSE attribute: `mfe_plant_systems::'Fuel Cycle'::I_total = inventory.total_atoms`, `mfe_plasma::Plasma::fuel_volume = geom.V`, and `mfe_plasma::Plasma::n_T0 = sustain.n_T0`. They are real native validator errors, not passes. The current generator independently resolves those public dependencies, reproduces its package exactly, and native tests compare inventory-derived requirement/decay and the independent oracle's plasma-profile stock. This gives executable evidence for the three bindings while the static validator limitation remains.

No original L6 issue was removed. This classification is limited to the changed identity set and supported executable paths; it does not certify the inherited 1,076 issues or omitted physical processes. Full native validation is recorded separately in `native-validation.log` with its actual nonzero exit status.
