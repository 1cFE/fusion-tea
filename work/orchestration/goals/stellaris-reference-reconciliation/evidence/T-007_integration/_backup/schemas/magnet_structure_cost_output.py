from pydantic import Field
from simkit.config.schema import MultiOutput

class Magnet_Structure_CostOutput(MultiOutput):
    """Multi-output container for Magnet_Structure_Cost.

Electromagnetic support cost, exclusive total or legacy casing basis.
cost=(legacy_casing_fraction*n_coils*m_casing+m_support)*steel_price*f_steel_fab.
The casing output remains an inherited floor diagnostic in total-support mode.
Native domain: every input finite and nonnegative; legacy_casing_fraction in [0,1]; finite nonnegative outputs with no positive product underflow. Historical multiplication order is preserved. effective_all_in_rate=steel_price*f_steel_fab exposes one assumed all-in rate; the factors do not establish measured material/fabrication subtotals.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D1-D2; T-005_structure_basis.md.
*Basis**: inherited 6 dollars/kg times 3 = 18 dollars/kg all-in assumption; unknown price year and manufacturing qualification, no demonstrated duplicate removed or sourced casing/intercoil split.
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:157
    """
    cost: float = Field(description="cost output")
    effective_all_in_rate: float = Field(description="effective_all_in_rate output")
