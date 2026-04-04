# HTS Compact Tokamak (D-T)

**Company**: Commonwealth Fusion Systems
**Last updated**: 2026-03-06
**Iterations completed**: 4
**Overall confidence**: high

## Summary

Compact high-field tokamak using HTS REBCO magnets achieving 20+ T field strength, enabling a fusion-relevant device at roughly half the linear size of ITER (R=3.3m vs 6.2m). CFS has demonstrated the core magnet technology (20 T large-bore HTS magnet, September 2021) and is constructing SPARC (Q~11 burning plasma experiment) with ARC as the follow-on commercial power plant design targeting 400 MWe. The concept uses ICRF heating, a FLiBe liquid immersion blanket for integrated tritium breeding and neutron shielding, and targets quasi-steady-state operation with burns lasting tens of minutes. Both SPARC and ARC have published designs with detailed physics and engineering parameters.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: CFS technology page (cfs.energy/technology); Sorbom et al. 2015 (arxiv.org/abs/1409.3540)
- **Notes**: Tokamak is the canonical MFE concept. No ambiguity.

### Confinement Concept
- **Value**: `Compact tokamak`
- **Confidence**: high
- **Citation**: Sorbom et al. 2015 — "ARC: A compact, high-field, fusion nuclear science facility"; CFS technology page
- **Notes**: The "compact" designation comes from using HTS magnets to achieve high field in a smaller device (R=3.3m vs ITER's R=6.2m). Not a spherical tokamak (aspect ratio ~3, not ~1.5).

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: SPARC Wikipedia; CFS technology page; Lin et al. 2020 discusses D-T operation scenarios
- **Notes**: D-T is explicitly the target fuel for both SPARC and ARC. SPARC will also do D-D reduced-field experiments, but the commercial target is D-T.

### Primary Heating
- **Value**: `RF (ICRH)`
- **Confidence**: high
- **Citation**: Lin & Wright et al., "Physics basis for the ICRF system of the SPARC tokamak," J. Plasma Phys. 86, 2020
- **Notes**: SPARC uses exclusively ICRF at 120 MHz, 25 MW coupled. ARC design adds 25 MW LHCD for current drive plus 13.6 MW ICRF for heating. ICRF/ICRH is the primary plasma heating method; LHCD is primarily for current drive (sustaining steady-state), not heating.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: medium
- **Citation**: Sorbom et al. 2015 (ARC paper); Colliva et al. 2024 (MDPI) — studied three cycles for ARC, concluded supercritical steam Rankine is "the most promising solution"; "Exploration of power conversion thermodynamic cycles for ARC fusion reactor" (ScienceDirect, 2020)
- **Notes**: The ARC baseline design uses a Rankine (steam) cycle at ~30% efficiency. sCO2 Brayton and combined cycles have been studied. Colliva et al. 2024 independently concluded supercritical steam Rankine is most promising. CFS has not publicly committed to a specific cycle for the commercial plant. `Thermal (steam)` is well-supported by all published analysis but remains medium confidence absent a CFS engineering commitment.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: SPARC targets Q ~ 11; ARC targets Q ~ 13.6. Both well above Q = 5 threshold where alpha heating dominates.
- **Notes**: SPARC is explicitly designed to demonstrate a burning plasma. ARC at Q > 10 is firmly in the burning plasma regime. Per schema: "Use Burning for concepts explicitly targeting ignition or high Q (>10)."

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: high
- **Citation**: CFS technology page; Sorbom et al. 2015; CFS 20 T magnet demonstration (September 2021)
- **Notes**: REBCO HTS tape wound into D-shaped TF coils. Peak field 23 T in coils, 12.2 T on-axis (SPARC) / 9.2 T on-axis (ARC). Demountable joints enable coil opening for maintenance. Operating temperature ~20 K. Two magnet variants: NINT (steel-plate stacked HTS) for TF coils, PIT VIPER cables for pulsed PF/CS coils.

### Tritium Breeding
- **Value**: `FLiBe blanket`
- **Confidence**: high
- **Citation**: Sorbom et al. 2015; Grokipedia ARC page; multiple CFS descriptions
- **Notes**: FLiBe (LiF-BeF2) liquid immersion blanket is the ARC baseline. TBR >= 1.1, optimizable to ~1.22. FLiBe serves triple duty: tritium breeding, neutron shielding, and heat removal.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: Sorbom et al. 2015; ARC design descriptions
- **Notes**: The FLiBe blanket explicitly serves as both tritium breeder and neutron shield, capturing ~80% of neutron power. Additional shielding includes 1 cm tungsten first wall and TiH2 neutron shielding to protect magnets. Textbook case for `Integrated blanket/shield` per schema.

### Operation Mode
- **Value**: `Quasi-steady`
- **Confidence**: high
- **Citation**: Multiple 2025-2026 CFS sources consistently describe ARC as pulsing "for tens of minutes at a time"; CFS blog on pulsed magnets; Sorbom et al. 2015
- **Notes**: Multiple recent CFS communications consistently describe ARC as pulsing "for tens of minutes at a time" — textbook `Quasi-steady`. The "steady power to the grid" language in CFS materials refers to continuous electrical output via FLiBe thermal storage, not continuous plasma. The original ARC paper (2015) targeted full steady-state via LHCD + bootstrap current, but this has evolved. SPARC itself is clearly pulsed (10-second flat-top).

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Operation mode is quasi-steady/continuous, not pulsed in the IFE/MIF sense
- **Notes**: N/A — quasi-steady-state operation with long burns (minutes+), not discrete pulsed events.

### Driver Technology
- **Value**: `HTS magnets (REBCO, 20 T)`
- **Confidence**: high
- **Citation**: CFS 20 T magnet demonstration (2021); Sorbom et al. 2015; all CFS technology descriptions
- **Notes**: The distinguishing engineering bet is the HTS REBCO magnets enabling compact high-field tokamak operation. Peak field demonstrated: 20 T (2021 milestone). ARC design peak field: 23 T in coils. Everything else (compact size, economics, demountable maintenance) flows from the magnet capability.

## Metadata Updates

### Published Machine/Plant?
- **Value**: Yes — both SPARC (under construction) and ARC (conceptual design published)
- **Confidence**: high
- **Citation**: Sorbom et al. 2015 (ARC); Creely et al. 2020 (SPARC overview, J. Plasma Phys.); CFS announced ARC site in Chesterfield, Virginia
- **Notes**: SPARC is under construction; ARC is a published conceptual power plant design with an announced Virginia site. ARC power output has evolved from 270 MWe in earlier papers to 400 MWe in current plans, with Google and Eni PPAs fully subscribing the capacity.

### Lab Experiments
- **Value**: ITER, JET (Culham), EAST (ASIPP), JT-60SA (QST/F4E), KSTAR (KFE), DIII-D (GA), Alcator C-Mod (MIT)
- **Confidence**: high
- **Notes**: Alcator C-Mod at MIT is particularly relevant — CFS spun out of MIT PSFC, and C-Mod demonstrated high-field compact tokamak physics (world record pressure). SPARC itself will be the most directly relevant experiment once operational.

## Remaining Gaps

### Energy Capture (medium confidence)
CFS has not publicly committed to Rankine vs. Brayton for the commercial ARC plant. The 2015 paper uses Rankine as baseline, and Colliva et al. 2024 independently concluded supercritical steam Rankine is most promising among three cycles studied. sCO2 Brayton has also been studied and could offer higher efficiency (up to 40%+). A CFS engineering commitment to a specific cycle would raise this to high. Searched: CFS website (JS-blocked), Wikipedia, Sorbom et al. 2015, ScienceDirect thermodynamic cycles paper (2020), Colliva et al. 2024 (MDPI).

This gap is unlikely to be resolved by further web research — it requires a new CFS publication or engineering disclosure. No further iteration recommended.

## Key Sources

1. Sorbom et al., "ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets," 2015 — [arXiv](https://arxiv.org/abs/1409.3540) / [MIT PSFC full text](https://library.psfc.mit.edu/catalog/reports/2010/15ja/15ja032/15ja032_full.pdf)
2. Lin & Wright et al., "Physics basis for the ICRF system of the SPARC tokamak," J. Plasma Phys. 86, 2020 — [Cambridge Core](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/physics-basis-for-the-icrf-system-of-the-sparc-tokamak/22016DD64F3C5CAD47563A1E4AE59934)
3. Creely et al., "Overview of the SPARC tokamak," J. Plasma Phys., 2020
4. "Exploration of power conversion thermodynamic cycles for ARC fusion reactor," Fusion Engineering and Design, 2020 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0920379620301939)
5. Colliva et al., "Power conversion thermodynamic cycles for ARC," MDPI, 2024 — concluded supercritical steam Rankine is "the most promising solution"
6. [SPARC (tokamak) — Wikipedia](https://en.wikipedia.org/wiki/SPARC_(tokamak))
7. [ARC fusion reactor — Grokipedia](https://grokipedia.com/page/ARC_fusion_reactor) — most detailed specifications source
8. [CFS Blog — SPARC Assembly](https://blog.cfs.energy/cfs-takes-its-next-step-toward-fusion-energy-assembling-the-sparc-tokamak/)
9. [CFS Blog — $863M Funding](https://blog.cfs.energy/how-863m-in-new-funding-fast-tracks-commercial-fusion-power/)
10. [CFS Blog — PIT VIPER Pulsed Power Magnets](https://cfs.energy/news-and-media/commonwealth-fusion-systems-second-breakthrough-superconducting-technology-handles-mammoth-pulses-of-power/)
11. [IEEE Spectrum — "This Fusion Reactor Is Held Together With Tape"](https://spectrum.ieee.org/fusion-2662267312)
12. [World Nuclear News — SPARC Assembly](https://www.world-nuclear-news.org/articles/assembly-starts-of-sparc-as-iter-cryopumps-completed)
13. [CFS Virginia Plant Announcement](https://fusionenergyinsights.com/blog/post/commonwealth-fusion-systems-to-build-world-s-first-commercial-fusion-power-plant-in-virginia)
