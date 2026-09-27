"""WI-096 selected salt machine count; retained WI-080/WI-078 equipment equations.

calculate contains the guarded equations. The typed wrapper follows the native generated ABI.
All costs USD2025 annual-CPI purchasing-power proxies, not equipment escalation.
WI-071 shares one raw USD2017/kg finished-fabrication rate across four bills.
ANL January2017 basis uses the inherited annual CPI ratio 321.9/245.1.
"""
from __future__ import annotations

import math

AUTO_IMPLEMENTED = False
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from whole_plant_conversion_tea.modules.cooling_equipment_selected_pumps.cooling_equipment_with_selected_salt_pump_count import Cooling_Equipment_With_Selected_Salt_Pump_CountInput


def calculate(inputs):
    x = dict(inputs)
    # OUTPUT_NAMES is embedded below; no dependency on runtime files or project code.
    out = {name: False if name in BOOL_OUTPUTS else 0.0 for name in OUTPUT_NAMES}
    if not isinstance(x['enabled'], bool):
        raise ValueError('enabled must be Boolean')
    if not x['enabled']:
        return out
    for name, value in x.items():
        if name != 'enabled' and (isinstance(value, bool) or not math.isfinite(value)):
            raise ValueError(f'{name} must be finite numeric')
    positive = ('n_loops','mdot_loop','dp_loop','helium_suction_K','helium_discharge_Pa','helium_hot_K','helium_cp','primary_shaft_MW','primary_electric_MW','q_ihx_MW','layout_multiplier','tube_wall','shell_wall','secondary_head','eta_p','eta_motor','machine_life','bundle_life','years','costscale','stainless_fabrication_usd2017_per_kg')
    if any(x[k] <= 0 for k in positive):
        raise ValueError('active equipment requires positive dimensions, flows, powers and lives')
    if x['n_mod'] != 1 or x['n_loops'] != int(x['n_loops']):
        raise ValueError('equipment supports one module and integer circuit count')
    if x['helium_gamma'] <= 1 or x['eta_p'] > 1 or x['eta_motor'] > 1 or x['primary_shaft_MW'] > x['primary_electric_MW']:
        raise ValueError('invalid gas ratio or efficiency/power ordering')
    if any(x[k] < 0 for k in ('accessory_mass','discount','makeup_fraction','inventory_reserve','removal_multiplier')) or x['makeup_fraction'] > 1:
        raise ValueError('negative allowance or invalid makeup fraction')
    if x['saltprice_source_choice'] not in (0, 1):
        raise ValueError('salt price source must be 0 (2011 bulk) or 1 (2021 small/pure)')
    if x['tube_wall'] >= .01905/2 or x['helium_discharge_Pa'] <= x['dp_loop']:
        raise ValueError('invalid tube bore or helium suction pressure')
    for key in ('helium_design_shaft_MW', 'helium_design_suction_Pa', 'salt_design_flow_kg_s', 'salt_design_head_m'):
        if x[key] <= 0: raise ValueError(f'{key} must be positive')
    for key in ('salt_design_eta_p', 'salt_design_eta_motor'):
        if not 0 < x[key] <= 1: raise ValueError(f'{key} must be in (0,1]')
    for key in ('helium_purchased_mass_kg', 'salt_purchased_mass_kg'):
        if x[key] < 0: raise ValueError(f'{key} must be nonnegative')
    k=x['salt_pumps_per_circuit']
    if k <= 0 or k != int(k):
        raise ValueError('salt_pumps_per_circuit must be a positive integer')
    n=x['n_loops']; scale=x['costscale']; pi=math.pi; rho_steel=8000.; hp=745.6998715822702; g=9.80665
    c78=321.9/65.2*scale; c06=321.9/201.6*scale; c17=321.9/245.1*scale
    install_pump=.27*(1+.155)
    def put(**kw): out.update(kw)
    ps=x['helium_discharge_Pa']-x['dp_loop']; gas_R=x['helium_cp']*(x['helium_gamma']-1)/x['helium_gamma']
    rho_he=ps/(gas_R*x['helium_suction_K'])
    shaft=x['primary_shaft_MW']/(2*n); electric=x['primary_electric_MW']/(2*n)
    # BNL pumping-duty denominator50hp, not motor nameplate140hp. Shaft
    # pumping duty is independent of external motor losses.
    machine78=550000*(.5+.5*(x['helium_design_suction_Pa']/(735*6894.757293168))*(x['helium_design_shaft_MW']*1e6/hp/50)**.28)
    package=(1+110000/550000)*machine78*c78
    pv=2*n*package; pinstall=install_pump*pv; pdesign=130000*c78
    put(circulator_count=2*n,circulator_flow=x['mdot_loop']/2,circulator_volume=x['mdot_loop']/(2*rho_he),circulator_suction_Pa=ps,circulator_shaft_MW=shaft,circulator_electric_MW=electric,primary_vendor=pv,primary_installation=pinstall,primary_design=pdesign,primary_spare=package,primary_circulators_cost=pv+pinstall+pdesign)
    # Fixed installed exchanger geometry and demand-derived capacity screen.
    od=.01905; tube_count=14852; length=11.6; area=tube_count*pi*od*length
    t=x['tube_wall']; sw=x['shell_wall']; ri=1.6; ro=ri+sw; shell_length=13.0
    put(hx_shell_bore=2*ri, hx_shell_wall=sw,
        hx_shell_length=shell_length, hx_tube_length=length)
    tube=rho_steel*area*t*(1-t/od)
    shell=rho_steel*pi*(ro*ro-ri*ri)*shell_length
    heads=rho_steel*4*pi/3*(ro**3-ri**3)
    sheets=2*rho_steel*pi*ri**2*.60
    hxmass=tube+shell+heads+sheets+x['accessory_mass']; bundle=tube+x['accessory_mass']
    hot=x['helium_hot_K']-738.15; cold=x['helium_suction_K']-543.15
    if min(hot,cold) <= 0: raise ValueError('nonpositive IHX terminal approach')
    lmtd=hot if math.isclose(hot,cold,rel_tol=1e-12) else (hot-cold)/math.log(hot/cold)
    uf=267.8e6/(area*((35-19.3)/math.log(35/19.3)))
    required=x['q_ihx_MW']*1e6/n/(uf*lmtd)
    hxp=hxmass*n*x['stainless_fabrication_usd2017_per_kg']*c17; hxi=.026*hxp
    put(tube_mass=tube,shell_mass=shell,heads_mass=heads,sheets_mass=sheets,hx_mass=hxmass,bundle_mass=bundle,ihx_installed_area=area,ihx_required_area=required,ihx_duty_MW=x['q_ihx_MW']/n,ihx_hot_approach=hot,ihx_cold_approach=cold,ihx_lmtd=lmtd,ihx_capacity_ok=required<=area,ihx_capacity_margin_m2=area-required,ihx_capacity_defined=1.0,hx_purchase=hxp,hx_installation=hxi,exchangers_cost=hxp+hxi)
    # Main and branch annular steel and independent internal inventory volumes.
    layout=x['layout_multiplier']; fitting=1+14440/66560
    straight=0.; hevol=0.
    for main_od in (1.3,1.1):
        main_id=main_od-2*.065; branch_id=main_id/3; branch_od=branch_id+2*.03
        branch_length=(4000/9-100)/18
        straight += rho_steel*pi/4*((main_od**2-main_id**2)*50+9*(branch_od**2-branch_id**2)*branch_length)*layout
        hevol += pi/4*(main_id**2*50+9*branch_id**2*branch_length)*layout
    ppm=straight*fitting*n; ppp=ppm*x['stainless_fabrication_usd2017_per_kg']*c17; ppi=.5*ppp
    put(primary_pipe_mass=ppm,primary_pipe_volume=hevol*n,primary_pipe_purchase=ppp,primary_pipe_installation=ppi,primary_piping_cost=ppp+ppi)
    # Salt: k selected cold-side machines each circuit; fixed scenario efficiencies.
    rc=2080-.733*270; rh=2080-.733*465; muc=.00622-1.02e-5*270; muh=.00622-1.02e-5*465
    saltflow=x['q_ihx_MW']*1e6/(1560*195); loopflow=saltflow/n
    shaftsalt=saltflow*g*x['secondary_head']/x['eta_p']/1e6; elecsalt=shaftsalt/x['eta_motor']
    qgpm=loopflow/(k*rc)*15850.323141489; hft=x['secondary_head']/0.3048
    s=qgpm*math.sqrt(hft); logs=math.log(s)
    pump06=3*math.exp(9.7171-.6019*logs+.0519*logs**2)
    ph=shaftsalt*1e6/(k*n*hp); eh=elecsalt*1e6/(k*n*hp); le=math.log(eh)
    motor06=1.3*math.exp(5.8259+.13141*le+.053255*le**2+.028628*le**3-.0035549*le**4)
    design_shaft=x['salt_design_flow_kg_s']*g*x['salt_design_head_m']/x['salt_design_eta_p']/1e6
    design_electric=design_shaft/x['salt_design_eta_motor']
    dgpm=x['salt_design_flow_kg_s']/rc*15850.323141489; dhft=x['salt_design_head_m']/0.3048
    ds=dgpm*math.sqrt(dhft); dl=math.log(ds); dph=design_shaft*1e6/hp; deh=design_electric*1e6/hp; dle=math.log(deh)
    design_pump06=3*math.exp(9.7171-.6019*dl+.0519*dl**2)
    design_motor06=1.3*math.exp(5.8259+.13141*dle+.053255*dle**2+.028628*dle**3-.0035549*dle**4)
    put(helium_design_shaft_MW=x['helium_design_shaft_MW'],helium_design_suction_Pa=x['helium_design_suction_Pa'],salt_design_flow_kg_s=x['salt_design_flow_kg_s'],salt_design_head_m=x['salt_design_head_m'],salt_design_shaft_MW=design_shaft,salt_design_electric_MW=design_electric,design_pump_flow_gpm=dgpm,design_pump_head_ft=dhft,design_pump_size_factor=ds,design_pump_shaft_hp=dph,design_motor_electric_hp=deh,design_pump_size_ok=400<=ds<=100000,design_pump_type_ok=50<=dgpm<=3500 and 50<=dhft<=200 and dph<=200,design_motor_base_ok=1<=deh<=700,design_motor_factor_ok=1<=deh<=250)
    saltpackage=(design_pump06+design_motor06)*c06; sv=saltpackage*k*n; si=install_pump*sv
    put(salt_flow=loopflow,salt_pump_flow=loopflow/k,salt_pump_shaft_MW=shaftsalt/(k*n),ihx_count=n,salt_shaft_MW=shaftsalt,salt_electric_MW=elecsalt,conversion_heat_MW=x['q_ihx_MW']+shaftsalt,salt_return_C=270-shaftsalt*1e6/(saltflow*1560),salt_pump_count=k*n,pump_flow_gpm=qgpm,pump_head_ft=hft,pump_size_factor=s,pump_shaft_hp=ph,motor_electric_hp=eh,secondary_vendor=sv,secondary_installation=si,secondary_spare=saltpackage,secondary_pumps_cost=sv+si,pump_size_ok=400<=s<=100000,pump_type_ok=50<=qgpm<=3500 and 50<=hft<=200 and ph<=200,motor_base_ok=1<=eh<=700,motor_factor_ok=1<=eh<=250)
    put(salt_pump_electric_MW=elecsalt/(k*n),total_salt_flow_kg_s=saltflow,installed_total_UA_MW_K=n*area*uf/1e6)
    # Smooth-pipe head diagnostic. No claim of solved exchanger/valve losses.
    saltid=.40; saltod=.44; cross=pi*saltid**2/4
    spm=rho_steel*pi/4*(saltod**2-saltid**2)*100*layout*n*fitting
    spp=spm*x['stainless_fabrication_usd2017_per_kg']*c17; spi=.5*spp
    velocities=[]; res=[]; losses=[]
    for rho,mu in ((rh,muh),(rc,muc)):
        v=loopflow/(rho*cross); re=rho*v*saltid/mu
        f=64/re if re<2300 else (-1.8*math.log10(6.9/re))**-2
        velocities.append(v); res.append(re); losses.append(f*50*layout/saltid*v*v/(2*g))
    loss=sum(losses)
    saltvoid=pi*ri**2*length-tube_count*pi*od**2/4*length-x['accessory_mass']/rho_steel
    if saltvoid<=0: raise ValueError('accessory displacement exceeds salt shell void')
    saltpipe=cross*100*layout*n; saltvol=saltpipe+saltvoid*n
    saltfill=saltvol*rc
    saltmass=x['salt_purchased_mass_kg']
    raw,year,cpi=(1.23,2011,224.9) if x['saltprice_source_choice']==0 else (2.53,2021,271.0)
    saltprice=raw*321.9/cpi*scale; saltcost=saltmass*saltprice
    put(secondary_pipe_mass=spm,secondary_pipe_purchase=spp,secondary_pipe_installation=spi,secondary_piping_cost=spp+spi,salt_velocity_hot=velocities[0],salt_velocity_cold=velocities[1],salt_Re_hot=res[0],salt_Re_cold=res[1],salt_straight_loss=loss,salt_head_remaining=x['secondary_head']-loss,salt_head_ok=loss<=x['secondary_head'],salt_flow_regime_ok=all(not 2300<=r<4000 for r in res),salt_pipe_volume=saltpipe,salt_hx_volume=saltvoid*n,salt_inventory_volume=saltvol,salt_inventory_mass=saltmass,salt_expansion_ratio=rc/rh,salt_price_raw=raw,salt_price_year=year,salt_unit_price=saltprice,salt_inventory_cost=saltcost,salt_bulk_scale_ok=saltmass>=1e7)
    hephysical=(hevol+61.5)*n
    hemean=(x['helium_hot_K']+x['helium_suction_K'])/2
    hefill=hephysical*x['helium_discharge_Pa']/(gas_R*hemean)
    hemass=x['helium_purchased_mass_kg']
    put(represented_fill_defined=1.0,helium_required_fill_mass_kg=hefill,salt_required_fill_mass_kg=saltfill,helium_inventory_target_mass_kg=hefill*(1+x['inventory_reserve']),salt_inventory_target_mass_kg=saltfill*(1+x['inventory_reserve']),helium_represented_fill_margin_kg=hemass-hefill,salt_represented_fill_margin_kg=saltmass-saltfill,represented_fill_ok=hemass>=hefill and saltmass>=saltfill)
    standard=hemass*gas_R*288.15/101325
    hecost=standard*14*321.9/313.7*scale
    ratio=hephysical/(879*n/9)
    put(helium_hx_volume=61.5*n,helium_inventory_volume=hephysical,helium_inventory_mass=hemass,helium_standard_volume=standard,helium_inventory_cost=hecost,helium_price_raw=14,helium_price_year=2024,source_volume_ratio=ratio,inventory_source_volume_ok=ratio<=1)
    inventory=hecost+saltcost; spares=package+saltpackage
    purchased=pv+pdesign+hxp+ppp+sv+spp+inventory+spares
    installation=pinstall+hxi+ppi+si+spi
    put(inventory_cost=inventory,spares_cost=spares,purchased_total=purchased,installation_total=installation,installed_total=purchased+installation,delivered_total=pv+package+hxp+ppp+spp)
    # Discrete replacement payments strictly before horizon; constant-base prices.
    mp=pv+sv; mi=pinstall+si; mr=mi*x['removal_multiplier']
    put(salt_machine_event_purchase=sv,salt_machine_event_installation=si,salt_machine_event_removal=si*x['removal_multiplier'])
    bp=bundle*n*x['stainless_fabrication_usd2017_per_kg']*c17; bi=.026*bp; br=.024*bp*x['removal_multiplier']
    def replacement(life):
        count=max(0, math.ceil(x['years']/life)-1)
        return count, sum((1+x['discount'])**(-k*life) for k in range(1,count+1))
    nm,dm=replacement(x['machine_life']); nb,db=replacement(x['bundle_life'])
    rate=x['discount']; years=x['years']
    crf=1/years if rate==0 else rate/(-math.expm1(-years*math.log1p(rate)))
    annual=((mp+mi+mr)*dm+(bp+bi+br)*db)*crf
    put(machine_event_purchase=mp,machine_event_installation=mi,machine_event_removal=mr,bundle_event_purchase=bp,bundle_event_installation=bi,bundle_event_removal=br,machine_events=nm,bundle_events=nb,replacement_annual=annual,helium_makeup_annual=hecost*x['makeup_fraction'],salt_makeup_annual=saltcost*x['makeup_fraction'],consumables_annual=inventory*x['makeup_fraction'],cycle_temperature_gap=x['sourcefitargument_C']-465,cycle_interface_ok=x['sourcefitargument_C']<=465)
    if any(not math.isfinite(v) for v in out.values()): raise ValueError('nonfinite equipment result')
    return out

