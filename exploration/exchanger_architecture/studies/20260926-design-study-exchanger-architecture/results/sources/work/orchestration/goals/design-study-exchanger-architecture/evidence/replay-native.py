"""Replay all retained native input maps into a fresh directory, never the sealed record."""
import argparse
import json
from pathlib import Path
import runpy
import shutil
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from exploration.aries_integrated.studies import study_route as route
from scripts.study import common
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--destination', type=Path, required=True)
args = parser.parse_args()
record = ROOT/'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture'
target = args.destination.resolve()
if target.exists():
    raise ValueError('destination must not exist; preserve previous evidence')
if target == record or record in target.parents:
    raise ValueError('cannot replay within sealed evidence')
target.mkdir(parents=True)
for name in ('manifest.json', 'proposed-points.json', 'axes.json'):
    shutil.copyfile(record/name, target/name)
route.MANIFEST_PATH=target/'manifest.json'
route.execute_baseline(target/'preparation', manifest_path=route.MANIFEST_PATH)
execute=runpy.run_path(str(ROOT/'exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/execute_study.py'))['execute']
execute(target, record/'results/integration_return_used.json')
old=common.read_json(record/'results/cases.json','sealed cases')['cases']
new=common.read_json(target/'results/cases.json','replay cases')['cases']
old={r['case']:r for r in old}; new={r['case']:r for r in new}
assert old.keys()==new.keys()
diff=[]
for name in old:
    for field in ('inputs','outputs','verdicts','state','executable_fingerprint'):
        if old[name][field]!=new[name][field]:
            diff.append({'case':name,'field':field})
(target/'replay-comparison.json').write_text(json.dumps({'case_count':len(old),'comparison':'exact stored maps/outputs/verdicts/state/executable; new native candidate IDs retained','differences':diff},indent=2)+'\n')
if diff: raise ValueError(f'{len(diff)} differing case fields; see replay-comparison.json')
print(json.dumps({'replay':'pass','cases':len(old),'destination':str(target)}))
