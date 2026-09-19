"""Stock native prepared-list study, inactive until accepted integration release."""
import json
from pathlib import Path
H=Path(__file__).resolve().parent

def release(require_rulings=True):
    authorization=json.loads((H/'preparation/execution-release.json').read_text())
    candidate=json.loads((H/'preparation/integration-return.json').read_text())
    if authorization.get('authorized_by')!='coordinator' or candidate.get('class')!='CANDIDATE':
        raise RuntimeError('Accepted native integration and coordinator execution release required')
    if not all(g['status']=='pass' for g in candidate['gates']):
        raise RuntimeError('Integration gates did not all pass')
    if authorization['candidate_pin']!=candidate['candidate']['pin']:
        raise RuntimeError('Execution release does not match candidate')
    if require_rulings:
        indicators=json.loads((H/'indicators.json').read_text())
        required={g['axis'] for g in indicators['groups'] if g['no_constraint_response']}
        rulings=json.loads((H/'preparation/owner-rulings.json').read_text())
        allowed={r['axis'] for r in rulings if r.get('authority')=='OWNER' and r.get('ruling') in ('sensitivity','declined') and r.get('evidence')}
        if not required <= allowed:raise RuntimeError('Missing owner ruling for unresisted axes: '+repr(sorted(required-allowed)))
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
    return route.run_points(H.name,proposals(),H/'results/study/_work',required_channels=channels())
