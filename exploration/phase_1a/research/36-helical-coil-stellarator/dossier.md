# Helical Coil Stellarator (D-T)

**Company**: Helical Fusion
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: high

## Summary

Helical Fusion is a Tokyo-based startup spun out from Japan's National Institute for Fusion Science (NIFS), developing a heliotron-type stellarator using two continuous helical HTS coils in a double-helix (DNA-like) geometry derived from the Large Helical Device (LHD). The concept targets steady-state D-T burning plasma at Q~13 with a published 50 MWe reactor design (HESTIA), using proprietary WISE REBCO conductor for 3D coil fabrication, 250 GHz continuous-wave gyrotrons for ECRH heating, and a liquid metal blanket system that serves as integrated first wall, tritium breeder, and neutron shield. The stellarator approach eliminates disruption risk and current drive power requirements, enabling true steady-state operation (~1 year continuous burns with ~3-month maintenance cycles). An integrated demonstration device (Helix HARUKA) is planned for assembly beginning 2026.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); company website
- **Notes**: Magnetic confinement via continuous helical coils in a stellarator/heliotron configuration.

### Confinement Concept
- **Value**: Stellarator (helical coil)
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "a kind of stellarator called heliotron composed of two continuous helical coils"
- **Notes**: The specific geometry is a heliotron — a stellarator variant using two continuous helical winding coils in a double-helix structure, directly derived from the LHD at NIFS. Distinct from modular coil stellarators (W7-X/Proxima Fusion) and planar coil stellarators (Thea Energy). The company sometimes uses the term "Helical-Stellarator."

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "deuterium-tritium fusion reactor, where tritium is self-produced using liquid metal blanket systems"
- **Notes**: Confirmed D-T fuel cycle with tritium self-sufficiency via blanket breeding.

### Primary Heating
- **Value**: RF (ECRH)
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "electron cyclotron heating is adopted for plasma heating"; joint research with QST on ECRH; R&D on 250 GHz, 1 MW, CW gyrotrons
- **Notes**: ECRH via gyrotrons is the primary and seemingly sole heating method. The company is developing 250 GHz / 1 MW continuous-wave gyrotrons jointly with QST. No mention of NBI as supplementary heating. Consistent with heliotron physics — no current drive needed, making NBI unnecessary.

### Energy Capture
- **Value**: Thermal (sCO2)
- **Confidence**: medium
- **Citation**: Helical Fusion collaborative research list mentions "power generation systems (CO2 gas turbines)"; Ishiyama & Tanaka, Fusion Science and Technology 75:8 (2019) — NIFS Oroshhi-2 sCO2 gas turbine demonstration plan targeting >50% efficiency at 800-1200 K
- **Notes**: Evidence strengthened by iteration 2 but not yet conclusive. Three supporting data points: (1) Helical Fusion lists "CO2 gas turbines" among 14 collaborative research areas; (2) The NIFS research infrastructure (Oroshhi-2) includes an sCO2 gas turbine demonstration plan; (3) The liquid metal blanket at high temperature is well-suited for sCO2 Brayton cycle. However, no single source explicitly states "HESTIA uses an sCO2 Brayton cycle as its power conversion system." This remains the only medium-confidence value.

### Plasma State
- **Value**: Burning
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — fusion gain Q~13, steady-state operation on the order of a year
- **Notes**: With Q~13, alpha heating significantly exceeds external heating. The stellarator advantage is that no recirculating power is needed for current drive, so Q~13 is sufficient for net electricity even at modest scale (50 MWe).

### Magnet Type
- **Value**: HTS (3D stellarator)
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); ANS Nuclear Newswire 2025-10-29 — 40 kA at 7 T, 15 K; WISE conductor uses stacked REBCO tapes
- **Notes**: Uses proprietary WISE (Wound and Impregnated Stacked Elastic tapes) conductor made from stacked REBCO tapes. Designed for flexibility in 3D helical coil winding, then impregnated with low-melting-point alloy for structural rigidity. Target field: 8 T at coil center. The October 2025 milestone demonstrated a world-first uninsulated large-scale HTS coil — 30 layers of REBCO, conductor cross-section ~3 cm, length >4 m. Continuous helical winding (not modular) is a distinguishing feature. Dedicated coil manufacturing machine completed with Sugino Machine; assembly of integrated demonstration device Helix HARUKA to begin 2026.

### Tritium Breeding
- **Value**: Liquid metal wall
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "modular-type Liquid Metal blanket"; "liquid metal free-surface flow" covers first wall including divertor; GALOP test system
- **Notes**: The liquid metal blanket serves triple duty: tritium breeding (lithium content), neutron shielding, and first-wall protection via free-surface flow. Eliminates the need for a separate divertor system. GALOP test system at NIFS validates a gas-driven liquid metal pump (no rotating components). Specific liquid metal composition remains unconfirmed — the FFHR heritage used FLiBe (molten salt), but HESTIA explicitly says "liquid metal" (distinct from molten salt). The NIFS Oroshhi-2 platform has LiPb loops, suggesting LiPb is one candidate. Structural material is high-Mn austenitic steel (Tohoku University collaboration, 2024).

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — liquid metal blanket with free-surface first wall; ANS Nuclear Newswire 2025-10-29 — "integrated blanket/divertor system"
- **Notes**: The ANS article explicitly describes the "integrated blanket/divertor system" as one of two key technology pillars for Helix HARUKA. Liquid metal blanket provides combined tritium breeding, neutron moderation/capture, heat removal, and first-wall protection. 14.1 MeV D-T neutron environment. Free-surface liquid metal flow on the first wall provides continuous surface renewal and eliminates plasma-facing component erosion concerns.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "steady-state operation is principally possible on the order of a year"; company tagline references "world's first steady-state fusion reactor"
- **Notes**: True steady-state operation is the defining advantage of the heliotron/stellarator approach. No plasma current means no current drive power and no disruption risk. Target: continuous operation for ~1 year, followed by ~3-month maintenance period, yielding >80% availability.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed burn cycle.

