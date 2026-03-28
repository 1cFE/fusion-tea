# Problem Statement: Reasoning Tree Algorithm — Next Steps

**Date**: 2026-03-22
**Status**: Problem framing for strategic design work
**Context**: Phase 2a has validated the core mechanism. Now we need to decide how to evolve the algorithm to achieve specific analytical goals.

---

## Background: What Phase 2a Established

The Phase 2a reasoning tree is an algorithm for exploring a design space through structured decomposition. Its key properties:

1. **Problem decomposition via algorithm.** A root question is expanded into options, each option produces constraints and new downstream questions, and the process recurses. The tree grows one level at a time.

2. **Intellectual honesty.** Each expansion reasons from first principles. The LLM is given accumulated context and universal requirements (R1–R6), NOT the answer. It doesn't name known concepts. The reasoning is supposed to be unbiased as to outcomes — the concepts should *emerge* from the physics.

3. **Grounding.** Every expansion is grounded by (a) the six universal requirements applied as lenses and (b) the accumulated context of all upstream decisions. These prevent unconstrained speculation.

The algorithm has been validated through L0 (5 confinement options, 22 constraints, strong negative-space explanations) and L1 (all 5 L0 branches expanded, producing 14 pending L2 nodes). The reasoning quality is high — the LLM derives physics-grounded trade-offs, correctly identifies non-viable approaches, and recovers recognizable concept families from first principles.

Full details: `exploration/phase_2a/report.md`

### Current Algorithm (pseudocode)

```
expand(node):
  prompt = format(prompt_template,
    accumulated_context = node.context,  # all decisions from root to here
    requirements = R1..R6,               # universal requirement lenses
    question = node.question)            # the design question to resolve

  response = claude_headless(prompt)     # stateless, no cross-branch memory

  for option in response.options:
    # Each option carries:
    #   - thesis (what trade-off it navigates)
    #   - requirement_analysis (how R1-R6 bear on this choice)
    #   - constraints (what is forced/eliminated/activated)
    #   - new_questions (downstream design questions this choice creates)
    #   - context_addition (summary of this choice for downstream context)
    #   - negative_space (non-viable approaches with physics reasoning)

    child = create_node(
      question = option.new_questions[0],      # FIRST downstream question only
      context = node.context + [option.context_addition])
    tree.add_child(node, child)

  extract_and_validate_constraints(response, constraint_registry)
```

### Open Questions from Phase 2a Report

Two design issues surfaced during execution that remain unresolved:

**1. How should the "next question" be determined?**
Currently, each option produces 5-6 downstream questions and only the first is used. The rest are discarded. The tree's entire branching structure is determined by the LLM's ordering within a single call. There is no ranking, no selection heuristic, and no human choice at this step.

**2. How should constraints be validated?**
All 22 L0 constraints are "unmappable" — their variables don't correspond to any table column. The LLM reasons at the physics level (field topology, loss cones, compression ratios); the table operates at the engineering classification level (Confinement Family, Magnet Type). The vocabulary gap may or may not close at deeper tree levels.

---

## Goals

We want to evolve the algorithmic framework to achieve three specific outcomes. These are ordered by concreteness but all are important.

### Goal 1: Reproduce and explain downstream table columns from upstream choices

The Phase 1b v2 table (`exploration/phase_1b_v2/table_v2.csv`) has 38 fusion concepts × 18 design columns. The first 8 columns capture confinement hierarchy (family, topology, sub-type). The remaining 10 columns capture other design dimensions: Fuel, Primary Heating, Energy Capture, Plasma State, Magnet Type, Tritium Breeding, Neutron Management, Operation Mode, Repetition Rate, Driver Technology.

**The question**: Can the reasoning framework, starting from confinement-level context, *derive* what the other columns should be through its normal decomposition process? Not by recalling known concepts, but by reasoning from accumulated constraints and requirements.

Two concrete test cases:

**Fuel prediction**: Given the accumulated context of a compact tokamak path (MFE → Tokamak → Compact + HTS), can the framework derive that D-T is the strongly favored fuel? Can it explain — through requirement analysis — why p-B11 is fundamentally worse in this context (not just "no one does it" but the physics reason it fails)? And would the same reasoning, applied in a different context (say, an FRC with direct energy conversion), produce a *different* fuel ranking?

**Energy Capture prediction**: Given a tokamak context, can the framework derive that thermal conversion is essentially the only viable energy capture method? Can it explain why direct energy conversion is structurally incompatible with closed magnetic topology? And can it show that the *same* question in a mirror context produces a different answer (hybrid or direct becomes viable because of the open geometry)?

This goal also encompasses negative space: can the framework explain why certain combinations *don't exist* in the table? Why is there no p-B11 tokamak? Why is there no D-T concept with primary direct energy conversion? These absences should be derivable as constraint violations, not just observed as empty cells.

