# Design Point Reasoning Trace — 15-sheared-flow-stabilized-z-pinch

## 1. Sources walked

- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/dossier.md` — synthesized taxonomy summary; used for orientation, device roadmap, and confirming which sources are authoritative
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/engineering-paradigms-paper-summary.md` — Thompson, Levitt, Nelson, Shumlak, *Fusion Science and Technology* 2023; the primary engineering reference for the commercial core concept: 200 MWt thermal per core, 19 MJ/pulse × 10 Hz, LiPb blanket (TBR ~1.1), plasma parameters (Table I), driver efficiency ~70%, core geometry (~3 m diameter, ~25 m³)
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/century-demo-system.md` — Zap Energy October 2024 press release ($130M Series D / Century operations start); contains the only published net electrical output figure: "a single Zap Energy module that will produce 50 megawatts of electricity"
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/zap-energy-website-how-it-works.md` — Zap Energy "How It Works" website; confirms DT fuel, 10 Hz commercial rep rate, no-magnet architecture; no electrical output figure
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/fuze-q-and-fuze-3.md` — FuZE device series overview; confirms FuZE-Q and FuZE-3 are physics R&D devices with no electrical output by design
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-02/sources/century-and-fuze-a-updates-2025.md` — APS DPP 2025 abstract (Levitt); confirms Century, FuZE-3, FuZE-A as engineering/physics platforms; no electrical output data
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-02/sources/fuze-3-gigapascal-results-2025.md` — FuZE-3 Nov 2025 gigapascal results; plasma performance data; no electrical output
- `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-03/sources/osti-servlets-purl-2588719/output.md` — LLNL-JRNL-2001600 "Challenges and Gaps in Pulsed Power for Fusion" 2025; driver maturity context, not P_native
- `exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/analysis.md` — prior D1+ analysis; consulted for cross-checks; not used as a primary source

## 2. Candidates surfaced

**Candidate A — Zap Energy SFS Z-Pinch Commercial Power Plant Module (Thompson et al. FST 2023 + Zap October 2024)**

The commercial design is described across two sources that must be read together. The Engineering Paradigms paper (Thompson et al., *FST* 2023) establishes the core geometry (~3 m diameter, ~25 m³ volume), thermal power (200 MWt nominal maximum per core, consistent with 19 MJ/pulse × 10 Hz = 190 MWt), LiPb blanket (TBR ~1.1), driver efficiency (~70%), and plasma parameters at commercial scale (1.2–1.5 MA, 30–35 keV, 200 µs). It does not state a net electrical output. The October 2024 Series D press release adds the only published net electrical figure: "Century...is close to the eventual size of a single Zap Energy module that will produce 50 megawatts of electricity. Future power plants will have multiple modules." This is a VP-attributed company statement, not a derived engineering result. No named pilot plant or intermediate commercial design is described anywhere in the source set.

Implied P_native: **50 MWe per module** (multi-module architecture confirmed; P_native is the per-module value).
Maturity status: paper-concept.
Published data: geometry (3 m, 25 m³), thermal power (200 MWt), fuel (DT), driver efficiency (~70%), LiPb blanket. Net electrical output stated in press release only; steam cycle design proprietary/undisclosed.

**Candidate B — FuZE / FuZE-Q / FuZE-3 devices**

Physics R&D devices. No electrical output by design. TRL 2–3. Not eligible.

**Candidate C — Century engineering platform**

100 kW average input power, non-DT (liquid bismuth, non-fusing) engineering test platform. No electrical output by design. Not eligible.

**Candidate D — FuZE-A (upcoming)**

Next physics device under development. No electrical output by design. Not eligible.

## 3. Selection

**Selected: Candidate A — Zap Energy SFS Z-Pinch Commercial Power Plant Module**

Candidate A is the only design in Zap Energy's portfolio with a published P_native. All other candidates are physics demonstrators or engineering test platforms with no electrical output by design. The selection rule resolves immediately: there is only one eligible design.

The 50 MWe figure comes from a VP-attributed sentence in the October 2024 Series D press release. The Engineering Paradigms paper (the only peer-reviewed engineering document) gives 200 MWt thermal but does not state net electrical. Because the 50 MWe is an official company statement in a funding announcement — not back-of-envelope in a physics paper — it is treated as the design-point P_native. It is broadly consistent with 200 MWt at ~35–37% net efficiency (~66–74 MWe gross minus ~15–25 MWe recirculating), though the thermal cycle design and recirculating power breakdown are not publicly documented.

The architecture is explicitly multi-module. P_native is the per-module electric power (50 MWe); n_mod = 20 at 1 GWe.

```yaml
proposal:
  concept_id: 15-sheared-flow-stabilized-z-pinch
  design_name: "Zap Energy SFS Z-Pinch Commercial Power Plant Module (Thompson et al. FST 2023; Zap October 2024)"
  maturity_tier: paper-concept
  grounding_confidence: medium
  p_native_mwe: 50
  primary_sources:
    - knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/engineering-paradigms-paper-summary.md
    - knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/century-demo-system.md
  selection_rationale: |
    Zap Energy publishes one commercial-scale design: a multi-module power plant whose
    natural unit is a single SFS Z-pinch core. The Engineering Paradigms paper
    (Thompson et al., FST 2023) establishes the module's thermal power (200 MWt), geometry
    (~3 m diameter, ~25 m³ core), fuel (DT), LiPb blanket (TBR ~1.1), and driver efficiency
    (~70%), but does not state net electrical output. The October 2024 Series D press release
    adds the single published electrical figure: "a single Zap Energy module that will
    produce 50 megawatts of electricity; future power plants will have multiple modules."
    P_native is the per-module value (50 MWe) to preserve the natural replication unit;
    n_mod = 20 at 1 GWe. No other commercial design with a P_native exists in the source
    set — the FuZE device series and Century are physics/engineering platforms with no
    electrical output by design.
  alternatives_considered:
    - design: "FuZE / FuZE-Q / FuZE-3 devices (Zap Energy physics R&D platform)"
      reason_rejected: no electrical output by design; physics demonstrators at TRL 2–3
      sensitivity_implication: >-
        n/a — these devices have no P_native and cannot serve as a design point;
        they are precursors to, not substitutes for, the commercial module concept
    - design: "Century engineering test platform (October 2024)"
      reason_rejected: non-DT (liquid bismuth, non-fusing), 100 kW input power, no electrical output by design
      sensitivity_implication: >-
        n/a — Century has no P_native; it is an engineering validation platform,
        not a candidate commercial design
    - design: "FuZE-A (upcoming physics device)"
      reason_rejected: physics R&D platform under development; no electrical output by design
      sensitivity_implication: >-
        n/a — FuZE-A has no P_native; it is the next step in the physics program,
        not a commercial design
