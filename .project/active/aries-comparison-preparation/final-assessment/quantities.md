# Geometry and equipment quantities

The 35 calculated quantity rows unaffected by the field finding have been reviewed. None establishes an independent ARIES prediction under the original factor-of-three criterion. Two pack dimensions can be shown as a descriptive comparison of the selected designs. Their source definition is clearer now, but their calculation from supplied pack geometry does not predict which pack ARIES needs.

## The winding packs have different shapes

| Quantity | Selected model | ARIES Table IV | Model/reference | Meaning |
|---|---:|---:|---:|---|
| First pack dimension | 0.360 m | 0.194 m | 1.856 | Descriptive only |
| Second pack dimension | 0.369 m | 0.743 m | 0.497 | Descriptive only |
| Product of dimensions | 0.13284 m² | 0.144142 m² | 0.922 | Supplementary arithmetic, not an added rubric row |
| Second/first dimension | 1.025 | 3.830 | — | Near-square model pack versus elongated reference pack |

Both individual nominal dimension ratios fall inside [1/3,3]. That does not demonstrate pack adequacy or field accuracy. The model pack still fails its own casing-fit check by 0.120 m in the radial direction. Similar cross-sectional area can coexist with a very different shape and an inadequate selected cavity.

Lyon p696 defines winding-pack cross-sectional area and toroidal width/radial depth. Table IV on p708 gives “coil dimensions” 0.194 × 0.743 m. This supports interpreting the values as winding-pack dimensions, rather than a complete coil casing. The internal-sheet and insulation inclusion boundary is still unresolved. The model explicitly includes selected internal fractions in pack_x/pack_y and adds external insulation/clearance separately. Do not replace its cavity dimensions with the source dimensions.

Model source: [fit definitions](../../../../models/library/analyses/mfe_winding_pack_fit.sysml), [bindings](../../../../models/library/cost_structure/mfe_power_core.sysml). Six inspected model files match the frozen archive byte-for-byte; [replay and identity evidence](evidence/quantity-rows.json).

## Other quantities and why they do not yet provide numerical validation

| Group | Rows | Assessment |
|---|---:|---|
| Cumulative outer radii | 11 | Consequences of the held uniform layer stack. ARIES full/tapered sectors do not define a unique matching radius. |
| Wall area, shell volumes and coil radii | 7 | Source plasma area is not first-wall area; source mass is not volume. The model coil radius is not the reference minimum plasma-to-coil distance. |
| Copper, solder, steel and helium masses | 4 | Inventory of the selected REBCO winding, whereas Table V reports total Nb3Sn winding-pack mass. Individual matching inventories are not established. |
| Winding-pack and total cold volume | 2 | Table V's 627.2 tonnes is a mass; conversion to volume would require unestablished material fractions/densities. |
| Pack/casing dimensions and allowances | 8 | Includes the two descriptive dimensions above. Remaining quantities are distinct cavity, exterior or clearance definitions without matched reference values. |
| Installed heating capacities | 2 | Computed from selected hardware and efficiencies. These are not operating heating-power predictions. |
| Refrigeration electricity | 1 | The model reports 2.189 MW. Lyon p708 combines plant and cryogenic power in 55 MW, so that number cannot serve as a cryogenic-only denominator. |

The source checks cover the retained system-study tables and definitions, not a claim that no matching data exist anywhere. [All 35 row dispositions](evidence/quantity-rows.json) retain their values and exact producers. [Source inspection receipt](evidence/quantity-source-receipt.json) records checked images and hashes.

## Reproduction

Run `.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/quantity-review.py` from the repository root. It reads the retained diagnostic report and frozen archive, verifies inspected model files, and rebuilds the row dispositions and supplementary arithmetic. It does not evaluate a plant or modify prior evidence.
