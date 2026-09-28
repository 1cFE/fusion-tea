"""Read-only one-case reproduction; all runtime artifacts go to a fresh temp dir."""
import csv
import importlib.util
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path('/home/reid/1cfe/fusion-tea')
STUDIES = ROOT / 'exploration/stellarator_e2e/studies'
sys.path.insert(0, str(STUDIES))
import study_route as route
from simkit.core.pipeline_executor import SerialPipelineExecutor
from simkit.evaluation import evaluator
from simkit.study.evidence_io import decode_evidence
from stellarator_tea.modules.mfe_heating_chain.heating_power_chain import Heating_Power_ChainModule

work = Path(tempfile.mkdtemp(prefix='blank-study-column-'))
trace = {'work_dir': str(work)}
prefix = route.P + 'heat__'
target = prefix + 'p_coupled'
control = route.P + 'lcoe_calc__lcoe'

def snapshot(values):
    return {'keys': sorted(values), 'heating': {
        key: {'type': type(value).__name__, 'value': value}
        for key, value in values.items() if key.startswith(prefix)
    }, 'control': {'type': type(values[control]).__name__,
                   'value': getattr(values[control], 'root', values[control])}
       if control in values else None}

original_module = Heating_Power_ChainModule.run
def module_run(self, *args, **kwargs):
    result = original_module(self, *args, **kwargs)
    trace['module_result'] = {'type': type(result.data).__name__,
                              'fields': result.data.model_dump()}
    return result
Heating_Power_ChainModule.run = module_run

original_run = SerialPipelineExecutor.run
def execute(self, graph, context, **kwargs):
    result = original_run(self, graph, context, **kwargs)
    trace['pipeline_context'] = snapshot(context.channels)
    trace['run_result'] = snapshot(result.outputs)
    trace['run_result_types'] = {key: type(value).__name__ for key, value in result.outputs.items()}
    return result
SerialPipelineExecutor.run = execute

original_project = evaluator.project
def project(result, **kwargs):
    evidence = original_project(result, **kwargs)
    trace['model_evidence'] = snapshot(evidence.outputs)
    trace['provenance'] = evidence.provenance.model_dump(mode='json')
    return evidence
evaluator.project = project

spec = importlib.util.spec_from_file_location('historical_study', STUDIES / '20260903-wall-and-heating/study.py')
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)
base = study.BASE
_, point = study.point(base['eta_source_heat'], base['I_coil'], base['n_e0'],
                       base['T_i0'], base['p_wallplug_heat'], 'baseline-probe')
trace['proposal'] = point
cases, db = route.run_points('blank-column-reproduction', [point], work)
case = cases[0]
trace['case_state'] = case.state
trace['case_outputs'] = snapshot(case.outputs)
with sqlite3.connect(db) as connection:
    connection.row_factory = sqlite3.Row
    row = dict(connection.execute('SELECT * FROM cases').fetchone())
trace['store_row'] = row
artifacts = list(work.rglob(row['evidence_digest'] + '.json'))
assert len(artifacts) == 1, artifacts
stored = decode_evidence(json.loads(artifacts[0].read_text()))
trace['stored_evidence'] = snapshot(stored['outputs'])
trace['artifact_path'] = str(artifacts[0])

# Exercise the actual historical exporter after restoring one missing column in
# its in-memory declaration only. No source/package/study record is changed.
study.CHANNELS['p_coupled_probe'] = target
csv_path = study.export(cases, {study._key(case.inputs): 'baseline-probe'}, work / 'blank.csv')
with csv_path.open() as handle:
    exported = list(csv.DictReader(handle))
trace['actual_study_export'] = {'path': str(csv_path), 'cell': exported[0]['p_coupled_probe'], 'rows': len(exported)}

route.CHANNELS['p_coupled_probe'] = target
try:
    route.csv_rows(cases, ['R', 'a', 'availability'])
except route.RouteError as error:
    trace['shared_export_refusal'] = str(error)
else:
    raise AssertionError('shared exporter unexpectedly accepted missing channel')

assert case.state == 'completed'
assert trace['module_result']['fields']['p_coupled'] == 50.0
assert trace['run_result']['heating'][target]['value'] == 50.0
assert target not in case.outputs
assert control in case.outputs
assert trace['actual_study_export']['cell'] == ''
assert trace['model_evidence']['keys'] == trace['stored_evidence']['keys'] == trace['case_outputs']['keys']
output = Path(sys.argv[1]) if len(sys.argv) > 1 else work / 'trace.json'
output.write_text(json.dumps(trace, indent=2) + '\n')
print(json.dumps({'trace': str(output), 'work': str(work),
                  'module_result': trace['module_result'],
                  'heating_at_exit': trace['run_result']['heating'],
                  'counts': {stage: len(trace[stage]['keys']) for stage in ['pipeline_context', 'run_result', 'model_evidence', 'stored_evidence', 'case_outputs']},
                  'state': case.state, 'csv_cell': exported[0]['p_coupled_probe'],
                  'shared_refusal': trace['shared_export_refusal']}, indent=2))
