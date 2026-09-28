---
question: |
  I want you to RESUME the $my-mental-model for .project/mental-alignment/runs/20260905-135058_harness-pipeline.md

  I am not happy with the current iteration. For reference, see:
  - .project/concepts/physical-innovation-narrative.md
  - .project/research/20260905_1cfe-writing-style.md
  - .project/research/20260905_1cfe-writing-style-sources/README.md
  In addition to the usual guidance for the mental model. Start a fresh agent to fully revise the synthesis to improve the content and the writing.
date: 2026-09-06 09:01
policy: carried
shape: plain_document
evidence:
  - Owner corrections in the carried conversation, 2026-09-06
  - .project/concepts/physical-innovation-narrative.md
  - .project/research/20260905_1cfe-writing-style.md
  - .project/research/20260905_1cfe-writing-style-sources/README.md and selected passages in all three archived HTML articles
  - .project/mental-alignment/feedback-synthesis.md
  - .project/mental-alignment/runs/20260905-142327_harness-pipeline.md
  - .project/CURRENT_WORK.md and .project/product/INDEX.md
  - CLAUDE.md
  - .project/product/0001-goal-round-native-operability.md
  - work/orchestration/GOAL_RUNBOOK.md
  - ../sysml-codegen/docs/architecture/overview.md
  - work/orchestration/goals/operating-point-closure/goal.md
  - work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md
  - exploration/stellarator_e2e/studies/20260901-sustainment-fence/synthesis.md
code_inspected: "Sustainment constraint and calculation definition in models/library/analyses/; generated constraint module, pipeline wiring, and maintained plasma_sustainment_impl.py in exploration/stellarator_e2e/generated; scripts/study/preflight.py run_gates; ../teax/packages/teax-simkit/simkit/study/store.py StudyStore construction and compatibility checks. Exact links appear in the appendix."
limits: "No tests or calculations run. The worked example uses the September 1–2 investigation and its administrator's recount, not the current model. Later stored-energy work is acknowledged from CURRENT_WORK, not independently reviewed. Code inspection checks representative structure, not the entire compiler or runtime. No hold-out sources examined."
---

# Investigating routes to cheap fusion

## TLDR

- The 1cfe project surveyed 38 fusion concepts and estimated their electricity costs using a common framework. It now aims to identify corridors to 1 cent/kWh: combinations of design choices and technology improvements that could reach that target.
- A promising improvement can create another engineering problem. Stronger magnetic field can help retain plasma energy, but the magnet's conductor must tolerate that field. A plant model connects these effects so an engineer can examine the whole tradeoff.
- Engineers need to revise those relationships as they learn, then calculate the consequences across many candidate designs. The harness supplies agents with the research, editing, calculation, and review tools to conduct that investigation.
- Agents use the results to choose the next task: seek better evidence, change the model, or evaluate another set of designs. They record the reasoning so another agent can review it or continue the work. The owner decides when the question is answered.
- A September 1–2 stellarator investigation found that its modeled machine could not meet both heating and conductor limits at the sampled 50 MW heating settings. That historical result directed further investigation toward the conductor and heating system; it was a next engineering question, not a demonstrated route to 1 cent/kWh.

## 1. Corridors to 1 cent/kWh

What would have to be true for fusion electricity to cost 1 cent/kWh? The 1cfe project began by surveying 38 fusion concepts and comparing their estimated electricity costs through the common 1costingFE framework. The next ambition is to identify corridors to that target: combinations of design choices and technology improvements that could make such cheap power possible.

Consider a stronger magnet. A stronger magnetic field can help the plasma retain its energy, reducing the heating needed to sustain it. But the conductor inside the magnet must tolerate the increased field. We need to know whether a proposed magnet improves the plant enough to justify what it demands of the conductor. Buying more heating instead presents another tradeoff: the plant consumes more electricity that it could otherwise sell.

