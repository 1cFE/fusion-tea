"""Independent WI-067 quantity oracle reconstructed from released design/source notes.

No production calculator is imported. Prices are USD2025 CPI proxies unless a
source year is part of the output name. This verifies arithmetic, not equipment
qualification or completeness of the declared Row7 boundary.
"""

import math
from collections.abc import Mapping

CPI = {1978: 65.2, 2006: 201.6, 2011: 224.9, 2017: 245.1,
       2021: 271.0, 2024: 313.7, 2025: 321.9}
HP_W = 745.6998715822702
G = 9.80665

DEFAULTS = {'enabled': False,
 'n_mod': 1,
 'n_loops': 18,
 'mdot_loop': 156.575,
 'dp_loop': 159300,
 'helium_suction_K': 567.221,
 'helium_discharge_Pa': 8000000.0,
 'helium_hot_K': 773.15,
 'helium_cp': 5193,
 'helium_gamma': 1.6666666666666667,
 'primary_shaft_MW': 86.7762,
 'primary_electric_MW': 86.7762,
 'q_ihx_MW': 3013.914942,
 'layout_multiplier': 1,
 'tube_wall': 0.0015,
 'shell_wall': 0.2,
 'accessory_mass': 10000,
 'secondary_head': 40,
 'eta_p': 0.75,
 'eta_motor': 0.95,
 'machine_life': 10,
 'bundle_life': 15,
 'years': 30,
 'discount': 0.07,
 'makeup_fraction': 0.001,
 'inventory_reserve': 0.1,
 'removal_multiplier': 1,
 'saltprice_source_choice': 0,
 'costscale': 1,
 'fabrication_rate_2017': 310,
 'sourcefitargument_C': 480}
NUMERIC_OUTPUTS = ('primary_circulators_cost',
 'primary_piping_cost',
 'exchangers_cost',
 'secondary_pumps_cost',
 'secondary_piping_cost',
 'inventory_cost',
 'spares_cost',
 'purchased_total',
 'installation_total',
 'installed_total',
 'delivered_total',
 'primary_vendor',
 'primary_installation',
 'primary_design',
 'primary_spare',
 'secondary_vendor',
 'secondary_installation',
 'secondary_spare',
 'hx_purchase',
 'hx_installation',
 'primary_pipe_purchase',
 'primary_pipe_installation',
 'secondary_pipe_purchase',
 'secondary_pipe_installation',
 'helium_inventory_cost',
 'salt_inventory_cost',
 'machine_event_purchase',
 'machine_event_installation',
 'machine_event_removal',
 'bundle_event_purchase',
 'bundle_event_installation',
 'bundle_event_removal',
 'replacement_annual',
 'consumables_annual',
 'helium_makeup_annual',
 'salt_makeup_annual',
 'salt_electric_MW',
 'salt_shaft_MW',
 'conversion_heat_MW',
 'circulator_shaft_MW',
 'circulator_electric_MW',
 'ihx_duty_MW',
 'tube_mass',
 'shell_mass',
 'heads_mass',
 'sheets_mass',
 'hx_mass',
 'bundle_mass',
 'primary_pipe_mass',
 'secondary_pipe_mass',
 'helium_inventory_mass',
 'salt_inventory_mass',
 'primary_pipe_volume',
 'helium_hx_volume',
 'helium_inventory_volume',
 'helium_standard_volume',
 'salt_pipe_volume',
 'salt_hx_volume',
 'salt_inventory_volume',
 'ihx_installed_area',
 'ihx_required_area',
 'circulator_count',
 'salt_pump_count',
 'source_volume_ratio',
 'salt_expansion_ratio',
 'salt_Re_hot',
 'salt_Re_cold',
 'pump_size_factor',
 'pump_shaft_hp',
 'motor_electric_hp',
 'machine_events',
 'bundle_events',
 'salt_price_raw',
 'salt_price_year',
 'salt_unit_price',
 'helium_price_raw',
 'helium_price_year',
 'circulator_flow',
 'circulator_volume',
 'circulator_suction_Pa',
 'ihx_hot_approach',
 'ihx_cold_approach',
 'ihx_lmtd',
 'salt_flow',
 'salt_velocity_hot',
 'salt_velocity_cold',
 'salt_straight_loss',
 'salt_head_remaining',
 'salt_return_C',
 'cycle_temperature_gap',
 'pump_flow_gpm',
 'pump_head_ft',
 'salt_pump_flow',
 'salt_pump_shaft_MW',
 'ihx_count')
BOOLEAN_OUTPUTS = ('ihx_capacity_ok',
 'pump_size_ok',
 'pump_type_ok',
 'motor_base_ok',
 'motor_factor_ok',
 'salt_head_ok',
 'salt_flow_regime_ok',
 'cycle_interface_ok',
 'salt_bulk_scale_ok',
 'inventory_source_volume_ok',
 'pressure_qualified',
 'helium_price_transfer_validated',
 'salt_pump_transfer_validated',
 'inventory_complete')


