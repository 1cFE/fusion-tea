"""Primary_Bypass_ControlModule Module Wrapper

TEAx module for Primary_Bypass_Control calculation.

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

Inputs:
    - secondary_cp_in: secondary_cp_in parameter
    - secondary_flow_in: secondary_flow_in parameter
    - secondary_inlet_in: secondary_inlet_in parameter
    - duty_in: duty_in parameter
    - tolerance_in: tolerance_in parameter
    - primary_cp_in: primary_cp_in parameter
    - max_bypass_in: max_bypass_in parameter
    - ua_in: ua_in parameter
    - primary_flow_in: primary_flow_in parameter
    - required_return_in: required_return_in parameter
    - primary_limit_in: primary_limit_in parameter

Outputs:
    - capability_at_solution: capability_at_solution result
    - return_residual: return_residual result
    - exchanger_primary_flow: exchanger_primary_flow result
    - ntu_at_solution: ntu_at_solution result
    - exchanger_return: exchanger_return result
    - feasible: feasible result
    - effectiveness_at_solution: effectiveness_at_solution result
    - return_residual_magnitude: return_residual_magnitude result
    - bypass_fraction: bypass_fraction result
    - mixed_return: mixed_return result
    - capability_open: capability_open result

SysML Source: root-0/loop_return_control.sysml:3

SysML Source: root-0/loop_return_control.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/loop_return_control/primary_bypass_control_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.primary_bypass_control_output import Primary_Bypass_ControlOutput


class Primary_Bypass_ControlInput(BaseModel):
    """Input model for Primary_Bypass_ControlModule.

    Attributes:
        secondary_cp_in: secondary_cp_in input
        secondary_flow_in: secondary_flow_in input
        secondary_inlet_in: secondary_inlet_in input
        duty_in: duty_in input
        tolerance_in: tolerance_in input
        primary_cp_in: primary_cp_in input
        max_bypass_in: max_bypass_in input
        ua_in: ua_in input
        primary_flow_in: primary_flow_in input
        required_return_in: required_return_in input
        primary_limit_in: primary_limit_in input
    """
    secondary_cp_in: float = Field(..., description="secondary_cp_in input")
    secondary_flow_in: float = Field(..., description="secondary_flow_in input")
    secondary_inlet_in: float = Field(..., description="secondary_inlet_in input")
    duty_in: float = Field(..., description="duty_in input")
    tolerance_in: float = Field(..., description="tolerance_in input")
    primary_cp_in: float = Field(..., description="primary_cp_in input")
    max_bypass_in: float = Field(..., description="max_bypass_in input")
    ua_in: float = Field(..., description="ua_in input")
    primary_flow_in: float = Field(..., description="primary_flow_in input")
    required_return_in: float = Field(..., description="required_return_in input")
    primary_limit_in: float = Field(..., description="primary_limit_in input")


class Primary_Bypass_ControlModule(ModuleBase[Primary_Bypass_ControlInput, Primary_Bypass_ControlOutput]):
    """TEAx module for Primary_Bypass_Control calculation.

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

Inputs:
    - secondary_cp_in: secondary_cp_in parameter
    - secondary_flow_in: secondary_flow_in parameter
    - secondary_inlet_in: secondary_inlet_in parameter
    - duty_in: duty_in parameter
    - tolerance_in: tolerance_in parameter
    - primary_cp_in: primary_cp_in parameter
    - max_bypass_in: max_bypass_in parameter
    - ua_in: ua_in parameter
    - primary_flow_in: primary_flow_in parameter
    - required_return_in: required_return_in parameter
    - primary_limit_in: primary_limit_in parameter

Outputs:
    - capability_at_solution: capability_at_solution result
    - return_residual: return_residual result
    - exchanger_primary_flow: exchanger_primary_flow result
    - ntu_at_solution: ntu_at_solution result
    - exchanger_return: exchanger_return result
    - feasible: feasible result
    - effectiveness_at_solution: effectiveness_at_solution result
    - return_residual_magnitude: return_residual_magnitude result
    - bypass_fraction: bypass_fraction result
    - mixed_return: mixed_return result
    - capability_open: capability_open result