```

## 4. Open questions

- **The 50 MWe claim is not derived in any published document.** The Engineering Paradigms paper gives 200 MWt thermal; the press release asserts 50 MWe net. At 200 MWt and 30% Rankine efficiency, gross electric is ~66 MWe; subtracting ~28 MWe recirculating driver load (from Q = 10 + 70% efficiency) yields ~38 MWe net — below the stated 50 MWe. Closing this gap requires either higher Rankine efficiency (~37–38%) or a lower recirculating fraction than the Q = 10 derivation implies. A published power balance would resolve this and could move grounding confidence from medium toward high.

- **No named pilot plant design exists.** The portfolio jumps from Century (100 kW engineering platform) to "commercial module." If Zap Energy defines and publishes a pilot plant, that design should replace or supplement this selection; a pilot would likely have a different P_native.

- **Module count per commercial plant is not published.** Multi-module architecture is confirmed but the commercial plant module count is unstated. This does not affect P_native but affects plant-level capital cost and economies-of-scale modeling downstream.

- **Q > 10 is calculated, not demonstrated.** The 50 MWe figure implicitly relies on Q > 10 to achieve positive net output. If FuZE-A or subsequent experiments establish an achievable Q significantly below 10, the net electrical projection is invalidated. Should this occur, the design point should be reconsidered and may route to freeform.

---

The document is ready to write. Please approve the write to `exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/design-points/proposal.md` and I'll save it.