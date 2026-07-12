from pydantic import Field
from simkit.config.schema import MultiOutput

class BatteryPackCostCalcOutput(MultiOutput):
    """Multi-output container for BatteryPackCostCalc.

Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:96
    """
    material_cost: float = Field(description="material_cost output")
    fab_cost: float = Field(description="fab_cost output")
    install_cost: float = Field(description="install_cost output")
    total_cost: float = Field(description="total_cost output")
    idiot_index: float = Field(description="idiot_index output")
