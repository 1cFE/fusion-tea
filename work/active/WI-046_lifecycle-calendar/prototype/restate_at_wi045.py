"""Phase-2 re-run of proto.py at WI-045's package state (2026-09-08): the predictions of record. Identical code; only the output path differs."""
"""WI-046 prototype (2026-09-08): the lifecycle calendar in both modes, pure Python.

Held mode: the retired 'Levelized Replacement Cost' chain carried verbatim
(levelized_replacement_cost_impl.py:70-101), checked with == against the
oracle mirror. Live mode: the deterministic finite-horizon calendar (research
Option B) as an interval walk, checked against the closed form
t_k = k*L/b + (k-1)*d. Synthetic boundary cases from the lifetime report
(lines 100-110). Design point from the entering pin (30abb21b...). Every number
in design.md comes from proto_results.json written here.
Run: uv run python work/active/WI-046_lifecycle-calendar/prototype/proto.py
"""
import json, math, sys
from pathlib import Path
sys.path.insert(0, "exploration/stellarator_e2e")
import verify_stellaris as vs

EPS = 1e-12


def crf(i, N):
    if i == 0.0:
        return 1.0 / N
    p = (1.0 + i) ** N
    return i * p / (p - 1.0)


# ---------------------------------------------------------------- held mode
def held_mode(q_n, fluence_limit, N, C, i, A_direct, coil_life):
    """The periodic chain verbatim (jnp.clip order; float n_rep; same pow path)."""
    core_lifetime_fpy = min(max(fluence_limit / max(q_n, 1e-6), 0.5), N * A_direct)
    core_lifetime_cal = core_lifetime_fpy / A_direct
    s = (1.0 + i) ** (-core_lifetime_cal)
    n_rep = max(0.0, float(math.ceil(N / core_lifetime_cal)) - 1.0)
    pv = C * s * (1.0 - s ** n_rep) / (1.0 - s)
    disc_pow_n = (1.0 + i) ** N
    crf_ = i * disc_pow_n / (disc_pow_n - 1.0)
    cost = crf_ * pv
    F = N * A_direct
    return dict(
        physical_life_fpy=core_lifetime_fpy, n_replacements=n_rep, productive_fpy=F,
        planned_downtime_yr=0.0, unplanned_downtime_yr=N - F, terminal_downtime_yr=0.0,
        availability=A_direct, replacement_pv=pv, cas72_annual=cost,
        coil_life_margin_fpy=coil_life - F, dated_energy_ratio=1.0,
        events=[k * core_lifetime_cal for k in range(1, int(n_rep) + 1)],
    )


# ---------------------------------------------------------------- live mode
def _validate(q_n, fluence_limit, N, d, u, C, i, coil_life):
    vals = dict(q_n=q_n, fluence_limit=fluence_limit, N=N, d=d, u=u, C=C, i=i, coil_life=coil_life)
    for k, v in vals.items():
        if not math.isfinite(v):
            raise ValueError(f"non-finite input {k}={v}")
    if N <= 0 or fluence_limit <= 0 or q_n < 0 or d < 0 or C < 0 or not (0.0 <= u < 1.0) or i <= -1.0:
        raise ValueError(f"input outside domain: {vals}")


def live_mode(q_n, fluence_limit, N, d, u, C, i, coil_life):
    """Interval walk. Productive time accrues at b = 1-u per online calendar year;
    an outage of length d starts when accumulated FPY reaches L; a replacement is
    bought only if restart t+d < N (strict); otherwise production ceases at t and
    the rest is terminal downtime. Segments (start, end, kind) are kept for the
    dated-energy ratio."""
    _validate(q_n, fluence_limit, N, d, u, C, i, coil_life)
    b = 1.0 - u
    L = math.inf if q_n == 0.0 else fluence_limit / q_n
    t, F, Tp, Tu, Tterm = 0.0, 0.0, 0.0, 0.0, 0.0
    events, segments = [], []
    while t < N:
        run = L / b                       # calendar years online until the limit
        if t + run >= N:                  # the horizon ends mid-run
            dt = N - t
            F += b * dt; Tu += u * dt
            segments.append((t, N, "online")); t = N
            break
        # reach the limit
        F += L; Tu += u * run
        segments.append((t, t + run, "online")); t += run
        if t + d < N:                     # restart strictly before the horizon
            events.append(t); Tp += d
            segments.append((t, t + d, "outage")); t += d
        else:                             # cease production; terminal downtime
            Tterm = N - t
            segments.append((t, N, "terminal")); t = N
    pv = sum(C / (1.0 + i) ** tk for tk in events)
    cas72 = crf(i, N) * pv
    A = F / N
    ratio = dated_energy_ratio(segments, b, N, i, F)
    return dict(
        physical_life_fpy=L, n_replacements=float(len(events)), productive_fpy=F,
        planned_downtime_yr=Tp, unplanned_downtime_yr=Tu, terminal_downtime_yr=Tterm,
        availability=A, replacement_pv=pv, cas72_annual=cas72,
        coil_life_margin_fpy=coil_life - F, dated_energy_ratio=ratio,
        events=events, identity_residual=(F + Tp + Tu + Tterm) - N,
    )


