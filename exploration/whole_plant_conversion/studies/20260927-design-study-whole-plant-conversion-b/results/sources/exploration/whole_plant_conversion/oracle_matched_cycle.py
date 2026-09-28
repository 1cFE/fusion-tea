"""Independent WI-073 cycle oracle derived from original NIST HTML rows.

Authorship/derivation and original-source receipts: WI-073 evidence/independent-oracle.
No production or generated solver imports. Properties are an independently extracted
asset, shared original sources but independent transcription/implementation.
"""
from pathlib import Path
import hashlib
import json
import math

STATE_NAMES = ('feed','main','hp','reheat','lp','condensate','condensate_pumped','heater')
MATCHED_REALS = tuple(f'{p}_{s}_{unit}' for s in STATE_NAMES for p,unit in
                      [('p','MPa'),('h','kJ_kg'),('mdot','kg_s'),('t','C'),('s','kJ_kgK')]
                      if not (s=='condensate_pumped' and p in ('t','s'))) + (
    'bleed_fraction','mdot_bleed_kg_s','salt_flow_total_kg_s','salt_main_flow_kg_s','salt_reheat_flow_kg_s',
    'q_main_MW','q_reheat_MW','q_condenser_MW','p_hp_shaft_MW','p_lp_shaft_MW',
    'p_condensate_shaft_MW','p_feedwater_shaft_MW','p_condensate_electric_MW','p_feedwater_electric_MW',
    'p_cycle_pumps_MW','p_gross_MW','eta_gross','p_cycle_net_before_cooling_MW','q_mechanical_loss_MW',
    'q_generator_loss_MW','q_pump_motor_loss_MW','q_rejection_before_cooling_MW','lp_quality','lp_moisture_fraction',
    'main_min_gap_K','reheat_min_gap_K','main_UA_MW_K','reheat_UA_MW_K','salt_heat_residual_MW',
    'heater_mass_residual_kg_s','heater_energy_residual_MW','cycle_shaft_residual_MW','cycle_electric_residual_MW')
MATCHED_BOOLS = ('active','main_UA_available','reheat_UA_available','main_admission_ok',
                 'reheat_admission_ok','turbine_equipment_qualified','installed_sg_capacity_qualified')
COOLING_REALS = ('water_flow_kg_s','p_cooling_pump_shaft_MW','p_cooling_pump_electric_MW',
                 'q_cooling_motor_loss_MW','q_total_rejection_MW','water_pump_rise_K',
                 'condenser_water_gap_K','water_energy_residual_MW','denominator_kJ_kg')
COOLING_BOOLS = ('active','reference_scenario','site_qualified','cooling_approach_ok')


def inactive(reals, booleans):
    return {**dict.fromkeys(reals,0.),**dict.fromkeys(booleans,False)}


def check_mode(value):
    if value not in (0,1):
        raise ValueError('mode must be exactly 0 or 1')
    return value==1


def check_finite(values):
    if any(not math.isfinite(v) for v in values):
        raise ValueError('nonfinite active input')


