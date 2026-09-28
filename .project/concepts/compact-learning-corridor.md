# Concept: Compact-Learning Corridor Dispatch

**Created:** 2026-09-11
**Status:** Draft

---

## Problem Statement

The six-corridors framework (`.project/concepts/six-corridors.md`) defines six structural cost-reduction premises for reaching 1¢/kWh fusion. The first corridor dispatch — the mature magnetic D-T corridor — is published and sets the reference for quality. The sixth corridor, the compact-learning corridor, has no dispatch yet.

This corridor is structurally different from the others. Its premise is not a physics trick or an engineering lever — it is that smallness itself drives cost reduction through three mechanisms: whole-device iteration speed, technology refresh on short cycles, and access to high-value early markets that fund the ride down the learning curve. Solar PV is the reference path. The corridor is physics-gated: conventional confinement favors larger devices, so anything this small needs an exotic regime that no one has demonstrated at fusion conditions.

The dispatch needs to answer: what is the cost floor for a compact fusion device, and does the learning-rate and market-sequencing argument change the picture enough to matter?

---

## Context: What We Know

### The reference dispatch (mature magnetic D-T) establishes the pattern

The published dispatch does five things well:

1. **Names the floor up front.** "2.5 ¢/kWh" in a callout box on the first page, with a one-sentence summary of what carries it and what could break it.
2. **Picks a representative architecture** through two independent published lenses (Brown's configuration lens, Whyte's areal-economics lens), declares the selection, and records the tradeoffs in an attribute matrix.
3. **Costs the representative bottom-up** using 1costingFE, then explains where the cost model's assumptions enter and what it does not cover.
4. **Builds an evidence ladder** — cumulative tiers from design basis (Tier 0) through speculation (Tier 3) — with each cost-down lever graded by the best demonstrated record and the known mechanism for the next tier.
5. **Produces a sensitivity chart** showing what moves the cost most, isolating each lever at its deepest evidence tier.

The conclusion is stated plainly: even at Tier 3 speculation, the corridor does not reach 1¢/kWh.

### Candidate concepts in our analysis

Four concepts from our 38-concept taxonomy sit naturally in this corridor:

| ID | Concept | LCOE ($/MWh) | Notes |
|----|---------|-------------|-------|
| 13 | Electrostatic Hybrid / Orbitron (Avalanche Energy) | 40.9 | 5 kW modules, 1000 needed for 1 GWe. D-T fuel. The low LCOE is an artifact of the automated costing pipeline applying standard CAS scaling to a radically nonstandard device — not a vetted number. |
| 15 | Sheared-Flow Z-Pinch (Zap Energy) | 60.1 | D-T, compact pulsed. The most visible real-world compact concept under active development. Room-scale device. |
| 24 | Dense Plasma Focus (LPP Fusion) | 234.8 | p-B11 fuel. Extremely compact. Also a candidate for corridor 5 (minimal-neutron). |
| 27 | Polywell (D-T) | 60.7 | Electrostatic/magnetic hybrid. No active commercial program. |

Peripheral candidates: Acoustic ICF / Sonofusion (concept 02, $99.5/MWh, very low confidence), Muon-Catalyzed Fusion (concept 16, $2068/MWh). These are more exotic than compact.

### What makes this corridor structurally different

The mature magnetic corridor is an engineering and finance stress test on settled physics. The compact-learning corridor is different in three ways:

1. **The physics gate comes first.** No compact concept has demonstrated Q>1 at fusion conditions. The dispatch cannot assume confinement closes and jump to economics — it has to frame the physics gate explicitly, then run the economics conditional on it closing.

2. **The economics are modular, not monolithic.** The standard TEA framework costs a single large plant. This corridor's premise is that many small units, iterated rapidly, follow a learning curve. The economic argument involves fleet-scale manufacturing cost decline, not single-plant capital optimization. 1costingFE's CAS scaling was not designed for this regime — the $41/MWh for the Orbitron is an example of what happens when you force a 5 kW module through a GW-scale cost model.

3. **The market-sequencing argument matters.** The other corridors target grid-scale baseload. This corridor argues that high-value early markets (remote sites, military, ships) tolerate high initial cost, and that revenue funds iteration. The dispatch needs to evaluate whether this arc is plausible, not just whether the mature fleet LCOE reaches 1¢/kWh.

