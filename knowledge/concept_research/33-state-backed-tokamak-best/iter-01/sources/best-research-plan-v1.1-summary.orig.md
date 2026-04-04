# BEST Research Plan v1.1 — Key Technical Extracts

**Source**: EUROfusion/ASIPP, "BEST Research Plan, 1st Edition: Missions and Pathways to Realisation", Version 1.1, 27 November 2025
**URL**: https://euro-fusion.org/wp-content/uploads/2025/11/BEST-Research-Plan-v1.1.pdf

## Company Identity

- The company is formally **Fusion Energy Technology Co., Ltd** (聚变新能(安徽)有限公司)
- Website: http://jbxnah.com
- Listed as "Neo Fusion" in some English-language databases (FusionXInvest)
- Majority owned by CNPC and Hefei Science Island (CAS)

## Main Parameters (Figure 1.4, p.16)

| Parameter | Value |
|-----------|-------|
| Major radius, R₀ | 3.6 m |
| Minor radius, a | 1.1 m |
| Elongation, κ | 1.88 |
| Triangularity, δ | 0.49 |
| Plasma volume | 142 m³ |
| Magnetic field, B₀ | 6.15 T |
| Plasma current, Ip | up to 7 MA |
| **Auxiliary heating (nominal / upgrade)** | |
| ECRH | 15 MW (24 MW) |
| ICRH | 10 MW (16 MW) |
| LH (Lower Hybrid) | 10 MW (16 MW) |
| NBI | 12 MW (15 MW) |
| Total Paux | ~50 MW |
| Tritium inventory | 110 g |

## Superconducting Magnet System (p.16)

- **TF coils**: 16 coils, 87.2 tons each. Cable-in-conduit conductor (CICC). **Graded Nb₃Sn** — ITER-standard Nb₃Sn for low-field, high-current-density Nb₃Sn for high-field regions.
- **PF coils**: 7 coils. Coils #1, #6, #7 are **Nb₃Sn**; coils #2-#5 are **NbTi**. Hybrid configuration.
- **CS (Central Solenoid)**: 6 modules, 180 tons total. **Hybrid CICC combining Nb₃Sn (LTS) and YBCO (HTS)**. Peak field 18.8 T (HTS sub-coils) and 12.4 T (LTS sub-coils). Nominal current 46.5 kA. Total flux 53 V·s.
- **CC (Correction Coils)**: 8 coils, ITER-heritage conductor.
- **Ferromagnetic Inserts (FI)**: Installed inside vacuum vessel (like ITER) to reduce field ripple <0.9%.
- **Total magnet system mass**: ~2000 tons

**Key insight**: The magnets are primarily LTS (Nb₃Sn, NbTi) with HTS (YBCO) used only in the CS high-field sub-coils. This is a hybrid LTS+HTS approach, not a full-HTS design like CFS/SPARC.

## Heating Systems (p.18-19)

- **ECRH**: 15 MW at 170 GHz, 3 equatorial launchers (ports B, C, D). Upgrade path to 24 MW.
- **ICRH**: 10 MW coupled, 2 equatorial antennas (ports F, H). Frequency range f = 40-65 MHz, with R&D to extend to 90 MHz. Hydrogen minority scenario at ~90 MHz for nominal B₀ = 6.15T.
- **LH (Lower Hybrid Current Drive)**: 10 MW at f = 4.6 GHz, 2 systems (ports K, P). For heating and current drive.
- **NBI**: 12 MW, positive-ion-based, acceleration voltage up to 120 kV (port O). Similar to JET NBI. Future upgrade to negative-ion NBI (N-NBI) at 500-800 keV.

Auxiliary heating primarily relies on RF systems (ECRH + ICRH + LHCD = 35 MW) supplemented by NBI (12 MW).

## Plasma-Facing Components (p.17)

- Full-tungsten first wall and divertor
- First wall: 240 modules, copper tiles coated with tungsten, CrZrCu heat sink, water-cooled at 4 MPa / 70°C
- Divertor: 48 cassette assemblies, actively cooled, designed for up to 10 MW/m² (15 MW/m² for monoblock designs)
- Remote handling required during D-T operations

## Tritium Breeding (Chapter 3)

- **BEST does NOT breed its own tritium** — relies on external supply (110 g initial inventory)
- **Three dedicated TBM (Test Blanket Module) ports** for testing breeding concepts
- ASIPP TBMs: CO₂ COOled Lithium lead (COOL) and Water Cooled Ceramic Breeder (WCCB)
- European TBMs: Water Cooled Lithium Lead (WCLL), Helium Cooled Pebble Bed (HCPB), or Water Lead Ceramic Breeder (WLCB)
- Materials under consideration: PbLi (liquid), Li₂TiO₃ and Li₄SiO₄ (ceramic), Be₁₂Ti (neutron multiplier)
- TBM testing is a technology validation platform for CFEDR blankets, not self-sufficient breeding

## Operation Mode

- Designed for **long-pulse operation** (>1000 seconds target)
- Also targets **short-pulse burning plasma** conditions (Q ≈ 5)
- Both steady-state (Q ≥ 1, long-pulse) and transient burning plasma (Q ≈ 5, shorter pulses) scenarios
- Conservative inductive scenarios: Q ≥ 1 with >50 MW fusion power
- Advanced scenarios: Q ≈ 5 in short pulses, approaching burning plasma

## Timeline (Figure 1.8, p.20)

- Construction: 2023-2027
- First plasma: end of 2027 / beginning of 2028
- Commissioning phase: H/D plasmas at half-field (B₀ = 3.1T), Ip up to ~3 MA
- Full-field deuterium: B₀ = 6.15T, Ip up to 5-6 MA
- First D-T plasma: at reduced current (~3-4 MA), then gradual increase to 7 MA
- **T1**: Scientific breakeven (Q ≥ 1) targeted before end of 2030
- **T2**: Long-pulse operation and fusion technology applications (2030-2035)
- **T3**: Alpha-particle and burning plasma studies (Q ≈ 5) (2032-2035+)

## Strategic Position

- Bridge between EAST/JET and ITER/CFEDR
- Will be the largest operating D-T tokamak prior to ITER
- Positioned between JET and ITER in both major radius and magnetic field (Figure 1.3)
- Self-described as "compact high-field tokamak" (though R=3.6m is mid-size, not compact in CFS sense)
- Part of ASIPP's EAST → BEST → CFEDR → PFPP progression
