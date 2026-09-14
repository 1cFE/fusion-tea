---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md, basis.md, evidence/accounting-research.md, evidence/material-research.md
---

# WI-040 design — material procurement and winding operations

## Decision and supported claim

[AGENT] Replace the live unsplit winding markup with tape procurement, explicit copper/solder/steel/helium procurement, and a separately calculated winding-operation estimate. Keep the old winding account and the older 1costingFE form as comparison channels. This is a scoped engineering estimate with declared transfer assumptions, not a reconstruction of the old multiplier or a complete factory quote. It directly addresses MR-WI040-1/2/4 and the goal's accounting question.

The source-supported additive form is PROCESS `acc2221`: superconductor/copper procurement, sheath/fixed conductor additions, winding, case and intercoil structure are distinct. The adopted winding term is conductor metres times 480 dollars/metre in 1990 dollars. Source locators and checked capture are in `evidence/accounting-research.md`. This design uses the source's winding term and material procurement; its separate steel-sheath charge would overlap our pack steel. The source's fixed cable charge has unresolved applicability to the REBCO construction and is a disclosed omission. Insulation between pancakes also lacks a quantified inventory. These limitations prevent a claim of complete manufactured-magnet cost.

## Physical ownership and dependencies

[AGENT] Preserve AD-008's existing coil, winding pack, casing and magnet-system structure. The winding pack owns composition, material density/price facts and helium state; the coil owns effective operating turn current. The magnet system owns the calculation combining coil geometry/current with pack quantities, as it already owns pack sizing and volume. No additional material part occurrences are needed to establish the four explicit inventory contributions for this bounded change.

Expose geometric winding volume separately from total cryogenic cold volume in 'Winding Pack Cold Volume'. Existing `vol_cold_total` and its arithmetic order remain unchanged; new `vol_winding_pack` excludes `vol_extra`. The material inventory reads the new output. Extra cold equipment therefore changes cryoplant loads but cannot purchase more winding material. The generic plant binds `magnet.winding_pack.T_inventory` to `cryoplant.T_cold_cryo`, so changing the existing temperature lever also changes helium density under the declared approximation. This creates no calculation cycle: cryoplant temperature is an input, while its heat load depends on magnet volume.

## Equations and interfaces

[AGENT] Add `mfe_winding_pack_cost.sysml` in the analysis library with two typed manual calculations. Their doc comments carry the normative equations and domains; manual completion is needed to refuse invalid scalar inputs deliberately. All ordinary values and both canonical/exploration trees remain source-owned; generated code implements this contract.

`'Winding Pack Material Inventory'` inputs: `volume_in`, `f_copper`, `f_solder`, `f_steel`, `f_helium`, `rho_copper`, `rho_solder`, `rho_steel`, `price_copper`, `price_solder`, `price_steel`, `price_helium`, `helium_pressure`, `temperature`, `helium_gas_constant`. Outputs in this order: `mass_copper`, `mass_solder`, `mass_steel`, `mass_helium`, `cost_copper`, `cost_solder`, `cost_steel`, `cost_helium`, `material_cost`, `helium_density`, `tape_volume`.

```text
rho_He = helium_pressure / (helium_gas_constant * temperature)
m_i = volume_in * f_i * rho_i
C_i = m_i * price_i
material_cost = C_copper + C_solder + C_steel + C_helium
tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium)
```

Volumes are m³, densities kg/m³, masses kg, pressures Pa, temperature K, gas constant J/(kg K), prices dollars/kg and costs dollars. Tape is already purchased as composite tape through the existing ampere-metre rate; its substrate and stabilizer are not charged again as external jacket/plate material. The residual tape volume is reported, not converted to a mass or re-priced. Fixed composition away from the source point is an explicit approximation; WI-038 must inspect that premise when conductor quantity changes.

`'Winding Pack Procurement Cost'` inputs: `n_coils`, `I_coil`, `f_set`, `c_coil`, `cost_per_kAm`, `turn_current`, `winding_rate_1990`, `cost_escalation`, `nonplanar_factor`, `material_cost_in`. Outputs in this order: `tape_cost`, `conductor_length`, `winding_fabrication_cost`, `cost`.

```text
K = n_coils * I_coil * f_set * c_coil / 1000  [kA m]
tape_cost = K * cost_per_kAm
conductor_length = 1000 * K / turn_current  [m of composite conductor]
winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor
cost = tape_cost + material_cost_in + winding_fabrication_cost
```

Use `magnet.material_inventory` and `magnet.winding_procurement` as calc usage names. Expose `magnet.winding_material_cost`, `magnet.winding_fabrication_cost`, `magnet.tape_procurement_cost` and `magnet.winding_cost_legacy`. Existing `magnet.winding_cost` default now points at `winding_procurement.cost`; its replacement seam remains available. Existing `winding_pack_cost` continues to compute the old comparison. `magnet.capital_cost` continues to add the selected winding cost to the separately computed casing cost. Primary structure and the cryoplant remain in their existing accounts.

