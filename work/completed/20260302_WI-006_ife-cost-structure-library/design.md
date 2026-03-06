---
Status: complete
Created: 2026-03-02
Updated: '2026-03-02'
Related Artifacts:
  Spec: ./spec.md
---

# WI-006: IFE Cost Structure Library — Design

## Overview

This design defines the SysML v2 library architecture for IFE economic modeling. The library provides 6 files across 3 subdirectories, delivering: a parameter metadata pattern, a costed component interface, a CAS account hierarchy, the 14 Hawker parameters, an LCOE calculation, and a fusion cycle gain constraint.

All files have been prototyped and validated with syside. The design is ready for refinement to production quality.

## Research Findings

### PyFECONS Architecture (Reference Implementation)

- **No common base class** for cost accounts — the interface is informal (all dataclasses with a `C{NNNNNN}` field of type `M_USD`)
- **CAS hierarchy is implicit** — the tree structure exists only in rollup arithmetic within `CostingData` methods (`costing_data.py:141-202`)
- **Three Union types** for MFE/IFE divergence: `CAS220103` (Coils|Lasers), `CAS220104` (SupplementaryHeating|IgnitionLasers), `CAS220108` (Divertor|TargetFactory)
- **LCOE formula** (`lcoe.py:11-27`): uses CRF × total capital + inflated O&M/fuel, divided by annual energy — simpler than Hawker's full DCF
- **Implication**: Our SysML model improves on PyFECONS by making the costed component interface explicit and the CAS hierarchy structural

### Hawker LCOE Formula (Exact Extraction)

The paper defines LCOE as a year-by-year DCF sum (Eq. 2.1), not a closed-form annuity:
```
LCOE = Σ(C_i / (1+d)^i) / Σ(E_i / (1+d)^i),  i = 1..N
```

Construction years 1..Yc (default 5): capital costs only, no energy.
Operation years Yc+1..N (default N=45): operating costs + energy.

**Closed-form equivalence** (our implementation): Since annual costs and energy are constant within each phase, the DCF sums reduce to geometric series with present value factors:
- `PVF_con = (1 - (1+d)^(-Yc)) / d` — construction phase
- `PVF_op = (1+d)^(-Yc) * (1 - (1+d)^(-N_op)) / d` — operation phase
- `LCOE = (C_cap * PVF_con + C_op * PVF_op) / (E * PVF_op)`

**Net electric power** (Eqs. 2.12-2.16 combined):
```
P_e = E_d × f × (μ_th × E_b × G × μ_d − 2)
```
The factor of 2 is Hawker's explicit approximation: recirculating power ≈ 2× driver power (driver + cooling).

**Driver lifetime** (Eqs. 2.8-2.9): expressed in shots, converted to years via `L_d = N_d / (31557600 × f × μ_a)`.

### SysML v2 Capabilities (Verified)

- **`attribute def` with bundled metadata**: Works. Supports `:>>` feature redefinition for setting values per instance.
- **`enum def`**: Works. Simple syntax with named members.
- **`calc def` with intermediates**: Works. Intermediate `attribute` declarations with `=` bindings. `return` keyword for result.
- **`**` exponentiation**: Works in syside. Used for `(1+d)^n` in present value factors.
- **`constraint def` with `in` parameters**: Works. Boolean result expression.
- **`abstract part def`**: Works for costed component interface.
- **Cross-file imports**: Work with `private import package_name::*` or specific member imports.

### Standard Library Gaps

- **No monetary units** in ISQ/SI (no $, $/MWh, $/kWe, $/J)
- **No MW/GW** in SI (only W, kW)
- Custom units would require `DimensionOneUnit` definitions with `ConversionByConvention`

## Design Decisions

### DD-1: Plain `Real` for all values (not ISQ typed quantities)

**Decision**: Use `Real` for all numeric values. Document units in doc comments.

