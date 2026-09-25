# Part 3: The full harness

Supports [the main post](fusion-tea-exploratory-modeling.md). Part 2, [turning a SysML model into a calculator](sysml-codegen-model-evaluation.md), covers evaluating one version of the model; this part covers everything around it.

## 1. The problem: engineering work that has to build on itself

We want an AI to do engineering work the way a small team does it over weeks: research a system, model it, run studies against the model, find what is wrong, fix it, and go around again. Part 2 showed how a study evaluates one version of the model. This part is about the rest of the loop: how the model gets its numbers, how it changes, and how anyone can tell whether a change was right.

The hard part is not any single session. A session with a good prompt does good work. The hard part is that every session starts from what earlier sessions wrote down, because that is all it has. The model, the sources, the study records and the decisions are the memory of the whole effort, and an agent's own context is gone when its session ends.

AI has inherent entropy. Left to its own devices, a modeling environment goes the way an unattended codebase does: it becomes chaotic and incomprehensible, which is what people mean by slop. Fighting that entropy is the job of the harness. The aim is a closed system that is never deterministic but stays predictable over time. Some of the problems it has to solve:

- Avoid multiple, conflicting sources of truth. The first study run under the study tooling found four values in the model with no source anywhere in the repository (`.project/research/20260822-120756_research-extraction-harness.md`). An agent that needs a value and cannot find one will supply a plausible one from memory, and the next session reads it as a fact.
- Keep work continuous across agent sessions, so that a fresh session can pick up where the last one stopped without redoing or undoing it.
- Keep intent consistent, so that agents working on one piece do not lose the forest for the trees.
- Hold the level of performance as the system grows in volume. That takes an architecture and a set of patterns that an agent, or a person, can still read and understand.

Part 1 argued that SysML v2's strict semantics help protect the model from this kind of entropy: the language fixes what a model can say and how, so an agent cannot redefine the semantics as it goes. But the model is a small part of the record. Nothing in the language protects the research behind a number, the study that found a problem, the decision about what to do about it, or the account of what was actually done.

So what is a harness? For this project it is four kinds of thing:

- Tools that provide deterministic structure: one script registers a source, one operation mints a work item, one pipeline regenerates the program from the model.
- Distinct prompts that define process stages, each doing a bounded chunk of work with a defined input and a defined record.
- Other agent prompts and reference material that enforce patterns and behaviors, so that reviewers, critics and rules keep the system in check.
- A file system that keeps everything organized and interpretable, so that anything the process names can be found.

Ours is far from refined. It has not demonstrated full closure over a long horizon, and it grew with need and by trial and error rather than from a design. But some of its techniques have shown promise, and the rest of this part walks through them: how the work sorts into classes, where each class writes its record, and what checks that record before the next session builds on it.

## 2. The mental model: three classes of work, and a loop above them

Before the harness had an outer loop, the full cycle from study to research to model change had run exactly once, by hand. A study found the model had no conductor-field limit and four values with no source. That became a research round and a modeling item, the program was regenerated, and the study resumed. Every hop worked, but every hop needed the person who built the system to read one artifact, decide, and start the next stage, and each hop said "I need X" in a different shape (`.project/concepts/goal-driven-model-development-harness.md`). The harness generalizes that cycle so that an agent can run it, and a second person can check it.

The work sorts into three classes. Each has its own deterministic tools, its own agent prompts, and its own record on disk, and a person can run any of them alone.

**Research** answers "we need to know X." Agents search and triage candidate sources, but one script does all the writing into the knowledge base. Given a URL or a PDF and three sentences about what the source is for, how to check its numbers, and what limits its authority, it captures the source, checks it against the quarantine, and commits the extraction, a manifest row and an index entry together, or writes nothing at all (`docs/research_seam_operator_guide.md`). A number in the model can then cite a page in the repository, and a search that found nothing is recorded so nobody runs it again.

