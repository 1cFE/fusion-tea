# Domain Knowledge

Curated domain insights that have passed through the research approval gate or been captured inline during modeling work. Each entry is a structured record of something we know about the domain that affects how we model it.

This file is the actionable feed for modeling work. Raw research lives in `knowledge/research/`; only approved, structured insights belong here.

---

### DI-001: CAS Hierarchy and Cost Account Structure
- **Source**: 20260105-103000_catf-mfe-architecture.md, 20260106-050051_cost-modeling-lcoe-strategy.md, 20260123-pyfecons-library-mapping-strategy.md
- **Context**: PyFECONS implements the ARPA-E standard Cost Account Structure with 37 categories (CAS10–LCOE). The hierarchy flows CAS10 (Pre-construction) → CAS20 (Direct) → CAS21–29 (subsystems) → CAS30–60 (Indirect/Financial) → CAS70–90 (Annualized) → LCOE. CAS22 (Reactor Plant Equipment) represents ~60% of total cost and drives design decisions.
- **Model implications**: Each CAS category should have a corresponding calc def or part def with an explicit `cas_category` attribute. The cost rollup must mirror the CAS hierarchy for direct validation against PyFECONS.
- **Analysis implications**: Enables per-category cost breakdown and direct comparison between reactor concepts using the same CAS structure.
- **Status**: addressed

### DI-002: Power Balance as Acyclic Calculation Foundation
- **Source**: 20260105-103000_catf-mfe-architecture.md, 20260106-050051_cost-modeling-lcoe-strategy.md
- **Context**: The calculation flow is strictly acyclic: PowerBalance → Geometry → Subsystem Costs → Totals → Annualized → LCOE. The power table outputs (p_alpha, p_neutron, p_net, q_eng) drive all downstream costs and provide the LCOE denominator. CATF baseline: p_nrl=2600 MW, eta_th=0.46, plant_availability=0.85.
- **Model implications**: Power balance calc defs must be completed and validated before cost calculations can be implemented. The acyclic dependency chain determines implementation order.
- **Analysis implications**: p_net accuracy directly affects LCOE accuracy; power balance validation against PyFECONS is the first critical verification gate.
- **Status**: addressed

### DI-003: Costed Component Interface Pattern
- **Source**: 20260110-strategic-cost-patterns.md, 20260107-final-cost-architecture.md, 20260123-pyfecons-library-mapping-strategy.md
- **Context**: Every cost-bearing part must specialize `abstract part def 'Costed Component'` with required attributes: capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index (capital/raw_material ratio). Cost rollup uses `NumericalFunctions::sum` for assemblies.
- **Model implications**: All costed parts must implement this interface. Leaf parts use direct calc defs; assembly parts aggregate child costs via sum(). Allocation costs (<5%) for minor items must have documented basis.
- **Analysis implications**: Uniform interface enables automated cost rollup, idiot index tracking, and cross-concept comparison.
- **Status**: captured

### DI-004: Multiplicity Cost Rollup via NumericalFunctions::sum
- **Source**: 20260112-055807_multiplicity-cost-rollup-gap.md, 20260112-061548_sysmlv2-discovery-reflection.md
- **Context**: `NumericalFunctions::sum` works correctly with multiplicity: `sum(tf_coils[12].capital_cost)` handles arrays of any size. This was resolved after five contradictory research reports — none had validated with actual testing until the coffee maker demo.
- **Model implications**: Use `private import NumericalFunctions::sum;` and sum() with array notation for cost rollup of multiplied parts. Source: `/syside/sysml.library/Kernel Libraries/Kernel Function Library/NumericalFunctions.kerml`.
- **Analysis implications**: No workaround needed for multiplicity in cost aggregation; standard library function is sufficient.
- **Status**: addressed

