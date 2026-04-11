# Spike Review: Constraint Propagation + ATMS

**Date**: 2026-03-09
**Artifacts reviewed**: `algorithm_ideation.md`, `spike_constraint_atms.py`, `docs/demo/constraint-propagation.html`
**Status**: Review + forward-looking analysis

---

## What the Spike Demonstrates

The spike implements constraint propagation with ATMS-style justification tracking on a toy fusion design space (8 variables, 12 constraints, 4 concepts). It proves the algorithmic mechanics:

1. **Propagation works.** Starting from a partial assignment (e.g., `{confinement=tokamak, fuel=DT, magnet_type=hts}`), the engine fires constraints iteratively until fixed point, correctly deriving forced choices, reduced domains, activations, and N/As.

2. **Justification tracking works.** Each derived fact carries its minimal assumption set:
   - `neutron_shielding = heavy` ← `{fuel=DT}` — depends only on fuel
   - `blanket = flibe` ← `{fuel=DT, confinement=tokamak, magnet_type=hts}` — depends on all three

   The difference is automatic. No hand-reasoning about what transfers.

3. **Transfer detection works.** Shared justification sets identify what's genuinely shared across concepts vs. concept-specific. Three D-T concepts share `neutron_shielding = heavy` with identical justification `{fuel=DT}`.

4. **Gap analysis works.** Novel input (stellarator + DHe3) correctly identifies which variables are determined, reduced, free, or N/A. Free variables = where the constraint set has no opinion.

5. **Contradiction detection works.** `{confinement=tokamak, fuel=pB11}` → contradiction via C8, with justification.

The interactive HTML demo makes all of this tangible — stepping through propagation, seeing domains narrow, comparing concepts side-by-side.

---

## What the Spike Does NOT Demonstrate

### 1. Knowledge discovery

The 12 constraints are hand-crafted from Phase 1d coupling analysis. C1–C12 encode the same three coupling clusters we already identified:
- Fuel-Neutron-Energy cluster → C1, C2, C3, C9
- Confinement-Heating-Plasma cluster → C4, C5, C6, C7
- Cross-cluster interaction → C8, C10, C11, C12

The algorithm APPLIES this knowledge systematically — valuable for rapid elaboration — but the knowledge content is exactly what the flat table analysis already revealed. The spike proves the mechanism is sound; it doesn't show where the constraints would come from at scale.

### 2. Solution-level transfer

The spike answers: "Do these two concepts share the same engineering SUB-PROBLEM?" (e.g., both need heavy shielding, both justified by `{fuel=DT}`).

It does NOT answer: "Can concept B reuse concept A's SOLUTION to that sub-problem?" Heavy shielding for a compact tokamak (toroidal geometry, steady-state neutron flux, integrated blanket/shield) is a different engineering problem than heavy shielding for a laser ICF chamber (spherical geometry, pulsed neutron loading, chamber survival between shots). The categorical variable `neutron_shielding = heavy` is shared; the engineering solution may not be.

This is the depth gap. The current framework operates at the classification-scheme level (the same level as the flat table). Real transfer decisions require engineering context below the categorical level.

### 3. Constraint completeness

When `energy_conversion` is FREE for stellarator + DHe3, the algorithm can't distinguish:
- **Genuinely unconstrained** — any option works equally well
- **Insufficiently constrained** — we haven't encoded the relevant rules

In reality, D-He3 produces charged particles (direct conversion viable) AND D-D side neutrons (thermal capture needed for some fraction), so `hybrid` is arguably the right answer. The constraint set is incomplete, not the design space.

This is actually a useful feature — FREE variables are a systematic map of where the constraint set needs enrichment — but the user must understand that "free" means "we don't know" not "anything goes."

### 4. Scaling path

8 variables and 12 constraints are trivially tractable. The real domain has:
- ~18 categorical variables from the v2 table
- Potentially 30-50 variables if engineering sub-dimensions are added (blanket type, coolant, first-wall material, divertor concept, target fabrication, chamber design, magnet winding, ...)
- Potentially 100+ constraints connecting them

Arc consistency (the propagation algorithm) is polynomial in the number of variables and constraints, so computational scaling is not the issue. **Constraint authoring** is. Each constraint requires domain knowledge to formulate and validate. Writing 100+ constraints by hand — and getting them right — is a significant knowledge engineering effort.

---

## Forward Analysis: Addressing the Limitations

### LLM-Assisted Constraint Derivation

The most promising path to scaling the constraint set is to use LLM calls to derive constraints, guided by the requirement primitives as structured prompts.

**The protocol:**

