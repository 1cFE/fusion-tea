from pydantic import Field
from simkit.config.schema import MultiOutput

class Three_Constituent_Recipe_SummaryOutput(MultiOutput):
    """Multi-output container for Three_Constituent_Recipe_Summary.

represented_fraction = fraction_1_in + fraction_2_in + fraction_3_in; unquantified_volume = region_volume_in * unquantified_fraction_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in. Units m3, kg and same-source-year dollars; no currency conversion. Finite nonnegative inputs, each fraction in [0,1]; sum of represented and unquantified fractions must equal one within 1e-12, an arithmetic closure tolerance. Check closure even at zero volume. Reject nonfinite outputs. Three explicitly represented material children plus an unquantified-volume complement; their mass and price coverage remain partial. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

SysML Source: root-0/sector_constituent_inventory.sysml:20
    """
    unquantified_volume: float = Field(description="unquantified_volume output")
    source_price_subtotal: float = Field(description="source_price_subtotal output")
    known_mass: float = Field(description="known_mass output")
    represented_fraction: float = Field(description="represented_fraction output")
