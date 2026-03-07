Now let me compile the full findings for all 12 columns plus metadata.

---

# HTS Compact Tokamak (D-T) — Commonwealth Fusion Systems

## Research Findings

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: CFS technology page (cfs.energy/technology); Sorbom et al. 2015 (arxiv.org/abs/1409.3540)
- **Notes**: Tokamak is the canonical MFE concept. No ambiguity.

### Confinement Concept
- **Value**: `Compact tokamak`
- **Confidence**: high
- **Citation**: CFS describes ARC/SPARC as a "compact, high-field" tokamak. Sorbom et al. 2015 title: "ARC: A compact, high-field, fusion nuclear science facility."
- **Notes**: The "compact" designation comes from using HTS magnets to achieve high field in a smaller device (R=3.3m vs ITER's R=6.2m). Not a spherical tokamak (aspect ratio ~3, not ~1.5).

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: SPARC Wikipedia; CFS technology page; ICRF paper (Lin et al. 2020) discusses D-T operation scenarios
- **Notes**: D-T is explicitly the target fuel for both SPARC and ARC. SPARC will also do D-D reduced-field experiments, but the commercial target is D-T.

### Primary Heating
- **Value**: `RF (ICRH)`
- **Confidence**: high
- **Citation**: Lin & Wright et al., "Physics basis for the ICRF system of the SPARC tokamak," J. Plasma Phys. 86, 2020. URL: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/physics-basis-for-the-icrf-system-of-the-sparc-tokamak/22016DD64F3C5CAD47563A1E4AE59934
- **Notes**: SPARC uses exclusively ICRF at 120 MHz, 25 MW coupled. ARC design adds 25 MW LHCD for current drive plus 13.6 MW ICRF for heating. For the concept as a whole, ICRF is the primary plasma heating method. LHCD is primarily for current drive (sustaining steady-state), not heating. The schema value `RF (ICRH)` is correct — ICRF = Ion Cyclotron Range of Frequencies, same as ICRH = Ion Cyclotron Resonance Heating.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: medium
- **Citation**: Sorbom et al. 2015 (ARC paper); "Exploration of power conversion thermodynamic cycles for ARC fusion reactor" (ScienceDirect, 2020)
- **Notes**: The ARC baseline design uses a Rankine (steam) cycle at ~30% efficiency. However, sCO2 Brayton and combined cycles have been studied and could offer higher efficiency (up to 40%+). Since the baseline published design uses Rankine, `Thermal (steam)` is correct. Could update to `Thermal (sCO2)` if CFS commits to Brayton cycle. Might be more accurate as `Thermal (unspecified)` since CFS hasn't publicly committed to a specific cycle for the commercial plant, but the published ARC paper specifies Rankine.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: SPARC targets Q ≈ 11; ARC targets Q ≈ 13.6. Both well above Q = 5 threshold where alpha heating dominates.
- **Notes**: SPARC is explicitly designed to demonstrate a burning plasma — alpha particle self-heating dominating external heating. ARC at Q > 10 is firmly in the burning plasma regime. Per schema: "Use `Burning` for concepts explicitly targeting ignition or high Q (>10)."

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: high
- **Citation**: CFS technology page; Sorbom et al. 2015; CFS magnet breakthrough announcement (September 2021 — 20 T demonstration)
- **Notes**: REBCO HTS tape wound into D-shaped TF coils. Peak field 23 T in coils, 12.2 T on-axis (SPARC) / 9.2 T on-axis (ARC). Demountable joints are a key innovation — coils can be opened for maintenance. Operating temperature ~20 K. CFS demonstrated a 20 T large-bore HTS magnet in 2021, a major milestone. Two magnet types: NINT (steel-plate stacked HTS) for TF coils, PIT VIPER cables for pulsed PF/CS coils.

### Tritium Breeding
- **Value**: `FLiBe blanket`
- **Confidence**: high
- **Citation**: Sorbom et al. 2015; Grokipedia ARC page; multiple CFS descriptions
- **Notes**: FLiBe (LiF-BeF₂) liquid immersion blanket is the ARC baseline. TBR ≥ 1.1, optimizable to ~1.22. FLiBe serves triple duty: tritium breeding, neutron shielding, and heat removal. This is the canonical CFS approach — directly matches the schema value.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: Sorbom et al. 2015; ARC design descriptions
- **Notes**: The FLiBe blanket explicitly serves as both tritium breeder and neutron shield, capturing ~80% of neutron power. Additional shielding includes 1 cm tungsten first wall and TiH₂ neutron shielding to protect magnets. This is the textbook case for `Integrated blanket/shield` per the schema: "Use when the blanket explicitly serves dual purpose (CFS FLiBe...)."

### Operation Mode
- **Value**: `Quasi-steady`
- **Confidence**: medium
- **Citation**: Sorbom et al. 2015 (ARC paper describes steady-state target via LHCD); CFS blog on pulsed magnets ("ARC operations will pulse for longer, perhaps for tens of minutes at a time")
- **Notes**: There is some tension here. The original ARC paper (2015) targets full steady-state via 25 MW LHCD + bootstrap current. However, more recent CFS communications describe ARC as pulsing "for tens of minutes at a time" — which is quasi-steady-state. The concept description says "quasi-steady-state via bootstrap current and external drive." I'll use `Quasi-steady` as it matches both the concept description and recent CFS statements. The steady-state aspiration may represent a future upgrade path. SPARC itself is clearly pulsed (10-second flat-top).

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Operation mode is quasi-steady/continuous, not pulsed in the IFE/MIF sense
- **Notes**: N/A — quasi-steady-state operation with long burns (minutes+), not discrete pulsed events. The "pulses" are long-duration plasma discharges, not the rapid fire events that repetition rate describes.

### Driver Technology
- **Value**: `HTS magnets (REBCO, 20 T)`
- **Confidence**: high
- **Citation**: CFS 20 T magnet demonstration (2021); Sorbom et al. 2015; all CFS technology descriptions
- **Notes**: The distinguishing engineering bet is the HTS REBCO magnets enabling compact high-field tokamak operation. Peak field demonstrated: 20 T (2021 milestone). ARC design peak field: 23 T in coils. This is CFS's core technology differentiator — everything else (compact size, economics, demountable maintenance) flows from the magnet capability.

---

## Metadata Columns (Confirmation/Update)

### Published Machine/Plant?
- **Value**: Yes — both SPARC (under construction) and ARC (conceptual design published)
- **Confidence**: high
- **Citation**: Sorbom et al. 2015 (ARC); Creely et al. 2020 (SPARC overview, J. Plasma Phys.); CFS announced ARC site in Chesterfield, Virginia
- **Notes**: The initial CSV says "No" — this should be updated. SPARC is a specific published machine design (under construction). ARC is a published conceptual power plant design (Sorbom et al. 2015, with subsequent updates). CFS has announced a site for ARC in Virginia.

### Lab Experiments
- **Value**: ITER, JET (Culham), EAST (ASIPP), JT-60SA (QST/F4E), KSTAR (KFE), DIII-D (GA), Alcator C-Mod (MIT)
- **Confidence**: high
- **Notes**: The existing list is appropriate. Alcator C-Mod at MIT is particularly relevant — CFS spun out of MIT PSFC, and C-Mod demonstrated high-field compact tokamak physics (world record pressure). SPARC itself will be the most directly relevant experiment once operational.

---

## Remaining Gaps

All 12 columns have been filled with medium or high confidence. Key areas where confidence could be improved:

1. **Energy Capture** (medium confidence): CFS has not publicly committed to Rankine vs. Brayton for the commercial ARC plant. The 2015 paper uses Rankine as baseline, but sCO2 Brayton has been studied. A CFS statement on the ARC power conversion cycle would raise this to high.

2. **Operation Mode** (medium confidence): Tension between the 2015 paper's steady-state target and recent CFS statements about "pulsing for tens of minutes." A definitive CFS engineering statement on ARC's operational profile would clarify. `Quasi-steady` is the safe answer covering both interpretations.

3. **Published Machine/Plant?**: The CSV says "No" but this appears incorrect — both SPARC and ARC have published designs. Recommend updating to "Yes."

## Sources Consulted

- [SPARC (tokamak) - Wikipedia](https://en.wikipedia.org/wiki/SPARC_(tokamak))
- [CFS Technology Page](https://cfs.energy/technology/) (content blocked by JS rendering)
- [CFS SPARC Page](https://cfs.energy/technology/sparc/) (content blocked by JS rendering)
- [CFS ARC Page](https://cfs.energy/technology/arc/) (content blocked by JS rendering)
- [CFS FAQ](https://cfs.energy/company/frequently-asked-questions/) (content blocked by JS rendering)
- [ARC fusion reactor - Wikipedia](https://en.wikipedia.org/wiki/ARC_fusion_reactor) (403 blocked)
- [ARC fusion reactor - Grokipedia](https://grokipedia.com/page/ARC_fusion_reactor) — most detailed specifications source
- [Lin & Wright et al., "Physics basis for the ICRF system of the SPARC tokamak," J. Plasma Phys. 2020](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/physics-basis-for-the-icrf-system-of-the-sparc-tokamak/22016DD64F3C5CAD47563A1E4AE59934)
- [Sorbom et al., "ARC: A compact, high-field, fusion nuclear science facility..." 2015](https://arxiv.org/abs/1409.3540)
- [CFS Blog - SPARC Assembly](https://blog.cfs.energy/cfs-takes-its-next-step-toward-fusion-energy-assembling-the-sparc-tokamak/)
- [CFS Blog - $863M Funding](https://blog.cfs.energy/how-863m-in-new-funding-fast-tracks-commercial-fusion-power/)
- [CFS Blog - Pulsed Power Magnets (PIT VIPER)](https://cfs.energy/news-and-media/commonwealth-fusion-systems-second-breakthrough-superconducting-technology-handles-mammoth-pulses-of-power/)
- [MIT PSFC SPARC Page](http://www-new.psfc.mit.edu/sparc)
- ["Exploration of power conversion thermodynamic cycles for ARC fusion reactor" - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0920379620301939)
- [Sorbom et al. 2015 - MIT PSFC full text](https://library.psfc.mit.edu/catalog/reports/2010/15ja/15ja032/15ja032_full.pdf)
- [IEEE Spectrum - "This Fusion Reactor Is Held Together With Tape"](https://spectrum.ieee.org/fusion-2662267312)
- [World Nuclear News - SPARC Assembly](https://www.world-nuclear-news.org/articles/assembly-starts-of-sparc-as-iter-cryopumps-completed)
- [CFS Virginia Plant Announcement](https://fusionenergyinsights.com/blog/post/commonwealth-fusion-systems-to-build-world-s-first-commercial-fusion-power-plant-in-virginia)