### DI-005: Redefines Semantics and Type Inheritance
- **Source**: 20260116-170015_sysmlv2-redefines-semantics-visualization.md
- **Context**: `part redefines child { ... }` correctly inherits type information through KerML subsetting specification. Types are derived (not stored), computed from ownedTyping UNION ownedRedefinition.redefinedFeature.type. Tom Sawyer visualization does not display inherited types, but this is a display limitation — semantics and code generation are correct.
- **Model implications**: Use redefines for parameterization as it is semantically correct. Do not add explicit types solely to fix visualization. Accept the Tom Sawyer display limitation.
- **Analysis implications**: Redefines-based specialization works end-to-end for sysml-codegen; no impact on generated code.
- **Status**: addressed

### DI-006: LCOE Visibility and Missing OpEx Components
- **Source**: 20260126-lcoe-visibility-requirements-analysis.md, 20260106-050051_cost-modeling-lcoe-strategy.md
- **Context**: LCOE = [C900000 + (C700000 + C800000) × (1+inflation)^lifetime] / [8760 × p_net × availability]. Currently missing: CAS70 (Annualized O&M, ~$60/kW-year default), CAS80 (Annualized Fuel/tritium cost), CAS90 (Annualized Financial = capital_recovery_factor × total_capital), and operating parameters (plant_lifetime, plant_availability, yearly_inflation). LCOE should decompose into capital, O&M, and fuel fractions.
- **Model implications**: Plan calc defs for CAS70, CAS80, and CAS90 categories. Define operating parameters at the plant level. Structure LCOE calc to expose three fractions separately.
- **Analysis implications**: Full LCOE cannot be computed until OpEx categories are modeled. Current CapEx visibility is strong; OpEx is the gap.
- **Status**: captured

### DI-007: PyFECONS Library Mapping and Component Reuse
- **Source**: 20260123-pyfecons-library-mapping-strategy.md
- **Context**: PyFECONS has ~70 shared modules (60%) vs 48 design-specific (30% MFE + IFE). Recommended library structure: foundation/ (types, units, materials, costing interface), definitions/ (plant, power_core, magnets/lasers, heating/exhaust, power_conversion, bop), calculations/ (power_balance, geometry, costing, lcoe), materials/ (HTS, structural, coolants). Base definitions specialize per reactor type (e.g., 'Heating System' → NBI/ICRF for MFE, Lasers for IFE).
- **Model implications**: Library package structure should mirror the recommended layout. Each CAS category maps to one calc def with 5–20 outputs. Implementation phases: Foundation → Core Components → CATF Design → Cost Calculations → Multi-Concept.
- **Analysis implications**: ~60% code reuse across reactor concepts enables rapid multi-concept comparison once library is established.
- **Status**: captured

### DI-008: Idiot Index for Manufacturing Efficiency Tracking
- **Source**: 20260110-strategic-cost-patterns.md, 20260110-mbse-cost-modeling-best-practices.md, heirarchical-cost-modeling-mbse-patterns.md
- **Context**: Idiot Index = Finished Cost / Raw Material Cost. SpaceX threshold: 10:1 flags components for investigation. Typical fusion values: Magnets 2.5–3.5, Blanket 3.0–4.0, Divertor 3.5–4.5.
- **Model implications**: Auto-compute `idiot_index = capital_cost / raw_material_cost` on all 'Costed Component' parts. High indices indicate design simplification or supplier negotiation opportunities.
- **Analysis implications**: Enables comparative manufacturing efficiency analysis across design variants. Visible in cost breakdown reports.
- **Status**: captured

### DI-009: SysMLv2 Conditional Expression Syntax
- **Source**: 20260105-172101_sysmlv2-conditional-expressions.md
- **Context**: Correct syntax is `if CONDITION? TRUE_VALUE else FALSE_VALUE`. Chained conditionals and enum comparisons work. Wrong syntax: no "then"/"endif", no C-style ternary `x ? y : z`.
- **Model implications**: PowerBalanceCalc can use conditionals for fuel-type-dependent alpha fraction instead of type specialization. Use conditionals for simple selection; reserve type specialization for complex variant behavior.
- **Analysis implications**: Eliminates need for separate calc defs per fuel type for simple parametric differences.
- **Status**: addressed

