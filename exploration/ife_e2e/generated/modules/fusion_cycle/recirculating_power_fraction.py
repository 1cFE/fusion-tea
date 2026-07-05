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
    - eta: eta parameter
    - gain: gain parameter
    - blanket_multiplier: blanket_multiplier parameter
    - thermal_efficiency: thermal_efficiency parameter

Outputs:
    - f_recirc: f_recirc result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/fusion_cycle.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/fusion_cycle.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/fusion_cycle/recirculating_power_fraction_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float


class Recirculating_Power_FractionInput(BaseModel):
    """Input model for Recirculating_Power_FractionModule.

    Attributes:
        eta: eta input
        gain: gain input
        blanket_multiplier: blanket_multiplier input
        thermal_efficiency: thermal_efficiency input
    """
    eta: float = Field(..., description="eta input")
    gain: float = Field(..., description="gain input")
    blanket_multiplier: float = Field(..., description="blanket_multiplier input")
    thermal_efficiency: float = Field(..., description="thermal_efficiency input")


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
    - eta: eta parameter
    - gain: gain parameter
    - blanket_multiplier: blanket_multiplier parameter
    - thermal_efficiency: thermal_efficiency parameter

Outputs:
    - f_recirc: f_recirc result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/fusion_cycle.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/fusion_cycle.sysml:4

    Calculation Specification:
        fusion_cycle_gain = eta * gain * blanket_multiplier * thermal_efficiency
        f_recirc = LiteralRationalEvaluation() / fusion_cycle_gain
        
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
        self, eta: float, gain: float, blanket_multiplier: float, thermal_efficiency: float    ) -> Recirculating_Power_FractionInput:
        """Validate inputs and fill defaults.

        Args:
            eta: eta input
            gain: gain input
            blanket_multiplier: blanket_multiplier input
            thermal_efficiency: thermal_efficiency input

        Returns:
            Validated input model
        """
        return Recirculating_Power_FractionInput(eta=eta, gain=gain, blanket_multiplier=blanket_multiplier, thermal_efficiency=thermal_efficiency)

    def run(
        self, eta: float, gain: float, blanket_multiplier: float, thermal_efficiency: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            eta: eta input
            gain: gain input
            blanket_multiplier: blanket_multiplier input
            thermal_efficiency: thermal_efficiency input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(eta, gain, blanket_multiplier, thermal_efficiency)

        # Import handwritten implementation
        from ife_tea.handwritten.fusion_cycle.recirculating_power_fraction_impl import (
            run_recirculating_power_fraction,
        )

        # Execute implementation - returns single value
        f_recirc = run_recirculating_power_fraction(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(f_recirc))
