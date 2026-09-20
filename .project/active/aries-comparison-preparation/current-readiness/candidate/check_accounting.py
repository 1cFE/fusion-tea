"""Reconcile current result accounts without reading historical numerical results."""
import argparse
import json
import math
from pathlib import Path
from candidate_common import digest, exclusive_document
from export_model_values import extract


def facility_children(outputs, inventory, prefix):
    actual={key for key in outputs if key.startswith(prefix+'buildings__') and key.endswith('__civil__cost_2025')}
    expected=set(inventory['facility_civil_children'])
    if len(expected)!=len(inventory['facility_civil_children']) or actual!=expected:
        raise ValueError('facility civil-child inventory differs')
    return [outputs[key] for key in inventory['facility_civil_children']]


def check(root, native_path, here=None):
    root=Path(root); here=Path(here or Path(__file__).parent)
    manifest=json.loads((here/'manifest.json').read_text())
    native=json.loads(Path(native_path).read_text())
    if native['state']!='completed': raise ValueError('cannot reconcile an incomplete execution')
    contract=json.loads((root/manifest['package_path']/'contracts/model_contract.json').read_text())
    mapped={row['id']:row for row in extract(manifest,contract,native)['quantities']}
    inventory=json.loads((here/'account-inventory.json').read_text())
    values=native['effective_inputs']|native['outputs']
    prefix=manifest['prefix']; v=lambda name:values[prefix+name]
    checks=[]
    def compare(name,actual,expected,*,absolute=1e-5):
        checks.append({'name':name,'actual':actual,'expected':expected,'residual':actual-expected,
                       'absolute_tolerance':absolute,
                       'passed':math.isclose(actual,expected,rel_tol=1e-12,abs_tol=absolute)})
    # Explicit power ownership; these are arithmetic identities, not physical limits.
    power=lambda name,actual,expected:compare(name,actual,expected,absolute=1e-9)
    primary=v('heat_transport__loop_live')*v('heat_transport__primary_loop__p_elec')+v('heat_transport__p_pump_direct')
    recovered=v('heat_transport__loop_live')*v('heat_transport__primary_loop__w_fluid')+v('heat_transport__eta_p_direct')*v('heat_transport__p_pump_direct')
    power('selected_primary_pump_electric',v('heat_transport__primary_loop__p_pump_total'),primary)
    power('selected_primary_recovered_heat',v('heat_transport__primary_loop__q_recovered_total'),recovered)
    secondary=v('heat_transport__cooling_guard__energy_mode')
    pumping=primary+secondary*v('heat_transport__equipment__salt_electric_MW')
    recovered+=secondary*v('heat_transport__equipment__salt_shaft_MW')
    power('total_pump_electric_once',v('heat_transport__cooling_energy__electric_total'),pumping)
    power('total_recovered_shaft_heat_once',v('heat_transport__cooling_energy__recovered_total'),recovered)
    fusion=v('plasma__fusion__p_fus');alpha=(3.52/17.58)*fusion
    thermal=v('blanket__mn')*(fusion-alpha)+alpha+v('operating_heat__p_coupled')+recovered
    power('thermal_balance',v('pb__p_th'),thermal)
    matched=v('turbine__matched_cycle_enabled');water=v('heat_rejection__cooling_water_enabled')
    if matched not in (0,1) or water not in (0,1) or (water and not matched):
        raise ValueError('inconsistent matched-cycle/cooling-water modes')
    eta=v('turbine__matched_cycle__eta_gross') if matched else v('turbine__cycle__eta_th')
    power('selected_gross_efficiency',v('turbine__cycle_selection__eta_selected'),eta)
    steam_pumps=v('turbine__matched_cycle__p_cycle_pumps_MW')
    water_pump=v('heat_rejection__cooling_water__p_cooling_pump_electric_MW')
    if not matched:power('inactive_steam_pumps',steam_pumps,0.)
    if not water:power('inactive_cooling_water_pump',water_pump,0.)
    gross=eta*thermal
    if matched:
        m=lambda name:v('turbine__matched_cycle__'+name)
        power('matched_conversion_heat_join',v('heat_transport__equipment__conversion_heat_MW'),thermal)
        power('matched_branch_heat_sum',m('q_main_MW')+m('q_reheat_MW'),thermal)
        power('matched_salt_total_flow',m('salt_flow_total_kg_s'),v('heat_transport__equipment__salt_flow')*v('heat_transport__equipment__ihx_count'))
        power('matched_salt_branch_flow',m('salt_main_flow_kg_s')+m('salt_reheat_flow_kg_s'),m('salt_flow_total_kg_s'))
        power('matched_gross_matches_power_balance',m('p_gross_MW'),gross)
        power('steam_pump_electric_sum',steam_pumps,m('p_condensate_electric_MW')+m('p_feedwater_electric_MW'))
        shaft=m('p_hp_shaft_MW')+m('p_lp_shaft_MW')
        pump_shaft=m('p_condensate_shaft_MW')+m('p_feedwater_shaft_MW')
        power('matched_generator_conversion',gross,shaft*v('turbine__generator__mechanical_efficiency')*v('turbine__generator__generator_efficiency'))
        power('matched_shaft_balance',thermal+pump_shaft,shaft+m('q_condenser_MW'))
        power('matched_loss_sum',m('q_rejection_before_cooling_MW'),m('q_condenser_MW')+m('q_mechanical_loss_MW')+m('q_generator_loss_MW')+m('q_pump_motor_loss_MW'))
        power('matched_electric_balance',thermal+steam_pumps,gross+m('q_rejection_before_cooling_MW'))
        power('matched_cycle_net_before_cooling',m('p_cycle_net_before_cooling_MW'),gross-steam_pumps)
    if water:
        w=lambda name:v('heat_rejection__cooling_water__'+name)
        power('cooling_water_own_heat',w('q_total_rejection_MW'),v('turbine__matched_cycle__q_rejection_before_cooling_MW')+water_pump)
        power('cooling_water_motor_loss',w('q_cooling_motor_loss_MW'),water_pump-w('p_cooling_pump_shaft_MW'))
    power('gross_electric_conversion',v('pb__p_et'),gross)
    recirculating=(v('power_supplies__tf_power__total')+v('power_supplies__p_pf')+pumping
        +v('f_sub')*gross+v('fuel_cycle__p_trit')+v('p_house')
        +v('cryoplant__p_tfcool')+v('cryoplant__p_pfcool')
        +v('cryoplant__refrigeration_sum__total')+v('operating_heat__p_wallplug')+steam_pumps+water_pump)
    power('recirculating_power',v('pb__rec_frac')*gross,recirculating)
    power('net_electric_balance',v('pb__p_net'),gross-recirculating)
    power('historical_subsystem_allowance',v('f_sub')*gross,v('f_sub')*v('pb__p_et'))
    compare('cas23_gross_power_driver',v('turbine__turbine_cost__cost'),v('n_mod')*gross*v('turbine__cost_per_mw'))
    compare('cas24_gross_power_driver',v('electric_plant__electric_cost__cost'),v('n_mod')*gross*v('electric_plant__cost_per_mw'))
    compare('cas25_total_thermal_driver',v('heat_rejection__heat_rejection_cost__cost'),v('n_mod')*thermal*v('heat_rejection__cost_per_mw'))
    compare('cas26_gross_power_driver',v('misc_plant__misc_cost__cost'),v('n_mod')*gross*v('misc_plant__cost_per_mw'))
    for equation in manifest['accounting']:
        ids=[equation['parent'],*equation['children']]
        if any(mapped[key]['status']!='mapped' for key in ids): raise ValueError('incomplete account '+equation['id'])
        compare(equation['id'],mapped[ids[0]]['model_value'],sum(mapped[key]['model_value'] for key in ids[1:]))
    direct=inventory['direct_disjoint_rows']
    if len(direct)!=23 or len(set(direct))!=23:
        raise ValueError('direct-account inventory must contain 23 unique declared rows')
    compare('direct_disjoint_23',v('cas2x_pre_contingency__cas2x_pre_contingency'),sum(mapped[key]['model_value'] for key in direct))
    # Active equipment branches are held live in the declared forward scenario.
    if v('heat_transport__equipment_cost_mode')==1:
        compare('cooling_equipment_children',v('heat_transport__cooling_selection__cost'),sum(
            v('heat_transport__equipment__'+name) for name in ('primary_circulators_cost','primary_piping_cost',
            'exchangers_cost','secondary_pumps_cost','secondary_piping_cost','inventory_cost','spares_cost')))
    if v('buildings__facilities_cost_mode')==1:
        civil=facility_children(native['outputs'],inventory,prefix)
        compare('facilities_children',v('buildings__facility_accounts__cost'),sum(civil)+v('buildings__ventilation__cost_2025')+v('buildings__site_allowance__cost'))
    if v('fuel_cycle__processing_enabled')==1:
        compare('fuel_processing_children',v('fuel_cycle__processing_cost__cost'),sum(v('fuel_cycle__processing_cost__'+name)
            for name in ('cleanup_capital','cleanup_installation','distiller_capital','distiller_installation',
                         'transfer_capital','transfer_installation','containment_capital','containment_installation')))
    compare('cas72_selected_replacements',v('cooling_annual__cas72_total'),v('calendar__cas72_annual')+v('heat_transport__cooling_selection__replacement_annual'))
    cooling_exclusion=v('heat_transport__equipment_cost_mode')*v('heat_transport__equipment__delivered_total')
    facility_exclusion=v('buildings__facilities_cost_mode')*(1+v('contingency_rate'))*v('buildings__facility_accounts__installed_facility_capital')
    fuel_exclusion=(1+v('contingency_rate'))*v('fuel_cycle__processing_cost__installation_total')
    compare('shipping_cooling_exclusion',v('shipping_scope__cooling_exclusion'),cooling_exclusion)
    compare('shipping_facility_exclusion',v('shipping_scope__facility_exclusion'),facility_exclusion)
    compare('shipping_fuel_installation_exclusion',v('shipping_scope__fuel_installation_exclusion'),fuel_exclusion)
    remaining=v('cas20_capital__cas20_capital')-cooling_exclusion-facility_exclusion-fuel_exclusion
    if remaining<0: raise ValueError('shipping exclusions exceed their capital base')
    compare('remaining_shipping_base',v('shipping_scope__remaining_shipping_base'),remaining)
    supplementary=(v('supplementary__shipping_frac')*remaining
        +v('supplementary_spares_frac')*v('cas23_to_28_capital__cas23_to_28_capital')
        +v('supplementary__tax_frac')*v('cas20_capital__cas20_capital')
        +v('supplementary__insurance_frac')*(v('cas20_capital__cas20_capital')+v('indirect__cost'))
        +(v('supplementary_startup_base')+v('supplementary_decom_base'))*v('n_mod')*v('pb__p_net')/v('supplementary__ref_net_power'))
    compare('supplementary_shipping_and_other_costs',v('supplementary__cost'),supplementary*(1+v('supplementary__contingency_rate_in')))
    energy=8760*v('pb__p_net')*v('calendar__availability')
    if energy<=0: raise ValueError('nonpositive annual electricity prevents meaningful LCOE')
    financed=v('total_capital__total_capital')*(1+v('discount_rate'))**(v('construction_years')/2)
    compare('headline_lcoe',(financed*v('cas71_calc__crf')+v('cas70_calc__annual_total'))/energy,v('lcoe_calc__lcoe'))
    compare('comparison_lcoe',(v('cas90_1cfe_calc__cas90')+v('cas70_calc__annual_total'))/energy,v('lcoe_1cfe_calc__lcoe'))
    return {'status':'pass' if all(row['passed'] for row in checks) else 'fail',
            'source_sha256':digest(native_path),'checks':checks,'annual_energy_mwh':energy,
            'tolerance':{'relative':1e-12,'cost_absolute':1e-5,'power_mw_absolute':1e-9},
            'limitations':['Arithmetic consistency does not validate physical applicability or complete installed cost.',
                           'Steam-generator cost inclusion remains unverified; no duplicate allowance added.',
                           'Full historical subsystem allowance plus explicit steam/CW pumps retains unresolved overlap.',
                           'Cooling-water rejection is cycle-only and remains site-unqualified.',
                           'Mixed monetary years remain unresolved.']}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--native-result',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result,ok=exclusive_document(args.out,lambda:check(args.root,args.native_result),inputs=[args.native_result,Path(__file__).with_name('manifest.json')])
    raise SystemExit(0 if ok and result['status']=='pass' else 1)
