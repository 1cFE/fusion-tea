# WI-070 proposed ABI

[AGENT] This is the intended interface before generation, not a claim that these keys already exist. Prefix `P=stellarator_09__stellaris__`; scalar monetary outputs are USD 2025 CPI purchasing power. Existing output names remain except the selected `fuel_handling_cost` alias changes producer as documented. Any emitted discrepancy must be reviewed against this contract rather than silently widening oracle coverage.

## Public configuration

Each new input below is `P + fuel_cycle__ + name`. Library formals use the same semantic name with `_in`, avoiding self-binding. Source rows are configured on the stellarator instance; generic processing defaults disabled.

| Name | Active default | Meaning/domain |
|---|---:|---|
| `processing_enabled` |true|Select the new cost method; false preserves the old account |
| `processing_source_conditions` |true|Explicit invocation of conditional source/feed scenario, not measured purity |
| `processing_capacity_margin` |1|Capacity/operating isotope flow, finite≥1; no spare train |
| `processing_price_multiplier` |1|Dimensionless source-price sensitivity, finite>0 |
| `processing_reference_flow` |2.08e-5|kg D+T/s reference per module, finite>0 |
| `processing_exponent` |0.3|Published ORNL component exponent, finite>0; changing it is a new source premise |
| `processing_target_cpi` |321.9|2025 annual CPI, finite>0 |
| `processing_transfer_cpi` |60.6|1977 CPI, finite>0 |
| `processing_cleanup_cpi` |82.4|1980 CPI, finite>0 |
| `processing_distiller_cpi` |65.2|1978 CPI, finite>0 |
| `processing_containment_cpi` |82.4|Central 1980; explicit study endpoints 65.2 (1978), 96.5 (1982), finite>0 |
| `processing_transfer_capital` / `processing_transfer_installation` |111000 /112000|Raw USD 1977, nonnegative |
| `processing_cleanup_capital` / `processing_cleanup_installation` |1000000 /70000|Raw USD 1980, nonnegative |
| `processing_distiller_capital` / `processing_distiller_installation` |1237000 /63000|Raw USD 1978, nonnegative |
| `processing_containment_capital` / `processing_containment_installation` |182000 /30000|Raw mixed 1978–1982 expenditure, nonnegative |

Do not create duplicate public inputs for operating flow, availability or breeding applicability. Bind `flow_in` from the new pure EXPOSE `fuel_cycle.dt_processing_flow = inventory.dt_processor_kg_s`; bind `inventory_enabled_in` from existing activation, `n_mod_in` from existing module owner and `legacy_cost_in` from the existing sibling `fuel_handling.cost`. The active flow producer remains 956444b5 arithmetic, not a recast cost equation.

## New calculation outputs

All 27 named outputs below belong to `P + fuel_cycle__processing_cost__ + name`:

- `flow_kg_s`: per-module actual operating inlet; `capacity_kg_s`: margin times that flow; `plant_capacity_kg_s`: n times per-module capacity; `flow_ratio`: per-module capacity/reference; `scaling_factor`: ratio to the source exponent.
- For each row name `transfer`, `cleanup`, `distiller`, `containment`: `{row}_reference_capital`, `{row}_reference_installation`, `{row}_capital`, `{row}_installation`. The reference pair is raw dollars converted to target CPI at source flow, one module and price multiplier 1. The actual pair is plant-total cost with margin, price and modules applied. Sixteen outputs total.
- `equipment_total`: sum of four actual capital rows; `installation_total`: sum of four actual installation rows; `module_total`: price-scaled subtotal for one module; `new_total`: n times that subtotal; `cost`: new_total when active, exact legacy otherwise; `defined_flag`: 1 only for active inventory and declared source-conditioned active processing, else 0.

In disabled mode the 26 new-method outputs other than selected `cost` are zero, including reference rows. In active zero-flow mode reference rows remain meaningful converted anchors while actual monetary sums are zero. Active processing with disabled inventory raises a ValueError before returning costs. Breeding-defined zero does not invalidate non-breeding exhaust pricing.

## Producer EXPOSEs and costed occurrence

- New `fuel_cycle.dt_processing_flow` exposes the unchanged upstream flow.
- Existing `fuel_cycle.fuel_handling_cost` now exposes `processing_cost.cost`, so generic CAS22 consumes the selected account once.
- New `fuel_cycle.fuel_processing_installation` exposes `processing_cost.installation_total` for shipping; it is zero in legacy mode.
- New `fuel_cycle.fuel_processing_defined` exposes the conditional flag. It is a reporting condition, not an additional plant qualification predicate.
- Existing `fuel_cycle.exhaust_processor` keeps atoms/mass bindings and acquires the standard CAS220500 capital interface plus equipment/direct-installation breakdown. Its per-module stock is unchanged; its plant-total capital_cost binds processing_cost.cost including legacy mode, and its breakdowns bind the same sibling producer; they are not added a second time to CAS22.
- Existing `fuel_cycle__fuel_handling__cost` remains the legacy power-proxy calculation. Rename its oracle semantic label to `fuel_handling_legacy` and map selected `fuel_handling` to `fuel_cycle__processing_cost__cost`. Preserve legacy output comparison explicitly; do not let the old map silently label the legacy number as active capital.

## Financial ABI changes

`Facility Shipping Scope` gains default-zero `fuel_installation_in` and `contingency_in` inputs. Generic plant binds actual processing installation and CAS29 rate. New `P + shipping_scope__fuel_installation_exclusion` equals installation*(1+contingency). Existing `remaining_shipping_base` subtracts this third exclusion. Existing cooling/facility exclusions retain exact identity and values.

`Supplementary Cost` gains default-zero `fuel_installation_exclusion_in`, bound to that output. Only its shipping term changes. All prior entry defaults and legacy routes remain valid; bound formals precede skipped default parameters under the retained generator convention.

The actual generated inventory, schemas and aliases must be reconciled after release. Add explicit expected new parameter/channel sets to the current MFE regression helper; all 27 calculation outputs and the new shipping output get independent oracle comparisons. Generated aliases may add captures but cannot replace raw row evidence.
