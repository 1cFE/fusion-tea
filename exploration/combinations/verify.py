"""Independent identity checks on the stored WI-093 case results (design § 8), plus the case summary.

Every identity is a Decimal recomputation from the stored inputs and outputs; no second implementation of any
definition. Also checks that each case's constraint report names exactly the assembly's checks with statuses
consistent with the stored margins, and that the package tree is unchanged after the runs.

Run: .codex-test/run python exploration/combinations/verify.py [--runs DIR --out-dir DIR]
"""
import hashlib
import json
import math
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'combinations_tea'
EVIDENCE = ROOT / 'work/completed/20260926_WI-093_combination-assemblies/evidence'
RUNS = EVIDENCE / 'native_runs'
L = 'combinations_loop_brayton__loop_brayton__'
C = 'combinations_plasma_chain__plasma_chain__'
F = 'combinations_lumped_fit__lumped_fit__'
E = 'combinations_circulator_purchase__circulator_purchase__'
D = lambda x: Decimal(str(x))
EXPECTED_GATES = {
    L: {'compressor_capacity__capacity_ok', 'turbine_capacity__capacity_ok', 'generator_capacity__capacity_ok',
        'rejection_capacity__capacity_ok', 'he_capacity__capacity_ok', 'checks__heat_removal_ok', 'checks__net_positive',
        'checks__loop_capacity_ok'},
    C: {b + '_capacity__capacity_ok' for b in ('he', 'pbli', 'divertor', 'compressor', 'turbine', 'rejection', 'generator', 'fuel')}
       | {b + '_pump__capacity_ok' for b in ('he', 'pbli', 'divertor')} | {'checks__heat_removal_ok', 'checks__net_positive'},
    F: {b + '_fit__domain_ok' for b in ('he', 'divertor', 'pbli')},
    E: {'circulator_capacity__capacity_ok'},
}
FAILURES = []


def close(a, b, tol=1e-6, what=''):
    fa, fb = float(a), float(b)
    if not (math.isfinite(fa) and math.isfinite(fb)) or abs(fa - fb) > tol:
        FAILURES.append(f'{what}: {a} vs {b} (diff {fa - fb}, tol {tol})')


def check(condition, what):
    if not condition:
        FAILURES.append(what)


class Case:
    def __init__(self, row):
        self.row = row
        self.out = row['outputs']
        self.inp = row['effective_inputs']

    def o(self, key):
        return self.out[key]

    def i(self, key):
        return self.inp[key]

    def gate(self, prefix, name):
        results = [r for r in self.out['constraint_report']['results'] if r['constraint_id'].startswith(prefix + name + '__')]
        check(len(results) == 1, f'{prefix}{name}: {len(results)} constraint results')
        return results[0]

    def gates(self, prefix):
        found = set()
        for r in self.out['constraint_report']['results']:
            cid = r['constraint_id']
            if cid.startswith(prefix):
                found.add('__'.join(cid[len(prefix):].split('__')[:2]))
        return found


def screen(case, prefix, part, demand, calc='evaluate', rating_key='selected_rating', rating=None):
    rating = case.i(prefix + part + '__' + rating_key) if rating is None else rating
    margin = case.o(prefix + part + '__' + calc + '__margin')
    close(margin, D(rating) - D(demand), tol=max(1e-6, 1e-9 * abs(float(rating))), what=f'{prefix}{part} margin')
    g = case.gate(prefix, part + '__capacity_ok')
    check(g['status'] == ('satisfied' if margin >= 0 else 'violated'), f'{prefix}{part} status {g["status"]} vs margin {margin}')
    return margin, g['status']


