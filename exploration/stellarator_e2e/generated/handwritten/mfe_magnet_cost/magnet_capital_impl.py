"""Auto-generated implementation for Magnet_Capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:137

SysML Expressions:
    capital_cost = winding_cost + structure_cost_in
    
Documentation:
CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/active/WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack and magnet-structure sub-accounts
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_cost.magnet_capital import Magnet_CapitalInput


def run_magnet_capital(inputs: Magnet_CapitalInput) -> float:
    """Execute Magnet_Capital calculation.

CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/active/WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack and magnet-structure sub-accounts

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:137

SysML Expressions:
    capital_cost = winding_cost + structure_cost_in
    
Documentation:
CAS22.1.3 magnet account rollup (WI-035 D6): the decomposed magnet
capital is the sum of the separately sized sub-accounts. Kept as a
calc def so the plant's magnet.capital_cost redefinition stays a
reference binding (the codegen-proven WI-021 pattern), not an
arithmetic redefinition expression (dropped by the pinned codegen,
WI-030).

*Source**: work/active/WI-035_magnet-closure/design.md
*Ref**: design D6 (rollup + comparison channel); design Risk 1
(redefinition envelope)
*Basis**: sum of winding-pack and magnet-structure sub-accounts

Args:
    inputs: Input parameters validated against Magnet_CapitalInput schema

Returns:
    float: capital_cost

Example:
    >>> inputs = Magnet_CapitalInput(...)
    >>> result = run_magnet_capital(inputs)
    """
    return (inputs.winding_cost + inputs.structure_cost_in)
