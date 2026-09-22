"""Check frozen-record integrity for this goal without re-evaluating the plant."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3

parser=argparse.ArgumentParser()
parser.add_argument('--record',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
r=args.record
read=lambda p:json.loads(p.read_text())
s=read(r/'snapshot.json')
body=(r/'record.md').read_text()
assert not re.search(r'<[^>]+>',body),'unresolved placeholder'
assert [int(x) for x in re.findall(r'^## (\d+)\.',body,re.M)]==list(range(1,18))
artifacts=s['arms'][0]['artifacts']
for a in artifacts:
    assert hashlib.sha256((r/a['path']).read_bytes()).hexdigest()==a['sha256'],a['path']
assert all(n in s['fingerprints'] for n in s['manifest']['content_used']['fingerprint_names'])
assert {a['store_id'] for a in s['arms']} <= {a['store_id'] for a in s['stores']}
rows=read(r/'results/cases.json')['cases']
proposals={p['case']:p['point'] for p in read(r/'proposed-points.json')['cases']}
assert len(rows)==len(proposals)==s['case_count']
assert {c['case'] for c in rows}==set(proposals)
assert all(c['inputs']==proposals[c['case']] and c['state']=='completed' for c in rows)
assert {c['executable_fingerprint'] for c in rows}=={s['fingerprints']['recorded_provenance.executable_fingerprint']}
v=read(r/'results/verification_summary.json')
assert v['outcome']=='pass'
store=r/s['stores'][0]['path']
con=sqlite3.connect('file:'+str(store.resolve())+'?mode=ro&immutable=1',uri=True)
assert con.execute('select count(*) from cases').fetchone()[0]==len(rows)
con.close()
ids=lambda text:{line.split('|')[1].strip(' `') for line in text.splitlines() if line.startswith('|') and line.split('|')[1].strip(' `').startswith(r.name+'#')}
findings=ids(body)
log=(r.parent/'DISCOVERY_LOG.md').read_text()
joined={line.split('|')[3].strip(' `') for line in log.splitlines() if line.startswith('| 20') and line.split('|')[3].strip(' `').startswith(r.name+'#')}
assert findings and findings==joined
receipt={'record':str(r),'passed':True,'cases':len(rows),'hashed_artifacts':len(artifacts),'findings':sorted(findings),'snapshot_sha256':hashlib.sha256((r/'snapshot.json').read_bytes()).hexdigest(),'coverage':'record identities, retained artifact digests, full stored/proposed input maps, completed store count, findings joins; no repeated physical evaluation'}
args.out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