---

## Ideas for Study and Evaluation

### Approach A: Physics-gate-first, then conditional economics

Structure the analysis in two halves:

**Half 1 — The physics gate.** Survey what confinement performance has been demonstrated in each compact regime (electrostatic, Z-pinch, dense plasma focus, polywell). State what Q, temperature, and confinement time each has reached, and what the gap to breakeven is. This is a literature compilation, not a modeling exercise — the dispatch reports where each concept stands against its own physics requirements.

**Half 2 — Conditional economics.** Assume the physics gate closes for the most plausible candidate(s). Then ask: what does the plant cost? Two sub-questions:

- **Single-unit economics.** What does one compact device cost to build and operate, and what is its LCOE at its native scale (kW to low MW)? This is where 1costingFE can contribute, but the cost model needs to be interrogated for scaling artifacts. The dispatch should be explicit about what the model covers and what it doesn't at this scale.
- **Fleet economics and learning.** If you build thousands of units, what learning rate would be needed to reach grid parity? Compare to observed learning rates for solar PV (~20% per doubling), gas turbines (~10%), and nuclear fission (~0%, negative in the West). State what cumulative production volume corresponds to each price point.

### Approach B: Architecture selection through the "why small" lens

Mirror the mature corridor's architecture selection, but use a different comparison frame. Instead of Brown's configuration lens and Whyte's areal-economics lens, compare compact candidates on:

- **Minimum viable scale** — what is the smallest device that could plausibly reach Q>1?
- **Iteration cycle time** — how long from build to test to rebuild?
- **Technology-refresh surface** — which components can be swapped between builds?
- **Market fit at native scale** — does the device's output match a real demand at its natural size?

Select a representative concept (likely the Z-pinch as most developed, or the Orbitron as most radical), and cost it in detail.

### Approach C: The evidence ladder, adapted

Build an evidence ladder like the mature corridor dispatch, but with tiers appropriate to this corridor:

- **Tier 0 — Current state:** No compact concept has reached breakeven. State the best demonstrated performance.
- **Tier 1 — Physics closure:** Assume Q>1 is demonstrated. What does the single-unit LCOE look like?
- **Tier 2 — Manufacturing learning:** Assume a learning rate consistent with analogous technologies. What cumulative volume reaches grid parity?
- **Tier 3 — Market sequencing:** Assume high-value early markets fund the first N units. Does the path pencil out?

This frames the corridor as a cascade of conditional bets, each testable, rather than a single cost floor.

### Recommended blend

Use Approach C (adapted evidence ladder) as the spine, with Approach A's physics survey as the foundation and Approach B's architecture selection to pick the representative concept(s). The result is a dispatch that:

1. States the physics gate honestly
2. Picks a representative architecture with stated reasoning
3. Costs it at native scale, explicitly noting where 1costingFE's assumptions break
4. Builds a conditional evidence ladder from current state through fleet learning
5. States the floor and what has to be true to reach it

---

## Target Layout (consistent with the reference dispatch)

### I. Introduction

Frame the corridor premise: smallness drives iteration, technology refresh, and market sequencing. State the going-in view from the six-corridors post. Name the floor in a callout box — this will be a conditional floor, something like "X ¢/kWh, conditional on physics closure and a Y% learning rate over Z doublings."

### II. Why compact fusion is hard

The physics gate. Survey what has been demonstrated in each compact regime. State the gap to breakeven plainly. This section replaces the mature corridor's "Why there is no consensus on the best magnetic architecture" — the analog here is "why almost nobody pursues compact confinement."

### III. Choosing an architecture for the corridor

Compare compact candidates on the axes that matter for this corridor (minimum viable scale, iteration speed, technology-refresh surface, market fit). Select one or two representatives. Record the tradeoffs in a comparison matrix analogous to the mature corridor's MCF Attribute Matrix.

### IV. Costing the representative

Bottom-up cost using 1costingFE at the concept's native scale. Be explicit about what the cost model covers and where its assumptions break for a device this small. State the single-unit LCOE at Tier 0 (current design basis, if one exists) and explain the dominant cost accounts.

### V. The evidence ladder

