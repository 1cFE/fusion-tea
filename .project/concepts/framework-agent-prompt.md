# Prompt: Formal Model of the Reasoning Tree

## Your task

Build a formal model of the reasoning tree algorithm — what it is, what it does, what its moving parts are, and how they relate. Write the output to `.project/concepts/reasoning-tree-formal-model.md`.

The purpose of this model: when someone reads the problem statement (`.project/concepts/reasoning-tree-problem-statement.md`) and tries to reason about how to evolve the algorithm, they currently have no foundation. They flounder — producing slop that restates the problem, proposes shallow solutions, or organizes concepts into taxonomies that don't do analytical work. This model should be the foundation that prevents that. It should give someone the precise vocabulary and structural understanding to reason clearly about the algorithm and its behavior.

This is NOT a solutions document. Do not propose algorithmic changes, new expansion modes, or implementation ideas. The deliverable is a precise conceptual model — abstractions that explain the algorithm's observed behavior and enable clear reasoning about its future behavior.

## What to read

Read these documents. They are the evolution of thinking on this problem, not ground truth. Each one gets something right and something wrong. Your job is to extract the signal, not summarize them. The signal includes the MOTIVATIONS and ORIGINAL INTENT. 

1. `exploration/context/context_dependent_design_spaces.md` — The original hypothesis: design spaces where upstream choices change what downstream questions exist. Read for the core phenomenon being modeled.

2. `exploration/context/research-pre-formal-concept-modeling.md` — Early research on formal approaches to this kind of problem. Read for what's been considered and rejected, and why.

3. `exploration/algorithm_ideation.md` — Design thinking on the algorithm before it was built. Multiple framings were explored. Read for the constraints on the solution space and what trade-offs were navigated.

4. `exploration/phase_2a/report.md` — The algorithm was built and run. L0 and L1 expansions produced strong results. Read this carefully — the results section is empirical ground truth. Understand what the algorithm actually produced, not just what it was supposed to produce.

Also read the tree state to see the actual data:
- `exploration/phase_2a/tree.json` (large — read the node IDs, questions, and structure; skim the expansion details)

Also read the problem statement that motivates the next phase of work:
- `.project/concepts/reasoning-tree-problem-statement.md`

## What the model must do

The model must give a reader and future AI Agents the ability to reason precisely about the following kinds of questions. THIS IS NOT THE ORDER YOU SHOULD FOLLOW. YOU MUST THINK CRITICALLY ABOUT HOW TO ORGANIZE AND PRESENT THE INFORAMTION. 

- How do we frame the problem we are trying to solve?
  - Restate as needed (but very concisely and sharply) the original motivations
  - Interpret, in our abstractions, what we are trying to achieve
  - Explain in this context what the extensions in the `reasoning-tree-problem-statement.md` are really asking for
- Explain how the algorithm current works. What are the concepts we work with, and how do they relate? 
- In this context, explain the specific SOURCE of challenges we are facing.
  - What would "prioritizing questions" mean?
  - What is the cause of the rapid broadening?
  - 
- Make sure, through all of this, you are mapping back to REAL concept design and engineering practices. 

The model should make these questions answerable through its abstractions, not by hand-waving or by deferring to "we'd need to run it and see."

## What "earning its spot" means

Every abstraction in your model must do at least one of:
- **Explain** an observed behavior (e.g., why the L0 expansion produced strong negative-space reasoning)
- **Predict** behavior in untested conditions (e.g., what would happen if you expanded with different initial context)
- **Distinguish** between things that look similar but behave differently (and say why the distinction matters)

If a concept doesn't explain, predict, or distinguish — cut it. A three-concept model that does real work is worth more than a ten-concept taxonomy that just organizes.

## What to avoid

- **Taxonomies for their own sake.** Don't classify things into types unless the types have different behavioral consequences that matter.
- **Restating the problem as if it were a solution.** "The tree needs to descend through abstraction levels" restates the problem. A model explains what determines behavior and why.
- **Deferring to empirical questions.** "This is an empirical question" is not analysis. If your model can't address something, say what's missing from the model and why.
- **Post-hoc rationalization.** Don't write chains of reasoning that look inevitable in retrospect. If the chain only works because you already know the answer (e.g., tokamaks exist), it's not a model — it's a narrative.
- **Fluff, hedging, throat-clearing.** No "it's worth noting that" or "this is an important distinction because." State the model.
- **Solutioning.** Any sentence that prescribes what the algorithm should do differently — delete it. The model describes what IS and what FOLLOWS FROM what is. Not what ought to be.

## Quality process

You MUST take FIVE LITERAL PASSES. 
- On the first pass, you will outline your approach in the document and present to the user. They will provide feedback to make sure you are on the right track. 
- Once approved, you will write a draft.
- Then you MUST RE-READ IT AND CRITIQUE IT:

1. **Does every concept do work?** For each abstraction: what does it explain that can't be explained without it? If nothing — cut it.
2. **Is this analytical or descriptive?** Does the model derive consequences from its premises, or does it just name and categorize things? "X is type A" is descriptive. "Because X has property P, it will behave as Y in context Z" is analytical.
3. **Does it serve the purpose?** Could someone use this model to reason clearly about the problem statement's goals? If a section doesn't help with that — why is it there?
4. **Am I smuggling in solutions?** Any implicit prescription about what the algorithm should do — find it and remove it.
5. **Would a sharp, impatient reader find this obvious or fluffy?** If yes, either the point is trivial (cut it) or you haven't pushed deep enough (go deeper).

After each critique pass, revise. The final document should be tight — No more than 150 lines. 

## Output

Write the final model to `.project/concepts/reasoning-tree-formal-model.md`. 
