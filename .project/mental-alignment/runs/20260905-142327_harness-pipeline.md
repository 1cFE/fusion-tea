---
question: |
  I want you to RESUME the $my-mental-model for .project/mental-alignment/runs/20260905-135058_harness-pipeline.md

  I am not happy with the current iteration. For reference, see:
  - .project/concepts/physical-innovation-narrative.md
  - .project/research/20260905_1cfe-writing-style.md
  - .project/research/20260905_1cfe-writing-style-sources/README.md
  In addition to the usual guidance for the mental model. Start a fresh agent to fully revise the synthesis to improve the content and the writing.
date: 2026-09-05 14:23
policy: discovered
shape: plain_document
subject: "The engineering harness across agentic-mbse, fusion-tea, sysml-codegen, and teax"
evidence:
  - .project/mental-alignment/runs/20260905-135058_harness-pipeline.md
  - .project/mental-alignment/feedback-synthesis.md
  - .project/concepts/physical-innovation-narrative.md
  - .project/research/20260905_1cfe-writing-style.md
  - .project/research/20260905_1cfe-writing-style-sources/README.md and its three archived article bodies
  - .project/CURRENT_WORK.md and CLAUDE.md
  - .project/product/0001-goal-round-native-operability.md
  - .project/research/20260904-135403_blog-series-topic-catalog.md, selected landscape and harness sections
  - docs/concept-pipeline/pipeline.md
  - work/orchestration/GOAL_RUNBOOK.md
  - ../sysml-codegen/docs/architecture/overview.md, selected architecture sections
  - work/orchestration/goals/operating-point-closure/goal.md
  - work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md
  - exploration/stellarator_e2e/studies/20260901-sustainment-fence/synthesis.md
  - .project/research/20260905-091948_blank-study-column-root-cause.md, summary and boundary trace
code_inspected: "Representative sustainment constraint, generated Python wrapper and pipeline wiring; maintained sustainment implementation's contract and declarations; study preflight entry point; TEAx StudyStore construction and compatibility check. Paths appear below."
limits: "No tests, studies, or physics calculations rerun. Historical counts are taken from the study administrator's recount. No full compiler, extractor, agent-dispatch, or runtime audit. Current generated code illustrates structure, not the historical executable. Quarantined hold-out material was not opened."
---

# The engineering harness

## TLDR

- The ambition is to make better decisions about physical technology before committing to hardware. For fusion, that means finding which assumptions make a plant look promising and what would have to be demonstrated for those assumptions to hold.
- A cost estimate becomes more useful when it accounts for how the machine's parts affect each other. Agents use research to establish those relationships, then run calculations to see how a design choice changes performance and cost or exceeds a component's limits.
- The repositories divide that work: `agentic-mbse` supports research and model authoring, `fusion-tea` holds the fusion investigation, `sysml-codegen` translates models into executable packages, and `teax` runs calculations and studies.
- Agents use these capabilities to pursue a question. They choose one task with a stated scope and stopping condition, examine its result, and revise the approach. Files preserve the evidence between sessions, so another agent can review the work or continue it.
- One stellarator investigation showed why these connections matter. Stronger magnetic field helped the plasma retain energy, but the field needed to meet the heating shortfall exceeded what the magnet's conductor could tolerate. The owner directed further work toward magnets and heating.

## 1. The harness connects component claims to plant consequences

The owner asks: “What would it take for us (humanity) to rapidly accelerate real innovation and progress in the world of physical technology?” The opportunity is to improve which concepts receive investment and understand “exactly *what* needs to be demonstrated for some larger concept to be viable”. [OWNER-VERBATIM: [narrative concept][purpose], § 1.]

A promising plasma is only part of a fusion power plant. A stronger magnet might help retain plasma energy, but it also asks more of the conductor. More heating might sustain the plasma, but it consumes electricity the plant could otherwise sell. We need to follow both consequences of a proposed improvement before deciding whether it helps the machine. Section 4 shows an investigation of this conflict.

