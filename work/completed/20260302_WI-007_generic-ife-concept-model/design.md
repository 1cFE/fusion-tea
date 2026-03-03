---
Status: complete
Created: 2026-03-02
Updated: '2026-03-02'
Related Artifacts:
  Spec: ./spec.md
---

# WI-007: Generic IFE Concept Model — Design

## Overview

Design a driver-agnostic IFE power plant model in `models/designs/generic_ife/` that composes subsystems (driver, target factory, reaction chamber), binds Hawker's 14 parameters to their physical homes, and wires everything to the library's LCOE calculation. The model serves as the template for driver-specific instantiations (WI-008 HIF).

## Research Findings

### SysML Pattern Validation

All required patterns were confirmed working in syside:

| Pattern | Status | Validated By |
|---------|--------|-------------|
| `calc` usage inside `part def` | Works | Coffee maker archive, syside docs |
| `in paramName = subpart.attr` binding | Works | Coffee maker archive (dot notation) |
| `abstract part def` | Works | `Costed Component` in current library |
| `:>>` feature redefinition for specialization | Works | WI-006 library files |
| Cross-package `private import` | Works | Coffee maker archive, WI-006 |
| `assert constraint` usage | Works | SysML v2 spec Section 7.20 |

### Hawker Parameter → Subsystem Mapping

Hawker's 14 parameters map to three subsystem groups and plant-level operations. This mapping drives the assembly structure:

| Parameter | Symbol | Subsystem Owner | Rationale |
|-----------|--------|----------------|-----------|
| Driver efficiency | mu_d | Driver | Physical property of the driver |
| Driver cost constant | gamma | Driver | $/J is driver-specific |
| Driver energy | E_d | Driver | Energy per pulse from driver bank |
| Driver lifetime | N_d | Driver | Shots before replacement |
| Target cost constant | delta | Target Factory | Per-target manufacturing cost |
| Blanket energy multiple | E_b | Chamber | Nuclear energy multiplication in blanket |
| Yield cost constant | beta | Chamber | Chamber/vessel cost proportional to yield |
| Gain | G | Plant (physics) | Target-driver interaction, not owned by one subsystem |
| Availability | mu_a | Plant (operations) | Whole-plant operational parameter |
| Frequency | f | Plant (operations) | Shot repetition rate (plant-level scheduling) |
| Thermal efficiency | mu_th | Plant (operations) | Power conversion efficiency |
| Plant cost constant | alpha | Plant (financial) | BOP capital $/kWe |
| O&M cost constant | epsilon | Plant (financial) | Annual O&M $/kWe-yr |
| Discount rate | d | Plant (financial) | Financial parameter |

