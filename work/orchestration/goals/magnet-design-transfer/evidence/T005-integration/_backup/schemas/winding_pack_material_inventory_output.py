from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Pack_Material_InventoryOutput(MultiOutput):
    """Multi-output container for Winding_Pack_Material_Inventory.

Non-tape winding-pack inventory and procurement, excluding casing and extra cold equipment.
Normative manual-completion equations: helium_density = helium_pressure / (helium_gas_constant * temperature); mass_i = volume_in * f_i * rho_i for copper, solder, steel and helium; cost_i = mass_i * price_i; material_cost = cost_copper + cost_solder + cost_steel + cost_helium; tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium).
Units: volume and tape_volume m^3; densities kg/m^3; masses kg; pressure Pa; temperature K; gas constant J/(kg K); prices dollars/kg; costs dollars. Tape is purchased separately as composite tape, with no second substrate/stabilizer charge. Fixed composition and ideal-gas helium are transfer approximations; inter-pancake insulation is unquantified and omitted.
Domain: every input and output finite; volume_in >= 0; each fraction >= 0 and < 1, with sum < 1; densities, pressure, temperature and gas constant > 0; prices >= 0. The typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic, and refuses non-finite results. Arithmetic validity does not qualify an arbitrary temperature or composition.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md; knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Reference**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md (20 K, 15/20 bar); knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Last Updated**: 2026-09-13

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:4
    """
    tape_volume: float = Field(description="tape_volume output")
    mass_steel: float = Field(description="mass_steel output")
    mass_helium: float = Field(description="mass_helium output")
    cost_copper: float = Field(description="cost_copper output")
    mass_copper: float = Field(description="mass_copper output")
    cost_helium: float = Field(description="cost_helium output")
    mass_solder: float = Field(description="mass_solder output")
    cost_steel: float = Field(description="cost_steel output")
    material_cost: float = Field(description="material_cost output")
    helium_density: float = Field(description="helium_density output")
    cost_solder: float = Field(description="cost_solder output")
