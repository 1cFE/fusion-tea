"""Additional reviewer checks on restored bytes only; launched by inherited interpreter."""
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
from urllib.parse import quote

state=json.loads(Path(sys.argv[1]).read_text());root=Path(state['root']);review=Path(state['review'])
assert Path.cwd()==root
c=root/'.project/active/aries-comparison-preparation/current-readiness/candidate'
sys.path.insert(0,str(c))
from candidate_common import digest

def save(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n')

if sys.argv[2]=='stores':
    receipts=[]
    ident=json.loads((c/'candidate-identity.json').read_text())
    for case in ['selected-forward','table5-conditioned','held-cycle-diagnostic','held-calendar-incompatibility']:
        p=c/'evidence/final-cases'/case;n=json.loads((p/'native-result.json').read_text());db=p/'native/current-comparison-fixed-point.db';before=digest(db)
        con=sqlite3.connect('file:'+quote(str(db),safe='/')+'?mode=ro&immutable=1',uri=True);con.row_factory=sqlite3.Row
        rows=con.execute('select * from cases').fetchall();assert len(rows)==1
        row=dict(rows[0]);compat=dict(con.execute('select * from compatibility').fetchone())
        assert compat['executable_fingerprint']==ident['executable_fingerprint']
        assert compat['model_contract_fingerprint']==ident['semantic_fingerprint']
        assert row['candidate_id']==n['candidate_id'] and row['state']==n['state']
        assert n['attempt_id']==case  # Adapter attempt is the outer output-directory name; native store attempt is separate.
        transitions=con.execute('select distinct attempt_id,candidate_id from attempt_transitions').fetchall()
        assert [(v[0],v[1]) for v in transitions]==[(row['attempt_id'],row['candidate_id'])]
        assert json.loads(row['inputs_json'])==n['requested_overrides']
        receipt={'case':case,'store_sha256':before,'native_sha256':digest(p/'native-result.json'),'state':row['state'],'candidate_id':row['candidate_id'],'attempt_id':row['attempt_id']}
        if row['state']=='completed':
            a=p/'native/artifacts'/f"{row['evidence_digest']}.json";assert digest(a)==row['evidence_digest'];data=json.loads(a.read_text())
            assert data['outputs']==n['outputs']
            assert {k:v for k,v in data['responses'].items() if k!='headline'}==n['verdicts']
            assessment=json.loads(row['assessment_json']);assert assessment['headline']==data['responses']['headline']=='violated'
            assert assessment['coverage']['assessed_gate_count']==28
            for filename,field in [('independent-check.json','result_sha256'),('account-check.json','source_sha256')]:
                checked=json.loads((p/filename).read_text());assert checked['status']=='pass' and checked[field]==receipt['native_sha256']
            receipt.update(outputs=len(data['outputs']),predicates=len(n['verdicts']),raw_violations=[k for k,v in n['verdicts'].items() if v!='satisfied'],artifact_digest=row['evidence_digest'])
        else:
            failure=json.loads(row['failure_json']);disposition=json.loads((p/'disposition.json').read_text());assert failure==disposition['failure'];assert disposition['store_sha256']==before
            assert row['evidence_digest'] is None and row['assessment_json'] is None
            assert 'live calendar' in failure['cause'];receipt['failure']=failure
        con.close();assert digest(db)==before;receipts.append(receipt)
    save(review/'archived-case-joins.json',receipts)
    print('Four immutable archived stores join exact inputs, identities, artifacts/results or retained refusal')
elif sys.argv[2]=='custody':
    from compare_candidate import write_report
    from report_custody import FIRST,read_original
    native=review/'synthetic-blind-probe/native-result.json';n=json.loads(native.read_text());assert n['state']=='completed' and n['run_kind']=='blind'
    observations=review/'synthetic-observations.json'
    save(observations,{'schema_version':1,'run_kind':'blind','execution_status':'completed','constraints':{k:v=='satisfied' for k,v in n['verdicts'].items()},'extrapolations':[],'quantities':{}})
    register=review/'disposable-synthetic-register'
    options=dict(here=c,report_kind='forward',result_register=register,archive=Path(state['archive']),request=review/'synthetic-blind-probe/request.raw.json',model_export=review/'synthetic-blind-export.json')
    report,ok=write_report(root,native,observations,review/'synthetic-first-report.json',**options)
    assert ok and not report['publication_ready'] and report['engineering_evidence']['engineering_acceptance_withheld']
    first=(register/FIRST).read_bytes();receipt=read_original(register,register/FIRST)
    assert receipt['artifacts']['archive']['sha256']==state['archive_sha256'] and len(receipt['artifacts'])==12
    second,ok=write_report(root,native,observations,review/'synthetic-second-forward.json',**options)
    assert not ok and 'already registered' in second['error'];assert (register/FIRST).read_bytes()==first
    original=hashlib.sha256(first).hexdigest()
    follow=dict(options,report_kind='corrected',original_identity=register/FIRST,correction_reason='Synthetic custody probe only; no reference data or changed science.')
    corrected,ok=write_report(root,native,observations,review/'synthetic-corrected-report.json',**follow)
    assert ok and corrected['original_forward_result']['identity_sha256']==original
    assert (register/FIRST).read_bytes()==first
    assert not (root/c.parent.relative_to(root)/'revealed-results').exists()
    save(review/'actual-archive-custody.json',{'status':'pass','scope':'Synthetic empty observations against actual restored blind diagnostic; disposable register only, no reveal or adoption','archive_sha256':state['archive_sha256'],'first_identity_sha256':original,'artifact_joins':12,'second_forward':'refused; original bytes unchanged','corrected_followup':'joins original identity; original bytes unchanged','publication_ready':False})
    print('Actual archive joins12artifacts; secondforward refused; correctedfollowup retains original')
else:raise ValueError(sys.argv[2])
