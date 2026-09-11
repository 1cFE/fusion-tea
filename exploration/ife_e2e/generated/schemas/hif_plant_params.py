from pydantic import BaseModel, Field


class HifPlantParams(BaseModel):
    """Parameters from hif_plant.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__availability: float = Field(default=0.9, description="Entry point: availability")
    hif_plant_pkg__hif_plant__chamber__blanket_energy_multiple: float = Field(default=1.15, description="Entry point: blanket_energy_multiple")
    hif_plant_pkg__hif_plant__chamber__yield_cost_constant: float = Field(default=5000000.0, description="Entry point: yield_cost_constant")
    hif_plant_pkg__hif_plant__discount_rate: float = Field(default=0.08, description="Entry point: discount_rate")
    hif_plant_pkg__hif_plant__driver__beam_energy_mj: float = Field(default=5.0, description="Entry point: beam_energy_mj")
    hif_plant_pkg__hif_plant__driver__num_chambers: float = Field(default=1.0, description="Entry point: num_chambers")
    hif_plant_pkg__hif_plant__frequency: float = Field(default=4.6, description="Entry point: frequency")
    hif_plant_pkg__hif_plant__gain: float = Field(default=87.0, description="Entry point: gain")
    hif_plant_pkg__hif_plant__om_cost_constant: float = Field(default=65.0, description="Entry point: om_cost_constant")
    hif_plant_pkg__hif_plant__plant_cost_constant: float = Field(default=2000.0, description="Entry point: plant_cost_constant")
    hif_plant_pkg__hif_plant__reactor_units: float = Field(default=1.0, description="Entry point: reactor_units")
    hif_plant_pkg__hif_plant__target_factory__cost_per_target: float = Field(default=10.0, description="Entry point: cost_per_target")
    hif_plant_pkg__hif_plant__target_factory_direct_cost_billions: float = Field(default=0.1, description="Entry point: target_factory_direct_cost_billions")
    hif_plant_pkg__hif_plant__thermal_efficiency: float = Field(default=0.45, description="Entry point: thermal_efficiency")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
