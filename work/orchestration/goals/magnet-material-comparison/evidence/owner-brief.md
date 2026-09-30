# Run-goal prompt: a sourced magnet-material comparison

Use the run-goal skill to ground and pursue the question below in `/home/reid/1cfe/fusion-tea`.

Goal slug: `magnet-material-comparison`. This prompt supplies the name; use it without another naming confirmation. Preserve this prompt as the goal's initiating brief. Create native goal records from the templates, then begin the first round. This prompt requests execution, including obtaining sources and making the necessary bounded model additions.

## Authority and purpose

[OWNER-VERBATIM] After discussing a proper magnet study including fetching data, the owner said: “yes, please write the goal and we will see how it goes. write a full run-goal prompt to /tmp”.

[AGENT] (ratified by owner, 2026-09-29) Start with a magnet-subsystem comparison of REBCO and Nb₃Sn at matched magnetic duty. Collect and assess sources first, build supported alternatives, then compare conductor inventory, winding space, refrigeration demand, and cost. Complete reactor redesign is outside this initial scope.

[AGENT] The detailed execution choices and bounds below implement that agreed direction. They are starting judgments, not owner-originated scientific requirements or predetermined findings. Refine them from evidence without silently changing the comparison's meaning. Preserve these authority distinctions in downstream records.

The consumer is the owner evaluating whether the model can support a credible component/material-choice study. Existing editorial corrections can proceed independently. A useful result may eventually support the write-up, but this goal must earn its conclusions through evidence.

## Engineering question

For the same specified magnetic duty in a supported operating range, how do explicit REBCO and Nb₃Sn winding alternatives compare in current margin, conductor inventory, winding fit, refrigeration demand, and subsystem cost, and which assumptions determine the preference?

Begin with REBCO near 20 K and Nb₃Sn near 4–4.5 K as candidate operating conditions. Choose exact temperatures, conductor constructions, and the comparison range from sources. Do not force Nb₃Sn into the existing 24.9 T Stellaris reference. Find a common supported lower-field range and explain the resulting scope. No numerical field ceiling in this prompt is a universal material limit.

The comparison must instantiate genuinely different conductor definitions with their applicable properties and equations. Changing a few price, temperature, or field-limit inputs in the same unsupported conductor law does not answer the question.

## Grounding and existing evidence

Read AGENTS.md, CLAUDE.md, `.agentic-mbse/codex.md`, `.project/codex-test-setup.md`, the run-goal skill, and the relevant sections of `work/orchestration/GOAL_RUNBOOK.md`. Read `modeling_project/REQUIREMENTS.md`, especially MR-7, and use the native modeling, research, integration, and study workflows where applicable. Use `.codex-test/run` for Python/toolkit commands in this worktree.

Start with:

- `.project/active/write-up/magnet-study-evaluation/evaluation.md` and `narrative-proposal.md`: prior category-fit investigation, source limitations, and replay findings. These are investigation evidence, not a sealed new study or authority for a physical conclusion.
- `.project/active/write-up/magnet-study-evaluation/data/claim-evidence.csv` and `replay/`: pointers to historical claims and current supplied-winding replay.
- `.project/active/write-up/feedback-resolution.md`: editorial context and accepted separation of this future study from the write-up corrections.
- `work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md` and the magnet-closure goal's records: earlier sizing behavior and its later repair. Locate current native work items through tracking rather than assuming active paths.
- `knowledge/SOURCE_INDEX.md`, `knowledge/KNOWLEDGE.md`, and relevant prior research: existing REBCO, EU DEMO Nb₃Sn winding, and ITER refrigeration evidence.
- Current conductor, magnet geometry, fit, cryogenic, and costing definitions and their consumers. Establish actual current bindings before designing alternatives.

Known limitations to verify and account for:

- The September sizing study uses one REBCO conductor and historical automatic sizing. Today's supplied-winding replay does not make it a material comparison.
- The current REBCO law is restricted to 20 K and includes inferred tape assumptions. Published tape measurements do not directly establish cable or winding-pack capability.
- The historical 24.9 T ceiling was calibrated to the Stellaris reference. The reported field rise with a larger winding comes from coil position while omitting a winding-size contribution that could change its sign.
- Refrigerator and building capacities in the replay start with zero margin. These are selected-capacity comparisons, not universal limits.
- The August REBCO/Nb₃Sn input swap predates current conductor physics and cannot serve as the new comparison's validation.

