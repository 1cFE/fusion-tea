"""Compound breeding guard must trace and independently evaluate both branches."""
import json
from pathlib import Path
import pytest
from scripts.study import indicators, verify

ROOT=Path(__file__).resolve().parents[2]

def entry():
    contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    return next(e for e in contract['constraint_catalog']['concrete_entries'] if e['source_local_identity']=='tbr_ok')

def test_actual_predicate_traces_both_guards():
    operator,leaves=indicators.predicate_operands(entry())
    assert operator=='and'
    assert leaves==[{'kind':'feature_ref','name':'defined_in'},{'kind':'literal','value':1.0},
                    {'kind':'feature_ref','name':'numerical_margin_in'},{'kind':'literal','value':0.0}]

@pytest.mark.parametrize('defined,margin,expected',[(1.,0.,True),(1.,-.01,False),(0.,1.,False),(0.,0.,False)])
def test_independent_conjunction_and_negation(defined,margin,expected):
    e=entry();cid=e['constraint_id']
    bindings={cid:{'defined_in':{'kind':'channel','key':'valid'},'numerical_margin_in':{'kind':'channel','key':'margin'}}}
    channels={'valid':defined,'margin':margin}
    assert verify.derive_verdict(cid,e,bindings,{}, {},channels)==(expected,2)
    e['is_negated']=True
    assert verify.derive_verdict(cid,e,bindings,{}, {},channels)==(not expected,2)

def test_false_first_branch_does_not_hide_missing_evidence():
    e=entry();cid=e['constraint_id']
    bindings={cid:{'defined_in':{'kind':'channel','key':'valid'},'numerical_margin_in':{'kind':'channel','key':'margin'}}}
    with pytest.raises(verify.VerifyError,match='oracle did not return'):
        verify.derive_verdict(cid,e,bindings,{}, {},{'valid':0.})

@pytest.mark.parametrize('arity',[0,1,3])
def test_malformed_conjunction_refused(arity):
    e=entry();ir=json.loads(e['predicate_ir']);ir['operands']=[ir['operands'][0]]*arity;e['predicate_ir']=json.dumps(ir)
    with pytest.raises(indicators.IndicatorError,match='exactly two'):
        indicators.predicate_operands(e)
    with pytest.raises(verify.VerifyError,match='exactly two'):
        verify.derive_verdict(e['constraint_id'],e,{}, {}, {},{})
