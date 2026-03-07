# Negative Triangularity Tokamak (D-T)

**Company**: Firefly Fusion
**Last updated**: 2026-03-06
**Iterations completed**: 3
**Overall confidence**: medium

## Summary

Firefly Fusion is developing a compact, high-field tokamak optimized for negative triangularity (NT) plasma shape, which stabilizes the plasma edge and improves heat exhaust compared to conventional positive-triangularity tokamaks. The company targets a major radius of 2-2.5 m with 10-12 T magnetic field using HTS magnets commercially (copper for the LUCIOLE prototype). NT plasmas have been experimentally validated on DIII-D (General Atomics) and TCV (EPFL/SPC). The closest published reference design is MANTA (Rutherford et al. 2024), a community academic study for an NT ARC-class pilot plant producing 450 MW fusion power at Q=11.5. Co-founder Justin Ball's research explores whether compact high-field NT tokamaks could operate with ohmic heating alone, eliminating auxiliary heating systems entirely. Firefly is very early-stage (founded 2024) with minimal public technical detail beyond high-level parameters.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by all sources
- **Notes**: Standard magnetic confinement tokamak.

### Confinement Concept
- **Value**: `Negative triangularity tokamak`
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by all sources including [GreyB interview](https://greyb.com/blog/firefly-fusion-scouted-interview), [DIII-D collaboration page](https://d3dfusion.org/fireflyfusion/)
- **Notes**: Plasma has inverted "D" cross-section. Prototype device named LUCIOLE.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: Baseline CSV. GreyB interview mentions "superheated hydrogen plasma" but does not explicitly name D-T; however the company targets burning plasma (Q>5) which is only feasible with D-T at these parameters.
- **Notes**: D-T is the only fuel cycle consistent with the target Q and device size.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: medium
- **Citation**: [Venture Kick profile](https://www.venturekick.ch/firefly-fusion) — "utilizing microwaves to create and control hot plasma"
- **Notes**: "Microwaves" suggests ECRH, but three competing hypotheses now exist: (1) ECRH — from Venture Kick "microwaves" language; (2) ICRH — the MANTA reference design uses ICRF at 40 MW / 110 MHz with He3 minority heating, with no ECRH in the design ([Rutherford et al. 2024](https://arxiv.org/abs/2405.20243)); (3) Ohmic-only — co-founder Ball's research ([Balestri, Ball, Coda 2024](https://arxiv.org/html/2407.06439v2)) explores eliminating auxiliary heating entirely. Firefly advisor Bucalossi directs IRFM/WEST which uses ICRH + LHCD + ECRH. Kept at ECRH/medium per merge rules (only direct Firefly source), but actual heating choice is genuinely uncertain.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: Inferred — D-T concept with no disclosed energy conversion approach. Schema notes: "Most D-T concepts default to Thermal (unspecified) unless they've explicitly stated their cycle choice."
- **Notes**: No source discusses energy capture or power conversion. Firefly website (March 2026) discloses no technical parameters. Default assignment per schema convention.

### Plasma State
- **Value**: `Burning`
- **Confidence**: medium
- **Citation**: [GreyB interview](https://greyb.com/blog/firefly-fusion-scouted-interview) — Q > 5, 50-100 MW fusion power with 20-30 MW heating input. Baseline CSV uses "burning plasma" language.
- **Notes**: Q > 5 is at the boundary between Sustained and Burning. Company explicitly uses "burning plasma" framing. Ball et al. analyze scenarios with Q > 10, which is firmly Burning. MANTA achieves Q=11.5 ([Rutherford et al. 2024](https://arxiv.org/abs/2405.20243)), consistent with Burning classification.

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: high
- **Citation**: [GreyB interview](https://greyb.com/blog/firefly-fusion-scouted-interview) — "HTS superconducting magnets, 10-12 T"; [Fusion Energy Base](https://www.fusionenergybase.com/organizations/firefly-fusion) — confirms phased strategy; [DIII-D page](https://d3dfusion.org/fireflyfusion/) — "actively-cooled copper magnets" for LUCIOLE; MANTA uses REBCO HTS at 11 T on-axis with demountable TF coils ([Rutherford et al. 2024](https://arxiv.org/abs/2405.20243))
- **Notes**: Phased approach: copper magnets for LUCIOLE prototype (enabling rapid iteration), HTS for commercial plants. Table value reflects commercial target. MANTA's REBCO HTS design confirms this is the standard approach for NT ARC-class tokamaks.

### Tritium Breeding
- **Value**: `TBD`
- **Confidence**: low
- **Citation**: No Firefly source discusses tritium breeding or blanket design.
- **Notes**: As a D-T concept, tritium breeding is required. MANTA reference design uses FLiBe liquid immersion blanket (TBR 1.15) with toroidally continuous tank serving dual breeder/coolant/shield function ([Rutherford et al. 2024](https://arxiv.org/abs/2405.20243)). If Firefly follows ARC-class heritage, `FLiBe blanket` is the likely value, but no company disclosure exists. Founded 2024 — blanket design likely not yet determined.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: low
- **Citation**: MANTA reference design uses FLiBe blanket that provides both tritium breeding and neutron shielding in one system ([Rutherford et al. 2024](https://arxiv.org/abs/2405.20243)); iter-02 source `manta-reference-design.md`
- **Notes**: Previous value was `Heavy shielding (14 MeV)` (low confidence, inferred from D-T fuel). Updated to `Integrated blanket/shield` (low confidence) based on MANTA proxy — the FLiBe blanket explicitly serves dual purpose as breeder and shield. Both values are low confidence since Firefly has not disclosed their approach. `Integrated blanket/shield` is more specific and aligns with ARC-class heritage. Per schema: "Use `Integrated blanket/shield` when the blanket explicitly serves dual purpose (CFS FLiBe...)."

### Operation Mode
- **Value**: `Quasi-steady`
- **Confidence**: medium
- **Citation**: MANTA reference design ([Rutherford et al. 2024](https://arxiv.org/abs/2405.20243)) — ~15 min inductive pulses with 2 min inter-pulse; Ball et al. ohmic-only research implies inductive/pulsed operation
- **Notes**: Reclassified from `Steady-state` (baseline CSV "Continuous") → `Quasi-steady` per schema v0.2 rule: pulse > 5 min = Quasi-steady. Multiple lines of evidence override the CSV: (1) MANTA is pulsed with ~15 min burns; (2) Ball's ohmic-only research implies inductive operation; (3) MANTA uses a large central solenoid for inductive current drive. Firefly website (March 2026) does not clarify.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: medium
- **Citation**: Follows from Operation Mode = Quasi-steady per schema v0.2.
- **Notes**: N/A per schema: quasi-steady concepts use N/A for repetition rate. MANTA's ~15 min pulses with 2 min inter-pulse are long-burn, not discrete pulsed events.

### Driver Technology
- **Value**: `HTS magnets + NT plasma shaping`
- **Confidence**: medium
- **Citation**: [GreyB interview](https://greyb.com/blog/firefly-fusion-scouted-interview) — 10-12 T HTS magnets; [DIII-D page](https://d3dfusion.org/fireflyfusion/) — NT plasma shape is the core innovation
- **Notes**: The distinguishing technology bet is the combination of high-field HTS magnets with negative triangularity geometry. NT is not just a plasma shape choice but a confinement optimization that claims to reduce required heating power by 5x. MANTA demonstrates this with only 23.5 MW power to SOL for a 450 MW fusion plant.

## Remaining Gaps

| Column | Current Status | What's been searched | What might resolve it |
|--------|---------------|---------------------|----------------------|
| **Primary Heating** | Medium confidence (ECRH from "microwaves"), but three competing hypotheses (ECRH, ICRH, ohmic-only) | Venture Kick, GreyB interview, Ball et al. paper, MANTA design, Firefly website | Direct Firefly technical publication or conference presentation. MANTA uses ICRH which weakens the ECRH inference. Unlikely to resolve without new Firefly disclosure. |
| **Energy Capture** | Medium confidence (default Thermal) | All sources — none discuss power conversion, including Firefly website | Firefly technical documentation. Unlikely to be resolved until company matures. |
| **Tritium Breeding** | TBD (MANTA uses FLiBe as proxy) | All sources — none discuss blanket; MANTA provides proxy | Firefly technical documentation. FLiBe is likely given ARC-class heritage but unconfirmed. |
| **Neutron Management** | Low confidence (Integrated blanket/shield from MANTA proxy) | All sources; MANTA design provides best proxy | Linked to tritium breeding — blanket choice determines neutron management. |
| **Operation Mode** | **Resolved** — reclassified to `Quasi-steady` per schema v0.2. MANTA and Ball evidence now aligned with value. | CSV, all sources, MANTA design, Ball et al. | Confidence remains medium; direct Firefly statement would raise to high. |

Further iterations are unlikely to resolve gaps without new Firefly publications, conference presentations, or FIA member profile updates. The company is very early-stage (founded 2024) and its website (as of March 2026) discloses no reactor parameters. **Iteration 3 confirmed this assessment** — no new technical information was found. A patent search turned up an unrelated spherical tokamak NT application. Firefly joined the Impulse deep-tech incubator near ITER/CEA Cadarache, but with no technical content. Recommend marking this concept as research-complete at current confidence levels.

## Key Sources

1. **GreyB / Scouted Interview with CEO Rustem Ospanov** — https://greyb.com/blog/firefly-fusion-scouted-interview — Key technical parameters (R=2-2.5m, B=10-12T, Q>5, P_fusion=50-100MW). Saved: `iter-01/sources/greyb-firefly-interview.md`
2. **MANTA Reference Design (Rutherford et al. 2024)** — https://arxiv.org/abs/2405.20243 — Closest published NT tokamak reference design. 450 MW, Q=11.5, pulsed, ICRF heating, FLiBe blanket. Saved: `iter-02/sources/manta-reference-design.md`
3. **DIII-D National Fusion Facility Collaboration Page** — https://d3dfusion.org/fireflyfusion/ — Confirms DIII-D collaboration, LUCIOLE prototype, copper magnets for prototype. Saved: `iter-01/sources/firefly-fusion-diii-d-collaboration.md`
4. **Balestri, Ball, Coda (2024) — Ohmic NT Tokamak Feasibility** — https://arxiv.org/html/2407.06439v2 — Academic basis for ohmic-only NT operation at compact high-field parameters. Saved: `iter-01/sources/ball-balestri-ohmic-nt-paper.md`
5. **Venture Kick Profile** — https://www.venturekick.ch/firefly-fusion — "Microwaves" heating mention, CHF 50k funding. Saved: `iter-01/sources/venture-kick-profile.md`
6. **Fusion Energy Base Profile** — https://www.fusionenergybase.com/organizations/firefly-fusion — Confirms phased magnet strategy, location, founding date. Saved: `iter-01/sources/fusion-energy-base-profile.md`
7. **Firefly Fusion Website (March 2026)** — https://fireflyfusion.energy/ — Team/advisor bios, no technical parameters disclosed. Saved: `iter-02/sources/firefly-website-2026.md`
