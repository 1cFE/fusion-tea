from pathlib import Path
import sys
from types import SimpleNamespace
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from diagnose import predicate_records


def test_unknown_predicate_token_refuses():
    evidence=SimpleNamespace(publications={'evaluation':{'status':'available_structured','structured_value':{'status':'new_unknown_token'}}})
    contract={'constraint_catalog':{'concrete_entries':[{'constraint_id':'id','evaluation_channel':'evaluation'}]}}
    with pytest.raises(ValueError,match='unsupported native predicate status'):predicate_records(evidence,contract)


def test_false_unknown_and_missing_are_distinct():
    evidence=SimpleNamespace(publications={
        'false':{'status':'available_structured','structured_value':{'status':'violated'}},
        'unknown':{'status':'available_structured','structured_value':{'status':'indeterminate'}},
        'blocked':{'status':'blocked_dependency','root_causes':['root']}})
    contract={'constraint_catalog':{'concrete_entries':[{'constraint_id':name,'evaluation_channel':name} for name in ('false','unknown','blocked','missing')]}}
    records=predicate_records(evidence,contract)
    assert {k:v['status'] for k,v in records.items()}=={'false':'violated','unknown':'indeterminate','blocked':'unavailable','missing':'unavailable'}
