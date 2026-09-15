"""Post-run analysis: record-local all-point oracle comparison (step 10b), the c_coil / vol_cold identities,
the four comparisons against the deposited befores, per-column a-minima, flips by case id, cryo share.
Reads results/points.csv and preparation/* only; writes results/*.json|csv. Every number in the report traces here."""
import csv, json, math, sys
from pathlib import Path
H = Path(__file__).resolve().parents[1]; R = H / 'results'; PRE = H / 'preparation'
P = 'stellarator_09__stellaris__'
def write(p, d): p.write_text(json.dumps(d, indent=2, allow_nan=False) + '\n')
def fl(x):
    try: return float(x)
    except: return None
def rel(a, b):
    if a is None or b is None: return None
    d = abs(a - b); s = max(abs(a), abs(b))
    return d / s if s > 0 else d
rows = list(csv.DictReader((R / 'points.csv').open()))
params = {}
import glob as _g
for _f in sorted(_g.glob(str(H.parent.parent / 'generated/inputs/*_params.json'))):
    params.update(json.loads(Path(_f).read_text()))
def pv(name):
    for k in (name, P + name):
        if k in params: return params[k]
    raise KeyError(name)
c_coil_ref, a_coil_ref, vol_cold_cryo = pv('magnet__coil__c_coil_ref'), pv('magnet__coil__a_coil_ref'), pv('magnet__vol_cold_cryo')
recirc_thr = pv('recirc_ok__threshold')
VERDICTS = ['beta_ok','burn_hold_ok','cond_strain_ok','cycle_domain_ok','divertor_heat_ok','heating_couple_positive_ok','heating_couple_upper_ok','heating_source_positive_ok','heating_source_upper_ok','loop_capacity_ok','loop_pressure_ok','net_positive','peak_field_ok','recirc_ok','sustainment_ok','tbr_ok','wall_load_ok','wp_stress_ok']
VERDICTS = [v for v in VERDICTS if v in rows[0]]
# ---------- 10b: all-point oracle comparison + identities
scan = json.loads((R / 'oracle-scan.json').read_text())
def pkey(pt): return json.dumps({k: float(v) for k, v in pt.items()}, sort_keys=True)
scan_by = {}
for arm, recs in scan['arms'].items():
    for rec in recs: scan_by[(arm, pkey(rec['point']))] = rec
props = json.loads((PRE / 'proposals.json').read_text())
INPUTS = ['plasma__R', 'plasma__a', 'magnet__coil__I_coil', 'magnet__winding_pack__B_max', 'plasma__n_e0', 'heating__p_wallplug_heat', 'availability_direct']
def row_point(r):
    return {P + k: float(r[k]) for k in INPUTS if r.get(k, '') != ''}
prop_by = {}
for arm, rs in props.items():
    for r in rs: prop_by[(arm, pkey(r['point']))] = r['point']
TOL = 1e-9; ITOL = 1e-12
cmp = {'tolerance_relative': TOL, 'identity_tolerance_relative': ITOL, 'points': 0, 'channels_compared': None, 'max_reldev': 0.0, 'worst': None, 'failures': [], 'identity_failures': [], 'channels_unpublished_by_oracle': []}
chan_cols = [c for c in rows[0] if c not in ('arm_id','column','source_case','candidate_id','full_satisfied','headline') and c not in VERDICTS]
for r in rows:
    pt = prop_by[(r['arm_id'], pkey(row_point(r)))]
    rec = scan_by[(r['arm_id'], pkey(pt))]
    cmp['points'] += 1
    compared = 0
    for c in chan_cols:
        k = P + c; v = fl(r[c])
        if k in rec['channels']:
            d = rel(v, rec['channels'][k]); compared += 1
            if d is not None and d > cmp['max_reldev']: cmp['max_reldev'], cmp['worst'] = d, {'candidate_id': r['candidate_id'], 'channel': c, 'package': v, 'oracle': rec['channels'][k]}
            if d is None or d > TOL: cmp['failures'].append({'candidate_id': r['candidate_id'], 'channel': c, 'package': v, 'oracle': rec['channels'][k], 'reldev': d})
        else:
            if c not in cmp['channels_unpublished_by_oracle']: cmp['channels_unpublished_by_oracle'].append(c)
    cmp['channels_compared'] = compared
    # identities from published channels and package inputs
    rc = fl(r['rb__r_coil_centre']); cc = fl(r['magnet__coil_length__c_coil']); vw = fl(r['magnet__wp_volume__vol_winding_pack']); vc = fl(r['magnet__wp_volume__vol_cold_total'])
    ic = c_coil_ref * rc / a_coil_ref
    if rel(cc, ic) > ITOL: cmp['identity_failures'].append({'candidate_id': r['candidate_id'], 'identity': 'c_coil', 'published': cc, 'expected': ic})
    if rel(vc, vw + vol_cold_cryo) > ITOL: cmp['identity_failures'].append({'candidate_id': r['candidate_id'], 'identity': 'vol_cold_total', 'published': vc, 'expected': vw + vol_cold_cryo})
