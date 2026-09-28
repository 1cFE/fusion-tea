from pydantic import BaseModel, Field


class FuelReuseParams(BaseModel):
    """Parameters from fuel_reuse.

    Generated from SysML calculation definitions.
    """
    aries_fuel_reuse__fuel_system__assumed_extraction: float = Field(default=1.0, description="Entry point: assumed_extraction")
    aries_fuel_reuse__fuel_system__decay_constant_s: float = Field(default=1.782785958230312e-09, description="Entry point: decay_constant_s")
    aries_fuel_reuse__fuel_system__dormant_inventory_atoms: float = Field(default=0.0, description="Entry point: dormant_inventory_atoms")
    aries_fuel_reuse__fuel_system__dormant_stock_growth_atoms_s: float = Field(default=0.0, description="Entry point: dormant_stock_growth_atoms_s")
    aries_fuel_reuse__fuel_system__exhaust_recovery: float = Field(default=0.99, description="Entry point: exhaust_recovery")
    aries_fuel_reuse__fuel_system__fusion_load_mw: float = Field(default=2436.0, description="Entry point: fusion_load_mw")
    aries_fuel_reuse__fuel_system__mev_joules: float = Field(default=1.6021766339999998e-13, description="Entry point: mev_joules")
    aries_fuel_reuse__fuel_system__pass_burn_fraction: float = Field(default=0.05, description="Entry point: pass_burn_fraction")
    aries_fuel_reuse__fuel_system__reaction_energy_mev: float = Field(default=17.58, description="Entry point: reaction_energy_mev")
    aries_fuel_reuse__fuel_system__tritium_atom_kg: float = Field(default=5.008267663228036e-27, description="Entry point: tritium_atom_kg")
    aries_fuel_reuse__fuel_system__unused_tbr_placeholder: float = Field(default=0.0, description="Entry point: unused_tbr_placeholder")
    aries_fuel_reuse__processing__assumed_conditions_supported: bool = Field(default=1.0, description="Entry point: assumed_conditions_supported")
    aries_fuel_reuse__processing__flow_available: bool = Field(default=1.0, description="Entry point: flow_available")
    aries_fuel_reuse__processing__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")
    aries_fuel_reuse__processing__selected_rating_atoms_s: float = Field(default=2e+22, description="Entry point: selected_rating_atoms_s")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
