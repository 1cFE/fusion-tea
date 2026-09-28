package mfe_vacuum {
    private import ScalarValues::*;

    calc def 'Vacuum Gas Load' {
        doc /*
        Torus exhaust gas load after recombination (WI-047):

          n_molecules    = (exhaust_rate_D + exhaust_rate_T) / 2 + helium_rate   [molecules/s]
          Q_total        = n_molecules * k_B * T_gas                            [Pa m^3/s]
          S_eff_required = Q_total / p_exhaust                                  [m^3/s]

        Hydrogen isotopes leave as diatomic molecules (D2, T2 and DT each carry two
        nuclei, so the molecule count is the atom count over two, whatever the
        pairing); helium ash is atomic. The throughput is the ideal-gas pV rate at
        the stated gas temperature; the required effective speed is that throughput
        divided by the pressure at the exhaust boundary. The pressure is a boundary
        condition at a stated location -- neither the plasma pressure nor the pre-shot
        base vacuum -- and no admissible source prints it for this machine; a concept
        that declares one says so at the binding. Pump-inlet speed and effective
        speed differ by duct conductance (1/S_eff = 1/S_pump + 1/C in the molecular,
        linear-conductance case); ducts, species-dependent speeds, regeneration duty,
        puff and seeding bypass, leakage and outgassing are not modelled. Nothing
        here maps a neutron load to a target load, and neither the vessel volume nor
        the coolant pumping power stands in for the gas load.

        Flat-Real (+ - * /) -- no manual stage.

        **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
        **Ref**: lines 124-130 (species-resolved throughput after recombination,
            Q = dN k_B T, S_eff = Q / p, conductance in series; Franchetti, CERN
            Vacuum I, slides 24-27 and 43-46, as cited there; ITER vacuum-system
            scope separation)
        **Basis**: Gas conservation at the exhaust boundary; ideal-gas throughput
        */

        // deuterium and tritium atoms leaving the plasma [atoms/s]
        in attribute exhaust_rate_D_in : Real;
        in attribute exhaust_rate_T_in : Real;
        // helium ash produced [atoms/s] (one per D-T reaction)
        in attribute helium_rate_in : Real;
        // gas temperature at the exhaust boundary [K], > 0
        in attribute T_gas_in : Real;
        // pressure at the exhaust boundary [Pa], > 0
        in attribute p_exhaust_in : Real;
        // Boltzmann constant [J/K], exact SI (2019 redefinition). Declared LAST:
        // the exact route matches an unbound defaulted formal by slot, and a
        // defaulted formal declared between bound ones is mis-slotted
        // (SI_RENDERING_COLLISION at WI-047 phase 1; every landed calc keeps its
        // defaulted formals after the bound ones).
        // Boltzmann constant [J/K], exact SI (2019 redefinition)
        in attribute k_B_in : Real default 1.380649e-23;

        out attribute n_molecules : Real = (exhaust_rate_D_in + exhaust_rate_T_in) / 2.0 + helium_rate_in;
        out attribute Q_total : Real = n_molecules * k_B_in * T_gas_in;
        out attribute S_eff_required : Real = Q_total / p_exhaust_in;
    }
}