**Model updates** change the SysML v2 in an organized way. Before an edit, the agent writes down what will change, which definitions and consumers it touches, and what source the change rests on. Then it makes the change, regenerates the program, and records the result so a reviewer can check the change against what was intended rather than only whether the numbers moved the right way. The stages that exist for this (spec, design, plan, implement, review) can be brief or skipped when the change is small, but the evidence obligation does not shrink with the stage count (`modeling_project/MODELING_PROCESS.md`).

**Studies** probe a generated program after codegen. A study pins the exact program version it runs against, sweeps inputs, and records what pushed back, what did not, and what the agent judges that to mean. It stops only on mechanical faults, never on a result that looks wrong; a surprising result is recorded and argued, not suppressed (`.claude/skills/run-study/runbook.md`). Part 2 covered the machinery; here the point is that a study is a bounded unit of work with a record that a later session can read cold.

| Class | Deterministic tool | Agent prompt | Record |
|---|---|---|---|
| Research | `scripts/source_registry.py`, `scripts/research_seam.py` | `/research-acquire` | `knowledge/sources/`, `knowledge/SOURCE_INDEX.md`, `knowledge/research/requests/` |
| Model updates | the modeling PM CLI, codegen, the six-level validator | `/spec-model` through `/implement-model`, `/quick-model` | `work/active/WI-NNN/`, then `work/completed/` |
| Studies | TEAx, the study record template and its checks | `/run-study` | `exploration/<pkg>/studies/<study-id>/` |

**Run-goal is the loop above them.** A goal is a specific question, written down with the operator before any work starts: the question in one sentence, who is asking and what they will do with the answer, what would count as answered, the invariants a comparison must preserve so a later round cannot drift the meaning of "better," the evidence already in the repository, how much effort is allowed, and which decisions the owner keeps (`work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal). A goal missing any of those is a draft, and a draft authorizes no task. The goal walked in section 4 was drafted while the owner was away; the agent filled every field, ran one cheap diagnostic as grounding evidence, and then stopped until the owner ratified the question the next day (`work/orchestration/goals/stored-energy-basis/goal.md`).

A goal is pursued in rounds. A round opens by writing one approach: what it assumes, what would make the agent abandon it, what model change it intends, and what study question it intends. It carries no task list. Tasks are chosen one at a time from the evidence in hand, each with a written scope before it starts, because a task list written before the evidence arrives is authority granted in advance (`.project/adr/0001-strategy-and-task.md`). Under that approach the round runs tasks drawn from the three classes, may change the model once and run one study, and records each task's result in the trail.

A round stops for exactly one of six reasons: a valid study reading, including a disappointing one; the premise the approach rested on turned out wrong; the meaning of "better" moved; an owner decision is pending; a declared limit was hit; or the goal is answered (`work/orchestration/GOAL_RUNBOOK.md` § Opening and closing a round). A round may close with no model change and no study. Finding nothing is a recorded result, and that is what makes rounds finite: a round that went nowhere still leaves a record where its hardest judgment was made.

Two checks sit around the round. Before follow-up work builds on a study reading, the reading and its proposed dispositions are checked, by a fresh session when the reading reinterprets a source or changes an interface. After the round closes, a reviewer who did not do the work walks the record against the cited evidence: did the round pursue the approach it declared, did each task stay in scope, did every finding it touched get its disposition, and is the proposed learning right (`.project/adr/0002-round-boundary.md`, `.project/adr/0005-review-topology.md`). "Fresh" means a different session, not a different task: an agent reading its own round with its own reasoning still in front of it is not a reviewer. Then the owner closes the goal, or the next round opens.

That gives three roles. The operator sets the question and holds the gates: merges, closures, and the scientific calls reserved in the goal. The round agent pursues one approach and writes the result. The fresh reviewer checks it (`.claude/skills/run-goal/SKILL.md`). A human or an agent can take any of the three, and the runbook is the same document for both.

The reader can now place any piece of the harness: it is a tool, a prompt, or a record belonging to one of the three classes, or it is part of the loop that decides which class to call next. The next section shows where each of those lives on disk.
