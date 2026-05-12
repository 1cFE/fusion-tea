# Section 5 (draft): Two concepts traced

**Drop-in replacement for the placeholder Section 5 in `explainer_outline.md`. Sources: the two conformed traces in this directory.**

---

The methodology is useful only if it produces traces that *discriminate*. To demonstrate, we walk two contrasting concepts end-to-end. They sit at opposite ends of the fusion landscape: one engineering-gated and ecosystem-rich, one physics-gated and ecosystem-thin. The trace surfaces exactly that contrast — but it surfaces it in a way categorical labels ("MFE vs. MFE-aneutronic") cannot.

## 01 — HTS Compact Tokamak (CFS ARC)

**Stage 1.** Low discount. Tokamak physics is the most-validated paradigm in fusion, drawing on ITER, JET, JT-60SA, EAST, KSTAR, DIII-D, Alcator C-Mod, and parallel HTS programs at Tokamak Energy. SPARC retires the burning-plasma question within ~24 months. The Stage-1 question — "does the physics work?" — is essentially closed for compact tokamaks.

**Stage 2.** A ~$15B FOAK overnight cost (1 GWe basis from the explorer model; nuclear-island fabricated cost $5.56B for ARC at 400 MWe) is the binding constraint. That cost sits at the upper edge of any private buyer pool — only hyperscaler consortia plus sovereign backstop can absorb it. But the offsetting structural advantage is real: REBCO has fallen from $36–198/m (2014) to ~$20/m (2025), a price reduction CFS's FOAK receives without funding, because non-fusion demand (MRI, grid, accelerators, defense directed-energy, aerospace motors) is pulling the global HTS supply curve down regardless of fusion. The regulatory frame (NRC Part 30, 2026) is a clean leverage pole, sidestepping the 2.2× building-cost penalty a Part-50 fit would impose. Dominant failure: **F2.a** (capital cost). Dominant leverage: **E2.a** (crossover-platform financing via REBCO's non-fusion markets).

**Stage 3.** The chasm tightens around supply rather than demand. Hyperscaler-anchored fleets of 3–10 ARCs are financeable, and Part-30 amortizes cleanly across the fleet. But REBCO capacity announced through 2027 (~10–15k km/yr) does not reach combined fusion-cohort demand at chasm-era deployment — and tritium / Li-6 / Be have no commercial ecosystem at all. The trace commits F3.a to the leverage pole (REBCO weight-dominates CAS22) but tags it bottleneck. The fuel-cycle constraint surfaces as a cross-stage carrier rather than a Stage-3 F-factor — a methodology friction worth noting.

**Stage 4.** Learning is R&D-driven, not volume-driven (low unit count, high unit cost; gas-turbine-like, not solar-like). Five-plus of the six Kavlak knobs have non-fusion ride-along (REBCO conductor R&D rides MRI/grid; FLiBe chemistry rides MSR fission; BOP is commodity). But the specialty-input position is failure-pole: at fleet scale, combined fusion REBCO demand plausibly dominates the conductor market, forcing fusion to drive its own Wright's Law on its dominant CAPEX line — and FLiBe / Li-6 / Be have no external markets to amortize against.

**Concept-level coordinates.** Dominant failure: **Stage 2 / F2.a** (FOAK financing gate). Dominant leverage: **Stage 2 / E2.a** (REBCO crossover-platform pull). The trace's recommended deep-dive format is a **1costingfe extension** — ARC has rich CAS-decomposed cost data and the analysis is parametric in nature, not structural. The three highest-value questions: (1) what capacity factor does the vessel-replacement cycle actually support, (2) what FOAK financing structure closes a $10–15B plant, (3) at what fleet size does the tritium/Li-6/Be supply gap force a step change.

## 18 — p-B11 FRC (TAE Da Vinci)

