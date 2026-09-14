"""WI-058 prototype: the bore form c_coil = c_coil_ref * (r_coil_centre / a_coil_ref) evaluated exactly
through the existing oracle by overriding k_coil per point so that k_coil * R == the new c_coil.
Predictions of record for the design point and the off-design points, at the entering pin."""
import sys, json
sys.path.insert(0, '/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies')
import oracle_entry as oe, verify_stellaris as vs
P = 'stellarator_09__stellaris__'
C_REF = 25.0
A_COIL_REF = vs.IN['magnet_a_coil_ref']
K_OLD = vs.IN['magnet_k_coil']
print('a_coil_ref', repr(A_COIL_REF), 'k_coil old', repr(K_OLD), 'k*12.7 ==25.0:', K_OLD * 12.7 == 25.0, repr(K_OLD * 12.7))
print('k_shape = c_ref/(2 pi a_coil_ref) =', repr(C_REF / (2 * 3.141592653589793 * A_COIL_REF)))
def pt(R, a, I=None):
    d = {f'{P}plasma__R': R, f'{P}plasma__a': a, f'{P}availability_direct': 0.0}
    if I is not None: d[f'{P}magnet__coil__I_coil'] = I
    return d
def rcc(a):
    base = oe.evaluate(pt(12.7, a))
    return base[f'{P}rb__r_coil_centre']
def new(R, a, I=None):
    r = rcc(a); c_new = C_REF * (r / A_COIL_REF)
    d = pt(R, a, I); d[f'{P}magnet__coil__k_coil'] = c_new / R
    ch = oe.evaluate(d); return ch, c_new, r
def old(R, a, I=None):
    return oe.evaluate(pt(R, a, I))
KEYS0 = ['lcoe_calc__lcoe', 'total_capital__total_capital', 'pb__p_net', 'pb__rec_frac', 'pb__p_th',
        'magnet__coil_length__c_coil', 'magnet__wp_volume__vol_cold_total', 'magnet__wp_volume__vol_winding_pack',
        'magnet__winding_procurement__conductor_length', 'magnet__winding_procurement__tape_cost',
        'magnet__winding_procurement__winding_fabrication_cost', 'magnet__material_inventory__material_cost',
        'magnet__winding_procurement__cost', 'magnet__winding_pack_cost__cost', 'magnet__magnet_structure_cost__cost',
        'magnet__magnet_capital_rollup__capital_cost', 'cryoplant__cryo_elec__p_elec', 'cryoplant__aux_cooling__cryo_cost',
        'magnet__peak_field_calc__B_peak', 'magnet__wp_stress__sigma_wp', 'magnet__stored_energy__W_mag', 'rb__r_coil_centre']
KEYS = [k for k in KEYS0 if P + k in oe.evaluate(pt(12.7, 1.3))]
print('oracle lacks:', [k for k in KEYS0 if k not in KEYS])
PTS = {'P0_design': (12.7, 1.3), 'P1_a1.4': (12.7, 1.4), 'P2_a2.2': (12.7, 2.2), 'P3_R15.7_a1.3': (15.7, 1.3),
       'P4_R15.7_a2.2': (15.7, 2.2), 'P5_R11.43_a1.3': (11.43, 1.3)}
out = {}
for name, (R, a) in PTS.items():
    o = old(R, a); n, c_new, r = new(R, a)
    row = {'R': R, 'a': a, 'r_coil_centre': r, 'c_coil_new': c_new, 'ratio': r / A_COIL_REF}
    for k in KEYS:
        ko, kn = o[P + k], n[P + k]
        row[k] = {'old': ko, 'new': kn, 'rel': (kn - ko) / ko if ko else None}
    out[name] = row
    print(f'\n== {name} R={R} a={a} r_cc={r!r} c_new={c_new!r} ratio={r / A_COIL_REF!r}')
    for k in KEYS:
        v = row[k]; print(f'  {k[len("magnet__") if k.startswith("magnet__") else 0:]:48s} old={v["old"]:<22.12g} new={v["new"]:<22.12g} rel={v["rel"] if v["rel"] is None else f"{v["rel"]:+.6e}"}')
    if name == 'P0_design':
        same = all(o[k] == n[k] for k in o); print('  P0 every channel identical:', same, '| differing:', [k[len(P):] for k in o if o[k] != n[k]][:5])
json.dump(out, open('/tmp/claude-1000/-home-reid-1cfe-fusion-tea/3a754c07-eb6e-407f-8afd-246f4e8140e4/scratchpad/wi058/proto_results.json', 'w'), indent=1)
