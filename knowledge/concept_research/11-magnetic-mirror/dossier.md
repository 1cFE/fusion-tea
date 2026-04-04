# Magnetic Mirror (D-T)

**Company**: Realta Fusion
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

Realta Fusion (founded 2022, UW-Madison spin-out) is developing compact, scalable, modular (CoSMo) fusion energy based on the axisymmetric tandem magnetic mirror. Their key innovation is using HTS REBCO magnets to achieve mirror ratios of 10+ (vs historical ~2), which they argue resolves the end-loss problem that historically killed mirror machines. The development pathway is WHAM (simple mirror, operational 2024, 17 T) → Anvil (end-plug demonstrator, ~2028) → Hammir (tandem mirror pilot plant, mid-2030s, targeting Q > 5, Qe > 1, >50 MWe). The open-ended linear geometry enables hybrid energy capture: thermal blanket for neutrons (which also breeds tritium from lithium) plus direct energy conversion (venetian blinds) for charged particles escaping through the ends. Performance scales at ~7 MW per meter of center cell length.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: Schema definition — magnetic mirror is steady-state magnetic confinement
- **Notes**: Magnetic mirror is explicitly listed under MFE in the schema. Linear open geometry with magnetic confinement.

### Confinement Concept
- **Value**: `Magnetic mirror`
- **Confidence**: high
- **Citation**: https://realtafusion.com/technology/; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion; https://thefusionreport.substack.com/p/interview-with-realta-fusion
- **Notes**: Specifically an axisymmetric tandem mirror. Central cell flanked by two end-plug mirror cells that create electrostatic plugging potentials to reduce end losses. Realta's proprietary design name is CoSMo (Compact, Scalable, Modular). Bottle-shaped geometry: strong HTS magnets at ends, weaker solenoid in central cell.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — "DT fuel" explicitly stated; https://thefusionreport.substack.com/p/interview-with-realta-fusion — "DT fuel for first generation systems"
- **Notes**: Confirmed as primary fuel cycle for first-generation systems. No mention of planned transition to advanced fuels.

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/ — WHAM uses ECH + NBI + HHFW; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — NBI for end-plug density, ECH for electron heating; https://arxiv.org/abs/2411.06644 — "modern neutral beams" for pilot plant
- **Notes**: Combines NBI (primary, for end-plug fueling and density), ECH (electron heating and end-plug potential), and HHFW RF (ion acceleration). `RF + NBI` is the best schema fit. Specific RF types include ECRH (110 GHz gyrotron) and HHFW.

### Energy Capture
- **Value**: `Hybrid (thermal + direct)`
- **Confidence**: high
- **Citation**: https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — "axisymmetric ferromagnetic venetian blinds" for direct energy conversion; https://thefusionreport.substack.com/p/interview-with-realta-fusion — "neutron energy is captured through traditional thermal blankets... charged helium 'ash' is captured via direct energy conversion as it exits the fusion chamber"
- **Notes**: Dual-channel: (1) neutron energy captured in thermal blanket, (2) charged particles escaping through open ends captured via direct energy conversion using venetian blinds. This lowers the Q threshold for net electricity. Performance scales at ~7 MW per meter of center cell length, theoretical 500 MW from Q=20. Specific thermal cycle (steam vs sCO2) not disclosed. MARS study achieved ~54% direct conversion efficiency. Near-term applications emphasize industrial heat delivery.

### Plasma State
- **Value**: `Sustained`
- **Confidence**: medium
- **Citation**: Inferred from steady-state operation mode and Q > 5 target; https://arxiv.org/abs/2411.06644; https://thefusionreport.substack.com/p/interview-with-realta-fusion — Q > 10 possible with longer center cell
- **Notes**: Steady-state operation with continuous NBI and RF heating. At Q > 5, alpha heating is significant but NBI/ECH still dominate — fits `Sustained` rather than `Burning` (which implies alpha-dominated heating at Q >> 5). If Q > 10-20 is achieved (longer center cell variant), the boundary becomes fuzzy, but the base Hammir design is clearly `Sustained`.

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/ — REBCO HTS magnets from CFS, 17 T; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — HTS REBCO magnets, mirror ratio 10+
- **Notes**: REBCO HTS magnets wound into axisymmetric solenoid/mirror coils. WHAM uses two CFS-built magnets achieving 17 T in bore (>20 T on conductor). Mirror geometry requires simple axisymmetric coils, not 3D stellarator shapes. End magnets are stronger, mid-section solenoid magnets are weaker — a stated cost advantage.

