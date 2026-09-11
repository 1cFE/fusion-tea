package hif_plant_pkg {
    private import ScalarValues::*;
    private import ife_plant::*;
    private import ife_subsystems::*;
    private import hif_driver::*;
    private import hif_economics::*;
    private import ife_lcoe::*;

    part hif_plant : 'IFE Power Plant' {
        doc /*
        HIF computed operating point using selected Osiris source inputs.

        Specializes the generic IFE power plant with Heavy Ion Fusion
        parameters from EIF-1992 (Osiris design), Meier 1986, and
        Bangerter 2013. Produces dual cost outputs:
        - Hawker LCOE (inherited from IFE Power Plant)
        - Meier COE (added as HIF-specific feature)

        **Source**: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
        **Ref**: Power plant operating parameters table — Osiris column
        **Basis**: Gain 87 is executable, so 5 MJ beam gives 435 MJ computed yield.
            Historical gain 87 and yield 432 MJ are independently rounded facts.
            Hawker and Meier share computed powers, not historical denominators.
        **Reference**: Osiris operating table image
        **Last Updated**: 2026-09-10
        */

        // === Subsystem specializations ===

        part :>> driver : 'HIF Driver' {
            doc /*
            HIF induction linac driver at Osiris operating point.
            Beam energy 5.0 MJ, single chamber; rate bound to plant frequency.
            */

            :>> beam_energy_mj = 5.0;
            :>> num_chambers = 1.0;
            :>> pulse_rate_ref = frequency;
        }

        part :>> target_factory {
            doc /*
            HIF target factory with retained $10/target scenario assumption.
            IFE targets are cryogenic indirect-drive hohlraums.

            **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
            **Ref**: Table 2 (parameter delta); Table 3 (sampled range $1-100/target)
            **Basis**: DI-003 — target cost as IFE operating cost.
                [INHERITED ESTIMATE] $10 is a selected scenario, not a
                published default. Prior choice: work/completed/20260303_WI-008_hif-concept-instantiation/design.md, subsystem diagram.
                Year-dollars: generic.
            */

            :>> cost_per_target = 10.0;
        }

        part :>> chamber {
            doc /*
            Liquid-wall reaction chamber (Osiris design). Thick molten
            FLiBe first wall at ~4 m radius, self-renewing liquid surface.
            HIF beams enter from two directions (12 beamlets total).

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Osiris chamber description (lines 599-626)
            **Basis**: EIF-1992 Osiris liquid-wall design
            */

            :>> wall_type = 'Wall Type'::liquid_wall;
            // Retained scenario assumption 1.15, not an Osiris fact or Hawker default.
            // Prior choice: work/completed/20260303_WI-008_hif-concept-instantiation/design.md, parameter table.
            // Source: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
            // Table 2 defines E_b; Table 3 samples 0.6-1.4 without selecting 1.15.
            :>> blanket_energy_multiple = 1.15;
            :>> yield_cost_constant = 5.0e6;
        }

        // === Plant-level operations parameters ===

        :>> availability = 0.90 {
            doc /*
            90% plant availability — later HIF reliability assumption, not an Osiris table fact.
            **Source**: knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md
            **Ref**: Line 672 (5 Hz, 40 years, 90% availability)
            **Basis**: Bangerter 2013 HIF reliability requirement
            */
        }

        :>> frequency = 4.6 {
            doc /*
            4.6 Hz pulse repetition rate (Osiris design point).
            **Source**: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
            **Ref**: Osiris operating parameters — Pulse rate: 4.6 Hz
            **Basis**: EIF-1992 Osiris design
            */
        }

        :>> gain = 87.0 {
            doc /*
            Printed gain 87 is the executable input. With 5 MJ beam this yields
            435 MJ; the independently rounded historical yield is 432 MJ.

            **Source**: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
            **Ref**: Osiris operating parameters — Gain: 87
            **Basis**: EIF-1992 Osiris indirect-drive HIF target
            */
        }

        :>> thermal_efficiency = 0.45 {
            doc /*
            Thermal-to-electric conversion efficiency.
            **Source**: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
            **Ref**: Osiris operating parameters — Thermal efficiency: 45%
            **Basis**: EIF-1992 Osiris steam cycle
            */
        }

        // === Plant-level financial parameters ===

        :>> discount_rate = 0.08 {
            doc /*
            Retained 8% discount-rate scenario for Hawker DCF.
            Meier's separate 8.3% fixed charge rate is unchanged.

            **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
            **Ref**: Table 2 (parameter d); Table 3 (sampled discount range 2-12%)
            **Basis**: [INHERITED ESTIMATE] Selected 8%, not a published default.
                Prior choice: work/completed/20260303_WI-008_hif-concept-instantiation/design.md, parameter table.
                Year-dollars: generic.
            */
        }

        :>> plant_cost_constant = 2000.0 {
            doc /*
            Balance-of-plant capital coefficient retained at $2000/kWe.
            This prior modeling estimate mapped Meier reactor cost to Hawker
            alpha. Its historical derivation used erroneous 2.054 GWt and held
            1.0 GWe, then added an estimated BOP allowance. Those are neither
            the image-verified 2.504 GWt nor the current computed power basis.
            The coefficient is retained without recalibration in this repair.

            **Source**: work/completed/20260303_WI-008_hif-concept-instantiation/design.md
            **Ref**: DD-WI008-5; parameter table; Meier validation at 2.054 GWt
            **Basis**: [INHERITED ESTIMATE] Prior approximate mapping, not a
                source-derived coefficient for the corrected case. Year-dollars: 1988$.
            */
        }

        :>> om_cost_constant = 65.0 {
            doc /*
            Annual O&M coefficient retained at $65/kWe-year.
            The prior estimate used 3% of approximately $3.3B at held 1 GWe
            (about $99/kWe-year), then reduced it for assumed Hawker scope
            overlap. That historical estimate is not recomputed from the
            corrected operating point; the scope adjustment remains an assumption.

            **Source**: work/completed/20260303_WI-008_hif-concept-instantiation/design.md;
                knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Prior DD-WI008-5 and parameter table; Meier Eq. 1 discussion (M = 3% of C_T)
            **Basis**: [INHERITED ESTIMATE] Prior O&M mapping retained.
                Year-dollars: 1988$.
            */
        }

        // === HIF-specific: Meier COE chain ===

        // Hawker Eqs. 2.12-2.16: common computed powers for both price channels.
        // These are not the historical Osiris thermal/net values retained below.
        attribute thermal_power_gw : Real = lcoe_calc.thermal_power_gw;
        attribute net_electric_power_gw : Real = lcoe_calc.net_electric_power_gw;
        // Meier Eqs. 2-3: one reactor unit; reference factory direct cost [$B, 1988$].
        attribute reactor_units : Real = 1.0;
        attribute target_factory_direct_cost_billions : Real = 0.1;

        calc meier_reactor_cost_calc : 'Meier Reactor Cost' {
            doc /*
            Meier's reactor cost at computed thermal power, single unit.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 3
            **Basis**: Meier 1986 reactor cost scaling
            */

            in thermal_power_gw_in = thermal_power_gw;
            in num_units = reactor_units;
        }

        calc meier_capital_calc : 'Meier Total Capital Cost' {
            doc /*
            Meier's total capital cost with 1.83x indirect multiplier.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 2
            **Basis**: Meier 1986 capital cost structure
            */

            in reactor_cost = meier_reactor_cost_calc.reactor_cost_billions;
            in driver_cost = driver.driver_cost_billions;
            // C_tfd = $0.1B target factory direct cost (Meier 1986 reference, 1988$)
            in target_factory_cost = target_factory_direct_cost_billions;
        }

        calc meier_coe_calc : 'Meier COE' {
            doc /*
            Meier's Cost of Electricity for the HIF plant.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 1
            **Basis**: Meier 1986 COE formula
            */

            in total_capital_billions = meier_capital_calc.total_capital_billions;
            in availability_in = availability;
            in net_electric_power_gw_in = net_electric_power_gw;
        }

        // === Exposed cost outputs ===

        // lcoe is inherited from IFE Power Plant
        // recirculating_fraction is inherited from IFE Power Plant
        // viability constraint is inherited from IFE Power Plant

        calc meier_price : 'Generating Electricity Price' {
            in numerator = meier_coe_calc.annualized_cost;
            in denominator = meier_coe_calc.energy_denominator;
            in net_power = net_electric_power;
        }
        attribute meier_coe : Real = meier_price.price {
            doc /*
            Meier COE in 1988 cents/kWh. Uses computed net power and 0.90 availability,
            8.3% fixed charge plus 3% O&M and 1.83 capital multiplier.
            Require meier_price.generating=1 and satisfied net_positive before use.
            Hawker uses its separate DCF and mixed inherited dollar conventions.
            */
        }
        // Historical Osiris reference facts, not executable constraints or price inputs.
        // Source: knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png
        // Reference: Osiris column, visually verified 2026-09-10. Units are in names.
        // The later 1.15 blanket multiplier, 0.90 availability and equal driver/cooling
        // assumption produce different computed powers and are not table transcriptions.
        attribute osiris_reference_beam_energy_mj : Real = 5.0;
        attribute osiris_reference_gain : Real = 87.0;
        attribute osiris_reference_yield_mj : Real = 432.0;
        attribute osiris_reference_frequency_hz : Real = 4.6;
        attribute osiris_reference_driver_efficiency_percent : Real = 28.0;
        attribute osiris_reference_fusion_power_mw : Real = 1987.0;
        attribute osiris_reference_thermal_power_mw : Real = 2504.0;
        attribute osiris_reference_thermal_efficiency_percent : Real = 45.0;
        attribute osiris_reference_gross_electric_power_mw : Real = 1127.0;
        attribute osiris_reference_driver_electric_power_mw : Real = 82.0;
        attribute osiris_reference_auxiliary_electric_power_mw : Real = 45.0;
        attribute osiris_reference_net_electric_power_mw : Real = 1000.0;
        attribute osiris_reference_coe_1992_cents_kwh : Real = 5.6;
    }
}
