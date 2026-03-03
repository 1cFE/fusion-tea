---
Status: complete
Created: 2026-03-02
Updated: '2026-03-03'
Related Artifacts:
  Spec: ./spec.md
---

# WI-008: HIF Concept Instantiation — Design

## Overview

Design the first concrete concept model: an HIF power plant that specializes the generic IFE model (WI-007) with Heavy Ion Fusion parameters. Three new files — Meier's cost formulas in library, an HIF Driver type definition, and an HIF plant instantiation with dual cost outputs (Hawker LCOE + Meier COE).

## Research Findings

### Parameter Definition Resolution (Spec Risk A2)

**Critical finding**: "Driver energy" (E_d) has different definitions across sources.

| Source | E_d Means | Evidence |
|--------|-----------|----------|
| Hawker 2020 / SysML library | Bank (stored) energy | `energy_on_target = driver_efficiency * driver_energy` in ife_lcoe.sysml:53 |
| EIF-1992 (Osiris) | Beam energy on target | Yield/E_d = 412/5 ≈ 82 ≈ G (matches table). If E_d were bank: G would need to be yield/(eta*E_d) = 412/1.75 = 235 ≠ 80 |
| Meier 1986 | Beam energy on target | Driver efficiency formula eta(E_d) at E_d=5 MJ gives 0.242 (Q=1) → 0.375 (Q=3) ≈ Osiris 0.35 |

**Conversion**: `E_d_bank = E_d_beam / eta`. For Osiris: 5.0/0.35 = 14.286 MJ = 14.286e6 J.

**Gain convention**: Same across all sources — G = yield / beam_energy. Our SysML's `fusion_energy_per_shot = gain * energy_on_target` is consistent because `energy_on_target = eta * E_d_bank = beam_energy`.

**Power balance note**: Hawker's simplified formula `P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)` gives ~525 MW for Osiris params, not 1000 MW. The "2x driver power" approximation is rough. This is expected — Hawker's model is parametric, not engineering-grade. The dual validation approach handles this: Meier's COE uses Osiris's actual thermal power.

> Source: Cross-analysis of ife_lcoe.sysml, EIF-1992 Osiris table, Meier 1986 Eqs. 5-8

### SysML Pattern Validation

All required patterns confirmed working via SysML v2 spec and prototype:

| Pattern | Status | Validated By |
|---------|--------|-------------|
| `part def 'HIF Driver' :> 'IFE Driver'` (concrete specialization) | Works | SysML Part 1 §7.6.2; prototype passes syside |
| `:>> efficiency = 0.35` (attribute redefinition with value) | Works | §7.6.5, §7.13.4; prototype |
| `part :>> driver : 'HIF Driver'` (type narrowing in instance) | Works | §7.6.1; prototype |
| `:>> cost_per_joule = meier_cost.gamma` (EXPOSE from internal calc) | Works | MODELING_GUIDE EXPOSE pattern; prototype |
| Adding HIF-specific attributes to specializing def | Works | §7.6.1 ("can add other features"); prototype |
| Adding calc usages to plant instance | Works | §7.6.3 ("usage can add own features"); prototype |
| `:>> availability = 0.90 { doc /* ... */ }` (redefinition with doc) | Works | Prototype passes syside |

### ADR-002 Calc Placement Resolution

Meier's HIF-specific formulas are `calc def` declarations → ADR-002 says all calc defs go in `library/`. This follows existing precedent: `ife_lcoe.sysml` is IFE-specific but lives in `library/analyses/`.

The calc defs are *definitions* (reusable types). Their concept-specificity is in the regression coefficients, not in the modeling element type. Design files contain *usages* (instances with bound values) per MR-3.

> Note: MR-WI008-10 ("no library modification") refers to existing files. Adding `hif_economics.sysml` is new file creation, not modification. See DD-WI008-1.

### HIF Parameter Values (Osiris Baseline)

Computed parameter values for the HIF plant model:

**Driver parameters**:

| Hawker Parameter | Symbol | HIF Value | Unit | Source |
|-----------------|--------|-----------|------|--------|
| efficiency | mu_d | 0.35 | fraction | EIF-1992 Osiris |
| energy (bank) | E_d | 14.286e6 | J | Derived: 5.0 MJ beam / 0.35 eta |
| cost_per_joule | gamma | ~68 | $/J | Derived: Meier formula at Osiris point |
| lifetime_shots | N_d | 6.0e9 | shots | Bangerter 2013 (40yr × 90% × 5Hz) |

