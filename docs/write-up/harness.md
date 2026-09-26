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

The main post describes exploratory modeling as a cycle: build a rough design, evaluate it, refine it, and go again. Inside that cycle an engineer does three recurring things: finds out what is known about the system, changes the model to reflect it, and evaluates the model to see what it now says. The harness treats each as a class of work with its own tools, prompts and record, and a person can run any of them on its own.

**Research** answers "we need to know X." Agents search and triage candidate sources, but one script does all the writing into the knowledge base. Given a URL or a PDF and three sentences about what the source is for, how to check its numbers, and what limits its authority, it captures the source, checks it against the quarantine, and commits the extraction, a manifest row and an index entry together, or writes nothing at all (`docs/research_seam_operator_guide.md`). A number in the model can then cite a page in the repository, and a search that found nothing is recorded so nobody runs it again.

**Model updates** change the SysML v2 in an organized way. Before an edit, the agent writes down what will change, which definitions and consumers it touches, and what source the change rests on. Then it makes the change, regenerates the program, and records the result so a reviewer can check the change against what was intended rather than only whether the numbers moved the right way. The stages that exist for this (spec, design, plan, implement, review) can be brief or skipped when the change is small, but the evidence obligation does not shrink with the stage count (`modeling_project/MODELING_PROCESS.md`).

**Studies** probe a generated program after codegen. A study runs against one pinned version of the generated program, sweeps inputs, and records what pushed back, what did not, and what the agent judges that to mean. It stops only on mechanical faults, never on a result that looks wrong; a surprising result is recorded and argued, not suppressed (`.claude/skills/run-study/runbook.md`). Part 2 covered the machinery; here the point is that a study is a bounded unit of work with a record that a later session can read cold.

| Class | Deterministic tool | Agent prompt | Record |
|---|---|---|---|
| Research | `scripts/source_registry.py`, `scripts/research_seam.py` | `/research-acquire` | `knowledge/sources/`, `knowledge/SOURCE_INDEX.md`, `knowledge/research/requests/` |
| Model updates | the modeling PM CLI, codegen, the six-level validator | `/spec-model` through `/implement-model`, `/quick-model` | `work/active/WI-NNN/`, then `work/completed/` |
| Studies | TEAx, the study record template and its checks | `/run-study` | `exploration/<pkg>/studies/<study-id>/` |

### The outer loop

A user can manage research, model development and studies directly, and that was our initial mode of operation. For the Stellaris demo we wanted to test whether the AI could take on larger chunks of work. The primitive we settled on is the **goal**.

What makes a goal different from a task is the shape of the uncertainty:

- We start with a clear motivation. There is a specific question, and we know what an answer would look like.
- We do not have a known series of actions to take. The next step depends on what the last one found.
- The total amount of work is not set. It might be one study, or it might be three model changes and some research.

A plan cannot carry that, because a plan lists the actions in advance. What can carry it is a fixed question, a bounded attempt at a time, and a record of each attempt that the next one builds on. Figure 1 shows that structure, and the rest of this section walks it from top to bottom.

![A goal at the top: a question and what would count as answering it, fixed while it runs. Below it, a round run by the AI: an approach, then tasks one at a time, with research and model changes before the model is pinned and studies after, ending in a record. Below that, a review by someone who did not do the work, then the owner: if the goal is answered it closes; if not, the next round opens with a revised approach.](harness-assets/goal-loop.png)

*Figure 1. One goal, pursued in rounds. Inside a round, the pin divides the tasks: before it the model can change; after it the model is fixed and studies run against it. The only path from one round to the next runs through the review and the owner. Rendered by `harness-assets/render_goal_loop.py`.*

