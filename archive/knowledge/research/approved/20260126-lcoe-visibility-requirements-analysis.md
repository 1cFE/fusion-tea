---
date: 2026-01-26T10:30:00-08:00
researcher: Claude
topic: "LCOE Visibility and Requirements Gap Analysis"
tags: [research, lcoe, cost-visibility, requirements, strategy-review]
status: complete
last_updated: 2026-01-26
---

# Research: LCOE Visibility and Requirements Gap Analysis

**Date**: 2026-01-26 10:30 PST
**Researcher**: Claude
**Research Type**: Strategy Review / Gap Analysis

## Research Question

1. Will the current PyFECONS library mapping strategy result in a clear LCOE calculation output?
2. How well have we specified maintenance/replacement cost models?
3. What visibility will we have into contributing factors (CapEx, OpEx, energy production)?
4. How well were the starting requirements and goals defined?

## Summary

- **LCOE calculation path is defined but incomplete** - The strategy shows LCOE as the "final output" but doesn't specify the intermediate calculations (CAS70, CAS80, CAS90) needed to get there
- **Maintenance/replacement modeling is minimal** - PyFECONS uses a simple 10% replacement factor (CAS220119) and $60/kW-year O&M; no component-specific lifetime modeling
- **CapEx visibility is strong** - The `'Costed Component'` pattern with CAS categories provides good traceability down to component level
- **OpEx and energy visibility have GAPS** - No SysML structures specified for annualized costs (CAS70-90) or power table integration
- **Requirements were loosely defined** - Original goals were "replicate PyFECONS" without specifying acceptance criteria for validation

---

## Detailed Findings

### 1. LCOE Calculation Structure in PyFECONS

#### 1.1 The LCOE Formula

**Source**: `/home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py`

```python
LCOE (C1000000) =
    (C900000 + (C700000 + C800000) * (1 + yearly_inflation)^plant_lifetime)
    / (8760 * p_net * n_mod * plant_availability)
```

**Components**:
| Component | Code | Description | Current SysML Status |
|-----------|------|-------------|---------------------|
| Annualized Financial | C900000 | CRF × Total Capital | NOT PLANNED |
| Annualized O&M | C700000 | 60 $/kW-year × P_net | NOT PLANNED |
| Annualized Fuel | C800000 | Tritium/target costs | NOT PLANNED |
| Net Power | p_net | PowerTable output | COMPLETE (MFE Power Balance) |
| Plant Lifetime | plant_lifetime | Years of operation | NOT PLANNED |
| Availability | plant_availability | Capacity factor | NOT PLANNED |
| Inflation | yearly_inflation | Annual escalation | NOT PLANNED |

**GAP IDENTIFIED**: The strategy (Section 10 roadmap) lists "LCOE calculation" as Phase 4 (P2), but doesn't specify what calc defs or structures are needed for CAS70-90.

#### 1.2 Total Capital Cost Rollup

**Source**: `/home/reid/PyFECONS/pyfecons/data.py`

```
C990000 = C100000 + C200000 + C300000 + C400000 + C500000 + C600000
        = Pre-construction + Direct + Indirect + Owner + Supplementary + Financial
```

**Current Strategy Coverage**:
- C200000 (Direct Costs): Partially covered - CAS20-29 in enum, but no aggregation calc def specified
- C100000, C300000-C600000: Listed in enum but no part defs or calc defs planned

#### 1.3 LCOE Breakdown Visibility (PyFECONS Provides)

PyFECONS can decompose LCOE into three parts:
```
LCOE_capital = C900000 / annual_energy
LCOE_om = (C700000 × inflation_factor) / annual_energy
LCOE_fuel = (C800000 × inflation_factor) / annual_energy
```

**GAP**: Our strategy doesn't specify outputting these intermediate values for cost driver analysis.

---

### 2. Maintenance and Replacement Cost Modeling

#### 2.1 Current PyFECONS Approach

