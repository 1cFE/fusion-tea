package E2EAttrExprLibrary {
    private import ScalarValues::Real;

    // Simple cost calculation (2 inputs, 5 outputs)
    calc def ComponentCostCalc {
        in attribute quantity : Real;
        in attribute unit_cost : Real;
        in attribute fab_factor : Real default := 0.45;
        in attribute install_factor : Real default := 0.30;

        out attribute material_cost : Real = quantity * unit_cost;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    // Financial calculation with exponentiation
    calc def AnnualizedCostCalc {
        in attribute total_capex : Real;
        in attribute discount_rate : Real;
        in attribute lifetime : Real;

        out attribute crf : Real =
            discount_rate * (1.0 + discount_rate) ** lifetime
            / ((1.0 + discount_rate) ** lifetime - 1.0);
        out attribute annualized_cost : Real = crf * total_capex;
    }

    // Energy calculation (simple)
    calc def EnergyCalc {
        in attribute power_mw : Real;
        in attribute availability : Real;

        out attribute annual_energy_mwh : Real = 8760.0 * power_mw * availability;
    }

    // LCOE (consumes upstream outputs)
    calc def SimpleLCOECalc {
        in attribute annualized_capital : Real;
        in attribute annual_om : Real;
        in attribute annual_energy : Real;

        out attribute lcoe : Real = (annualized_capital + annual_om) / annual_energy;
    }
}
