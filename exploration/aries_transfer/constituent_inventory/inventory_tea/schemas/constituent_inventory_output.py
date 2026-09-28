from pydantic import Field
from simkit.config.schema import MultiOutput

class Constituent_InventoryOutput(MultiOutput):
    """Multi-output container for Constituent_Inventory.

constituent_volume = region_volume_in * fraction_in; known_mass = constituent_volume * density_in; source_price_subtotal = known_mass * unit_price_in. Units m3, kg/m3 and source-year dollars/kg yield kg and source-year dollars. Finite nonnegative inputs, fraction in [0,1], density strictly positive. Reject nonfinite outputs. A missing density or price is not zero; an unquantified constituent is represented outside this calculation. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

SysML Source: root-0/sector_constituent_inventory.sysml:10
    """
    constituent_volume: float = Field(description="constituent_volume output")
    known_mass: float = Field(description="known_mass output")
    source_price_subtotal: float = Field(description="source_price_subtotal output")