def matched_interface(inputs, tables=None):
    """Independent contract adapter; inputs use inventory names without _in."""
    if not check_mode(inputs['enabled']):
        return inactive(MATCHED_REALS,MATCHED_BOOLS)
    check_finite(inputs.values())
    admitted = inputs['heat_available_MW']
    selected = inputs['source_heat_MW'] + inputs['selected_recovered_MW']
    if not math.isclose(admitted, selected, rel_tol=1e-12, abs_tol=1e-8):
        raise ValueError('matched heat differs from source plus selected recovered heat')
    if inputs['main_pressure_MPa']!=6.2 or inputs['extraction_pressure_MPa']!=.8:
        raise ValueError('fixed pressure table supports 6.2/0.8 MPa only')
    for key,value in inputs.items():
        if key.startswith('eta_') and not 0<value<=1:
            raise ValueError(f'efficiency outside (0,1]: {key}')
    for key in ('heat_available_MW','salt_flow_per_circuit','salt_circuit_count','salt_cp_kJ_kgK'):
        if inputs[key]<=0:
            raise ValueError(f'nonpositive {key}')
    flow = inputs['salt_flow_per_circuit']*inputs['salt_circuit_count']
    salt_heat = flow*inputs['salt_cp_kJ_kgK']*(inputs['salt_hot_C']-inputs['salt_return_C'])/1000
    if salt_heat<=0 or not math.isclose(inputs['heat_available_MW'],salt_heat,rel_tol=1e-12,abs_tol=1e-8):
        raise ValueError('inconsistent salt heat boundary')
    tables = load()[0] if tables is None else tables
    if inputs['steam_temperature_C']<=max(ref['t'] for ref in phase(tables['main'],'liquid')):
        raise ValueError('main steam must be superheated')
    if inputs['reheat_temperature_C']<=max(ref['t'] for ref in phase(tables['extraction'],'liquid')):
        raise ValueError('reheated steam must be superheated')
    output = cycle(tables,condenser=inputs['condenser_temperature_C'],steam=inputs['steam_temperature_C'],
                   reheat=inputs['reheat_temperature_C'],heat=inputs['heat_available_MW'],salt_flow=flow,
                   salt_hot=inputs['salt_hot_C'],salt_cold=inputs['salt_return_C'],salt_cp=inputs['salt_cp_kJ_kgK'],
                   eta_hp=inputs['eta_hp'],eta_lp=inputs['eta_lp'],eta_cp=inputs['eta_condensate_pump'],
                   eta_fp=inputs['eta_feedwater_pump'],eta_motor=inputs['eta_pump_motor'],
                   eta_mechanical=inputs['eta_mechanical'],eta_generator=inputs['eta_generator'])
    assert set(output)==set(MATCHED_REALS+MATCHED_BOOLS)
    return output


def cooling_interface(inputs,tables=None):
    if not check_mode(inputs['enabled']):
        return inactive(COOLING_REALS,COOLING_BOOLS)
    if not check_mode(inputs['cycle_active']):
        raise ValueError('cooling requires active matched cycle')
    check_finite(inputs.values())
    if not inputs['water_inlet_C']<inputs['water_outlet_C'] or inputs['head_m']<0:
        raise ValueError('invalid cooling water temperature order or head')
    if not 0<inputs['eta_pump']<=1 or not 0<inputs['eta_motor']<=1:
        raise ValueError('invalid cooling water efficiency')
    if inputs['q_rejection_before_cooling_MW']<=0:
        raise ValueError('nonpositive rejection')
    tables = load()[0] if tables is None else tables
    out = cooling(tables,{'q_rejection_before_cooling_MW':inputs['q_rejection_before_cooling_MW'],
                          't_condensate_C':inputs['condenser_temperature_C']},
                  inlet=inputs['water_inlet_C'],outlet=inputs['water_outlet_C'],head=inputs['head_m'],
                  eta_pump=inputs['eta_pump'],eta_motor=inputs['eta_motor'])
    assert set(out)==set(COOLING_REALS+COOLING_BOOLS)
    return out


def selection_interface(inputs):
    selected = check_mode(inputs['matched_enabled'])
    return {'eta_selected':inputs['matched_eta'] if selected else inputs['legacy_eta'],
            'legacy_domain_applicable':not selected,'matched_domain_applicable':selected}


def load():
    path = Path(__file__).with_name("oracle_matched_cycle_properties.json")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != "b8e5a7d156c7422d95b654bc073e273fd663fc86b6c2151f56b90caec3a40b7b":
        raise ValueError("independent matched-cycle property asset digest mismatch")
    return json.loads(raw), {}

def interp(rows, key, value):
    rows = sorted(rows, key=lambda r:r[key])
    if not rows[0][key] <= value <= rows[-1][key]:
        raise ValueError(f'{key}={value} outside [{rows[0][key]}, {rows[-1][key]}]')
    for r in rows:
        if r[key] == value:
            return dict(r)
    for a, b in zip(rows, rows[1:]):
        if a[key] < value < b[key]:
            f = (value-a[key])/(b[key]-a[key])
            return {k: a[k]+f*(b[k]-a[k]) for k in a if k!='phase'}
    raise AssertionError('interpolation interval missing')


def phase(table, name):
    return [r for r in table if r['phase']==name]


