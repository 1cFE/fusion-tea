from pydantic import BaseModel, Field


class CombinationsCirculatorPurchaseParams(BaseModel):
    """Parameters from combinations_circulator_purchase.

    Generated from SysML calculation definitions.
    """
    combinations_circulator_purchase__circulator_purchase__circulator_capacity__assumed_supported: bool = Field(default=1.0, description="Entry point: assumed_supported")
    combinations_circulator_purchase__circulator_purchase__circulator_capacity__demand: float = Field(default=6.26003337158886, description="Entry point: demand")
    combinations_circulator_purchase__circulator_purchase__circulator_capacity__demand_available: bool = Field(default=1.0, description="Entry point: demand_available")
    combinations_circulator_purchase__circulator_purchase__circulator_capacity__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")
    combinations_circulator_purchase__circulator_purchase__circulator_equipment__estimate_mode: float = Field(default=0.0, description="Entry point: estimate_mode")
    combinations_circulator_purchase__circulator_purchase__circulator_equipment__price_factor: float = Field(default=1.0, description="Entry point: price_factor")
    combinations_circulator_purchase__circulator_purchase__circulator_equipment__reference_cost: float = Field(default=442174444.74911624, description="Entry point: reference_cost")
    combinations_circulator_purchase__circulator_purchase__circulator_equipment__reference_quantity: float = Field(default=6.26003337158886, description="Entry point: reference_quantity")
    combinations_circulator_purchase__circulator_purchase__circulator_equipment__selected_rating: float = Field(default=8.0, description="Entry point: selected_rating")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