cmp['outcome'] = 'pass' if not cmp['failures'] and not cmp['identity_failures'] else 'fail'
cmp['package_inputs_used'] = {'c_coil_ref': c_coil_ref, 'a_coil_ref': a_coil_ref, 'vol_cold_cryo': vol_cold_cryo, 'recirc_ok__threshold': recirc_thr}
write(R / 'oracle-all-points.json', cmp)
print('10b all-point oracle:', cmp['outcome'], 'points', cmp['points'], 'channels', cmp['channels_compared'], 'max reldev', cmp['max_reldev'], 'unpublished', cmp['channels_unpublished_by_oracle'])
# ---------- comparisons
MAG = ['lcoe_calc__lcoe','magnet__magnet_capital_rollup__capital_cost','magnet__winding_procurement__cost','magnet__winding_procurement__tape_cost','magnet__winding_procurement__winding_fabrication_cost','magnet__material_inventory__material_cost','magnet__magnet_structure_cost__cost','cryoplant__cryo_elec__p_elec','cryoplant__aux_cooling__cryo_cost','pb__rec_frac','pb__p_net','plasma__fusion__p_fus','magnet__peak_field_calc__B_peak','magnet__stored_energy__W_mag','magnet__casing_mass__m_casing','total_capital__total_capital','magnet__wp_volume__vol_winding_pack','magnet__coil_length__c_coil']
def vset(r): return {v: r[v] for v in VERDICTS}
def feasible(r): return all(r[v] == 'satisfied' for v in VERDICTS)
# (1a) matched window vs committed (package-level, entering pin)
before_mw = {c['source_case']: c for c in json.loads((PRE / 'before-matched-window.json').read_text())['cases']}
mw_rows = []
flips_mw = []
for r in rows:
    if r['arm_id'] != 'arm-matched-window': continue
    b = before_mw[r['source_case']]
    ent = {}
    for c in MAG:
        k = P + c
        if k in b['committed_channels']: ent[c] = {'before': b['committed_channels'][k], 'after': fl(r[c]), 'ratio': (fl(r[c]) / b['committed_channels'][k]) if b['committed_channels'][k] else None}
    ent['c_coil'] = {'before_old_form': b['committed_c_coil_by_old_form'], 'after': fl(r['magnet__coil_length__c_coil'])}
    ent['lcoe'] = {'before': b['committed_lcoe'], 'after': fl(r['lcoe_calc__lcoe']), 'delta': fl(r['lcoe_calc__lcoe']) - b['committed_lcoe']}
    bv = b['committed_verdicts']; av = vset(r)
    fl_ = {v: (bv.get(v), av[v]) for v in VERDICTS if bv.get(v) != av[v]}
    for v, (x, y) in fl_.items():
        op = {'recirc_ok': ('pb__rec_frac', recirc_thr), 'net_positive': ('pb__p_net', 0.0)}.get(v, (None, None))
        flips_mw.append({'source_case': r['source_case'], 'candidate_id': r['candidate_id'], 'verdict': v, 'before': x, 'after': y, 'operand': op[0], 'operand_before': b['committed_channels'].get(P + op[0]) if op[0] else None, 'operand_after': fl(r[op[0]]) if op[0] else None, 'threshold': op[1], 'inputs': b['inputs']})
    mw_rows.append({'source_case': r['source_case'], 'candidate_id': r['candidate_id'], 'inputs': b['inputs'], 'feasible_before_18': all(x == 'satisfied' for x in bv.values()), 'feasible_after_18': feasible(r), 'channels': ent, 'flips': fl_})