```
FOR EACH requirement primitive (P1–P7):
  FOR EACH variable pair (v_i, v_j) not yet covered:
    PROMPT the LLM:
      "Given the requirement '{P_k description}', and two design variables:
       - {v_i}: domain = {d_i}
       - {v_j}: domain = {d_j}

       Are there values of v_i that FORCE, RESTRICT, or EXCLUDE values of v_j
       in order to satisfy this requirement?

       For each constraint found, provide:
       - condition (when it fires)
       - consequence (what it restricts)
       - physics justification (why, in 1-2 sentences)
       - confidence (high / medium / low)"

    VALIDATE returned constraints against:
      - Known concept data (does the constraint hold for all 38 concepts?)
      - Contradiction with existing constraints
      - Domain expert review (flag low-confidence for human review)

    ADD validated constraints to the constraint set
```

**Why requirements-as-lenses works here:** The requirements provide STRUCTURE to the LLM prompt. Instead of asking "what constraints exist between confinement and heating?" (open-ended, likely to produce surface-level answers), you ask "given the requirement 'achieve net energy gain,' what constraints exist between confinement and heating?" This focuses the LLM on the physics reasoning that actually generates the constraint.

**Why this might work well:**

1. **The knowledge exists in pre-training.** Fusion physics constraints are well-documented in textbooks, review papers, and design studies. An LLM trained on this literature can articulate why p-B11 requires T_i > 100 keV, why tokamaks need current drive for steady-state, why IFE chambers face pulsed loading. The constraint format (condition → consequence) is a structured extraction task, which LLMs handle well.

2. **The requirement primitives bound the search.** Without structure, "find all constraints between 50 variables" is O(n²) pairs × unbounded constraint space. With 7 requirements as lenses, each prompt is focused: "how does THIS requirement constrain THIS variable pair?" The requirements decompose the problem.

3. **Validation against the 38-concept dataset is automatic.** Every derived constraint can be checked: does it hold for all known concepts? If CFS violates a proposed constraint, either the constraint is wrong or CFS is misclassified. The 38 concepts serve as a validation set for the constraint derivation.

4. **Incremental enrichment.** Start with the ~12 constraints from the spike. Run the LLM derivation loop. Each round adds constraints, which reduces FREE variables in gap analysis, which identifies where to focus the next round. The constraint set converges as the gap analysis converges to no FREE variables.

**What could go wrong:**

- **Hallucinated constraints.** The LLM might generate plausible-sounding but incorrect physics rules. Mitigation: validate every constraint against the 38-concept dataset before accepting it.
- **Over-constraining.** The LLM might generate constraints that are true in general but have exceptions. E.g., "tokamaks require RF or NBI heating" is true for most but ignores ohmic-only devices. Mitigation: check for false positives against the dataset.
- **Under-constraining.** The LLM might miss subtle constraints that only manifest in specific combinations. Mitigation: the gap analysis identifies remaining FREE variables, which can be targeted in subsequent derivation rounds.
- **Conflation of hard constraints with soft preferences.** "D-T concepts MUST have heavy shielding" (hard) vs. "stellarators PREFER ECRH over NBI" (soft). The LLM may not reliably distinguish these. Mitigation: ask explicitly for the constraint type and require physics justification.

### Going Beyond Categorical Variables

The spike's variables match the flat table columns. But the Phase 1d finding was that within-family differentiation FAILS at this level — CFS and Tokamak Energy both map to `{confinement=tokamak, fuel=DT, magnet_type=hts}`, and constraint propagation gives them identical traces. To distinguish them, we need sub-categorical variables.

**Tiered variable approach:**

| Tier | Variables | Domain type | Example |
|------|-----------|-------------|---------|
| 1: Approach | Confinement, fuel, heating, energy conversion | Small categorical (3-6 values) | `confinement ∈ {tokamak, stellarator, ...}` |
| 2: Configuration | Blanket type, coolant, magnet winding, target type | Medium categorical (3-10 values) | `blanket ∈ {FLiBe, LiPb, solid_breeder, liquid_Li}` |
| 3: Design point | Field strength, plasma volume, pulse energy, rep rate | Continuous ranges or ordinal | `field_strength ∈ {moderate(5-10T), high(10-20T), very_high(>20T)}` |

Tier 1 variables are what the spike already has. Tier 2 variables are conditionally activated by Tier 1 choices (the spike already handles activation). Tier 3 variables are where CFS (20T, compact) diverges from Tokamak Energy (5T, spherical) — the design point that defines the concept's unique thesis.

The constraint propagation algorithm handles all three tiers without modification — it doesn't care whether variables are categorical or discretized-continuous. The scaling challenge is constraint authoring (more variables = more pairs to check for constraints).

