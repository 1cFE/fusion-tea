"""Repair first capture: select executable k_isen, not generated doc expression."""
import json,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
p=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py'
s=p.read_text();original=(HERE/'entering-primary-body.py').read_text()
s=s[:s.index('    k_isen =')]+original[original.rindex('    k_isen ='):]
compile(s,str(p),'exec');p.write_text(s)
for name in ('candidate-seeds.json','candidate-package-hashes.json','generation-changes.json'):
 shutil.copyfile(HERE/name,HERE/('initial-'+name))
seeds=json.loads((HERE/'candidate-seeds.json').read_text());seeds[str(p.relative_to(ROOT/'exploration/stellarator_e2e/generated'))]=hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'candidate-seeds.json').write_text(json.dumps(seeds,indent=2)+'\n')
(HERE/'candidate-package-hashes.json').unlink()
impl=HERE/'implement.py';impl.write_text(impl.read_text().replace("original.index('    k_isen =')","original.rindex('    k_isen =')"))
