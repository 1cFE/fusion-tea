"""Auto-generated implementation for Conductor_Strain.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:197

SysML Expressions:
    eps_cond = f_cond * sigma_wp / E_wp
    
Documentation:
Strain in the HTS tape stack [1] (WI-036, D4):

  eps_cond = f_cond * sigma_wp / E_wp

The conductor is checked separately from the structure because every
surveyed HTS fusion design -- the Stellaris source included -- runs
two checks, a stress check against the structure and a strain check
against the conductor, and this model previously ran only the first.
REBCO is brittle; its performance is governed by strain.

f_cond is a load-sharing factor calibrated from the source's own
reported pair: the winding pack peaks at ~600 MPa von Mises while the
HTS stack strain stays below 0.2%, so the stack sees about two-thirds
of the pack-average strain -- the soldered Cu jacket offloads it.
Both anchors are printed *bounds* taken as values, so the operand
over-estimates strain; that conservatism is disclosed, not corrected.

Honest limit: von Mises is not uniaxial stress and a pack-level stress
is not local tape stress. This is a composition standing in for a
finite-element result the source does not publish, calibrated from the
source's own numbers rather than assumed (the k_sigma convention
applied to a second quantity).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
*Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
stack peak strain below 0.2% "within acceptable limits, even when
adding strain from bending"); output.md:173,197 (Barth, Mondonico
& Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
strain, there are no discernible differences")
*Basis**: pack-average strain scaled by a sourced load-sharing
factor; concept-agnostic (MR-3)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.conductor_strain import Conductor_StrainInput


def run_conductor_strain(inputs: Conductor_StrainInput) -> float:
    """Execute Conductor_Strain calculation.

Strain in the HTS tape stack [1] (WI-036, D4):

  eps_cond = f_cond * sigma_wp / E_wp

The conductor is checked separately from the structure because every
surveyed HTS fusion design -- the Stellaris source included -- runs
two checks, a stress check against the structure and a strain check
against the conductor, and this model previously ran only the first.
REBCO is brittle; its performance is governed by strain.

f_cond is a load-sharing factor calibrated from the source's own
reported pair: the winding pack peaks at ~600 MPa von Mises while the
HTS stack strain stays below 0.2%, so the stack sees about two-thirds
of the pack-average strain -- the soldered Cu jacket offloads it.
Both anchors are printed *bounds* taken as values, so the operand
over-estimates strain; that conservatism is disclosed, not corrected.

Honest limit: von Mises is not uniaxial stress and a pack-level stress
is not local tape stress. This is a composition standing in for a
finite-element result the source does not publish, calibrated from the
source's own numbers rather than assumed (the k_sigma convention
applied to a second quantity).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
*Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
stack peak strain below 0.2% "within acceptable limits, even when
adding strain from bending"); output.md:173,197 (Barth, Mondonico
& Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
strain, there are no discernible differences")
*Basis**: pack-average strain scaled by a sourced load-sharing
factor; concept-agnostic (MR-3)

SysML Source: root-0/analyses/mfe_magnet_field.sysml:197

SysML Expressions:
    eps_cond = f_cond * sigma_wp / E_wp
    
Documentation:
Strain in the HTS tape stack [1] (WI-036, D4):

  eps_cond = f_cond * sigma_wp / E_wp

The conductor is checked separately from the structure because every
surveyed HTS fusion design -- the Stellaris source included -- runs
two checks, a stress check against the structure and a strain check
against the conductor, and this model previously ran only the first.
REBCO is brittle; its performance is governed by strain.

f_cond is a load-sharing factor calibrated from the source's own
reported pair: the winding pack peaks at ~600 MPa von Mises while the
HTS stack strain stays below 0.2%, so the stack sees about two-thirds
of the pack-average strain -- the soldered Cu jacket offloads it.
Both anchors are printed *bounds* taken as values, so the operand
over-estimates strain; that conservatism is disclosed, not corrected.

Honest limit: von Mises is not uniaxial stress and a pack-level stress
is not local tape stress. This is a composition standing in for a
finite-element result the source does not publish, calibrated from the
source's own numbers rather than assumed (the k_sigma convention
applied to a second quantity).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
*Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
stack peak strain below 0.2% "within acceptable limits, even when
adding strain from bending"); output.md:173,197 (Barth, Mondonico
& Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
strain, there are no discernible differences")
*Basis**: pack-average strain scaled by a sourced load-sharing
factor; concept-agnostic (MR-3)

Args:
    inputs: Input parameters validated against Conductor_StrainInput schema

Returns:
    float: eps_cond

Example:
    >>> inputs = Conductor_StrainInput(...)
    >>> result = run_conductor_strain(inputs)
    """
    return ((inputs.f_cond * inputs.sigma_wp) / inputs.E_wp)
