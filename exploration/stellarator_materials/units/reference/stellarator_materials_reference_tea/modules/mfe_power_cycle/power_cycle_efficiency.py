"""Power_Cycle_EfficiencyModule Module Wrapper

TEAx module for Power_Cycle_Efficiency calculation.

Secondary-cycle efficiency from the primary loop's outlet temperature by a
printed fit (WI-045, goal plant-closure):

  T2_C           = T_hot - dT_approach - 273.15          [C]  (physical conversion)
  eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta   [1]
  eta_th         = cycle_live * eta_fit + eta_th_direct  [1]
  margin_low     = T2_C - T2_min                         [C]
  margin_high    = T2_max - T2_C                         [C]
  domain_product = margin_low * margin_high              [C^2]

THE FIT'S VERSION CONTRACT: the printed Kovari et al. 2016 Table 4 form
uses the literal 273 inside the logarithm (T_offset_fit); the physical
273.15 converts the loop's kelvin outlet to the fit's Celsius argument.
They are different numbers on purpose (the research section D). The
fit is used literally; delta_eta is the printed low-temperature-divertor
correction, bound 0 by an instance that carries no divertor loop, said so
at the binding. The fit is a correlation on other codes' cycle modelling
(Dostal, with the 0.0179 benchmark adjustment already inside the printed
coefficients), not a measured plant efficiency.

FAIL CLOSED: outside [T2_min, T2_max] the paired 'Cycle Fit Domain'
constraint reads violated on domain_product; eta_fit is still published,
never clamped or extrapolated silently. A non-positive logarithm argument
raises in the executable.

DORMANCY (packet section 3): cycle_live 0 with eta_th_direct at the old
held efficiency gives eta_th = 0.0 * eta_fit + eta_th_direct, the old
scalar to the bit.

EXECUTABLE SEMANTIC (Rung B, the WI-029 CAS72 pattern): the logarithm is
outside the codegen arithmetic envelope (+ - * / ** only), so this calc
routes to the handwritten codegen stage (manual_required). The generated
handwritten impl is normative and is guarded bit-exact (rel 1e-9) by the
oracle mirror in verify_stellaris.py. The outputs are declared without
expressions (a manual interface); the chain above is the model-resident
statement.

*Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
(Kovari et al. 2016, FED 104, 9-20, DOI 10.1016/j.fusengdes.2016.01.007)
*Ref**: output.md:355 (Table 4: the fitting functions, T2 ranges, T1-T2 approach);
journal p. 17 render work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png
*Basis**: printed secondary-cycle efficiency correlation on the turbine-inlet temperature;
concept-agnostic (MR-3) -- coefficients, domain and approach bound by instances

Inputs:
    - eta_th_direct_in: eta_th_direct_in parameter
    - delta_eta_in: delta_eta_in parameter
    - b_fit_in: b_fit_in parameter
    - cycle_live_in: cycle_live_in parameter
    - T_hot_in: T_hot_in parameter
    - T2_min_in: T2_min_in parameter
    - dT_approach_in: dT_approach_in parameter
    - T2_max_in: T2_max_in parameter
    - a_fit_in: a_fit_in parameter
    - T_offset_fit_in: T_offset_fit_in parameter

Outputs:
    - margin_low: margin_low result
    - T2_C: T2_C result
    - margin_high: margin_high result
    - eta_th: eta_th result
    - eta_fit: eta_fit result
    - domain_product: domain_product result

SysML Source: root-0/analyses/mfe_power_cycle.sysml:4

SysML Source: root-0/analyses/mfe_power_cycle.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.power_cycle_efficiency_output import Power_Cycle_EfficiencyOutput


class Power_Cycle_EfficiencyInput(BaseModel):
    """Input model for Power_Cycle_EfficiencyModule.

    Attributes:
        eta_th_direct_in: eta_th_direct_in input
        delta_eta_in: delta_eta_in input
        b_fit_in: b_fit_in input
        cycle_live_in: cycle_live_in input
        T_hot_in: T_hot_in input
        T2_min_in: T2_min_in input
        dT_approach_in: dT_approach_in input
        T2_max_in: T2_max_in input
        a_fit_in: a_fit_in input
        T_offset_fit_in: T_offset_fit_in input
    """
    eta_th_direct_in: float = Field(..., description="eta_th_direct_in input")
    delta_eta_in: float = Field(..., description="delta_eta_in input")
    b_fit_in: float = Field(..., description="b_fit_in input")
    cycle_live_in: float = Field(..., description="cycle_live_in input")
    T_hot_in: float = Field(..., description="T_hot_in input")
    T2_min_in: float = Field(..., description="T2_min_in input")
    dT_approach_in: float = Field(..., description="dT_approach_in input")
    T2_max_in: float = Field(..., description="T2_max_in input")
    a_fit_in: float = Field(..., description="a_fit_in input")
    T_offset_fit_in: float = Field(..., description="T_offset_fit_in input")


class Power_Cycle_EfficiencyModule(ModuleBase[Power_Cycle_EfficiencyInput, Power_Cycle_EfficiencyOutput]):
    """TEAx module for Power_Cycle_Efficiency calculation.

