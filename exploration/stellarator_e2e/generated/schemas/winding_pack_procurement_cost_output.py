from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Pack_Procurement_CostOutput(MultiOutput):
    """Multi-output container for Winding_Pack_Procurement_Cost.

Additive full-composite tape procurement, external pack materials and winding operations. Casing and primary support remain separate accounts. Normative manual equations: tape_area = tape_width * tape_thickness; tape_length = tape_volume_in / tape_area; tape_cost = tape_length * tape_price_per_m; conductor_length = n_coils * I_coil * f_set * c_coil / turn_current; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Units: tape_volume_in m^3; width and full composite thickness m; tape_price_per_m dollars per metre of that complete purchased tape; tape_length individual tape metres. I_coil ampere-turns; turn_current A; conductor_length composite-conductor metres; winding_rate_1990 dollars1990/conductor-m; other costs dollars. The existing volume input already includes field-envelope quantity scaling. Never apply another envelope factor to tape price. Tape substrate/stabilizer are included in the complete tape purchase; external copper jacket, solder, steel and helium are separate. Winding operations are an inherited transfer assumption, not a complete factory quote. Insulation, spares, yield and integer tape counts are unquantified.
Domain: all inputs and outputs finite; n_coils, c_coil, turn_current, tape_width, tape_thickness, cost_escalation and nonplanar_factor > 0; I_coil, tape_volume_in, tape_price_per_m, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Computed tape_area finite and positive; positive volume requires positive tape_length; positive length and price require positive tape_cost. Typed manual completion raises calculation- and quantity-named ValueError before invalid arithmetic and refuses nonfinite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: work/active/WI-060_tape-procurement-quantity-basis/design.md (volume/cross-section identity and conditional construction); knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42
    """
    winding_fabrication_cost: float = Field(description="winding_fabrication_cost output")
    tape_length: float = Field(description="tape_length output")
    cost: float = Field(description="cost output")
    tape_cost: float = Field(description="tape_cost output")
    conductor_length: float = Field(description="conductor_length output")
