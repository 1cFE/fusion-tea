# Comparison contract — feasibility screen before the main study

[AGENT] The owner-authorized fourth design submission passed independent review on 2026-09-26. This contract and the reviewed WI-096 design permit bounded implementation; main-study release still requires native validation and independent integration review. Authority: `evidence/owner-brief.md`, `evidence/owner-direction-fourth-submission.md`, and `evidence/design-review-fourth-submission.md`. Earlier failed designs and diagnostics remain in the review history and candidate ledger.

## Independent choices and equal quantities

| Quantity | Role and proposed treatment | Authority/support |
|---|---|---|
| Conversion technology | Chosen: helium/salt/steam or helium Brayton | [OWNER] categorical component question |
| Source | Unchanged Primary Coolant Loop calculation with fixed original hardware and inlet/rise; shared selected resistance scenario, including an explicit allowance for controllers | [AGENT] conditional imposed resistance, not predicted branch-dependent valve hydraulics |
| Source operating points | Independently chosen source heat and IHX circuit offers; both branches receive the same calculated loop outputs within each pair | [OWNER] preserve design choices; [AGENT] proposed heat offers 2500/2800/3000 MW, circuit offers 10/11/12/14; no external matching search |
| Common upstream source | Reactor, fuel, magnets and upstream plant accounts excluded from subsystem metric; any shared pumping electricity and installed hardware must have identical, explicit treatment | [OWNER] isolated boundary permitted; no whole-plant LCOE claim |
| Equipment | Supplied quantities, ratings, geometry, prices and applicable conditions enumerated before execution; retain insufficient offers | [OWNER], MR-7 |
| Operating controls | Brayton flow and pressure ratio remain selected; model-owned bypass fractions regulate return when installed exchanger capability suffices, otherwise the case fails. Steam settings remain within the offered conditions. | [OWNER] justify controller behavior and variable roles; existing controller reuse subject to review |
| Finance | USD2025, availability 0.85, real discount 0.05, life 30 calendar years, commissioning-time capital; dated replacements and explicit recurring allowances | [AGENT] matched assumptions; source-declared currency and CPI evidence retained separately |

Source heat, cycle flow, pressure ratio and purchased equipment stay independent selections. The proposed physical control changes helium flow through an exchanger by routing the calculated remainder around it, then mixing to the required return. The controller must demonstrate sufficient capability and retain inadequate combinations as failures. Its inventory, prices, electrical load and pressure-service assumptions belong in the comparison. Source flow and required return follow the loop and may differ between source points. Bounded scalar controller/cooler diagnostics are not native assembled-package evidence.

[OWNER] Name the result **the selected steam offer versus tested Brayton offers at matched source conditions**, using **conversion-subsystem cost per net MWh**. The inherited steam offer supports fewer operating degrees of freedom; record declined/unsupported directions. This is not an equally optimized technology comparison or whole-plant LCOE.

## Consequences and equipment scope

Calculate heat transferred, source return, steam/helium states, compressor/turbine work, generator losses, pumps and heat rejection. Conversion net equals generated electricity minus every conversion electric load inside the boundary. Keep primary circulation and its recovered heat joined consistently; 3,301 MW is not a new reactor baseline but the nominal exchanger duty including recovered pumping work.

The steam inventory must include helium-to-salt exchangers, relevant piping, salt pumps/inventory, steam generator and reheater, steam machinery and generator, condenser/feedwater equipment and heat rejection. The Brayton inventory must include primary-to-cycle exchanger, compressors, turbine/generator, recuperator, intercoolers/precooler, coolant circuits/pumps and heat rejection. Both include the proposed bypass/control equipment and its selected-price assumption. Aggregate account scopes must be disjoint and their empirical support explicit. Cost contributions are initial capital, replacement, nonfuel operation and electricity denominator. Reactor fuel is outside the isolated conversion metric; any full-plant interpretation must restore shared source/fuel costs explicitly.

The scope assessment must include finite-water-cooler physics, the salt-pump-count variant, recuperator conductance/effectiveness, source-return control and all energy/cost ledgers. Their actual new algebra, modified bodies, reused solvers and new iterative closures must be enumerated in the design and reviewed against the handwritten-solver limit. They are not collectively classified as interface wiring.

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
