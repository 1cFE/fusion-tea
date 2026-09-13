from pydantic import Field
from simkit.config.schema import MultiOutput

class Lifecycle_CalendarOutput(MultiOutput):
    """Multi-output container for Lifecycle_Calendar.

One clock for the neutron-damage-limited in-vessel set (first wall /
blanket + divertor, bundled): physical life -> a dated replacement
calendar over the plant horizon -> productive full-power years,
downtimes, availability, the replacement present value and CAS72.
Replaces 'Levelized Replacement Cost' (WI-029 / WI-041), whose periodic
physical timing is carried as this calc's HELD MODE (WI-046; goal
plant-closure round 1; basis packet sections 2, 3, 8).

LIVE MODE (availability_direct_in = 0), the deterministic finite-horizon
calendar (research Option B):

  L      = fluence_limit / q_n                         [FPY] (q_n = 0: infinite)
  b      = 1 - u                                       productive fraction online
  walk from t = 0 with new components in capital: an online interval
  accrues productive time b*dt and unplanned downtime u*dt; when the
  accumulated life reaches L an outage of length d starts at that date
  t_k, the event is charged at t_k, nothing ages during the outage, and
  the bundled clock resets; a replacement is bought only if restart
  t_k + d falls STRICTLY before N; otherwise production ceases at t_k
  and N - t_k is terminal downtime; the horizon ending mid-run closes the
  last interval.
  Closed form for one bundled event: t_k = k*L/b + (k-1)*d.
  F + T_planned + T_unplanned + T_terminal = N          (identity)
  availability     = F / N
  replacement_pv   = sum_k C / (1+i)^t_k                (payment at outage start)
  cas72_annual     = CRF(i, N) * replacement_pv         (CRF = 1/N at i = 0)
  coil_life_margin = coil_life - F                      (reported, never a fence)
  dated_energy_ratio = PV of the calendar's yearly energy over the PV of the
                       uniform annual-equivalent energy (P_net cancels);
                       1.0 for uniform production; the exact-DCF headline
                       would divide by this ratio -- the annual-equivalent
                       convention stays the headline (WI-029 Option ii).

HELD MODE (availability_direct_in > 0), the retired physical chain
(levelized_replacement_cost_impl.py:70-101 at the WI-044 pin, the 1cfe
guards carried as WI-029 MF-1 carried them; economics.py:53-75,
model.py:102-111 at pin 0254385):

  core_lifetime_FPY = clip(fluence_limit / max(q_n, 1e-6), 0.5, N*A)
  core_lifetime_cal = core_lifetime_FPY / A
  s                 = (1 + i)^(-core_lifetime_cal)
  n_rep             = max(0, ceil(N / core_lifetime_cal) - 1)
  pv                = C * s * (1 - s^n_rep) / (1 - s)
  cas72_annual      = CRF(i, N) * pv
  availability      = A;  F = N*A;  T_unplanned = N - N*A (undifferentiated)

The held mode is the compatibility bridge: with availability_direct at a
concept's former constant its physical outputs remain bit-identical. Finance
uses stable equivalent rate-limit expressions (WI-052). It is not a calendar and its
guards are not material evidence (the 0.5 FPY floor is a gradient guard,
the N*A cap a horizon cap); the live mode has neither and fails loudly
on an invalid input.

WHAT THIS IS NOT: whole-plant lifetime closure. One bundled event; the
divertor's separate life, other scheduled maintenance (cryoplant,
turbine, vacuum, fuel systems), decay-heat cooling and imported
electricity during outages, replacement labour and waste are outside it;
the coil's finite dose life is a reported margin because no admissible
source gives its response to shielding or geometry. Availability
integrates TIME: the loop, the exhaust and the conversion are sized at
the online operating point and are not derated by it. Fixed staffing
(CAS71) stays per calendar year; no lost-sales cost is added while the
energy is removed from the denominator.

EXECUTABLE SEMANTIC: the walk and ceil are outside the codegen envelope
(+ - * / ** only), so this calc routes to the handwritten stage
(manual_required); the generated handwritten impl is normative and is
checked by independent dated-flow and yearly-energy references in
tests/models/test_mfe_financial_calendar.py. The legacy study oracle
retains its separately scoped finance migration.

Concept-agnostic: every quantity is an input (MR-3). Event dates are a
diagnostic artifact of the impl, not outputs.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf (Stellaris, sec. 2.11, pp. 28-29; Table 6, p. 21 -- read as the renders under work/orchestration/goals/plant-closure/evidence/grounding_sources/); knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md (Kovari et al. 2016, sec. 8); /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: Stellaris p. 29 (seven months estimated; five months and 90 % targets; four years between major maintenance); p. 28 (cooldown and recommissioning ~30 days each, inside the estimate); Table 6 (first-wall structure lifetime ~4-6 FPY; coil lifetime ~10 FPY); Kovari 2016 sec. 8 eq. 54 (planned / unplanned overlap), eqs. 55-59 (blanket / divertor lifetimes and outages -- the precedent for distinct lives, not adopted); economics.py:53-75, model.py:102-111 (the held chain); knowledge/research/pending/20260907-163520_lifetime-availability-closure-prework.md sec. Option B
*Basis**: deterministic finite-horizon replacement calendar on the peak wall load; annual-equivalent economics with the exact-dated shadow
*Source**: native calendar equations above; the preceding external citations are inherited and not reverified by WI-052
*Ref**: work/active/WI-052_mfe-financial-rate-limits/design.md, Numerical method and justification
*Basis**: stable CRF, held periodic PV and dated log1p discount weights; event walk, clipping, count and yearly-bin accumulation retained
*Last Updated**: 2026-09-12 (native equation and numerical method verification)

SysML Source: root-0/analyses/mfe_lifecycle.sysml:4
    """
    availability: float = Field(description="availability output")
    coil_life_margin_fpy: float = Field(description="coil_life_margin_fpy output")
    replacement_pv: float = Field(description="replacement_pv output")
    planned_downtime_yr: float = Field(description="planned_downtime_yr output")
    terminal_downtime_yr: float = Field(description="terminal_downtime_yr output")
    unplanned_downtime_yr: float = Field(description="unplanned_downtime_yr output")
    productive_fpy: float = Field(description="productive_fpy output")
    dated_energy_ratio: float = Field(description="dated_energy_ratio output")
    cas72_annual: float = Field(description="cas72_annual output")
    n_replacements: float = Field(description="n_replacements output")
    physical_life_fpy: float = Field(description="physical_life_fpy output")
