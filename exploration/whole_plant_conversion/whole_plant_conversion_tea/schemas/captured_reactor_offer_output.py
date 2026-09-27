from pydantic import Field
from simkit.config.schema import MultiOutput

class Captured_Reactor_OfferOutput(MultiOutput):
    """Multi-output container for Captured_Reactor_Offer.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/captured_reactor_offer_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:14
    """
    nuclear_transport_qualified: float = Field(description="nuclear_transport_qualified output")
    inventory_cold_W: float = Field(description="inventory_cold_W output")
    identity_supported: float = Field(description="identity_supported output")
    peak_field: float = Field(description="peak_field output")
    cold_rating_W: float = Field(description="cold_rating_W output")
    support_cost: float = Field(description="support_cost output")
    cold_volume_m3: float = Field(description="cold_volume_m3 output")
    intercept_temperature_K: float = Field(description="intercept_temperature_K output")
    intercept_inventory_W: float = Field(description="intercept_inventory_W output")
    turn_current_A: float = Field(description="turn_current_A output")
    axis_field: float = Field(description="axis_field output")
    strain_margin: float = Field(description="strain_margin output")
    magnet_capital: float = Field(description="magnet_capital output")
    cold_W: float = Field(description="cold_W output")
    stress_margin_Pa: float = Field(description="stress_margin_Pa output")
    current_margin: float = Field(description="current_margin output")
    coil_drive_MW: float = Field(description="coil_drive_MW output")
    material_cost: float = Field(description="material_cost output")
    stress_Pa: float = Field(description="stress_Pa output")
    intercept_W: float = Field(description="intercept_W output")
    field_extrapolated: float = Field(description="field_extrapolated output")
    cold_carnot_fraction: float = Field(description="cold_carnot_fraction output")
    strain: float = Field(description="strain output")
    fixed_cold_MW: float = Field(description="fixed_cold_MW output")
    insulation_cost: float = Field(description="insulation_cost output")
    cold_margin_W: float = Field(description="cold_margin_W output")
    global_construction_qualified: float = Field(description="global_construction_qualified output")
    intercept_carnot_fraction: float = Field(description="intercept_carnot_fraction output")
    ambient_temperature_K: float = Field(description="ambient_temperature_K output")
    winding_cost: float = Field(description="winding_cost output")
    tape_cost: float = Field(description="tape_cost output")
    field_margin_T: float = Field(description="field_margin_T output")
    intercept_rating_W: float = Field(description="intercept_rating_W output")
    fit_margin: float = Field(description="fit_margin output")
    intercept_margin_W: float = Field(description="intercept_margin_W output")
    cold_temperature_K: float = Field(description="cold_temperature_K output")
    nuclear_heating_W_m3: float = Field(description="nuclear_heating_W_m3 output")
    refrigeration_MW: float = Field(description="refrigeration_MW output")
