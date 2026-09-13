import re,json,subprocess
from pathlib import Path
h=Path(__file__).resolve().parent
paths=['models/library/analyses/'+n+'.sysml' for n in ['mfe_heating_chain','mfe_divertor_heat','mfe_power_balance']]+['models/designs/generic_mfe/mfe_plant.sysml','models/designs/stellarator_09/stellarator_plant.sysml']
def clean(text):
 text=re.sub(r'/\*.*?\*/',lambda m:'\n'*m.group().count('\n'),text,flags=re.S)
 return [(i,re.sub(r'//.*','',line).strip()) for i,line in enumerate(text.splitlines(),1)]
rows=[]
for path in paths:
 old=clean(subprocess.check_output(['git','show','546218a5:'+path]).decode());lookup={line:i for i,line in old if line}
 for line,body in clean(Path(path).read_text()):
  values=re.findall(r'(?<![A-Za-z_\d])(?:\d+\.\d*|\d+)(?:[eE][-+]?\d+)?',body)
  if not values:continue
  inherited=body in lookup
  assert inherited or body in ['efficiency > 0.0','efficiency <= 1.0'],(path,line,body)
  rows.append({'model':f'{path}:{line}','statement':body,'values':values,'baseline':f'{path}:{lookup[body]}@546218a5' if inherited else 'design.md: scalar fraction domain; algebraic definition','discrepancy_percent':0 if inherited else None,'status':'PASS inherited exact' if inherited else 'PASS design-specific domain literal'})
(h/'numerical-inventory.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'numeric source lines; all inherited byte-equivalent statements except two documented domain bounds')
