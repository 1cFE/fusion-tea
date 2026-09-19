"""WI-069 physical identities and counterexamples through the typed public module."""
import importlib
import math

import pytest

from tests.models.test_winding_pack_cost import runtime_paths, evaluate, output

# Deliberately simple unit-defined hand case: 100 T atoms/s burned, kg/atom scale
# chosen only to make arithmetic readable; these are not reactor assumptions.
CASE = dict(enabled_in=True, held_inventory_in=0., p_fus_in=1e-4, q_eff_in=1.,
            mev_to_joules_in=1., burn_fraction_in=.5, t_recycle_in=.8,
            tbr_available_in=1.3, breeding_defined_in=1., eta_extract_in=.9,
            lambda_T_in=0., G_stock_in=0., m_T_kg_in=.003, m_D_kg_in=.002,
            plasma_volume_in=10., n_T0_in=30., alpha_n_in=2., tau_feed_in=2.,
            tau_process_in=3., tau_blanket_in=4., tau_extract_in=1., tau_buffer_in=1.,
            tau_reserve_in=2., reserve_fraction_in=.25, startup_extension_in=2.,
            shutdown_duration_in=10., availability_in=.5, s_per_year_in=100.)


@pytest.fixture(scope='module')
def run_inventory(runtime_paths):
    module = importlib.import_module('stellarator_tea.modules.mfe_fuel_cycle.fuel_inventory')
    impl = importlib.import_module('stellarator_tea.handwritten.mfe_fuel_cycle.fuel_inventory_impl')
    assert impl.AUTO_IMPLEMENTED is False

    def run(changes=None):
        values = CASE | (changes or {})
        typed = module.Fuel_InventoryInput(**values)
        direct = dict(zip(module.Fuel_InventoryOutput.model_fields, impl.run_fuel_inventory(typed), strict=True))
        public = module.Fuel_InventoryModule().run(**values).data.model_dump()
        assert direct == public
        return public
    return run


def test_hand_case_stocks_and_stream_conservation(run_inventory):
    x = run_inventory()
    for name, atoms in dict(feed=400, plasma=100, processor=300, blanket=520,
                           extraction=130, buffer=200, reserve=100, working=1650, total=1750).items():
        assert x[name + '_atoms'] == pytest.approx(atoms)
        assert x[name + '_kg'] == pytest.approx(atoms * .003)
    assert x['injection_kg_s'] == pytest.approx(x['burn_kg_s'] + x['exhaust_kg_s'])
    assert x['exhaust_kg_s'] == pytest.approx(x['recycle_kg_s'] + x['recycle_loss_kg_s'])
    assert x['production_kg_s'] == pytest.approx(x['extracted_kg_s'] + x['extraction_loss_kg_s'])
    assert x['makeup_signed_kg_s'] == pytest.approx(.009)
    assert x['dt_processor_kg_s'] == pytest.approx(.5)
    assert x['dt_processor_kg_s'] != 2 * x['exhaust_kg_s']


@pytest.mark.parametrize('alpha', [-.5, 0., .5, 2., 10.])
def test_profile_stock_by_independent_midpoint_quadrature(run_inventory, alpha):
    # Integrate in volume coordinate u=1-rho^2; no production formula used.
    n = 200000
    integral = math.fsum(((i + .5) / n) ** alpha for i in range(n)) / n
    expected = CASE['n_T0_in'] * CASE['plasma_volume_in'] * integral
    assert run_inventory({'alpha_n_in': alpha})['plasma_atoms'] == pytest.approx(expected, rel=.002)


@pytest.mark.parametrize('process,blanket,extract,tbr,extension', [
    (3.,4.,1.,1.3,2.), (8.,1.,0.,2.,0.), (1.,4.,2.,.1,20.), (5.,5.,0.,3.,5.), (0.,0.,0.,2.,0.)])
