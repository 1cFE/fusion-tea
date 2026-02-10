package E2EAttrExprDesign {
    private import ScalarValues::Real;
    private import E2EAttrExprLibrary::*;

    part e2e_plant {
        // Literal parameters (entry points)
        attribute quantity : Real = 100.0;
        attribute unit_cost : Real = 50.0;
        attribute discount_rate : Real = 0.05;
        attribute lifetime : Real = 25.0;
        attribute availability : Real = 0.90;
        attribute om_rate : Real = 20.0;

        // FORMULA: unit conversion (simple) — Pattern 1
        attribute power_mw : Real = quantity * unit_cost / 1000000.0;

        // FORMULA: chain (depends on power_mw FORMULA) — Pattern 2
        attribute power_kw : Real = power_mw * 1000.0;

        // FORMULA: O&M cost from FORMULA chain — Pattern 3
        attribute annual_om : Real = om_rate * power_kw;

        // FORMULA: area (for fan-in testing) — Pattern 4
        attribute length : Real = 10.0;
        attribute width : Real = 5.0;
        attribute height : Real = 3.0;
        attribute area : Real = length * width;

        // FORMULA: 3-term — Pattern 5
        attribute volume : Real = length * width * height;

        // Fan-in FORMULA (depends on area FORMULA + literal) — Pattern 6
        attribute cost_per_sqm : Real = 12.0;
        attribute surface_cost : Real = area * cost_per_sqm;

        // CalcUsage: binds to literal params — Pattern 7
        calc component_cost : ComponentCostCalc {
            in quantity = quantity;
            in unit_cost = unit_cost;
        }

        // EXPOSE_PURE: surface calc output — Pattern 9
        attribute total_capex : Real = component_cost.total_cost;

        // CalcUsage: financial calc with exponentiation — Pattern 8, 12
        calc financial : AnnualizedCostCalc {
            in total_capex = total_capex;
            in discount_rate = discount_rate;
            in lifetime = lifetime;
        }

        // CalcUsage: energy calc, binds to FORMULA computed attr — Pattern 10
        calc energy : EnergyCalc {
            in power_mw = power_mw;
            in availability = availability;
        }

        // CalcUsage: LCOE, binds to mix of upstream outputs + FORMULA — Pattern 11
        calc lcoe : SimpleLCOECalc {
            in annualized_capital = financial.annualized_cost;
            in annual_om = annual_om;
            in annual_energy = energy.annual_energy_mwh;
        }
    }
}
