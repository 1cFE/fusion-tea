"""Source-based WI-048 oracle, independent of generated code and closed-form DCF.

Osiris inputs: energy_from_inertial_fusion/images/page_007_table_0.png.
Driver/reactor/finance: Meier Eqs. 1-5, retaining 1988 dollars.
Power and annual cash flows: Hawker Eqs. 2.1-2.16, retaining the mixed cost basis.
"""
from math import isclose

PREFIX = 'hif_plant_pkg__hif_plant__'
NET_GATE = PREFIX + 'net_positive__1d299cceab19c61c'
HEURISTIC = PREFIX + 'viability__81ddf10fb1d1749b'
BASE = {
    'driver__beam_energy_mj': 5.0, 'driver__efficiency': 0.28, 'frequency': 4.6,
    'gain': 87.0, 'chamber__blanket_energy_multiple': 1.15, 'thermal_efficiency': 0.45,
    'availability': 0.90, 'driver__num_chambers': 1.0, 'driver__lifetime_shots': 6.0e9,
    'reactor_units': 1.0, 'target_factory_direct_cost_billions': 0.1,
    'discount_rate': 0.08, 'plant_cost_constant': 2000.0, 'om_cost_constant': 65.0,
    'target_factory__cost_per_target': 10.0, 'chamber__yield_cost_constant': 5.0e6,
    'construction_duration': 5.0, 'operational_duration': 40.0,
}
MUTATIONS = {
    'baseline': {}, 'beam10': {'driver__beam_energy_mj': 10.0},
    'eff35': {'driver__efficiency': 0.35}, 'rate5': {'frequency': 5.0},
}
BOUNDARY_BASE = {'driver__efficiency':0.1, 'gain':100.0,
                 'chamber__blanket_energy_multiple':1.0, 'frequency':5.0}
BOUNDARIES = {
    'counterexample': {'driver__efficiency':0.1, 'gain':100.0,
                      'chamber__blanket_energy_multiple':0.6, 'thermal_efficiency':0.3},
    'zero': dict(BOUNDARY_BASE, thermal_efficiency=0.2),
    'negative_neighbor': dict(BOUNDARY_BASE, thermal_efficiency=0.199999999),
    'positive_neighbor': dict(BOUNDARY_BASE, thermal_efficiency=0.200000001),
    'roundoff_positive': dict(BOUNDARY_BASE, frequency=4.6, thermal_efficiency=0.2),
}


def source_oracle(overrides=None):
    """Derive physical quantities, procurement and an explicit annual DCF sum."""
    v = BASE | (overrides or {})
    beam = v['driver__beam_energy_mj'] * 1e6
    bank = beam / v['driver__efficiency']
    rate = v['frequency']
    yield_j = beam * v['gain']
    fusion = yield_j * rate
    thermal = fusion * v['chamber__blanket_energy_multiple']
    gross = thermal * v['thermal_efficiency']
    driver = bank * rate
    net = gross - 2 * driver
    shots = rate * (365.25 * 24 * 3600) * v['availability']
    lifetime = v['driver__lifetime_shots'] / shots
    rate_factor = 1 + 0.0088 * (rate - 5)
    procurement = (0.32 + 0.088 * beam / 1e6) * (1.25 + 0.05 * v['driver__num_chambers']) * rate_factor
    driver_dollars = procurement * 1e9
    replacement = driver_dollars * shots / v['driver__lifetime_shots']
    reactor = 0.66 * (thermal / 1.67e9) ** 0.49 * (0.72 * v['reactor_units'] + 0.28)
    total = 1.83 * (reactor + procurement + v['target_factory_direct_cost_billions'])
    annualized = (0.083 + 0.03) * total
    meier_denominator = 0.0876 * v['availability'] * net / 1e9
    capex = v['plant_cost_constant'] * net / 1000 + v['chamber__yield_cost_constant'] * yield_j / 1e9 + driver_dollars
    opex = v['target_factory__cost_per_target'] * shots + v['om_cost_constant'] * net / 1000 + replacement
    annual_mwh = net / 1e6 * 8760 * v['availability']
    construction = int(v['construction_duration'])
    operation = int(v['operational_duration'])
    assert construction == v['construction_duration'] and operation == v['operational_duration'], (
        'source_oracle is the integer dated-stream reference; use decimal_present_value_reference for Real durations')
    # Explicit cash flows by calendar year; the production core uses geometric-series factors.
    cashflows = [(year, capex / construction, 0.0) for year in range(1, construction + 1)]
    cashflows += [(year, opex, annual_mwh) for year in range(construction + 1, construction + operation + 1)]
    discounted_cost = sum(cost / (1 + v['discount_rate']) ** year for year, cost, _ in cashflows)
    discounted_energy = sum(energy / (1 + v['discount_rate']) ** year for year, _, energy in cashflows)
    physical = dict(energy_on_target=beam, fusion_energy_per_shot=yield_j, fusion_power=fusion,
                    thermal_power=thermal, thermal_power_gw=thermal / 1e9, gross_electric_power=gross,
                    driver_electric_power=driver, other_parasitic_power=driver, net_electric_power=net,
                    net_electric_power_gw=net / 1e9, driver_recirculating_fraction=driver / gross,
                    total_recirculating_fraction=2 * driver / gross, shots_per_year=shots,
                    driver_lifetime_years=lifetime, driver_capital_cost=driver_dollars,
                    annual_driver_replacement_cost=replacement, discounted_cost=discounted_cost,
                    discounted_energy=discounted_energy)
    expected = {PREFIX + 'lcoe_calc__' + key:value for key,value in physical.items()}
    expected.update({PREFIX + key:value for key,value in {
        'driver__meier_cost__bank_energy_joules':bank, 'driver__meier_cost__cost_billions':procurement,
        'driver__meier_cost__gamma':driver_dollars / bank,
        'meier_reactor_cost_calc__reactor_cost_billions':reactor,
        'meier_capital_calc__total_capital_billions':total, 'meier_coe_calc__annualized_cost':annualized,
        'meier_coe_calc__energy_denominator':meier_denominator,
        'recirc_calc__f_recirc':driver / gross,
        'pv_factors__construction_factor':sum((1 + v['discount_rate']) ** -year for year in range(1, construction + 1)),
        'pv_factors__operation_factor':sum((1 + v['discount_rate']) ** -year for year in range(construction + 1, construction + operation + 1)),
        'hawker_price__price':discounted_cost / discounted_energy if net > 0 else 0,
        'meier_price__price':annualized / meier_denominator if net > 0 else 0,
        'hawker_price__generating':float(net > 0), 'meier_price__generating':float(net > 0),
    }.items()})
    return expected


