"""Handwritten implementation for Lifecycle_Calendar (WI-046; goal plant-closure round 1).

AUTO_IMPLEMENTED = False  (hand-written, normative -- do not regenerate over
this file; the bridge sets preserve_handwritten=True. When the calc's
interface changes the generator re-stencils it and this body is restored by
hand, as WI-041 did on 2026-09-04.)

SysML Source: models/analyses/mfe_lifecycle.sysml ('Lifecycle Calendar')

Executable semantic (normative, per the calc doc). Two modes, selected by
availability_direct_in:

LIVE (availability_direct_in == 0.0): the deterministic finite-horizon calendar
(research Option B; design D1 the interval walk). Physical life L = fluence /
q_n (q_n == 0 -> infinite). b = 1 - u. From t = 0: an online interval accrues
F += b*dt, T_u += u*dt; when the accumulated life reaches L an outage of length
d starts at t_k; the event is charged at t_k; the clock resets; a replacement is
bought only if t_k + d < N strictly, else production ceases and N - t_k is
terminal downtime. F + T_p + T_u + T_term == N to 1e-12. availability = F/N.
replacement_pv = sum C/(1+i)**t_k; cas72 = CRF(i,N)*pv with CRF = 1/N at i = 0.
coil_life_margin = coil_life - F. dated_energy_ratio: calendar-year bins from
commissioning (design D3). Invalid or non-finite inputs RAISE; no floors.

HELD (0 < availability_direct_in <= 1): the retired 'Levelized Replacement
Cost' physical chain -- levelized_replacement_cost_impl.py:70-101 at the WI-044
pin (WI-029 MF-1 carried 1cfe's three guards verbatim: the inner max(q_n,1e-6),
the clip floor 0.5 / cap N*A in jnp order, the outer max(0, ...); the float
n_rep preserves the existing count; WI-041 made the wall load the PEAK
handed in). availability = A_direct; F = N*A; T_p = 0; T_u = N - N*A
(undifferentiated held downtime, design D2); T_term = 0; physical_life = the
clipped value; coil margin on N*A; dated_energy_ratio = 1.0.

Source: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
Ref:    economics.py:53-75 (levelized_replacement_cost); model.py:102-111
        (_core_lifetime_fpy -- the clip and the inner max); economics.py:6-10 (CRF);
        Stellaris sec. 2.11 pp. 28-29 and Table 6 p. 21 (the renders under
        work/orchestration/goals/plant-closure/evidence/grounding_sources/);
        research 20260907-163520_lifetime-availability-closure-prework.md Option B
Basis:  one clock for damage, dated replacement, availability and CAS72
WI-052 Source: models/library/analyses/mfe_lifecycle.sysml, Lifecycle Calendar.
Ref: work/active/WI-052_mfe-financial-rate-limits/design.md, Numerical method and justification.
Basis: stable CRF and held PV; log1p dated weights with unchanged physical walk
and yearly-bin accumulation. External citations above remain inherited.
Last Updated: 2026-09-12 (native equation and numerical method verification).
"""

import math
from stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.financial_factors import crf as stable_crf, periodic_pv

from stellarator_materials_nb3sn_tea.modules.mfe_lifecycle.lifecycle_calendar import (
    Lifecycle_CalendarInput,
)

AUTO_IMPLEMENTED = False
_EPS = 1e-12


def _crf(i: float, N: float) -> float:
    return stable_crf(i, N)


def _clip(value: float, lo: float, hi: float) -> float:
    """jnp.clip semantics verbatim: floor first, THEN cap (model.py:102-111)."""
    return min(max(value, lo), hi)


def lifecycle_calendar_held(cost_per_event, q_n, fluence_limit, availability,
                            interest_rate, operational_years, coil_life_fpy):
    """Retained periodic timing and clipping; stable equivalent financial factors."""
    core_lifetime_fpy = _clip(fluence_limit / max(q_n, 1e-6), 0.5,
                              operational_years * availability)
    core_lifetime_cal = core_lifetime_fpy / availability
    n_rep = max(0.0, float(math.ceil(operational_years / core_lifetime_cal)) - 1.0)
    pv = periodic_pv(cost_per_event, interest_rate, core_lifetime_cal, n_rep)
    crf = stable_crf(interest_rate, operational_years)
    cost = crf * pv
    F = operational_years * availability
    return dict(
        physical_life_fpy=core_lifetime_fpy, n_replacements=n_rep, productive_fpy=F,
        planned_downtime_yr=0.0, unplanned_downtime_yr=operational_years - F,
        terminal_downtime_yr=0.0, availability=availability, replacement_pv=pv,
        cas72_annual=cost, coil_life_margin_fpy=coil_life_fpy - F,
        dated_energy_ratio=1.0,
        events=[k * core_lifetime_cal for k in range(1, int(n_rep) + 1)],
    )


def _validate_live(q_n, fluence_limit, N, d, u, C, i, coil_life):
    vals = dict(q_n=q_n, fluence_limit=fluence_limit, N=N, d=d, u=u, C=C, i=i,
                coil_life=coil_life)
    for k, v in vals.items():
        if not math.isfinite(v):
            raise ValueError(f"Lifecycle Calendar: non-finite input {k}={v!r}")
    if (N <= 0.0 or fluence_limit <= 0.0 or q_n < 0.0 or d < 0.0 or C < 0.0
            or not (0.0 <= u < 1.0) or i <= -1.0):
        raise ValueError(f"Lifecycle Calendar: input outside domain {vals!r}")


