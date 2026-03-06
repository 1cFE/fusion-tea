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

### `library/analyses/`

| File | Package | Key Elements | Purpose |
|------|---------|-------------|---------|
| `ife_lcoe.sysml` | `ife_lcoe` | `calc def 'IFE LCOE'` | Closed-form DCF LCOE calculation taking 14 parameters, producing $/MWh |
| `fusion_cycle.sysml` | `fusion_cycle` | `calc def 'Recirculating Power Fraction'`, `constraint def 'Viability Threshold'` | Fusion cycle gain analysis and eta*G viability constraint |
| `hif_economics.sysml` | `hif_economics` | `calc def 'Meier HIF Driver Cost'`, `'Meier Reactor Cost'`, `'Meier Total Capital Cost'`, `'Meier COE'` | Meier 1986 HIF engineering-economic cost formulas (driver cost, reactor cost, capital cost, COE) |

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

## Note

Previous CATF-oriented models (foundation package, power balance, test patterns) have been archived to `archive/models/`. They can be revived when tokamak modeling begins under the new investigation-driven workflow.
