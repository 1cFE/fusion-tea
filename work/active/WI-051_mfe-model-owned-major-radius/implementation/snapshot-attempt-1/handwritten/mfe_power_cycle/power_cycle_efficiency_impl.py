"""Handwritten implementation for Power_Cycle_Efficiency (WI-045, goal plant-closure; Rung B).

AUTO_IMPLEMENTED = False  (hand-written, normative -- do not regenerate over
this file; the bridge sets preserve_handwritten=True. When the calc's
interface changes the generator re-stencils it and this body is restored by
hand, then the package is regenerated a second time -- WI-041's recipe.)

SysML Source: models/analyses/mfe_power_cycle.sysml ('Power Cycle Efficiency')

Executable semantic (normative, per the calc doc):

  T2_C           = T_hot - dT_approach - 273.15          [C]  physical conversion
  eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta
  eta_th         = cycle_live * eta_fit + eta_th_direct
  margin_low     = T2_C - T2_min
  margin_high    = T2_max - T2_C
  domain_product = margin_low * margin_high

THE FIT IS USED LITERALLY: T_offset_fit is the printed 273 inside the
logarithm (Kovari et al. 2016 Table 4), a fit convention distinct from the
physical 273.15 that converts the loop's kelvin outlet to Celsius. Nothing is
clamped: outside the domain 'Cycle Fit Domain' reads violated on
domain_product and eta_fit is still published; a non-positive logarithm
argument raises (fail closed, never a plausible number).

DORMANCY: cycle_live 0 gives eta_th = 0.0 * eta_fit + eta_th_direct, the
pre-WI-045 held scalar to the bit.

The oracle mirror in verify_stellaris.py re-derives this chain independently
and run_stellaris_single.py asserts agreement at rel 1e-9.

Return-tuple order matches the regenerated caller's unpack
(modules/mfe_power_cycle/power_cycle_efficiency.py):
(margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product) -- read from
the stencil at the 2026-09-08 regeneration (design D13; the WI-042 precedent).
The caller's order is NOT the declaration order; the caller is never edited.

Source: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
Ref:    output.md:355 (Table 4); journal p. 17
Basis:  printed secondary-cycle efficiency correlation on the turbine-inlet temperature
"""

import math

from stellarator_tea.modules.mfe_power_cycle.power_cycle_efficiency import (
    Power_Cycle_EfficiencyInput,
)

AUTO_IMPLEMENTED = False


def power_cycle_efficiency(
    T_hot: float,
    dT_approach: float,
    a_fit: float,
    b_fit: float,
    T_offset_fit: float,
    T2_min: float,
    T2_max: float,
    delta_eta: float,
    cycle_live: float,
    eta_th_direct: float,
) -> tuple[float, float, float, float, float, float]:
    """The fit, its dormant form and its domain margins, in the caller's order.

    Pure float64; no clamping. Returns
    (margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product).
    """
    T2_C = T_hot - dT_approach - 273.15
    eta_fit = a_fit * math.log(T2_C + T_offset_fit) - b_fit - delta_eta
    eta_th = cycle_live * eta_fit + eta_th_direct
    margin_low = T2_C - T2_min
    margin_high = T2_max - T2_C
    domain_product = margin_low * margin_high
    return (margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product)


def run_power_cycle_efficiency(inputs: Power_Cycle_EfficiencyInput) -> tuple[float, float, float, float, float, float]:
    """Execute Power_Cycle_Efficiency -- returns
    (margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product)."""
    return power_cycle_efficiency(
        T_hot=inputs.T_hot_in,
        dT_approach=inputs.dT_approach_in,
        a_fit=inputs.a_fit_in,
        b_fit=inputs.b_fit_in,
        T_offset_fit=inputs.T_offset_fit_in,
        T2_min=inputs.T2_min_in,
        T2_max=inputs.T2_max_in,
        delta_eta=inputs.delta_eta_in,
        cycle_live=inputs.cycle_live_in,
        eta_th_direct=inputs.eta_th_direct_in,
    )
