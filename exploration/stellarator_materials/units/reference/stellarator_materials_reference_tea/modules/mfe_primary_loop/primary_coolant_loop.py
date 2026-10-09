"""Primary_Coolant_LoopModule Module Wrapper

TEAx module for Primary_Coolant_Loop calculation.

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

Compressor arithmetic also requires finite p_loop_in > dp_loop >= 0 Pa. Typed completion refuses nonpositive suction before division or fractional power and reports supplied pressure, calculated loss and suction. This mathematical prerequisite does not qualify the empirical loss law off its reference conditions. Unsupported execution supplies no completed plant evaluation.

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

Inputs:
    - q_source_in: q_source_in parameter
    - cp_in: cp_in parameter
    - mdot_loop_ref_in: mdot_loop_ref_in parameter
    - T_in_in: T_in_in parameter
    - p_pump_direct_in: p_pump_direct_in parameter
    - gamma_in: gamma_in parameter
    - f_loss_in: f_loss_in parameter
    - n_loops_in: n_loops_in parameter
    - dp_loop_ref_in: dp_loop_ref_in parameter
    - loop_live_in: loop_live_in parameter
    - eta_p_direct_in: eta_p_direct_in parameter
    - dT_blanket_in: dT_blanket_in parameter
    - p_loop_in: p_loop_in parameter
    - eta_is_in: eta_is_in parameter
    - mdot_loop_rated_in: mdot_loop_rated_in parameter
    - eta_drive_in: eta_drive_in parameter

Outputs:
    - p_loop_margin: p_loop_margin result
    - q_recovered_total: q_recovered_total result
    - p_elec: p_elec result
    - p_pump_total: p_pump_total result
    - T_out: T_out result
    - T_comp_in: T_comp_in result
    - dp_loop: dp_loop result
    - mdot_loop: mdot_loop result
    - w_fluid: w_fluid result
    - capacity_margin: capacity_margin result
    - q_ihx: q_ihx result
    - mdot: mdot result
    - r_comp: r_comp result

SysML Source: root-0/analyses/mfe_primary_loop.sysml:4

SysML Source: root-0/analyses/mfe_primary_loop.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_primary_loop/primary_coolant_loop_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.primary_coolant_loop_output import Primary_Coolant_LoopOutput


class Primary_Coolant_LoopInput(BaseModel):
    """Input model for Primary_Coolant_LoopModule.

    Attributes:
        q_source_in: q_source_in input
        cp_in: cp_in input
        mdot_loop_ref_in: mdot_loop_ref_in input
        T_in_in: T_in_in input
        p_pump_direct_in: p_pump_direct_in input
        gamma_in: gamma_in input
        f_loss_in: f_loss_in input
        n_loops_in: n_loops_in input
        dp_loop_ref_in: dp_loop_ref_in input
        loop_live_in: loop_live_in input
        eta_p_direct_in: eta_p_direct_in input
        dT_blanket_in: dT_blanket_in input
        p_loop_in: p_loop_in input
        eta_is_in: eta_is_in input
        mdot_loop_rated_in: mdot_loop_rated_in input
        eta_drive_in: eta_drive_in input
    """
    q_source_in: float = Field(..., description="q_source_in input")
    cp_in: float = Field(..., description="cp_in input")
    mdot_loop_ref_in: float = Field(..., description="mdot_loop_ref_in input")
    T_in_in: float = Field(..., description="T_in_in input")
    p_pump_direct_in: float = Field(..., description="p_pump_direct_in input")
    gamma_in: float = Field(..., description="gamma_in input")
    f_loss_in: float = Field(..., description="f_loss_in input")
    n_loops_in: float = Field(..., description="n_loops_in input")
    dp_loop_ref_in: float = Field(..., description="dp_loop_ref_in input")
    loop_live_in: float = Field(..., description="loop_live_in input")
    eta_p_direct_in: float = Field(..., description="eta_p_direct_in input")
    dT_blanket_in: float = Field(..., description="dT_blanket_in input")
    p_loop_in: float = Field(..., description="p_loop_in input")
    eta_is_in: float = Field(..., description="eta_is_in input")
    mdot_loop_rated_in: float = Field(..., description="mdot_loop_rated_in input")
    eta_drive_in: float = Field(..., description="eta_drive_in input")


class Primary_Coolant_LoopModule(ModuleBase[Primary_Coolant_LoopInput, Primary_Coolant_LoopOutput]):
    """TEAx module for Primary_Coolant_Loop calculation.

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