def brayton(case, P, he_available, extra_aux=()):
    """Closure, expander, recuperator and electrical identities shared by C-1 and C-2 (the same definitions, new partners)."""
    o, i = case.o, case.i
    c = D(i(P + 'cycle__selected_flow')) * D(i(P + 'cycle__cp')) / D('1e6')
    T_turbine = D(o(P + 'heat_exchangers__evaluate__turbine_temperature'))
    close(o(P + 'heat_exchangers__evaluate__accepted_heat'), c * (T_turbine - D(o(P + 'heat_exchangers__evaluate__heater_inlet'))), what=P + 'accepted heat')
    close(o(P + 'heat_exchangers__evaluate__heater_inlet'), o(P + 'recuperator__evaluate__cold_out'), tol=1e-10, what=P + 'recuperator state: heater inlet = recuperator cold out')
    # Cycle stream through each stage: the whole flow in series (mode 0); in the published network (mode 1) the PbLi and
    # divertor stages split the stream by the supplied fraction (network_heat_driven_closure_impl.py:31).
    split = D(o(P + 'heat_exchangers__evaluate__pbli_split_used'))
    series = o(P + 'heat_exchangers__evaluate__network_mode_used') == 0
    stream = {'he': c, 'pbli': c if series else split * c, 'divertor': c if series else (1 - split) * c}
    for b in ('he', 'pbli', 'divertor'):
        q = D(o(P + f'heat_exchangers__evaluate__{b}_transferred'))
        close(q, stream[b] * (D(o(P + f'heat_exchangers__evaluate__{b}_secondary_out')) - D(o(P + f'heat_exchangers__evaluate__{b}_secondary_in'))), what=P + b + ' transferred')
        close(he_available[b], q + D(o(P + f'heat_exchangers__evaluate__{b}_unmet')), what=P + b + ' available = transferred + unmet')
    close(o(P + 'heat_exchangers__evaluate__unmet_heat'), sum(D(o(P + f'heat_exchangers__evaluate__{b}_unmet')) for b in ('he', 'pbli', 'divertor')), what=P + 'unmet sum')
    check(abs(o(P + 'heat_exchangers__evaluate__closure_residual')) <= 1e-6, P + 'closure residual')
    check(1 <= o(P + 'heat_exchangers__evaluate__iterations') <= 100, P + 'iterations')
    close(o(P + 'rejection_capacity__' + ('rejected_heat__rejected_heat' if P == L else 'cycle_rejection__cycle_rejection')),
          -(D(o(P + 'intercooler_1__evaluate__heat_into_fluid')) + D(o(P + 'intercooler_2__evaluate__heat_into_fluid')) + D(o(P + 'precooler__evaluate__heat_into_fluid'))), what=P + 'rejected heat expression')
    e = lambda k: D(o(P + 'electrical__evaluate__' + k))
    close(e('compressor_demand'), sum(D(o(P + f'compressor_{k}__evaluate__shaft_demand')) for k in (1, 2, 3)), what=P + 'compressor demand')
    close(e('net_shaft'), D(o(P + 'turbine__evaluate__shaft_produced')) - e('compressor_demand'), what=P + 'net shaft')
    aux = e('primary_pump_electric') + e('heating_electric') + e('cryo_electric') + e('fuel_electric') + e('control_electric') + e('other_electric_demand')
    close(e('auxiliary_electric'), aux, what=P + 'auxiliary sum')
    close(e('net_electric'), e('gross_electric') - e('shaft_import') - aux, what=P + 'net electric')
    close(e('fuel_electric'), e('fuel_base_electric') + e('fuel_variable_electric'), what=P + 'fuel electric')
    g = case.gate(P, 'checks__heat_removal_ok')
    unmet = o(P + 'heat_exchangers__evaluate__unmet_heat')
    check(g['status'] == ('satisfied' if unmet <= i(P + 'checks__energy_tolerance') else 'violated'), P + f'heat_removal status {g["status"]} vs unmet {unmet}')
    g = case.gate(P, 'checks__net_positive')
    check(g['status'] == ('satisfied' if o(P + 'electrical__evaluate__net_electric') > 0 else 'violated'), P + 'net_positive status')


