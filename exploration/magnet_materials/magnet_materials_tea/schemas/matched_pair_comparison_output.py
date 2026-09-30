from pydantic import Field
from simkit.config.schema import MultiOutput

class Matched_Pair_ComparisonOutput(MultiOutput):
    """Multi-output container for Matched_Pair_Comparison.

Compares the two supplied windings at one duty. rankable = all_pass_nb3sn*all_pass_rebco, where each all_pass = acceptance_pass*fit_pass*cu_pass*steel_pass*capacity_pass (acceptance_pass already requires a supported status); pair_status = status_nb3sn when both statuses are supported (non-zero), else 0; cost_difference = annualized_rebco - annualized_nb3sn; breakeven_rebco_price_per_m = rebco_price_per_m - cost_difference/(crf*rebco_element_length); breakeven_rebco_price_per_kAm = breakeven_rebco_price_per_m/(rebco_ic_tape_op/1000), per kA*m of tape critical current at the operating field and conductor temperature. Break-even prices are reported for every pair but are meaningful only when rankable = 1. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.8 (D2, D7); contract sections 7-8. **Basis**: [AGENT] cost is linear in the REBCO price per metre, so the break-even price follows from recorded outputs. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/matched_pair_comparison_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/magnet_conductor_alternatives.sysml:247
    """
    breakeven_rebco_price_per_m: float = Field(description="breakeven_rebco_price_per_m output")
    breakeven_rebco_price_per_kAm: float = Field(description="breakeven_rebco_price_per_kAm output")
    pair_status: float = Field(description="pair_status output")
    cost_difference: float = Field(description="cost_difference output")
    rankable: float = Field(description="rankable output")
