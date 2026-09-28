import importlib.util
import json
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).parent))
import adapter as a
import report as r
import observations as o


def test_explicit_post_reveal_selection():
    rows=a.strict((a.HERE/'mapping.json').read_bytes())['inputs']
    base={row['key']:1 for row in rows}
    point,selection=a.select({'schema_version':'adapter-request/v1','purpose':'post_reveal_comparison','values':{}},base)
    assert point=={} and selection['held_fallback'] and not selection['fully_reference_specified']
    with pytest.raises(ValueError):a.select({'schema_version':'adapter-request/v1','purpose':'blind','values':{}},base)


def test_interrupted_first_report(tmp_path,monkeypatch):
    monkeypatch.setattr(a,'verify_identity',lambda:None)
    first,_=a.reserve(tmp_path/'attempts','first')
    a.reserve(tmp_path/'attempts','second')
    obs=tmp_path/'observations.json';a.document(obs,o.template(first))
    report=r.report(first,obs,tmp_path/'reports','first')
    assert report['state']=='reported',report
    assert report['interrupted']
    assert len(report['numerical_comparison']['rows'])==276
    assert all(row['status']=='blocked' for row in report['numerical_comparison']['rows'])
    assert report['first_execution_attempt']['attempt']=='first'
    with pytest.raises(FileExistsError):r.report(first,obs,tmp_path/'reports','first')


def test_duplicate_request_and_bad_definition():
    with pytest.raises(ValueError):a.strict('{"x":1,"x":2}')
    row=a.strict((a.HERE/'mapping.json').read_bytes())['inputs'][0]
    request={'schema_version':'adapter-request/v1','purpose':'post_reveal_comparison','values':{row['key']:{'value':1,'unit':row['unit'],'definition':'wrong','resolution':'matched','source':'synthetic test'}}}
    with pytest.raises(ValueError):a.select(request,{row['key']:1})


def retained_fixture(tmp_path,monkeypatch,state='completed'):
    monkeypatch.setattr(a,'verify_identity',lambda:None)
    attempt,first=a.reserve(tmp_path/'attempts','first')
    manifest=a.strict((a.HERE/'historical-manifest.json').read_bytes())
    contract=a.strict((a.PACKAGE/'contracts/model_contract.json').read_bytes())
    native={'state':state,'first_attempt':first,'outputs':{},'effective_inputs':{},'input_roles':{},'verdicts':{},'identity_sha256':a.sha(a.HERE/'identity.json')}
    if state=='completed':
        native['effective_inputs']=a.defaults(contract)
        native['input_roles']={k:'held' for k in native['effective_inputs']}
        native['outputs']={row['channel_name']:1 for row in contract['outputs']}
        native['verdicts']={row['constraint_id']:'satisfied' for row in contract['constraint_catalog']['concrete_entries']}
    a.document(attempt/'result.json',native)
    a.document(attempt/'model-export.json',a.export(native,manifest,contract))
    a.document(attempt/'receipt.json',{'artifacts':{p.name:a.sha(p) for p in attempt.iterdir()}})
    return attempt


def test_complete_report_and_native_mismatch(tmp_path,monkeypatch):
    attempt=retained_fixture(tmp_path,monkeypatch)
    obs=o.template(attempt);path=tmp_path/'obs.json';a.document(path,obs)
    result=r.report(attempt,path,tmp_path/'reports','ok')
    assert result['state']=='reported',result
    assert len(result['current_predicates'])==67
    assert result['numerical_comparison']['constraints_complete']
    row=next(row for row in obs['quantities'].values() if row['model_valid'])
    row['model']['value']+=1
    bad=tmp_path/'bad.json';a.document(bad,obs)
    assert r.report(attempt,bad,tmp_path/'reports','bad')['state']=='report_refused'


def test_refused_native_and_undefined_cannot_be_restored(tmp_path,monkeypatch):
    attempt=retained_fixture(tmp_path,monkeypatch,'execution_refused')
    obs=o.template(attempt);path=tmp_path/'obs.json';a.document(path,obs)
    result=r.report(attempt,path,tmp_path/'reports','refusal')
    assert result['state']=='reported',result
    assert len(result['numerical_comparison']['rows'])==276
    row=obs['quantities']['major_radius'];row['model']['value']=1;row['model_valid']=True
    bad=tmp_path/'bad.json';a.document(bad,obs)
    assert r.report(attempt,bad,tmp_path/'reports','fabrication')['state']=='report_refused'


def test_tampered_pointer_and_attempt(tmp_path,monkeypatch):
    attempt=retained_fixture(tmp_path,monkeypatch)
    path=tmp_path/'obs.json';a.document(path,o.template(attempt))
    pointer=attempt.parent/'first-attempt.json';original=pointer.read_bytes();pointer.write_text('{"schema_version":"first-attempt/v1","attempt":"different"}')
    assert r.report(attempt,path,tmp_path/'reports','pointer')['state']=='report_refused'
    pointer.write_bytes(original)
    (attempt/'result.json').write_text('{}')
    assert r.report(attempt,path,tmp_path/'reports','tamper')['state']=='report_refused'


def test_absent_attempt_is_not_interruption(tmp_path,monkeypatch):
    monkeypatch.setattr(a,'verify_identity',lambda:None)
    first,_=a.reserve(tmp_path/'attempts','first')
    obs=tmp_path/'obs.json';a.document(obs,o.template(first))
    result=r.report(tmp_path/'attempts'/'missing',obs,tmp_path/'reports','missing')
    assert result['state']=='report_refused'


@pytest.mark.parametrize('partial', ['{', '{"state":"completed"}'])
def test_interrupted_terminal_writes_are_unavailable(tmp_path,monkeypatch,partial):
    monkeypatch.setattr(a,'verify_identity',lambda:None)
    first,_=a.reserve(tmp_path/'attempts','first')
    (first/'result.json').write_text(partial)
    obs=tmp_path/'obs.json';a.document(obs,o.template(first))
    result=r.report(first,obs,tmp_path/'reports','incomplete')
    assert result['state']=='reported',result
    assert result['interrupted'] and len(result['numerical_comparison']['rows'])==276
    assert all(row['status']=='blocked' for row in result['numerical_comparison']['rows'])
