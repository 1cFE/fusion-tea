"""Recirculating_Power_FractionModule Module Wrapper

TEAx module for Recirculating_Power_Fraction calculation.

Computes the recirculating power fraction for an IFE plant.
f_recirc = 1 / (eta * G * M * epsilon)

The recirculating power fraction determines what fraction of
gross electric output must be fed back to the driver. Values
above ~0.25 (fusion cycle gain below ~4) create a sharp knee
in the cost curve.

*Source**: knowledge/sources/energy_from_inertial_fusion/output.md
*Ref**: Components section (fusion cycle gain discussion)
*Basis**: DI-001 — eta*G must exceed ~10 for viability

Inputs:
    - gain_in: gain_in parameter
    - thermal_efficiency_in: thermal_efficiency_in parameter
    - eta: eta parameter
    - blanket_multiplier: blanket_multiplier parameter

Outputs:
    - f_recirc: f_recirc result

SysML Source: root-0/analyses/fusion_cycle.sysml:4

SysML Source: root-0/analyses/fusion_cycle.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/fusion_cycle/recirculating_power_fraction_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float


class Recirculating_Power_FractionInput(BaseModel):
    """Input model for Recirculating_Power_FractionModule.

    Attributes:
        gain_in: gain_in input
        thermal_efficiency_in: thermal_efficiency_in input
        eta: eta input
        blanket_multiplier: blanket_multiplier input
    """
    gain_in: float = Field(..., description="gain_in input")
    thermal_efficiency_in: float = Field(..., description="thermal_efficiency_in input")
    eta: float = Field(..., description="eta input")
    blanket_multiplier: float = Field(..., description="blanket_multiplier input")


class Recirculating_Power_FractionModule(ModuleBase[Recirculating_Power_FractionInput, Float]):
    """TEAx module for Recirculating_Power_Fraction calculation.

Computes the recirculating power fraction for an IFE plant.
f_recirc = 1 / (eta * G * M * epsilon)

The recirculating power fraction determines what fraction of
gross electric output must be fed back to the driver. Values
above ~0.25 (fusion cycle gain below ~4) create a sharp knee
in the cost curve.

*Source**: knowledge/sources/energy_from_inertial_fusion/output.md
*Ref**: Components section (fusion cycle gain discussion)
*Basis**: DI-001 — eta*G must exceed ~10 for viability

Inputs:
    - gain_in: gain_in parameter
    - thermal_efficiency_in: thermal_efficiency_in parameter
    - eta: eta parameter
    - blanket_multiplier: blanket_multiplier parameter

Outputs:
    - f_recirc: f_recirc result

SysML Source: root-0/analyses/fusion_cycle.sysml:4

    SysML Source: root-0/analyses/fusion_cycle.sysml:4

    Calculation Specification:
        fusion_cycle_gain = eta * gain_in * blanket_multiplier * thermal_efficiency_in
        f_recirc = 1.0 / fusion_cycle_gain
        
Documentation:
Computes the recirculating power fraction for an IFE plant.
f_recirc = 1 / (eta * G * M * epsilon)

The recirculating power fraction determines what fraction of
gross electric output must be fed back to the driver. Values
above ~0.25 (fusion cycle gain below ~4) create a sharp knee
in the cost curve.

*Source**: knowledge/sources/energy_from_inertial_fusion/output.md
*Ref**: Components section (fusion cycle gain discussion)
*Basis**: DI-001 — eta*G must exceed ~10 for viability

    IMPLEMENTATION: See ife_tea.handwritten.fusion_cycle.recirculating_power_fraction_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Recirculating_Power_FractionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, gain_in: float, thermal_efficiency_in: float, eta: float, blanket_multiplier: float    ) -> Recirculating_Power_FractionInput:
        """Validate inputs and fill defaults.

        Args:
            gain_in: gain_in input
            thermal_efficiency_in: thermal_efficiency_in input
            eta: eta input
            blanket_multiplier: blanket_multiplier input

        Returns:
            Validated input model
        """
        return Recirculating_Power_FractionInput(gain_in=gain_in, thermal_efficiency_in=thermal_efficiency_in, eta=eta, blanket_multiplier=blanket_multiplier)

    def run(
        self, gain_in: float, thermal_efficiency_in: float, eta: float, blanket_multiplier: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            gain_in: gain_in input
            thermal_efficiency_in: thermal_efficiency_in input
            eta: eta input
            blanket_multiplier: blanket_multiplier input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(gain_in, thermal_efficiency_in, eta, blanket_multiplier)

        # Import handwritten implementation
        from ife_tea.handwritten.fusion_cycle.recirculating_power_fraction_impl import (
            run_recirculating_power_fraction,
        )

        # Execute implementation - returns single value
        f_recirc = run_recirculating_power_fraction(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(f_recirc))
