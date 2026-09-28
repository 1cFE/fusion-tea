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
 part def BreedingModel :> Blanket { attribute model_t:Real; attribute model_R:Real; attribute model_shield:Real; calc breeding:Breed { in t_in=model_t; in R_in=model_R; in shield_in=model_shield;} attribute computed_tbr:Real=breeding.total; attribute computed_defined:Real=breeding.valid;}
 part stellaris:Plant {
  part :>> blanket : BreedingModel {
   :>> model_t=t; :>> model_R=stellaris.plasma.R; :>> model_shield=stellaris.shield.t;
   :>> tbr=breeding.total;
  }
  calc adequacy:Adequacy {in achieved=blanket.tbr;in required=fuel_cycle.required;}
  assert constraint tbr_ok:Floor {in actual=blanket.tbr;in limit=fuel_cycle.required;}
 }
 part held:Plant { part :>> blanket { :>> tbr=1.074; } }
}