**Stage 1.** The Stage-1 question is open in a fundamentally different way. p-B11 requires sustained T_i >> T_e at ion temperatures roughly 50–80× higher than current FRC demonstrations, and Q > 1 in the aneutronic regime has never been demonstrated. The methodology treats Stage 1 as a discount, not a gate — but for this concept, the discount cannot capture the actual risk. Da Vinci's commissioning campaign is a binary: below the threshold, there is no LCOE; above it, the rest of the trace applies.

**Stage 2.** The capital story is the inverse of ARC's. Da Vinci targets 50 MWe initial scaling to 350–500 MWe; the explorer model puts overnight cost at $3,089/kW at 1 GWe. Unit cost is hyperscaler-accessible without sovereign backstop. The dominant Stage-2 failure factor, however, is not capital — it is **F2.b** at the failure pole, because the build itself carries the physics-validation cliff. Dominant leverage: **F2.c** at the leverage pole — TAE is the cleanest fit in the candidate set to NRC Part 30. No tritium accountancy, no remote handling, hands-on maintenance. The regulatory advantage is structurally locked in by the fuel choice.

**Stage 3.** Site-specialization is low (resistive copper coils, no FLiBe loop, no breeding blanket), and a hyperscaler can commit to ~12 units in a 600 MWe envelope. Regulatory amortization is strong (F3.d leverage pole). But the dominant subsystem — high-energy NBI (250 keV protons, ~30 MW class) — has no non-fusion industrial supply chain. F3.a sits at the failure pole, bottleneck-tagged, with no MRI-grade ride-along to scale capacity alongside fusion.

**Stage 4.** Learning is R&D-driven (steady-state, sub-1-GWe units cannot reach Wright's Law volumes). The cost-reduction knobs are few and mostly fusion-specific: NBI efficiency, ICC efficiency, Q_plasma, capacity factor. F4.a sits at the failure pole. The single bright spot at Stage 4 is **F4.c at the leverage pole, slack** — B-11 isotope separation is mature, with semiconductor-doping market providing baseline non-fusion demand. p-B11 has the cleanest specialty-input position in the candidate set.

**Concept-level coordinates.** Dominant failure: **Stage 2 / F2.b** (physics-validation cliff at commissioning, mapped to F2.b as the closest rubric code — see Methodology friction below). Dominant leverage: **Stage 2 / F2.c at leverage pole** (Part-30 fit, slack). Deep-dive format: **1costingfe extension with explicit Branch-A/B/C scenario logic** — a viability map, not a central-case LCOE estimator. A SysML structural model would add false precision over a foundational binary.

## What the contrast surfaces

Both concepts die at Stage 2 — but for opposite reasons and under opposite ecosystem positions. ARC dies if the capital pool can't absorb a $15B plant; p-B11 FRC dies if the plasma doesn't converge in commissioning. ARC's leverage is **distinct-E** (a non-fusion industrial market funding its dominant CAPEX line); p-B11's leverage is **ecosystem-relational-F** (a regulatory frame that fits its hazard profile). A naive cross-concept ranking would compare LCOE central estimates and conclude ARC is the "better" concept; the trace shows they are answering different questions, and that an investor reasoning across both learns things that neither concept can teach alone.

The deep-dive format implications also diverge cleanly: ARC's value comes from parametric refinement of a well-anchored cost decomposition; p-B11's value comes from building a viability map that quantifies the regulatory + supply-chain leverage *independent of* the physics binary, so an investor knows what they would be buying if the physics works. Same methodology, opposite analytical artifacts. That is what makes the portfolio informative.

## Methodology friction encountered (footnote)

Both traces flagged real frictions with the rubric. (1) Ecosystem-relational F-factors that aggregate over multiple critical components (F2.d covers REBCO *and* tritium *and* Li-6 for ARC; pole commitment requires a weighting rule). (2) The Stage-1 "discount, not gate" treatment leaves no native vocabulary for physics-viability cliffs that surface at Stage-2 commissioning (p-B11 had to use F2.b as a proxy). Both findings are written up in `worked_examples/methodology_findings.md` with candidate resolutions; they should be folded into the next revision of `concept_part2.md` before applying the trace to the remaining ~36 concepts.
