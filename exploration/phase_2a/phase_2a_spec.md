# Phase 2a Spec: Generative Reasoning Tree

**Date**: 2026-03-09
**Status**: Draft
**Depends on**: Phase 1 results (table, 1b_v2 analysis, 1d verdict), spike review
**Supersedes**: `phase_2a/phase_2a_spec.md` (misguided — scaled the spike instead of building the algorithm)

---

## Objective

**Test whether a structured, requirements-driven decomposition protocol can derive the constraints that shape the fusion design space** — producing a reasoning tree that explains *why* concepts diverge, *why* certain combinations don't exist, and *where* knowledge transfers across concept families.

Phase 1 proved the flat table is a classification scheme: it records WHAT each concept chose but not WHY. The reasoning tree inverts this — starting from universal requirements and building outward, so that each branch point carries an explanation of the forces that cause concepts to diverge.

The core claim being tested: **the same universal requirement, interpreted in different accumulated contexts, produces different constraints and solutions.** The tree expansion generates constraints; the 38-concept table validates them; the justification sets enable transfer analysis. The constraint registry that accumulates during expansion is the primary knowledge artifact — not the tree shape itself.

Recovery of known concept families is a sanity check (the tree should arrive at recognizable concepts). The real tests are: can the tree explain the **negative space** (absent combinations), produce **validated constraints** from first-principles reasoning, and make **transfer opportunities** formally visible?

---

## Background

### What Phase 1 established

- The flat table (38 concepts × 18 columns) is a **classification scheme** with ~2 effective degrees of freedom (concept + fuel)
- **0% generative coherence** with unconditional random sampling; 23% with family-conditional sampling
- **Three tightly coupled clusters**: Confinement-Heating-Plasma, Fuel-Neutron-Energy, Driver-Hardware
- The table describes WHAT but not WHY — within-family differentiation fails (Test 4)
- Columns carry approach-level information but miss strategy-level differentiation

### What the spike established

- Constraint propagation + ATMS is a sound mechanism for tracking justifications
- But: the spike reimplements the flat table with inference (predefined variables, predefined domains, predefined constraints → pruning)
- The interesting thing is the PROCESS of building the tree, not the static structure

### What the review concluded

- Static AND/OR graphs don't capture context-dependence — AND branches imply independence, which is exactly what the design space ISN'T
- Requirements are not nodes in a graph — they are LENSES applied at each decision point
- The value is in the reasoning trace, not the tree shape
- The algorithm should BUILD the design space, not traverse a pre-specified one

---

## The Algorithm

### Requirements (the lenses)

Universal conditions that every fusion power concept must satisfy. These are not nodes in the tree — they are applied as evaluation lenses at every decision point, generating context-dependent questions.

| ID | Requirement | What it demands | What questions it generates |
|---|---|---|---|
| R1 | **Fuel the reaction** | Sustainable fuel supply for the chosen reaction | What fuel cycle? Where does fuel come from? (D-T → tritium breeding. p-B11 → commercially available. D-He3 → He3 sourcing problem) |
| R2 | **Achieve fusion conditions** | Create and sustain the conditions for fusion to occur | How do you confine? What geometry? How do you heat? How do you maintain stability? |
| R3 | **Produce net energy** | More energy out than the entire plant consumes | What's the gain? What's the driver efficiency? What fraction recirculates? How do you close the energy balance? |
| R4 | **Extract usable energy** | Convert fusion energy products into deliverable form | What carries the energy (neutrons vs. charged particles)? Thermal conversion or direct? What power cycle? |
| R5 | **Manage the nuclear environment** | Safely handle all nuclear byproducts | Shielding? Activation? Waste classification? Tritium safety? |
| R6 | **Maintain structural and material integrity** | The plant must survive the environment it creates | Neutron damage? Thermal loads? Cyclic stress? Plasma-material interaction? |

