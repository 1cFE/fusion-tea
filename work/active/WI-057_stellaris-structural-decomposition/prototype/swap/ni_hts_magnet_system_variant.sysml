    part def 'NI HTS Magnet System' :> 'Magnet System' {
        attribute t_charge_h : Real;
        // an insulation-free winding needs a thicker casing: the variant prices the casing with its own formula
        attribute f_ins_markup : Real default 0.0;
        calc magnet_structure_cost_ni : 'Magnet Structure Cost NI' {
            in n_coils = coil.n_coils;
            in m_casing = casing.m_casing;
            in steel_price = casing.steel_price;
            in f_steel_fab = casing.f_steel_fab;
            in f_ins = f_ins_markup;
        }
        :>> structure_cost = magnet_structure_cost_ni.cost;
    }
