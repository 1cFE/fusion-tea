"""Static complete pipeline census; AST guard index is evidence, not semantic certification."""
from pathlib import Path
import ast,json,yaml,hashlib,re
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;P=ROOT/'exploration/stellarator_e2e/generated'
mods=yaml.safe_load((P/'pipelines/pipeline.yaml').read_text())['modules']; producers={};consumers={}
for name,m in mods.items():
 for field,bind in m.get('outputs',{}).items():producers[bind.split()[-1]]=(name,field)
 for field,bind in m.get('inputs',{}).items():consumers.setdefault(bind.split()[-1],[]).append((name,field))
manual={}
for path in sorted((P/'handwritten').rglob('*_impl.py')):
 text=path.read_text();tree=ast.parse(text);guards=[]
 for node in ast.walk(tree):
  if isinstance(node,(ast.If,ast.Raise,ast.Assert)):
   content=ast.get_source_segment(text,node)
   if len(content)>4000:content=content[:4000]+' [TRUNCATED; inspect source]'
   guards.append({'line':node.lineno,'kind':type(node).__name__,'code':content})
 manual[path.stem.removesuffix('_impl')]={'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'guards':guards}
rows=[]
for name,m in mods.items():
 mt=m['module_type']; stem=re.sub(r'(?<!^)(?=[A-Z])','_',mt.split('.')[-1].removesuffix('Module')).lower();stem=mt.split('.')[-1].removesuffix('Module').lower()
 candidates=[v for k,v in manual.items() if k.replace('_','')==stem.replace('_','')]
 row={'instance':name,'module_type':mt,'inputs':m.get('inputs',{}),'outputs':m.get('outputs',{}),'consumers':{b.split()[-1]:consumers.get(b.split()[-1],[]) for b in m.get('outputs',{}).values()},'manual_candidates':candidates}
 rows.append(row)
(OUT/'chain-inventory.json').write_text(json.dumps({'scope':'Every generated pipeline module, including dormant-but-evaluated paths; guards are an index, not a claim of complete scientific limits.','modules':rows,'manual_bodies':manual},indent=2))
# Static descendant closure from concrete binding producer edges.
adj={n:set() for n in mods}
for channel,ps in producers.items():
 for c,_ in consumers.get(channel,[]):adj[ps[0]].add(c)
desc={}
for n in adj:
 seen=set();todo=list(adj[n])
 while todo:
  c=todo.pop()
  if c in seen:continue
  seen.add(c);todo+=list(adj[c])
 desc[n]=sorted(seen)
(OUT/'descendants.json').write_text(json.dumps(desc,indent=2))
print('modules',len(rows),'manual bodies',len(manual),'output channels',len(producers),'manual matches',sum(bool(r['manual_candidates']) for r in rows))
