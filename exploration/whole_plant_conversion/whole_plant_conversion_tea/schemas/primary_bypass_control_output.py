from pydantic import Field
from simkit.config.schema import MultiOutput

class Primary_Bypass_ControlOutput(MultiOutput):
    """Multi-output container for Primary_Bypass_Control.

Primary-side bypass control that holds a heat-driven loop's return
requirement at a counterflow exchanger (WI-095, goal design-study-parameters,
the owner's direction of 2026-09-26). The loop delivers the duty q at the
primary temperature T_out with heat capacity rate C_h = primary_flow * primary_cp
/ 1e6 [MW/K] and requires the helium back at required_return = T_out - q / C_h
(the 'Primary Coolant Loop' T_comp_in). A fraction f of the primary flow
bypasses the exchanger at T_out and mixes with the exchanger outlet; the
exchanger sees C_h(f) = (1 - f) * C_h against the secondary rate
C_s = secondary_flow * secondary_cp / 1e6 entering at secondary_inlet, with
conductance UA [MW/K]:
  C_min = min(C_h(f), C_s), C_max = max(C_h(f), C_s), C_r = C_min / C_max,
  NTU = UA / C_min,
  eps = NTU / (1 + NTU)                                   if |1 - C_r| < 1e-10,
  eps = (1 - exp(-NTU (1 - C_r))) / (1 - C_r exp(-NTU (1 - C_r)))   otherwise,
  capability(f) = eps * C_min * max(T_out - secondary_inlet, 0)   [MW]
(the closure body's form, so capability(0) equals the closure's stage capability).
capability decreases strictly in f: with u = UA / C_h(f) - UA / C_s the
counterflow form is capability = UA (T_out - secondary_inlet) / (u / (1 - exp(-u))
+ UA / C_s), u / (1 - exp(-u)) increases in u and u increases as C_h(f) falls;
capability tends to 0 as f tends to 1, so the root is unique. The control solves
capability(f) = q for f in [0, 1) by bisection (|capability - q| <= 1e-9 MW or an
interval below 1e-15, at most 200 iterations); a bracket that is not decreasing
and bisection exhaustion both raise (a refusal, never a returned value). Outputs:
  feasible                = 1 if capability(0) >= q else 0
  capability_open         = capability(0)
  bypass_fraction         = f (0 when infeasible)
  capability_at_solution  = capability(f)                          [MW]
  exchanger_primary_flow  = (1 - f) * primary_flow                 [kg/s]
  exchanger_return        = T_out - capability(f) / C_h(f)         [K]
    (the outlet the exchanger reaches, never computed from q; f = 0 when infeasible)
  mixed_return            = f * T_out + (1 - f) * exchanger_return
                          = T_out - capability(f) / C_h               [K]
  return_residual         = mixed_return - required_return         [K]
  return_residual_magnitude = |return_residual|                     [K]
  effectiveness_at_solution, ntu_at_solution at f (at 0 when infeasible)
The residual is (q - capability(f)) / C_h plus the loop-side identity
T_out - q / C_h - required_return (zero when the exchanger cp equals the loop cp):
about 1e-10 K at the solve tolerance when feasible, the physical deficit
(q - capability(0)) / C_h when infeasible, so 'Return Condition Held' at 1e-6 K
is the root-solve closure and fails every infeasible case. The bypass's own pressure loss, valve
hardware and cost are not modeled. Domain: primary_flow, primary_cp,
secondary_flow, secondary_cp > 0; UA >= 0; q >= 0; 0 <= max_bypass <= 1;
tolerance > 0; a stage with T_out <= secondary_inlet has capability 0.
*Source**: work/active/WI-095_loop-return-control/design.md section 1-3
*Ref**: models/library/analyses/mfe_primary_loop.sysml (T_comp_in requirement);
the 'Network Heat Driven Closure' body stage arithmetic
*Basis**: [AGENT] explicit control model of a stated requirement; concept-agnostic (MR-3)

SysML Source: root-0/loop_return_control.sysml:3
    """
    capability_at_solution: float = Field(description="capability_at_solution output")
    return_residual: float = Field(description="return_residual output")
    exchanger_primary_flow: float = Field(description="exchanger_primary_flow output")
    ntu_at_solution: float = Field(description="ntu_at_solution output")
    exchanger_return: float = Field(description="exchanger_return output")
    feasible: float = Field(description="feasible output")
    effectiveness_at_solution: float = Field(description="effectiveness_at_solution output")
    return_residual_magnitude: float = Field(description="return_residual_magnitude output")
    bypass_fraction: float = Field(description="bypass_fraction output")
    mixed_return: float = Field(description="mixed_return output")
    capability_open: float = Field(description="capability_open output")