**Rationale**: Custom monetary unit definitions (for $, $/MWh, $/J) are complex and untested with syside's quantity arithmetic. For this first pass (pattern-defining work), getting the structure right matters more than compile-time unit checking. Units are documented in doc comments per MR-4's citation format.

**Trade-off**: No compile-time dimensional analysis. Mitigated by doc comment conventions.

**Upgrade path**: When MFE modeling begins and the library is shared more broadly, typed quantities can be added as an enhancement.

### DD-2: `attribute def 'Economic Parameter'` for parameter metadata

**Decision**: Bundle value/min/max/sensitivity into a reusable `attribute def`. Each of the 14 Hawker parameters is an attribute of this type with `:>>` feature redefinition.

**Rationale**: Machine-readable metadata (not just doc comments). Supports future programmatic access to ranges and sensitivities for Monte Carlo or sensitivity analysis via codegen.

**Alternative rejected**: Simple `Real` attributes with ranges only in doc comments — not machine-readable, can't be validated or iterated programmatically.

### DD-3: Closed-form DCF for LCOE (not year-by-year iteration)

**Decision**: Express Hawker's DCF as a closed-form ratio using present value factors, implemented in a single `calc def`.

**Rationale**: SysML v2 calc defs do not support iteration/looping. The closed-form is mathematically equivalent to the year-by-year sum (geometric series) for constant annual cost/energy streams, which is exactly Hawker's model structure.

**Verified**: `(1+d)**n` parses correctly in syside.

### DD-4: Library subdirectory organization per MODELING_GUIDE convention

**Decision**: Three subdirectories: `foundation/`, `cost_structure/`, `analyses/`.

**Rationale**: Follows MODELING_GUIDE.md package structure. Separates concerns: base types → domain structure → calculations. Scales to future additions (MFE parameters, additional analyses).

### DD-5: CAS hierarchy as part def specializations of 'Costed Component'

**Decision**: Each CAS level 2 account is a `part def` specializing `'CAS Account'` which specializes `'Costed Component'`. Scope classification via `'CAS Scope'` enum attribute.

**Rationale**: Type-safe — downstream users instantiate `'CAS22 Power Core'`, not a generic account with a string code. The specialization hierarchy mirrors the CAS tree. Scope classification as enum (not doc comment) is queryable.

**Alternative rejected**: Single generic `'CAS Account'` with string code — no type safety.

### DD-6: Separate parameter definitions from LCOE calculation

**Decision**: `ife_cost_parameters.sysml` defines the 14 parameters with metadata. `ife_lcoe.sysml` defines the calculation. They are independent packages — the calc def takes 14 `Real` inputs, not an `'IFE Cost Parameters'` part.

**Rationale**: The calc def is pure math — it doesn't need to know about the parameter metadata (ranges, sensitivities). This separation means the calc can be reused with any parameter source (including WI-008's HIF-specific values that may override defaults). WI-007 wires them together.

## Proposed Design

### File Structure

```
models/library/
├── foundation/
│   ├── economic_parameter.sysml    # attribute def + enum def
│   └── costed_component.sysml     # abstract part def
├── cost_structure/
│   ├── cas_hierarchy.sysml         # CAS account part defs
│   └── ife_cost_parameters.sysml   # 14 Hawker parameters
└── analyses/
    ├── ife_lcoe.sysml              # calc def
    └── fusion_cycle.sysml          # calc def + constraint def
```

### Element Catalog