OUTPUT_NAMES = ('primary_circulators_cost', 'primary_piping_cost', 'exchangers_cost', 'secondary_pumps_cost', 'secondary_piping_cost', 'inventory_cost', 'spares_cost', 'purchased_total', 'installation_total', 'installed_total', 'delivered_total', 'primary_vendor', 'primary_installation', 'primary_design', 'primary_spare', 'secondary_vendor', 'secondary_installation', 'secondary_spare', 'hx_purchase', 'hx_installation', 'primary_pipe_purchase', 'primary_pipe_installation', 'secondary_pipe_purchase', 'secondary_pipe_installation', 'helium_inventory_cost', 'salt_inventory_cost', 'machine_event_purchase', 'machine_event_installation', 'machine_event_removal', 'bundle_event_purchase', 'bundle_event_installation', 'bundle_event_removal', 'replacement_annual', 'consumables_annual', 'helium_makeup_annual', 'salt_makeup_annual', 'salt_electric_MW', 'salt_shaft_MW', 'conversion_heat_MW', 'circulator_shaft_MW', 'circulator_electric_MW', 'ihx_duty_MW', 'tube_mass', 'shell_mass', 'heads_mass', 'sheets_mass', 'hx_mass', 'bundle_mass', 'primary_pipe_mass', 'secondary_pipe_mass', 'helium_inventory_mass', 'salt_inventory_mass', 'primary_pipe_volume', 'helium_hx_volume', 'helium_inventory_volume', 'helium_standard_volume', 'salt_pipe_volume', 'salt_hx_volume', 'salt_inventory_volume', 'ihx_installed_area', 'ihx_required_area', 'circulator_count', 'salt_pump_count', 'source_volume_ratio', 'salt_expansion_ratio', 'salt_Re_hot', 'salt_Re_cold', 'pump_size_factor', 'pump_shaft_hp', 'motor_electric_hp', 'machine_events', 'bundle_events', 'salt_price_raw', 'salt_price_year', 'salt_unit_price', 'helium_price_raw', 'helium_price_year', 'circulator_flow', 'circulator_volume', 'circulator_suction_Pa', 'ihx_hot_approach', 'ihx_cold_approach', 'ihx_lmtd', 'salt_flow', 'salt_velocity_hot', 'salt_velocity_cold', 'salt_straight_loss', 'salt_head_remaining', 'salt_return_C', 'cycle_temperature_gap', 'pump_flow_gpm', 'pump_head_ft', 'ihx_capacity_ok', 'pump_size_ok', 'pump_type_ok', 'motor_base_ok', 'motor_factor_ok', 'salt_head_ok', 'salt_flow_regime_ok', 'cycle_interface_ok', 'salt_bulk_scale_ok', 'inventory_source_volume_ok', 'pressure_qualified', 'helium_price_transfer_validated', 'salt_pump_transfer_validated', 'inventory_complete', 'salt_pump_flow', 'salt_pump_shaft_MW', 'ihx_count')
OUTPUT_NAMES += ('hx_shell_bore', 'hx_shell_wall', 'hx_shell_length', 'hx_tube_length')
BOOL_OUTPUTS = ('ihx_capacity_ok', 'pump_size_ok', 'pump_type_ok', 'motor_base_ok', 'motor_factor_ok', 'salt_head_ok', 'salt_flow_regime_ok', 'cycle_interface_ok', 'salt_bulk_scale_ok', 'inventory_source_volume_ok', 'pressure_qualified', 'helium_price_transfer_validated', 'salt_pump_transfer_validated', 'inventory_complete')

