"""Supplied_Source_BasisModule Module Wrapper

TEAx module for Supplied_Source_Basis calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_source_basis_impl.py; reviewed equations in design/configuration.

Inputs:
    - divertor_limit_in: divertor_limit_in parameter
    - alpha_proxy_in: alpha_proxy_in parameter
    - divertor_area_in: divertor_area_in parameter
    - heating_wall_rating_in: heating_wall_rating_in parameter
    - heating_source_efficiency_in: heating_source_efficiency_in parameter
    - neutron_multiplier_in: neutron_multiplier_in parameter
    - wall_fusion_reference_in: wall_fusion_reference_in parameter
    - divertor_peaking_in: divertor_peaking_in parameter
    - alpha_retention_in: alpha_retention_in parameter
    - heating_coupling_efficiency_in: heating_coupling_efficiency_in parameter
    - fusion_envelope_MW_in: fusion_envelope_MW_in parameter
    - radiation_fraction_in: radiation_fraction_in parameter
    - wall_reference_in: wall_reference_in parameter
    - heating_coupled_rating_in: heating_coupled_rating_in parameter
    - deposited_heating_MW_in: deposited_heating_MW_in parameter
    - q_source_MW_in: q_source_MW_in parameter

Outputs:
    - heating_loss_MW: heating_loss_MW result
    - heating_wall_margin: heating_wall_margin result
    - domain_supported: domain_supported result
    - divertor_load: divertor_load result
    - heating_coupled_margin: heating_coupled_margin result
    - source_qualified: source_qualified result
    - fusion_envelope_margin: fusion_envelope_margin result
    - divertor_margin: divertor_margin result
    - wall_load: wall_load result
    - reconstructed_source_MW: reconstructed_source_MW result
    - fusion_MW: fusion_MW result
    - heating_wall_MW: heating_wall_MW result
    - source_residual: source_residual result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:141

SysML Source: root-0/whole_plant_conversion_accounts.sysml:141

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/supplied_source_basis_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.supplied_source_basis_output import Supplied_Source_BasisOutput


class Supplied_Source_BasisInput(BaseModel):
    """Input model for Supplied_Source_BasisModule.

    Attributes:
        divertor_limit_in: divertor_limit_in input
        alpha_proxy_in: alpha_proxy_in input
        divertor_area_in: divertor_area_in input
        heating_wall_rating_in: heating_wall_rating_in input
        heating_source_efficiency_in: heating_source_efficiency_in input
        neutron_multiplier_in: neutron_multiplier_in input
        wall_fusion_reference_in: wall_fusion_reference_in input
        divertor_peaking_in: divertor_peaking_in input
        alpha_retention_in: alpha_retention_in input
        heating_coupling_efficiency_in: heating_coupling_efficiency_in input
        fusion_envelope_MW_in: fusion_envelope_MW_in input
        radiation_fraction_in: radiation_fraction_in input
        wall_reference_in: wall_reference_in input
        heating_coupled_rating_in: heating_coupled_rating_in input
        deposited_heating_MW_in: deposited_heating_MW_in input
        q_source_MW_in: q_source_MW_in input
    """
    divertor_limit_in: float = Field(..., description="divertor_limit_in input")
    alpha_proxy_in: float = Field(..., description="alpha_proxy_in input")
    divertor_area_in: float = Field(..., description="divertor_area_in input")
    heating_wall_rating_in: float = Field(..., description="heating_wall_rating_in input")
    heating_source_efficiency_in: float = Field(..., description="heating_source_efficiency_in input")
    neutron_multiplier_in: float = Field(..., description="neutron_multiplier_in input")
    wall_fusion_reference_in: float = Field(..., description="wall_fusion_reference_in input")
    divertor_peaking_in: float = Field(..., description="divertor_peaking_in input")
    alpha_retention_in: float = Field(..., description="alpha_retention_in input")
    heating_coupling_efficiency_in: float = Field(..., description="heating_coupling_efficiency_in input")
    fusion_envelope_MW_in: float = Field(..., description="fusion_envelope_MW_in input")
    radiation_fraction_in: float = Field(..., description="radiation_fraction_in input")
    wall_reference_in: float = Field(..., description="wall_reference_in input")
    heating_coupled_rating_in: float = Field(..., description="heating_coupled_rating_in input")
    deposited_heating_MW_in: float = Field(..., description="deposited_heating_MW_in input")
    q_source_MW_in: float = Field(..., description="q_source_MW_in input")


class Supplied_Source_BasisModule(ModuleBase[Supplied_Source_BasisInput, Supplied_Source_BasisOutput]):
    """TEAx module for Supplied_Source_Basis calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_source_basis_impl.py; reviewed equations in design/configuration.

