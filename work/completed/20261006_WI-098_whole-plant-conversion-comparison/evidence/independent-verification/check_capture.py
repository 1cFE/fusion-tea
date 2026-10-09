"""Independent selected magnet arithmetic from original source equations.
No native body or numerical output is used to derive an expected value.
Scope is supplied equipment, not the full recalculated plasma operating point.
"""
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
CAP=HERE.parent/'magnet-capture'
P='stellarator_09__stellaris__'
a=json.loads((CAP/'offer-inputs.json').read_text())
rows=json.loads((CAP/'native-cases.json').read_text())
n=rows[1]['outputs']; expected={}
def get(k):return a[P+k]
def emit(calc,**kw):
 for k,v in kw.items():expected[P+calc+'__'+k]=v
wp=lambda k:get('magnet__winding_pack__'+k)
coil=lambda k:get('magnet__coil__'+k)
cr=lambda k:get('cryoplant__'+k)
case=lambda k:get('magnet__casing__'+k)
# The accepted fixed radial geometry, independently rebuilt from selected inputs.
R=get("plasma__R")
bore=get("plasma__a")+sum(get(k) for k in ["blanket__first_wall__vacuum_t","blanket__first_wall__firstwall_t","blanket__blanket_t","blanket__reflector_t","shield__ht_shield_t","structure__structure_t","vessel__gap1_t","vessel__vessel_t"])+coil("coil_t")/2
assert math.isclose(bore,3.15)
current=coil('reference_turns')*coil('turn_current')
axis=get('magnet__field_calc__mu0')*coil('k_link')*coil('n_coils')*current/(get('magnet__field_calc__two_pi')*R)
peak=axis*coil('peak_ratio')*(R/(R-bore))/(coil('R_ref')/(coil('R_ref')-coil('a_coil_ref')))
length=coil('c_coil_ref')*bore/coil('a_coil_ref')
volume=wp('f_wp_vol')*coil('n_coils')*wp('wp_side')**2*length
emit('magnet__winding_state',I_coil=current,j_wp_effective=current/(wp('wp_side')**2*1e6))
emit('magnet__field_calc',B_axis=axis);emit('magnet__peak_field_calc',B_peak=peak)
emit('magnet__coil_length',c_coil=length)
emit('magnet__wp_volume',vol_winding_pack=volume,vol_cold_total=volume+get('magnet__vol_cold_cryo'))
stress=wp('k_sigma')*current*peak/wp('wp_side')
emit('magnet__wp_stress',sigma_wp=stress);emit('magnet__cond_strain',eps_cond=wp('f_cond')*stress/wp('E_wp'))
emit('magnet__stored_energy',W_mag=case('W_mag_ref')*(current/coil('I_ref'))**2*(bore/coil('a_coil_ref'))**2*coil('R_ref')/R)
material={};rhohe=wp('helium_pressure')/(wp('helium_gas_constant')*cr('T_cold_cryo'))
for m in ['copper','solder','steel','helium']:
 material['mass_'+m]=volume*wp('f_'+m)*(rhohe if m=='helium' else wp('rho_'+m))
 material['cost_'+m]=material['mass_'+m]*wp('price_'+m)
tapevol=volume*(1-math.fsum(wp('f_'+m) for m in ['copper','solder','steel','helium']))
material.update(helium_density=rhohe,tape_volume=tapevol,material_cost=math.fsum(material['cost_'+m] for m in ['copper','solder','steel','helium']))
emit('magnet__material_inventory',**material)
tapelen=tapevol/(wp('tape_width')*wp('tape_thickness'));conductor=coil('n_coils')*coil('reference_turns')*coil('f_set')*length
fabrication=conductor*wp('winding_rate_1990')*wp('cost_escalation')*wp('nonplanar_factor')
windcost=tapelen*wp('tape_price_per_m')+material['material_cost']+fabrication
emit('magnet__winding_procurement',tape_length=tapelen,tape_cost=tapelen*wp('tape_price_per_m'),conductor_length=conductor,winding_fabrication_cost=fabrication,cost=windcost)
root=math.sqrt(wp('fit_aspect_ratio'));fit={}
for d,s,cavity,ext in [('x',wp('wp_side')*root,coil('coil_t')-2*case('wall_thickness'),coil('coil_t')),('y',wp('wp_side')/root,case('interior_y'),case('interior_y')+2*case('wall_thickness'))]:
 internal=s*wp('internal_build_'+d);insulated=s+internal+2*wp('ground_insulation');required=insulated+2*case('assembly_clearance')
 for name,value in [('nominal',s),('internal',internal),('pack',s+internal),('insulated',insulated),('required',required),('cavity',cavity),('exterior',ext),('margin',cavity-required)]:fit[name+'_'+d]=value