### Driver Technology
- **Value**: Continuous helical HTS coils (REBCO WISE conductor, 8 T) + 250 GHz CW gyrotrons
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); ANS Nuclear Newswire 2025-10-29; Sugino Machine collaboration announcement
- **Notes**: Two key technology bets: (1) WISE HTS conductor enabling continuous helical coils for the heliotron geometry — the October 2025 milestone demonstrated 40 kA at 7 T in an uninsulated configuration, and a dedicated manufacturing machine is completed; (2) high-power CW ECRH gyrotrons at 250 GHz for steady-state plasma heating. Coil manufacturing approach (flexible REBCO tape stacking + low-melting-point alloy impregnation) is proprietary.

## Remaining Gaps

1. **Energy Capture** (medium confidence): Three independent data points support sCO2 (collaborative research listing, NIFS Oroshhi-2 sCO2 demo plan, thermal compatibility with liquid metal blanket), but no source explicitly confirms "HESTIA baseline power conversion = sCO2 Brayton cycle." The full text of the AIP paper (behind paywall) may contain this information. Alternatively, a conference presentation or investor deck might state it directly. Confidence cannot be raised to high without a direct statement.

2. **Tritium Breeding — specific liquid metal composition**: The liquid metal type (pure Li, LiPb, or other) is not publicly confirmed. HESTIA explicitly says "liquid metal" (distinct from FFHR's FLiBe molten salt). The NIFS Oroshhi-2 has LiPb loops, and the Tohoku University collaboration on corrosion-resistant high-Mn steel is consistent with a corrosive liquid metal (Li or LiPb). The full AIP paper may specify this.

3. **Thermal power output**: Only 50 MWe (electric) is stated. Thermal power can be estimated from Q~13 and conversion efficiency but isn't directly stated.

## Key Sources

1. AIP Physics of Plasmas 30, 050601 (2023) — Primary reactor design paper (HESTIA); abstract at https://ui.adsabs.harvard.edu/abs/2023PhPl...30e0601M/abstract
2. ANS Nuclear Newswire (2025-10-29) — HTS coil milestone: https://www.ans.org/news/2025-10-29/article-7500/helical-fusion-marks-milestone-in-progress-toward-fusion-power/
3. BusinessWire (2025-10-26) — Milestone press release: https://www.businesswire.com/news/home/20251026597002/en/
4. BusinessWire (2025-12-04) — Series A Extension ($5.5M): https://www.businesswire.com/news/home/20251204842199/en/
5. Helical Fusion website: https://www.helicalfusion.com/en (redirects to global.helicalfusion.com)
6. Helical Fusion GALOP blanket test system announcement: https://www.helicalfusion.com/en/post/helical-fusion-unveils-galop-a-groundbreaking-liquid-metal-blanket-testing-system-essential-for-co
7. ResearchGate — WISE conductor paper: https://www.researchgate.net/publication/346465961
8. Sugino Machine coil manufacturing collaboration: https://global.helicalfusion.com/post/helical-fusion-completes-a-new-coil-manufacturing-machine-for-its-integrated-demonstration-device-in
9. Springer — Helical Fusion Reactor Concepts chapter: https://link.springer.com/chapter/10.1007/978-3-031-17711-8_9
10. Ishiyama & Tanaka (2019) — sCO2 demo plan at Oroshhi-2, Fusion Science and Technology 75:8: https://www.semanticscholar.org/paper/Demonstration-Plan-of-Nuclear-Fusion-Power-by-CO2-Ishiyama-Tanaka/c65a8bee89527829427288e4fe2a278409abad6e
11. Tanaka & Sagara — Oroshhi-2 FLiNaK/LiPb twin loops: https://www.semanticscholar.org/paper/Liquid-Blanket-Collaboration-Platform-Oroshhi-2-at-Tanaka-Sagara/6aa3a1a42420da041a9d98e1bb46169e57112b79
12. Helical Fusion — Tohoku University materials collaboration: https://www.helicalfusion.com/en/post/helical-fusion-inc-and-tohoku-university-s-institute-for-materials-research-pioneer-revolutionary-m
13. Interesting Engineering — Japan steady-state reactor: https://interestingengineering.com/energy/nuclear-fusion-reactor-japan-launch
14. Interesting Engineering — coil manufacturing machine: https://interestingengineering.com/energy/japan-fusion-startup-completes-coil-manufacturing