def verify_c1(case):
    o, i, P = case.o, case.i, L
    q = D(i(P + 'blanket_source__q_source'))
    cp, dT, n = D(i(P + 'primary_loop__loop_cp')), D(i(P + 'primary_loop__loop_dT_blanket')), D(i(P + 'primary_loop__n_loops'))
    lp = lambda k: D(o(P + 'primary_loop__evaluate__' + k))
    close(lp('mdot'), q * D('1e6') / (cp * dT), what='C-1 loop mdot')
    close(lp('mdot_loop'), lp('mdot') / n, what='C-1 mdot_loop')
    close(lp('T_out'), D(i(P + 'primary_loop__loop_T_in')) + dT, what='C-1 T_out')
    close(lp('q_ihx'), q + lp('w_fluid'), what='C-1 q_ihx')
    close(lp('q_recovered_total'), D(i(P + 'primary_loop__loop_live')) * lp('w_fluid') + D(i(P + 'primary_loop__eta_p_direct')) * D(i(P + 'primary_loop__p_pump_direct')), what='C-1 q_recovered_total')
    close(lp('capacity_margin'), D(i(P + 'primary_loop__mdot_loop_rated')) - lp('mdot_loop'), what='C-1 capacity_margin')
    close(o(P + 'electrical__evaluate__pump_loss'), lp('p_elec') - lp('q_recovered_total'), what='C-1 pump loss')
    brayton(case, P, {'he': lp('q_ihx'), 'pbli': D(0), 'divertor': D(0)})
    for b in ('pbli', 'divertor'):
        check(o(P + f'heat_exchangers__evaluate__{b}_transferred') == 0 and o(P + f'heat_exchangers__evaluate__{b}_state_defined') == 0, f'C-1 idle {b} stage transfers nothing')
    g = case.gate(P, 'checks__loop_capacity_ok')
    check(g['status'] == ('satisfied' if lp('mdot_loop') <= D(i(P + 'primary_loop__mdot_loop_rated')) else 'violated'), 'C-1 loop_capacity status')
    margins = {}
    for part, demand in (('compressor_capacity', o(P + 'electrical__evaluate__compressor_demand')), ('turbine_capacity', o(P + 'turbine__evaluate__shaft_produced')),
                         ('generator_capacity', o(P + 'electrical__evaluate__gross_electric')), ('rejection_capacity', o(P + 'rejection_capacity__rejected_heat__rejected_heat')),
                         ('he_capacity', lp('q_ihx'))):
        margins[part] = screen(case, P, part, demand)
    check(case.gates(P) == EXPECTED_GATES[P], f'C-1 gates {sorted(case.gates(P) ^ EXPECTED_GATES[P])}')
    return dict(cycle_flow=i(P + 'cycle__selected_flow'), ratio=i(P + 'compressor_1__selected_ratio'),
                ratings={k: i(P + k + '__selected_rating') for k in ('compressor_capacity', 'turbine_capacity', 'generator_capacity', 'rejection_capacity', 'he_capacity')},
                loop_mdot=float(lp('mdot')), loop_T_out=float(lp('T_out')), q_ihx=float(lp('q_ihx')), loop_p_elec=float(lp('p_elec')), loop_capacity_margin=float(lp('capacity_margin')),
                turbine_temperature=o(P + 'heat_exchangers__evaluate__turbine_temperature'), heater_inlet=o(P + 'heat_exchangers__evaluate__heater_inlet'),
                accepted_heat=o(P + 'heat_exchangers__evaluate__accepted_heat'), unmet_heat=o(P + 'heat_exchangers__evaluate__unmet_heat'),
                he_hot_bound_margin=o(P + 'heat_exchangers__evaluate__he_hot_bound_margin'),
                compressor_demand=o(P + 'electrical__evaluate__compressor_demand'), turbine_shaft=o(P + 'turbine__evaluate__shaft_produced'),
                gross_electric=o(P + 'electrical__evaluate__gross_electric'), net_electric=o(P + 'electrical__evaluate__net_electric'),
                rejected_heat=o(P + 'rejection_capacity__rejected_heat__rejected_heat'),
                margins={k: float(v[0]) for k, v in margins.items()}, violated=sorted(k for k, v in margins.items() if v[1] == 'violated') + [g for g in ('checks__heat_removal_ok', 'checks__net_positive', 'checks__loop_capacity_ok') if case.gate(P, g)['status'] == 'violated'])