Cumulative tiers, adapted for this corridor:

| Tier | Frame | Content |
|------|-------|---------|
| 0 | Current state | No breakeven demonstrated. State best performance. Single-unit cost at design basis if available. |
| 1 | Physics closure | Assume Q>1. What does single-unit LCOE look like with credible engineering? |
| 2 | Manufacturing scale | Apply learning rates from analog industries. What volume reaches grid parity? |
| 3 | Market-sequenced deployment | High-value early markets fund the first units. Full fleet cost after learning. |

Produce a chart analogous to Figure 3 in the reference dispatch.

### VI. What moves the cost

Sensitivity analysis. For a compact device, the dominant levers will be different from the mature corridor's (where magnets and financing dominate). Likely candidates: Q_eng (because it's near 1, small changes matter enormously), module manufacturing cost, availability at small scale, learning rate. Produce a tornado chart analogous to Figure 4.

### VII. The learning-rate question

This section has no analog in the mature corridor dispatch — it's unique to this corridor. Compare the required learning rate to historical precedents. Solar PV's ~20% learning rate per doubling took decades of cumulative production to reach grid parity. Gas turbines were slower. Nuclear fission never learned. State what the compact fusion arc would need and whether that is consistent with any observed technology trajectory.

### VIII. Conclusion

State the floor, the conditions, and whether the corridor reaches 1¢/kWh under any plausible combination. The mature corridor's conclusion is: "Even with the most speculative plant-wide assumptions applied simultaneously, this corridor does not reach 1¢/kWh." This corridor's conclusion will likely be more conditional: something like "the corridor could reach X if [physics gate] and [learning rate] and [market access], but none of those conditions has been demonstrated."

### Appendix — Basis of estimates

Analogous to the reference dispatch's appendix. Document the specific assumptions, model configurations, and data sources.

---

## Non-Goals / Out of Scope

- **[AGENT]** Building new cost models for compact concepts. The dispatch uses existing 1costingFE runs, interrogated for scaling artifacts, not purpose-built compact-device models.
- **[AGENT]** Resolving the physics gate. The dispatch reports the current state and frames the economics conditional on closure. It does not attempt to assess whether any compact regime will actually reach Q>1.
- **[AGENT]** Detailed market analysis for military, remote, or maritime applications. The dispatch references these as the market-sequencing premise but does not model demand curves or willingness-to-pay.
- **[AGENT]** Covering corridors 2-5. Each corridor gets its own dispatch.

## Open Questions

1. **Which concept to select as representative?** The Z-pinch (Zap Energy) is the most developed and funded. The Orbitron (Avalanche) is the most radical and tests the premise hardest. The dispatch might need both — one as the "most plausible" and one as the "purest embodiment of the premise."
2. **How to handle the learning-rate argument quantitatively?** We could build a simple Wright's law model (cost = a × cumulative_volume^(-b)) and show what b needs to be. Or we could stay qualitative and compare to precedents. The former is more rigorous; the latter may be all the evidence supports.
3. **Where does the Z-pinch sit across corridors?** Zap Energy's device is compact, but it's also pulsed — it could live in corridor 2 (pulsed-plant) as easily as corridor 6. The dispatch needs to be clear about why it belongs here, or acknowledge the overlap.
4. **What does 1costingFE actually produce for these concepts?** The $41/MWh for the Orbitron and $61/MWh for the Z-pinch come from the automated pipeline. Before writing the dispatch, these numbers need to be inspected for scaling artifacts. The dispatch should show its work on where the model's assumptions break.

---

## Next-Stage Handoff

**Settled here:**
- **[AGENT]** The dispatch follows the mature magnetic corridor's structure (floor callout → architecture selection → bottom-up costing → evidence ladder → sensitivity → conclusion), adapted for this corridor's structural differences.
- **[AGENT]** The physics gate is reported, not resolved. The economics are conditional.
- **[AGENT]** The learning-rate and market-sequencing arguments get their own section, unique to this corridor.

**Needs resolution next:**
- Representative concept selection (one or two?)
- Quantitative vs. qualitative treatment of the learning-rate argument
- Inspection of 1costingFE outputs for scaling artifacts at compact scale
- Whether to build any new model runs or rely entirely on existing pipeline data
