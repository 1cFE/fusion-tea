"""Levelized_Replacement_CostModule Module Wrapper

TEAx module for Levelized_Replacement_Cost calculation.

CAS72 levelized scheduled-replacement cost of the neutron-damage-
limited in-vessel accounts (first wall / blanket + divertor):

  q_n              = the wall load handed in             [MW/m^2]
  core_lifetime_FPY= clip(fluence_limit / max(q_n, 1e-6),
                          0.5, operational_years*availability)
  core_lifetime_cal= core_lifetime_FPY / availability     [cal-yr]
  s                = (1 + i)^(-core_lifetime_cal)
  n_rep            = max(0, ceil(operational_years/core_lifetime_cal) - 1)
  pv               = cost_per_event * s * (1 - s^n_rep) / (1 - s)
  cost             = CRF(i, n) * pv

The replaceable core survives a fixed neutron fluence, so its life in
full-power years is the fluence limit divided by the wall load, and its
calendar life divides again by availability. Each replacement is a
discrete event discounted at its own date; `n_rep` counts the events
inside the plant life (the final core is never replaced, hence -1).

THE WALL LOAD IS AN INPUT, NOT COMPUTED HERE (WI-041). The plant binds
the PEAK neutron wall load ('Neutron Wall Load Peak'), because the
source and its cited method set in-vessel lifetime by the peak load and
not the average: Stellaris Table 6 derives the first-wall lifetime
(~4-6 FPY) from the peak first-wall DPA, and Lion 2022 states "the
lifetime of the blanket is determined by the peak loads". A concept
with no source peak binds a calibration of 1.0 and its average arrives
here unchanged. Before WI-041 this calc computed its own neutron power
over the circular-torus area, i.e. the average.

EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): `max`, `min` and `floor`
are invocations, which fall outside the codegen arithmetic envelope
(+ - * / ** only, calc_compat_renderer.py:39-46), so this calc routes
to the handwritten codegen stage (manual_required). The generated
handwritten impl is normative and is guarded bit-exact (rel 1e-9) by
the oracle mirror in verify_stellaris.py. Both carry 1cfe's guards
VERBATIM -- the clip floor/cap, the inner max(q_n, 1e-6), and the outer
max(0, ...) -- rather than dropping them as point-inert no-ops: they go
live at study-sweep extremes and a dropped guard would return a wrong
CAS72 silently and discontinuously.

Two faithful re-expressions in the model-resident statement, both exact
identities changing no value: clip(z, lo, hi) is written min(max(z, lo),
hi) -- jnp.clip's own order -- and ceil(z) is written -floor(-z) (the KerML
Real function library has floor, min and max but no ceiling or clip). The handwritten impl
uses Python's math.ceil and the same guards directly.

EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
marked for revert -- see models/stellarator_migration_ledger.md): the
pinned codegen admits no function invocation (max/min/floor) in an
executable expression, so the model-resident statement of the chain
above is carried as this doc and the output is declared without an
expression (a manual interface). The pre-migration body, with the
intermediates p_neutron, q_n, fpy_raw, fpy_cap, core_lifetime_fpy,
core_lifetime_cal, s, n_rep, pv, disc_pow_n, crf, is recorded verbatim
in the ledger row and in git at the migration PR's parent.

`n_rep` is a discontinuous step function of the live neutron/geometry
chain and is computed every run -- never frozen as a defaulted input.

Concept-agnostic: the fluence limit, the wall loading, the replaceable-
account cost, and the plant life are all inputs (MR-3).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385); knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
*Ref**: economics.py:53-75 (levelized_replacement_cost); model.py:102-111
(_core_lifetime_fpy, the clip and inner max); economics.py:6-10 (CRF);
defaults.py:291 (fluence_limit_dt), defaults.py:299 (replaceable accounts);
Stellaris Table 6 image (images/page_020_table_0.png: peak DPA in the
first wall 10.7 DPA/FPY -> estimated first-wall lifetime ~4-6 FPY);
Lion 2022 output.md line 88 (lifetime determined by the peak loads)
*Basis**: Fluence-limited replacement schedule on the peak wall load, discretely discounted and annuitized

Inputs:
    - q_n_in: q_n_in parameter
    - cost_per_event: cost_per_event parameter
    - operational_years_in: operational_years_in parameter
    - availability_in: availability_in parameter
    - fluence_limit_in: fluence_limit_in parameter
    - interest_rate: interest_rate parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:796

SysML Source: root-0/analyses/mfe_account_costs.sysml:796

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/levelized_replacement_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Levelized_Replacement_CostInput(BaseModel):
    """Input model for Levelized_Replacement_CostModule.

    Attributes:
        q_n_in: q_n_in input
        cost_per_event: cost_per_event input
        operational_years_in: operational_years_in input
        availability_in: availability_in input
        fluence_limit_in: fluence_limit_in input
        interest_rate: interest_rate input
    """
    q_n_in: float = Field(..., description="q_n_in input")
    cost_per_event: float = Field(..., description="cost_per_event input")
    operational_years_in: float = Field(..., description="operational_years_in input")
    availability_in: float = Field(..., description="availability_in input")
    fluence_limit_in: float = Field(..., description="fluence_limit_in input")
    interest_rate: float = Field(..., description="interest_rate input")


class Levelized_Replacement_CostModule(ModuleBase[Levelized_Replacement_CostInput, Float]):
    """TEAx module for Levelized_Replacement_Cost calculation.

