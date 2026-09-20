package Probe {
private import ScalarValues::*;
calc def Legacy {
 in attribute x_in : Real;
 out attribute gross_out : Real = x_in * 2.0;
}
calc def Match {
 in attribute enabled_in : Real;
 in attribute legacy_in : Real;
 in attribute property_in : Real;
 out attribute gross_out : Real;
 out attribute state_h : Real;
 out attribute pump_out : Real;
}
calc def Sink {
 in attribute value_in : Real;
 out attribute result : Real = value_in;
}
part def Component { attribute enthalpy : Real; }
part def Turbine {
 attribute raw : Real default 3.0;
 attribute enabled : Real default 0.0;
 attribute property_value : Real default -1.0;
 calc legacy : Legacy { in x_in = raw; }
 calc matched : Match { in enabled_in = enabled; in legacy_in = legacy.gross_out; in property_in = property_value; }
 attribute gross : Real = matched.gross_out;
 attribute state_h : Real = matched.state_h;
 part steam : Component { :>> enthalpy = matched.state_h; }
}
part def Plant {
 part turbine : Turbine;
 calc sink : Sink { in value_in = turbine.gross; }
}
part plant : Plant;
}