from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path.cwd()))
p=Path('models/designs/stellarator_09/stellarator_plant.sysml');s=p.read_text();a=s.index('            part :>> reheater {');b=s.index('            }',a);s=s[:a]+ '\n'.join(line for line in s[a:b].split('\n') if ':>> pressure_MPa' not in line)+s[b:];p.write_text(s)
p=Path('models/library/structure/mfe_steam_cycle_components.sysml');s=p.read_text();i=s.rfind('}');s=s[:i]+'''    part def 'Steam Extraction Splitter' {
        doc /* WI-073 ideal extraction junction. Both branches retain HP outlet pressure and enthalpy; mass flow divides explicitly. */
        port inlet : ~'Water State Port';
        port reheat_out : 'Water State Port';
        port bleed_out : 'Water State Port';
        attribute total_flow_kg_s : Real;
        attribute reheat_flow_kg_s : Real;
        attribute bleed_flow_kg_s : Real;
        attribute pressure_MPa : Real;
        attribute enthalpy_kJ_kg : Real;
    }
    part def 'Salt Branch Distributor' {
        doc /* WI-073 parallel salt branches. Paired Thermal Ports split the hot supply and join the equal-temperature cold returns. Temperatures below use Celsius; generic port temperature is Kelvin. Pressure loss is outside this cycle model. */
        port supply_return : ~'Thermal Port';
        port main_branch : 'Thermal Port';
        port reheat_branch : 'Thermal Port';
        attribute total_flow_kg_s : Real;
        attribute main_flow_kg_s : Real;
        attribute reheat_flow_kg_s : Real;
        attribute hot_C : Real;
        attribute return_C : Real;
    }
'''+s[i:];p.write_text(s)
p=Path('models/designs/generic_mfe/mfe_subsystems.sysml');s=p.read_text();s=s.replace("        port main_salt_branch : 'Thermal Port';\n        port reheat_salt_branch : 'Thermal Port';\n",''); states={'main_steam_generator':('feed','main'),'hp_turbine':('main','hp'),'reheater':('hp','reheat'),'lp_turbine':('reheat','lp'),'open_feedwater_heater':(None,'heater'),'condenser':('lp','condensate'),'condensate_pump':('condensate',None),'feedwater_pump':('heater','feed')}
for name,(src,dst) in states.items():
 a=s.index('        part '+name+' :');b=s.index('\n',a)+1;extra=''
 for direction,st in [('in',src),('out',dst)]:
  if st:
   extra+=f"            attribute temperature_{direction}_C : Real = 'Turbine Plant'::t_{st}_C;\n            attribute entropy_{direction}_kJ_kgK : Real = 'Turbine Plant'::s_{st}_kJ_kgK;\n"
 s=s[:b]+extra+s[b:]
pos=s.index("        calc matched_cycle :")
extra='''        part extraction_splitter : 'Steam Extraction Splitter' {
            :>> total_flow_kg_s = 'Turbine Plant'::mdot_hp_kg_s;
            :>> reheat_flow_kg_s = 'Turbine Plant'::mdot_reheat_kg_s;
            :>> bleed_flow_kg_s = 'Turbine Plant'::mdot_bleed_kg_s;
            :>> pressure_MPa = 'Turbine Plant'::p_hp_MPa;
            :>> enthalpy_kJ_kg = 'Turbine Plant'::h_hp_kJ_kg;
        }
        part salt_distributor : 'Salt Branch Distributor' {
            :>> total_flow_kg_s = 'Turbine Plant'::salt_flow_total_kg_s;
            :>> main_flow_kg_s = 'Turbine Plant'::salt_main_flow_kg_s;
            :>> reheat_flow_kg_s = 'Turbine Plant'::salt_reheat_flow_kg_s;
            :>> hot_C = 'Turbine Plant'::cycle_salt_hot_C;
            :>> return_C = 'Turbine Plant'::cycle_salt_return_C;
        }
'''
s=s[:pos]+extra+s[pos:];s=s.replace('connect hp_turbine.outlet to reheater.inlet;','connect hp_turbine.outlet to extraction_splitter.inlet;\n        connect extraction_splitter.reheat_out to reheater.inlet;').replace('connect hp_turbine.outlet to open_feedwater_heater.bleed_in;','connect extraction_splitter.bleed_out to open_feedwater_heater.bleed_in;').replace('connect coolant to main_salt_branch;\n        connect coolant to reheat_salt_branch;','connect coolant to salt_distributor.supply_return;').replace('connect main_salt_branch to main_steam_generator.salt;','connect salt_distributor.main_branch to main_steam_generator.salt;').replace('connect reheat_salt_branch to reheater.salt;','connect salt_distributor.reheat_branch to reheater.salt;');p.write_text(s)
from tests.model_families import MFE,materialize_canonical_subset
materialize_canonical_subset(MFE,MFE.twin)
(MFE.twin/'data').mkdir(exist_ok=True)
shutil.copyfile('models/library/data/matched_steam_properties.json',MFE.twin/'data/matched_steam_properties.json')
from sysml_codegen.cli import GenerationConfig,run_codegen
assert run_codegen(GenerationConfig(models_path=MFE.twin,output_path=Path('/tmp/wi073-stencil'),package_name='stellarator_tea',overwrite=True))
