# The full harness: how an AI grows a model without the model going bad

Outline for the Part 3 support of [the main post](fusion-tea-exploratory-modeling.md). Story first, in beats; evidence paths at the end of each beat. `[AGENT]` throughout: this is a proposed telling for owner discussion, not a settled structure. Quotes marked `[OWNER-VERBATIM]` come from the harness concept doc.

## The story in one paragraph

Parts 1 and 2 showed a model that can be executed and swept. Part 3 answers the question that sits behind exploratory modeling: if the point is to grow the model over weeks, with an agent doing most of the growing, what stops the model from quietly going wrong? The answer is a harness. Not a bigger prompt, but a set of small workflows that each own their own records, a thin goal layer on top that decides what to do next and cites rather than restates, and a handful of mechanical checks that refuse work which cannot prove itself. The reader should finish knowing what a round is, where everything lives, and which checks they would trust.

## Beat 1. The problem: the loop worked, but only with its builder in it

- Open with the three moving pieces the reader already has from Part 2: update the model, generate the program, run a study. Each was closed on its own terms.
- The loop had run once by hand. A study found the model had no conductor-field limit and four values with no source. That became a modeling item, a research round, a regenerated package, a resumed study. Every hop worked. Every hop needed the builder to read one artifact, decide, and invoke the next stage.
- The owner's expectation reframes the goal: `[OWNER-VERBATIM]` "for any of the 'study'-looking goals, I FULLY expect the outcome 95% of the time to be 'that doesn't seem quite right, we need to revisit the model'". So the product of a study is usually a model change, and the harness exists to make model changes honest.
- The entropy argument from Part 1, applied here: an agent editing a model for weeks will drift unless the structure pushes back. The harness is the structure.
- Three design goals, from the main post: performance, token efficiency, and staying organized as it grows.
- Evidence: `.project/concepts/goal-driven-model-development-harness.md` (problem statement, owner's words).

## Beat 2. The mental model: native workflows do the work, a goal layer decides

- Give the reader one frame before any detail. Three native workflows, each with its own records, plus one layer above that never does the work itself.
  - **Modeling PM** (`work/`): spec, design, plan, implement, close. Changes the SysML model and regenerates the program.
  - **Research** (`knowledge/`): find a source, capture it, hold-out check it, register it so the model can cite it.
  - **Study** (`exploration/`): pin a package, sweep it, record what responded and what did not.
  - **Goal layer** (`work/orchestration/goals/`): asks a grounded question, runs it in rounds, sends each finding to one of three places (fix the model, find a source, declare a gap), and gets reviewed.
- The one rule that keeps them from disagreeing: the goal layer **cites, never restates**. If a fact is copied into the trail, there are now two copies that can drift.
- The second rule: **files are the memory.** A fresh session must be able to resume from disk. `[OWNER-VERBATIM]` "we MUST design for 'resumes'."
- The third: **criticism is required.** `[OWNER-VERBATIM]` "I have found that criticism is pretty much required to get good results." And the reviewer is never the author's session.
- Figure: the nested picture the main post sketches. SysML models in the middle, then the generated programs and studies, then the knowledge base and PM records, then the goal trail around the outside.
- Evidence: `work/orchestration/GOAL_RUNBOOK.md` § What this is, § The five surfaces, § What "fresh" means.

## Beat 3. The filesystem view: where to find things

- One annotated tree. Keep it to the directories a reader would open, and say for each what question it answers and who writes it.
  - `models/library/` and `models/designs/`: the model. Concept-agnostic definitions versus a specific plant. This is the MR-3 split from Part 2.
  - `exploration/<pkg>/`: the generated program and every study record against it.
  - `knowledge/sources/`, `knowledge/SOURCE_INDEX.md`, `knowledge/KNOWLEDGE.md`: what the model is allowed to cite, and the insights extracted from it.
  - `knowledge/holdout/`: quarantined material the agent must never read. Set up for the Part 4 test.
  - `work/`: the modeling PM's backlog and items.
  - `.project/`: the coding PM for tooling work, and the ADRs that record why the harness is shaped this way.
  - `work/orchestration/goals/<goal>/`: `goal.md`, `trail.md`, `learnings.md`, `evidence/`.
  - `.claude/skills/` and commands: the prompts and runbooks the agent loads on demand.
- Say plainly that two PM systems coexist and never write each other's state. A goal may cite a `.project/` artifact by path and commit digest, and that is the whole interface.
- Evidence: `CLAUDE.md` § Project Structure and § Project Management, `.project/adr/0006-goal-evidence-seam.md`.

## Beat 4. The logical view: a goal, a round, a task

- Define the three words once, in ascending order, then show them as one diagram.
  - A **task** is one bounded objective. It may span several native stages (a research invocation, a modeling item, a regeneration). It has a scope, a start and a return.
  - A **round** is one agent's attempt at one strategy. The strategy is written down first: the approach, its assumptions, the conditions to abandon it, the model increment intended, the study question intended. No task list. If you can list all the tasks, it is a plan, not an experiment.
  - A **goal** is a grounded question, pursued in rounds, with a written definition of what counts as answered, plus stop rules and owner-reserved gates.
- A round is bounded by construction: at most one promoted pin and one committed study. That is what makes two rounds comparable.
- A round closes on exactly one of six triggers: a valid study reading (adverse counts), a strategy blocker, changed comparison meaning, an unresolved owner gate, a declared limit, or the goal answered. An honest empty round is a result.
- Who touches what: the round agent appends to the trail; a fresh session reviews; the owner holds merge, push, close and every reserved gate. `[OWNER-VERBATIM]` (stops) "generally when there are major decision points. with a focus on intent."
- Figure: goal → round (strategy) → tasks → native workflows → study reading → dispositions → review → learnings → next round.
- Evidence: `GOAL_RUNBOOK.md` § Opening and closing a round, § Running one task; ADR-0001, ADR-0002.

## Beat 5. One round, walked

- Use a real thread the main post already mentions so the reader sees the same story from inside the machinery: the heating gap on the Stellaris design point.
  - Study said the paper's design point needed 90.6 MW of heating against 50 installed.
  - Round strategy: the gap is in how helium ash is shaped in the plasma.
  - Tasks: research (find the sourced relationship), modeling item (change the calculation, regenerate, recapture snapshot), integration check, re-run the study.
  - Reading: 49.08 MW, on the boundary, nothing tuned. Round closes on a valid reading.
  - Dispositions: the re-run showed most feasible points were ignited plasmas the model could not hold. That became the next goal and a new constraint.
- Show the trail entries as they actually look: `## Round N`, `### Strategy revision`, `### Round N result`, and the disposition rows. A few lines, not the whole file.
- Point at the evolution viewer for what the model looked like before and after. This is the hinge to Part 4.
- Evidence: `work/orchestration/goals/stellaris-plasma-power-balance/` and `work/orchestration/goals/burn-control/` (confirm which goals carry this thread before drafting), `work/narratives/`.

## Beat 6. Research and ingestion: a source is a thing you can prove you have

- The problem: an agent that cites from memory is worse than one that cites nothing. Every number in the model must resolve to a file in the repo (MR-4).
- The seam between "we need to know X" and "the repo now contains evidence about X" has one writer. The registry script captures the source, checks it against the hold-out list, and commits the source directory, manifest row and index block together, or leaves the repo untouched.
- A source's durable identity is the SHA-256 of its raw bytes as fetched (ADR-0008). Say why in one line: a URL moves, a hash does not.
- A research run returns one of four classes, and two of them are answers rather than failures: registered, bounded negative, operator queue, blocker. "Found nothing usable" is recorded as a result so nobody searches for it again.
- The hold-out check is what made the Part 4 test possible. Mention it here, explain it there.
- Evidence: `docs/research_seam_operator_guide.md`, `scripts/source_registry.py`, `knowledge/holdout/aries-cs/PROTOCOL.md`, ADR-0008.

## Beat 7. The modeling PM: a recap, not a re-explanation

- Keep this short. The reader does not need the whole spec-design-plan-implement pipeline; they need to know it exists, what it produces, and where the harness leans on it.
- What a modeling item produces: a changed model, a regenerated program, a recaptured snapshot, a re-pinned manifest, and a work record that the goal trail cites.
- Validation levels the item runs before closing (name the six levels, one line).
- The design-choice rule (MR-7) belongs here because it is the rule the ARIES false start violated: evaluate the equipment the designer supplied, never silently size it from demand. One sentence on why that matters for a study.
- The September right-sizing: reviews and stage documents became risk-triggered rather than mandatory, with bounded reviewer budgets. Worth a sentence because it is the harness correcting its own overhead, and it feeds the "left behind" figure.
- Evidence: `CLAUDE.md` § Modeling PM, `modeling_project/MODELING_PROCESS.md`, `modeling_project/REQUIREMENTS.md` (MR-4, MR-7), `.project/active/harness-right-size/report.md`.

## Beat 8. The checks that keep it honest

- Frame: the harness has many prose rules and a few mechanical ones. The mechanical ones are the ones a reader should trust, so name them and say what each refuses.
  - **The integration seam proves, it does not perform.** It regenerates the package in place and demands zero moved bytes, recaptures the snapshot and demands the tracked file back, recomputes the pin and demands the recorded value. Ten gates in order; stops at the first failure. A refusal means the modeling item is not finished (ADR-0009: integration is a fixed-point proof).
  - **The study fails closed on mechanical conditions only.** A missing key, a fingerprint mismatch, a dirty package stop the study. A result that looks wrong never does; it is recorded and argued.
  - **Indicator vocabulary is fixed.** "No constraint response" is a sound negative. "Constraints reachable" is a possible path, never a claim. "Unresisted" is the agent's judgment, never a tool output. This is how a study avoids overclaiming.
  - **Citations resolve.** Every quantitative value carries a source that resolves to a repo path.
  - **The critic is never the author's session.** Fresh review at the disposition checkpoint and at round close (ADR-0005).
  - **The owner holds the gates.** Merge, push, close, archive, and every scientific decision the goal reserved.
- Close the beat with the honest limit: these checks establish that the program is the model and the arithmetic is right. They do not establish physical realism. That distinction carries into Part 4.
- Evidence: `docs/integration_seam_operator_guide.md`, `.claude/skills/run-study/runbook.md`, `modeling_project/STUDY_POLICY.md`, ADR-0005, ADR-0009.

## Beat 9. What it cost, and what we would change

- The "left behind" figure from the main post: repo size over time, colored by actively used versus superseded. Say plainly that the harness accreted and was trimmed, and that lean-first persistence (ADR-0003: prose files first, harden only on an observed failure) was the rule that kept the trimming possible.
- What we would do next, as a short list rather than a roadmap:
  - Token cost per round, measured rather than felt.
  - The DAG limitation from Part 2 surfaces here as a harness problem too: coupled systems need a numerical solver stage the round agent can dispatch.
  - Running a goal end to end by a person who did not build the repo. Success criterion 1 of the concept has not been demonstrated by a stranger.
  - Fewer, sharper checks. The right-sizing was a first pass.
- Hand off to Part 4: the harness is the thing under test in the demo, not just the model.
- Evidence: ADR-0003, `.project/active/harness-right-size/report.md`, the concept's success criteria.

## Questions for the owner

1. Is the helium ash round the right one to walk in Beat 5, or is there a round with a cleaner research → model → study sequence?
2. How deep should Beat 7 go on the modeling PM? The Part 1 blog post may already cover enough of it.
3. Beat 9 "what we would change": keep it here, or move it entirely to Part 5 of the main post?
4. Two figures proposed (nested circles in Beat 2, the round loop in Beat 4). Is the filesystem tree in Beat 3 a third figure or a code block?
5. Should the token and repo-size numbers be gathered now, so the figure is real before drafting starts?
