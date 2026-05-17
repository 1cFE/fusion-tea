# Energy Singularity — Technical Overview

Compiled from multiple sources, March 2026.

## Company Profile

- **Founded**: June 2021, Shanghai, China
- **Focus**: Commercially viable high-temperature superconducting tokamak devices and operational control software
- **First private fusion company in China**
- **Workforce**: ~135 employees (as of late 2024)
- **Funding**: ~$110M raised for HH70; seeking additional $500M for HH170
- **Investors include**: miHoYo (Genshin Impact developer), NIO (electric car maker)

## HH70 — World's First Full HTS Tokamak

### Key Parameters
- **Major radius (R0)**: 0.7 m (some sources say 0.75 m)
- **Minor radius (a)**: 0.25–0.3 m
- **Toroidal field at plasma center (B0)**: 0.6 T
- **Maximum field on magnet coils (Bmax)**: 2.5 T
- **Coil operating temperature**: 20 K

### Magnet System
- **26 HTS magnets total**: 12 TF + 6 PF + 8 CS coils
- **All coils use REBCO** (Rare Earth Barium Copper Oxide) tape
- **Conductor**: Two 12mm-wide HTS tapes with 10mm REBCO core sandwiched between copper tapes; ~230 μm tape thickness, ~480 μm total conductor thickness after soldering
- **TF coil dimensions**: 2.015 m height × 1.03 m width
- **TF coil**: 3 double-pancake coils (DPCs), each 90 turns = 270 turns total, 450 m HTS conductor per TF coil
- **TF rated current**: 666 A
- **Total TF inductance**: 6.48 H
- **Supplier**: Shanghai Superconductor

### Heating Systems
- **Pre-ionization methods demonstrated**:
  1. Localized helical magnetic flux injection (electron gun)
  2. Ion cyclotron radiofrequency (ICRF) heating
- **No ECRH, LHCD, or NBI mentioned** in any public source for HH70

### Plasma Records (progression)
- First plasma: June 2024
- 120-second steady-state: January 6, 2026 (shot #5319)
- 335-second steady-state: January 2026 (shot #5609)
- 1,337-second steady-state: February 2026 (shot #5755)
- AI-based plasma control system used for optimization
- ~100 shots/day (vs. 20-30/day at JET)

### Construction
- Design started March 2022, assembly completed February 2024
- ~95% domestically sourced materials
- Built in under 2 years — fastest superconducting tokamak construction

## Jingtian Magnet (景天)

- **Purpose**: R&D and validation for HH170 TF magnets
- **Peak field achieved**: 21.7 T (surpassing CFS/MIT SPARC TFMC record of 20.1 T)
- **Dimensions**: ~3 m × 1.4 m, ~7.5 tons
- **Winding pack**: 32 stacked REBCO-based single-pancake coils
- **Center bore**: 0.5 m²
- **Operating current**: 24,300 A per turn
- **Publication**: IEEE Transactions on Applied Superconductivity (2025)

## HH170 — Next-Generation Device

- **Target**: Q > 10 (D-T equivalent energy gain)
- **Planned completion**: 2027
- **Magnetic field**: ~110% of SPARC (i.e., ~22+ T on coil)
- **Size**: ~90% diameter of SPARC, ~70% volume of SPARC
- **Target magnet field**: up to 25 T (per some sources)
- **Described as**: "world's smallest and lowest-cost tokamak device capable of achieving 10-fold energy gain"
- **Steady-state, high-magnetic-field, high-temperature superconducting model**

## HH380 — Demo Power Plant

- **Timeline**: Construction starts after 2030
- **Purpose**: Demonstration fusion power plant
- **No technical specifications publicly available**

## Roadmap
1. HH70 (2024) — proof of concept, all-HTS tokamak
2. HH170 (2027) — Q > 10 scientific demonstration
3. HH380 (post-2030) — demonstration power plant
4. Commercialization target: before 2035

## What's NOT Publicly Known
- Blanket design / tritium breeding approach for HH170/HH380
- Energy conversion method (thermal cycle type)
- Detailed heating systems for HH170 (beyond ICRF on HH70)
- Neutron shielding approach
- Specific plasma temperatures or densities

## Sources
- Energy Singularity official website: https://www.energysingularity.cn/en/
- ScienceDirect paper (HH70 commissioning): doi:10.1016/j.fusengdes.2025.115341
- ScienceDirect paper (HH70 magnet system): doi:10.1016/j.supcon.2024.100119
- IEEE TAS paper (Jingtian magnet): published 2025
- Interesting Engineering: multiple articles (2024-2026)
- SCMP, China Daily, Yicai Global: various articles
