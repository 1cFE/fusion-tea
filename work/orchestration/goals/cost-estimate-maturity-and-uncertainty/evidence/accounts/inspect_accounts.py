"""Read the verified frozen baseline; never evaluate or alter a plant model."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
STUDY = ROOT / 'exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs'
PREFIX = 'stellarator_09__stellaris__'
baseline = json.loads((STUDY / 'results/baseline_result.json').read_text())
channels = {k.removeprefix(PREFIX): v for k, v in baseline['channels'].items()}
inputs = {k.removeprefix(PREFIX): v for f in sorted((STUDY / 'preparation/producer-package/inputs').glob('*.json')) for k, v in json.loads(f.read_text()).items()}
inputs.update({k.removeprefix(PREFIX): v for k, v in baseline['point'].items()})
v = channels.__getitem__
groups = [
    ('CAS21', 'Facilities and site', 'buildings__facility_accounts__cost'),
    ('C220103', 'Magnet', 'magnet__magnet_capital_rollup__capital_cost'),
    ('C220101', 'Blanket and first wall', 'blanket__blanket_cost__cost'),
    ('C220102', 'Shield', 'shield__shield_cost__cost'),
    ('C220104', 'Heating', 'heating__heating_cost__cost'),
    ('C220105', 'Nonmagnet structure', 'structure__structure_cost__cost'),
    ('C220106', 'Vessel shell', 'vessel__vessel_cost__cost'),
    ('C220107', 'Power supplies', 'power_supplies__power_supplies_cost__cost'),
    ('C220108', 'Divertor', 'divertor__divertor_cost__cost'),
    ('C220110', 'Remote handling', 'remote_handling__cost'),
    ('C220111', 'Reactor installation', 'installation__cost'),
    ('C220200', 'Heat transport', 'heat_transport__cooling_selection__cost'),
    ('C220300', 'Cryoplant and auxiliary cooling', 'cryoplant__aux_cooling__cost'),
    ('C220400', 'Waste handling', 'waste__cost'),
    ('C220500', 'Fuel processing', 'fuel_cycle__processing_cost__cost'),
    ('C220600', 'Other reactor equipment', 'other_rpe__cost'),
    ('C220700', 'Central instrumentation and controls', 'inc_cost__cost'),
    ('CAS23', 'Turbine', 'turbine__turbine_cost__cost'),
    ('CAS24', 'Electrical plant', 'electric_plant__electric_cost__cost'),
    ('CAS25', 'Heat rejection', 'heat_rejection__heat_rejection_cost__cost'),
    ('CAS26', 'Miscellaneous plant', 'misc_plant__misc_cost__cost'),
    ('CAS27', 'Special materials', 'special_materials_capital__special_materials_capital'),
    ('CAS28', 'Digital twin', '@cas28_capital'),
]
rows = []
direct = v('cas2x_pre_contingency__cas2x_pre_contingency')
for account, label, channel in groups:
    value = inputs[channel[1:]] if channel.startswith('@') else v(channel)
    rows.append(dict(account=account, function=label, channel=channel, usd=value, direct_share=value/direct))
children = {}
children['C220200'] = {k: v('heat_transport__equipment__' + k) for k in ['primary_circulators_cost', 'primary_piping_cost', 'exchangers_cost', 'secondary_pumps_cost', 'secondary_piping_cost', 'inventory_cost', 'spares_cost']}
children['C220103'] = {k: v(k) for k in ['magnet__winding_procurement__tape_cost', 'magnet__winding_procurement__winding_fabrication_cost', 'magnet__material_inventory__cost_copper', 'magnet__material_inventory__cost_solder', 'magnet__material_inventory__cost_steel', 'magnet__material_inventory__cost_helium', 'magnet__insulation_inventory__stock_cost', 'magnet__magnet_structure_cost__cost']}
children['CAS21'] = {k: val for k, val in channels.items() if k.startswith('buildings__') and k.endswith('__civil__cost_2025')}
children['CAS21'].update({k: v(k) for k in ['buildings__ventilation__cost_2025', 'buildings__site_allowance__cost']})
children['C220500'] = {k: v('fuel_cycle__processing_cost__' + k) for k in ['cleanup_capital','cleanup_installation','distiller_capital','distiller_installation','transfer_capital','transfer_installation','containment_capital','containment_installation']}
checks = {}
def check(name, actual, expected):
    error = actual - expected
    assert abs(error) < 1e-4, (name, error)
    checks[name] = dict(actual=actual, expected=expected, error=error, pass_absolute_tolerance_usd=1e-4)
check('direct', sum(r['usd'] for r in rows), direct)
for account, detail in children.items():
    check(account, sum(detail.values()), next(r['usd'] for r in rows if r['account'] == account))
overnight_components = {k: v(k) for k in ['facility_preconstruction__cost','cas20_capital__cas20_capital','indirect__cost','owner__cost','supplementary__cost']}
check('overnight', sum(overnight_components.values()), v('overnight_capital__overnight_capital'))
check('CAS20', direct + v('contingency__cost'), v('cas20_capital__cas20_capital'))
children['CAS50'] = {
    'shipping': inputs['supplementary__shipping_frac'] * v('shipping_scope__remaining_shipping_base'),
    'spares': inputs['supplementary_spares_frac'] * v('cas23_to_28_capital__cas23_to_28_capital'),
    'tax': inputs['supplementary__tax_frac'] * v('cas20_capital__cas20_capital'),
    'insurance': inputs['supplementary__insurance_frac'] * (v('cas20_capital__cas20_capital') + v('indirect__cost')),
    'startup_fuel': inputs['supplementary_startup_base'] * inputs['n_mod'] * v('pb__p_net') / inputs['supplementary__ref_net_power'],
    'decommissioning': inputs['supplementary_decom_base'] * inputs['n_mod'] * v('pb__p_net') / inputs['supplementary__ref_net_power'],
}
check('CAS50', sum(children['CAS50'].values()) * (1+inputs['supplementary__contingency_rate_in']), v('supplementary__cost'))
check('CAS70', v('cas71_calc__levelized')+v('cooling_annual__cas72_total'), v('cas70_calc__cas70'))
check('annual_total', v('cas70_calc__cas70')+v('cas80_calc__levelized'), v('cas70_calc__annual_total'))
energy = 8760 * v('pb__p_net') * v('calendar__availability')
financing = (1+inputs['discount_rate'])**(inputs['construction_years']/2)
headline_annual_capital = v('total_capital__total_capital') * financing * v('cas71_calc__crf')
check('headline_lcoe', (headline_annual_capital+v('cas70_calc__annual_total'))/energy,v('lcoe_calc__lcoe'))
check('comparison_lcoe', (v('cas90_1cfe_calc__cas90')+v('cas70_calc__annual_total'))/energy,v('lcoe_1cfe_calc__lcoe'))
snap = json.loads((STUDY / 'snapshot.json').read_text())
receipt = json.loads((STUDY / 'preparation/integration-return.json').read_text())
package_comparison = []
for file in sorted((STUDY/'preparation/producer-package').rglob('*')):
    if not file.is_file() or '__pycache__' in file.parts: continue
    rel=file.relative_to(STUDY/'preparation/producer-package')
    current=ROOT/'exploration/stellarator_e2e/generated'/rel
    package_comparison.append({'path':str(rel),'frozen_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'current_matches':current.is_file() and current.read_bytes()==file.read_bytes()})
result = dict(kind='Author read-only account extraction; not independent certification or a new study', source=str(STUDY.relative_to(ROOT)), source_sha256=hashlib.sha256((STUDY/'results/baseline_result.json').read_bytes()).hexdigest(), source_model=snap['package'], identity=receipt['candidate'], baseline_execution=baseline['executed_under'], direct_accounts=rows, children=children, overnight_components=overnight_components, checks=checks, annual_energy_mwh=energy, midpoint_financing_factor=financing, headline_annual_capital_usd=headline_annual_capital, comparison_financed_capital_usd=v('total_capital__total_capital')+v('idc__cost'), all_verdicts=baseline['verdicts'], package_comparison=package_comparison)
(OUT/'account-extraction.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'fixed-inputs.json').write_text(json.dumps(inputs,indent=2,sort_keys=True)+'\n')
with (OUT/'functional-accounts.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(json.dumps({'checks':len(checks),'all_checks_pass':True,'direct_usd':direct,'overnight_usd':v('total_capital__total_capital'),'annual_energy_mwh':energy,'headline_annual_capital_usd':headline_annual_capital,'package_files':len(package_comparison),'package_mismatches':[r['path'] for r in package_comparison if not r['current_matches']]},indent=2))
