"""Inventory only the explicitly owned current MFE package and models."""
import hashlib,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
def inventory(package):
 return {str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
if __name__=='__main__':
 hashes=inventory(PACKAGE)
 seeds={str(p.relative_to(PACKAGE/'handwritten')):hashes[str(p.relative_to(PACKAGE))] for p in (PACKAGE/'handwritten').rglob('*.py') if p.name=='financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$',p.read_text(),re.M)}
 assert len(seeds)==10,seeds
 (HERE/'entering-package-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 (HERE/'manual-seeds.json').write_text(json.dumps(seeds,indent=2)+'\n')
 for name in list(seeds)+['mfe_magnet_field/winding_pack_sizing_impl.py','mfe_magnet_field/coil_set_axis_field_impl.py']:
  dest=HERE/'original-bodies'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PACKAGE/'handwritten'/name,dest)
 print('Captured ten normative seeds and current package identity')
