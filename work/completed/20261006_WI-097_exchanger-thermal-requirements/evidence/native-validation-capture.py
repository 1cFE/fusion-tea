"""Compare complete diagnostic identities, retaining source expressions for additions."""
import json
import re
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from agentic_mbse.validation import validate_structure, validate_architecture

HERE=Path(__file__).resolve().parent
BASE='exploration/aries_integrated/input_models'
CURRENT='exploration/exchanger_architecture/thermal_requirements/input_models'
results={name:{str(level):asdict(fn(path)) for level,fn in ((2,validate_structure),(6,validate_architecture))}
         for name,path in (('baseline',BASE),('current',CURRENT))}
normalize=lambda text:re.sub(r':\d+(?=\D|$)',':LINE',str(text).replace(CURRENT,'MODELS').replace(BASE,'MODELS'))
comparison={}
for level in ('2','6'):
    old=Counter(map(normalize,results['baseline'][level]['issues']))
    new=Counter(map(normalize,results['current'][level]['issues']))
    comparison[level]={'baseline_count':sum(old.values()),'current_count':sum(new.values()),
                       'added':list((new-old).elements()),'removed':list((old-new).elements())}
for name,data in results.items():
    (HERE/('native-validation-'+name+'.json')).write_text(json.dumps(data,indent=2,default=str)+'\n')
(HERE/'native-validation-comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
print(json.dumps(comparison,indent=2))
