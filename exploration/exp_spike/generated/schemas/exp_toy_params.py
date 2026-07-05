from pydantic import BaseModel, Field


class ExpToyParams(BaseModel):
    """Parameters from exp_toy.sysml.

    Generated from SysML calculation definitions.
    """
    exp_toy__exp_plant__reactivity_calc__t_kev: float = Field(default=10.0, description="Entry point: t_kev")
    exp_toy__exp_plant__reactivity_calc__c_coeff: float = Field(default=6.4e-14, description="Entry point: c_coeff")
    exp_toy__exp_plant__reactivity_calc__b_gamow: float = Field(default=19.98, description="Entry point: b_gamow")
    exp_toy__exp_plant__doublings_calc__target_gain: float = Field(default=100.0, description="Entry point: target_gain")
    exp_toy__exp_plant__exp_control_calc__exponent_arg: float = Field(default=10.0, description="Entry point: exponent_arg")

    model_config = {"frozen": True, "extra": "forbid"}
