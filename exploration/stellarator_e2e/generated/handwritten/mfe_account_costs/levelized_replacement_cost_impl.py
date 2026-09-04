"""Handwritten implementation for Levelized_Replacement_Cost (WI-029, Rung B; WI-041 operand).

AUTO_IMPLEMENTED = False  (hand-written, normative — do not regenerate over
this file; the bridge sets preserve_handwritten=True. When the calc's
interface changes the generator re-stencils it and this body is restored by
hand, as WI-041 did on 2026-09-04.)

SysML Source: models/analyses/mfe_account_costs.sysml ('Levelized Replacement Cost')

Executable semantic (normative, per the calc doc) — CAS72, the levelized
scheduled replacement of the fluence-limited in-vessel accounts:

  q_n               = the wall load handed in                        [MW/m^2]
  core_lifetime_FPY = clip(fluence_limit / max(q_n, 1e-6),
                           0.5, operational_years * availability)   [FPY]
  core_lifetime_cal = core_lifetime_FPY / availability              [cal-yr]
  s                 = (1 + i) ** (-core_lifetime_cal)
  n_rep             = max(0, ceil(operational_years / core_lifetime_cal) - 1)
  pv                = cost_per_event * s * (1 - s ** n_rep) / (1 - s)
  cost              = CRF(i, n) * pv

THE WALL LOAD IS AN INPUT (WI-041): the plant binds the PEAK neutron wall
load ('Neutron Wall Load Peak' = the circular-torus average times a
source-anchored calibration), because the source and its cited method set
in-vessel lifetime by the peak load, not the average (Stellaris Table 6
image: peak DPA 10.7 DPA/FPY -> first-wall lifetime ~4-6 FPY; Lion 2022
line 88). Before WI-041 this function computed its own neutron power,
``p_fus * (1 - ash_frac) / firstwall_area``, i.e. the average; those two
lines are gone and the three inputs with them.

GUARDS ARE CARRIED VERBATIM, not dropped as point-inert no-ops (design MF-1):
the inner ``max(q_n, 1e-6)`` keeps the 1/q_n gradient finite, the ``clip``
floor 0.5 and cap ``n * availability`` stop replacement outside the plant
life, and the outer ``max(0, ...)`` floors the replacement count. All three
are inert at the pinned design point and go live at study-sweep extremes;
dropping one would return a wrong CAS72 silently and discontinuously.
Python has no envelope restriction, so carrying them is free.

``n_rep`` is computed live every run — never frozen as a defaulted input. It
is a step function of the wall-load chain (n/t = 5.79 at the WI-041 baseline
on the peak; it was 4.40 on the average, so the count stepped 4 -> 5).

The oracle mirror in verify_stellaris.py re-derives this identical guarded
chain independently, and run_stellaris_single.py asserts agreement at
rel 1e-9 — including on synthetic inputs where each guard binds.

Source: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
Ref:    economics.py:53-75 (levelized_replacement_cost); model.py:102-111
        (_core_lifetime_fpy — the clip and the inner max); economics.py:6-10 (CRF);
        Stellaris Table 6 image (images/page_020_table_0.png); Lion 2022 line 88
Basis:  Fluence-limited replacement schedule on the peak wall load, discretely
        discounted and annuitized
"""

import math

from stellarator_tea.modules.mfe_account_costs.levelized_replacement_cost import (
    Levelized_Replacement_CostInput,
)

AUTO_IMPLEMENTED = False


def _clip(value: float, lo: float, hi: float) -> float:
    """jnp.clip semantics verbatim: floor first, THEN cap (model.py:102-111).
    Order matters when lo > hi — jnp.clip returns hi, so keep min outermost."""
    return min(max(value, lo), hi)


def levelized_replacement_cost(
    cost_per_event: float,
    q_n: float,
    fluence_limit: float,
    availability: float,
    interest_rate: float,
    operational_years: float,
) -> float:
    """The full guarded CAS72 chain on the wall load handed in. Pure float64;
    no clamping beyond 1cfe's."""
    # GUARD 1 (inner max) + GUARD 2 (clip floor/cap) — model.py:102-111.
    core_lifetime_fpy = _clip(
        fluence_limit / max(q_n, 1e-6),
        0.5,
        operational_years * availability,
    )
    core_lifetime_cal = core_lifetime_fpy / availability

    # Discount factor over one replacement interval (economics.py:53-75).
    s = (1.0 + interest_rate) ** (-core_lifetime_cal)

    # GUARD 3 (outer max) — the final core is never replaced, hence the -1.
    # Float n_rep (not int) so s ** n_rep takes the same libm pow path as 1cfe.
    n_rep = max(0.0, float(math.ceil(operational_years / core_lifetime_cal)) - 1.0)

    pv = cost_per_event * s * (1.0 - s**n_rep) / (1.0 - s)

    # CRF(i, n) — economics.py:6-10.
    disc_pow_n = (1.0 + interest_rate) ** operational_years
    crf = interest_rate * disc_pow_n / (disc_pow_n - 1.0)
    return crf * pv


def run_levelized_replacement_cost(inputs: Levelized_Replacement_CostInput) -> float:
    """Execute Levelized_Replacement_Cost — returns CAS72 [$/yr]."""
    return levelized_replacement_cost(
        cost_per_event=inputs.cost_per_event,
        q_n=inputs.q_n_in,
        fluence_limit=inputs.fluence_limit_in,
        availability=inputs.availability_in,
        interest_rate=inputs.interest_rate,
        operational_years=inputs.operational_years_in,
    )
