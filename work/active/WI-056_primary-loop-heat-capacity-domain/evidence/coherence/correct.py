"""Restore exact generated signature; preserve all runtime statements/guards."""
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent;EVIDENCE=HERE.parent;PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
p=PACKAGE/'handwritten/mfe_primary_loop/primary_coolant_loop_impl.py';old=p.read_text();new=old.replace('-> tuple[float, ...]:','-> tuple['+', '.join(['float']*13)+']:')
assert old!=new
for tree in (ast.parse(old),ast.parse(new)):compile(tree,str(p),'exec')
a,b=ast.parse(old),ast.parse(new)
for tree in (a,b):next(n for n in tree.body if isinstance(n,ast.FunctionDef)).returns=None
assert ast.dump(a)==ast.dump(b),'Runtime statements changed'
p.write_text(new)
seeds=json.loads((EVIDENCE/'candidate-seeds.json').read_text());name=str(p.relative_to(PACKAGE));previous=seeds[name];seeds[name]=hashlib.sha256(p.read_bytes()).hexdigest()
(EVIDENCE/'corrected-candidate-seeds.json').write_text(json.dumps(seeds,indent=2)+'\n')
(HERE/'signature-correction.json').write_text(json.dumps({'path':name,'before':previous,'after':seeds[name],'only_return_annotation_changed':True,'return_arity':13},indent=2)+'\n')
s=(EVIDENCE/'regenerate.py').read_text().replace("HERE/'candidate-seeds.json'","HERE/'corrected-candidate-seeds.json'").replace("HERE/'candidate-package-hashes.json'","HERE/'corrected-package-hashes.json'").replace("HERE/'generation-changes.json'","HERE/'coherence/generation-changes.json'")
s=s.replace('preserve_handwritten=True,**kwargs','preserve_handwritten=True,smart_regen=True,**kwargs')
s=s.replace('Checked current MFE generator: thirteen frozen normative seeds, fresh outputs.','Corrected current MFE generator: exact typed seeds and stock smart regeneration.')
(EVIDENCE/'regenerate_corrected.py').write_text(s)
