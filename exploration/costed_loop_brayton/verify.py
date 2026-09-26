"""Independent identity checks on the stored WI-094 case results (design section 7), plus the control comparison.

Every identity is a Decimal recomputation from the stored inputs and outputs; no second implementation of any definition
(the package-owned oracle under studies/ is the study verifier's independent re-derivation). Also checks that each case's
constraint report names exactly the assembly's nine checks with statuses consistent with the stored margins, that every
output is finite, that the five control cases match their sealed WI-093 C-1 channels exactly, and that the package tree
is unchanged after the runs.

Run: .codex-test/run python exploration/costed_loop_brayton/verify.py [--runs DIR --out-dir DIR]
"""
import argparse
import json
import math
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'costed_loop_brayton_tea'
EVIDENCE = ROOT / 'work/active/WI-095_loop-return-control/evidence'  # WI-094's receipts stay under its own evidence directory
RUNS = EVIDENCE / 'native_runs'
P = 'costed_loop_brayton__plant__'
D = lambda x: Decimal(str(x))
EXPECTED_GATES = {'compressor_capacity__capacity_ok', 'turbine_capacity__capacity_ok', 'generator_capacity__capacity_ok',
                  'rejection_capacity__capacity_ok', 'he_capacity__capacity_ok', 'fuel_inventory__capacity_ok',
                  'checks__heat_removal_ok', 'checks__net_positive', 'checks__loop_capacity_ok'}
PURCHASES = {'compressor_equipment': 'compressor_capacity__selected_rating', 'turbine_equipment': 'turbine_capacity__selected_rating',
             'generator_equipment': 'generator_capacity__selected_rating', 'heat_rejection_equipment': 'rejection_capacity__selected_rating',
             'he_duty_equipment': 'he_capacity__selected_rating', 'he_hx': 'he_hx__selected_area'}
CONTRIBUTIONS = ('capital', 'om', 'tritium', 'deuterium', 'consumables', 'imports', 'supply', 'replacement', 'other_overhaul', 'terminal', 'salvage')
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
        self.row, self.out, self.inp = row, row['outputs'], row['effective_inputs']

    def o(self, key):
        return self.out[P + key]

    def i(self, key):
        return self.inp[P + key]

    def gate(self, name):
        results = [r for r in self.out['constraint_report']['results'] if r['constraint_id'].startswith(P + name + '__')]
        check(len(results) == 1, f'{name}: {len(results)} constraint results')
        return results[0]


def screen(case, part, demand, calc='evaluate', rating_key='selected_rating'):
    rating = case.i(part + '__' + rating_key)
    margin = case.o(part + '__' + calc + '__margin')
    close(margin, D(rating) - D(demand), tol=max(1e-6, 1e-9 * abs(float(rating))), what=f'{part} margin')
    g = case.gate(part + '__capacity_ok')
    check(g['status'] == ('satisfied' if margin >= 0 else 'violated'), f'{part} status {g["status"]} vs margin {margin}')


