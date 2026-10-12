"""One R-only PreparedListStrategy definition on the stock lifecycle."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
HERE=Path(__file__).resolve().parent

def proposals():
    window=json.loads((HERE/'preparation/window-freeze.json').read_text())
    return [{route.P+'R':r} for r in window['R_m']]

def channels():
    expected=json.loads((HERE/'context/expectations.json').read_text())
    return {key.removeprefix(route.P):key for key in expected['channels']}

def run():
    return route.run_points(HERE.name,proposals(),HERE/'results/store',required_channels=channels())
