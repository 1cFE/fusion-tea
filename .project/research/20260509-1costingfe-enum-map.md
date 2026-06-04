# Concept-to-ENUM Fit Ranking

Each concept in the corpus is ranked by how closely it maps to the **closest-available** `ConfinementConcept` ENUM in `1costingfe` — not necessarily the ENUM that was actually used in the concept's `model_setup.py`. This surfaces (a) where the framework's existing ENUMs already capture the architecture well, (b) where an ENUM exists but only partially fits, and (c) where the concept has no analog in the framework at all.

Reference: `1costingfe` master @ 4ca4d49 (includes the new `DIPOLE` ENUM and the Zap-style `STAGED_ZPINCH` calibration).

## Rubric

- **Rank 1** — concept maps cleanly to the ENUM; framework defaults capture the dominant cost drivers
- **Rank 2** — ENUM is the closest available analog but with notable architectural strain (fuel, driver class, conversion path, target/chamber specifics)
- **Rank 3** — no applicable ENUM; the concept's architecture has no analog in costingfe

## Ranking

| # | Concept | Best-fit ENUM | Fuel | Rank | Notes |
|---|---|---|---|:-:|---|
| 01 | hts-compact-tokamak (CFS ARC) | TOKAMAK | DT | **1** | Textbook tokamak; geometry and HTS magnet stack are what the ENUM was calibrated for |
| 02 | acoustic-icf-sonofusion | — | DD | **3** | Acoustic-driven IFE has no analog in any ENUM |
| 03 | laser-icf-liquid-jet-target (Cortex) | LASER_IFE | DD | **2** | Laser driver fits, but the gold-nanoshell + femtosecond + liquid-jet target architecture has no parallel in the ENUM's chamber/target defaults |
| 04 | laser-icf (HB11) | LASER_IFE | PB11 | **2** | Laser driver fits, but PB11 fuel and the per-shot consumable kT magnetic-field coil have no representation in the ENUM defaults |
| 05 | planar-coil-stellarator (Thea) | STELLARATOR | DT | **1** | Stellarator topology + DT — direct ENUM territory |
| 06 | magnetic-mirror (Pale Blue) | MIRROR | PB11 | **2** | Mirror geometry fits, but p-B11 aneutronic operation with rotation-sustained DEC strains the ENUM's steady-state thermal power balance |
| 07 | maglif (Pacific Fusion) | MAGLIF | DT | **1** | Dedicated MAGLIF ENUM covers the architecture; pulsed-power liner-compression layout is the calibration case |
| 08 | frc-w-direct-conversion (Helion) | PULSED_FRC | DHE3 | **2** | FRC topology fits, but INDUCTIVE_DEC conversion + DHE3 fuel + colliding-FRC compression deviate from the ENUM's thermal/DT defaults |
| 09 | qi-stellarator-hts (Stellaris) | STELLARATOR | DT | **1** | Quasi-isodynamic stellarator + DT — clean ENUM territory |
| 10 | large-scale-stellarator | STELLARATOR | DT | **1** | Direct stellarator + DT |
| 11 | magnetic-mirror (Realta CoSMo) | MIRROR | DT | **1** | Steady-state DT tandem mirror — what the ENUM was built for |
| 12 | levitated-dipole (OpenStar) | DIPOLE | DT | **1** | Single levitated SC coil + stationary support coils + DT — the DIPOLE ENUM's calibration case |
| 13 | electrostatic-hybrid (Orbitron) | ORBITRON | DT | **2** | ENUM matches the rotating-electrode electrostatic concept family, but Orbitron's specific drive architecture isn't captured beyond generic markup coefficients |
| 14 | mtf-pneumatic-compression (General Fusion) | MAG_TARGET | DT | **2** | MAG_TARGET catch-all hosts MIF; the pneumatic-piston driver with liquid-metal vortex chamber has no specific calibration |
| 15 | sheared-flow-z-pinch (Zap) | STAGED_ZPINCH | DT | **1** | costingfe YAML explicitly calibrated against Zap-style SFSZP — "Zap Energy-like" reference design, gas-injection (no manufactured targets), 1 Hz rep rate, stabilization coils, compact linear geometry all match Zap directly |
| 16 | muon-catalyzed-fusion (Acceleron) | — | DT | **3** | Accelerator + muon production economics has no analog in any ENUM |
| 17a | laser-icf-hybrid-drive (Xcimer) | LASER_IFE | DT | **2** | Laser IFE fits broadly, but KrF excimer (vs DPSSL default), two-beam hybrid direct drive, and FLiBe thick-liquid-wall chamber all deviate from the ENUM's reference design |
| 17b | laser-icf-fast-ignition (Focused Energy) | LASER_IFE | DT | **2** | Laser IFE fits, but fast ignition uses separate compression + ignition lasers — the ENUM treats both as one driver |
| 18 | p-b11-frc (TAE) | MIRROR | PB11 | **2** | TAE's linear geometry, steady-state NBI sustainment, and end-cell DEC are mirror-like and fit the MIRROR ENUM workflow; however the FRC closed-field-line core (and its formation/sustainment hardware) sits inside the mirror trap with no direct analog, and PB11 fuel deviates from DT defaults |
| 19 | orbital-levitated-dipole (Zephyr) | DIPOLE | DT | **2** | Dipole magnetic topology fits the ENUM, but the orbital deployment context introduces structural/launch-cost factors that have no terrestrial-plant analog |
| 20a | type-one-stellarator | STELLARATOR | DT | **1** | Direct stellarator + DT |
| 20b | renaissance-stellarator | STELLARATOR | DT | **1** | Direct stellarator + DT |
| 21 | spherical-tokamak-hts (Tokamak Energy) | TOKAMAK | DT | **1** | Spherical aspect ratio is accommodated within the TOKAMAK ENUM via geometric parameters |
| 22 | projectile-icf (First Light) | HEAVY_ION | DT | **2** | The IFE driver→target→chamber→blanket→thermal workflow that HEAVY_ION provides fits FLF abstractly, but the EM/projectile launcher is structurally different hardware from a heavy-ion accelerator and the per-MW driver cost constant would need full recalibration; the "amplifier" target architecture also has no analog |
| 23 | laser-icf-nanostructured-target (Marvel) | LASER_IFE | PB11 | **2** | Laser IFE fits with INDUCTIVE_DEC pulsed_conversion mode, but PB11 fuel and the nanostructured target are not captured in defaults |
| 24 | dense-plasma-focus (LPP) | DENSE_PLASMA_FOCUS | PB11 | **2** | ENUM exists for the DPF architecture but with partial cost-coefficient wiring; PB11 + beam-extracted direct conversion adds further deviation |
| 25 | heavy-ion-beam-icf | HEAVY_ION | DT | **1** | Heavy-ion-beam IFE is the dedicated ENUM case |
| 26 | laser-icf-indirect-drive (Inertia Thunderwall) | LASER_IFE | DT | **1** | Textbook DPSSL laser IFE with indirect drive — the ENUM's calibration case |
| 27 | polywell (EMC2) | POLYWELL | PB11 | **2** | ENUM covers the polyhedral magnetic-well IEC topology, but aneutronic IEC has specific cost drivers (high-voltage feedthrough, electron injection) not represented in defaults |
| 28 | hts-tokamak-full-hts | TOKAMAK | DT | **1** | Tokamak + DT with full HTS magnet system |
| 29 | negative-triangularity-tokamak | TOKAMAK | DT | **1** | Tokamak geometric variant; ENUM accommodates triangularity as a parameter |
| 30 | laser-icf-nif-commercialization (Focused Energy LIFE-class) | LASER_IFE | DT | **1** | Textbook DPSSL laser IFE; the LIFE-class architecture the ENUM was largely calibrated against |
| 31 | laser-icf-oec-architecture (BLF) | LASER_IFE | DT | **2** | Laser IFE fits broadly, but the Optical Energy Collection architecture makes mirror cost the dominant driver, not laser — the ENUM's cost-share assumptions are inverted |
| 32 | laser-icf-french-national (GenF) | LASER_IFE | DT | **1** | DPSSL shock-ignition direct drive falls within the ENUM's scope |
| 33 | state-backed-tokamak-best (Neo/ASIPP) | TOKAMAK | DT | **1** | Conventional ARIES-class tokamak |
| 34 | compact-spherical-tokamak-india | TOKAMAK | DT | **1** | Spherical tokamak variant |
| 35 | polomac-magnetic-confinement (Deutelio) | — | DT | **3** | Novel multipole magnetic geometry has no analog in any ENUM |
| 36 | helical-coil-stellarator (HESTIA) | STELLARATOR | DT | **1** | Direct stellarator + DT |
| 37 | mtif (Magneto-Inertial Fusion Tech) | MAG_TARGET | DD | **2** | MAG_TARGET catch-all hosts the MIF approach; the specific compression architecture and DD fuel aren't directly calibrated |
| 38 | particle-accelerator-driven-fusion (SHINE-style) | — | DT | **3** | Spallation-neutron-driven sub-critical assembly has no analog; HEAVY_ION ENUM is for IFE compression, structurally different |
| 39 | spherical-tokamak-cs-free-p-b11 (ENN) | TOKAMAK | PB11 | **2** | Tokamak geometry fits, but CS-free operation, PB11 fuel, and the planned DEC channel each deviate from the ENUM's calibration |

**Truly-bespoke residual** (no applicable ENUM in costingfe at all): 02 sonofusion, 16 muon-catalyzed, 35 polomac multipole, 38 accelerator-driven (SHINE).
