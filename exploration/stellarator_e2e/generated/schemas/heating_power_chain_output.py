from pydantic import Field
from simkit.config.schema import MultiOutput

class Heating_Power_ChainOutput(MultiOutput):
    """Multi-output container for Heating_Power_Chain.

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
selected by the powers, never by an efficiency. A dormant concept
must ALSO bind eta_source to its former lumped efficiency: with the
efficiencies left at 1.0, p_wallplug_total = p_coupled_direct /
eta_pin_eff equals its coupled power with no conversion loss (the
WI-039 grader's EI-5; the WI-039 restatement table binds
eta_source = eta_pin_effective for exactly this reason).

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
    """
    p_wallplug_total: float = Field(description="p_wallplug_total output")
    p_delivered: float = Field(description="p_delivered output")
    p_coupled: float = Field(description="p_coupled output")
    eta_pin_eff: float = Field(description="eta_pin_eff output")