Compressor arithmetic also requires finite p_loop_in > dp_loop >= 0 Pa. Typed completion refuses nonpositive suction before division or fractional power and reports supplied pressure, calculated loss and suction. This mathematical prerequisite does not qualify the empirical loss law off its reference conditions. Unsupported execution supplies no completed plant evaluation.

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

Inputs:
    - q_source_in: q_source_in parameter
    - cp_in: cp_in parameter
    - mdot_loop_ref_in: mdot_loop_ref_in parameter
    - T_in_in: T_in_in parameter
    - p_pump_direct_in: p_pump_direct_in parameter
    - gamma_in: gamma_in parameter
    - f_loss_in: f_loss_in parameter
    - n_loops_in: n_loops_in parameter
    - dp_loop_ref_in: dp_loop_ref_in parameter
    - loop_live_in: loop_live_in parameter
    - eta_p_direct_in: eta_p_direct_in parameter
    - dT_blanket_in: dT_blanket_in parameter
    - p_loop_in: p_loop_in parameter
    - eta_is_in: eta_is_in parameter
    - mdot_loop_rated_in: mdot_loop_rated_in parameter
    - eta_drive_in: eta_drive_in parameter

Outputs:
    - p_loop_margin: p_loop_margin result
    - q_recovered_total: q_recovered_total result
    - p_elec: p_elec result
    - p_pump_total: p_pump_total result
    - T_out: T_out result
    - T_comp_in: T_comp_in result
    - dp_loop: dp_loop result
    - mdot_loop: mdot_loop result
    - w_fluid: w_fluid result
    - capacity_margin: capacity_margin result
    - q_ihx: q_ihx result
    - mdot: mdot result
    - r_comp: r_comp result

SysML Source: root-0/analyses/mfe_primary_loop.sysml:4

    SysML Source: root-0/analyses/mfe_primary_loop.sysml:4

    Calculation Specification:
        f_loss_in = 1.0
        eta_drive_in = 1.0
        loop_live_in = 0.0
        p_pump_direct_in = 0.0
        eta_p_direct_in = 0.0
        
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

INPUT DOMAIN (WI-056): cp_in and dT_blanket_in must each be finite
and strictly positive. cp is specific heat [J/(kg K)]; dT_blanket
is the positive coolant heating rise [K]. A negative pair is invalid.
Native typed manual completion raises ValueError before arithmetic.
This domain also applies for q_source = 0 and loop_live = 0 because
the chain always evaluates. Reference values are examples, not bounds.
The thirteen outputs below require this guarded manual completion;
the ordered equations above remain the normative valid calculation.

