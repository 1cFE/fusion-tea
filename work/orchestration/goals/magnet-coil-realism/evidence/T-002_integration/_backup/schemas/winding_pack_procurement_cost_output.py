from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Pack_Procurement_CostOutput(MultiOutput):
    """Multi-output container for Winding_Pack_Procurement_Cost.

Additive composite-tape procurement, non-tape material procurement and winding operations. Casing and primary structure remain separate accounts. Normative manual-completion equations: K = n_coils * I_coil * f_set * c_coil / 1000 [kA m]; tape_cost = K * cost_per_kAm; conductor_length = 1000 * K / turn_current [m]; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Inputs: n_coils and f_set dimensionless; I_coil ampere-turns; c_coil m; cost_per_kAm dollars/(kA m); turn_current A; winding_rate_1990 dollars1990/m; escalation and nonplanar factor dimensionless; material_cost_in dollars. Outputs: costs dollars, conductor_length m of composite conductor (not tape metres). Winding operations are not a complete factory quote or a labor-only rate. Steel sheath charges would overlap explicit pack steel; unresolved fixed cable and insulation quantities are omitted. Rate transfer to REBCO is an assumption.
Domain: every input and output finite; n_coils, c_coil, turn_current, cost_escalation and nonplanar_factor > 0; I_coil, cost_per_kAm, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic and refuses non-finite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-13

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42
    """
    winding_fabrication_cost: float = Field(description="winding_fabrication_cost output")
    cost: float = Field(description="cost output")
    tape_cost: float = Field(description="tape_cost output")
    conductor_length: float = Field(description="conductor_length output")
