"""SV-091: represented calendar boundaries, independent dated finance and energy."""
import importlib.util
import json
import math
import os
import sys
from decimal import Decimal as D, localcontext
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'work/active/WI-052_mfe-financial-rate-limits/implementation'
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
import reference_finance as ref
from stellarator_tea.modules.mfe_lifecycle.lifecycle_calendar import Lifecycle_CalendarModule, Lifecycle_CalendarInput
from stellarator_tea.handwritten.mfe_lifecycle import lifecycle_calendar_impl as current

KEYS=('availability','coil_life_margin_fpy','replacement_pv','planned_downtime_yr','terminal_downtime_yr','unplanned_downtime_yr','productive_fpy','dated_energy_ratio','cas72_annual','n_replacements','physical_life_fpy')
PHYSICAL=tuple(k for k in KEYS if k not in ('replacement_pv','cas72_annual','dated_energy_ratio'))
RATES=[0.,.02,.08]+[s*x for x in (1e-4,1e-8,1e-12,1e-16,1e-18) for s in (-1,1)]
BASE=dict(cost_per_event=1e6,q_n_in=1.,fluence_limit_in=2.,interest_rate=.08,operational_years_in=8.,outage_years_in=.5,unplanned_fraction_in=0.,coil_life_fpy_in=100.,availability_direct_in=0.)

def neighbors(value):return (math.nextafter(value,-math.inf),value,math.nextafter(value,math.inf))

def fixtures():
    cases={}
    def add(name,**changes):cases[name]=dict(BASE,**changes)
    add('live_multiple');add('live_zero_damage',q_n_in=0.);add('live_zero_cost',cost_per_event=0.);add('live_no_events',fluence_limit_in=16.)
    add('live_zero_outage',outage_years_in=0.)
    add('live_fractional_unplanned',operational_years_in=8.5,unplanned_fraction_in=.25)
    add('live_terminal_inside',operational_years_in=2.25)
    for j,n in enumerate(neighbors(2.)):
        add(f'live_run_end_{j}',operational_years_in=n)
    for j,n in enumerate(neighbors(2.5)):
        add(f'live_completion_{j}',operational_years_in=n)
    for j,n in enumerate(neighbors(3.+1e-12)):
        add(f'energy_ceil_epsilon_{j}',operational_years_in=n)
    for j,l in enumerate(neighbors(1.)):
        add(f'energy_segment_year_{j}',fluence_limit_in=l,operational_years_in=4.,outage_years_in=1.)
    for j,q in enumerate(neighbors(1e-6)):
        add(f'held_wall_floor_{j}',availability_direct_in=.5,fluence_limit_in=1e-6,q_n_in=q)
    for j,l in enumerate(neighbors(.5)):
        add(f'held_life_floor_{j}',availability_direct_in=.5,fluence_limit_in=l)
    for j,l in enumerate(neighbors(4.)):
        add(f'held_cap_{j}',availability_direct_in=.5,fluence_limit_in=l)
    for j,n in enumerate(neighbors(8.)):
        add(f'held_count_{j}',availability_direct_in=.5,operational_years_in=n)
    for j,n in enumerate(neighbors(1.)):
        add(f'held_cap_below_floor_{j}',availability_direct_in=.5,operational_years_in=n,fluence_limit_in=.125)
    add('held_subannual_cap',availability_direct_in=.5,operational_years_in=.25,fluence_limit_in=.125)
    add('held_fractional',availability_direct_in=.5,operational_years_in=8.5)
    add('held_zero_cost',availability_direct_in=.5,cost_per_event=0.)
    return cases
CASES=fixtures()