> gamma computation: C_dd = (0.32+0.088×5)×(1.25+0.05×1)×(1+0.0088×(3.5−5)) = 0.76×1.30×0.987 = $0.975B. gamma = 0.975e9/14.286e6 = $68.25/J

**Plant-level parameters**:

| Hawker Parameter | Symbol | HIF Value | Unit | Source | Notes |
|-----------------|--------|-----------|------|--------|-------|
| availability | mu_a | 0.90 | fraction | Bangerter 2013 | 90% reliability target |
| frequency | f | 3.5 | Hz | EIF-1992 Osiris | |
| gain | G | 80 | — | EIF-1992 Osiris | yield/beam convention |
| thermal_efficiency | mu_th | 0.43 | fraction | EIF-1992 Osiris | |
| discount_rate | d | 0.08 | fraction | Hawker default | financial, not concept-specific |
| plant_cost_constant | alpha | 2000 | $/kWe | [ESTIMATED] from Meier C_rd | see DD-WI008-5 |
| om_cost_constant | epsilon | 65 | $/kWe-yr | [ESTIMATED] from Meier 3% | see DD-WI008-5 |
| target_cost_constant | delta | 10 | $/target | Hawker default | HIF-specific data sparse |
| blanket_energy_multiple | E_b | 1.15 | — | Bangerter M=1.1-1.3 | midpoint |
| yield_cost_constant | beta | 5.0e6 | $/GJ | Hawker default | |

