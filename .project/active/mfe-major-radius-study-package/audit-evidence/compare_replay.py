import collections,json,xml.etree.ElementTree as ET
from pathlib import Path
out=Path(__file__).parent; impl=out.parent/'implementation'
def parse(path):
    rows={}
    for case in ET.parse(path).iter('testcase'):
        node=case.attrib['classname']+'::'+case.attrib['name']
        events=[(kind,case.find(kind)) for kind in ['failure','error','skipped']]
        kind,event=next(((kind,e) for kind,e in events if e is not None),('passed',None))
        rows[node]={'outcome':kind,'message':event.attrib.get('message','') if event is not None else ''}
    return rows
entering=parse(impl/'entering.xml'); prior=parse(impl/'current-first.xml'); targeted=parse(out/'targeted.xml'); broad=parse(out/'broad.xml')
assert len(targeted)==233 and all(r['outcome']=='passed' for r in targeted.values())
failures={node:row for node,row in broad.items() if row['outcome'] in {'failure','error'}}
assert len(failures)==97
for node,row in failures.items():
    assert 'test_study_publication_fail_closed' in node
    assert entering[node]==prior[node]==row,(node,entering.get(node),prior.get(node),row)
restored={node:{'entering':entering[node],'current':row} for node,row in broad.items() if row['outcome']=='passed' and node in entering and entering[node]['outcome'] in {'failure','error'}}
prior_restored={node for node,row in prior.items() if row['outcome']=='passed' and node in entering and entering[node]['outcome'] in {'failure','error'}}
unchecked=sorted(prior_restored-set(broad))
assert all(broad[n]['outcome']=='passed' for n in prior_restored & set(broad))
summary={'targeted':dict(collections.Counter(r['outcome'] for r in targeted.values())),'broad':dict(collections.Counter(r['outcome'] for r in broad.values())),'identical_historical_failures':len(failures),'author_current_first_restored':len(prior_restored),'author_restored_independently_replayed':len(prior_restored & set(broad)),'restored_nodes_excluded_for_write_safety':unchecked,'all_current_restored':len(restored)}
(out/'replay-comparison.json').write_text(json.dumps({'summary':summary,'historical_failure_matches':failures,'restored':restored},indent=2)+'\n')
print(json.dumps(summary,indent=2))
