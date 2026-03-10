# Algorithm Ideation: Beyond the AND/OR Graph

**Date**: 2026-03-09
**Status**: Brainstorm — fresh perspectives on the Phase 2 problem
**Input**: `phase_2_concept.md`, `phase_2_concept_review.md`, Phase 1 results

---

## The Problem Restated

The flat table is a classification scheme with ~2 effective degrees of freedom. The AND/OR graph (as sketched in the concept doc) was supposed to capture context-dependence, but the review found it doesn't — static AND branches imply independent sub-problems, which is exactly what the design space ISN'T. The review reframed the question:

> Can we define a general decomposition algorithm that, when executed on different concepts, produces useful reasoning traces — and are those traces more informative than the flat table?

This document explores algorithm and data structure ideas that might answer that question. The goal is to find an approach that is **algorithmic** (not hand-crafted), **produces reasoning traces** (not just structure), and **makes transfer formally justified** (not ad hoc).

---

## Idea 1: Fiber Bundles — Describe Transitions, Not Coordinates

The design space has exactly the property mathematicians call a **fiber bundle**: the "fiber" (set of available choices) changes depending on where you are in the "base space" (prior decisions). A D-T base point has a tritium-breeding fiber attached; a p-B11 base point doesn't.

The flat table tries to flatten all fibers into a single global coordinate system. That's what produces N/As — coordinates that don't exist in certain fibers.

