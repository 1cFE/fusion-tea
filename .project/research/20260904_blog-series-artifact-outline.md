# Blog series: engineering models that can be tested and improved

Date: 2026-09-04. Status: proposed editorial outline, not an approved publication plan.

## Audience and purpose

- [OWNER-VERBATIM] Audience: "anyone with a technical or engineering background with rough familiarity with the process for engineering hardware systems."
- [OWNER] Approachability is the critical criterion. Outline primary posts and all supporting HTML deep dives, hosted on GitHub, with clear message points and only a couple of supporting sentences per point.
- [AGENT] Proposed package: four primary posts and six HTML companions. Titles, grouping, sequence, examples, and presentation choices below are agent recommendations; the cited research catalog is supporting material, not owner-settled scope.
- [AGENT] Throughline: We are building a way to investigate what must be true for cheap fusion power. Connected engineering models let us test design changes, and agent-assisted studies help expose and repair the assumptions that determine the answer.
- [AGENT] Reader entry: assume familiarity with components, requirements, trade studies, and design reviews. Introduce fusion physics, SysML, electricity-cost terminology, and agent workflows through the example that needs them.

## Primary posts

### P1. Change the design. Follow the cost.

**Main message:** A useful cost model follows an engineering change through the plant: what it changes physically, what must be bought, and how much electricity remains to sell.

- **The cost target tells us which engineering questions to ask.** Start with 1cFE's question: what must be true to reach one cent per kilowatt-hour? Place the broad concept survey and selected deep studies in that investigation, then introduce the stellarator as the worked example for this modeling route.
- **The engineering model connects parts, calculations, and limits.** Follow internal power consumption into saleable electricity and cost, using the corrected pumping-power assumption as the opening example. Introduce SysML as the written model, agentic-mbse as the research and modeling toolkit, sysml-codegen as the translator, and TEAx as the calculation and study runtime.
- **That connected model becomes something we can experiment with.** Show one evaluated design and then a comparison across designs, with both cost and engineering-check results. Explain that 1costingFE supplies broad costing from specified design points, while this route makes selected engineering relationships explicit in the model; the demonstrated execution evaluates proposed points rather than generally solving backward from a target.

Companions: H1 for the project map; H2 for the complete worked example. The short post should leave a reader able to explain why changing one input can change several parts of the answer.

Evidence: [project scope](../../modeling_project/OVERVIEW.md), [pumping-power study](../../exploration/stellarator_e2e/studies/20260829-p-pump-fence/record.md), [pipeline hypothesis dossier](../../modeling_project/HYPOTHESIS_DOSSIER.md), [1costingFE introduction](../../../1costingfe/docs/blog/3%20Intro/1costingfe-intro-post.md), [TEAx execution and studies](../../../teax/docs/evaluation-and-study.md).

### P2. The cheapest design exposed what our model was missing

**Main message:** Exploring a design space tests the model as well as the design. An apparent bargain can reveal a missing physical benefit, an unsupported operating point, or an unpriced component.

- **A cheaper component can lose at the plant level.** The historical magnet comparison found the cheaper magnet option feasible at none of the evaluated points. It also exposed a model that represented field-related penalties without rewarding field through confinement, giving the next modeling task a concrete purpose.
- **A trade study must say what stays fixed.** Compare heating efficiency at fixed electrical draw with efficiency at fixed heat delivered to the plasma. The modeled cost trends have opposite signs because one experiment increases source output while the other reduces the electricity consumed internally.
- **Improving the model can make its answer worse.** Correcting an average-versus-peak wall-load check made the reference model fail the limit and increased replacement costs. Show why that is progress in understanding the design, while keeping each result tied to its model version and evaluated range.

Companion: H3 for the sequence of engineering changes and interactive comparisons. The concluding question is what engineering relationship must be understood next.

Evidence: [magnet A/B study](../../exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md), [operating-point narrative](../../work/narratives/20260904-184254Z-operating-point-closure.md), [priced-levers narrative](../../work/narratives/20260904-184254Z-priced-levers.md), [heating narrative](../../work/narratives/20260904-184254Z-wall-and-heating.md), [wall correction and integration](../../work/orchestration/goals/wall-and-heating/trail.md).

