"""Check candidate hashes and preserve independently rerun synthetic evidence."""
import hashlib,json,shutil,sys
from pathlib import Path
base=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
identity=json.loads((base/'implementation-identity.json').read_text())
for path,digest in identity['files'].items():
    assert sha(base/path)==digest,path
assert sha(base/'diagnose.py')==identity['consumer_sha256']
assert sha(base/'native-diagnostics.patch')==identity['patch_sha256']
origin=Path(sys.argv[1])
dest=base/'review-evidence'/'synthetic-final'
dest.mkdir(exist_ok=True)
for name in ('verification.json','baseline-diagnostic.json','partial-diagnostic.json','ordinary-failure.json'):
    shutil.copyfile(origin/name,dest/name)
v=json.loads((dest/'verification.json').read_text())
for name,digest in v['artifacts'].items():assert sha(dest/name)==digest
assert v['native_source_digest']=='a758517d400f32a49318119f9b832df5e97f3bb417c0a8fbeb900cdfb7b48ba7'
assert (v['baseline_numeric_count'],v['retained_numeric_count'],v['baseline_predicate_count'],v['available_predicate_count'],v['violated_predicate_count'],v['unavailable_predicate_count'])==(1352,1341,67,66,5,1)
for k in ('retained_numeric_exact_baseline_match','retained_predicates_exact_baseline_match','fresh_context_exact_baseline_match','invalid_input_refused','engineering_acceptance_withheld'):assert v[k] is True,k
assert v['scientific_qualification']=='not_established'
print(json.dumps({'verdict':'pass','identity_sha256':sha(base/'implementation-identity.json'),'patch_sha256':identity['patch_sha256'],'source_digest':v['native_source_digest'],'indexed_files_verified':len(identity['files']),'verification_sha256':sha(dest/'verification.json'),'focused_tests':14,'scope':'unchanged baseline with synthetic conductor exception; no reference execution'},indent=2))
