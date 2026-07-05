package hif_driver {
    private import ScalarValues::*;
    private import ife_subsystems::*;
    private import hif_economics::*;

    part def 'HIF Driver' :> 'IFE Driver' {
        doc /*
        Heavy Ion Fusion driver: induction linear accelerator.
        Osiris baseline operating point from EIF-1992.

        Inherits the four generic IFE driver parameters (efficiency,
        cost_per_joule, energy, lifetime_shots) from IFE Driver and
        sets them to HIF-specific values. Adds HIF-specific attributes
        (beam_energy_mj, num_chambers, pulse_rate_ref) and uses Meier's
        driver cost formula to derive cost_per_joule (gamma).

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
        **Ref**: Power plant operating parameters table — Osiris column
        **Basis**: Osiris HIF plant design (1.0 GWe, liquid-wall chamber,
            induction linac driver). Year-dollars: mixed (1988$/1992$).
        */

        // === HIF-specific attributes ===

        attribute beam_energy_mj : Real {
            doc /*
            Beam energy on target per shot. This is the energy delivered
            to the fusion target, NOT the bank/stored energy. The bank
            energy (IFE Driver's 'energy' attribute) = beam_energy / efficiency.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
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
            Reference pulse repetition rate for driver cost scaling.
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

            in beam_energy_mj = beam_energy_mj;
            in driver_efficiency = efficiency;
            in num_chambers = num_chambers;
            in rep_rate = pulse_rate_ref;
        }

        // === Inherited interface parameters ===

        :>> efficiency = 0.35;
        :>> cost_per_joule = meier_cost.gamma;
        :>> energy = 14.286e6;
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

    part hif_driver_instance : 'HIF Driver' {
        doc /*
        Concrete standalone instantiation of the HIF driver at the
        Osiris operating point (5.0 MJ beam, single chamber, 3.5 Hz).

        Exists so codegen template expansion emits the meier_cost
        module: codegen keys calc modules off part *usages*, and the
        redefining usage inside hif_plant (part :>> driver) is indexed
        under its inherited type 'IFE Driver', not 'HIF Driver'
        (WI-014 rider; see WI-015 findings).

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
        **Ref**: Osiris operating parameters table
        **Basis**: Same Osiris point as hif_plant's driver binding
        */

        :>> beam_energy_mj = 5.0;
        :>> num_chambers = 1.0;
        :>> pulse_rate_ref = 3.5;
    }
}
