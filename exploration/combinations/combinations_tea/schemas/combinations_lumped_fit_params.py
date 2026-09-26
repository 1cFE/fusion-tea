from pydantic import BaseModel, Field


class CombinationsLumpedFitParams(BaseModel):
    """Parameters from combinations_lumped_fit.

    Generated from SysML calculation definitions.
    """
    combinations_lumped_fit__lumped_fit__divertor_fit__T2_max: float = Field(default=642.0, description="Entry point: T2_max")
    combinations_lumped_fit__lumped_fit__divertor_fit__T2_min: float = Field(default=384.0, description="Entry point: T2_min")
    combinations_lumped_fit__lumped_fit__divertor_fit__T_hot: float = Field(default=973.15, description="Entry point: T_hot")
    combinations_lumped_fit__lumped_fit__divertor_fit__T_offset_fit: float = Field(default=273.0, description="Entry point: T_offset_fit")
    combinations_lumped_fit__lumped_fit__divertor_fit__a_fit: float = Field(default=0.1802, description="Entry point: a_fit")
    combinations_lumped_fit__lumped_fit__divertor_fit__b_fit: float = Field(default=0.7823, description="Entry point: b_fit")
    combinations_lumped_fit__lumped_fit__divertor_fit__cycle_live: float = Field(default=1.0, description="Entry point: cycle_live")
    combinations_lumped_fit__lumped_fit__divertor_fit__dT_approach: float = Field(default=20.0, description="Entry point: dT_approach")
    combinations_lumped_fit__lumped_fit__divertor_fit__delta_eta: float = Field(default=0.0, description="Entry point: delta_eta")
    combinations_lumped_fit__lumped_fit__divertor_fit__eta_th_direct: float = Field(default=0.0, description="Entry point: eta_th_direct")
    combinations_lumped_fit__lumped_fit__he_fit__T2_max: float = Field(default=642.0, description="Entry point: T2_max")
    combinations_lumped_fit__lumped_fit__he_fit__T2_min: float = Field(default=384.0, description="Entry point: T2_min")
    combinations_lumped_fit__lumped_fit__he_fit__T_hot: float = Field(default=729.15, description="Entry point: T_hot")
    combinations_lumped_fit__lumped_fit__he_fit__T_offset_fit: float = Field(default=273.0, description="Entry point: T_offset_fit")
    combinations_lumped_fit__lumped_fit__he_fit__a_fit: float = Field(default=0.1802, description="Entry point: a_fit")
    combinations_lumped_fit__lumped_fit__he_fit__b_fit: float = Field(default=0.7823, description="Entry point: b_fit")
    combinations_lumped_fit__lumped_fit__he_fit__cycle_live: float = Field(default=1.0, description="Entry point: cycle_live")
    combinations_lumped_fit__lumped_fit__he_fit__dT_approach: float = Field(default=20.0, description="Entry point: dT_approach")
    combinations_lumped_fit__lumped_fit__he_fit__delta_eta: float = Field(default=0.0, description="Entry point: delta_eta")
    combinations_lumped_fit__lumped_fit__he_fit__eta_th_direct: float = Field(default=0.0, description="Entry point: eta_th_direct")
    combinations_lumped_fit__lumped_fit__pbli_fit__T2_max: float = Field(default=642.0, description="Entry point: T2_max")
    combinations_lumped_fit__lumped_fit__pbli_fit__T2_min: float = Field(default=384.0, description="Entry point: T2_min")
    combinations_lumped_fit__lumped_fit__pbli_fit__T_hot: float = Field(default=1011.15, description="Entry point: T_hot")
    combinations_lumped_fit__lumped_fit__pbli_fit__T_offset_fit: float = Field(default=273.0, description="Entry point: T_offset_fit")
    combinations_lumped_fit__lumped_fit__pbli_fit__a_fit: float = Field(default=0.1802, description="Entry point: a_fit")
    combinations_lumped_fit__lumped_fit__pbli_fit__b_fit: float = Field(default=0.7823, description="Entry point: b_fit")
    combinations_lumped_fit__lumped_fit__pbli_fit__cycle_live: float = Field(default=1.0, description="Entry point: cycle_live")
    combinations_lumped_fit__lumped_fit__pbli_fit__dT_approach: float = Field(default=20.0, description="Entry point: dT_approach")
    combinations_lumped_fit__lumped_fit__pbli_fit__delta_eta: float = Field(default=0.0, description="Entry point: delta_eta")
    combinations_lumped_fit__lumped_fit__pbli_fit__eta_th_direct: float = Field(default=0.0, description="Entry point: eta_th_direct")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
