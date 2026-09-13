package mfe_lcoe_dcf {
    private import ScalarValues::*;

    calc def 'LCOE DCF' {
        doc /*
        Generic discounted-cash-flow LCOE core [$/MWh]. Concept-agnostic: it
        takes an already-rolled-up total capital and annual O&M plus the plant
        performance and financing terms, and returns levelized cost of
        electricity. Unlike 'IFE LCOE' (which bundles IFE-specific cost
        categories), this is a clean DCF core reusable by any concept.

          CRF        = d*(1+d)^N / ((1+d)^N - 1)      (capital recovery factor)
          IDC factor = (1+d)^(Yc/2)                    (interest during
                                                        construction, midpoint)
          annual capital = total_capital * IDC * CRF
          annual energy  = 8760 * P_net * availability [MWh/yr]
          LCOE = (annual capital + annual O&M) / annual energy

        The IDC term compounds construction spend to commissioning using the
        even-spend midpoint convention (Yc/2), a standard TEA financing
        adjustment. CRF and the annual-energy denominator follow 1costingFE.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py
        **Ref**: economics.py:6-10 (compute_crf), economics.py:88-92 (compute_lcoe)
        **Basis**: Standard DCF LCOE; annuitized capital + O&M over energy sold
        */

        // Total overnight capital [$]
        in attribute total_capital_in : Real;
        // Annual O&M cost [$/yr]
        in attribute annual_om_in : Real;
        // Net electric power [MW]
        in attribute net_electric_mw : Real;
        // Capacity factor [0..1]
        in attribute availability_in : Real;
        // Discount / interest rate [1/yr]
        in attribute discount_rate_in : Real;
        // Construction period Yc [yr]
        in attribute construction_years_in : Real;
        // Operating lifetime N [yr]
        in attribute operational_years_in : Real;

        out attribute lcoe : Real;

    }
}
