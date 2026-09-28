"""Synthetic native diagnostic verification only; accepts no reference request."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE/'native-teax'))
from simkit.evaluation.failure import EvaluationFailed
from simkit.study.bridge import CandidateBridge
from exploration.stellarator_e2e.studies import study_route as route


def predicate_records(evidence,contract):
    records={}
    for entry in contract['constraint_catalog']['concrete_entries']:
        channel=entry['evaluation_channel'];publication=evidence.publications.get(channel)
        if publication is None or publication['status']!='available_structured':
            records[entry['constraint_id']]={'status':'unavailable','reason':dict(publication) if publication else 'missing publication'}
            continue
        value=publication['structured_value'];status=value.get('status')
        if status not in ('satisfied','violated','indeterminate'):
            raise ValueError('unsupported native predicate status: '+repr(status))
        records[entry['constraint_id']]={'status':status,'native_evaluation':value}
    return records


def write(path,value):
    from simkit.evaluation.diagnostics import plain
    with Path(path).open('x') as stream:json.dump(plain(value),stream,indent=2,sort_keys=True,allow_nan=False);stream.write('\n')


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    prepared=route.prepare(route.PACKAGE_DIR,out)
    contract=json.loads((route.PACKAGE_DIR/'contracts/model_contract.json').read_text())
    typed=CandidateBridge(prepared.entry_models).build({})
    baseline=prepared.evaluate(typed)
    complete=prepared.diagnose(typed)
    assert dict(complete.numeric_outputs)==dict(baseline.outputs)
    baseline_predicates=predicate_records(complete,contract)
    assert {k:v['status'] for k,v in baseline_predicates.items()}=={k:v for k,v in baseline.responses.items() if k!='headline'}
    write(out/'baseline-diagnostic.json',complete.to_document())
    failed='stellarator_09__stellaris__magnet__conductor_current'
    original=prepared._executor._execute_module
    def injection(key,spec,context):
        if key==failed:raise ValueError('synthetic conductor fault; unchanged baseline inputs')
        return original(key,spec,context)
    with patch.object(prepared._executor,'_execute_module',injection):
        try:prepared.evaluate(typed)
        except EvaluationFailed as exc:write(out/'ordinary-failure.json',exc.failure.model_dump(mode='json'))
        else:raise AssertionError('ordinary evaluation stopped failing')
        partial=prepared.diagnose(typed)
    records=predicate_records(partial,contract)
    assert all(value==baseline.outputs[key] for key,value in partial.numeric_outputs.items())
    assert all(record['status']==baseline_predicates[key]['status'] for key,record in records.items() if record['status']!='unavailable')
    # Fresh diagnostic context after a prior fault must recover the original baseline exactly.
    recovered=prepared.diagnose(typed)
    assert recovered.to_document()==complete.to_document()
    write(out/'partial-diagnostic.json',partial.to_document())
    overlay=json.loads((ROOT/'.project/active/model-evaluation-comparison-adapter/v1/current-overlay.json').read_text())
    definedness={}
    for key,flags in overlay.get('defined_when',{}).items():
        values={flag:partial.numeric_outputs.get(flag) for flag in flags}
        status='unavailable' if any(v not in (0.,1.) for v in values.values()) else 'defined' if all(values.values()) else 'undefined'
        definedness[key]={'model_definedness':status,'flags':values}
    invalid_input_refused=False
    try:prepared.diagnose({})
    except EvaluationFailed as exc:invalid_input_refused=exc.failure.phase.value=='entry_validation'
    assert invalid_input_refused
    receipt={'purpose':'synthetic diagnostic verification; no reference execution',
        'scientific_qualification':'not_established','engineering_acceptance_withheld':True,
        'qualification':'Conductor-independent is not field-independent. This test demonstrates execution continuation at unchanged synthetic baseline; it does not establish scientific transfer to reference geometry.',
        'baseline_numeric_count':len(baseline.outputs),'baseline_predicate_count':len(baseline_predicates),
        'retained_numeric_count':len(partial.numeric_outputs),'available_predicate_count':sum(r['status']!='unavailable' for r in records.values()),
        'unavailable_predicate_count':sum(r['status']=='unavailable' for r in records.values()),
        'violated_predicate_count':sum(r['status']=='violated' for r in records.values()),
        'partial_state':partial.state,'retained_numeric_exact_baseline_match':True,'retained_predicates_exact_baseline_match':True,
        'fresh_context_exact_baseline_match':True,'invalid_input_refused':invalid_input_refused,
        'native_predicates':records,'model_definedness':definedness,
        'conditional_economic_arithmetic':{k:v for k,v in partial.numeric_outputs.items() if k.endswith('__lcoe')},
        'native_source_digest':partial.provenance['native_source_digest'],
        'artifacts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}}
    write(out/'verification.json',receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('native_predicates','model_definedness','artifacts')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path)
    run(p.parse_args().out)
