# Ecosystem Markets Brief — Prompt

You are producing a short, fact-dense markdown reference document that will be reused as input to multiple per-concept fusion down-selection traces. The down-selection methodology distinguishes:

- **Ecosystem-relational F-factors** — concept's position relative to external (non-fusion) ecosystems. Failure pole = no external support, must internalize. Leverage pole = strong external supply, ride existing scale-up. Carries a *slack* (external demand has headroom) or *bottleneck* (combined demand strains supply) qualifier.
- **Distinct E-factors** — independent leverage mechanisms (crossover-platform financing, talent inflow) with no failure counterpart.

The traces need consistent facts about adjacent-industry markets per critical fusion component. Write a brief covering ONLY the components below. For each: external market size, growth trend, current/projected supply state (slack vs. bottleneck through ~2035), and which fusion concepts depend on it (where known). Use citations inline (paper, year, or org+year). Mark unknowns explicitly as `[unknown]` rather than guessing.

## Components to cover

1. **REBCO HTS tape** — global production capacity, $/kA-m trajectory 2014–2026, non-fusion demand drivers (MRI, grid, motors, accelerators, defense), bottleneck risk if combined fusion fleet demand materializes ~2030–2035.
2. **High-power lasers (kJ-class, MJ-class, high-rep-rate)** — industrial laser market scale, defense pulsed-laser programs, IFE-specific gaps (rep rate, wall-plug efficiency). Who makes them, what's their non-fusion revenue.
3. **Pulsed-power capacitors and Marx generators** — defense (NIF, Z-machine, IMG), commercial (medical, accelerator), capacitor industrial supply. Bottleneck risk for FRC/Z-pinch/MagLIF fleet.
4. **FLiBe / Li-6 / Be** — current production scale (any source), enrichment capacity for Li-6, beryllium toxicology constraints, fusion-specific bottleneck severity.
5. **Tritium** — current global inventory (CANDU + military), breeding required at fleet scale, kg/year supply gap.
6. **Cryogenic D-T target fabrication** — only IFE-relevant. Current capacity (NIF, OMEGA), industrial scale required for rep-rated IFE.
7. **Boron-11 (enriched p-B11 fuel)** — current isotope-separation capacity, market price, scale-up barriers, non-fusion demand (semiconductor doping, control rods).

For each, end with a 1-line **assessment for fusion downselection**: which pole is the current state and whether the trajectory is slack-likely or bottleneck-likely at fleet scale.

## Output format

Markdown. ~150–300 words per component. Use H2 per component. Cite inline. No preamble, no closing. Begin directly with `## REBCO HTS tape`.

## Audience and use

This becomes a shared reference; subsequent prompts will paste it inline. Density and citability matter more than prose. Don't editorialize — facts and assessments only.
