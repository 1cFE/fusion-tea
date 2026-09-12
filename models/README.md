# SysML v2 Models

This directory contains SysML v2 textual models for fusion power plant techno-economic analysis.

## Structure

- `library/` — Reusable definitions (part defs, calc defs, materials)
- `designs/` — Specific fusion concept instances

## Library Catalog

### `library/foundation/`

| File | Package | Key Elements | Purpose |
|------|---------|-------------|---------|
| `economic_parameter.sysml` | `economic_parameter` | `attribute def 'Economic Parameter'`, `enum def 'CAS Scope'` | Reusable parameter metadata type (value/min/max/sensitivity) and CAS scope classification |
| `costed_component.sysml` | `costed_component` | `abstract part def 'Costed Component'` | Standard interface for cost-bearing components (capital_cost + cas_code) |

### `library/cost_structure/`

| File | Package | Key Elements | Purpose |
|------|---------|-------------|---------|
| `cas_hierarchy.sysml` | `cas_hierarchy` | `part def 'CAS Account'`, 9 level 2 specializations (CAS20-27, CAS90) | CAS cost account hierarchy with shared/divergent classification |
| `ife_cost_parameters.sysml` | `ife_cost_parameters` | `part def 'IFE Cost Parameters'` (14 attributes) | Hawker's 14 IFE cost model parameters with Monte Carlo ranges and sensitivity rankings |
| [mfe_power_core.sysml](library/cost_structure/mfe_power_core.sysml) | `mfe_power_core` | `part def 'Magnet System'`, `'Heating and CD'`, `'Divertor'` | MFE power-core component types and their CAS specializations |

### `library/analyses/`

| File | Package | Key Elements | Purpose |
|------|---------|-------------|---------|
| `ife_lcoe.sysml` | `ife_lcoe` | `calc def 'IFE LCOE'` | Closed-form DCF LCOE calculation taking 14 parameters, producing $/MWh |
| `fusion_cycle.sysml` | `fusion_cycle` | `calc def 'Recirculating Power Fraction'`, `constraint def 'Viability Threshold'` | Fusion cycle gain analysis and eta*G viability constraint |
| `hif_economics.sysml` | `hif_economics` | `calc def 'Meier HIF Driver Cost'`, `'Meier Reactor Cost'`, `'Meier Total Capital Cost'`, `'Meier COE'` | Meier 1986 HIF engineering-economic cost formulas (driver cost, reactor cost, capital cost, COE) |

The MFE analysis files below each declare a package with the same name as the file stem. These descriptions identify the implemented calculations; their presence does not establish engineering validity across arbitrary inputs. The [current audit assessment](../work/analysis/20260912-fusion-audit-current-assessment.md) records the remaining applicability and verification limits.

| File / package | Purpose |
|---|---|
| [mfe_plasma_scaling.sysml](library/analyses/mfe_plasma_scaling.sysml) | Plasma geometry, radial build, fusion power, wall loading, beta and conductor peak-field calculations |
| [mfe_plasma_sustainment.sysml](library/analyses/mfe_plasma_sustainment.sysml) | Plasma sustainment, including the ISS04 confinement and radiation calculations |
| [mfe_heating_chain.sysml](library/analyses/mfe_heating_chain.sysml) | Heating conversion and operating demand, with heating-efficiency constraints |
| [mfe_power_balance.sysml](library/analyses/mfe_power_balance.sysml) | Reactor source heat, thermal/electric power balance and recirculating power |
| [mfe_primary_loop.sysml](library/analyses/mfe_primary_loop.sysml) | Primary coolant-loop response |
| [mfe_power_cycle.sysml](library/analyses/mfe_power_cycle.sysml) | Thermal-to-electric conversion efficiency |
| [mfe_cryo_plant.sysml](library/analyses/mfe_cryo_plant.sysml) | Cryoplant electrical demand |
| [mfe_magnet_field.sysml](library/analyses/mfe_magnet_field.sysml) | Coil field, winding-pack sizing/stress, conductor strain, winding length, cold volume and stored energy |
| [mfe_magnet_cost.sysml](library/analyses/mfe_magnet_cost.sysml) | Magnet winding, casing, structure and capital costs |
| [mfe_account_costs.sysml](library/analyses/mfe_account_costs.sysml) | Component/account costs, financial factors and annual/capital rollups |
| [mfe_lcoe_dcf.sysml](library/analyses/mfe_lcoe_dcf.sysml) | Discounted-cash-flow electricity price |
| [mfe_lifecycle.sysml](library/analyses/mfe_lifecycle.sysml) | Replacement calendar, downtime, availability and replacement costs |
| [mfe_fuel_cycle.sysml](library/analyses/mfe_fuel_cycle.sysml) | Fuel-cycle flows |
| [mfe_divertor_heat.sysml](library/analyses/mfe_divertor_heat.sysml) | Divertor heat ledger |
| [mfe_vacuum.sysml](library/analyses/mfe_vacuum.sysml) | Vacuum gas load |
| [mfe_viability.sysml](library/analyses/mfe_viability.sysml) | Power, plasma, magnet, sustainment, loop and cycle constraint definitions |

