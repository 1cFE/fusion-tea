"""Grounding probe for goal magnet-coil-realism: a- and R-transects at the current pin, magnet channels.
Oracle-side diagnostic via exploration/stellarator_e2e/studies/oracle_entry.evaluate; never package evidence."""
import sys, json, csv, os
ROOT = '/home/reid/1cfe/fusion-tea'
sys.path.insert(0, f'{ROOT}/exploration/stellarator_e2e/studies')
import oracle_entry as oe
P = 'stellarator_09__stellaris__'
OUT = os.path.dirname(os.path.abspath(__file__))

def point(R, a):
    return {f'{P}plasma__R': R, f'{P}plasma__a': a, f'{P}availability_direct': 0.0}

base = oe.evaluate(point(12.7, 1.3))
keys = sorted(base)
open(f'{OUT}/keys.txt', 'w').write('\n'.join(keys))
kw = ('coil', 'cryo', 'casing', 'structure', 'magnet', 'wind', 'wp_', 'lcoe_calc', 'total_capital', 'p_net', 'rec_frac', 'B_peak', 'W_mag', 'vol_cold', 'p_cryo', 'p_elec', 'geom__V', 'aux_cooling', 'p_fus')
sel = [k for k in keys if any(w in k for w in kw)]
print('BASELINE selected channels:')
for k in sel:
    print(f'  {k[len(P):]:60s} {base[k]}')

# Channels for the transect tables (resolved by substring; first match)
def find(*subs):
    for k in keys:
        kk = k[len(P):]
        if all(s in kk for s in subs):
            return k
    return None
want = {
 'lcoe': find('lcoe_calc__lcoe'), 'total_capital': find('total_capital__total_capital'),
 'p_net': find('pb__p_net'), 'rec_frac': find('pb__rec_frac'), 'p_fus': find('fusion__p_fus'),
 'c_coil': find('coil_length') or find('c_coil'), 'vol_cold': find('vol_cold'),
 'p_cryo': find('cryo_elec__p_elec') or find('p_elec'), 'cryo_cost': find('cryo_cost'),
 'B_peak': find('peak_field_calc__B_peak') or find('B_peak'), 'W_mag': find('W_mag'),
 'm_casing': find('m_casing'), 'structure_cost': find('magnet_structure') or find('structure_cost'),
 'winding_pack_cost': find('winding_pack_cost') or find('wp_cost'), 'material_cost': find('material_cost'),
 'magnet_capital': find('magnet_capital_rollup__capital_cost') or find('magnet_capital'),
}
print('\nRESOLVED:', json.dumps({k: (v[len(P):] if v else None) for k, v in want.items()}, indent=1))

rows = []
def run(tag, R, a):
    try:
        ch = oe.evaluate(point(R, a))
    except Exception as e:
        rows.append({'transect': tag, 'R': R, 'a': a, 'err': f'{type(e).__name__}: {e}'}); return
    r = {'transect': tag, 'R': R, 'a': a, 'err': ''}
    for k, v in want.items():
        r[k] = ch[v] if v else None
    rows.append(r)
for a in [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]:
    run('a@R12.7', 12.7, a)
for R in [11.43, 12.0, 12.7, 13.5, 14.2, 15.0, 15.7]:
    run('R@a1.3', R, 1.3)
for R in [12.7, 14.2, 15.7]:
    run('R@a2.2', R, 2.2)
cols = ['transect', 'R', 'a', 'err'] + list(want)
with open(f'{OUT}/transects.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print('\nTRANSECTS')
print(','.join(cols))
for r in rows:
    print(','.join(str(r.get(c, '')) if not isinstance(r.get(c), float) else f'{r[c]:.6g}' for c in cols))