write(R / 'comparison-matched-window.json', {'reference': 'preparation/before-matched-window.json (package-level, entering pin 8ff5bb7c…)', 'cases': mw_rows, 'flips': flips_mw, 'feasible_before_18': sum(x['feasible_before_18'] for x in mw_rows), 'feasible_after_18': sum(x['feasible_after_18'] for x in mw_rows), 'lcoe_delta_min': min(x['channels']['lcoe']['delta'] for x in mw_rows), 'lcoe_delta_max': max(x['channels']['lcoe']['delta'] for x in mw_rows)})
print('matched window: flips', len(flips_mw), 'feasible before/after', sum(x['feasible_before_18'] for x in mw_rows), sum(x['feasible_after_18'] for x in mw_rows))
# (1b) transects vs entering-pin oracle (oracle-side)
bo = list(csv.DictReader((PRE / 'before-entering-pin-oracle-transects.csv').open()))
def bkey(arm, col, R_, a_): return (arm, col, round(float(R_), 6), round(float(a_), 6))
bo_by = {bkey(b['arm'], b['column'], b['R'], b['a']): b for b in bo}
tr_rows = []; flips_tr = []
for r in rows:
    if r['arm_id'] == 'arm-matched-window': continue
    pt = prop_by[(r['arm_id'], pkey(row_point(r)))]
    b = bo_by[bkey(r['arm_id'], r['column'], pt[P + 'plasma__R'], pt[P + 'plasma__a'])]
    ent = {}
    for c in MAG:
        if c in b and b[c] not in ('', None):
            ent[c] = {'before_oracle': fl(b[c]), 'after': fl(r[c]), 'ratio': (fl(r[c]) / fl(b[c])) if fl(b[c]) else None}
    ent['c_coil'] = {'before_old_form': fl(b['c_coil_old_form']), 'after': fl(r['magnet__coil_length__c_coil'])}
    # oracle-side before verdicts for the two reachable checks
    bef_rec = fl(b['pb__rec_frac']) <= recirc_thr; bef_net = fl(b['pb__p_net']) > 0
    aft_rec = r['recirc_ok'] == 'satisfied'; aft_net = r['net_positive'] == 'satisfied'
    fl_ = {}
    if bef_rec != aft_rec: fl_['recirc_ok'] = {'before_oracle': bef_rec, 'after': aft_rec, 'rec_frac_before': fl(b['pb__rec_frac']), 'rec_frac_after': fl(r['pb__rec_frac']), 'threshold': recirc_thr}
    if bef_net != aft_net: fl_['net_positive'] = {'before_oracle': bef_net, 'after': aft_net, 'p_net_before': fl(b['pb__p_net']), 'p_net_after': fl(r['pb__p_net'])}
    if fl_: flips_tr.append({'candidate_id': r['candidate_id'], 'arm': r['arm_id'], 'column': r['column'], 'R': pt[P + 'plasma__R'], 'a': pt[P + 'plasma__a'], 'flips': fl_})
    tr_rows.append({'candidate_id': r['candidate_id'], 'arm': r['arm_id'], 'column': r['column'], 'R': pt[P + 'plasma__R'], 'a': pt[P + 'plasma__a'], 'feasible_after_18': feasible(r), 'verdicts_after': vset(r), 'channels': ent})
write(R / 'comparison-transects.json', {'reference': 'preparation/before-entering-pin-oracle-transects.csv (oracle-side diagnostic at the entering pin; NOT package evidence; only recirc_ok and net_positive re-derivable there)', 'points': tr_rows, 'flips': flips_tr})
print('transects: oracle-side flips', len(flips_tr))
# (1c) plant-closure anchors (different package; no attribution)
pc = json.loads((PRE / 'before-plant-closure-anchors.json').read_text())
anchors = {}
for cid, col, a_ in (('20260912-plant-closure:c0113', 'cheap-100', 1.7), ('20260912-plant-closure:c0130', 'cheap-220', 1.7)):
    r = next(x for x in rows if x['arm_id'] == 'arm-a-transect' and x['column'] == col and abs(fl(x['rb__r_coil_centre']) - (a_ + 1.85)) < 1e-9)
    prow = pc['cases'][cid]['row']
    anchors[cid] = {'plant_closure_pin': pc['source_pin_extra'], 'committed_lcoe': pc['cases'][cid]['committed_from_historical_window_summary']['lcoe'], 'committed_lcoe_1cfe': pc['cases'][cid]['committed_from_historical_window_summary']['lcoe_1cfe'], 'committed_full_satisfied': prow.get('full_satisfied'), 'current_candidate_id': r['candidate_id'], 'current_lcoe': fl(r['lcoe_calc__lcoe']), 'current_feasible_18': feasible(r), 'current_verdicts': vset(r), 'entering_pin_oracle_lcoe': fl(bo_by[bkey('arm-a-transect', col, 12.7, a_)]['lcoe_calc__lcoe']), 'note': 'Committed values are at a different package (pre-WI-057/040/038); attribute nothing to WI-058.'}
