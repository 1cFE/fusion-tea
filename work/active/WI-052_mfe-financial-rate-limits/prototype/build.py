"""Scoped materialization and native generation; never invokes preservation helpers."""
from pathlib import Path
import re
import shutil
import sys
from tests.model_families import MFE, materialize_canonical_subset
from sysml_codegen.cli import GenerationConfig, run_codegen

ROOT = Path(__file__).resolve().parent
MODELS = materialize_canonical_subset(MFE, ROOT/'models')
for filename, calc, start, outputs in [
    ('mfe_account_costs.sysml','IDC Closed-Form Cost','        attribute f_idc', '        out attribute cost : Real;\n'),
    ('mfe_account_costs.sysml','Levelized Annual Cost','        // CRF(i,n)', '        out attribute crf : Real;\n        out attribute levelized : Real;\n'),
    ('mfe_lcoe_dcf.sysml','LCOE DCF','        // (1+d)^N', '        out attribute lcoe : Real;\n'),
]:
    p=MODELS/'analyses'/filename
    text=p.read_text(); begin=text.index("    calc def '"+calc+"'")
    a=text.index(start,begin); b=text.index('\n    }',a)
    text=text[:a]+outputs+text[b:]
    p.write_text(text)

package=ROOT/'generated'
config=dict(models_path=MODELS, output_path=package, package_name='wi052_probe', overwrite=True)
assert run_codegen(GenerationConfig(**config))
# Copy only explicitly located existing manual modules. No helper that reads
# study pins, research/quarantine, or external source trees is used.
source=Path('exploration/stellarator_e2e/generated/handwritten')
for p in source.rglob('*_impl.py'):
    text=p.read_text()
    if re.search(r'^AUTO_IMPLEMENTED = False',text,re.M):
        dest=package/'handwritten'/p.relative_to(source)
        dest.write_text(text.replace('stellarator_tea.','wi052_probe.'))
hand=package/'handwritten'
(hand/'mfe_account_costs/financial_factors.py').write_text((ROOT/'factors.py').read_text())
calendar=hand/'mfe_lifecycle/lifecycle_calendar_impl.py'
text=calendar.read_text()
text=text.replace('import math\n', 'import math\nfrom wi052_probe.handwritten.mfe_account_costs.financial_factors import crf as stable_crf, periodic_pv\n')
a=text.index('    if i == 0.0:', text.index('def _crf'))
b=text.index('\n\n\ndef _clip',a)
text=text[:a]+'    return stable_crf(i, N)'+text[b:]
a=text.index('    s = (1.0 + interest_rate)')
b=text.index('    cost = crf * pv',a)
text=text[:a]+'''    n_rep = max(0.0, float(math.ceil(operational_years / core_lifetime_cal)) - 1.0)
    pv = periodic_pv(cost_per_event, interest_rate, core_lifetime_cal, n_rep)
    crf = stable_crf(interest_rate, operational_years)
'''+text[b:]
text=text.replace('sum(C / (1.0 + i) ** t_k for t_k in events)', 'math.fsum(C * math.exp(-t_k * math.log1p(i)) for t_k in events)')
text=text.replace('(1.0 + i) ** (-y)', 'math.exp(-y * math.log1p(i))')
calendar.write_text(text)
for folder,name,typed,body in [
    ('mfe_account_costs','idc_closed_form_cost','IDC_Closed_Form_Cost', 'return idc(inputs.interest_rate, inputs.construction_years_in) * inputs.overnight_cost'),
    ('mfe_account_costs','levelized_annual_cost','Levelized_Annual_Cost', 'c = crf(inputs.interest_rate, inputs.operational_years_in)\n    return c * annuity_pv(inputs.annual_cost, inputs.interest_rate, inputs.inflation_rate_in, inputs.operational_years_in, inputs.project_time), c'),
    ('mfe_lcoe_dcf','lcoe_dcf','LCOE_DCF', 'c = crf(inputs.discount_rate_in, inputs.operational_years_in)\n    midpoint = math.exp(inputs.construction_years_in / 2.0 * math.log1p(inputs.discount_rate_in))\n    return (inputs.total_capital_in * midpoint * c + inputs.annual_om_in) / (8760.0 * inputs.net_electric_mw * inputs.availability_in)'),
]:
    (hand/folder/(name+'_impl.py')).write_text(f'''import math
from wi052_probe.modules.{folder}.{name} import {typed}Input
from wi052_probe.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc
AUTO_IMPLEMENTED = False
def run_{name}(inputs: {typed}Input) -> {'tuple[float, float]' if name=='levelized_annual_cost' else 'float'}:
    {body}
''')
assert run_codegen(GenerationConfig(**config,preserve_handwritten=True))
def files():
    return {str(p.relative_to(package)):p.read_bytes() for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
before=files()
assert run_codegen(GenerationConfig(**config,preserve_handwritten=True))
assert files()==before
assert run_codegen(GenerationConfig(**config,preserve_handwritten=True,smart_regen=True))
assert files()==before
print('PASS native generation; all package bytes including shared helper preserved on normal and smart regeneration')