### P3. Giving AI agents an engineering job they can finish—and others can check

**Main message:** Agents become useful collaborators when a question leads to bounded work, executable checks, a reviewable result, and a clear next decision.

- **Start with an engineering question and an observable answer.** Use a real goal such as checking whether the modeled plant has enough heating to sustain its chosen plasma state. Show how that question becomes research, a model change, and a study, including an attempted solution that the evidence ruled out.
- **The coordination system makes the work survive beyond one conversation.** Explain the harness as agents plus procedures, tools, and saved records: what was attempted, which model ran, what happened, and what remains unresolved. Show how another session can continue or inspect the work from those records.
- **Review changes what happens next.** Follow one reviewer correction into the next engineering decision, such as distinguishing the constraint that blocks the most candidates from the one that blocks cheaper candidates. Make the division of responsibility concrete: agents research and execute, scripts enforce mechanical checks, separate sessions critique, and the owner sets direction and closes or redirects goals.

Companion: H4 for one complete round, with actual artifacts and handoffs. The benefit is demonstrated continuity and correction; the documented workflow still uses an operator to arrange fresh review sessions.

Evidence: [goal-harness concept](../concepts/goal-driven-model-development-harness.md), [operating runbook](../../work/orchestration/GOAL_RUNBOOK.md), [verified product promise and limits](../product/0001-goal-round-native-operability.md), [priced-levers review and decisions](../../work/orchestration/goals/priced-levers/trail.md).

### P4. What our AI-built engineering models have actually demonstrated

**Main message:** The project began with testable bets about agent-assisted research, formal models, and executable studies. Different experiments establish different parts of that case.

- **Agents have derived useful engineering relationships from research.** Explain the bounded blind-derivation experiment: agents worked from literature without the comparison code, then their relations were compared with that code. It found useful agreement, defensible differences, and two defects in the reference implementation; its scope was one family and a few relations.
- **Faithful execution and sound engineering require different evidence.** Exact agreement with a checking calculation tests translation; account-by-account reconciliation tests agreement with another costing implementation. Source inspection, behavior away from the reference point, and independent engineering comparisons address further questions that arithmetic agreement cannot settle.
- **The next test is more demanding than the last.** Show how studies exposed missing relationships and how repeated grading measured specific improvements in model depth. State that the planned independent stellarator comparison remains unperformed at this outline's cutoff, and identify what it is meant to test.

Companions: H5 for one source-to-result investigation; H6 for the evidence by claim. End with the remaining engineering questions and the evidence that would answer them.

Evidence: [hypothesis dossier](../../modeling_project/HYPOTHESIS_DOSSIER.md), [blind derivation comparison](../../work/completed/20260705_WI-016_h2-blind-derivation/comparison.md), [cost reconciliation](../../exploration/stellarator_e2e/HANDSHAKE_REPORT.md), [maturation concept](../concepts/stellarator-demo-maturation.md), [depth rubric](../active/demo-depth-rubric/rubric.md).

## Supporting HTML artifacts

These six companions are the proposed complete supporting set. Each should open with an engineering question, show a useful result before implementation detail, and allow readers to inspect the evidence without installing the project. Proposed filenames below are destinations, not existing or published pages.

### H1. How the fusion landscape leads to deeper engineering studies

Proposed destination: `docs/series/landscape.html`. Supports P1; a shared orientation page for the series.

- **Broad comparisons help choose the next questions.** Show the concept landscape, common costing basis, and uncertainties that motivate closer investigation. Distinguish choosing informative studies from declaring a winning reactor.
- **The project uses two routes with different strengths.** Draw the breadth pipeline that prepares 1costingFE inputs alongside the route that develops and executes formal engineering models. Put the stellarator and colleagues' corridor studies in context without implying that every surveyed concept has a SysML model.
- **Readers can follow the question that interests them.** Link a few representative concepts to existing explainers and public tools. Use the map to lead into the worked engineering example rather than reproducing the whole concept database.