write(R / 'comparison-plant-closure-anchors.json', anchors)
# (3) a-minima per column
mins = {}
for col in ('design', 'cheap-100', 'cheap-220'):
    pts = [x for x in rows if x['arm_id'] == 'arm-a-transect' and x['column'] == col]
    def a_of(x): return round(fl(x['rb__r_coil_centre']) - 1.85, 6)
    after_all = min(pts, key=lambda x: fl(x['lcoe_calc__lcoe'])); feas = [x for x in pts if feasible(x)]
    before = [b for b in bo if b['arm'] == 'arm-a-transect' and b['column'] == col]
    bmin = min(before, key=lambda b: fl(b['lcoe_calc__lcoe']))
    mins[col] = {'after_min_all_points': {'a': a_of(after_all), 'lcoe': fl(after_all['lcoe_calc__lcoe']), 'feasible_18': feasible(after_all), 'violated': [v for v in VERDICTS if after_all[v] != 'satisfied']}, 'after_feasible_18_points': [a_of(x) for x in feas], 'after_min_feasible_18': ({'a': a_of(min(feas, key=lambda x: fl(x['lcoe_calc__lcoe']))), 'lcoe': fl(min(feas, key=lambda x: fl(x['lcoe_calc__lcoe']))['lcoe_calc__lcoe'])} if feas else None), 'before_oracle_min_all_points': {'a': fl(bmin['a']), 'lcoe': fl(bmin['lcoe_calc__lcoe'])}, 'after_lcoe_by_a': {a_of(x): fl(x['lcoe_calc__lcoe']) for x in pts}, 'before_oracle_lcoe_by_a': {fl(b['a']): fl(b['lcoe_calc__lcoe']) for b in before}}
write(R / 'a-minima.json', mins)
for col, m in mins.items(): print(col, 'before min', m['before_oracle_min_all_points'], 'after min', m['after_min_all_points']['a'], m['after_min_all_points']['lcoe'], 'feasible-18 points', m['after_feasible_18_points'])
# (4) cryo share of recirculating power
def share(r):
    p_th = fl(r['pb__p_th']); rec = fl(r['pb__rec_frac']); pnet = fl(r['pb__p_net']); pc_ = fl(r['cryoplant__cryo_elec__p_elec'])
    gross = pnet / (1 - rec) if rec < 1 else None; recirc = gross * rec if gross else None
    return {'p_cryo_MW': pc_, 'p_gross_MW': gross, 'p_recirc_MW': recirc, 'cryo_share_of_recirc': (pc_ / recirc) if recirc else None}
dp = next(x for x in rows if x['arm_id'] == 'arm-a-transect' and x['column'] == 'design' and abs(fl(x['rb__r_coil_centre']) - 3.15) < 1e-9)
c13 = next(x for x in rows if x['arm_id'] == 'arm-a-transect' and x['column'] == 'cheap-100' and abs(fl(x['rb__r_coil_centre']) - 3.55) < 1e-9)
write(R / 'cryo-share.json', {'design_point': share(dp), 'c0113_coordinates': share(c13), 'derivation': 'p_gross = p_net / (1 - rec_frac); p_recirc = p_gross * rec_frac; share = p_cryo / p_recirc, from the published pb__ channels'})
print('cryo share', share(dp)['cryo_share_of_recirc'], share(c13)['cryo_share_of_recirc'])
# per-axis response summary (R transect invariance of the winding chain)
inv = {}
for col in ('design-a1.3', 'cheap-100-a1.7', 'cheap-220-a1.7'):
    pts = [x for x in rows if x['arm_id'] == 'arm-R-transect' and x['column'] == col]
    vals = {c: sorted({r[c] for r in pts}) for c in ('magnet__coil_length__c_coil', 'magnet__winding_procurement__cost', 'magnet__wp_volume__vol_winding_pack', 'magnet__wp_volume__vol_cold_total')}
    inv[col] = {c: {'distinct_values': len(v), 'value': v[0] if len(v) == 1 else v} for c, v in vals.items()}
    inv[col]['lcoe_by_R'] = {fl(x['plasma__R']): fl(x['lcoe_calc__lcoe']) for x in pts}
    inv[col]['rec_frac_by_R'] = {fl(x['plasma__R']): fl(x['pb__rec_frac']) for x in pts}
    inv[col]['recirc_ok_by_R'] = {fl(x['plasma__R']): x['recirc_ok'] for x in pts}
write(R / 'R-invariance.json', inv)
print('R-transect winding-chain distinct values per column:', {c: {k: v['distinct_values'] for k, v in d.items() if isinstance(v, dict) and 'distinct_values' in v} for c, d in inv.items()})
print('ANALYZE_DONE')