def profile(table, low, high, mass, salt_cold, salt_hot):
    # Water coordinate increases from inlet to outlet; countercurrent salt
    # temperature increases linearly with transferred enthalpy on this axis.
    points = [(low['h'], low['t'])]
    points += [(r['h'],r['t']) for r in table if low['h'] < r['h'] < high['h']]
    points += [(high['h'],high['t'])]
    points.sort()
    gaps = [salt_cold+(salt_hot-salt_cold)*(h-low['h'])/(high['h']-low['h'])-t for h,t in points]
    minimum = min(gaps)
    if minimum <= 0:
        return minimum, 0., False
    integrals = []
    for (a,_),(b,_), ga, gb in zip(points,points[1:],gaps,gaps[1:]):
        dq = mass*(b-a)/1000
        # Integral dQ/(a+bQ): logarithmic mean; stable equal-gap limit.
        integrals.append(dq/ga if ga==gb else dq*math.log1p((gb-ga)/ga)/(gb-ga))
    return minimum, math.fsum(integrals), True


def cycle(tables, condenser=42., steam=445., reheat=445., heat=3306.889098848892,
          salt_flow=10852.114436183412, salt_hot=465., salt_cold=269.664729914530,
          salt_cp=1.560, eta_hp=.9, eta_lp=.9, eta_cp=.8, eta_fp=.8,
          eta_motor=.95, eta_mechanical=.99, eta_generator=.98):
    main, ext, sat = tables['main'], tables['extraction'], tables['saturation']
    liquid, vapor = phase(sat,'liquid'), phase(sat,'vapor')
    c, cv = interp(liquid,'t',condenser), interp(vapor,'t',condenser)
    heater = max(phase(ext,'liquid'),key=lambda r:r['t'])
    cpwork = c['v']*(.8-c['p'])*1000/eta_cp
    cp = {'p':.8,'h':c['h']+cpwork}
    fpwork = heater['v']*(6.2-.8)*1000/eta_fp
    feed = interp(phase(main,'liquid'),'h',heater['h']+fpwork)
    m = interp(phase(main,'vapor'),'t',steam)
    idealhp = interp(ext,'s',m['s'])
    hp = interp(ext,'h',m['h']-eta_hp*(m['h']-idealhp['h']))
    rh = interp(phase(ext,'vapor'),'t',reheat)
    xideal = (rh['s']-c['s'])/(cv['s']-c['s'])
    if not 0 <= xideal <= 1:
        raise ValueError('LP isentropic endpoint outside two phase domain')
    hlpideal = c['h']+xideal*(cv['h']-c['h'])
    hlp = rh['h']-eta_lp*(rh['h']-hlpideal)
    quality = (hlp-c['h'])/(cv['h']-c['h'])
    if not 0 <= quality <= 1:
        raise ValueError('LP actual endpoint outside two phase domain')
    lp = {'p':c['p'],'t':condenser,'h':hlp,'s':c['s']+quality*(cv['s']-c['s'])}
    bleed = (heater['h']-cp['h'])/(hp['h']-cp['h'])
    assert 0 < bleed < 1
    qmain = m['h']-feed['h']
    qrh = (1-bleed)*(rh['h']-hp['h'])
    flow = heat*1000/(qmain+qrh)
    lowflow = flow*(1-bleed)
    states = {'feed':feed,'main':m,'hp':hp,'reheat':rh,'lp':lp,'condensate':c,'condensate_pumped':cp,'heater':heater}
    o = {}
    for name, st in states.items():
        for prop, unit in [('p','MPa'),('h','kJ_kg'),('s','kJ_kgK'),('t','C')]:
            if prop in st:
                o[f'{prop}_{name}_{unit}'] = st[prop]
        o[f'mdot_{name}_kg_s'] = lowflow if name in ('reheat','lp','condensate','condensate_pumped') else flow
    o.update(bleed_fraction=bleed, mdot_bleed_kg_s=flow*bleed, salt_flow_total_kg_s=salt_flow,
             q_main_MW=flow*qmain/1000, q_reheat_MW=flow*qrh/1000,
             q_condenser_MW=lowflow*(hlp-c['h'])/1000,
             p_hp_shaft_MW=flow*(m['h']-hp['h'])/1000,
             p_lp_shaft_MW=lowflow*(rh['h']-hlp)/1000,
             p_condensate_shaft_MW=lowflow*cpwork/1000,
             p_feedwater_shaft_MW=flow*fpwork/1000,
             lp_quality=quality, lp_moisture_fraction=1-quality)
    for label in ('condensate','feedwater'):
        o[f'p_{label}_electric_MW'] = o[f'p_{label}_shaft_MW']/eta_motor
    pumps = o['p_condensate_shaft_MW']+o['p_feedwater_shaft_MW']
    turbine = o['p_hp_shaft_MW']+o['p_lp_shaft_MW']
    o['p_cycle_pumps_MW'] = pumps/eta_motor
    o['q_mechanical_loss_MW'] = turbine*(1-eta_mechanical)
    o['q_generator_loss_MW'] = turbine*eta_mechanical*(1-eta_generator)
    o['q_pump_motor_loss_MW'] = o['p_cycle_pumps_MW']-pumps
    o['p_gross_MW'] = turbine*eta_mechanical*eta_generator
    o['eta_gross'] = o['p_gross_MW']/heat
    o['p_cycle_net_before_cooling_MW'] = o['p_gross_MW']-o['p_cycle_pumps_MW']
    o['q_rejection_before_cooling_MW'] = math.fsum(o[k] for k in ('q_condenser_MW','q_mechanical_loss_MW','q_generator_loss_MW','q_pump_motor_loss_MW'))
    o['salt_main_flow_kg_s'] = salt_flow*o['q_main_MW']/heat
    o['salt_reheat_flow_kg_s'] = salt_flow*o['q_reheat_MW']/heat
    o['salt_heat_residual_MW'] = heat-salt_flow*salt_cp*(salt_hot-salt_cold)/1000
    # Signed interface: total inlet mass minus mixed outlet mass.
    o['heater_mass_residual_kg_s'] = math.fsum((lowflow, flow*bleed, -flow))
    o['heater_energy_residual_MW'] = (lowflow*cp['h']+flow*bleed*hp['h']-flow*heater['h'])/1000
    o['cycle_shaft_residual_MW'] = heat+pumps-turbine-o['q_condenser_MW']
    o['cycle_electric_residual_MW'] = heat-o['p_cycle_net_before_cooling_MW']-o['q_rejection_before_cooling_MW']
    for name, table, lo, hi, mdot in [('main',main,feed,m,flow),('reheat',ext,hp,rh,lowflow)]:
        gap, ua, available = profile(table,lo,hi,mdot,salt_cold,salt_hot)
        o[f'{name}_min_gap_K'], o[f'{name}_UA_MW_K'] = gap,ua
        o[f'{name}_UA_available'],o[f'{name}_admission_ok'] = available,gap>0
    o.update(active=True,turbine_equipment_qualified=False,installed_sg_capacity_qualified=False)
    return o