def _annulus(inside, wall, length):
    return math.pi * wall * (inside + wall) * length


def _lmtd(a, b):
    if min(a, b) <= 0:
        raise ValueError("Heat exchanger terminal approaches must be positive")
    return a if a == b else (a - b) / math.log(a / b)


def _annual_replacement(cost, life, horizon, rate):
    """Sum actual strict-before-horizon events; avoids geometric-series cancellation."""
    if min(life, horizon) <= 0 or rate < 0:
        raise ValueError("Positive life/horizon and nonnegative discount required")
    crf = 1 / horizon if rate == 0 else rate / -math.expm1(-horizon * math.log1p(rate))
    n = math.ceil(horizon / life) - 1
    return cost * crf * math.fsum(math.exp(-k * life * math.log1p(rate)) for k in range(1, n + 1))


def _pump_price(flow_m3_s, head_m, electric_W):
    flow_gpm = flow_m3_s * 60 / 0.003785411784
    head_ft = head_m / 0.3048
    size = flow_gpm * math.sqrt(head_ft)
    s = math.log(size)
    pump = 3 * math.exp(9.7171 - 0.6019 * s + 0.0519 * s * s)
    p = math.log(electric_W / HP_W)
    motor = 1.3 * math.exp(5.8259 + 0.13141*p + 0.053255*p**2 + 0.028628*p**3 - 0.0035549*p**4)
    return pump, motor, flow_gpm, head_ft, size


def _pipe_diagnostics(mdot, diameter, hot_length, cold_length):
    area = math.pi * diameter**2 / 4
    out = {}
    loss = 0.0
    for name, temperature, length in (("cold", 270, cold_length), ("hot", 465, hot_length)):
        rho = max(2080 - 0.733 * temperature, 1000)
        mu = max(0.00622 - 0.0000102 * temperature, 1e-6)
        v = mdot / (rho * area)
        re = mdot * diameter / (area * mu)
        f = 64/re if re < 2300 else (-1.8*math.log10(6.9/re))**-2
        loss += f * length / diameter * v*v / (2*G)
        out.update({f"{name}_velocity": v, f"{name}_reynolds": re, f"{name}_darcy": f})
    out["loss"] = loss
    return out


