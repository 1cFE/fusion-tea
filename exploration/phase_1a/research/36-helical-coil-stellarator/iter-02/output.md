Now let me compile the complete verified dossier output.

---

# Helical Coil Stellarator (D-T) — Iteration 2 Research Findings

This iteration focused on verifying and strengthening all existing column values, with particular attention to the medium-confidence Energy Capture value and the unspecified liquid metal composition.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); all company materials
- **Notes**: Magnetic confinement via continuous helical coils in a stellarator/heliotron configuration. No ambiguity.

### Confinement Concept
- **Value**: Stellarator (helical coil)
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "a kind of stellarator called heliotron composed of two continuous helical coils"
- **Notes**: Confirmed. The specific geometry is a heliotron — two continuous helical winding coils in a double-helix (DNA-like) structure, directly derived from the LHD at NIFS. The company uses "Helical-Stellarator" or "helical stellarator" terminology. Distinct from modular coil stellarators (W7-X/Proxima) and planar coil stellarators (Thea Energy).

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "deuterium-tritium fusion reactor, where tritium is self-produced using liquid metal blanket systems"
- **Notes**: Confirmed. No suggestion of advanced fuels.

### Primary Heating
- **Value**: RF (ECRH)
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "electron cyclotron heating is adopted for plasma heating"; R&D on 250 GHz, 1 MW, CW gyrotrons
- **Notes**: Confirmed. ECRH via gyrotrons is the primary and seemingly sole heating method. No plasma current drive needed (inherent stellarator advantage), making NBI unnecessary. The company is developing 250 GHz / 1 MW continuous-wave gyrotrons jointly with QST.

### Energy Capture
- **Value**: Thermal (sCO2)
- **Confidence**: medium
- **Citation**: Helical Fusion collaborative research list mentions "power generation systems (CO2 gas turbines)"; NIFS Oroshhi-2 sCO2 demonstration plan (Ishiyama & Tanaka, Fusion Science and Technology 75:8, 2019) targeting >50% efficiency at 800-1200 K
- **Notes**: Evidence strengthened but not conclusive. Three supporting data points: (1) Helical Fusion lists "CO2 gas turbines" among 14 collaborative research areas; (2) The NIFS research infrastructure (Oroshhi-2) includes an sCO2 gas turbine demonstration plan; (3) The liquid metal blanket at high temperature is well-suited for sCO2 Brayton cycle. However, no single source explicitly states "HESTIA uses an sCO2 Brayton cycle as its power conversion system." This remains the only medium-confidence value.

### Plasma State
- **Value**: Burning
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — fusion gain Q~13, steady-state operation on the order of a year
- **Notes**: Confirmed. With Q~13, alpha heating significantly dominates external heating. The stellarator advantage is that no recirculating power is needed for current drive, so Q~13 is sufficient for net electricity at modest scale (50 MWe).

### Magnet Type
- **Value**: HTS (3D stellarator)
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); ANS Nuclear Newswire 2025-10-29 — 40 kA at 7 T, 15 K; WISE conductor uses stacked REBCO tapes
- **Notes**: Confirmed and strengthened with new details. The October 2025 milestone demonstrated an **uninsulated** large-scale HTS coil (world's first) — 30 layers of REBCO, conductor cross-section ~3 cm, length >4 m. Target field: 8 T at coil center. Uses proprietary WISE (Wound and Impregnated Stacked Elastic tapes) conductor — flexible REBCO tape stacking + low-melting-point alloy impregnation for structural rigidity. Dedicated coil manufacturing machine completed with Sugino Machine; assembly of Helix HARUKA to begin 2026.

### Tritium Breeding
- **Value**: Liquid metal wall
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "modular-type Liquid Metal blanket"; "liquid metal free-surface flow" covers first wall including divertor
- **Notes**: Confirmed. The liquid metal blanket serves triple duty: tritium breeding, neutron shielding, and first-wall protection via free-surface flow. GALOP test system at NIFS validates gas-driven liquid metal pump (no rotating components). **Specific liquid metal composition remains unconfirmed** — the FFHR heritage used FLiBe (molten salt), but HESTIA explicitly says "liquid metal" (distinct from molten salt). The NIFS Oroshhi-2 platform has LiPb loops, suggesting LiPb is one candidate. Structural material is high-Mn austenitic steel (Tohoku University collaboration, 2024).

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — liquid metal blanket with free-surface first wall; ANS 2025-10-29 — "integrated blanket/divertor system"
- **Notes**: Confirmed. The ANS article explicitly uses the phrase "integrated blanket/divertor system" as one of two key technology pillars for Helix HARUKA. Liquid metal blanket provides combined tritium breeding, neutron moderation/capture, heat removal, and first-wall protection. 14.1 MeV D-T neutron environment.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); company tagline "world's first steady-state fusion reactor"
- **Notes**: Confirmed. True steady-state is the defining advantage. No plasma current → no current drive power → no disruption risk. Target: continuous operation ~1 year, followed by ~3-month maintenance. Commercial requirements explicitly include "steady operation" (per Interesting Engineering article on coil manufacturing).

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed burn cycle. No change.

