"""Independent dated-cashflow reconciliation of reviewed WI-091 finance.

Authority: WI-091 design accepted at b4ed8ecb. No native implementation imports.
Explicit Decimal cashflows replace production CRF and discount helper formulas.
Public/generated key bindings belong in lifecycle_bindings.py after ABI delivery.
"""
from decimal import Decimal, localcontext
from math import isfinite


def evaluate(*, overnight, net_power, annual_energy, years, availability,
             discount_rate, construction_years, annual_operating, annual_om,
             annual_tritium, annual_deuterium, annual_consumables, annual_import,
             supply_service_annual, replacement_interval, replacement_count,
             replacement_event_cost, terminal_fraction, salvage_fraction,
             other_overhaul_fraction, other_overhaul_year, annual_burn_kg,
             annual_loss_kg, annual_decay_kg, new_feed_kg):
    """Return unqualified diagnostic names; all currency is constant USD2004.

    Negative controls deliberately raise. The caller must never substitute this
    oracle for native evidence or a refused native lifecycle price.
    """
    values = locals().copy()
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v)
           for v in values.values()):
        raise ValueError('finite numeric financial inputs required')
    if years <= 0 or years != int(years):
        raise ValueError('positive integer calendar operating years required')
    if net_power <= 0 or annual_energy <= 0:
        raise ValueError('nonpositive net electricity: LCOE undefined')
    if not 0 < availability <= 1 or not 0 <= discount_rate <= 1:
        raise ValueError('unsupported availability or real discount rate')
    if replacement_interval <= 0 or other_overhaul_year <= 0:
        raise ValueError('invalid event date or interval')
    if replacement_count < 0 or replacement_count != int(replacement_count) or replacement_count >= 1_000_000:
        raise ValueError('invalid replacement event count')
    if any(value < 0 for name, value in values.items()
           if name not in ('net_power', 'annual_energy', 'availability', 'discount_rate')):
        raise ValueError('negative financial amount or selection')
    components = {
        'om': annual_om, 'tritium': annual_tritium,
        'deuterium': annual_deuterium, 'consumables': annual_consumables,
        'import': annual_import,
    }
    if abs(sum(components.values()) - annual_operating) > max(1e-6, abs(annual_operating)*1e-12):
        raise ValueError('annual operating components do not reconcile')
    if abs(annual_energy - 8760*net_power*availability) > max(1e-6, abs(annual_energy)*1e-12):
        raise ValueError('annual energy does not reconcile with net power and availability')
    with localcontext() as context:
        context.prec = 60
        d = lambda value: Decimal(str(value))
        one = Decimal(1)
        base = one + d(discount_rate)
        weight = lambda date: context.power(base, -d(date))
        dates = []
        k = 1
        # Explicit event enumeration avoids the production ceil boundary formula.
        while k*d(replacement_interval) < d(years):
            dates.append(k*d(replacement_interval))
            k += 1
            if k > 1_000_000:
                raise ValueError('oracle event enumeration exceeded support')
        if len(dates) != replacement_count:
            raise ValueError('replacement count disagrees with dated event schedule')
        annual_weights = [weight(year) for year in range(1, int(years)+1)]
        annuity = sum(annual_weights, Decimal(0))
        pv_energy = d(annual_energy)*annuity
        pv = {name: sum((d(amount)*w for w in annual_weights), Decimal(0))
              for name, amount in components.items()}
        pv['supply_service'] = d(supply_service_annual)*annuity
        pv['capital'] = d(overnight)*weight(-d(construction_years)/2)
        pv['replacement'] = sum((d(replacement_event_cost)*weight(date) for date in dates), Decimal(0))
        occurred = other_overhaul_year < years
        overhaul_amount = d(overnight)*d(other_overhaul_fraction) if occurred else Decimal(0)
        pv['other_overhaul'] = overhaul_amount*weight(other_overhaul_year)
        gross_terminal = d(overnight)*d(terminal_fraction)
        salvage_amount = d(overnight)*d(salvage_fraction)
        pv['decommissioning'] = gross_terminal*weight(years)
        pv['salvage'] = -salvage_amount*weight(years)
        total = sum(pv.values(), Decimal(0))
        noncapital = total-pv['capital']
        gross_feed = d(annual_burn_kg)+d(annual_loss_kg)+d(annual_decay_kg)
        result = {
            'annuity': annuity, 'crf': one/annuity,
            'financed_capital': pv['capital'], 'idc': pv['capital']-d(overnight),
            'annual_capital': pv['capital']/annuity,
            'pv_energy': pv_energy, 'lifetime_energy': d(annual_energy)*d(years),
            'pv_annual_operating': d(annual_operating)*annuity,
            'pv_terminal': pv['decommissioning']+pv['salvage'],
            'pv_total': total, 'noncapital_annual': noncapital/annuity,
            'annual_total': total/annuity, 'lcoe': total/pv_energy,
            'other_overhaul_occurs': Decimal(int(occurred)),
            'other_overhaul_amount': overhaul_amount,
            'gross_terminal_amount': gross_terminal, 'salvage_amount': salvage_amount,
            'gross_new_tritium_requirement': gross_feed,
            'additional_feed': d(new_feed_kg),
            'external_tritium': max(gross_feed-d(new_feed_kg), Decimal(0)),
            'curtailed_feed': max(d(new_feed_kg)-gross_feed, Decimal(0)),
        }
        result.update({'pv_'+name: value for name, value in pv.items()})
        result.update({'lcoe_'+name: value/pv_energy for name, value in pv.items()})
        return {name: float(value) for name, value in result.items()}
