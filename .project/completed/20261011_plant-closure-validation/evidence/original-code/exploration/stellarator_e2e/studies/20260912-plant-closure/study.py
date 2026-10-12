"""One native PreparedListStrategy study; no custom execution loop."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
H=Path(__file__).resolve().parent

def proposals():
    assert json.loads((H/'preparation/reduced-window-freeze.json').read_text())['frozen'] is True
    return json.loads((H/'preparation/reduced-proposals.json').read_text())

def channels():
    return json.loads((H/'preparation/required-channels.json').read_text())

def run():
    return route.run_points(H.name, proposals(), H/'results/targeted-store', required_channels=channels())
