from pydantic import BaseModel, Field


class MagnetMaterialVariantsParams(BaseModel):
    """Parameters from magnet_material_variants.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__rebco_material__cryoplant__intercept_demand_available: bool = Field(default=1.0, description="Entry point: intercept_demand_available")
    stellarator_09_materials__rebco_material__cryoplant__inventory_enabled: bool = Field(default=0.0, description="Entry point: inventory_enabled")
    stellarator_09_materials__rebco_material__magnet__pack_field__mu0_in: float = Field(default=1.25663706212e-06, description="Entry point: mu0_in")
    stellarator_09_materials__rebco_material__magnet__rebco_law_enabled: float = Field(default=0.0, description="Entry point: rebco_law_enabled")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
