from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Inventory_and_CostOutput(MultiOutput):
    """Multi-output container for Winding_Inventory_and_Cost.

Inventory and cost of the supplied winding; never from demand. conductor_length = turns*coils*turn_length; element_length = n_elements*conductor_length; element_mass = element_area*1e-6*conductor_length*element_density (element_area is the total element area per turn, mm2); cu_mass = cu_space*(1 - cu_void)*1e-6*conductor_length*rho_cu; steel_mass = steel_area*1e-6*conductor_length*rho_steel; solder_mass = solder_area*1e-6*conductor_length*rho_solder; sc_cost = element_length*element_price_per_m; materials_cost = cu_mass*price_cu + steel_mass*price_steel + solder_mass*price_solder; manufacturing_cost = conductor_length*manufacturing_per_m; winding_capital = sc_cost + materials_cost + manufacturing_cost; ampere_metres = turn_current*conductor_length. Cabling twist is ignored (contract section 7). **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.4; contract section 7 (cost accounting and boundary). **Basis**: [AGENT] partial accounting within the evaluated categories; winding labour, heat treatment, stacking, case and structure excluded (contract section 7). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_inventory_and_cost_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:132
    """
    cu_mass: float = Field(description="cu_mass output")
    sc_cost: float = Field(description="sc_cost output")
    winding_capital: float = Field(description="winding_capital output")
    manufacturing_cost: float = Field(description="manufacturing_cost output")
    conductor_length: float = Field(description="conductor_length output")
    element_length: float = Field(description="element_length output")
    materials_cost: float = Field(description="materials_cost output")
    element_mass: float = Field(description="element_mass output")
    steel_mass: float = Field(description="steel_mass output")
    solder_mass: float = Field(description="solder_mass output")
    ampere_metres: float = Field(description="ampere_metres output")
