from pathlib import Path
import json
from sysml_codegen.cli import GenerationConfig, run_codegen
ROOT=Path(__file__).resolve().parent
common='''package Probe {
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
'''
selector='''part def Turbine {
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
}'''
specialized='''part def Turbine {
 attribute raw : Real default 3.0;
 calc legacy : Legacy { in x_in = raw; }
 attribute gross : Real = legacy.gross_out;
}
part def MatchedTurbine :> Turbine {
 attribute enabled : Real default 1.0;
 attribute property_value : Real default 4.0;
 calc matched : Match { in enabled_in = enabled; in legacy_in = legacy.gross_out; in property_in = property_value; }
 attribute :>> gross = matched.gross_out;
 attribute state_h : Real = matched.state_h;
 part steam : Component { :>> enthalpy = matched.state_h; }
}
part def Plant {
 part turbine : Turbine;
 calc sink : Sink { in value_in = turbine.gross; }
}
part plant : Plant { part :>> turbine : MatchedTurbine; }
}'''
results={}
for name,body in [('selector',selector),('specialized',specialized)]:
 d=ROOT/name; (d/'models').mkdir(parents=True,exist_ok=True)
 (d/'models'/'probe.sysml').write_text(common+body)
 try: results[name]=run_codegen(GenerationConfig(models_path=d/'models',output_path=d/'pkg',package_name=f'probe_{name}',overwrite=True))
 except Exception as e: results[name]={'error':type(e).__name__,'message':str(e)}
(ROOT/'generation-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
# Separate fixture: replace inherited calculation with a specializing calc type.
replacement=common.replace('calc def Match {','calc def Match :> Legacy {').replace(' out attribute gross_out : Real;',' out attribute :>> gross_out : Real;')
replacement+='''part def Turbine {
 attribute raw : Real default 3.0;
 calc cycle : Legacy { in x_in = raw; }
 attribute gross : Real = cycle.gross_out;
}
part def MatchedTurbine :> Turbine {
 attribute enabled : Real default 1.0;
 attribute property_value : Real default 4.0;
 calc :>> cycle : Match {
  in enabled_in = enabled;
  in legacy_in = raw;
  in property_in = property_value;
 }
}
part def Plant {
 part turbine : Turbine;
 calc sink : Sink { in value_in = turbine.gross; }
}
part plant : Plant { part :>> turbine : MatchedTurbine; }
}'''
d=ROOT/'replacement'; (d/'models').mkdir(parents=True,exist_ok=True)
(d/'models'/'probe.sysml').write_text(replacement)
try: results['replacement']=run_codegen(GenerationConfig(models_path=d/'models',output_path=d/'pkg',package_name='probe_replacement',overwrite=True))
except Exception as e: results['replacement']={'error':type(e).__name__,'message':str(e)}
(ROOT/'generation-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
