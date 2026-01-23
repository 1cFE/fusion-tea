package FoundationUnits {
    doc /*
    Unit definitions and imports for fusion power plant modeling.
    Imports SI/ISQ standard units and defines custom cost units.

    **Source**: /home/reid/PyFECONS/pyfecons/units.py
    **Last Updated**: 2026-01-23
    */

    // ============================================================
    // SECTION 1: STANDARD IMPORTS
    // ============================================================

    // Scalar value types
    public import ScalarValues::Real;
    public import ScalarValues::Integer;
    public import ScalarValues::Boolean;
    public import ScalarValues::String;

    // SI base units
    public import SI::*;

    // ISQ quantity kinds
    public import ISQ::*;

    // Numerical functions for aggregation
    public import NumericalFunctions::sum;

    // ============================================================
    // SECTION 2: CUSTOM COST UNITS
    // ============================================================

    attribute def M_USD :> Real {
        doc /*
        Cost in millions of US dollars.
        Primary unit for all capital and operating costs.

        **Source**: PyFECONS units.py lines 82-86
        **Last Updated**: 2026-01-23
        */
    }

    attribute def USD_KG :> Real {
        doc /*
        Cost per unit mass in USD/kg.
        Used for material cost rates.

        **Source**: PyFECONS units.py lines 143-145
        **Last Updated**: 2026-01-23
        */
    }

    attribute def USD_M3 :> Real {
        doc /*
        Cost per unit volume in USD/m^3.
        Used for volume-based material costs.

        **Source**: PyFECONS units.py lines 138-140
        **Last Updated**: 2026-01-23
        */
    }

    attribute def USD_W :> Real {
        doc /*
        Cost per unit power in USD/W.
        Used for power supply and equipment costs.

        **Source**: PyFECONS units.py lines 118-121
        **Last Updated**: 2026-01-23
        */
    }

    // ============================================================
    // SECTION 3: DIMENSIONLESS TYPES
    // ============================================================

    attribute def Percent :> Real {
        doc /*
        Percentage value (0-100 scale).
        Used for efficiencies, availability factors.

        **Source**: PyFECONS units.py lines 65-68
        **Last Updated**: 2026-01-23
        */
    }

    attribute def Ratio :> Real {
        doc /*
        Dimensionless ratio (typically 0-1 scale).
        Used for fractions, multiplication factors.

        **Source**: PyFECONS units.py lines 72-74
        **Last Updated**: 2026-01-23
        */
    }
}
