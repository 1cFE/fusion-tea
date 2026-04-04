Research complete. Here's a summary of the key findings:

## Summary

The BEST Research Plan v1.1 (EUROfusion/ASIPP, Nov 2025) provided comprehensive specifications for all 12 columns. Key findings:

| Column | Value | Confidence |
|--------|-------|------------|
| Confinement Family | `MFE` | high |
| Confinement Concept | `Compact tokamak` | medium (schema mismatch — R=3.6m is mid-size) |
| Fuel | `D-T` | high |
| Primary Heating | `RF + NBI` | high (35 MW RF + 12 MW NBI = ~50 MW total) |
| Energy Capture | `Thermal (unspecified)` | low (experimental device, no power conversion system) |
| Plasma State | `Burning` | medium (target Q≈5, initial ops at lower Q) |
| Magnet Type | `LTS+HTS` | high (Nb₃Sn/NbTi TF+PF with YBCO in CS high-field) |
| Tritium Breeding | `TBD` | high (external supply + 3 TBM test ports) |
| Neutron Management | `Heavy shielding (14 MeV)` | high |
| Operation Mode | `Quasi-steady` | high (long-pulse >1000s, not true steady-state) |
| Repetition Rate | `N/A` | high |
| Driver Technology | `LTS+HTS magnets (Nb₃Sn/YBCO, 6.15T) + multi-method H&CD (50 MW)` | high |

**Notable corrections to initial CSV data:**
- Operation mode listed as "Continuous" should be `Quasi-steady` (long-pulse tokamak, not steady-state)
- The magnet system is hybrid LTS+HTS, not full HTS — primarily ITER-heritage Nb₃Sn with YBCO only in the CS
- Company name "Neo Fusion" = "Fusion Energy Technology Co., Ltd" (聚变新能)

All outputs saved to `./output.md` and source extracts to `./sources/`.