**The goal is written first** Before any work starts, the owner and an agent write the goal (`work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal). It carries:

- the question, in one sentence, and who is asking;
- what would count as answered, concrete enough that two people would agree;
- the invariants a comparison must preserve, so a later round cannot drift the meaning of "better";
- the evidence already in the repository, so a round is not spent on a question already answered;
- the limits on rounds and retries, and the decisions the owner keeps.

The goal is not changed as it executes. 

**A round is one bounded attempt at the question.** It opens with an approach: the agent's bet on how to answer the question, what that bet assumes, what would make the agent abandon it, and what model change and study it expects to need. The approach carries no task list, because a list written before the evidence arrives is authority granted in advance (`.project/adr/0001-strategy-and-task.md`).

**The round then works through tasks one at a time.** Each task is a piece of research, a model change or a study, carried out through that class's own workflow. It gets a written scope before it starts and a written return when it finishes, and that return feeds the decision on what to do next. This is how the agent follows the evidence without a plan.

**A round pins the model at most once.** That limit keeps rounds bounded. When the round's model changes have landed, codegen regenerates the program and the round pins that exact version. Any and all studies then belong to one known version of the model and can be compared with earlier ones. Learnings from the studies inform the next round.

A round can also stop early, for example when the premise of its approach proves wrong or it hits a declared limit. Either way, it ends by writing down what it tried, what it found and why it stopped.

**Nothing builds on a round until it has been checked.** Two checks sit at the boundary between rounds. Before any follow-up acts on a study's reading, the reading and the proposed dispositions (what will be done about each finding) are checked. After the round closes, a fresh reviewer, one who did not do the work, walks the record against the cited evidence: did the round pursue the approach it declared, did each task stay in scope, did every finding it touched get its disposition, and is the proposed learning right (`.project/adr/0002-round-boundary.md`, `.project/adr/0005-review-topology.md`).

**Then the owner decides whether the goal is answered.** If it is, the owner closes it. If not, the next round opens with a revised approach that starts from what the last round found.

That gives three roles. The owner sets the question and holds the gates: merges, closures, and the scientific calls reserved in the goal. The round agent pursues one approach and writes the result. The fresh reviewer checks it (`.claude/skills/run-goal/SKILL.md`). A human or an agent can take any of the three, and the runbook is the same document for both.

The reader can now place any piece of the harness: it is a tool, a prompt, or a record belonging to one of the three classes, or it is part of the loop that decides which class to call next. The next section shows where each of those lives on disk.

## 3. Where everything lives

Agent sessions keep no memory between them, so the work carries forward only through the repository. A new session has to find what earlier sessions wrote and be able to trust it. We divide the repository into a few areas, one for each part of the harness described in section 2, and organize every area the same way so that a session knows how to find and add to any of them.

Each class of work from section 2 writes to its own areas, the goal loop has one, and the harness itself has one:

- **Sources** (`knowledge/`) hold what research finds. Every number in the model cites a file here. One directory, `knowledge/holdout/`, is quarantined for the test in Part 4: agents are told never to read it, and the registration script refuses anything from it.
- **The model** (`models/`) is the SysML v2 description of the plant. Model updates are the only work that changes it.
- **The program and studies** (`exploration/<pkg>/`, one directory per generated package) hold what is generated from the model and what runs against it: the program codegen writes (Part 2), the pin that fixes which version of it a study uses, and the study records.
- **Work items and modeling rules** (`work/`, `modeling_project/`) record each model update from its spec to its evidence, along with the requirements every update must meet.
- **Goals** (`work/orchestration/`) hold the outer loop's records: the goal, the trail of rounds and the accepted learnings. A trail cites records in the other areas instead of holding results of its own.
- **The harness** (`.claude/`, `.project/`) holds the agent prompts and the engineering of the harness itself, including the decision records behind the goal loop.

We reuse similar patterns across these components: an index file where a session starts, a tool that adds entries so they keep their structure, and a record that keeps the history of changes. `CLAUDE.md` at the root points to each area's index.

**Indexes.** Each area has one file where a session starts, and that file points to the rest. A session looking for the source behind a number reads `SOURCE_INDEX.md`, which says what each source is for, how to check its numbers and what limits its authority. A session resuming a goal reads `goal.md` and then the trail. A session can therefore find what it needs by following references from `CLAUDE.md` instead of searching the repository.

**Write tools.** Where a record needs a strict structure, agents add to it through a tool instead of editing the file. In round 1 of the goal in section 4, a research request found two papers, and `source_registry.py` registered each one by writing its extraction, its manifest row with the hash and its index entry in one step. If any part had failed, it would have written nothing. The model and the goal records have no write tool, for different reasons. The model's structure comes from SysML itself: the language fixes what a model can say, and the validator checks each change. We built the goal records as plain files with written rules and add a tool only when a real run shows a written rule failing (`.project/adr/0003-lean-first-persistence.md`). So far their templates and fixed headings have been enough.

**History.** Each area keeps a record that later work can rely on, and entries are added to it rather than edited. The trail is only appended to, and a correction is a dated amendment that names what it corrects. A committed study record is not changed. A finding's first sighting in the discovery log stays as written, and later rows record what was done about it. A new session can therefore read an old record and know it describes what happened at the time.

Three further rules apply across all the areas.

- Records refer to each other by path instead of copying. A number in the model cites a file in `knowledge/sources/`, and a goal's trail cites a study's directory instead of restating its results. Each fact has one home, so a correction cannot leave two versions that disagree.
- The status of a piece of work is read from its files, not stored separately. We avoided separate status fields because they drift out of step with the records they describe (`work/orchestration/GOAL_RUNBOOK.md` § Opening and closing a round).
- Searches that found nothing are recorded with the queries that were tried, and a round that ends without a result still writes one. A new session can see that the ground was already covered.

Table 1 shows how each area implements the pattern.

*Table 1. The areas of the repository and the pattern each one follows.*

| Area | Index | Write tool | History | Key rule |
|---|---|---|---|---|
| **Sources** `knowledge/` | `SOURCE_INDEX.md` | `scripts/source_registry.py` registers a source; `scripts/research_seam.py` tracks a research request | `MANIFEST.jsonl`; `research/requests/`, including searches that found nothing | A fetched source is identified by the hash of its raw bytes, and a changed source is refused |
| **Model** `models/` | `README.md` | None. Agents edit the SysML; the language and the six-level validator hold its structure | The work item behind each change | Reusable definitions and design values are kept apart, and every number cites a source (MR-3, MR-4) |
| **Program and studies** `exploration/<pkg>/` | `studies/ANNEX.md` | Codegen writes the program; `scripts/integrate.py` accepts a pin; each study fills a record template that `tests/study/` checks | Each committed study record; `studies/DISCOVERY_LOG.md` | A pin is accepted only if regenerating the program from the model changes nothing, and a committed record is never edited |
| **Work items and modeling rules** `work/`, `modeling_project/` | `work/BACKLOG.md`, `modeling_project/REQUIREMENTS.md` | `agentic-mbse pm` operations add and close items, promote requirements and register decisions | `work/completed/` | A work item's stage is read from which of its files exist |
| **Goals** `work/orchestration/` | `GOAL_RUNBOOK.md`, then each goal's `goal.md` | None. Templates with fixed headings | `trail.md`, append-only; `learnings.md` | Whether a round is open is read from the trail's headings |
| **Harness** `.project/`, `.claude/` | `.project/CURRENT_WORK.md` | None | `.project/completed/CHANGELOG.md`; decision records in `.project/adr/` | Changes to the harness are tracked apart from changes to the model |

<details>
<summary>Directory tree of the areas above, with the goal from section 4 as the example</summary>

```text
fusion-tea/
├── CLAUDE.md                        the first file every session reads; it points to everything below
├── models/                          the SysML v2 model
│   ├── library/                     reusable definitions: components, calculations, cost accounts
│   └── designs/stellarator_09/      the Stellaris design: its values and its design choices
├── exploration/stellarator_e2e/     what is generated from the model, and what runs against it
│   ├── models/                      a copy of models/ that codegen reads; a test fails on any difference
│   ├── generated/                   the generated program (Part 2)
│   └── studies/
│       ├── manifest.json            the pin: fingerprints of the program version studies run against
│       ├── DISCOVERY_LOG.md         every finding a study sighted, and what was decided about it
│       └── 20260905-stored-energy-basis/    one study record: plan, results, synthesis
├── knowledge/                       what the model's numbers cite
│   ├── sources/                     one directory per registered source: extracted text, page images
│   ├── MANIFEST.jsonl               one row per source, with the hash that identifies it
│   ├── SOURCE_INDEX.md              what each source is for, how to check it, what limits it
│   ├── research/requests/           research requests (REQ-W-01.json); negatives/ records searches that found nothing usable
│   └── holdout/                     quarantined: never read
├── modeling_project/                the modeling rules: requirements, modeling process, study policy
├── work/                            the modeling records
│   ├── BACKLOG.md                   the work item list, changed only through the modeling PM's commands
│   ├── active/                      work items in progress
│   ├── completed/20260906_WI-042_sourced-helium-ash-profile/    one closed work item: spec, design, plan, evidence
│   └── orchestration/
│       ├── GOAL_RUNBOOK.md          how to run a goal, for a person or an agent
│       └── goals/stored-energy-basis/    goal.md, trail.md, learnings.md, evidence/
├── .claude/                         agent prompts: commands (/spec-model, /research-acquire), skills (run-goal, run-study)
├── scripts/                         deterministic tools: source_registry.py, research_seam.py, integrate.py
└── .project/                        the engineering of the harness itself, with its decision records in adr/
```

</details>

The next section follows one goal through these areas, from a discrepancy in a single number, through a research request and a work item, to a re-run study.
