package wi029_lcoe_construction {
    private import ScalarValues::*;

    // CAS71 / CAS80 shared levelization wrapper (economics.py:13-50).
    // Growing-annuity PV of a real annual stream, annuitized by CRF.
    // Flat-Real: + - * / ** only -> Rung A (codegen).
    calc def 'Levelized Annual Cost' {
        in attribute annual_cost : Real;        // raw annual stream [$/yr]
        in attribute interest_rate : Real;      // i
        in attribute inflation_rate : Real;     // g (escalation)
        in attribute operational_years : Real;  // n
        in attribute project_time : Real;       // Tc (NOAK: construction_time)

        // CRF(i,n). Source economics.py:6-10.
        attribute disc_pow_n : Real = (1.0 + interest_rate) ** operational_years;
        attribute crf : Real = interest_rate * disc_pow_n / (disc_pow_n - 1.0);

        // A1 = escalated first-operating-year cost. economics.py:40.
        attribute a1 : Real = annual_cost * (1.0 + inflation_rate) ** project_time;

        // Growing-annuity present value. economics.py:44-46.
        attribute pv : Real =
            a1 * (1.0 - ((1.0 + inflation_rate) / (1.0 + interest_rate)) ** operational_years)
            / (interest_rate - inflation_rate);

        out attribute levelized : Real = crf * pv;
    }

    // CAS80 raw annual fuel (DT branch, costs.py:476-544). Flat-Real -> Rung A.
    calc def 'DT Fuel Cost' {
        in attribute p_fus : Real;              // fusion power [MW]
        in attribute n_mod : Real default 1.0;
        in attribute availability : Real;
        in attribute cost_per_rxn : Real;       // M_D*u_D + M_Li6*u_Li6 [$/rxn]
        in attribute q_eff : Real;              // Q_DT [MeV/rxn]
        in attribute mev_to_joules : Real;      // MEV_TO_JOULES
        in attribute burn_fraction : Real;
        in attribute fuel_recovery : Real;

        // reactions/yr * $/rxn -> annual fuel [$/yr]. costs.py:~500.
        attribute annual_raw : Real =
            n_mod * p_fus * (3600.0 * 8760.0) * availability * cost_per_rxn
            / (q_eff * mev_to_joules);

        // burn-up recovery correction. costs.py:~520.
        attribute burn_correction : Real =
            1.0 + (1.0 - burn_fraction) / burn_fraction * (1.0 - fuel_recovery);

        out attribute annual_fuel : Real = annual_raw * burn_correction;
    }
}