SysML Source: root-0/loop_return_control.sysml:3

    SysML Source: root-0/loop_return_control.sysml:3

    Calculation Specification:
        See documentation:
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

    IMPLEMENTATION: See component_alternatives_tea.handwritten.loop_return_control.primary_bypass_control_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts capability_at_solution, return_residual, exchanger_primary_flow, ntu_at_solution, exchanger_return, feasible, effectiveness_at_solution, return_residual_magnitude, bypass_fraction, mixed_return, capability_open fields to separate channels.
    """

    name: str = "Primary_Bypass_ControlModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, secondary_cp_in: float, secondary_flow_in: float, secondary_inlet_in: float, duty_in: float, tolerance_in: float, primary_cp_in: float, max_bypass_in: float, ua_in: float, primary_flow_in: float, required_return_in: float, primary_limit_in: float    ) -> Primary_Bypass_ControlInput:
        """Validate inputs and fill defaults.

        Args:
            secondary_cp_in: secondary_cp_in input
            secondary_flow_in: secondary_flow_in input
            secondary_inlet_in: secondary_inlet_in input
            duty_in: duty_in input
            tolerance_in: tolerance_in input
            primary_cp_in: primary_cp_in input
            max_bypass_in: max_bypass_in input
            ua_in: ua_in input
            primary_flow_in: primary_flow_in input
            required_return_in: required_return_in input
            primary_limit_in: primary_limit_in input

        Returns:
            Validated input model
        """
        return Primary_Bypass_ControlInput(secondary_cp_in=secondary_cp_in, secondary_flow_in=secondary_flow_in, secondary_inlet_in=secondary_inlet_in, duty_in=duty_in, tolerance_in=tolerance_in, primary_cp_in=primary_cp_in, max_bypass_in=max_bypass_in, ua_in=ua_in, primary_flow_in=primary_flow_in, required_return_in=required_return_in, primary_limit_in=primary_limit_in)

    def run(
        self, secondary_cp_in: float, secondary_flow_in: float, secondary_inlet_in: float, duty_in: float, tolerance_in: float, primary_cp_in: float, max_bypass_in: float, ua_in: float, primary_flow_in: float, required_return_in: float, primary_limit_in: float    ) -> ModuleResult[Primary_Bypass_ControlOutput]:
        """Execute calculation.

        Args:
            secondary_cp_in: secondary_cp_in input
            secondary_flow_in: secondary_flow_in input
            secondary_inlet_in: secondary_inlet_in input
            duty_in: duty_in input
            tolerance_in: tolerance_in input
            primary_cp_in: primary_cp_in input
            max_bypass_in: max_bypass_in input
            ua_in: ua_in input
            primary_flow_in: primary_flow_in input
            required_return_in: required_return_in input
            primary_limit_in: primary_limit_in input

        Returns:
            Module result with Primary_Bypass_ControlOutput (capability_at_solution, return_residual, exchanger_primary_flow, ntu_at_solution, exchanger_return, feasible, effectiveness_at_solution, return_residual_magnitude, bypass_fraction, mixed_return, capability_open)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(secondary_cp_in, secondary_flow_in, secondary_inlet_in, duty_in, tolerance_in, primary_cp_in, max_bypass_in, ua_in, primary_flow_in, required_return_in, primary_limit_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.loop_return_control.primary_bypass_control_impl import (
            run_primary_bypass_control,
        )

        # Execute implementation - returns tuple of values
        capability_at_solution, return_residual, exchanger_primary_flow, ntu_at_solution, exchanger_return, feasible, effectiveness_at_solution, return_residual_magnitude, bypass_fraction, mixed_return, capability_open = run_primary_bypass_control(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Primary_Bypass_ControlOutput(
                capability_at_solution=capability_at_solution,
                return_residual=return_residual,
                exchanger_primary_flow=exchanger_primary_flow,
                ntu_at_solution=ntu_at_solution,
                exchanger_return=exchanger_return,
                feasible=feasible,
                effectiveness_at_solution=effectiveness_at_solution,
                return_residual_magnitude=return_residual_magnitude,
                bypass_fraction=bypass_fraction,
                mixed_return=mixed_return,
                capability_open=capability_open,
            )
        )