def dated_energy_ratio(segments, b, N, i, F):
    """Calendar-year bins from commissioning (year y covers (y-1, y]); the
    production inside year y is b x the online calendar time in it; the ratio is
    PV(E_y) / (E_avg x sum of discount factors), P_net cancelling. 1.0 exactly
    when production is uniform."""
    if F == 0.0:
        return float("nan")
    n_years = int(math.ceil(N - EPS))
    E_avg = F / N
    num, den = 0.0, 0.0
    for y in range(1, n_years + 1):
        y0, y1 = float(y - 1), min(float(y), N)
        online = 0.0
        for s0, s1, kind in segments:
            if kind != "online":
                continue
            lo, hi = max(s0, y0), min(s1, y1)
            if hi > lo:
                online += hi - lo
        E_y = b * online
        disc = (1.0 + i) ** (-y)
        num += E_y * disc
        den += E_avg * (y1 - y0) * disc
    return num / den


def closed_form_events(L, b, d, N):
    """t_k = k L/b + (k-1) d for every k whose restart t_k + d < N."""
    out, k = [], 1
    while True:
        tk = k * L / b + (k - 1) * d
        if tk >= N or tk + d >= N:
            break
        out.append(tk); k += 1
    return out


# ---------------------------------------------------------------- the design point
P = vs.IN
base = vs.compute()
q_peak = base["wall_load_peak"]
C = base["blanket"] + base["divertor"]          # replacement_cost_per_event, n_mod 1
N, i, fl = P["operational_years"], P["discount_rate"], P["fluence_limit"]
coil_life = 10.0
d7 = 7.0 / 12.0
d5 = 5.0 / 12.0

held = held_mode(q_peak, fl, N, C, i, P["availability"], coil_life)
mirror = vs._oracle_levelized_replacement_cost(
    cost_per_event=C, q_n=q_peak, fluence_limit=fl, availability=P["availability"],
    interest_rate=i, operational_years=N)
assert held["cas72_annual"] == mirror == base["cas72_annual"], (held["cas72_annual"], mirror, base["cas72_annual"])

live = {}
for label, d, u in [("7mo_u0", d7, 0.0), ("7mo_u005", d7, 0.05), ("7mo_u010", d7, 0.10),
                    ("5mo_u0", d5, 0.0), ("5mo_u005", d5, 0.05), ("5mo_u010", d5, 0.10),
                    ("10mo_u0", 10.0 / 12.0, 0.0)]:
    r = live_mode(q_peak, fl, N, d, u, C, i, coil_life)
    cf = closed_form_events(r["physical_life_fpy"], 1.0 - u, d, N)
    assert len(cf) == len(r["events"]) and all(abs(a - b_) < 1e-12 for a, b_ in zip(cf, r["events"])), (label, cf, r["events"])
    assert abs(r["identity_residual"]) < 1e-12
    live[label] = r


def with_availability(A):
    saved = P["availability"]; P["availability"] = A
    try:
        return vs.compute()
    finally:
        P["availability"] = saved

# LCOE at the entering pin with only availability moved (the oracle's CAS72 stays
# periodic; the live CAS72 is substituted by hand in the numerator).
lcoe_live = {}
for label, r in live.items():
    o = with_availability(r["availability"])
    annual_om_live = o["annual_om"] - o["cas72_annual"] + r["cas72_annual"]
    lcoe_live[label] = dict(
        lcoe_oracle_availability_only=o["lcoe"],
        lcoe_with_live_cas72=(o["annual_capital"] + annual_om_live) / o["annual_energy_mwh"]
        if "annual_capital" in o else None,
    )

