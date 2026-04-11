# Phase 2 Concept Review: Issues and Reframing

**Date**: 2026-03-09
**Status**: Checkpoint — digesting before proceeding
**Input**: `phase_2_concept.md` + discussion

---

## Issues Identified

### 1. The AND/OR graph doesn't inherently capture context-dependence

The original context document hypothesized that the fusion design space is context-dependent — that each design decision reshapes the downstream problem landscape. The AND/OR graph was proposed as a structure that could represent this. But in working through the concrete formulations (Approaches A, B, C), a structural problem emerged:

**AND nodes assume independent sub-problems.** When the root says "solve P1 AND P2 AND ... AND P7," it implies these can be decomposed and solved in parallel. But the whole point of context-dependence is that they CAN'T — P4 (Sustain Operation) decomposes completely differently depending on what was decided for P1 (Achieve Fusion Conditions) and P3 (Convert Energy). Putting them as AND-siblings hides the dependency that IS the interesting structure.

The AND/OR graph was supposed to capture context-dependence. It doesn't — at least not as a static structure with requirements as AND branches. The context-dependence lives in how the graph gets BUILT, not in the graph itself.

### 2. The sequential decision tree fix is domain-knowledge-heavy and uninformative

The natural fix — make the graph sequential so that each decision has upstream context — produces a hand-crafted tree that recapitulates known engineering knowledge. "Given D-T compact tokamak, here are the sub-problems..." This is correct but not novel. We already know what sub-problems each concept faces. Encoding that knowledge into a tree doesn't produce new understanding.

The reason this is uninteresting: the suggested structure relies entirely on domain expertise to hand-place every node. If you need an expert to build the tree, and the tree only contains what the expert already knows, the tree hasn't earned its keep.

### 3. Requirements are not design decisions

The primitive requirements (P1–P7) were placed in the graph as nodes to decompose. But requirements are not decisions — they are CONDITIONS that must be satisfied. You don't "choose" to achieve fusion conditions; you must. The decomposition of HOW you satisfy a requirement is where the design decisions live, and that decomposition depends on everything else you've decided.

Requirements cannot be modeled as AND branches because they aren't independent sub-problems. They are more like lenses or filters that apply to every design decision. When you're choosing a confinement approach, you're not just "solving P1" — you're making a choice that will be evaluated against ALL the requirements simultaneously.

### 4. The "requirements as a lens" idea got lost

The original context document described primitive requirements as analogous to Alexander's large-scale patterns — invariant conditions that get decomposed differently depending on the generative path. This was meant to describe a PROCESS, not a structure. The requirements shape how you think about each decision, they don't sit as nodes in a tree.

When this was translated into AND/OR graph formulations, the requirements got reified as structural elements (AND branches, sub-problem nodes). This lost the dynamic quality — requirements as an active lens applied during decomposition, not a static branch to be filled in.

---

## The Reframing

### What we actually want

Two goals:
1. **Better understanding**: A framework that, when applied to a concept, reveals WHY the concept looks the way it does — not just WHAT it chose, but the reasoning chain from problem to solution.
2. **Future discovery**: A framework general enough that, applied to a novel starting point, it could help fill in the design decisions around a new idea — or expose where current knowledge runs out.

### The key insight: it's about PROCESS + ALGORITHM, not just structure

The flat table is a static artifact (structure only, no process). The AND/OR graph as sketched was also a static artifact (richer structure, but still no process). Neither captures the dynamic quality of context-dependent design.

What matters is:
- **The process of building the tree** — how each node gets expanded, what information feeds the expansion, how context accumulates
- **Recording that process** — the reasoning trace IS the understanding
- **Generalizing that process** — if the algorithm is general enough, it can be applied to novel situations

The tree that results from running the process is a useful artifact, but the VALUE is in the process and its recording, not just the final tree shape.

### The algorithm (sketch)

At any point in the decomposition:

```
GIVEN:
  - accumulated_decisions: the design choices made so far (path from root)
  - requirement_primitives: the set of requirements that must be satisfied
    (plus any additional requirements accumulated from prior decisions)
  - current_problem: the next design question to resolve

APPLY:
  A knowledge-based process that:
  1. Considers the current problem IN THE CONTEXT of accumulated decisions
  2. Uses requirement primitives as LENSES to evaluate and shape options
  3. Produces a decision tree for the current problem
  4. Records the reasoning (why these options, why not others, what each
     option implies for downstream problems and requirement satisfaction)

OUTPUT:
  - A set of options for the current problem (OR branches)
  - For each option: new decisions added to accumulated context
  - For each option: new sub-problems generated (next problems to solve)
  - For each option: updated requirement status (which requirements are
    helped, hurt, or unchanged by this choice)
```

