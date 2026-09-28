from pydantic import Field
from simkit.config.schema import MultiOutput

class Cold_Load_SumOutput(MultiOutput):
    """Multi-output container for Cold_Load_Sum.

Assemble cold MW once; uplift only the legacy nuclear/fixed and
explicit structure-nuclear terms, never the enumerated inventory.
Native completion requires finite positive rho_structure and finite
nonnegative q_nuc_structure, m_support and q_inventory_cold.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D5. **Basis**: heat balance, W to MW conversion.
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:62
    """
    q_structure_nuclear: float = Field(description="q_structure_nuclear output")
    p_cold: float = Field(description="p_cold output")
