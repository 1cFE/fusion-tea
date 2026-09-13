"""Auto-generated implementation for Primary_Coolant_Loop.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_primary_loop.sysml:4

SysML Expressions:
    f_loss_in = 1.0
    eta_drive_in = 1.0
    loop_live_in = 0.0
    p_pump_direct_in = 0.0
    eta_p_direct_in = 0.0
    mdot = q_source_in * 1000000.0 / (cp_in * dT_blanket_in)
    T_out = T_in_in + dT_blanket_in
    mdot_loop = mdot / n_loops_in
    dp_loop = f_loss_in * dp_loop_ref_in * (mdot_loop / mdot_loop_ref_in) ** 2
    p_loop_margin = p_loop_in - dp_loop
    r_comp = p_loop_in / (p_loop_in - dp_loop)
    k_isen = (gamma_in - 1.0) / gamma_in
    T_comp_in = T_in_in / (1.0 + (r_comp ** k_isen - 1.0) / eta_is_in)
    w_fluid = mdot * cp_in * (T_in_in - T_comp_in) / 1000000.0
    p_elec = w_fluid / eta_drive_in
    q_ihx = q_source_in + w_fluid
    capacity_margin = mdot_loop_ref_in - mdot_loop
    p_pump_total = loop_live_in * p_elec + p_pump_direct_in
    q_recovered_total = loop_live_in * w_fluid + eta_p_direct_in * p_pump_direct_in
    
Documentation:
Representative helium primary circuit in sized-flow mode (WI-045, goal
plant-closure; the research 20260907-163520_primary-loop-cycle-closure-prework
section 2). One hydraulic path stands for the circuit; the loop count
scales it. Dependency order: source heat -> flow -> per-path loss at the
reference's nominal density -> compressor -> fluid work -> electrical
draw -> IHX duty. There is no edge from the plant's thermal power back to
the flow.

  mdot        = q_source * 1e6 / (cp * dT_blanket)            [kg/s]
  T_out       = T_in + dT_blanket                             [K]
  mdot_loop   = mdot / n_loops                                [kg/s]
  dp_loop     = f_loss * dp_loop_ref * (mdot_loop/mdot_loop_ref)^2  [Pa]
  r_comp      = p_loop / (p_loop - dp_loop)                   [1]
  T_comp_in   = T_in / (1 + (r_comp^((gamma-1)/gamma) - 1)/eta_is)  [K]
  w_fluid     = mdot * cp * (T_in - T_comp_in) / 1e6          [MW]
  p_elec      = w_fluid / eta_drive                           [MW]
  q_ihx       = q_source + w_fluid                            [MW]
  p_pump_total       = loop_live * p_elec + p_pump_direct     [MW]
  q_recovered_total  = loop_live * w_fluid + eta_p_direct * p_pump_direct [MW]

THE LOSS LAW is a constant loss coefficient about the reference layout
at its nominal density: the reference's per-path loss scaled by the
square of the per-loop flow ratio, rho_ref/rho taken as 1 (the loop is
held at the reference's pressure and temperature window). It computes
loss from flow; it is NOT a fraction of thermal power (the form the
owner rejected 2026-08-28). A broad R/a extrapolation of the law is
unsupported: the circuit's geometry is the reference's, held.

THE COMPRESSOR is isentropic compression from the compressor inlet at
the isentropic efficiency eta_is, with the blanket inlet T_in held by
the secondary-side cooling; T_comp_in is what the IHX must deliver, not
evidence that it can (the exchanger is not sized here).

ALL FLUID WORK IS RECOVERED into the IHX duty (the reference's own
energy check: IHX duty 2231.1 - blanket heat 2101.7 = 129.4 MW against
130.8 MW printed circulator power). eta_drive converts fluid work to
electrical draw; an instance binding it to 1.0 reads the source's
printed circulator figure as the boundary and its draw as a LOWER
BOUND on the true electrical draw (drive losses a surfaced missing input).

DORMANCY (packet section 3): loop_live 0 with the direct terms at the
old held scalars gives p_pump_total = 0.0 * p_elec + p_pump_direct and
q_recovered_total = 0.0 * w_fluid + eta_p_direct * p_pump_direct, which
are the old scalars to the bit for finite p_elec and w_fluid; the power
balance then reproduces the pre-WI-045 accounting exactly. The chain
always evaluates; only what it hands to the power balance is switched.

Constant ideal-gas helium properties (cp, gamma) over the reference
window; the reference's own implied cp is 0.10 % under ideal helium.

*Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
(Moscato et al., EUROfusion WPBOP-CPR(18) 20276); NASA compressor thermodynamics
(w = cp T_in (r^((gamma-1)/gamma) - 1)/eta_is); NIST helium cp
*Ref**: output.md:79 (8 MPa, 300-500 C), :81 (2101.7 MW, 2025.7 kg/s), :89-91 (9 loops),
Table 1 :105-113 (two compressors per loop), Table 2 :128 (IHX duties), Table 3 :151-154
(per-path losses, circulator power); raw.pdf p. 6 Table 3 (kPa basis)
*Basis**: sized-flow representative circuit with a constant loss coefficient and an
isentropic compressor; concept-agnostic (MR-3) -- every fact bound by instances
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_primary_loop.primary_coolant_loop import Primary_Coolant_LoopInput


def run_primary_coolant_loop(inputs: Primary_Coolant_LoopInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Execute Primary_Coolant_Loop calculation.

Representative helium primary circuit in sized-flow mode (WI-045, goal
plant-closure; the research 20260907-163520_primary-loop-cycle-closure-prework
section 2). One hydraulic path stands for the circuit; the loop count
scales it. Dependency order: source heat -> flow -> per-path loss at the
reference's nominal density -> compressor -> fluid work -> electrical
draw -> IHX duty. There is no edge from the plant's thermal power back to
the flow.

  mdot        = q_source * 1e6 / (cp * dT_blanket)            [kg/s]
  T_out       = T_in + dT_blanket                             [K]
  mdot_loop   = mdot / n_loops                                [kg/s]
  dp_loop     = f_loss * dp_loop_ref * (mdot_loop/mdot_loop_ref)^2  [Pa]
  r_comp      = p_loop / (p_loop - dp_loop)                   [1]
  T_comp_in   = T_in / (1 + (r_comp^((gamma-1)/gamma) - 1)/eta_is)  [K]
  w_fluid     = mdot * cp * (T_in - T_comp_in) / 1e6          [MW]
  p_elec      = w_fluid / eta_drive                           [MW]
  q_ihx       = q_source + w_fluid                            [MW]
  p_pump_total       = loop_live * p_elec + p_pump_direct     [MW]
  q_recovered_total  = loop_live * w_fluid + eta_p_direct * p_pump_direct [MW]

THE LOSS LAW is a constant loss coefficient about the reference layout
at its nominal density: the reference's per-path loss scaled by the
square of the per-loop flow ratio, rho_ref/rho taken as 1 (the loop is
held at the reference's pressure and temperature window). It computes
loss from flow; it is NOT a fraction of thermal power (the form the
owner rejected 2026-08-28). A broad R/a extrapolation of the law is
unsupported: the circuit's geometry is the reference's, held.

THE COMPRESSOR is isentropic compression from the compressor inlet at
the isentropic efficiency eta_is, with the blanket inlet T_in held by
the secondary-side cooling; T_comp_in is what the IHX must deliver, not
evidence that it can (the exchanger is not sized here).

ALL FLUID WORK IS RECOVERED into the IHX duty (the reference's own
energy check: IHX duty 2231.1 - blanket heat 2101.7 = 129.4 MW against
130.8 MW printed circulator power). eta_drive converts fluid work to
electrical draw; an instance binding it to 1.0 reads the source's
printed circulator figure as the boundary and its draw as a LOWER
BOUND on the true electrical draw (drive losses a surfaced missing input).

DORMANCY (packet section 3): loop_live 0 with the direct terms at the
old held scalars gives p_pump_total = 0.0 * p_elec + p_pump_direct and
q_recovered_total = 0.0 * w_fluid + eta_p_direct * p_pump_direct, which
are the old scalars to the bit for finite p_elec and w_fluid; the power
balance then reproduces the pre-WI-045 accounting exactly. The chain
always evaluates; only what it hands to the power balance is switched.

Constant ideal-gas helium properties (cp, gamma) over the reference
window; the reference's own implied cp is 0.10 % under ideal helium.

*Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
(Moscato et al., EUROfusion WPBOP-CPR(18) 20276); NASA compressor thermodynamics
(w = cp T_in (r^((gamma-1)/gamma) - 1)/eta_is); NIST helium cp
*Ref**: output.md:79 (8 MPa, 300-500 C), :81 (2101.7 MW, 2025.7 kg/s), :89-91 (9 loops),
Table 1 :105-113 (two compressors per loop), Table 2 :128 (IHX duties), Table 3 :151-154
(per-path losses, circulator power); raw.pdf p. 6 Table 3 (kPa basis)
*Basis**: sized-flow representative circuit with a constant loss coefficient and an
isentropic compressor; concept-agnostic (MR-3) -- every fact bound by instances

SysML Source: root-0/analyses/mfe_primary_loop.sysml:4

SysML Expressions:
    f_loss_in = 1.0
    eta_drive_in = 1.0
    loop_live_in = 0.0
    p_pump_direct_in = 0.0
    eta_p_direct_in = 0.0
    mdot = q_source_in * 1000000.0 / (cp_in * dT_blanket_in)
    T_out = T_in_in + dT_blanket_in
    mdot_loop = mdot / n_loops_in
    dp_loop = f_loss_in * dp_loop_ref_in * (mdot_loop / mdot_loop_ref_in) ** 2
    p_loop_margin = p_loop_in - dp_loop
    r_comp = p_loop_in / (p_loop_in - dp_loop)
    k_isen = (gamma_in - 1.0) / gamma_in
    T_comp_in = T_in_in / (1.0 + (r_comp ** k_isen - 1.0) / eta_is_in)
    w_fluid = mdot * cp_in * (T_in_in - T_comp_in) / 1000000.0
    p_elec = w_fluid / eta_drive_in
    q_ihx = q_source_in + w_fluid
    capacity_margin = mdot_loop_ref_in - mdot_loop
    p_pump_total = loop_live_in * p_elec + p_pump_direct_in
    q_recovered_total = loop_live_in * w_fluid + eta_p_direct_in * p_pump_direct_in
    
Documentation:
Representative helium primary circuit in sized-flow mode (WI-045, goal
plant-closure; the research 20260907-163520_primary-loop-cycle-closure-prework
section 2). One hydraulic path stands for the circuit; the loop count
scales it. Dependency order: source heat -> flow -> per-path loss at the
reference's nominal density -> compressor -> fluid work -> electrical
draw -> IHX duty. There is no edge from the plant's thermal power back to
the flow.

  mdot        = q_source * 1e6 / (cp * dT_blanket)            [kg/s]
  T_out       = T_in + dT_blanket                             [K]
  mdot_loop   = mdot / n_loops                                [kg/s]
  dp_loop     = f_loss * dp_loop_ref * (mdot_loop/mdot_loop_ref)^2  [Pa]
  r_comp      = p_loop / (p_loop - dp_loop)                   [1]
  T_comp_in   = T_in / (1 + (r_comp^((gamma-1)/gamma) - 1)/eta_is)  [K]
  w_fluid     = mdot * cp * (T_in - T_comp_in) / 1e6          [MW]
  p_elec      = w_fluid / eta_drive                           [MW]
  q_ihx       = q_source + w_fluid                            [MW]
  p_pump_total       = loop_live * p_elec + p_pump_direct     [MW]
  q_recovered_total  = loop_live * w_fluid + eta_p_direct * p_pump_direct [MW]

THE LOSS LAW is a constant loss coefficient about the reference layout
at its nominal density: the reference's per-path loss scaled by the
square of the per-loop flow ratio, rho_ref/rho taken as 1 (the loop is
held at the reference's pressure and temperature window). It computes
loss from flow; it is NOT a fraction of thermal power (the form the
owner rejected 2026-08-28). A broad R/a extrapolation of the law is
unsupported: the circuit's geometry is the reference's, held.

THE COMPRESSOR is isentropic compression from the compressor inlet at
the isentropic efficiency eta_is, with the blanket inlet T_in held by
the secondary-side cooling; T_comp_in is what the IHX must deliver, not
evidence that it can (the exchanger is not sized here).

ALL FLUID WORK IS RECOVERED into the IHX duty (the reference's own
energy check: IHX duty 2231.1 - blanket heat 2101.7 = 129.4 MW against
130.8 MW printed circulator power). eta_drive converts fluid work to
electrical draw; an instance binding it to 1.0 reads the source's
printed circulator figure as the boundary and its draw as a LOWER
BOUND on the true electrical draw (drive losses a surfaced missing input).

DORMANCY (packet section 3): loop_live 0 with the direct terms at the
old held scalars gives p_pump_total = 0.0 * p_elec + p_pump_direct and
q_recovered_total = 0.0 * w_fluid + eta_p_direct * p_pump_direct, which
are the old scalars to the bit for finite p_elec and w_fluid; the power
balance then reproduces the pre-WI-045 accounting exactly. The chain
always evaluates; only what it hands to the power balance is switched.

Constant ideal-gas helium properties (cp, gamma) over the reference
window; the reference's own implied cp is 0.10 % under ideal helium.

*Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
(Moscato et al., EUROfusion WPBOP-CPR(18) 20276); NASA compressor thermodynamics
(w = cp T_in (r^((gamma-1)/gamma) - 1)/eta_is); NIST helium cp
*Ref**: output.md:79 (8 MPa, 300-500 C), :81 (2101.7 MW, 2025.7 kg/s), :89-91 (9 loops),
Table 1 :105-113 (two compressors per loop), Table 2 :128 (IHX duties), Table 3 :151-154
(per-path losses, circulator power); raw.pdf p. 6 Table 3 (kPa basis)
*Basis**: sized-flow representative circuit with a constant loss coefficient and an
isentropic compressor; concept-agnostic (MR-3) -- every fact bound by instances

Args:
    inputs: Input parameters validated against Primary_Coolant_LoopInput schema

Returns:
    tuple[float, ...]: (p_loop_margin, q_recovered_total, p_elec, p_pump_total, T_out, T_comp_in, dp_loop, mdot_loop, w_fluid, capacity_margin, q_ihx, mdot, r_comp)

Example:
    >>> inputs = Primary_Coolant_LoopInput(...)
    >>> p_loop_margin, q_recovered_total, p_elec, p_pump_total, T_out, T_comp_in, dp_loop, mdot_loop, w_fluid, capacity_margin, q_ihx, mdot, r_comp = run_primary_coolant_loop(inputs)
    """
    k_isen = ((inputs.gamma_in - 1.0) / inputs.gamma_in)
    mdot = ((inputs.q_source_in * 1000000.0) / (inputs.cp_in * inputs.dT_blanket_in))
    mdot_loop = (mdot / inputs.n_loops_in)
    dp_loop = ((inputs.f_loss_in * inputs.dp_loop_ref_in) * ((mdot_loop / inputs.mdot_loop_ref_in) ** 2))
    r_comp = (inputs.p_loop_in / (inputs.p_loop_in - dp_loop))
    T_comp_in = (inputs.T_in_in / (1.0 + (((r_comp ** k_isen) - 1.0) / inputs.eta_is_in)))
    w_fluid = (((mdot * inputs.cp_in) * (inputs.T_in_in - T_comp_in)) / 1000000.0)
    p_elec = (w_fluid / inputs.eta_drive_in)
    return (
        (inputs.p_loop_in - dp_loop),  # p_loop_margin
        ((inputs.loop_live_in * w_fluid) + (inputs.eta_p_direct_in * inputs.p_pump_direct_in)),  # q_recovered_total
        p_elec,
        ((inputs.loop_live_in * p_elec) + inputs.p_pump_direct_in),  # p_pump_total
        (inputs.T_in_in + inputs.dT_blanket_in),  # T_out
        T_comp_in,
        dp_loop,
        mdot_loop,
        w_fluid,
        (inputs.mdot_loop_ref_in - mdot_loop),  # capacity_margin
        (inputs.q_source_in + w_fluid),  # q_ihx
        mdot,
        r_comp,
    )
