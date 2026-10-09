from pydantic import Field
from simkit.config.schema import MultiOutput

class Pack_Field_ChecksOutput(MultiOutput):
    """Multi-output container for Pack_Field_Checks.

Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:29
    """
    R_over_sqrt_A_wp: float = Field(description="R_over_sqrt_A_wp output")
    ampere_floor: float = Field(description="ampere_floor output")
    ampere_floor_margin: float = Field(description="ampere_floor_margin output")
