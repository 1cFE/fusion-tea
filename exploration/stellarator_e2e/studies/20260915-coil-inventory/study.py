"""One native PreparedListStrategy study over the union of the three arms' points, one store; no custom loop.
Proposals are the unique bare point dicts of preparation/proposals.json; arms are joined back by exact coordinates."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
H = Path(__file__).resolve().parent
ARMS = ('arm-a-transect', 'arm-R-transect', 'arm-matched-window', 'arm-assumptions')

def _key(p): return json.dumps({k: float(v) for k, v in p.items()}, sort_keys=True)

def proposals():
    seen, out = set(), []
    for arm in ARMS:
        for r in json.loads((H / 'preparation/proposals.json').read_text())[arm]:
            k = _key(r['point'])
            if k not in seen: seen.add(k); out.append(dict(r['point']))
    return out

def channels():
    req = json.loads((H / 'preparation/required-channels.json').read_text())
    return {k.split('stellarator_09__stellaris__', 1)[1]: k for k in req}

def run():
    return route.run_points(H.name, proposals(), H / 'results/study/_work', required_channels=channels())
