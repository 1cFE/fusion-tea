# Concept Analysis Status

Snapshot: 2026-04-20. 38 concepts from `exploration/concept_explorer/data/concept_registry.json`.

**Columns:**
- **Iter** — number of `iter-N/` directories under `exploration/concept_analysis/analyses/{id}-*/` that contain `analysis_output.md` or `verdict.json` (empty-shell dirs from aborted gap-check runs are excluded)
- **model_setup** — `yes` = `model_setup.py` exists; `stale` = exists but header starts `# STALE:`; `no` = missing
- **1costingfe** — `yes` if `model_setup.py` has `from costingfe ...`; `no` = custom hand-built model; `-` = no `model_setup.py`
- **Extracted** — `exploration/concept_explorer/data/{id}.json` exists; `stale` if a `.stale` sibling marker is present
- **Approved** — `Status: approved` in `analysis.md` frontmatter

| ID  | Name | Company | Iter | model_setup | 1costingfe | Extracted | Approved |
|-----|------|---------|-----:|-------------|------------|-----------|----------|
| 01  | HTS Compact Tokamak | Commonwealth Fusion Systems | 7 | yes | yes | yes | no |
| 02  | Acoustic ICF / Sonofusion (D-D) | Sonofusion Energy | 6 | yes | no | yes | no |
| 03  | Laser ICF - Liquid Jet Target (D-D) | Cortex Fusion Systems | 1 | yes | yes | yes | no |
| 04  | Laser ICF - p-B11 Fast Ignition | HB11 Energy | 1 | yes | yes | yes | no |
| 05  | Planar Coil Stellarator | Thea Energy | 1 | yes | yes | yes | no |
| 06  | Magnetic Mirror (p-B11) | Pale Blue Fusion | 1 | yes | yes | yes | no |
| 07  | MagLIF (D-T) | Pacific Fusion, Fuse Energy Technologies | 9 | yes | yes | yes | no |
| 08  | FRC w/ Direct Conversion | Helion Energy | 4 | yes | yes | yes | no |
| 09  | QI Stellarator - HTS | Proxima Fusion | 9 | yes | yes | yes | no |
| 10  | Large-Scale Stellarator | Gauss Fusion | 3 | yes | yes | yes | no |
| 11  | Magnetic Mirror (D-T) | Realta Fusion | 1 | yes | yes | yes | no |
| 12  | Levitated Dipole (D-T) | OpenStar Technologies | 4 | yes | no | yes | no |
| 13  | Electrostatic Hybrid (D-T) | Avalanche Energy | 5 | yes | no | yes | no |
| 14  | Magnetized Target Fusion - Pneumatic Compression (D-T) | General Fusion | 3 | yes | yes | yes | no |
| 15  | Sheared-Flow Stabilized Z-Pinch | Zap Energy | 3 | yes | no | yes | no |
| 16  | Muon-Catalyzed Fusion (D-T) | Acceleron Fusion | 3 | yes | no | yes | no |
| 17a | Laser ICF - Hybrid Direct Drive (D-T) | Xcimer Energy | 6 | yes | yes | yes | no |
| 17b | Laser ICF - Fast Ignition (D-T) | Focused Energy | 3 | yes | yes | yes | no |
| 18  | p-B11 FRC | TAE Technologies | 3 | yes | yes | yes | no |
| 19  | Orbital Levitated Dipole (D-He3) | Zephyr Fusion | 3 | no | - | yes | no |
| 20a | QI Modular HTS Stellarator - Infinity Two | Type One Energy | 3 | yes | yes | yes | no |
| 20b | Compact Liquid-Wall HTS Stellarator | Renaissance Fusion | 3 | yes | yes | yes | no |
| 21  | Spherical Tokamak - HTS | Tokamak Energy | 1 | yes | yes | yes | yes |
| 22  | Projectile ICF (D-T) | First Light Fusion, NearStar Fusion | 5 | yes | no | yes | no |
| 23  | Laser ICF - Nanostructured Target (p-B11) | Marvel Fusion | 3 | yes | yes | yes | no |
| 24  | Dense Plasma Focus (p-B11) | LPPFusion | 3 | yes | yes | yes | no |
| 25  | Heavy Ion Beam ICF (D-T) | Intensity Energy | 3 | yes | yes | yes | no |
| 26  | Laser ICF - Indirect Drive (D-T) | Inertia Enterprises | 3 | yes | yes | yes | no |
| 27  | Polywell (D-T) | EMC2 | 3 | yes | yes | yes | no |
| 28  | HTS Tokamak - Full HTS | Energy Singularity | 3 | yes | yes | yes | no |
| 29  | Negative Triangularity Tokamak | Firefly Fusion | 3 | yes | yes | yes | no |
| 30  | Laser ICF - NIF Commercialization (D-T) | Inertia Enterprises | 3 | yes | yes | yes | no |
| 31  | Laser ICF - OEC Architecture (D-T) | Blue Laser Fusion (BLF) | 3 | yes | yes | yes | no |
| 32  | Laser ICF - French National Direct Drive (D-T) | GenF Systems | 3 | yes | yes | yes | no |
| 33  | State-Backed Tokamak - BEST | Neo Fusion | 3 | yes | yes | yes | no |
| 34  | Compact Spherical Tokamak - India | Pranos Fusion | 3 | yes | yes | yes | no |
| 35  | PoloMac Magnetic Confinement | Deutelio | 4 | yes | yes | yes | no |
| 36  | Helical Coil Stellarator | Helical Fusion | 3 | yes | yes | yes | no |

