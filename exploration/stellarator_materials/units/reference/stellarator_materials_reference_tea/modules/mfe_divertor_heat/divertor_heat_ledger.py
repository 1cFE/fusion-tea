"""Divertor_Heat_LedgerModule Module Wrapper

TEAx module for Divertor_Heat_Ledger calculation.

Divertor surface-heat ledger, reduced to conservation and one sourced
fixed-geometry case (WI-047):

  p_heat_abs        = p_alpha_heat + p_coupled                       [MW]
  p_sep             = p_heat_abs - p_rad_core                         [MW]
  f_rad_edge        = (f_rad_total * p_heat_abs - p_rad_core) / p_sep  [1]
  f_rad_edge_in_range = f_rad_edge * (1 - f_rad_edge)                 [1] (>= 0 iff in [0, 1])
  p_target_nonrad   = p_heat_abs - f_rad_total * p_heat_abs           [MW]
  q_target_peak     = q_target_ref * p_target_nonrad / p_nonrad_ref   [MW/m^2]
  q_target_peak_area_scaled = q_target_peak * R_ref / R               [MW/m^2] (reported shadow)
  q_target_margin   = q_target_limit - q_target_peak                  [MW/m^2]
  p_heat_operating_minus_installed = p_aux_required - p_installed_coupled [MW]

The absorbed heating is the alpha heating retained in the plasma plus the
sustained operating coupled auxiliary heating, also used by the thermal sum.
The signed required-minus-installed diagnostic uses a separate installed
capacity operand; it does not change the operating heat ledger.
Radiation is a DESTINATION of that heating, never added to it: the core
radiation the sustainment chain composes leaves through the first wall; the
source's radiated fraction f_rad_total is a TOTAL (core plus edge), so the
edge share is derived and reported, not clamped -- a value outside [0, 1]
means the held total and the computed core radiation are inconsistent at
that point, and the in-range channel lets a study count such points.

The peak target flux is the source's own case scaled linearly in the
non-radiated load at FIXED target geometry and transport (q_target_ref at
p_nonrad_ref): no target area, wetted fraction, emissivity, view factor,
erosion or transient enters. A machine of another size keeps the source's
target; the R-scaled output publishes what a target whose wetted length grows
with the major radius would read, and nothing asserts on it. The limit a
concept binds is an adopted steady-state threshold, not an irradiated-
component lifetime. The source's divertor case (a total radiated fraction)
and its first-wall cooling case (100 % radiated) are two load cases and are
never summed. Written p_heat_abs - f * p_heat_abs so the source's own numbers
reproduce to the double (500 - 450 = 50).

WI-065 normative typed manual completion extends the above equations:
  p_rad_total = f_rad_total * p_heat_abs [MW]
  p_rad_edge = p_rad_total - p_rad_core [MW]
  p_target_deposited = target_capture_fraction * p_target_nonrad [MW]
  p_nonrad_uncaptured = p_target_nonrad - p_target_deposited [MW]
  peak_equivalent_area = target_capture_fraction * p_nonrad_ref / q_target_ref [m^2] when q_target_ref > 0, otherwise carrier 0
  peak_equivalent_area_defined = 1 iff q_target_ref > 0, otherwise 0
  f_rad_edge_defined = 1 iff p_sep > 0, otherwise 0 with f_rad_edge carrier 0
  power_account_valid = 1 iff p_rad_edge >= 0 and p_coupled >= 0, otherwise 0
Conservation: p_heat_abs = p_rad_core + p_rad_edge + p_target_deposited + p_nonrad_uncaptured. The existing p_target_nonrad denotes incoming non-radiated transport before target capture, not target deposition.
Every input/intermediate/output must be finite. Alpha, core and installed powers, reference peak and limit are nonnegative; p_coupled and p_aux_required are signed. Require p_heat_abs >= 0. Negative operating auxiliary demand is the existing burn-hold diagnostic, not physical negative heating; report it with account-valid 0. Fractions lie in [0,1]; p_nonrad_ref, R and R_ref are positive; p_rad_core <= p_heat_abs. Active q_target_ref requires positive capture and finite positive equivalent area. Refuse underflow losing expected positive power, area or peak. Negative edge radiation is reported unchanged with account-valid 0. Signed margins remain valid failure diagnostics.
Capture is paired reference-profile metadata: 0.99 with 9.5 MW/m^2 or 0.97 with 5 MW/m^2, each at 50 MW. Changing capture alone changes deposited power and equivalent area together, never multiplies the sourced peak again. The peak-equivalent area is A_wet/k_peak, not separately measured wetted area or peaking factor. For target groups j, deposited share D_j=s_j*D, q_avg,j=D_j/A_wet,j, q_peak,j=k_j*q_avg,j, and the reported global peak is max_j(q_peak,j), with sum(s_j)=1. No independent s_j, A_wet,j or k_j is established, so these are not executable geometry levers. D/peak_equivalent_area reconstructs the peak only for an active source pair.
The source is a resonant island divertor. The R-scaled shadow is conditional on footprint length proportional to R with held width, sharing and profile. Neither output is an average. A physical interpretation requires area-defined 1, account-valid 1 and a supported paired profile. Dormant q_target_ref=0 has no physical zero-area interpretation. The 10 MW/m^2 predicate is a necessary non-radiated transport screen; omitted radiation surface deposition prevents total target-load qualification.
Retained alpha in this ledger differs from the plant's total alpha boundary, including the inherited alpha-fraction rounding difference. Destinations do not add plant generation. No divertor coolant loop or area-based cost is implied; the inherited power-scaled cost is unchanged.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: lines 1219-1246 (90 % of the net core heating radiated; 500 MW ->
50 MW; the two transport cases (100 eV, 3 m^2/s) 97 % / 5 MW/m^2 and
(200 eV, 1 m^2/s) 99 % / 9.5 MW/m^2; "remain below 10 MW/m^2"; ~200 mm
strike width); 1135-1137 (recycling, ash removal, neutral compression and
erosion left for later work); 1244-1250 (the values hinge on the radiated
fraction; transients for future study); 1284 (the first-wall case at
100 %, a different load case); page render
work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png
*Basis**: Heat conservation from absorbed heating to the target on the
source's fixed-geometry case, scaled in load only

Inputs:
    - p_nonrad_ref_in: p_nonrad_ref_in parameter
    - p_alpha_heat_in: p_alpha_heat_in parameter
    - R_ref_in: R_ref_in parameter
    - p_aux_required_in: p_aux_required_in parameter
    - R_in: R_in parameter
    - target_capture_fraction_in: target_capture_fraction_in parameter
    - q_target_limit_in: q_target_limit_in parameter
    - p_installed_coupled_in: p_installed_coupled_in parameter
    - q_target_ref_in: q_target_ref_in parameter
    - p_coupled_in: p_coupled_in parameter
    - p_rad_core_in: p_rad_core_in parameter
    - f_rad_total_in: f_rad_total_in parameter

Outputs:
    - peak_equivalent_area: peak_equivalent_area result
    - q_target_peak_area_scaled: q_target_peak_area_scaled result
    - f_rad_edge_defined: f_rad_edge_defined result
    - peak_equivalent_area_defined: peak_equivalent_area_defined result
    - p_heat_abs: p_heat_abs result
    - f_rad_edge_in_range: f_rad_edge_in_range result
    - q_target_margin: q_target_margin result
    - p_rad_total: p_rad_total result
    - p_target_nonrad: p_target_nonrad result
    - p_nonrad_uncaptured: p_nonrad_uncaptured result
    - f_rad_edge: f_rad_edge result
    - p_target_deposited: p_target_deposited result
    - p_rad_edge: p_rad_edge result
    - p_heat_operating_minus_installed: p_heat_operating_minus_installed result
    - power_account_valid: power_account_valid result
    - p_sep: p_sep result
    - q_target_peak: q_target_peak result

SysML Source: root-0/analyses/mfe_divertor_heat.sysml:4

SysML Source: root-0/analyses/mfe_divertor_heat.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_divertor_heat/divertor_heat_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.divertor_heat_ledger_output import Divertor_Heat_LedgerOutput


class Divertor_Heat_LedgerInput(BaseModel):
    """Input model for Divertor_Heat_LedgerModule.

    Attributes:
        p_nonrad_ref_in: p_nonrad_ref_in input
        p_alpha_heat_in: p_alpha_heat_in input
        R_ref_in: R_ref_in input
        p_aux_required_in: p_aux_required_in input
        R_in: R_in input
        target_capture_fraction_in: target_capture_fraction_in input
        q_target_limit_in: q_target_limit_in input
        p_installed_coupled_in: p_installed_coupled_in input
        q_target_ref_in: q_target_ref_in input
        p_coupled_in: p_coupled_in input
        p_rad_core_in: p_rad_core_in input
        f_rad_total_in: f_rad_total_in input
    """
    p_nonrad_ref_in: float = Field(..., description="p_nonrad_ref_in input")
    p_alpha_heat_in: float = Field(..., description="p_alpha_heat_in input")
    R_ref_in: float = Field(..., description="R_ref_in input")
    p_aux_required_in: float = Field(..., description="p_aux_required_in input")
    R_in: float = Field(..., description="R_in input")
    target_capture_fraction_in: float = Field(..., description="target_capture_fraction_in input")
    q_target_limit_in: float = Field(..., description="q_target_limit_in input")
    p_installed_coupled_in: float = Field(..., description="p_installed_coupled_in input")
    q_target_ref_in: float = Field(..., description="q_target_ref_in input")
    p_coupled_in: float = Field(..., description="p_coupled_in input")
    p_rad_core_in: float = Field(..., description="p_rad_core_in input")
    f_rad_total_in: float = Field(..., description="f_rad_total_in input")


class Divertor_Heat_LedgerModule(ModuleBase[Divertor_Heat_LedgerInput, Divertor_Heat_LedgerOutput]):
    """TEAx module for Divertor_Heat_Ledger calculation.