> Source: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`
> Ref: Table 1 (parameter definitions), Equations 2.1-2.16
> Basis: Hawker's cost decomposition maps parameters to five categories (plant, yield, driver, target, O&M)

### CAS22 Sub-Account Structure

Per ARIES Cost Account Documentation and DI-002, CAS22 level 3 sub-accounts for IFE:

| Sub-Account | Name | Scope | Physical Subsystem |
|-------------|------|-------|--------------------|
| 22.1.1 | First Wall / Blanket | shared | Reaction Chamber |
| 22.1.2 | Shield | shared | Reaction Chamber |
| 22.1.3 | Driver | ife_divergent | IFE Driver |
| 22.1.5 | Primary Structure | shared | Reaction Chamber |
| 22.1.8 | Target Factory | ife_divergent | Target Factory |

> Source: `knowledge/sources/aries_cost_account_documentation/output.md`
> Ref: CAS22 sub-account definitions
> Basis: DI-002 — CAS22 is the IFE-MFE divergence point

### Chamber Wall Types

Three fundamentally different IFE chamber approaches:

| Type | First Wall | Protection | Typical Drivers |
|------|-----------|------------|-----------------|
| Dry wall | SiC, carbon composite | None — surface ablation | Laser |
| Wetted wall | Thin liquid film on structure | Moderate — film renewal | Various |
| Liquid wall | Thick FLiBe/Li curtain | Maximum — eliminates solid FW | Heavy-ion, pulser |

> Source: `knowledge/sources/energy_from_inertial_fusion/output.md`
> Ref: Chamber concepts section
> Basis: EIF-1992 classification of IFE chamber approaches

## Design Decisions

### DD-WI007-1: Two-File Organization

**Decision**: Two SysML files in `models/designs/generic_ife/`:
1. `ife_subsystems.sysml` — Type definitions (driver, target factory, chamber, CAS22 sub-accounts, enums)
2. `ife_plant.sysml` — Plant assembly (composition, parameter binding, LCOE wiring)

**Rationale**: Separates type definitions from assembly/binding logic. Follows AD-004's separation of concerns. The subsystem types are reusable across different plant configurations; the plant assembly is the specific wiring.

### DD-WI007-2: CAS22 Sub-Accounts as Specialization Chain

**Decision**: Each CAS22 level 3 sub-account is a `part def` specializing `'CAS22 Power Core'` from the library. Physical subsystems then specialize the appropriate CAS sub-account:
```
Costed Component → CAS Account → CAS22 Power Core → CAS22.1.3 Driver → IFE Driver
```

**Rationale**: Type-safe CAS mapping. Follows AD-005's pattern of typed part def specializations. The driver IS-A CAS22.1.3 element — inheritance captures this. The alternative (composition — driver HAS-A CAS account) would break the Costed Component interface chain.

### DD-WI007-3: Abstract Driver with Four Interface Parameters

**Decision**: `abstract part def 'IFE Driver'` with four concrete `Real` attributes (efficiency, cost_per_joule, energy, lifetime_shots). WI-008 specializes with `:>> efficiency = 0.25;` etc.

**Rationale**: The four driver-specific Hawker parameters define the complete economic interface for any IFE driver. Abstract ensures it can't be instantiated without specialization. Per AD-001, all attributes are `Real` with units in doc comments.

### DD-WI007-4: Top-Down Parameter Flow (Hawker Model)

**Decision**: Parameters flow from subsystems → plant → LCOE calc. The library's `'IFE LCOE'` calc is used as a calc usage within the plant, with 14 inputs bound to subsystem attributes via dot notation. No intermediate CAS-level cost rollup.

**Rationale**: Hawker's model is parametric top-down — 14 parameters → LCOE. There's no CAS-level cost aggregation in the formula. Subsystems own their engineering parameters; the LCOE calc computes costs internally. The `capital_cost` attribute inherited via Costed Component is available for future bottom-up models but not used in the Hawker calculation.

**Alternative rejected**: Bottom-up cost rollup (each subsystem computes capital_cost, then aggregate). This would require decomposing Hawker's formula differently and duplicating computation. Better left for WI-008 or a more detailed cost model.

### DD-WI007-5: Reaction Chamber as Physical Composite

**Decision**: `'Reaction Chamber'` is a composite part def (not specializing a single CAS account) that contains CAS22 sub-account parts for blanket (22.1.1), shield (22.1.2), and primary structure (22.1.5). It owns Hawker parameters blanket_energy_multiple (E_b) and yield_cost_constant (beta).

**Rationale**: The chamber spans three CAS sub-accounts — it can't cleanly specialize one. Composition captures the physical reality: a chamber contains a blanket, shield, and support structure. The Hawker parameters (E_b, beta) are chamber-level aggregate properties.

### DD-WI007-6: Gain as Plant-Level Physics Parameter

**Decision**: Target gain (G) is defined at the plant level, not owned by any single subsystem.

**Rationale**: Gain is a property of the target-driver interaction — it depends on both the target design and the driver characteristics. No single subsystem owns it. Defining it at the plant level makes the physics explicit and allows different driver-target combinations to set it.

## Proposed Design

### Component Hierarchy

```
IFE Power Plant
├── driver : IFE Driver [abstract]          → CAS22.1.3
│   ├── efficiency : Real                   (eta / mu_d)
│   ├── cost_per_joule : Real               (gamma)
│   ├── energy : Real                       (E_d)
│   └── lifetime_shots : Real               (N_d)
├── target_factory : Target Factory          → CAS22.1.8
│   └── cost_per_target : Real              (delta)
├── chamber : Reaction Chamber
│   ├── wall_type : Wall Type               (dry/wetted/liquid)
│   ├── blanket_energy_multiple : Real      (E_b)
│   ├── yield_cost_constant : Real          (beta)
│   ├── blanket : CAS22.1.1 First Wall Blanket
│   ├── shield : CAS22.1.2 Shield
│   └── structure : CAS22.1.5 Primary Structure
├── [Plant-Level Operations]
│   ├── availability : Real                 (mu_a)
│   ├── frequency : Real                   (f)
│   ├── gain : Real                        (G)
│   └── thermal_efficiency : Real           (mu_th)
├── [Plant-Level Financial]
│   ├── discount_rate : Real                (d)
│   ├── plant_cost_constant : Real          (alpha)
│   └── om_cost_constant : Real             (epsilon)
├── lcoe_calc : IFE LCOE                   [calc usage]
│   └── 14 inputs bound to subsystem/plant attributes
├── recirc_calc : Recirculating Power Fraction [calc usage]
│   └── 4 inputs: eta, G, E_b, mu_th
└── viability : Viability Threshold          [constraint usage]
    └── 2 inputs: eta, G
