"""One stock native study over the deduplicated proposal list; no evaluator loop."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
H=Path(__file__).resolve().parent

def proposals():
 return [r['point'] for r in json.loads((H/'preparation/unique-proposals.json').read_text())]

def channels():
 return {k[len(route.P):]:k for k in json.loads((H/'preparation/required-channels.json').read_text())}

def run():
 return route.run_points(H.name,proposals(),H/'results/study/_work',required_channels=channels())
