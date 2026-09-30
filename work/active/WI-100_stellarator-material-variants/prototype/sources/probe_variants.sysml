package probe_variants {
    doc /* WI-100 probes P1-P4 (scratch only): minimal variants that rebind the staged seams. Not a model. */
    private import ScalarValues::*;
    private import mfe_power_core::*;
    private import mfe_plant_systems::*;
    private import mfe_cryo_inventory::*;
    calc def 'REBCO Shape Branch' {
        doc /* Probe P4 copy of the design section 2.4 conditional glue calc: shape_mode = 1 above the last knot, else 0. */
        in attribute B_peak_in : Real default 0.0;
        in attribute B_knot_max_in : Real default 0.0;
        out attribute shape_mode : Real;
    }
    part def 'Probe Magnet System' :> 'Magnet System' {
        :>> rebco_law_enabled = 0.0;
        attribute probe_winding_extra : Real;
        calc winding_sum : 'Electrical Power Sum' {
            in p_a = winding_procurement.cost;
            in p_b = probe_winding_extra;
        }
        calc shape_branch : 'REBCO Shape Branch' {
            in B_peak_in = peak_field_calc.B_peak;
            in B_knot_max_in = probe_knot;
        }
        attribute probe_knot : Real;
        attribute probe_shape_mode : Real = shape_branch.shape_mode;
        :>> winding_cost = winding_sum.total;
    }
    part def 'Probe Cryoplant' :> 'Cryoplant' {
        :>> inventory_enabled = false;
        attribute probe_p_extra : Real;
        attribute probe_drive : Real;
        attribute probe_q_cold : Real;
        attribute probe_q_shield : Real;
        attribute probe_capital : Real;
        calc staged_elec : 'Electrical Power Sum' {
            in p_a = refrigeration_sum.total;
            in p_b = probe_p_extra;
        }
        calc staged_drive : 'Electrical Power Sum' {
            in p_a = probe_drive;
            in p_b = inventory.p_drive;
        }
        calc staged_cold : 'Electrical Power Sum' {
            in p_a = probe_q_cold;
            in p_b = cold_load_W_demand_conversion.demand;
        }
        calc staged_shield : 'Electrical Power Sum' {
            in p_a = probe_q_shield;
            in p_b = inventory.q_inventory_shield;
        }
        calc staged_capital : 'Electrical Power Sum' {
            in p_a = probe_capital;
            in p_b = 0.0;
        }
        :>> purchase_cost_per_module = staged_capital.total;
        :>> cold_load_W_required = staged_cold.total;
        :>> intercept_load_W_required = staged_shield.total;
        :>> intercept_demand_available = true;
        :>> p_elec = staged_elec.total;
        :>> p_drive = staged_drive.total;
    }
}
