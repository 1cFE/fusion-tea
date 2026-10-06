"""Independent WI-096 component checks; no native-package validity claim.

Run with .codex-test/run python <path> --out <fresh-json-path>.
Quadrature integrates in water temperature; finance uses Decimal dated sums.
Only retained property/body imports are adapted, without changing their bytes.
"""
from __future__ import annotations
import argparse
import bisect
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[4]
BODIES = ROOT / 'exploration/component_alternatives/bodies/component_alternatives_thermal'
PROPERTIES = ROOT / 'exploration/stellarator_e2e/generated/handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py'
SOURCE_RECEIPT = ROOT / 'work/orchestration/goals/design-study-component-alternatives/evidence/fourth-submission-control-probe.json'
GAS_RECEIPT = ROOT / 'work/orchestration/goals/design-study-component-alternatives/evidence/fourth-submission-thermal-revised-offer-probe.json'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def close(a, b, absolute=1e-8, relative=1e-11):
    assert math.isclose(a, b, abs_tol=absolute, rel_tol=relative), (a, b, a-b)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists(): raise FileExistsError(args.out)
    initial_body_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in BODIES.glob('*_impl.py')}
    prop = load(PROPERTIES, 'matched_steam_cycle_impl')
    # The cooler imports only these retained property functions. This provides
    # that dependency without pretending to have generated package/schema proof.
    sys.modules['component_alternatives_tea.handwritten.mfe_matched_steam_cycle.matched_steam_cycle_impl'] = prop
    water = load(PROPERTIES.with_name('cooling_water_rejection_impl.py'), 'cooling_water_rejection_impl')
    cooler = load(BODIES/'finite_water_cooler_impl.py', 'cooler')
    boundary = load(BODIES/'controlled_conversion_boundary_impl.py', 'boundary')
    recuperator = load(BODIES/'recuperator_installed_capability_impl.py', 'recuperator')
    ledger = load(BODIES/'conversion_subsystem_ledger_impl.py', 'ledger')
    # Reused DCF body needs its old package's annotation import. Supply the
    # schema name only; calculation receives the production SimpleNamespace.
    # The separate Decimal oracle below uses neither financial implementation.
    schema_name='costed_loop_brayton_tea.modules.mfe_lcoe_dcf.lcoe_dcf'
    schema=ModuleType(schema_name);schema.LCOE_DCFInput=SimpleNamespace
    sys.modules[schema_name]=schema
    retained=ROOT/'exploration/costed_loop_brayton/costed_loop_brayton_tea/handwritten'
    factors=load(retained/'mfe_account_costs/financial_factors.py','component_alternatives_tea.handwritten.mfe_account_costs.financial_factors')
    sys.modules['costed_loop_brayton_tea.handwritten.mfe_account_costs.financial_factors']=factors
    dcf=load(retained/'mfe_lcoe_dcf/lcoe_dcf_impl.py','component_alternatives_tea.handwritten.mfe_lcoe_dcf.lcoe_dcf_impl')
    tables = json.loads(prop.SOURCE_ASSET_JSON)['tables']['saturation']['rows']
    liquid = sorted((r for r in tables if r['phase']=='liquid'), key=lambda r:r['T'])
    temps, enthalpies = [r['T'] for r in liquid], [r['h'] for r in liquid]

    def lerp(xs, ys, value):
        assert xs[0] <= value <= xs[-1], ('outside retained table', value)
        j = min(max(bisect.bisect_right(xs, value)-1, 0), len(xs)-2)
        return ys[j] + (ys[j+1]-ys[j])*(value-xs[j])/(xs[j+1]-xs[j])
    h = lambda t: lerp(temps, enthalpies, t)
    temperature = lambda ent: lerp(enthalpies, temps, ent)

    def quadrature(x, y, subdivisions):
        # Integral in water temperature: dQ = mdot*cp(T)*dT/1000.
        # Gas enthalpy loss maps the water enthalpy increase into gas T.
        tin, tout, flow = y['water_inlet_after_C'], y['water_outlet_C'], y['water_flow']
        q = -x['gas_heat_into_fluid']
        cuts = [tin]+[t for t in temps if tin<t<tout]+[tout]
        values = []
        gaps = []
        for a,b in zip(cuts, cuts[1:]):
            cp = (h(b)-h(a))/(b-a)
            def integrand(t):
                gas = x['gas_outlet_K']-273.15 + (x['gas_inlet_K']-x['gas_outlet_K'])*flow*(h(t)-h(tin))/(1000*q)
                gap = gas-t
                assert gap>0
                return flow*cp/(1000*gap)
            step = (b-a)/subdivisions
            total = integrand(a)+integrand(b)
            total += math.fsum((4 if i%2 else 2)*integrand(a+i*step) for i in range(1,subdivisions))
            values.append(total*step/3)
            for t in (a,b):
                gas = x['gas_outlet_K']-273.15 + (x['gas_inlet_K']-x['gas_outlet_K'])*flow*(h(t)-h(tin))/(1000*q)
                gaps.append(gas-t)
        return math.fsum(values), min(gaps), len(cuts)-2

    gas = json.loads(GAS_RECEIPT.read_text())
    cooler_cases = []
    max_quad_error = 0.
    max_refinement_error = 0.
    for offer in gas['offers']:
        for index, case in enumerate(offer['coolers']):
            x = cooler.INPUTS | dict(gas_inlet_K=case['hot_C']+273.15,gas_outlet_K=case['cold_C']+273.15,gas_heat_into_fluid=-case['duty_MW'],ua=case['installed_UA'])
            y = cooler.calculate(x)
            record = {'offer': offer['offer'], 'index':index, 'inputs':x, 'outputs':y}
            expected = case['state']=='completed'
            assert bool(y['evaluation_defined']) is expected
            if expected:
                coarse,gap,knots = quadrature(x,y,32)
                fine,_,_ = quadrature(x,y,64)
                close(fine,x['ua'])
                close(gap,y['min_gap'])
                close(y['water_flow']*(h(y['water_outlet_C'])-h(x['water_inlet_C']))/1000,case['duty_MW']+y['pump_electric'])
                max_quad_error=max(max_quad_error,abs(fine-y['required_ua']))
                max_refinement_error=max(max_refinement_error,abs(fine-coarse))
                record.update(quadrature_ua=fine,quadrature_refinement_error=fine-coarse,property_knots_crossed=knots)
                # Independent capacity choices change margins only.
                altered=cooler.calculate(x|{'flow_rating':1.,'power_rating':.01,'duty_rating':1.})
                for key in ('water_outlet_C','water_flow','pump_electric','required_ua'):
                    assert altered[key]==y[key]
                assert all(altered[k]<0 for k in ('flow_margin','power_margin','duty_margin'))
            else:
                assert y['failure_code']==2 and not y['evaluation_defined']
                assert not y['bracket_low_ua']<=x['ua']<=y['bracket_high_ua']
                assert y['water_flow']==0 and y['water_outlet_C']==0
            cooler_cases.append(record)

    extra_coolers=[]
    # Single property segment, constant terminal gap: exact integral Q/dT.
    equal = cooler.INPUTS | dict(gas_inlet_K=308.55,gas_outlet_K=308.25,gas_heat_into_fluid=-100.,ua=10.,water_inlet_C=25.1,head=0.)
    eq=cooler.calculate(equal)
    close(eq['water_outlet_C'],25.4,absolute=2e-8)
    close(eq['required_ua'],100/10)
    extra_coolers.append({'name':'equal_gap_single_segment','inputs':equal,'outputs':eq})
    for inlet in (20.,59.0):
        # Manufactured operating case with independently integrated supplied UA.
        # Target water states are test data, never study-selected equipment.
        x=cooler.INPUTS|dict(water_inlet_C=inlet,head=0.,gas_inlet_K=373.15,gas_outlet_K=343.15,gas_heat_into_fluid=-100.)
        tout=inlet+.5
        trial=dict(water_inlet_after_C=inlet,water_outlet_C=tout,water_flow=100000/(h(tout)-h(inlet)))
        ua,_,_=quadrature(x,trial,64)
        x['ua']=ua;y=cooler.calculate(x)
        # Check the actual solved integral directly; temperature is secondary.
        solved_ua,_,_=quadrature(x,y,256)
        close(solved_ua,ua,absolute=1e-8)
        close(y['required_ua'],ua,absolute=1.1e-10)
        extra_coolers.append({'name':f'property_domain_inlet_{inlet}','inputs':x,'outputs':y,'oracle_ua':ua})
    cooler_refusals=[]
    for changes in ({'water_inlet_C':19.99},{'water_inlet_C':60.},{'water_inlet_C':59.99,'head':1000.},{'head':-1.},{'eta_p':0.},{'gas_heat_into_fluid':0.},{'gas_outlet_K':500.}):
        try:cooler.calculate(cooler.INPUTS|changes)
        except ValueError as error:cooler_refusals.append({'changes':changes,'reason':str(error)})
        else:raise AssertionError(('expected cooler refusal',changes))
    pinch=cooler.calculate(cooler.INPUTS|{'gas_outlet_K':298.15})
    assert pinch['evaluation_defined']==0 and pinch['failure_code']==1 and pinch['min_gap']<0

    source_cases=[]
    sources=json.loads(SOURCE_RECEIPT.read_text())
    for case in sources['cases']:
        p,c=case['primary'],case['control']
        flow=p['q_ihx']*1e6/(1560*195)
        shaft=flow*9.80665*40/.75/1e6
        x=boundary.INPUTS|dict(available=p['q_ihx'],capability_open=c['capability_open'],raw_heat=c['capability_at_solution'],feasible=c['feasible'],return_residual=c['return_residual'],primary_flow=p['mdot'],exchanger_flow=c['exchanger_primary_flow'],bypass_fraction=c['bypass_fraction'],pressure=8e6,hot_temperature=p['T_out'],dp=p['dp_loop'],salt_flow=flow,salt_shaft=shaft,salt_electric=shaft/.95)
        y=boundary.calculate(x)
        enough=c['capability_open']>=p['q_ihx']
        assert bool(y['converged']) is enough
        if enough:
            assert y['actual_heat']==p['q_ihx'] and y['salt_hot']==465.
            assert abs(y['duty_correction'])<=1e-8
        else:
            assert y['actual_heat']==c['capability_at_solution'] and y['duty_correction']==0
            assert y['salt_hot']<465 and y['unremoved_heat']>0
        close(y['bypass_flow'],p['mdot']*c['bypass_fraction'])
        close(y['added_dp'],p['dp_loop']/1.1*.1)
        close(flow*1560*(y['salt_hot']-y['salt_return'])/1e6,y['steam_heat'])
        # Run the actual retained steam/water bodies to check heat joins and
        # controller/salt/steam/water loads once across passing and failed source.
        steam_inputs=dict(enabled=1,heat_available_MW=y['steam_heat'],source_heat_MW=y['actual_heat'],selected_recovered_MW=shaft,salt_flow_per_circuit=flow/case['n_ihx'],salt_circuit_count=case['n_ihx'],salt_hot_C=y['salt_hot'],salt_return_C=y['salt_return'],salt_cp_kJ_kgK=1.56,main_pressure_MPa=6.2,extraction_pressure_MPa=.8,steam_temperature_C=445.,reheat_temperature_C=445.,condenser_temperature_C=42.,eta_hp=.9,eta_lp=.9,eta_condensate_pump=.8,eta_feedwater_pump=.8,eta_pump_motor=.95,eta_mechanical=.99,eta_generator=.98)
        s=prop.calculate(steam_inputs)
        loss=boundary.calculate(boundary.INPUTS|dict(cycle_rejection=s['q_rejection_before_cooling_MW'],salt_electric=shaft/.95,salt_shaft=shaft))
        w=water.calculate(dict(enabled=1,cycle_active=1,q_rejection_before_cooling_MW=loss['rejection_load'],condenser_temperature_C=42.,water_inlet_C=25.,water_outlet_C=35.,head_m=20.,eta_pump=.8,eta_motor=.95))
        l=ledger.calculate(ledger.INPUTS|dict(available_heat=p['q_ihx'],actual_heat=y['actual_heat'],gross=s['p_gross_MW'],steam_pumps=s['p_cycle_pumps_MW'],salt_pumps=shaft/.95,water1=w['p_cooling_pump_electric_MW'],rejected1=w['q_total_rejection_MW']))
        close(l['conversion_energy_residual'],0.,absolute=1e-8)
        close(l['energy_residual'],y['unremoved_heat'],absolute=1e-8)
        source_cases.append({'source':case['q_source_MW'],'n':case['n_ihx'],'boundary_inputs':x,'boundary_outputs':y,'steam_gross':s['p_gross_MW'],'steam_rejection':s['q_rejection_before_cooling_MW'],'water_outputs':w,'ledger_outputs':l})

    admission=[]
    base=boundary.INPUTS|dict(available=1000.,capability_open=1100.,raw_heat=1000.+5e-9,feasible=1.,return_residual=1e-7,salt_flow=1000e6/(1560*195))
    for name,change,expected in [('converged',{},True),('raw_duty_shortfall',{'raw_heat':1000-2e-8},False),('raw_return_mismatch',{'return_residual':2e-6},False),('solver_failure',{'feasible':0.},False),('one_ulp_open_shortfall',{'capability_open':math.nextafter(1000.,0.)},False),('boundary_return',{'return_residual':1e-6},True),('outside_return',{'return_residual':math.nextafter(1e-6,math.inf)},False)]:
        x=base|change;y=boundary.calculate(x)
        assert bool(y['converged']) is expected
        assert y['actual_heat']==(x['available'] if expected else x['raw_heat'])
        if not expected:assert y['duty_correction']==0
        admission.append({'name':name,'inputs':x,'outputs':y})
    gas_boundary=boundary.INPUTS|dict(available=gas['source']['q_ihx'],capability_open=gas['primary_bypass']['capability_open'],raw_heat=gas['primary_bypass']['capability_at_solution'],feasible=1.,return_residual=gas['primary_bypass']['return_residual'],primary_flow=gas['source']['mdot'],exchanger_flow=gas['primary_bypass']['exchanger_primary_flow'],bypass_fraction=gas['primary_bypass']['bypass_fraction'])
    full=boundary.calculate(gas_boundary);small=boundary.calculate(gas_boundary|{'bypass_flow_rating':500.})
    assert full['controller_capacity_ok']==1 and small['controller_capacity_ok']==0
    assert full['actual_heat']==small['actual_heat']

    # Direct discounted cashflow oracle: dated annual payments and dated events
    # in Decimal, independent of production factors or logarithmic formulas.
    finance=[]
    for rate in (0.,.05):
        for years in (20.,30.):
            x=ledger.INPUTS|dict(available_heat=1000.,actual_heat=1000.,gross=300.,steam_pumps=10.,salt_pumps=5.,water1=3.,controller_electric=.1,rejected1=718.1,capital1=30e6,capital2=2e6,capital3=100e6,capital4=40e6,currency_factor=1.7,controller_capital=10e6,separately_replaced_capital=6.6e6,salt_vendor=2e6,salt_installation=.6e6,salt_removal=.3e6,bundle_event=4e6,salt_stock_cost=2e6,rate=rate,years=years,scope_correction=3e6,common_source_pv=11e6)
            y=ledger.calculate(x)
            with localcontext() as ctx:
                ctx.prec=45
                d=lambda z:Decimal(str(z))
                discount=lambda year:(1+d(rate))**(-year)
                annual_factors=[discount(t) for t in range(1,int(years)+1)]
                ann=sum(annual_factors)
                cap=sum(d(x[f'capital{i}'])*d(x['currency_factor']) for i in range(1,11))+d(x['controller_capital'])
                recurring=cap-d(x['capital2'])*d(x['currency_factor'])-d(x['separately_replaced_capital'])
                machine=sum(d(2.9e6)*discount(t) for t in range(10,int(years),10))
                bundle=sum(d(4e6)*discount(t) for t in range(15,int(years),15))
                conversion=recurring*d(.2)*discount(15) if years>15 else 0
                cost=cap+machine+bundle+conversion+(recurring*d(.02)+d(2e6)*d(.001))*ann
                energy=d(8760)*d(.85)*(d(300)-d(18.1))*ann
                expected=dict(capital_total=cap,recurring_base=recurring,annuity_factor=ann,machine_replacement_pv=machine,bundle_replacement_pv=bundle,conversion_replacement_pv=conversion,accounted_pv=cost,discounted_energy=energy,cost_per_net_MWh=(cost+d(14e6))/energy)
                for key,value in expected.items():close(y[key],float(value),relative=2e-14,absolute=1e-7)
            close(y['conversion_energy_residual'],0.)
            finance.append({'inputs':x,'outputs':y,'decimal_oracle':{k:str(v) for k,v in expected.items()}})
    nonpositive=[]
    original_dcf=dcf.run_lcoe_dcf
    def forbidden_dcf(*a,**kw):raise AssertionError('positive-energy DCF called for nonpositive net')
    dcf.run_lcoe_dcf=forbidden_dcf
    for gross in (0.,.1):
        y=ledger.calculate(ledger.INPUTS|{'gross':gross})
        assert y['net_electric']<=0 and y['economic_defined']==0 and y['cost_per_net_MWh']==0
        nonpositive.append(y)
    dcf.run_lcoe_dcf=original_dcf
    # Generator and pump-loss joins: delta efficiency costs equal delta rejected
    # machine heat. They are not deducted again as electrical loads.
    loss_cases=[]
    for eta in (.95,.98):
        y=boundary.calculate(boundary.INPUTS|dict(net_shaft=500.,gross_electric=eta*500.,cycle_rejection=100.,salt_shaft=5.,salt_electric=5/.95))
        close(y['generator_loss'],500*(1-eta))
        close(y['rejection_load'],100+500*(1-eta)+5/.95-5+.1)
        loss_cases.append({'generator_efficiency':eta,'outputs':y})
    # A consuming shaft receives motor electricity. The motor's wasted work
    # is additional rejected heat and preserves the signed energy ledger.
    imported=boundary.calculate(boundary.INPUTS|dict(net_shaft=-100.,imported_electric=125.))
    close(imported['motor_import_loss'],25.)
    consuming=ledger.calculate(ledger.INPUTS|dict(available_heat=100.,actual_heat=100.,gross=0.,shaft_import=125.,water4=.2,rejected1=200.,rejected4=imported['rejection_load']+.2))
    close(consuming['conversion_energy_residual'],0.)
    assert consuming['economic_defined']==0 and consuming['net_electric']<0
    loss_cases.append({'name':'imported_drive','boundary_outputs':imported,'ledger_outputs':consuming})
    recup=[]
    for ua in (0.,60.,80.):
        for flow in (1500.,2000.,2500.):
            y=recuperator.calculate(dict(ua=ua,flow=flow,cp=5193.))
            # Equal-capacity heat exchange effectiveness rearranged as a
            # thermal-resistance identity: epsilon/(1-epsilon) = UA/C.
            close(y['effectiveness']/(1-y['effectiveness']),ua/y['capacity_rate'])
            recup.append({'ua':ua,'flow':flow,'outputs':y})

    paths=[*sorted(BODIES.glob('*_impl.py')),PROPERTIES,PROPERTIES.with_name('cooling_water_rejection_impl.py'),retained/'mfe_account_costs/financial_factors.py',retained/'mfe_lcoe_dcf/lcoe_dcf_impl.py',SOURCE_RECEIPT,GAS_RECEIPT]
    assert initial_body_hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in BODIES.glob('*_impl.py')}, 'body changed during check; rerun current revision'
    receipt={'scope':'Independent component check only; original properties via module alias, no generated schemas or native-package validation. Implementation files read only.', 'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'cooler_catalog':cooler_cases,'extra_coolers':extra_coolers,'cooler_refusals':cooler_refusals,'pinch':pinch,'max_quadrature_error_MW_K':max_quad_error,'max_quadrature_refinement_error_MW_K':max_refinement_error,'source_cases':source_cases,'admission_predicates':admission,'controller_full':full,'controller_insufficient':small,'finance':finance,'nonpositive_economics':nonpositive,'loss_joins':loss_cases,'recuperator':recup}
    args.out.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'cooler_catalog_cases':len(cooler_cases),'source_cases':len(source_cases),'finance_cases':len(finance),'max_quadrature_error_MW_K':max_quad_error,'max_refinement_error_MW_K':max_refinement_error,'receipt':str(args.out)}))


if __name__=='__main__':main()