def verify_c2(case):
    o, i, P = case.o, case.i, C
    p_fus = D(o(P + 'plasma__fusion__p_fus'))
    check(i(P + 'source__producer_mode') == 1 and o(P + 'source__evaluate__selected_mode') == 1, 'C-2 mode 1')
    close(o(P + 'source__evaluate__selected_power'), p_fus, what='C-2 selected power = plasma p_fus')
    fuel = lambda k: D(o(P + 'fuel__evaluate__' + k))
    E_J = D(i(P + 'fuel__reaction_energy_mev')) * D(i(P + 'fuel__mev_joules'))
    close(fuel('burn_rate'), p_fus * D('1e6') / E_J, tol=1e12, what='C-2 burn rate')  # atoms/s at 1e21 scale; 1e12 is 1e-9 relative
    close(fuel('inject_rate'), fuel('burn_rate') / D(i(P + 'fuel__pass_burn_fraction')), tol=1e13, what='C-2 inject rate')
    close(fuel('exhaust_rate'), fuel('inject_rate') - fuel('burn_rate'), tol=1e13, what='C-2 exhaust rate')
    close(fuel('loss_rate'), (1 - D(i(P + 'fuel__exhaust_recovery'))) * fuel('exhaust_rate'), tol=1e11, what='C-2 loss rate')
    close(o(P + 'fuel_inventory__atoms__atoms'), D(i(P + 'fuel_inventory__selected_tritium_kg')) / D(i(P + 'fuel__tritium_atom_kg')), tol=1e16, what='C-2 inventory atoms')
    dep = lambda k: D(o(P + 'deposition__evaluate__' + k))
    close(dep('he_deposition') + dep('pbli_deposition') + dep('divertor_deposition'), dep('nuclear_gain') + p_fus + D(i(P + 'deposition__auxiliary_heat')), what='C-2 deposition partition')
    close(dep('source_residual'), 0, what='C-2 source residual')
    delivered = {}
    for b, recv, exp in (('he', dep('exchange'), D(0)), ('pbli', D(0), dep('exchange')), ('divertor', D(0), D(0))):
        delivered[b] = D(o(P + b + '_coolant__evaluate__delivered_heat'))
        close(delivered[b], dep(b + '_deposition') + recv - exp + dep(b + '_friction'), what='C-2 delivered ' + b)
    close(dep('pump_electric'), sum(D(o(P + b + '_pump__evaluate__electric')) for b in ('he', 'pbli', 'divertor')), what='C-2 pump electric sum')
    brayton(case, P, delivered)
    margins = {}
    for part, demand in (('he_capacity', delivered['he']), ('pbli_capacity', delivered['pbli']), ('divertor_capacity', delivered['divertor']),
                         ('compressor_capacity', o(P + 'electrical__evaluate__compressor_demand')), ('turbine_capacity', o(P + 'turbine__evaluate__shaft_produced')),
                         ('rejection_capacity', o(P + 'rejection_capacity__cycle_rejection__cycle_rejection')), ('generator_capacity', o(P + 'electrical__evaluate__gross_electric')),
                         ('fuel_capacity', fuel('exhaust_rate'))):
        margins[part] = screen(case, P, part, demand)
    for b in ('he', 'pbli', 'divertor'):
        margins[b + '_pump'] = screen(case, P, b + '_pump', o(P + b + '_pump__evaluate__operating_flow'), calc='screen', rating_key='selected_flow_capacity')
    check(case.gates(P) == EXPECTED_GATES[P], f'C-2 gates {sorted(case.gates(P) ^ EXPECTED_GATES[P])}')
    return dict(n_e0=i(P + 'plasma__n_e0'), alpha_n=i(P + 'plasma__alpha_n'), alpha_T=i(P + 'plasma__alpha_T'), cycle_flow=i(P + 'cycle__selected_flow'),
                recuperator_effectiveness=i(P + 'cycle__recuperator_effectiveness'), network_mode=i(P + 'heat_exchangers__network_mode'),
                p_fus=float(p_fus), p_aux_required_published=o(P + 'plasma__sustain__p_aux_required'), assembly_auxiliary_heat=i(P + 'deposition__auxiliary_heat'),
                beta=o(P + 'plasma__beta_calc__beta'), burn_rate=float(fuel('burn_rate')), exhaust_rate=float(fuel('exhaust_rate')),
                delivered={b: float(v) for b, v in delivered.items()},
                turbine_temperature=o(P + 'heat_exchangers__evaluate__turbine_temperature'), accepted_heat=o(P + 'heat_exchangers__evaluate__accepted_heat'),
                unmet_heat=o(P + 'heat_exchangers__evaluate__unmet_heat'), unmet_by_branch={b: o(P + f'heat_exchangers__evaluate__{b}_unmet') for b in ('he', 'pbli', 'divertor')},
                compressor_demand=o(P + 'electrical__evaluate__compressor_demand'), gross_electric=o(P + 'electrical__evaluate__gross_electric'),
                net_electric=o(P + 'electrical__evaluate__net_electric'),
                margins={k: float(v[0]) for k, v in margins.items()}, violated=sorted(k for k, v in margins.items() if v[1] == 'violated') + [g for g in ('checks__heat_removal_ok', 'checks__net_positive') if case.gate(P, g)['status'] == 'violated'])


