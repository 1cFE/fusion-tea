# Comparison contract — feasibility screen before the main study

[AGENT] Proposed 2026-09-26. This contract defines the desired matched comparison and its admission conditions. The main study is not released by writing it. The fresh review at `evidence/feasibility-review.md` determines which follow-up is justified. Owner authority: `evidence/owner-brief.md`.

## Independent choices and equal quantities

| Quantity | Role and proposed treatment | Authority/support |
|---|---|---|
| Conversion technology | Chosen: helium/salt/steam or helium Brayton | [OWNER] categorical component question |
| Source at nominal | Supplied helium at 773.15 K, with the existing Stellaris loop's nominal exchanger duty and required return read from native outputs | [AGENT] isolate conversion; [INHERITED] C-1 and WI-095 |
| Source operating points | Proposed 80/90/100% duty at equal hot/return temperatures within each pair; source flow supplied consistently with duty and cp | [AGENT] candidates for interface review, not a qualified reactor operating range |
| Common upstream source | Reactor, fuel, magnets and upstream plant accounts excluded from subsystem metric; any shared pumping electricity and installed hardware must have identical, explicit treatment | [OWNER] isolated boundary permitted; no whole-plant LCOE claim |
| Equipment | Supplied quantities, ratings, geometry, prices and applicable conditions enumerated before execution; retain insufficient offers | [OWNER], MR-7 |
| Operating controls | Steam settings within admitted equipment conditions; Brayton flow and pressure ratio on matched heat/return points, with equal opportunity to investigate supported choices | [OWNER]; no automatic equipment purchase |
| Finance | One currency year, availability, real discount rate, calendar life and replacement convention; specify values only with the accepted cost boundary | [OWNER]; unresolved during readiness audit |

The source-flow identity is an operating balance, not an installed-pump selection. This would change how the source is supplied relative to the whole Stellaris loop; it needs an explicit design-role record and review before assembly. No such model edit has been made.

## Consequences and equipment scope

Calculate heat transferred, source return, steam/helium states, compressor/turbine work, generator losses, pumps and heat rejection. Conversion net equals generated electricity minus every conversion electric load inside the boundary. Keep primary circulation and its recovered heat joined consistently; 3,301 MW is not a new reactor baseline but the nominal exchanger duty including recovered pumping work.

The steam inventory must include helium-to-salt exchangers, relevant piping, salt pumps/inventory, steam generator and reheater, steam machinery and generator, condenser/feedwater equipment and heat rejection. The Brayton inventory must include primary-to-cycle exchanger, compressors, turbine/generator, recuperator, intercoolers/precooler, coolant circuits/pumps and heat rejection. Existing aggregate offers must have disjoint scope, not assumed coverage. Cost contributions are initial capital, replacement, nonfuel operation and electricity denominator. Reactor fuel is outside the isolated conversion metric; any full-plant interpretation must restore the shared source/fuel costs explicitly.

## Failure and support rules

- A nonpositive temperature approach, incomplete source heat removal, inconsistent required return or inadequate selected equipment is a failed engineering case, even if it produces electricity.
- An operating point outside the equipment's supported conditions is unsupported; setting a validity flag does not qualify it.
- A fixed outlet temperature with no evaluated heat-removal equipment is a missing physical check. It must stay visible and prevents claiming complete equipment feasibility.
- Unpriced required equipment is unknown, not zero. Price sensitivities cannot create its physical applicability.
- Native execution and independent equation checks do not establish scientific qualification. Prior all-checks-passing points have only the checks their packages implement.

## Uncertainty and materiality

[AGENT] A released study would examine at least machine efficiency and equipment prices, and cooling demand where it can affect the result. Use supported performance ranges; an assumption-only variation is labeled as such. Report source-temperature or duty cases refused by any component. Proposed decision materiality is 5 MW and 5 USD per net MWh (consistent with the predecessor's engineering-scale interpretation), subject to review before use; numerical balances retain each native component's tolerance and are never loosened to admit a case. A ranking inside the uncertainty/materiality band yields no recommendation.

## Bounded readiness diagnostics

[AGENT] Before main-study release, execute only named existing-package interface diagnostics, keeping all outputs, exceptions and verdicts. Proposed controls: unchanged Stellaris steam; lower salt boundary; lower steam setting on unchanged equipment; lower/higher helium temperature on unchanged equipment; C-1 original Brayton point and existing no-bypass matched point. These are a readiness screen, not matched alternatives, not optimization, and not an economic study. They test whether the audit's guard/condition claims reproduce. No reported difference between these controls is a technology ranking.

The readiness screen needs no new modeling item because it changes only diagnostic entry values on unchanged packages. Any new source binding, equation, cost scope or equipment applicability requires a native model work item, reviewed design roles and executable evidence before use. If the review establishes a blocking physical or unsupported-cost requirement, preserve a bounded negative with a candidate ledger and figures that show the gap; explicitly mark the requested matched economic study and sensitivity results unmet.
