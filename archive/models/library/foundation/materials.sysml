package FoundationMaterials {
    doc /*
    Material definitions for fusion power plant components.
    Each material has physical properties needed for mass and cost calculations.

    Properties at reference conditions (typically 20-25C, 1 atm).
    Temperature-dependent properties may be added in future versions.

    **Source**: Engineering references, ITER documentation
    **Last Updated**: 2026-01-23
    */

    private import ScalarValues::Real;

    // ============================================================
    // SECTION 1: FIRST WALL MATERIALS
    // ============================================================

    part def 'Tungsten' {
        doc /*
        Pure tungsten for plasma-facing components.
        High melting point, excellent thermal conductivity, high density.

        **Source**: Engineering Toolbox, ITER documentation
        **Reference**: https://www.iter.org/machine/blanket
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 19300.0;
        attribute thermal_conductivity : Real = 173.0;
        attribute unit_cost : Real = 50.0;
    }

    part def 'Beryllium' {
        doc /*
        Beryllium for neutron multiplication and first wall.
        Low density, high thermal conductivity, good neutron properties.

        **Source**: BeST (Beryllium Science and Technology Association)
        **Reference**: https://www.beryllium.eu/properties-of-beryllium
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 1840.0;
        attribute thermal_conductivity : Real = 216.0;
        attribute unit_cost : Real = 500.0;
    }

    part def 'Liquid Lithium' {
        doc /*
        Liquid lithium for flowing first wall concepts.
        Excellent thermal properties, tritium breeding capability.
        Density at 300C operating temperature.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 512.0;
        attribute thermal_conductivity : Real = 46.0;
        attribute unit_cost : Real = 150.0;
    }

    part def 'FLiBe Salt' {
        doc /*
        Lithium fluoride - beryllium fluoride molten salt (2LiF-BeF2).
        Used as coolant and tritium breeder.
        Density at 500C operating temperature.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 1940.0;
        attribute thermal_conductivity : Real = 1.0;
        attribute unit_cost : Real = 200.0;
    }

    // ============================================================
    // SECTION 2: STRUCTURAL MATERIALS
    // ============================================================

    part def 'Stainless Steel 316' {
        doc /*
        Austenitic stainless steel 316L for structural components.
        Standard nuclear-grade structural material.

        **Source**: ASM MatWeb, AZoM
        **Reference**: https://www.azom.com/properties.aspx?ArticleID=863
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 8000.0;
        attribute thermal_conductivity : Real = 16.3;
        attribute unit_cost : Real = 5.0;
    }

    part def 'Ferritic Martensitic Steel' {
        doc /*
        Reduced-activation ferritic/martensitic steel (RAFM).
        Examples: EUROFER97, F82H, CLAM.
        Preferred structural material for high-fluence applications.

        **Source**: ITER documentation, fusion materials literature
        **Reference**: https://www.nuclear-power.com
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 7800.0;
        attribute thermal_conductivity : Real = 26.0;
        attribute unit_cost : Real = 8.0;
    }

    part def 'ODS Steel' {
        doc /*
        Oxide Dispersion Strengthened steel.
        Enhanced high-temperature creep resistance.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 7900.0;
        attribute thermal_conductivity : Real = 20.0;
        attribute unit_cost : Real = 25.0;
    }

    part def 'Vanadium Alloy' {
        doc /*
        Vanadium alloy (V-4Cr-4Ti) for advanced blanket structures.
        Low activation, high thermal conductivity.

        **Source**: AZoM, fusion materials literature
        **Reference**: https://www.azom.com/article.aspx?ArticleID=7643
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 6100.0;
        attribute thermal_conductivity : Real = 30.7;
        attribute unit_cost : Real = 100.0;
    }

    // ============================================================
    // SECTION 3: COOLANT MATERIALS
    // ============================================================

    part def 'Lead Lithium' {
        doc /*
        Lead-lithium eutectic (Pb-17Li) for blanket coolant/breeder.
        High density liquid metal with good breeding properties.
        Density at 350C operating temperature.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 9400.0;
        attribute thermal_conductivity : Real = 15.0;
        attribute unit_cost : Real = 10.0;
    }

    part def 'Helium Coolant' {
        doc /*
        Helium gas coolant at typical blanket conditions.
        Inert, high-temperature capable, no activation.
        Density varies significantly with pressure and temperature.

        **Source**: Standard gas properties
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 0.16;
        attribute thermal_conductivity : Real = 0.15;
        attribute unit_cost : Real = 20.0;
    }

    part def 'Water Coolant' {
        doc /*
        Pressurized water coolant.
        Standard PWR-type cooling at ambient conditions.

        **Source**: Standard water properties
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 1000.0;
        attribute thermal_conductivity : Real = 0.6;
        attribute unit_cost : Real = 0.01;
    }

    // ============================================================
    // SECTION 4: MAGNET MATERIALS
    // ============================================================

    part def 'REBCO Superconductor' {
        doc /*
        Rare-earth barium copper oxide (REBCO) high-temperature superconductor.
        Used in HTS magnet coils.
        Thermal conductivity at cryogenic temperatures (77K).

        **Source**: Superconductor manufacturer data
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 6300.0;
        attribute thermal_conductivity : Real = 3.0;
        attribute unit_cost : Real = 1000.0;
    }
}
