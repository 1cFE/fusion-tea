"""Install reviewed transport data as design-owned data and a typed manual seed.

Use only after the response release and its independent review are accepted.
The model package needs no transport engine at execution time.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
BODY='''"""WI-066 interpolation of the immutable design-owned transport response.

Physical source and validation: models/designs/stellarator_09/breeding_response.json.
The numerical lower estimate excludes unresolved physical scenario/shape bias.
Undefined carriers are not physical zero breeding and cannot pass adequacy.
"""
import bisect
import math
from stellarator_tea.modules.mfe_tritium_breeding.blanket_tritium_breeding import Blanket_Tritium_BreedingInput

AUTO_IMPLEMENTED = False
SOURCE_ASSET_SHA256 = "ASSET_DIGEST"
RESPONSE_ASSET = FULL_ASSET_LITERAL
TABLE = TABLE_LITERAL


def run_blanket_tritium_breeding(inputs: Blanket_Tritium_BreedingInput) -> tuple[float, float, float, float, float, float, float]:
    invalid = (0.0,) * 7
    if not all(math.isfinite(getattr(inputs, name)) for name in type(inputs).model_fields):
        return invalid
    if any(getattr(inputs, name) != value for name, value in TABLE['fixed_geometry'].items()):
        return invalid
    nodes = TABLE['nodes']
    thicknesses = [node['thickness_m'] for node in nodes]
    thickness = inputs.blanket_t_in
    if not thicknesses[0] <= thickness <= thicknesses[-1]:
        return invalid
    index = min(bisect.bisect_right(thicknesses, thickness) - 1, len(nodes) - 2)
    left, right = nodes[index:index+2]
    fraction = (thickness - left['thickness_m']) / (right['thickness_m'] - left['thickness_m'])
    li6 = left['tbr_li6'] * (1-fraction) + right['tbr_li6'] * fraction
    li7 = left['tbr_li7'] * (1-fraction) + right['tbr_li7'] * fraction
    mean = li6 + li7
    variance = ((1-fraction)*left['std_error'])**2 + (fraction*right['std_error'])**2
    standard_error = math.sqrt(variance)
    allowance = TABLE['interpolation_allowance']
    lower = mean - TABLE['statistical_multiplier'] * standard_error - allowance
    values = (allowance, lower, 1.0, li6, standard_error, li7, mean)
    return values if all(math.isfinite(x) for x in values) else invalid
'''

def install(source):
    data=json.loads(source.read_text())
    required={'fixed_geometry','nodes','interpolation_allowance','statistical_multiplier'}
    assert required<=data.keys()
    assert len(data['nodes'])==5
    assert [n['thickness_m'] for n in data['nodes']]==[.6,.7,.8,.9,1.]
    assert data['interpolation_allowance']==.01 and data['statistical_multiplier']==2
    # Full scenario and validation provenance travels with the design data.
    contents=json.dumps(data,indent=2,sort_keys=True)+'\n'
    asset=ROOT/'models/designs/stellarator_09/breeding_response.json'
    twin=ROOT/'exploration/stellarator_e2e/models/designs/stellarator_09/breeding_response.json'
    asset.write_text(contents);twin.write_text(contents)
    digest=hashlib.sha256(contents.encode()).hexdigest()
    table={name:data[name] for name in sorted(required)}
    body=BODY.replace('ASSET_DIGEST',digest).replace('FULL_ASSET_LITERAL',repr(data)).replace('TABLE_LITERAL',repr(table))
    seed=HERE.parent/'seeds/blanket_tritium_breeding_impl.py';seed.write_text(body)
    dest=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding'
    dest.mkdir(parents=True,exist_ok=True)
    for name in ('blanket_tritium_breeding_impl.py','tritium_breeding_adequacy_impl.py'):
        (dest/name).write_bytes((HERE.parent/'seeds'/name).read_bytes())
    print('Installed design response asset and two reviewed manual seeds',digest)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('release',type=Path);args=p.parse_args();install(args.release)