```

### Element Details

#### Wall Type (enum def)

```sysml
enum def 'Wall Type' {
    doc /* Classification of IFE reaction chamber first wall approaches.
        Source: knowledge/sources/energy_from_inertial_fusion/output.md
        Ref: Chamber concepts section
        Basis: EIF-1992 three-category classification */
    dry_wall;
    wetted_wall;
    liquid_wall;
}
```

#### CAS22 Level 3 Sub-Accounts (5 part defs)

Each specializes `'CAS22 Power Core'` from the library:

```sysml
part def 'CAS22.1.1 First Wall Blanket' :> 'CAS22 Power Core' {
    doc /* CAS Account 22.1.1: First Wall and Blanket.
        Scope: shared. Energy capture and tritium breeding.
        Source: knowledge/sources/aries_cost_account_documentation/output.md
        Ref: CAS22.1.1 section */
    :>> scope = 'CAS Scope'::shared;
}
```

Similar for 22.1.2 (Shield, shared), 22.1.3 (Driver, ife_divergent), 22.1.5 (Primary Structure, shared), 22.1.8 (Target Factory, ife_divergent).

#### IFE Driver (abstract part def)

```sysml
abstract part def 'IFE Driver' :> 'CAS22.1.3 Driver' {
    doc /* Abstract IFE driver subsystem. Concrete driver types (HIF, laser,
        pulser) specialize this with specific parameter values.

        The four attributes map to Hawker's driver-specific parameters.
        Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        Ref: Table 1 (parameters mu_d, gamma, E_d, N_d)
        Basis: DI-004 — driver cost reference points span 3 orders of magnitude */

    attribute efficiency : Real;         // mu_d, wall-plug efficiency (fraction)
    attribute cost_per_joule : Real;     // gamma, driver capital cost ($/J)
    attribute energy : Real;             // E_d, driver bank energy (J)
    attribute lifetime_shots : Real;     // N_d, shots before replacement
}
```

- **Specialization**: `:> 'CAS22.1.3 Driver'` → inherits CAS Account chain → inherits capital_cost, cas_code
- **Abstract**: Cannot be instantiated; WI-008 creates `'HIF Driver' :> 'IFE Driver'` with concrete values
- **No defaults**: Parameters have no default values — they must be set by each specialization
- **MR-WI007-2**: Satisfies abstract driver with 4 required parameters (SV-009)

#### Target Factory (part def)

```sysml
part def 'Target Factory' :> 'CAS22.1.8 Target Factory' {
    doc /* IFE target manufacturing facility. Produces expendable targets
        consumed on each shot. Cost is an operating expense, not capital.

        Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        Ref: Table 1 (parameter delta)
        Basis: DI-003 — target cost is a unique IFE operating cost category */

    attribute cost_per_target : Real;    // delta, $/target
}
```

- **Not abstract**: Cost_per_target can be set directly via `:>>` without specialization
- **Operating cost**: The LCOE calc treats this as annual operating cost (delta × shots_per_year), distinct from driver capital cost
- **MR-WI007-3**: Satisfies target factory as operating cost (SV-006)

#### Reaction Chamber (part def)

```sysml
part def 'Reaction Chamber' {
    doc /* IFE reaction chamber assembly. Contains first wall/blanket,
        shield, and primary structure. Chamber parameters E_b (blanket
        energy multiple) and beta (yield cost constant) are aggregate
        properties of the chamber system.

        Source: knowledge/sources/energy_from_inertial_fusion/output.md
        Ref: Chamber concepts section
        Basis: EIF-1992 IFE chamber classification */

    attribute wall_type : 'Wall Type';
    attribute blanket_energy_multiple : Real;  // E_b, dimensionless
    attribute yield_cost_constant : Real;      // beta, $/GJ

    part blanket : 'CAS22.1.1 First Wall Blanket';
    part shield : 'CAS22.1.2 Shield';
    part structure : 'CAS22.1.5 Primary Structure';
}
```

- **Composite**: Contains three CAS22 sub-account parts (DD-WI007-5)
- **Does NOT specialize CAS Account**: Spans multiple accounts
- **MR-WI007-4**: Wall type enum + blanket energy multiple (SV-006)

#### IFE Power Plant (part def)

```sysml
part def 'IFE Power Plant' {
    doc /* Generic driver-agnostic IFE power plant.
        Composes subsystems and wires Hawker's 14 parameters to LCOE.

        Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        Ref: Equations 2.1-2.16 (complete model)
        Basis: Hawker 2020 parametric IFE LCOE model */

    // === Subsystems ===
    part driver : 'IFE Driver';
    part target_factory : 'Target Factory';
    part chamber : 'Reaction Chamber';

    // === Plant-level operations parameters ===
    attribute availability : Real;           // mu_a, fraction
    attribute frequency : Real;              // f, Hz
    attribute gain : Real;                   // G, dimensionless (DD-WI007-6)
    attribute thermal_efficiency : Real;     // mu_th, fraction

    // === Plant-level financial parameters ===
    attribute discount_rate : Real;          // d, fraction
    attribute plant_cost_constant : Real;    // alpha, $/kWe
    attribute om_cost_constant : Real;       // epsilon, $/kWe-yr

    // === LCOE Calculation ===
    calc lcoe_calc : 'IFE LCOE' {
        in availability = availability;
        in blanket_energy_multiple = chamber.blanket_energy_multiple;
        in discount_rate = discount_rate;
        in driver_cost_constant = driver.cost_per_joule;
        in driver_efficiency = driver.efficiency;
        in driver_energy = driver.energy;
        in driver_lifetime_shots = driver.lifetime_shots;
        in frequency = frequency;
        in gain = gain;
        in om_cost_constant = om_cost_constant;
        in plant_cost_constant = plant_cost_constant;
        in target_cost_constant = target_factory.cost_per_target;
        in thermal_efficiency = thermal_efficiency;
        in yield_cost_constant = chamber.yield_cost_constant;
    }

    // === Expose LCOE result ===
    attribute lcoe : Real = lcoe_calc.lcoe;

    // === Power balance ===
    calc recirc_calc : 'Recirculating Power Fraction' {
        in eta = driver.efficiency;
        in gain = gain;
        in blanket_multiplier = chamber.blanket_energy_multiple;
        in thermal_efficiency = thermal_efficiency;
    }

    attribute recirculating_fraction : Real = recirc_calc.f_recirc;

    // === Viability constraint ===
    assert constraint viability : 'Viability Threshold' {
        in eta = driver.efficiency;
        in gain = gain;
    }
}
```

### Cross-File Bindings

#### Import Map

| File | Imports From | Elements Used |
|------|-------------|--------------|
| `ife_subsystems.sysml` | `ScalarValues::*` | `Real` |
| | `costed_component::*` | (inherited via CAS chain) |
| | `cas_hierarchy::*` | `'CAS22 Power Core'`, `'CAS Account'`, `'CAS Scope'` |
| `ife_plant.sysml` | `ScalarValues::*` | `Real` |
| | `ife_subsystems::*` | `'IFE Driver'`, `'Target Factory'`, `'Reaction Chamber'` |
| | `ife_lcoe::*` | `'IFE LCOE'` calc def |
| | `fusion_cycle::*` | `'Recirculating Power Fraction'`, `'Viability Threshold'` |

#### Dataflow Diagram

```
                    ife_subsystems.sysml              ife_plant.sysml
                    ─────────────────────             ─────────────────

