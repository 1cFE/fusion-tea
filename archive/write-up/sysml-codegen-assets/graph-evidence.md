# Stellarator graph evidence

[AGENT] This is a mechanically extracted, editorially selected view of the current generated stellarator package. The fourteen nodes are real TEAx modules. Every displayed edge is a direct declared binding; no path is collapsed. Labels are shortened for a public diagram.

## Identity

Current executable fingerprint: `3e3bf467fd98ad927cf12409f1c36807b92e9e8eaa4fd598a2fcd79c00ae698f`. Generator version: `0.1.1`; runtime contract: `2.0.0`. Repository HEAD at capture: `8014aa19417841deed838f2d101561360d81ea62`. This HEAD is checkout context, not an assertion that the generated package was built from that commit.

Pipeline: `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml`; SHA256 `933226bd9fb3b57c98251f6d1898697b139a208761ba2480ec05f4a461071f57`. The bytes match the package contract entry. Full source hashes, module keys, port bindings, defaults and omitted boundary inputs are in [graph-evidence.json](graph-evidence.json).

## Recommended figure

Read from axis field and radial build through peak field, selected current density and winding-pack size. From pack size, separate branches lead to geometric fit and material inventory/procurement. Conductor current is checked from the realized inventory. The three checks consume calculated field or margins; no check resizes the design to force a pass.

The drawing should label its scope “Magnet calculation slice; secondary inputs and other plant branches omitted.” Procurement is winding procurement cost, not complete magnet or plant cost.

| Diagram ID | Label | Pipeline line |
|---|---|---:|
| `radial_build` | Radial build | 504 |
| `field_calc` | Axis field | 112 |
| `coil_length` | Coil length | 552 |
| `peak_field_calc` | Peak conductor field | 623 |
| `current_sizing` | Current-driven pack sizing | 636 |
| `wp_sizing` | Winding-pack side | 669 |
| `wp_fit` | Winding-pack fit | 730 |
| `wp_volume` | Winding-pack volume | 762 |
| `material_inventory` | Material inventory | 815 |
| `winding_procurement` | Winding procurement cost | 847 |
| `conductor_current` | Conductor current margin | 871 |
| `peak_field_ok` | Field limit check | 3225 |
| `reference_conductor_current_ok` | Current margin check | 3234 |
| `wp_fit_ok` | Pack fit check | 3268 |

## Direct edges

| From | To | Producer output → consumer input |
|---|---|---|
| `radial_build` | `coil_length` | `r_coil_centre` → `a_coil` |
| `field_calc` | `peak_field_calc` | `root` → `B_axis_in` |
| `radial_build` | `peak_field_calc` | `r_coil_centre` → `a_coil_in` |
| `peak_field_calc` | `current_sizing` | `root` → `B_peak` |
| `current_sizing` | `wp_sizing` | `selected_effective_density` → `j_wp` |
| `wp_sizing` | `wp_fit` | `root` → `wp_side` |
| `coil_length` | `wp_volume` | `root` → `c_coil` |
| `wp_sizing` | `wp_volume` | `root` → `wp_side` |
| `wp_volume` | `material_inventory` | `vol_winding_pack` → `volume_in` |
| `material_inventory` | `winding_procurement` | `material_cost` → `material_cost_in` |
| `material_inventory` | `winding_procurement` | `tape_volume` → `tape_volume_in` |
| `coil_length` | `winding_procurement` | `root` → `c_coil` |
| `winding_procurement` | `conductor_current` | `conductor_length` → `conductor_length` |
| `winding_procurement` | `conductor_current` | `tape_length` → `tape_length` |
| `peak_field_calc` | `conductor_current` | `root` → `B_peak` |
| `peak_field_calc` | `peak_field_ok` | `root` → `B_peak` |
| `conductor_current` | `reference_conductor_current_ok` | `margin_fraction` → `margin_fraction_in` |
| `wp_fit` | `wp_fit_ok` | `minimum_margin` → `minimum_margin_in` |

