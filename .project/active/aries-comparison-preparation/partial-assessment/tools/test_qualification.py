"""Real generated DAG checks; no plant/reference execution."""
import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / 'post-reveal-investigation/failure-propagation/native-teax'))
from simkit.config.pipeline_schema import PipelineSpecLoader
from simkit.core.pipeline_graph import PipelineDagBuilder
from qualification import ROOTS, combine_qualifications, qualify


@pytest.fixture
def case():
    package = ROOT / 'exploration/stellarator_e2e/generated'
    graph = PipelineDagBuilder().build(PipelineSpecLoader().load(package / 'pipelines/pipeline.yaml'))
    contract = json.loads((package / 'contracts/model_contract.json').read_text())
    exit_spec = next(spec for spec in graph.spec.modules.values() if spec.is_exit)
    observations = {'publications': {
        key: {'channel': binding.channel_name, 'producer': graph.channel_providers[binding.channel_name],
              'status': 'available_numeric'} for key, binding in exit_spec.outputs.items()
    }}
    return graph, observations, contract


def test_real_graph_transitive_paths_and_unaffected_retention(case):
    graph, observations, contract = case
    result = qualify(*case)
    assert len(result['publications']) == len(observations['publications'])
    assert len(result['predicates']) == 67
    assert any(record['field_applicability'] == 'unaffected_by_field_finding'
               for record in result['publications'].values())
    assert any(record["producer"].endswith("__lcoe_calc") and record['causes']
               for record in result['publications'].values())
    for publication in result['publications'].values():
        for cause in publication['causes']:
            assert cause['path'][0] == ROOTS[cause['root']]['module']
            assert cause['path'][-1] == publication['producer']
            assert all(right in graph.adjacency[left] for left, right in zip(cause['path'], cause['path'][1:]))
    for name, root in ROOTS.items():
        own = result['publications'][root['channel']]
        assert any(cause['root'] == name and cause['path'] == [root['module']] for cause in own['causes'])
    peak = result['publications'][ROOTS['peak_field']['channel']]
    assert {cause['root'] for cause in peak['causes']} == {'axis_field', 'peak_field'}
    independent = result['publications']['stellarator_09__stellaris__magnet__winding_state__I_coil']
    assert independent['field_applicability'] == 'unaffected_by_field_finding'
    assert independent['causes'] == []


def test_root_execution_failure_never_erases_scientific_paths(case):
    before = qualify(*case)
    graph, observations, contract = case
    for publication in observations['publications'].values():
        if publication['producer'] == ROOTS['axis_field']['module']:
            publication['status'] = 'unavailable_module_error'
    after = qualify(*case)
    for key in before['publications']:
        assert before['publications'][key]['causes'] == after['publications'][key]['causes']
    root = after['publications'][ROOTS['axis_field']['channel']]
    assert root['execution_status'] == 'unavailable_module_error'
    assert root['field_applicability'] == 'unknown_unqualified'


@pytest.mark.parametrize('name', ROOTS)
@pytest.mark.parametrize('damage', ['missing', 'ambiguous', 'wrong_channel'])
def test_root_completeness_fails_closed(case, name, damage):
    graph, observations, contract = case
    spec = graph.spec.modules[ROOTS[name]['module']]
    if damage == 'missing':
        del graph.spec.modules[spec.key]
    elif damage == 'ambiguous':
        graph.spec.modules['unexpected_second_root'] = spec.model_copy(update={'key': 'unexpected_second_root'})
    else:
        spec.outputs['root'] = spec.outputs['root'].model_copy(update={'channel_name': 'wrong'})
    with pytest.raises(ValueError, match='pinned|Pinned'):
        qualify(graph, observations, contract)


def test_predicate_and_diagnostic_coverage_fail_closed(case):
    graph, observations, contract = case
    del observations['publications'][next(iter(observations['publications']))]
    with pytest.raises(ValueError, match='coverage'):
        qualify(*case)


def test_combining_producer_and_flag_preserves_all_roots(case):
    result = qualify(*case)['publications']
    unaffected = next(record for record in result.values() if not record['causes'])
    affected = result[ROOTS['peak_field']['channel']]
    combined = combine_qualifications([unaffected, affected, affected])
    assert combined['field_applicability'] == 'unknown_unqualified'
    assert {cause['root'] for cause in combined['causes']} == set(ROOTS)
    assert len(combined['causes']) == 2
    assert combine_qualifications([unaffected])['field_applicability'] == 'unaffected_by_field_finding'
    with pytest.raises(ValueError, match='empty'):
        combine_qualifications([])