Library                                               IFE Power Plant
┌─────────────────┐                                   ┌───────────────────────┐
│ CAS22 Power Core│◄─── CAS22.1.x sub-accounts ───► │ driver (abstract)     │
│ CAS Account     │     ├── CAS22.1.1 FW/Blanket    │   .efficiency ─────┐  │
│ Costed Component│     ├── CAS22.1.2 Shield         │   .cost_per_joule ─┤  │
│ CAS Scope       │     ├── CAS22.1.3 Driver         │   .energy ─────────┤  │
└─────────────────┘     ├── CAS22.1.5 Structure      │   .lifetime_shots ─┤  │
                        └── CAS22.1.8 Target Fac.    │                    │  │
                                                      │ target_factory     │  │
                             IFE Driver [abstract] ──►│   .cost_per_target ┤  │
                             Target Factory ─────────►│                    │  │
                             Reaction Chamber ───────►│ chamber            │  │
                             Wall Type ──────────────►│   .blanket_E_mult ─┤  │
                                                      │   .yield_cost_c ───┤  │
┌─────────────────┐                                   │                    │  │
│ IFE LCOE        │◄─── lcoe_calc usage ─────────────│ plant attrs ───────┤  │
│   (14 in, 1 out)│                                   │   availability ────┤  │
└─────────────────┘                                   │   frequency ───────┤  │
                                                      │   gain ────────────┤  │