**Why these six.** R2 (achieve fusion) is the central question — it generates the first and deepest branching. R1 (fuel) and R3 (net energy) drive the next tier of divergence: fuel choice determines the nuclear environment, and net energy requirements drive the compact-vs-large, high-efficiency-vs-high-gain splits that differentiate concepts within a family. R4 (extract energy) separates thermal-conversion concepts from direct-conversion concepts — a real structural divergence driven by what the reaction produces. R5 (nuclear environment) and R6 (structural integrity) become increasingly generative at deeper levels, where the specific engineering challenges of each path emerge.

The set is extensible. If a branch point reveals a missing lens (e.g., economics, licensability, manufacturability), add it and note the discovery. P6 (economics) and P7 (licensable/buildable) from the earlier concept doc are deliberately excluded for now — they are evaluation criteria applied to completed concept paths rather than drivers of design branching, but that hypothesis may prove wrong.

### The process

At each node in the tree:

```
GIVEN:
  - accumulated_context: all design choices made on the path from root to here
  - requirements: {R1, R2, R3, R4, R5, R6} + any requirements accumulated from prior decisions
  - current_question: the design question to resolve at this node

APPLY domain knowledge + reasoning:
  1. State the question IN CONTEXT of accumulated decisions
  2. Apply each requirement as a LENS:
     - Which requirements bear on this question?
     - How does each requirement constrain or shape the options?
  3. Generate options (the OR branches):
     - What are the distinct approaches to answering this question?
     - For each: WHY is this a viable path? What is the thesis?
  4. For each option, derive consequences:
     - What new questions does this choice CREATE?
     - Which requirements change status? (easier to satisfy, harder, new sub-requirements activated)
     - What downstream problem landscape does this choice generate?

OUTPUT (per node):
  - The question, in context
  - Which requirements bear on it and how
  - The options, each with:
    - Reasoning / thesis
    - New downstream questions generated
    - Requirement status changes
```

### Worked example (level 1)

**Root question**: "How do we confine fusion?" (generated by applying R2 to empty context)

**Requirements bearing**: R2 directly; R1, R3, R5, R6 shape the options indirectly. R4 (extract energy) is not yet discriminating at this level.

**Options**:

1. **Magnetic confinement** — Use magnetic fields to confine a hot plasma indefinitely
   - *Thesis*: Sustain a continuous (or long-pulse) plasma; field geometry provides confinement
   - *New questions*: What field geometry? What field strength? How to heat to ignition? How to maintain stability? What magnets?
   - *R3 (net energy)*: Confinement quality × volume × heating efficiency determines Q. Steady-state operation avoids pulsed-power losses.
   - *R5 (nuclear)*: If D-T fuel (most likely), 14.1 MeV neutrons → shielding, activation, tritium breeding become dominant engineering challenges
   - *R6 (structural)*: Steady-state neutron flux → first wall / blanket lifetime is the structural challenge

2. **Inertial confinement** — Compress fuel to extreme density; confinement by inertia during burn
   - *Thesis*: Don't try to hold plasma; instead, make it burn faster than it disassembles
   - *New questions*: What driver? How to achieve symmetric compression? Target design? Chamber survival between shots? Repetition rate?
   - *R3 (net energy)*: Driver efficiency is THE challenge — lasers are 5–15% wall-plug efficient. Must compensate with high target gain.
   - *R5 (nuclear)*: Pulsed neutron loading; chamber sees shock + debris each shot
   - *R6 (structural)*: Cyclic shock loading dominates; fundamentally different structural challenge than MFE

3. **Hybrid / magnetized target** — Combine: magnetically pre-condition plasma, then compress
   - *Thesis*: Relax requirements on both field strength (vs. pure MFE) and driver energy (vs. pure IFE)
   - *New questions*: What target? What compression mechanism? How to magnetize the target? What rep rate?
   - *R3 (net energy)*: Lower driver energy needed (magnetized target requires less compression), but pulsed operation.
   - *R5/R6*: Depends heavily on specific approach — pulsed like IFE but with magnetic components