def test_startup_stock_by_time_integrated_storage_trajectory(run_inventory, process, blanket, extract, tbr, extension):
    row = run_inventory(dict(tau_process_in=process, tau_blanket_in=blanket,
                            tau_extract_in=extract, tbr_available_in=tbr, startup_extension_in=extension))
    horizon = row['startup_horizon_s']
    # Integrate storage withdrawals across a fine partition containing stream events.
    nodes = sorted({0., process, blanket + extract, horizon} | {horizon * i / 1000 for i in range(1001)})
    balance = 0.; minimum = 0.
    for a, b in zip(nodes, nodes[1:]):
        t = (a+b)/2
        supply = (80. if t >= process else 0.) + (.9*tbr*100 if t >= blanket+extract else 0.)
        balance += (supply-200.)*(b-a)
        minimum = min(minimum, balance)
    assert row['startup_deficit_atoms'] == pytest.approx(-minimum, abs=1e-8)
    assert row['startup_minimum_atoms'] == pytest.approx(row['prefill_atoms'] + row['reserve_atoms'] - minimum)
    assert row['startup_minimum_atoms'] - row['startup_deficit_atoms'] == pytest.approx(800.)
    assert row['startup_decay_allowance_atoms'] == 0


def test_reserve_and_breeder_fill_counted_once(run_inventory):
    base = run_inventory()
    doubled = run_inventory({'tau_reserve_in': 4.})
    assert doubled['startup_minimum_atoms'] - base['startup_minimum_atoms'] == pytest.approx(100.)
    assert doubled['total_atoms'] - base['total_atoms'] == pytest.approx(100.)
    assert base['startup_minimum_atoms'] == pytest.approx(1646.)
    assert base['prefill_atoms'] == 700.


@pytest.mark.parametrize('decay', [0., 1e-12, .001, .1])
def test_decay_allowance_bounds_decay_of_extra_stock_itself(run_inventory, decay):
    x = run_inventory({'lambda_T_in': decay})
    allowance = x['startup_decay_allowance_atoms']
    horizon = x['startup_horizon_s']
    # Gross production is an upper bound: no subtraction for burn/losses.
    bound_mass = x['startup_conservative_atoms'] + 130. * horizon
    assert allowance == pytest.approx(decay * horizon * bound_mass)
    integrated_upper = decay * (x['startup_conservative_atoms'] * horizon + .5*130.*horizon**2)
    assert allowance >= integrated_upper


def test_half_life_and_small_shutdown_decay_are_stable(run_inventory):
    x = run_inventory({'lambda_T_in': math.log(2)/10})
    assert x['shutdown_remaining_kg'] == pytest.approx(x['total_kg']/2)
    y = run_inventory({'lambda_T_in': 1e-20})
    assert y['shutdown_decay_loss_kg'] > 0
    assert y['shutdown_decay_loss_kg'] == pytest.approx(y['total_kg']*1e-19, rel=1e-12, abs=0)
    late = run_inventory({'lambda_T_in': .01, 'shutdown_duration_in': 5000.})
    assert late['shutdown_remaining_kg'] > 0
    assert late['shutdown_remaining_kg'] == pytest.approx(late['total_kg'] * math.exp(-50), rel=1e-12, abs=0)


def test_availability_changes_annual_flows_not_installed_capacity_or_stock(run_inventory):
    a = run_inventory({'lambda_T_in': .001})
    b = run_inventory({'lambda_T_in': .001, 'availability_in': 0.})
    for name in a:
        if not name.startswith('annual_') and name != 'calendar_processor_kg_s':
            assert a[name] == b[name], name
    assert b['annual_injection_kg'] == 0
    assert b['annual_decay_kg'] == a['annual_decay_kg'] > 0
    assert b['annual_makeup_signed_kg'] == b['annual_decay_kg']


def test_lossless_limits_and_power_scaling(run_inventory):
    ideal = run_inventory({'burn_fraction_in': 1., 't_recycle_in': 1., 'eta_extract_in': 1., 'tbr_available_in': 1.})
    assert ideal['processor_atoms'] == ideal['exhaust_kg_s'] == ideal['recycle_loss_kg_s'] == 0
    assert ideal['makeup_signed_kg_s'] == 0
    a = run_inventory(); b = run_inventory({'p_fus_in': 2e-4})
    assert b['injection_kg_s'] == 2*a['injection_kg_s']
    assert b['total_atoms'] - b['plasma_atoms'] == 2*(a['total_atoms']-a['plasma_atoms'])


def test_dormant_and_undefined_breeding_are_explicit_diagnostic_states(run_inventory):
    dormant = run_inventory({'enabled_in': False, 'held_inventory_in': 42.})
    assert dormant.pop('total_atoms') == 42.
    assert set(dormant.values()) == {0.}
    x = run_inventory({'breeding_defined_in': 0., 'tbr_available_in': 0.})
    assert x['defined_flag'] == 0
    assert x['processor_atoms'] == 300.
    assert all(math.isfinite(v) for v in x.values())
    # Invalid producer status overrides a finite stale TBR carrier.
    assert run_inventory({'breeding_defined_in': 0., 'tbr_available_in': 1.7}) == x


