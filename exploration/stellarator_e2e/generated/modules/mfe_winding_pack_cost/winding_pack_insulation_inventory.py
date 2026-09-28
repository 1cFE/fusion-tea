"""Winding_Pack_Insulation_InventoryModule Module Wrapper

TEAx module for Winding_Pack_Insulation_Inventory calculation.

Conditional additional internal solid-sheet inventory and unpriced ground-layer envelope, excluding assembly clearance and extra cold equipment.
Normative manual equations: internal_volume = volume_in*(internal_fraction_x+internal_fraction_y+internal_fraction_x*internal_fraction_y); perimeter = 2*n_coils*c_coil*wp_side*f_perimeter*(sqrt(aspect_ratio)*(1+internal_fraction_x)+(1+internal_fraction_y)/sqrt(aspect_ratio)); ground_volume = ground_thickness*perimeter+4*ground_thickness*ground_thickness*n_coils*c_coil; sheet_area = internal_volume/sheet_thickness; stock_cost = sheet_area*sheet_price.
Units: volumes m^3, wp_side/c_coil/thicknesses m, sheet_area m^2, sheet_price dollars/m^2, stock_cost dollars; other inputs dimensionless. Current wp_side and geometric volume scale the frozen relative coil-section distribution with equal circumference and common aspect ratio. Area and perimeter distribution factors are distinct. Closed coils have no end layer. Internal solid-sheet occupancy and exclusion from the winding charge are assumptions; this is not a demonstrated missing charge. Ground wrapping, impregnation, installation, waste and qualification remain unresolved. The laminate stock already includes cured resin.
Domain: every input and intermediate/output finite; volume_in, ground_thickness and sheet_price >= 0; wp_side, aspect_ratio, n_coils, c_coil, sheet_thickness > 0; internal fractions >= 0; 0 < f_perimeter <= 1. Positive products/divisions must not underflow to zero. Fractions are added build relative to the underlying section, not material occupancy fractions. No independently inconsistent volume/distribution interpretation is certified by this arithmetic.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/; work/orchestration/goals/magnet-manufacturing-cost-completeness/evidence/manufacturing-research.md.
*Reference**: Stellaris Tables 7-8 and Figure 40; work/active/WI-063_magnet-manufacturing-account-completeness/design.md; goal evidence/source-design-review.md.
*Last Updated**: 2026-09-15

Inputs:
    - internal_fraction_x: internal_fraction_x parameter
    - aspect_ratio: aspect_ratio parameter
    - f_perimeter: f_perimeter parameter
    - internal_fraction_y: internal_fraction_y parameter
    - ground_thickness: ground_thickness parameter
    - wp_side: wp_side parameter
    - n_coils: n_coils parameter
    - sheet_thickness: sheet_thickness parameter
    - c_coil: c_coil parameter
    - sheet_price: sheet_price parameter
    - volume_in: volume_in parameter

Outputs:
    - ground_volume: ground_volume result
    - stock_cost: stock_cost result
    - internal_volume: internal_volume result
    - sheet_area: sheet_area result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:70

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:70

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_winding_pack_cost/winding_pack_insulation_inventory_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.winding_pack_insulation_inventory_output import Winding_Pack_Insulation_InventoryOutput


class Winding_Pack_Insulation_InventoryInput(BaseModel):
    """Input model for Winding_Pack_Insulation_InventoryModule.

    Attributes:
        internal_fraction_x: internal_fraction_x input
        aspect_ratio: aspect_ratio input
        f_perimeter: f_perimeter input
        internal_fraction_y: internal_fraction_y input
        ground_thickness: ground_thickness input
        wp_side: wp_side input
        n_coils: n_coils input
        sheet_thickness: sheet_thickness input
        c_coil: c_coil input
        sheet_price: sheet_price input
        volume_in: volume_in input
    """
    internal_fraction_x: float = Field(..., description="internal_fraction_x input")
    aspect_ratio: float = Field(..., description="aspect_ratio input")
    f_perimeter: float = Field(..., description="f_perimeter input")
    internal_fraction_y: float = Field(..., description="internal_fraction_y input")
    ground_thickness: float = Field(..., description="ground_thickness input")
    wp_side: float = Field(..., description="wp_side input")
    n_coils: float = Field(..., description="n_coils input")
    sheet_thickness: float = Field(..., description="sheet_thickness input")
    c_coil: float = Field(..., description="c_coil input")
    sheet_price: float = Field(..., description="sheet_price input")
    volume_in: float = Field(..., description="volume_in input")


class Winding_Pack_Insulation_InventoryModule(ModuleBase[Winding_Pack_Insulation_InventoryInput, Winding_Pack_Insulation_InventoryOutput]):
    """TEAx module for Winding_Pack_Insulation_Inventory calculation.

