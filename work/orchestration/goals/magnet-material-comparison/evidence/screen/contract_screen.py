"""Coordinator feasibility screen of comparison-contract r1 (NOT the study, NOT independently checked).

Purpose: show reviewers the magnitudes the contract implies. Values carry the unchecked
source interpretations listed in the contract. Run: python3 contract_screen.py
"""
import json, math

# Nb3Sn: Tsui & Hampshire 2012 Table 5c, BEAS II, ITER form, engineering Jc, strains as fractions
NB = dict(p=0.489, q=1.618, C=2.227e10, Ca1=226.93, Ca2=203.86, e0a=0.00187, Bc20=30.28, Tc0=16.02)
D_STRAND = 0.82e-3
A_STRAND = math.pi / 4 * D_STRAND**2  # m^2

def s_strain(e, P=NB):
    esh = P['Ca2'] * P['e0a'] / math.sqrt(P['Ca1']**2 - P['Ca2']**2)
    num = P['Ca1'] * (math.sqrt(esh**2 + P['e0a']**2) - math.sqrt((e - esh)**2 + P['e0a']**2)) - P['Ca2'] * e
    return 1 + num / (1 - P['Ca1'] * P['e0a'])

def ic_strand(B, T, e, P=NB):
    s = s_strain(e, P)
    tc = P['Tc0'] * s ** (1 / 3)
    t = T / tc
    if t >= 1: return 0.0
    bc2 = P['Bc20'] * s * (1 - t**1.52)
    b = B / bc2
    if b >= 1: return 0.0
    jc = P['C'] / B * s * (1 - t**1.52) * (1 - t**2) * b**P['p'] * (1 - b)**P['q']
    return jc * A_STRAND

# REBCO: Molodyk Fig. 1a digitized 20 K shape (rebco note), normalized at 20 T (225 A), anchor 198 A
SHAPE = {8: 2.11, 10: 1.85, 12: 1.61, 15: 1.33, 20: 1.0}
def g_shape(B):
    ks = sorted(SHAPE)
    for a, b in zip(ks, ks[1:]):
        if a <= B <= b:
            la, lb = math.log(a), math.log(b)
            w = (math.log(B) - la) / (lb - la)
            return math.exp((1 - w) * math.log(SHAPE[a]) + w * math.log(SHAPE[b]))
    raise ValueError(B)
A_TAPE = 4e-3 * 56e-6
def ic_tape(B, T, anchor=198.0, tstar=22.0):
    return anchor * g_shape(B) * math.exp(-(T - 20.0) / tstar)

N_TURNS, N_COILS, L_TURN = 308, 48, 321600.0 / (48 * 308)
A_AVAIL = 0.36**2 / 308 * 1e6  # mm^2 per turn

def construction_P(I, B, sc_area_mm2, sc_cu_mm2):
    cable = sc_area_mm2 / 0.8
    cu_extra = max(0.0, I / 100.0 - sc_cu_mm2)
    steel = 9.36 * (I / 1e3) * (B / 12.04)
    return (cable + cu_extra + steel) / (1 - 0.237)

rows = []
for B in [8, 9, 10, 11, 12]:
    I = 50e3 * B / 24.9
    # Nb3Sn: smallest n with n*Ic(B, 6.7 K, -0.3%) >= I
    ic67 = ic_strand(B, 6.7, -0.003)
    n_nb = math.ceil(I / ic67)
    a_nb = n_nb * A_STRAND * 1e6
    gross_nb = construction_P(I, B, a_nb, a_nb / 2)
    # REBCO: smallest n with I <= 0.8 * n * 0.9 * Ic_tape(B, 20 K)
    ic20 = ic_tape(B, 20.0)
    n_re = math.ceil(I / (0.8 * 0.9 * ic20))
    a_re = n_re * A_TAPE * 1e6
    gross_re = construction_P(I, B, a_re, a_re * 10 / 56)
    L = N_TURNS * N_COILS * L_TURN
    rows.append(dict(B_T=B, I_kA=round(I / 1e3, 3),
        nb3sn=dict(ic_strand_6p7K_A=round(ic67, 2), ic_strand_5p2K_A=round(ic_strand(B, 5.2, -0.003), 2), n=n_nb,
                   gross_mm2=round(gross_nb, 1), fit_margin_mm2=round(A_AVAIL - gross_nb, 1), strand_km=round(n_nb * L / 1e3)),
        rebco=dict(ic_tape_20K_A=round(ic20, 2), n=n_re, gross_mm2=round(gross_re, 1),
                   fit_margin_mm2=round(A_AVAIL - gross_re, 1), tape_km=round(n_re * L / 1e3))))

print(json.dumps(dict(note='coordinator screen of contract r1; unchecked inputs; not study evidence',
                      available_mm2_per_turn=round(A_AVAIL, 1), rows=rows), indent=1))
