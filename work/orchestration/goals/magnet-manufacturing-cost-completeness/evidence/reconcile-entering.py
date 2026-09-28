"""Reconcile existing frozen native outputs without claiming a new study."""
import json
from pathlib import Path
from math import isclose
ROOT=Path(__file__).resolve().parents[5]
source=ROOT/'exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/baseline_result.json'
r=json.loads(source.read_text()); c=r['channels']; prefix='stellarator_09__stellaris__'
def value(k): return c[prefix+k]
materials={m:value('magnet__material_inventory__cost_'+m) for m in ('copper','solder','steel','helium')}
tape=value('magnet__winding_procurement__tape_cost'); winding=value('magnet__winding_procurement__winding_fabrication_cost')
pack=value('magnet__winding_procurement__cost'); support=value('magnet__magnet_structure_cost__cost'); magnet=value('magnet__magnet_capital_rollup__capital_cost')
checks={'external_material_sum':(sum(materials.values()),value('magnet__material_inventory__material_cost')), 'pack_sum':(tape+sum(materials.values())+winding,pack), 'magnet_sum':(pack+support,magnet), 'tape_metre_basis':(value('magnet__winding_procurement__tape_length')*20,tape), 'support_effective_rate':(value('magnet__support_mass__m_support')*18,support)}
assert all(isclose(a,b,rel_tol=1e-12,abs_tol=1e-6) for a,b in checks.values())
out={'source':str(source.relative_to(ROOT)), 'executed_under':r['executed_under'], 'units':'USD nominal mixed/partly normalized bases; not a reconciled common-year total','tape':tape,'external_materials':materials,'winding_operations':winding,'pack':pack,'all_in_support':support,'magnet':magnet,'nonmagnet_allowance':value('structure__structure_cost__cost'),'conductor_m':value('magnet__winding_procurement__conductor_length'),'support_kg':value('magnet__support_mass__m_support'),'checks':{k:{'computed':a,'native':b,'pass':True} for k,(a,b) in checks.items()},'limitation':'Support is an all-in scenario, not an observed stock/fabrication split. No unpriced term is assigned zero by this reconciliation.'}
(Path(__file__).parent/'entering-reconciliation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
