"""Independent WI-069 source identities and time-domain startup checks."""
import math
from pathlib import Path
import sys

import pytest

E2E = Path(__file__).resolve().parents[2] / 'exploration' / 'stellarator_e2e'
sys.path.insert(0, str(E2E))
import oracle_fuel_inventory as oracle


def scenario(**changes):
    # One T atom burned per second, artificial unit masses for auditable hand cases.
    p = dict(enabled=True, held_inventory=0., p_fus=1e-6, q_eff=1., mev_to_joules=1.,
             burn_fraction=.5, t_recycle=1., tbr_available=1., breeding_defined=1.,
             eta_extract=1., lambda_T=0., G_stock=0., m_T_kg=1., m_D_kg=2/3,
             plasma_volume=3., n_T0=2., alpha_n=1., tau_feed=0., tau_process=2.,
             tau_blanket=1., tau_extract=2., tau_buffer=0., reserve_fraction=0.,
             tau_reserve=0., startup_extension=1., shutdown_duration=1.,
             availability=.5, s_per_year=100.)
    p.update(changes)
    return p


def test_reviewed_hand_case_and_separate_prefill():
    r = oracle.evaluate(**scenario())
    assert r['startup_deficit_atoms'] == 5
    assert r['startup_minimum_atoms'] == 8  # 5 draw + 3 plasma prefill
    assert r['working_atoms'] == 8  # 3 plasma + 2 processor + 1 zone + 2 extractor
    assert r['makeup_signed_kg_s'] == 0
    reserve = oracle.evaluate(**scenario(tau_feed=2, tau_buffer=4,
                                        tau_reserve=6, reserve_fraction=.25))
    assert reserve['prefill_atoms'] == 15
    assert reserve['reserve_atoms'] == 3
    assert reserve['startup_minimum_atoms'] == 23
    assert reserve['startup_deficit_atoms'] == 5


@pytest.mark.parametrize('process,zone,extract,tbr,extension', [
    (2,1,2,1,1), (5,1,1,1.5,3), (0,0,0,2,1), (3,1,2,2,5),
    (2,1,2,0,10), (0,1,2,1.3,4), (5,0,0,1.3,4), (2,1,2,.7,100),
])
def test_startup_against_integrated_storage(process,zone,extract,tbr,extension):
    p = scenario(tau_process=process,tau_blanket=zone,tau_extract=extract,
                 tbr_available=tbr,startup_extension=extension,
                 tau_reserve=2,reserve_fraction=.25,tau_feed=1,tau_buffer=2)
    r = oracle.evaluate(**p)
    # Directly step the usable-storage ODE through independently constructed
    # event-aligned intervals. Stock starts after feed/plasma/buffer prefill.
    storage = r['startup_minimum_atoms']-r['prefill_atoms']
    minimum = storage
    h = r['startup_horizon_s']
    events = sorted(set((0.,process,zone+extract,h)))
    for left,right in zip(events,events[1:]):
        dt=(right-left)/1000
        for i in range(1000):
            t=left+(i+.5)*dt
            inflow=(1 if t>=process else 0)+(tbr if t>=zone+extract else 0)
            storage += (inflow-2)*dt
            minimum=min(minimum,storage)
    assert minimum == pytest.approx(r['reserve_atoms'], abs=1e-9)
    assert minimum-0.001 < r['reserve_atoms']  # any smaller initial supply fails


def test_decay_allowance_bounds_integrated_total_stock_decay():
    p=scenario(lambda_T=.003,tbr_available=1.1,t_recycle=.95,eta_extract=.9,
               startup_extension=10,tau_feed=2,tau_reserve=3,reserve_fraction=.25)
    r=oracle.evaluate(**p)
    # Independently solve total-stock ODE exactly per interval, including loss
    # commencement at processor/extractor outlet and decay of the allowance.
    total=r['startup_conservative_atoms']
    decayed=0.
    lam=p['lambda_T']
    production=p['tbr_available']
    events=sorted(set((0.,p['tau_process'],p['tau_blanket']+p['tau_extract'],r['startup_horizon_s'])))
    for a,b in zip(events,events[1:]):
        loss=(1-p['t_recycle']) if a>=p['tau_process'] else 0.
        loss += production*(1-p['eta_extract']) if a>=p['tau_blanket']+p['tau_extract'] else 0.
        source=production-1-loss
        dt=b-a
        equilibrium=source/lam
        end=equilibrium+(total-equilibrium)*math.exp(-lam*dt)
        decayed += total+source*dt-end
        total=end
    assert 0 < decayed <= r['startup_decay_allowance_atoms']
    assert r['startup_conservative_atoms']-decayed >= r['startup_minimum_atoms']


