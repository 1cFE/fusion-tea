"""Author checks of the independent numerical reference, not independent review."""
from decimal import Decimal
import json
import math
import re
import reference as ref


def half_last_digit(text):
    return Decimal(5) * Decimal(10) ** (Decimal(text).as_tuple().exponent-1)


tables, receipts = ref.load()
checks = {}
for name, source in ref.SOURCES.items():
    raw = (ref.ROOT/'knowledge/sources'/source/'raw.html').read_text()
    # Separate regex extraction must agree exactly with HTMLParser extraction.
    raw_rows = []
    for row in re.findall(r'<tr>(.*?)</tr>',raw,re.S):
        cells = re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if len(cells)>=14 and cells[-1] in ('liquid','vapor'):
            raw_rows.append(cells)
    assert len(raw_rows)==len(tables[name])
    worst_ratio = 0.
    for cells, row in zip(raw_rows,tables[name]):
        assert [float(v) for v in cells[:7]] == [row[k] for k in ('t','p','rho','v','u','h','s')]
        p,v,u,h = (Decimal(cells[i]) for i in (1,3,4,5))
        dp,dv,du,dh = (half_last_digit(cells[i]) for i in (1,3,4,5))
        bound = du+dh+1000*(abs(p)*dv+abs(v)*dp+dp*dv)
        residual = abs(h-u-1000*p*v)
        assert residual <= bound, (name,row,residual,bound)
        worst_ratio = max(worst_ratio,float(residual/bound))
    checks[name] = {'transcription_rows_checked':len(raw_rows),'h_u_pv_display_precision_max_fraction':worst_ratio}

results = json.loads((ref.HERE/'reference-results.json').read_text())
for label,r in results.items():
    c = r['cycle']
    assert all(abs(v)<1e-8 for k,v in c.items() if 'residual' in k)
    assert abs(r['cooling']['water_energy_residual_MW'])<1e-8
    assert c['s_hp_kJ_kgK'] > c['s_main_kJ_kgK']
    assert c['s_lp_kJ_kgK'] > c['s_reheat_kJ_kgK']
    assert math.isclose(c['q_main_MW']+c['q_reheat_MW'],3306.889098848892,rel_tol=1e-12)
    assert math.isclose(c['salt_main_flow_kg_s']+c['salt_reheat_flow_kg_s'],10852.114436183412,rel_tol=1e-12)

pump_checks = {}
for label,r in results.items():
    c = r['cycle']
    heater = max(ref.phase(tables['extraction'],'liquid'),key=lambda r:r['t'])
    table_feed = ref.interp(ref.phase(tables['main'],'liquid'),'s',heater['s'])
    ideal_vdp = heater['v']*5400
    ideal_table = table_feed['h']-heater['h']
    record = {'feed_ideal_vdp_kJ_kg':ideal_vdp,'feed_ideal_table_hs_kJ_kg':ideal_table,
              'feed_relative_difference':ideal_vdp/ideal_table-1}
    liquid = ref.interp(ref.phase(tables['saturation'],'liquid'),'t',c['t_condensate_C'])
    try:
        ideal_cp = ref.interp(ref.phase(tables['extraction'],'liquid'),'s',liquid['s'])
        table_work = ideal_cp['h']-liquid['h']
        vdp_work = liquid['v']*(.8-liquid['p'])*1000
        record.update(condensate_ideal_vdp_kJ_kg=vdp_work,condensate_ideal_table_hs_kJ_kg=table_work,
                      condensate_relative_difference=vdp_work/table_work-1)
    except ValueError as error:
        record['condensate_table_hs_unavailable'] = str(error)
    pump_checks[label] = record

# Exact interval reversibility at all tabulated phases: forward T->h then h->T.
roundtrip = {}
for name, table in tables.items():
    for ph in ('liquid','vapor'):
        rows = ref.phase(table,ph)
        maximum = 0.
        for a,b in zip(rows,rows[1:]):
            t = (a['t']+b['t'])/2
            h = ref.interp(rows,'t',t)['h']
            back = ref.interp(rows,'h',h)['t']
            maximum = max(maximum,abs(back-t))
        roundtrip[name+'_'+ph] = maximum
        assert maximum<1e-8

checks.update(pump_approximation=pump_checks,interpolation_inverse_max_delta_C=roundtrip,
              balance_cases_checked=list(results),balance_absolute_tolerance=1e-8)

