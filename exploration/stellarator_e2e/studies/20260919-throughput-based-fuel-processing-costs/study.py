"""Stock native prepared-list study, inactive until accepted integration release."""
import json
from pathlib import Path
H=Path(__file__).resolve().parent

def release():
    authorization=json.loads((H/'preparation/execution-release.json').read_text())
    candidate=json.loads((H/'preparation/integration-return.json').read_text())
    if authorization.get('authorized_by')!='coordinator' or candidate.get('class')!='CANDIDATE':
        raise RuntimeError('Accepted native integration and coordinator execution release required')
    if not all(g['status']=='pass' for g in candidate['gates']):
        raise RuntimeError('Integration gates did not all pass')
    if authorization['candidate_pin']!=candidate['candidate']['pin']:
        raise RuntimeError('Execution release does not match candidate')
    return candidate

def proposals():
    return [r['point'] for r in json.loads((H/'preparation/proposals.json').read_text())]

def channels():
    from exploration.stellarator_e2e.studies import study_route as route
    keys=json.loads((H/'preparation/required-channels.json').read_text())
    return {key.removeprefix(route.P):key for key in keys}

def run():
    release()
    from exploration.stellarator_e2e.studies import study_route as route
    return route.run_points(H.name,proposals(),H/'results/study/retry-1',required_channels=channels())