To answer that kind of question, an engineer needs to connect evidence about individual components to calculations of the whole plant. Those connections form a model: a description of the machine's parts, the equations governing their behavior, and the limits they must satisfy. Changing the magnetic field should change the calculated heating requirement and test the conductor limit. Varying those choices across candidate designs is a study. Its results show where the modeled plant works, what it costs, and which limits prevent further improvement.

The SysML-driven framework discussed here is a proposed route to corridor identification, tested on stellarator designs. It equips AI agents to assemble engineering evidence, build these models, and investigate the results. The harness is the combination of tools, instructions, and work records that supports that investigation. Its value would be better decisions before building hardware: which concepts deserve investment, and what a technology demonstration must establish for a promising corridor to hold.

Source and authority: [OWNER] project progression and corridor target, supplied in the September 6 corrections; [OWNER] investment and demonstration purpose in [the narrative concept][purpose], §§ 1–4. The explanation of models and studies is [AGENT]; the magnet example is grounded in the historical investigation in § 5.

Visual cue: follow a stronger magnetic field into lower heating demand and a higher burden on the conductor, then connect the resulting design choices to electricity cost.

## 2. Adding the missing physics

An investigation will often reveal that the model is missing a relationship. The stellarator model once charged for stronger magnets without accounting for how stronger field helps retain plasma energy. Searching that model could not reveal the tradeoff just described. The engineer first had to add the missing physics.

Textual SysMLv2 gives engineers and agents a language for making such changes. A model can name the plasma, magnets, and heating equipment; define their calculations; and connect a calculated output to another component's input. The plant description lives in text files, so an agent can inspect it, edit it on a branch, and present the change for review. In this project, `fusion-tea` holds the fusion models and their supporting evidence. `agentic-mbse` supplies research and modeling workflows for developing them.

The harness supports branching, exploration, and rapid iteration in these textual SysMLv2 models. Automating model development brings familiar software-engineering challenges: delivering scoped tasks, maintaining good architecture, and fighting generated slop. Because the models abstract real physics and engineering, their authors must be especially vigilant against hallucinations. An invented equation can execute correctly while giving a false account of the machine. Research citations, calculation checks, and separate review address different parts of that problem.

Source and authority: [OWNER] the software-to-systems progression, September 6 corrections. [INHERITED] repository responsibilities in [the project guide][project-guide], Project Structure and Modeling PM; [INHERITED] the missing confinement relationship in [the historical goal][goal], Consumer. The explanatory rationale is [AGENT].

Visual cue: show a small model change that adds the field-to-heating relationship, with a source citation attached and the affected plant calculations highlighted.

## 3. Running the plant calculations

Once the relationships are represented, an engineer can ask what happens at a particular set of design choices. How much heating does this plasma require? Can the installed equipment supply it? Does the conductor tolerate the resulting field? What electricity cost follows? Answering requires executing the calculations in dependency order and checking their results against the modeled limits.

`sysml-codegen` translates the SysML model into a Python package and wires its calculations together. It translates supported expressions directly, including the comparison of required and installed heating. For the numerical calculation of required heating, the agent declares the inputs and outputs in SysML, documents the equations there, and implements the calculation in maintained Python. Adding physics can therefore mean editing both the plant description and its Python implementation.

TEAx runs the resulting calculations and comparisons. The heating check reports whether the requirement is met, along with the values and margin. A design can therefore return an electricity cost and still fail the heating requirement. The engineer needs both results to judge it.

A study repeats this evaluation across selected inputs, such as magnetic field, plasma density, and heating capacity. Before execution, the study records the exact package version, checks that the selected inputs exist, and confirms that the reference design reproduces its recorded results. Holding that version fixed makes differences between candidate designs interpretable: the inputs changed, while the equations stayed the same. TEAx stores execution evidence; the study retains results and a written interpretation for subsequent review.

Source and authority: [INHERITED] implemented architecture in [the codegen overview][codegen], opening and Data Flow, and [expression compilation][expressions], What This Module Does. [Observed code] the [SysML heating constraint][constraint], [required-heating definition][sustainment], [maintained calculation][implementation], [generated comparison][wrapper], [input wiring][wiring], [study preflight][preflight], and [TEAx storage][store]. Reasons for the division are [AGENT].