inputs = dict(enabled=1,heat_available_MW=3306.889098848892,salt_flow_per_circuit=10852.114436183412/14,
              source_heat_MW=3125.9322770825056,selected_recovered_MW=180.95682176638664,
              salt_circuit_count=14,salt_hot_C=465.,salt_return_C=269.664729914530,salt_cp_kJ_kgK=1.560,
              main_pressure_MPa=6.2,extraction_pressure_MPa=.8,steam_temperature_C=445.,reheat_temperature_C=445.,
              condenser_temperature_C=42.,eta_hp=.9,eta_lp=.9,eta_condensate_pump=.8,eta_feedwater_pump=.8,
              eta_pump_motor=.95,eta_mechanical=.99,eta_generator=.98)
baseline = ref.matched_interface(inputs,tables)
assert baseline==results['baseline']['cycle']
assert set(baseline)==set(ref.MATCHED_REALS+ref.MATCHED_BOOLS)
assert ref.matched_interface({'enabled':0})==ref.inactive(ref.MATCHED_REALS,ref.MATCHED_BOOLS)
assert ref.cooling_interface({'enabled':0})==ref.inactive(ref.COOLING_REALS,ref.COOLING_BOOLS)
count18 = ref.matched_interface({**inputs,'salt_circuit_count':18,'salt_flow_per_circuit':10852.114436183412/18},tables)
assert count18==baseline
refusals = []
for label,updates in [('wrong_main_pressure',{'main_pressure_MPa':6.3}),
                      ('wrong_extraction_pressure',{'extraction_pressure_MPa':.81}),
                      ('invalid_mode',{'enabled':.5}),('nonfinite',{'eta_hp':float('nan')}),
                      ('zero_eta',{'eta_hp':0}),('overunity_eta',{'eta_lp':1.01}),
                      ('zero_heat',{'heat_available_MW':0}),('doubled_count',{'salt_circuit_count':28}),
                      ('inconsistent_selected_recovery',{'selected_recovered_MW':0}),
                      ('cold_condenser',{'condenser_temperature_C':19.999999}),
                      ('hot_condenser',{'condenser_temperature_C':60.000001}),
                      ('hot_main',{'steam_temperature_C':455.000001}),
                      ('hot_reheat',{'reheat_temperature_C':455.000001}),
                      ('main_saturation',{'steam_temperature_C':receipts['main']['saturation_endpoints'][0]['t']}),
                      ('reheat_saturation',{'reheat_temperature_C':receipts['extraction']['saturation_endpoints'][0]['t']})]:
    try:
        ref.matched_interface({**inputs,**updates},tables)
    except (ValueError,AssertionError) as error:
        refusals.append({'case':label,'reason':str(error)})
    else:
        raise AssertionError(f'expected refusal: {label}')
zero_gap = ref.matched_interface({**inputs,'salt_hot_C':445.,'salt_return_C':inputs['salt_return_C']-20},tables)
assert zero_gap['main_min_gap_K']==0 and not zero_gap['main_admission_ok'] and not zero_gap['main_UA_available']
assert zero_gap['reheat_min_gap_K']==0 and not zero_gap['reheat_admission_ok'] and not zero_gap['reheat_UA_available']
cw = dict(enabled=1,cycle_active=1,q_rejection_before_cooling_MW=baseline['q_rejection_before_cooling_MW'],
          condenser_temperature_C=42.,water_inlet_C=25.,water_outlet_C=35.,head_m=20.,eta_pump=.8,eta_motor=.95)
assert ref.cooling_interface(cw,tables)==results['baseline']['cooling']
for label,updates in [('inactive_cycle',{'cycle_active':0}),('negative_denominator',{'head_m':100000}),
                      ('water_order',{'water_inlet_C':35}),('water_domain',{'water_inlet_C':19}),
                      ('negative_head',{'head_m':-1}),('invalid_mode',{'enabled':2})]:
    try:
        ref.cooling_interface({**cw,**updates},tables)
    except ValueError as error:
        refusals.append({'case':'cooling_'+label,'reason':str(error)})
    else:
        raise AssertionError(f'expected refusal: {label}')
assert not ref.cooling_interface({**cw,'condenser_temperature_C':35},tables)['cooling_approach_ok']
checks.update(contract_numeric_count=len(ref.MATCHED_REALS),contract_boolean_count=len(ref.MATCHED_BOOLS),
              conditional_cooling_numeric_count=len(ref.COOLING_REALS),conditional_cooling_boolean_count=len(ref.COOLING_BOOLS),
              matched_refusals=refusals,disabled_without_property_access=True,
              zero_gap_retained_with_unavailable_UA=True,nondefault18_circuit_identity=True)
(ref.HERE/'reference-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
