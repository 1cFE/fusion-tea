"""Auto-generated implementation for Fuel_Cycle_Flows.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:4

SysML Expressions:
    s_per_fpy_in = 31536000.0
    E_fus_J = q_eff_in * mev_to_joules_in
    burn_rate = p_fus_in * 1000000.0 / E_fus_J
    inject_rate = burn_rate / burn_fraction_in
    exhaust_rate = inject_rate - burn_rate
    loss_rate = (1.0 - t_recycle_in) * exhaust_rate
    tbr_required = (burn_rate + loss_rate + lambda_T_in * I_total_in + G_stock_in) / (eta_extract_in * burn_rate)
    tbr_margin = tbr_available_in - tbr_required
    burn_kg_per_fpy = burn_rate * m_T_kg_in * s_per_fpy_in
    
Documentation:
Tritium flows of a D-T plant, reduced to conservation (WI-047):

  E_fus_J         = q_eff * mev_to_joules                        [J]
  burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
  inject_rate     = burn_rate / burn_fraction                    [atoms/s]
  exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
  loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
  tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                    / (eta_extract * burn_rate)                  [1]
  tbr_margin      = tbr_available - tbr_required                 [1]
  burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

One D-T reaction burns one tritium atom; the fusion power fixes the burn,
the single-pass burn fraction fixes the circulating stream, and the recovery
of the unburned stream fixes the permanent loss. The required breeding ratio
is the tritium that must be bred per atom burned to replace burn, permanent
loss, decay of the held inventory and any stock growth, divided by the
extraction efficiency from breeder to usable supply. The margin against the
ACHIEVED ratio a concept binds is a reported margin. In the WI-066
stellarator, a separate adequacy calculation compares computed breeding
with this requirement and the retained design floor. Its validity flag
also governs interpretation of this raw margin when transport is undefined.
Recovery remains an explicit conditional scenario, not a measured efficiency.

Inventory is supplied through I_total. WI-069 computes the stellarator stock
through the separate Fuel Inventory calculation; other instances may retain
dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
and flows in the plant (the calendar's productive time); stock decays through
calendar time too -- the two clocks are the lifecycle calc's, not this one's.

This calc computes REQUIRED breeding; achieved neutronics comes through
the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
keeps its own burn correction on the same burn_fraction and the same
recovery number read as a feedstock cost factor; the two calcs read the
same inputs and mean different things, and say so.

Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
58 (startup as a residence-time balance, not computed here), 60 (the
conditional 1.19 finding)
*Basis**: Tritium conservation on the burned, circulating and bred streams
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_reference_tea.modules.mfe_fuel_cycle.fuel_cycle_flows import Fuel_Cycle_FlowsInput


def run_fuel_cycle_flows(inputs: Fuel_Cycle_FlowsInput) -> tuple[float, float, float, float, float, float, float]:
    """Execute Fuel_Cycle_Flows calculation.

Tritium flows of a D-T plant, reduced to conservation (WI-047):

  E_fus_J         = q_eff * mev_to_joules                        [J]
  burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
  inject_rate     = burn_rate / burn_fraction                    [atoms/s]
  exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
  loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
  tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                    / (eta_extract * burn_rate)                  [1]
  tbr_margin      = tbr_available - tbr_required                 [1]
  burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

One D-T reaction burns one tritium atom; the fusion power fixes the burn,
the single-pass burn fraction fixes the circulating stream, and the recovery
of the unburned stream fixes the permanent loss. The required breeding ratio
is the tritium that must be bred per atom burned to replace burn, permanent
loss, decay of the held inventory and any stock growth, divided by the
extraction efficiency from breeder to usable supply. The margin against the
ACHIEVED ratio a concept binds is a reported margin. In the WI-066
stellarator, a separate adequacy calculation compares computed breeding
with this requirement and the retained design floor. Its validity flag
also governs interpretation of this raw margin when transport is undefined.
Recovery remains an explicit conditional scenario, not a measured efficiency.

