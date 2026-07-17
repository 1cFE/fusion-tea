from pydantic import BaseModel, Field


class MfePlantParams(BaseModel):
    """Parameters from mfe_plant.sysml.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__blanket__structure_factor: float = Field(default=1.0, description="Entry point: structure_factor")
    stellarator_09__stellaris__blanket__unit_cost: float = Field(default=600000.0, description="Entry point: unit_cost")
    stellarator_09__stellaris__blanket_cost__alpha: float = Field(default=0.6, description="Entry point: alpha")
    stellarator_09__stellaris__blanket_cost__p_th_ref: float = Field(default=2500.0, description="Entry point: p_th_ref")
    stellarator_09__stellaris__contingency__direct_subtotal: float = Field(default=1.0, description="Entry point: direct_subtotal")
    stellarator_09__stellaris__divertor_cost__alpha: float = Field(default=0.5, description="Entry point: alpha")
    stellarator_09__stellaris__divertor_cost__p_th_ref: float = Field(default=1000.0, description="Entry point: p_th_ref")
    stellarator_09__stellaris__electric_cost__n_mod: float = Field(default=1.0, description="Entry point: n_mod")
    stellarator_09__stellaris__electric_plant__cost_per_mw: float = Field(default=86400.0, description="Entry point: cost_per_mw")
    stellarator_09__stellaris__geom__pi: float = Field(default=3.14159265358979, description="Entry point: pi")
    stellarator_09__stellaris__heat_rejection__cost_per_mw: float = Field(default=35060.0, description="Entry point: cost_per_mw")
    stellarator_09__stellaris__heat_rejection_cost__n_mod: float = Field(default=1.0, description="Entry point: n_mod")
    stellarator_09__stellaris__indirect__direct_cost: float = Field(default=1.0, description="Entry point: direct_cost")
    stellarator_09__stellaris__indirect__reference_construction_time: float = Field(default=6.0, description="Entry point: reference_construction_time")
    stellarator_09__stellaris__lcoe_calc__total_capital: float = Field(default=1.0, description="Entry point: total_capital")
    stellarator_09__stellaris__magnet__B: float = Field(default=5.86, description="Entry point: B")
    stellarator_09__stellaris__magnet__G: float = Field(default=78.95683520871486, description="Entry point: G")
    stellarator_09__stellaris__magnet__R0: float = Field(default=12.7, description="Entry point: R0")
    stellarator_09__stellaris__magnet__coil_markup: float = Field(default=5.87, description="Entry point: coil_markup")
    stellarator_09__stellaris__magnet__cost_per_kAm: float = Field(default=50.0, description="Entry point: cost_per_kAm")
    stellarator_09__stellaris__magnet_cost__mu0: float = Field(default=1.25663706212e-06, description="Entry point: mu0")
    stellarator_09__stellaris__misc_cost__n_mod: float = Field(default=1.0, description="Entry point: n_mod")
    stellarator_09__stellaris__misc_plant__cost_per_mw: float = Field(default=52590.0, description="Entry point: cost_per_mw")
    stellarator_09__stellaris__power_supplies__base: float = Field(default=80000000.0, description="Entry point: base")
    stellarator_09__stellaris__power_supplies_cost__alpha: float = Field(default=0.7, description="Entry point: alpha")
    stellarator_09__stellaris__power_supplies_cost__p_et_ref: float = Field(default=1100.0, description="Entry point: p_et_ref")
    stellarator_09__stellaris__rb__pi: float = Field(default=3.14159265358979, description="Entry point: pi")
    stellarator_09__stellaris__shield__shield_scale: float = Field(default=1.0, description="Entry point: shield_scale")
    stellarator_09__stellaris__shield__unit_cost: float = Field(default=740000.0, description="Entry point: unit_cost")
    stellarator_09__stellaris__shield_cost__alpha: float = Field(default=0.6, description="Entry point: alpha")
    stellarator_09__stellaris__shield_cost__p_th_ref: float = Field(default=2500.0, description="Entry point: p_th_ref")
    stellarator_09__stellaris__structure__unit_cost: float = Field(default=150000.0, description="Entry point: unit_cost")
    stellarator_09__stellaris__structure_cost__alpha: float = Field(default=0.5, description="Entry point: alpha")
    stellarator_09__stellaris__structure_cost__p_et_ref: float = Field(default=1100.0, description="Entry point: p_et_ref")
    stellarator_09__stellaris__turbine__cost_per_mw: float = Field(default=202840.0, description="Entry point: cost_per_mw")
    stellarator_09__stellaris__turbine_cost__n_mod: float = Field(default=1.0, description="Entry point: n_mod")
    stellarator_09__stellaris__vessel__unit_cost: float = Field(default=720000.0, description="Entry point: unit_cost")
    stellarator_09__stellaris__vessel_cost__alpha: float = Field(default=0.6, description="Entry point: alpha")
    stellarator_09__stellaris__vessel_cost__p_et_ref: float = Field(default=1100.0, description="Entry point: p_et_ref")

    model_config = {"frozen": True, "extra": "forbid"}
