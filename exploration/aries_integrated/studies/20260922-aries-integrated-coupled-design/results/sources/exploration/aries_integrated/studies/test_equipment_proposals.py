"""Preparation invariants independent of the generated model or evaluator."""
import pytest
from exploration.aries_integrated.studies import equipment_proposals as p
from exploration.aries_integrated.studies import equipment_oracle as o


def test_complete_proposals_preserve_hardware_for_thermal():
    fields={key for row in p.axes() for key in row['keys']}
    nominal=dict.fromkeys(fields,1.)
    canonical={name:nominal|{'marker':float(i)} for i,name in enumerate((
        'nominal-calculated','nominal-source-assumed','literal-Lyon-source-input','literal-Raffray-accounting'))}
    rows=p.propose(canonical,fields|{'marker'})['cases']
    assert len(rows)==64
    assert sum(row['arm']=='thermal' for row in rows)==54
    hardware={p.key('he_hx','selected_area'),p.key('he_pump','selected_flow_capacity')}
    for row in rows:
        if row['arm'] in ('thermal','demand'):
            assert {k:row['point'][k] for k in hardware}=={k:nominal[k] for k in hardware}
    for row in rows[:4]:
        assert row['point']==canonical[row['case']]


def test_missing_new_abi_field_refuses():
    with pytest.raises(ValueError,match='absent from generated ABI'):
        p.declare_axes([])


def test_geometry_vs_property_role():
    assert o.exchanger(50000,1000)==50
    assert o.exchanger(50000,500)==25
    assert o.purchase(50000,50000,100)==100
    assert o.purchase(75000,50000,100)==150


def test_schedule_excludes_initial_and_terminal_events():
    result=o.schedule(5,1,20,10)
    assert result['event_times']==[5,10,15]
    assert result['lifetime_total']==30


def test_pump_operating_response_and_fixed_source_mode():
    assert o.pump(3261,3261,156,.8)==156
    assert o.pump(4891.5,3261,156,.8)==pytest.approx(526.5)
    assert o.pump(4891.5,3261,156,.8,fixed=True)==156


def test_selected_stock_affects_decay_not_burn():
    args=dict(burn_rate=1e20,loss_rate=1e18,exhaust_rate=2e21,atom_mass=5e-27,
              seconds_per_year=31536000,availability=.85,residence_s=1000,
              decay_constant=1.78e-9,recovered_kg=0,price_musd_kg=30)
    low=o.fuel(selected_kg=10,**args)
    high=o.fuel(selected_kg=20,**args)
    assert high['annual_burn_kg']==low['annual_burn_kg']
    assert high['annual_decay_kg']==2*low['annual_decay_kg']
    assert high['initial_stock_cost']==2*low['initial_stock_cost']


def test_unknown_predicate_is_not_assumed_balance(monkeypatch):
    from exploration.aries_integrated.studies import oracle_entry, study_route
    monkeypatch.setattr(study_route,'interface',lambda:{'constraints':{
        'aries_integrated_plant__new_owner__new_rule__123':'new_rule'}})
    with pytest.raises(ValueError,match='no reviewed predicate mapping'):
        oracle_entry.operand_bindings()
