from pydantic import BaseModel, Field


class PlasmaIntegrationParams(BaseModel):
    """Parameters from plasma_integration.

    Generated from SysML calculation definitions.
    """
    aries_cs_plasma_integration__plasma__amplitude: float = Field(default=5e+20, description="Entry point: amplitude")
    aries_cs_plasma_integration__plasma__density_profile_exponent: float = Field(default=1.0, description="Entry point: density_profile_exponent")
    aries_cs_plasma_integration__plasma__density_radial_exponent: float = Field(default=12.0, description="Entry point: density_radial_exponent")
    aries_cs_plasma_integration__plasma__deuterium_fraction: float = Field(default=0.5, description="Entry point: deuterium_fraction")
    aries_cs_plasma_integration__plasma__edge_ratio: float = Field(default=0.1, description="Entry point: edge_ratio")
    aries_cs_plasma_integration__plasma__field: float = Field(default=5.7, description="Entry point: field")
    aries_cs_plasma_integration__plasma__helium_fraction: float = Field(default=0.0335, description="Entry point: helium_fraction")
    aries_cs_plasma_integration__plasma__hollowness: float = Field(default=0.66, description="Entry point: hollowness")
    aries_cs_plasma_integration__plasma__sample_rho: float = Field(default=0.5, description="Entry point: sample_rho")
    aries_cs_plasma_integration__plasma__temperature_axis: float = Field(default=11.83, description="Entry point: temperature_axis")
    aries_cs_plasma_integration__plasma__temperature_edge: float = Field(default=0.2, description="Entry point: temperature_edge")
    aries_cs_plasma_integration__plasma__temperature_profile_exponent: float = Field(default=1.0, description="Entry point: temperature_profile_exponent")
    aries_cs_plasma_integration__plasma__temperature_radial_exponent: float = Field(default=2.0, description="Entry point: temperature_radial_exponent")
    aries_cs_plasma_integration__plasma__volume: float = Field(default=444.0, description="Entry point: volume")
    aries_cs_plasma_integration__plasma__volume_exponent: float = Field(default=2.0, description="Entry point: volume_exponent")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
