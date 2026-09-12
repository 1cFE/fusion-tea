"""Auto-generated implementation for Heating_Power_Chain.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_heating_chain.sysml:4

SysML Expressions:
    p_wallplug = 0.0
    eta_source = 1.0
    eta_couple = 1.0
    p_delivered_direct = 0.0
    p_coupled_direct = 0.0
    eta_pin_eff = eta_source * eta_couple
    p_delivered = p_wallplug * eta_source + p_delivered_direct
    p_coupled = p_wallplug * eta_source * eta_couple + p_coupled_direct
    p_wallplug_total = p_wallplug + p_coupled_direct / eta_pin_eff
    
Documentation:
Supplementary-heating power chain (WI-039): installed wall-plug
electrical power -> source output -> power coupled into the plasma.

    p_delivered      = p_wallplug * eta_source + p_delivered_direct
    p_coupled        = p_wallplug * eta_source * eta_couple
                       + p_coupled_direct
    eta_pin_eff      = eta_source * eta_couple
    p_wallplug_total = p_wallplug + p_coupled_direct / eta_pin_eff

Two stages, because the pinned source publishes two and no more:
a per-method source efficiency (wall-plug -> delivered power, before
plasma coupling) and a per-concept coupling efficiency, combined
there as eta_pin = eta_source x eta_couple. There is no transmission
efficiency in the pinned source, so no third stage is modelled --
a stage would need a number no admissible source publishes, and a
missing input is surfaced, never defaulted (WI-039 MR-WI039-2).

p_delivered is the COST driver: the per-MW heating rates are
calibrated to source procurement (ITER gyrotron for ECRH), so the
account follows source-output power, not wall-plug power.
p_coupled is the PHYSICS driver: it enters the thermal sum and is
what a sustained-heating fence compares against the plasma's
requirement. p_wallplug_total is the RECIRCULATING driver.

Dormant-safe (the WI-024 cryoplant pattern): a concept that knows
its heating powers outright binds the direct terms and leaves the
chain unbound; a concept deriving them binds the chain and zeroes
the direct terms. eta_source and eta_couple default to 1.0 (not 0)
so a dormant chain's eta_pin_eff stays defined -- the mode is
selected by the powers, never by an efficiency.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py
*Ref**: defaults.py:102-108 ("Heating wall-plug source efficiency
by method (wall-plug -> delivered power, before plasma
coupling). Combined with a per-concept eta_couple (in the
concept YAML) to form eta_pin = eta_source x eta_couple.");
cas22.py:446-459 (C220104, per-MW cost on delivered power);
physics.py:321-323 (wall-plug heating in the recirculating sum)
*Basis**: two-stage heating conversion chain; concept-agnostic
(MR-3) -- all values bound by instances
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_heating_chain.heating_power_chain import Heating_Power_ChainInput


def run_heating_power_chain(inputs: Heating_Power_ChainInput) -> tuple[float, float, float, float]:
    """Execute Heating_Power_Chain calculation.

Supplementary-heating power chain (WI-039): installed wall-plug
electrical power -> source output -> power coupled into the plasma.

    p_delivered      = p_wallplug * eta_source + p_delivered_direct
    p_coupled        = p_wallplug * eta_source * eta_couple
                       + p_coupled_direct
    eta_pin_eff      = eta_source * eta_couple
    p_wallplug_total = p_wallplug + p_coupled_direct / eta_pin_eff

Two stages, because the pinned source publishes two and no more:
a per-method source efficiency (wall-plug -> delivered power, before
plasma coupling) and a per-concept coupling efficiency, combined
there as eta_pin = eta_source x eta_couple. There is no transmission
efficiency in the pinned source, so no third stage is modelled --
a stage would need a number no admissible source publishes, and a
missing input is surfaced, never defaulted (WI-039 MR-WI039-2).

p_delivered is the COST driver: the per-MW heating rates are
calibrated to source procurement (ITER gyrotron for ECRH), so the
account follows source-output power, not wall-plug power.
p_coupled is the PHYSICS driver: it enters the thermal sum and is
what a sustained-heating fence compares against the plasma's
requirement. p_wallplug_total is the RECIRCULATING driver.

