"""Bounded design diagnostic: chosen source heat and unchanged salt bypass body.

Run from repository root; --out must name a new file. No source/ratio search.
This does not execute the proposed assembled model or qualify valve hydraulics.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from types import SimpleNamespace


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('--out must name a new file')
    loop_path = Path('exploration/costed_loop_brayton/costed_loop_brayton_tea/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py')
    control_path = Path('exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py')
    loop = load(loop_path, 'loop')
    control = load(control_path, 'control')
    base = dict(T_in_in=573.15, dT_blanket_in=200., cp_in=5193., gamma_in=5/3,
                p_loop_in=8e6, n_loops_in=14., mdot_loop_ref_in=225.07777777777778,
                mdot_loop_rated_in=225.07777777777778, dp_loop_ref_in=329187.1856931558,
                f_loss_in=1.1, eta_is_in=.772796639536644, eta_drive_in=1.,
                loop_live_in=1., p_pump_direct_in=0., eta_p_direct_in=0.)
    ua_one = 267.8/((35-19.3)/math.log(35/19.3))
    rows = []
    for q in (2500., 2800., 3000.):
        primary = loop.calculate(SimpleNamespace(q_source_in=q, **base))
        for n in (10, 11, 12, 14):
            salt_flow = primary['q_ihx']*1e6/(1560*195)
            c = control.calculate(SimpleNamespace(
                ua_in=n*ua_one, primary_flow_in=primary['mdot'], primary_cp_in=5193.,
                secondary_flow_in=salt_flow, secondary_cp_in=1560.,
                primary_limit_in=primary['T_out'], secondary_inlet_in=543.15,
                duty_in=primary['q_ihx'], required_return_in=primary['T_comp_in'],
                max_bypass_in=.5, tolerance_in=1e-6))
            actual = c['capability_at_solution']
            shaft = salt_flow*9.80665*40/.75/1e6
            hot = 270+actual*1e6/(salt_flow*1560)
            cold = 270-shaft*1e6/(salt_flow*1560)
            bypass_flow = primary['mdot']-c['exchanger_primary_flow']
            dp_allowance = primary['dp_loop']*(1-1/1.1)
            rows.append(dict(q_source_MW=q, n_ihx=n, primary=primary, control=c,
                actual_steam_source_MW=actual, source_unremoved_MW=primary['q_ihx']-actual,
                actual_salt_hot_C=hot, salt_return_C=cold,
                steam_heat_available_MW=actual+shaft,
                salt_energy_residual_MW=salt_flow*1560*(hot-cold)/1e6-actual-shaft,
                salt_per_pump_k4_kg_s=salt_flow/(4*n),
                salt_225_margin_kg_s=225-salt_flow/(4*n),
                salt_250_margin_kg_s=250-salt_flow/(4*n),
                imposed_controller_dp_Pa=dp_allowance,
                controller_flow_ok=primary['mdot']<=4000 and bypass_flow<=2000,
                controller_dp_ok=dp_allowance<=100000,
                controller_bypass_ok=c['bypass_fraction']<=.5,
                source_and_controller_match=bool(c['feasible'] and abs(c['return_residual'])<=1e-6)))
    result = dict(purpose=__doc__, fixed_loop_inputs=base,
        source_offers_MW=[2500,2800,3000], ihx_offers=[10,11,12,14],
        bodies={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (loop_path,control_path)},
        limitations=['Imposed common resistance, no valve Cv or fraction-dependent hydraulic prediction.',
                    'Only source/salt controller arithmetic; no native assembly, gas, cooler, cost or steam solver execution.'],
        cases=rows)
    with args.out.open('x') as f:
        f.write(json.dumps(result, indent=2, allow_nan=False)+'\n')
    for row in rows:
        print(json.dumps({k:row[k] for k in ('q_source_MW','n_ihx','source_and_controller_match','source_unremoved_MW','actual_salt_hot_C','salt_250_margin_kg_s')}))


if __name__ == '__main__':
    main()
