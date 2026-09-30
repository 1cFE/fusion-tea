"""Coordinator: default values for the WI-099 design file (anchor D, 10 T, reference offers, common-P).
Not the study's offer policy (that is the independent oracle author's); these are defaults only.
Run: .codex-test/run python work/active/WI-099_magnet-conductor-alternatives/make_reference_case.py"""
import json, math
from pathlib import Path

WST = dict(p=0.578, q=2.211, C1=20823.0, Ca1=47.52, Ca2=0.0, eps0a=0.00218, Bc20=34.22, Tc0=16.26)  # Breschi 2017 Table III
def s_strain(e, P):
    esh = P['Ca2'] * P['eps0a'] / math.sqrt(P['Ca1']**2 - P['Ca2']**2)
    return 1 + (P['Ca1'] * (math.sqrt(esh**2 + P['eps0a']**2) - math.sqrt((e - esh)**2 + P['eps0a']**2)) - P['Ca2'] * e) / (1 - P['Ca1'] * P['eps0a'])
def ic_strand(B, T, e, P):
    s = s_strain(e, P); t = T / (P['Tc0'] * s ** (1/3)); b = B / (P['Bc20'] * s * (1 - t**1.52))
    return P['C1'] / B * s * (1 - t**1.52) * (1 - t**2) * b**P['p'] * (1 - b)**P['q']
KN = {8: 2.11, 10: 1.85, 12: 1.61, 15: 1.33, 20: 1.0}
def g(B):
    ks = sorted(KN)
    for a, b in zip(ks, ks[1:]):
        if a <= B <= b:
            w = (math.log(B) - math.log(a)) / (math.log(b) - math.log(a))
            return math.exp((1 - w) * math.log(KN[a]) + w * math.log(KN[b]))
up = lambda x: math.ceil(x * 1e6) / 1e6
L0 = 2.45e-8
def k316(T):
    c = [-1.4087, 1.3982, 0.2543, -0.6260, 0.2334, 0.4256, -0.4658, 0.1650, -0.0199]
    x = math.log10(T); return 10 ** sum(ci * x**i for i, ci in enumerate(c))
def K(T, Ts=77.0, n=4000):
    h = (Ts - T) / n; return h * (sum(k316(T + i * h) for i in range(1, n)) + (k316(T) + k316(Ts)) / 2)

B, Bref, Iref = 10.0, 12.04, 104950.0
I = Iref * B / Bref; kA = I / 1e3
duty = dict(coils=16.0, turns=142.0, turn_length=55.6, available_area=1296 * 411 / 142, I_ref=Iref, B_ref=Bref, B_peak=B)
econ = dict(crf=0.08, availability=0.8, electricity_price=60.0, hours=8760.0, usd2015_to_2021=271.0 / 237.0)
common_cold = dict(nuclear_density=35.5, cold_volume=16 * 1.296 * 0.411 * 55.6, radiation_ref=1300.0, conduction_ref=4600.0,
                   T_conduction_ref=4.0, n_leads=4.0, f_lead=1.25, L0=L0, p_joint_ref=256 * 1e-9 * Iref**2, I_joint_ref=Iref,
                   shield_static=1102000.0, load_multiplier=1.0)
refr = dict(eta_mode=0.0, eta_const=0.24, green_a=0.155, green_b=0.23, f_carnot_shield=0.20, capital_mode=0.0,
            green_c=3.1e6, green_d=0.65, T_green=4.5)
inv = dict(element_density=8900.0, rho_cu=8940.0, rho_steel=8000.0, rho_solder=8390.0, price_cu=11.0, price_steel=6.0,
           price_solder=64.44111923663972, manufacturing_per_m=0.0)
RATINGS = [1e3, 1.5e3, 2e3, 3e3, 5e3, 7.5e3, 10e3, 15e3, 20e3, 30e3, 50e3, 75e3]

def construction_P(elem_area, elem_cu):
    return dict(cabling_factor=0.97, cable_void=0.20, cu_space=up(max(0.0, I / 93.4 - elem_cu) / 0.9),
                steel_area=up(12.66 * kA * B / 12.04), misc_area=up(1.1077 * kA), solder_area=0.0, ins_fraction=0.237,
                J_cu_rule=93.4, cu_void=0.10, cu_per_kA_rule=0.0, steel_per_kA_rule=12.66, B_steel_ref=12.04, steel_B_scaling=1.0)

def cold(Ts):
    c = common_cold
    q = (c['nuclear_density'] * c['cold_volume'] + c['radiation_ref'] + c['conduction_ref'] * K(Ts) / K(c['T_conduction_ref'])
         + c['f_lead'] * c['n_leads'] * I * math.sqrt(L0 * (77**2 - Ts**2)) + c['p_joint_ref'] * (I / c['I_joint_ref'])**2)
    return q

nb_n = math.ceil(I / ic_strand(B, 4.5 + 0.7 + 1.5, -0.003, WST))
nb_area = nb_n * math.pi / 4 * 0.82**2
nb = dict(n_elements=float(nb_n), T_supply=4.5, nuclear_rise=0.7, margin_rise=1.5, fraction_rule=0.8, acceptance_rule=0.0,
          strand_diameter=0.00082, strand_copper_fraction=0.5, eps_intrinsic=-0.003, **WST,
          **construction_P(nb_area, nb_area / 2), **inv, element_price_per_m=8.0, **common_cold, **refr)
nb['rating_cold'] = next(r for r in RATINGS if r >= cold(4.5))
ict = 198.0 * g(B) * math.exp(-0.7 / 22.0)
re_n = math.ceil(I / (0.8 * 0.9 * ict))
re_area = re_n * 0.004 * 56e-6 * 1e6
re = dict(n_elements=float(re_n), T_supply=20.0, nuclear_rise=0.7, margin_rise=1.5, fraction_rule=0.8, acceptance_rule=1.0,
          tape_width=0.004, tape_thickness=56e-6, tape_copper_fraction=10 / 56, anchor_ic=198.0, shape_mode=0.0,
          g8=2.11, g10=1.85, g12=1.61, g15=1.33, g20=1.0, alpha=0.6, T_star=22.0, degradation=0.90,
          **construction_P(re_area, re_area * 10 / 56), **inv, element_price_per_m=80.0, **common_cold, **refr)
re['rating_cold'] = next(r for r in RATINGS if r >= cold(20.0))
out = dict(note='WI-099 design defaults: anchor D (EU DEMO TF envelope), 10 T, common-P reference offers; coordinator-computed, '
                'overridden per case by the study. Sources: comparison-contract.md r3.',
           duty=duty, economics=econ, nb3sn=nb, rebco=re,
           diagnostics=dict(turn_current=I, nb3sn_q_cold=cold(4.5), rebco_q_cold=cold(20.0), K45=K(4.5), K20=K(20.0)))
Path(__file__).with_name('reference-case.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out['diagnostics'], indent=1), nb_n, re_n, nb['rating_cold'], re['rating_cold'])
