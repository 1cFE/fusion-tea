package hif_driver {
    private import ScalarValues::*;
    private import ife_subsystems::*;
    private import hif_economics::*;

    part def 'HIF Driver' :> 'IFE Driver' {
        doc /*
        Heavy Ion Fusion driver: induction linear accelerator.
        Source-informed operating point with computed bank energy.

        Inherits the four generic IFE driver parameters (efficiency,
        cost_per_joule, energy, lifetime_shots) from IFE Driver and
        sets them to HIF-specific values. Adds HIF-specific attributes
        (beam_energy_mj, num_chambers, pulse_rate_ref) and uses Meier's
        driver cost formula to derive cost_per_joule (gamma).

        **Source**: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
        **Ref**: Power plant operating parameters table — Osiris column
        **Basis**: Osiris HIF plant design (1.0 GWe, liquid-wall chamber,
            induction linac driver). Driver procurement retains Meier 1988 dollars; the historical
            Osiris COE is separately reported in 1992 cents/kWh.
        **Reference**: Osiris table image; Meier Eq. 5
        **Last Updated**: 2026-09-10
        */

        // === HIF-specific attributes ===

        attribute beam_energy_mj : Real {
            doc /*
            Beam energy on target per shot. This is the energy delivered
            to the fusion target, NOT the bank/stored energy. The bank
            energy (IFE Driver's 'energy' attribute) = beam_energy / efficiency.

            **Source**: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
            **Ref**: Osiris operating parameters — Driver energy: 5.0 MJ
            **Basis**: EIF-1992 Osiris design point
            */
        }

        attribute num_chambers : Real {
            doc /*
            Number of reactor chambers served by this driver.
            Single-chamber is the reference configuration.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 5 (N_c parameter)
            **Basis**: Meier 1986 — multi-chamber factor in driver cost
            */
        }

        attribute pulse_rate_ref : Real {
            doc /*
            Operating pulse repetition rate for driver cost scaling, bound
            to plant frequency by the HIF instance.
            Meier's formula uses 5 Hz as the baseline; cost increases
            by 4.4% per 5 Hz above that.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 5 (v parameter, lines 190-191)
            **Basis**: Meier 1986 — rep rate factor in driver cost
            */
        }

        // === Meier driver cost computation ===

        calc meier_cost : 'Meier HIF Driver Cost' {
            doc /*
            Computes HIF driver cost using Meier's parametric formula.
            Returns gamma ($/J of bank energy) for the Hawker LCOE model,
            and exposes cost_billions for the Meier COE chain.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 5 (lines 173-192)
            **Basis**: Meier 1986 parametric driver cost formula
            */

            in beam_energy_mj_in = beam_energy_mj;
            in driver_efficiency = efficiency;
            in num_chambers_in = num_chambers;
            in rep_rate = pulse_rate_ref;
        }

        // === Inherited interface parameters ===

        :>> efficiency = 0.28;
        :>> cost_per_joule = meier_cost.gamma;
        :>> energy = meier_cost.bank_energy_joules;
        :>> lifetime_shots = 6.0e9;

        // === Exposed intermediate for Meier COE chain ===

        attribute driver_cost_billions : Real = meier_cost.cost_billions {
            doc /*
            Driver direct capital cost in $B (1988$). Exposed for use
            in Meier's total capital cost and COE calculations.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 5
            **Basis**: Meier 1986 driver cost output
            */
        }
    }
}