Visual cue: follow the heating requirement from SysML through the generated comparison to one recorded design result; then show the same calculation repeated at several inputs.

## 4. Agents choose the next task from the results

A study answers questions within the model it was given. It cannot decide whether a missing relationship made the question misleading. That judgment belongs to the engineer and the agents conducting the investigation. They may need better source evidence, a different equation, or another study before recommending a hardware change.

The operator begins with a goal: a question, the evidence already available, and a concrete condition for calling it answered. A goal agent proposes an approach and chooses one scoped task at a time. A task might research a conductor limit, add a heating calculation, prepare the executable package, or run a study. The agent uses the relevant workflow and tools, examines what came back, and chooses the next task from that evidence. If the approach rests on a failed assumption, the agent records why it must change.

The records make this reasoning available beyond one conversation. The goal file preserves the question and answer conditions. A trail records tasks and decisions, with links to the actual research, model changes, and study results. A later agent reads those files to continue the investigation and checks the underlying artifacts to establish what completed. Reviewed learnings preserve what the investigation established.

Separate agents challenge the interpretation and the work. Before proposed follow-up actions proceed, a reviewer checks whether they follow from the study's evidence. When the agent finishes pursuing an approach, a reviewer examines the tasks it completed and the conclusions it proposes to retain. The operator brings in these reviewers, each from a session that did not do the work, and the owner decides whether the goal is answered.

[Dropdown: What does `/run-goal` do?] It gives an agent the instructions for conducting this process. The agent reads files, calls tools, and writes results during its session. Persistent files carry the investigation between sessions; the command itself is not a continuously running service.

Source and authority: [INHERITED] operating contract in [the goal runbook][runbook], The five surfaces, What “fresh” means, Running one task, and The fresh review. The distinction between evaluating inputs and reconsidering the model is [AGENT].

Visual cue: show one task returning evidence to the goal agent, the next-task decision, and the operator's handoff to a fresh reviewer. Place the files each participant reads or writes beside that interaction.

## 5. The stellarator's heating problem

The September 1–2, 2026 investigation put this process to work on the missing magnetic-field benefit. The initial approach tried to calculate the temperature at which the plasma would settle, with heating balancing energy losses. The prototype found no such stable temperature within that version of the reference machine's engineering limits. It also showed that small errors in the power balance could produce large changes in the calculated temperature. The agent stopped this approach before carrying it into the production model.

The agent could still calculate a useful engineering requirement: at a chosen temperature and density, how much external heating would the plasma need after accounting for heating from fusion itself? This gave the study a quantity to compare across designs even when the previous calculation could not find a stable temperature. Comparing required heating with installed capacity tested whether the machine could supply enough power; it did not establish that the plasma would remain at the chosen temperature. Stronger field could now reduce the heating requirement while increasing the field experienced by the conductor, so the study could examine where both limits were met.

Measurement: at 50 MW delivered to the plasma, none of the 154 field-and-density cases, including the reference design, passed all the modeled limits. Every case that met the heating requirement exceeded the conductor's peak-field limit. Increasing delivered heating to 110 MW produced cases that passed those limits in the tested window. These are results from that historical model and sampled range; subsequent investigations have revised its physics assumptions.

The result gave the owner a concrete next choice: investigate conductor capability or the heating system. The owner directed follow-up work toward both. The study had shown one way to meet the modeled limits with more heating, but it had not varied conductor capability and could not say which improvement would be cheaper. The next comparison could ask how much conductor capability would avoid the extra heating, and whether that magnet would cost less than the larger heating system and the electricity it consumes.

[Dropdown: Did this identify a corridor to 1 cent/kWh?] No. It identified an obstacle and useful next investigations in one evolving stellarator model. Reaching the cost target would require further improvements and evidence that the modeled relationships describe the hardware.