| Element | Type | Package | File | MR Served |
|---------|------|---------|------|-----------|
| `'Economic Parameter'` | attribute def | `economic_parameter` | `foundation/economic_parameter.sysml` | MR-WI006-1 |
| `'CAS Scope'` | enum def | `economic_parameter` | `foundation/economic_parameter.sysml` | MR-WI006-2 |
| `'Costed Component'` | abstract part def | `costed_component` | `foundation/costed_component.sysml` | MR-WI006-5 |
| `'CAS Account'` | part def :> 'Costed Component' | `cas_hierarchy` | `cost_structure/cas_hierarchy.sysml` | MR-WI006-2 |
| `'CAS20 Land'` .. `'CAS90 Indirect Costs'` | part defs :> 'CAS Account' | `cas_hierarchy` | `cost_structure/cas_hierarchy.sysml` | MR-WI006-2 |
| `'IFE Cost Parameters'` | part def | `ife_cost_parameters` | `cost_structure/ife_cost_parameters.sysml` | MR-WI006-1 |
| `'IFE LCOE'` | calc def | `ife_lcoe` | `analyses/ife_lcoe.sysml` | MR-WI006-3 |
| `'Recirculating Power Fraction'` | calc def | `fusion_cycle` | `analyses/fusion_cycle.sysml` | MR-WI006-4 |
| `'Viability Threshold'` | constraint def | `fusion_cycle` | `analyses/fusion_cycle.sysml` | MR-WI006-4 |

### Per-Element Design

#### `attribute def 'Economic Parameter'`

A bundled metadata type for cost model parameters. Four `Real` fields: `value`, `min_value`, `max_value`, `sensitivity`.

```sysml
attribute def 'Economic Parameter' {
    attribute value : Real;
    attribute min_value : Real;
    attribute max_value : Real;
    attribute sensitivity : Real;
}
```

No constraints on the attribute def itself (range validation deferred — adding constraints here would require every usage to satisfy them, which is restrictive for parameter exploration).

#### `enum def 'CAS Scope'`

Simple two-member enum: `shared`, `ife_divergent`. Defined in the same package as `'Economic Parameter'` since both are foundation-level types.

Why only two members (not `shared`, `ife_specific`, `ife_divergent`): At CAS level 2, no account is purely IFE-specific — all accounts exist for both MFE and IFE, they just have different internal structure at CAS22. The `ife_divergent` classification captures this. Fully IFE-specific accounts (like target factory) are CAS level 3 sub-accounts, deferred to WI-007.

#### `abstract part def 'Costed Component'`

Minimal interface: `capital_cost : Real` and `cas_code : String`. Deliberately minimal — MR-2 says "at minimum `capital_cost`". Additional cost attributes (annual_om_cost, replacement_cost) can be added when needed without breaking existing specializations.

#### `'CAS Account'` and Level 2 Specializations

`'CAS Account' :> 'Costed Component'` adds `account_name : String` and `scope : 'CAS Scope'`. Nine specializations cover CAS20-27 and CAS90 (indirect costs grouped), each with doc comments citing ARIES Cost Account Documentation.

Scope assignments:
- `shared`: CAS20, 21, 23, 24, 25, 26, 27, 90
- `ife_divergent`: CAS22

#### `part def 'IFE Cost Parameters'`

Bundles all 14 Hawker parameters as attributes of type `'Economic Parameter'`. Each uses `:>>` redefinition to set value, min_value, max_value, and sensitivity. Doc comments on each attribute document units and cite Hawker Table 1.

Units by parameter:
- Dimensionless fractions: availability, blanket_energy_multiple, discount_rate, driver_efficiency, gain, thermal_efficiency
- $/J: driver_cost_constant
- J: driver_energy (range 0.5-50 MJ, stored as J)
- shots: driver_lifetime
- Hz: frequency
- $/kWe-yr: om_cost_constant
- $/kWe: plant_cost_constant
- $/target: target_cost_constant
- $/GJ: yield_cost_constant

#### `calc def 'IFE LCOE'`

Takes 14 `Real` inputs (the Hawker parameters) plus 2 optional constants (construction_years, operational_years). Computes LCOE in $/MWh through the following chain:

```
Physics:
  energy_on_target = driver_efficiency × driver_energy
  fusion_energy_per_shot = gain × energy_on_target
  net_electric_power = driver_energy × frequency × (μ_th × E_b × G × μ_d − 2)
  net_electric_kw = net_electric_power / 1000

Shot economics:
  shots_per_year = 31557600 × frequency × availability
  driver_lifetime_years = driver_lifetime_shots / shots_per_year

Annual costs:
  annual_capital_cost = (α×P_e + β×E_f/1e9 + γ×E_d) / Yc
  annual_operating_cost = δ×N_y + ε×P_e + γ×E_d/L_d
  annual_energy = 8760 × P_e × μ_a / 1000

Present value factors:
  pvf_construction = (1 − (1+d)^(−Yc)) / d
  pvf_operation = (1+d)^(−Yc) × (1 − (1+d)^(−N_op)) / d

Result:
  LCOE = (C_cap × PVF_con + C_op × PVF_op) / (E × PVF_op)
```

13 intermediate attributes, 1 return value. All intermediate values are exposed as named attributes for traceability and debugging.

#### `calc def 'Recirculating Power Fraction'`

Computes `f_recirc = 1 / (eta × G × M × epsilon)`. Exposes `fusion_cycle_gain` as an intermediate.

#### `constraint def 'Viability Threshold'`

`eta × gain >= threshold` where threshold defaults to 10.0. Three `in` parameters allow binding at usage sites.

### Cross-File Bindings

| Consumer File | Import | Source Package | Elements Used |
|--------------|--------|---------------|---------------|
| `cas_hierarchy.sysml` | `private import costed_component::*` | `costed_component` | `'Costed Component'` |
| `cas_hierarchy.sysml` | `private import economic_parameter::'CAS Scope'` | `economic_parameter` | `'CAS Scope'` |
| `ife_cost_parameters.sysml` | `private import economic_parameter::'Economic Parameter'` | `economic_parameter` | `'Economic Parameter'` |

The `ife_lcoe.sysml` and `fusion_cycle.sysml` are self-contained (use only `ScalarValues::Real`).

**Dataflow** (unidirectional, no circular imports):
```
foundation/economic_parameter.sysml ←── cost_structure/ife_cost_parameters.sysml
foundation/costed_component.sysml  ←── cost_structure/cas_hierarchy.sysml
foundation/economic_parameter.sysml ←── cost_structure/cas_hierarchy.sysml

analyses/ife_lcoe.sysml           (standalone)
analyses/fusion_cycle.sysml       (standalone)
```

WI-007 will wire parameters → LCOE calc and parameters → viability constraint.

### Downstream Usage Pattern (WI-007 Preview)

This library is designed so WI-007 can create a generic IFE plant like:

```sysml
package generic_ife {
    private import ife_cost_parameters::*;
    private import ife_lcoe::*;
    private import fusion_cycle::*;
    private import cas_hierarchy::*;

    part ife_plant {
        // Instantiate parameters with defaults
        part params : 'IFE Cost Parameters';

        // CAS structure
        part cas22 : 'CAS22 Power Core';
        part cas23 : 'CAS23 Turbine Plant';
        // ...

        // Wire parameters to LCOE calculation
        calc lcoe_calc : 'IFE LCOE' {
            in availability = params.availability.value;
            in gain = params.gain.value;
            // ...
        }

        // Assert viability
        assert constraint viability : 'Viability Threshold' {
            in eta = params.driver_efficiency.value;
            in gain = params.gain.value;
        }

        // EXPOSE
        attribute lcoe : Real = lcoe_calc.lcoe;
    }
}
```

## Validation Plan

### Level 1: Parse Validation
All files must parse with `uv run python -m syside check` — zero errors.

### Level 2: Structural Verification
- 14 parameters in `'IFE Cost Parameters'` with correct metadata
- 9 CAS account part defs covering CAS20-27 and CAS90
- LCOE calc def has 14+2 inputs, 13 intermediates, 1 return
- Viability constraint has 3 inputs and Boolean result

### Level 3: Integration
- Cross-file imports resolve between all 6 files
- No circular dependencies
- Package names are unique

