from pydantic import BaseModel, Field


class ConstituentInventoryParams(BaseModel):
    """Parameters from constituent_inventory.

    Generated from SysML calculation definitions.
    """
    aries_constituent_inventory__behind_divertor__coverage: float = Field(default=0.106, description="Entry point: coverage")
    aries_constituent_inventory__behind_divertor__ferritic_steel__component_rate: float = Field(default=103.0, description="Entry point: component_rate")
    aries_constituent_inventory__behind_divertor__ferritic_steel__material_density: float = Field(default=7800.0, description="Entry point: material_density")
    aries_constituent_inventory__behind_divertor__ferritic_steel__volume_fraction: float = Field(default=0.08, description="Entry point: volume_fraction")
    aries_constituent_inventory__behind_divertor__helium_fraction: float = Field(default=0.08, description="Entry point: helium_fraction")
    aries_constituent_inventory__behind_divertor__lipb__component_rate: float = Field(default=17.1, description="Entry point: component_rate")
    aries_constituent_inventory__behind_divertor__lipb__material_density: float = Field(default=8897.0, description="Entry point: material_density")
    aries_constituent_inventory__behind_divertor__lipb__volume_fraction: float = Field(default=0.75, description="Entry point: volume_fraction")
    aries_constituent_inventory__behind_divertor__midpoint_area_basis: float = Field(default=1.0, description="Entry point: midpoint_area_basis")
    aries_constituent_inventory__behind_divertor__sic_insert__component_rate: float = Field(default=101.0, description="Entry point: component_rate")
    aries_constituent_inventory__behind_divertor__sic_insert__material_density: float = Field(default=3200.0, description="Entry point: material_density")
    aries_constituent_inventory__behind_divertor__sic_insert__volume_fraction: float = Field(default=0.09, description="Entry point: volume_fraction")
    aries_constituent_inventory__behind_divertor__thickness: float = Field(default=0.35, description="Entry point: thickness")
    aries_constituent_inventory__full__coverage: float = Field(default=0.654, description="Entry point: coverage")
    aries_constituent_inventory__full__ferritic_steel__component_rate: float = Field(default=103.0, description="Entry point: component_rate")
    aries_constituent_inventory__full__ferritic_steel__material_density: float = Field(default=7800.0, description="Entry point: material_density")
    aries_constituent_inventory__full__ferritic_steel__volume_fraction: float = Field(default=0.06, description="Entry point: volume_fraction")
    aries_constituent_inventory__full__helium_fraction: float = Field(default=0.08, description="Entry point: helium_fraction")
    aries_constituent_inventory__full__lipb__component_rate: float = Field(default=17.1, description="Entry point: component_rate")
    aries_constituent_inventory__full__lipb__material_density: float = Field(default=8897.0, description="Entry point: material_density")
    aries_constituent_inventory__full__lipb__volume_fraction: float = Field(default=0.79, description="Entry point: volume_fraction")
    aries_constituent_inventory__full__midpoint_area_basis: float = Field(default=1.0, description="Entry point: midpoint_area_basis")
    aries_constituent_inventory__full__sic_insert__component_rate: float = Field(default=101.0, description="Entry point: component_rate")
    aries_constituent_inventory__full__sic_insert__material_density: float = Field(default=3200.0, description="Entry point: material_density")
    aries_constituent_inventory__full__sic_insert__volume_fraction: float = Field(default=0.07, description="Entry point: volume_fraction")
    aries_constituent_inventory__full__thickness: float = Field(default=0.543, description="Entry point: thickness")
    aries_constituent_inventory__tapered__coverage: float = Field(default=0.24, description="Entry point: coverage")
    aries_constituent_inventory__tapered__ferritic_steel__component_rate: float = Field(default=103.0, description="Entry point: component_rate")
    aries_constituent_inventory__tapered__ferritic_steel__material_density: float = Field(default=7800.0, description="Entry point: material_density")
    aries_constituent_inventory__tapered__ferritic_steel__volume_fraction: float = Field(default=0.08, description="Entry point: volume_fraction")
    aries_constituent_inventory__tapered__helium_fraction: float = Field(default=0.08, description="Entry point: helium_fraction")
    aries_constituent_inventory__tapered__lipb__component_rate: float = Field(default=17.1, description="Entry point: component_rate")
    aries_constituent_inventory__tapered__lipb__material_density: float = Field(default=8897.0, description="Entry point: material_density")
    aries_constituent_inventory__tapered__lipb__volume_fraction: float = Field(default=0.76, description="Entry point: volume_fraction")
    aries_constituent_inventory__tapered__midpoint_area_basis: float = Field(default=1.0, description="Entry point: midpoint_area_basis")
    aries_constituent_inventory__tapered__sic_insert__component_rate: float = Field(default=101.0, description="Entry point: component_rate")
    aries_constituent_inventory__tapered__sic_insert__material_density: float = Field(default=3200.0, description="Entry point: material_density")
    aries_constituent_inventory__tapered__sic_insert__volume_fraction: float = Field(default=0.08, description="Entry point: volume_fraction")
    aries_constituent_inventory__tapered__thickness: float = Field(default=0.25, description="Entry point: thickness")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
