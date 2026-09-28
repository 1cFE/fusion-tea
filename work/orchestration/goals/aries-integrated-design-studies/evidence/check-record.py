"""Check frozen record transport, complete pairing and native-store attempt identity."""
import argparse, hashlib, json, re, sqlite3
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.record
read=lambda f:json.loads((r/f).read_text())
s=read('snapshot.json');bad=[]
for arm in s['arms']:
 for f in arm['artifacts']:
  path=r/f['path']
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=f['sha256']:bad.append(f['path'])
assert not bad,bad
text=(r/'record.md').read_text();assert len(re.findall(r'^## (?:[1-9]|1[0-7])\. ',text,re.M))==17
assert not re.search(r'<[^>]+>|SNAPSHOT_PENDING',text)
assert all(n in s['fingerprints'] for n in s['manifest']['content_used']['fingerprint_names'])
assert all(arm['store_id'] in {st['store_id'] for st in s['stores']} for arm in s['arms'])
rows=read('results/cases.json')['cases'];decl={x['case']:x for x in read('proposed-points.json')['cases']};assert len(rows)==len(decl)
for row in rows:assert row['inputs']==decl[row['case']]['point'] and row['state']=='completed'
pairs={}
for row in rows:pairs.setdefault(decl[row['case']]['design'],[]).append(row)
for name,pair in pairs.items():
 assert len(pair)==2
 aa,bb=sorted(pair,key=lambda x:x['inputs']['aries_integrated_plant__fuel_inventory__annual_recovery_kg'])
 changed={k for k in aa['inputs'] if aa['inputs'][k]!=bb['inputs'][k]}
 assert changed=={'aries_integrated_plant__fuel_inventory__annual_recovery_kg','aries_integrated_plant__finance__supply_service_annual'}
 assert aa['inputs']['aries_integrated_plant__fuel_inventory__annual_recovery_kg']==0 and bb['inputs']['aries_integrated_plant__fuel_inventory__annual_recovery_kg']==100
 assert aa['inputs']['aries_integrated_plant__finance__supply_service_annual']==0 and bb['inputs']['aries_integrated_plant__finance__supply_service_annual']==30e6
st=r/'results/native'/f'{r.name}.db'; con=sqlite3.connect('file:'+str(st.resolve())+'?mode=ro&immutable=1',uri=True)
counts=dict(con.execute('select state,count(*) from attempt_transitions group by state'));assert counts=={'started':len(rows),'committed':len(rows)}
assert con.execute('select max(attempt_number) from attempt_transitions').fetchone()[0]==1;con.close()
log=(r.parent/'DISCOVERY_LOG.md').read_text();ids=set(re.findall(re.escape(r.name)+r'#\d+',text));logged={line.split('|')[3].strip().strip('`') for line in log.splitlines() if line.startswith('| 20') and line.split('|')[3].strip().strip('`').startswith(r.name+'#')};assert ids==logged
out={'passed':True,'cases':len(rows),'physical_pairs':len(pairs),'hashed_artifacts':sum(len(x['artifacts']) for x in s['arms']),'attempts':counts,'finding_joins':len(ids),'snapshot_sha256':hashlib.sha256((r/'snapshot.json').read_bytes()).hexdigest()};a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
