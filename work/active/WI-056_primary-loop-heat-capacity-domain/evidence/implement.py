"""Apply the bounded canonical primary-loop contract and ordered completion."""
import hashlib,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
def inventory(path):
 return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
if __name__=='__main__':
 hashes=inventory(PACKAGE);(HERE/'entering-package-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 oldseeds=json.loads((HERE.parents[1]/'WI-055_winding-pack-input-domain/evidence/candidate-seeds.json').read_text())
 assert len(oldseeds)==12 and all(hashes[n]==h for n,h in oldseeds.items())
 (HERE/'entering-seeds.json').write_text(json.dumps(oldseeds,indent=2)+'\n')
 body=PACKAGE/'handwritten/mfe_primary_loop/primary_coolant_loop_impl.py';original=body.read_text()
 (HERE/'entering-primary-body.py').write_text(original)
 p=ROOT/'models/library/analyses/mfe_primary_loop.sysml';s=p.read_text()
 s=s.replace('        Constant ideal-gas helium properties', '''        INPUT DOMAIN (WI-056): cp_in and dT_blanket_in must each be finite
        and strictly positive. cp is specific heat [J/(kg K)]; dT_blanket
        is the positive coolant heating rise [K]. A negative pair is invalid.
        Native typed manual completion raises ValueError before arithmetic.
        This domain also applies for q_source = 0 and loop_live = 0 because
        the chain always evaluates. Reference values are examples, not bounds.
        The thirteen outputs below require this guarded manual completion;
        the ordered equations above remain the normative valid calculation.

        Constant ideal-gas helium properties''')
 start=s.index('        out attribute mdot : Real =')
 suffix=s[start:];suffix=re.sub(r'(out attribute \w+ : Real)\s*=.*?;',r'\1;',suffix,flags=re.S)
 suffix=re.sub(r'        attribute k_isen : Real =.*?;\n','',suffix,flags=re.S)
 s=s[:start]+suffix;p.write_text(s)
 (ROOT/'exploration/stellarator_e2e/models/analyses/mfe_primary_loop.sysml').write_text(s)
 # Retain exact ordered executable body and ABI, replacing generated documentation.
 code=original[original.rindex('    k_isen ='):]
 header='''"""WI-056 typed completion of the canonical finite-positive primary-loop domain.

Valid arithmetic and thirteen-output ABI are preserved from the entering generated
body. Equations and physical assumptions: models/library/analyses/mfe_primary_loop.sysml.
"""
import math
from stellarator_tea.modules.mfe_primary_loop.primary_coolant_loop import Primary_Coolant_LoopInput

AUTO_IMPLEMENTED = False


def run_primary_coolant_loop(inputs: Primary_Coolant_LoopInput) -> tuple[float, ...]:
    """Evaluate the always-active chain after checking its two heating operands."""
    if not math.isfinite(inputs.cp_in) or inputs.cp_in <= 0:
        raise ValueError("Primary Coolant Loop: cp_in must be finite and positive")
    if not math.isfinite(inputs.dT_blanket_in) or inputs.dT_blanket_in <= 0:
        raise ValueError("Primary Coolant Loop: dT_blanket_in must be finite and positive")
'''
 body.write_text(header+code)
 seeds=oldseeds|{str(body.relative_to(PACKAGE)):hashlib.sha256(body.read_bytes()).hexdigest()}
 (HERE/'candidate-seeds.json').write_text(json.dumps(seeds,indent=2)+'\n')
 plan=HERE.parent/'plan.md';plan.write_text(plan.read_text().replace('- [ ] Retain entering','- [x] Retain entering').replace('- [ ] Implement canonical','- [x] Implement canonical'))
 print('Implemented bounded contract; preserved twelve seeds and added guarded primary-loop completion')
