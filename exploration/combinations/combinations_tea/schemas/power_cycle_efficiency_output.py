from pydantic import Field
from simkit.config.schema import MultiOutput

class Power_Cycle_EfficiencyOutput(MultiOutput):
    """Multi-output container for Power_Cycle_Efficiency.

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

SysML Source: root-0/mfe_power_cycle.sysml:4
    """
    margin_low: float = Field(description="margin_low output")
    T2_C: float = Field(description="T2_C output")
    margin_high: float = Field(description="margin_high output")
    eta_th: float = Field(description="eta_th output")
    eta_fit: float = Field(description="eta_fit output")
    domain_product: float = Field(description="domain_product output")
