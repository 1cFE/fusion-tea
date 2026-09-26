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

The question is not changed as it executes; any other change is a dated amendment.

**A round is one bounded attempt at the question.** It opens with an approach: the agent's bet on how to answer the question, what that bet assumes, what would make the agent abandon it, and what model change and study it expects to need. The approach carries no task list, because a list written before the evidence arrives is authority granted in advance (`.project/adr/0001-strategy-and-task.md`).

**The round then works through tasks one at a time (or multiple independent tasks run in parallel).** Each task is a piece of research, a model change or a study, carried out through that class's own workflow. It gets a written scope before it starts and a written return when it finishes, and that return feeds the decision on what to do next. This is how the agent follows the evidence without a plan.

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

## 4. A worked example: the stored-energy goal

To show how the loop in Figure 1 works in practice, we follow one goal from its question to its close. The goal investigated why the model's stored plasma energy was 9 percent above the value printed in the Stellaris design paper. It ran two rounds between 4 and 6 September 2026 (`work/orchestration/goals/stored-energy-basis/`).

### Goal

**The discrepancy.** Our model reproduced the paper's power balance to within 4 percent on every term except the energy stored in the plasma.

- The model's stored energy was 9 percent above the paper's. The model integrates assumed density and temperature profiles over the plasma volume and found 551 MJ, where the paper prints 504.65 MJ.
- A small change in stored energy has a big impact on losses. In the model's confinement scaling, the loss by conduction grows roughly as the 2.5th power of stored energy, so a 9 percent excess adds about 25 percent to the loss.
- With higher losses, the design point needed more heating input power. The heating has to make up the loss, and the model said the plasma needed 90.6 MW against the 50 MW the design installs.
- Downstream, the wall load is also impacted, which drives cost.
  - Stored energy sets the confinement time. When the model overstates stored energy, its confinement scaling gives a shorter energy confinement time.
  - Confinement time sets how much helium ash stays in the plasma. Following the paper, the model holds ash for eight times the energy confinement time, so a shorter confinement time leaves less ash.
  - Less ash means more fusion. With less ash diluting the fuel, fusion power comes out higher.
  - More fusion means a higher wall load. The peak wall load scales with fusion power and sets how often the first wall is replaced, which is part of the plant's cost. At the design point it was 4.09 MW/m², just over its 4.05 limit.

Two earlier goals had treated the gap as outside their scope, under an agent-written rule that stored energy is never tuned to match the paper, and no work item owned it.

**The goal.** Before writing the goal, the agent ran a quick check on a copy of the calculation, leaving the model unchanged. It found two things:

- The heating failure depends on the stored energy. With the stored energy scaled down to the printed value, the required heating fell from 90.6 to 37.5 MW, and both the heating and wall-load checks passed.
- The printed value may not be the right number to match. Every reading of the paper's plotted profiles and printed peak values that the agent tried gave 527 to 575 MJ, not 504.65. The paper's printed beta implies 567 MJ.

The agent then wrote the goal around what was still open, and the owner approved it the next day:

- **Question:** what in the model's calculation causes the 9 percent excess, and is the paper's printed value the right number to match?
- **Answered when:** the excess is explained, or bounded where it cannot be explained, and the owner has decided how the model should calculate stored energy.
- **Invariant:** the model's stored energy is never tuned toward the printed value.
- **Owner keeps:** any change to how the model shapes its profiles.

### Round 1: find the paper's definition

The round's approach was to explain the excess without changing the model. It ran two tasks.

*Task 1, research: how does the paper define stored energy?*

- **What it was:** one research request asking what the paper's "total plasma energy" integrates (`knowledge/research/requests/REQ-W-01.json`).
- **Changes:** two sources registered in the knowledge base, a 2021 journal paper and a 2023 doctoral thesis by the Stellaris paper's first author. Both describe the systems code the paper used. Nothing in the model changed.
- **Findings:** the paper's own rules give 518.3 MJ, not the printed 504.65. The sources define stored energy as the thermal energy of the assumed profiles over the plasma volume. With that definition, the paper's rules at its printed peak values also reproduce its fusion power (2711 against 2700 MW) and densities. The model's 9.2 percent excess over the printed value splits into three parts:
  - 5.3 points come from the helium ash, the helium the fusion reactions leave in the plasma. The model gave the ash the fuel's broad profile, while the paper's own rule peaks it in the core, where the fusion happens.
  - 1.2 points come from the profile exponents. The model's were read from the paper's plotted curves, which differ slightly from the values the paper states.
  - 2.7 points lie between the paper's own rules and its printed value, and no source we found explains them.