To answer that kind of question, an engineer needs to connect evidence about individual components to calculations of the whole plant. An agent can help build and exercise those relationships, then use the results to argue for another calculation, better evidence, or a model change. That is the purpose of the harness. [AGENT synthesis of the [topic catalog][catalog], §§ 5.3–5.7, and the [goal runbook][runbook], § The native seams.]

That work demands support for branching, exploration, and rapid iteration in textual SysMLv2 models. Automating it brings familiar software-engineering problems: delivering scoped tasks, maintaining good architecture, and fighting generated slop. Because these models represent real physics and engineering, model authors must be especially vigilant against hallucinations: plausible-looking equations or values can misrepresent the machine being analyzed. [OWNER: progression supplied in the 2026-09-06 correction.]

Stepping back, the 1cfe project has surveyed 38 fusion concepts and developed high-level models of their levelized cost of electricity (LCOE) using the common 1costingFE framework. The larger aim is to identify corridors to fusion electricity at 1 cent/kWh: combinations of design choices and technology assumptions that could reach that cost. The SysML-driven framework discussed here is a proposed route to identifying those corridors, tested on stellarator designs. [OWNER: narrative supplied in the 2026-09-06 correction; project context in [the topic catalog][catalog], §§ 2 and 5.2.]

For the visual, follow one design choice into its performance benefit, engineering burden, and economic consequence. Distinguish calculated consequences from what a hardware demonstration must establish.

## 2. Studies run Python packages built from engineering models

Model authors need to express components, calculations, and connections in a form they can revise and review. Studies need an executable package they can run repeatedly. Textual SysML serves the first job; generated Python serves the second. This separation lets authors change the machine's structure without manually rewiring every downstream calculation. [AGENT rationale, grounded in [the tooling catalog][catalog], § 5.4, and [codegen architecture][codegen], opening and § Data Flow.]

The author uses `agentic-mbse` research and modeling support to turn source material into model definitions and citations. In `fusion-tea`, those reusable definitions are combined into particular plant designs alongside their evidence. [INHERITED: [tooling catalog][catalog], §§ 5.3–5.4; [project structure][project-guide], § Project Structure.]

To construct that executable, `sysml-codegen` resolves each reference to the particular component instance and output supplying its value, then emits interfaces and wiring. Some numerical work remains maintained Python behind those interfaces; the sustainment calculation, for example, integrates plasma profiles and iterates the helium balance. Local package checks in `fusion-tea` establish the candidate to study, and `teax` runs cases and retains their evidence. [INHERITED implemented architecture: [codegen overview][codegen], § Data Flow; observed code: [sustainment implementation][sustainment-impl], opening contract, [preflight checks][preflight], lines 333–390, and [study store][store], lines 93–152.]

The heating comparison shows what survives the transformation. In the model, required plasma heating must not exceed installed plasma heating. Generated wiring supplies both calculated values to a Python interface, which returns their observed values, a verdict, and a margin. The engineering relationship now participates in every evaluated design point. [Observed code: [SysML constraint][constraint], lines 201–226; [generated wrapper][wrapper], lines 15–49; [wiring][wiring], lines 985–991.]

[Dropdown: What does “harness” mean here?] It is the combination of agent instructions, callable programs, evidence, and work records that supports an engineering investigation. A command such as `/run-goal` supplies instructions to a session. The session decides and calls tools; the command name does not imply a separate process. [AGENT explanatory definition, grounded in [the runbook][runbook], opening and § Running one task.]

For the visual, follow evidence → model → generated calculations → study evidence, with repository ownership attached. Distinguish agent work from program execution; expand the heating comparison in a detail view.

## 3. Agents choose the next task from the results

