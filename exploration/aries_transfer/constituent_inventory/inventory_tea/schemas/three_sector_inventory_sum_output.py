from pydantic import Field
from simkit.config.schema import MultiOutput

class Three_Sector_Inventory_SumOutput(MultiOutput):
    """Multi-output container for Three_Sector_Inventory_Sum.

The three supplied lateral coverages must each lie in [0,1] and sum to one within 1e-12, including zero-volume cases. Refuse inconsistent supplied partitions; never normalize them. This establishes arithmetic partition closure, not geometric nonoverlap qualification.

volume = volume_1_in + volume_2_in + volume_3_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in; unquantified_volume = unquantified_volume_1_in + unquantified_volume_2_in + unquantified_volume_3_in. Inputs and outputs finite nonnegative. Units m3, kg and same-source-year dollars; no currency conversion. Sums three nonoverlapping lateral layer occurrences, not arbitrary stacked area fractions. Partial source-price sum is not installed capital. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

SysML Source: root-0/sector_constituent_inventory.sysml:38
    """
    known_mass: float = Field(description="known_mass output")
    unquantified_volume: float = Field(description="unquantified_volume output")
    source_price_subtotal: float = Field(description="source_price_subtotal output")
    volume: float = Field(description="volume output")
