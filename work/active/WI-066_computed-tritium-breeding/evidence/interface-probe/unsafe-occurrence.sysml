package probe {
 private import ScalarValues::*;
 calc def Breed { in attribute t_in:Real; in attribute R_in:Real; in attribute shield_in:Real; out attribute total:Real; out attribute valid:Real; }
 calc def Fuel { in attribute achieved:Real; out attribute required:Real=1.19; out attribute margin:Real=achieved-required; }
 calc def Adequacy { in attribute achieved:Real; in attribute required:Real; out attribute margin:Real=achieved-required; }
 constraint def Floor { in attribute actual:Real; in attribute limit:Real; actual>=limit }
 part def Blanket { attribute t:Real default 0.8; attribute tbr:Real default 1.0; }
 part def Plasma { attribute R:Real default 12.7; }
 part def Shield { attribute t:Real default 0.2; }
 part def FuelCycle { attribute tbr:Real; calc fuel:Fuel {in achieved=tbr;} attribute required:Real=fuel.required; }
 part def Plant {
  part blanket:Blanket;
  part plasma:Plasma;
  part shield:Shield;
  part fuel_cycle:FuelCycle { :>> tbr=blanket.tbr; }
 }
 part stellaris:Plant {
  part :>> blanket {
   calc breeding:Breed { in t_in=t; in R_in=stellaris.plasma.R; in shield_in=stellaris.shield.t; }
   :>> tbr=breeding.total;
   attribute defined_flag:Real=breeding.valid;
  }
  calc adequacy:Adequacy {in achieved=blanket.tbr;in required=fuel_cycle.required;}
  assert constraint tbr_ok:Floor {in actual=blanket.tbr;in limit=fuel_cycle.required;}
 }
 part held:Plant { part :>> blanket { :>> tbr=1.074; } }
}