Secondary-cycle efficiency from the primary loop's outlet temperature by a
printed fit (WI-045, goal plant-closure):

  T2_C           = T_hot - dT_approach - 273.15          [C]  (physical conversion)
  eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta   [1]
  eta_th         = cycle_live * eta_fit + eta_th_direct  [1]
  margin_low     = T2_C - T2_min                         [C]
  margin_high    = T2_max - T2_C                         [C]
  domain_product = margin_low * margin_high              [C^2]

THE FIT'S VERSION CONTRACT: the printed Kovari et al. 2016 Table 4 form
uses the literal 273 inside the logarithm (T_offset_fit); the physical
273.15 converts the loop's kelvin outlet to the fit's Celsius argument.
They are different numbers on purpose (the research section D). The
fit is used literally; delta_eta is the printed low-temperature-divertor
correction, bound 0 by an instance that carries no divertor loop, said so
at the binding. The fit is a correlation on other codes' cycle modelling
(Dostal, with the 0.0179 benchmark adjustment already inside the printed
coefficients), not a measured plant efficiency.

FAIL CLOSED: outside [T2_min, T2_max] the paired 'Cycle Fit Domain'
constraint reads violated on domain_product; eta_fit is still published,
never clamped or extrapolated silently. A non-positive logarithm argument
raises in the executable.

DORMANCY (packet section 3): cycle_live 0 with eta_th_direct at the old
held efficiency gives eta_th = 0.0 * eta_fit + eta_th_direct, the old
scalar to the bit.

EXECUTABLE SEMANTIC (Rung B, the WI-029 CAS72 pattern): the logarithm is
outside the codegen arithmetic envelope (+ - * / ** only), so this calc
routes to the handwritten codegen stage (manual_required). The generated
handwritten impl is normative and is guarded bit-exact (rel 1e-9) by the
oracle mirror in verify_stellaris.py. The outputs are declared without
expressions (a manual interface); the chain above is the model-resident
statement.

*Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
(Kovari et al. 2016, FED 104, 9-20, DOI 10.1016/j.fusengdes.2016.01.007)
*Ref**: output.md:355 (Table 4: the fitting functions, T2 ranges, T1-T2 approach);
journal p. 17 render work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png
*Basis**: printed secondary-cycle efficiency correlation on the turbine-inlet temperature;
concept-agnostic (MR-3) -- coefficients, domain and approach bound by instances

Inputs:
    - eta_th_direct_in: eta_th_direct_in parameter
    - delta_eta_in: delta_eta_in parameter
    - b_fit_in: b_fit_in parameter
    - cycle_live_in: cycle_live_in parameter
    - T_hot_in: T_hot_in parameter
    - T2_min_in: T2_min_in parameter
    - dT_approach_in: dT_approach_in parameter
    - T2_max_in: T2_max_in parameter
    - a_fit_in: a_fit_in parameter
    - T_offset_fit_in: T_offset_fit_in parameter

Outputs:
    - margin_low: margin_low result
    - T2_C: T2_C result
    - margin_high: margin_high result
    - eta_th: eta_th result
    - eta_fit: eta_fit result
    - domain_product: domain_product result

SysML Source: root-0/analyses/mfe_power_cycle.sysml:4

    SysML Source: root-0/analyses/mfe_power_cycle.sysml:4

    Calculation Specification:
        delta_eta_in = 0.0
        cycle_live_in = 0.0
        eta_th_direct_in = 0.0
        
Documentation:
Secondary-cycle efficiency from the primary loop's outlet temperature by a
printed fit (WI-045, goal plant-closure):

  T2_C           = T_hot - dT_approach - 273.15          [C]  (physical conversion)
  eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta   [1]
  eta_th         = cycle_live * eta_fit + eta_th_direct  [1]
  margin_low     = T2_C - T2_min                         [C]
  margin_high    = T2_max - T2_C                         [C]
  domain_product = margin_low * margin_high              [C^2]