### Tritium Breeding
- **Value**: `Li blanket (unspecified)`
- **Confidence**: medium
- **Citation**: https://thefusionreport.substack.com/p/interview-with-realta-fusion — "thermal blankets (which also produce tritium from lithium)"
- **Notes**: The Fusion Report interview explicitly states the blanket produces tritium from lithium. However, the specific blanket type (FLiBe, LiPb, liquid Li, solid ceramic) is not disclosed. Historical MARS study used Li17Pb83 (LiPb) with TBR of 1.15, but Realta may choose differently. Linear geometry simplifies blanket design vs toroidal devices. Hammir pre-conceptual design paper (expected 2026) may specify the blanket type.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: https://thefusionreport.substack.com/p/interview-with-realta-fusion — blanket captures neutrons AND breeds tritium; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — "reactor blanket" for neutron energy capture
- **Notes**: D-T produces 14.1 MeV neutrons. The Fusion Report interview confirms the blanket serves dual purposes (energy capture + tritium breeding), which is the definition of `Integrated blanket/shield`. The linear central cell geometry naturally lends itself to a surrounding cylindrical integrated blanket/shield (as in the MARS study). Specific shielding architecture not yet published by Realta.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://meetings-archive.aps.org/dpp/2025/gm12/2/ — Hammir targets 3+ hours continuous operation; schema notes mirrors are characteristically steady-state
- **Notes**: Magnetic mirrors are inherently steady-state — no pulsed plasma current, no disruptions. The 3-hour target is a demonstration milestone, not a physical pulse length limit. NBI and ECH run continuously.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept — repetition rate not applicable
- **Notes**: N/A — continuous operation, not pulsed.

### Driver Technology
- **Value**: `HTS mirror magnets (REBCO, 17+ T) + NBI + ECH`
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion; https://arxiv.org/abs/2411.06644; https://thefusionreport.substack.com/p/interview-with-realta-fusion
- **Notes**: Key technology bets: (1) HTS REBCO magnets enabling mirror ratios of 10+ (vs historical ~2), fundamentally changing confinement viability; (2) Modern NBI for end-plug sustainment; (3) ECH/HHFW for electron heating and ion acceleration. Direct energy conversion via venetian blinds is a secondary but important technology element. Cost advantage: longer center cell uses cheaper, weaker solenoid magnets (~7 MW per additional meter).

## Remaining Gaps

1. **Tritium Breeding** (medium confidence): Upgraded from `TBD` to `Li blanket (unspecified)` in iter-02. The specific blanket type (FLiBe, LiPb, liquid Li, HCPB) remains undisclosed. The Hammir pre-conceptual design paper (expected 2026) should specify this. Not worth another research iteration — needs the published paper.

2. **Neutron Management** (medium confidence): `Integrated blanket/shield` is well-supported by the dual-purpose blanket description but Realta has not published specific shielding architecture details. Unlikely to resolve further without the Hammir design paper.

3. **Plasma State** (medium confidence): `Sustained` is correct for the base Q > 5 Hammir design. Could become `Burning` at Q > 10-20 (longer center cell variant). Low priority — value is defensible.

4. **Energy Capture specifics**: Thermal cycle type (steam vs sCO2) undisclosed. DEC efficiency numbers not given by Realta (MARS achieved ~54%). Not a schema gap but useful for downstream cost modeling.

## Key Sources

1. [Fusion Hub - Startup Spotlight: Realta Fusion](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion) — Most detailed technical source: DT fuel, NBI+ECH, REBCO magnets, venetian blind DEC, stabilization. Saved: `iter-01/sources/realta-fusion-hub-spotlight.md`
2. [The Fusion Report - Interview with Realta Fusion](https://thefusionreport.substack.com/p/interview-with-realta-fusion) — Key iter-02 source: confirms lithium-based tritium breeding, DEC for charged particles, ~7 MW/m scaling. Saved: `iter-02/sources/fusion-report-interview-realta.md`
3. [arXiv 2411.06644 - Confinement predictions for Hammir](https://arxiv.org/abs/2411.06644) — Q > 5 modeling, 50m center cell, DCLC management. Saved: `iter-01/sources/arxiv-2411-06644-confinement-predictions.md`
4. [APS DPP 2025 - Sutherland talk](https://meetings-archive.aps.org/dpp/2025/gm12/2/) — Anvil as end-plug demonstrator, Hammir targets Qe>1 and >50 MWe. Saved: `iter-01/sources/aps-dpp-2025-sutherland.md`
5. [WHAM experiment website](https://wham.physics.wisc.edu/) — 17 T REBCO, ECH+NBI+HHFW, first plasma July 2024. Saved: `iter-01/sources/wham-experiment-details.md`
6. [Realta Fusion Q>5 modeling PR](https://www.prnewswire.com/news-releases/realta-fusion-models-commercially-viable-energy-gain-in-magnetic-mirror-power-plant-302523527.html) — Hammir Q>5, DCLC instability management
7. [MARS study](https://www.semanticscholar.org/paper/The-Mirror-Advanced-Reactor-Study-(MARS)-Logan/1dda92c411abd0ea6f2a8c2ab7e3c523c30c887f) — Historical context: LiPb blanket, TBR 1.15, direct conversion
8. [CFS magnet delivery to WHAM](https://cfs.energy/news-and-media/commonwealth-fusion-systems-delivers-hts-magnets-to-uw-wham-project/)
9. [Realta Fusion $9.5M SVB facility (Feb 2026)](https://www.prnewswire.com/news-releases/realta-fusion-secures-9-5-million-growth-capital-facility-from-silicon-valley-bank-a-division-of-first-citizens-bank-302689285.html) — Funding update, industrial heat focus
10. [MARS study (OSTI)](https://www.osti.gov/biblio/5981974) — Historical reference: LiPb blanket, 36% plant efficiency, gridless direct converters