OUTPUT_NAMES += ('helium_design_shaft_MW', 'helium_design_suction_Pa', 'salt_design_flow_kg_s', 'salt_design_head_m', 'salt_design_shaft_MW', 'salt_design_electric_MW', 'design_pump_flow_gpm', 'design_pump_head_ft', 'design_pump_size_factor', 'design_pump_shaft_hp', 'design_motor_electric_hp', 'helium_required_fill_mass_kg', 'salt_required_fill_mass_kg', 'helium_inventory_target_mass_kg', 'salt_inventory_target_mass_kg', 'helium_represented_fill_margin_kg', 'salt_represented_fill_margin_kg', 'design_pump_size_ok', 'design_pump_type_ok', 'design_motor_base_ok', 'design_motor_factor_ok', 'machine_off_design_performance_qualified', 'represented_fill_ok')
BOOL_OUTPUTS += ('design_pump_size_ok', 'design_pump_type_ok', 'design_motor_base_ok', 'design_motor_factor_ok', 'machine_off_design_performance_qualified', 'represented_fill_ok')

OUTPUT_NAMES += ('represented_fill_defined', 'ihx_capacity_margin_m2', 'ihx_capacity_defined')

OUTPUT_NAMES += ('salt_machine_event_purchase', 'salt_machine_event_installation', 'salt_machine_event_removal', 'salt_pump_electric_MW', 'total_salt_flow_kg_s', 'installed_total_UA_MW_K')