┌─────────────────┐                                   │   thermal_eff ─────┤  │
│ Recirc. Power   │◄─── recirc_calc usage ───────────│   discount_rate ───┤  │
│ Viability Thresh│◄─── viability constraint ────────│   plant_cost_c ────┤  │
└─────────────────┘                                   │   om_cost_c ───────┘  │
                                                      │                       │
                                                      │ lcoe : Real (result)  │
                                                      │ recirc_frac : Real    │
                                                      └───────────────────────┘
```

#### Parameter Binding Table (MR-WI007-8)

| LCOE Calc Input | Source Expression | Hawker Symbol |
|-----------------|------------------|---------------|
| `availability` | `availability` | mu_a |
| `blanket_energy_multiple` | `chamber.blanket_energy_multiple` | E_b |
| `discount_rate` | `discount_rate` | d |
| `driver_cost_constant` | `driver.cost_per_joule` | gamma |
| `driver_efficiency` | `driver.efficiency` | mu_d |
| `driver_energy` | `driver.energy` | E_d |
| `driver_lifetime_shots` | `driver.lifetime_shots` | N_d |
| `frequency` | `frequency` | f |
| `gain` | `gain` | G |
| `om_cost_constant` | `om_cost_constant` | epsilon |
| `plant_cost_constant` | `plant_cost_constant` | alpha |
| `target_cost_constant` | `target_factory.cost_per_target` | delta |
| `thermal_efficiency` | `thermal_efficiency` | mu_th |
| `yield_cost_constant` | `chamber.yield_cost_constant` | beta |

All 14 parameters bound. 4 from driver, 1 from target factory, 2 from chamber, 7 at plant level.

### Specialization Pattern (for WI-008)

The design enables clean specialization for HIF:

```sysml
// WI-008 will do this — shown here to validate the pattern
part hif_plant : 'IFE Power Plant' {
    // Specialize abstract driver to HIF
    part redefines driver : 'HIF Driver' {
        :>> efficiency = 0.25;
        :>> cost_per_joule = 5.0;
        :>> energy = 5.0e6;
        :>> lifetime_shots = 1.0e9;
    }

    // Set target factory cost
    :>> target_factory.cost_per_target = 0.19;

    // Set chamber parameters
    :>> chamber.wall_type = 'Wall Type'::liquid_wall;
    :>> chamber.blanket_energy_multiple = 1.2;
    :>> chamber.yield_cost_constant = 5.0e6;

    // Set plant-level parameters
    :>> availability = 0.70;
    :>> frequency = 5.0;
    :>> gain = 100.0;
    // ... etc.
}
```

## Validation Plan

### Parse Validation (Level 1)

```bash
uv run syside check models/designs/generic_ife/ife_subsystems.sysml \
    models/designs/generic_ife/ife_plant.sysml \
    models/library/foundation/economic_parameter.sysml \
    models/library/foundation/costed_component.sysml \
    models/library/cost_structure/cas_hierarchy.sysml \
    models/library/cost_structure/ife_cost_parameters.sysml \
    models/library/analyses/ife_lcoe.sysml \
    models/library/analyses/fusion_cycle.sysml