Inputs:
    - divertor_limit_in: divertor_limit_in parameter
    - alpha_proxy_in: alpha_proxy_in parameter
    - divertor_area_in: divertor_area_in parameter
    - heating_wall_rating_in: heating_wall_rating_in parameter
    - heating_source_efficiency_in: heating_source_efficiency_in parameter
    - neutron_multiplier_in: neutron_multiplier_in parameter
    - wall_fusion_reference_in: wall_fusion_reference_in parameter
    - divertor_peaking_in: divertor_peaking_in parameter
    - alpha_retention_in: alpha_retention_in parameter
    - heating_coupling_efficiency_in: heating_coupling_efficiency_in parameter
    - fusion_envelope_MW_in: fusion_envelope_MW_in parameter
    - radiation_fraction_in: radiation_fraction_in parameter
    - wall_reference_in: wall_reference_in parameter
    - heating_coupled_rating_in: heating_coupled_rating_in parameter
    - deposited_heating_MW_in: deposited_heating_MW_in parameter
    - q_source_MW_in: q_source_MW_in parameter

Outputs:
    - heating_loss_MW: heating_loss_MW result
    - heating_wall_margin: heating_wall_margin result
    - domain_supported: domain_supported result
    - divertor_load: divertor_load result
    - heating_coupled_margin: heating_coupled_margin result
    - source_qualified: source_qualified result
    - fusion_envelope_margin: fusion_envelope_margin result
    - divertor_margin: divertor_margin result
    - wall_load: wall_load result
    - reconstructed_source_MW: reconstructed_source_MW result
    - fusion_MW: fusion_MW result
    - heating_wall_MW: heating_wall_MW result
    - source_residual: source_residual result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:141

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:141

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_source_basis_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.supplied_source_basis_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts heating_loss_MW, heating_wall_margin, domain_supported, divertor_load, heating_coupled_margin, source_qualified, fusion_envelope_margin, divertor_margin, wall_load, reconstructed_source_MW, fusion_MW, heating_wall_MW, source_residual fields to separate channels.
    """

    name: str = "Supplied_Source_BasisModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, divertor_limit_in: float, alpha_proxy_in: float, divertor_area_in: float, heating_wall_rating_in: float, heating_source_efficiency_in: float, neutron_multiplier_in: float, wall_fusion_reference_in: float, divertor_peaking_in: float, alpha_retention_in: float, heating_coupling_efficiency_in: float, fusion_envelope_MW_in: float, radiation_fraction_in: float, wall_reference_in: float, heating_coupled_rating_in: float, deposited_heating_MW_in: float, q_source_MW_in: float    ) -> Supplied_Source_BasisInput:
        """Validate inputs and fill defaults.

        Args:
            divertor_limit_in: divertor_limit_in input
            alpha_proxy_in: alpha_proxy_in input
            divertor_area_in: divertor_area_in input
            heating_wall_rating_in: heating_wall_rating_in input
            heating_source_efficiency_in: heating_source_efficiency_in input
            neutron_multiplier_in: neutron_multiplier_in input
            wall_fusion_reference_in: wall_fusion_reference_in input
            divertor_peaking_in: divertor_peaking_in input
            alpha_retention_in: alpha_retention_in input
            heating_coupling_efficiency_in: heating_coupling_efficiency_in input
            fusion_envelope_MW_in: fusion_envelope_MW_in input
            radiation_fraction_in: radiation_fraction_in input
            wall_reference_in: wall_reference_in input
            heating_coupled_rating_in: heating_coupled_rating_in input
            deposited_heating_MW_in: deposited_heating_MW_in input
            q_source_MW_in: q_source_MW_in input

        Returns:
            Validated input model
        """
        return Supplied_Source_BasisInput(divertor_limit_in=divertor_limit_in, alpha_proxy_in=alpha_proxy_in, divertor_area_in=divertor_area_in, heating_wall_rating_in=heating_wall_rating_in, heating_source_efficiency_in=heating_source_efficiency_in, neutron_multiplier_in=neutron_multiplier_in, wall_fusion_reference_in=wall_fusion_reference_in, divertor_peaking_in=divertor_peaking_in, alpha_retention_in=alpha_retention_in, heating_coupling_efficiency_in=heating_coupling_efficiency_in, fusion_envelope_MW_in=fusion_envelope_MW_in, radiation_fraction_in=radiation_fraction_in, wall_reference_in=wall_reference_in, heating_coupled_rating_in=heating_coupled_rating_in, deposited_heating_MW_in=deposited_heating_MW_in, q_source_MW_in=q_source_MW_in)

    def run(
        self, divertor_limit_in: float, alpha_proxy_in: float, divertor_area_in: float, heating_wall_rating_in: float, heating_source_efficiency_in: float, neutron_multiplier_in: float, wall_fusion_reference_in: float, divertor_peaking_in: float, alpha_retention_in: float, heating_coupling_efficiency_in: float, fusion_envelope_MW_in: float, radiation_fraction_in: float, wall_reference_in: float, heating_coupled_rating_in: float, deposited_heating_MW_in: float, q_source_MW_in: float    ) -> ModuleResult[Supplied_Source_BasisOutput]:
        """Execute calculation.

        Args:
            divertor_limit_in: divertor_limit_in input
            alpha_proxy_in: alpha_proxy_in input
            divertor_area_in: divertor_area_in input
            heating_wall_rating_in: heating_wall_rating_in input
            heating_source_efficiency_in: heating_source_efficiency_in input
            neutron_multiplier_in: neutron_multiplier_in input
            wall_fusion_reference_in: wall_fusion_reference_in input
            divertor_peaking_in: divertor_peaking_in input
            alpha_retention_in: alpha_retention_in input
            heating_coupling_efficiency_in: heating_coupling_efficiency_in input
            fusion_envelope_MW_in: fusion_envelope_MW_in input
            radiation_fraction_in: radiation_fraction_in input
            wall_reference_in: wall_reference_in input
            heating_coupled_rating_in: heating_coupled_rating_in input
            deposited_heating_MW_in: deposited_heating_MW_in input
            q_source_MW_in: q_source_MW_in input

        Returns:
            Module result with Supplied_Source_BasisOutput (heating_loss_MW, heating_wall_margin, domain_supported, divertor_load, heating_coupled_margin, source_qualified, fusion_envelope_margin, divertor_margin, wall_load, reconstructed_source_MW, fusion_MW, heating_wall_MW, source_residual)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(divertor_limit_in, alpha_proxy_in, divertor_area_in, heating_wall_rating_in, heating_source_efficiency_in, neutron_multiplier_in, wall_fusion_reference_in, divertor_peaking_in, alpha_retention_in, heating_coupling_efficiency_in, fusion_envelope_MW_in, radiation_fraction_in, wall_reference_in, heating_coupled_rating_in, deposited_heating_MW_in, q_source_MW_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.supplied_source_basis_impl import (
            run_supplied_source_basis,
        )

        # Execute implementation - returns tuple of values
        heating_loss_MW, heating_wall_margin, domain_supported, divertor_load, heating_coupled_margin, source_qualified, fusion_envelope_margin, divertor_margin, wall_load, reconstructed_source_MW, fusion_MW, heating_wall_MW, source_residual = run_supplied_source_basis(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Supplied_Source_BasisOutput(
                heating_loss_MW=heating_loss_MW,
                heating_wall_margin=heating_wall_margin,
                domain_supported=domain_supported,
                divertor_load=divertor_load,
                heating_coupled_margin=heating_coupled_margin,
                source_qualified=source_qualified,
                fusion_envelope_margin=fusion_envelope_margin,
                divertor_margin=divertor_margin,
                wall_load=wall_load,
                reconstructed_source_MW=reconstructed_source_MW,
                fusion_MW=fusion_MW,
                heating_wall_MW=heating_wall_MW,
                source_residual=source_residual,
            )
        )
