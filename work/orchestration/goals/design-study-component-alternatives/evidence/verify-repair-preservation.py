"""Check owner-required preserved evidence, independent oracle and tolerances."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
if args.out.exists():raise ValueError('preservation receipt exists')
baseline=Path(__file__).with_name('repair-preservation-before.json')
rows=json.loads(baseline.read_text())['files'];failures=[]
for row in rows:
    path=ROOT/row['path']
    actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    if actual!=row['sha256']:failures.append({'path':row['path'],'expected':row['sha256'],'actual':actual})
result={'status':'fail' if failures else 'pass','checked_files':len(rows),'baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'failures':failures}
args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(failures))
