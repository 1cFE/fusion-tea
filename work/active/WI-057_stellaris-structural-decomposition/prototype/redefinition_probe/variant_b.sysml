package RedefProbe {
    private import ScalarValues::*;
    calc def BaseCost { in n : Real; in m : Real; return cost : Real = n * m; }
    calc def VarCost { in n : Real; in m : Real; in f : Real; return cost : Real = n * m * (1.0 + f); }
    part def Casing { attribute m : Real; }
    part def Magnet {
        attribute n : Real;
        part casing : Casing;
        calc structure_cost : BaseCost { in n = 'Magnet'::n; in m = casing.m; }
        attribute cost : Real = structure_cost.cost;
    }
    part def VarMagnet :> Magnet {
        attribute f_markup : Real default 0.0;
        calc :>> structure_cost : VarCost { :>> f = f_markup; }
    }
    part def Plant { part magnet : Magnet; attribute total : Real = magnet.cost; }
    part probe : Plant {
        part :>> magnet : VarMagnet { :>> n = 48.0; :>> f_markup = 0.1; part :>> casing { :>> m = 63000.0; } }
    }
}