Dormant-safe (the WI-024 cryoplant pattern): a concept that knows
its heating powers outright binds the direct terms and leaves the
chain unbound; a concept deriving them binds the chain and zeroes
the direct terms. eta_source and eta_couple default to 1.0 (not 0)
so a dormant chain's eta_pin_eff stays defined -- the mode is
selected by the powers, never by an efficiency.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py
*Ref**: defaults.py:102-108 ("Heating wall-plug source efficiency
by method (wall-plug -> delivered power, before plasma
coupling). Combined with a per-concept eta_couple (in the
concept YAML) to form eta_pin = eta_source x eta_couple.");
cas22.py:446-459 (C220104, per-MW cost on delivered power);
physics.py:321-323 (wall-plug heating in the recirculating sum)
*Basis**: two-stage heating conversion chain; concept-agnostic
(MR-3) -- all values bound by instances

SysML Source: root-0/analyses/mfe_heating_chain.sysml:4

SysML Expressions:
    p_wallplug = 0.0
    eta_source = 1.0
    eta_couple = 1.0
    p_delivered_direct = 0.0
    p_coupled_direct = 0.0
    eta_pin_eff = eta_source * eta_couple
    p_delivered = p_wallplug * eta_source + p_delivered_direct
    p_coupled = p_wallplug * eta_source * eta_couple + p_coupled_direct
    p_wallplug_total = p_wallplug + p_coupled_direct / eta_pin_eff
    
Documentation:
Supplementary-heating power chain (WI-039): installed wall-plug
electrical power -> source output -> power coupled into the plasma.

    p_delivered      = p_wallplug * eta_source + p_delivered_direct
    p_coupled        = p_wallplug * eta_source * eta_couple
                       + p_coupled_direct
    eta_pin_eff      = eta_source * eta_couple
    p_wallplug_total = p_wallplug + p_coupled_direct / eta_pin_eff

Two stages, because the pinned source publishes two and no more:
a per-method source efficiency (wall-plug -> delivered power, before
plasma coupling) and a per-concept coupling efficiency, combined
there as eta_pin = eta_source x eta_couple. There is no transmission
efficiency in the pinned source, so no third stage is modelled --
a stage would need a number no admissible source publishes, and a
missing input is surfaced, never defaulted (WI-039 MR-WI039-2).

p_delivered is the COST driver: the per-MW heating rates are
calibrated to source procurement (ITER gyrotron for ECRH), so the
account follows source-output power, not wall-plug power.
p_coupled is the PHYSICS driver: it enters the thermal sum and is
what a sustained-heating fence compares against the plasma's
requirement. p_wallplug_total is the RECIRCULATING driver.

Dormant-safe (the WI-024 cryoplant pattern): a concept that knows
its heating powers outright binds the direct terms and leaves the
chain unbound; a concept deriving them binds the chain and zeroes
the direct terms. eta_source and eta_couple default to 1.0 (not 0)
so a dormant chain's eta_pin_eff stays defined -- the mode is
selected by the powers, never by an efficiency.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py
*Ref**: defaults.py:102-108 ("Heating wall-plug source efficiency
by method (wall-plug -> delivered power, before plasma
coupling). Combined with a per-concept eta_couple (in the
concept YAML) to form eta_pin = eta_source x eta_couple.");
cas22.py:446-459 (C220104, per-MW cost on delivered power);
physics.py:321-323 (wall-plug heating in the recirculating sum)
*Basis**: two-stage heating conversion chain; concept-agnostic
(MR-3) -- all values bound by instances

Args:
    inputs: Input parameters validated against Heating_Power_ChainInput schema

Returns:
    tuple[float, ...]: (p_wallplug_total, p_delivered, p_coupled, eta_pin_eff)

Example:
    >>> inputs = Heating_Power_ChainInput(...)
    >>> p_wallplug_total, p_delivered, p_coupled, eta_pin_eff = run_heating_power_chain(inputs)
    """
    eta_pin_eff = (inputs.eta_source * inputs.eta_couple)
    return (
        (inputs.p_wallplug + (inputs.p_coupled_direct / eta_pin_eff)),  # p_wallplug_total
        ((inputs.p_wallplug * inputs.eta_source) + inputs.p_delivered_direct),  # p_delivered
        (((inputs.p_wallplug * inputs.eta_source) * inputs.eta_couple) + inputs.p_coupled_direct),  # p_coupled
        eta_pin_eff,
    )