def lifecycle_calendar_live(cost_per_event, q_n, fluence_limit, interest_rate,
                            operational_years, outage_years, unplanned_fraction,
                            coil_life_fpy):
    """The deterministic finite-horizon calendar (the live mode), as an interval walk."""
    N, d, u, C, i = (operational_years, outage_years, unplanned_fraction,
                     cost_per_event, interest_rate)
    _validate_live(q_n, fluence_limit, N, d, u, C, i, coil_life_fpy)
    b = 1.0 - u
    L = math.inf if q_n == 0.0 else fluence_limit / q_n
    t = F = T_p = T_u = T_term = 0.0
    events, segments = [], []
    while t < N:
        run = L / b
        if t + run >= N:
            dt = N - t
            F += b * dt
            T_u += u * dt
            segments.append((t, N))
            t = N
            break
        F += L
        T_u += u * run
        segments.append((t, t + run))
        t += run
        if t + d < N:
            events.append(t)
            T_p += d
            t += d
        else:
            T_term = N - t
            t = N
    pv = math.fsum(C * math.exp(-t_k * math.log1p(i)) for t_k in events)
    A = F / N
    return dict(
        physical_life_fpy=L, n_replacements=float(len(events)), productive_fpy=F,
        planned_downtime_yr=T_p, unplanned_downtime_yr=T_u, terminal_downtime_yr=T_term,
        availability=A, replacement_pv=pv, cas72_annual=_crf(i, N) * pv,
        coil_life_margin_fpy=coil_life_fpy - F,
        dated_energy_ratio=_dated_energy_ratio(segments, b, N, i, F),
        events=events,
    )


def _dated_energy_ratio(segments, b, N, i, F):
    """Design D3: calendar-year bins (y-1, y] from commissioning; E_y = b x online
    time inside year y; PV(E_y) / (E_avg x sum of discounted year lengths)."""
    if F == 0.0:
        raise ValueError("Lifecycle Calendar: zero productive time -- energy undefined")
    n_years = int(math.ceil(N - _EPS))
    E_avg = F / N
    num = den = 0.0
    for y in range(1, n_years + 1):
        y0, y1 = float(y - 1), min(float(y), N)
        online = sum(max(0.0, min(s1, y1) - max(s0, y0)) for s0, s1 in segments)
        disc = math.exp(-y * math.log1p(i))
        num += b * online * disc
        den += E_avg * (y1 - y0) * disc
    return num / den


def lifecycle_calendar(inputs) -> dict:
    """Mode select (design D8): availability_direct_in == 0 -> live; (0, 1] -> held."""
    A_direct = inputs.availability_direct_in
    if not math.isfinite(A_direct) or A_direct < 0.0 or A_direct > 1.0:
        raise ValueError(f"Lifecycle Calendar: availability_direct_in {A_direct!r} outside [0, 1]")
    if A_direct > 0.0:
        return lifecycle_calendar_held(
            cost_per_event=inputs.cost_per_event, q_n=inputs.q_n_in,
            fluence_limit=inputs.fluence_limit_in, availability=A_direct,
            interest_rate=inputs.interest_rate, operational_years=inputs.operational_years_in,
            coil_life_fpy=inputs.coil_life_fpy_in)
    return lifecycle_calendar_live(
        cost_per_event=inputs.cost_per_event, q_n=inputs.q_n_in,
        fluence_limit=inputs.fluence_limit_in, interest_rate=inputs.interest_rate,
        operational_years=inputs.operational_years_in, outage_years=inputs.outage_years_in,
        unplanned_fraction=inputs.unplanned_fraction_in, coil_life_fpy=inputs.coil_life_fpy_in)


def calendar_events(inputs) -> list[float]:
    """Diagnostic (design D6): the event dates; not a channel."""
    return lifecycle_calendar(inputs)["events"]


def run_lifecycle_calendar(inputs: Lifecycle_CalendarInput) -> tuple[
    float, float, float, float, float, float, float, float, float, float, float
]:
    """Execute Lifecycle_Calendar -- returns the eleven outputs in the generated
    caller's unpack order, read from modules/mfe_lifecycle/lifecycle_calendar.py
    at the 2026-09-08 regeneration (NOT the SysML declaration order -- the WI-045
    cycle impl found the same):
      (availability, coil_life_margin_fpy, replacement_pv, planned_downtime_yr,
       terminal_downtime_yr, unplanned_downtime_yr, productive_fpy,
       dated_energy_ratio, cas72_annual, n_replacements, physical_life_fpy)"""
    r = lifecycle_calendar(inputs)
    return (r["availability"], r["coil_life_margin_fpy"], r["replacement_pv"],
            r["planned_downtime_yr"], r["terminal_downtime_yr"], r["unplanned_downtime_yr"],
            r["productive_fpy"], r["dated_energy_ratio"], r["cas72_annual"],
            r["n_replacements"], r["physical_life_fpy"])