**Scheduled Replacement (CAS220119)**:
- **Source**: `/home/reid/PyFECONS/pyfecons/costing/calculations/cas22/cas220119_replacement.py`
- **Formula**: `C220119 = replacement_factor × C220100` (typically 10%)
- **Treatment**: One-time capital cost at project start
- **Limitation**: No component-specific replacement schedules

**Annual O&M (CAS70)**:
- **Source**: `/home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py`
- **Formula**: `C700000 = 60 × P_net × 1000` (M_USD)
- **Treatment**: Simple $/kW-year scaling
- **Note**: TODO in code mentions `C750000 = 0.1 × C220000` for spare parts (not implemented)

**Availability Factor**:
- **Source**: `/home/reid/PyFECONS/pyfecons/inputs/basic.py`
- **Parameter**: `plant_availability` (typically 0.85)
- **Treatment**: Multiplies energy output in LCOE denominator

#### 2.2 Current Strategy Coverage

| Item | PyFECONS Location | Strategy Coverage |
|------|-------------------|-------------------|
| Scheduled Replacement | CAS220119 | CAS enum value exists, no calc def planned |
| O&M Costs | CAS70 | CAS enum value exists, no calc def planned |
| Fuel Costs | CAS80 | CAS enum value exists, no calc def planned |
| Plant Lifetime | Basic.plant_lifetime | No attribute planned |
| Availability | Basic.plant_availability | No attribute planned |
| Component Lifetimes | Not modeled | Not planned |

**GAP IDENTIFIED**: The strategy mentions CAS70-90 in the enum but doesn't specify:
- Calc defs for computing annualized costs
- Where plant operating parameters (lifetime, availability) are stored
- How replacement costs flow into LCOE

#### 2.3 Component Lifetime Modeling (Not in PyFECONS)

PyFECONS does NOT model:
- Individual component lifetimes (e.g., first wall: 5 years, magnets: 30 years)
- Replacement scheduling during plant operation
- Downtime costs during replacement
- Learning curves on replacement components

**OPPORTUNITY**: SysML could enhance PyFECONS by adding component-specific lifetime attributes, but this would be a scope expansion beyond "replicate PyFECONS."

---

### 3. Cost Visibility Analysis

#### 3.1 CapEx Visibility (STRONG in Current Strategy)

The `'Costed Component'` pattern provides excellent CapEx traceability:

```
Plant Total (C990000)
├── Reactor Plant Equipment (C220000)
│   ├── Magnet System (CAS220103) ← 'Magnet System'.capital_cost
│   │   ├── TF Coils [12] ← sum(tf_coils.capital_cost)
│   │   ├── PF Coils [6] ← sum(pf_coils.capital_cost)
│   │   └── CS Coil ← cs_coil.capital_cost
│   ├── Blanket (CAS220101) ← 'Blanket System'.capital_cost
│   └── ... other CAS22 components
├── Buildings (CAS21)
└── ... other direct costs
```

**Strengths**:
- Every costed part tagged with CAS category
- Multi-category breakdown (material, fab, installation)
- Automatic aggregation via `sum()`
- Idiot index for manufacturing efficiency

**What's Missing for Full CapEx Visibility**:
- Aggregation calc defs at CAS20, CAS22 levels
- Total capital cost (C990000) calculation
- Pre-construction and indirect costs (CAS10, CAS30-60)

#### 3.2 OpEx Visibility (GAPS in Current Strategy)

**Not specified in strategy**:
- `calc def AnnualizedOMCostCalc` for CAS70
- `calc def AnnualizedFuelCostCalc` for CAS80
- `calc def AnnualizedFinancialCostCalc` for CAS90
- Part or attribute structure for operating parameters

**PyFECONS OpEx Parameters** (would need SysML attributes):
| Parameter | Type | Typical Value | SysML Location Needed |
|-----------|------|---------------|----------------------|
| `plant_lifetime` | Years | 30 | `'Fusion Power Plant'` attribute |
| `plant_availability` | Percent | 0.85 | `'Fusion Power Plant'` attribute |
| `capital_recovery_factor` | Ratio | 0.09 | Financial calc input |
| `yearly_inflation` | Percent | 0.0245 | Financial calc input |

