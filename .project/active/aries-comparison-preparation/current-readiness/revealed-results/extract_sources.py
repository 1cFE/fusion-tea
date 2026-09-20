"""After committed reveal: pagewise PDF skill extraction with retained receipts."""
import datetime, hashlib, importlib.metadata, json, pathlib, shutil, subprocess, sys
ROOT=pathlib.Path('/home/reid/1cfe/fusion-tea')
BASE=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'knowledge/holdout/aries-cs'
OUT=SRC/'extracted/20260920-r3'
SCRIPT=ROOT/'.agents/skills/pdf-analysis/scripts/extract_page.py'
def main():
 assert 'status: revealed' in (SRC/'PROTOCOL.md').read_text()
 OUT.mkdir(parents=True,exist_ok=False)
 manifest=json.loads((SRC/'manifest.json').read_text())
 versions={n:importlib.metadata.version(n) for n in ('pymupdf','pymupdf4llm')}
 (OUT/'extraction-environment.json').write_text(json.dumps({'python':sys.version,'versions':versions,'skill_script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'page_index':'zero-based'},indent=2)+'\n')
 shutil.copy2(SCRIPT,OUT/'extract_page.py')
 for source in manifest['files']:
  pdf=SRC/source['filename']; assert hashlib.sha256(pdf.read_bytes()).hexdigest()==source['sha256']
  dest=OUT/pdf.stem; dest.mkdir(); shutil.copy2(pdf,dest/pdf.name)
  for page in range(source['pages']):
   target=dest/f'page-{page:02d}.md'; cmd=[sys.executable,str(SCRIPT),str(pdf),str(page),'--mode','markdown','--output',str(target)]
   start=datetime.datetime.now(datetime.timezone.utc).isoformat()
   result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
   log=dest/f'page-{page:02d}.log';log.write_text(result.stdout+'\n'+result.stderr)
   receipt={'utc':start,'cwd':str(ROOT),'argv':cmd,'exit_status':result.returncode,'input':str(pdf),'output':str(target),'stdout_stderr':str(log)}
   with (OUT/'commands.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
   if result.returncode: raise RuntimeError(f'Extraction failed {pdf} {page}; see {log}')
  print(pdf.name,'extracted',flush=True)
if __name__=='__main__': main()