@pytest.mark.parametrize('key', list(CASE))
def test_nonfinite_inputs_refused(run_inventory, key):
    with pytest.raises(ValueError):
        run_inventory({key: math.nan})


@pytest.mark.parametrize('changes', [dict(p_fus_in=0.), dict(m_T_kg_in=0.), dict(m_D_kg_in=0.),
    dict(q_eff_in=0.), dict(mev_to_joules_in=0.), dict(s_per_year_in=0.), dict(burn_fraction_in=0.),
    dict(burn_fraction_in=1.1), dict(t_recycle_in=-.1), dict(t_recycle_in=1.1), dict(eta_extract_in=0.),
    dict(eta_extract_in=1.1), dict(alpha_n_in=-1.), dict(tau_process_in=-1.), dict(G_stock_in=1.),
    dict(reserve_fraction_in=1.1), dict(availability_in=-.1), dict(lambda_T_in=1.),
    dict(breeding_defined_in=.5), dict(p_fus_in=1e308), dict(n_T0_in=1e308),
    dict(q_eff_in=1e-300, mev_to_joules_in=1e-300),
    dict(p_fus_in=1e-320, q_eff_in=1e300),
    dict(lambda_T_in=1e200, shutdown_duration_in=1e200, tau_feed_in=0., tau_process_in=0.,
         tau_blanket_in=0., tau_extract_in=0., tau_buffer_in=0., tau_reserve_in=0.,
         startup_extension_in=0., n_T0_in=0.)])
def test_invalid_active_domains_and_overflow_refused(run_inventory, changes):
    with pytest.raises(ValueError):
        run_inventory(changes)


def test_reserve_interruption_does_not_change_residence_diagnostic(run_inventory):
    x = run_inventory({'lambda_T_in': .001, 'tau_reserve_in': 1000.})
    assert x['max_decay_residence'] == .004


@pytest.mark.codegen_available
def test_native_inventory_drives_existing_breeding_and_preserves_fuel_cost(evaluate):
    base = evaluate()
    changed = evaluate({'fuel_cycle__tau_process': 28800.})
    for row in (base, changed):
        assert output(row, 'fuel_cycle__inventory__defined_flag') == 1
        assert output(row, 'fuel_cycle__inventory__burn_kg_s') == pytest.approx(output(row, 'fuel_cycle__fuel__burn_rate')*5.008267663228036e-27, rel=1e-12, abs=1e-18)
        burn = output(row, 'fuel_cycle__fuel__burn_rate')
        stock = output(row, 'fuel_cycle__inventory__total_atoms')
        expected = (burn + output(row, 'fuel_cycle__fuel__loss_rate') + 1.782785958230312e-9*stock)/burn
        assert output(row, 'fuel_cycle__fuel__tbr_required') == pytest.approx(expected, rel=1e-12)
        assert output(row, 'breeding_adequacy__decay_rate') == pytest.approx(1.782785958230312e-9*stock)
    assert output(changed, 'fuel_cycle__inventory__total_kg') > output(base, 'fuel_cycle__inventory__total_kg')
    assert output(changed, 'fuel_cycle__fuel__tbr_required') > output(base, 'fuel_cycle__fuel__tbr_required')
    assert output(changed, 'fuel_cycle__fuel_calc__annual_fuel') == output(base, 'fuel_cycle__fuel_calc__annual_fuel')


@pytest.mark.codegen_available
def test_native_dormant_inventory_preserves_legacy_held_requirement(evaluate):
    zero = evaluate({'fuel_cycle__inventory_enabled': False, 'fuel_cycle__held_inventory': 0.})
    held = evaluate({'fuel_cycle__inventory_enabled': False, 'fuel_cycle__held_inventory': 1e26})
    assert output(zero, 'fuel_cycle__fuel__tbr_required') == pytest.approx(1.19)
    assert output(zero, 'fuel_cycle__inventory__defined_flag') == 0.
    assert output(held, 'fuel_cycle__inventory__total_atoms') == 1e26
    burn = output(held, 'fuel_cycle__fuel__burn_rate')
    assert output(held, 'fuel_cycle__fuel__tbr_required') == pytest.approx(1.19 + 1.782785958230312e-9*1e26/burn)