def test_particle_inventory_matches_numerical_volume_integral():
    p=scenario(alpha_n=.7,n_T0=8,plasma_volume=17)
    n=100000
    # u=1-rho^2 makes dV=V du: midpoint quadrature of the original profile.
    numerical=p['n_T0']*p['plasma_volume']*sum(((i+.5)/n)**p['alpha_n'] for i in range(n))/n
    assert oracle.evaluate(**p)['plasma_atoms'] == pytest.approx(numerical,rel=2e-8)


def test_flow_capacity_loss_and_calendar_identities():
    p=scenario(t_recycle=.9,eta_extract=.8,tbr_available=1.3,lambda_T=.001)
    r=oracle.evaluate(**p)
    assert r['injection_kg_s']-r['recycle_kg_s'] == pytest.approx(r['burn_kg_s']+r['recycle_loss_kg_s'])
    assert r['production_kg_s'] == pytest.approx(r['extracted_kg_s']+r['extraction_loss_kg_s'])
    assert r['processor_atoms'] == 2  # before recovery loss
    assert r['dt_processor_kg_s'] == pytest.approx(5/3)
    stopped=oracle.evaluate(**{**p,'availability':0})
    assert stopped['exhaust_kg_s']==r['exhaust_kg_s']
    assert stopped['dt_processor_kg_day']==r['dt_processor_kg_day']
    assert stopped['annual_exhaust_kg']==0
    assert stopped['annual_decay_kg']==r['annual_decay_kg']
    assert stopped['annual_makeup_signed_kg']==stopped['annual_decay_kg']


def test_shutdown_half_life_and_tiny_loss():
    r=oracle.evaluate(**scenario(lambda_T=math.log(2)/100,shutdown_duration=100))
    assert r['shutdown_remaining_kg']==pytest.approx(.5*r['total_kg'])
    assert r['shutdown_decay_loss_kg']==pytest.approx(.5*r['total_kg'])
    tiny=oracle.evaluate(**scenario(lambda_T=1e-30,shutdown_duration=1))
    assert tiny['shutdown_decay_loss_kg']>0


def test_undefined_production_and_dormant_carriers():
    p=scenario(breeding_defined=0,tbr_available=1.7)
    r=oracle.evaluate(**p)
    assert r['defined_flag']==0
    assert r['production_kg_s']==r['blanket_atoms']==0
    assert r['processor_atoms']==2
    assert r['burn_kg_s']==1
    dormant=oracle.evaluate(enabled=False,held_inventory=123)
    assert dormant['total_atoms']==123
    assert sum(v for k,v in dormant.items() if k!='total_atoms')==0
    assert set(r)==set(oracle.OUTPUTS)


@pytest.mark.parametrize('key,value', [
    ('enabled',.5),('breeding_defined',.5),('burn_fraction',0),('burn_fraction',1.01),
    ('eta_extract',0),('t_recycle',-1),('reserve_fraction',1.1),('availability',-.1),
    ('tau_feed',-1),('tau_process',-1),('tau_blanket',-1),('tau_extract',-1),
    ('tau_buffer',-1),('tau_reserve',-1),('startup_extension',-1),
    ('shutdown_duration',-1),('G_stock',1),('alpha_n',-1),('plasma_volume',-1),
    ('n_T0',-1),('p_fus',-1),('p_fus',0),('held_inventory',-1),('tbr_available',-1),('lambda_T',-1),
    ('m_D_kg',0),('m_T_kg',0),('q_eff',0),('mev_to_joules',0),('s_per_year',0),
    ('lambda_T',.25),('n_T0',float('nan')),('tau_process',float('inf')),
    ('p_fus',1e308),
])
def test_invalid_active_inputs_fail(key,value):
    with pytest.raises(ValueError):
        oracle.evaluate(**scenario(**{key:value}))


def test_all_active_inputs_finite():
    for key in scenario():
        with pytest.raises(ValueError):
            oracle.evaluate(**scenario(**{key:float('nan')}))


def test_current_native_mapping_and_retired_override():
    from studies import oracle_entry
    prefix=oracle_entry.P
    mappings=oracle_entry.ORACLE_OUTPUT_TO_CHANNEL
    for field in oracle.OUTPUTS:
        assert mappings['inventory_'+field]==prefix+'fuel_cycle__inventory__'+field
    with pytest.raises(oracle_entry.OracleSeamError):
        oracle_entry._oracle_overrides({prefix+'fuel_cycle__I_total':1})
    with pytest.raises(oracle_entry.OracleSeamError):
        oracle_entry._oracle_overrides({prefix+'fuel_cycle__inventory_enabled':.5})


def test_reserve_is_not_a_residence_delay():
    a=oracle.evaluate(**scenario(lambda_T=.001,tau_reserve=1,reserve_fraction=.25))
    b=oracle.evaluate(**scenario(lambda_T=.001,tau_reserve=1000,reserve_fraction=.25))
    assert a['max_decay_residence']==b['max_decay_residence']==.002
    assert b['reserve_atoms']>a['reserve_atoms']


