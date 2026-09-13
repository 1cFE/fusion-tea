"""Differential validation, fresh snapshot generation and protected-source checks."""
import json, shutil, sys
from collections import Counter
from pathlib import Path
from build import H, ROOT, hashes, dump
from tests.model_families import MFE, canonical_path
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level6_architecture import validate_architecture
from sysml_codegen.cli import GenerationConfig, run_codegen
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
diff={}
def issues(result): return Counter(str(x.message if hasattr(x,'message') else x).split(' at file:')[0] for x in result.issues)
for level,fn in [('L2',validate_structure),('L6',validate_architecture)]:
    a,b=issues(fn(str(H/'entering-models'))),issues(fn(str(H/'models')))
    diff[level]={'before':sum(a.values()),'after':sum(b.values()),'added':list((b-a).elements()),'removed':list((a-b).elements()),'inherited':dict(a&b)}
dump('validation-diff.json',diff)
assert all(not v['added'] and not v['removed'] for v in diff.values())
snapshot=H/'instance_graph_snapshot.json'; capture_instance_graph_snapshot([H/'models'],snapshot)
target=H/'from-snapshot'; manual=json.loads((H/'manual-preservation.json').read_text())
for name in manual:
    f=target/name; f.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(H/'generated'/name,f)
assert run_codegen(GenerationConfig(output_path=target,from_snapshot=snapshot,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True))
assert hashes(target)==hashes(H/'generated')
before=json.loads((H/'execution-start.json').read_text())
assert before['package_before']==hashes(ROOT/'exploration/stellarator_e2e/generated')
assert before['family_before']=={p:__import__('hashlib').sha256(canonical_path(p).read_bytes()).hexdigest() for p in MFE.owned}
assert all(canonical_path(p).read_bytes()==(MFE.twin/p).read_bytes() for p in MFE.owned)
changed=[p for p in MFE.owned if (H/'models'/p).read_bytes()!=(H/'entering-models'/p).read_bytes()]
assert changed==['designs/generic_mfe/mfe_plant.sysml','designs/stellarator_09/stellarator_plant.sysml']
dump('preservation.json',{'live_equals_snapshot':True,'production_package_unchanged':True,'canonical_unchanged':True,'twins_equal':23,'prototype_changed_logical_files':changed,'manual_hashes':manual,'fresh_generated_body_count':len(list((H/'generated/handwritten').rglob('*_impl.py')))-len(manual)})
print('PASS diagnostic differential, live/snapshot equality, protected canonical/package and handwritten preservation')