### Goal 2: Context-dependent questions should emerge naturally within families

When the framework descends into a specific concept family, the *right* engineering questions should appear as downstream questions — questions that only make sense in that specific context.

**Laser IFE example**: When exploring the laser IFE path, the question of direct drive vs. indirect drive should emerge as a meaningful design question. More interestingly: does "ash handling" (clearing debris and unburned fuel from the chamber between shots) come up naturally? This question exists because of the accumulated context: pulsed operation + target destruction + required rep rate → a debris clearing problem that doesn't exist in steady-state MFE.

**MFE example**: When exploring the tokamak path, does "current drive" emerge as the critical sustainment challenge? It should — because plasma-current-driven rotational transform requires continuous current drive to avoid ohmic decay. This question doesn't arise for stellarators (no plasma current needed) or for IFE (no sustained plasma at all).

The test here is whether the framework captures the *causal structure* of the design space: specific upstream choices create specific downstream questions that wouldn't exist otherwise. The questions should emerge from the decomposition, not be pre-specified.

### Goal 3: Seed the decision tree with priors and reason from them

The framework should support "seeded" exploration — starting with certain assumptions or desired properties pre-loaded, and seeing how the tree evolves differently.

**Concrete example**: "If you had a really cheap, effective way of doing direct energy capture, what would be the concept you would pursue?"

This seed should change the reasoning at every downstream decision point. Confinement options that produce directed charged-particle streams (mirrors, FRCs) should become more attractive. Fuel choices that put more energy into charged particles (aneutronic fuels like p-B11, D-He3) should be favored. The entire concept architecture should shift — and the shift should be *traceable* through the requirement analyses at each node ("R4 is now easily satisfied by the seed assumption, so the fuel choice can optimize for other requirements like R2 instead").

The key constraint: the seeded exploration must preserve the algorithm's core properties (decomposition, honesty, grounding). It should NOT be "ask the LLM what concept to build given cheap DEC." It should be the same decomposition process, but with the seed as an additional grounding element in the accumulated context. The reasoning should be unbiased except for the explicit seed.

Other potential seeds worth exploring:
- "Tritium is freely available in unlimited quantities at zero cost"
- "HTS magnets can produce 50 T fields at $10/kA-m"
- "A new material exists that is immune to neutron damage up to 200 DPA"
- "Steady-state plasma confinement with no disruptions is impossible" (what if the tokamak path is closed?)

Each seed should produce a detectably different tree, and the differences should be explainable in terms of how the seed changes the requirement analysis.

---

## Constraints on Solutions

Any proposed algorithmic evolution must preserve:

1. **The decomposition structure.** Understanding must be built step by step, with each step grounded in what came before. One-shot prompts that ask the LLM to predict an answer directly are not acceptable — they bypass the reasoning process that IS the value.

2. **Intellectual honesty.** The LLM should not know what answer it's "supposed" to get. The reasoning should be unbiased as to outcomes. Concepts should emerge from physics + requirements, not from recall.

3. **Grounding.** Every expansion must be constrained by (a) universal requirements and (b) accumulated context. Unconstrained speculation — even if interesting — isn't what we're building.

4. **Tractability.** The solution must be implementable with the existing infrastructure (headless `claude -p` calls, JSON output, Python scripts). It should be feasible to run experiments within a reasonable budget (~$10-50 in LLM costs).

---

## Key References

- **Phase 2a report**: `exploration/phase_2a/report.md` — full description of algorithm, results, open questions
- **Phase 2 concept**: `exploration/phase_2_concept.md` — three framings (subsystem, primitives, forces) and their trade-offs
- **Phase 2 concept review**: `exploration/phase_2_concept_review.md` — why AND/OR graphs failed, why process > structure
- **Algorithm ideation**: `exploration/algorithm_ideation.md` — early thinking on the algorithm
- **Table v2 schema**: `exploration/phase_1b_v2/schema_v2.md` — the 18 columns and their controlled vocabularies
- **Table v2 data**: `exploration/phase_1b_v2/table_v2.csv` — 38 concepts × 18 columns
- **Current tree state**: `exploration/phase_2a/tree.json` — 20 nodes (6 expanded, 14 pending L2)
- **Current constraint registry**: `exploration/phase_2a/constraints.json` — 22 constraints, all unmappable
- **Current prompt template**: `exploration/phase_2a/prompt.md` — the prompt used for expansions
- **Phase 1d report**: `exploration/phase_1d/report.md` — why the flat table is a classification scheme, not a design space (0/30 generative coherence, ~2 effective DoF)
- **Phase 2a plan**: `exploration/phase_2a/plan.md` — implementation plan with execution checklist
- **Phase 2a scripts**: `exploration/phase_2a/expand.py`, `validate.py`, `render.py`