#### 3.3 Energy Production Visibility (PARTIAL)

**Complete**:
- MFE Power Balance calc def (p_net, p_alpha, p_neutron, q_sci, q_eng)

**Missing**:
- IFE Power Balance calc def
- PowerTable-equivalent part def that aggregates power values
- Connection from p_net to LCOE denominator

---

### 4. Requirements Definition Analysis

#### 4.1 Original Goals (from OVERVIEW.md)

```markdown
**Goals**:
1. Formal Integration - Connect behavior, structure, and physics
2. Validation Framework - Constraint-based checking
3. Design Exploration - Parametric studies
4. Bottom-Up Analysis - LCOE estimation from components
```

**Observation**: These are high-level aspirational goals, not testable requirements.

#### 4.2 Strategy Document Goals (20260123)

```markdown
**Research Question**: How should we map PyFECONS structure into SysML to enable:
1. Multi-concept fusion plant modeling (MFE, IFE, MIF)
2. Component reuse between designs
3. LCOE estimation with traceable cost breakdowns
4. Validation against PyFECONS calculations
```

**Better**, but still missing:
- Acceptance criteria (what tolerance for validation?)
- Scope boundaries (which CAS categories are required vs optional?)
- Specific LCOE outputs required

#### 4.3 What's Missing in Requirements

| Requirement Area | Current State | What's Needed |
|------------------|---------------|---------------|
| **LCOE Output** | "Final output" | Specific: LCOE in $/MWh, plus breakdown by capital/O&M/fuel |
| **Validation Tolerance** | None specified | E.g., "Within 5% of PyFECONS for CATF baseline" |
| **CAS Coverage** | Enum has all codes | Which are required for MVP vs Phase 2? |
| **Physics Fidelity** | "Match PyFECONS" | Which calculations need full fidelity vs simplified? |
| **OpEx Requirements** | Not specified | Need CAS70-90 calc defs, operating parameters |
| **Component Lifetimes** | Not specified | Is this in scope or out of scope? |

---

### 5. Recommended Strategy Updates

#### 5.1 Add Explicit LCOE Requirements

Create a new section in the strategy document or a separate spec:

```markdown
## LCOE Calculation Requirements

### Required Outputs
1. **LCOE_total** (C1000000): Levelized Cost of Electricity in $/MWh
2. **LCOE_capital**: Capital contribution to LCOE
3. **LCOE_om**: O&M contribution to LCOE
4. **LCOE_fuel**: Fuel contribution to LCOE
5. **Annual_energy**: 8760 × p_net × n_mod × availability (MWh)

### Required Inputs (Operating Parameters)
1. `plant_lifetime : Years` - on 'Fusion Power Plant' part def
2. `plant_availability : Percent` - on 'Fusion Power Plant' part def
3. `n_mod : Integer` - number of modules
4. `yearly_inflation : Percent` - financial parameter
5. `capital_recovery_factor : Ratio` - default 0.09

### Required Intermediate Calculations
1. `calc def TotalCapitalCostCalc` - Sum CAS10-60
2. `calc def AnnualizedFinancialCalc` - CRF × C990000
3. `calc def AnnualizedOMCalc` - 60 $/kW-yr × P_net
4. `calc def AnnualizedFuelCalc` - Reactor-type-specific
5. `calc def LCOECalc` - Final LCOE formula
```

#### 5.2 Add OpEx Infrastructure to Roadmap

Update Phase 4 (P2: Cost Rollup and LCOE) to include:

```markdown
### Phase 4: Cost Calculations (P2)

**Scope** (expanded):
1. `library/calculations/costing/cas_rollup.sysml`
   - `calc def DirectCostTotalCalc` (CAS20 = sum CAS21-29)
   - `calc def TotalCapitalCostCalc` (C990000 = sum CAS10-60)

2. `library/calculations/costing/annualized/`
   - `cas70_om.sysml` - `calc def AnnualizedOMCalc`
   - `cas80_fuel_mfe.sysml` - `calc def MFEFuelCostCalc`
   - `cas90_financial.sysml` - `calc def AnnualizedFinancialCalc`

3. `library/calculations/lcoe/lcoe.sysml`
   - `calc def LCOECalc` - Complete LCOE formula
   - Outputs: LCOE_total, LCOE_capital, LCOE_om, LCOE_fuel

4. `library/definitions/plant.sysml` (update)
   - Add operating parameters: plant_lifetime, plant_availability, n_mod
   - Add financial parameters attribute group
```

#### 5.3 Clarify Replacement/Maintenance Scope

Add explicit decision to strategy:

```markdown
### Design Decision: Replacement Cost Modeling

**Decision**: Follow PyFECONS approach (simple percentage-based replacement)

**Rationale**:
- PyFECONS uses `replacement_factor × C220100` (typically 10%)
- Component-specific lifetime modeling is out of scope for MVP
- Matches validation baseline

**Future Enhancement** (out of scope):
- Component-specific lifetimes (first wall, magnets, etc.)
- Replacement scheduling during plant operation
- NPV of replacement cash flows

**Implementation**:
- Add `replacement_factor : Ratio` attribute to `'Primary Structure'` part def
- Add `calc def ScheduledReplacementCalc` computing CAS220119
```

#### 5.4 Add Validation Acceptance Criteria

```markdown
### Validation Acceptance Criteria

**CATF MFE Baseline Validation**:
| Metric | PyFECONS Value | Tolerance |
|--------|----------------|-----------|
| p_net | [TBD from DefineInputs] | ±1% |
| C220000 (Reactor Equipment) | [TBD] | ±5% |
| C990000 (Total Capital) | [TBD] | ±5% |
| LCOE (C1000000) | [TBD] | ±5% |

**Validation Process**:
1. Run PyFECONS with CATF inputs → baseline values
2. Run SysML model with same inputs → model values
3. Compare and document deviations
4. Pass: All metrics within tolerance
```

---

## Feasibility Assessment

### Can Current Strategy Produce LCOE? **PARTIALLY**

**What's Ready**:
- CapEx component costs (via 'Costed Component' pattern)
- Power balance (p_net from MFE Power Balance)
- CAS category taxonomy (enum)

**What's Missing**:
- Annualized cost calc defs (CAS70-90)
- Total capital cost aggregation (C990000)
- Operating parameters (lifetime, availability)
- Final LCOE calc def

**Estimated Additional Work**: 2-3 new calc def files, updates to plant.sysml

### Are Maintenance Costs Covered? **MINIMALLY**

**Covered**:
- CAS220119 in enum (scheduled replacement)
- `replacement_factor` mentioned in backlog

**Not Covered**:
- Actual calc def for CAS220119
- O&M calc def (CAS70)
- Component lifetime modeling (out of scope for PyFECONS parity)

### Is Cost Visibility Sufficient? **FOR CAPEX YES, FOR OPEX NO**

**CapEx Visibility**: Excellent
- Every component tagged with CAS category
- Multi-category breakdown (material/fab/install)
- Automatic rollup via sum()

**OpEx Visibility**: Gap
- No structure for annualized costs
- No part def or calc def for operating parameters
- LCOE components not separated

---

## Recommendations

### Immediate (Before P1 Work)

1. **Add operating parameters to `'Fusion Power Plant'` spec**
   - `plant_lifetime : Years`
   - `plant_availability : Percent`
   - `n_mod : Integer`

2. **Specify LCOE output requirements**
   - Document what LCOE outputs are required (total + breakdown)
   - Add to P2 scope in backlog

3. **Document maintenance scope decision**
   - Explicitly state that component-specific lifetimes are out of scope
   - Note as future enhancement

