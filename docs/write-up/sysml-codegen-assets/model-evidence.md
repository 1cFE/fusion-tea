# Stellarator code evidence for the public explainer

[AGENT] Checked against current local files on 2026-09-19. These are source excerpts, not new model changes or a fresh execution. Code fences omit surrounding packages/imports and documentation only where stated. Sources are current mutable files; hashes below identify this reading. Do not assume these current files are identical to the September 17 study's frozen package.

## Recommended opener: current and geometry produce magnetic field

Source: `models/library/analyses/mfe_magnet_field.sysml`, lines 4–46. The excerpt removes documentation and comment lines but retains the full declaration and its exact mathematical expression.

```sysml
calc def 'Coil Set Axis Field' {
    in attribute n_coils : Real;
    in attribute I_coil : Real;
    in attribute k_link : Real;
    in attribute R0 : Real;
    in attribute mu0 : Real default 1.25663706212e-6;
    in attribute two_pi : Real default 6.283185307179586;

    out attribute B_axis : Real = mu0 * k_link * n_coils * I_coil / (two_pi * R0);
}
```

Interpretation: coil count, single-coil ampere-turns, a held linkage factor, and major radius produce the axis-averaged field. `I_coil` uses a historical “current” name, but the model's winding-sizing documentation explicitly identifies it as total ampere-turns. It is not the per-turn transport current. `k_link` transfers the reference coil set's current distribution and axis linkage; this expression is not a three-dimensional magnetic-field solver.

The reusable component is declared as `part def 'Magnet System' :> 'CAS22.1.3 Magnet System'` at `models/library/cost_structure/mfe_power_core.sysml:77`. Inside it, lines 174–179 bind the calculation:

```sysml
calc field_calc : 'Coil Set Axis Field' {
    in n_coils = coil.n_coils;
    in I_coil = coil.I_coil;
    in k_link = coil.k_link;
    in R0 = coil.R0;
}
```

The same component exposes the result at line 105:

```sysml
attribute B : Real = field_calc.B_axis;
```

The concrete design starts with `part stellaris : 'MFE Power Plant'` at `models/designs/stellarator_09/stellarator_plant.sysml:34`, refines `magnet` at line 105 and its `coil` at line 193. The design binds 48 coils at line 215 and 15,400,000 ampere-turns at line 246. Preserve these paths if showing a shortened nested component illustration; do not invent a new toy component.

## Geometry check: the winding pack must fit its casing

Source: `models/library/cost_structure/mfe_power_core.sysml`, lines 267–277. Exact calculation usage:

```sysml
calc wp_fit : 'Winding Pack Casing Fit' {
    in wp_side = winding_pack.wp_side;
    in aspect_ratio = winding_pack.fit_aspect_ratio;
    in internal_fraction_x = winding_pack.internal_build_x;
    in internal_fraction_y = winding_pack.internal_build_y;
    in ground_insulation = winding_pack.ground_insulation;
    in radial_allocation = coil.coil_t;
    in interior_y = casing.interior_y;
    in wall_thickness = casing.wall_thickness;
    in assembly_clearance = casing.assembly_clearance;
}
```

The result is exposed at line 294:

```sysml
attribute fit_minimum_margin : Real = wp_fit.minimum_margin;
```

The constraint definition is in `models/library/analyses/mfe_winding_pack_fit.sysml`, lines 38–42; its documentation comment is omitted here:

```sysml
constraint def 'Winding Pack Fits Casing' {
    in attribute minimum_margin_in : Real;
    minimum_margin_in >= 0.0
}
```

Its concrete assertion is in `models/designs/stellarator_09/stellarator_plant.sysml`, lines 2008–2010:

```sysml
assert constraint wp_fit_ok : 'Winding Pack Fits Casing' {
    in minimum_margin_in = magnet.fit_minimum_margin;
}
```

The calculation compares a centered, aligned rectangular winding envelope against a casing cavity after insulation and assembly allowances. A negative finite margin is a valid failed check. This is a local geometric screen, not global nonplanar fit or manufacturing qualification. Its calculation definition declares outputs without executable expressions; the normative equations are in its documentation and its implementation is handwritten.

## Actual handwritten numerical implementation

Source: `exploration/stellarator_e2e/generated/handwritten/mfe_magnet_field/winding_pack_sizing_impl.py`, lines 8–14. Exact function:

```python
def run_winding_pack_sizing(inputs: Winding_Pack_SizingInput) -> float:
    """Size finite nonnegative amp-turn magnitude at finite positive A/mm²."""
    if not math.isfinite(inputs.I_coil) or inputs.I_coil < 0:
        raise ValueError("Winding Pack Sizing: I_coil must be finite and nonnegative")
    if not math.isfinite(inputs.j_wp) or inputs.j_wp <= 0:
        raise ValueError("Winding Pack Sizing: j_wp must be finite and positive")
    return (((inputs.I_coil / inputs.j_wp) ** 0.5) / 1000.0)
```

This file declares `AUTO_IMPLEMENTED = False` at line 5. It receives a generated typed input object, enforces the model's numerical domain, and returns the winding-pack side in metres. The division by 1,000 converts the square root's millimetres to metres. The model contract is `models/library/analyses/mfe_magnet_field.sysml:91–139`: inputs `I_coil` and `j_wp`, output `wp_side`, and the normative sizing equation and domain in its documentation. `models/library/cost_structure/mfe_power_core.sysml:244–247` binds its usage. This is an actual small handwritten numerical method; do not call it a surrogate or imply its Python was translated automatically.

