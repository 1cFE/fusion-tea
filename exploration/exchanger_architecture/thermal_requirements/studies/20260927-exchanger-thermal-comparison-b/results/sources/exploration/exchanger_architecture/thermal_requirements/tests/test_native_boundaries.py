"""Native requirement-boundary mutations; fixtures are not study candidates."""
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('wi097_boundary_runner',HERE/'run.py')
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def test_native_hot_terminal_requirement_boundary():
    original=next(r for r in json.loads((runner.EVIDENCE/'native-controls.json').read_text()) if r['case']=='offer-b-0')
    gap=original['outputs'][runner.PREFIX+'heat_exchangers__evaluate__he_hot_terminal_difference']
    runtime=runner.load_runtime()
    receipts=[]
    for offset,expected,label in ((-1e-3,'satisfied','below'),(0.,'satisfied','equal'),(1e-3,'violated','above')):
        changes=original['effective_inputs']|{runner.PREFIX+'heat_exchangers__he_hot_approach':gap+offset}
        result=runner.execute_case('requirement-'+label,changes,runtime,runner.EVIDENCE/'native-boundary-runs')
        assert result['status']=='evaluated'
        assert result['outputs'][runner.PREFIX+'heat_exchangers__evaluate__he_hot_terminal_difference']==gap
        verdict=next(x for x in result['outputs']['constraint_report']['results'] if '__he_hot_approach_ok__' in x['constraint_id'])
        assert verdict['status']==expected
        receipts.append(result)
    (runner.EVIDENCE/'native-boundaries.json').write_text(json.dumps(receipts,indent=2)+'\n')