## First milestone: establish data sufficiency

Use the research seam described in `docs/research_seam_operator_guide.md`, including request records, acquisition bookkeeping, and source registration. Apply the prescribed clean-room/source-access screen before fetching. Read the screening protocol as required; do not inspect quarantined scientific content or infer that an earlier source exception applies to this goal. Prefer existing registered sources and primary public evidence. Fetch missing permitted papers, supplements, datasets, and manufacturer documentation; retain source artifacts and inspect figures/tables behind consequential numbers.

Useful starting leads, to evaluate rather than adopt uncritically:

- Registered Molodyk et al. REBCO paper, DOI `10.1038/s41598-021-81559-z`: https://www.nature.com/articles/s41598-021-81559-z
- Registered Demattè/Bruzzone EU DEMO winding-pack study under `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/`.
- Registered ITER cryoplant sources under `knowledge/sources/iter_cryoplant_iter_org/`.
- NIST Nb₃Sn field/temperature/strain scaling lead: https://www.nist.gov/publications/extrapolative-scaling-expression-fitting-equation-extrapolating-full-icbte-data

Produce an evidence matrix covering:

1. Conductor identity, construction, dimensions, and critical-current dependence on field and temperature; strain and REBCO field orientation where relevant. State the measured domain, fitting domain, electric-field criterion, and any extrapolation.
2. The conversion from tape/strand performance to engineering conductor and winding-pack performance: stabilizer, copper/non-copper basis, substrate, jacket, insulation, voids, cooling space, cabling degradation, and packing assumptions. Avoid mixing current-density denominators.
3. Operating margins and the support for any mechanical or thermal limits used as checks.
4. Cryogenic heat loads and refrigerator electrical demand at the selected temperatures, with temperature stages and load allocation explicit. A plant-wide efficiency inferred from mixed-temperature loads is not automatically a single-stage refrigerator law.
5. Cost basis: physical purchase units, amount purchased, currency/year, fabrication and installation scope, replacements if modeled, and uncertainty. Identify whether figures describe tape, strand, cable, winding, or installed magnets.

Classify each required quantity as directly supported, derived, a bounded assumption, or unavailable. State what each gap prevents. Have consequential new source interpretations/equations independently checked against originals before dependent modeling.

Proceed autonomously if evidence supports a useful conditional comparison. If cost evidence supports only ranges, use ranges and break-even analysis. If conductor or packing evidence cannot support a matched comparison, report the precise gap and close the round as unmet; do not manufacture properties. A data-sufficiency report alone is partial completion of the overall question.

## Comparison contract before implementation and the main study

Write and independently review a compact contract defining:

- Magnetic duty and geometry boundary: ampere-turn demand, relevant field magnitude/orientation, conductor length basis, spatial allocation, and operating assumptions. Explain which are fixed, derived, or varied, and why the combination is physically consistent.
- A common supported range for both alternatives. Separate any REBCO-only high-field extension from the matched comparison.
- Actual offered winding designs, selected operating temperatures, and current margins. Different materials may need different inventories to meet the same duty; enumerate those choices explicitly and price the selected inventory.
- Outputs, accounting boundary, failure/unsupported conditions, numerical tolerances, and criteria for a materially different result.
- Which mechanical, protection, irradiation, lifetime, or geometry effects are evaluated and which limit the interpretation. A subsystem screening comparison does not require full magnet qualification, but omitted effects cannot support a qualified-design claim.

A supplied field-demand benchmark is an acceptable initial boundary if it is coherent and its limits are explicit. If geometry changes feed back into field in the claimed result, repair or replace the deficient geometry relationship with supported evidence first. Do not claim a reactor redesign from a fixed-duty calculation. Do not claim that lowering the field preserves Stellaris plasma performance.

## Model and study requirements

Use native model work items for additive conductor alternatives, required interfaces, and cryogenic/cost changes. Preserve existing reference behavior and historical packages/studies through isolated variants and relevant regression evidence.