# ---------------------------------------------------------------- synthetic cases
syn = {}
r = live_mode(q_n=1.0, fluence_limit=4.0, N=10.0, d=7 / 12, u=0.0, C=1.0, i=0.0, coil_life=0.0)
syn["L4_d7over12_N10"] = r
assert r["n_replacements"] == 2 and abs(r["events"][0] - 4.0) < EPS and abs(r["events"][1] - (8 + 7 / 12)) < EPS
assert abs(r["planned_downtime_yr"] - 7 / 6) < EPS and abs(r["productive_fpy"] - 53 / 6) < EPS and abs(r["availability"] - 0.883333333333333) < 1e-9
assert abs(r["cas72_annual"] - 2.0 / 10.0) < EPS      # i = 0: direct sum over N
r = live_mode(1.0, 4.0, 8.7, 7 / 12, 0.0, 1.0, 0.0, 0.0)
syn["L4_N8.7"] = r
assert r["n_replacements"] == 1 and abs(r["productive_fpy"] - 8.0) < EPS and abs(r["terminal_downtime_yr"] - (8.7 - (8 + 7 / 12))) < EPS
r = live_mode(1.0, 4.0, 9 + 2 / 12, 7 / 12, 0.0, 1.0, 0.0, 0.0)
syn["L4_N9.1667_equality"] = r
assert r["n_replacements"] == 1, r
r = live_mode(1.0, 4.0, 9 + 2 / 12 + 1e-6, 7 / 12, 0.0, 1.0, 0.0, 0.0)
syn["L4_N9.1667_plus"] = r
assert r["n_replacements"] == 2, r
r = live_mode(0.0, 18.0, 30.0, 7 / 12, 0.05, 1.0, 0.07, 10.0)
syn["q0"] = r
assert r["n_replacements"] == 0 and abs(r["availability"] - 0.95) < EPS and r["planned_downtime_yr"] == 0.0
r = live_mode(q_peak, fl, N, 0.0, 0.0, C, i, coil_life)
syn["no_outage_u0"] = r
assert abs(r["availability"] - 1.0) < EPS and r["cas72_annual"] > 0.0
r = live_mode(q_peak, fl, 3000.0, d7, 0.0, C, i, coil_life)
L = fl / q_peak
syn["long_horizon"] = dict(availability=r["availability"], asymptote=L / (L + d7), n=r["n_replacements"])
assert abs(r["availability"] - L / (L + d7)) < 2e-3
# u perturbation never raises productive FPY
Fs = [live_mode(q_peak, fl, N, d7, u, C, i, coil_life)["productive_fpy"] for u in (0.0, 0.02, 0.05, 0.1, 0.2)]
assert all(a >= b_ for a, b_ in zip(Fs, Fs[1:])), Fs
# held mode on the single runner's three guard cases == mirror
guards = [
    dict(cost_per_event=671_160_000.0, q_n=100.0 * (1.0 - 0.2002275312855518) / 660.0791423448563, fluence_limit=500.0, availability=0.9, interest_rate=0.07, operational_years=30.0),
    dict(cost_per_event=671_160_000.0, q_n=200_000.0 * (1.0 - 0.2002275312855518) / 660.0791423448563, fluence_limit=18.0, availability=0.9, interest_rate=0.07, operational_years=30.0),
    dict(cost_per_event=671_160_000.0, q_n=50.0 * (1.0 - 0.2002275312855518) / 660.0791423448563, fluence_limit=18.0, availability=0.9, interest_rate=0.07, operational_years=5.0),
]
guard_eq = [held_mode(g["q_n"], g["fluence_limit"], g["operational_years"], g["cost_per_event"], g["interest_rate"], g["availability"], 10.0)["cas72_annual"] == vs._oracle_levelized_replacement_cost(**g) for g in guards]
assert all(guard_eq), guard_eq
# a high-wall-load committed point where the count steps (from the minor-radius record)
import csv
steps = []
with open("exploration/stellarator_e2e/studies/20260907-minor-radius/results/points.csv") as f:
    for row in csv.DictReader(f):
        try:
            qp = float(row["wall_load_peak_MW_m2"]) if "wall_load_peak_MW_m2" in row else None
        except ValueError:
            qp = None
        if qp is None:
            break
        steps.append((row.get("case_id"), qp))