```

All files must pass with 0 errors (SV-010).

### Structural Verification (Level 2)

- SV-006: Plant has driver, target_factory, chamber subsystems → model inspection
- SV-007: CAS22 sub-accounts 22.1.1, 22.1.2, 22.1.3, 22.1.5, 22.1.8 exist → model inspection
- SV-009: Driver is abstract with 4 attributes → model inspection

### Reasonableness Check (Level 3)

- SV-008: LCOE with Hawker defaults within $25–120/MWh → requires evaluation (deferred to implementation — syside evaluation may not support the full calc chain, but structural correctness is verifiable)

## Validation Report

### Prototype Results

Prototype files created and validated:
- `models/designs/generic_ife/ife_subsystems.sysml` — subsystem definitions
- `models/designs/generic_ife/ife_plant.sysml` — plant assembly with LCOE binding

```
$ uv run python -m syside check models/library/**/*.sysml models/designs/generic_ife/*.sysml
Checks passed!
```

**All patterns validated**:
- `abstract part def 'IFE Driver'` with 5-level specialization chain → PASS
- `calc` usage inside `part def` with `in paramName = expr` bindings → PASS
- Dot notation for sub-part attributes (`driver.efficiency`, `chamber.blanket_energy_multiple`) → PASS
- `assert constraint` usage with bound inputs → PASS
- Cross-package imports (design → library) → PASS
- `enum def 'Wall Type'` → PASS

**Confidence**: HIGH — prototype passes Level 1 validation; all patterns confirmed working.

## Implementation Checklist

### Phase 1: Subsystem Definitions (`ife_subsystems.sysml`)
- [ ] Create `models/designs/generic_ife/` directory
- [ ] Define `'Wall Type'` enum def
- [ ] Define 5 CAS22 level 3 sub-account part defs
- [ ] Define `'IFE Driver'` abstract part def
- [ ] Define `'Target Factory'` part def
- [ ] Define `'Reaction Chamber'` part def with sub-parts
- [ ] Validate: `syside check` on subsystems + library dependencies

### Phase 2: Plant Assembly (`ife_plant.sysml`)
- [ ] Define `'IFE Power Plant'` part def with composed subsystems
- [ ] Add plant-level operations and financial parameters
- [ ] Wire LCOE calc usage with 14 input bindings
- [ ] Wire recirculating power fraction calc usage
- [ ] Wire viability threshold constraint
- [ ] Add doc comments with citations on all elements
- [ ] Validate: `syside check` on all files

### Phase 3: Verification
- [ ] Verify SV-006 through SV-010
- [ ] Verify no driver-specific values (MR-WI007-10)
- [ ] Verify all citations present (MR-WI007-9)
- [ ] Update VALIDATION_MATRIX.md statuses

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `assert constraint` usage syntax may differ from prototype | Low | Low | Validated in SysML spec; adjust syntax if needed |
| Calc usage result access (`lcoe_calc.lcoe`) may need different accessor | Low | Medium | Coffee maker uses `cost_model.total_cost` successfully |
| 5-level specialization chain may cause syside issues | Low | Medium | Test incrementally — CAS22 sub-accounts first, then driver |
| `part redefines driver : 'HIF Driver'` pattern for WI-008 may need adjustment | Medium | Low | Not needed for WI-007; validate during WI-008 design |

## Approval

**Status**: Pending user approval.

Design is ready for review. No architectural alternatives needed — the patterns are well-established from WI-006 and validated prototypes.
