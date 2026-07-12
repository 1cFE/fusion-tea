from pydantic import BaseModel, Field


class IfePlantParams(BaseModel):
    """Parameters from ife_plant.sysml.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__chamber__blanket_energy_multiple: float = Field(default=1.15, description="Entry point: blanket_energy_multiple")
    hif_plant_pkg__hif_plant__chamber__yield_cost_constant: float = Field(default=5000000.0, description="Entry point: yield_cost_constant")
    hif_plant_pkg__hif_plant__driver__efficiency: float = Field(default=0.35, description="Entry point: efficiency")
    hif_plant_pkg__hif_plant__driver__energy: float = Field(default=14286000.0, description="Entry point: energy")
    hif_plant_pkg__hif_plant__driver__lifetime_shots: float = Field(default=6000000000.0, description="Entry point: lifetime_shots")
    hif_plant_pkg__hif_plant__lcoe_calc__construction_years: float = Field(default=5.0, description="Entry point: construction_years")
    hif_plant_pkg__hif_plant__lcoe_calc__operational_years: float = Field(default=40.0, description="Entry point: operational_years")
    hif_plant_pkg__hif_plant__target_factory__cost_per_target: float = Field(default=10.0, description="Entry point: cost_per_target")

    model_config = {"frozen": True, "extra": "forbid"}