@pytest.fixture(scope='module')
def entering():
    path=HERE/'entering/package/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py'
    spec=importlib.util.spec_from_file_location('wi052_entering_calendar',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def close(actual,expected):
    with localcontext() as ctx:
        ctx.prec=100
        error=abs(D(actual)-expected)
        if expected:error/=abs(expected)
        assert error<=D('1e-9'),(actual,str(expected),str(error))

def independent_schedule(x):
    """Closed-form event index construction; no production helper or oracle."""
    N=x['operational_years_in'];A=x['availability_direct_in']
    if A:
        life=min(max(x['fluence_limit_in']/max(x['q_n_in'],1e-6),.5),N*A)
        interval=life/A
        count=max(0,math.ceil(N/interval)-1)
        return [k*interval for k in range(1,count+1)],[],{'life':life,'interval':interval,'count':count,'floor':life==.5,'cap':life==N*A}
    b=1-x['unplanned_fraction_in'];d=x['outage_years_in']
    life=math.inf if x['q_n_in']==0 else x['fluence_limit_in']/x['q_n_in']
    run=life/b
    if math.isinf(run):return [],[(0.,N)],{'run':run,'count':0}
    dates=[];segments=[];k=0
    while True:
        start=k*(run+d)
        if start>=N:break
        end=start+run
        segments.append((start,min(end,N)))
        if end>=N or end+d>=N:break
        dates.append(end);k+=1
    return dates,segments,{'run':run,'count':len(dates),'completion_before':bool(dates)}

def energy_reference(segments,b,N,i,F):
    """Decimal interval intersection and dated-year PV with inherited epsilon count."""
    with localcontext() as ctx:
        ctx.prec=100
        numerator=denominator=D(0)
        for year in range(1,math.ceil(N-1e-12)+1):
            lo,hi=D(year-1),min(D(year),D(N))
            online=sum((max(D(0),min(D(end),hi)-max(D(start),lo)) for start,end in segments),D(0))
            weight=(1+D(i))**(-year)
            numerator+=D(b)*online*weight
            denominator+=(D(F)/D(N))*(hi-lo)*weight
        return numerator,denominator,numerator/denominator

@pytest.mark.parametrize('name',CASES)
def test_all_public_fields_at_represented_boundaries(name,entering,record_property):
    x=CASES[name]
    original=entering.lifecycle_calendar(Lifecycle_CalendarInput(**x))
    dates,segments,branch=independent_schedule(x)
    assert original['events']==dates,(name,original['events'],dates)
    record_property('represented_boundary',json.dumps({'name':name,'inputs':x,'branch':branch,'events':dates}))
    for rate in RATES:
        inputs=Lifecycle_CalendarInput(**dict(x,interest_rate=rate))
        actual=current.lifecycle_calendar(inputs)
        public=Lifecycle_CalendarModule().run(**inputs.model_dump()).data.model_dump()
        assert tuple(public)==KEYS
        assert all(public[k]==actual[k] for k in KEYS)
        assert actual['events']==original['events']
        assert {k:actual[k] for k in PHYSICAL}=={k:original[k] for k in PHYSICAL}
        try:
            at_rate=entering.lifecycle_calendar(inputs)
        except ZeroDivisionError:
            at_rate=None
        if at_rate is not None:
            assert {k:actual[k] for k in PHYSICAL}=={k:at_rate[k] for k in PHYSICAL}
            assert actual['events']==at_rate['events']
        pv=ref.dated_pv(x['cost_per_event'],rate,dates)
        close(actual['replacement_pv'],pv)
        with localcontext() as ctx:
            ctx.prec=100
            close(actual['cas72_annual'],pv*ref.crf(rate,x['operational_years_in']))
        if x['availability_direct_in']:
            assert actual['dated_energy_ratio']==1.
        else:
            num,den,ratio=energy_reference(segments,1-x['unplanned_fraction_in'],x['operational_years_in'],rate,actual['productive_fpy'])
            captured={}
            def profile(frame,event,arg):
                if event=='return' and frame.f_code is current._dated_energy_ratio.__code__:captured.update(frame.f_locals)
            previous=sys.getprofile();sys.setprofile(profile)
            try:actual_ratio=current._dated_energy_ratio(segments,1-x['unplanned_fraction_in'],x['operational_years_in'],rate,actual['productive_fpy'])
            finally:sys.setprofile(previous)
            close(captured['num'],num);close(captured['den'],den)
            close(actual_ratio,ratio);close(actual['dated_energy_ratio'],ratio)