def calculate(inputs: Mapping) -> dict:
    """Evaluate interface inputs; dormant mode returns zero with false predicates."""
    x = dict(DEFAULTS)
    x.update(inputs)
    out = dict.fromkeys(NUMERIC_OUTPUTS, 0.0)
    out.update(dict.fromkeys(BOOLEAN_OUTPUTS, False))
    if not isinstance(x['enabled'], bool):
        raise ValueError('enabled must be Boolean')
    if not x['enabled']:
        return out
    for key in DEFAULTS:
        if key != 'enabled' and not math.isfinite(x[key]):
            raise ValueError(f'Nonfinite {key}')
    if isinstance(x['fabrication_rate_2017'], bool):
        raise ValueError('Fabrication rate must be numeric, not Boolean')
    n = x['n_loops']
    if x['n_mod'] != 1 or n < 1 or n != int(n):
        raise ValueError('Active equipment requires one module and integer positive circuits')
    for key in ('mdot_loop', 'dp_loop', 'helium_suction_K', 'helium_hot_K', 'helium_cp',
                'primary_shaft_MW', 'primary_electric_MW', 'q_ihx_MW', 'layout_multiplier',
                'tube_wall', 'shell_wall', 'secondary_head', 'machine_life', 'bundle_life', 'years', 'fabrication_rate_2017'):
        if x[key] <= 0:
            raise ValueError(f'Nonpositive {key}')
    if x['tube_wall'] >= .01905/2 or x['helium_gamma'] <= 1:
        raise ValueError('Invalid tube wall or helium gamma')
    if not 0 < x['eta_p'] <= 1 or not 0 < x['eta_motor'] <= 1:
        raise ValueError('Invalid efficiency')
    for key in ('accessory_mass', 'discount', 'makeup_fraction', 'inventory_reserve', 'removal_multiplier', 'costscale'):
        if x[key] < 0:
            raise ValueError(f'Negative {key}')
    if x['saltprice_source_choice'] not in (0, 1):
        raise ValueError('Salt price choice must be 0 or 1')
    pi = math.pi
    R = x['helium_cp'] * (1 - 1/x['helium_gamma'])
    suction = x['helium_discharge_Pa'] - x['dp_loop']
    if suction <= 0:
        raise ValueError('Nonpositive helium suction pressure')
    count = 2*n
    out.update(circulator_count=count, salt_pump_count=count, ihx_count=n,
               circulator_flow=x['mdot_loop']/2, circulator_suction_Pa=suction,
               circulator_volume=x['mdot_loop']/2 * R*x['helium_suction_K']/suction,
               circulator_shaft_MW=x['primary_shaft_MW']/count,
               circulator_electric_MW=x['primary_electric_MW']/count,
               ihx_duty_MW=x['q_ihx_MW']/n)
    hot, cold = x['helium_hot_K']-738.15, x['helium_suction_K']-543.15
    installed_area = 14852*pi*.01905*11.6
    uf = 267.8e6/(installed_area * _lmtd(35, 19.3))
    lmtd = _lmtd(hot, cold)
    required_area = x['q_ihx_MW']*1e6/n/uf/lmtd
    out.update(ihx_hot_approach=hot, ihx_cold_approach=cold, ihx_lmtd=lmtd,
               ihx_installed_area=installed_area, ihx_required_area=required_area,
               ihx_capacity_ok=required_area <= installed_area)
    tube_mass = 8000*_annulus(.01905-2*x['tube_wall'], x['tube_wall'], 14852*11.6)
    shell_mass = 8000*_annulus(3.2, x['shell_wall'], 13)
    heads_mass = 8000*4*pi/3*((1.6+x['shell_wall'])**3-1.6**3)
    sheets_mass = 8000*2*pi*1.6**2*.6
    hx_mass = tube_mass+shell_mass+heads_mass+sheets_mass+x['accessory_mass']
    out.update(tube_mass=tube_mass, shell_mass=shell_mass, heads_mass=heads_mass,
               sheets_mass=sheets_mass, hx_mass=hx_mass, bundle_mass=tube_mass+x['accessory_mass'])
    layout=x['layout_multiplier']
    steel_volume=pipe_volume=0.0
    for diameter in (1.17, .97):
        for bore, wall, length in ((diameter,.065,50), (diameter/3,.030,9*(4000/9-100)/18)):
            steel_volume += _annulus(bore, wall, length*layout)
            pipe_volume += pi*bore*bore/4*length*layout
    fittings = 1+14440/66560
    primary_pipe_mass = steel_volume*8000*fittings*n
    salt_pipe_mass = _annulus(.4,.02,100*layout)*8000*fittings*n
    he_pipe = pipe_volume*n
    he_hx = 61.5*n
    reserve = 1+x['inventory_reserve']
    he_volume = (he_pipe+he_hx)*reserve
    he_mean = (x['helium_hot_K']+x['helium_suction_K'])/2
    he_mass = he_volume*x['helium_discharge_Pa']/(R*he_mean)
    he_std = he_mass*R*288.15/101325
    salt_pipe = pi*.4**2/4*100*layout*n
    salt_hx = (pi*1.6**2*11.6 - pi*.01905**2/4*14852*11.6 - x['accessory_mass']/8000)*n
    if salt_hx <= 0:
        raise ValueError('Nonpositive salt exchanger void')
    salt_volume = (salt_pipe+salt_hx)*reserve
    salt_mass = salt_volume*1882.09
    out.update(primary_pipe_mass=primary_pipe_mass, secondary_pipe_mass=salt_pipe_mass,
               primary_pipe_volume=he_pipe, helium_hx_volume=he_hx,
               helium_inventory_volume=he_pipe+he_hx, helium_inventory_mass=he_mass,
               helium_standard_volume=he_std, salt_pipe_volume=salt_pipe,
               salt_hx_volume=salt_hx, salt_inventory_volume=salt_pipe+salt_hx,
               salt_inventory_mass=salt_mass, source_volume_ratio=(he_pipe+he_hx)/(879*n/9),
               salt_expansion_ratio=1882.09/1739.155,
               inventory_source_volume_ok=he_pipe+he_hx <= 879*n/9,
               salt_bulk_scale_ok=salt_mass > 1e7)
    mdot = x['q_ihx_MW']*1e6/(1560*195*n)
    shaft_W = mdot*n*G*x['secondary_head']/x['eta_p']
    electric_W = shaft_W/x['eta_motor']
    pump, motor, gpm, head_ft, size = _pump_price(mdot/2/1882.09,x['secondary_head'],electric_W/count)
    diagnostics = _pipe_diagnostics(mdot,.4,50*layout,50*layout)
    shaft_hp = shaft_W/count/HP_W
    motor_hp = electric_W/count/HP_W
    out.update(salt_flow=mdot, salt_pump_flow=mdot/2, salt_pump_shaft_MW=shaft_W/count/1e6, salt_shaft_MW=shaft_W/1e6, salt_electric_MW=electric_W/1e6,
               conversion_heat_MW=x['q_ihx_MW']+shaft_W/1e6,
               salt_return_C=270-shaft_W/(mdot*n*1560),
               salt_velocity_hot=diagnostics['hot_velocity'],salt_velocity_cold=diagnostics['cold_velocity'],
               salt_Re_hot=diagnostics['hot_reynolds'],salt_Re_cold=diagnostics['cold_reynolds'],
               salt_straight_loss=diagnostics['loss'], salt_head_remaining=x['secondary_head']-diagnostics['loss'],
               pump_flow_gpm=gpm,pump_head_ft=head_ft,pump_size_factor=size,pump_shaft_hp=shaft_hp,
               motor_electric_hp=motor_hp, pump_size_ok=400<=size<=100000,
               pump_type_ok=50<=gpm<=3500 and 50<=head_ft<=200 and shaft_hp<=200,
               motor_base_ok=1<=motor_hp<=700,motor_factor_ok=1<=motor_hp<=250,
               salt_head_ok=diagnostics['loss']<=x['secondary_head'],
               salt_flow_regime_ok=all(not 2300<=diagnostics[k]<4000 for k in ('hot_reynolds','cold_reynolds')),
               cycle_temperature_gap=x['sourcefitargument_C']-465,
               cycle_interface_ok=x['sourcefitargument_C']<=465)
    money = lambda amount, year: amount*CPI[2025]/CPI[year]*x['costscale']
    machine = 550000*(.5+.5*(suction/(735*6894.757293168))*(out['circulator_shaft_MW']*1e6/HP_W/50)**.28)
    primary_each = money(1.2*machine,1978)
    secondary_each = money(pump+motor,2006)
    vendor_p, vendor_s = primary_each*count, secondary_each*count
    assembly_factor=.27*1.155
    install_p,install_s = vendor_p*assembly_factor,vendor_s*assembly_factor
    hx_purchase=money(x['fabrication_rate_2017']*hx_mass*n,2017)
    pp=money(x['fabrication_rate_2017']*primary_pipe_mass,2017)
    sp=money(x['fabrication_rate_2017']*salt_pipe_mass,2017)
    price,year=(1.23,2011) if x['saltprice_source_choice']==0 else (2.53,2021)
    salt_unit=money(price,year)
    he_cost=money(14*he_std,2024)
    salt_cost=salt_mass*salt_unit
    design=money(130000,1978)
    out.update(primary_vendor=vendor_p,primary_installation=install_p,primary_design=design,
               primary_spare=primary_each, secondary_vendor=vendor_s,secondary_installation=install_s,
               secondary_spare=secondary_each,hx_purchase=hx_purchase,hx_installation=.026*hx_purchase,
               primary_pipe_purchase=pp,primary_pipe_installation=.5*pp,
               secondary_pipe_purchase=sp,secondary_pipe_installation=.5*sp,
               helium_inventory_cost=he_cost,salt_inventory_cost=salt_cost,
               salt_price_raw=price,salt_price_year=year,salt_unit_price=salt_unit,
               helium_price_raw=14,helium_price_year=2024,
               primary_circulators_cost=vendor_p+install_p+design,primary_piping_cost=1.5*pp,
               exchangers_cost=1.026*hx_purchase,secondary_pumps_cost=vendor_s+install_s,
               secondary_piping_cost=1.5*sp,inventory_cost=he_cost+salt_cost,
               spares_cost=primary_each+secondary_each)
    out['purchased_total']=vendor_p+vendor_s+design+hx_purchase+pp+sp+he_cost+salt_cost+primary_each+secondary_each
    out['installation_total']=install_p+install_s+.026*hx_purchase+.5*(pp+sp)
    out['installed_total']=out['purchased_total']+out['installation_total']
    out['delivered_total']=vendor_p+primary_each+hx_purchase+pp+sp
    bundle=money(x['fabrication_rate_2017']*(tube_mass+x['accessory_mass'])*n,2017)
    machine_install=install_p+install_s
    out.update(machine_event_purchase=vendor_p+vendor_s,machine_event_installation=machine_install,
               machine_event_removal=machine_install*x['removal_multiplier'],bundle_event_purchase=bundle,
               bundle_event_installation=.026*bundle,bundle_event_removal=.024*bundle*x['removal_multiplier'],
               machine_events=math.ceil(x['years']/x['machine_life'])-1,
               bundle_events=math.ceil(x['years']/x['bundle_life'])-1,
               helium_makeup_annual=he_cost*x['makeup_fraction'],salt_makeup_annual=salt_cost*x['makeup_fraction'],
               consumables_annual=(he_cost+salt_cost)*x['makeup_fraction'])
    annual=0.0
    for group,life in (('machine',x['machine_life']),('bundle',x['bundle_life'])):
        event=sum(out[f'{group}_event_{part}'] for part in ('purchase','installation','removal'))
        annual+=_annual_replacement(event,life,x['years'],x['discount'])
    out['replacement_annual']=annual
    return out
