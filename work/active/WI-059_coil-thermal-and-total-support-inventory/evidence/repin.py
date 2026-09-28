"""WI-059 producer metadata, derived from the completed package and native baseline."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from scripts.study import manifest as m
from scripts.integrate import rederived_census
pkg=ROOT/'exploration/stellarator_e2e/generated'
p=ROOT/'exploration/stellarator_e2e/studies/manifest.json'
d=json.loads(p.read_text()); fp=m.indicator_input_fingerprint(pkg)
d['fingerprints']['indicator_inputs']=fp|{'files':[x['path'] for x in fp['files']]}
semantic=m.read_semantic_fingerprint(pkg)
d['fingerprints']['recorded_provenance']={'semantic_fingerprint':semantic,'executable_fingerprint':m.read_executable_fingerprint(pkg)}
# Native single agrees with independent oracle at this value (native log retained).
d['baseline']['headline']['value']=146.30855606334038
p.write_text(json.dumps(d,indent=2)+'\n');m.load(p)
census={'derived_against_semantic_fingerprint':semantic}|rederived_census(pkg)
(ROOT/'tests/models/data/mfe_census.json').write_text(json.dumps(census,indent=2)+'\n')
print(json.dumps(d['fingerprints'],indent=2));print('native entries',census['entry_points'])
