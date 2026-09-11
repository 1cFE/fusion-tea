"""Read-only sealed-module probe; explicit Decimal cash flows are independent PV evidence."""
import hashlib
import json
from decimal import Decimal as D, localcontext
from pathlib import Path
import traceback

from exploration.ife_e2e.studies import study_route as route
from tests.ife_oracle import BASE, BOUNDARIES

HERE = Path(__file__).resolve().parent
module, fingerprint = route.package_loader(route.PACKAGE_DIR, HERE / 'pkg_link').load()
from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEInput
from ife_tea.handwritten.ife_lcoe.ife_lcoe_impl import run_ife_lcoe
from ife_tea.modules.ife_lcoe.generating_electricity_price import Generating_Electricity_PriceInput
from ife_tea.handwritten.ife_lcoe.generating_electricity_price_impl import run_generating_electricity_price


def inputs(overrides):
    v = BASE | overrides
    beam = v['driver__beam_energy_mj']
    bank = beam * 1e6 / v['driver__efficiency']
    procurement = (0.32 + 0.088 * beam) * (1.25 + 0.05 * v['driver__num_chambers']) * (1 + 0.0088 * (v['frequency'] - 5)) * 1e9
    return IFE_LCOEInput(availability_in=v['availability'], blanket_energy_multiple=v['chamber__blanket_energy_multiple'], discount_rate_in=v['discount_rate'], driver_cost_constant=procurement/bank, driver_efficiency=v['driver__efficiency'], driver_energy=bank, driver_lifetime_shots=v['driver__lifetime_shots'], frequency_in=v['frequency'], gain_in=v['gain'], om_cost_constant_in=v['om_cost_constant'], plant_cost_constant_in=v['plant_cost_constant'], target_cost_constant=v['target_factory__cost_per_target'], thermal_efficiency_in=v['thermal_efficiency'], yield_cost_constant=v['chamber__yield_cost_constant'], construction_years=v['lcoe_calc__construction_years'], operational_years=v['lcoe_calc__operational_years'])


def dated_sums(overrides):
    with localcontext() as ctx:
        ctx.prec = 80
        v = {k:D(str(x)) for k,x in (BASE | overrides).items()}
        beam = v['driver__beam_energy_mj'] * D('1e6')
        bank = beam/v['driver__efficiency']
        rate = v['frequency']
        fusion_yield = beam*v['gain']
        net = fusion_yield*rate*v['chamber__blanket_energy_multiple']*v['thermal_efficiency'] - 2*bank*rate
        shots = D(31557600)*rate*v['availability']
        procurement = (D('.32')+D('.088')*beam/D('1e6'))*(D('1.25')+D('.05')*v['driver__num_chambers'])*(1+D('.0088')*(rate-5))*D('1e9')
        capital = v['plant_cost_constant']*net/1000 + v['chamber__yield_cost_constant']*fusion_yield/D('1e9') + procurement
        operating = v['target_factory__cost_per_target']*shots+v['om_cost_constant']*net/1000+procurement*shots/v['driver__lifetime_shots']
        annual_energy = net/D('1e6')*8760*v['availability']
        construction, operation = v['lcoe_calc__construction_years'],v['lcoe_calc__operational_years']
        assert construction == int(construction) and operation == int(operation), 'oracle scope, not model domain'
        r = v['discount_rate']
        cash = [(y,capital/construction,D(0)) for y in range(1,int(construction)+1)]
        cash += [(y,operating,annual_energy) for y in range(int(construction)+1,int(construction+operation)+1)]
        cost = sum(c/(1+r)**y for y,c,e in cash)
        energy = sum(e/(1+r)**y for y,c,e in cash)
        return dict(discounted_cost=float(cost),discounted_energy=float(energy),price=float(cost/energy) if net>0 else 0.0)


rates = [0.08,0.0] + [sign*10.0**(-n) for n in [4,8,12,14,16,18] for sign in [1,-1]]
rows=[]
for scenario, mutation in [('baseline',{}),('net_zero',BOUNDARIES['zero']),('non_generator',BOUNDARIES['counterexample'])]:
    for rate in rates:
        overrides=mutation | {'discount_rate':rate}
        p=inputs(overrides)
        expected=dated_sums(overrides)
        row=dict(scenario=scenario,rate=rate,inputs=p.model_dump(),decimal_dated_sums=expected)
        try:
            out=run_ife_lcoe(p)
            actual=dict(discounted_cost=out[9],discounted_energy=out[2])
            row['actual']=actual
            row['net_power']=out[8]
            row['relative_errors']={k:(actual[k]-expected[k])/expected[k] if expected[k] else None for k in actual}
            row['guard_reached']=True
            try:
                price, generating = run_generating_electricity_price(Generating_Electricity_PriceInput(numerator=out[9],denominator=out[2],net_power=out[8]))
                actual['price']=price
                row['generating']=generating
                row['relative_errors']['price']=(price-expected['price'])/expected['price'] if expected['price'] else None
            except Exception:
                row['price_error']=traceback.format_exc()
        except Exception:
            row['core_error']=traceback.format_exc()
            row['guard_reached']=False
        rows.append(row)

# Fractional durations are accepted and evaluated by the current model. The
# annual oracle is deliberately not used to claim dated fractional cash flows.
fractional=[]
for rate in [0.08,0.0]:
    p=inputs({'discount_rate':rate,'lcoe_calc__construction_years':5.5,'lcoe_calc__operational_years':40.5})
    try:
        out=run_ife_lcoe(p)
        fractional.append(dict(rate=rate,accepted=True,cost=out[9],energy=out[2]))
    except Exception as exc:
        fractional.append(dict(rate=rate,accepted=True,error=repr(exc)))

seal=json.loads((route.PACKAGE_DIR/'contracts/package_contract.json').read_text())
tracked=[Path('models/library/analyses/ife_lcoe.sysml'), route.PACKAGE_DIR/'handwritten/ife_lcoe/ife_lcoe_impl.py',route.PACKAGE_DIR/'handwritten/ife_lcoe/generating_electricity_price_impl.py',Path('tests/ife_oracle.py')]
result=dict(executable_fingerprint=fingerprint,seal=seal,fractional_duration_probes=fractional,files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked},rows=rows)
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
for row in rows:
    if row['scenario']=='baseline':
        print(row['rate'], row.get('relative_errors'), 'CORE ERROR' if 'core_error' in row else 'PRICE ERROR' if 'price_error' in row else '')
print('identity',fingerprint)
print('zero reference', rows[1]['decimal_dated_sums'])
print('fractional durations',fractional)
(HERE/'pkg_link'/'ife_tea').unlink()
(HERE/'pkg_link').rmdir()
