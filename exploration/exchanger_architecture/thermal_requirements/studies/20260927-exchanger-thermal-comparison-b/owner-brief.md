# Run-goal prompt: exchanger architecture, operating range and electricity cost

Goal slug: design-study-exchanger-architecture

## The engineering question

How does connecting the available heat exchangers in series versus a series-then-parallel network change the usable operating range and cost of electricity? Is there a range where the connection choice makes one design preferable, once heat removal, equipment and architecture-specific costs are accounted for?

The class is architecture: which components connect to which streams, including flow division and mixing. A numerical selector may execute existing architecture alternatives, but document the distinct physical connection graphs. Do not present a change in plasma density alone as an architecture study.

## Class-specific strategy

- Start from the verified series/network study, not from scratch. At hollowness 0.66 and peak density 5.5e20 m^-3 the series case removes all heat while the network leaves about 45 MW; at 5.75e20 both fail despite a net-output ranking reversal. Those invalid high-output cases are a motivation to map the operating boundary, not evidence of an LCOE winner.
- Choose and explain a named source and equipment configuration. Prefer a calculated-plasma chain where its heating and downstream balances can be made consistent. If supplied source duties are necessary, label this as a downstream architecture comparison and state what is held equal. Do not mix the 423 MW and 891 MW scenarios without explicitly defining both.
- Compare the existing series and series-then-parallel definitions at equal source conditions, exchanger hardware and cost/finance conventions. In the network, treat branch split as a supplied operating choice. Establish whether a poor fixed split explains the prior failures: use a bounded split study and compare the best passing tested setting fairly against the series branch, with the same other operating freedom.
- Separate two questions: (1) what changes from connections alone with fixed hardware; (2) if neither arrangement supports the desired range, can an explicitly enumerated alternative inventory change the choice after its cost is included? Do not silently enlarge areas, machines or ratings to clear failures.
- Carry return-temperature requirements, all branch duties, generator and auxiliary loads, pressure-loss/pumping assumptions and heat rejection consistently. Identify whether the present model makes architecture costs artificially identical. Account for branch-specific equipment and bounded piping/pressure-drop costs where justified. Where a quantitative law is unavailable, show a transparent break-even extra-cost/extra-power allowance rather than inventing a detailed cost estimate.
- Study at least one common load range and the small set of operating choices needed to evaluate both arrangements fairly. Report pass/fail boundaries, net electricity, selected capital and lifecycle cost contributions. Use paired LCOE differences under consistent fuel assumptions; separate plasma/fuel effects from connection effects.
- Seek an interpretable result: an operating-range extension, lower cost at a common passing load, equivalent performance until a heat-transfer limit, or a break-even cost showing the ranking is unsupported. A ranking reversal occurring only among heat-removal failures is not a usable design recommendation.
- Test the physical explanation against consequential uncertainties in conductance, temperature approaches, pumping losses and architecture-specific cost. Respect the incomplete blanket temperature/duty/flow coupling. Do not vary physically dependent source quantities independently and call them realizable blanket designs.

## Figures and result required

Provide a simple series/parallel connection diagram, a common-load versus operating-choice plot showing heat-removal and equipment boundaries, and an LCOE or delta-LCOE comparison restricted to passing modeled cases. Keep failed points visible separately. Include a break-even cost/power plot if missing architecture-specific costs prevent a supported direct ranking. Explain which connection is preferable in which tested region, or why the existing evidence cannot select one.

## Purpose and authority

Use the run-goal workflow. The owner requests a study that demonstrates how the expanded Stellaris/ARIES component library helps evaluate engineering choices. We need an understandable design question, a named starting configuration, a credible comparison and an explained result. A parameter sweep that merely produces numbers is insufficient.

The question is not how closely we can reproduce ARIES. It is what alternative design choices the expanded library lets us evaluate, what changes in performance and LCOE, and why. Do not make an arbitrary fixed tritium-supply threshold the central result. Do not manufacture novelty, a ranking reversal or a positive result. An explained absence of advantage, a bounded applicability limit or an inadequate-model result is legitimate; report unmet completion criteria honestly.

Read AGENTS.md, CLAUDE.md, .agentic-mbse/codex.md, .project/codex-test-setup.md, the run-goal skill and native runbook. Use native goal templates and the prescribed runtime. Read MR-7 and follow the modeling workflow for changes. The slug below is supplied by this prompt; use it without another naming confirmation. Preserve this prompt as the owner brief. Specific study strategies below are proposed starting approaches, not required findings.

## Grounding records

- docs/write-up/sysml-codegen-model-evaluation.md, section 1.1: the distinction between parameters, component/material alternatives and architecture.
- docs/write-up/aries-model-transfer-outline.md: the reader's question; editorial context, not authoritative numerical evidence.
- work/orchestration/goals/design-space-combinations/{goal,trail,learnings,answer}.md and evidence/choice-inventory.md, compatibility-map.md.
- The WI-093 combination-assemblies report and evidence; locate its current active/completed path through native tracking. Its cross-plant assemblies prove partial reuse, not full plant qualification.
- work/orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md.
- work/orchestration/goals/aries-reconciled-alternative-economics/answer.md.
- exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/ and its verified results.