CAS72 levelized scheduled-replacement cost of the neutron-damage-
limited in-vessel accounts (first wall / blanket + divertor):

  q_n              = the wall load handed in             [MW/m^2]
  core_lifetime_FPY= clip(fluence_limit / max(q_n, 1e-6),
                          0.5, operational_years*availability)
  core_lifetime_cal= core_lifetime_FPY / availability     [cal-yr]
  s                = (1 + i)^(-core_lifetime_cal)
  n_rep            = max(0, ceil(operational_years/core_lifetime_cal) - 1)
  pv               = cost_per_event * s * (1 - s^n_rep) / (1 - s)
  cost             = CRF(i, n) * pv

The replaceable core survives a fixed neutron fluence, so its life in
full-power years is the fluence limit divided by the wall load, and its
calendar life divides again by availability. Each replacement is a
discrete event discounted at its own date; `n_rep` counts the events
inside the plant life (the final core is never replaced, hence -1).

THE WALL LOAD IS AN INPUT, NOT COMPUTED HERE (WI-041). The plant binds
the PEAK neutron wall load ('Neutron Wall Load Peak'), because the
source and its cited method set in-vessel lifetime by the peak load and
not the average: Stellaris Table 6 derives the first-wall lifetime
(~4-6 FPY) from the peak first-wall DPA, and Lion 2022 states "the
lifetime of the blanket is determined by the peak loads". A concept
with no source peak binds a calibration of 1.0 and its average arrives
here unchanged. Before WI-041 this calc computed its own neutron power
over the circular-torus area, i.e. the average.

EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): `max`, `min` and `floor`
are invocations, which fall outside the codegen arithmetic envelope
(+ - * / ** only, calc_compat_renderer.py:39-46), so this calc routes
to the handwritten codegen stage (manual_required). The generated
handwritten impl is normative and is guarded bit-exact (rel 1e-9) by
the oracle mirror in verify_stellaris.py. Both carry 1cfe's guards
VERBATIM -- the clip floor/cap, the inner max(q_n, 1e-6), and the outer
max(0, ...) -- rather than dropping them as point-inert no-ops: they go
live at study-sweep extremes and a dropped guard would return a wrong
CAS72 silently and discontinuously.

Two faithful re-expressions in the model-resident statement, both exact
identities changing no value: clip(z, lo, hi) is written min(max(z, lo),
hi) -- jnp.clip's own order -- and ceil(z) is written -floor(-z) (the KerML
Real function library has floor, min and max but no ceiling or clip). The handwritten impl
uses Python's math.ceil and the same guards directly.

EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
marked for revert -- see models/stellarator_migration_ledger.md): the
pinned codegen admits no function invocation (max/min/floor) in an
executable expression, so the model-resident statement of the chain
above is carried as this doc and the output is declared without an
expression (a manual interface). The pre-migration body, with the
intermediates p_neutron, q_n, fpy_raw, fpy_cap, core_lifetime_fpy,
core_lifetime_cal, s, n_rep, pv, disc_pow_n, crf, is recorded verbatim
in the ledger row and in git at the migration PR's parent.

`n_rep` is a discontinuous step function of the live neutron/geometry
chain and is computed every run -- never frozen as a defaulted input.

Concept-agnostic: the fluence limit, the wall loading, the replaceable-
account cost, and the plant life are all inputs (MR-3).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385); knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
*Ref**: economics.py:53-75 (levelized_replacement_cost); model.py:102-111
(_core_lifetime_fpy, the clip and inner max); economics.py:6-10 (CRF);
defaults.py:291 (fluence_limit_dt), defaults.py:299 (replaceable accounts);
Stellaris Table 6 image (images/page_020_table_0.png: peak DPA in the
first wall 10.7 DPA/FPY -> estimated first-wall lifetime ~4-6 FPY);
Lion 2022 output.md line 88 (lifetime determined by the peak loads)
*Basis**: Fluence-limited replacement schedule on the peak wall load, discretely discounted and annuitized

Inputs:
    - q_n_in: q_n_in parameter
    - cost_per_event: cost_per_event parameter
    - operational_years_in: operational_years_in parameter
    - availability_in: availability_in parameter
    - fluence_limit_in: fluence_limit_in parameter
    - interest_rate: interest_rate parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:796

    SysML Source: root-0/analyses/mfe_account_costs.sysml:796

    Calculation Specification:
        See documentation:
CAS72 levelized scheduled-replacement cost of the neutron-damage-
limited in-vessel accounts (first wall / blanket + divertor):

  q_n              = the wall load handed in             [MW/m^2]
  core_lifetime_FPY= clip(fluence_limit / max(q_n, 1e-6),
                          0.5, operational_years*availability)
  core_lifetime_cal= core_lifetime_FPY / availability     [cal-yr]
  s                = (1 + i)^(-core_lifetime_cal)
  n_rep            = max(0, ceil(operational_years/core_lifetime_cal) - 1)
  pv               = cost_per_event * s * (1 - s^n_rep) / (1 - s)
  cost             = CRF(i, n) * pv