### Driver Technology
- **Value**: Continuous helical HTS coils (REBCO WISE conductor, 8 T) + 250 GHz CW gyrotrons
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); ANS Nuclear Newswire 2025-10-29; Sugino Machine collaboration announcement
- **Notes**: Confirmed and strengthened. Two key technology bets: (1) WISE HTS conductor enabling continuous helical coils — the October 2025 milestone demonstrated 40 kA at 7 T in a no-insulation configuration, and a dedicated manufacturing machine is completed; (2) 250 GHz CW ECRH gyrotrons for steady-state plasma heating.

## Remaining Gaps

1. **Energy Capture** (medium confidence): This is the only remaining gap. Three independent data points support sCO2 (collaborative research listing, NIFS Oroshhi-2 sCO2 demo plan, thermal compatibility with liquid metal blanket), but no source explicitly confirms "HESTIA baseline power conversion = sCO2 Brayton cycle." The full text of the AIP paper (behind paywall) may contain this information. Alternatively, a conference presentation or investor deck might state it directly. Confidence cannot be raised to high without a direct statement.

2. **Tritium Breeding — specific liquid metal composition**: The liquid metal type (pure Li, LiPb, Sn-alloy, or other) is not publicly confirmed. The FFHR heritage used FLiBe (molten salt), but HESTIA explicitly moved to "liquid metal." The NIFS Oroshhi-2 has LiPb loops. The Tohoku University collaboration developed corrosion-resistant structural steel, which suggests the liquid metal may be corrosive (consistent with Li or LiPb). The full AIP paper may specify this.

3. **Thermal power output**: Only 50 MWe (electric) is stated. With Q~13 and ~40% conversion efficiency (typical for sCO2), thermal power would be ~125 MWth — but this is inference, not a stated value.

## Sources Consulted

### Primary Sources (yielded useful information)
- [AIP Physics of Plasmas 30, 050601 (2023) — abstract](https://ui.adsabs.harvard.edu/abs/2023PhPl...30e0601M/abstract) — HESTIA design paper
- [ANS Nuclear Newswire (2025-10-29) — HTS coil milestone](https://www.ans.org/news/2025-10-29/article-7500/helical-fusion-marks-milestone-in-progress-toward-fusion-power/)
- [BusinessWire (2025-10-26) — Milestone press release](https://www.businesswire.com/news/home/20251026597002/en/)
- [BusinessWire (2025-12-04) — Series A Extension](https://www.businesswire.com/news/home/20251204842199/en/)
- [Interesting Engineering — Japan steady-state reactor](https://interestingengineering.com/energy/nuclear-fusion-reactor-japan-launch)
- [Interesting Engineering — coil manufacturing machine](https://interestingengineering.com/energy/japan-fusion-startup-completes-coil-manufacturing)
- [Helical Fusion — GALOP announcement](https://global.helicalfusion.com/post/helical-fusion-unveils-galop-a-groundbreaking-liquid-metal-blanket-testing-system-essential-for-co)
- [Helical Fusion — Sugino Machine collaboration](https://global.helicalfusion.com/post/helical-fusion-completes-a-new-coil-manufacturing-machine-for-its-integrated-demonstration-device-in)
- [Helical Fusion — Tohoku University materials](https://www.helicalfusion.com/en/post/helical-fusion-inc-and-tohoku-university-s-institute-for-materials-research-pioneer-revolutionary-m)
- [Ishiyama & Tanaka (2019) — sCO2 demo plan at Oroshhi-2](https://www.semanticscholar.org/paper/Demonstration-Plan-of-Nuclear-Fusion-Power-by-CO2-Ishiyama-Tanaka/c65a8bee89527829427288e4fe2a278409abad6e)
- [Tanaka & Sagara — Oroshhi-2 FLiNaK/LiPb twin loops](https://www.semanticscholar.org/paper/Liquid-Blanket-Collaboration-Platform-Oroshhi-2-at-Tanaka-Sagara/6aa3a1a42420da041a9d98e1bb46169e57112b79)
- [OUCI — AIP paper alternate access](https://ouci.dntb.gov.ua/en/works/9QaJMdm9/)
- [CoLab — AIP paper alternate access](https://colab.ws/articles/10.1063/5.0145222)

### FFHR Heritage Sources
- [Sagara et al. — FLiBe blanket for FFHR (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0022311597001542)
- [Sagara et al. — FLiBe blanket design and development](https://www.sciencedirect.com/science/article/abs/pii/S0920379600003604)
- [FFHR-c1 evaluation (ResearchGate)](https://www.researchgate.net/publication/273037050_An_evaluation_of_fusion_gain_in_the_compact_helical_fusion_reactor_FFHR-c1)

### Sources Attempted but No New Information
- Helical Fusion R&D page (global.helicalfusion.com/rd) — Wix site, content didn't render
- AIP full paper (pubs.aip.org) — 403 forbidden (paywall)
- MDPI Energies 16(11):4430 — 403 forbidden; this appears to be about a different stellarator (DEMO-like), not HESTIA
- Clean Energy Platform — general fusion industry overview, no Helical Fusion specifics
- World Nuclear News — Japanese supermarket chain fusion power agreement (tangential)