*Task 2, evaluation: what would the paper's rules mean for the design point?*

- **What it was:** re-run the quick check at 518.3 MJ, and write the round's proposed learnings and its dispositions for the earlier findings this evidence touched.
- **Changes:** nothing in the model. The dispositions were checked before they were recorded and passed on the third submission.
- **Findings:** at 518.3 MJ, a simple scaling estimate put the design point at 51.4 MW of required heating against 50. It still failed the heating check, but by 1.4 MW rather than 40.6, and the wall load passed. That was the number the owner needed to decide whether to change the model.

**How the round ended.** The round then stopped to wait for the owner, because the one thing left was the owner's decision on how the model should calculate stored energy. A fresh reviewer checked the round, raised six precision-level findings, and accepted three learnings with corrections.

**The owner's ruling.** The round offered two options: keep the model and footnote the gap, or change the ash profile to follow the paper's rule. The owner ruled: "we should fix the ash profile (and make sure this scales up for larger stellarators). and I don't want to add the footnote." The printed value was still not a target. The change implements the paper's rule, and the stored energy is whatever that rule gives.

### Round 2: fix the profile and study again

The round's approach was to make the owner's fix as one model change, pin the regenerated program, and re-run an earlier study against it. It ran three tasks.

*Task 1, model change: compute the ash profile from the paper's rule.*

- **What it was:** one work item, carried through spec, design, plan and implementation (`work/completed/20260906_WI-042_sourced-helium-ash-profile/`).
- **Changes:** the ash profile is now computed from the paper's rule at every design point, and the electron density follows from charge balance. Because the shape comes from the rule rather than from an exponent fitted at the paper's design point, it stays valid when a study moves to other machine sizes, as the owner asked. The program was regenerated from the changed model, and nothing was tuned.
- **Findings:** the design point now passes the heating check, by a small margin.
  - Stored energy fell from 551 to 519.9 MJ, and the required heating fell from 90.6 to 49.08 MW against 50.
  - Round 1's estimate had predicted a narrow failure at 51.4 MW. The estimate scaled stored energy alone, while the real change also reshaped the electron density, which moved the density and radiation loss the estimate had held fixed. The net result was a pass by 0.92 MW instead of a failure by 1.4.
  - Fusion power fell 2.7 percent, because the core now holds more ash and less fuel. That brought the wall load under its limit (3.98 against 4.05 MW/m²), and with less electricity produced, levelized cost rose from 313.5 to 322.3 $/MWh.

*Task 2, pin.* The integration check regenerated the program from the model, confirmed that nothing changed, and accepted the pin on its first run.

*Task 3, study: re-run the earlier window at the new pin.*

- **What it was:** a re-run of an earlier study's 6,311-point window against the new pin (`exploration/stellarator_e2e/studies/20260905-stored-energy-basis/`).
- **Changes:** a critique of the study plan changed it before any point ran. The earlier study had dropped its 13 keV rows only because the old profile made them fail the heating check, so the round restored them, for 7,712 points in all.
- **Findings:**
  - Most of the earlier driven points now ignite. The earlier study had classed 681 points as driven, meaning they need some external heating within what the design supplies. At the new pin 510 of them ignite, meaning fusion heating alone exceeds the losses. The model checks only that the plasma needs no more heating than the design supplies, so an ignited point passes the check, but the model does not represent how that burn would be controlled.
  - The cheapest driven point moved to a machine larger and cooler than the paper's design. It sits at major radius 15.7 m, minor radius 2.2 m and 13 keV, at 202.19 $/MWh, on the edge of the minor-radius range the window allowed.
  - The paper's design point sits on the boundary of feasibility. It passes every limit, but the heating check passes by only 0.92 MW, which corresponds to about 1 MJ of stored energy. The paper's own figures for that stored energy range from 504.65 MJ, printed, to 567 MJ, implied by its beta. The earlier result that it needs 90 MW no longer holds, and whether it is feasible cannot be decided from the paper.