Presentation: one clickable project map, a small comparison of the two routes, and a compact concept example. Reuse selected material from [the concept-pipeline draft](../../docs/concept-pipeline/pipeline.md), [down-selection explainer](../../docs/demo/down-select.html), and [Score Explorer](../../docs/index.html); verify draft corridor claims before publication.

### H2. Follow a plant model all the way to a trade-study result

Proposed destination: `docs/series/model-to-study.html`. Supports P1 and supplies technical detail for P3.

- **A component's behavior and cost are connected in the model.** Let readers inspect a small plant diagram and follow one parameter into calculations, equipment costs, and engineering limits. Show a short source-model excerpt beside the plain-language explanation.
- **The generated program preserves those connections.** Trace that same parameter through the executable inputs, calculation, and result. Explain each tool's responsibility at the point where it acts, with deeper sections for model translation, generated versus supplied calculation code, and TEAx execution.
- **A study is a specified comparison with inspectable evidence.** Walk through the actual power-cycle and magnet A/B studies: question, changed and held quantities, pre-run checks, results, verification, and a second reader's interpretation. Let readers inspect one point's cost, failed checks, and whether applicable checks were assessed.

Presentation: connected model explorer plus two comparison tabs and expandable real artifact exhibits. Adapt [the existing workflow page](../../docs/demo/index.html), [the dated IFE demonstration](../../docs/demo/closed-loop.html), [the existing A/B explainer render](../mental-alignment/runs/20260823-151503_run-study-e2e-explainer_resumed.html), and [the TEAx explainer](../../../teax/docs/teax-study-explainer.html).

Relationship to existing work: the [approved A/B explainer spec](../active/run-study-e2e-explainer/spec.md) is an existing scoped item. This proposal reuses its work; it does not amend or certify that item. Keep its two studies as dated evidence and distinguish their tooling from later execution behavior.

### H3. How each new engineering constraint changed the design study

Proposed destination: `docs/series/stellarator-studies.html`. Supports P2.

- **A map of low cost needs a map of what can work.** Step through selected historical model versions as field, confinement, heating, and wall loading become connected. Each version shows its own tested region and assumptions; changing the model can change which designs pass.
- **What stays fixed determines what an efficiency improvement buys.** Let readers switch between fixed electrical draw and fixed delivered heating. Show power flow, source rating, plant self-consumption, and the recorded cost trend together.
- **A flat cost curve can reveal a missing cost account.** Show winding-pack geometry changing stress and refrigeration while magnet capital remains unchanged in the priced-levers study. Connect that result to the missing pack-material costs and the resulting development question.

Presentation: dated study selector, constraint overlays, and an efficiency comparison using recorded cases. Use [study records and data](../../exploration/stellarator_e2e/studies/) and the [three narrative snapshots](../../work/narratives/); retain the old [proof-of-life report](../../exploration/stellarator_e2e/study/report.html) only as historical evidence.

### H4. Follow one engineering question through the agent team

Proposed destination: `docs/series/agent-round.html`. Supports P3.

- **The question determines the work.** Follow the operating-point goal from the inability to check heating sufficiency through the failed solver prototype and the eventual forward heating-requirement calculation. Make the reason for the change in approach visible.
- **Each handoff transfers evidence another person can inspect.** Show the actual task, source findings, model change, identified executable, study result, and review. Let readers open short excerpts and follow links to the complete records.
- **A round ends in a justified next decision.** Show what the study answered, what remained unresolved, and who decided what followed. Include the actual scope of human involvement and a reviewer correction from the chosen goal.

Presentation: a worked timeline with lanes for the owner, working agent, tools, and separate reviewers. Reuse the [operating-point narrative and its evidence links](../../work/narratives/20260904-184254Z-operating-point-closure.md); use the [current runbook](../../work/orchestration/GOAL_RUNBOOK.md) to explain the procedure without turning the page into an operator manual.

### H5. Follow a wall-load number from the paper to the electricity cost

Proposed destination: `docs/series/source-to-result.html`. Supports P4 and deepens P2's wall-load example.

