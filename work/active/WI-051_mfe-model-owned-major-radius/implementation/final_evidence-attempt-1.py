"""Retain location-aware diagnostics, regression deltas and exact production protection."""
import difflib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from common import H, ROOT, ITEM, PRODUCTION, hashes, sha, dump
from prepare import protected


def full_differential():
    from agentic_mbse.validation.level2_structure import validate_structure
    from agentic_mbse.validation.level6_architecture import validate_architecture
    maps={}
    for source in (H/'models').rglob('*.sysml'):
        relative=str(source.relative_to(H/'models'))
        old=(H/'entering-models'/relative).read_text().splitlines()
        new=source.read_text().splitlines()
        mapping={}
        for block in difflib.SequenceMatcher(a=old,b=new,autojunk=False).get_matching_blocks():
            for offset in range(block.size): mapping[block.b+offset+1]=block.a+offset+1
        maps[relative]=mapping
    report={}
    for level,fn in [('L2',validate_structure),('L6',validate_architecture)]:
        all_rows={}
        for side,root in [('before',H/'entering-models'),('after',H/'models')]:
            rows=[]
            for issue in fn(str(root)).issues:
                raw=str(issue.message if hasattr(issue,'message') else issue)
                normalized=raw.replace(str(root)+'/', '')
                match=re.search(r' at file:(.*\.sysml):(\d+)',normalized)
                location=None
                if match:
                    relative,line=match.group(1),int(match.group(2))
                    mapped=line if side=='before' else maps[relative].get(line)
                    location={'file':relative,'line':line,'entering_line':mapped}
                    # Only identical source lines are mapped; a diagnostic on a changed
                    # statement cannot disappear under permissive line normalization.
                    replacement=f' at file:{relative}:{mapped if mapped is not None else "CHANGED-"+str(line)}'
                    normalized=normalized[:match.start()]+replacement+normalized[match.end():]
                rows.append({'raw':raw,'normalized':normalized,'affected_location':location})
            all_rows[side]=rows
        a,b=(Counter(r['normalized'] for r in all_rows[side]) for side in ('before','after'))
        report[level]={'before_count':sum(a.values()),'after_count':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements()),'inherited':dict(a&b),'diagnostics':all_rows}
    dump('full-validation-diff.json',report)
    assert all(not r['added'] and not r['removed'] for r in report.values())
    assert report['L2']['after_count']==10 and report['L6']['after_count']==229


def test_nodes(path):
    result={}
    for node in ET.parse(path).getroot().iter('testcase'):
        key=node.attrib['classname'].replace('.','/')+'.py::'+node.attrib['name']
        child=next((c for c in node if c.tag in ('failure','error','skipped')),None)
        result[key]={'outcome':child.tag if child is not None else 'passed','reason':child.attrib.get('message','') if child is not None else ''}
    return result


def regression():
    a=test_nodes(H/'entering-tests.xml');b=test_nodes(H/'final-tests-attempt-1.xml')
    report={'entering':a,'final':b,'added':{k:b[k] for k in b.keys()-a.keys()},'removed':{k:a[k] for k in a.keys()-b.keys()},'changed':{k:{'before':a[k],'after':b[k]} for k in a.keys()&b.keys() if a[k]!=b[k]},'inherited':{k:a[k] for k in a.keys()&b.keys() if a[k]==b[k]},'entering_counts':dict(Counter(x['outcome'] for x in a.values())),'final_counts':dict(Counter(x['outcome'] for x in b.values()))}
    dump('regression-diff.json',report)
    assert not report['removed'] and not report['changed']
    assert all(r['outcome']=='passed' for r in report['added'].values())


def preservation():
    before=json.loads((H/'protected-before.json').read_text());after=protected()
    changed={k:{'before':before.get(k),'after':after.get(k)} for k in before.keys()|after.keys() if before.get(k)!=after.get(k)}
    dump('protected-final.json',after)
    dump('protection-diff.json',{'entering_count':len(before),'final_count':len(after),'changed':changed})
    assert not changed
    pkg=hashes(PRODUCTION)
    assert pkg==json.loads((H/'production-hashes.json').read_text())==hashes(H/'source-attempt-1')==hashes(H/'snapshot-attempt-1')
    assert hashes(H/'models')==json.loads((H/'source-hashes.json').read_text())
    assert sha(ROOT/'exploration/stellarator_e2e/stellarator.snapshot.json')==sha(H/'instance_graph_snapshot.json')
    from tests.model_families import MFE,canonical_path
    assert all(canonical_path(p).read_bytes()==(MFE.twin/p).read_bytes()==(H/'models'/p).read_bytes() for p in MFE.owned)
    dump('final-identities.json',{'semantic_fingerprint':json.loads((PRODUCTION/'contracts/model_contract.json').read_text())['semantic_fingerprint'],'executable_fingerprint':json.loads((H/'acceptance-attempt-2/contract-delta.json').read_text())['executable_fingerprint'],'package_files':pkg,'source_files':hashes(H/'models'),'snapshot_sha256':sha(H/'instance_graph_snapshot.json'),'manual':json.loads((H/'generation.json').read_text())['manual'],'protected_entries':len(after)})
    (H/'final-status.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=ROOT))

if __name__=='__main__':
    import sys
    sys.path.insert(0,str(ROOT))
    full_differential()
    regression()
    preservation()
    print('PASS full location-aware diagnostic differential, per-node regression and protected/package equality')