**The insight**: describe the space by its **transition functions** (what changes and what's preserved when you switch contexts), not by its coordinates. Transfer = two points in different fibers that project to the same point in a shared sub-bundle.

**Practical implication**: instead of asking "what columns do CFS and TAE share?", ask "when I move from the CFS context to the TAE context, which derived engineering consequences survive the transition?" The things that survive are the transferable parts; the things that break are the context-dependent parts.

**Assessment**: Conceptually clarifying but abstract. Not directly implementable as a prototype. Its value is as a framing that prevents us from falling back into flat-table thinking.

---

## Idea 2: Constraint Propagation

There's a well-studied algorithm family that does exactly what the review doc described: **constraint propagation** (arc consistency, AC-3, and descendants).

### How it works

- **Variables**: design dimensions (confinement type, fuel, heating method, blanket type, etc.)
- **Domains**: the set of possible values for each variable (some variables start inactive — they don't exist until activated by an upstream choice)
- **Constraints**: rules linking variables. These encode the coupling clusters from Phase 1d.

The algorithm:
1. Start with a partial assignment (e.g., `confinement = compact_tokamak, fuel = D-T`)
2. **Propagate**: each assignment activates constraints that prune domains of unassigned variables. Some variables get activated (tritium_breeding becomes relevant). Some values get eliminated (direct_energy_conversion becomes impractical).
3. **Record the propagation trace**: which constraint fired, what it eliminated, why.
4. At each step, check: is the remaining domain **empty** (contradiction)? **Singleton** (forced choice)? **Multi-valued** (genuine design freedom)?

### What it produces

The propagation trace naturally distinguishes:
- **Determined** columns — forced by upstream choices (singleton domains after propagation)
- **Free** columns — genuine design freedom (multi-valued domains)
- **Activated** columns — variables that only enter the constraint network when certain values are assigned upstream (the context-dependence)
- **Eliminated** values — pruned options with explicit justification (which constraint killed them)

### Why this fits

- **Algorithmic, not hand-crafted**: the process is general; the knowledge lives in the constraints
- **Produces the reasoning trace** the review doc asks for — each propagation step is a recorded inference
- **The constraint set is the reusable artifact** — not the tree shape, which varies per concept
- **Directly testable**: run propagation from different starting points, compare traces
- **The 0% coherence result becomes a prediction**: random sampling ignores constraints → mostly lands in pruned regions → incoherent

### Connection to Phase 1 results

The three coupling clusters from Phase 1d map directly to constraint groups:
- **Confinement-Heating-Plasma** cluster → constraints like `IF confinement_family = IFE THEN operation_mode = pulsed AND plasma_state = compressed`
- **Fuel-Neutron-Energy** cluster → constraints like `IF fuel = D-T THEN neutron_management = heavy_shielding AND activate(tritium_breeding)`
- **Driver-Hardware** cluster → constraints like `IF confinement = stellarator THEN magnet_type IN {HTS, conventional_SC}`

**Assessment**: Strong candidate. Algorithmically clean, produces exactly the artifacts we need, and the constraint set grows incrementally. The main risk is that interesting design reasoning might live BETWEEN the constraint firings — the "why choose THIS resolution of the remaining freedom?" question that Approach C (forces) captured.

---

## Idea 3: Assumption-Based Truth Maintenance (ATMS)

A classic AI technique from de Kleer (1986) that seems almost purpose-built for this problem. An ATMS tracks **which assumptions support each conclusion**. Every derived fact carries a **justification set** showing exactly which upstream assumptions it depends on.

### Applied to fusion concepts

- Each concept is a **set of assumptions** (its design choices)
- Each engineering consequence carries its **justification set**
  - "Need heavy neutron shielding" ← justification: `{fuel = D-T}`
  - "Need TBR > 1.0 in compact toroidal geometry" ← justification: `{fuel = D-T, confinement = compact_tokamak}`
  - "Disruption severity scales with stored energy / volume" ← justification: `{confinement = tokamak, design_point = compact_high_field}`

### Transfer via shared justifications

**Transfer** becomes formally justified: "This conclusion has justification set `{fuel = D-T, neutron_flux = 14.1 MeV}`. Any concept whose assumptions include these can reuse this conclusion."

Two concepts arriving at "solve tritium breeding" via different paths:
- CFS: `{fuel = D-T, confinement = compact_tokamak}` → tritium breeding problem with context `{toroidal_geometry, compact, high_field, limited_blanket_space}`
- Realta (mirror): `{fuel = D-T, confinement = magnetic_mirror}` → tritium breeding problem with context `{linear_geometry, open_ends, moderate_blanket_space}`

The shared justification subset is `{fuel = D-T}`. The divergent parts are the geometry-specific terms. Transfer of the tritium breeding REQUIREMENT is justified (both need TBR > 1.0). Transfer of the blanket SOLUTION may not be (different geometries). The ATMS makes this distinction explicit and automatic.

### Novelty detection

When a new concept's assumptions don't match ANY existing justification set for a sub-problem, you've found a **genuine gap** — a sub-problem that hasn't been solved in this context before. This is the "where does existing knowledge run out?" question from the context document, Section 8.

### Relation to constraint propagation

ATMS and constraint propagation are complementary:
- **Constraint propagation** determines WHAT follows from a set of choices (forward inference)
- **ATMS** records WHY each conclusion holds (dependency tracking)

Running both together: propagation fires constraints and derives conclusions; ATMS records the minimal assumption set for each derived fact. The result is a fully-traced inference from design choices to engineering consequences, with transfer criteria embedded in the justification structure.

**Assessment**: This is the key addition that makes constraint propagation useful for transfer analysis. Without ATMS, propagation tells you what's determined but not why — you'd have to re-derive the justification for each transfer decision. With ATMS, the justification is maintained incrementally and transfer queries are lookups.

---

## Idea 4: Design as Satisfiability (SAT/SMT)

The 0% coherence rate means: satisfying assignments are a tiny fraction of the Cartesian product. This is literally a **satisfiability** problem.

Encode the constraints as a SAT or SMT formula and use a solver to:
- **Enumerate all satisfying assignments** — gives the actual design space (~30-40 viable combinations estimated in Phase 1d)
- **Find minimal unsatisfiable cores** — when a combination fails, the solver returns the **smallest set of conflicting choices**. More precise than "Fuel × Neutron Management is coupled."
- **Incremental solving** — add a new choice (e.g., `confinement = novel_concept_X`) and ask: what's still satisfiable? Where does propagation stop?

**Assessment**: Useful as a validation tool (enumerate the real space, confirm the ~2 DOF estimate computationally). Less useful as a reasoning tool — SAT solvers don't produce human-readable explanations of WHY something is unsatisfiable. Better as a complement to constraint propagation + ATMS than as the primary approach.

---

## Idea 5: Biological Morphospace Analogy

Evolutionary biology has the same structure: the **morphospace** of all possible body plans is enormous, but actual organisms cluster in tiny regions because **developmental constraints** make most of the space unreachable. (D'Arcy Thompson, Pere Alberch, Stuart Kauffman.)

The fusion design space has the same property: the morphological table defines a huge Cartesian product, but physics + engineering cascades restrict you to a small viable region. The key evo-devo insight: **the constraints are more informative than the organisms**. Understanding WHY most of the space is empty tells you more than cataloging the occupied points.

This suggests the core artifact isn't the graph of existing concepts — it's the **constraint network** itself. The concepts are witnesses that certain regions are satisfiable; the constraints explain why the rest isn't.

**Assessment**: Confirms the direction — invest in the constraint network as the primary knowledge artifact, not in the concept representations. The concepts are test cases that validate the constraints.

---

## Synthesis: Constraint Propagation + ATMS

Ideas 2 and 3 combine into a coherent approach:

### The system

1. **Variables** with conditional activation (some only exist in certain contexts)
2. **Constraints** encoding physics and engineering couplings (the knowledge artifact)
3. **Constraint propagation** to derive consequences from partial assignments (the algorithm)
4. **ATMS-style dependency tracking** to maintain justification sets for every derived fact (the transfer mechanism)

### What it produces for each concept

A **propagation trace**: a sequence of `(constraint, triggered_by, consequence, justification_set)` tuples that records the full reasoning chain from initial choices to engineering consequences. This is the "reasoning trace" the review doc asked for.

### What it produces across concepts

A **transfer map**: for any derived engineering consequence, the justification set tells you exactly which concepts can share it and which can't. Convergence points (shared sub-problems with overlapping justifications) emerge automatically — no need to hand-identify them.

### What it produces for novel concepts

A **gap analysis**: propagate from a novel starting point, see where propagation stops (no constraints fire → genuine unknown), where it produces singletons (determined → forced design choices), and where it produces multi-valued domains (genuine freedom → design decisions to be made).

### Where the forces / trade-offs live

The forces from Approach C (concept doc) don't disappear — they become a specific TYPE of constraint: **soft constraints** or **trade-off constraints** that don't eliminate options but annotate them with tensions. "High field improves confinement BUT increases structural stress" isn't a hard constraint (both values are viable) — it's a trade-off annotation on the `field_strength` variable. These can be layered on after the hard constraints are working.

### Growth path

1. Start with hard constraints from Phase 1d coupling clusters (~20-30 rules)
2. Add variable activation rules (context-dependence)
3. Add ATMS dependency tracking
4. Add soft constraints / trade-off annotations (forces)
5. Add quantitative parameters (the annotation layer from the concept doc)

---

## Spike Plan: Toy Demonstration

**Goal**: Demonstrate the constraint propagation + ATMS algorithm on a small toy problem, proving the mechanics work before mapping onto the full fusion domain.

**Duration**: A few hours — this is a proof-of-mechanism, not production code.

### The toy problem

A simplified fusion-like design space with ~6-8 variables, ~10-15 constraints, and ~4-5 "concepts" to trace through. Small enough to verify by hand, large enough to demonstrate:
- Constraint propagation from partial assignments
- Variable activation (some variables only relevant in certain contexts)
- ATMS dependency tracking (justification sets for derived facts)
- Transfer detection (shared justification sets across concepts)
- Gap analysis (propagation on a novel input)

### Toy variables (simplified fusion)

| Variable | Domain | Notes |
|----------|--------|-------|
| `confinement` | {tokamak, stellarator, laser_icf, z_pinch} | Always active |
| `fuel` | {DT, DHe3, pB11} | Always active |
| `heating` | {rf, nbi, laser, ohmic, compression} | Always active |
| `blanket` | {flibe, lipb, solid_breeder, none} | Active only if fuel=DT |
| `neutron_shielding` | {heavy, moderate, minimal} | Always active |
| `energy_conversion` | {thermal_steam, thermal_sco2, direct_electric, hybrid} | Always active |
| `rep_rate` | {steady_state, low_hz, high_hz} | Active only if pulsed |
| `magnet_type` | {hts, lts, conventional, none} | Active only if confinement needs magnets |

### Toy constraints (~12 rules)

```
C1:  fuel=DT        → activate(blanket), neutron_shielding=heavy
C2:  fuel=DHe3      → neutron_shielding=moderate
C3:  fuel=pB11      → neutron_shielding=minimal, energy_conversion ∈ {direct_electric, hybrid}
C4:  confinement=laser_icf → heating=laser, deactivate(magnet_type), activate(rep_rate)
C5:  confinement=tokamak   → heating ∈ {rf, nbi, ohmic}, activate(magnet_type)
C6:  confinement=stellarator → heating ∈ {rf, nbi}, activate(magnet_type), magnet_type ≠ conventional
C7:  confinement=z_pinch   → heating ∈ {ohmic, compression}, activate(rep_rate)
C8:  fuel=pB11 ∧ confinement=tokamak → CONTRADICTION (T_i too high for tokamak confinement)
C9:  fuel=DT → energy_conversion ∈ {thermal_steam, thermal_sco2}
C10: confinement=laser_icf ∧ fuel=DT → blanket ∈ {flibe, lipb}
C11: confinement=tokamak ∧ magnet_type=hts → blanket ∈ {flibe}  (compact geometry constraint)
C12: heating=laser → confinement=laser_icf  (reverse constraint)
```

### Toy concepts to trace

| Name | Initial assignment | Loosely models |
|------|-------------------|----------------|
| "CompactTok" | confinement=tokamak, fuel=DT, magnet_type=hts | CFS |
| "AneutronicFRC" | confinement=z_pinch, fuel=pB11 | TAE-like (simplified) |
| "LaserDT" | confinement=laser_icf, fuel=DT | Xcimer/Focused Energy |
| "DTStellarator" | confinement=stellarator, fuel=DT | Proxima/Type One |

### What the spike should demonstrate

1. **Propagation traces differ by concept**: CompactTok's trace activates blanket and forces flibe; AneutronicFRC's trace never activates blanket but forces direct conversion.

2. **Determined vs. free variables**: after propagation, some variables are forced (singleton domain), some have reduced but multi-valued domains (real design freedom), and some are not activated (N/A).

3. **ATMS justification sets**: "need heavy neutron shielding" carries justification `{fuel=DT}` — shared across CompactTok, LaserDT, and DTStellarator. "blanket must be flibe" carries justification `{fuel=DT, confinement=tokamak, magnet_type=hts}` — specific to CompactTok.

4. **Transfer detection**: query "which concepts share the justification for heavy shielding?" → {CompactTok, LaserDT, DTStellarator}. Query "which share the blanket=flibe justification?" → {CompactTok only}.

5. **Contradiction detection**: attempt confinement=tokamak, fuel=pB11 → C8 fires → contradiction with justification `{fuel=pB11, confinement=tokamak}`.

6. **Gap analysis**: propagate from confinement=stellarator, fuel=DHe3 (a concept not in the toy set). See what's determined, what's free, what's N/A.

### Implementation sketch

A single Python script (~200-300 lines):

```
class Variable:       # name, domain, active flag
class Constraint:     # condition → consequence, with ID
class Justification:  # set of (variable, value) assumptions
class PropagationEngine:
    propagate(partial_assignment) → trace
class ATMS:
    record(fact, justification)
    query_shared(fact) → set of concepts that share this justification
```

Output: print the propagation trace for each concept, then the transfer map.

### Success criteria

- [ ] Propagation produces different traces for each concept
- [ ] Justification sets are minimal (no redundant assumptions)
- [ ] Transfer queries return correct shared sets
- [ ] Contradiction is detected with correct justification
- [ ] Novel input (stellarator + DHe3) produces a reasonable partial result with identifiable gaps
- [ ] The output is more informative than listing column values (the flat table equivalent)

### What we learn

**If it works**: the algorithm mechanics are sound, and the question becomes "how do we encode real fusion constraints?" — a domain knowledge problem, not an algorithm problem. Proceed to map the Phase 1d coupling clusters into the constraint format and run on real concepts.

**If it struggles**: the toy problem will reveal where the algorithm breaks — maybe the constraint language is too rigid, maybe the ATMS overhead isn't worth it for small problems, maybe the interesting reasoning happens in the gaps between constraints. These are useful findings that shape what to try next.