Divertor surface-heat ledger, reduced to conservation and one sourced
fixed-geometry case (WI-047):

  p_heat_abs        = p_alpha_heat + p_coupled                       [MW]
  p_sep             = p_heat_abs - p_rad_core                         [MW]
  f_rad_edge        = (f_rad_total * p_heat_abs - p_rad_core) / p_sep  [1]
  f_rad_edge_in_range = f_rad_edge * (1 - f_rad_edge)                 [1] (>= 0 iff in [0, 1])
  p_target_nonrad   = p_heat_abs - f_rad_total * p_heat_abs           [MW]
  q_target_peak     = q_target_ref * p_target_nonrad / p_nonrad_ref   [MW/m^2]
  q_target_peak_area_scaled = q_target_peak * R_ref / R               [MW/m^2] (reported shadow)
  q_target_margin   = q_target_limit - q_target_peak                  [MW/m^2]
  p_heat_operating_minus_installed = p_aux_required - p_installed_coupled [MW]

The absorbed heating is the alpha heating retained in the plasma plus the
sustained operating coupled auxiliary heating, also used by the thermal sum.
The signed required-minus-installed diagnostic uses a separate installed
capacity operand; it does not change the operating heat ledger.
Radiation is a DESTINATION of that heating, never added to it: the core
radiation the sustainment chain composes leaves through the first wall; the
source's radiated fraction f_rad_total is a TOTAL (core plus edge), so the
edge share is derived and reported, not clamped -- a value outside [0, 1]
means the held total and the computed core radiation are inconsistent at
that point, and the in-range channel lets a study count such points.

