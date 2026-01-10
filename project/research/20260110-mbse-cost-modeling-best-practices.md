---
date: 2026-01-10
researcher: Claude
topic: "MBSE Cost Modeling Best Practices: Industry Standards and Patterns"
tags: [research, cost-modeling, mbse, sysml, standards, industry-practices]
status: complete
last_updated: 2026-01-10
---

# Research: MBSE Cost Modeling Best Practices

**Date**: 2026-01-10
**Researcher**: Claude
**Research Type**: Industry Standards and Best Practices Survey

## Executive Summary

This research surveys industry standards, academic literature, and commercial tooling approaches for cost modeling within Model-Based Systems Engineering (MBSE). Key findings:

1. **SysML v2 officially adopted (July 2025)** enables better parametric modeling and integration
2. **COSYSMO integration with MBSE** is actively being developed by INCOSE community
3. **NASA/DoD have mature WBS standards** (MIL-STD-881, NASA WBS Handbook) that can inform CBS design
4. **The "Idiot Index"** (cost/material ratio) is a validated manufacturing cost metric from SpaceX/Tesla
5. **ESA is adapting MBSE methodology** to SysML v2 with ECSS standards integration
6. **Commercial tools** (Cameo/MagicDraw) have parametric cost analysis plugins but limited built-in cost aggregation

## Research Questions Addressed

### Q1: SysML/SysMLv2 Cost Modeling Patterns

#### Finding: COSYSMO Convergence with MBSE

The most significant recent development is the 2024 INCOSE paper on integrating COSYSMO (Constructive Systems Engineering Cost Model) with MBSE tools.

**Key Insights**:
- COSYSMO was originally developed in 2005 for document-based SE, now being updated for SysML
- The paper "facilitates the convergence of COSYSMO and MBSE by updating the COSYSMO counting rules to specifically address size driver selection and assessment in a SysML model"
- Advanced modeling tool features can "streamline and automate cost estimation activities"
- Modern MBSE tools' queries and crosscutting views "enhance the completeness, quality, and consistency of parametric cost estimation"

**COSYSMO Size Drivers** (relevant to fusion TEA):
1. Number of system requirements
2. Number of operational scenarios
3. Number of interfaces
4. Number of algorithms

**COSYSMO Cost Estimating Relationship**:
```
Effort = Size × EM₁ × EM₂ × ... × EM₁₄
```
Where:
- Size = weighted sum of 4 additive size drivers
- EM = 14 multiplicative effort multipliers (complexity factors)

**Application to Fusion TEA**:
- Size drivers map to: number of subsystems, design parameters, physics algorithms, interface points
- Effort multipliers could include: technical complexity, team experience, tool maturity
- This is primarily for **SE effort estimation**, not hardware cost, but the parametric pattern applies

#### Finding: Digital Engineering Integration

NASA/DoD digital engineering strategies emphasize:
- Creating a "digital thread" linking design decisions to cost impacts
- Computer-readable models replacing document-based processes
- MBSE as enabler for lifecycle cost visibility

**Cost Savings from MBSE** (from DoD studies):
- 25-30% average cost savings in automotive deployments
- 35-40% average time savings
- U.S. Air Force T-7 Red Hawk: 50% software dev time reduction, 80% assembly hours reduction

**Implication**: The fusion TEA project's approach of tightly coupling SysML models with cost calculations aligns with cutting-edge DoD/NASA practices.

---

### Q2: Cost Breakdown Structure (CBS) Standards

#### Finding: MIL-STD-881 Work Breakdown Structure

**NOTE**: MIL-STD-881 is actually about **Work Breakdown Structures (WBS)**, not Cost Breakdown Structures directly. However, CBS often mirrors WBS structure.

**MIL-STD-881F** (latest revision, 2024):
- Provides standardized WBS for defense materiel systems
- Mandatory for all ACAT I, II, III DoD programs
- Integrates WBS with cost, schedule, risk, and performance tracking
- Includes commodity-specific templates (aerospace, space systems, ships, etc.)

**Key Structure** (relevant to fusion plants):
- Level 1: Total System
- Level 2: Major subsystems (standardized by commodity)
- Level 3-7: Detailed breakdown (project-specific)
- Level 7 must align with NASA Core Financial System accounting structure