**How the round ended.** The study's reading and its dispositions passed their check on the second submission, and the round stopped on that reading. A fresh reviewer recounted the study's numbers with their own script, raised eight precision-level findings that reopened no task, and recommended closing the goal.

**The close.** The owner closed the goal on 6 September and declined to ask the paper's author about the remaining 2.7 points. An answer would not change what the model says, because its 519.9 MJ is already above both the printed value and what the paper's rules give, and the verdict is the same across that range. The ignited points became the next goal, `burn-control`, and the minor-radius edge became the goal after that, `minor-radius`.

Sections 5 to 7 look at three parts of this goal in more detail: the research request that registered the two sources, the work item that changed the model, and the checks that ran before each result was used.

## 5. Research: from a question to a citable source

We want every number in the model to cite a page in a source that anyone can open in the repository. An agent that cannot find a value will often supply a plausible one from memory, and the next session reads that value as a fact. The research workflow therefore separates judgment from writing: agents search for sources and decide which are useful, and one script does all the writing into the knowledge base. We follow round 1's research request from section 4 through each step and the record it leaves.

**The request.** A research request is a small JSON file with the question, who is waiting for the answer, where to look, and how much effort is allowed (`knowledge/research/requests/REQ-W-01.json`).

- The question asked how the Stellaris paper defines its printed total plasma energy and volume averages, and which magnetic field its beta refers to.
- The consumer was the stored-energy calculation in the model.
- The places to look started with the paper's own pages, then its supplementary material, Proxima Fusion's publications, the systems-code papers it cites, and the papers behind its confinement scaling.
- The limits were six searches and three registrations.

**The search.** A research agent ran the search from a written prompt that the round saved first (`work/orchestration/goals/stored-energy-basis/evidence/T-001_REQ-W-01_prompt.md`). The prompt carried the quarantine rules, because the registration script checks for quarantined material only when a source is registered, after the agent would already have read it. A second script, `scripts/research_seam.py`, kept the run's record, and every search and every candidate went into its log with a decision (`knowledge/research/requests/runs/REQ-W-01/`):

- Kept: a 2021 journal paper and a 2023 doctoral thesis by the Stellaris paper's first author, which define stored energy in the systems code the paper uses.
- Rejected: the publisher's page, because the paper has no supplementary data; two Proxima Fusion pages that state no definitions; and a paper on the Helios design, which the quarantine bars, so the agent did not open it.
- Queued for a person: a query to the paper's author, whose paper offers data on request, and the paywalled paper that defines the confinement scaling.

**The registration.** Each kept source goes in through `scripts/source_registry.py`, which refuses to register a source without three sentences: what it is for, how to check its numbers, and what limits its authority. It also records a hash of the file as fetched, so a later copy can be checked against it. For the 2021 paper the three sentences say:

- Use for: its equations (8) to (11) define stored energy as the thermal energy of the assumed profiles over the plasma volume, with no fast-particle term.
- Validation: check the equations on the PDF page, because they exist only as images in the extracted text.
- Caveat: this is the definition in the authors' systems code, not a statement by the Stellaris paper, and it does not settle whether the printed 504.65 MJ is this quantity.

The caveat carried into the goal's learnings, which describe the definition as the authors' systems code's rather than the paper's own.

**The return.** When the run closes, the bookkeeping script computes the result from what landed on disk, not from what the agent reports (`return.json` in the run directory). This run returned `REGISTERED`: two sources registered and citable, and two candidates queued. Because candidates were queued, no negative result was written. A search that still has a named source someone could obtain is not a dead end, so the request stays open to search again. When a search does find nothing, the script writes a negative result listing the queries and candidates, and the same request cannot run again without a stated reason.

**What the model cites.** The model's stored-energy calculation now cites both sources by their repository paths (`models/library/analyses/mfe_plasma_sustainment.sysml:130`). A reviewer can open the page behind the definition, and the index entry tells them what to check and what the source does not settle. The queued author query was the owner's to send, and the owner declined it at the goal's close.