When a calculation exposes a bad assumption, the agent needs to reconsider its approach. The operator and agent first record the question and what would count as an answer. Under a declared strategy, the agent then chooses one bounded task from the evidence available and calls the relevant research, modeling, integration, or study workflow. A failed premise can end the round before any production model or study exists. [INHERITED operating contract: [runbook][runbook], §§ Grounding a goal, Opening and closing a round, and Running one task.]

The programs in § 2 carry out defined operations; the agents argue what the results establish. A separate study reader examines the committed experiment, and a fresh reviewer checks the round's work and proposed learning. The owner retains the decision to close the goal. [INHERITED: [runbook][runbook], §§ The fresh review, Grounding a goal, and The native seams.]

This connects two kinds of dependency. Calculation outputs feed other calculations within the model. After a study, the agent uses those results to decide what work is worth doing next, including whether the model needs to change. Section 4 shows that feedback in operation. [AGENT synthesis of the runbook and worked example.]

The next session needs the reasoning as well as the result. It reads the question and answer conditions in the goal file, then follows the trail's task, outcome, and decision references to the underlying evidence. Reviewed learnings record what the round established. Before continuing, the agent checks the native work and study artifacts to see what actually completed. [INHERITED: [runbook][runbook], §§ The five surfaces and Resuming an interruption.]

[Dropdown: Is the filesystem a database?] It serves as shared memory for much of the investigation, but the records have different storage rules. Goal records are Markdown; the modeling registry uses structured frontmatter and dedicated update operations; TEAx uses SQLite with associated evidence files. [Observed store construction: [store][store], lines 93–152; documented modeling operations: [project guide][project-guide].]

For the visual, show operator → goal session → selected work → stored result → separate reading/review → next decision. Put file reads and writes on the arrows, with the next task chosen after the result.

## 4. The stellarator study exposed conflicting heating and magnet limits

An earlier model charged for stronger field without crediting its ability to help retain plasma energy. The agent proposed investigating whether the machine could sustain its assumed plasma state. This is the selected `/run-goal` example, `operating-point-closure`, completed over September 1–2, 2026. [EXAMPLE: [goal][example-goal], §§ Consumer and Amendments. Its question and answer conditions were AGENT proposals under owner delegation.]

The agent first tried to solve plasma temperature from a steady-state power balance. In source checks and a prototype, it found no stable, feasible burn within the baseline machine's modeled limits, along with sensitivity to the stored-energy calculation. The agent ended the round with a strategy blocker. It now had a reason to change the formulation before production implementation. [INHERITED historical findings: [prototype notes][prototype], §§ The blocking findings and Consequence.]

The revised approach kept density and temperature as design choices, computed the heating they required, and compared that requirement with installed capacity. The agent carried the change through model work, executable-package preparation, and a study of field, density, temperature, and heating. The current constraint in § 2 shows the comparison's implemented form; the historical study used its own recorded package. [INHERITED: [prior run][previous], § 4.3, with native study evidence in [the administrator's reading][reading].]

