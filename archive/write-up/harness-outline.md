# Part 3: The full harness

Outline for discussion. Supports [the main post](fusion-tea-exploratory-modeling.md).

1. **The problem.** We want an AI to do engineering work that builds on itself over weeks: research a system, model it, study it, find what is wrong, fix it, repeat. The problem is that every session works from what earlier sessions wrote, and without structure that record degrades faster than it grows.
   - Numbers lose their sources.
   - Documents pile up that nothing uses, and later sessions treat them as truth.
   - Part 1's strict semantics protect the model. Nothing yet protects the research, studies, decisions and process around it.

2. **The mental model.** Three classes of work, each of which a person can run on its own, and an outer loop for taking on bigger chunks.
   - **Research:** find sources, pull them into the repo, organize what they say so every number traces to a page. Agents search and triage; one script does all the writing, so nothing gets in without a hash and an index entry.
   - **Model updates:** write SysMLv2 in an organized way. State what will change and why, change it, regenerate the program, record it so it can be reviewed against what was intended.
   - **Studies:** after codegen, probe the model. Pin an exact program version, sweep inputs, record what pushed back, what did not, and what that means.
   - Each class has its own deterministic tools, agent prompts, and record on disk.
   - **Run-goal** is the outer loop. A goal is a specific question, written with what counts as an answer, what the owner keeps, and how much effort is allowed.
   - A goal is pursued in rounds. A round writes down one approach, runs scoped tasks drawn from the three classes, may change the model once and run one study, and records each result.
   - A round stops for a defined reason: a study reading, a false premise, an owner decision, or an effort cap. Finding nothing is a recorded result.
   - Before follow-up builds on a round, and at its close, an agent in a fresh session checks the record against the cited evidence. Then the owner closes the goal or the next round opens.

3. **Where everything lives.** One annotated directory tree so the reader can find anything the rest of the piece names.
   - The model, the generated programs and studies, the citable sources, the work records, the goal trail.
   - The quarantine directory the agent must never read, which is what makes the Part 4 test possible.

4. **One round, walked.** One goal carried a real finding all the way through the loop, and the reader should see the whole arc before any mechanism. Beats 5 through 7 each zoom into one step of this same story.
   - The model's stored plasma energy came out 9 percent above the paper's printed number. That gap meant the design point needed 90.6 MW of heating against 50 installed.
   - A cheap check before the goal opened showed that scaling to the printed number would flip the verdict, but also that the printed number could not be reached from the paper's own figures. The target itself was suspect.
   - Round 1 sent one research request. Two systems-code papers by the same author were registered. Applying their definition with the paper's own profile rules split the gap: about five points from the helium ash being given the fuel's flat shape instead of peaking in the core, one from profile exponents, three the paper itself cannot close.
   - The owner ruled: fix the ash profile, tune nothing, no footnote.
   - Round 2 landed that one change, regenerated the program, and pinned it. Heating fell to 49.08 MW against 50. The wall load came under its limit.
   - The re-run study showed most "driven" points across the wider window now ignite, which the model could not handle. The owner closed the goal, declined to ask the author about the last three points, and the surprise became the next goal.
   - Evolution viewer for the model before and after.

5. **Research.** Zoom into round 1's research request. A number is only as good as its source, and an agent will cite from memory if allowed, so one script is the only thing that writes into the knowledge base.
   - What the reader sees: the request file, the run that fetched and registered the two papers with their hashes, and the recorded negative that no admissible source reproduces the printed value.
   - The rules: one writer, sources identified by the hash of their raw bytes, quarantine checked before any fetch, and "found nothing" recorded so nobody searches again.

6. **Changing the model.** Zoom into the work item behind round 2. A model change is a stated intent, one change, a regenerated program, and a record, with nothing tuned to hit a number.
   - What the reader sees: the item's stated intent (give the ash the paper's peaked profile), the one calculation that changed, the regenerated program, and the new pin that makes the re-run comparable to the old one.
   - The rule: the record exists so a reviewer can check the change against what was intended, not just whether the numbers moved the right way.

7. **The checks.** Zoom into what proved round 2. The harness has many rules in prose and a few that are mechanical, and the mechanical ones are the ones to trust.
   - What the reader sees: the check that the regenerated program matches the model byte for byte, the pre-execution critique that raised eleven findings on the study plan before any point ran, and the fresh reviewer on each round who did not do the work. (Verify at fill-in which checks ran on this goal and which came later.)
   - The rules: a study stops only on mechanical faults, never on a result that looks wrong; fixed vocabulary for "nothing pushed back," "something might," and "I judge this unresisted"; every number resolves to a source file; the owner keeps merges, closures and reserved scientific calls.
   - The limit: satisfied by 0.92 MW says the arithmetic is right and the program is the model. It does not say the plasma is real. "Is feasible" cannot be decided from the paper.

8. **What it cost, and what next.** The harness grew faster than it was used, and starting with plain files and adding machinery only after a real failure is what made trimming it possible.
   - Repo size over time, colored by what is still active.
   - The September pass that made reviews and stage documents conditional on risk, because the process had grown heavier than the work.
   - Which of the three goals held: good work, efficient agent, no hand cleanup.
   - Short list of what we would do next. Hand off to Parts 4 and 5.

Open: whether 8 stays here or moves to Part 5; whether to gather the repo-size numbers before drafting.
