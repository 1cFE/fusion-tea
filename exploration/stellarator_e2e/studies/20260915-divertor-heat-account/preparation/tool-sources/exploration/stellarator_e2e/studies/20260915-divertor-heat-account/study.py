"""Stock native prepared-list definition, usable only after coordinator release."""
import json
from pathlib import Path

H = Path(__file__).resolve().parent


def proposals():
    rows = json.loads((H / 'preparation/unique-proposals.json').read_text())
    assert 0 < len(rows) <= 40
    return [row['point'] for row in rows]


def channels():
    from exploration.stellarator_e2e.studies import study_route as route
    keys = json.loads((H / 'preparation/required-channels.json').read_text())
    return {key[len(route.P):]: key for key in keys}


def run():
    release = json.loads((H / 'preparation/execution-release.json').read_text())
    candidate = json.loads((H / 'preparation/integration-return.json').read_text())
    assert release['authorized_by'] == 'coordinator'
    assert candidate['class'] == 'CANDIDATE'
    assert all(gate['status'] == 'pass' for gate in candidate['gates'])
    assert release['candidate_pin'] == candidate['candidate']['pin']
    from exploration.stellarator_e2e.studies import study_route as route
    return route.run_points(H.name, proposals(), H / 'results/study/_work',
                            required_channels=channels())