Stronger field now had a benefit as well as a burden: it helped the plasma retain energy and could reduce the external heating needed, while raising the field experienced by the magnet's conductor. A feasible design point had to meet the heating requirement within the conductor's limit. [AGENT explanation of the inherited results in [the administrator's reading][reading], §§ What it found and Findings carried forward.]

Measurement: at 50 MW delivered to the plasma, none of the 154 evaluated field-density rows, including the baseline, was feasible. Every row that met the heating requirement exceeded the conductor's peak-field limit. At 110 MW, the tested window contained feasible points. Across the complete study, 9 of 334 evaluated rows were feasible; another 10 proposed points were excluded before execution. These are historical counts from [the administrator's recount][reading], §§ What it found and Findings carried forward.

The owner used this evidence to direct further work toward conductor capability and the heating system, then closed the goal. Those were concrete routes to investigate, although the study had not varied conductor capability and could not establish which route would be cheaper. [OWNER close and follow-on decisions recorded in [goal amendments][example-goal]; study limitation in [the reading][reading], § What the record does not support.]

[Dropdown: Does a feasible point mean the plant works?] It means the point passed the checks represented in that model. It does not establish unmodeled behavior or validate the underlying physics. In this study, some internal heating quantities came from the checking calculation's own export and were not independently verified. [INHERITED historical disclosure: [the reading][reading], § What the record does not support.]

For the visual, show the strategy change as a short timeline, then compare the sampled field-density points at 50 and 110 MW, colored by the constraints that reject them. Use the historical results directory beside [the reading][reading]; identify exclusions and the sampled window.

## Judgment

All judgments below are [AGENT].

- Concern: some computed outputs disappeared before storage, as the later [publication investigation][publication] established. A passing numerical comparison does not establish that every requested output was checked.
- Concern: the entire workflow has not been exercised under every promised condition. The [product promise][promise], § Scope, records gaps in live testing of research bookkeeping and an integration check. Keep those gaps beside claims about operation by a new user.
- Unresolved uncertainty: the example shows how an investigation produced a better next question. It does not measure how much this improves engineering productivity or investment decisions. Which magnet or heating improvement would be cheapest also remained unanswered by this study.
- Source disagreement: the later narrative assigns all nine feasible points to 110 MW; the administrator counts nine across the complete study. This synthesis follows [the administrator's reading][reading], which also identifies an arm-labeling error.
- Evidence limitation: the four-view order comes from the previous synthesis's OWNER attribution. The original message supplying that outline was unavailable to this fresh agent; this revision preserves the inherited order.
- Suggested spot check: follow the heating comparison from its source citation through generated wiring to a recorded verdict. Then examine the 50 MW rows against both heating and conductor constraints. That tests the mechanism on which this explanation rests.

## Source pointers

The four views remain in their inherited order: end goal, structural setup, behavioral view, worked example. The heading wording and explanatory prose are [AGENT].

The three archived articles and their [close reading][style] informed the opening question, the explanation of parts through their purpose, and the use of one design choice to expose interacting consequences. They are writing references, not technical evidence for this system.

[purpose]: /home/reid/1cfe/fusion-tea/.project/concepts/physical-innovation-narrative.md
[style]: /home/reid/1cfe/fusion-tea/.project/research/20260905_1cfe-writing-style.md
[catalog]: /home/reid/1cfe/fusion-tea/.project/research/20260904-135403_blog-series-topic-catalog.md
[project-guide]: /home/reid/1cfe/fusion-tea/CLAUDE.md
[concept-pipeline]: /home/reid/1cfe/fusion-tea/docs/concept-pipeline/pipeline.md
[codegen]: /home/reid/1cfe/sysml-codegen/docs/architecture/overview.md
[runbook]: /home/reid/1cfe/fusion-tea/work/orchestration/GOAL_RUNBOOK.md
[store]: /home/reid/1cfe/teax/packages/teax-simkit/simkit/study/store.py
[constraint]: /home/reid/1cfe/fusion-tea/models/library/analyses/mfe_viability.sysml:201
[wrapper]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/generated/modules/stellarator_09/stellarissustainmentokconstraintmodule.py:15
[wiring]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:985
[preflight]: /home/reid/1cfe/fusion-tea/scripts/study/preflight.py:333
[example-goal]: /home/reid/1cfe/fusion-tea/work/orchestration/goals/operating-point-closure/goal.md
[prototype]: /home/reid/1cfe/fusion-tea/work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md
[reading]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies/20260901-sustainment-fence/synthesis.md
[previous]: /home/reid/1cfe/fusion-tea/.project/mental-alignment/runs/20260905-135058_harness-pipeline.md
[promise]: /home/reid/1cfe/fusion-tea/.project/product/0001-goal-round-native-operability.md
[publication]: /home/reid/1cfe/fusion-tea/.project/research/20260905-091948_blank-study-column-root-cause.md
[sustainment-impl]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py
