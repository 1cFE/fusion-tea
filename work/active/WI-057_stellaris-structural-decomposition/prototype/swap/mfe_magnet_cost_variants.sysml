package mfe_magnet_cost_variants {
    private import ScalarValues::*;
    // WI-057 prototype: a formula variant for the swap demonstration (not a sourced model).
    calc def 'Magnet Structure Cost NI' {
        in n_coils : Real;
        in m_casing : Real;
        in steel_price : Real;
        in f_steel_fab : Real;
        in f_ins : Real;
        return cost : Real = n_coils * m_casing * steel_price * f_steel_fab * (1.0 + f_ins);
    }
}