def test_full_oracle_preserves_existing_channels_and_consumes_computed_stock():
    from studies import oracle_entry as e
    channels=e.evaluate({})
    p=e.vs.IN
    prefix=e.P
    mass=channels[prefix+'fuel_cycle__inventory__total_kg']
    assert mass>0
    assert channels[prefix+'magnet__material_inventory__mass_copper']>0
    burn=channels[prefix+'fuel_cycle__fuel__burn_rate']
    loss=channels[prefix+'fuel_cycle__fuel__loss_rate']
    required=(burn+loss+p['lambda_T']*mass/p['m_T_kg']+p['G_stock'])/(p['eta_extract']*burn)
    assert channels[prefix+'fuel_cycle__fuel__tbr_required']==pytest.approx(required,rel=1e-14)
    assert channels[prefix+'fuel_cycle__inventory__burn_kg_s']==pytest.approx(burn*p['m_T_kg'],rel=1e-14)


# Native tests consume sealed package outputs; no implementation source is read.
from tests.models.test_winding_pack_cost import runtime_paths, evaluate as native_evaluate

NATIVE_CASES = {
    'slow-processing-and-extraction': {'fuel_cycle__tau_feed':1800., 'fuel_cycle__tau_process':18000.,
                                     'fuel_cycle__tau_blanket':8640., 'fuel_cycle__tau_extract':432000.},
    'fast-processing-short-reserve': {'fuel_cycle__tau_process':4680., 'fuel_cycle__tau_reserve':21600.},
    'immediate-breeding-before-recycle': {'fuel_cycle__tau_blanket':0., 'fuel_cycle__tau_extract':0.},
    'loss-and-burn-sensitivity': {'fuel_cycle__burn_fraction':.025, 'fuel_cycle__t_recycle':.999,
                                'fuel_cycle__eta_extract':.95},
    'buffer-reserve-and-extension': {'fuel_cycle__tau_buffer':3600., 'fuel_cycle__reserve_fraction':1.,
                                    'fuel_cycle__startup_extension':259200.},
    'availability': {'unplanned_fraction':.2},
    'zero-decay': {'fuel_cycle__lambda_T':0.},
    'profile-shape': {'plasma__alpha_n':.8},
    'shutdown-duration': {'fuel_cycle__shutdown_duration':388800000.},
    'dormant-held-inventory': {'fuel_cycle__inventory_enabled':False,'fuel_cycle__processing_enabled':False,'fuel_cycle__held_inventory':1e25},
}


@pytest.mark.codegen_available
@pytest.mark.parametrize('case', NATIVE_CASES)
def test_native_off_reference_inventory_matches_independent_oracle(native_evaluate,case):
    from studies import oracle_entry as e
    changes=NATIVE_CASES[case]
    row=native_evaluate(changes)
    expected=e.evaluate({e.P+k:v for k,v in changes.items()})
    for field in oracle.OUTPUTS:
        channel=e.P+'fuel_cycle__inventory__'+field
        assert row.outputs[channel]==pytest.approx(expected[channel],rel=1e-9,abs=1e-18), (case,field)


def test_long_shutdown_keeps_positive_exponential_tail():
    p=scenario(lambda_T=.001,shutdown_duration=600000.)
    r=oracle.evaluate(**p)
    expected=r['total_kg']*math.exp(-600)
    assert expected>0
    assert r['shutdown_remaining_kg']==pytest.approx(expected,rel=1e-14,abs=0.)
    assert r['shutdown_decay_loss_kg']==r['total_kg']


@pytest.mark.codegen_available
def test_native_long_shutdown_keeps_positive_exponential_tail(native_evaluate):
    from studies import oracle_entry as e
    changes={'fuel_cycle__shutdown_duration':3e11}
    row=native_evaluate(changes)
    expected=e.evaluate({e.P+k:v for k,v in changes.items()})
    channel=e.P+'fuel_cycle__inventory__shutdown_remaining_kg'
    assert expected[channel]>0
    assert row.outputs[channel]==pytest.approx(expected[channel],rel=1e-9,abs=0.)


@pytest.mark.parametrize('changes', [
    {'q_eff':1e308,'mev_to_joules':1e308},
    {'q_eff':1e-300,'mev_to_joules':1e-300},
    {'lambda_T':1e308,'shutdown_duration':1e308},
    {'p_fus':1e308,'q_eff':1e308},
    {'p_fus':1e-300,'q_eff':1e308},
])
def test_intermediate_overflow_or_underflow_cannot_vanish(changes):
    with pytest.raises(ValueError):
        oracle.evaluate(**scenario(**changes))
