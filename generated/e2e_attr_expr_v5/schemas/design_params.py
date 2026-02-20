from pydantic import BaseModel, Field


class DesignParams(BaseModel):
    """Parameters from design.sysml.

    Generated from SysML calculation definitions.
    """
    E2EAttrExprDesign__e2e_plant__quantity: float = Field(default=100.0, description="Entry point: quantity")
    E2EAttrExprDesign__e2e_plant__unit_cost: float = Field(default=50.0, description="Entry point: unit_cost")
    E2EAttrExprDesign__e2e_plant__om_rate: float = Field(default=20.0, description="Entry point: om_rate")
    E2EAttrExprDesign__e2e_plant__length: float = Field(default=10.0, description="Entry point: length")
    E2EAttrExprDesign__e2e_plant__width: float = Field(default=5.0, description="Entry point: width")
    E2EAttrExprDesign__e2e_plant__height: float = Field(default=3.0, description="Entry point: height")
    E2EAttrExprDesign__e2e_plant__cost_per_sqm: float = Field(default=12.0, description="Entry point: cost_per_sqm")
    E2EAttrExprDesign__e2e_plant__component_cost__quantity: float = Field(default=100.0, description="Entry point: quantity")
    E2EAttrExprDesign__e2e_plant__component_cost__unit_cost: float = Field(default=50.0, description="Entry point: unit_cost")
    E2EAttrExprDesign__e2e_plant__financial__discount_rate: float = Field(default=0.05, description="Entry point: discount_rate")
    E2EAttrExprDesign__e2e_plant__financial__lifetime: float = Field(default=25.0, description="Entry point: lifetime")
    E2EAttrExprDesign__e2e_plant__energy__availability: float = Field(default=0.9, description="Entry point: availability")
    E2EAttrExprDesign__e2e_plant__component_cost__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    E2EAttrExprDesign__e2e_plant__component_cost__install_factor: float = Field(default=0.3, description="Entry point: install_factor")

    model_config = {"frozen": True, "extra": "forbid"}