## Summary

- Total concepts: **38**
- Analysis started (`iter-N/` with content): **38** (all concepts)
- `model_setup.py` present: **37** (all fresh; 19 has analysis but no model_setup)
- Using `1costingfe` framework: **31** (of 37); the other 6 use hand-built models
- Extracted to explorer data: **38** (all concepts, 0 stale)
- Approved: **1**
- **Zero gap-checked or not-started concepts remain**

## Changes Since Last Snapshot (2026-04-20 morning)

- **Final 5 concepts analyzed** (gap-checked → I3): 26 (Laser ICF - Indirect Drive), 27 (Polywell), 31 (Laser ICF - OEC Architecture), 32 (Laser ICF - French National), 36 (Helical Coil Stellarator) — all with costingfe model_setup
- **All 38 concepts now have analysis, extraction, and model_setup** (except 19 which lacks model_setup)
- **Pipeline state summary**: 1 approved, 8 synthesized (3 stale), 6 reviewed, 23 iterating, 0 gap-checked

## Historical Changes

### 2026-04-19 (refreshed)

- **model_setup.py refreshed** (stale → yes): 02, 08 — only 35 remained stale
- **02 extraction no longer stale** — `.stale` marker cleared
- **Iteration progress**: 02 (5→6), 08 (3→4), 12 (3→4), 13 (3→5), 33 (1→3), 34 (0→3)
- **34 new artifacts**: model_setup.py (costingfe) added; analysis progressed from 0 to 3 iterations
- **Stale synthesis.md** on 02, 08, 12 (downstream of refreshed model_setup/analysis updates)
- **Pipeline state summary**: 1 approved, 8 synthesized (3 stale), 6 reviewed, 13 iterating, 10 gap-checked

### 2026-04-19 (post-staleness-fix)

- **Staleness propagation fix landed** — `propagate_staleness` now takes a regeneration set; producers clear their own markers on write. False stale markers from the old bug stripped from 07, 09, 10, 13, 16, 17b, 20a, 20b.
- **model_setup.py refreshed** (stale → yes): 01, 07, 09, 10, 13, 15, 16, 17a, 17b, 20a, 22, 28
- **Extracted** added for 13, 16, 17b, 35; stale marker cleared on 01; 02 extraction newly marked stale
- **New analyses** (0 → 3 iter): **13, 16, 17b, 20b, 29, 30**; **20a** progressed 0 → 3; **33** progressed 0 → 1
- **02 extended** 3 → 5 iter (plus extraction went stale)
- **Iter count changes**: 15 (4→3) and 17a (7→6) reflect exclusion of empty-shell iter dirs under revised column definition
- **Fresh/stale mix**: fresh `model_setup.py` grew from 8 → 25; stale count fell from 11 → 3 (02, 08, 35)

