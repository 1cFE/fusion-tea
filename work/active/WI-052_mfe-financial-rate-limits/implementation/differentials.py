"""Match complete validation and regression identities, retaining raw evidence."""
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def identity(value):
    # Locations remain in raw records. Identity is diagnostic + logical file;
    # documentation edits can shift lines without changing an issue.
    value=re.sub(r'(?:file:)?(?:/tmp/fusion-mfe-financial-rate-limits/)?(?:exploration/stellarator_e2e/models/|models/|work/active/WI-052_mfe-financial-rate-limits/implementation/(?:entering/)?models/)', 'MODEL/',value)
    return re.sub(r'(:\d+)(?::\d+)?(?=\s|$)', '',value)

def validation():
    result={}
    for name in ('canonical','mirror'):
        old=json.loads((HERE/f'entering/issues-{name}.json').read_text());new=json.loads((HERE/f'issues-{name}.json').read_text())
        rows=[]
        for a,b in zip(old,new):
            before=Counter(identity(x) for x in a['issues']);after=Counter(identity(x) for x in b['issues'])
            rows.append({'level':a['level'],'retained':list((before&after).elements()),'repaired':list((before-after).elements()),'new':list((after-before).elements()),'entering_success':a['success'],'candidate_success':b['success']})
        result[name]=rows
    (HERE/'validation-differential.json').write_text(json.dumps(result,indent=2)+'\n')
    assert not any(r['new'] for rows in result.values() for r in rows), 'New validation issues'
    print('PASS every validation issue matched by diagnostic and logical location')

def tests(path):
    rows={}
    for case in ET.parse(path).getroot().iter('testcase'):
        node=case.attrib.get('classname','').replace('.','/')+'::'+case.attrib['name']
        status=next((x for x in ('failure','error','skipped') if case.find(x) is not None),'passed')
        rows[node]={'status':status,'message':case.find(status).attrib.get('message','') if status!='passed' else ''}
    return rows

def regression():
    result={}
    for name in ('models','study'):
        old=tests(HERE/f'entering/pytest-{name}.xml');new=tests(HERE/f'pytest-{name}.xml')
        retained={k:{'entering':v,'candidate':new[k]} for k,v in old.items() if v['status']!='passed' and k in new and new[k]['status']==v['status']}
        repaired={k:v for k,v in old.items() if v['status']!='passed' and k in new and new[k]['status']=='passed'}
        fresh={k:v for k,v in new.items() if v['status'] in ('failure','error') and (k not in old or old[k]['status'] not in ('failure','error'))}
        result[name]={'retained':retained,'repaired':repaired,'new_failures':fresh,'removed_nodes':sorted(set(old)-set(new)),'new_nodes':sorted(set(new)-set(old))}
    (HERE/'regression-differential.json').write_text(json.dumps(result,indent=2)+'\n')
    assert not any(x['new_failures'] for x in result.values()),'New regression failures'
    print('PASS individual regression identity comparison')
if __name__=='__main__':
    validation()
    if (HERE/'pytest-study.xml').exists():regression()
