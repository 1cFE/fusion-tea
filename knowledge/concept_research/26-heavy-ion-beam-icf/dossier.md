# Heavy Ion Beam ICF (D-T)

**Company**: Intensity Energy (unverified — almost certainly a placeholder; not found in FIA 2025 survey of 53 companies or any public database)
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: medium

## Summary

Heavy ion beam ICF uses linear induction accelerators to drive heavy ion beams (e.g., Bi²⁺ at ~10 GeV) onto direct-drive DT targets, compressing fuel to ~1000x solid density. The key advantage over laser ICF is driver wall-plug efficiency of 30-40% (vs 1-15% for lasers), and the accelerator's inherent modularity — hundreds of identical induction cells enable factory mass production. Two detailed power plant designs exist (HIBALL, HYLIFE-II) from national lab programs in the 1980s-90s, and experimental platforms (NDCX-II at LBNL, FAIR/SIS100 at GSI) continue advancing relevant beam physics. No private company is currently known to be pursuing this approach commercially; "Intensity Energy" could not be verified as an existing entity despite exhaustive searches including the FIA 2025 survey.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by HIF literature (arxiv 2005.07520)
- **Notes**: None

### Confinement Concept
- **Value**: Heavy ion beam ICF
- **Confidence**: high
- **Citation**: Baseline CSV; schema Column 2 vocabulary
- **Notes**: Direct-drive targets. Heavy ions deposit energy volumetrically (stopping range ~0.5-1 mm), unlike laser surface absorption.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Baseline CSV; HIBALL (KfK-3202), HYLIFE-II (OSTI 7021072)
- **Notes**: All published HIF power plant designs use D-T fuel.

### Primary Heating
- **Value**: Heavy ion beam
- **Confidence**: high
- **Citation**: Schema Column 4 vocabulary; LBNL HIF program literature
- **Notes**: US reference: induction linac. European reference: RF linac (GSI/HIDIF). Beam energy 3-8 MJ per shot. HIBALL: 10 GeV Bi²⁺ at 160 mA. HYLIFE-II: 5 MJ per shot.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: medium
- **Citation**: HIBALL (KfK-3202); HYLIFE-II final report (OSTI 7021072); confirmed by OSTI report title "Improved HYLIFE-II heat transport system and steam power plant"
- **Notes**: Both published power plant designs use conventional steam Rankine cycle. A multi-unit HYLIFE-II study also evaluated MHD+Steam hybrid, but baseline remains conventional steam. Confidence remains medium because values are inferred from historical designs, not a company disclosure — modern designs might opt for sCO2.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Schema Column 6 definition; HIF target physics literature
- **Notes**: Fuel compressed to ~1000x solid density by ion beam-driven ablation implosion.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema Column 7 vocabulary; iter-01/sources/hif-technology-overview.md
- **Notes**: The accelerator uses superconducting quadrupole magnet arrays for beam transport, but these confine the beam, not the plasma. Per schema: "Driver subsystem may contain magnets, but these confine the beam, not the plasma."

### Tritium Breeding
- **Value**: Li blanket (unspecified)
- **Confidence**: medium
- **Citation**: HIBALL (KfK-3202) — LiPb; HYLIFE-II (OSTI 7021072) — FLiBe
- **Notes**: Historical designs differ: HIBALL uses LiPb blanket (TBR ~1.195), HYLIFE-II uses FLiBe molten salt jets. Recorded as "unspecified" because no company has selected a specific approach. Both designs demonstrate viable breeding. HYLIFE-II tritium inventory: 0.5 g in molten salt, 140 g in tube wall metal.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: medium
- **Citation**: HYLIFE-II final report (OSTI 7021072); HIBALL (KfK-3202)
- **Notes**: Both designs use liquid blankets serving dual tritium breeding + neutron shielding function. HYLIFE-II thick flowing FLiBe jets also protect the first wall, enabling 30-year chamber lifetime with no replacement. HIBALL LiPb blanket similarly integrates functions.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Baseline CSV; all HIF power plant designs
- **Notes**: Discrete implosion events separated by target injection/reload cycles.

### Repetition Rate
- **Value**: ~10 Hz
- **Confidence**: high
- **Citation**: arxiv 2005.07520 (2020 review) — states "~10-15 Hz" for HIF reactors; HIBALL 4-chamber x 5 Hz = 20 Hz system rate; HYLIFE-II 6 Hz single chamber
- **Notes**: Upgraded from medium to high confidence based on 2020 review paper directly stating ~10-15 Hz target for HIF reactors, which aligns well with the ~10 Hz schema vocabulary value. Historical single-chamber designs at 5-6 Hz; multi-chamber configurations achieve higher system rates.

### Driver Technology
- **Value**: Linear induction accelerator
- **Confidence**: high
- **Citation**: Baseline CSV; LBNL HIF program; HIBALL (KfK-3202)
- **Notes**: US reference design. Hundreds of identical induction cells enable factory mass production. European alternative is RF linac (GSI/HIDIF). HYLIFE-II estimated $570M direct cost for recirculating induction accelerator driver. HIBALL design requires ~3 km linac.

## Remaining Gaps

| Column | Status | What's been searched | What might resolve it |
|--------|--------|---------------------|----------------------|
| Energy Capture | medium — confirmed as steam from historical designs | HIBALL, HYLIFE-II reports, OSTI titles | Cannot reach high confidence without an actual company making design choices. Modern HIF studies might specify sCO2 but none found. |
| Tritium Breeding | medium — two historical options, no company choice | HIBALL (LiPb), HYLIFE-II (FLiBe) | Cannot reach high confidence without a company selecting a specific blanket type. |
| Neutron Management | medium — inferred from historical designs | HIBALL, HYLIFE-II reports | Same as tritium breeding — requires a company design decision. |
| Company verification | Definitively unverifiable | FIA 2025 survey (53 companies), Crunchbase, LinkedIn, ARPA-E, DOE awards, Wikipedia, news, conference proceedings | "Intensity Energy" is almost certainly a placeholder. No private company of any name pursues heavy ion beam ICF commercially. |

**Recommendation**: No further iterations recommended. The medium-confidence values (energy capture, tritium breeding, neutron management) cannot reach high confidence without an actual company making design choices. The technology fundamentals are well-characterized from decades of national lab work. The concept is comprehensively documented from historical studies.

## Key Sources

1. **HIBALL Study** (KfK-3202, 1985) — German/US heavy ion beam power plant design. LiPb blanket, 10 GeV Bi²⁺, 3.8 GWe.
2. **HYLIFE-II Final Report** (OSTI 7021072, LLNL 1990s) — FLiBe thick-liquid-wall HIF power plant. 940 MWe baseline, 6.5 c/kWh. Includes "Improved HYLIFE-II heat transport system and steam power plant" companion report.
3. **arxiv 2005.07520** (2020) — HIF technology overview and review. Driver efficiency comparisons, target physics, ~10-15 Hz rep rate for power plants.
4. **NDCX-II** (LBNL, operational since ~2012) — Neutralized drift compression experiment, heavy ion beam physics platform.
5. **FAIR/SIS100** (GSI Darmstadt, commissioning 2025) — Heavy ion synchrotron with high-intensity pulses relevant to HIF.
6. **FIA 2025 Survey** — Survey of 53 fusion companies; "Intensity Energy" not listed.
7. **iter-01/sources/hif-technology-overview.md** — Compiled technical overview from multiple sources.
8. **iter-01/sources/intensity-energy-search-results.md** — Documentation of failed company verification searches.