Each option generates a DIFFERENT downstream problem landscape. That divergence IS the context-dependence the flat table couldn't represent.

### Key properties

1. **Questions are not predefined.** They emerge from applying requirements to accumulated context. "What target fabrication method?" only exists on the IFE branch. "What divertor concept?" only exists on the tokamak sub-branch.

2. **Requirements are re-applied at every level.** The same R6 (structural integrity) generates different questions depending on context: neutron damage to first wall (MFE), shock loading on chamber (IFE), electrode erosion (Z-pinch).

3. **The tree is the output.** Concepts are paths through the tree, not inputs to it. Following `confine → magnetic → tokamak → compact/high-field → HTS` arrives at something recognizable as CFS. The concept emerges; it isn't pre-selected.

4. **Branch points explain divergence.** At each OR node, the reasoning explains WHY concepts diverge — not just that they chose differently, but what problem each choice is solving and what trade-off it navigates.

---

## Scope

### Depth

Expand to **3–4 levels**, which should be enough to reach recognizable concept families:

- **Level 0**: Root (empty context)
- **Level 1**: Confinement approach (MFE / IFE / MIF / exotic)
- **Level 2**: Concept family within approach (tokamak / stellarator / mirror / FRC / ... for MFE)
- **Level 3**: Key differentiating choices within family (compact vs. conventional tokamak, fuel choice, etc.)
- **Level 4** (selective): Concept-specific thesis (where specific startups become identifiable)

### Breadth

- **Level 1**: Expand all branches (3–4 options)
- **Level 2**: Expand all branches within MFE (largest family, most diversity); selectively expand IFE and MIF
- **Level 3+**: Follow branches that lead toward well-known concepts, to test recovery. Don't exhaustively expand every path.

Target: ~30–50 nodes total. Enough to test the algorithm, not so many that review becomes intractable.

### Branching control

At each node, the question "how many options?" is answered by the domain knowledge, not by a fixed branching factor. Some questions have 2 options (D-T vs. advanced fuels at the highest level), some have 5+ (MFE topology variants). The algorithm follows the domain.

---

## Implementation

### Three-layer architecture

See `phase_2a_design.md` for full design. Summary:

1. **Layer 1 — LLM reasoning (creative)**: headless, stateless `claude -p` calls. Each node sees only its own path from root. The prompt provides accumulated context, R1–R6 lenses, and the current question. The LLM generates options with thesis, requirement analysis, derived constraints, and new questions. Explicitly prompted for first-principles reasoning and negative space.

2. **Layer 2 — Constraint capture (analytical)**: extracts formal constraints from LLM output. Validates each constraint against `table_v2.csv` (the 38-concept table). Checks cross-branch consistency. Builds the constraint registry — the primary knowledge artifact. Constraint set starts **empty** and grows during expansion (output, not input).

3. **Layer 3 — Justification tracking (transfer)**: each validated constraint carries its justification set (the accumulated context that produced it). Transfer detection is a lookup on shared justification subsets across paths.

### Execution approach

1. **Round 0**: Design and test prompt template. Dry run on root node. Verify JSON output, constraint extraction, table validation.
2. **Round 1**: Expand root → Level 1 (confinement approaches). Validate constraints. Render. Review.
3. **Round 2**: Expand Level 1 → Level 2 (concept families). Validate. Render. Review.
4. **Round 3**: Expand selected Level 2 → Level 3 (differentiating choices). Validate. Render. Review.
5. **Assess**: Constraint registry analysis + tree path analysis → `assessment.md`.

Each round: expand → validate → render → human review. Review between rounds catches errors before they propagate.

---

## Success Criteria

### Calibrating the bar

The schema's hierarchy (Confinement Family → MFE Topology → Tokamak Shape) already encodes a 3-level tree with thesis statements at the leaves ("Compact: High-field-enabled compact design, R < ~2.5 m. HTS magnets enable strong field in small volume."). Levels 0–2 of the reasoning tree will largely rediscover this known structure. **Recovering concept families is necessary but not sufficient** — it's the easy test. The tree earns its keep in three harder ways:

