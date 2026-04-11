# HTS Tokamak - Full HTS (D-T)

**Company**: Energy Singularity
**Last updated**: 2026-03-06
**Iterations completed**: 3
**Overall confidence**: medium

## Summary

Energy Singularity is a Shanghai-based company building the world's first fully HTS tokamak — all toroidal field, poloidal field, and central solenoid coils use REBCO high-temperature superconductor. Their prototype HH70 (26 coils: 12 TF, 6 PF, 8 CS) achieved a 1,337-second steady-state plasma in February 2026 across 5,755 total shots, with toroidal field upgraded from 0.6 T to >1 T after a December 2024 cryogenic upgrade. Their Jingtian prototype magnet reached 21.7 T peak field (later sources report 22.4 T), surpassing the CFS/MIT 20 T record. The next machine, HH170, targets Q > 10 at ~14 T on-axis (~110% of SPARC) in ~70% of SPARC volume using D-shaped HTS magnets targeting 25 T peak field, with completion expected by 2027. The demo power station HH380 is planned post-2030.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by research
- **Notes**: Standard magnetic confinement via tokamak geometry.

### Confinement Concept
- **Value**: Compact tokamak
- **Confidence**: high
- **Citation**: Research iter-01 — HH170 is ~70% of SPARC volume with higher field; iter-02 confirms "world's smallest and lowest-cost tokamak capable of Q > 10"
- **Notes**: Full HTS enables compact design. All coils (TF, PF, CS) are REBCO — unique among tokamak concepts. HH70 major radius 0.75 m, minor radius ~0.25-0.31 m.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by research
- **Notes**: Standard deuterium-tritium fuel cycle. HH170 targets "D-T equivalent" Q > 10 — may not actually burn D-T fuel in that machine.

### Primary Heating
- **Value**: RF (ICRH)
- **Confidence**: medium
- **Citation**: Research iter-01/iter-02 — ICRF confirmed on HH70; electron gun used for pre-ionization
- **Notes**: ICRH confirmed on the HH70 prototype. Electron gun used for pre-ionization (not primary heating). Heating plan for HH170 and production machines not publicly disclosed; may differ from prototype.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: Research iter-01 — standard D-T inference; iter-02 confirms no disclosure
- **Notes**: No company-specific disclosure found across two research iterations. Inferred from D-T fuel cycle (14.1 MeV neutrons require thermal conversion). HH380 engineering details not yet public.

### Plasma State
- **Value**: Burning
- **Confidence**: medium
- **Citation**: Research iter-01 — HH170 targets Q > 10
- **Notes**: HH170 targets Q > 10, which implies alpha-heating-dominated plasma. HH70 is sub-burning (experimental prototype). Classification based on target commercial operation.

### Magnet Type
- **Value**: HTS (wound)
- **Confidence**: high
- **Citation**: Research iter-01/iter-02 — Jingtian magnet 21.7-22.4 T peak field, all-REBCO coil set
- **Notes**: Distinguishing feature: ALL coils (TF, PF, CS) are REBCO HTS — 26 coils total on HH70 (12 TF, 6 PF, 8 CS). Jingtian prototype magnet achieved 21.7 T peak field (later sources report 22-22.4 T; company website now lists 22 T). Most other HTS tokamak concepts use HTS for TF coils only.

