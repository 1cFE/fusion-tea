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

        in attribute total_capital : Real;      // Total overnight capital [$]
        in attribute annual_om : Real;          // Annual O&M cost [$/yr]
        in attribute net_electric_mw : Real;    // Net electric power [MW]
        in attribute availability : Real;       // Capacity factor [0..1]
        in attribute discount_rate : Real;      // Discount / interest rate [1/yr]
        in attribute construction_years : Real; // Construction period Yc [yr]
        in attribute operational_years : Real;  // Operating lifetime N [yr]

        // (1+d)^N, reused in the CRF numerator and denominator.
        // Source: economics.py:10.
        attribute discount_pow_n : Real =
            (1.0 + discount_rate) ** operational_years;

        // Capital recovery factor. Source: economics.py:6-10.
        attribute crf : Real =
            discount_rate * discount_pow_n / (discount_pow_n - 1.0);

        // Interest during construction (even-spend midpoint). 2.0 = midpoint of
        // an evenly spread construction spend.
        attribute idc_factor : Real =
            (1.0 + discount_rate) ** (construction_years / 2.0);

        // Annualized capital charge.
        attribute annual_capital : Real =
            total_capital * idc_factor * crf;

        // Annual energy sold [MWh/yr]. 8760.0 = hours/year. Source: economics.py:90.
        attribute annual_energy_mwh : Real =
            8760.0 * net_electric_mw * availability;

        // Levelized cost of electricity [$/MWh]. Source: economics.py:88-92.
        out attribute lcoe : Real =
            (annual_capital + annual_om) / annual_energy_mwh;
    }
}
