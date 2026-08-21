# Design Point Reasoning Trace — 14-magnetized-target-fusion-pneumatic-compression

## 1. Sources walked

- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/dossier.md` — synthesized summary; used for orientation, schema confidence values, and source inventory
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-fst-2025-fuel-cycles.md` — Hildebrand/Flynn et al. FST 2025 peer-reviewed paper; the most specific public technical document on the GF MTF commercial power plant: confirms ~4 m cavity diameter, pneumatic piston array, DT fuel, liquid metal wall (Li or PbLi), commercial tritium fuel cycle parameters
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-iaea-fec-2025-abstract.md` — Hildebrand et al. IAEA FEC 2025 abstract; confirms LM26 is 50% plasma scale of the commercial machine, uses electromagnetic theta-pinch of solid lithium liner (surrogate), no electrical output
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-lm26-milestones-2025.md` — April 2025 LM26 first plasma compression announcement; confirms LM26 demo machine identity and milestone context, no electrical output statement
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-01/sources/general-fusion-technology-overview.md` — GF website technology overview; confirms concept description, liquid metal wall, pulsed approach; limited quantitative content (sparse extraction)
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-01/sources/general-fusion-technical-details.md` — COMSOL 2025 article on LM26 and commercial MTF concept; confirms "repeats once per second in a commercial plant," confirms LM26 uses electromagnetic compression as surrogate, commercial plant uses pneumatic pistons
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-03/sources/generalfusion-fusion-demo-plant/output.md` — GF commercialization path page (generalfusion.com/commercialization-path/); describes Lawson Program (LM26), commercialization engineering program, and FOAK plant targeting energy production around 2035; confirms engineering breakeven goal; no P_native stated
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-04/sources/en-wiki-general-fusion/output.md` — Wikipedia article on General Fusion; states "MTF power plant proposed by General Fusion would produce about 300 MWe from two 150 MW machines running in tandem" (citing Krotez et al. 2023, 30th IEEE SOFE); describes cancelled UK Fusion Demonstration Program (70% scale, 1 pulse/day, no electrical output, put on hold 2023)
- `knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-04/sources/globenewswire-news-release-2022-12-12-2571959-0-en-general/output.md` — GlobeNewswire Dec 2022 press release; documents plasma and compression prototype milestones; confirms plasma injector and compression testbed technology status
- `exploration/concept_analysis/analyses/14-magnetized-target-fusion-pneumatic-compression/analysis.md` — prior D1+ analysis; used as reference to orient to source list and cross-check parameter values already synthesized; not used as primary source authority per prompt instructions

---

## 2. Candidates surfaced

**Candidate A — LM26 (Lawson Machine 26)**

LM26 is General Fusion's current large-scale demonstration machine, operational since late 2024 at the Vancouver headquarters. It is explicitly described as a 50% plasma scale of the commercial machine. The compression mechanism is an electromagnetic theta-pinch that collapses a solid lithium liner — a deliberate engineering surrogate for the commercial pneumatic liquid-metal system. LM26 runs on deuterium only (no tritium). The design's stated goals are to achieve 10 keV ion temperature by 2025 and Lawson criterion (nTτ > 10²¹ m⁻³·keV·s) by 2026. No electrical output is part of the design or claimed. Maturity status: operating physics demonstrator. **P_native: none — no electrical output by design. Does not qualify.**

**Candidate B — Fusion Demonstration Program (UK / Culham)**

Between 2021 and 2023, General Fusion announced and partially developed a 70% scale prototype at the UK Atomic Energy Authority's Culham campus, with a reported cost of US$400M. Wikipedia documents its key differences from the commercial plant: 70% scale, 1 pulse per day (vs. 1 Hz commercial), helium-driven rather than steam/hydraulic pistons, and liquid lithium rather than lead-lithium. The plant was designed to demonstrate plasma physics and compression at near-scale — not to produce electricity. In 2023, General Fusion placed this program on hold in order to redirect resources to LM26, a different machine focused on demonstrating scientific breakeven. No electrical output was ever part of the Fusion Demonstration Program concept. Maturity status: partially designed, on hold / cancelled. **P_native: none — no electrical output by design. Does not qualify.**

**Candidate C — GF MTF Commercial Power Plant (Krotez et al. 2023 SOFE conceptual design)**

The Krotez, Segas, Khalzov, and Suponitsky paper presented at the 30th IEEE Symposium on Fusion Engineering (July 2023) is the most recent published conceptual design for General Fusion's commercial MTF power plant. Wikipedia quotes it directly: "the MTF power plant proposed by General Fusion would produce about 300 MWe from two 150 MW machines running in tandem." The FST 2025 peer-reviewed paper (Flynn et al.) treats this as the design under study, confirming ~4 m cavity diameter, pneumatic piston drivers, liquid metal wall (Li or PbLi under evaluation), DT fuel, and ~1 Hz repetition rate. The GF commercialization roadmap targets a FOAK implementation of this design producing energy at commercial scale around 2035. Architecture: two 150 MWe modules operating in tandem. Maturity: paper-concept (published conceptual design; no commercial-scale pneumatic liquid-metal hardware demonstrated). **P_native: 150 MWe per module.** The plant total (300 MWe) is the sum of two natural replication units, not a single machine's output.