**Estimated LCOE**: ~66 $/MWh at these parameters (within Hawker's $25-120 range).

**Meier COE check**: C_T ≈ $3.3B at Osiris point → COE ≈ 4.7 cents/kWh (reasonably close to Meier's 5.0 reference and Osiris's 3.6).

## Design Decisions

### DD-WI008-1: Meier Calc Defs in Library

**Decision**: Place four Meier calc defs in `models/library/analyses/hif_economics.sysml` per ADR-002.

**Rationale**: ADR-002 requires all `calc def` declarations in library. This follows the precedent set by `ife_lcoe.sysml` (IFE-specific but in library). Calc defs are *definitions* — concept-specificity is in the coefficients, not the modeling element type. Design files contain *usages*.

**MR-WI008-10 compliance**: Adding a new library file is not modification of existing files.

### DD-WI008-2: Meier Driver Cost Returns Gamma

**Decision**: The `'Meier HIF Driver Cost'` calc def takes beam energy (MJ), driver efficiency, num chambers, and rep rate. It returns gamma ($/J of bank energy) as the primary output, with cost_billions accessible as an intermediate attribute.

**Rationale**: Bridges Meier's engineering model to Hawker's parametric model in a single calc def. The HIF Driver sets `cost_per_joule = meier_cost.gamma` via the EXPOSE pattern, which flows into the inherited Hawker LCOE calc automatically.

**Alternative rejected**: Returning cost_billions as primary and computing gamma in the design file — would violate ADR-002 (derived expression in design).

### DD-WI008-3: HIF Driver Owns Meier Cost Computation

**Decision**: `'HIF Driver'` part def contains the Meier driver cost calc as an internal calc usage. It also exposes `driver_cost_billions` for the Meier COE chain.

**Rationale**: The driver cost computation semantically belongs to the driver subsystem. The calc usage binds to driver-local attributes (beam_energy_mj, efficiency, num_chambers, pulse_rate_ref), keeping all driver economics encapsulated.

### DD-WI008-4: Bank Energy Convention for IFE Driver Interface

**Decision**: The inherited `energy` attribute (from IFE Driver) uses bank/stored energy in Joules, per Hawker/SysML convention. A new `beam_energy_mj` attribute on HIF Driver stores beam energy in MJ (Meier/EIF convention). The fixed relationship: `energy = beam_energy_mj * 1e6 / efficiency`.

**Rationale**: Preserves backward compatibility with the generic IFE model (which uses bank energy in the LCOE calc). The beam energy attribute is needed for the Meier formula, which uses beam energy. The `energy` value (14.286e6 J) is pre-computed and set as a literal to avoid a derived expression.

**Trade-off**: Setting `energy` as a literal (14.286e6) rather than computing it from beam_energy_mj/efficiency means changing beam_energy_mj alone won't automatically update energy. This is acceptable because the Osiris operating point is fixed — parametric exploration requires changing multiple parameters consistently.

### DD-WI008-5: Aggregate Parameters Estimated with Explicit Basis

**Decision**: plant_cost_constant (alpha = $2000/kWe) and om_cost_constant (epsilon = $65/kWe-yr) are set as estimates with explicit `[ESTIMATED]` citation basis, since Meier's cost decomposition doesn't map cleanly to Hawker's aggregate parameters.

**Rationale**: Hawker's alpha covers all non-driver/non-chamber capital, while Meier disaggregates into reactor cost + indirect multiplier. Exact mapping would require decomposing Meier's formula differently. Since the Meier COE chain provides the engineering-validated cost output, approximate Hawker parameters are acceptable for the cross-concept comparable LCOE.

### DD-WI008-6: Dual Cost Outputs via Inheritance + Extension

**Decision**: The HIF plant inherits Hawker LCOE from `IFE Power Plant` and adds a Meier COE calc chain as new features. Both are exposed as top-level attributes: `lcoe` (inherited) and `meier_coe` (added).

**Rationale**: SysML v2 allows usages to add features beyond their type's definition (spec §7.6.3). This enables the HIF plant to carry two independent cost models without modifying the generic IFE plant definition.

### DD-WI008-7: Three-File Organization

**Decision**: Three files:
1. `models/library/analyses/hif_economics.sysml` — Meier calc defs (4 calc defs)
2. `models/designs/hif_ife/hif_driver.sysml` — HIF Driver part def (type + Meier cost wiring)
3. `models/designs/hif_ife/hif_plant.sysml` — HIF plant instance (params + Meier COE chain)

**Rationale**: Follows AD-004 (library subdirectory organization) and WI-007's precedent (subsystem types separate from plant assembly). The library file contains definitions; the design files contain specializations and instances.

## Proposed Design

### Component Hierarchy

```
HIF Power Plant (hif_plant : 'IFE Power Plant')
├── [inherited] lcoe_calc : 'IFE LCOE'        → attribute lcoe : Real
├── [inherited] recirc_calc                     → attribute recirculating_fraction : Real
├── [inherited] viability constraint
│
├── driver : 'HIF Driver' :> 'IFE Driver'      → CAS22.1.3
│   ├── [inherited] efficiency = 0.35
│   ├── [inherited] cost_per_joule = meier_cost.gamma  (~$68/J)
│   ├── [inherited] energy = 14.286e6                  (bank energy, J)
│   ├── [inherited] lifetime_shots = 6.0e9
│   ├── [added] beam_energy_mj = 5.0                  (Meier convention)
│   ├── [added] num_chambers = 1.0
│   ├── [added] pulse_rate_ref = 3.5
│   ├── [added] meier_cost : 'Meier HIF Driver Cost'
│   └── [added] driver_cost_billions : Real            (exposed for COE chain)
│
├── target_factory : 'Target Factory'           → CAS22.1.8
│   └── cost_per_target = 10.0
│
├── chamber : 'Reaction Chamber'
│   ├── wall_type = liquid_wall
│   ├── blanket_energy_multiple = 1.15
│   ├── yield_cost_constant = 5.0e6
│   ├── blanket : CAS22.1.1
│   ├── shield : CAS22.1.2
│   └── structure : CAS22.1.5
│
├── [inherited] Plant-level operations: availability=0.90, frequency=3.5, gain=80, thermal_eff=0.43
├── [inherited] Plant-level financial: discount_rate=0.08, alpha=2000, epsilon=65
│
├── [added] thermal_power_gw = 2.054                   (Osiris, for Meier COE)
├── [added] net_electric_power_gw = 1.0
├── [added] meier_reactor_cost_calc : 'Meier Reactor Cost'
├── [added] meier_capital_calc : 'Meier Total Capital Cost'
├── [added] meier_coe_calc : 'Meier COE'
└── [added] meier_coe : Real                           (exposed COE output)
```

### Element Details

#### Meier HIF Driver Cost (calc def, library)

```sysml
calc def 'Meier HIF Driver Cost' {
    in attribute beam_energy_mj : Real;      // E_d, beam energy [MJ]
    in attribute driver_efficiency : Real;    // eta_d
    in attribute num_chambers : Real;         // N_c
    in attribute rep_rate : Real;             // v [Hz]

    // Meier Eq. 5: C_dd [$B, 1988$]
    attribute cost_billions : Real =
        (0.32 + 0.088 * beam_energy_mj)
        * (1.25 + 0.05 * num_chambers)
        * (1.0 + 0.0088 * (rep_rate - 5.0));

    // Bridge: gamma = C_dd / E_d_bank
    attribute bank_energy_joules : Real =
        beam_energy_mj * 1.0e6 / driver_efficiency;

    return gamma : Real = cost_billions * 1.0e9 / bank_energy_joules;
}
```

Verification: At E_d=5 MJ, eta=0.35, N_c=1, v=3.5 Hz → C_dd=$0.975B, gamma=$68.25/J

> Source: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
> Ref: Eq. 5 (lines 173-192)

#### Meier Reactor Cost, Total Capital, COE (calc defs, library)

Three chained calc defs implementing Meier's full engineering-economic model:

- **Reactor cost**: `C_rd = 0.66 * (P_t/1.67)^0.49 * (0.72*N_u + 0.28)` [$B]
- **Total capital**: `C_T = 1.83 * (C_rd + C_dd + C_tfd)` [$B]
- **COE**: `(0.113 * C_T) / (0.0876 * a * P_n)` [cents/kWh]

Verification: At P_t=2.054 GWt, C_dd=$0.975B, C_tfd=$0.1B, a=0.90, P_n=1.0 GWe:
C_rd=$0.732B, C_T=$3.31B, COE=4.74 cents/kWh

> Source: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
> Ref: Eqs. 1-4

#### HIF Driver (part def, designs)

```sysml
part def 'HIF Driver' :> 'IFE Driver' {
    // HIF-specific attributes
    attribute beam_energy_mj : Real;
    attribute num_chambers : Real;
    attribute pulse_rate_ref : Real;

    // Meier driver cost (internal calc usage)
    calc meier_cost : 'Meier HIF Driver Cost' { ... }

    // Set inherited interface parameters
    :>> efficiency = 0.35;
    :>> cost_per_joule = meier_cost.gamma;
    :>> energy = 14.286e6;
    :>> lifetime_shots = 6.0e9;

    // Expose for Meier COE chain
    attribute driver_cost_billions : Real = meier_cost.cost_billions;
}
```

Specialization chain: `Costed Component → CAS Account → CAS22 Power Core → CAS22.1.3 Driver → IFE Driver → HIF Driver`

#### HIF Power Plant (part usage, designs)

```sysml
part hif_plant : 'IFE Power Plant' {
    // Type-narrow driver to HIF
    part :>> driver : 'HIF Driver' {
        :>> beam_energy_mj = 5.0;
        :>> num_chambers = 1.0;
        :>> pulse_rate_ref = 3.5;
    }

    // Set remaining plant parameters
    :>> availability = 0.90;
    :>> frequency = 3.5;
    :>> gain = 80.0;
    // ... (all 14 Hawker params bound)

    // Meier COE chain (added features)
    calc meier_reactor_cost_calc : 'Meier Reactor Cost' { ... }
    calc meier_capital_calc : 'Meier Total Capital Cost' { ... }
    calc meier_coe_calc : 'Meier COE' { ... }
    attribute meier_coe : Real = meier_coe_calc.coe_cents_kwh;
}
```

### Cross-File Bindings

#### Import Map

| File | Imports From | Elements Used |
|------|-------------|--------------|
| `hif_economics.sysml` | `ScalarValues::*` | `Real` |
| `hif_driver.sysml` | `ScalarValues::*` | `Real` |
| | `ife_subsystems::*` | `'IFE Driver'` (specialization target) |
| | `hif_economics::*` | `'Meier HIF Driver Cost'` |
| `hif_plant.sysml` | `ScalarValues::*` | `Real` |
| | `ife_plant::*` | `'IFE Power Plant'` (instantiation target) |
| | `ife_subsystems::*` | `'Wall Type'` (enum) |
| | `hif_driver::*` | `'HIF Driver'` |
| | `hif_economics::*` | `'Meier Reactor Cost'`, `'Meier Total Capital Cost'`, `'Meier COE'` |

#### Dataflow Diagram

```
Library (calc defs)                    HIF Design (usages + values)
═══════════════════                    ════════════════════════════

hif_economics.sysml                    hif_driver.sysml
┌─────────────────────────┐            ┌──────────────────────────────┐
│ 'Meier HIF Driver Cost' │◄───usage───│ 'HIF Driver' :> 'IFE Driver' │
│   in: beam_E, eta, Nc, v│            │   beam_energy_mj = 5.0       │
│   out: gamma, cost_$B   │            │   num_chambers = 1.0          │
├─────────────────────────┤            │   pulse_rate_ref = 3.5        │
│ 'Meier Reactor Cost'    │◄──┐        │   efficiency = 0.35           │
│   in: P_t, N_u          │   │        │   cost_per_joule ← gamma     │
│   out: C_rd $B           │   │        │   energy = 14.286e6           │
├─────────────────────────┤   │        │   lifetime_shots = 6e9        │
│ 'Meier Total Capital'   │◄──┤        │   driver_cost_billions ← C_dd │
│   in: C_rd, C_dd, C_tfd │   │        └──────────────┬───────────────┘
│   out: C_T $B            │   │                       │
├─────────────────────────┤   │        hif_plant.sysml │
│ 'Meier COE'             │◄──┤        ┌───────────────▼───────────────┐
│   in: C_T, a, P_n       │   │        │ hif_plant : 'IFE Power Plant' │
│   out: COE cents/kWh    │   │        │                               │
└─────────────────────────┘   │        │  driver : 'HIF Driver'        │
                              │        │    └── gamma, C_dd flow up    │
ife_lcoe.sysml                │        │                               │
┌─────────────────────────┐   │        │  Meier COE chain:             │
│ 'IFE LCOE' (inherited)  │   ├usage──│    reactor_cost_calc           │
│   14 Hawker params       │   │        │    capital_calc               │
│   out: LCOE $/MWh       │   │        │    coe_calc                   │
└─────────────────────────┘   │        │                               │
                              │        │  Outputs:                     │
fusion_cycle.sysml            │        │    lcoe (inherited)           │
┌─────────────────────────┐   │        │    meier_coe (added)          │
│ Recirc Power, Viability  │   │        │    recirculating_fraction     │
│ (inherited)              │   │        └───────────────────────────────┘
└─────────────────────────┘   │
                              │
ife_subsystems.sysml          │
┌─────────────────────────┐   │
│ 'IFE Driver' (abstract)  │   │
│ 'Target Factory'         │   │
│ 'Reaction Chamber'       │   │
│ 'Wall Type' enum         │───┘
└─────────────────────────┘

ife_plant.sysml
┌─────────────────────────┐
│ 'IFE Power Plant'        │
│   (instantiation target) │
└─────────────────────────┘
```

#### Parameter Binding Table (Hawker LCOE → HIF values)

| LCOE Calc Input | Bound To | HIF Value | Source |
|-----------------|----------|-----------|--------|
| `availability` | `hif_plant.availability` | 0.90 | Bangerter 2013 |
| `blanket_energy_multiple` | `hif_plant.chamber.blanket_energy_multiple` | 1.15 | Bangerter 2013 |
| `discount_rate` | `hif_plant.discount_rate` | 0.08 | Hawker default |
| `driver_cost_constant` | `hif_plant.driver.cost_per_joule` | ~68 (from Meier) | Meier 1986 Eq. 5 |
| `driver_efficiency` | `hif_plant.driver.efficiency` | 0.35 | EIF-1992 Osiris |
| `driver_energy` | `hif_plant.driver.energy` | 14.286e6 | Derived: 5.0 MJ / 0.35 |
| `driver_lifetime_shots` | `hif_plant.driver.lifetime_shots` | 6.0e9 | Bangerter 2013 |
| `frequency` | `hif_plant.frequency` | 3.5 | EIF-1992 Osiris |
| `gain` | `hif_plant.gain` | 80 | EIF-1992 Osiris |
| `om_cost_constant` | `hif_plant.om_cost_constant` | 65 | [ESTIMATED] |
| `plant_cost_constant` | `hif_plant.plant_cost_constant` | 2000 | [ESTIMATED] |
| `target_cost_constant` | `hif_plant.target_factory.cost_per_target` | 10 | Hawker default |
| `thermal_efficiency` | `hif_plant.thermal_efficiency` | 0.43 | EIF-1992 Osiris |
| `yield_cost_constant` | `hif_plant.chamber.yield_cost_constant` | 5.0e6 | Hawker default |

All 14 parameters bound. 4 from driver (including gamma from Meier), 1 from target factory, 2 from chamber, 7 at plant level.

## Validation Plan

### Parse Validation (Level 1)

```bash
uv run python -m syside check -Werror \
    models/library/foundation/economic_parameter.sysml \
    models/library/foundation/costed_component.sysml \
    models/library/cost_structure/cas_hierarchy.sysml \
    models/library/cost_structure/ife_cost_parameters.sysml \
    models/library/analyses/ife_lcoe.sysml \
    models/library/analyses/fusion_cycle.sysml \
    models/library/analyses/hif_economics.sysml \
    models/designs/generic_ife/ife_subsystems.sysml \
    models/designs/generic_ife/ife_plant.sysml \
    models/designs/hif_ife/hif_driver.sysml \
    models/designs/hif_ife/hif_plant.sysml
```

All files must pass with 0 errors, 0 warnings (SV-015).

### Structural Verification (Level 2)

- SV-011: HIF Driver specializes IFE Driver, has 4 interface params set
- SV-012: Meier driver cost calc produces ~$0.975B at Osiris point
- SV-009 (existing): IFE Driver still abstract with 4 params

### Reasonableness Checks (Level 3)

- SV-013: Hawker LCOE with HIF params produces ~66 $/MWh (positive, within $25-120)
- SV-014: Meier COE at reference case produces ~4.7-5.0 cents/kWh (±15%)
- Viability constraint: eta*G = 0.35*80 = 28 >> 10 ✓

## Validation Report

### Prototype Results

Three prototype files created and validated:

| File | Location | Status |
|------|----------|--------|
| `hif_economics.sysml` | `models/library/analyses/` | Level 1 PASS |
| `hif_driver.sysml` | `models/designs/hif_ife/` | Level 1 PASS |
| `hif_plant.sysml` | `models/designs/hif_ife/` | Level 1 PASS |

```
$ uv run python -m syside check -Werror [all 11 files]
Checks passed!
```

**All patterns validated**:
- `part def 'HIF Driver' :> 'IFE Driver'` with concrete param values → PASS
- `part :>> driver : 'HIF Driver'` type narrowing → PASS
- `:>> cost_per_joule = meier_cost.gamma` EXPOSE from internal calc → PASS
- Meier calc chain (4 calc usages) in plant instance → PASS
- `:>> parameter = value { doc /* ... */ }` redefinition with doc comments → PASS
- Cross-package imports (HIF → generic IFE → library) → PASS
- No warnings with -Werror → PASS

**Confidence**: HIGH — prototype passes Level 1 with all patterns confirmed.

## Implementation Checklist

### Phase 1: Library Calc Defs (`hif_economics.sysml`)

- [ ] Review and refine all 4 calc def doc comments (Source/Ref/Basis complete)
- [ ] Verify formula constants against source document
- [ ] Validate: `syside check` on library files

### Phase 2: HIF Driver (`hif_driver.sysml`)

- [ ] Review doc comments on all HIF-specific attributes
- [ ] Verify meier_cost calc binding
- [ ] Verify EXPOSE pattern for cost_per_joule and driver_cost_billions
- [ ] Verify inherited params (efficiency, energy, lifetime_shots) have correct values
- [ ] Validate: `syside check` on driver + dependencies

### Phase 3: HIF Plant (`hif_plant.sysml`)

- [ ] Review all 14 parameter values and their citations
- [ ] Review doc comments on all `[ESTIMATED]` parameters
- [ ] Verify Meier COE chain bindings
- [ ] Verify both outputs (lcoe, meier_coe) are exposed
- [ ] Validate: `syside check` on all files

### Phase 4: Verification & Close

- [ ] Run full Level 1 check (all 11 files, -Werror)
- [ ] Verify SV-011 through SV-015
- [ ] Write Python verification script for LCOE/COE reasonableness (SV-013, SV-014)
- [ ] Update VALIDATION_MATRIX.md statuses
- [ ] Update models/README.md with HIF catalog entries
- [ ] Confirm no generic_ife or library files modified (git diff)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hawker LCOE and Meier COE diverge significantly | High | Low | Expected — different models with different structures. Document both; each validated against own reference |
| `energy = 14.286e6` literal becomes stale if beam_energy_mj changes | Low | Low | Osiris operating point is fixed; parametric exploration out of scope for WI-008 |
| `[ESTIMATED]` parameters (alpha, epsilon) produce unreasonable LCOE | Medium | Medium | Pre-computed LCOE ≈ $66/MWh is within range; Python verification script validates |
| Meier COE at Osiris point (4.7¢) doesn't match published Osiris COE (3.6¢) | High | Low | Meier formula was fit to Cascade, not Osiris specifically. 32% deviation documented as known limitation |

## Approval

**Status**: Pending user approval.

The design is complete with a validated prototype passing Level 1 (0 errors, 0 warnings). All SysML patterns are confirmed working. The dual cost output approach (inherited Hawker LCOE + added Meier COE) provides two independent validation paths.