### DI-010: Reactor Type Taxonomy (MFE, IFE, MIF)
- **Source**: 20260123-pyfecons-library-mapping-strategy.md, 20260105-103000_catf-mfe-architecture.md
- **Context**: Three top-level reactor types: MFE (Magnetic Fusion Energy, fully implemented in PyFECONS), IFE (Inertial Fusion Energy, fully implemented), MIF (Magneto-Inertial, placeholder). MFE confinement types include Spherical Tokamak, Magnetic Mirror, Stellarator, etc. IFE includes Laser-Driven Direct Drive, Indirect drive, etc. Fuel types: DT, DD, DHe3, PB11.
- **Model implications**: Define enums for ReactorType, ConfinementType, FuelType. Each reactor type gets a separate designs/ subdirectory. Shared components in library/; type-specific assemblies in designs/.
- **Analysis implications**: Multi-concept comparison requires consistent CAS structure across reactor types, enabled by shared library definitions.
- **Status**: addressed

### DI-011: Industry Cost Estimation Standards (AACE, MIL-STD-881)
- **Source**: 20260110-mbse-cost-modeling-best-practices.md, heirarchical-cost-modeling-mbse-patterns.md
- **Context**: AACE estimate classification: Class 5 (±30–50%) through Class 1 (±3–10%). Fusion estimates are typically Class 4 (parametric, ±20–35%). Magnets: Class 4 from ITER/SPARC data. Blanket: Class 4–5 (novel). Buildings: Class 3 (good precedent).
- **Model implications**: Track estimation_method, aace_class, and data_source metadata on cost line items. Report confidence ranges per AACE accuracy bands.
- **Analysis implications**: Uncertainty quantification via AACE class enables P10/P50/P90 distributions for LCOE.
- **Status**: captured

### DI-012: Three-Layer Design-Time Cost Validation
- **Source**: 20260110-strategic-cost-patterns.md
- **Context**: Validation pipeline: Layer 1 = model structure rules (agentic-mbse validate), Layer 2 = SysML constraint defs (PositiveCost, ReasonableIdiotIndex 1.0–20.0, MaterialFractionBounds 20–80%), Layer 3 = runtime post-execution validators. Runtime bounds: overnight $/kW 3,000–15,000, LCOE 30–200 $/MWh, CAS22 fraction 30–70%.
- **Model implications**: Implement constraint defs for Layer 2 validation. Design models so that cost outputs are checkable at each layer.
- **Analysis implications**: Systematic bounds checking catches errors early. Runtime validation catches integration issues.
- **Status**: captured

### DI-013: Standard Cost Output Schema for Cross-Concept Comparison
- **Source**: 20260106-050051_cost-modeling-lcoe-strategy.md, 20260110-strategic-cost-patterns.md
- **Context**: All designs must expose 30+ standardized outputs: capital costs by CAS category, component breakdown, efficiency metrics (overnight $/kW, idiot indices), LCOE decomposition (total, capital fraction, O&M fraction, fuel fraction), and annual energy production.
- **Model implications**: Define a StandardCostOutputs calc def or interface that all designs implement. sysml-codegen generates Pydantic models from these multi-output calc defs.
- **Analysis implications**: Enables direct JSON-level comparison across reactor concepts. Visualization via stacked bars for CAS breakdown, Sankey for cost flow.
- **Status**: captured

### DI-014: Estimation Metadata and Data Source Traceability
- **Source**: 20260110-strategic-cost-patterns.md, 20260110-mbse-cost-modeling-best-practices.md
- **Context**: Every cost item should track: estimation_method (parametric, analogous, engineering, expert, vendor, actual), aace_class (1–5), data_source (e.g., "PyFECONS CAS220103"), basis_of_estimate (link to justification). Multi-category breakdown: material, fabrication, installation, assembly overhead.
- **Model implications**: Attach metadata attributes to cost calc defs or use doc comments with structured Source/Reference fields. Git history plus metadata provides full cost rationale chain.
- **Analysis implications**: Enables systematic uncertainty tracking and audit trail for regulatory or investor review.
- **Status**: captured
