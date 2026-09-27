# Run-goal: choose the conversion system by its effect on the whole plant

## Owner intent

Use the run-goal workflow to finish the steam-versus-helium-Brayton component trade study at the system level.

[OWNER-VERBATIM] “the whole idea of component-level trade studies is EXACTLY seeing the effect at a system level.”

[OWNER-VERBATIM] “these are the ONLY results I will really have to show for the ENTIRETY of a one-year project.”

The required result is an understandable engineering study: choose between conversion alternatives in the same reactor concept, calculate the consequences for complete-plant electricity and lifecycle cost, and explain what determines the preferred choice. The owner accepts explicit modeling assumptions and scientific limitations. The result does not need vendor qualification, but it must answer the plant-level question. A comparison that omits the reactor or primary circulation is not completion.

Proposed slug [AGENT]: `design-study-whole-plant-conversion`. Use this name when grounding the goal; do not stop solely to reconfirm it. Retain this prompt as the owner brief, preserving the distinction between owner intent and the proposed execution strategy below.

## Question and completion condition

For one consistently specified reactor concept, how does selecting the modeled steam or helium Brayton conversion system change net electricity exported, whole-plant LCOE and the assumptions under which each choice is preferable?

Completion requires a verified, reproducible whole-plant comparison with at least one common supported operating condition, an explained cost/power decomposition, and sensitivities sufficient to say whether the preference is robust or assumption-dependent. Seek useful coverage across the predecessor's three source loads, but do not claim unsupported operating points. A robust winner is not required; a quantified conditional preference or no material difference is a valid answer.

Do not downgrade this endpoint to conversion-subsystem cost, another arbitrary common-cost surcharge, or successful numerical execution. A break-even surcharge is useful supporting analysis, not a replacement for a traceable plant cost inventory. If a material prerequisite genuinely prevents the requested comparison, name it and report partial completion rather than declaring the narrower result sufficient.

## Read first and reuse

Follow AGENTS.md, CLAUDE.md, the local run-goal skill, work/orchestration/GOAL_RUNBOOK.md and the prescribed runtime in .project/codex-test-setup.md. Ground a persistent contract and plan using native templates.

Read:

- `work/orchestration/goals/design-study-component-alternatives/{answer,trail,learnings}.md`, its comparison contract, cost audit, monetary basis, engineering-equalities record and final reviews.
- Its repaired sealed study `exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/`, including candidate inputs, failed cases, verification, source state, price assumptions and replay instructions.
- WI-096's spec, design and report; locate the current path through native tracking.
- `work/orchestration/goals/design-space-combinations/answer.md` and compatibility evidence.
- Existing Stellaris whole-plant power, fuel, capital and lifecycle definitions and their applicable reviews.
- `work/orchestration/goals/aries-reconciled-alternative-economics/answer.md` and the integrated equipment/LCOE goals for reusable accounting and known assumptions.
- `modeling_project/REQUIREMENTS.md`, especially MR-7, and the study policy.
- `docs/write-up/sysml-codegen-model-evaluation.md` section 1.1 for presentation intent. Owner write-ups are context, not numerical evidence, and must not be edited by this goal.

The predecessor already verified 498 cases after numerical repairs with unchanged oracle and tolerances. Reuse that evidence. Its nominal subsystem ranking found no material cost difference at 2500/2800 MW source heat and a 9.446 USD2025/net MWh Brayton advantage at 3000 MW. Steam produced more electricity at all three selected pairs. The study excluded reactor/fuel and primary circulation electricity/costs, so those rankings are not plant rankings. Its approximate 1.831 billion USD2025 common-cost crossover motivates this goal; it is not a target to reproduce.

## 1. Establish one common reactor and comparison boundary

Proposed starting approach [AGENT]: extend the predecessor's Stellaris-helium source basis into a consistently accounted complete plant. Choose the strongest existing compatible reactor inventory and explain why. Do not stitch arbitrary favorable entries from different plants into an unlabeled baseline.

Produce a concise configuration/account table before the main study:

- Common reactor geometry, source heat and its definition, plasma/fuel basis, blanket and primary loop, installed inventories, service assumptions and financial conventions.
- Conversion-dependent equipment: intermediate exchangers, salt circuit where needed, turbine/compressors, recuperator, cooling water, heat rejection, controls and generators.
- Every major capital account, annual expense, replacement and terminal item, identifying its source, inherited estimate or explicit assumption.
- Every electrical load and where it enters the plant ledger.
- Chosen quantities, calculated quantities, supported operating ranges and constraints.

The source's reactor heat input is not automatically fusion power. Identify neutron multiplication, deposited heating and recovered pumping heat before deriving fuel demand. If the plasma operating point cannot be independently reconstructed, supplying a common source condition is acceptable for isolating this component choice. State that clearly, derive compatible fuel and heating assumptions, and still include the whole reactor's costs and loads. No fabricated core-validation claim is needed.

Within each matched pair, keep the upstream reactor inventory and operating assumptions equal unless the conversion choice physically changes them. Where it does, model or explicitly bound that consequence. Across loads, distinguish operation of one installed plant from purchasing different reactor inventories; do not silently resize the core or copy a load-inappropriate account total.

Use reasonable, explicit assumptions for missing minor scope. For a material unknown, establish a credible range and its effect on the conclusion. Do not make the headline depend on an unexplained fixed 100 kg/year tritium threshold or a fuel price chosen for dramatic results. A conditional breeding/supply assumption is allowed; show how changing it affects the paired recommendation.

## 2. Complete the native system integration

