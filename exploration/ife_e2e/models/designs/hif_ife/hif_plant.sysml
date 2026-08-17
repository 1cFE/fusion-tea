package hif_plant_pkg {
    private import ScalarValues::*;
    private import ife_plant::*;
    private import ife_subsystems::*;
    private import hif_driver::*;
    private import hif_economics::*;

    part hif_plant : 'IFE Power Plant' {
        doc /*
        HIF power plant — Osiris baseline instantiation.

        Specializes the generic IFE power plant with Heavy Ion Fusion
        parameters from EIF-1992 (Osiris design), Meier 1986, and
        Bangerter 2013. Produces dual cost outputs:
        - Hawker LCOE (inherited from IFE Power Plant)
        - Meier COE (added as HIF-specific feature)

        **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
        **Ref**: Power plant operating parameters table — Osiris column
        **Basis**: Osiris 1.0 GWe HIF plant with liquid-wall chamber
        */

        // === Subsystem specializations ===

        part :>> driver : 'HIF Driver' {
            doc /*
            HIF induction linac driver at Osiris operating point.
            Beam energy 5.0 MJ, single chamber, 3.5 Hz.
            */

            :>> beam_energy_mj = 5.0;
            :>> num_chambers = 1.0;
            :>> pulse_rate_ref = 3.5;
        }

        part :>> target_factory {
            doc /*
            HIF target factory. Per-target cost from EIF-1992 era
            estimates. IFE targets are cryogenic indirect-drive hohlraums.

            **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
            **Ref**: Table 1 (parameter delta, range $1-100)
            **Basis**: DI-003 — target cost as IFE operating cost.
                Hawker default $10 used; HIF-specific target cost data
                is sparse. Year-dollars: generic.
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
            :>> blanket_energy_multiple = 1.15;
            :>> yield_cost_constant = 5.0e6;
        }

        // === Plant-level operations parameters ===

        :>> availability = 0.90 {
            doc /*
            90% plant availability — HIF reliability target.
            **Source**: knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md
            **Ref**: Line 672 (5 Hz, 40 years, 90% availability)
            **Basis**: Bangerter 2013 HIF reliability requirement
            */
        }

        :>> frequency = 3.5 {
            doc /*
            3.5 Hz pulse repetition rate (Osiris design point).
            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Osiris operating parameters — Pulse rate: 3.5 Hz
            **Basis**: EIF-1992 Osiris design
            */
        }

        :>> gain = 80.0 {
            doc /*
            Target gain = yield / beam energy (physics convention).
            Osiris: 412 MJ yield / 5.0 MJ beam ≈ 82, rounded to 80.
            Consistent with Bangerter Table 1 Hybrid target (G=60)
            and Close-Coupled target (G=130) range.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Osiris operating parameters — Gain: 80
            **Basis**: EIF-1992 Osiris indirect-drive HIF target
            */
        }

        :>> thermal_efficiency = 0.43 {
            doc /*
            Thermal-to-electric conversion efficiency.
            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Osiris operating parameters — Thermal efficiency: 43%
            **Basis**: EIF-1992 Osiris steam cycle
            */
        }

        // === Plant-level financial parameters ===

        :>> discount_rate = 0.08 {
            doc /*
            Discount rate — financial parameter, not concept-specific.
            Matches Hawker's default. Meier uses 8.3% fixed charge rate
            which is comparable.

            **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
            **Ref**: Table 1 (parameter d, default 0.08)
            **Basis**: Hawker 2020 default. Year-dollars: generic.
            */
        }

        :>> plant_cost_constant = 2000.0 {
            doc /*
            Balance-of-plant capital cost per kWe. Derived from Meier's
            reactor cost: C_rd ≈ $0.73B at 2.054 GWt, with 1.83x indirect
            multiplier = $1.34B for 1.0 GWe → $1340/kWe. Rounded up to
            $2000/kWe to account for BOP elements beyond Meier's C_rd.
            Within Hawker's range ($1000-6000/kWe).

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eqs. 2-3 (reactor cost structure)
            **Basis**: [ESTIMATED] Approximate mapping of Meier reactor
                cost to Hawker alpha. Year-dollars: 1988$.
            */
        }

        :>> om_cost_constant = 65.0 {
            doc /*
            Annual O&M cost per kWe capacity. Meier uses 3% of total
            capital for O&M: 0.03 × ~$3.3B / 1e6 kW ≈ $99/kWe-yr.
            Reduced to $65/kWe-yr as Meier's rate includes items that
            Hawker captures elsewhere. Within Hawker's range ($10-100).

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 1 (M = 3% of C_T, line 101)
            **Basis**: [ESTIMATED] Meier's 3% O&M rate, adjusted for
                Hawker model scope. Year-dollars: 1988$.
            */
        }

        // === HIF-specific: Meier COE chain ===

        attribute thermal_power_gw : Real = 2.054 {
            doc /*
            Thermal power in GW. From Osiris operating parameters table.
            Used as input to Meier's reactor cost formula.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Osiris operating parameters — Thermal power: 2054 MW
            **Basis**: EIF-1992 Osiris design. Note: cannot be cleanly
                derived from Hawker's simplified power balance formula.
            */
        }

        attribute net_electric_power_gw : Real = 1.0 {
            doc /*
            Net electric power in GW. Osiris design target.
            Used in Meier's COE formula denominator.

            **Source**: knowledge/sources/energy_from_inertial_fusion/output.md
            **Ref**: Osiris operating parameters — Net electric power: 1000 MWe
            **Basis**: EIF-1992 Osiris design target
            */
        }

        calc meier_reactor_cost_calc : 'Meier Reactor Cost' {
            doc /*
            Meier's reactor cost at Osiris thermal power, single unit.

            **Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
            **Ref**: Eq. 3
            **Basis**: Meier 1986 reactor cost scaling
            */

            in thermal_power_gw_in = thermal_power_gw;
            in num_units = 1.0;
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
            in target_factory_cost = 0.1;
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

        attribute meier_coe : Real = meier_coe_calc.coe_cents_kwh {
            doc /*
            Meier COE output in cents/kWh (1988$). Independent validation
            output alongside the inherited Hawker LCOE ($/MWh).

            Expected: ~5 cents/kWh at Meier reference parameters.
            */
        }
    }
}
