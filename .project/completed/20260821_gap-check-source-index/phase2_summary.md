# Phase 2 Per-Concept Summary

Auto-generated classifier output. Columns: blocking_count baseline→new, Δ, fleet citations split into §1-5 ("integrated") vs §6 ("recommended") for baseline and new, classification.

## Deviation class legend

- **1-fleet-downgrade**: new integrates fleet sources AND blocking_count dropped — intended effect; accept.
- **2-fleet-reclassify**: new integrates fleet sources; blocking_count flat/up — reclassification within tier; accept.
- **1a-recommend-only-downgrade-SUSPECT**: blocking_count dropped without §1-5 integration; LLM may have over-confidently downgraded based on knowing-source-exists. **Inspect.**
- **2a-recommend-only**: fleet sources only in §6; no §1-5 integration; blocking_count flat/up. Mild partial-failure of injection; usually acceptable.
- **3-no-fleet-judgment-noise**: no fleet citations at all; |Δ|≤2; LLM judgment drift within expected envelope; accept as noise per Phase 1 decision.
- **3a-no-fleet-LARGE-DRIFT**: no fleet citations; |Δ|≥3; outside envelope. **Inspect.**
- **5-regression**: baseline had fleet integration; new lost it. **Inspect / consider revert.**

## Table

| concept | bc | → | bc | Δ | fleet§1-5 b→n | fleet§6 b→n | class |
|---------|----|----|----|----|----------------|---------------|-------|
| `01-hts-compact-tokamak` | 1 | → | 4 | +3 | 2→2 | 1→4 | 2-fleet-reclassify |
| `02-acoustic-icf-sonofusion` | 8 | → | 8 | +0 | 0→0 | 0→1 | 2a-recommend-only |
| `03-laser-icf-liquid-jet-target` | 7 | → | 8 | +1 | 0→0 | 0→3 | 2a-recommend-only |
| `04-laser-icf` | 4 | → | 7 | +3 | 0→0 | 0→3 | 2a-recommend-only |
| `05-planar-coil-stellarator` | 3 | → | 3 | +0 | 0→0 | 0→3 | 2a-recommend-only |
| `06-magnetic-mirror` | 13 | → | 8 | -5 | 0→1 | 0→1 | 1-fleet-downgrade |
| `07-maglif` | 3 | → | 3 | +0 | 0→0 | 0→3 | 2a-recommend-only |
| `08-frc-w-direct-conversion` | 7 | → | 6 | -1 | 0→1 | 0→0 | 1-fleet-downgrade |
| `09-qi-stellarator-hts` | 2 | → | 3 | +1 | 0→1 | 0→4 | 2-fleet-reclassify |
| `10-large-scale-stellarator` | 0 | → | 2 | +2 | 0→1 | 0→7 | 2-fleet-reclassify |
| `11-magnetic-mirror` | 4 | → | 3 | -1 | 0→0 | 0→2 | 1a-recommend-only-downgrade-SUSPECT |
| `12-levitated-dipole` | 4 | → | 0 | -4 | 0→3 | 0→6 | 1-fleet-downgrade |
| `13-electrostatic-hybrid` | 6 | → | 6 | +0 | 0→0 | 0→1 | 2a-recommend-only |
| `14-magnetized-target-fusion-pneumatic-compression` | 4 | → | 4 | +0 | 0→0 | 0→4 | 2a-recommend-only |
| `15-sheared-flow-stabilized-z-pinch` | 5 | → | 6 | +1 | 0→0 | 0→3 | 2a-recommend-only |
| `16-muon-catalyzed-fusion` | 6 | → | 5 | -1 | 0→0 | 0→0 | 3-no-fleet-judgment-noise |
| `17a-laser-icf-hybrid-drive` | 4 | → | 3 | -1 | 0→1 | 0→1 | 1-fleet-downgrade |
| `17b-laser-icf-fast-ignition` | 6 | → | 6 | +0 | 0→0 | 0→2 | 2a-recommend-only |
| `18-p-b11-frc` | 8 | → | 5 | -3 | 0→0 | 0→1 | 1a-recommend-only-downgrade-SUSPECT |
| `19-orbital-levitated-dipole` | 10 | → | 10 | +0 | 0→0 | 0→0 | 3-no-fleet-judgment-noise |
| `20a-type-one-stellarator` | 3 | → | 4 | +1 | 0→2 | 0→3 | 2-fleet-reclassify |
| `20b-renaissance-stellarator` | 4 | → | 4 | +0 | 0→1 | 0→2 | 2-fleet-reclassify |
| `21-spherical-tokamak-hts` | 3 | → | 4 | +1 | 0→3 | 0→0 | 2-fleet-reclassify |
| `22-projectile-icf` | 7 | → | 5 | -2 | 0→0 | 0→4 | 1a-recommend-only-downgrade-SUSPECT |
| `23-laser-icf-nanostructured-target` | 7 | → | 6 | -1 | 0→0 | 0→2 | 1a-recommend-only-downgrade-SUSPECT |
| `24-dense-plasma-focus` | 6 | → | 7 | +1 | 0→0 | 0→3 | 2a-recommend-only |
| `25-heavy-ion-beam-icf` | 2 | → | 0 | -2 | 0→3 | 0→5 | 1-fleet-downgrade |
| `26-laser-icf-indirect-drive` | 2 | → | 2 | +0 | 0→3 | 0→0 | 2-fleet-reclassify |
| `27-polywell` | 7 | → | 6 | -1 | 0→0 | 0→2 | 1a-recommend-only-downgrade-SUSPECT |
| `28-hts-tokamak-full-hts` | 5 | → | 6 | +1 | 0→5 | 0→1 | 2-fleet-reclassify |
| `29-negative-triangularity-tokamak` | 1 | → | 2 | +1 | 0→0 | 0→3 | 2a-recommend-only |
| `30-laser-icf-nif-commercialization` | 5 | → | 4 | -1 | 0→0 | 0→2 | 1a-recommend-only-downgrade-SUSPECT |
| `31-laser-icf-oec-architecture` | 4 | → | 8 | +4 | 0→0 | 0→5 | 2a-recommend-only |
| `32-laser-icf-french-national` | 6 | → | 6 | +0 | 0→0 | 0→3 | 2a-recommend-only |
| `33-state-backed-tokamak-best` | 4 | → | 4 | +0 | 0→1 | 0→4 | 2-fleet-reclassify |
| `35-polomac-magnetic-confinement` | 9 | → | 12 | +3 | 0→0 | 0→3 | 2a-recommend-only |
| `36-helical-coil-stellarator` | 1 | → | 4 | +3 | 0→0 | 0→3 | 2a-recommend-only |
| `37-magnetized-target-inertial-fusion-mtif` | 6 | → | 9 | +3 | 0→0 | 0→2 | 2a-recommend-only |
| `38-particle-accelerator-driven-fusion` | 4 | → | 8 | +4 | 0→1 | 0→1 | 2-fleet-reclassify |
| `39-spherical-tokamak-cs-free-p-b11` | 8 | → | 7 | -1 | 0→0 | 0→2 | 1a-recommend-only-downgrade-SUSPECT |