The peak target flux is the source's own case scaled linearly in the
non-radiated load at FIXED target geometry and transport (q_target_ref at
p_nonrad_ref): no target area, wetted fraction, emissivity, view factor,
erosion or transient enters. A machine of another size keeps the source's
target; the R-scaled output publishes what a target whose wetted length grows
with the major radius would read, and nothing asserts on it. The limit a
concept binds is an adopted steady-state threshold, not an irradiated-
component lifetime. The source's divertor case (a total radiated fraction)
and its first-wall cooling case (100 % radiated) are two load cases and are
never summed. Written p_heat_abs - f * p_heat_abs so the source's own numbers
reproduce to the double (500 - 450 = 50).

WI-065 normative typed manual completion extends the above equations:
  p_rad_total = f_rad_total * p_heat_abs [MW]
  p_rad_edge = p_rad_total - p_rad_core [MW]
  p_target_deposited = target_capture_fraction * p_target_nonrad [MW]
  p_nonrad_uncaptured = p_target_nonrad - p_target_deposited [MW]
  peak_equivalent_area = target_capture_fraction * p_nonrad_ref / q_target_ref [m^2] when q_target_ref > 0, otherwise carrier 0
  peak_equivalent_area_defined = 1 iff q_target_ref > 0, otherwise 0
  f_rad_edge_defined = 1 iff p_sep > 0, otherwise 0 with f_rad_edge carrier 0
  power_account_valid = 1 iff p_rad_edge >= 0 and p_coupled >= 0, otherwise 0