Source and authority: [EXAMPLE] the [goal][goal], Amendments; [prototype findings][prototype], Blocking findings and Consequence; and [study administrator's recount][reading], Findings carried forward and What the record does not support. The goal's original question and approach were [AGENT] under owner delegation; the follow-on choices and close were [OWNER]. Later model revisions are recorded in [current work][current].

Visual cue: show the change from solving temperature to calculating required heating, then the competing heating and conductor limits at 50 and 110 MW. Use the historical study's results, label the sampled region and date, and distinguish a feasible modeled case from a demonstrated machine.

## Judgment

All judgments here are [AGENT].

- The historical example demonstrates useful feedback between research, model changes, and calculations. It does not measure an improvement in engineering productivity or demonstrate a corridor to the cost target.
- The heating numbers depend on the physics representation. Subsequent stored-energy work changed that representation, as the current-work record reports. The September 1–2 results should illustrate the investigation at that time, not prescribe today's heating requirement.
- Some internal heating quantities in the historical study came only from the checking calculation's own export. The study administrator disclosed that they were not independently verified. A numerical agreement claim must retain that limitation.
- The product's documented operating promise still lists gaps in live testing of research bookkeeping and an integration check. The runbook explains intended operation; those gaps prevent treating every described route as equally demonstrated. See [the product promise][promise], Scope.
- The prior synthesis disagreed with the study administrator about the allocation of feasible cases among study arms. This version uses the administrator's recounted 50 MW result and its supported statement that feasible cases exist at 110 MW, without carrying the disputed allocation.
- A useful spot check is to trace required and installed heating through the model, generated wiring, and a historical verdict. Then inspect the cases that pass heating at 50 MW and confirm that their conductor verdicts fail. That checks the central mechanism and the example's conclusion.

## Evidence and editorial notes

The owner's September 6 corrections establish the project context and the software-to-systems argument. The opening and sequence are [AGENT] editorial choices. The three archived articles are writing references: their introductions establish a question before introducing tools, and the engineering explainer develops component interactions through their consequences. They supply no technical evidence for the harness.

The research and modeling workflow roles were checked in the project guide and runbook. Code inspection covered representative calculation definitions, numerical implementation, constraint wiring, study checks, and storage, not the whole implementation. No tests or calculations were run. Current generated code illustrates the mechanism; the historical study's committed record supplies the September 1–2 measurements.

[purpose]: /home/reid/1cfe/fusion-tea/.project/concepts/physical-innovation-narrative.md
[project-guide]: /home/reid/1cfe/fusion-tea/CLAUDE.md
[codegen]: /home/reid/1cfe/sysml-codegen/docs/architecture/overview.md
[expressions]: /home/reid/1cfe/sysml-codegen/docs/architecture/reference/14-expression-compiler.md
[runbook]: /home/reid/1cfe/fusion-tea/work/orchestration/GOAL_RUNBOOK.md
[constraint]: /home/reid/1cfe/fusion-tea/models/library/analyses/mfe_viability.sysml:201
[sustainment]: /home/reid/1cfe/fusion-tea/models/library/analyses/mfe_plasma_sustainment.sysml:4
[implementation]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py:1
[wrapper]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/generated/modules/stellarator_09/stellarissustainmentokconstraintmodule.py:15
[wiring]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:985
[preflight]: /home/reid/1cfe/fusion-tea/scripts/study/preflight.py:333
[store]: /home/reid/1cfe/teax/packages/teax-simkit/simkit/study/store.py:93
[goal]: /home/reid/1cfe/fusion-tea/work/orchestration/goals/operating-point-closure/goal.md
[prototype]: /home/reid/1cfe/fusion-tea/work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md
[reading]: /home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies/20260901-sustainment-fence/synthesis.md
[current]: /home/reid/1cfe/fusion-tea/.project/CURRENT_WORK.md
[promise]: /home/reid/1cfe/fusion-tea/.project/product/0001-goal-round-native-operability.md