hi = None
if steps:
    hi = max(steps, key=lambda t: t[1])
    hi_live = live_mode(hi[1], fl, N, d7, 0.0, C, i, coil_life)
    hi_held = held_mode(hi[1], fl, N, C, i, 0.85, coil_life)
    syn["high_wall_load_point"] = dict(case_id=hi[0], q_peak=hi[1], live_n=hi_live["n_replacements"], live_A=hi_live["availability"], held_n=hi_held["n_replacements"], held_L_cal=hi_held["physical_life_fpy"] / 0.85)

out = dict(
    design_point=dict(q_peak=q_peak, fluence_limit=fl, N=N, i=i, cost_per_event=C, coil_life=coil_life,
                      physical_life_fpy=fl / q_peak, held_L_cal=(fl / q_peak) / 0.85),
    held=held, held_equals_mirror=held["cas72_annual"] == mirror, mirror=mirror, baseline_lcoe=base["lcoe"],
    live=live, lcoe_live=lcoe_live, synthetic=syn,
)
Path("work/active/WI-046_lifecycle-calendar/prototype/proto_results_at_wi045.json").write_text(json.dumps(out, indent=1, default=float))
print("held == mirror:", out["held_equals_mirror"], held["cas72_annual"])
for k, r in live.items():
    print(f"{k:9s} n {int(r['n_replacements'])} A {r['availability']:.6f} F {r['productive_fpy']:.4f} Tp {r['planned_downtime_yr']:.4f} Tterm {r['terminal_downtime_yr']:.4f} PV {r['replacement_pv']/1e6:.3f} CAS72 {r['cas72_annual']/1e6:.4f} ratio {r['dated_energy_ratio']:.6f} coil {r['coil_life_margin_fpy']:.3f} events {[round(e,4) for e in r['events']]}")
for k, r in lcoe_live.items(): print(k, r)
print("synthetic", json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'events'} if isinstance(v, dict) else v for k, v in syn.items()}, indent=0, default=float)[:1500])


# ---------------------------------------------------------------- addendum: exact LCOE with the live CAS72; a stepping point
def lcoe_with_calendar(r):
    o = with_availability(r["availability"])
    E = 8760.0 * o["p_net"] * r["availability"]
    # o["lcoe"] = (annual_capital + annual_om_periodic) / E ; swap the CAS72 term
    return o["lcoe"] + (r["cas72_annual"] - o["cas72_annual"]) / E, o["cas72_annual"], E

lcoe_exact = {}
for label, r in live.items():
    l, cas72_periodic_at_live_A, E = lcoe_with_calendar(r)
    lcoe_exact[label] = dict(lcoe=l, cas72_periodic_at_live_A=cas72_periodic_at_live_A, annual_energy_mwh=E)
out["lcoe_exact"] = lcoe_exact
hi_rows = []
with open("exploration/stellarator_e2e/studies/20260907-minor-radius/results/points.csv") as f:
    rd = csv.DictReader(f)
    qcol = next(c for c in rd.fieldnames if c.startswith("wall_load_peak"))
    for row in rd:
        try:
            hi_rows.append((row["case_id"], float(row[qcol]), row.get("feasible", ""), float(row["lcoe"]) if row.get("lcoe") else None))
        except (ValueError, KeyError):
            pass
hi_rows.sort(key=lambda t: -t[1])
picks = {}
for cid, qp, feas, lc in hi_rows[:1] + [t for t in hi_rows if t[2] in ("True", "1", "true")][:1]:
    lv = live_mode(qp, fl, N, d7, 0.0, C, i, coil_life); hd = held_mode(qp, fl, N, C, i, 0.85, coil_life)
    picks[cid] = dict(q_peak=qp, feasible_flag=feas, committed_lcoe=lc, live_n=lv["n_replacements"], live_A=lv["availability"], live_events=lv["events"], held_n=hd["n_replacements"], held_L_cal=hd["physical_life_fpy"] / 0.85)
out["stepping_points"] = dict(q_column=qcol, picks=picks)
Path("work/active/WI-046_lifecycle-calendar/prototype/proto_results_at_wi045.json").write_text(json.dumps(out, indent=1, default=float))
print("LCOE exact:", json.dumps(lcoe_exact, indent=0)); print("steps:", json.dumps(out["stepping_points"], indent=0, default=float))
