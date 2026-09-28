# Proposed WI-069 executable interface

[AGENT] Proposed for coordinator/reviewer release; no scientific implementation has started. One library `calc def 'Fuel Inventory'` in `mfe_fuel_cycle.sysml`; active usage `fuel_cycle.inventory`; generated module `mfe_fuel_cycle.fuel_inventory`. Scalar outputs use the generated schema's ordered field list for the manual tuple ABI. Public channel prefix is `stellarator_09__stellaris__fuel_cycle__inventory__`.

## Input formals

| Formal | Unit / meaning |
|---|---|
| enabled_in | Boolean; generic false, stellarator true |
| held_inventory_in | atoms; generic legacy held stock, dormant branch only |
| p_fus_in | MW |
| q_eff_in | MeV/reaction |
| mev_to_joules_in | J/MeV |
| burn_fraction_in | dimensionless, (0,1] |
| t_recycle_in | dimensionless, [0,1] |
| tbr_available_in | gross T atoms/reaction |
| breeding_defined_in | exact 0/1 applicability flag |
| eta_extract_in | dimensionless, (0,1] |
| lambda_T_in | 1/s |
| G_stock_in | atoms/s; active mode requires zero |
| m_T_kg_in | kg/T atom |
| m_D_kg_in | kg/D atom |
| plasma_volume_in | m³ |
| n_T0_in | T atoms/m³ |
| alpha_n_in | dimensionless profile exponent, greater than −1 |
| tau_feed_in | s |
| tau_process_in | s |
| tau_blanket_in | s |
| tau_extract_in | s |
| tau_buffer_in | s |
| reserve_fraction_in | dimensionless q, [0,1] |
| tau_reserve_in | s |
| startup_extension_in | s |
| shutdown_duration_in | s |
| availability_in | calendar productive fraction, [0,1] |
| s_per_year_in | s/year; existing 31,536,000-second year |

[AGENT] Owning Fuel Cycle scenario attributes use the same names without `_in`, except existing `fuel_q_eff`, `mev_to_joules`, `m_T_kg`, `lambda_T`, `G_stock`, `availability`, `p_fus`, `tbr`, `burn_fraction`, and `t_recycle` retain their existing names. New activation attribute is `inventory_enabled`; generic held inventory is `held_inventory`. Plasma density/profile/volume and breeding validity bind owning producer EXPOSEs. Existing `I_total` becomes EXPOSE of `inventory.total_atoms`.

## Exact proposed outputs

All amount names ending `_atoms` are T atoms; all `_kg` are tritium kg except explicitly `dt_`-prefixed quantities. Source stock children read these EXPOSEs rather than recomputing physics.

- Stock pairs: `feed_atoms`, `feed_kg`; `plasma_atoms`, `plasma_kg`; `processor_atoms`, `processor_kg`; `blanket_atoms`, `blanket_kg`; `extraction_atoms`, `extraction_kg`; `buffer_atoms`, `buffer_kg`; `reserve_atoms`, `reserve_kg`; `working_atoms`, `working_kg`; `total_atoms`, `total_kg`.
- Startup pairs: `prefill_atoms`, `prefill_kg` (feed+plasma+buffer, reserve reported separately); `startup_deficit_atoms`, `startup_deficit_kg`; `startup_minimum_atoms`, `startup_minimum_kg`; `startup_decay_allowance_atoms`, `startup_decay_allowance_kg`; `startup_conservative_atoms`, `startup_conservative_kg`.
- Timing/scale: `recycle_delay_s`, `breeding_delay_s`, `startup_horizon_s`, `max_decay_residence` (dimensionless maximum λτ across modeled residence times).
- Full-power tritium rates, each with `_kg_s` and `_kg_day`: `burn`, `injection`, `exhaust`, `recycle`, `production`, `extracted`, `recycle_loss`, `extraction_loss`. For example `burn_kg_s`, `burn_kg_day`.
- Hydrogen isotope capacity: `dt_injection_kg_s`, `dt_injection_kg_day`, `dt_processor_kg_s`, `dt_processor_kg_day` (equal D/T atom flows with distinct atomic masses).
- Operating stock decay and supply: `decay_kg_s`, `makeup_signed_kg_s`, `external_shortfall_kg_s`.
- Calendar totals: `annual_burn_kg`, `annual_injection_kg`, `annual_exhaust_kg`, `annual_recycle_kg`, `annual_production_kg`, `annual_extracted_kg`, `annual_recycle_loss_kg`, `annual_extraction_loss_kg`, `annual_decay_kg`, `annual_makeup_signed_kg`, `annual_external_shortfall_kg`; `calendar_processor_kg_s` is annual tritium exhaust divided by seconds/year.
- Shutdown: `shutdown_remaining_kg`, `shutdown_decay_loss_kg`.
- Interpretation: `defined_flag` (exact 0/1). Its inactive and undefined-breeding semantics require reviewed disposition before implementation. Invalid active physical inputs should raise ValueError; undefined transport is an inherited diagnostic state and must preserve the existing cost-diagnostic route.

## Physical occurrences

[AGENT] Add reusable non-cost-bearing `Fuel Stock` with `atoms` and `mass_kg` interfaces, and occurrences `feed_equipment`, `plasma_inventory`, `exhaust_processor`, `breeder_zone`, `extraction_equipment`, `working_storage`, `reserve_storage` under Fuel Cycle. Each occurrence documents function, incoming stream and residence or policy basis; their amount attributes bind matching inventory outputs. No new fuel-processing costs.
