from pydantic import Field
from simkit.config.schema import MultiOutput

class InverterCostCalcOutput(MultiOutput):
    """Multi-output container for InverterCostCalc.

Cost calculation for string inverters.
Material cost driven by power rating.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:50
    """
    material_cost: float = Field(description="material_cost output")
    fab_cost: float = Field(description="fab_cost output")
    install_cost: float = Field(description="install_cost output")
    total_cost: float = Field(description="total_cost output")
    idiot_index: float = Field(description="idiot_index output")
