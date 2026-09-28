"""Compare every rebuilt complete point and alias with the retained failed record."""
from pathlib import Path
import collections,hashlib,json
HERE=Path(__file__).resolve().parent
OLD=HERE.parent.parent/'20260927-design-study-whole-plant-conversion/preparation'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=read(OLD/'proposed-points.json');new=read(HERE/'proposed-points.json')
def aliases(doc):
 out={}
 for point in doc['cases']:
  for alias in point['aliases']:
   assert alias['case'] not in out
   out[alias['case']]=dict(point=point['point'],point_id=point['point_id'],alias=alias)
 return out
before,after=aliases(old),aliases(new)
changed=[];metadata=[]
for name in sorted(set(before)&set(after)):
 a,b=before[name],after[name]
 delta={k:dict(before=a['point'][k],after=b['point'][k]) for k in a['point'] if a['point'][k]!=b['point'][k]}
 if delta:changed.append(dict(alias=name,old_point_id=a['point_id'],new_point_id=b['point_id'],scenario=b['alias']['scenario'],family=b['alias']['family'],branch=b['alias']['branch'],input_differences=delta))
 md={k:dict(before=a['alias'].get(k),after=b['alias'].get(k)) for k in set(a['alias'])|set(b['alias']) if a['alias'].get(k)!=b['alias'].get(k)}
 if md:metadata.append(dict(alias=name,differences=md))
oldids={r['point_id'] for r in old['cases']};newids={r['point_id'] for r in new['cases']}
oldanchors=read(OLD/'anchors.json');newanchors=read(HERE/'anchors.json')
anchors=[]
for group in oldanchors:
 if oldanchors[group]!=newanchors[group]:anchors.append(group)
result=dict(old_proposal_sha256=sha(OLD/'proposed-points.json'),new_proposal_sha256=sha(HERE/'proposed-points.json'),old_unique_points=len(oldids),new_unique_points=len(newids),unchanged_unique_points=len(oldids&newids),removed_point_ids=sorted(oldids-newids),added_point_ids=sorted(newids-oldids),old_alias_count=len(before),new_alias_count=len(after),removed_aliases=sorted(set(before)-set(after)),added_aliases=sorted(set(after)-set(before)),changed_alias_count=len(changed),changed_point_count=len({r['new_point_id'] for r in changed}),changed_by_family=dict(collections.Counter(r['family'] for r in changed)),changed_aliases=changed,metadata_changes=metadata,changed_anchor_groups=anchors,interpretation='Exact byte-value input comparison; new oracle result changes alone do not count as changed inputs. All differences require coordinator disposition before main execution.')
(HERE/'original-point-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('changed_aliases','metadata_changes','removed_point_ids','added_point_ids')},indent=2))
