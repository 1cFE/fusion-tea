"""Independent archive/export custody verification. Never executes the model."""
import collections, hashlib, importlib.util, json, pathlib, shutil, sqlite3, sys, tarfile, tempfile
root=pathlib.Path('/home/reid/1cfe/fusion-tea')
prep=root/'.project/active/aries-comparison-preparation/post-reveal-preparation'
reg=root/'.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1'
out=reg/'replay-verification'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
write=lambda p,v:p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
adopt=read(prep/'adoption.json'); archive=root/adopt['archive']
assert sha(archive)==adopt['archive_sha256']
restore=pathlib.Path(tempfile.mkdtemp(prefix='aries-independent-replay-'))
with tarfile.open(archive) as tf:
    members=tf.getmembers(); assert len(members)==adopt['archive_members']
    tf.extractall(restore,filter='data')
tools=restore/prep.relative_to(root)/'tools'
sys.path.insert(0,str(tools))
import adapter as a
identity=a.verify_identity()
assert sha(tools/'identity.json')==adopt['identity_sha256']
attempt=reg/'attempts/first-forward'
before={str(p.relative_to(attempt)):sha(p) for p in attempt.rglob('*') if p.is_file()}
receipt=read(attempt/'receipt.json')
assert all(before[k]==v for k,v in receipt['artifacts'].items())
assert sorted(p.name for p in (reg/'attempts').iterdir() if p.is_dir())==['first-forward']
pointer=read(reg/'attempts/first-attempt.json')|{'pointer_sha256':sha(reg/'attempts/first-attempt.json')}
assert pointer==receipt['first_attempt']
native=read(attempt/'result.json'); assert native['first_attempt']==pointer
assert sha(reg/'request.json')==sha(attempt/'request.raw.json')==adopt['artifacts'][str(prep.relative_to(root)/'mapping/proposed-reference-request.json')]
contract=read(a.PACKAGE/'contracts/model_contract.json')
point,selection=a.select(read(reg/'request.json'),a.defaults(contract))
assert selection | {'requested_overrides':point}==read(attempt/'selection.json')
assert len(point)==3 and len(selection['effective_inputs'])==704
assert all(native[k]==v for k,v in selection.items())
export=a.export(native,read(tools/'historical-manifest.json'),contract)
assert export==read(attempt/'model-export.json')
write(out/'model-export.json',export)
assert sha(out/'model-export.json')==sha(attempt/'model-export.json')
assert len(export['rows'])==276 and not native['outputs'] and not native['verdicts']
# Copy only: immutable SQLite cannot create or alter original WAL/SHM bytes.
assert (attempt/'native/adapter-preparation-v1.db-wal').stat().st_size==0
copy=out/'native-copy.db'; shutil.copyfile(attempt/'native/adapter-preparation-v1.db',copy)
conn=sqlite3.connect(copy.as_uri()+'?immutable=1',uri=True)
tables=[r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
db={t:{'columns':[r[1] for r in conn.execute('PRAGMA table_info("'+t+'")')], 'rows':conn.execute('SELECT * FROM "'+t+'"').fetchall()} for t in tables}
conn.close(); write(out/'database-inspection.json',db)
assert before=={str(p.relative_to(attempt)):sha(p) for p in attempt.rglob('*') if p.is_file()}
result={'schema_version':'independent-replay-custody/v1','archive_sha256':sha(archive),'archive_members':len(members),'restored_root':str(restore),'identity_sha256':sha(tools/'identity.json'),'pinned_files_verified':len(identity['files']),'original_artifact_hashes':before,'original_receipt_verified':True,'original_attempt_unchanged':True,'first_attempt':pointer,'physical_attempt_directories':['first-forward'],'new_physical_evaluations':0,'request_sha256':sha(reg/'request.json'),'selection_reproduced':True,'supplied_inputs':len(point),'held_inputs':len(selection['effective_inputs'])-len(point),'export_reproduced_byte_identically':True,'export_rows':len(export['rows']),'export_status_counts':dict(collections.Counter(r['status'] for r in export['rows'])),'execution_state':native['state'],'output_count':len(native['outputs']),'returned_predicate_count':len(native['verdicts']),'required_predicate_count':len(contract['constraint_catalog']['concrete_entries']),'database_copy_sha256':sha(copy),'database_tables':tables,'report_replay':'pending'}
write(reg/'review/replay-receipt.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='original_artifact_hashes'},indent=2))