This is NOT a static graph traversal. It's an iterative expansion where each step uses the full accumulated context. The "algorithm" is really a protocol for structured reasoning about design decisions.

### How this differs from the AND/OR graph approaches

| Aspect | AND/OR graph (as sketched) | Process-based approach |
|---|---|---|
| Requirements | Nodes in the graph (AND branches) | External lenses applied at each step |
| Context | Implicit in graph position | Explicit accumulated state |
| Sub-problems | Pre-specified or hand-crafted | Generated by the process at each step |
| Independence | AND implies independent | Independence assessed per-step |
| Understanding | Read the graph | Read the reasoning trace |
| Novelty | Enumerate paths in existing graph | Apply the process to a new starting point |

### The AND/OR structure is still relevant, but differently

The AND/OR distinction doesn't disappear — it shows up in how you STAGE problems:

- Some problems are largely independent of upstream decisions. **P3 (Convert Energy)** is a reasonable example — the thermodynamic cycle options don't depend heavily on confinement type. These can be explored as AND-parallel sub-graphs. Running them in parallel expands the option space (more combinations, including potentially surprising ones).

- Some problems are heavily context-dependent. **P4 (Sustain Operation)** varies radically by concept — tritium breeding only exists for D-T, target fabrication only exists for IFE, electrode cycling only exists for pulsed concepts. These must be STAGED after the decisions that create their context.

The trade-off in staging is explicit:

- **More parallel (AND-like)**: Larger combinatorial space → more infeasible combinations, but also more chance of exposing hidden viable combinations that domain experts wouldn't consider.
- **More sequential**: Smaller, more curated space → higher feasibility rate, but limited to combinations an expert would already think of.

The staging decision itself is a design choice for the algorithm, not a property of the domain.

### Where this leads

The experimental question for Phase 2 is no longer "what static graph structure best represents the fusion design space?" It's:

**Can we define a general decomposition algorithm that, when executed on different concepts, produces useful reasoning traces — and are those traces more informative than the flat table for understanding concepts and identifying transfer opportunities?**

The prototype would be:
1. Define the algorithm (the protocol for structured decomposition)
2. Run it on 2-3 concepts
3. Examine the traces: do they reveal structure? Do convergence points emerge naturally? Is the reasoning reusable?
4. Test: given a novel starting point (a new confinement concept), does the algorithm help fill in the design decisions, or does it break down?

### How the 29 confinement types actually emerged

A grounding example from the discussion: the 29 different confinement concepts in the table didn't come from an algorithm. They came from decades of physics research, where someone had an insight ("what if the magnetic field lines were helical instead of purely toroidal?") and then worked through the implications. Getting from "magnetic confinement" to "stellarator" is not turning a crank — it's a creative leap informed by deep physics understanding.

The algorithm we're designing doesn't need to MAKE those leaps. What it needs to do is: given that someone HAS made a leap (proposed a new confinement concept), rapidly and systematically work through all the downstream design decisions. What sub-problems does this concept face? What solutions exist? Where does existing knowledge transfer, and where are there genuine unknowns?

This is the practical value proposition: not replacing invention, but providing scaffolding for rapidly elaborating a novel idea into a structured design, using existing knowledge where it applies and flagging gaps where it doesn't.

---

## Open Questions (for digestion)

1. **What is the right level of generality for the algorithm?** Too general → it's just "think carefully about each decision." Too specific → it's domain-knowledge-heavy and doesn't generalize. Where's the sweet spot?

2. **What does "recording the process" look like concretely?** A reasoning trace per node? A structured document? How do you make it both human-readable (for understanding) and machine-processable (for analysis)?

3. **How do you decide staging?** Which sub-problems to explore in parallel (AND-like, more combinatorial) vs. sequentially (staged, more curated)? Is this a per-problem judgment call, or can it be systematized?

4. **What's the minimal prototype?** What's the smallest thing we could build and test that would tell us whether this process-based approach has legs?

5. **Where do forces/trade-offs fit?** Approach C (Force-Resolution Cascades) from the concept document was the richest for capturing design reasoning. Does that reasoning naturally emerge from the process, or does it need to be explicitly encoded in the algorithm?