### Numerical Validation (deferred to WI-007)
With Hawker defaults, expected net electric power:
```
P_e = 10e6 × 0.2 × (0.40 × 1.2 × 500 × 0.10 − 2) = 2e6 × (24 − 2) = 44 MW
```
This is a small plant (Hawker's defaults are conservative center of Monte Carlo space). LCOE validation against Hawker's range ($25-120/MWh) requires instantiation in WI-007.

## Validation Report

### Prototype Status: PASS

**Files created**: 6
**Total lines**: 583
**Parse validation**: All 6 files pass individually and together
**Cross-file imports**: All resolve correctly
**Circular dependencies**: None

```
$ uv run python -m syside check models/library/**/*.sysml
Checks passed!
```

### Validation Details

| Check | Result |
|-------|--------|
| `economic_parameter.sysml` — parse | PASS |
| `costed_component.sysml` — parse | PASS |
| `cas_hierarchy.sysml` — parse + cross-file imports | PASS |
| `ife_cost_parameters.sysml` — parse + attribute def usage | PASS |
| `ife_lcoe.sysml` — parse + `**` exponentiation + intermediates | PASS |
| `fusion_cycle.sysml` — parse + constraint def | PASS |
| All 6 files together — integration | PASS |

### Findings During Prototyping

1. **`import` requires explicit visibility** — syside enforces `private import` or `public import`, unlike spec examples that show bare `import`. All imports use `private import`.
2. **`**` exponentiation works** — `(1.0 + discount_rate) ** construction_years` parses correctly.
3. **`calc def` intermediates work** — attributes with `=` bindings inside calc defs parse correctly, including chained dependencies (intermediate using another intermediate).
4. **`return` keyword works** — `return lcoe : Real = ...` parses as the calc def result.
5. **`constraint def` trailing expression works** — `eta * gain >= threshold` without semicolon parses as the Boolean result.
6. **`:>>` feature redefinition works** — setting `Economic Parameter` fields within `IFE Cost Parameters` usages.

### Issues Found: None

## Implementation Checklist

### Phase 1: Foundation (complete — prototype validated)
- [x] `foundation/economic_parameter.sysml` — `'Economic Parameter'` attribute def, `'CAS Scope'` enum
- [x] `foundation/costed_component.sysml` — `'Costed Component'` abstract part def
- [x] Parse validation

### Phase 2: Cost Structure (complete — prototype validated)
- [x] `cost_structure/cas_hierarchy.sysml` — `'CAS Account'` base + 9 level 2 specializations
- [x] `cost_structure/ife_cost_parameters.sysml` — 14 Hawker parameters
- [x] Cross-file import validation

### Phase 3: Analyses (complete — prototype validated)
- [x] `analyses/ife_lcoe.sysml` — LCOE calc def with DCF
- [x] `analyses/fusion_cycle.sysml` — recirculating power calc + viability constraint
- [x] Parse validation

### Phase 4: Refinement (for `/plan-model`)
- [ ] Verify all doc comments have complete Source/Ref/Basis citations
- [ ] Review naming consistency across all elements
- [ ] Update `models/README.md` with library catalog
- [ ] Register architectural decisions in `ARCHITECTURE.md`
- [ ] Final integration validation with all files

## Risks

| Risk | Likelihood | Impact | Status |
|------|------------|--------|--------|
| `**` not supported in syside | Eliminated | — | **Resolved** — works in prototype |
| `attribute def` metadata pattern too rigid | Low | Low | Mitigated — `:>>` allows override |
| LCOE closed-form diverges from Hawker's year-by-year DCF | Very Low | Medium | Mathematically equivalent for constant annual streams — validated by derivation |
| Plain `Real` causes unit confusion downstream | Medium | Low | Mitigated by doc comments with explicit unit documentation; upgrade path to typed quantities exists |

---

**Next**: `/plan-model` for refinement of validated prototype to production quality