- **A readable extraction can still misstate the source.** Put verified source evidence beside the mistaken extraction and explain the actual discrepancy. Show where document extraction, indexing, source registration, and page inspection fit into the research workflow.
- **A correct number still needs the correct physical meaning.** Explain average versus peak wall loading, the sourced calibration, and why a peak limit must be compared with a peak quantity. State that this is a calibrated relationship with assumptions about wall shape, not a new three-dimensional neutron simulation.
- **The correction changes engineering and economics together.** Follow the corrected peak into the wall verdict, component lifetime, replacement count, annual cost, and electricity cost. Show that the resulting reference model fails the wall check; this does not establish that the published reactor design cannot work.

Presentation: a source-to-equation-to-result trace with before/after values and expandable evidence. Start from the [page-verified source-basis report](../../work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md), use implemented values from the [task and integration record](../../work/orchestration/goals/wall-and-heating/trail.md), and adapt extraction explanations from [agentic-mbse's internals](../../../agentic-mbse/docs/extraction-internals.md).

### H6. Which tests support which claims?

Proposed destination: `docs/series/evidence.html`. Supports P4 and provides a common evidence reference for the series.

- **The original bets can be assessed separately.** Present agent research, model authoring, representation of engineering relationships, and executable exploration as distinct claims. For each, show the dated experiment, result, and remaining uncertainty.
- **Agreement has to be interpreted.** Contrast a calculation that checks the same equations, the bounded blind derivation, and the 1costingFE reconciliation. Use the reconciliation's explained differences to show why matching or differing headline costs alone is insufficient.
- **Model improvement and independent validation are separate milestones.** Show selected subsystem grades before and after engineering work, alongside the unperformed independent stellarator comparison. Keep mechanical checks, physical completeness, and evidence of real-world accuracy distinguishable.

Presentation: a compact claim/evidence/limit matrix, an expandable reconciliation waterfall, and a few before/after model-depth examples. Use the [dossier](../../modeling_project/HYPOTHESIS_DOSSIER.md), [handshake report](../../exploration/stellarator_e2e/HANDSHAKE_REPORT.md), and [grading records](../active/demo-depth-rubric/).

## Evidence and reuse notes

- [AGENT] Keep numeric comparisons within their recorded model version. The July IFE demonstration had manual wiring and externally applied viability checks; current execution documentation describes generated constraints and coverage-aware outcomes. These are different stages of the toolchain.
- [AGENT] The latest wall implementation inspected for this outline reports a peak of approximately 4.088 MW/m² against 4.05, and baseline electricity cost of approximately $313.51/MWh. Its baseline fails wall loading and sustainment; the new study had started but no completed result was used here. Earlier optimum values are historical study results, not current feasible designs.
- [AGENT] The cost reconciliation is a completed demonstration at a recorded model state. Later model development is not required to preserve those values; the source report includes explicit remainders and different financing conventions.
- [AGENT] Treat the existing constraint-propagation HTML as an exploratory assumption-management demonstration. It is not an explanation of the current numerical constraint executor. The full dependency graph, runtime internals, and extraction history can sit behind relevant deep-dive sections rather than becoming additional primary posts.
- [AGENT] Some useful HTML drafts already exist under `.project/mental-alignment/runs/` even though the earlier A/B outline is missing. They are reuse candidates, not published or certified artifacts.
- [AGENT] The four primary posts should carry their conclusions independently of the companions. A reader should be able to stop after a post with a clear engineering takeaway, or follow its HTML link to inspect how the claim was established.

## Public context checked

The existing [June concept-pipeline post](https://1cf.energy/from-papers-to-plant-economics/) already explains the broad survey and first costing pass. This series can build on that coverage while supplying enough orientation for a new reader. The [updates index](https://1cf.energy/updates/) also lists the earlier modeling-method and 1costingFE introductions.

Supporting reads were divided among three agents: pipeline and execution evidence; stellarator studies and the goal harness; landscape, corridor context, and existing visual assets. The main agent read the catalog, project context, original hypothesis evidence, prior reader feedback, and the existing A/B explainer specification, then synthesized this proposal.
