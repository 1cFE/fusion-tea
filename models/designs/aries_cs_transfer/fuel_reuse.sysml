package aries_fuel_reuse {
    private import ScalarValues::*;
    private import mfe_fuel_cycle::*;
    private import mfe_viability::*;

    part fuel_system {
        doc /* Conditioned tritium exhaust evaluation, not ARIES installed-fuel-system qualification. Source: work/active/WI-082_aries-existing-component-transfer-proof/spec.md. Reference: analysis contract and MR-7 roles. Last Updated: 2026-09-21. */
        attribute fusion_load_mw : Real = 2436.0 {
            doc /* Source: .project/active/aries-comparison-preparation/alternative-point-screen/evidence/source-Lyon-page-23.png. Ref: Lyon Table VII, printed p716, reference fusion power MW. Basis: visually verified supplied load, not independently predicted fusion power. */
        }
        // Inherited constants: models/designs/stellarator_09/stellarator_plant.sysml:1474-1477,1507,1605.
        attribute reaction_energy_mev : Real = 17.58;
        attribute mev_joules : Real = 1.6021766339999998e-13;
        attribute tritium_atom_kg : Real = 5.008267663228036e-27;
        attribute pass_burn_fraction : Real = 0.05;
        attribute exhaust_recovery : Real = 0.99;
        attribute decay_constant_s : Real = 1.782785958230312e-09;
        // AGENT dormant assumptions; breeding outputs are outside this case's accepted result.
        attribute unused_tbr_placeholder : Real = 0.0;
        attribute assumed_extraction : Real = 1.0;
        attribute dormant_inventory_atoms : Real = 0.0;
        attribute dormant_stock_growth_atoms_s : Real = 0.0;
        calc flows : 'Fuel Cycle Flows' {
            in p_fus_in = fusion_load_mw;
            in q_eff_in = reaction_energy_mev;
            in mev_to_joules_in = mev_joules;
            in burn_fraction_in = pass_burn_fraction;
            in t_recycle_in = exhaust_recovery;
            in tbr_available_in = unused_tbr_placeholder;
            in eta_extract_in = assumed_extraction;
            in lambda_T_in = decay_constant_s;
            in I_total_in = dormant_inventory_atoms;
            in G_stock_in = dormant_stock_growth_atoms_s;
            in m_T_kg_in = tritium_atom_kg;
            in s_per_fpy_in = 31536000.0;
        }
        attribute exhaust_atoms_s : Real = flows.exhaust_rate;
    }

    part processing {
        doc /* AGENT conditional scalar tritium-processing choice, units atoms/s. No vendor map, D+T inventory, cost or ARIES installed-capability claim. Source: work/active/WI-082_aries-existing-component-transfer-proof/spec.md. Reference: analysis contract. Last Updated: 2026-09-21. */
        attribute selected_rating_atoms_s : Real = 2.0e22;
        attribute assumed_conditions_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute flow_available : Boolean = true;
        calc capacity : 'Offered Capacity Screen' {
            in rating_in = selected_rating_atoms_s;
            in demand_in = fuel_system.exhaust_atoms_s;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_conditions_supported;
            in demand_available_in = flow_available;
        }
        attribute margin_atoms_s : Real = capacity.margin;
        attribute evaluation_defined : Real = capacity.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin_atoms_s;
        }
    }
}
