package plant_chain_probe {
    private import ScalarValues::*;
    private import mfe_tail_supplementary_costs::*;
    private import mfe_account_costs::*;

    // WI-028 risky-construct probe: the 4-deep cross-calc overnight chain
    //   cas2x -> contingency -> cas20 -> indirect -> cas30 -> supplementary
    // where supplementary ALSO reads cas20 directly. Mirrors the WI-025
    // contingency/indirect attribute->calc->attribute pattern one level deeper.
    // This is a parse-level shape check only; codegen capture is the plan step.
    part def 'Overnight Probe' {
        // stand-in upstream account aggregates (bound to real channels in the plant)
        attribute powercore_capital : Real = 3.4e9;
        attribute bop_capital : Real = 4.84e8;
        attribute buildings_capital : Real = 6.19e8;
        attribute special_materials_capital : Real = 2.08e7;
        attribute preconstruction_capital : Real = 1.85e7;
        attribute cas28_capital : Real = 5.0e6;
        attribute p_net : Real = 1000.0;
        attribute p_th : Real = 2819.07;
        attribute p_et : Real = 1127.63;
        attribute p_cryo : Real = 0.8;

        // --- CAS22 tail accounts ---
        calc remote_handling : 'Remote Handling Cost' {
            in base = 150.0e6; in concept_scale = 1.0; in p_et = p_et;
        }
        calc installation : 'Installation Labor Cost' {
            in installation_frac = 0.14;
            in reactor_subtotal = powercore_capital + remote_handling.cost;
        }
        calc coolant : 'Coolant Cost' {
            in primary_base = 166.0e6; in p_net = p_net;
            in intermediate_base = 40.6e6; in p_th = p_th;
        }
        calc aux_cooling : 'Aux Cooling Cost' {
            in aux_per_mw = 1100.0; in p_th = p_th;
            in cryo_base = 200.0e6; in p_cryo = p_cryo;
        }
        calc waste : 'Plant Power-Law Cost' {
            in base = 1.96e6; in power = p_th; in ref_power = 1000.0; in alpha = 1.0;
        }
        calc fuel_handling : 'Plant Power-Law Cost' {
            in base = 120.0e6; in power = p_net; in ref_power = 1000.0; in alpha = 0.7;
        }
        calc other_rpe : 'Plant Power-Law Cost' {
            in base = 11.5e6; in power = p_net; in ref_power = 1000.0; in alpha = 0.8;
        }
        calc inc_cost : 'Plant Power-Law Cost' {
            in base = 85.0e6; in power = p_th; in ref_power = 3500.0; in alpha = 0.65;
        }

        attribute cas22_tail_capital : Real =
            remote_handling.cost + installation.cost + coolant.cost
            + aux_cooling.cost + waste.cost + fuel_handling.cost
            + other_rpe.cost + inc_cost.cost;
        attribute cas22_capital : Real = powercore_capital + cas22_tail_capital;

        // --- CAS20 series: cas2x -> contingency -> cas20 -> indirect -> cas30 ---
        attribute cas2x_pre_contingency : Real =
            buildings_capital + cas22_capital + bop_capital
            + special_materials_capital + cas28_capital;
        calc contingency : 'Contingency Cost' {
            in contingency_rate = 0.0; in direct_subtotal = cas2x_pre_contingency;
        }
        attribute cas20_capital : Real = cas2x_pre_contingency + contingency.cost;
        calc indirect : 'Indirect Cost' {
            in indirect_fraction = 0.20; in direct_cost = cas20_capital;
            in construction_time = 8.0;
        }
        attribute cas30_capital : Real = indirect.cost;
        attribute cas23_to_28_capital : Real =
            bop_capital + special_materials_capital + cas28_capital;

        // --- CAS40 / CAS50 at overnight level (NOT in cas2x: no contingency/indirect) ---
        calc owner : 'Plant Power-Law Cost' {
            in base = 41.2e6; in power = p_net; in ref_power = 1000.0; in alpha = 0.5;
        }
        calc supplementary : 'Supplementary Cost' {
            in spares_frac = 0.03; in startup_fuel_base = 40.0e6; in decom_base = 272.0e6;
            in cas20 = cas20_capital; in cas23_to_28 = cas23_to_28_capital;
            in cas30 = cas30_capital; in p_net = p_net;
        }
        attribute overnight_capital : Real =
            preconstruction_capital + cas20_capital + cas30_capital
            + owner.cost + supplementary.cost;

        // --- CAS60 reserved gate: reproduced line, total_capital = overnight (Option C) ---
        calc idc : 'IDC Closed-Form Cost' {
            in interest_rate = 0.07; in construction_years = 8.0;
            in overnight_cost = overnight_capital;
        }
        attribute total_capital : Real = overnight_capital;   // Option C default
    }
}
