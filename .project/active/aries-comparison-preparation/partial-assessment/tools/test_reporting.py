"""Report tests consume retained synthetic evidence; no reference evaluation."""
import copy
import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_qualification import case
from qualification import qualify
from definedness import GUARDS, P, assess_definedness
from reporting import build_report

COMPARISON = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


@pytest.fixture
def materials(case):
    graph, _, contract = case
    diagnostic = read(COMPARISON / 'post-reveal-investigation/failure-propagation/evidence/synthetic-v2/partial-diagnostic.json')
    manifest = read(COMPARISON / 'post-reveal-preparation/tools/historical-manifest.json')
    overlay = read(COMPARISON / 'post-reveal-preparation/tools/current-overlay.json')
    selection = read(COMPARISON / 'post-reveal-results/post-reveal-v1/attempts/first-forward/selection.json')
    observations = read(COMPARISON / 'post-reveal-results/post-reveal-v1/observations.json')
    return graph, diagnostic, contract, manifest, overlay, selection, observations


def report(materials):
    graph, diagnostic, contract, manifest, overlay, selection, observations = materials
    qualification = qualify(graph, diagnostic, contract)
    definedness = assess_definedness(graph, diagnostic)
    return build_report(diagnostic, qualification, selection, manifest, overlay, observations, contract, definedness)


def test_preserves_rows_native_verdicts_and_never_certifies(materials):
    result = report(materials)
    assert [r['id'] for r in result['rows']] == [q['id'] for q in materials[3]['quantities']]
    assert result['predicate_counts'] == {'satisfied': 61, 'violated': 5, 'unavailable': 1}
    assert len(result['predicates']) == 67
    assert all(r['supported_prediction'] is None and r['comparison_ratio'] is None for r in result['rows'])
    assert all(not p['engineering_acceptance'] for p in result['predicates'].values())
    lcoe = [r for r in result['rows'] if any(p.endswith('__lcoe') for p in r['producers'])]
    assert lcoe and all(r['raw_arithmetic'] is not None and r['field_qualification']['causes'] for r in lcoe)
    assert any(r['role'] == 'held' and r['raw_arithmetic'] is not None and
               r['field_qualification']['field_applicability'] == 'unaffected_by_field_finding' for r in result['rows'])


@pytest.mark.parametrize('value,expected', [(0, 'undefined'), (None, 'unknown'), (2, 'unknown'), (1, 'defined')])
def test_guard_suppresses_carrier_and_downstream(value, expected, materials):
    graph, diagnostic, *_ = materials
    flag = P + 'fuel_cycle__processing_cost__defined_flag'
    if value is None:
        diagnostic['numeric_outputs'].pop(flag)
    else:
        diagnostic['numeric_outputs'][flag] = value
    guarded = assess_definedness(graph, diagnostic)['publications']
    lcoe = P + 'lcoe_calc__lcoe'
    assert flag in guarded[lcoe]['guards']
    assert guarded[lcoe]['model_definedness'] == expected
    result = report(materials)
    rows = [r for r in result['rows'] if lcoe in r['producers']]
    assert rows and all(r['raw_arithmetic'] is not None for r in rows)
    assert all(r['diagnostic_value'] is None for r in rows) if value != 1 else all(r['diagnostic_value'] is not None for r in rows)
    assert all(r['supported_prediction'] is None for r in rows)


def test_ua_guard_is_specific_not_whole_cycle(materials):
    graph, diagnostic, *_ = materials
    flag = P + 'turbine__matched_cycle__main_UA_available'
    diagnostic['numeric_outputs'][flag] = 0
    records = assess_definedness(graph, diagnostic)['publications']
    assert records[P + 'turbine__matched_cycle__main_UA_MW_K']['model_definedness'] == 'undefined'
    assert flag not in records[P + 'turbine__matched_cycle__reheat_UA_MW_K']['guards']
    assert flag not in records[P + 'lcoe_calc__lcoe']['guards']


def test_guard_inventory_refuses_missing_flag(materials):
    graph, diagnostic, *_ = materials
    del diagnostic['publications'][next(iter(GUARDS))]
    with pytest.raises(ValueError, match='missing pinned'):
        assess_definedness(graph, diagnostic)


def test_indeterminate_and_bad_predicate_are_not_pass(materials):
    graph, diagnostic, contract, *_ = materials
    channel = contract['constraint_catalog']['concrete_entries'][0]['evaluation_channel']
    diagnostic['publications'][channel].update(status='available_structured', structured_value={'status': 'indeterminate'})
    assert report(materials)['predicate_counts']['indeterminate'] == 1
    diagnostic['publications'][channel]['structured_value']['status'] = 'probably_passed'
    with pytest.raises(ValueError, match='vocabulary'):
        report(materials)