Inventory is supplied through I_total. WI-069 computes the stellarator stock
through the separate Fuel Inventory calculation; other instances may retain
dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
and flows in the plant (the calendar's productive time); stock decays through
calendar time too -- the two clocks are the lifecycle calc's, not this one's.

This calc computes REQUIRED breeding; achieved neutronics comes through
the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
keeps its own burn correction on the same burn_fraction and the same
recovery number read as a feedstock cost factor; the two calcs read the
same inputs and mean different things, and say so.

Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
58 (startup as a residence-time balance, not computed here), 60 (the
conditional 1.19 finding)
*Basis**: Tritium conservation on the burned, circulating and bred streams

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:4

SysML Expressions:
    s_per_fpy_in = 31536000.0
    E_fus_J = q_eff_in * mev_to_joules_in
    burn_rate = p_fus_in * 1000000.0 / E_fus_J
    inject_rate = burn_rate / burn_fraction_in
    exhaust_rate = inject_rate - burn_rate
    loss_rate = (1.0 - t_recycle_in) * exhaust_rate
    tbr_required = (burn_rate + loss_rate + lambda_T_in * I_total_in + G_stock_in) / (eta_extract_in * burn_rate)
    tbr_margin = tbr_available_in - tbr_required
    burn_kg_per_fpy = burn_rate * m_T_kg_in * s_per_fpy_in
    
Documentation:
Tritium flows of a D-T plant, reduced to conservation (WI-047):

  E_fus_J         = q_eff * mev_to_joules                        [J]
  burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
  inject_rate     = burn_rate / burn_fraction                    [atoms/s]
  exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
  loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
  tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                    / (eta_extract * burn_rate)                  [1]
  tbr_margin      = tbr_available - tbr_required                 [1]
  burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

One D-T reaction burns one tritium atom; the fusion power fixes the burn,
the single-pass burn fraction fixes the circulating stream, and the recovery
of the unburned stream fixes the permanent loss. The required breeding ratio
is the tritium that must be bred per atom burned to replace burn, permanent
loss, decay of the held inventory and any stock growth, divided by the
extraction efficiency from breeder to usable supply. The margin against the
ACHIEVED ratio a concept binds is a reported margin. In the WI-066
stellarator, a separate adequacy calculation compares computed breeding
with this requirement and the retained design floor. Its validity flag
also governs interpretation of this raw margin when transport is undefined.
Recovery remains an explicit conditional scenario, not a measured efficiency.

Inventory is supplied through I_total. WI-069 computes the stellarator stock
through the separate Fuel Inventory calculation; other instances may retain
dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
and flows in the plant (the calendar's productive time); stock decays through
calendar time too -- the two clocks are the lifecycle calc's, not this one's.

This calc computes REQUIRED breeding; achieved neutronics comes through
the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
keeps its own burn correction on the same burn_fraction and the same
recovery number read as a feedstock cost factor; the two calcs read the
same inputs and mean different things, and say so.

Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
58 (startup as a residence-time balance, not computed here), 60 (the
conditional 1.19 finding)
*Basis**: Tritium conservation on the burned, circulating and bred streams

Args:
    inputs: Input parameters validated against Fuel_Cycle_FlowsInput schema

Returns:
    tuple[float, ...]: (burn_kg_per_fpy, inject_rate, burn_rate, tbr_margin, tbr_required, loss_rate, exhaust_rate)

Example:
    >>> inputs = Fuel_Cycle_FlowsInput(...)
    >>> burn_kg_per_fpy, inject_rate, burn_rate, tbr_margin, tbr_required, loss_rate, exhaust_rate = run_fuel_cycle_flows(inputs)
    """
    E_fus_J = (inputs.q_eff_in * inputs.mev_to_joules_in)
    burn_rate = ((inputs.p_fus_in * 1000000.0) / E_fus_J)
    inject_rate = (burn_rate / inputs.burn_fraction_in)
    exhaust_rate = (inject_rate - burn_rate)
    loss_rate = ((1.0 - inputs.t_recycle_in) * exhaust_rate)
    tbr_required = ((((burn_rate + loss_rate) + (inputs.lambda_T_in * inputs.I_total_in)) + inputs.G_stock_in) / (inputs.eta_extract_in * burn_rate))
    return (
        ((burn_rate * inputs.m_T_kg_in) * inputs.s_per_fpy_in),  # burn_kg_per_fpy
        inject_rate,
        burn_rate,
        (inputs.tbr_available_in - tbr_required),  # tbr_margin
        tbr_required,
        loss_rate,
        exhaust_rate,
    )