Conservation: p_heat_abs = p_rad_core + p_rad_edge + p_target_deposited + p_nonrad_uncaptured. The existing p_target_nonrad denotes incoming non-radiated transport before target capture, not target deposition.
Every input/intermediate/output must be finite. Alpha, core and installed powers, reference peak and limit are nonnegative; p_coupled and p_aux_required are signed. Require p_heat_abs >= 0. Negative operating auxiliary demand is the existing burn-hold diagnostic, not physical negative heating; report it with account-valid 0. Fractions lie in [0,1]; p_nonrad_ref, R and R_ref are positive; p_rad_core <= p_heat_abs. Active q_target_ref requires positive capture and finite positive equivalent area. Refuse underflow losing expected positive power, area or peak. Negative edge radiation is reported unchanged with account-valid 0. Signed margins remain valid failure diagnostics.
Capture is paired reference-profile metadata: 0.99 with 9.5 MW/m^2 or 0.97 with 5 MW/m^2, each at 50 MW. Changing capture alone changes deposited power and equivalent area together, never multiplies the sourced peak again. The peak-equivalent area is A_wet/k_peak, not separately measured wetted area or peaking factor. For target groups j, deposited share D_j=s_j*D, q_avg,j=D_j/A_wet,j, q_peak,j=k_j*q_avg,j, and the reported global peak is max_j(q_peak,j), with sum(s_j)=1. No independent s_j, A_wet,j or k_j is established, so these are not executable geometry levers. D/peak_equivalent_area reconstructs the peak only for an active source pair.
The source is a resonant island divertor. The R-scaled shadow is conditional on footprint length proportional to R with held width, sharing and profile. Neither output is an average. A physical interpretation requires area-defined 1, account-valid 1 and a supported paired profile. Dormant q_target_ref=0 has no physical zero-area interpretation. The 10 MW/m^2 predicate is a necessary non-radiated transport screen; omitted radiation surface deposition prevents total target-load qualification.
Retained alpha in this ledger differs from the plant's total alpha boundary, including the inherited alpha-fraction rounding difference. Destinations do not add plant generation. No divertor coolant loop or area-based cost is implied; the inherited power-scaled cost is unchanged.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: lines 1219-1246 (90 % of the net core heating radiated; 500 MW ->
50 MW; the two transport cases (100 eV, 3 m^2/s) 97 % / 5 MW/m^2 and
(200 eV, 1 m^2/s) 99 % / 9.5 MW/m^2; "remain below 10 MW/m^2"; ~200 mm
strike width); 1135-1137 (recycling, ash removal, neutral compression and
erosion left for later work); 1244-1250 (the values hinge on the radiated
fraction; transients for future study); 1284 (the first-wall case at
100 %, a different load case); page render
work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png
*Basis**: Heat conservation from absorbed heating to the target on the
source's fixed-geometry case, scaled in load only

Inputs:
    - p_nonrad_ref_in: p_nonrad_ref_in parameter
    - p_alpha_heat_in: p_alpha_heat_in parameter
    - R_ref_in: R_ref_in parameter
    - p_aux_required_in: p_aux_required_in parameter
    - R_in: R_in parameter
    - target_capture_fraction_in: target_capture_fraction_in parameter
    - q_target_limit_in: q_target_limit_in parameter
    - p_installed_coupled_in: p_installed_coupled_in parameter
    - q_target_ref_in: q_target_ref_in parameter
    - p_coupled_in: p_coupled_in parameter
    - p_rad_core_in: p_rad_core_in parameter
    - f_rad_total_in: f_rad_total_in parameter