def cooling(tables, cycle_result, inlet=25., outlet=35., head=20., eta_pump=.8, eta_motor=.95):
    liquid = phase(tables['saturation'],'liquid')
    a,b = interp(liquid,'t',inlet),interp(liquid,'t',outlet)
    dh = b['h']-a['h']
    shaft = 9.80665*head/eta_pump/1000  # MW conversion follows the source-owned shaft-work operation order.
    elec = shaft/eta_motor
    denominator = dh-elec
    if denominator<=0:
        raise ValueError('nonpositive cooling water heat capacity after pump heating')
    rejection = cycle_result['q_rejection_before_cooling_MW']
    flow = rejection*1000/denominator
    gap = cycle_result['t_condensate_C']-outlet
    return dict(water_flow_kg_s=flow,p_cooling_pump_shaft_MW=flow*shaft/1000,
                p_cooling_pump_electric_MW=flow*elec/1000,q_cooling_motor_loss_MW=flow*(elec-shaft)/1000,
                q_total_rejection_MW=rejection+flow*elec/1000,
                water_pump_rise_K=elec/(dh/(outlet-inlet)),condenser_water_gap_K=gap,
                water_energy_residual_MW=flow*dh/1000-rejection-flow*elec/1000,
                denominator_kJ_kg=denominator,active=True,reference_scenario=True,site_qualified=False,cooling_approach_ok=gap>0)
