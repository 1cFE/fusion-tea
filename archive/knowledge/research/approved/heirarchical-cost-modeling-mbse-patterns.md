# Hierarchical cost modeling in MBSE: SysMLv2 patterns and cross-domain best practices

**Effective cost modeling in Model-Based Systems Engineering requires combining SysMLv2's enhanced expression capabilities with proven domain cost structures from aerospace/defense and energy sectors.** No standardized OMG cost profile exists, but practitioners have developed robust patterns using constraint definitions, recursive rollups, and hierarchical value aggregation. The aerospace MIL-STD-881 Work Breakdown Structure and energy sector's LCOE frameworks provide complementary cost categorization schemes that can inform a unified SysMLv2 cost metamodel. This synthesis enables consistent cost rollup at any decomposition level while supporting commodity multiple calculations and completeness validation.

---

## SysMLv2 offers enhanced mechanisms for cost modeling

The OMG SysML specification provides foundational constructs for cost representation but **no official cost profile exists**. In SysML v1.x, practitioners built cost models using Value Properties typed by currency ValueTypes, Constraint Blocks defining mathematical relationships, and Parametric Diagrams binding constraint parameters to system values. These patterns enabled hierarchical rollup but required tool-specific extensions—Cameo's Rollup Pattern Wizard being the most mature commercial implementation.

SysMLv2 introduces significant improvements for cost modeling. The new **attribute definitions** replace value properties with more precise semantics, while **constraint definitions** enable formal mathematical expressions that evaluate deterministically. The built-in expression language supports dimensional analysis with automatic unit checking through an enhanced units library. Most importantly, the usage-focused modeling paradigm creates natural decomposition hierarchies where parts can be specialized while inheriting cost calculation behaviors.

A practical SysMLv2 cost modeling pattern leverages these constructs:

```sysml
attribute def CostValue :> ISQ::MonetaryAmount {
    attribute currency : CurrencyUnit;
}

part def CostableElement {
    attribute directMaterialCost : CostValue;
    attribute directLaborCost : CostValue;
    attribute overheadCost : CostValue;
    attribute totalCost : CostValue;
    
    constraint totalCostCalc {
        totalCost == directMaterialCost + directLaborCost + overheadCost
    }
}
```

The key insight from InterCAX research is that **recursive rollup through inheritance** minimizes parametric relation complexity. Making the cost constraint a property of a supertype enables redefinition and recursion throughout the parts tree, preserving component individuality while enabling automatic aggregation.

---

## MIL-STD-881 provides the definitive aerospace cost breakdown architecture

The DoD's MIL-STD-881F establishes **11 standard Work Breakdown Structures** across defense materiel categories—aircraft, missiles, ships, space systems, launch vehicles, and others. The standard mandates government-controlled definitions for WBS Levels 1-3, with contractor discretion for Level 4 and below. This creates consistent top-level categories while allowing necessary detail variation.

Common elements appearing across all defense systems include Integration/Assembly/Test, Systems Engineering, Program Management, Test and Evaluation, Peculiar and Common Support Equipment, and Initial Spares. These elements map directly to SysMLv2 part definitions that can be reused across system variants.

NASA's Cost Estimating Handbook v4.0 complements MIL-STD-881 with a **12-step cost estimating process** organized into Project Definition, Cost Methodology, and Cost Estimate phases. NASA's standard Level 2 WBS elements—Project Management, Systems Engineering, Mission Assurance, Payload, Flight Systems, Ground Systems, and Mission Operations—provide a space-systems-specific hierarchy that maps cleanly to SysML block decomposition.

The parametric cost relationships (CERs) used in aerospace follow the general form **Cost = k × (Parameter)^b**, where mass, power, and complexity drive most estimates. The NASA/Air Force Cost Model (NAFCOM) organizes costs into distinct Elements of Cost: Labor (engineering and manufacturing hours), Material (raw materials and purchased parts), Subcontracts, Other Direct Charges, Overhead, and G&A. This EOC breakdown provides the categorical structure for BOM-style cost extraction.

---

## Energy sector cost structures emphasize lifecycle levelization

The **Levelized Cost of Energy (LCOE)** framework differs fundamentally from aerospace cost structures by normalizing all costs to a per-unit-energy basis ($/MWh) over project lifetime. The core equation—LCOE = (CapEx × FCR + OpEx) / Net Annual Energy—integrates capital recovery, operating costs, and production into a single comparable metric.

NREL's Annual Technology Baseline provides the most comprehensive publicly available cost database, organized hierarchically:

- **Level 1**: Technology categories (wind, solar, storage, thermal)
- **Level 2**: Cost and performance parameters (CapEx, O&M, capacity factor, LCOE)
- **Level 3**: Scenario dimensions (Conservative/Moderate/Advanced innovation paths)

