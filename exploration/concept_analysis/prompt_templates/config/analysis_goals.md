# Analysis Goals

These are the objectives the analysis agent works toward. Every section of the
analysis should contribute to answering these questions.

**What is already fixed upstream (do NOT re-decide):** the concept's confinement
family, its 1costingFE archetype, the fixed list of comparable concepts, and the
named design point (plant name, maturity, native net-electric power `P_native`,
and grounding confidence) are all determined by the upstream tables and arrive
through the analysis frontmatter. They are inputs, not outputs. Your job is not
to choose a family, a nearest neighbour, or a plant — it is to *articulate the
delta* against the fixed comparables and to *extract and account for* the design
point you are given.

1. **Family-Delta Articulation**: Given the fixed comparables, what does this
   design point do differently, and how does that difference move cost? Name the
   specific subsystem, the direction of the cost effect (advantage / penalty /
   neutral), and the magnitude where the data supports it. "It is a tokamak" is
   not a delta; "its all-REBCO TF coils replace the LTS magnets the comparable
   prices at $X/kg" is.

2. **Design-Point Parameter Extraction**: Extract the complete quantitative
   description (geometry, physics, performance) of the *named* design point at
   its *native* scale. Every LCOE-relevant parameter you record must describe
   that one plant — not a different machine, not a different power level, not a
   roadmap aspiration.

3. **TEA Implications**: For each family-delta, state the techno-economic
   consequence. Which differences create cost advantages, which create cost
   penalties, which are cost-neutral, and which are simply unknown for lack of
   data?

4. **Override-Candidate Discovery**: For each canonical 1costingFE account the
   archetype touches, decide whether the dossier names a company-grounded
   quantity, unit cost, or published dollar figure that justifies departing from
   the library default. The library carries the default story; an override is an
   *accountable, evidence-backed* departure from it — not a guess and not an
   optimism adjustment.

5. **Risks and Assumptions**: Are the key risks and assumptions called out, and
   is the analysis honest about what it does not know? How should each be carried
   into the TEA — as a sensitivity parameter, a scenario branch, or an explicit
   data gap?
