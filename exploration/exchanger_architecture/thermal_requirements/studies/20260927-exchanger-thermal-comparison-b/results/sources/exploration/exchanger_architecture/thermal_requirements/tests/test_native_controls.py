"""Acceptance assertions against complete native receipts and sealed predecessor."""
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[4]
EVIDENCE=ROOT/'work/active/WI-097_exchanger-thermal-requirements/evidence'
P='aries_integrated_plant__'
H=P+'heat_exchangers__evaluate__'


@pytest.fixture(scope='module')
def rows():
    return {r['case']:r for r in json.loads((EVIDENCE/'native-controls.json').read_text())}


def statuses(row):
    return {r['constraint_id']:r['status'] for r in row['outputs']['constraint_report']['results']}


def test_complete_legacy_preservation(rows):
    saved=json.loads((ROOT/'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/cases.json').read_text())['cases']
    summary=[]
    for name,row in rows.items():
        if not name.startswith('replay-'):
            continue
        assert row['status']=='evaluated'
        old=next(s for s in saved if s['inputs']=={k:row['effective_inputs'][k] for k in s['inputs']})
        assert len(old['outputs'])==551
        assert {k:row['outputs'][k] for k in old['outputs']}==old['outputs']
        now=statuses(row)
        assert {k:now[k] for k in old['verdicts']}==old['verdicts']
        summary.append({'case':name,'predecessor':old['case'],'numeric_channels':551,'legacy_predicates':14,'bit_exact':True})
    assert len(summary)==7
    (EVIDENCE/'native-legacy-preservation.json').write_text(json.dumps(summary,indent=2)+'\n')


def test_all_native_cases_evaluate(rows):
    assert len(rows)==18
    assert all(row['status']=='evaluated' for row in rows.values())
    for row in rows.values():
        assert len(statuses(row))==35
        assert abs(row['outputs'][P+'plant_ledger__evaluate__plant_residual'])<1e-6


@pytest.mark.parametrize('name',['offer-a-0','offer-a-1','offer-b-0','offer-b-1'])
def test_offered_cases_pass_all_native_checks(rows,name):
    row=rows[name]
    assert set(statuses(row).values())=={'satisfied'}
    assert row['outputs'][P+'plant_ledger__evaluate__net_electric']>0


def test_inadequate_conductance_propagates_into_actual_cycle(rows):
    a=rows['offer-b-0']['outputs'];b=rows['partial-transfer']['outputs']
    assert b[H+'pbli_unmet']>100
    assert b[H+'turbine_temperature']<a[H+'turbine_temperature']
    assert b[P+'plant_ledger__evaluate__net_electric']<a[P+'plant_ledger__evaluate__net_electric']
    assert b[H+'pbli_return_residual']==pytest.approx(b[H+'pbli_unmet']/(26860.*190./1e6),abs=1e-8)
    assert any('heat_removal_ok' in k and v=='violated' for k,v in statuses(rows['partial-transfer']).items())


def test_undefined_state_and_control_limit_cannot_pass(rows):
    zero=rows['zero-conductance']
    assert zero['outputs'][H+'divertor_state_defined']==0.
    assert any('divertor_state_ok' in k and v=='violated' for k,v in statuses(zero).items())
    control=rows['control-authority-failure']
    assert control['outputs'][H+'he_bypass_fraction']>.01
    assert any('he_control_ok' in k and v=='violated' for k,v in statuses(control).items())
    assert control['outputs'][H+'accepted_heat']==rows['offer-b-0']['outputs'][H+'accepted_heat']


def test_original_ua_preserves_heat_but_fails_approach(rows):
    for mode in ('0','1'):
        row=rows['original-controlled-'+mode]
        assert row['outputs'][H+'unmet_heat']==0.
        assert row['outputs'][H+'divertor_transferred']>300.
        assert row['outputs'][H+'divertor_cold_terminal_difference']<30.
        assert any('cold_approach_ok' in k and v=='violated' for k,v in statuses(row).items())


def test_explicit_purchases_and_held_equipment(rows):
    summary=[]
    for name in ('offer-a-0','offer-a-1','offer-b-0','offer-b-1','offer-b-linear-price'):
        row=rows[name];out=row['outputs'];inp=row['effective_inputs']
        total=0.
        for branch in ('he','pbli','divertor'):
            stem=P+branch+'_hx__'
            area=inp[stem+'selected_area']
            expected=inp[stem+'reference_cost']*inp[stem+'price_factor']*area/inp[stem+'reference_quantity']
            assert out[stem+'purchase__purchased_quantity']==area
            assert out[stem+'purchase__capital']==pytest.approx(expected,abs=1e-7)
            assert out[stem+'purchase__extrapolated']==1.
            total+=out[stem+'purchase__capital']
            if name!='offer-b-linear-price':
                assert out[stem+'purchase__capital']==pytest.approx(58325700.,abs=1e-7)
        assert total==pytest.approx(44327532. if name=='offer-b-linear-price' else 174977100.,abs=1e-6)
        summary.append({'case':name,'hx_capital_usd2004':total,'extrapolation_flags_preserved':True})
    for offer in ('a','b'):
        a=rows['offer-'+offer+'-0'];b=rows['offer-'+offer+'-1']
        for key,value in a['outputs'].items():
            if '__purchase__' in key:
                assert b['outputs'][key]==value
        for key,value in a['effective_inputs'].items():
            if any(x in key for x in ('selected_area','selected_rating','selected_flow_capacity')):
                assert b['effective_inputs'][key]==value
    (EVIDENCE/'native-purchase-invariants.json').write_text(json.dumps(summary,indent=2)+'\n')