THE FIT'S VERSION CONTRACT: the printed Kovari et al. 2016 Table 4 form
uses the literal 273 inside the logarithm (T_offset_fit); the physical
273.15 converts the loop's kelvin outlet to the fit's Celsius argument.
They are different numbers on purpose (the research section D). The
fit is used literally; delta_eta is the printed low-temperature-divertor
correction, bound 0 by an instance that carries no divertor loop, said so
at the binding. The fit is a correlation on other codes' cycle modelling
(Dostal, with the 0.0179 benchmark adjustment already inside the printed
coefficients), not a measured plant efficiency.

FAIL CLOSED: outside [T2_min, T2_max] the paired 'Cycle Fit Domain'
constraint reads violated on domain_product; eta_fit is still published,
never clamped or extrapolated silently. A non-positive logarithm argument
raises in the executable.

DORMANCY (packet section 3): cycle_live 0 with eta_th_direct at the old
held efficiency gives eta_th = 0.0 * eta_fit + eta_th_direct, the old
scalar to the bit.

EXECUTABLE SEMANTIC (Rung B, the WI-029 CAS72 pattern): the logarithm is
outside the codegen arithmetic envelope (+ - * / ** only), so this calc
routes to the handwritten codegen stage (manual_required). The generated
handwritten impl is normative and is guarded bit-exact (rel 1e-9) by the
oracle mirror in verify_stellaris.py. The outputs are declared without
expressions (a manual interface); the chain above is the model-resident
statement.

*Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
(Kovari et al. 2016, FED 104, 9-20, DOI 10.1016/j.fusengdes.2016.01.007)
*Ref**: output.md:355 (Table 4: the fitting functions, T2 ranges, T1-T2 approach);
journal p. 17 render work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png
*Basis**: printed secondary-cycle efficiency correlation on the turbine-inlet temperature;
concept-agnostic (MR-3) -- coefficients, domain and approach bound by instances

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_power_cycle.power_cycle_efficiency_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product fields to separate channels.
    """

    name: str = "Power_Cycle_EfficiencyModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, eta_th_direct_in: float, delta_eta_in: float, b_fit_in: float, cycle_live_in: float, T_hot_in: float, T2_min_in: float, dT_approach_in: float, T2_max_in: float, a_fit_in: float, T_offset_fit_in: float    ) -> Power_Cycle_EfficiencyInput:
        """Validate inputs and fill defaults.

        Args:
            eta_th_direct_in: eta_th_direct_in input
            delta_eta_in: delta_eta_in input
            b_fit_in: b_fit_in input
            cycle_live_in: cycle_live_in input
            T_hot_in: T_hot_in input
            T2_min_in: T2_min_in input
            dT_approach_in: dT_approach_in input
            T2_max_in: T2_max_in input
            a_fit_in: a_fit_in input
            T_offset_fit_in: T_offset_fit_in input

        Returns:
            Validated input model
        """
        return Power_Cycle_EfficiencyInput(eta_th_direct_in=eta_th_direct_in, delta_eta_in=delta_eta_in, b_fit_in=b_fit_in, cycle_live_in=cycle_live_in, T_hot_in=T_hot_in, T2_min_in=T2_min_in, dT_approach_in=dT_approach_in, T2_max_in=T2_max_in, a_fit_in=a_fit_in, T_offset_fit_in=T_offset_fit_in)

    def run(
        self, eta_th_direct_in: float, delta_eta_in: float, b_fit_in: float, cycle_live_in: float, T_hot_in: float, T2_min_in: float, dT_approach_in: float, T2_max_in: float, a_fit_in: float, T_offset_fit_in: float    ) -> ModuleResult[Power_Cycle_EfficiencyOutput]:
        """Execute calculation.

        Args:
            eta_th_direct_in: eta_th_direct_in input
            delta_eta_in: delta_eta_in input
            b_fit_in: b_fit_in input
            cycle_live_in: cycle_live_in input
            T_hot_in: T_hot_in input
            T2_min_in: T2_min_in input
            dT_approach_in: dT_approach_in input
            T2_max_in: T2_max_in input
            a_fit_in: a_fit_in input
            T_offset_fit_in: T_offset_fit_in input

        Returns:
            Module result with Power_Cycle_EfficiencyOutput (margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(eta_th_direct_in, delta_eta_in, b_fit_in, cycle_live_in, T_hot_in, T2_min_in, dT_approach_in, T2_max_in, a_fit_in, T_offset_fit_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_power_cycle.power_cycle_efficiency_impl import (
            run_power_cycle_efficiency,
        )

        # Execute implementation - returns tuple of values
        margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product = run_power_cycle_efficiency(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Power_Cycle_EfficiencyOutput(
                margin_low=margin_low,
                T2_C=T2_C,
                margin_high=margin_high,
                eta_th=eta_th,
                eta_fit=eta_fit,
                domain_product=domain_product,
            )
        )
