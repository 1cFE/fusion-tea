"""Accounting evidence over the retained native baseline; unknowns stay null."""
import json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
r=json.loads((HERE/'baseline.json').read_text());o=r['outputs'];P='stellarator_09__stellaris__'
def get(name):return o[P+name]
metal={m:get('magnet__material_inventory__cost_'+m) for m in ('copper','solder','steel','helium')}
tape=get('magnet__winding_procurement__tape_cost');sheet=get('magnet__insulation_inventory__stock_cost')
wind=get('magnet__winding_procurement__winding_fabrication_cost');support=get('magnet__magnet_structure_cost__cost')
mat=tape+sum(metal.values())+sheet
magnet=get('magnet__magnet_capital_rollup__capital_cost')
assert math.isclose(mat+wind+support,magnet,rel_tol=1e-12)
enter=json.loads((ROOT/'work/orchestration/goals/magnet-manufacturing-cost-completeness/evidence/entering-reconciliation.json').read_text())
assert math.isclose(magnet-enter['magnet'],sheet,rel_tol=1e-12,abs_tol=1e-6)
assert get('magnet__wp_fit__minimum_margin')<0 and get('magnet__conductor_current__margin_current')<0
result={'scope':'conditional priced subset, not complete manufacturing or reconciled common-year total',
 'units':'USD; per-account price-year limitations in account-ledger.md',
 'priced_material_stock':{'complete_tape':tape,'external_materials':metal,'conditional_internal_sheet':sheet,'subtotal':mat},
 'winding_operations':wind,'all_in_electromagnetic_supports':support,'effective_support_rate_usd_kg':get('magnet__magnet_structure_cost__effective_all_in_rate'),
 'magnet_priced_subtotal':magnet,'nonmagnet_allowance':get('structure__structure_cost__cost'),
 'magnet_plus_nonmagnet_allowance':magnet+get('structure__structure_cost__cost'),
 'insulation':{'internal_sheet_m3':get('magnet__insulation_inventory__internal_volume'),'internal_sheet_m2':get('magnet__insulation_inventory__sheet_area'),'ground_envelope_m3':get('magnet__insulation_inventory__ground_volume'),'ground_material_cost':None,'ground_installation_cost':None},
 'unresolved_costs':{'fixed_cable_manufacture':None,'incremental_joints_testing_assembly':None,'incremental_winding_effort':None,'waste_yield_rework':None,'free_resin_impregnation':None},
 'assumed_boundary':'Internal sheet purchase is assumed additional to historical winding; zero-increment cost-only alternative keeps geometry unchanged.',
 'zero_increment_alternative_magnet':enter['magnet'],'added_sheet_charge':magnet-enter['magnet'],
 'lcoe':get('lcoe_calc__lcoe'),'fit_minimum_margin_m':get('magnet__wp_fit__minimum_margin'),'current_margin_A':get('magnet__conductor_current__margin_current'),
 'checks':{'material_winding_allin_sum':True,'added_charge_equals_sheet':True,'adverse_reference_physics_retained':True}}
(HERE/'reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
