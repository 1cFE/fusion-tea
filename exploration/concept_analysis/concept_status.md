# Concept Analysis Status

Snapshot: 2026-04-19. 38 concepts from `exploration/concept_explorer/data/concept_registry.json`.

**Columns:**
- **Iter** — number of `iter-N/` directories under `exploration/concept_analysis/analyses/{id}-*/` that contain `analysis_output.md` or `verdict.json` (empty-shell dirs from aborted gap-check runs are excluded)
- **model_setup** — `yes` = `model_setup.py` exists; `stale` = exists but header starts `# STALE:`; `no` = missing
- **1costingfe** — `yes` if `model_setup.py` has `from costingfe ...`; `no` = custom hand-built model; `-` = no `model_setup.py`
- **Extracted** — `exploration/concept_explorer/data/{id}.json` exists; `stale` if a `.stale` sibling marker is present
- **Approved** — `Status: approved` in `analysis.md` frontmatter

| ID  | Name | Company | Iter | model_setup | 1costingfe | Extracted | Approved |
|-----|------|---------|-----:|-------------|------------|-----------|----------|
| 01  | HTS Compact Tokamak | Commonwealth Fusion Systems | 7 | yes | yes | yes | no |
| 02  | Acoustic ICF / Sonofusion (D-D) | Sonofusion Energy | 3 | stale | no | yes | no |
| 03  | Laser ICF - Liquid Jet Target (D-D) | Cortex Fusion Systems | 1 | yes | yes | yes | no |
| 04  | Laser ICF - p-B11 Fast Ignition | HB11 Energy | 1 | yes | yes | yes | no |
| 05  | Planar Coil Stellarator | Thea Energy | 1 | yes | yes | yes | no |
| 06  | Magnetic Mirror (p-B11) | Pale Blue Fusion | 1 | yes | yes | yes | no |
| 07  | MagLIF (D-T) | Pacific Fusion, Fuse Energy Technologies | 9 | stale | yes | yes | no |
| 08  | FRC w/ Direct Conversion | Helion Energy | 3 | stale | yes | yes | no |
| 09  | QI Stellarator - HTS | Proxima Fusion | 9 | stale | yes | yes | no |
| 10  | Large-Scale Stellarator | Gauss Fusion | 3 | stale | yes | yes | no |
| 11  | Magnetic Mirror (D-T) | Realta Fusion | 1 | yes | yes | yes | no |
| 12  | Levitated Dipole (D-T) | OpenStar Technologies | 3 | yes | no | yes | no |
| 13  | Electrostatic Hybrid (D-T) | Avalanche Energy | 0 | no | - | no | no |
| 14  | Magnetized Target Fusion - Pneumatic Compression (D-T) | General Fusion | 3 | yes | yes | yes | no |
| 15  | Sheared-Flow Stabilized Z-Pinch | Zap Energy | 3 | yes | no | yes | no |
| 16  | Muon-Catalyzed Fusion (D-T) | Acceleron Fusion | 0 | no | - | no | no |
| 17a | Laser ICF - Hybrid Direct Drive (D-T) | Xcimer Energy | 6 | yes | yes | yes | no |
| 17b | Laser ICF - Fast Ignition (D-T) | Focused Energy | 0 | no | - | no | no |
| 18  | p-B11 FRC | TAE Technologies | 0 | no | - | no | no |
| 19  | Orbital Levitated Dipole (D-He3) | Zephyr Fusion | 0 | no | - | no | no |
| 20a | QI Modular HTS Stellarator - Infinity Two | Type One Energy | 0 | no | - | no | no |
| 20b | Compact Liquid-Wall HTS Stellarator | Renaissance Fusion | 0 | no | - | no | no |
| 21  | Spherical Tokamak - HTS | Tokamak Energy | 1 | yes | yes | yes | yes |
| 22  | Projectile ICF (D-T) | First Light Fusion, NearStar Fusion | 5 | yes | no | yes | no |
| 23  | Laser ICF - Nanostructured Target (p-B11) | Marvel Fusion | 0 | no | - | no | no |
| 24  | Dense Plasma Focus (p-B11) | LPPFusion | 0 | no | - | no | no |
| 25  | Heavy Ion Beam ICF (D-T) | Intensity Energy | 0 | no | - | no | no |
| 26  | Laser ICF - Indirect Drive (D-T) | Inertia Enterprises | 0 | no | - | no | no |
| 27  | Polywell (D-T) | EMC2 | 0 | no | - | no | no |
| 28  | HTS Tokamak - Full HTS | Energy Singularity | 3 | yes | yes | yes | no |
| 29  | Negative Triangularity Tokamak | Firefly Fusion | 0 | no | - | no | no |
| 30  | Laser ICF - NIF Commercialization (D-T) | Inertia Enterprises | 0 | no | - | no | no |
| 31  | Laser ICF - OEC Architecture (D-T) | Blue Laser Fusion (BLF) | 0 | no | - | no | no |
| 32  | Laser ICF - French National Direct Drive (D-T) | GenF Systems | 0 | no | - | no | no |
| 33  | State-Backed Tokamak - BEST | Neo Fusion | 0 | no | - | no | no |
| 34  | Compact Spherical Tokamak - India | Pranos Fusion | 0 | no | - | no | no |
| 35  | PoloMac Magnetic Confinement | Deutelio | 2 | stale | no | yes | no |
| 36  | Helical Coil Stellarator | Helical Fusion | 0 | no | - | no | no |

## Summary

- Total concepts: **38**
- Analysis started (`iter-N/` with content): **19**
- `model_setup.py` present: **19** (13 fresh, 6 stale)
- Using `1costingfe` framework: **14** (of 19); the other 5 use hand-built models
- Extracted to explorer data: **19** (0 stale)
- Approved: **1**

## Changes Since 2026-04-11

- **model_setup.py refreshed** (stale → yes): 01, 15, 17a, 22, 28
- **Extracted** added for 35; stale marker cleared on 01
- **Iter count changes**: 15 (4→3) and 17a (7→6) reflect exclusion of empty-shell iter dirs under revised column definition
- **Fresh/stale mix**: fresh `model_setup.py` grew from 8 → 13; stale count fell from 11 → 6