def verify_case(name, case):
    c = case
    for key, value in c.out.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            check(math.isfinite(value), f'{name}: nonfinite output {key}')
    found = {'__'.join(r['constraint_id'][len(P):].split('__')[:2]) for r in c.out['constraint_report']['results']}
    check(found == EXPECTED_GATES, f'{name}: constraint set {sorted(found ^ EXPECTED_GATES)}')
    # C-1 identities (WI-093 design section 8)
    q, cp, dT = D(c.i('blanket_source__q_source')), D(c.i('primary_loop__loop_cp')), D(c.i('primary_loop__loop_dT_blanket'))
    close(c.o('primary_loop__evaluate__mdot'), q * D(1e6) / (cp * dT), tol=1e-6, what=f'{name}: loop mdot')
    close(c.o('primary_loop__evaluate__q_ihx'), q + D(c.o('primary_loop__evaluate__w_fluid')), tol=1e-6, what=f'{name}: q_ihx')
    close(c.o('primary_loop__evaluate__capacity_margin'), D(c.i('primary_loop__mdot_loop_rated')) - D(c.o('primary_loop__evaluate__mdot_loop')), tol=1e-9, what=f'{name}: loop margin')
    cyc = D(c.i('cycle__selected_flow')) * D(c.i('cycle__cp')) / D(1e6)
    close(c.o('heat_exchangers__evaluate__accepted_heat'), cyc * (D(c.o('heat_exchangers__evaluate__turbine_temperature')) - D(c.o('heat_exchangers__evaluate__heater_inlet'))), tol=1e-5, what=f'{name}: accepted heat')
    close(c.o('heat_exchangers__evaluate__unmet_heat'), D(c.o('primary_loop__evaluate__q_ihx')) - D(c.o('heat_exchangers__evaluate__accepted_heat')), tol=1e-6, what=f'{name}: unmet')
    comp = sum(D(c.o(f'compressor_{i}__evaluate__shaft_demand')) for i in (1, 2, 3))
    close(c.o('electrical__evaluate__compressor_demand'), comp, tol=1e-6, what=f'{name}: compressor demand')
    shaft = D(c.o('turbine__evaluate__shaft_produced')) - comp
    close(c.o('electrical__evaluate__gross_electric'), D(c.i('electrical__generator_efficiency')) * max(shaft, D(0)), tol=1e-6, what=f'{name}: gross')
    aux = D(c.o('primary_loop__evaluate__p_elec')) + D(c.i('electrical__auxiliary_heat')) / D(c.i('electrical__heating_efficiency')) + D(c.i('electrical__cryo')) \
        + D(c.i('electrical__fuel_base')) + D(c.i('electrical__fuel_coefficient')) * D(c.i('electrical__fuel_exhaust')) + D(c.i('electrical__control')) + D(c.i('electrical__other_electric'))
    close(c.o('electrical__evaluate__net_electric'), D(c.o('electrical__evaluate__gross_electric')) - D(c.o('electrical__evaluate__shaft_import')) - aux, tol=1e-6, what=f'{name}: net')
    rej = -(D(c.o('intercooler_1__evaluate__heat_into_fluid')) + D(c.o('intercooler_2__evaluate__heat_into_fluid')) + D(c.o('precooler__evaluate__heat_into_fluid')))
    close(c.o('rejection_capacity__rejected_heat__rejected_heat'), rej, tol=1e-6, what=f'{name}: rejected heat')
    screen(c, 'compressor_capacity', c.o('electrical__evaluate__compressor_demand'))
    screen(c, 'turbine_capacity', c.o('turbine__evaluate__shaft_produced'))
    screen(c, 'generator_capacity', c.o('electrical__evaluate__gross_electric'))
    screen(c, 'rejection_capacity', c.o('rejection_capacity__rejected_heat__rejected_heat'))
    screen(c, 'he_capacity', c.o('primary_loop__evaluate__q_ihx'))
    screen(c, 'fuel_inventory', c.o('fuel_inventory__annual__required_stock'), calc='screen', rating_key='selected_tritium_kg')
    for gate, ok in (('checks__heat_removal_ok', c.o('heat_exchangers__evaluate__unmet_heat') <= c.i('checks__energy_tolerance')),
                     ('checks__net_positive', c.o('electrical__evaluate__net_electric') > 0),
                     ('checks__loop_capacity_ok', c.o('primary_loop__evaluate__mdot_loop') <= c.i('primary_loop__mdot_loop_rated'))):
        check(c.gate(gate)['status'] == ('satisfied' if ok else 'violated'), f'{name}: {gate}')
    # purchases: capital = reference cost x factor x selected / reference; extrapolated outside [0.5, 1.5]
    total = D(0)
    for part, quantity_key in PURCHASES.items():
        qty, ref_q, ref_c, f = D(c.i(quantity_key)), D(c.i(part + '__reference_quantity')), D(c.i(part + '__reference_cost')), D(c.i(part + '__price_factor'))
        ratio = qty / ref_q
        close(c.o(part + '__purchase__capital'), ref_c * f * ratio, tol=max(1e-3, 1e-9 * float(ref_c)), what=f'{name}: {part} capital')
        close(c.o(part + '__purchase__extrapolated'), 1.0 if (ratio < D('0.5') or ratio > D('1.5')) else 0.0, tol=0, what=f'{name}: {part} extrapolated')
        total += D(c.o(part + '__purchase__capital'))
    total += D(c.o('conversion_services__purchase__cost'))
    close(c.o('conversion_services__purchase__cost'), D(c.i('conversion_services__reference_cost')) * D(c.i('conversion_services__price_factor')) * D(c.i('conversion_services__selected_quantity')), tol=1e-3, what=f'{name}: conversion services')
    close(c.o('priced_equipment__evaluate__total'), total, tol=1e-3, what=f'{name}: priced total')
    close(c.o('rest_of_plant__purchase__cost'), D(c.i('rest_of_plant__reference_cost')) * D(c.i('rest_of_plant__price_factor')), tol=1e-3, what=f'{name}: rest of plant')
    stock = D(c.i('fuel_inventory__selected_tritium_kg')) * D(c.i('fuel_inventory__tritium_price'))
    close(c.o('fuel_inventory__purchase__amount'), stock, tol=1e-3, what=f'{name}: stock')
    direct = D(c.o('rest_of_plant__purchase__cost')) + D(c.o('priced_equipment__evaluate__total')) + stock
    close(c.o('direct_cost__evaluate__total'), direct, tol=1e-3, what=f'{name}: direct')
    indirect = D(c.i('indirect_cost__fraction')) * direct
    close(c.o('indirect_cost__evaluate__cost'), indirect, tol=1e-3, what=f'{name}: indirect')
    contingency = D(c.i('contingency__fraction')) * (direct + indirect)
    close(c.o('contingency__evaluate__cost'), contingency, tol=1e-3, what=f'{name}: contingency')
    owner = D(c.i('owner_commissioning__fraction')) * direct
    close(c.o('owner_commissioning__evaluate__amount'), owner, tol=1e-3, what=f'{name}: owner')
    close(c.o('cost_ledger__evaluate__overnight'), direct + indirect + contingency + owner, tol=1e-2, what=f'{name}: overnight')
    net, avail = D(c.o('electrical__evaluate__net_electric')), D(c.i('cost_schedule__availability'))
    close(c.o('cost_ledger__evaluate__annual_export_mwh'), max(net, D(0)) * D(8760) * avail, tol=1e-3, what=f'{name}: annual export')
    # fuel: burn from the supplied fusion power; annual makeup; tritium cost
    e_fus = D(c.i('fuel__reaction_energy_mev')) * D(c.i('fuel__mev_joules'))
    burn = D(c.i('fusion_source__p_fus')) * D(1e6) / e_fus
    close(c.o('fuel__evaluate__burn_rate'), burn, tol=float(burn) * 1e-9, what=f'{name}: burn rate')
    exhaust = burn / D(c.i('fuel__pass_burn_fraction')) - burn
    close(c.o('fuel__evaluate__exhaust_rate'), exhaust, tol=float(exhaust) * 1e-9, what=f'{name}: exhaust rate')
    makeup = D(c.o('fuel_inventory__annual__annual_burn')) + D(c.o('fuel_inventory__annual__annual_loss')) + D(c.o('fuel_inventory__annual__annual_decay'))
    external = max(makeup - D(c.i('fuel_inventory__annual_recovery_kg')), D(0))
    close(c.o('fuel_inventory__annual__annual_external'), external, tol=1e-9, what=f'{name}: external tritium')
    close(c.o('fuel_inventory__annual__annual_cost'), external * D(c.i('fuel_inventory__tritium_price')), tol=1e-2, what=f'{name}: tritium cost')
    operating = D(c.o('annual_om__evaluate__annual_om')) + D(c.o('fuel_inventory__annual__annual_cost')) + D(c.o('fuel_inventory__deuterium__annual_fuel')) + D(c.i('cost_ledger__consumables')) + D(c.o('cost_ledger__evaluate__annual_import_cost'))
    close(c.o('cost_ledger__evaluate__annual_operating'), operating, tol=1e-2, what=f'{name}: annual operating')
    # replacement schedule
    interval = D(c.i('cost_schedule__replacement_life_fpy')) / avail
    years = D(c.i('cost_schedule__plant_years'))
    count = max(0, math.ceil(years / interval) - 1)
    close(c.o('replacement__evaluate__interval_years'), interval, tol=1e-9, what=f'{name}: replacement interval')
    close(c.o('replacement__evaluate__event_count'), count, tol=0, what=f'{name}: replacement count')
    close(c.o('replacement__evaluate__event_cost'), D(c.i('replacement_scope__selected_event_scope')) * D(c.i('cost_schedule__replacement_factor')), tol=1e-3, what=f'{name}: event cost')
    # LCOE: the eleven contributions sum to lcoe_sum, and lcoe_sum equals the price
    total_lcoe = sum(D(c.o(f'lifecycle_accounts__evaluate__{k}_lcoe')) for k in CONTRIBUTIONS)
    close(c.o('lifecycle_accounts__evaluate__lcoe_sum'), total_lcoe, tol=1e-6, what=f'{name}: contributions sum')
    close(c.o('lifecycle_price__evaluate__lcoe'), c.o('lifecycle_accounts__evaluate__lcoe_sum'), tol=1e-6, what=f'{name}: lcoe equals lcoe_sum')
    close(c.o('lifecycle_accounts__evaluate__annual_energy'), c.o('cost_ledger__evaluate__annual_export_mwh'), tol=1e-3, what=f'{name}: annual energy')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=RUNS)
    parser.add_argument('--out-dir', type=Path, default=EVIDENCE)
    args = parser.parse_args()
    summary = json.loads((args.runs / 'summary.json').read_text())
    verified, refused = [], []
    for entry in summary['cases']:
        row = json.loads((args.runs / entry['case'] / 'result.json').read_text())
        if row['status'] != 'evaluated':
            refused.append(entry['case']); continue
        before = len(FAILURES)
        verify_case(entry['case'], Case(row))
        verified.append({'case': entry['case'], 'failures': FAILURES[before:]})
    controls = summary.get('controls', {})
    EXPECTED_REFUSAL = 'LCOE undefined for nonpositive net electricity'
    for name, comparison in controls.items():
        if 'refused' in comparison:
            # design section 6: the 4,000 kg/s control has negative net, so the lifecycle body refuses it on this package
            check(name == 'c1-flow4000-reselected-ratings' and comparison['refused'] == EXPECTED_REFUSAL,
                  f'control {name}: unexpected refusal {comparison["refused"]!r}')
            continue
        check(comparison['exact'], f'control {name}: {len(comparison["differences"])} C-1 channels or {len(comparison.get("verdict_differences", []))} verdicts differ from the sealed WI-093 receipt')
    import subprocess
    clean = subprocess.run(['git', 'status', '--porcelain', '--', str(PACKAGE.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True).stdout == ''
    check(clean, 'package tree not clean after the runs')
    result = {'fingerprint': summary['fingerprint'], 'verified_cases': len(verified), 'refused_cases': refused, 'controls_exact': {k: (v['exact'] if 'refused' not in v else 'refused: ' + v['refused']) for k, v in controls.items()},
              'package_tree_clean': clean, 'failures': FAILURES, 'passed': not FAILURES}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / 'verification-summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'failures'} | {'n_failures': len(FAILURES)}))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
