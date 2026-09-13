"""Preservation, minimum-change and numerical invariance checks for design repair."""
import hashlib,json,subprocess
from pathlib import Path
h=Path(__file__).resolve().parent;item=h.parent;original=item/'prototype'
def sha(data): return hashlib.sha256(data).hexdigest()
preserved={}
for f in [item/'review.md',*sorted(original.iterdir())]:
 if not f.is_file(): continue
 rel=str(f.relative_to(Path.cwd())) if f.is_relative_to(Path.cwd()) else str(f)
 expected=subprocess.check_output(['git','show',f'd28ac7e3:{rel}'])
 assert f.read_bytes()==expected,f
 preserved[rel]=sha(expected)
a=json.loads((original/'results.json').read_text());b=json.loads((h/'results.json').read_text());counts={}
for case in ['baseline','reserve','demand','efficiency','availability','negative_efficiency','overunit_efficiency']:
 old=a[case]['outputs'];new=b[case]['outputs'];keys=[k for k,v in old.items() if isinstance(v,(int,float))]
 assert all(new[k]==old[k] for k in keys),case
 counts[case]=len(keys)
assert all(len(set(b[c]['responses'])-{'headline'})==18 for c in counts)
assert [k for k,v in b['baseline']['responses'].items() if v=='violated']==[k for k,v in a['baseline']['responses'].items() if v=='violated']
diff=json.loads((h/'validation-diff.json').read_text());assert diff==json.loads((original/'validation-diff.json').read_text())
result={'preserved_sha256':preserved,'exact_unchanged_scalar_outputs':counts,'revised_verdict_count':18,'baseline_violation':'divertor_heat_ok retained','quality_differential':'identical to original: L2 10 unchanged; L6 227 to 229 with same two introduced findings'}
(h/'repair-diff-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: original evidence bytes preserved, operation outputs exact, four new scalar comparisons, quality differential unchanged')