### Tritium Breeding
- **Value**: TBD
- **Confidence**: high (that it's TBD)
- **Citation**: Research iter-01/iter-02 — extensive search across 15+ English and Chinese sources found no disclosure
- **Notes**: No blanket technology disclosed. Confirmed across 3 iterations and 20+ sources. Structurally unresolvable at current company stage: HH70 is experimental (no D-T, no neutrons), HH170 targets "D-T equivalent" Q > 10 but may not burn D-T, and HH380 (where blanket design becomes critical) is post-2030. China's CFETR program is developing WCCB, HCCB, and sCO2-cooled LiPb blankets which could influence future choice, but no connection to Energy Singularity exists yet.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: medium
- **Citation**: Research iter-01/iter-02 — physics-based inference from D-T fuel; no company-specific disclosure found
- **Notes**: Inferred from D-T fuel cycle producing 14.1 MeV neutrons. No company-specific shielding or blanket design disclosed. Could be upgraded to `Integrated blanket/shield` if blanket details emerge.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by HH70 achieving 1,337-second steady-state plasma (Feb 2026, shot #5,755)
- **Notes**: Long-pulse steady-state demonstrated on prototype. AI-based plasma control system used.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Schema rule — steady-state concept
- **Notes**: N/A — continuous operation, not pulsed.

### Driver Technology
- **Value**: HTS magnets (REBCO, 25 T)
- **Confidence**: high
- **Citation**: Research iter-02 — HH170 D-shaped HTS magnets target 25 T peak field; Jingtian demonstration at 21.7-22.4 T
- **Notes**: Full HTS coil set (TF + PF + CS) is the key technology differentiator. 25 T reflects HH170 target peak field for D-shaped magnets (upgrade from iter-01's "22+ T" estimate). Jingtian prototype demonstrated 21.7 T (some sources: 22.4 T). >96% domestic component localization rate.

## Remaining Gaps

| Column | Current State | What's Been Searched | Potential Resolution |
|--------|--------------|---------------------|---------------------|
| Primary Heating | Medium — HH70 ICRH confirmed, HH170 plan unknown | General web research (2 iterations), Chinese-language sources | ScienceDirect commissioning paper (paywalled); HH170 engineering publications if/when released |
| Energy Capture | Medium — generic D-T inference | General web research (2 iterations) | HH380 engineering publications if/when released (post-2030) |
| Plasma State | Medium — based on Q > 10 target | General web research (2 iterations) | HH170 physics design papers |
| Tritium Breeding | TBD — structurally unresolvable | 15+ sources across English/Chinese; company website (blocked) | Unlikely to resolve before HH380 engineering phase (post-2030) |
| Neutron Management | Medium — physics inference only | General web research (2 iterations) | HH170/HH380 engineering design publications |

**Recommendation**: This concept is research-complete for differentiation table purposes. Three iterations and 20+ sources have been exhausted. The remaining gaps are structurally unresolvable — they depend on engineering decisions Energy Singularity hasn't made yet (HH380 is post-2030). The ScienceDirect HH70 commissioning paper remains the only unexplored source (paywalled), but it covers an experimental machine (no D-T) and is unlikely to address blanket, shielding, or power conversion design.

## Key Sources

1. Research iteration 1 output (iter-01/output.md) — web research on Energy Singularity, HH70, HH170, Jingtian magnet
2. Research iteration 2 output (iter-02/output.md) — targeted research on tritium breeding, HH170 magnet specs, Chinese-language sources
3. Research iteration 3 output (iter-03/output.md) — final confirmation pass; no new data found across 8 targeted searches
3. Xinhua: Shanghai's "artificial sun" achieves new tech breakthrough (Feb 2026) — https://english.news.cn/20260206/31e447b7e3504b0d802ef705556f66ef/c.html
4. InterestingEngineering: Energy Singularity seeks $500M — https://interestingengineering.com/energy/500m-target-record-holding-hh70-tokamak
5. 36kr: Chinese private enterprise fusion profile — https://eu.36kr.com/en/p/3399945429878919
6. NextBigFuture: World's First Fully HTS Tokamak — https://www.nextbigfuture.com/2024/07/worlds-first-fully-high-temperature-superconducting-tokamak-is-chinas-hh70.html
7. FusionEnergyBase: HH70 project page — https://www.fusionenergybase.com/projects/hh70
8. IAEA World Fusion Outlook 2025 — Jingtian magnet featured — https://www-pub.iaea.org/MTCD/publications/PDF/p15935-25-02871E_WFO25_web.pdf
9. ScienceDirect (paywalled): "Design, commissioning, and first operation of HH70" — Fusion Engineering and Design, 2025
10. ScienceDirect (paywalled): "Development and construction of magnet system for world's first full HTS tokamak"
11. Baseline concept CSV — initial company/concept identification
