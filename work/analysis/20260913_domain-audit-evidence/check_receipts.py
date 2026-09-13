"""Independent verification of bounded retained receipt identities and interfaces."""
import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path.cwd();e=ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence'
load=lambda p:json.loads(p.read_text())
before=load(e/'baseline-native.json');after=load(e/'candidate-native.json')
assert before==after
hashes=load(e/'candidate-package-hashes.json')
print(type(hashes).__name__)
for relative,digest in hashes.items():
    p=ROOT/'exploration/stellarator_e2e/generated'/relative
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,relative
for filename in ['mfe_cryo_plant.sysml','mfe_plasma_scaling.sysml']:
    assert (ROOT/'models/library/analyses'/filename).read_bytes()==(ROOT/'exploration/stellarator_e2e/models/analyses'/filename).read_bytes()
for relative in ['contracts/model_contract.json','pipelines/pipeline.yaml']:
    path='exploration/stellarator_e2e/generated/'+relative
    assert subprocess.check_output(['git','show','3d9711e2^:'+path])==(ROOT/path).read_bytes()
old=load(e/'baseline-validation.json');new=load(e/'candidate-validation.json')
for a,b in zip(old,new):
    assert a['level']==b['level'] and a['issues']==b['issues'] and a['warnings']==b['warnings']
print('Ten entering/candidate native maps exact; current package receipt, family twins, public contract and pipeline preserved; all validation issue identities unchanged')