**LLM-assisted derivation scales here too.** The Tier 2 and Tier 3 constraints are MORE likely to be well-covered in the literature, because they're the specific engineering trade-offs that reactor design studies have explored in detail. "If field strength > 15T, then blanket space is constrained, which restricts blanket type to high-density options (FLiBe, LiPb)" is the kind of constraint that appears in dozens of tokamak design papers.

### Solution-Level Transfer

The current spike identifies shared sub-problems. Extending to shared solutions requires annotating the OR choices (the values within each domain) with their own context:

```
Variable: blanket
Value: FLiBe
  Context: {
    geometry: toroidal | cylindrical | spherical
    neutron_spectrum: 14.1_MeV (D-T primary)
    operating_temperature: 460-700°C
    flow_regime: forced convection, MHD effects in high-field
    dual_function: breeder + coolant + shielding
  }
```

Two concepts that both select `blanket = FLiBe` share the value, but transfer of the blanket DESIGN depends on context overlap. A compact tokamak (toroidal, high-field → MHD drag significant) and a laser ICF chamber (spherical, no field → no MHD) both use FLiBe, but the engineering solution is different.

The ATMS justification tells you WHY each concept needs FLiBe. The solution context tells you WHETHER the specific implementation transfers. These are complementary:
- Justification-based transfer: "Do we face the same sub-problem?" (shared justification → yes)
- Context-based transfer: "Can we use the same solution?" (overlapping context → maybe)

**Implementation path:** Add a `solution_context` annotation layer to the constraint engine. When a variable is determined to a specific value, the engine records not just the justification (which assumptions forced this) but also the accumulated context (what upstream choices shape the engineering solution). Transfer queries compare both.

This is more complex than the current spike but doesn't require a different algorithm — it's an enrichment of the data model, not a change in the propagation logic.

### Scaling: From 12 Constraints to 100+

**Phase 1 (mechanical):** Map the 18 v2 table columns to Tier 1 + Tier 2 variables. Encode the Phase 1d coupling clusters as constraints. This should produce ~30-40 constraints — enough to reproduce the table's structure computationally.

**Phase 2 (LLM-assisted enrichment):** Run the requirement-primitive-guided derivation loop. For each of P1–P7, systematically check all variable pairs. Target: 80-120 constraints. Validate against the 38-concept dataset.

**Phase 3 (Tier 3 + solution context):** Add design-point variables (discretized continuous). Add solution context annotations. This is where within-family differentiation becomes possible.

**Constraint management:** At 100+ constraints, you need:
- A constraint registry (ID, description, condition, consequence, source, confidence, validation status)
- Automated validation (run all 38 concepts, check for violations)
- Conflict detection (do two constraints produce contradictory consequences for any valid input?)
- Coverage analysis (which variable pairs have no constraints? → gap in knowledge)

This is a software engineering problem, not an algorithm problem. The propagation engine doesn't change.

---

## Key Insight from the Review

The spike validated the ALGORITHM (constraint propagation + ATMS is the right mechanism). What it revealed is that the hard problem is KNOWLEDGE ENGINEERING — systematically building and validating the constraint set.

The constraint derivation protocol (requirement primitives × variable pairs → LLM-generated constraints → dataset validation) is a concrete, automatable path to scaling. The requirement primitives serve their intended role: not as nodes in a graph, but as structured lenses that focus constraint derivation.

The morphospace analogy holds: invest in the constraints, not in the concept representations. The concepts are test cases. The constraints are the knowledge.

---

## Recommended Next Steps

1. **Encode real variables.** Map the 18 v2 table columns into the constraint engine's variable format. Add conditional activation rules (the ones already known from Phase 1b_v2's N/A chains).

2. **Encode real Tier 1 constraints.** Translate the Phase 1d coupling clusters into constraint rules. Target: ~30-40 constraints. Validate: run on all 38 concepts, check that propagation reproduces the known table structure.

3. **Build the LLM derivation pipeline.** Script the requirement-guided constraint derivation loop. Run one round on a few variable pairs to test the protocol. Assess: does the LLM produce valid, non-trivial constraints? What's the false positive rate against the dataset?

4. **Iterate.** Run gap analysis on the expanded constraint set. Identify remaining FREE variables. Target the next derivation round at those gaps.

The goal of steps 1-2 is to confirm the algorithm works at real scale. The goal of steps 3-4 is to test whether LLM-assisted constraint derivation is viable as a scaling mechanism. If step 3 fails (LLM produces mostly garbage constraints), the approach still works but requires manual constraint authoring, which limits scale. If step 3 succeeds, the constraint set becomes a living knowledge artifact that grows with the investigation.