---

## 3. Selection

The only candidate with a published electrical design point is **Candidate C — the GF MTF Commercial Power Plant, Krotez et al. 2023 SOFE conceptual design**. Candidates A (LM26) and B (UK Fusion Demonstration Program) both lack electrical output by design and are disqualified under the selection rule. Candidate C is the company's authoritative published commercial design, with geometry (4 m cavity), driver (pneumatic piston array), fuel (DT), and power output (two 150 MWe modules) all documented across a peer-reviewed paper (FST 2025) and a conference conceptual design (Krotez 2023).

The architecture is explicitly two-module: two 150 MWe machines run in tandem to produce 300 MWe at the plant level. Per the multi-module rule, P_native is the per-module value (150 MWe), because that is the natural replication unit the 1 GWe comparison scales by module count. Scaling the 300 MWe plant total to 1 GWe would imply growing each individual machine to 300 MWe — a design that does not exist in any published source.

```yaml
proposal:
  concept_id: 14-magnetized-target-fusion-pneumatic-compression
  design_name: "GF MTF Commercial Power Plant — Krotez et al. 2023 SOFE conceptual design (150 MWe per module, two-module architecture)"
  maturity_tier: paper-concept
  p_native_mwe: 150
  primary_sources:
    - knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-04/sources/en-wiki-general-fusion/output.md
    - knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-fst-2025-fuel-cycles.md
  selection_rationale: |
    The Krotez et al. 2023 SOFE conceptual design is the only GF design with a
    published electrical output: 300 MWe from two 150 MWe modules in tandem, as
    reported by Wikipedia citing that paper directly. The FST 2025 peer-reviewed
    paper (Flynn et al.) treats this as the design under study and grounds its
    geometry (~4 m cavity), pneumatic piston driver, and DT fuel cycle parameters.
    LM26 and the cancelled UK Fusion Demonstration Program both lack electrical
    output by design and do not qualify. P_native is the per-module value (150 MWe)
    because the design's natural architecture is two independent 150 MWe machines
    running in tandem; scaling to 1 GWe adds modules, not grows the machine.
  alternatives_considered:
    - design: "LM26 (Lawson Machine 26)"
      reason_rejected: no electrical output by design — 50% plasma scale physics demonstrator using electromagnetic theta-pinch surrogate
      sensitivity_implication: "LM26 has no P_native and cannot serve as a design point. If LM26 or a successor produces unexpected electrical output data, revisit whether a sub-commercial design-point option becomes available. No directional LCOE shift applies — this is a route-to-freeform branch, not a P_native choice."
    - design: "Fusion Demonstration Program (UK / Culham, 70% scale)"
      reason_rejected: no electrical output by design — 70% scale physics prototype, on hold since 2023, 1 pulse/day repetition rate
      sensitivity_implication: "No P_native; not a qualifying design point regardless of scale. If GF had built the UK FDP through to a net-electricity phase (which was never planned), it would have represented a sub-commercial pilot rather than a commercial design — routing to a different maturity tier, not a competing P_native."
```

---

## 4. Open questions

- **Krotez et al. 2023 SOFE paper not directly ingested.** The primary authority for the two-module 150 MWe architecture is a conference paper (30th IEEE SOFE, E-267) that is referenced in Wikipedia but not present as a primary extraction in the source tree. Wikipedia's characterization ("about 300 MWe from two 150 MW machines") may be paraphrasing rather than quoting. If the paper states a different module count or per-module power (e.g., a single 300 MWe machine or a different phase of the design), the P_native would shift. Ingesting that paper directly would confirm or correct this selection's load-bearing claim.

- **FOAK plant (2035) design-point consistency.** The GF commercialization roadmap describes a FOAK plant producing energy at commercial scale around 2035 with an "integrated commercial-scale MTF machine." It is not confirmed whether this FOAK plant uses the Krotez 2023 two-module architecture unchanged or a revised design with different geometry or P_native. If GF publishes engineering parameters for the FOAK plant (e.g., through a CDR-level document or partnership announcement with Hatch/CNL), revisit whether P_native changes from 150 MWe.

- **Liquid metal composition selection.** Li vs. PbLi remains unresolved as of the sources available. This does not affect P_native or the design-point selection, but it is a prerequisite for populating cost model branches downstream. Once GF announces the commercial liquid metal selection, the fuel cycle cost structure bifurcates (ISS-dominant for PbLi; blanket-extraction-dominant for Li).

- **Post-LM26 design revision risk.** LM26's results (compression ratio achieved, plasma parameters) could drive a geometry change in the commercial design if the ~4 m cavity or 350-fold volumetric compression target proves infeasible at that scale. A redesign to a smaller or larger cavity would change the two-module P_native. Watch for GF's IAEA FEC 2026 abstract, which targets Lawson criterion demonstration and may include updated commercial design parameters.