**WBS-to-CBS Relationship**:
- "One of the favored approaches to developing a CBS is to mimic its companion WBS"
- "They often adopt the same numbering system"
- CBS categorizes costs by roles/teams, WBS by deliverables
- Both support hierarchical rollup

**Application to Fusion TEA**:
- PyFECONS CAS structure already follows this pattern (CAS20 → CAS22 → CAS220101, etc.)
- Our approach of hierarchical part definitions mirrors WBS decomposition
- Cost rollup pattern (leaf → subsystem → system) matches WBS aggregation
- Can reference MIL-STD-881 appendices for similar systems (e.g., space systems for high-tech precedents)

#### Finding: NASA WBS Handbook Integration with EVM

**NASA WBS Handbook** (NASA/SP-2016-3404/REV1):
- "The WBS integrates technical, cost, and schedule parameters"
- "Provides necessary framework for detailed cost estimation and control"
- Top 2 levels dictated by Agency standard templates
- Must correlate exactly (Level 7) with financial accounting structure for Earned Value Management (EVM)

**WBS and Cost Estimation Relationship**:
```
Project Cost Forecast = Σ(Work Package Costs) × Cost Growth Factors
```

**Organizational Elements** (applicable to fusion plants):
- Project Management
- Systems Engineering & Integration (SE&I)
- Safety & Mission Assurance (S&MA)
- Common products reflected appropriately

**Implication**: Our cost architecture should include:
1. Standard top-level categories (like PyFECONS CAS structure)
2. Project-specific subsystem breakdown at lower levels
3. Integration/testing/commissioning cost categories (not just hardware)
4. Traceability from leaf components to top-level totals

---

### Q3: Bill of Materials (BOM) Generation Patterns

#### Finding: Hierarchical BOM with Cost Rollup

**BOM Structure**:
- "Multi-level BOM shows the relationship (parent-child) between components, sub-assemblies, and assemblies"
- Modern BOM systems support up to 15 levels of hierarchy
- Includes planning bills, percentage bills, phantom parts, kit parts

**Cost Rollup Mechanism**:
- "OpenBOM calculates roll-up of specific property (e.g., Cost, Mass) bottom-up"
- "Places roll-up for each level on the upper-level BOM"
- Example: `axle_assembly.cost = screw.cost + wheel.cost + axle.cost`

**BOM Calculation Methods**:
1. **Cost implosion**: Sum costs from lowest BOM level upwards
2. **What-if costing**: Test alternative materials/suppliers
3. **Actual costing**: Track real costs vs. estimates

**BOM Types Across Lifecycle**:
- **Engineering BOM (EBOM)**: Design intent
- **Manufacturing BOM (MBOM)**: Build sequence and tooling
- **Service BOM (sBOM)**: Spare parts and maintenance

**Application to Fusion TEA**:
- Our `'Costed Component'` abstract part def = BOM item interface
- SysML part hierarchy = EBOM structure
- Each part's `capital_cost` attribute = rolled-up BOM cost
- Can extend to MBOM (manufacturing complexity factors) and sBOM (replacement parts) later

**Digital Thread Connection**:
- "BOM connects design intent (EBOM), manufacturing requirements (MBOM), and service configurations (sBOM)"
- "Forms foundation for digital thread continuity across product lifecycle"

**Implication**: The nested cost model pattern we're developing is exactly the BOM cost rollup pattern, implemented in SysML.

---

### Q4: The "Idiot Index" / Commodity Multiple

#### Finding: Validated Manufacturing Cost Metric