Outputs:
    - peak_equivalent_area: peak_equivalent_area result
    - q_target_peak_area_scaled: q_target_peak_area_scaled result
    - f_rad_edge_defined: f_rad_edge_defined result
    - peak_equivalent_area_defined: peak_equivalent_area_defined result
    - p_heat_abs: p_heat_abs result
    - f_rad_edge_in_range: f_rad_edge_in_range result
    - q_target_margin: q_target_margin result
    - p_rad_total: p_rad_total result
    - p_target_nonrad: p_target_nonrad result
    - p_nonrad_uncaptured: p_nonrad_uncaptured result
    - f_rad_edge: f_rad_edge result
    - p_target_deposited: p_target_deposited result
    - p_rad_edge: p_rad_edge result
    - p_heat_operating_minus_installed: p_heat_operating_minus_installed result
    - power_account_valid: power_account_valid result
    - p_sep: p_sep result
    - q_target_peak: q_target_peak result

SysML Source: root-0/analyses/mfe_divertor_heat.sysml:4

    SysML Source: root-0/analyses/mfe_divertor_heat.sysml:4

    Calculation Specification:
        See documentation:
Divertor surface-heat ledger, reduced to conservation and one sourced
fixed-geometry case (WI-047):

  p_heat_abs        = p_alpha_heat + p_coupled                       [MW]
  p_sep             = p_heat_abs - p_rad_core                         [MW]
  f_rad_edge        = (f_rad_total * p_heat_abs - p_rad_core) / p_sep  [1]
  f_rad_edge_in_range = f_rad_edge * (1 - f_rad_edge)                 [1] (>= 0 iff in [0, 1])
  p_target_nonrad   = p_heat_abs - f_rad_total * p_heat_abs           [MW]
  q_target_peak     = q_target_ref * p_target_nonrad / p_nonrad_ref   [MW/m^2]
  q_target_peak_area_scaled = q_target_peak * R_ref / R               [MW/m^2] (reported shadow)
  q_target_margin   = q_target_limit - q_target_peak                  [MW/m^2]
  p_heat_operating_minus_installed = p_aux_required - p_installed_coupled [MW]

The absorbed heating is the alpha heating retained in the plasma plus the
sustained operating coupled auxiliary heating, also used by the thermal sum.
The signed required-minus-installed diagnostic uses a separate installed
capacity operand; it does not change the operating heat ledger.
Radiation is a DESTINATION of that heating, never added to it: the core
radiation the sustainment chain composes leaves through the first wall; the
source's radiated fraction f_rad_total is a TOTAL (core plus edge), so the
edge share is derived and reported, not clamped -- a value outside [0, 1]
means the held total and the computed core radiation are inconsistent at
that point, and the in-range channel lets a study count such points.

The peak target flux is the source's own case scaled linearly in the
non-radiated load at FIXED target geometry and transport (q_target_ref at
p_nonrad_ref): no target area, wetted fraction, emissivity, view factor,
erosion or transient enters. A machine of another size keeps the source's
target; the R-scaled output publishes what a target whose wetted length grows
with the major radius would read, and nothing asserts on it. The limit a
concept binds is an adopted steady-state threshold, not an irradiated-
component lifetime. The source's divertor case (a total radiated fraction)
and its first-wall cooling case (100 % radiated) are two load cases and are
never summed. Written p_heat_abs - f * p_heat_abs so the source's own numbers
reproduce to the double (500 - 450 = 50).

WI-065 normative typed manual completion extends the above equations:
  p_rad_total = f_rad_total * p_heat_abs [MW]
  p_rad_edge = p_rad_total - p_rad_core [MW]
  p_target_deposited = target_capture_fraction * p_target_nonrad [MW]
  p_nonrad_uncaptured = p_target_nonrad - p_target_deposited [MW]
  peak_equivalent_area = target_capture_fraction * p_nonrad_ref / q_target_ref [m^2] when q_target_ref > 0, otherwise carrier 0
  peak_equivalent_area_defined = 1 iff q_target_ref > 0, otherwise 0
  f_rad_edge_defined = 1 iff p_sep > 0, otherwise 0 with f_rad_edge carrier 0
  power_account_valid = 1 iff p_rad_edge >= 0 and p_coupled >= 0, otherwise 0