Apply MR-7 throughout: turns, parallel conductor count, pack dimensions, and installed refrigeration capacity remain explicit choices where appropriate. Calculate requirements and compare them with supplied capacity. A separately declared search may propose candidate hardware, but the evaluator must not silently resize each case until it passes. Inventory and cost must follow the supplied design.

Verify insufficient and sufficient supplied designs for each applicable capacity/fit relation, plus unsupported-domain behavior. Check units, current-density conversions, temperature dependence, and representative source points independently of the implementation. A calculation reproducing its own formula is not sufficient validation.

Run a bounded native study with matched cases spanning a useful supported duty range and explicit design offers. Keep failed and unsupported cases with distinct status. Show the consequences of material choice through conductor quantity, fit/margin, cold load, electrical refrigeration demand, and cost. Explain at least one matched comparison causally.

Test at least two consequential uncertainties chosen from the evidence, likely winding packing/cabling performance, cryogenic load/efficiency, and conductor price. Report where preferences reverse or remain unresolved. Do not demand a winner, a dramatic crossover, or a global optimum. Price uncertainty may justify a break-even price instead of a point ranking.

Keep economics within the declared magnet/refrigeration subsystem. Full-plant LCOE is outside this initial goal. Report partial accounting explicitly when an unsupported cost category prevents a total installed-cost claim.

## Execution bounds and ownership

[AGENT] Initial limit: at most four rounds, following native per-round pin/study and retry limits. Start with source sufficiency and a supported comparison contract; choose subsequent tasks from results rather than committing to a fixed sequence of rounds. At the limit, deliver the best supported answer and identify unmet criteria.

Source acquisition, bounded model additions/repairs, native studies, and required independent reviews are within the intended execution scope. Routine implementation choices need no repeated owner confirmation. Return material scope changes, unresolved scientific choices that change comparison meaning, and source-access exceptions to the owner. Full reactor optimization or a new detailed electromagnetic/mechanical solver would require an expanded scope.

Use fresh subagents for independent source/math checks and triggered design/integration reviews. Supply self-contained briefs and original evidence; in Codex use `fork_turns: "none"`. Parallelize independent research with clear file ownership and integrate registry/shared changes carefully. If required review is unavailable, park dependent work under the runbook and continue independent work where useful.

Preserve unrelated work and the owner's article/HTML. Do not publish, push, merge, purchase sources, or contact vendors/authors. Record unavailable evidence and the access needed. Formal goal closure and work-item closure remain owner-held. Follow native PM ownership; cite editorial artifacts as evidence rather than copying their state into modeling records.

## Deliverables and answer contract

Provide:

- Native grounded goal, trail, learnings, and linked research/model/study records.
- Source evidence matrix and data-sufficiency finding, with retrieved artifacts, exact source locations, and derived calculations.
- Reviewed comparison contract and supported alternative definitions.
- A sealed, verified native study with case identities, explicit choices, failed/unsupported statuses, validation/review evidence, and exact replay instructions.
- `answer.md` explaining what differs between the materials, what the comparison establishes, which assumptions matter, and what remains unanswered.
- A compact results table and useful SVG/PNG figures with source data and rendering script, including margins/fit and refrigeration/cost tradeoffs. Every plotted result must trace to a recorded case.
- A short proposed narrative explaining the starting duty, changed material/design, measured consequences, and limits. Assess whether it now qualifies as a defensible component/material-choice example. Do not edit the article or supporting HTML.

The question is answered when an executed, independently checked comparison of genuinely different supported conductor alternatives quantifies the requested subsystem consequences at matched duty, uses consistent accounting, and tests the assumptions that could change the conclusion. Where a dimension is only bounded, say so and show whether the bound still supports a decision. If missing physics or costs prevent the requested conclusion, report partial/unmet completion and the exact next evidence needed. Scientific qualification of a complete stellarator magnet is beyond this answer contract.

Begin by grounding the goal from this brief and inspecting the existing source/model evidence. Continue within these bounds until the answer contract is met, a reserved gate blocks dependent work, or the round limit is reached.