Extend an isolated model/package using the existing verified conversion alternatives and existing plant accounting machinery. Model-owned calculations must generate the system power and cost result; reporting scripts may extract and plot it, not supply missing plant physics or a parallel hand-built LCOE formula.

Define plant net export as generated electrical output minus all applicable conversion and upstream electrical consumption. Trace primary circulators, plasma heating wall-plug demand, cryogenics, fuel processing, cooling, controls and other auxiliaries exactly once. Distinguish compressor shaft work already subtracted within the cycle from separate electrical loads. Count recovered friction heat once as heat while retaining the associated electrical demand. Check imported-power and nonpositive-net cases explicitly.

Enforce source/exchanger return conditions, temperature approaches, finite cooling, offered capacities and supported properties. Reuse the recent return-control and numerical lessons; do not rank a case merely because older checks omit a required interface condition.

Build an explicit account mapping so existing whole-plant steam/conversion allowances are removed when replaced, and new purchases are not charged twice. Use consistent currency years and documented conversion, finance, availability, lifetime, replacements and decommissioning. An unknown cost must be labeled and bounded, not omitted because it is common to both branches: a common numerator can change the ranking when electricity differs.

Preserve MR-7. Equipment choices stay supplied; inadequate selections fail. Coupled physical closures belong in the model, with independently selected inputs separated from solved operating states. A controller may calculate an operating action under reviewed assumptions; it may not silently purchase hardware or choose a preferred design.

Obtain independent review of the complete power/cost boundary and variable roles before dependent main-study work. Repair numerical implementation defects and revalidate changed executables rather than copying native errors into the oracle or loosening thresholds to obtain a result. Follow declared caps and surface required exceptions.

## 3. Run a fair plant-level component trade study

- Replay the predecessor's controls and document which outputs change solely because the accounting boundary is now complete.
- Re-evaluate compatible passing offers at the predecessor's common source conditions. Re-rank equipment and operating choices by whole-plant LCOE. Do not assume the subsystem's least-cost offer is also the plant's least-cost offer.
- Give both branches a comparable opportunity to choose supported operating settings and explicitly priced equipment offers. Their models have different operating freedoms; state those limits rather than claiming equal global optimization. If a small justified extension is necessary for a fair comparison, implement it through the modeling workflow. Do not open an unbounded technology-development program.
- Keep all attempted cases, including unsupported domains and engineering failures. Rank only supported cases satisfying the implemented system requirements, and disclose scientific qualification limits.
- Show net export, annual electricity, whole-plant overnight/financed capital, fuel, nonfuel operation, replacements, terminal costs and LCOE contributions for each representative pair.
- Attribute the system difference to conversion output, internal power demand, conversion purchases/service, common reactor expenses and any branch-dependent upstream consequences. Use diagnostic substitutions for attribution only, clearly labeled; never present a substituted output as an independent prediction.
- Sweep the uncertainties that can change the choice: conversion prices and efficiency, credible common reactor cost scope, primary/other electrical loads, fuel supply and availability where relevant. Report intervals or break-even thresholds without presenting arbitrary sweep endpoints as established uncertainty bounds.
- Explain whether including the reactor changes the predecessor's ranking and why. If it does not, explain why the preference survives. Either result can support the demo; do not seek a predetermined winner.

## 4. Deliver a result a reader can understand

Lead the answer with the engineering conclusion, not task counts:

“We held [reactor concept and operating condition] fixed and changed [conversion option]. This changed [net export and cost] because [mechanism]. The preference survives [tested changes] and changes when [specific assumption or threshold].”

Provide:

1. A compact pair of whole-plant assembly diagrams, highlighting the component choice and common reactor, with both energy and cost boundaries visible.
2. A baseline/alternative table with full net export, capital and whole-plant LCOE in one currency year.
3. A system-level power and cost contribution figure that explains the choice. Show the subsystem-only ranking beside the whole-plant result where useful; label both boundaries.
4. A preference/sensitivity plot identifying where either branch is cheaper, indeterminate or unsupported. Exclude failed cases from winner curves but show their status separately.
5. A concise proposed article passage stating the design question, result, causal explanation and a proportionate caveat. Do not bury the result in implementation history or imply vendor qualification.
6. Source data with case identities and check status, SVG/PNG figures, a reproducible renderer, the full candidate ledger, exact replay commands and sealed numerical verification.

The final independent review must explicitly check that the headline is whole-plant LCOE with complete declared power/cost scope, that the original subsystem ranking was not reused without reranking, and that the conclusion is supported despite remaining assumptions.

## Execution, preservation and closure

Use subagents for bounded upstream accounting, conversion/interface and independent review tasks with explicit file ownership. Coordinate shared integration sequentially. Keep a findings log suitable for the write-up: what transferred, what required a new relationship, and what the system comparison taught us.

Additive isolated models/packages, necessary interface and accounting repairs, targeted studies, independent review and local commits are within this requested work. Preserve existing Stellaris and ARIES baselines, both prior conversion records, source evidence and historical failed attempts. Another architecture goal is active; do not concurrently edit its owned files or rely on unreviewed changes. Use retained sources first and respect research access restrictions. No purchases or external messages without authorization.

Commit coherent task increments with explicit paths; never include the owner's staged write-ups. Do not edit the report itself. No push or merge. Ground bounded rounds and retry limits through the runbook; do not evade a cap by renaming a task. Formal goal and item closure remain with the owner.

Stop as complete only when the plant-level engineering/economic question above is answered on verified evidence. Passing tests, assembling both branches or documenting why subsystem costs differ are necessary steps, not the requested endpoint.
