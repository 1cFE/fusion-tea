"""Auto-generated implementation for Divertor_Heat_Ledger.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_divertor_heat.sysml:4

SysML Expressions:
    p_heat_abs = p_alpha_heat_in + p_coupled_in
    p_sep = p_heat_abs - p_rad_core_in
    f_rad_edge = (f_rad_total_in * p_heat_abs - p_rad_core_in) / p_sep
    f_rad_edge_in_range = f_rad_edge * (1.0 - f_rad_edge)
    p_target_nonrad = p_heat_abs - f_rad_total_in * p_heat_abs
    q_target_peak = q_target_ref_in * p_target_nonrad / p_nonrad_ref_in
    q_target_peak_area_scaled = q_target_peak * R_ref_in / R_in
    q_target_margin = q_target_limit_in - q_target_peak
    p_heat_operating_minus_installed = p_aux_required_in - p_installed_coupled_in
    
Documentation:
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

Flat-Real (+ - * /) -- no manual stage.

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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_divertor_heat.divertor_heat_ledger import Divertor_Heat_LedgerInput


def run_divertor_heat_ledger(inputs: Divertor_Heat_LedgerInput) -> tuple[float, float, float, float, float, float, float, float, float]:
    """Execute Divertor_Heat_Ledger calculation.

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

Flat-Real (+ - * /) -- no manual stage.

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

SysML Source: root-0/analyses/mfe_divertor_heat.sysml:4

SysML Expressions:
    p_heat_abs = p_alpha_heat_in + p_coupled_in
    p_sep = p_heat_abs - p_rad_core_in
    f_rad_edge = (f_rad_total_in * p_heat_abs - p_rad_core_in) / p_sep
    f_rad_edge_in_range = f_rad_edge * (1.0 - f_rad_edge)
    p_target_nonrad = p_heat_abs - f_rad_total_in * p_heat_abs
    q_target_peak = q_target_ref_in * p_target_nonrad / p_nonrad_ref_in
    q_target_peak_area_scaled = q_target_peak * R_ref_in / R_in
    q_target_margin = q_target_limit_in - q_target_peak
    p_heat_operating_minus_installed = p_aux_required_in - p_installed_coupled_in
    
Documentation:
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

Flat-Real (+ - * /) -- no manual stage.

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

Args:
    inputs: Input parameters validated against Divertor_Heat_LedgerInput schema

Returns:
    tuple[float, ...]: (q_target_peak_area_scaled, p_heat_abs, f_rad_edge_in_range, q_target_margin, p_target_nonrad, f_rad_edge, p_heat_operating_minus_installed, p_sep, q_target_peak)

Example:
    >>> inputs = Divertor_Heat_LedgerInput(...)
    >>> q_target_peak_area_scaled, p_heat_abs, f_rad_edge_in_range, q_target_margin, p_target_nonrad, f_rad_edge, p_heat_operating_minus_installed, p_sep, q_target_peak = run_divertor_heat_ledger(inputs)
    """
    p_heat_abs = (inputs.p_alpha_heat_in + inputs.p_coupled_in)
    p_target_nonrad = (p_heat_abs - (inputs.f_rad_total_in * p_heat_abs))
    p_sep = (p_heat_abs - inputs.p_rad_core_in)
    f_rad_edge = (((inputs.f_rad_total_in * p_heat_abs) - inputs.p_rad_core_in) / p_sep)
    q_target_peak = ((inputs.q_target_ref_in * p_target_nonrad) / inputs.p_nonrad_ref_in)
    return (
        ((q_target_peak * inputs.R_ref_in) / inputs.R_in),  # q_target_peak_area_scaled
        p_heat_abs,
        (f_rad_edge * (1.0 - f_rad_edge)),  # f_rad_edge_in_range
        (inputs.q_target_limit_in - q_target_peak),  # q_target_margin
        p_target_nonrad,
        f_rad_edge,
        (inputs.p_aux_required_in - inputs.p_installed_coupled_in),  # p_heat_operating_minus_installed
        p_sep,
        q_target_peak,
    )