### Near-Term (P2 Planning)

4. **Expand P2: Cost Rollup and LCOE scope**
   - Add annualized cost calc defs (CAS70-90)
   - Add LCOE calc def with component outputs
   - Add financial parameter inputs

5. **Create PyFECONS baseline values document**
   - Run CATF example through PyFECONS
   - Extract all intermediate values for validation
   - Document tolerances

### Deferred (P3+)

6. **Component lifetime modeling** (if needed beyond PyFECONS)
   - Per-component lifetime attributes
   - Replacement scheduling analysis
   - Enhanced availability modeling

---

## Open Questions for User

1. **LCOE Decomposition**: Do you need LCOE broken down by capital/O&M/fuel, or just total LCOE?

2. **Validation Tolerance**: What tolerance is acceptable for matching PyFECONS? (Suggested: ±5%)

3. **Component Lifetimes**: Is modeling individual component lifetimes (beyond PyFECONS capability) a goal, or strictly out of scope?

4. **Pre-construction/Indirect Costs**: CAS10, CAS30-60 are in the enum but not in any planned part defs. Are these needed for MVP?

---

## Code/Model References

### PyFECONS Files
- `/home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py` - LCOE formula
- `/home/reid/PyFECONS/pyfecons/costing/calculations/cas70_annualized_om.py` - O&M calculation
- `/home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py` - Financial costs
- `/home/reid/PyFECONS/pyfecons/costing/calculations/cas22/cas220119_replacement.py` - Replacement costs
- `/home/reid/PyFECONS/pyfecons/data.py` - Data container with aggregation methods
- `/home/reid/PyFECONS/pyfecons/inputs/basic.py` - Operating parameters

### Project Files
- `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md` - Current strategy
- `modeling_pm/docs/COST_MODELING.md` - Cost modeling patterns
- `models/library/foundation/costing.sysml` - 'Costed Component' interface
- `modeling_pm/backlog/BACKLOG.md` - Work items and phases

---

## Appendix: LCOE Calculation Flow Diagram

```
                    INPUTS
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌─────────┐     ┌──────────┐     ┌──────────┐
│ Physics │     │  CapEx   │     │Financial │
│ (p_net) │     │(CAS10-60)│     │Parameters│
└────┬────┘     └────┬─────┘     └────┬─────┘
     │               │                 │
     │               ▼                 │
     │         ┌──────────┐            │
     │         │ C990000  │◄───────────┘
     │         │(Total Cap│            │
     │         └────┬─────┘            │
     │              │                  │
     │              ▼                  │
     │         ┌──────────┐            │
     │         │ C900000  │◄── CRF ────┘
     │         │(Ann.Fin) │
     │         └────┬─────┘
     │              │
     │   ┌──────────┼──────────┐
     │   │          │          │
     ▼   ▼          ▼          ▼
┌───────────┐ ┌──────────┐ ┌──────────┐
│  C700000  │ │ C900000  │ │ C800000  │
│ (Ann.O&M) │ │(Ann.Fin) │ │(Ann.Fuel)│
└─────┬─────┘ └────┬─────┘ └────┬─────┘
      │            │             │
      └────────────┼─────────────┘
                   │
                   ▼
              ┌─────────┐
              │  LCOE   │ = Numerator / (8760 × p_net × n_mod × avail)
              │($/MWh)  │
              └─────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
         ▼         ▼         ▼
    LCOE_cap  LCOE_om  LCOE_fuel
   (visible) (visible) (visible)
```

**Current Strategy Coverage**:
- GREEN: p_net (MFE Power Balance complete)
- GREEN: CapEx components (via 'Costed Component')
- RED: C990000 aggregation (not specified)
- RED: C700000, C800000, C900000 (not specified)
- RED: LCOE calc def (P2 backlog, but scope unclear)
- RED: Financial parameters (not specified)

---

**Last Updated**: 2026-01-26