# Native wrapper reads the emitted output schema order at invocation.
def run_cooling_equipment_with_selected_salt_pump_count(inputs: Cooling_Equipment_With_Selected_Salt_Pump_CountInput) -> tuple[float, ...]:
    """Complete the native typed calculation using its generated tuple ABI."""
    result = calculate({
        'salt_pumps_per_circuit': inputs.salt_pumps_per_circuit_in,
        'helium_design_shaft_MW': inputs.helium_design_shaft_MW_in,
        'helium_design_suction_Pa': inputs.helium_design_suction_Pa_in,
        'salt_design_flow_kg_s': inputs.salt_design_flow_kg_s_in,
        'salt_design_head_m': inputs.salt_design_head_m_in,
        'salt_design_eta_p': inputs.salt_design_eta_p_in,
        'salt_design_eta_motor': inputs.salt_design_eta_motor_in,
        'helium_purchased_mass_kg': inputs.helium_purchased_mass_kg_in,
        'salt_purchased_mass_kg': inputs.salt_purchased_mass_kg_in,

        'enabled': inputs.enabled_in,
        'n_mod': inputs.n_mod_in,
        'n_loops': inputs.n_loops_in,
        'mdot_loop': inputs.mdot_loop_in,
        'dp_loop': inputs.dp_loop_in,
        'helium_suction_K': inputs.helium_suction_K_in,
        'helium_discharge_Pa': inputs.helium_discharge_Pa_in,
        'helium_hot_K': inputs.helium_hot_K_in,
        'helium_cp': inputs.helium_cp_in,
        'helium_gamma': inputs.helium_gamma_in,
        'primary_shaft_MW': inputs.primary_shaft_MW_in,
        'primary_electric_MW': inputs.primary_electric_MW_in,
        'q_ihx_MW': inputs.q_ihx_MW_in,
        'layout_multiplier': inputs.layout_multiplier_in,
        'tube_wall': inputs.tube_wall_in,
        'shell_wall': inputs.shell_wall_in,
        'accessory_mass': inputs.accessory_mass_in,
        'secondary_head': inputs.secondary_head_in,
        'eta_p': inputs.eta_p_in,
        'eta_motor': inputs.eta_motor_in,
        'machine_life': inputs.machine_life_in,
        'bundle_life': inputs.bundle_life_in,
        'years': inputs.years_in,
        'discount': inputs.discount_in,
        'makeup_fraction': inputs.makeup_fraction_in,
        'inventory_reserve': inputs.inventory_reserve_in,
        'removal_multiplier': inputs.removal_multiplier_in,
        'saltprice_source_choice': inputs.saltprice_source_choice_in,
        'costscale': inputs.costscale_in,
        'stainless_fabrication_usd2017_per_kg': inputs.stainless_fabrication_usd2017_per_kg_in,
        'sourcefitargument_C': inputs.sourcefitargument_C_in,
    })
    from whole_plant_conversion_tea.schemas.cooling_equipment_with_selected_salt_pump_count_output import Cooling_Equipment_With_Selected_Salt_Pump_CountOutput
    return tuple(result[name] for name in Cooling_Equipment_With_Selected_Salt_Pump_CountOutput.model_fields)
