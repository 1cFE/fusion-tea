from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Pack_Insulation_InventoryOutput(MultiOutput):
    """Multi-output container for Winding_Pack_Insulation_Inventory.

Conditional additional internal solid-sheet inventory and unpriced ground-layer envelope, excluding assembly clearance and extra cold equipment.
Normative manual equations: internal_volume = volume_in*(internal_fraction_x+internal_fraction_y+internal_fraction_x*internal_fraction_y); perimeter = 2*n_coils*c_coil*wp_side*f_perimeter*(sqrt(aspect_ratio)*(1+internal_fraction_x)+(1+internal_fraction_y)/sqrt(aspect_ratio)); ground_volume = ground_thickness*perimeter+4*ground_thickness*ground_thickness*n_coils*c_coil; sheet_area = internal_volume/sheet_thickness; stock_cost = sheet_area*sheet_price.
Units: volumes m^3, wp_side/c_coil/thicknesses m, sheet_area m^2, sheet_price dollars/m^2, stock_cost dollars; other inputs dimensionless. Current wp_side and geometric volume scale the frozen relative coil-section distribution with equal circumference and common aspect ratio. Area and perimeter distribution factors are distinct. Closed coils have no end layer. Internal solid-sheet occupancy and exclusion from the winding charge are assumptions; this is not a demonstrated missing charge. Ground wrapping, impregnation, installation, waste and qualification remain unresolved. The laminate stock already includes cured resin.
Domain: every input and intermediate/output finite; volume_in, ground_thickness and sheet_price >= 0; wp_side, aspect_ratio, n_coils, c_coil, sheet_thickness > 0; internal fractions >= 0; 0 < f_perimeter <= 1. Positive products/divisions must not underflow to zero. Fractions are added build relative to the underlying section, not material occupancy fractions. No independently inconsistent volume/distribution interpretation is certified by this arithmetic.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/; work/orchestration/goals/magnet-manufacturing-cost-completeness/evidence/manufacturing-research.md.
*Reference**: Stellaris Tables 7-8 and Figure 40; work/active/WI-063_magnet-manufacturing-account-completeness/design.md; goal evidence/source-design-review.md.
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:70
    """
    ground_volume: float = Field(description="ground_volume output")
    stock_cost: float = Field(description="stock_cost output")
    internal_volume: float = Field(description="internal_volume output")
    sheet_area: float = Field(description="sheet_area output")
