---
Status: approved
Created: 2026-09-11
Updated: 2026-09-11
Related Artifacts:
  Spec: ./spec.md
---

# IFE zero-discount design

## Decision and scope

[AGENT] Calculate the two present-value factors in one small, typed native handwritten completion. Keep physics, annual costs, discounted cost/energy multiplication and the existing price guard in their current definitions. This removes cancellation and the zero-rate singularity without changing cash-flow timing. The working prototype passes the required numerical cases through sealed public execution.

[AGENT] This is a bounded structural departure from AD-003's single-calculation implementation. The closed-form finance remains identical. The parent accepted this direction and the necessary two-key duration migration during design on 2026-09-11, contingent on validation. This is agent-originated architecture, not owner-settled financial policy. The complete design awaits parent acceptance and independent review.

## Findings and alternatives

Hawker Eq. 2.1 discounts separately dated annual costs and energy. The following source paragraph defines five construction years and forty operating years: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141–148`, registered in `knowledge/SOURCE_INDEX.md:28`. For integer durations the construction payments occupy years 1 through Yc and operation occupies Yc+1 through Yc+Nop. The existing Real-duration formulas extend that geometric expression algebraically. The independent integer oracle retains explicit dates; the fractional oracle is explicitly an algebraic reference. This stage inspected the registered extraction and makes no new image-certification claim.

The existing IFE library already computes the entire physics and annual-cost chain. No additional domain equation is needed. `models/library/analyses/ife_lcoe.sysml:118` is the defective factor block; the final guarded price definition at `:141` is an inherited WI-048 dependency. AD-001/004/006 support documented Real values, library analyses and parameter separation. No shared MFE definition changes.

A fresh syside expert inspected the installed generator at `/home/reid/1cfe/fusion-tea/.venv/lib/python3.12/site-packages/sysml_codegen/`. `extraction/calc_compat_renderer.py:77` rejects invocation nodes, so native special-function rendering is unavailable. The same file at `:103` rejects feature chains in calculation outputs. `elaboration/elaborate.py:761` attaches part/package members but cannot attach a nested calculation owned by another calc definition. `extraction/expression_compiler.py:263` selects manual completion for output-only declarations. These are pinned-toolchain limitations, not claims about SysML language validity.

[AGENT] Rejected alternatives: a local polynomial needs an approximation window and transition; a handwritten whole LCOE would duplicate physics and finance. Neither is needed because the separate factor stage works. No shared generator repair is required.

## Elements and dataflow

| Element | Engineering meaning and interface | Location |
|---|---|---|
| `IFE Present Value Factors` definition | Inputs: dimensionless discount rate, Real construction years and Real operation years. Outputs: construction and operation factors in years. Normative equations below; output-only declarations select the typed manual completion. | `models/library/analyses/ife_lcoe.sysml` |
| `IFE LCOE` definition | Replace the subtractive factor expressions with two Real factor inputs. Retain all existing physical/annual arithmetic, duration input types, outputs and current price contract. Declare all inputs before output/intermediate features so positional redefinition remains valid. | Same file |
| `construction_duration`, `operational_duration` | Plant Real parameters defaulting to 5.0 and 40.0; direct bindings supply both definitions. | `models/designs/generic_ife/ife_plant.sysml` |
| `pv_factors` usage | Bind rate and both durations from the plant; supply both factors to `lcoe_calc`. | Same generic plant |
| Typed factor completion | Implement only stable transcendental evaluation and the exact-zero branch. Generated return order is operation factor, then construction factor. | `exploration/ife_e2e/generated/handwritten/ife_lcoe/ife_present_value_factors_impl.py` |

The directed path is plant rate/durations → factors → discounted cost/energy → existing price guard. The existing physical and annual-cost chain supplies the other inputs to the cost/energy combination. Neither price nor factor depends on a downstream result. Existing imports from `ife_lcoe` cover the new definition; all calculation definitions remain in the library. Canonical changes propagate to the two corresponding IFE twin files through the existing family mapping.

| Binding | Supplier |
|---|---|
| `pv_factors.discount_rate_in`, existing `lcoe_calc.discount_rate_in` | Plant `discount_rate` |
| `pv_factors.construction_years_in`, `lcoe_calc.construction_years` | Plant `construction_duration` |
| `pv_factors.operational_years_in`, `lcoe_calc.operational_years` | Plant `operational_duration` |
| `lcoe_calc.pvf_construction` | `pv_factors.construction_factor` |
| `lcoe_calc.pvf_operation` | `pv_factors.operation_factor` |
| Existing Hawker guard | Unchanged cost, energy and actual net power outputs |

The old direct module interface gains two required factor inputs. Retain its original discount and operational-duration formals for a small change surface, even though their direct arithmetic moves to the factor definition. Direct module callers must construct the factor input and bind its named outputs before calling the LCOE core. No caller should reimplement the numerical formula.

## Evaluation and numerical argument

Let `l = log1p(d)` and `A(n,d) = -expm1(-n*l)/d` for nonzero d. Return `A(Yc,d)` and `exp(-Yc*l)*A(Nop,d)`. At exactly d=0 return Yc and Nop. This is algebraically the existing expression, since exp(log1p(d))=1+d. As d tends to zero, log1p(d)/d tends to 1 and expm1(x)/x tends to 1, hence A(n,0)=n for Real n. The discounted construction and operation dates are unchanged.

`log1p` avoids rounding 1+d to one; `expm1` avoids subtracting near-equal powers. No truncated local series, clipping threshold or arbitrary near-zero rate switch is introduced. The only branch is equality to zero, including signed zero. Within the tested duration/rate window, all intermediates remain representable. For the largest tested negative exponent magnitude, 200.5×log(2)≈139, elementary-function error can amplify with that exponent but stays well below 1e-9 in the actual independent comparisons. Extreme floating-point overflow/underflow remains a representability limitation; the tested window is evidence, not a newly supported-domain restriction or an all-Real error proof.

The evidence covers Real duration pairs (5,40), (5.5,40.5), (0.25,0.5), (1,1), (20,100), (50.5,200.5). This includes the required baseline/fractional cases, subannual values, minimal integer periods, and much longer lifetimes. Each uses zero, 8%, and both signs of 1e-4, 1e-8, 1e-12, 1e-14, 1e-16 and 1e-18 at generating, zero-net and negative-net points. The generating case also uses ±50% at every duration pair to test appreciable duration-times-rate products. Zero and both sides of the exact-zero branch are covered; no evidence bound becomes model validation policy.

## Interfaces and deferred impact

Every key below carries the existing `hif_plant_pkg__hif_plant__` prefix.

| Old entry | New entry | Type/default |
|---|---|---|
| `lcoe_calc__construction_years` | `construction_duration` | Real / 5.0 years |
| `lcoe_calc__operational_years` | `operational_duration` | Real / 40.0 years |

Two numeric outputs are added: `pv_factors__construction_factor` and `pv_factors__operation_factor`. All old response names remain. `prototype/input-reference-failure.txt` records the failed attempt to retain old duration keys by reading the calculation inputs: exact generation rejects `CalculationUsage` as a containment anchor with `SI_OCCURRENCE_MISSING`. The parent accepted the two-key migration after this evidence. Duration behavior itself is preserved by direct shared bindings and the numerical checks.

Implementation must migrate affected current entry/channel censuses and executable callers, including temporary live/snapshot packages and `tests/ife_execution.py`'s completion helper. Regenerate package schemas, contracts, manifests and pipeline natively. Preserve both typed manual implementations when completing temporary packages. Regeneration uses `preserve_handwritten=True`; the smart route additionally sets `smart_regen=True`. Smart alone combined with overwrite clears the handwritten directory before signature comparison in this pin and is not the preservation route.

Study entry-key snapshots, channel metadata, manifests and package pins become stale. Their refresh and study execution remain separate parent tasks. This item must identify that impact without rewriting study records or claiming current studies have been rerun.

## Prototype and validation

Reproduce from repository root:

```bash
PYTHONPATH=. .codex-test/run python work/active/WI-049_ife-zero-discount-repair/prototype/build.py
PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit .codex-test/run python work/active/WI-049_ife-zero-discount-repair/prototype/execute.py
.codex-test/run agentic-mbse validate --complete work/active/WI-049_ife-zero-discount-repair/prototype/models
```

`prototype/build.py` materializes the eleven-file canonical IFE subset and changes only its analysis/plant copies. Production models are untouched. Its inherited LCOE introduction still describes the old expression; implementation must update that prose to describe the delegation and limit. The executable factor definition has resolving Source/Ref/Basis comments. Early parser failures are retained as probe history; the final `generation.txt` corresponds to successful generation.

| Evidence | Actual result |
|---|---|
| `prototype/execution.txt`, `execution.json` | 264 sealed public evaluations pass independent 80-digit references. Maximum relative error across cost, energy, eligible price and both factors: 6.026965908260528e-15. True-zero channels are checked absolutely at 1e-9. |
| Zero generating baseline | Cost 58,111,257,843.81798 dollars; energy 274,751,655.9428571 MWh; price 211.50466825904763 dollars/MWh. |
| `prototype/positive-neighbor.json` | Required WI-048 positive neighbor at zero, ±1e-12 and 8% remains generating; maximum cost/energy/price residual 4.0967553318407833e-16. |
| Native regeneration | Full package bytes match after repeated preservation and preservation-plus-smart regeneration. The typed factor signature and the inherited typed price guard remain intact; sealed loader succeeds. |
| `prototype/validation.txt` | L1–5 PASS. L1 has zero parser errors/warnings; L2 has zero structural issues; L3 has zero cycles. L6 FAIL with 50 static/EXPOSE issues, the same count and categories recorded for the inherited WI-048 final family. Full issue-by-issue final attribution belongs to implementation. |

Integer reference factors are explicit 80-digit dated sums applied to independently reconstructed annual quantities. Fractional factors use a separate high-precision difference-of-powers expression, distinctly labeled. Neither imports the production factor function. The positive-neighbor output file records results but its final assertions must be hardened into retained acceptance tests during implementation. Prototype response records retain named verdicts for inspection; production tests must assert the exact named net verdict and supported consumer eligibility in addition to indicators and sentinels.

## Implementation and verification checklist

- [ ] Refine the two canonical model files and synchronize their IFE twins; complete the numerical-limit/delegation comments and direct traceability without changing source interpretation.
- [ ] Natively regenerate IFE, install the typed factor completion alongside the existing guard, reseal through supported generation, and verify both preservation routes.
- [ ] Migrate executable direct-module callers, package-completion helpers, two duration entry keys and two output channels; record deferred study metadata impact explicitly.
- [ ] Turn required SV-076/077 cases into retained generated-execution regressions. Verify cost, energy and eligible price separately with the spec's tolerance; include integer/fractional references, signed/zero energy and exact eligibility.
- [ ] Complete SV-078 before/after comparison of every existing baseline output, Meier and unaffected channels; retain positive-neighbor checks and supported consumer exclusions.
- [ ] Run relevant IFE family/live-snapshot/regeneration/consumer tests and final model Levels 1–6; distinguish inherited debt and require a fresh independent item audit.

## Risks and acceptance

Manual return order and generated signatures are easy to misread. Use the emitted typed signature and named output schema; keep factor scope limited to the documented equations. Duration migration can hide in old callers; census tests and actual baseline mutations must detect it. Passing the quotient alone is insufficient: cost and energy assertions are mandatory. The finite window does not certify arbitrarily extreme IEEE inputs. Financial normalization, source rulings, MFE, study refresh and residual acceptance remain parent/owner reservations from the alignment.

[AGENT] Prototype PASS for feasibility and the documented numerical window. The parent owns design acceptance; final acceptance requires the later independent audit. No production implementation, PM close/archive, study execution or dependency change occurred in this stage.

## Parent stage acceptance — 2026-09-11

[AGENT] Accepted after fresh `review.md` PASS. The bounded AD-003 structural departure and two-key duration migration preserve the existing finance and Real-valued duration behavior. Carry the review's citation and retained-assertion follow-through into the plan. The parent captured all thirty current production outputs and both verdicts in `entry-baseline/` before implementation; use it for SV-078's before/after comparison. No owner-reserved decision was exercised.