## Class counts

- 1-fleet-downgrade: 5
- 1a-recommend-only-downgrade-SUSPECT: 7
- 2-fleet-reclassify: 10
- 2a-recommend-only: 16
- 3-no-fleet-judgment-noise: 2

## Concepts flagged for inspection

- **11-magnetic-mirror** (1a-recommend-only-downgrade-SUSPECT, Δ=-1): new mentions fleet sources only in §6 recs (2); blocking_count dropped without integration — possible over-confident downgrade
- **18-p-b11-frc** (1a-recommend-only-downgrade-SUSPECT, Δ=-3): new mentions fleet sources only in §6 recs (1); blocking_count dropped without integration — possible over-confident downgrade
- **22-projectile-icf** (1a-recommend-only-downgrade-SUSPECT, Δ=-2): new mentions fleet sources only in §6 recs (4); blocking_count dropped without integration — possible over-confident downgrade
- **23-laser-icf-nanostructured-target** (1a-recommend-only-downgrade-SUSPECT, Δ=-1): new mentions fleet sources only in §6 recs (2); blocking_count dropped without integration — possible over-confident downgrade
- **27-polywell** (1a-recommend-only-downgrade-SUSPECT, Δ=-1): new mentions fleet sources only in §6 recs (2); blocking_count dropped without integration — possible over-confident downgrade
- **30-laser-icf-nif-commercialization** (1a-recommend-only-downgrade-SUSPECT, Δ=-1): new mentions fleet sources only in §6 recs (2); blocking_count dropped without integration — possible over-confident downgrade
- **39-spherical-tokamak-cs-free-p-b11** (1a-recommend-only-downgrade-SUSPECT, Δ=-1): new mentions fleet sources only in §6 recs (2); blocking_count dropped without integration — possible over-confident downgrade