Conditional additional internal solid-sheet inventory and unpriced ground-layer envelope, excluding assembly clearance and extra cold equipment.
Normative manual equations: internal_volume = volume_in*(internal_fraction_x+internal_fraction_y+internal_fraction_x*internal_fraction_y); perimeter = 2*n_coils*c_coil*wp_side*f_perimeter*(sqrt(aspect_ratio)*(1+internal_fraction_x)+(1+internal_fraction_y)/sqrt(aspect_ratio)); ground_volume = ground_thickness*perimeter+4*ground_thickness*ground_thickness*n_coils*c_coil; sheet_area = internal_volume/sheet_thickness; stock_cost = sheet_area*sheet_price.
Units: volumes m^3, wp_side/c_coil/thicknesses m, sheet_area m^2, sheet_price dollars/m^2, stock_cost dollars; other inputs dimensionless. Current wp_side and geometric volume scale the frozen relative coil-section distribution with equal circumference and common aspect ratio. Area and perimeter distribution factors are distinct. Closed coils have no end layer. Internal solid-sheet occupancy and exclusion from the winding charge are assumptions; this is not a demonstrated missing charge. Ground wrapping, impregnation, installation, waste and qualification remain unresolved. The laminate stock already includes cured resin.
Domain: every input and intermediate/output finite; volume_in, ground_thickness and sheet_price >= 0; wp_side, aspect_ratio, n_coils, c_coil, sheet_thickness > 0; internal fractions >= 0; 0 < f_perimeter <= 1. Positive products/divisions must not underflow to zero. Fractions are added build relative to the underlying section, not material occupancy fractions. No independently inconsistent volume/distribution interpretation is certified by this arithmetic.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/; work/orchestration/goals/magnet-manufacturing-cost-completeness/evidence/manufacturing-research.md.
*Reference**: Stellaris Tables 7-8 and Figure 40; work/active/WI-063_magnet-manufacturing-account-completeness/design.md; goal evidence/source-design-review.md.
*Last Updated**: 2026-09-15

Inputs:
    - internal_fraction_x: internal_fraction_x parameter
    - aspect_ratio: aspect_ratio parameter
    - f_perimeter: f_perimeter parameter
    - internal_fraction_y: internal_fraction_y parameter
    - ground_thickness: ground_thickness parameter
    - wp_side: wp_side parameter
    - n_coils: n_coils parameter
    - sheet_thickness: sheet_thickness parameter
    - c_coil: c_coil parameter
    - sheet_price: sheet_price parameter
    - volume_in: volume_in parameter

Outputs:
    - ground_volume: ground_volume result
    - stock_cost: stock_cost result
    - internal_volume: internal_volume result
    - sheet_area: sheet_area result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:70

    SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:70

    Calculation Specification:
        See documentation:
Conditional additional internal solid-sheet inventory and unpriced ground-layer envelope, excluding assembly clearance and extra cold equipment.
Normative manual equations: internal_volume = volume_in*(internal_fraction_x+internal_fraction_y+internal_fraction_x*internal_fraction_y); perimeter = 2*n_coils*c_coil*wp_side*f_perimeter*(sqrt(aspect_ratio)*(1+internal_fraction_x)+(1+internal_fraction_y)/sqrt(aspect_ratio)); ground_volume = ground_thickness*perimeter+4*ground_thickness*ground_thickness*n_coils*c_coil; sheet_area = internal_volume/sheet_thickness; stock_cost = sheet_area*sheet_price.
Units: volumes m^3, wp_side/c_coil/thicknesses m, sheet_area m^2, sheet_price dollars/m^2, stock_cost dollars; other inputs dimensionless. Current wp_side and geometric volume scale the frozen relative coil-section distribution with equal circumference and common aspect ratio. Area and perimeter distribution factors are distinct. Closed coils have no end layer. Internal solid-sheet occupancy and exclusion from the winding charge are assumptions; this is not a demonstrated missing charge. Ground wrapping, impregnation, installation, waste and qualification remain unresolved. The laminate stock already includes cured resin.
Domain: every input and intermediate/output finite; volume_in, ground_thickness and sheet_price >= 0; wp_side, aspect_ratio, n_coils, c_coil, sheet_thickness > 0; internal fractions >= 0; 0 < f_perimeter <= 1. Positive products/divisions must not underflow to zero. Fractions are added build relative to the underlying section, not material occupancy fractions. No independently inconsistent volume/distribution interpretation is certified by this arithmetic.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/; work/orchestration/goals/magnet-manufacturing-cost-completeness/evidence/manufacturing-research.md.
*Reference**: Stellaris Tables 7-8 and Figure 40; work/active/WI-063_magnet-manufacturing-account-completeness/design.md; goal evidence/source-design-review.md.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_insulation_inventory_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts ground_volume, stock_cost, internal_volume, sheet_area fields to separate channels.
    """

    name: str = "Winding_Pack_Insulation_InventoryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, internal_fraction_x: float, aspect_ratio: float, f_perimeter: float, internal_fraction_y: float, ground_thickness: float, wp_side: float, n_coils: float, sheet_thickness: float, c_coil: float, sheet_price: float, volume_in: float    ) -> Winding_Pack_Insulation_InventoryInput:
        """Validate inputs and fill defaults.

        Args:
            internal_fraction_x: internal_fraction_x input
            aspect_ratio: aspect_ratio input
            f_perimeter: f_perimeter input
            internal_fraction_y: internal_fraction_y input
            ground_thickness: ground_thickness input
            wp_side: wp_side input
            n_coils: n_coils input
            sheet_thickness: sheet_thickness input
            c_coil: c_coil input
            sheet_price: sheet_price input
            volume_in: volume_in input

        Returns:
            Validated input model
        """
        return Winding_Pack_Insulation_InventoryInput(internal_fraction_x=internal_fraction_x, aspect_ratio=aspect_ratio, f_perimeter=f_perimeter, internal_fraction_y=internal_fraction_y, ground_thickness=ground_thickness, wp_side=wp_side, n_coils=n_coils, sheet_thickness=sheet_thickness, c_coil=c_coil, sheet_price=sheet_price, volume_in=volume_in)

    def run(
        self, internal_fraction_x: float, aspect_ratio: float, f_perimeter: float, internal_fraction_y: float, ground_thickness: float, wp_side: float, n_coils: float, sheet_thickness: float, c_coil: float, sheet_price: float, volume_in: float    ) -> ModuleResult[Winding_Pack_Insulation_InventoryOutput]:
        """Execute calculation.

        Args:
            internal_fraction_x: internal_fraction_x input
            aspect_ratio: aspect_ratio input
            f_perimeter: f_perimeter input
            internal_fraction_y: internal_fraction_y input
            ground_thickness: ground_thickness input
            wp_side: wp_side input
            n_coils: n_coils input
            sheet_thickness: sheet_thickness input
            c_coil: c_coil input
            sheet_price: sheet_price input
            volume_in: volume_in input

        Returns:
            Module result with Winding_Pack_Insulation_InventoryOutput (ground_volume, stock_cost, internal_volume, sheet_area)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(internal_fraction_x, aspect_ratio, f_perimeter, internal_fraction_y, ground_thickness, wp_side, n_coils, sheet_thickness, c_coil, sheet_price, volume_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_insulation_inventory_impl import (
            run_winding_pack_insulation_inventory,
        )

        # Execute implementation - returns tuple of values
        ground_volume, stock_cost, internal_volume, sheet_area = run_winding_pack_insulation_inventory(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Pack_Insulation_InventoryOutput(
                ground_volume=ground_volume,
                stock_cost=stock_cost,
                internal_volume=internal_volume,
                sheet_area=sheet_area,
            )
        )