Compressor arithmetic also requires finite p_loop_in > dp_loop >= 0 Pa. Typed completion refuses nonpositive suction before division or fractional power and reports supplied pressure, calculated loss and suction. This mathematical prerequisite does not qualify the empirical loss law off its reference conditions. Unsupported execution supplies no completed plant evaluation.

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

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_primary_loop.primary_coolant_loop_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts p_loop_margin, q_recovered_total, p_elec, p_pump_total, T_out, T_comp_in, dp_loop, mdot_loop, w_fluid, capacity_margin, q_ihx, mdot, r_comp fields to separate channels.
    """

    name: str = "Primary_Coolant_LoopModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, q_source_in: float, cp_in: float, mdot_loop_ref_in: float, T_in_in: float, p_pump_direct_in: float, gamma_in: float, f_loss_in: float, n_loops_in: float, dp_loop_ref_in: float, loop_live_in: float, eta_p_direct_in: float, dT_blanket_in: float, p_loop_in: float, eta_is_in: float, mdot_loop_rated_in: float, eta_drive_in: float    ) -> Primary_Coolant_LoopInput:
        """Validate inputs and fill defaults.

        Args:
            q_source_in: q_source_in input
            cp_in: cp_in input
            mdot_loop_ref_in: mdot_loop_ref_in input
            T_in_in: T_in_in input
            p_pump_direct_in: p_pump_direct_in input
            gamma_in: gamma_in input
            f_loss_in: f_loss_in input
            n_loops_in: n_loops_in input
            dp_loop_ref_in: dp_loop_ref_in input
            loop_live_in: loop_live_in input
            eta_p_direct_in: eta_p_direct_in input
            dT_blanket_in: dT_blanket_in input
            p_loop_in: p_loop_in input
            eta_is_in: eta_is_in input
            mdot_loop_rated_in: mdot_loop_rated_in input
            eta_drive_in: eta_drive_in input

        Returns:
            Validated input model
        """
        return Primary_Coolant_LoopInput(q_source_in=q_source_in, cp_in=cp_in, mdot_loop_ref_in=mdot_loop_ref_in, T_in_in=T_in_in, p_pump_direct_in=p_pump_direct_in, gamma_in=gamma_in, f_loss_in=f_loss_in, n_loops_in=n_loops_in, dp_loop_ref_in=dp_loop_ref_in, loop_live_in=loop_live_in, eta_p_direct_in=eta_p_direct_in, dT_blanket_in=dT_blanket_in, p_loop_in=p_loop_in, eta_is_in=eta_is_in, mdot_loop_rated_in=mdot_loop_rated_in, eta_drive_in=eta_drive_in)

    def run(
        self, q_source_in: float, cp_in: float, mdot_loop_ref_in: float, T_in_in: float, p_pump_direct_in: float, gamma_in: float, f_loss_in: float, n_loops_in: float, dp_loop_ref_in: float, loop_live_in: float, eta_p_direct_in: float, dT_blanket_in: float, p_loop_in: float, eta_is_in: float, mdot_loop_rated_in: float, eta_drive_in: float    ) -> ModuleResult[Primary_Coolant_LoopOutput]:
        """Execute calculation.

        Args:
            q_source_in: q_source_in input
            cp_in: cp_in input
            mdot_loop_ref_in: mdot_loop_ref_in input
            T_in_in: T_in_in input
            p_pump_direct_in: p_pump_direct_in input
            gamma_in: gamma_in input
            f_loss_in: f_loss_in input
            n_loops_in: n_loops_in input
            dp_loop_ref_in: dp_loop_ref_in input
            loop_live_in: loop_live_in input
            eta_p_direct_in: eta_p_direct_in input
            dT_blanket_in: dT_blanket_in input
            p_loop_in: p_loop_in input
            eta_is_in: eta_is_in input
            mdot_loop_rated_in: mdot_loop_rated_in input
            eta_drive_in: eta_drive_in input

        Returns:
            Module result with Primary_Coolant_LoopOutput (p_loop_margin, q_recovered_total, p_elec, p_pump_total, T_out, T_comp_in, dp_loop, mdot_loop, w_fluid, capacity_margin, q_ihx, mdot, r_comp)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(q_source_in, cp_in, mdot_loop_ref_in, T_in_in, p_pump_direct_in, gamma_in, f_loss_in, n_loops_in, dp_loop_ref_in, loop_live_in, eta_p_direct_in, dT_blanket_in, p_loop_in, eta_is_in, mdot_loop_rated_in, eta_drive_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_primary_loop.primary_coolant_loop_impl import (
            run_primary_coolant_loop,
        )

        # Execute implementation - returns tuple of values
        p_loop_margin, q_recovered_total, p_elec, p_pump_total, T_out, T_comp_in, dp_loop, mdot_loop, w_fluid, capacity_margin, q_ihx, mdot, r_comp = run_primary_coolant_loop(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Primary_Coolant_LoopOutput(
                p_loop_margin=p_loop_margin,
                q_recovered_total=q_recovered_total,
                p_elec=p_elec,
                p_pump_total=p_pump_total,
                T_out=T_out,
                T_comp_in=T_comp_in,
                dp_loop=dp_loop,
                mdot_loop=mdot_loop,
                w_fluid=w_fluid,
                capacity_margin=capacity_margin,
                q_ihx=q_ihx,
                mdot=mdot,
                r_comp=r_comp,
            )
        )
