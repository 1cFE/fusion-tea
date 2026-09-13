from pydantic import Field
from simkit.config.schema import MultiOutput

class Primary_Coolant_LoopOutput(MultiOutput):
    """Multi-output container for Primary_Coolant_Loop.

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

INPUT DOMAIN (WI-056): cp_in and dT_blanket_in must each be finite
and strictly positive. cp is specific heat [J/(kg K)]; dT_blanket
is the positive coolant heating rise [K]. A negative pair is invalid.
Native typed manual completion raises ValueError before arithmetic.
This domain also applies for q_source = 0 and loop_live = 0 because
the chain always evaluates. Reference values are examples, not bounds.
The thirteen outputs below require this guarded manual completion;
the ordered equations above remain the normative valid calculation.

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
    """
    p_loop_margin: float = Field(description="p_loop_margin output")
    q_recovered_total: float = Field(description="q_recovered_total output")
    p_elec: float = Field(description="p_elec output")
    p_pump_total: float = Field(description="p_pump_total output")
    T_out: float = Field(description="T_out output")
    T_comp_in: float = Field(description="T_comp_in output")
    dp_loop: float = Field(description="dp_loop output")
    mdot_loop: float = Field(description="mdot_loop output")
    w_fluid: float = Field(description="w_fluid output")
    capacity_margin: float = Field(description="capacity_margin output")
    q_ihx: float = Field(description="q_ihx output")
    mdot: float = Field(description="mdot output")
    r_comp: float = Field(description="r_comp output")
