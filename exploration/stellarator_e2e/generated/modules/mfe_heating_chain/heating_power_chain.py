"""Heating_Power_ChainModule Module Wrapper

TEAx module for Heating_Power_Chain calculation.

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

Inputs:
    - p_coupled_direct: p_coupled_direct parameter
    - eta_couple: eta_couple parameter
    - p_delivered_direct: p_delivered_direct parameter
    - eta_source: eta_source parameter
    - p_wallplug: p_wallplug parameter

Outputs:
    - p_wallplug_total: p_wallplug_total result
    - p_delivered: p_delivered result
    - p_coupled: p_coupled result
    - eta_pin_eff: eta_pin_eff result

SysML Source: root-0/analyses/mfe_heating_chain.sysml:4

SysML Source: root-0/analyses/mfe_heating_chain.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_heating_chain/heating_power_chain_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.heating_power_chain_output import Heating_Power_ChainOutput


class Heating_Power_ChainInput(BaseModel):
    """Input model for Heating_Power_ChainModule.

    Attributes:
        p_coupled_direct: p_coupled_direct input
        eta_couple: eta_couple input
        p_delivered_direct: p_delivered_direct input
        eta_source: eta_source input
        p_wallplug: p_wallplug input
    """
    p_coupled_direct: float = Field(..., description="p_coupled_direct input")
    eta_couple: float = Field(..., description="eta_couple input")
    p_delivered_direct: float = Field(..., description="p_delivered_direct input")
    eta_source: float = Field(..., description="eta_source input")
    p_wallplug: float = Field(..., description="p_wallplug input")


class Heating_Power_ChainModule(ModuleBase[Heating_Power_ChainInput, Heating_Power_ChainOutput]):
    """TEAx module for Heating_Power_Chain calculation.

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

Inputs:
    - p_coupled_direct: p_coupled_direct parameter
    - eta_couple: eta_couple parameter
    - p_delivered_direct: p_delivered_direct parameter
    - eta_source: eta_source parameter
    - p_wallplug: p_wallplug parameter

Outputs:
    - p_wallplug_total: p_wallplug_total result
    - p_delivered: p_delivered result
    - p_coupled: p_coupled result
    - eta_pin_eff: eta_pin_eff result

SysML Source: root-0/analyses/mfe_heating_chain.sysml:4

    SysML Source: root-0/analyses/mfe_heating_chain.sysml:4

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_heating_chain.heating_power_chain_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts p_wallplug_total, p_delivered, p_coupled, eta_pin_eff fields to separate channels.
    """

    name: str = "Heating_Power_ChainModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_coupled_direct: float, eta_couple: float, p_delivered_direct: float, eta_source: float, p_wallplug: float    ) -> Heating_Power_ChainInput:
        """Validate inputs and fill defaults.

        Args:
            p_coupled_direct: p_coupled_direct input
            eta_couple: eta_couple input
            p_delivered_direct: p_delivered_direct input
            eta_source: eta_source input
            p_wallplug: p_wallplug input

        Returns:
            Validated input model
        """
        return Heating_Power_ChainInput(p_coupled_direct=p_coupled_direct, eta_couple=eta_couple, p_delivered_direct=p_delivered_direct, eta_source=eta_source, p_wallplug=p_wallplug)

    def run(
        self, p_coupled_direct: float, eta_couple: float, p_delivered_direct: float, eta_source: float, p_wallplug: float    ) -> ModuleResult[Heating_Power_ChainOutput]:
        """Execute calculation.

        Args:
            p_coupled_direct: p_coupled_direct input
            eta_couple: eta_couple input
            p_delivered_direct: p_delivered_direct input
            eta_source: eta_source input
            p_wallplug: p_wallplug input

        Returns:
            Module result with Heating_Power_ChainOutput (p_wallplug_total, p_delivered, p_coupled, eta_pin_eff)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_coupled_direct, eta_couple, p_delivered_direct, eta_source, p_wallplug)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_heating_chain.heating_power_chain_impl import (
            run_heating_power_chain,
        )

        # Execute implementation - returns tuple of values
        p_wallplug_total, p_delivered, p_coupled, eta_pin_eff = run_heating_power_chain(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Heating_Power_ChainOutput(
                p_wallplug_total=p_wallplug_total,
                p_delivered=p_delivered,
                p_coupled=p_coupled,
                eta_pin_eff=eta_pin_eff,
            )
        )
