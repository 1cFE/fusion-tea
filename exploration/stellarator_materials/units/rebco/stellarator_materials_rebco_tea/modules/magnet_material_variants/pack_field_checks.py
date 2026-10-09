"""Pack_Field_ChecksModule Module Wrapper

TEAx module for Pack_Field_Checks calculation.

Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30

Inputs:
    - mu0_in: mu0_in parameter
    - B_peak_in: B_peak_in parameter
    - wp_side_in: wp_side_in parameter
    - I_coil_in: I_coil_in parameter
    - R_in: R_in parameter

Outputs:
    - R_over_sqrt_A_wp: R_over_sqrt_A_wp result
    - ampere_floor: ampere_floor result
    - ampere_floor_margin: ampere_floor_margin result

SysML Source: root-0/analyses/magnet_material_variants.sysml:29

SysML Source: root-0/analyses/magnet_material_variants.sysml:29

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_material_variants/pack_field_checks_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.pack_field_checks_output import Pack_Field_ChecksOutput


class Pack_Field_ChecksInput(BaseModel):
    """Input model for Pack_Field_ChecksModule.

    Attributes:
        mu0_in: mu0_in input
        B_peak_in: B_peak_in input
        wp_side_in: wp_side_in input
        I_coil_in: I_coil_in input
        R_in: R_in input
    """
    mu0_in: float = Field(..., description="mu0_in input")
    B_peak_in: float = Field(..., description="B_peak_in input")
    wp_side_in: float = Field(..., description="wp_side_in input")
    I_coil_in: float = Field(..., description="I_coil_in input")
    R_in: float = Field(..., description="R_in input")


class Pack_Field_ChecksModule(ModuleBase[Pack_Field_ChecksInput, Pack_Field_ChecksOutput]):
    """TEAx module for Pack_Field_Checks calculation.

Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30

Inputs:
    - mu0_in: mu0_in parameter
    - B_peak_in: B_peak_in parameter
    - wp_side_in: wp_side_in parameter
    - I_coil_in: I_coil_in parameter
    - R_in: R_in parameter

Outputs:
    - R_over_sqrt_A_wp: R_over_sqrt_A_wp result
    - ampere_floor: ampere_floor result
    - ampere_floor_margin: ampere_floor_margin result

SysML Source: root-0/analyses/magnet_material_variants.sysml:29

    SysML Source: root-0/analyses/magnet_material_variants.sysml:29

    Calculation Specification:
        B_peak_in = 0.0
        I_coil_in = 0.0
        R_in = 0.0
        wp_side_in = 1.0
        mu0_in = 1.25663706212e-06
        R_over_sqrt_A_wp = R_in / wp_side_in
        ampere_floor = mu0_in * I_coil_in / (4.0 * wp_side_in)
        ampere_floor_margin = B_peak_in - ampere_floor
        
Documentation:
Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.magnet_material_variants.pack_field_checks_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts R_over_sqrt_A_wp, ampere_floor, ampere_floor_margin fields to separate channels.
    """

    name: str = "Pack_Field_ChecksModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, mu0_in: float, B_peak_in: float, wp_side_in: float, I_coil_in: float, R_in: float    ) -> Pack_Field_ChecksInput:
        """Validate inputs and fill defaults.

        Args:
            mu0_in: mu0_in input
            B_peak_in: B_peak_in input
            wp_side_in: wp_side_in input
            I_coil_in: I_coil_in input
            R_in: R_in input

        Returns:
            Validated input model
        """
        return Pack_Field_ChecksInput(mu0_in=mu0_in, B_peak_in=B_peak_in, wp_side_in=wp_side_in, I_coil_in=I_coil_in, R_in=R_in)

    def run(
        self, mu0_in: float, B_peak_in: float, wp_side_in: float, I_coil_in: float, R_in: float    ) -> ModuleResult[Pack_Field_ChecksOutput]:
        """Execute calculation.

        Args:
            mu0_in: mu0_in input
            B_peak_in: B_peak_in input
            wp_side_in: wp_side_in input
            I_coil_in: I_coil_in input
            R_in: R_in input

        Returns:
            Module result with Pack_Field_ChecksOutput (R_over_sqrt_A_wp, ampere_floor, ampere_floor_margin)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(mu0_in, B_peak_in, wp_side_in, I_coil_in, R_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.magnet_material_variants.pack_field_checks_impl import (
            run_pack_field_checks,
        )

        # Execute implementation - returns tuple of values
        R_over_sqrt_A_wp, ampere_floor, ampere_floor_margin = run_pack_field_checks(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Pack_Field_ChecksOutput(
                R_over_sqrt_A_wp=R_over_sqrt_A_wp,
                ampere_floor=ampere_floor,
                ampere_floor_margin=ampere_floor_margin,
            )
        )
