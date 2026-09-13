"""Positive native controls captured before and after the bounded correction."""
import importlib.util,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
s=importlib.util.spec_from_file_location('native_probe',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
P=p.P+'magnet__'
p.CASES={'baseline':{},'half_current':{P+'I_coil':7700000.},'double_current':{P+'I_coil':30800000.},'half_density':{P+'j_wp':59.4135802469136},'double_density':{P+'j_wp':237.6543209876544},'outside_source_density':{P+'j_wp':500.}}
p.run(ROOT/'exploration/stellarator_e2e/generated',HERE/(sys.argv[1]+'.json'))
