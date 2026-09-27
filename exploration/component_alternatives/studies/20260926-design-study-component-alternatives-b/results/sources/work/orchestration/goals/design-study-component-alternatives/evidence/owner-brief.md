# Run-goal prompt: a matched comparison of alternative conversion components

Goal slug: design-study-component-alternatives

## The engineering question

For the same supported reactor heat source, how do the modeled steam and helium Brayton conversion options differ in net electricity, required equipment and conditional LCOE? Can the alternatives developed around different plants support a meaningful choice between components?

This is a categorical component/subsystem choice. It is not a comparison between the complete published Stellaris and ARIES plants, whose many simultaneous differences prevent attribution.

## Class-specific strategy

- First inspect the compatibility map and identify a common, physically supportable heat-source boundary. Candidate starting points are the Stellaris helium source used in C-1, or the ARIES divertor helium source identified as C-3-compatible with the steam path. Do not assume their interfaces are interchangeable merely because both carry heat in MW.
- Prefer the largest useful common boundary that can be evaluated with existing definitions and modest justified integration work. If only an isolated source loop supports a fair comparison, state that scope and calculate the cost per net MWh of that conversion subsystem. Do not label an isolated subsystem metric whole-plant LCOE. A full-plant comparison must include the remaining heat paths and common plant accounts explicitly.
- Fix source heat duty, temperatures, return requirements and upstream costs consistently. Specify whether each alternative includes its required intermediate exchanger, salt loop, cooling system and machinery. Necessary connecting equipment belongs inside the compared conversion subsystem and must be costed. Do not force one topology onto incompatible technology or grant one branch free heat transfer.
- Build both branches using the applicable existing definitions. Audit fixed steam temperature/rated-condition assumptions and the Brayton source matching. Do not alter guards or use a lumped efficiency fit to impersonate a missing physical component. Reuse the existing alternatives where supported; record any required new relationship as an extension, not demonstrated unchanged reuse.
- Supply explicit equipment inventories and cost bases for both choices. Give both branches the same opportunity for a bounded operating-parameter study and explicit offered-equipment selections. Do not compare one tuned branch with an arbitrarily poor default of the other. Report common-design and branch-specific choices separately.
- Keep reactor/fuel assumptions and financial conventions matched. Resolve relevant auxiliary and heating accounting before computing net electricity. Explain differences through temperature matching, conversion performance, internal power consumption and purchased equipment.
- Evaluate a small set of common source operating points within the overlap of supported ranges, not just one favorable point. Test whether the relative result survives uncertainty in prices and component efficiencies. Unsupported extrapolation is not evidence of an economic crossover.
- If steam/Brayton cannot support a fair comparison within this goal's budget, report the specific missing interface or cost requirement. You may evaluate another genuine physical component/material alternative only if the evidence shows it answers the owner's expanded-library question. Comparing two price correlations for the same equipment or two numerical settings does not satisfy this class.

## Figures and result required

Show the two assemblies and their common comparison boundary in a simple diagram. Provide matched net-output and cost-contribution comparisons and a delta-LCOE or subsystem cost-per-MWh plot over the supported common source range, with uncertainty and failed cases visible. Answer which option performs better under which assumptions, or explain why the evidence supports no recommendation. Pure execution/reuse evidence is not sufficient completion.

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
