"""Retain the scalar diagnostic that produced source-coupling-probe.json.

The arithmetic and receipt fields reproduce the original inline diagnostic.
The added CLI requires a new output path; it never overwrites an existing file.
This is diagnostic evidence, not an approved study-policy/model implementation.
Run from the repository root with .codex-test/run python and --out <new-path>.
The receipt's revision records the checkout used for each replay.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
from pathlib import Path
from types import SimpleNamespace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    retained = Path(__file__).with_suffix(".json").resolve()
    if args.out.resolve() == retained:
        parser.error("--out must not name the retained source-coupling-probe.json")
    if args.out.exists():
        parser.error("--out must name a new file")

    body = Path('exploration/costed_loop_brayton/costed_loop_brayton_tea/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py')
    spec = importlib.util.spec_from_file_location('loop_probe', body)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = dict(T_in_in=573.15, dT_blanket_in=200., cp_in=5193., gamma_in=5/3,
                p_loop_in=8e6, n_loops_in=14., mdot_loop_ref_in=225.07777777777778,
                mdot_loop_rated_in=225.07777777777778, dp_loop_ref_in=329187.1856931558,
                f_loss_in=1., eta_is_in=.772796639536644, eta_drive_in=1.,
                loop_live_in=1., p_pump_direct_in=0., eta_p_direct_in=0.)
    area = 14852*math.pi*.01905*11.6
    lmtd = lambda a, b: a if a == b else (a-b)/math.log(a/b)
    ua_one = 267.8/lmtd(35, 19.3)
    nominal = 3125.9322770825056

    def evaluate(q, n):
        out = module.calculate(SimpleNamespace(q_source_in=q, **base))
        h = out['T_out']-738.15
        c = out['T_comp_in']-543.15
        matched = n*ua_one*lmtd(h, c)
        return out['q_ihx']-matched, out, matched

    rows = []
    for n in (10, 11, 12):
        lo, hi = 1000., nominal
        fl, _, _ = evaluate(lo, n)
        fh, _, _ = evaluate(hi, n)
        bracket = {'q_source_MW': [lo, hi], 'residual_MW': [fl, fh]}
        if not fl < 0 < fh:
            raise RuntimeError('no bracket')
        for iteration in range(1, 201):
            mid = (lo+hi)/2
            f, out, matched = evaluate(mid, n)
            if abs(f) <= 1e-9:
                break
            if f > 0:
                hi = mid
            else:
                lo = mid
        else:
            raise RuntimeError('nonconvergence')
        ch = out['mdot']*base['cp_in']/1e6
        salt_total = out['q_ihx']*1e6/(1560*195)
        cs = salt_total*1560/1e6
        cmin, cmax = min(ch, cs), max(ch, cs)
        cr = cmin/cmax
        ntu = n*ua_one/cmin
        eps = ntu/(1+ntu) if abs(1-cr) < 1e-10 else -math.expm1(-ntu*(1-cr))/(1-cr*math.exp(-ntu*(1-cr)))
        achieved = eps*cmin*(out['T_out']-543.15)
        ret = out['T_out']-achieved/ch
        salt_per = salt_total/n/4
        rows.append(dict(
            n_ihx=n, bracket=bracket, iterations=iteration, q_source_MW=mid,
            primary_loop=out, ihx_lmtd_duty_MW=matched,
            source_match_residual_MW=f, ihx_ntu_achieved_MW=achieved,
            ntu_duty_residual_MW=achieved-out['q_ihx'],
            actual_helium_return_K=ret, return_residual_K=ret-out['T_comp_in'],
            source_energy_residual_MW=out['q_ihx']-ch*(out['T_out']-out['T_comp_in']),
            source_heat_below_nominal=mid <= nominal,
            delivered_heat_below_nominal=out['q_ihx'] <= 3301.2132114869937,
            primary_flow_capacity_ok=out['capacity_margin'] >= 0,
            positive_suction=out['p_loop_margin'] > 0,
            hot_approach_K=out['T_out']-738.15,
            cold_approach_K=out['T_comp_in']-543.15,
            salt_flow_per_pump_k4_kg_s=salt_per,
            salt_225kg_s_offer_margin=225-salt_per,
            salt_250kg_s_offer_margin=250-salt_per,
            salt_operating_shaft_hp=salt_per*9.80665*40/.75/745.6998715822702,
        ))
    result = {
        'purpose': 'Bounded scalar source-loop/IHX matching diagnostic, not native integrated validation or reactor/hydraulic qualification',
        'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'loop_body': str(body),
        'loop_body_sha256': hashlib.sha256(body.read_bytes()).hexdigest(),
        'fixed_loop_inputs': base,
        'source_nominal_MW': nominal,
        'ihx_catalog': [10, 11, 12],
        'ihx_area_per_circuit_m2': area,
        'ihx_UA_per_circuit_MW_K': ua_one,
        'equations': {
            'root': 'loop.q_ihx(q_source)-n_ihx*UA_one*LMTD(loop.T_out-738.15,loop.T_comp_in-543.15)=0',
            'UA_one': '267.8/((35-19.3)/log(35/19.3))',
            'policy': 'bisection q_source in [1000,3125.9322770825056] MW, abs residual<=1e-9 MW, max200 iterations; no hardware mutated',
            'independent_check': 'counterflow effectiveness-NTU with helium and salt heat-capacity rates; achieved duty determines actual primary return',
        },
        'limitations': [
            'Original pressure-loss law includes reference IHX loss; changing IHX circuit topology is not a hydraulic prediction. Total-resistance law is retained as an explicit assumption.',
            'No plasma/blanket/source response model or validated reactor turndown range.',
            'Not a complete native generated/oracle or new assembly execution.',
            'Primary upstream costs and pumping excluded equally from conversion metric; loop outputs retained for context.',
        ],
        'cases': rows,
    }
    with args.out.open('x') as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False)+'\n')
    for row in rows:
        print(json.dumps({key: row[key] for key in (
            'n_ihx', 'q_source_MW', 'ihx_lmtd_duty_MW', 'actual_helium_return_K',
            'return_residual_K', 'source_match_residual_MW',
            'salt_flow_per_pump_k4_kg_s', 'salt_225kg_s_offer_margin',
            'salt_operating_shaft_hp',
        )}))
        print('primaryflowmargin', row['primary_loop']['capacity_margin'],
              'primarypumpMW', row['primary_loop']['p_elec'])


if __name__ == '__main__':
    main()
