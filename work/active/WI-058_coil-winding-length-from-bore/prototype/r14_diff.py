import sys, json
sys.path.insert(0, '/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies')
import oracle_entry as oe, verify_stellaris as vs
P = 'stellarator_09__stellaris__'
A_REF = vs.IN['magnet_a_coil_ref']
def run(R, a, override=None):
    d = {f'{P}plasma__R': R, f'{P}plasma__a': a}
    if override: d.update(override)
    return oe.evaluate(d)
for (R, a) in [(14.0, 1.3), (12.7, 1.3)]:
    old = run(R, a)
    r = old[f'{P}rb__r_coil_centre']; c_new = 25.0 * (r / A_REF)
    new = run(R, a, {f'{P}magnet__coil__k_coil': c_new / R})
    diff = sorted(k[len(P):] for k in old if old[k] != new[k])
    print(f'R={R} a={a}: differing channels {len(diff)} of {len(old)}')
    for k in diff:
        print(f'   {k:58s} {old[P+k]!r:>26} -> {new[P+k]!r} rel {(new[P+k]-old[P+k])/old[P+k] if old[P+k] else float("nan"):+.3e}')
    json.dump(diff, open(f'/tmp/claude-1000/-home-reid-1cfe-fusion-tea/3a754c07-eb6e-407f-8afd-246f4e8140e4/scratchpad/wi058/r14_differing_channels.json', 'w'), indent=1)