1. **Negative space** — why certain combinations DON'T exist (no p-B11 tokamak, no steady-state IFE, no D-T with direct conversion). The tree should make absences explainable through requirement interactions, not just empirically absent.
2. **Within-family differentiation** — where CFS diverges from Tokamak Energy diverges from Energy Singularity. The schema has a label for each; the tree should reveal what forces drive the divergence.
3. **Cross-cutting requirement interactions** — where the lenses generate questions that cut across the schema hierarchy (e.g., R3 net energy bears differently on compact vs. spherical tokamak; R6 structural integrity creates different challenges for laser ICF vs. Z-pinch, even though both are pulsed).

### Primary: Negative Space + Constraint Validation

1. **Negative space explanation** (the hard test): The tree must make at least 3 "absent combinations" explainable — not just noting that they don't exist, but showing which requirement lens, applied to which accumulated context, produces the contradiction or makes the path non-viable. Target examples:
   - Why no p-B11 tokamak? (R2 achieve fusion: T_i requirement exceeds tokamak confinement capability)
   - Why no steady-state IFE? (R2: inertial confinement is inherently pulsed — "confinement by inertia during burn" means the plasma exists only during the implosion)
   - Why no D-T with direct energy conversion? (R4 extract energy: 80% of D-T energy is in neutrons, which cannot be directly converted to electricity)

   If the tree can explain these absences through its own reasoning structure (not just because we know the answer), it demonstrates genuine explanatory power beyond the flat table.

2. **Constraint validation rate**: Constraints extracted from LLM reasoning at each node are validated against `table_v2.csv`. The tree earns its keep if:
   - **>70% of extracted constraints validate** against the 38-concept table (the LLM derives real patterns from first principles, not hallucinated rules)
   - **Flagged constraints** (hold for most but not all concepts) produce interesting exceptions — table errors, genuine outliers, or under-specified conditions that need refinement
   - **<20% rejection rate** (constraints that flatly contradict the table)

   A high validation rate means the requirements-driven decomposition produces real knowledge. A low rate means the LLM is confabulating plausible-but-wrong rules.

3. **Divergence reasoning adds value over schema descriptions**: At branch points where the schema already provides thesis statements, the tree's reasoning must add something — typically the requirement interactions that MOTIVATE the thesis. "Compact tokamak uses high-field HTS" (schema-level) vs. "R3 (net energy) favors compactness because Q scales with B⁴, so higher field → smaller device at same Q; but R6 (structural integrity) is harder because neutron flux density increases with compactness, and R1 (fuel) gets harder because blanket space for tritium breeding is constrained" (tree-level). The tree should show the trade-off structure, not just the label.

### Primary: Concept Recovery (sanity check)

4. **Concept family recovery**: Paths through the tree correspond to recognizable concept families — tokamak, stellarator, laser ICF, Z-pinch, FRC, MTF. This should be straightforward. Failure here means the algorithm is broken at a basic level. Success is necessary but not sufficient.

### Secondary: Discovery

Assessed opportunistically — we don't need this to succeed, but we want to notice it if it happens.

5. **Novel paths**: Do any paths through the tree lead to concept configurations that are NOT in the 38-concept table? If so, what percentage pass a basic physics sniff test (not obviously incoherent)? This is the generative test that the flat table failed at 0% — even a modest hit rate would be meaningful.

6. **Novel questions**: Does the algorithm generate downstream questions at any node that aren't represented in the table's 18 columns? These would be design dimensions the classification scheme missed — evidence that the top-down process sees structure the bottom-up table didn't capture. (In the constraint registry, these appear as constraints referencing variables not mappable to any table column.)

### Secondary: Transferability

Assessed via the constraint registry's justification sets — does the structure make transfer opportunities formally visible?