def verify_c4(case):
    o, i, P = case.o, case.i, F
    rows = {}
    for b in ('he', 'divertor', 'pbli'):
        part = b + '_fit__'
        T2 = D(i(P + part + 'T_hot')) - D(i(P + part + 'dT_approach')) - D('273.15')
        close(o(P + part + 'cycle__T2_C'), T2, what=f'C-4 {b} T2')
        eta = float(i(P + part + 'a_fit')) * math.log(float(T2) + float(i(P + part + 'T_offset_fit'))) - float(i(P + part + 'b_fit')) - float(i(P + part + 'delta_eta'))
        close(o(P + part + 'cycle__eta_fit'), eta, tol=1e-9, what=f'C-4 {b} eta_fit')
        close(o(P + part + 'cycle__eta_th'), D(i(P + part + 'cycle_live')) * D(o(P + part + 'cycle__eta_fit')) + D(i(P + part + 'eta_th_direct')), what=f'C-4 {b} eta_th')
        lo, hi = T2 - D(i(P + part + 'T2_min')), D(i(P + part + 'T2_max')) - T2
        close(o(P + part + 'cycle__domain_product'), lo * hi, what=f'C-4 {b} domain product')
        g = case.gate(P, part + 'domain_ok')
        check(g['status'] == ('satisfied' if lo * hi >= 0 else 'violated'), f'C-4 {b} domain status')
        rows[b] = dict(T_hot=i(P + part + 'T_hot'), T2_C=float(T2), eta_fit=o(P + part + 'cycle__eta_fit'), margin_low=float(lo), margin_high=float(hi), domain_product=float(lo * hi), status=g['status'])
    check(case.gates(P) == EXPECTED_GATES[P], 'C-4 gates')
    return rows


def verify_c5(case):
    o, i, P = case.o, case.i, E
    q = lambda k: D(i(P + 'circulator_equipment__' + k))
    r = q('selected_rating') / q('reference_quantity')
    close(o(P + 'circulator_equipment__purchase__quantity_ratio'), r, tol=1e-12, what='C-5 ratio')
    close(o(P + 'circulator_equipment__purchase__capital'), q('reference_cost') * q('price_factor') * r, tol=1e-3, what='C-5 capital')
    check(o(P + 'circulator_equipment__purchase__extrapolated') == float(r < D('0.5') or r > D('1.5')), 'C-5 extrapolated flag')
    margin, status = screen(case, P, 'circulator_capacity', i(P + 'circulator_capacity__demand'), rating=i(P + 'circulator_equipment__selected_rating'))
    check(case.gates(P) == EXPECTED_GATES[P], 'C-5 gates')
    return dict(selected_rating=i(P + 'circulator_equipment__selected_rating'), demand=i(P + 'circulator_capacity__demand'), quantity_ratio=float(r),
                capital=o(P + 'circulator_equipment__purchase__capital'), extrapolated=o(P + 'circulator_equipment__purchase__extrapolated'), margin=float(margin), status=status)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=RUNS, help='directory of <case>/result.json and summary.json (default: the sealed evidence)')
    parser.add_argument('--out-dir', type=Path, default=EVIDENCE, help='where verification-summary.json and cases-summary.json are written (default: the sealed evidence)')
    args = parser.parse_args()
    runs, out_dir = args.runs, args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    built = json.loads((EVIDENCE / 'build-hashes.json').read_text())['package_tree']
    now = {str(p.relative_to(PACKAGE)): sha(p) for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    check(built == now, 'package tree changed since the build: ' + repr(sorted(k for k in set(built) | set(now) if built.get(k) != now.get(k))[:5]))
    summary = json.loads((runs / 'summary.json').read_text())
    cases = {}
    for entry in summary['cases']:
        name = entry['case']
        row = json.load((runs / name / 'result.json').open())
        record = dict(status=row['status'], assemblies_changed=row['assemblies_changed'], fingerprint=row['fingerprint'])
        if row['status'] != 'evaluated':
            record.update(error=row['error'], refusing_module=row.get('refusing_module'))
            check(bool(row['error']), name + ': refusal carries a message')
            cases[name] = record
            continue
        case = Case(row)
        # "executes" means every numeric output is finite (goal invariant), not only that the pipeline returned.
        nonfinite = [k for k, v in case.out.items() if isinstance(v, (int, float)) and not isinstance(v, bool) and not math.isfinite(v)]
        check(not nonfinite, f'{name}: non-finite outputs {nonfinite[:5]}')
        n = len(case.out['constraint_report']['results'])
        check(n == 25, f'{name}: {n} constraint results, expected 25')
        record['C-1'] = verify_c1(case)
        record['C-2'] = verify_c2(case)
        record['C-4'] = verify_c4(case)
        record['C-5'] = verify_c5(case)
        cases[name] = record
    result = dict(fingerprint=summary['fingerprint'], cases_verified=len(cases), failures=FAILURES, passed=not FAILURES)
    (out_dir / 'verification-summary.json').write_text(json.dumps(result, indent=2) + '\n')
    (out_dir / 'cases-summary.json').write_text(json.dumps(cases, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'failures'}))
    for f in FAILURES:
        print('FAIL', f)
    raise SystemExit(0 if not FAILURES else 1)


if __name__ == '__main__':
    main()