A richer real manual method is `exploration/stellarator_e2e/generated/handwritten/mfe_conductor_current/rebco_conductor_current_impl.py`. It computes conditional tape/composite-conductor capacity with explicit width, temperature, field, and extrapolation checks. It is useful if the article needs an example beyond a square root, but its source-transfer assumptions need more explanation than the compact sizing function.

## Actual response-table surrogate

The current stellarator package uses a handwritten piecewise-linear breeding response at `exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py:17–39`. Its embedded table comes from the design-owned `models/designs/stellarator_09/breeding_response.json`. That asset records five thickness nodes from 0.60 to 1.00 m, the fixed geometry, scenario, numerical validation, and OpenMC 0.15.2 provenance. At evaluation time this function interpolates existing transport results; it does not run neutron transport or train a model.

Exact interpolation lines 28–34, after the finite-input, fixed-geometry, and thickness-domain checks:

```python
index = min(bisect.bisect_right(thicknesses, thickness) - 1, len(nodes) - 2)
left, right = nodes[index:index+2]
fraction = (thickness - left['thickness_m']) / (right['thickness_m'] - left['thickness_m'])
li6 = left['tbr_li6'] * (1-fraction) + right['tbr_li6'] * fraction
li7 = left['tbr_li7'] * (1-fraction) + right['tbr_li7'] * fraction
mean = li6 + li7
variance = ((1-fraction)*left['std_error'])**2 + (fraction*right['std_error'])**2
```

The function also calculates a numerical lower estimate using the interpolated statistical uncertainty and an interpolation allowance. Inputs outside the fixed geometry or thickness interval return an undefined response (`breeding_defined = 0`); the seven zero-valued return slots are not a physical prediction of zero breeding. The response is conditional on the modeled toroidal helium/PbLi scenario and opening/material assumptions. The numerical lower estimate is not a physical confidence bound, and this is not a validated shaped-stellarator transport solution.

Suggested public prose: “The blanket model uses a response table from neutron-transport calculations. A handwritten function interpolates that table as blanket thickness changes within the investigated range. The plant model receives the breeding estimate through the same typed calculation interface as the simpler equations.”

## Actual structural substitution, if needed

There is a real blanket specialization, not merely a hypothetical technology swap. `models/designs/generic_mfe/mfe_subsystems.sysml:101` declares:

```sysml
part def 'Transport Calculated Blanket' :> 'Blanket' {
```

`models/designs/generic_mfe/mfe_plant.sysml:162` declares the inherited usage:

```sysml
part blanket : 'Blanket' {
```

`models/designs/stellarator_09/stellarator_plant.sysml:566` selects the specialization:

```sysml
part :>> blanket : 'Transport Calculated Blanket' {
```

These are exact opening declaration lines from three separate contexts, not one standalone code block. The specialization owns a `breeding` calculation using `'Blanket Tritium Breeding'` at `mfe_subsystems.sysml:113`, replacing a held breeding-ratio interface with a computed response. This demonstrates selection of a more specific component model. It does not establish interchangeable blanket materials or a runtime switch between helium and another primary coolant.

## Implementation preservation

Both translated and custom Python implementations live under `handwritten/` in the generated package. Preservation options can retain an existing body when its interface is unchanged, even if the SysML equation has changed. Generating a fresh package updates translated equations; retaining implementations requires checking them against the revised model.

For a calculation whose expression cannot be translated, codegen can generate the function interface with a placeholder body that raises `NotImplementedError` until the author supplies the method. The declared inputs and outputs place that implementation in the plant's calculation network; broken plant wiring still blocks generation.

## Input-generation details

When a calculation reads an externally supplied attribute, such as the plasma radius, codegen exposes the supplying attribute as a public input. Several calculations that read that attribute share the same input. A value supplied by a calculation remains connected to its producing output.

Authored values provide initial settings. A literal bound directly to a calculation input is also exposed with that literal as its initial value. A calculation input left unbound becomes a public input with its supported modeled default, or a `null` placeholder that must be filled before evaluation. A missing or ambiguous reference stops generation; it does not become a free parameter.

Inputs are grouped into files, normally by their declaring model source. Keys within each file are flat and preserve component paths rather than reproducing the nested component tree. Schemas describe types and defaults. File-based runs load JSON, while studies can supply typed values in memory.

## Source SHA-256

| File | SHA-256 |
|---|---|
| `models/library/analyses/mfe_magnet_field.sysml` | `aebe4e7caca0bdd8cc8d722c3cdaea626386396eb750fe392a3115c1b4d419a0` |
| `models/library/cost_structure/mfe_power_core.sysml` | `83b321a3314abf65cb143566630a4a736e07fc248c8f8de687b9ec8361c196ef` |
| `models/library/analyses/mfe_winding_pack_fit.sysml` | `8de45020c7efe4d6b03ed43615f7743967c2c5e7a681d8f462d7b0a3e358a8ca` |
| `models/designs/stellarator_09/stellarator_plant.sysml` | `2a2c2cd95b9bc90b00fcc9a5e9cf9fbf25e95dbb62a6a79ebda183a92d4f50ec` |
| `models/designs/generic_mfe/mfe_subsystems.sysml` | `a649b7f14345768aaf83c62e6782cdab6e56ac6cd0e094ffb6cfed77162d954e` |
| `exploration/stellarator_e2e/generated/handwritten/mfe_magnet_field/winding_pack_sizing_impl.py` | `3637b96536d48d6bd817fe69007ba61e62e742bdd213774856dffbbf4774dc5f` |
| `models/designs/stellarator_09/breeding_response.json` | `0252c650233fc2b78541c47cf5b2f73937677ba3271b50e729d74ec284441f7f` |
| `exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py` | `2ab24cf8b6a7c3c0bf929f284a880e2998401451366c6727f9d619be2a904bdc` |