Section 6 follows the work item that used this definition to change the model.

## 6. Model updates: the ash-profile work item

Model changes go through work items, each with four stages: a spec, a design, a plan and the implementation, checked by the six-level validation stack. The [earlier post](https://1cf.energy/searching-the-fusion-design-space-systematically/) describes these stages. Here we show one work item, WI-042, which made round 2's change (`work/completed/20260906_WI-042_sourced-helium-ash-profile/`).

**Spec.** The spec turned the owner's ruling into 15 requirements, each with its source and a way to check it. The ones that define the change:

- The ash profile follows the paper's rule at every design point, never a fixed exponent.
- The electron density follows from charge balance.
- Stored energy and beta use the same plasma pressure. Before the change, beta had its own copy of the pressure calculation.
- Nothing else is tuned. The fuel and temperature exponents, the peak values and the stored-energy formula stay as they are.

**Design.** The design predicted every affected result with a prototype calculation before the program was regenerated. It also checked that the fix holds for larger machines, as the owner asked. Across the machine sizes the earlier studies covered, the correction to stored energy ranged from 1 to 23 percent, larger where the machine holds more ash.

**Plan.** Before regenerating the program, the item committed the model edits together with a written account of the eight earlier studies the change affects. None of their stored-energy results can be rescaled, because the change moves each one by a different amount, so the account names a re-run of the most recent study as the update. Writing it first meant it could not be fitted to the new results.

**Implementation.** The rule itself is a few lines of the stored-energy calculation's Python (`exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py`):

```python
# The ash shape: the fusion-rate profile normalised to its peak, S(0) = 1
# (Eq. A.5 pointwise, tau* uniform in rho; WI-042 D1).
def S(u: float) -> float:
    return (u ** (2.0 * alpha_n)) * _sigv_dt(T_i0 * (u ** alpha_T)) / sigv_peak

# ...

# The derived electron profile and its diagnostics (D1).
def n_e(u: float) -> float:
    return 2.0 * n_D0 * (u ** alpha_n) + 2.0 * n_He0 * S(u)
```

Here `u` is 1 − ρ², which falls from 1 at the plasma's center to 0 at its edge, and the fuel density follows `u ** alpha_n`. The fusion rate at each radius is the fuel density squared times the reaction rate at the local temperature, so `S` gives the ash that rate's shape. Before the change, the ash followed the fuel's shape, `u ** alpha_n`. The electron density is then the ions' charge: one electron for each deuterium or tritium ion and two for each helium ion.

The regenerated program matched the design's prediction:

| At the paper's design point | Before | Predicted by the design | Regenerated program |
|---|---|---|---|
| Stored energy (MJ) | 551.4 | 519.9 | 519.9 |
| Required heating (MW; 50 installed) | 90.6 | 49.08 | 49.08 |
| Peak wall load (MW/m²; limit 4.05) | 4.09 | 3.98 | 3.98 |
| Levelized cost ($/MWh) | 313.5 | 322.3 | 322.3 |

- A second implementation of the calculation (`exploration/stellarator_e2e/verify_stellaris.py`), written from the design's equations, agreed exactly. This shows the program implements those equations.
- At the paper's printed peak values, the new calculation reproduces round 1's results exactly, 524.5 and 518.3 MJ. This ties the equations to round 1's research.
- The new program got its own pin, and the earlier study keeps its old one, so each result stays tied to the version of the model that produced it.

**Review.** The round 2 reviewer checked the record against the spec. Only one input value changed, the removed electron-profile exponent, and none of the values the owner had reserved moved. The account of affected studies was committed 27 minutes before the regenerated program.

Section 7 describes the checks that ran along the way and what they caught.

## 7. Checks: code and fresh reviewers

A major challenge in running an AI system over many sessions is catching its errors early, before later work builds on them. An agent can state a number it never computed (a hallucination), misread its own results, or claim more than its evidence supports. To catch these, we use two general classes of checks: checks written as code, which pass or refuse with no judgment involved, and reviews by an agent in a fresh session that did not do the work. Below we describe the mechanisms in each class, each with an example from the stored-energy goal.

**Code checks: is the program the model, and do the numbers reproduce?**

- **Validation levels.** The six levels from the [earlier post](https://1cf.energy/searching-the-fusion-design-space-systematically/) check the SysML itself after every edit, from whether it parses to whether every value cites a source.
- **Integration check.** Before a new version of the program is pinned for studies, a script regenerates the program from the model and confirms that nothing changes. That shows the program the studies will use is exactly the one the current model describes. The script also runs the program at the design point and confirms it matches the reference calculation from section 6 (`docs/integration_seam_operator_guide.md`).
- **Regression tests.** Test suites for the model and the study tools hold the model's expected results, so a change that moves a result fails a test until someone updates it and records why. **Example:** the plan for the ash-profile change listed every place the change had to update, but it missed three study tests. They failed, and that is how they were found.
- **Study checks.** During a study, the program's results are compared with the reference calculation. **Example:** in round 2's study, the stored energy agreed at all 7,712 points.

**Agent reviews: is the reading right?**

- **Critique of the study plan.** Before a study runs, a fresh agent reviews its plan for choices that would make the results misleading. **Example:** when round 2 set out to re-run an earlier study, the critique noticed that the earlier study had dropped its 13 keV rows only because the old profile made them fail the heating check. Under the corrected profile the cheapest driven designs were in those rows, so the plan was changed to include them before any point ran.
- **Recount of the study record.** After a study runs, an agent that did not run it recomputes every count in the written record from the raw results. **Example:** in round 2's study it found seven statements that did not match the data, such as an average cost increase reported as if it held at every point, and one omission. They were corrected in an addendum, and no result changed.
- **Checkpoint on the conclusions.** Before any follow-up acts on a study, a fresh agent checks the study's conclusions and the proposed follow-up against the evidence. **Example:** round 2's reading said the design point was undecided because its heating margin fell inside the paper's 2.7 percent residual. The checkpoint found that this reason pointed the wrong way, because the model's stored energy is above both of the paper's values, and sent the reading back. The corrected reason is the one section 4 gives.
- **Fresh review of the round.** After a round closes, a fresh agent checks it against its approach and scope, re-runs the tests and recounts the numbers with its own scripts. **Example:** round 2's reviewer found a learning that described a 39 percent drop in the amount of ash as "halves", and the learning was corrected before it was recorded.

**What the checks establish.** The code checks show that the model is well formed and that the program computes it correctly. The agent reviews show that the study's design and its conclusions fit the evidence, and on this goal they produced the corrections that mattered.

These checks show that the work is consistent with the model and its sources. They do not show that the model predicts a real plant correctly, which is what the hold-out test in Part 4 is designed to test.

## 8. Where the harness stands

We built the harness so that an AI could carry engineering work across many sessions and have that work build on itself. Our assessment has three parts: the harness is still being refined, it runs our demo's goals almost on its own, and its analysis has been credible but has leaned on a published design to check against. That last part leaves our biggest open question.

**It is still being refined.** We continued to develop the harness as we used it and found issues. Many of those fixes were new rules written into the agents' instructions. As much as possible, moving these prompt-rules into deterministic scripts improves scalability.

**It runs goals almost on its own.** We estimate that about 95 percent of the work on our demo's goals ran without us. The stored-energy goal was an early one, and the owner stepped in at four points: approving the goal, leaving the research decision to the agent, ruling on the fix, and closing the goal. Agents did everything else, including the research request, the work item, the regenerated program and its pin, the 7,712-point study, and six reviews by fresh agents. Later goals needed even less. The four goals that built the integrated ARIES model in Part 4 ran seven rounds between them, and the owner's only input was a written brief at the start and the decision to close at the end.

**Its analysis has been credible, but it has leaned on ground truth.** Many of the issues we caught were found by comparing the model with a published design, such as the Stellaris paper.

**The open question.** Our biggest open question is whether the harness's own checks are enough in a domain with no published design to compare against. The checks in section 7 test the work against the model and its sources, so they do not test whether the model's own assumptions are right. Part 4 describes the hold-out test we designed to probe this: the model was built without the ARIES-CS publications and then compared with them.