Known issues to check when relevant: the steam path expects a salt-loop interface and has fixed temperature assumptions; the hybrid plasma assembly omits its own calculated heating requirement from the electrical balance; one peaked-profile case reports a negative sustainment requirement that was not interpreted; blanket source temperature is not fully coupled to duty and flow; pump-law assumptions can change conclusions; recuperator and cycle-side costs lack complete equipment support. These are specific prerequisites or limitations to resolve, not a mandate to repair every model.

## Common execution and comparison requirements

1. Ground a persistent goal contract and bounded round plan. Start by inspecting existing evidence, then run a small recorded screening study if needed. State the original design point in plain engineering terms: which components, selected equipment, operating settings, calculated outputs and inherited assumptions. Explain why it is a useful starting point. Do not introduce an unexplained 423 MW or 891 MW baseline.
2. Before the main study, write a comparison contract: independent choices, quantities held equal, calculated consequences, permitted equipment reselections, accounting boundary, failure conditions, scientific support and materiality/tolerances. Have the risky interface and comparison assumptions independently reviewed. Routine scope choices within this prompt do not require another owner approval.
3. Reuse existing equations and cost machinery. Small, justified interface/accounting repairs or additive alternatives are authorized through the modeling workflow and applicable independent review. An adapter may map units or names but must not conceal new physics. Retain the pre-repair replay and identify changed behavior. If a credible comparison requires a major new physical model, surface that dependency and report partial completion rather than substituting an unsupported calculation.
4. Preserve design choices: no silent equipment sizing, demand-derived purchases or automatic constraint satisfaction. If selecting alternative equipment, enumerate explicit offered ratings and prices before execution, account for them, and report that selection as a separate design decision. Performance changes requiring different hardware must carry its costs or be labeled unsupported performance sensitivities.
5. Track the complete relevant energy and cost boundaries, including pumps, compressors, external heating, generator losses, heat rejection, purchased equipment, replacements and operating expense. Do not count a load twice or leave it out to make branches comparable. Do not insert reference net electricity into a claimed prediction.
6. Use consistent currency, finance, lifetime, availability and fuel conventions across each matched comparison. Show capital, nonfuel operation, fuel and electricity-denominator contributions separately. Fuel supply remains conditional unless modeled and supported. Test whether reasonable fuel assumptions change a recommendation; do not equate absent breeding qualification with an established market-purchase scenario. If absolute LCOE is too assumption-dependent, provide paired delta-LCOE and cost contributions, with the absolute figures explicitly conditional.
7. Separate numerical execution, passing implemented engineering checks and scientific qualification. A case that cannot remove its heat or exceeds selected equipment is not an LCOE winner. Preserve failed cases; distinguish them in every plot and ranking. Missing checks must remain visible even if all existing checks pass.
8. Explain at least one decision relationship using matched cases and an energy/cost decomposition. Check it against consequential modeling assumptions. Do not search only for dramatic outcomes; retain the screened questions and explain why the selected one teaches something useful.
9. Use subagents for bounded source/interface/cost audits and fresh independent reviews, with explicit ownership and preservation instructions. Keep a findings log, failed attempts, a changed/reused inventory and replay commands. Commit coherent increments using explicit paths; never sweep the shared index into a goal commit. Preserve owner write-up edits and other agents' work.
10. Work in goal-owned study/model/package locations. Preserve the existing Stellaris and ARIES packages, historical studies and their behavior; create isolated variants where needed. These three study prompts may be run by different agents: coordinate shared changes rather than concurrently editing or repinning the same library or manifest. No push, merge, external messages or purchases. Respect source-access restrictions and the scope of existing exceptions.

## Deliverables and stopping conditions

Produce answer.md, a complete candidate ledger, sealed study evidence, independent review and exact replay instructions. Include publication-ready SVG/PNG figures, their source data and a reproducible rendering script in the goal evidence directory. Do not edit the owner's article. Supply a short proposed passage explaining: starting design, changed decision, measured consequence, mechanism and practical limit. Every plotted point must trace to a case identity and its check status.

Completion requires an executed and verified comparison that answers the class-specific question below, consistent performance/cost accounting, a causal explanation, and a sensitivity check on the assumptions that could change the conclusion. Running cases or demonstrating reusable interfaces alone does not complete an economic comparison. If the goal remains blocked by missing physics, incompatible interfaces or unsupported costs, name the exact gap and assess partial/unmet completion. Do not call it met because an illustrative plot exists.

Use a maximum of four rounds, with retry limits from the runbook. Begin with a bounded screen, then select one primary question rather than collecting unrelated studies. Formal goal and work-item closure remain with the owner.
