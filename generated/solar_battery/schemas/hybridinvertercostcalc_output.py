from pydantic import Field
from simkit.config.schema import MultiOutput

class HybridInverterCostCalcOutput(MultiOutput):
    """Multi-output container for HybridInverterCostCalc.

Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:119
    """
    material_cost: float = Field(description="material_cost output")
    fab_cost: float = Field(description="fab_cost output")
    install_cost: float = Field(description="install_cost output")
    total_cost: float = Field(description="total_cost output")
    idiot_index: float = Field(description="idiot_index output")
