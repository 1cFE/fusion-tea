from pydantic import Field
from simkit.config.schema import MultiOutput

class PVModuleCostCalcOutput(MultiOutput):
    """Multi-output container for PVModuleCostCalc.

Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:27
    """
    material_cost: float = Field(description="material_cost output")
    fab_cost: float = Field(description="fab_cost output")
    install_cost: float = Field(description="install_cost output")
    total_cost: float = Field(description="total_cost output")
    idiot_index: float = Field(description="idiot_index output")