## Design Catalog

### `designs/generic_ife/`

| File | Package | Key Elements | Purpose |
|------|---------|-------------|---------|
| `ife_subsystems.sysml` | `ife_subsystems` | `abstract part def 'IFE Driver'`, `part def 'Target Factory'`, `part def 'Reaction Chamber'`, `enum def 'Wall Type'` | IFE subsystem type definitions with CAS22 sub-account mapping |
| `ife_plant.sysml` | `ife_plant` | `part def 'IFE Power Plant'` | Generic IFE plant assembly with 14-param LCOE binding, power balance, and viability constraint |

### `designs/hif_ife/`

| File | Package | Key Elements | Purpose |
|------|---------|-------------|---------|
| `hif_driver.sysml` | `hif_driver` | `part def 'HIF Driver'` | HIF induction linac driver specializing IFE Driver with Meier cost formula and Osiris baseline parameters |
| `hif_plant.sysml` | `hif_plant_pkg` | `part hif_plant` | Osiris baseline HIF plant with dual cost outputs (Hawker LCOE + Meier COE) |

### `designs/generic_mfe/`

| File | Package | Key Elements | Purpose |
|---|---|---|---|
| [mfe_subsystems.sysml](designs/generic_mfe/mfe_subsystems.sysml) | `mfe_subsystems` | `part def 'Blanket'`, `'Shield'`, `'Vacuum Vessel'`, and balance-of-plant types | MFE subsystem definitions with cost-account specializations |
| [mfe_plant.sysml](designs/generic_mfe/mfe_plant.sysml) | `mfe_plant` | `abstract part def 'MFE Power Plant'` | Plant assembly joining physics, equipment costs, lifecycle, financial outputs and constraints |

The current assembly includes an ISS04 sustainment chain and ECRH operating-heating path. The demonstrated concrete configuration is the stellarator below. General confinement and mixed-heating reuse remain open audit questions; see F10 in the [assessment](../work/analysis/20260912-fusion-audit-current-assessment.md).

### `designs/stellarator_09/`

| File | Package | Key Elements | Purpose |
|---|---|---|---|
| [stellarator_plant.sysml](designs/stellarator_09/stellarator_plant.sysml) | `stellarator_09` | `part stellaris : 'MFE Power Plant'` | Stellaris instance with direct density input, ECRH-only heating and stellarator coil geometry |

The executable MFE study package and consumers live in [exploration/stellarator_e2e](../exploration/stellarator_e2e/). Calculation definitions, plant bindings and study verdicts are distinct: use the accepted package's constraint catalog and its study record for the evaluated constraints and results.

## Archived models

Previous CATF-oriented models and test patterns are retained in [archive/models](../archive/models/) as historical material. Reuse requires checking their assumptions, interfaces and validation against the intended application.

## IFE computed operating point and Osiris reference

WI-048 uses Osiris beam 5 MJ, gain 87, efficiency 0.28, rate 4.6 Hz and thermal conversion 0.45. One derived bank energy (beam/efficiency) feeds driver power, capital and replacement costs. Hawker and Meier pricing consume the same computed thermal and net powers. With the retained 1.15 blanket multiplier, 0.90 availability and equal driver/cooling allowance, this case produces 435 MJ yield and 871.231785714 MW net. These later approximations do not reproduce the historical Osiris balance.

The thirteen `osiris_reference_*` attributes preserve the printed table, including gain 87, yield 432 MJ, thermal power 2504 MW, net power 1000 MW and 5.6 in 1992 cents/kWh. Source: `knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png`. Historical facts are not price denominators. Hawker dollars/MWh retain the existing mixed cost assumptions and DCF; Meier retains 1988 cents/kWh and its fixed-charge convention.

The executable price channels are `hawker_price__price` and `meier_price__price`, each with a Real `__generating` indicator (0 or 1). `net_positive` asserts actual net W > 0. Supported price consumers require both indicator 1 and a satisfied named net verdict. Non-generators return an invalid zero sentinel. The retained eta-times-gain assertion is an economic heuristic. Driver-only and total parasitic fractions are separately exposed; the old `recirculating_fraction` alias remains driver-only. Powers are in W, with explicit thermal/net GW outputs.
