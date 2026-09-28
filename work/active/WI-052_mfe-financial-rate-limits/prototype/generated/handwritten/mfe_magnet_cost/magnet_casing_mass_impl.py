"""Auto-generated implementation for Magnet_Casing_Mass.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

SysML Expressions:
    m_casing = m_casing_ref * (W_mag / W_mag_ref) ** 0.78
    
Documentation:
Casing steel mass per coil [kg] from the coil set's stored magnetic
energy, anchored at a reference (WI-044):

  m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
law from existing machines" (L607) that Stellarator-PROCESS uses for
the total coil support-structure mass because "the total mass is a
good proxy, both for the cost and the support structure complexity".
The source prints no units for the constant, so the constant is
absorbed by the anchor: m_casing_ref is the instance's casing mass at
its reference stored energy and only the exponent is carried. The
anchor keeps whatever seam the instance's reference carries (for
Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
design D5); the scale responds to the bore through W_mag and the seam
stays named at the binding. Disclosed limit (the source's own): the
law "does not show whether the design point has local unsupportable
forces" (L609).

*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
output.md L607 (the empirical law and its role), L609 (its limit)
*Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
concept-agnostic (MR-3) -- all values bound by instances
"""

AUTO_IMPLEMENTED = True

from wi052_probe.modules.mfe_magnet_cost.magnet_casing_mass import Magnet_Casing_MassInput


def run_magnet_casing_mass(inputs: Magnet_Casing_MassInput) -> float:
    """Execute Magnet_Casing_Mass calculation.

Casing steel mass per coil [kg] from the coil set's stored magnetic
energy, anchored at a reference (WI-044):

  m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
law from existing machines" (L607) that Stellarator-PROCESS uses for
the total coil support-structure mass because "the total mass is a
good proxy, both for the cost and the support structure complexity".
The source prints no units for the constant, so the constant is
absorbed by the anchor: m_casing_ref is the instance's casing mass at
its reference stored energy and only the exponent is carried. The
anchor keeps whatever seam the instance's reference carries (for
Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
design D5); the scale responds to the bore through W_mag and the seam
stays named at the binding. Disclosed limit (the source's own): the
law "does not show whether the design point has local unsupportable
forces" (L609).

*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
output.md L607 (the empirical law and its role), L609 (its limit)
*Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
concept-agnostic (MR-3) -- all values bound by instances

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

SysML Expressions:
    m_casing = m_casing_ref * (W_mag / W_mag_ref) ** 0.78
    
Documentation:
Casing steel mass per coil [kg] from the coil set's stored magnetic
energy, anchored at a reference (WI-044):

  m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
law from existing machines" (L607) that Stellarator-PROCESS uses for
the total coil support-structure mass because "the total mass is a
good proxy, both for the cost and the support structure complexity".
The source prints no units for the constant, so the constant is
absorbed by the anchor: m_casing_ref is the instance's casing mass at
its reference stored energy and only the exponent is carried. The
anchor keeps whatever seam the instance's reference carries (for
Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
design D5); the scale responds to the bore through W_mag and the seam
stays named at the binding. Disclosed limit (the source's own): the
law "does not show whether the design point has local unsupportable
forces" (L609).

*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
output.md L607 (the empirical law and its role), L609 (its limit)
*Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
concept-agnostic (MR-3) -- all values bound by instances

Args:
    inputs: Input parameters validated against Magnet_Casing_MassInput schema

Returns:
    float: m_casing

Example:
    >>> inputs = Magnet_Casing_MassInput(...)
    >>> result = run_magnet_casing_mass(inputs)
    """
    return (inputs.m_casing_ref * ((inputs.W_mag / inputs.W_mag_ref) ** 0.78))