7. **Shared constraints across branches**: Do different paths through the tree produce the same validated constraint with overlapping justification sets? (e.g., D-T tokamak and D-T laser ICF both deriving "must breed tritium" with shared justification `{fuel: D-T}`). Count the convergence points — each is a candidate transfer opportunity.

8. **Context differentiation at convergence**: Where two paths produce the same constraint, does the justification set make clear what's shared (the constraint condition) vs. what differs (the broader accumulated context)? The justification set should tell you whether transfer of the SOLUTION is justified, not just transfer of the PROBLEM.

### Informative (either way)

9. **Completeness**: How many of the 38 known concepts have a path that reaches them? Where does the tree stop short? (We don't expect 100% — scope is 3–4 levels, selective breadth.)

10. **Missing requirements**: Does the tree expansion reveal that R1–R6 are insufficient — that there are branch points where a new requirement lens is needed?

11. **Ordering sensitivity**: At any node, could a different question ordering produce a different tree structure? If so, is this a problem (the tree is arbitrary) or a feature (different orderings reveal different structure)?

12. **Constraint registry quality**: How many total constraints accumulated? What fraction validated vs. flagged vs. rejected? What's the coverage across table columns? Where are the gaps? This is a measure of how much formalized knowledge the protocol extracted.

---

## Non-Goals

- **Production code.** This is a document/analysis exercise, not a software system.
- **Complete 38-concept coverage.** We're testing the algorithm on a sample, not exhaustively mapping every concept.
- **Quantitative parameters.** No numbers (field strength in Tesla, plasma temperature in keV) at this stage. The tree is structural/qualitative. Quantitative annotation is a later phase.
- **Cost modeling.** LCOE and CAS mapping come after the tree structure is validated.
- **Automating the algorithm.** The LLM + human review process is manual and deliberate. Automation is a later concern.

---

## What We Learn

**If it works** (primary criteria pass): The protocol produces validated constraints from first-principles reasoning, explains the negative space, and generates divergence reasoning richer than the schema's labels. The constraint registry becomes a formalized knowledge artifact — the design space's rules, derived generatively and validated empirically. Proceed to Phase 2b (cross-concept transfer using justification sets) and Phase 2c (analysis of constraint structure, coverage gaps, and novel variables).

**If the constraint registry is rich** (criterion 12): A large, high-quality constraint set validated against 38 concepts is valuable independently of the tree. It's the "constraint network" that `algorithm_ideation.md` identified as the reusable artifact — invest in the constraints, not the concept representations. Future work could use this registry for propagation (as in the spike), SAT-based enumeration, or gap analysis on novel concepts.

**If discovery shows up** (criteria 5–6): Novel paths or novel variables demonstrate that the top-down process sees structure the bottom-up table didn't capture. Particularly valuable if the constraint registry contains validated rules referencing variables outside the table's 18 columns — these are design dimensions the classification scheme missed.

**If transferability is visible** (criteria 7–8): Shared constraints with overlapping justification sets provide a principled basis for Phase 2b's cross-concept transfer test. The justification sets tell you not just that two concepts share a sub-problem, but exactly which upstream decisions create the shared context and where the contexts diverge.

**If it partially works**: Some branches produce validated constraints; others produce mostly rejected ones. We learn WHERE the LLM's first-principles reasoning is reliable (probably Tier 1 approach-level constraints) and where it breaks down (probably Tier 3 design-point-level constraints that require quantitative knowledge). The validation rate by tree level is diagnostic.

**If it fails**: The constraint validation rate is low (<50%), the negative space isn't explained by the tree's own reasoning, or the tree produces reasoning that contradicts the table. In this case, the LLM either can't do reliable first-principles reasoning about fusion design (the domain knowledge isn't accessible in the right way) or the prompt protocol doesn't extract it effectively. Either finding shapes what to try differently — possibly more constrained prompts, different requirement decomposition, or a fundamentally different approach to constraint derivation.
