"""Magnet_Support_MassModule Module Wrapper

TEAx module for Magnet_Support_Mass calculation.

Total electromagnetic coil-support mass [kg], not a casing split.
*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
*Reference**: Lion2021 Eq56; Lion2023 Eq2.89 and following MJ/tonne text.
*Basis**: [AGENT] adopts later source unit convention for earlier fit;
later fit has different coefficient/exponent. No local stress qualification.
Native domain: finite c_support>=0; zero coefficient returns dormant0;
otherwise finite W_mag>=0, e_support>0 and finite output.
*Last Updated**: 2026-09-15

Inputs:
    - W_mag: W_mag parameter
    - e_support: e_support parameter
    - c_support: c_support parameter

Outputs:
    - m_support: m_support result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:141

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:141

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_support_mass_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Magnet_Support_MassInput(BaseModel):
    """Input model for Magnet_Support_MassModule.

    Attributes:
        W_mag: W_mag input
        e_support: e_support input
        c_support: c_support input
    """
    W_mag: float = Field(..., description="W_mag input")
    e_support: float = Field(..., description="e_support input")
    c_support: float = Field(..., description="c_support input")


class Magnet_Support_MassModule(ModuleBase[Magnet_Support_MassInput, Float]):
    """TEAx module for Magnet_Support_Mass calculation.

Total electromagnetic coil-support mass [kg], not a casing split.
*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
*Reference**: Lion2021 Eq56; Lion2023 Eq2.89 and following MJ/tonne text.
*Basis**: [AGENT] adopts later source unit convention for earlier fit;
later fit has different coefficient/exponent. No local stress qualification.
Native domain: finite c_support>=0; zero coefficient returns dormant0;
otherwise finite W_mag>=0, e_support>0 and finite output.
*Last Updated**: 2026-09-15

Inputs:
    - W_mag: W_mag parameter
    - e_support: e_support parameter
    - c_support: c_support parameter

Outputs:
    - m_support: m_support result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:141

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:141

    Calculation Specification:
        c_support = 0.0
        e_support = 0.78
        m_support = 1000.0 * c_support * (W_mag / 1000000.0) ** e_support
        
Documentation:
Total electromagnetic coil-support mass [kg], not a casing split.
*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
*Reference**: Lion2021 Eq56; Lion2023 Eq2.89 and following MJ/tonne text.
*Basis**: [AGENT] adopts later source unit convention for earlier fit;
later fit has different coefficient/exponent. No local stress qualification.
Native domain: finite c_support>=0; zero coefficient returns dormant0;
otherwise finite W_mag>=0, e_support>0 and finite output.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.magnet_support_mass_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Magnet_Support_MassModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, W_mag: float, e_support: float, c_support: float    ) -> Magnet_Support_MassInput:
        """Validate inputs and fill defaults.

        Args:
            W_mag: W_mag input
            e_support: e_support input
            c_support: c_support input

        Returns:
            Validated input model
        """
        return Magnet_Support_MassInput(W_mag=W_mag, e_support=e_support, c_support=c_support)

    def run(
        self, W_mag: float, e_support: float, c_support: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            W_mag: W_mag input
            e_support: e_support input
            c_support: c_support input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(W_mag, e_support, c_support)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.magnet_support_mass_impl import (
            run_magnet_support_mass,
        )

        # Execute implementation - returns single value
        m_support = run_magnet_support_mass(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(m_support))
