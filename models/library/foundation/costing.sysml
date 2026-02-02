package Costing {
    doc /*
    Cost modeling foundation for fusion power plant techno-economic analysis.
    Defines the 'Costed Component' interface that all cost-bearing parts must specialize.

    **Source**: Validated by Coffee Maker demo model (models/tests/coffee_maker/)
    **Reference**: modeling_pm/docs/COST_MODELING.md
    **Last Updated**: 2026-01-26
    */

    // Required for numeric types
    private import ScalarValues::Real;

    // Required for cost aggregation over multiplicities (re-exported for consumers)
    private import NumericalFunctions::sum;

    // ============================================================
    // SECTION 1: CAS CATEGORY ENUMERATION
    // ============================================================

    enum def CASCategory {
        doc /*
        Cost Account Structure (CAS) categories for fusion plant costing.
        Hierarchical taxonomy from PyFECONS costing framework.

        Level 1: CAS10-90 (top-level accounts)
        Level 2: CAS21-29 (direct cost subcategories)
        Level 3: CAS220101-220119 (reactor equipment details)

        Note: Some CAS codes have reactor-type-specific meanings:
        - CAS220103: Magnets/Coils (MFE) or Lasers (IFE)
        - CAS220104: Supplementary Heating (MFE) or Ignition (IFE)
        - CAS220108: Divertor (MFE) or Target Factory (IFE)

        **Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/categories/
        **Reference**: modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md
        **Last Updated**: 2026-01-26
        */

        // Level 1 - Top-Level Accounts
        CAS10;  // Pre-Construction Costs
        CAS20;  // Direct Costs (aggregates CAS21-29)
        CAS30;  // Capitalized Indirect Service Costs
        CAS40;  // Capitalized Owner Costs
        CAS50;  // Capitalized Supplementary Costs
        CAS60;  // Capitalized Financial Costs
        CAS70;  // Annualized O&M Costs
        CAS80;  // Annualized Fuel Costs
        CAS90;  // Annualized Financial Costs

        // Level 2 - Direct Cost Subcategories (under CAS20)
        CAS21;  // Buildings and Structures
        CAS22;  // Reactor Plant Equipment (aggregates CAS2201-2207)
        CAS23;  // Turbine Plant Equipment
        CAS24;  // Electric Plant Equipment
        CAS25;  // Miscellaneous Plant Equipment
        CAS26;  // Heat Rejection System
        CAS27;  // Special Materials
        CAS28;  // Digital Twin
        CAS29;  // Contingency (Direct)

        // Level 3 - Reactor Equipment Details (under CAS22)
        CAS220101;  // Reactor Equipment (First Wall and Blanket)
        CAS220102;  // Radiation Shield
        CAS220103;  // Magnets/Coils (MFE) or Lasers (IFE)
        CAS220104;  // Supplementary Heating (MFE) or Ignition (IFE)
        CAS220105;  // Primary Structure and Support
        CAS220106;  // Vacuum System
        CAS220107;  // Power Supplies
        CAS220108;  // Divertor (MFE) or Target Factory (IFE)
        CAS220109;  // Direct Energy Converter
        CAS220111;  // Assembly and Installation
        CAS220119;  // Scheduled Replacement Cost

        // Level 3 - Reactor Auxiliary Systems (under CAS22)
        CAS2202;    // Main and Secondary Coolant
        CAS2203;    // Auxiliary Cooling
        CAS2204;    // Radioactive Waste Treatment
        CAS2205;    // Fuel Handling and Storage
        CAS2206;    // Other Reactor Plant Equipment
        CAS2207;    // Instrumentation and Control
    }

    // ============================================================
    // SECTION 2: COSTED COMPONENT INTERFACE
    // ============================================================

    abstract part def 'Costed Component' {
        doc /*
        Abstract interface for all cost-bearing components.
        Every costed part must specialize this and provide values for cost attributes.

        Usage Pattern (Leaf Parts):
        1. Specialize this interface
        2. Assign cas_category to appropriate CAS code
        3. Create embedded cost_model calc usage
        4. Bind all cost attributes via redefinition (:>>)

        Usage Pattern (Assembly Parts):
        1. Specialize this interface
        2. Assign cas_category to appropriate CAS code
        3. Aggregate child costs using sum() for arrays
        4. Compute idiot_index as capital_cost / raw_material_cost

        **Pattern**: Validated by Coffee Maker demo model
        **Source**: modeling_pm/docs/COST_MODELING.md
        **Reference**: models/tests/coffee_maker/library.sysml:19-37
        **Last Updated**: 2026-01-26
        */

        // CAS category for cost reporting and grouping
        attribute cas_category : CASCategory;

        // Required cost attributes (multi-category breakdown)
        attribute capital_cost : Real;          // Total cost for LCOE calculation
        attribute raw_material_cost : Real;     // Material portion for cost driver analysis
        attribute fabrication_cost : Real;      // Manufacturing labor/overhead
        attribute installation_cost : Real;     // On-site assembly and integration

        // Derived efficiency metric (SpaceX "idiot index")
        // Typical values: 2-4 for complex systems, >5 suggests cost reduction opportunity
        attribute idiot_index : Real;           // capital_cost / raw_material_cost
    }
}
