"""Independent WI-096 thermal and conversion-cost verification equations.

Authority: work/active/WI-096_matched-conversion-subsystems/design.md sections 3-8.
Development checks: that item's evidence/four-body-check.py and .json.
Properties: the independently transcribed WI-073 oracle_matched_cycle_properties
asset, verified by oracle_matched_cycle.load(). No native bodies are imported.

Differences from production: the cooler integrates in water temperature using
piecewise heat capacities and logarithmic means, then uses Brent's method.
Production integrates in transferred heat and bisects. Ledger discounted payments
use 45-digit Decimal arithmetic. Integer-year annuities sum annual payments;
fractional horizons use the same continuous extension of the annual annuity.
Cooler iteration counts are solver diagnostics and are deliberately not returned
or certified. All other returned names have the production output semantics.
The 1e-7 C inward bracket offsets are retained numerical-domain policy, not new
hardware selection. No study input or installed capacity is selected by this code.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from functools import lru_cache
import math
from collections.abc import Mapping

from scipy.optimize import brentq

try:
    from . import oracle_matched_cycle as properties
except ImportError:
    import oracle_matched_cycle as properties


BOUNDARY_OUTPUTS = tuple('converged actual_heat unremoved_heat duty_correction raw_heat_residual raw_return_residual salt_hot salt_return steam_heat bypass_flow added_dp total_flow_margin exchanger_flow_margin bypass_flow_margin bypass_fraction_margin pressure_margin temperature_margin added_dp_margin controller_capacity_ok source_adequate generator_loss motor_import_loss salt_motor_loss rejection_load'.split())
COOLER_OUTPUTS = tuple('evaluation_defined failure_code duty water_inlet_after_C water_outlet_C water_flow pump_electric total_rejection min_gap required_ua ua_residual energy_residual flow_margin power_margin duty_margin bracket_low_ua bracket_high_ua'.split())
RECUPERATOR_OUTPUTS = ('capacity_rate', 'effectiveness')
LEDGER_OUTPUTS = tuple('gross_electric electrical_load net_electric total_rejected unremoved_heat energy_residual conversion_energy_residual conversion_energy_residual_magnitude capital_total recurring_base annual_service annual_makeup machine_replacement_pv bundle_replacement_pv conversion_replacement_pv replacement_pv annuity_factor annual_energy discounted_energy accounted_pv corrected_pv cost_per_net_MWh economic_defined energy_tolerance'.split()) + tuple(f'capital_{i}' for i in range(1, 11))
CERTIFIED_OUTPUTS = {'boundary': BOUNDARY_OUTPUTS, 'cooler': COOLER_OUTPUTS, 'recuperator': RECUPERATOR_OUTPUTS, 'ledger': LEDGER_OUTPUTS}
DIAGNOSTIC_OUTPUTS = {'cooler': ('iterations',)}


def _finite(x: Mapping) -> None:
    if any(not math.isfinite(v) for v in x.values()):
        raise ValueError('oracle requires finite inputs')


def boundary(x: Mapping) -> dict:
    """Check control admission, selected capacities and thermal/electric joins."""
    _finite(x)
    if x['loss_factor'] <= 0 or x['salt_cp'] <= 0:
        raise ValueError('positive loss factor and salt heat capacity required')
    heat_error = x['raw_heat'] - x['available']
    admitted = all((x['feasible'] == 1,
                    x['capability_open'] >= x['available'],
                    abs(heat_error) <= 1e-8,
                    abs(x['return_residual']) <= 1e-6))
    duty = x['available'] if admitted else x['raw_heat']
    if x['salt_flow'] > 0:
        capacity = x['salt_flow'] * x['salt_cp'] / 1e6
        cold = 270. - x['salt_shaft'] / capacity
        hot = 465. if admitted else 270. + duty / capacity
    else:
        cold, hot = 0., (465. if admitted else 0.)
    bypass_flow = x['primary_flow'] - x['exchanger_flow']
    added_loss = x['dp'] - x['dp'] / x['loss_factor']
    margins = {
        'total_flow_margin': x['total_flow_rating'] - x['primary_flow'],
        'exchanger_flow_margin': x['exchanger_flow_rating'] - x['exchanger_flow'],
        'bypass_flow_margin': x['bypass_flow_rating'] - bypass_flow,
        'bypass_fraction_margin': x['max_bypass'] - x['bypass_fraction'],
        'pressure_margin': x['pressure_rating'] - x['pressure'],
        'temperature_margin': x['temperature_rating'] - x['hot_temperature'],
        'added_dp_margin': x['added_dp_rating'] - added_loss,
    }
    generator_loss = (x['net_shaft'] if x['net_shaft'] > 0 else 0.) - x['gross_electric']
    imported_loss = x['imported_electric'] - (abs(x['net_shaft']) if x['net_shaft'] < 0 else 0.)
    salt_loss = x['salt_electric'] - x['salt_shaft']
    return dict(converged=float(admitted), actual_heat=duty,
                unremoved_heat=x['available']-duty, duty_correction=duty-x['raw_heat'],
                raw_heat_residual=heat_error, raw_return_residual=x['return_residual'],
                salt_hot=hot, salt_return=cold, steam_heat=duty+x['salt_shaft'],
                bypass_flow=bypass_flow, added_dp=added_loss, **margins,
                controller_capacity_ok=float(min(margins.values()) >= 0),
                source_adequate=float(admitted), generator_loss=generator_loss,
                motor_import_loss=imported_loss, salt_motor_loss=salt_loss,
                rejection_load=math.fsum((x['cycle_rejection'], generator_loss, imported_loss, salt_loss, x['actuation'])))


@lru_cache(maxsize=1)
def _liquid_rows():
    tables, _ = properties.load()
    return sorted(properties.phase(tables['saturation'], 'liquid'), key=lambda row: row['t'])


def _inverse_log_mean(a: float, b: float) -> float:
    """Integral of reciprocal linear temperature gap over a unit interval."""
    if a <= 0 or b <= 0:
        raise ValueError('cooler profile has a nonpositive gap')
    difference = b-a
    if difference == 0:
        return 1/a
    symmetric_ratio = difference/(a+b)
    logarithm = (2*math.atanh(symmetric_ratio) if abs(symmetric_ratio) < .5
                 else math.log(b)-math.log(a))
    return logarithm/difference


def cooler(x: Mapping) -> dict:
    """Independent piecewise-water cooler with a Brent outlet-temperature root."""
    _finite(x)
    duty = -x['gas_heat_into_fluid']
    gas_cold = x['gas_outlet_K']-273.15
    gas_hot = x['gas_inlet_K']-273.15
    if duty <= 0 or gas_hot <= gas_cold or x['ua'] <= 0:
        raise ValueError('positive cooling duty, gas temperature decrease and UA required')
    if not (20 <= x['water_inlet_C'] < 60 and x['head'] >= 0
            and 0 < x['eta_p'] <= 1 and 0 < x['eta_motor'] <= 1):
        raise ValueError('water or pump outside the supported domain')
    rows = _liquid_rows()
    enthalpy = lambda t: properties.interp(rows, 't', t)['h']
    specific_electric = 9.80665*x['head']/(1000*x['eta_p']*x['eta_motor'])
    reservoir_h = enthalpy(x['water_inlet_C'])
    inlet_h = reservoir_h+specific_electric
    water_inlet = properties.interp(rows, 'h', inlet_h)['t']
    result = dict.fromkeys(COOLER_OUTPUTS, 0.)
    result.update(duty=duty, water_inlet_after_C=water_inlet,
                  duty_margin=x['duty_rating']-duty)
    limit = min(gas_hot, 60.)
    if water_inlet >= limit or gas_cold <= water_inlet:
        result.update(failure_code=1., min_gap=gas_cold-water_inlet)
        return result

    def evaluate(outlet):
        outlet_h = enthalpy(outlet)
        water_rise = outlet_h-inlet_h
        mass_flow = 1000*duty/water_rise
        # Traverse water-temperature intervals, each with its own constant cp.
        # Their heat fractions set the simultaneous gas temperatures. Exact
        # endpoint temperatures avoid an enthalpy-inversion rounding cycle.
        nodes = [(water_inlet, inlet_h)]
        nodes += [(r['t'], r['h']) for r in rows if water_inlet < r['t'] < outlet]
        nodes.append((outlet, outlet_h))
        gaps = [gas_cold+(gas_hot-gas_cold)*(h-inlet_h)/water_rise-t for t,h in nodes]
        gaps[0], gaps[-1] = gas_cold-water_inlet, gas_hot-outlet
        if min(gaps) <= 0:
            raise ValueError('cooler property profile crosses the gas temperature')
        pieces = []
        for i, ((ta, ha), (tb, hb)) in enumerate(zip(nodes, nodes[1:])):
            cp = (hb-ha)/(tb-ta)
            heat = mass_flow*cp*(tb-ta)/1000
            pieces.append(heat*_inverse_log_mean(gaps[i], gaps[i+1]))
        return math.fsum(pieces), mass_flow, min(gaps)

    lower, upper = water_inlet+1e-7, limit-1e-7
    if lower >= upper:
        result['failure_code'] = 1.
        return result
    ua_low, ua_high = evaluate(lower)[0], evaluate(upper)[0]
    result.update(bracket_low_ua=ua_low, bracket_high_ua=ua_high)
    if not ua_low <= x['ua'] <= ua_high:
        result['failure_code'] = 2.
        return result
    outlet = brentq(lambda t: evaluate(t)[0]-x['ua'], lower, upper,
                    xtol=1e-11, rtol=1e-14, maxiter=200)
    required, flow, gap = evaluate(outlet)
    power = flow*specific_electric/1000
    result.update(evaluation_defined=1., water_outlet_C=outlet, water_flow=flow,
                  pump_electric=power, total_rejection=duty+power, min_gap=gap,
                  required_ua=required, ua_residual=required-x['ua'],
                  energy_residual=flow*(enthalpy(outlet)-reservoir_h)/1000-duty-power,
                  flow_margin=x['flow_rating']-flow, power_margin=x['power_rating']-power)
    return result


def recuperator(x: Mapping) -> dict:
    """Balanced counterflow heat-capacity/thermal-resistance relationship."""
    _finite(x)
    if x['ua'] < 0 or x['flow'] <= 0 or x['cp'] <= 0:
        raise ValueError('nonnegative UA and positive flow/cp required')
    rate = x['flow']*x['cp']/1e6
    effectiveness = 0. if x['ua'] == 0 else 1/(1+rate/x['ua'])
    return dict(capacity_rate=rate, effectiveness=effectiveness)


def ledger(x: Mapping) -> dict:
    """Disjoint conversion scope and independent high-precision dated cashflows."""
    _finite(x)
    if x['rate'] < 0 or x['years'] <= 0 or not 0 < x['availability'] <= 1 or min(x['machine_life'], x['bundle_life']) <= 0:
        raise ValueError('financial inputs outside the supported domain')
    # The public electrical boundary uses represented IEEE sums. Retain that
    # convention for zero-net admission; Decimal independently values costs.
    load = math.fsum(x[key] for key in ('shaft_import', 'steam_pumps', 'salt_pumps', 'water1', 'water2', 'water3', 'water4', 'controller_electric'))
    net = x['gross']-load
    rejection = math.fsum(x[f'rejected{i}'] for i in range(1, 5))
    with localcontext() as context:
        context.prec = 45
        d = lambda value: Decimal(str(value))
        rate, horizon = d(x['rate']), d(x['years'])
        discount = lambda time: (1+rate)**(-time)
        if rate == 0:
            annuity = horizon
        elif horizon == horizon.to_integral_value() and horizon <= 10000:
            annuity = sum(discount(Decimal(t)) for t in range(1, int(horizon)+1))
        else:
            annuity = (1-discount(horizon))/rate
        capital = {f'capital_{i}': d(x[f'capital{i}'])*d(x['currency_factor']) for i in range(1, 11)}
        total = sum(capital.values())+d(x['controller_capital'])
        recurring = total-capital['capital_2']-d(x['separately_replaced_capital'])
        annual_service = recurring*d(x['annual_service_fraction'])
        annual_makeup = d(x['salt_stock_cost'])*d(x['makeup_fraction'])

        def dated_events(amount, life):
            time, period = d(life), d(life)
            payments = Decimal(0)
            while time < horizon:
                payments += amount*discount(time)
                time += period
            return payments

        machine = dated_events(sum(d(x[k]) for k in ('salt_vendor', 'salt_installation', 'salt_removal')), x['machine_life'])
        bundle = dated_events(d(x['bundle_event']), x['bundle_life'])
        event_year = d(x['replacement_year'])
        conversion = recurring*d(x['replacement_fraction'])*discount(event_year) if 0 < event_year < horizon else Decimal(0)
        replacement = machine+bundle+conversion
        annual_energy = Decimal(8760)*d(net)*d(x['availability'])
        energy = annual_energy*annuity
        accounted = total+replacement+(annual_service+annual_makeup)*annuity
        corrected = accounted+d(x['scope_correction'])+d(x['common_source_pv'])
        values = dict(capital_total=total, recurring_base=recurring,
                      annual_service=annual_service, annual_makeup=annual_makeup,
                      machine_replacement_pv=machine, bundle_replacement_pv=bundle,
                      conversion_replacement_pv=conversion, replacement_pv=replacement,
                      annuity_factor=annuity, annual_energy=annual_energy,
                      discounted_energy=energy, accounted_pv=accounted, corrected_pv=corrected,
                      cost_per_net_MWh=corrected/energy if net > 0 else Decimal(0), **capital)
        result = {key: float(value) for key, value in values.items()}
    result.update(gross_electric=x['gross'], electrical_load=load, net_electric=net,
                  total_rejected=rejection, unremoved_heat=x['available_heat']-x['actual_heat'],
                  energy_residual=x['available_heat']-net-rejection,
                  conversion_energy_residual=x['actual_heat']-net-rejection,
                  conversion_energy_residual_magnitude=abs(x['actual_heat']-net-rejection),
                  economic_defined=float(net > 0), energy_tolerance=max(1e-6, abs(x['available_heat'])*1e-9))
    return result