## Parameter choices

All choices below are [AGENT] unless explicitly identified as source values. Fractions are Table 7 image values: copper .35, solder .12, steel .36, helium .08; their residual .09 is tape. Sources, retrieval dates and raw-HTML/PDF locators are in the two research reports.

| Attribute on winding_pack unless stated | Initial value | Basis and limit |
|---|---|---|
| f_copper/f_solder/f_steel/f_helium | .35/.12/.36/.08 | Source image; fixed-composition transfer approximation. |
| rho_copper/rho_solder/rho_steel | 8940/8390/8000 kg/m³ | Rounded supplier densities; Sn63Pb37 is a selected solder proxy, not the source's identified alloy. Cryogenic metal contraction is omitted. |
| price_copper/price_steel | 11/6 dollars/kg | Inherited 2026-era 1costingFE stock-price assumptions, not new market quotes; pack steel fabrication is represented by the separate operation estimate. |
| price_solder | 29.23 / 0.45359237 dollars/kg | Captured 2026 retail Sn63Pb37 bar quote; procurement proxy, no bulk discount assumed. |
| price_helium | (14 * 2077.2644 * 288.15 / 101325) * (334.4 / 313.7) dollars/kg | USGS 2024 Grade-A base dollars/standard m³ converted to mass at the reported standard conditions; estimated2026 CPI adjustment; surcharges/transport omitted. |
| helium_pressure | 1.5e6 Pa | Lower end of the source's15–20bar operating range. |
| T_inventory | bound to cryoplant.T_cold_cryo | Existing20K baseline; inventory responds to the same temperature. |
| helium_gas_constant | 2077.2644 J/(kg K) | Helium ideal-gas specific constant; NIST cross-check in material research. |
| coil.turn_current | 50000 A | Source maximum adopted as common effective operating current; shortest-length assumption at fixed ampere-metres, sensitivity25–50kA. |
| winding_rate_1990 | 480 dollars1990/m | PROCESS winding operations, transferred to REBCO. |
| cost_escalation | 334.4 / 130.7 | Estimated2026 CPI /1990 CPI, a general purchasing-power proxy. Completed2025 alternative321.9/130.7 retained as sensitivity. |
| nonplanar_factor | 1.9 | Inherited transfer assumption, not a independently qualified universal penalty; explore .5–2 times the chosen total winding rate. |

The new pack estimate uses estimated2026 dollars. This does not normalize the entire inherited plant account tree to a common year. No parameter is selected to reproduce the old magnet total. Exact downstream changes will be measured against `baseline-before.json`, not used as targets.

## Domains and engineering limits

[AGENT] Both manual calcs require finite inputs and finite outputs. Inventory requires volume≥0; every fraction≥0 and <1; sum of four fractions<1; all densities, pressure, temperature and gas constant>0; prices≥0. Procurement requires n_coils>0, I_coil≥0, 0<f_set≤1, c_coil>0, cost_per_kAm≥0, turn_current>0, winding_rate_1990≥0, cost_escalation>0, nonplanar_factor>0, material_cost_in≥0. Reject violations with a ValueError naming the calculation and offending quantity before arithmetic; reject non-finite output after arithmetic. Zero local volume/current remains allowed where meaningful; downstream stress retains its own stricter nonzero denominator domain.

These are arithmetic domains. Source support is narrower: default REBCO composition at20K and15–20bar. The ideal-gas approximation is within1.5% of the two NIST20K points; NIST20bar sampled15–50K points differ by less than5%, not a proven continuous error bound. At10K it is roughly12% low, so no low-temperature-conductor inventory qualification is claimed. Geometry/current-density transfer holds composition, configuration and source shape factors; it does not prove a pack fits its casing or that an arbitrary aspect ratio is buildable.

## Consumer restatement before regeneration

[AGENT] Retain every existing channel, including legacy winding cost, and change only the selected winding account feeding capital. New inventory/procurement outputs and parameter keys join the model contract. Recompute the census, snapshot, manifest and indicator fixtures through native producers. Update the independent oracle and its entry/output mappings to cover all new quantities and preserve the old comparison channel. Historical study records are immutable; current tests and runners must describe the changed cost basis explicitly. Reconcile scalar differences by actual cost ancestry; do not suppress arbitrary output checks.

## Evidence plan

Source checks establish transcription and parameter basis. Independent physical checks recover each mass/volume relation, sum procurement, and compare helium to NIST. Controlled perturbations distinguish pack volume, extra cold volume, tape price, one material price, effective turn current and winding rate. A freshly generated package must preserve typed manual completions and match the live package. Baseline/off-reference checks preserve old physics and verdicts and explain every changed cost channel. Final native audit is independent; integration and the goal study follow the audited model.