fit['minimum_margin']=min(fit['margin_x'],fit['margin_y']);emit('magnet__wp_fit',**fit)
fx,fy=wp('internal_build_x'),wp('internal_build_y');t=wp('ground_insulation')
internal=volume*(fx+fy+fx*fy);sheet=internal/wp('insulation_sheet_thickness');stock=sheet*wp('insulation_sheet_price')
ground=coil('n_coils')*length*(2*t*wp('f_wp_perimeter')*(fit['nominal_x']*(1+fx)+fit['nominal_y']*(1+fy))+4*t*t)
emit('magnet__insulation_inventory',internal_volume=internal,ground_volume=ground,sheet_area=sheet,stock_cost=stock)
tapeI=wp('reference_tape_current')*wp('tape_width')/.004*(peak/20)**(-.6)*wp('material_factor')*wp('orientation_factor')
ns=tapelen/conductor;nr=ns*coil('f_set')/wp('f_wp_vol');factor=math.prod(wp(k) for k in ['cabling_factor','degradation_factor','sharing_factor'])
cs,cf=ns*tapeI*factor,nr*tapeI*factor;allowed=cf*wp('allowable_fraction')
emit('magnet__conductor_current',parallel_tapes_set=ns,parallel_tapes_reference=nr,tape_critical_current=tapeI,critical_current_set=cs,critical_current_reference=cf,operating_fraction_set=coil('turn_current')/cs,operating_fraction_reference=coil('turn_current')/cf,allowable_current=allowed,margin_current=allowed-coil('turn_current'),margin_fraction=wp('allowable_fraction')-coil('turn_current')/cf,field_extrapolated=float(peak>24))
structure=(get('magnet__legacy_casing_fraction')*coil('n_coils')*case('m_casing')+get('magnet__m_support'))*case('steel_price')*case('f_steel_fab')
emit('magnet__magnet_structure_cost',cost=structure,effective_all_in_rate=case('steel_price')*case('f_steel_fab'))
emit('magnet__magnet_capital_rollup',capital_cost=math.fsum([windcost,structure,stock]))
tc,ts,ta=cr('T_cold_cryo'),cr('T_shield'),cr('T_amb_cryo')
area=coil('n_coils')*length*4*(wp('wp_side')+2*cr('t_case'));areaS=area*cr('shield_area_ratio')
lead=cr('f_lead')*cr('n_leads')*coil('turn_current')
lc=lead*math.sqrt(cr('L0')*(ts*ts-tc*tc));ls=lead*math.sqrt(cr('L0')*(ta*ta-ts*ts))
rc=area*cr('eps_eff')*cr('sigma_SB')*(ts**4-tc**4);rs=areaS*cr('q_MLI')-rc
sc=coil('n_coils')*cr('g_per_coil')*cr('k_c')*(ts-tc);ss=coil('n_coils')*cr('g_per_coil')*cr('k_s')*(ta-ts)-sc
cold=math.fsum([lc,rc,sc]);shield=math.fsum([ls,rs,ss]);drive=(lc+ls)*1e-6+cr('joint_drive_fraction')*cr('p_fixed_cryo')
emit('cryoplant__inventory',area_cold=area,area_shield=areaS,q_lead_cold=lc,q_lead_shield=ls,q_rad_cold=rc,q_rad_shield=rs,q_support_cold=sc,q_support_shield=ss,q_inventory_cold=cold,q_inventory_shield=shield,p_drive=drive)
structureheat=cr('q_nuc_structure')*get('magnet__m_support')/cr('rho_structure')*1e-6
p_cold=(wp('q_nuc_cryo')*(volume+get('magnet__vol_cold_cryo'))*1e-6+cr('p_fixed_cryo')+structureheat)*cr('f_uplift_cryo')+cold*1e-6
pc=p_cold*(ta-tc)/(cr('f_carnot_cryo')*tc)+cr('p_cryo');ps=shield*1e-6*(ta-ts)/(cr('f_carnot_shield')*ts)
emit('cryoplant__cold_load',p_cold=p_cold,q_structure_nuclear=structureheat)
emit('cryoplant__cold_load_W_demand_conversion',demand=p_cold*1e6)
emit('cryoplant__cryo_elec',p_elec=pc);emit('cryoplant__shield_elec',p_elec=ps);emit('cryoplant__refrigeration_sum',total=pc+ps)
for name,demand,rating in [('cold_stage',p_cold*1e6,cr('rated_cold_W')),('intercept_stage',shield,cr('rated_intercept_W')),('direct_electric',cr('p_cryo'),cr('rated_direct_electric_MW'))]:
 emit('cryoplant__'+name+'_capability',margin=rating-demand,applicable=1.,supported=1.,evaluation_defined=1.,capacity_ok=float(rating>=demand))
differences=[dict(channel=k,expected=v,actual=n.get(k)) for k,v in expected.items() if k not in n or not math.isclose(v,n[k],rel_tol=1e-9,abs_tol=1e-12)]
report=dict(status='pass' if not differences else 'fail',comparisons=len(expected),differences=differences,expected=expected,inputs_sha256=hashlib.sha256((CAP/'offer-inputs.json').read_bytes()).hexdigest(),capture_sha256=hashlib.sha256((CAP/'native-cases.json').read_bytes()).hexdigest(),qualification='Arithmetic and local component checks under supplied35.5W/m3 nuclear-heating assumption. Conservative transport bound for enlarged geometry not established.',source_qualified=0,transport_qualified=0)
(HERE/'capture-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],report['comparisons'],differences)
assert not differences