def assert_source_outputs(actual, overrides=None):
    expected = source_oracle(overrides)
    assert set(actual) == set(expected)
    for name, value in expected.items():
        absolute_watts = 1e-6 if name.endswith(("fusion_power", "thermal_power", "gross_electric_power", "driver_electric_power", "other_parasitic_power", "net_electric_power")) else 0.0
        assert isclose(actual[name], value, rel_tol=1e-9, abs_tol=absolute_watts), (name, actual[name], value)


def decimal_present_value_reference(overrides=None):
    """80-digit independent annual reconstruction; integer dates or fractional algebra.

    Integer factors explicitly sum dated payments. Fractional factors evaluate
    the inherited difference-of-powers extension, never the production algorithm.
    Returned Decimal values retain the full reference precision for comparisons.
    """
    from decimal import Decimal as D, localcontext

    with localcontext() as context:
        context.prec = 80
        v = {key: D(str(value)) for key, value in (BASE | (overrides or {})).items()}
        beam = v['driver__beam_energy_mj'] * D('1e6')
        bank = beam / v['driver__efficiency']
        frequency = v['frequency']
        fusion_per_shot = beam * v['gain']
        net = (fusion_per_shot * frequency * v['chamber__blanket_energy_multiple']
               * v['thermal_efficiency'] - 2 * bank * frequency)
        # Hawker uses 365.25 days for shots and 8760 hours for annual energy.
        shots = D(31557600) * frequency * v['availability']
        procurement = ((D('.32') + D('.088') * beam / D('1e6'))
                       * (D('1.25') + D('.05') * v['driver__num_chambers'])
                       * (1 + D('.0088') * (frequency - 5)) * D('1e9'))
        capital = (v['plant_cost_constant'] * net / 1000
                   + v['chamber__yield_cost_constant'] * fusion_per_shot / D('1e9')
                   + procurement)
        operating = (v['target_factory__cost_per_target'] * shots
                     + v['om_cost_constant'] * net / 1000
                     + procurement * shots / v['driver__lifetime_shots'])
        annual_mwh = net / D('1e6') * 8760 * v['availability']
        construction = v['construction_duration']
        operation = v['operational_duration']
        rate = v['discount_rate']
        integer = construction == int(construction) and operation == int(operation)
        if integer:
            construction_factor = sum((1 + rate) ** -year
                                      for year in range(1, int(construction) + 1))
            operation_factor = sum((1 + rate) ** -year for year in range(
                int(construction) + 1, int(construction + operation) + 1))
        elif rate == 0:
            construction_factor, operation_factor = construction, operation
        else:
            construction_factor = (1 - (1 + rate) ** -construction) / rate
            operation_factor = ((1 + rate) ** -construction
                                - (1 + rate) ** (-construction - operation)) / rate
        cost = capital / construction * construction_factor + operating * operation_factor
        energy = annual_mwh * operation_factor
        return {
            'discounted_cost': cost, 'discounted_energy': energy,
            'price': cost / energy if net > 0 else D(0),
            'construction_factor': construction_factor, 'operation_factor': operation_factor,
        }, 'dated_integer_sums' if integer else 'fractional_power_extension'