**Definition** (from Elon Musk's SpaceX/Tesla methodology):
```
Idiot Index = Finished Product Cost / Raw Material Cost
```

**Application**:
- "Elon has his finance teams at Tesla and SpaceX track the idiot index by component in every product"
- High ratio (e.g., 1:50 for rockets historically) indicates inefficiency or price gouging
- Used to identify opportunities for in-house manufacturing or design simplification

**Companion Metric - Slacker Index**:
```
Slacker Index = Time to Get Part / Time to Make Part
```

**Examples**:
- "$10,000 valve made from $100 of steel → Idiot Index = 100 → overpaying"
- SpaceX brought rocket cost down ~90% by systematically reducing idiot indices

**Application to Fusion TEA**:
- Can calculate idiot index for major components (magnets, blanket, structure)
- Magnet example: `idiot_index = magnet.capital_cost / magnet.conductor_material_cost`
- High indices indicate where cost reduction R&D should focus
- Tracks value-add from manufacturing vs. material costs

**Implementation Pattern**:
```sysml
calc def ComponentCostAnalysis {
    in attribute raw_material_cost : Real;
    in attribute finished_component_cost : Real;

    out attribute idiot_index : Real = finished_component_cost / raw_material_cost;
    out attribute value_added_fraction : Real =
        (finished_component_cost - raw_material_cost) / finished_component_cost;
}
```

**Note**: The exact term "commodity multiple" did not appear in search results; "idiot index" is the industry term for this concept.

---

### Q5: Parametric Cost Estimation Integration

#### Finding: Bottom-Up, Analogous, and Parametric Methods

**Three Primary Cost Estimation Techniques**:

**1. Bottom-Up Estimating**:
- "Constructs estimates for higher level cost elements by aggregating or 'rolling up' detailed estimates from lower level cost elements"
- Uses Work Breakdown Structure (WBS) to define hierarchy
- High accuracy (typically ±10-15%) but time-intensive
- **Most relevant to our approach**: This is exactly our nested cost model pattern

**2. Analogous Estimating**:
- "Top-down estimation technique for estimating the cost, resources and durations of projects"
- Based on historical data from similar systems
- Lower accuracy but fast (useful for early-stage estimates)
- "Many development programs have heritage or legacy systems that can serve as a basis"
- Adjustments made for size/performance differences

**3. Parametric Estimating**:
- Uses statistical relationships between variables
- Example: Cost = a × (Weight)^b × (Complexity Factor)
- COSYSMO is a parametric model for SE effort
- Requires calibration database

**Combining Approaches**:
- "You can use the bottom-up approach together with analogous estimating technique or parametric estimating technique"
- Bottom-up for detailed components, parametric for high-level aggregation
- Analogous for validating reasonableness

**Application to Fusion TEA**:
- **Bottom-up**: Leaf-level cost calcs (conductor volume × $/m³)
- **Parametric**: Scaling laws (magnet cost ~ B⁴)
- **Analogous**: Validation against ARIES-AT, SPARC, ITER cost data
- Hybrid approach maximizes accuracy and flexibility

---

### Q6: ESA MBSE Methodology and ECSS Standards

#### Finding: European Space Agency Leading MBSE Adoption

**ESA MBSE Methodology** (presented at INCOSE IW 2025):
- Based on ECSS (European Cooperation for Space Standardization) standards
- Adapting to SysML v2 through "ESA SysML Solution"
- Ground and Space Segment Engineering Framework (GSEF) - web platform for space missions
- "By using ECSS standards as starting point, processes, terminology and expected outputs are familiar to engineers"

**ECSS Standards** (139 active standards):
- Management (planning, cost, schedule, risk)
- Engineering (technical requirements, design)
- Product Assurance (quality, reliability, safety)
- Space Sustainability

**Model-Based Budget Management**:
- Research presented at MBSE2022 on "model based approach to budget management for Earth Return Orbiter"
- Virtual Spacecraft Design (VSD) project enables MBSE methodology for space systems

**MBSE and Digitalization**:
- "Engineering of space systems is collaborative, iterative process integrating various domain-specific viewpoints"
- "ESA employs MBSE and Semantic-Based System Engineering (SBSE) together to improve digital continuity"
- Relation between MBSE modeling artifacts and ECSS deliverables defined

**Application to Fusion TEA**:
- Space systems share characteristics with fusion plants: complex, high-tech, long development
- Can reference ECSS methodology for validation gates, review processes
- ESA's approach of starting from established standards (ECSS) mirrors our use of PyFECONS
- Model-based budget management directly applicable to our cost architecture

---

### Q7: Commercial Tool Cost Modeling Capabilities

#### Finding: Cameo Systems Modeler (formerly MagicDraw)

**Cameo Simulation Toolkit**:
- "Dynamically solves constraints in context of full systems simulation"
- "Allows tracking and maintaining dependencies among critical parameters such as size, weight, speed, power, temperature, cost"
- **Rollup Pattern Wizard**: "Easily calculate totals for analyzing Mass, Power, Cost"
- "Calculations run recursively to instantly check against constraints"

**ParaMagic Plugin**:
- "Allows performing parametric trade studies and 'what-if' scenarios"
- Swaps given and target values in instance models
- Requires Mathematica for math solving

**Integration Capabilities**:
- Excel spreadsheets for large input datasets
- Matlab, Mathematica, OpenModelica for external solvers
- Multi-output support for trade studies

**Limitations**:
- Cost rollup is semi-manual (requires wizard)
- No built-in cost breakdown standards (user must define structure)
- Additional license cost for Simulation Toolkit
- Proprietary, not open-source

**Application to Fusion TEA**:
- Our approach (SysML v2 + sysml-codegen + teax-simkit) is more open and automated
- Cameo's rollup wizard validates the hierarchical cost aggregation pattern
- Their parametric study capabilities inspire our multi-design comparison framework
- We can achieve similar functionality with open tooling

---

## Synthesis: Recommended Patterns for Fusion TEA

### Pattern 1: Hierarchical Cost Breakdown (CBS aligned with WBS)

**Standard**: Follow NASA WBS / DoD MIL-STD-881 structure

**Implementation**:
```
Level 1: Total Plant Cost (LCOE output)
├─ Level 2: CAS20 Direct Capital
│  ├─ Level 3: CAS22 Reactor Plant Equipment
│  │  ├─ Level 4: CAS220101 Blanket & First Wall
│  │  │  ├─ Level 5: Breeding Zone
│  │  │  └─ Level 5: First Wall Armor
│  │  ├─ Level 4: CAS220103 Magnets
│  │  │  ├─ Level 5: TF Coil System
│  │  │  │  ├─ Level 6: Conductor
│  │  │  │  └─ Level 6: Structure
│  │  │  └─ Level 5: PF Coil System
│  │  └─ ...
│  └─ Level 3: CAS23 Turbine Plant
├─ Level 2: CAS30 Indirect Costs
└─ Level 2: CAS70-90 Operating Costs
```

**Rationale**: PyFECONS already implements this; our SysML model should mirror it.

---

### Pattern 2: Bottom-Up Cost Aggregation with Parametric Calc Defs

**Standard**: INCOSE cost estimation best practices + COSYSMO principles

**Implementation**:
1. **Leaf Level** (Level 5-6): Parametric cost calc defs
   - Example: `TFCoilConductorCost = volume × cost_per_m3 × quantity`

2. **Subsystem Level** (Level 4): Rollup calc defs
   - Example: `TFCoilCost = conductor_cost + structure_cost + integration_cost`

3. **System Level** (Level 3): Category rollup
   - Example: `CAS220103 = sum(all magnet subsystems)`

4. **Plant Level** (Level 1-2): LCOE calculation
   - Aggregates all CAS categories + financial parameters

**Rationale**: Matches industry "bottom-up with parametric" hybrid approach.

---

### Pattern 3: Standard Cost Output Schema

**Standard**: Based on ARPA-E CAS structure used by PyFECONS

**Implementation**: All fusion design models MUST expose these outputs:

```sysml
calc def StandardCostOutputs {
    // CAPITAL COSTS (CAS structure)
    out attribute cas20_direct_total : Real;
    out attribute cas21_buildings : Real;
    out attribute cas22_reactor_equipment : Real;
    out attribute cas22_magnets : Real;           // Breakdown
    out attribute cas22_blanket : Real;           // Breakdown
    out attribute cas22_divertor : Real;          // Breakdown
    out attribute cas23_turbine : Real;
    out attribute cas24_electric : Real;
    out attribute cas25_misc : Real;
    out attribute cas26_heat_rejection : Real;
    out attribute cas27_special_materials : Real;
    out attribute cas30_indirect : Real;
    out attribute cas40_owners : Real;
    out attribute cas50_supplementary : Real;
    out attribute cas60_financial : Real;

    // OPERATING COSTS
    out attribute cas70_annual_om : Real;
    out attribute cas80_annual_fuel : Real;
    out attribute cas90_annualized_capital : Real;

    // SUMMARY METRICS
    out attribute total_capital_cost : Real;
    out attribute overnight_cost_per_kw : Real;
    out attribute lcoe : Real;                    // [$/MWh]

    // BREAKDOWN FRACTIONS
    out attribute capital_lcoe_fraction : Real;
    out attribute om_lcoe_fraction : Real;
    out attribute fuel_lcoe_fraction : Real;
    out attribute magnet_cost_fraction : Real;    // % of CAS22
    out attribute blanket_cost_fraction : Real;   // % of CAS22

    // COST EFFICIENCY METRICS
    out attribute magnet_idiot_index : Real;      // finished/material
    out attribute blanket_idiot_index : Real;
}
```

**Rationale**:
- Enables systematic cross-concept comparison
- Compatible with PyFECONS validation
- Supports sensitivity analysis and trade studies

---

### Pattern 4: Costed Component Interface

**Standard**: Abstract base definition pattern (common in MBSE)

**Implementation**:
```sysml
abstract part def 'Costed Component' {
    doc /*
    All cost-bearing components must specialize this definition.
    Ensures consistent cost interface across system hierarchy.
    */

    // Required attributes
    attribute capital_cost : Real;

    // Optional lifecycle attributes
    attribute annual_operating_cost : Real default := 0.0;
    attribute replacement_cost : Real default := 0.0;
    attribute replacement_interval_years : Real default := 40.0;

    // Optional material cost tracking (for idiot index)
    attribute raw_material_cost : Real default := 0.0;
    attribute idiot_index : Real = capital_cost / raw_material_cost;
}
```

**Rationale**: Enforces consistent cost interface, enables recursive rollup, supports lifecycle analysis.

---

### Pattern 5: Semantic Cost Calc Defs (Not Generic Math)

**Standard**: COSYSMO principle of domain-specific models

**Bad Pattern** (generic math abstraction):
```sysml
// AVOID THIS
calc def Multiply {
    in x : Real;
    in y : Real;
    out result : Real = x * y;
}
```

**Good Pattern** (domain-specific with documentation):
```sysml
calc def TFCoilConductorCost {
    doc /*
    TF coil conductor cost based on HTS tape volume and market pricing.

    **Source**: PyFECONS CAS220103
    **Assumptions**:
    - REBCO HTS tape at $150/kA-m (2025 pricing)
    - Structural fraction = 0.3
    - Integration labor = 0.25 × material cost
    */

    in attribute tape_length : Real;              // [m]
    in attribute current_rating : Real;           // [kA]
    in attribute n_coils : Integer;
    in attribute hts_cost_per_ka_m : Real default := 150.0;

    out attribute material_cost : Real =
        tape_length × current_rating × n_coils × hts_cost_per_ka_m / 1.0e6;

    out attribute structural_cost : Real = material_cost × 0.3;
    out attribute integration_cost : Real = material_cost × 0.25;
    out attribute total_capital : Real =
        material_cost + structural_cost + integration_cost;

    // Metrics
    out attribute cost_per_coil : Real = total_capital / n_coils;
    out attribute material_fraction : Real = material_cost / total_capital;
}
```

**Rationale**:
- Encodes domain knowledge explicitly
- Traceable to source (PyFECONS)
- Self-documenting
- Exposes intermediate values for debugging/validation

---

### Pattern 6: Multi-Output for Full Visibility

**Standard**: Digital thread principle - expose all intermediate values

**Implementation**: Every calc def should expose:
- Primary output (e.g., `total_capital`)
- Intermediate calculations (e.g., `material_cost`, `labor_cost`)
- Breakdown fractions (e.g., `material_fraction`)
- Cost efficiency metrics (e.g., `idiot_index`, `cost_per_unit`)

**Benefits**:
- Debugging (trace unexpected costs to specific drivers)
- Validation (compare intermediate values with PyFECONS)
- Sensitivity analysis (identify high-leverage cost drivers)
- Transparency (auditable cost models)

**Tooling Support**:
- sysml-codegen automatically generates multi-output Pydantic models
- teax-simkit routes each output to separate channel
- RunManifest captures all outputs for comparison

---

## Validation Framework (agentic-mbse Level 9)

### Rule 1: Every Costed Component Has Cost Calc Def

**Check**: For each `PartDefinition` specializing `'Costed Component'`:
- Verify corresponding `CalculationDefinition` exists
- Naming convention: `{PartDefName}Cost` or `{PartDefName}CostCalc`

**Severity**: ERROR (blocks codegen)

### Rule 2: Cost Calc Inputs Match Part Attributes

**Check**: For each cost calc def:
- Extract all input parameters
- Find associated part definition
- Verify inputs are subset of part attributes (or explicit external parameters)

**Severity**: WARNING (may indicate missing data binding)

### Rule 3: All Cost-Bearing Parts Have Cost Calc Usages

**Check**: For each `PartUsage` in design files:
- If its type specializes `'Costed Component'`
- Verify at least one `CalculationUsage` exists that references it

**Severity**: ERROR (cost will be missing from rollup)

### Rule 4: Standard Outputs Present

**Check**: Top-level design file must expose StandardCostOutputs schema:
- All required CAS categories
- LCOE and summary metrics
- Breakdown fractions

**Severity**: ERROR (cannot compare across designs)

---

## Comparison with Current Fusion TEA Architecture

| Aspect | Current Approach | Industry Best Practice | Assessment |
|--------|-----------------|------------------------|------------|
| **Hierarchical CBS** | PyFECONS CAS structure | NASA WBS / MIL-STD-881 | ✅ Aligned |
| **Cost Rollup** | Bottom-up aggregation | Bottom-up + parametric hybrid | ✅ Aligned |
| **Cost Calc Defs** | Semantic (domain-specific) | Domain-specific (COSYSMO principle) | ✅ Aligned |
| **Component Interface** | `'Costed Component'` abstract part def | Abstract base definition pattern | ✅ Aligned |
| **Multi-Output** | All calcs expose 5-20+ outputs | Digital thread visibility | ✅ Aligned |
| **Validation** | agentic-mbse Level 9 planned | Validation gates in ECSS/DoD | ✅ Aligned |
| **Nested Calc Models** | Preferred pattern (tooling gap) | Not standard (explicit wiring common) | ⚠️ Advanced |
| **Standard Outputs** | Planned StandardCostOutputs | Required for cross-project comparison | ✅ Aligned |
| **Idiot Index** | Not yet implemented | SpaceX/Tesla best practice | 🔄 Should add |

**Overall Assessment**: The fusion TEA architecture aligns well with industry best practices. Key differentiator is nested cost model pattern, which is more advanced than typical MBSE cost approaches but requires tooling enhancement.

---

## Recommendations

### Immediate Actions (Phase 1)

1. **Implement StandardCostOutputs schema** in `models/library/calculations/standard_outputs.sysml`
   - All 30+ required outputs documented
   - Reference as interface all designs must satisfy

2. **Add idiot index calculations** to material-intensive subsystems:
   - Magnets (conductor material vs. finished coil cost)
   - Blanket (steel/lithium vs. finished module cost)
   - Structure (steel vs. fabricated structure cost)

3. **Document CBS-to-WBS mapping** in `MODELING_GUIDE.md`:
   - Reference MIL-STD-881 for precedent
   - Map PyFECONS CAS structure to NASA WBS levels
   - Define naming conventions for part defs at each level

4. **Implement Level 9 validation rules** in agentic-mbse:
   - Start with Rules 1 and 3 (highest value)
   - Add Rule 4 for design gate checks

### Medium-Term Actions (Phase 2)

5. **Develop comparison framework**:
   - Visualization scripts for CAS breakdown bar charts
   - Sankey diagram for cost flow
   - Tornado plots for sensitivity analysis

6. **Add analogous cost validation**:
   - Compare CATF outputs with ARIES-AT, SPARC published costs
   - Document assumptions/adjustments for differences
   - Build confidence in model accuracy

7. **Enhance tooling for nested cost models**:
   - Implement sysml-codegen enhancements per prior research
   - Enable automatic calc instantiation per part usage
   - Simplify design files (remove manual wiring)

### Long-Term Actions (Phase 3)

8. **Extend to lifecycle cost**:
   - Scheduled replacement costs
   - Decommissioning cost models
   - Learning curves for serial production

9. **Uncertainty quantification**:
   - Add min/max/confidence attributes to cost params
   - Monte Carlo simulation for cost uncertainty propagation
   - Risk-adjusted LCOE calculation

10. **Cross-domain integration**:
    - Link structural analysis (stress, fatigue) to replacement schedules
    - Couple neutronics (damage) to maintenance costs
    - Integrate supply chain (lead time) with construction schedule

---

## Gaps in Industry Practice (Opportunities for Contribution)

### Gap 1: Limited SysML v2 Cost Modeling Literature

**Observation**: Most MBSE cost modeling literature focuses on SysML v1.x. SysML v2 adoption for cost modeling is nascent.

**Opportunity**: Fusion TEA project could publish:
- SysML v2 cost modeling patterns
- Validation of nested cost model approach
- Open-source tooling (sysml-codegen + teax-simkit)
- Case study: multi-concept comparison

**Venues**: INCOSE International Symposium, IEEE Systems Journal

### Gap 2: Hardware Cost Estimation (vs. SE Effort)

**Observation**: COSYSMO focuses on systems engineering **effort** estimation, not hardware **cost**. Most MBSE literature addresses project costs, not product costs.

**Opportunity**: Fusion TEA cost models directly estimate hardware LCOE, filling a gap in MBSE literature.

### Gap 3: Open-Source MBSE Cost Tools

**Observation**: Commercial tools (Cameo) have proprietary cost modeling plugins. No open-source equivalent exists.

**Opportunity**: Our sysml-codegen + teax-simkit stack is open-source and specifically designed for cost analysis pipelines.

### Gap 4: Physics-Based Parametric Cost Models

**Observation**: Most parametric cost models are statistical (regression on historical data). Few encode physics-based scaling laws.

**Opportunity**: Fusion cost models combine:
- Physics scaling (B⁴ for magnets, neutron flux for blanket lifetime)
- Engineering heuristics (structural fractions, integration factors)
- Economic parameters (learning curves, financial assumptions)

This hybrid approach is rare in MBSE literature.

---

## References

### Industry Standards

1. **MIL-STD-881F** (2024) - Work Breakdown Structures for Defense Materiel Items
   - Source: [GlobalSpec](https://standards.globalspec.com/std/14535306/mil-std-881f)

2. **NASA WBS Handbook** (NASA/SP-2016-3404/REV1)
   - Source: [NASA Technical Reports Server](https://ntrs.nasa.gov/citations/20180000844)

3. **ECSS Standards** - European Cooperation for Space Standardization
   - Source: [ECSS Official Site](https://ecss.nl/)

### Academic Papers

4. Papke et al. (2024) - "The Convergence of COSYSMO Parametric Cost Estimation with Model-Based Systems Engineering"
   - Source: [INCOSE International Symposium](https://incose.onlinelibrary.wiley.com/doi/abs/10.1002/iis2.13176)

5. Papke (2018) - "Integration of Parametric Cost Estimation with System Architecture"
   - Source: [INCOSE International Symposium](https://incose.onlinelibrary.wiley.com/doi/abs/10.1002/j.2334-5837.2018.00544.x)

6. ESA (2024) - "The European Space Agency MBSE Methodology"
   - Source: [INCOSE International Symposium](https://incose.onlinelibrary.wiley.com/doi/10.1002/iis2.13256)

### Industry Resources

7. **SEBoK** - Systems Engineering Body of Knowledge, "Cost Estimating and Analysis"
   - Source: [SEBoK Wiki](https://sebokwiki.org/wiki/Cost_Estimating_and_Analysis_in_Systems_Engineering)

8. **Idiot Index** - Elon Musk's cost efficiency metric
   - Source: [Exponential Industry](https://substack.exponentialindustry.com/p/ratio-of-finished-cost-to-material-cost-musk)

9. **OpenBOM** - Bill of Materials Rollups
   - Source: [Medium Article](https://medium.com/@openbom/bill-of-materials-rollups-101-using-openbom-471ff5904a8b)

### Commercial Tools

10. **Cameo Systems Modeler** - No Magic (Dassault Systèmes)
    - Source: [3DS Product Page](https://www.3ds.com/products/catia/no-magic/cameo-systems-modeler)

11. **Cameo Simulation Toolkit** - Parametric analysis plugin
    - Source: [3DS Product Page](https://www.3ds.com/products/catia/no-magic/cameo-simulation-toolkit)

### SysML v2 Specification

12. **SysML v2 Official Specification** (July 2025 adoption)
    - Source: [OMG SysML v2](https://www.omg.org/sysml/sysmlv2/)

---

## Appendix A: COSYSMO Size Drivers Detail

From Ricardo Valerdi's original COSYSMO model:

**Size Driver 1: Requirements**
- Count of system-level requirements
- Excludes software-only, includes hardware/system interface requirements

**Size Driver 2: Interfaces**
- Count of external interfaces
- Includes human-machine, hardware-hardware, hardware-software

**Size Driver 3: Algorithms**
- Count of unique algorithms requiring systems engineering
- Includes control algorithms, trade studies, optimization routines

**Size Driver 4: Operational Scenarios**
- Count of distinct operational scenarios
- Includes nominal operations, off-nominal, degraded modes

**Application to Fusion Plant**:
- Requirements: ~500 system requirements for ITER-class plant
- Interfaces: ~200 (plasma-facing, coolant, power extraction, control)
- Algorithms: ~50 (plasma control, tritium breeding, thermal management)
- Scenarios: ~20 (startup, steady-state, shutdown, ELMS, disruption recovery)

**COSYSMO Effort Estimation** (for reference):
```
Effort (person-months) = 2.5 × Size^1.06 × EM₁ × EM₂ × ... × EM₁₄
```

Where typical effort multipliers include:
- Requirements understanding (0.88 - 1.20)
- Architecture understanding (0.90 - 1.14)
- Technology availability (0.91 - 1.15)
- Tool support (0.88 - 1.20)

---

## Appendix B: BOM Cost Rollup Example

**Hierarchical Structure**:
```
Bike (finished product)
├─ Frame
│  ├─ Tubing (raw material: $50)
│  └─ Welding + Finishing (value-add: $150)
│  Total Frame Cost: $200
│
├─ Front Wheel
│  ├─ Hub (material: $10, finished: $50)
│  ├─ Tire (material: $5, finished: $30)
│  └─ Assembly (labor: $10)
│  Total Wheel Cost: $90
│
└─ Rear Wheel
   └─ (same as front: $90)

Assembly & QC: $50

Total Bike Cost: $200 + $90 + $90 + $50 = $430

Idiot Index (Bike): $430 / ($50+$10+$5+$10+$5) = $430/$80 = 5.4
```

**Interpretation**:
- Idiot Index = 5.4 → Value-add is 440% of material cost
- Reasonable for engineered product with significant labor/integration
- If ratio were 50:1, would indicate opportunity for cost reduction

**Fusion Plant Parallel**:
```
CATF Plant: $5,000M
├─ Magnets: $1,200M
│  ├─ HTS Conductor (material): $400M
│  ├─ Structure (material): $100M
│  └─ Fabrication/Integration (value-add): $700M
│  Idiot Index: $1,200M / $500M = 2.4 ✓ reasonable
│
├─ Blanket: $800M
│  ├─ Li₄SiO₄ + steel (material): $200M
│  └─ Fabrication/Integration: $600M
│  Idiot Index: $800M / $200M = 4.0 ✓ reasonable
│
└─ ...
```

High idiot indices would indicate targets for design simplification or supplier negotiation.

---

## Appendix C: Digital Thread Concept

**Definition**: "A digital thread is the communication framework connecting data across the product lifecycle, enabling automated and integrated data flow."

**Layers**:
1. **Requirements** (system specs)
2. **Design** (CAD, SysML models)
3. **Analysis** (FEA, thermal, cost)
4. **Manufacturing** (MBOM, process plans)
5. **Operations** (sensor data, maintenance logs)
6. **Disposal** (decommissioning, recycling)

**Cost Thread**:
```
Design Decision → Part Geometry → Material Volume → Material Cost →
Manufacturing Complexity → Labor Hours → Total Part Cost →
System Cost → LCOE
```

**Traceability**:
- Change magnet field strength (design) → propagates to conductor volume → material cost → total magnet cost → CAS22 → LCOE
- Digital thread enables "what-if" analysis with full cost impact visibility

**Fusion TEA Implementation**:
- SysML models = design layer
- sysml-codegen = transforms to analysis modules
- teax-simkit = executes cost calculations
- Output manifests = results layer
- Git history = traceability of design evolution

---

**Last Updated**: 2026-01-10
**Related Research**:
- `project/research/20260106-065431_cost-architecture-patterns.md`
- `project/research/20260107-final-cost-architecture.md`
- `project/research/NEXT_cost-architecture-patterns.md`
