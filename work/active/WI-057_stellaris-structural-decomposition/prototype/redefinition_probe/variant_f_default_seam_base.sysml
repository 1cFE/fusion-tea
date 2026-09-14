package RedefProbe {
    private import ScalarValues::*;
    calc def BaseCost { in n : Real; in m : Real; return cost : Real = n * m; }
    calc def VarCost { in n : Real; in m : Real; in f : Real; return cost : Real = n * m * (1.0 + f); }
    calc def Total { in c : Real; return total : Real = c * 2.0; }
    part def Casing { attribute m : Real; }
    part def Magnet {
        attribute n : Real;
        part casing : Casing;
        calc structure_cost : BaseCost { in n = 'Magnet'::n; in m = casing.m; }
        // the EXPOSE as a DEFAULT, so a variant may point it at its own calc
        attribute cost : Real default structure_cost.cost;
    }
    part def VarMagnet :> Magnet {
        attribute f_markup : Real default 0.0;
        calc structure_cost_ni : VarCost { in n = 'VarMagnet'::n; in m = casing.m; in f = f_markup; }
        :>> cost = structure_cost_ni.cost;
    }
    part def Plant {
        part magnet : Magnet;
        calc total_calc : Total { in c = magnet.cost; }
        attribute total : Real = total_calc.total;
    }
    part probe : Plant {
        part :>> magnet { :>> n = 48.0; part :>> casing { :>> m = 63000.0; } }
    }
}