The replaceable core survives a fixed neutron fluence, so its life in
full-power years is the fluence limit divided by the wall load, and its
calendar life divides again by availability. Each replacement is a
discrete event discounted at its own date; `n_rep` counts the events
inside the plant life (the final core is never replaced, hence -1).

THE WALL LOAD IS AN INPUT, NOT COMPUTED HERE (WI-041). The plant binds
the PEAK neutron wall load ('Neutron Wall Load Peak'), because the
source and its cited method set in-vessel lifetime by the peak load and
not the average: Stellaris Table 6 derives the first-wall lifetime
(~4-6 FPY) from the peak first-wall DPA, and Lion 2022 states "the
lifetime of the blanket is determined by the peak loads". A concept
with no source peak binds a calibration of 1.0 and its average arrives
here unchanged. Before WI-041 this calc computed its own neutron power
over the circular-torus area, i.e. the average.

EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): `max`, `min` and `floor`
are invocations, which fall outside the codegen arithmetic envelope
(+ - * / ** only, calc_compat_renderer.py:39-46), so this calc routes
to the handwritten codegen stage (manual_required). The generated
handwritten impl is normative and is guarded bit-exact (rel 1e-9) by
the oracle mirror in verify_stellaris.py. Both carry 1cfe's guards
VERBATIM -- the clip floor/cap, the inner max(q_n, 1e-6), and the outer
max(0, ...) -- rather than dropping them as point-inert no-ops: they go
live at study-sweep extremes and a dropped guard would return a wrong
CAS72 silently and discontinuously.

Two faithful re-expressions in the model-resident statement, both exact
identities changing no value: clip(z, lo, hi) is written min(max(z, lo),
hi) -- jnp.clip's own order -- and ceil(z) is written -floor(-z) (the KerML
Real function library has floor, min and max but no ceiling or clip). The handwritten impl
uses Python's math.ceil and the same guards directly.

EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
marked for revert -- see models/stellarator_migration_ledger.md): the
pinned codegen admits no function invocation (max/min/floor) in an
executable expression, so the model-resident statement of the chain
above is carried as this doc and the output is declared without an
expression (a manual interface). The pre-migration body, with the
intermediates p_neutron, q_n, fpy_raw, fpy_cap, core_lifetime_fpy,
core_lifetime_cal, s, n_rep, pv, disc_pow_n, crf, is recorded verbatim
in the ledger row and in git at the migration PR's parent.

`n_rep` is a discontinuous step function of the live neutron/geometry
chain and is computed every run -- never frozen as a defaulted input.

Concept-agnostic: the fluence limit, the wall loading, the replaceable-
account cost, and the plant life are all inputs (MR-3).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385); knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
*Ref**: economics.py:53-75 (levelized_replacement_cost); model.py:102-111
(_core_lifetime_fpy, the clip and inner max); economics.py:6-10 (CRF);
defaults.py:291 (fluence_limit_dt), defaults.py:299 (replaceable accounts);
Stellaris Table 6 image (images/page_020_table_0.png: peak DPA in the
first wall 10.7 DPA/FPY -> estimated first-wall lifetime ~4-6 FPY);
Lion 2022 output.md line 88 (lifetime determined by the peak loads)
*Basis**: Fluence-limited replacement schedule on the peak wall load, discretely discounted and annuitized

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.levelized_replacement_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Levelized_Replacement_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, q_n_in: float, cost_per_event: float, operational_years_in: float, availability_in: float, fluence_limit_in: float, interest_rate: float    ) -> Levelized_Replacement_CostInput:
        """Validate inputs and fill defaults.

        Args:
            q_n_in: q_n_in input
            cost_per_event: cost_per_event input
            operational_years_in: operational_years_in input
            availability_in: availability_in input
            fluence_limit_in: fluence_limit_in input
            interest_rate: interest_rate input

        Returns:
            Validated input model
        """
        return Levelized_Replacement_CostInput(q_n_in=q_n_in, cost_per_event=cost_per_event, operational_years_in=operational_years_in, availability_in=availability_in, fluence_limit_in=fluence_limit_in, interest_rate=interest_rate)

    def run(
        self, q_n_in: float, cost_per_event: float, operational_years_in: float, availability_in: float, fluence_limit_in: float, interest_rate: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            q_n_in: q_n_in input
            cost_per_event: cost_per_event input
            operational_years_in: operational_years_in input
            availability_in: availability_in input
            fluence_limit_in: fluence_limit_in input
            interest_rate: interest_rate input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(q_n_in, cost_per_event, operational_years_in, availability_in, fluence_limit_in, interest_rate)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.levelized_replacement_cost_impl import (
            run_levelized_replacement_cost,
        )

        # Execute implementation - returns single value
        cost = run_levelized_replacement_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
