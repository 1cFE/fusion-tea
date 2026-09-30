"""Coordinator magnitude screen for comparison-contract r2 (NOT the study, NOT independently checked).
Two anchors, calibrated construction P, native C, both margin rules. Run: python3 contract_screen_r2.py"""
import json, math
def s_strain(e, P):
    esh = P['Ca2'] * P['e0a'] / math.sqrt(P['Ca1']**2 - P['Ca2']**2)
    num = P['Ca1'] * (math.sqrt(esh**2 + P['e0a']**2) - math.sqrt((e - esh)**2 + P['e0a']**2)) - P['Ca2'] * e
    return 1 + num / (1 - P['Ca1'] * P['e0a'])

BEAS2 = dict(p=0.489, q=1.618, C=2.227e10, Ca1=226.93, Ca2=203.86, e0a=0.00187, Bc20=30.28, Tc0=16.02)
OST = dict(p=0.746, q=2.335, C=5.421e10, Ca1=79.94, Ca2=45.04, e0a=0.00207, Bc20=32.59, Tc0=16.26)
A_STR = math.pi / 4 * 0.82**2  # mm2
def ic_strand(B, T, e, P):
    s = s_strain(e, P); tc = P['Tc0'] * s ** (1/3); t = T / tc
    if t >= 1: return 0.0
    bc2 = P['Bc20'] * s * (1 - t**1.52); b = B / bc2
    if b >= 1: return 0.0
    return P['C'] / B * s * (1 - t**1.52) * (1 - t**2) * b**P['p'] * (1 - b)**P['q'] * A_STR * 1e-6
SHAPE = {8: 2.11, 10: 1.85, 12: 1.61, 15: 1.33, 20: 1.0}
def g(B):
    ks = sorted(SHAPE)
    for a, b in zip(ks, ks[1:]):
        if a <= B <= b:
            w = (math.log(B) - math.log(a)) / (math.log(b) - math.log(a))
            return math.exp((1-w)*math.log(SHAPE[a]) + w*math.log(SHAPE[b]))
A_TAPE = 0.224
def ic_tape(B, T): return 198.0 * g(B) * math.exp(-(T - 20.0) / 22.0) * 0.90

ANCHORS = {'D': dict(nc=16, N=142, L=55.6, avail=1296*411/142, Iref=104.95e3, Bref=12.04),
           'S': dict(nc=48, N=308, L=21.75, avail=360*360/308, Iref=50e3, Bref=24.9)}

def construct_P(I, B, sc_mm2, sc_cu_mm2, jcu):
    kA = I / 1e3
    cable = sc_mm2 / 0.97 / 0.80
    cu_space = max(0.0, I / jcu - sc_cu_mm2) / 0.90
    steel = 12.66 * kA * (B / 12.04)
    misc = 1.049 * kA
    return (cable + cu_space + steel + misc) / (1 - 0.237)
def construct_C(I, B, sc_mm2):
    kA = I / 1e3
    return sc_mm2 + (2.945 + 1.010 + 0.673) * kA + 3.030 * kA * (B / 24.9)

out = []
for an, A in ANCHORS.items():
    for B in [8, 9, 10, 11, 12, 13]:
        I = A['Iref'] * B / A['Bref']; L = A['nc'] * A['N'] * A['L']
        row = dict(anchor=an, B=B, I_kA=round(I/1e3, 2), avail=round(A['avail'], 1))
        for grade, P in (('BEAS2', BEAS2), ('OST', OST)):
            n = math.ceil(I / ic_strand(B, 6.7, -0.003, P))
            sc = n * A_STR
            row['nb_'+grade] = dict(n=n, fitP=round(A['avail'] - construct_P(I, B, sc, sc/2, 93.4), 1),
                                   fitC=round(A['avail'] - construct_C(I, B, sc), 1), km=round(n*L/1e3))
        n = math.ceil(I / (0.8 * ic_tape(B, 20.7)))
        sc = n * A_TAPE
        row['re'] = dict(n=n, fitP=round(A['avail'] - construct_P(I, B, sc, sc*10/56, 100.0), 1),
                         fitC=round(A['avail'] - construct_C(I, B, sc), 1), km=round(n*L/1e3))
        out.append(row)
print(json.dumps(dict(note='coordinator screen r2; unchecked calibrations; not study evidence', rows=out), indent=1))
