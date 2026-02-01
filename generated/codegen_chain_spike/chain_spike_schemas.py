"""Fusion-specific Pydantic schemas for TEAx pipeline integration.

NOTE: This file is generated from a reference template. It defines the shared
FusionParams schema that many calculation modules use as input.

Source: PyFECONS CATF/mfe/DefineInputs.py
"""

from pydantic import BaseModel, Field


class FusionParams(BaseModel):
    """Fusion reactor parameters for CATF MFE design.

    Source: PyFECONS CATF/mfe/DefineInputs.py
    """

    p_fusion: float = Field(..., gt=0, description="Total fusion power [MW]")
    p_input: float = Field(..., ge=0, description="Auxiliary heating power [MW]")
    m_neutron: float = Field(
        ..., ge=1.0, le=1.5, description="Neutron multiplication factor"
    )
    eta_thermal: float = Field(
        ..., gt=0, le=0.5, description="Thermal conversion efficiency"
    )
    f_pump: float = Field(..., ge=0, description="Pump power fraction")
    eta_pump: float = Field(..., gt=0, le=1.0, description="Pump efficiency")
    f_subsystem: float = Field(..., ge=0, description="Subsystem power fraction")
    eta_direct: float = Field(
        ..., ge=0, le=1.0, description="Direct conversion efficiency"
    )


__all__ = [
    "FusionParams",
]
