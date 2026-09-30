"""Operating_Heating_PowerModule Module Wrapper

TEAx module for Operating_Heating_Power calculation.

Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11

Inputs:
    - eta_source_in: eta_source_in parameter
    - p_required_in: p_required_in parameter
    - eta_couple_in: eta_couple_in parameter

Outputs:
    - p_wallplug: p_wallplug result
    - p_coupled: p_coupled result
    - p_delivered: p_delivered result

SysML Source: root-0/analyses/mfe_heating_chain.sysml:79

SysML Source: root-0/analyses/mfe_heating_chain.sysml:79

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_heating_chain/operating_heating_power_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.operating_heating_power_output import Operating_Heating_PowerOutput


class Operating_Heating_PowerInput(BaseModel):
    """Input model for Operating_Heating_PowerModule.

    Attributes:
        eta_source_in: eta_source_in input
        p_required_in: p_required_in input
        eta_couple_in: eta_couple_in input
    """
    eta_source_in: float = Field(..., description="eta_source_in input")
    p_required_in: float = Field(..., description="p_required_in input")
    eta_couple_in: float = Field(..., description="eta_couple_in input")


class Operating_Heating_PowerModule(ModuleBase[Operating_Heating_PowerInput, Operating_Heating_PowerOutput]):
    """TEAx module for Operating_Heating_Power calculation.

Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11

Inputs:
    - eta_source_in: eta_source_in parameter
    - p_required_in: p_required_in parameter
    - eta_couple_in: eta_couple_in parameter

Outputs:
    - p_wallplug: p_wallplug result
    - p_coupled: p_coupled result
    - p_delivered: p_delivered result

SysML Source: root-0/analyses/mfe_heating_chain.sysml:79

    SysML Source: root-0/analyses/mfe_heating_chain.sysml:79

    Calculation Specification:
        p_coupled = p_required_in
        p_delivered = p_required_in / eta_couple_in
        p_wallplug = p_delivered / eta_source_in
        
Documentation:
Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_heating_chain.operating_heating_power_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts p_wallplug, p_coupled, p_delivered fields to separate channels.
    """

    name: str = "Operating_Heating_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, eta_source_in: float, p_required_in: float, eta_couple_in: float    ) -> Operating_Heating_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            eta_source_in: eta_source_in input
            p_required_in: p_required_in input
            eta_couple_in: eta_couple_in input

        Returns:
            Validated input model
        """
        return Operating_Heating_PowerInput(eta_source_in=eta_source_in, p_required_in=p_required_in, eta_couple_in=eta_couple_in)

    def run(
        self, eta_source_in: float, p_required_in: float, eta_couple_in: float    ) -> ModuleResult[Operating_Heating_PowerOutput]:
        """Execute calculation.

        Args:
            eta_source_in: eta_source_in input
            p_required_in: p_required_in input
            eta_couple_in: eta_couple_in input

        Returns:
            Module result with Operating_Heating_PowerOutput (p_wallplug, p_coupled, p_delivered)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(eta_source_in, p_required_in, eta_couple_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_heating_chain.operating_heating_power_impl import (
            run_operating_heating_power,
        )

        # Execute implementation - returns tuple of values
        p_wallplug, p_coupled, p_delivered = run_operating_heating_power(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Operating_Heating_PowerOutput(
                p_wallplug=p_wallplug,
                p_coupled=p_coupled,
                p_delivered=p_delivered,
            )
        )