## Frozen study distinction

`20260915-joint-magnet-sizing` records package commit `a8589d6b5aebbb42c525f7bab9a036a474fc8e6b` and executable fingerprint `8e4aa8eaebf2667a74565e6e66fc9ce5947c6d27ccfc210f8452e82d87fba45f`. Its saved pipeline SHA256 is `64db3141ee887c53f3b79739f18c1ae4c8931358fb9bcd5d809b6047950a9ade` and matches its snapshot. Thirteen of fourteen full module specifications match the current pipeline. The current radial-build module adds an `outer_radius` output unused by this view. **All eighteen displayed port-level edges match the frozen pipeline.** This compares names, types, input bindings and outputs only; it does not establish identical implementations, defaults or results.

`20260917-pre-reveal-feasible-neighborhood` records package commit `d53d6ec5748442833ff44bc179bb988bce726486` and executable fingerprint `f52729e684f513d1b210c75f523340085786440fa2828490309b96493755fd14`. Its saved pipeline SHA256 is `df7a42ce2c9d0c572655bd52107103143791c323088e30b00dac91df8e78f2d1` and matches its snapshot. Thirteen of fourteen full module specifications match the current pipeline. The current radial-build module adds an `outer_radius` output unused by this view. **All eighteen displayed port-level edges match the frozen pipeline.** This compares names, types, input bindings and outputs only; it does not establish identical implementations, defaults or results.

## Authentic snippets

The JSON below is a subset of the current `inputs/stellarator_plant_params.json`, retaining exact names and values. Other parameters remain in that file and other parameter groups.

```json
{
  "stellarator_09__stellaris__plasma__R": 12.7,
  "stellarator_09__stellaris__magnet__coil__I_coil": 15400000.0,
  "stellarator_09__stellaris__magnet__coil__n_coils": 48.0,
  "stellarator_09__stellaris__magnet__coil__k_link": 0.7731331164622419
}
```

The following module blocks are verbatim pipeline excerpts. The field calculation shows shared attribute inputs and library defaults. Pack sizing shows a calculated input alongside an external input.

```yaml
  stellarator_09__stellaris__magnet__field_calc:
    module_type: mfe_magnet_field.Coil_Set_Axis_FieldModule
    inputs:
      two_pi: float mfe_magnet_field_params.stellarator_09__stellaris__magnet__field_calc__two_pi
      I_coil: float stellarator_plant_params.stellarator_09__stellaris__magnet__coil__I_coil
      R0: float stellarator_plant_params.stellarator_09__stellaris__plasma__R
      n_coils: float stellarator_plant_params.stellarator_09__stellaris__magnet__coil__n_coils
      k_link: float stellarator_plant_params.stellarator_09__stellaris__magnet__coil__k_link
      mu0: float mfe_magnet_field_params.stellarator_09__stellaris__magnet__field_calc__mu0
    outputs:
      root: RootModel[float] stellarator_09__stellaris__magnet__field_calc__B_axis
```

```yaml
  stellarator_09__stellaris__magnet__wp_sizing:
    module_type: mfe_magnet_field.Winding_Pack_SizingModule
    inputs:
      j_wp: float stellarator_09__stellaris__magnet__current_sizing__selected_effective_density
      I_coil: float stellarator_plant_params.stellarator_09__stellaris__magnet__coil__I_coil
    outputs:
      root: RootModel[float] stellarator_09__stellaris__magnet__wp_sizing__wp_side
```

The source calculation is `models/library/analyses/mfe_magnet_field.sysml:4`; its output expression is `B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)`. Its usage bindings are at `models/library/cost_structure/mfe_power_core.sysml:174`. The coil-set linkage factor is a held transfer assumption, not a solved three-dimensional magnetic field.

## Verification limits

This extraction checked declared channel producers, free-input keys and the two frozen pipeline hashes. It performed no model execution and no independent physical validation. The current complete package has changed since both studies; retain their frozen evidence for numerical claims.
