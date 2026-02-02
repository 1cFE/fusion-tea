# SysML v2 Models

This directory contains SysML v2 textual models for fusion power plant techno-economic analysis.

## Structure

- `library/` - Reusable definitions
  - `foundation/` - Base types, units, materials
    - `types.sysml` - Enums (FuelType, ReactorType, EnergyConversion, etc.)
    - `units.sysml` - Custom unit types (Percent, Ratio, etc.)
    - `materials.sysml` - Material part definitions
  - `calculations/` - Calculation definitions (physics equations, formulas)
    - `power_balance/` - Power balance calculations
      - `power_balance.sysml` - Generic power balance
      - `mfe_power_balance.sysml` - MFE-specific power flow

- `designs/` - Specific fusion concept designs
  - CATF (Compact Advanced Tokamak Fusion) - planned
  - Future: Stellarator, mirror machines, novel concepts

## Available Calc Definitions

### Power Balance (`library/calculations/power_balance/`)

**Generic Calculations** (`power_balance.sysml`):
- `'Alpha Power Calc'` - Compute charged particle power by fuel type (DT, DD, DHE3, PB11)
- `'Power Balance Calc'` - Generic power balance (p_alpha, p_neutron, q_sci)

**MFE-Specific** (`mfe_power_balance.sysml`):
- `'MFE Power Balance Calc'` - Full MFE power flow (16 inputs, 15 outputs)
  - Thermal power, thermal electric, recirculating power
  - Engineering Q, recirculating fraction, net electric power

**Import Patterns for Design Files:**
```sysml
// Import generic calc
private import PowerBalanceLibrary::'Power Balance Calc';

// Import MFE-specific calc
private import MFEPowerBalanceLibrary::'MFE Power Balance Calc';

// Import alpha calc (also available)
private import PowerBalanceLibrary::'Alpha Power Calc';
```

## Getting Started

Use `/design-model {feature}` to start creating models.

## Validation

Models are validated against PyFECONS calculations. Use `/audit-models` to check alignment.