CapEx breakdown structures vary by technology but follow a consistent pattern. For **wind energy**, NREL allocates costs across Turbine CapEx (**41%** for nacelle, rotor, tower), Balance of System (**22%** for foundations, electrical collection, roads), and Soft Costs (**11%** for engineering, permits, financing). Offshore wind adds substructure/foundation costs that often exceed turbine costs.

The critical distinction from aerospace is **O&M treatment**. Energy sector O&M typically represents 20-40% of LCOE split into fixed ($/kW-yr) and variable ($/MWh) components. Aerospace operating and support costs often exceed 60-70% of total lifecycle cost with far more detailed sustainment WBS elements covering personnel, depot maintenance, and logistics.

---

## Parametric tools reveal proven data model architectures

SEER and PRICE TruePlanning have refined hierarchical cost modeling over decades. **SEER** organizes cost elements across multiple dimensions—for software using size parameters (SLOC, function points), technology factors, and entropy; for hardware using component counts, manufacturing complexity, material specifications, and TRL. SEER supports flexible WBS organization with parent-child relationships, recursive rollup, and industry-specific knowledge bases.

**PRICE TruePlanning** uses a Product Breakdown Structure as its organizing framework with integrated models for hardware lifecycle, software development, assembly/integration, and program management. PRICE's risk methodology employs the **Method of Moments** for uncertainty analysis with triangular distributions and configurable correlation levels.

The cost estimation methodology taxonomy recognized by NASA, GAO, and ICEAA comprises four approaches with specific applicability:

| Methodology | When Applied | Accuracy Range |
|-------------|--------------|----------------|
| **Analogy** | Pre-Phase A/Phase A, limited data | ±30-50% |
| **Parametric** | Trade studies, design-to-cost | ±20-35% |
| **Engineering Build-Up** | Phase C/D, production | ±10-20% |
| **Expert Judgment** | Supplement other methods | Variable |

Both tools handle **recursive cost rollups** through consistent bottom-up aggregation patterns: component costs sum to assembly costs, which sum to subsystem costs, which sum to system costs. Indirect costs (overhead, G&A) are allocated at specified levels using proportional, activity-based, or direct allocation methods.

---

## The Idiot Index quantifies manufacturing efficiency opportunities

The **Idiot Index** (or Commodity Multiple) measures the ratio of finished component cost to raw material cost. Coined by Elon Musk at SpaceX, the metric follows from first-principles analysis: if a component's finished cost is 50× its material basis cost, significant manufacturing optimization opportunity likely exists.

**Calculation**: Idiot Index = Component Cost ÷ Raw Material Cost

SpaceX uses a rough threshold of **10:1** to flag components warranting cost reduction investigation. The $120,000 actuator recreated in-house for $5,000 (24:1 reduction) and $1,500 NASA door latch replaced with a modified $30 bathroom latch (50:1) illustrate the metric's targeting value.

Computing commodity multiples requires maintaining two cost dimensions in the data model:

1. **Manufactured/Purchased Cost**: Actual BOM cost from suppliers or work-in-process
2. **Material Basis Cost**: Commodity-level pricing for base materials (metals, polymers, electronics feedstock)

The Idiot Index is essentially a simplified **should-cost analysis** metric. Traditional value engineering (originating with Lawrence Miles at GE in the 1940s) provides the established methodology that the Idiot Index operationalizes as a single prioritization number. In SysMLv2, this requires attribute definitions capturing both cost values and deriving the ratio through a constraint expression.

---

## BOM-based costing extends beyond materials to capture full costs

Modern Bill of Materials structures must integrate direct costs (materials, labor, equipment) with indirect costs (overhead, G&A) for accurate hierarchical rollup. The standard BOM cost element hierarchy includes:

1. **Material costs** — Raw materials, purchased components, subassemblies
2. **Labor costs** — Direct wages by skill category, setup time, processing time
3. **Manufacturing overhead** — Work center rates × processing time
4. **Tooling/fixtures** — Amortized special tooling costs
5. **Subcontract services** — External processing and purchased services
6. **Logistics** — Transportation, warehousing, handling

Activity-Based Costing (ABC) provides a four-tier framework for cost categorization: **unit-level** costs (40-70%, varying with production volume), **batch-level** costs (10-32%, per production run), **product-sustaining** costs (10-24%, R&D and engineering), and **facility-sustaining** costs (5-15%, general overhead).

For SysMLv2 modeling, each cost tier should map to distinct attribute definitions with explicit allocation rules. The rollup algorithm must handle **mixed cost types**: unit-level costs multiply by quantity and sum directly, while batch-level and product-sustaining costs require allocation bases (labor hours, material value, or activity drivers).

---

