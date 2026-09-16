"""All-point comparison and bounded current/inventory/fit interpretation."""
import json
import math
from collections import Counter
from pathlib import Path

H = Path(__file__).resolve().parents[1]
R = H / 'results'
P = 'stellarator_09__stellaris__'
M = 'magnet__'
LIMITS = ['Continuous uniform-field reference-conductor current estimate; construction, orientation and sharing remain conditional.', 'Available cavity is an explicit allocation assumption; pack field/shape effects, casing wall strength and coil-to-coil clearance are not qualified.', 'Existing stress, thermal and support proxies remain; transverse casing changes lack a full mass/thermal response.', 'Tape price and manufacturing proxies omit performance premiums and unpriced manufacturing; no global optimum or global infeasibility claim.']


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (R / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def close(a, b):
    return math.isfinite(a) and math.isfinite(b) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def main():
    rows = read(R / 'native-cases.json')
    byid = {r['proposal_id']: r for r in rows}
    assert len(byid) == len(rows) and rows
    proposals = read(H / 'preparation/proposals.json')
    props = {p['id']: p for p in proposals}
    scan = {r.get('proposal_id', r.get('id')): r for r in read(R / 'oracle-scan.json')['rows']}
    catalog = read(R / 'predicate-catalog.json')
    assert len(catalog) == 20
    defaults = read(H / 'preparation/resolved-defaults.json')
    current = next(cid for cid, e in catalog.items() if e['source_local_identity'] == 'reference_conductor_current_ok')
    fit = next(cid for cid, e in catalog.items() if 'fit' in e['source_local_identity'])
    other = set(catalog) - {current, fit}
    assert len(other) == 18
    aliases = {pid: [p for p in proposals if p['canonical_proposal_id'] == pid] for pid in byid}
    failures, sign_differences = [], []
    scalars = predicates = 0
    max_relative = 0.
    for row in rows:
        expected = scan[row['proposal_id']]
        assert row['inputs'] == expected['point']
        assert set(row['verdicts']) == set(expected['verdicts']) == set(catalog)
        for key, value in expected['channels'].items():
            got = row['outputs'][key]
            scalars += 1
            max_relative = max(max_relative, abs(got-value)/max(abs(got), abs(value), 1e-300))
            if not close(got, value):
                failures.append({'proposal_id': row['proposal_id'], 'channel': key, 'native': got, 'oracle': value})
        for cid, verdict in expected['verdicts'].items():
            predicates += 1
            if row['verdicts'][cid] == verdict:
                continue
            change = {'proposal_id': row['proposal_id'], 'constraint_id': cid, 'native': row['verdicts'][cid], 'oracle': verdict}
            inputs = defaults | row['inputs']
            key = P + M + 'conductor_current__margin_fraction'
            if cid == current and inputs[P+M+'winding_pack__sizing_mode'] == 1 and inputs[P+M+'winding_pack__inventory_multiplier'] == 1 and abs(row['outputs'][key]) <= 1e-12 and abs(expected['channels'][key]) <= 1e-12:
                sign_differences.append(change | {'native_margin': row['outputs'][key], 'oracle_margin': expected['channels'][key], 'interpretation': 'Exact predicate sign disagreement at analytic zero; both exact verdicts retained. No predicate tolerance applied.'})
            else:
                failures.append(change)
    write('oracle-all-points.json', {'outcome': 'fail' if failures else 'exact-boundary-sign-differences' if sign_differences else 'pass', 'cases': len(rows), 'scalar_comparisons': scalars, 'predicate_comparisons': predicates, 'max_relative_deviation': max_relative, 'failures': failures, 'exact_boundary_sign_differences': sign_differences, 'unmapped_native_channels': sorted(set(rows[0]['outputs'])-set(scan[rows[0]['proposal_id']]['channels']))})
    summaries, residuals = {}, []
    for row in rows:
        inputs = defaults | row['inputs']
        def inp(name): return inputs[P+M+name]
        def val(name): return row['outputs'][P+name]
        def magnet(name): return val(M+name)
        sizing = {key: value for key, value in row['outputs'].items() if key.startswith(P+M+'current_sizing__')}
        sizing = {key.split('__')[-1]: value for key, value in sizing.items()}
        actual_tapes = magnet('conductor_current__parallel_tapes_reference')
        actual_area = magnet('wp_sizing__wp_side')**2
        fraction = 1-sum(inp('winding_pack__'+key) for key in ('f_copper','f_solder','f_steel','f_helium'))
        conductor_area = actual_tapes*inp('winding_pack__tape_width')*inp('winding_pack__tape_thickness')/fraction
        multiplier = inp('winding_pack__inventory_multiplier')
        operating = magnet('conductor_current__operating_fraction_reference')
        ground_clearance = inp('winding_pack__ground_insulation')+inp('casing__assembly_clearance')
        max_side = min((inp('coil__coil_t')-2*inp('casing__wall_thickness')-2*ground_clearance)/(1+inp('winding_pack__internal_build_x')), (inp('casing__interior_y')-2*ground_clearance)/(1+inp('winding_pack__internal_build_y')))
        if inp('winding_pack__sizing_mode') == 1:
            residuals.append({'proposal_id': row['proposal_id'], 'inventory_multiplier': multiplier, 'tape_count_relative_residual': actual_tapes/(sizing['required_tapes']*multiplier)-1, 'pack_area_relative_residual': actual_area/(sizing['required_pack_area']*multiplier)-1, 'operating_fraction_relative_residual': operating/(inp('winding_pack__allowable_fraction')/multiplier)-1, 'margin_fraction': magnet('conductor_current__margin_fraction'), 'margin_current_A': magnet('conductor_current__margin_current'), 'native_current_verdict': row['verdicts'][current], 'oracle_current_verdict': scan[row['proposal_id']]['verdicts'][current]})
        quantities = {'actual_field_T': magnet('peak_field_calc__B_peak'), 'actual_reference_tapes': actual_tapes, 'actual_set_effective_tapes': magnet('conductor_current__parallel_tapes_set'), 'selected_pack_area_m2': actual_area, 'actual_conductor_area_m2': conductor_area, 'required_cavity_x_m': magnet('wp_fit__required_x'), 'required_cavity_y_m': magnet('wp_fit__required_y'), 'required_radial_exterior_m': magnet('wp_fit__required_x')+2*inp('casing__wall_thickness'), 'allocated_radial_exterior_m': magnet('wp_fit__exterior_x'), 'independent_radial_allocation_m': inp('coil__coil_t'), 'independent_transverse_cavity_m': inp('casing__interior_y'), 'fit_margin_x_m': magnet('wp_fit__margin_x'), 'fit_margin_y_m': magnet('wp_fit__margin_y'), 'operating_fraction': operating, 'turns': inp('coil__I_coil')/inp('coil__turn_current'), 'square_max_side_m': max_side, 'required_total_performance_multiplier_for_fit': sizing['required_pack_area']*multiplier/max_side**2 if max_side > 0 else None, 'threshold_interpretation': 'Required gain relative to this point performance at fixed field/allocation; not achieved capability. Applies to square shape only.', 'square_threshold_applicable': inp('winding_pack__fit_aspect_ratio') == 1}
        for label, key in {'tape_length_m':'winding_procurement__tape_length', 'conductor_length_m':'winding_procurement__conductor_length', 'tape_procurement_cost':'winding_procurement__tape_cost', 'winding_cost':'winding_procurement__cost', 'winding_fabrication_cost':'winding_procurement__winding_fabrication_cost', 'support_cost':'magnet_structure_cost__cost', 'insulation_stock_cost':'insulation_inventory__stock_cost', 'magnet_cost':'magnet_capital_rollup__capital_cost', 'cold_total_volume_m3':'wp_volume__vol_cold_total', 'cold_winding_volume_m3':'wp_volume__vol_winding_pack', 'stress_Pa':'wp_stress__sigma_wp', 'strain':'cond_strain__eps_cond', 'stored_energy_J':'stored_energy__W_mag', 'support_mass_kg':'support_mass__m_support'}.items():
            quantities[label] = magnet(key)
        required_square_side = math.sqrt(sizing['required_pack_area']*multiplier)
        quantities['current_required_square_side_m'] = required_square_side
        quantities['smallest_square_radial_allocation_at_held_field_m'] = required_square_side*(1+inp('winding_pack__internal_build_x'))+2*ground_clearance+2*inp('casing__wall_thickness')
        quantities['smallest_square_transverse_cavity_at_held_field_m'] = required_square_side*(1+inp('winding_pack__internal_build_y'))+2*ground_clearance
        quantities['required_allocation_interpretation'] = 'Closed-form space required for current-driven inventory at this held field, with stated internal build/insulation/clearance/wall. Changing allocation changes field and requires reevaluation; this is not a feedback-resolved root.'
        quantities['performance_threshold_units'] = 'dimensionless gain; square area m^2, square side and allocations m; relative_default includes material/orientation/retention products relative to unity.'
        quantities['required_total_performance_multiplier_relative_default'] = quantities['required_total_performance_multiplier_for_fit'] * math.prod(inp('winding_pack__'+key) for key in ('material_factor','orientation_factor','cabling_factor','degradation_factor','sharing_factor')) if max_side > 0 else None
        quantities['radial_space_deficit_m'] = max(0., -quantities['fit_margin_x_m'])
        quantities['transverse_space_deficit_m'] = max(0., -quantities['fit_margin_y_m'])
        quantities['refrigeration_MW'] = val('cryoplant__refrigeration_sum__total')
        quantities['selected_field_limit_T'] = inp('winding_pack__B_max')
        quantities['field_signed_deficit_T'] = quantities['actual_field_T']-quantities['selected_field_limit_T']
        quantities['divertor_peak_MW_per_m2'] = val('divertor__divheat__q_target_peak')
        quantities['divertor_limit_MW_per_m2'] = inputs[P+'divertor__q_target_limit']
        quantities['divertor_margin_MW_per_m2'] = quantities['divertor_limit_MW_per_m2']-quantities['divertor_peak_MW_per_m2']
        quantities['loop_required_flow_kg_per_s'] = val('heat_transport__primary_loop__mdot_loop')
        quantities['loop_rated_flow_kg_per_s'] = inputs[P+'heat_transport__mdot_loop_ref']
        quantities['loop_capacity_margin_kg_per_s'] = val('heat_transport__primary_loop__capacity_margin')
        quantities['sustainment_required_coupled_MW'] = val('plasma__sustain__p_aux_required')
        quantities['sustainment_installed_coupled_MW'] = val('heating__heat__p_coupled')
        quantities['sustainment_margin_MW'] = quantities['sustainment_installed_coupled_MW']-quantities['sustainment_required_coupled_MW']
        quantities['burn_signed_auxiliary_requirement_MW'] = quantities['sustainment_required_coupled_MW']
        quantities['wall_peak_MW_per_m2'] = val('blanket__first_wall__wall_peak_calc__wall_load_peak')
        quantities['wall_limit_MW_per_m2'] = inputs[P+'wall_load_limit']
        quantities['wall_margin_MW_per_m2'] = quantities['wall_limit_MW_per_m2']-quantities['wall_peak_MW_per_m2']

        summaries[row['proposal_id']] = {'proposal_id': row['proposal_id'], 'candidate_id': row['candidate_id'], 'inputs': row['inputs'], 'state': row['state'], 'headline': row['headline'], 'lcoe': val('lcoe_calc__lcoe'), 'current_satisfied': row['verdicts'][current]=='satisfied', 'fit_satisfied': row['verdicts'][fit]=='satisfied', 'other18_satisfied': all(row['verdicts'][cid]=='satisfied' for cid in other), 'all20_satisfied': all(v=='satisfied' for v in row['verdicts'].values()), 'violated': [catalog[cid]['source_local_identity'] for cid,v in row['verdicts'].items() if v!='satisfied'], 'sizing': sizing, 'quantities': quantities, 'report_aliases': [p['id'] for p in aliases[row['proposal_id']]]}
    write('sizing-residuals.json', {'scope': 'Analytic internal closure only, not conductor qualification; exact current predicate unchanged.', 'cases': residuals, 'max_absolute_relative_residuals': {key: max((abs(r[key]) for r in residuals), default=0.) for key in ('tape_count_relative_residual','pack_area_relative_residual','operating_fraction_relative_residual')}})
    entering = read(R/'entering-all-points.json')
    comparison = []
    preservation_failures = []
    assert {r['proposal_id'] for r in entering['rows']} == set(byid)
    for old in entering['rows']:
        row = byid[old['proposal_id']]
        mode = (defaults | row['inputs'])[P+M+'winding_pack__sizing_mode']
        entry = {'proposal_id': row['proposal_id'], 'mode': mode, 'entering_point': old['point'], 'entering_outcome': old['outcome'], 'interpretation': 'Matched mode0 preservation' if mode == 0 else 'Mode1 physical consequences against entering mode0 at the same coordinates'}
        if old['outcome'] == 'evaluated':
            changes = {key: {'before':value, 'after':row['outputs'][key], 'delta':row['outputs'][key]-value} for key,value in old['channels'].items() if not close(value,row['outputs'][key])}
            flips = {cid: {'before':value, 'after':row['verdicts'][cid]} for cid,value in old['verdicts'].items() if value != row['verdicts'][cid]}
            entry |= {'scalar_comparisons':len(old['channels']), 'changed_channels':changes, 'predicate_flips':flips}
            if mode == 0 and (changes or flips): preservation_failures.append(entry)
        else:
            entry['error'] = old['error']
            if mode == 0: preservation_failures.append(entry)
        comparison.append(entry)
    write('comparison-entering.json', {'scope':entering['scope'], 'mode0_preservation_outcome':'fail' if preservation_failures else 'pass', 'preservation_failures':preservation_failures, 'cases':comparison})

    def aggregate(ids, *, cohort_cost=False):
        cases = [summaries[k] for k in sorted(set(ids))]
        feasible = [c for c in cases if c['all20_satisfied']]
        cost = {'cheapest_sampled_all20_conditional':min(feasible,key=lambda c:c['lcoe']) if feasible else None, 'cost_interpretation':'Cheapest evaluated all20 pass within this cohort only; historical/enhanced assumptions remain separate, no global optimum.'} if cohort_cost else {}
        return cost | {'unique_cases':len(cases), 'current_passes':sum(c['current_satisfied'] for c in cases), 'fit_passes':sum(c['fit_satisfied'] for c in cases), 'other18_passes':sum(c['other18_satisfied'] for c in cases), 'all20_passes':sum(c['all20_satisfied'] for c in cases), 'violations':dict(Counter(v for c in cases for v in c['violated'])), 'case_ids':[c['proposal_id'] for c in cases]}

    default_ids = set()
    for pid, row in byid.items():
        inp = defaults | row['inputs']
        if inp[P+M+'winding_pack__sizing_mode'] != 1 or inp[P+M+'winding_pack__B_max'] != 24.9: continue
        if any(inp[P+M+'winding_pack__'+k] != 1 for k in ('material_factor','orientation_factor','cabling_factor','degradation_factor','sharing_factor','fit_aspect_ratio')): continue
        if any(p['family'] in ('historical-controls','performance-sensitivity','shape-sensitivity') or p.get('scenario') not in (None,'default') for p in aliases[pid]): continue
        default_ids.add(pid)
    eligible = [summaries[pid] for pid in default_ids if summaries[pid]['all20_satisfied']]
    families = {f:aggregate((p['canonical_proposal_id'] for p in proposals if p['family']==f), cohort_cost=True) for f in sorted({p['family'] for p in proposals})}
    scenarios = {s:aggregate((p['canonical_proposal_id'] for p in proposals if p.get('scenario')==s), cohort_cost=True) for s in sorted({p['scenario'] for p in proposals if p.get('scenario') is not None})}
    stages = {s:aggregate(p['canonical_proposal_id'] for p in proposals if p.get('stage',p['family'])==s) for s in sorted({p.get('stage',p['family']) for p in proposals})}
    pairs = []
    for p in proposals:
        if not p.get('anchor_id'): continue
        a = summaries[props[p['anchor_id']]['canonical_proposal_id']]
        b = summaries[p['canonical_proposal_id']]
        pairs.append({'proposal_id':p['id'], 'anchor_id':p['anchor_id'], 'lcoe_delta':b['lcoe']-a['lcoe'], 'quantity_deltas':{k:b['quantities'][k]-v for k,v in a['quantities'].items() if isinstance(v,(int,float)) and not isinstance(v,bool) and isinstance(b['quantities'][k],(int,float))}, 'before_violated':a['violated'], 'after_violated':b['violated']})
    exact_path = R/'exact-boundary-diagnostic.json'
    exact = read(exact_path) if exact_path.exists() else None
    reference = summaries[props['reference']['canonical_proposal_id']] if 'reference' in props else None
    write('analysis.json', {'scope':'Finite investigated points under declared allocation/performance assumptions; cheapest sampled default feasible point only.', 'limitations':LIMITS, 'unique_cases':len(rows), 'report_rows':len(proposals), 'overall':aggregate(byid), 'default_cases':aggregate(default_ids), 'cheapest_default_all20':min(eligible,key=lambda c:c['lcoe']) if eligible else None, 'families':families, 'scenarios':scenarios, 'stages':stages, 'reference':reference, 'paired_consequences':pairs, 'exact_boundary_diagnostic':exact, 'exact_boundary_interpretation':'Separate multiplier1 diagnostic retains native/oracle signed margins and exact verdicts; excluded from cohort without changing acceptance. Analytic closure is not qualification.', 'cases':list(summaries.values())})
    if sign_differences:
        print('ATTENTION: exact-boundary sign differences retained in oracle-all-points.json:',len(sign_differences))
    assert not failures, 'Native/oracle comparison failures; inspect oracle-all-points.json before release'
    assert not preservation_failures, 'Mode0 entering preservation failed'
    print('All-point analysis:',len(rows),'cases;',scalars,'scalar and',predicates,'predicate comparisons')


if __name__ == '__main__':
    main()