Conservation: p_heat_abs = p_rad_core + p_rad_edge + p_target_deposited + p_nonrad_uncaptured. The existing p_target_nonrad denotes incoming non-radiated transport before target capture, not target deposition.
Every input/intermediate/output must be finite. Alpha, core and installed powers, reference peak and limit are nonnegative; p_coupled and p_aux_required are signed. Require p_heat_abs >= 0. Negative operating auxiliary demand is the existing burn-hold diagnostic, not physical negative heating; report it with account-valid 0. Fractions lie in [0,1]; p_nonrad_ref, R and R_ref are positive; p_rad_core <= p_heat_abs. Active q_target_ref requires positive capture and finite positive equivalent area. Refuse underflow losing expected positive power, area or peak. Negative edge radiation is reported unchanged with account-valid 0. Signed margins remain valid failure diagnostics.
Capture is paired reference-profile metadata: 0.99 with 9.5 MW/m^2 or 0.97 with 5 MW/m^2, each at 50 MW. Changing capture alone changes deposited power and equivalent area together, never multiplies the sourced peak again. The peak-equivalent area is A_wet/k_peak, not separately measured wetted area or peaking factor. For target groups j, deposited share D_j=s_j*D, q_avg,j=D_j/A_wet,j, q_peak,j=k_j*q_avg,j, and the reported global peak is max_j(q_peak,j), with sum(s_j)=1. No independent s_j, A_wet,j or k_j is established, so these are not executable geometry levers. D/peak_equivalent_area reconstructs the peak only for an active source pair.
The source is a resonant island divertor. The R-scaled shadow is conditional on footprint length proportional to R with held width, sharing and profile. Neither output is an average. A physical interpretation requires area-defined 1, account-valid 1 and a supported paired profile. Dormant q_target_ref=0 has no physical zero-area interpretation. The 10 MW/m^2 predicate is a necessary non-radiated transport screen; omitted radiation surface deposition prevents total target-load qualification.
Retained alpha in this ledger differs from the plant's total alpha boundary, including the inherited alpha-fraction rounding difference. Destinations do not add plant generation. No divertor coolant loop or area-based cost is implied; the inherited power-scaled cost is unchanged.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: lines 1219-1246 (90 % of the net core heating radiated; 500 MW ->
50 MW; the two transport cases (100 eV, 3 m^2/s) 97 % / 5 MW/m^2 and
(200 eV, 1 m^2/s) 99 % / 9.5 MW/m^2; "remain below 10 MW/m^2"; ~200 mm
strike width); 1135-1137 (recycling, ash removal, neutral compression and
erosion left for later work); 1244-1250 (the values hinge on the radiated
fraction; transients for future study); 1284 (the first-wall case at
100 %, a different load case); page render
work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png
*Basis**: Heat conservation from absorbed heating to the target on the
source's fixed-geometry case, scaled in load only

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_divertor_heat.divertor_heat_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts peak_equivalent_area, q_target_peak_area_scaled, f_rad_edge_defined, peak_equivalent_area_defined, p_heat_abs, f_rad_edge_in_range, q_target_margin, p_rad_total, p_target_nonrad, p_nonrad_uncaptured, f_rad_edge, p_target_deposited, p_rad_edge, p_heat_operating_minus_installed, power_account_valid, p_sep, q_target_peak fields to separate channels.
    """

    name: str = "Divertor_Heat_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_nonrad_ref_in: float, p_alpha_heat_in: float, R_ref_in: float, p_aux_required_in: float, R_in: float, target_capture_fraction_in: float, q_target_limit_in: float, p_installed_coupled_in: float, q_target_ref_in: float, p_coupled_in: float, p_rad_core_in: float, f_rad_total_in: float    ) -> Divertor_Heat_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            p_nonrad_ref_in: p_nonrad_ref_in input
            p_alpha_heat_in: p_alpha_heat_in input
            R_ref_in: R_ref_in input
            p_aux_required_in: p_aux_required_in input
            R_in: R_in input
            target_capture_fraction_in: target_capture_fraction_in input
            q_target_limit_in: q_target_limit_in input
            p_installed_coupled_in: p_installed_coupled_in input
            q_target_ref_in: q_target_ref_in input
            p_coupled_in: p_coupled_in input
            p_rad_core_in: p_rad_core_in input
            f_rad_total_in: f_rad_total_in input

        Returns:
            Validated input model
        """
        return Divertor_Heat_LedgerInput(p_nonrad_ref_in=p_nonrad_ref_in, p_alpha_heat_in=p_alpha_heat_in, R_ref_in=R_ref_in, p_aux_required_in=p_aux_required_in, R_in=R_in, target_capture_fraction_in=target_capture_fraction_in, q_target_limit_in=q_target_limit_in, p_installed_coupled_in=p_installed_coupled_in, q_target_ref_in=q_target_ref_in, p_coupled_in=p_coupled_in, p_rad_core_in=p_rad_core_in, f_rad_total_in=f_rad_total_in)

    def run(
        self, p_nonrad_ref_in: float, p_alpha_heat_in: float, R_ref_in: float, p_aux_required_in: float, R_in: float, target_capture_fraction_in: float, q_target_limit_in: float, p_installed_coupled_in: float, q_target_ref_in: float, p_coupled_in: float, p_rad_core_in: float, f_rad_total_in: float    ) -> ModuleResult[Divertor_Heat_LedgerOutput]:
        """Execute calculation.

        Args:
            p_nonrad_ref_in: p_nonrad_ref_in input
            p_alpha_heat_in: p_alpha_heat_in input
            R_ref_in: R_ref_in input
            p_aux_required_in: p_aux_required_in input
            R_in: R_in input
            target_capture_fraction_in: target_capture_fraction_in input
            q_target_limit_in: q_target_limit_in input
            p_installed_coupled_in: p_installed_coupled_in input
            q_target_ref_in: q_target_ref_in input
            p_coupled_in: p_coupled_in input
            p_rad_core_in: p_rad_core_in input
            f_rad_total_in: f_rad_total_in input

        Returns:
            Module result with Divertor_Heat_LedgerOutput (peak_equivalent_area, q_target_peak_area_scaled, f_rad_edge_defined, peak_equivalent_area_defined, p_heat_abs, f_rad_edge_in_range, q_target_margin, p_rad_total, p_target_nonrad, p_nonrad_uncaptured, f_rad_edge, p_target_deposited, p_rad_edge, p_heat_operating_minus_installed, power_account_valid, p_sep, q_target_peak)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_nonrad_ref_in, p_alpha_heat_in, R_ref_in, p_aux_required_in, R_in, target_capture_fraction_in, q_target_limit_in, p_installed_coupled_in, q_target_ref_in, p_coupled_in, p_rad_core_in, f_rad_total_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_divertor_heat.divertor_heat_ledger_impl import (
            run_divertor_heat_ledger,
        )

        # Execute implementation - returns tuple of values
        peak_equivalent_area, q_target_peak_area_scaled, f_rad_edge_defined, peak_equivalent_area_defined, p_heat_abs, f_rad_edge_in_range, q_target_margin, p_rad_total, p_target_nonrad, p_nonrad_uncaptured, f_rad_edge, p_target_deposited, p_rad_edge, p_heat_operating_minus_installed, power_account_valid, p_sep, q_target_peak = run_divertor_heat_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Divertor_Heat_LedgerOutput(
                peak_equivalent_area=peak_equivalent_area,
                q_target_peak_area_scaled=q_target_peak_area_scaled,
                f_rad_edge_defined=f_rad_edge_defined,
                peak_equivalent_area_defined=peak_equivalent_area_defined,
                p_heat_abs=p_heat_abs,
                f_rad_edge_in_range=f_rad_edge_in_range,
                q_target_margin=q_target_margin,
                p_rad_total=p_rad_total,
                p_target_nonrad=p_target_nonrad,
                p_nonrad_uncaptured=p_nonrad_uncaptured,
                f_rad_edge=f_rad_edge,
                p_target_deposited=p_target_deposited,
                p_rad_edge=p_rad_edge,
                p_heat_operating_minus_installed=p_heat_operating_minus_installed,
                power_account_valid=power_account_valid,
                p_sep=p_sep,
                q_target_peak=q_target_peak,
            )
        )