## Design rules determine cost function allocation

Deciding when a component requires its own cost function versus inheriting from parent assembly follows established criteria:

**Individual cost functions required when:**
- Part represents >5-10% of parent assembly cost
- Make-vs-buy decision is active
- Multiple design variants or configurations exist
- High Idiot Index (>10:1) signals optimization opportunity
- Component is on critical supply chain path
- Price volatility or supply risk warrants tracking

**Assembly-level allocation acceptable when:**
- Low-cost standard hardware (fasteners, seals, washers)
- Stable commodity pricing
- Off-the-shelf components with minimal design control
- Floor stock items expensed rather than capitalized
- Bundled kit purchases from single supplier

AACE's estimate classification system provides maturity-based guidance: at **Class 5** (0-2% definition), use parametric methods with coarse WBS; at **Class 1** (65-100% definition), use detailed bottom-up costing with full component-level functions. SysMLv2 models can enforce this through metadata annotations indicating cost maturity class and acceptable methodology.

---

## Completeness validation ensures no cost gaps

The **100% rule** from WBS standards applies equally to cost models: every element in the system breakdown must have cost coverage, and cost rollups must sum correctly through the hierarchy. Practical validation approaches include:

**Structural validation:**
- Every BOM component has an assigned cost source (CostMethodology attribute)
- Recursive rollup sums match total assembly costs
- No orphan parts exist without cost assignment

**Coverage metrics:**
- BOM item count equals costed item count
- Zero-cost or null values flagged as exceptions
- Missing cost database entries identified

**Reconciliation checks:**
- Parametric estimates versus build-up estimates (variance <15% expected)
- Cost-per-weight reasonableness ($/kg benchmarks by technology)
- Historical actual comparison where available

In SysMLv2, completeness validation can be enforced through **constraint expressions** at the system level that verify all parts have non-null cost values and that rollup calculations are mathematically consistent. Model-level invariants can require that every part usage includes cost coverage metadata.

---

## Practical SysMLv2 cost modeling pattern recommendations

Based on this cross-domain synthesis, a robust SysMLv2 cost modeling pattern should incorporate these elements:

**Cost attribute hierarchy:**
```sysml
attribute def CostElement {
    attribute costType : CostCategory;  // Material, Labor, Overhead, Subcontract
    attribute costMethod : CostMethodology; // Parametric, Analogy, BuildUp, Judgment
    attribute costMaturity : AACEClass;  // 1-5 estimate classification
    attribute value : CostValue;
    attribute materialBasisValue : CostValue; // For commodity multiple
}
```

**Recursive rollup constraint pattern:**
```sysml
part def CostableAssembly :> CostableElement {
    part subParts : CostableElement[*];
    
    constraint costRollup {
        totalCost == directCost + sum(subParts.totalCost)
    }
    
    constraint commodityMultiple {
        idiotIndex == totalCost / materialBasisCost
    }
}
```

**Completeness validation constraint:**
```sysml
constraint def CostCoverageComplete {
    assert constraint {
        allParts->forAll(p | p.totalCost > 0 and p.costMethod <> null)
    }
}
```

**Category alignment with domain standards:**
- Aerospace: Map to MIL-STD-881 common elements and NASA EOC categories
- Energy: Map to NREL CapEx/OpEx hierarchies with fixed/variable O&M distinction
- Cross-domain: Use ABC cost hierarchy (unit/batch/product/facility) as universal structure

The resulting cost model supports extraction to BOM-like formats by traversing the parts tree and collecting CostElement attributes with their categorical typing. Commodity multiples compute automatically at any level through the materialBasisValue attributes. Completeness validation runs as model-level assertions flagging cost coverage gaps before milestone reviews.

---

## Conclusion

Hierarchical cost modeling in MBSE requires bridging formal systems modeling languages with established cost engineering practices from multiple domains. **SysMLv2's enhanced constraint and expression capabilities enable cost modeling patterns that were awkward or impossible in SysML v1.x**, particularly recursive rollups with proper typing and automated commodity multiple calculations.

The aerospace and energy sectors have evolved complementary cost structures—MIL-STD-881's product-oriented WBS and NREL's outcome-oriented LCOE framework—that inform a unified approach. Parametric tools like SEER and PRICE demonstrate that proven hierarchical rollup algorithms and cost element taxonomies translate directly to SysMLv2 constructs.

Three key design decisions will determine success: (1) adopting ABC cost hierarchy for universal categorization across domains; (2) maintaining dual cost values (manufactured and material-basis) to enable commodity multiple analysis; and (3) implementing constraint-based completeness validation that enforces cost coverage before model release. These patterns enable consistent cost rollup at any decomposition level while producing BOM-like outputs suitable for acquisition, production, and should-cost analysis workflows.