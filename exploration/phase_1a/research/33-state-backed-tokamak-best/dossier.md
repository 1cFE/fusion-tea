# State-Backed Tokamak - BEST (D-T)

**Company**: Neo Fusion (Fusion Energy Technology Co., Ltd / 聚变新能)
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: medium

## Summary

BEST (Burning Plasma Experimental Superconducting Tokamak) is a mid-size tokamak (R=3.6m, B=6.15T, Ip up to 7 MA) under construction at Hefei, China, targeting first plasma in late 2027. It uses a hybrid LTS+HTS magnet system (primarily Nb3Sn/NbTi with YBCO only in the CS high-field sub-coils) and ~50 MW of multi-method auxiliary heating (ECRH + ICRH + LHCD + NBI). BEST is an experimental device positioned between EAST/JET and ITER in China's national fusion roadmap (EAST -> BEST -> CFEDR -> PFPP), targeting Q>=1 by 2030 and Q~5 burning plasma studies by 2032-2035. It is majority state-owned through CNPC and the Chinese Academy of Sciences.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, EUROfusion/ASIPP, Nov 2025
- **Notes**: Standard tokamak magnetic confinement.

### Confinement Concept
- **Value**: `Compact tokamak`
- **Confidence**: medium
- **Citation**: BEST Research Plan v1.1, p.16 (R0=3.6m, a=1.1m, B0=6.15T)
- **Notes**: BEST self-describes as a "compact high-field tokamak," but R=3.6m is mid-size — larger than CFS SPARC (R=1.85m) yet smaller than ITER (R=6.2m). No exact schema match for "mid-size tokamak." Using `Compact tokamak` per the project's self-description, but this is a schema fit issue worth noting. Aspect ratio A=3.27, elongation kappa=1.88, triangularity delta=0.49.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, Chapter 3
- **Notes**: 110g tritium inventory. D-T operations planned after initial H/D commissioning phase.

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, p.18-19
- **Notes**: Multi-method system totaling ~50 MW: ECRH 15 MW (170 GHz), ICRH 10 MW (40-65 MHz), LHCD 10 MW (4.6 GHz), NBI 12 MW (120 kV positive-ion). RF systems dominate at 35 MW vs 12 MW NBI. Upgrade path to ~71 MW total.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: CFETR power conversion studies (2021, 2024, 2025); BEST COOL TBM design
- **Notes**: BEST is an experimental device with no power conversion system. However, multiple published studies on CFETR (the next step in China's fusion roadmap after BEST) recommend sCO2 Brayton cycle as the preferred power conversion technology, achieving 34-40% thermal efficiency. BEST's own COOL TBM test port uses sCO2 as the blanket coolant, directly coupling to this approach. The value remains `Thermal (unspecified)` since BEST itself does not generate electricity, but the evidence clearly points to sCO2 Brayton for downstream CFEDR/PFPP reactors.

### Plasma State
- **Value**: `Burning`
- **Confidence**: medium
- **Citation**: BEST Research Plan v1.1, p.20 (timeline T3: burning plasma studies, Q~5)
- **Notes**: Target Q~5 in advanced scenarios qualifies as burning plasma (alpha heating significant but not fully dominant). Initial operations will be at lower Q (>=1). The "Burning" classification reflects the ultimate target, not initial operating conditions.

### Magnet Type
- **Value**: `LTS+HTS`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, p.16 (magnet system description)
- **Notes**: Primarily LTS — TF coils: graded Nb3Sn (16 coils, 87.2t each); PF coils: Nb3Sn (#1,6,7) + NbTi (#2-5); CS: hybrid Nb3Sn + YBCO (HTS), peak field 18.8T in HTS sub-coils. HTS used only in CS high-field region. Total magnet mass ~2000t. This is NOT a full-HTS design like CFS/SPARC.

### Tritium Breeding
- **Value**: `TBD`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, Chapter 3
- **Notes**: BEST does not breed its own tritium — relies on external supply (110g inventory). Has 3 dedicated TBM (Test Blanket Module) test ports for validating breeding concepts for future CFEDR: COOL (CO2-cooled LiPb), WCCB (water-cooled ceramic breeder), plus European TBM options (WCLL, HCPB, WLCB). TBM testing is technology validation, not self-sufficient breeding. `TBD` is the correct schema value since this is a D-T device that hasn't committed to a breeding approach for a power-plant configuration.

### Neutron Management
- **Value**: `Heavy shielding (14 MeV)`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, p.17 (PFC description)
- **Notes**: Full-tungsten first wall and divertor. 240 first-wall modules (W-coated Cu tiles, CrZrCu heat sink, water-cooled at 4 MPa/70C). 48 divertor cassettes rated to 10-15 MW/m2. Remote handling required during D-T operations. No integrated blanket/shield — separate shielding approach.

### Operation Mode
- **Value**: `Quasi-steady`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, p.20
- **Notes**: Designed for long-pulse operation (>1000s target) but not true steady-state. Also targets short-pulse burning plasma conditions (Q~5). Corrects the initial CSV value of "Continuous" — BEST is a long-pulse tokamak, not a steady-state device.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Schema convention — quasi-steady/steady-state concepts
- **Notes**: N/A — quasi-steady-state operation, not pulsed.

### Driver Technology
- **Value**: `LTS+HTS magnets (Nb3Sn/YBCO, 6.15T) + multi-method H&CD (50 MW)`
- **Confidence**: high
- **Citation**: BEST Research Plan v1.1, p.16-19
- **Notes**: The distinguishing engineering features are: (1) hybrid LTS+HTS magnet system with YBCO only in CS high-field coils, and (2) comprehensive 4-method heating and current drive portfolio (ECRH/ICRH/LHCD/NBI). ITER-heritage conductor technology throughout.

## Remaining Gaps

| Column | Status | Notes |
|--------|--------|-------|
| Confinement Concept | medium confidence | "Compact tokamak" is the closest schema value but R=3.6m is mid-size. May warrant schema discussion at checkpoint review. |
| Energy Capture | medium confidence | Upgraded from low in iter-02. Value is `Thermal (unspecified)` because BEST is experimental, but CFETR studies strongly indicate sCO2 Brayton for the reactor lineage. Further improvement would require BEST/CFEDR to formally commit to a power conversion architecture. |
| Plasma State | medium confidence | "Burning" reflects target Q~5, but initial ops will be sub-burning. Could be refined with more detail on operational phases. |

All other columns are at high confidence. The BEST Research Plan v1.1 was an exceptionally comprehensive source that resolved most questions in a single iteration.

## Key Sources

1. **BEST Research Plan v1.1** — EUROfusion/ASIPP, "BEST Research Plan, 1st Edition: Missions and Pathways to Realisation", Version 1.1, 27 November 2025. https://euro-fusion.org/wp-content/uploads/2025/11/BEST-Research-Plan-v1.1.pdf
   - Saved extract: `iter-01/sources/best-research-plan-v1.1-summary.md`
   - Covers: all technical parameters, magnet system, heating, tritium breeding, timeline, strategic position

2. **Neo Fusion company profile** — FusionXInvest, 36kr
   - Saved extract: `iter-01/sources/neo-fusion-company-profile.md`
   - Covers: company identity, ownership (CNPC, CAS), funding ($214M), relationship to ASIPP

3. **CFETR power conversion studies** — Multiple published papers (2021, 2024, 2025) on supercritical CO2 Brayton cycle for China's fusion power plant lineage
   - Covers: power conversion technology selection for CFEDR/PFPP, thermal efficiency (34-40%), sCO2 as preferred cycle
