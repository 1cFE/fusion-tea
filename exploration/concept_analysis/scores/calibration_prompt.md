# Cross-Concept Score Calibration

You are performing cross-concept calibration of LCOE Downselect Potential scores.
This is Pass 2 of a two-pass scoring system. Pass 1 (per-concept scoring) is
complete. Your job is to enforce consistency across all concepts.

## Verified Scores (from Python extraction)

The following table was extracted and computed by Python. It includes:
- C1, C3, C4, C5, C8: from Claude's per-concept scoring (Pass 1)
- C2, C6: deterministic category-based assignments (Python)
- C7: computed from F1-F7 function means with heritage credit and caps (Python)
- Binary risk count per concept

**Do NOT re-extract scores from synthesis files.** Use this table as your starting point.

# Verified Scores

| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Binary Risks |
|---------|----|----|----|----|----|----|----|----|-------------|
| 01-hts-compact-tokamak | 3.2 | 2.5 | 2.3 | 2.5 | 2.0 | 2.5 | 4.0 | 3.5 | 2 |
| 02-acoustic-icf-sonofusion | 3.6 | 4.0 | 3.4 | 3.0 | 3.5 | 3.0 | 1.5 | 2.0 | 2 |
| 03-laser-icf-liquid-jet-target | 2.8 | 3.5 | 3.0 | 3.5 | 2.3 | 3.0 | 1.0 | 1.8 | 2 |
| 05-planar-coil-stellarator | 4.5 | 2.5 | 2.5 | 3.0 | 2.0 | 2.5 | 4.0 | 3.5 | 2 |
| 06-magnetic-mirror | 1.3 | 3.5 | 3.8 | 3.0 | 4.3 | 4.5 | 3.0 | 1.3 | 4 |
| 07-maglif | 3.7 | 3.0 | 2.8 | 3.0 | 2.1 | 2.0 | 3.5 | 2.5 | 4 |
| 08-frc-w-direct-conversion | 5.0 | 3.5 | 3.4 | 3.5 | 3.7 | 3.5 | 1.5 | 2.5 | 4 |
| 09-qi-stellarator-hts | 2.5 | 2.5 | 3.3 | 3.0 | 1.7 | 2.5 | 4.0 | 3.8 | 6 |
| 10-large-scale-stellarator | 3.3 | 2.5 | 2.7 | 3.0 | 1.7 | 2.5 | 4.0 | 3.3 | 3 |
| 12-levitated-dipole | 4.0 | 2.0 | 3.1 | 3.5 | 2.1 | 2.5 | 3.5 | 3.5 | 2 |
| 13-electrostatic-hybrid | 5.0 | 4.0 | 3.6 | 3.8 | 3.0 | 2.5 | 3.0 | 2.3 | 3 |
| 14-magnetized-target-fusion-pneumatic-compression | 2.8 | 3.0 | 3.4 | 2.5 | 1.8 | 2.0 | 1.5 | 2.5 | 6 |
| 15-sheared-flow-stabilized-z-pinch | 4.1 | 3.5 | 2.5 | 3.4 | 1.7 | 2.0 | 3.0 | 2.5 | 3 |
| 16-muon-catalyzed-fusion | 2.8 | 4.0 | 3.3 | 3.5 | 2.4 | 2.5 | 4.0 | 1.8 | 2 |
| 17a-laser-icf-hybrid-drive | 4.1 | 3.5 | 3.2 | 3.5 | 1.7 | 2.0 | 3.5 | 2.8 | 7 |
| 17b-laser-icf-fast-ignition | 3.7 | 3.5 | 2.8 | 3.5 | 1.8 | 2.0 | 3.5 | 2.3 | 9 |
| 18-p-b11-frc | 3.0 | 3.5 | 3.6 | 4.0 | 3.7 | 4.5 | 1.5 | 2.0 | 5 |
| 19-orbital-levitated-dipole | 3.0 | 2.0 | 2.9 | 4.0 | 4.3 | 4.0 | 1.0 | 1.3 | 4 |
| 20a-type-one-stellarator | 2.8 | 2.5 | 2.3 | 3.0 | 2.0 | 2.5 | 4.0 | 3.5 | 2 |
| 20b-renaissance-stellarator | 4.8 | 2.5 | 3.2 | 3.5 | 1.7 | 2.5 | 4.0 | 2.5 | 7 |
| 21-spherical-tokamak-hts | 2.0 | 2.5 | 3.1 | 2.5 | 2.0 | 2.5 | 3.5 | 2.5 | 2 |
| 22-projectile-icf | 2.4 | 4.0 | 2.9 | 3.5 | 1.7 | 2.0 | 3.5 | 2.3 | 3 |
| 23-laser-icf-nanostructured-target | 5.0 | 3.5 | 3.5 | 3.5 | 4.5 | 4.0 | 3.5 | 2.0 | 3 |
| 24-dense-plasma-focus | 5.0 | 4.0 | 3.5 | 3.5 | 5.0 | 4.0 | 1.0 | 1.8 | 5 |
| 25-heavy-ion-beam-icf | 5.0 | 4.0 | 3.3 | 3.0 | 1.7 | 2.0 | 2.5 | 3.0 | 6 |
| 26-laser-icf-indirect-drive | 3.2 | 3.5 | 3.4 | 3.5 | 2.4 | 2.0 | 4.0 | 2.5 | 4 |
| 27-polywell | 3.7 | 4.0 | 3.3 | 3.0 | 1.7 | 2.5 | 1.5 | 2.3 | 4 |
| 28-hts-tokamak-full-hts | 2.8 | 2.5 | 3.3 | 3.0 | 1.7 | 2.5 | 4.0 | 2.0 | 2 |
| 29-negative-triangularity-tokamak | 3.0 | 2.5 | 2.7 | 3.0 | 1.7 | 2.5 | 4.0 | 3.3 | 1 |
| 30-laser-icf-nif-commercialization | 4.6 | 3.5 | 4.2 | 2.5 | 1.7 | 2.0 | 3.5 | 2.2 | 5 |
| 31-laser-icf-oec-architecture | 4.5 | 3.5 | 3.2 | 3.0 | 2.3 | 2.0 | 3.5 | 2.8 | 5 |
| 32-laser-icf-french-national | 3.8 | 3.5 | 3.2 | 3.5 | 1.7 | 2.0 | 3.5 | 2.3 | 4 |
| 33-state-backed-tokamak-best | 2.1 | 2.5 | 3.7 | 2.5 | 1.8 | 2.5 | 4.0 | 2.5 | 3 |
| 35-polomac-magnetic-confinement | 2.0 | 4.0 | 2.9 | 3.5 | 2.8 | 3.5 | 1.0 | 2.0 | 5 |
| 36-helical-coil-stellarator | 2.4 | 2.5 | 2.5 | 3.5 | 2.8 | 2.5 | 4.0 | 2.8 | 5 |

## Function-Level Means (after heritage credit)

| Concept | F1 | F2 | F3 | F4 | F5 | F6 | F7 |
|---------|----|----|----|----|----|----|-----|
| 01-hts-compact-tokamak | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 02-acoustic-icf-sonofusion | 1.5 | 2.0 | 3.0 | 3.0 | 4.5 | 5.0 | 5.0 |
| 03-laser-icf-liquid-jet-target | 1.0 | 3.0 | 2.0 | 2.0 | 3.5 | 3.0 | 4.5 |
| 05-planar-coil-stellarator | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 06-magnetic-mirror | 2.5 | 3.0 | 2.5 | 3.5 | 5.0 | 3.0 | 2.5 |
| 07-maglif | 3.0 | 3.5 | 4.5 | 3.0 | 3.3 | 3.0 | 3.5 |
| 08-frc-w-direct-conversion | 2.5 | 2.5 | 4.0 | 2.5 | 4.0 | 1.5 | 3.0 |
| 09-qi-stellarator-hts | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 10-large-scale-stellarator | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.5 |
| 12-levitated-dipole | 3.0 | 3.5 | 3.0 | 3.5 | 3.0 | 3.0 | 4.5 |
| 13-electrostatic-hybrid | 3.0 | 3.5 | 2.5 | 3.0 | 3.0 | 2.0 | 4.0 |
| 14-magnetized-target-fusion-pneumatic-compression | 3.0 | 1.5 | 2.5 | 3.5 | 4.5 | 3.0 | 3.0 |
| 15-sheared-flow-stabilized-z-pinch | 2.5 | 2.5 | 3.0 | 2.5 | 3.5 | 3.0 | 4.5 |
| 16-muon-catalyzed-fusion | 2.5 | 2.5 | 5.0 | 4.0 | 4.5 | 3.5 | 4.5 |
| 17a-laser-icf-hybrid-drive | 3.5 | 3.5 | 3.5 | 4.0 | 3.5 | 3.5 | 4.5 |
| 17b-laser-icf-fast-ignition | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 4.0 |
| 18-p-b11-frc | 1.5 | 2.5 | 3.0 | 2.5 | 5.0 | 5.0 | 4.5 |
| 19-orbital-levitated-dipole | 2.0 | 2.5 | 4.5 | 2.5 | 4.0 | 1.0 | 2.0 |
| 20a-type-one-stellarator | 4.0 | 4.5 | 4.0 | 4.0 | 4.0 | 4.0 | 5.0 |
| 20b-renaissance-stellarator | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 21-spherical-tokamak-hts | 3.5 | 4.0 | 3.5 | 3.5 | 3.0 | 3.0 | 4.0 |
| 22-projectile-icf | 3.5 | 3.5 | 3.5 | 2.5 | 3.5 | 3.5 | 5.0 |
| 23-laser-icf-nanostructured-target | 2.5 | 3.0 | 3.5 | 3.5 | 4.5 | 4.0 | 3.5 |
| 24-dense-plasma-focus | 1.5 | 3.5 | 2.5 | 1.5 | 3.0 | 2.5 | 1.0 |
| 25-heavy-ion-beam-icf | 2.0 | 2.5 | 2.0 | 3.0 | 3.0 | 2.5 | 4.0 |
| 26-laser-icf-indirect-drive | 3.5 | 3.5 | 4.5 | 3.5 | 3.5 | 3.5 | 4.5 |
| 27-polywell | 2.0 | 3.0 | 3.0 | 2.5 | 2.5 | 1.5 | 3.5 |
| 28-hts-tokamak-full-hts | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.5 |
| 29-negative-triangularity-tokamak | 4.0 | 4.0 | 4.0 | 4.5 | 4.0 | 4.0 | 4.0 |
| 30-laser-icf-nif-commercialization | 3.5 | 3.5 | 4.0 | 3.5 | 3.5 | 3.5 | 4.5 |
| 31-laser-icf-oec-architecture | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 |
| 32-laser-icf-french-national | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 4.5 |
| 33-state-backed-tokamak-best | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 35-polomac-magnetic-confinement | 1.0 | 3.0 | 1.0 | 1.5 | 3.0 | 5.0 | 5.0 |
| 36-helical-coil-stellarator | 4.0 | 4.0 | 4.5 | 4.0 | 4.0 | 4.0 | 4.0 |

## Energy Capture, Heritage, and Peer Group (audit trail)

Heritage lineage and floor are derived from architecture (table.csv), not from concept IDs, so they survive renumbering. Heritage credit applies to D-T fuel only — non-D-T concepts show floor 1.0.

| Concept | Energy Capture | η_th | Heritage Lineage | Floor | Peer Group |
|---------|----------------|------|------------------|-------|------------|
| 01-hts-compact-tokamak | Thermal (steam) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 02-acoustic-icf-sonofusion | TBD | 0.35 | — | 1.0 | Exotic |
| 03-laser-icf-liquid-jet-target | TBD | 0.35 | — | 1.0 | Exotic |
| 05-planar-coil-stellarator | Thermal (steam) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 06-magnetic-mirror | Direct (charged particle) | 0.70 | — | 1.0 | p-B11 |
| 07-maglif | Thermal (unspecified) | 0.35 | magLIF | 3.0 | D-T Pulsed (MIF/Z-pinch) |
| 08-frc-w-direct-conversion | Direct (inductive) | 0.85 | — | 1.0 | Aneutronic |
| 09-qi-stellarator-hts | Thermal (unspecified) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 10-large-scale-stellarator | Thermal (unspecified) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 12-levitated-dipole | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 13-electrostatic-hybrid | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 14-magnetized-target-fusion-pneumatic-compression | Thermal (steam) | 0.35 | — | 1.0 | Exotic |
| 15-sheared-flow-stabilized-z-pinch | Thermal (steam) | 0.35 | Z-pinch | 2.5 | D-T Pulsed (MIF/Z-pinch) |
| 16-muon-catalyzed-fusion | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 17a-laser-icf-hybrid-drive | Thermal (unspecified) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 17b-laser-icf-fast-ignition | Thermal (steam) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 18-p-b11-frc | Thermal (steam) | 0.35 | — | 1.0 | Aneutronic FRC |
| 19-orbital-levitated-dipole | Direct (charged particle) | 0.70 | — | 1.0 | Aneutronic |
| 20a-type-one-stellarator | Thermal (steam) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 20b-renaissance-stellarator | Thermal (sCO2) | 0.48 | Stellarator | 4.0 | D-T Stellarators |
| 21-spherical-tokamak-hts | Thermal (unspecified) | 0.35 | Spherical Tokamak | 3.0 | D-T Tokamaks |
| 22-projectile-icf | Thermal (steam) | 0.35 | — | 1.0 | Exotic |
| 23-laser-icf-nanostructured-target | Hybrid (thermal + direct) | 0.55 | — | 1.0 | p-B11 |
| 24-dense-plasma-focus | Direct (charged particle) | 0.70 | — | 1.0 | p-B11 |
| 25-heavy-ion-beam-icf | Thermal (steam) | 0.35 | — | 1.0 | Exotic |
| 26-laser-icf-indirect-drive | Thermal (steam) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 27-polywell | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 28-hts-tokamak-full-hts | Thermal (unspecified) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 29-negative-triangularity-tokamak | Thermal (unspecified) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 30-laser-icf-nif-commercialization | Thermal (steam) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 31-laser-icf-oec-architecture | Hybrid (thermal + direct) | 0.55 | Laser IFE | 3.5 | D-T Laser IFE |
| 32-laser-icf-french-national | Thermal (unspecified) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 33-state-backed-tokamak-best | Thermal (unspecified) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 35-polomac-magnetic-confinement | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 36-helical-coil-stellarator | Thermal (sCO2) | 0.48 | Stellarator | 4.0 | D-T Stellarators |

## Binary Risks per Concept

### 01-hts-compact-tokamak
- TBR <1.0 in FLiBe blanket (commercial fleet cannot scale without tritium breeding self-sufficiency)
- Tritium processing plant failure or tritium extraction from FLiBe at <95% efficiency (cannot sustain D-T fuel cycle)

### 02-acoustic-icf-sonofusion
- Fusion from acoustic cavitation undemonstrated: temperature gap of ~10,000× (16,000 K achieved vs. 10⁸ K required for D-D thermonuclear ignition) is unbridged. Zero replicated experimental evidence. If acoustic compression cannot achieve fusion-relevant temperatures, concept produces zero net electricity.
- PZT transducer neutron irradiation failure: if piezoelectric materials depolarize or fracture under 2.45 MeV neutron flux at fusion-relevant fluences (10¹⁴ n/cm²/s), acoustic driver becomes inoperable and no neutron-tolerant piezoelectric replacement exists.

### 03-laser-icf-liquid-jet-target
- Plasma performance: if Q < 1 (plasmonic enhancement fails to accelerate deuterons to fusion-relevant energies), no net electricity is produced
- Instability control: if plasma instabilities inside nanoshells quench plasmonic field enhancement, fusion rate drops to zero

### 05-planar-coil-stellarator
- TBR <1.1 → tritium inventory depletes → plant shutdown (F6 physics)
- Tritium extraction efficiency <99% → regulatory inventory limit exceeded → plant shutdown (F6 hardware)

### 06-magnetic-mirror
- Nonthermal p-B11 plasma operation — bremsstrahlung dominance prevents net gain
- Alpha channeling efficiency — if <40% of theoretical, nonthermal distribution unsustainable
- Ponderomotive barrier failure — helium ash accumulation poisons plasma
- Helium extraction failure — ash buildup stops fusion within ~10 confinement times

### 07-maglif
- F1 Physics: Ignition failure — if Lawson parameter χ cannot reach ≥1.0 at practical drive currents (60+ MA), no net energy is produced and commercial operation is impossible.
- F4 Physics: Chamber pressure spike / FLiBe liquid wall reconstitution failure — if thick liquid wall cannot be reconstituted within 1 second or chamber pressure exceeds structural limits at GJ-scale yields, plant cannot operate at 1 Hz. Reducing to 0.1 Hz makes LCOE uncompetitive (305 $/MWh).
- F4 Hardware: Chamber lifetime <1000 shots due to combined environment failure — if shock + neutron + FLiBe corrosion + thermal cycling causes chamber/electrode cracking in <1000 shots, plant must shut down every ~10 days for replacement, dropping capacity factor to <30% and making LCOE >150 $/MWh.
- F6 Physics: Tritium breeding ratio (TBR) < 1.0 — if FLiBe blanket cannot breed sufficient tritium due to neutron streaming losses through RTL ports, plant cannot sustain operation without external tritium purchases, exhausting global supply in ~25 years across all D-T fusion plants.

### 08-frc-w-direct-conversion
- D-He3 fusion below ignition threshold (ion temperature <45 keV) — burn fraction → 0, LCOE → ∞
- He-3 self-breeding cycle does not close at commercial scale — no fuel supply for D-He3 operation
- He-3 extraction/separation infeasible at commercial kg/year throughput — fuel cycle fails
- Direct energy recovery efficiency falls below 90% threshold — round-trip energy balance negative, plant becomes net consumer

### 09-qi-stellarator-hts
- F1 Physics: H₉₈ confinement enhancement < 1.30 → fusion power < 2,700 MW → net electric output < 1,000 MW → plant economics fail
- F3 Physics: MHD instabilities or bootstrap current exceed design limits → plasma equilibrium uncontrollable → disruption-free operation lost
- F3 Hardware: 50 modular HTS coils cannot maintain ≤1 mm positioning tolerance → QI magnetic field optimization fails → confinement degrades → plasma performance fails
- F5 Physics: Coil neutron fluence > 3×10²² m⁻² before 10 full-power years → REBCO critical current degradation >10% → coil quench risk → early magnet replacement → extended plant shutdown
- F6 Physics: TBR < 1.0 (after all engineering losses) → tritium self-sufficiency fails → external tritium purchase required (per framework: mandatory binary classification)
- F6 Hardware: Tritium extraction from PbLi fails or efficiency < 50% → tritium inventory accumulates in blanket → radiological hazard → plant shutdown (per framework: mandatory binary classification)

### 10-large-scale-stellarator
- F1 Hardware: Superconducting coil quench or irreversible HTS degradation under 40-year fusion neutron fluence (10²³ n/m²) prevents plant operation
- F6 Physics: TBR < 1.0 due to unaccounted losses in 3D geometry prevents tritium self-sufficiency and commercial viability
- F6 Hardware: Tritium processing failure at kg/day scale or permeation barrier failure creates safety shutdown or prevents fuel cycle closure

### 12-levitated-dipole
- Confinement scaling below Bohm-like (n·τ_e < 50% of target) causes Q_sci < 7 and net power near zero
- Tritium breeding ratio (TBR) < 1.0 prevents tritium self-sufficiency and limits fleet scalability

### 13-electrostatic-hybrid
- Coulomb collision thermalization prevents Q>1: If experimental measurement confirms Lampe-Mannheimer (1998) critique that collision rates exceed fusion rates by 25-37× at required densities, net energy gain is unachievable regardless of engineering optimizations
- Electron cyclotron drift instability (ECDI) disrupts ion confinement at commercial density >10¹⁰ cm⁻³: If ECDI cannot be suppressed at fusion-relevant density, required triple product for Q>1 is unattainable
- Tritium breeding ratio <1.0: Without a breeding blanket achieving TBR≥1.05, purchased tritium cost at $35k/g scales inversely with Q and becomes LCOE-prohibitive at low Q (contributes $57k/MWh at Q=10, diverging to infinity as Q approaches break-even)

### 14-magnetized-target-fusion-pneumatic-compression
- Pneumatic compression system synchronization failure — if piston timing scatter exceeds 1% or mechanical infeasibility prevents operation, no fallback driver exists
- Compression ratio shortfall — if 12:1 cavity compression cannot be achieved in liquid metal (8:1 in water tests vs 12:1 target), plasma cannot reach fusion conditions
- Lawson criterion failure at commercial scale — if nTτ < 10²¹ with pneumatic compression (LM26 electromagnetic surrogate does not validate commercial driver), net energy gain impossible
- Tritium breeding ratio below self-sufficiency — if TBR < 1.05 (1.5 predicted, unvalidated), external tritium required (unavailable at fleet scale)
- Li-6 enrichment supply bottleneck — Western capacity must scale 2–10× for D-T fleet (shared showstopper with all D-T concepts)
- Liquid metal vortex reformation failure — if vortex cannot reform within 1 second at 1 Hz, repetition rate falls below viability threshold (~0.1 Hz minimum for LCOE <$150/MWh)

### 15-sheared-flow-stabilized-z-pinch
- Q < ~7: recirculating fraction > 70%, net electric output marginal or negative (F1 physics)
- TBR < 1.0: tritium-negative plant, cannot self-sustain (F6 physics)
- Tritium extraction failure: inventory buildup exceeds safety limits (F6 hardware)

### 16-muon-catalyzed-fusion
- Driver physics: muon production energy cost >2.0 GeV yields net energy sink regardless of hardware (Q_sci too low for positive net electricity)
- Fuel cycle: tritium breeding ratio <1.0 requires indefinite external tritium supply (economically infeasible, supply-limited)

### 17a-laser-icf-hybrid-drive
- Capsule gain Qc < 143 (at η_laser 7%) — wall-plug gain Q_wp falls below commercial viability threshold of 10
- Laser wall-plug efficiency < 5% — required Qsci for viability rises to ≥200, exceeding near-term achievable gains
- SBS NLO phase preservation failure at >100 kJ — cascades to implosion asymmetry and Qc collapse
- Two-beam HDD implosion asymmetry — hot-spot non-uniformity quenches fusion yield below commercial threshold
- SBS wavefront degradation at MJ scale — cascades to two-beam implosion failure
- TBR < 1.0 (FLiNaK ~1.05 marginal) — tritium breeding insufficient for self-sufficiency
- Tritium extraction failure — inventory accumulation triggers regulatory shutdown

### 17b-laser-icf-fast-ignition
- DT core compression to ignition-relevant ρR and T_ion — if physics fails, no net electricity
- Laser wall-plug efficiency <7% — recirculating power exceeds economically viable threshold
- 10 Hz repetition rate failure — if laser cannot sustain 10 Hz, plant output falls below 1 GWe design
- Diode pump module cost >$0.05/W — driver capital becomes prohibitively expensive
- Final optics neutron damage failure within <10^5 shots — if no replacement scheme maintains >65% availability, plant is economically non-viable
- Rayleigh-Taylor instability growth factor >50 — implosion symmetry breaks down, compression fails
- Proton beam divergence >20° half-angle — coupling efficiency collapses below ignition threshold
- TBR <1.0 long-term — tritium self-sufficiency impossible, concept requires perpetual external supply
- DT capsule fabrication failure at 900,000/day <$0.50/target — if cost >$1.00/target or production rate cannot scale, economics fail

### 18-p-b11-frc
- Q_plasma > 1 never demonstrated for p-B11 — required Q ≥ 25–30 at steam baseline, demonstrated <0.001, no theoretical or experimental basis for crossing this gap. Branch A (no LCOE) cannot be ruled out.
- T_i >> T_e regime at 150+ keV unsustainable — non-equilibrium beam-driven plasma validated only at ~1 keV; if equilibration dominates at fusion temperatures, bremsstrahlung losses force net negative energy.
- FRC stability at multi-MA plasma current and 1–2 m major radius unvalidated — C-2W demonstrates only at 0.4 m / 350 kA; ~10× current scale-up with no validated stability scaling.
- NBI wall-plug-to-plasma efficiency below 0.20 at Da Vinci beam energies — would push Q_plasma viability threshold above achievable values and force Branch A.
- Continuous (CW) FRC operation undemonstrated — current pulse record ~40 ms vs. continuous requirement; if duty-cycle-limited, capacity factor approaches zero.

### 19-orbital-levitated-dipole
- D-He3 triple product <10^20 keV·s·m^-3 prevents ignition (F1 physics)
- HTS coil radiation damage or cryocooler failure causes irreversible plant loss (F1 hardware)
- He3 self-breeding <100% requires external procurement at $30M/kg (F6 physics)
- He3 extraction/purification system failure requires external procurement (F6 hardware)

### 20a-type-one-stellarator
- Island divertor particle exhaust <0.5% (classical design + pessimistic transport + no baffling improvements) forces helium ash accumulation, limiting 2-year burn cycles to <1 year effective operation or requiring unplanned auxiliary pumping capital — only binary if no fallback to LIBD and transport assumptions pessimistic
- Tritium extraction efficiency from HCPB <80% over 2-year continuous cycle with no external tritium purchase fallback — breeding shortfall forces early shutdown; only binary if TBR margin insufficient to cover extraction losses (current 30% margin likely adequate unless extraction <<80%)

### 20b-renaissance-stellarator
- Ignition (Q=∞) at compact stellarator geometry: ISS04 scaling predicts n·τ_E ~11× below Lawson threshold at published design point
- Liquid Li-LiH wall stability at 25 MW/m² plasma-facing heat flux and 10 T magnetic field without MHD-driven confinement degradation
- Alpha-particle-driven instabilities at ignition conditions in compact QI stellarator (no experimental precedent in any stellarator)
- 3D stellarator magnetic field precision <1 mm RMS maintained under neutron irradiation and thermal cycling of laser-patterned HTS cylinders
- Plasma exhaust solution at 25 MW/m² steady-state heat flux with Z_eff <2.0 (no divertor design published)
- TBR = 1.60 validation at fusion-relevant 14 MeV neutron flux in 3D stellarator geometry with port penetrations
- Tritium extraction from flowing Li-LiH circuit at kg/day rates with <1% inventory holdup and heat exchanger permeation <1 Ci/day

### 21-spherical-tokamak-hts
- TBR < 1.0 with realistic port fractions in outboard-only blanket geometry
- Tritium extraction failure from liquid Li at kg/day plant scale

### 22-projectile-icf
- Target gain below 200× at 60 km/s projectile velocity prevents net electricity production at baseline rep rate (0.033 Hz)
- EM launcher failure to reach 60 km/s causes gain to fall below commercial threshold, making net electricity impossible
- Tritium breeding ratio below 1.0 prevents self-sufficiency and blocks fleet deployment (note: FLF's TBR 1.8 validation retires this risk, but listed per D-T framework rule)

### 23-laser-icf-nanostructured-target
- F1 Physics: p-B11 ignition failure — Q < 1 never demonstrated, four orders of magnitude gap from HB11 experimental results to commercial Q ≥ 5
- F1 Hardware: Laser driver wall-plug efficiency failure — WPE remains <5% instead of reaching ≥10%, recirculating power exceeds net output
- F2 Hardware: Laser diode pump cost failure — diode cost remains at $0.3–$1.3/W instead of reaching $0.01/W target, driver capital uncompetitive

### 24-dense-plasma-focus
- Q_sci < 1.41 (net electric breakeven) — if scientific gain remains below 1.41, gross electric output cannot sustain driver recharge and auxiliary loads, resulting in zero or negative net power
- QMF bremsstrahlung suppression failure — if Quantum Magnetic Field effect does not suppress bremsstrahlung as theorized, p-B11 fusion power will be exceeded by radiation losses under classical plasma physics, making net energy impossible
- Ion beam decelerator efficiency < 0.65 — if ion beam energy recovery falls below ~65%, combined direct energy conversion efficiency drops below breakeven threshold and net electric power becomes negative (no thermal cycle fallback exists)
- Filament instability unresolved — if current-sheath filament disruption during rundown cannot be suppressed, fusion yield remains at ~0.25 J level (Q_sci ~10⁻⁶), preventing any approach to net energy
- Repetition rate < 100 Hz — if electrode erosion or thermal limits prevent sustained operation above ~100 Hz, plant net power falls below ~500 MWe and LCOE exceeds 15 ¢/kWh, rendering the concept economically unviable

### 25-heavy-ion-beam-icf
- Target gain <50 → recirculating power exceeds generation, no net electricity
- Final focus system failure → no target implosion, no fusion
- Rayleigh-Taylor instability breakup → no hot-spot formation, no ignition
- Beam asymmetry >5% RMS → seeds RT instability, no ignition
- TBR <1.0 → fuel cycle cannot close, external tritium not viable at commercial scale
- Tritium extraction failure from FLiBe/LiPb → fuel recycling fails, plant cannot sustain operation

### 26-laser-icf-indirect-drive
- Capsule gain G < 100 → Q_eng falls below unity; plant produces no net electricity (F1 physics)
- Laser wall-plug efficiency < 5% → recirculating power fraction exceeds 50%; net output collapses (F2 physics)
- TBR < 1.0 (Inertia liquid Li, unanalyzed) → tritium self-sufficiency fails; external tritium purchase required indefinitely (F6 physics)
- Tritium extraction efficiency < 90% → tritium inventory accumulates in blanket; target factory runs out of fuel within weeks (F6 hardware)

### 27-polywell
- Electron confinement scaling fails at commercial density (γ >> 0.1): virtual cathode cannot form at 10²¹ m⁻³, Q < 1
- E-beam driver cannot sustain virtual cathode: recirculating power exceeds gross electric, negative net output
- Virtual cathode oscillations unstable: time-averaged Q < 1 due to intermittent confinement collapse
- Tritium breeding ratio TBR < 1.0: polyhedral geometry with coil neutron shadowing cannot achieve self-sustaining fuel cycle

### 28-hts-tokamak-full-hts
- TBR < 1.0 (tritium breeding ratio insufficient to sustain fuel cycle)
- Tritium extraction failure from blanket at commercial scale

### 29-negative-triangularity-tokamak
- Tritium breeding ratio below self-sufficiency (TBR < 1.02 after accounting for decay and processing losses)

### 30-laser-icf-nif-commercialization
- F2-Hardware: Final optics failure with no replacement scheme → plant cannot operate (laser beams cannot reach target)
- F3-Hardware: Target injection positioning failure (>±10 μm error) → laser beams miss target → no fusion → catastrophic optics damage + chamber contamination
- F4-Hardware: First wall structural failure (pulsed fatigue or neutron embrittlement) → vacuum/coolant breach → plant shutdown; or beam port contamination → shot failure
- F6-Physics: TBR < 1.0 → insufficient tritium breeding → external purchase required → economically infeasible
- F6-Hardware: Tritium extraction failure (<90% recovery) → TBR_effective < 1.0 → external tritium purchase → economically infeasible

### 31-laser-icf-oec-architecture
- Target gain G < 100 due to LPI (Function 1 physics)
- OEC mirror radiation degradation forcing annual replacement (Function 2 hardware)
- LPI backscatter >15% collapsing gain to G < 100 (Function 3 physics)
- Chamber clearing limiting repetition rate to ≤5 Hz (Function 4 hardware)
- Tritium breeding ratio TBR < 1.0 requiring external tritium purchase (Function 6 physics)

### 32-laser-icf-french-national
- Target gain G <60 results in recirculating power >70% making net output unviable
- Tritium breeding ratio TBR <1.0 prevents fuel cycle closure with >1 kg/day consumption vs <2 kg/year global supply making plant inoperable
- First wall lifetime <6 months causes availability <60% driving LCOE >140 $/MWh making concept uneconomic
- Tritium extraction efficiency <90% requires TBR >1.1 to compensate making fuel cycle closure harder to achieve

### 33-state-backed-tokamak-best
- TBR < 1.0 for commercial PFPP — if BEST TBM program fails to demonstrate TBR > 1.1, PFPP cannot close tritium fuel cycle and requires perpetual external tritium supply unavailable at commercial scale
- W impurity radiation collapse in burning plasma — if core W concentration exceeds ~10⁻⁵, radiative cooling terminates fusion; undemonstrated at Q > 1
- RWM instability at βN > 2.5 — if resistive wall mode feedback fails at commercial βN (CFETR Phase II requires βN = 3.54 for Q = 23.5), plasma terminates and net electricity is impossible

### 35-polomac-magnetic-confinement
- F1 Physics: D-D plasma Q < 5 → net power negative, no commercial viability
- F1 Hardware: In-vessel SC coil neutron damage or frequent quench → CF ≤ 0.40, economically nonviable
- F3 Physics: High-beta plasma instability + frequent disruptions → CF < 0.30, plant nonviable
- F3 Hardware: Disruptions damage/destroy in-vessel SC coil → multiple per year → CF < 0.40, economically nonviable
- F5 Hardware: In-vessel coil inadequate neutron shielding → coil lifetime < 3 FPY → unsustainable replacement frequency, economically nonviable

### 36-helical-coil-stellarator
- TBR < 1.0: No tritium self-sufficiency (3D neutron transport calculation incomplete as of 2023; 80 at.% Li-6 required; if TBR fails, external tritium supply unavailable at reactor scale)
- 250 GHz CW gyrotrons at 1 MW do not exist (TRL 1-2; no fallback heating system; 170 GHz would require different plasma operating point, unvalidated)
- Liquid metal blanket circulation failure (GALOP pump power unknown; if MHD pressure drop exceeds pump capacity or corrosion breaches module, blanket overheats and tritium extraction fails)
- sCO₂ thermal efficiency <32% at Q=13 (break-even threshold; only 20 kWe demo at 20% exists; if sCO₂ fails to achieve >40%, fallback to Rankine at 40% reduces P_net by 55% and inflates LCOE 2.2×)
- Confinement failure if H-factor <1.0 or stellarator MHD instability at reactor density (if Q drops below ~5, net electricity impossible; LHD heritage provides strong floor but heliotron at HESTIA scale undemonstrated)



## Concept File Paths

When you need justification detail for a calibration question, read the synthesis
and/or analysis file at the paths below. Read on demand — do not read all files upfront.

- **01-hts-compact-tokamak**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`
- **02-acoustic-icf-sonofusion**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/analysis.md`
- **03-laser-icf-liquid-jet-target**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/analysis.md`
- **05-planar-coil-stellarator**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/analysis.md`
- **06-magnetic-mirror**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/06-magnetic-mirror/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/06-magnetic-mirror/analysis.md`
- **07-maglif**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`
- **08-frc-w-direct-conversion**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/analysis.md`
- **09-qi-stellarator-hts**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md`
- **10-large-scale-stellarator**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/analysis.md`
- **12-levitated-dipole**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/analysis.md`
- **13-electrostatic-hybrid**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/analysis.md`
- **14-magnetized-target-fusion-pneumatic-compression**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/14-magnetized-target-fusion-pneumatic-compression/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/14-magnetized-target-fusion-pneumatic-compression/analysis.md`
- **15-sheared-flow-stabilized-z-pinch**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/analysis.md`
- **16-muon-catalyzed-fusion**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/analysis.md`
- **17a-laser-icf-hybrid-drive**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/analysis.md`
- **17b-laser-icf-fast-ignition**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/analysis.md`
- **18-p-b11-frc**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/analysis.md`
- **19-orbital-levitated-dipole**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/analysis.md`
- **20a-type-one-stellarator**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/analysis.md`
- **20b-renaissance-stellarator**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/analysis.md`
- **21-spherical-tokamak-hts**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`
- **22-projectile-icf**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/22-projectile-icf/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/22-projectile-icf/analysis.md`
- **23-laser-icf-nanostructured-target**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/analysis.md`
- **24-dense-plasma-focus**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/analysis.md`
- **25-heavy-ion-beam-icf**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/analysis.md`
- **26-laser-icf-indirect-drive**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/26-laser-icf-indirect-drive/analysis.md`
- **27-polywell**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/analysis.md`
- **28-hts-tokamak-full-hts**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/analysis.md`
- **29-negative-triangularity-tokamak**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/analysis.md`
- **30-laser-icf-nif-commercialization**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/analysis.md`
- **31-laser-icf-oec-architecture**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/analysis.md`
- **32-laser-icf-french-national**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/analysis.md`
- **33-state-backed-tokamak-best**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/analysis.md`
- **35-polomac-magnetic-confinement**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/analysis.md`
- **36-helical-coil-stellarator**
  - Synthesis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/synthesis.md`
  - Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/analysis.md`

## Calibration Questions

Apply Q1-Q7 in order. For each question, state what you checked, what you found,
and what adjustment (if any) you made. Apply all adjustments automatically — do
not ask for confirmation.

### Q1: Driver reality check

For each concept:
- If the concept has a novel monolithic driver that represents >30% of capital cost:
  **cap C1 at 3.0** (a monolithic driver cannot be modularized).
- If the driver is fusion-unique AND not factory-manufacturable:
  **cap C3 sub-factor A (learning rate) at 2.0**, then recompute C3.

### Q2: Binary/degrading classification and C7 floor

(a) **Verify classifications:** Read each concept's C7 risk matrix (in synthesis
Section 8). Ensure every cell has a binary or degrading label. Apply mandatory
binary classifications if missing:
- TBR < 1.0 for any D-T concept: binary
- Tritium extraction failure: binary
- He-3 self-breeding at scale: binary
- He-3 extraction/purification: binary
- External tritium or He-3 purchase is NOT a valid fallback for reclassification

(b) **Verify fallbacks:** For each binary risk, check if a valid fallback exists
that would reclassify it as degrading. Tritium/He-3 breeding and extraction risks
must ALWAYS remain binary — no fallback can reclassify these.

(c) **Binary count floor:** After all reclassifications, if binary risk count >= 5,
the binary count drags C7 down — but **never below the concept's heritage floor**.
A heritage-lineage D-T concept faces the same shared D-T binary risks (TBR,
tritium extraction, Li-6 supply, etc.) as every other D-T concept; the heritage
pathway acknowledges that mitigation paths exist for these shared risks. Crushing
C7 to 1.0 for a thoroughly-enumerated heritage concept punishes thoroughness, not
risk.

**Rule:** if binary risk count >= 5, set
`C7_new = min(C7_current, max(1.0, heritage_floor))`.

In words: drop C7 to the floor (heritage floor for heritage concepts, 1.0 for
non-heritage concepts), but only if doing so lowers C7 — never raise C7 with this
rule.

Heritage floors (lookup by concept ID prefix; D-T fuel only):

| Heritage lineage | Floor | Concept ID prefixes |
|-----------------|-------|---------------------|
| Tokamak | 4.0 | 01, 21, 28, 29, 33, 34 |
| Stellarator | 4.0 | 05, 09, 10, 20a, 20b, 36 |
| Spherical Tokamak | 3.0 | (assign if applicable) |
| Laser IFE | 3.5 | 03, 04, 17a, 17b, 26, 30, 31, 32 |
| Mirror | 2.5 | 06, 11 |
| FRC | 2.5 | 08, 18 |
| Z-pinch | 2.5 | 15 |
| magLIF | 3.0 | 07 |
| Non-heritage / alternate fuel | 1.0 | all others |

For non-D-T concepts (p-B11, D-He3, aneutronic, exotic), the floor is 1.0 — the
override fully crushes C7 as before.

**Worked examples:**
- 09-Proxima (Stellarator, 6 binaries): heritage floor = 4.0. C7_current = 4.0
  (after F-level heritage). Override → min(4.0, max(1.0, 4.0)) = 4.0. No change.
- 17a-Xcimer (Laser IFE, 7 binaries): heritage floor = 3.5. C7_current = 3.5.
  Override → min(3.5, max(1.0, 3.5)) = 3.5. No change.
- 27-Polywell (no heritage, 6 binaries hypothetical): floor = 1.0. C7_current = 3.0.
  Override → min(3.0, max(1.0, 1.0)) = 1.0. Full crush as before.

### Q3: Site-specific C5 check

For each concept, check if C5 includes site-specific adjustments (named sites,
brownfield advantages, proximity to water sources). If found, strip the adjustment
and recompute C5 from the rubric sub-factors only (thermal rejection + fuel safety).

### Q4: Sub-factor arithmetic check

For each concept:
- Recompute each criterion from its sub-factors using the framework formulas
- Flag any criterion where the reported score deviates >0.3 from the computed
  sub-factor average
- Check for double-counting between sub-factors within a criterion
- Remove any single-concept ad-hoc adjustments (bonuses or penalties not in the framework)
- Correct scores to match sub-factor arithmetic

### Q5: C7 verification

Verify that the Python-computed C7 correctly applied:
- Heritage credit floors on **F1-F7** (D-T concepts only) — the heritage floor is
  applied to every function score, not just F1-F3
- Function-level cap (any function mean <= 1.5 after heritage -> C7 capped at that value)
- Mean computation (mean of F1-F7, rounded to nearest 0.5)

If any computation appears incorrect, flag it as an informational output with the
expected value. Do NOT override Python's C7 — flag only.

### Q6: Peer consistency check

Compare C1-C8 scores within each peer group:

| Peer Group | Concepts |
|-----------|----------|
| D-T Tokamaks | 01-CFS, 21-TE, 28-ES, 29-Firefly, 33-BEST, 34-India |
| D-T Stellarators | 05-Thea, 09-Proxima, 10-Gauss, 20a-Type One, 20b-Renaissance, 36-Helical |
| D-T Mirrors | 11-Realta |
| D-T Laser IFE | 17a-Xcimer, 17b-Focused, 26-Indirect, 30-NIF, 31-Blue Laser, 32-French |
| D-T Pulsed (MIF/Z-pinch) | 07-MagLIF, 14-GF, 15-Zap |
| D-T Other | 22-FLF, 25-HIF, 12-OpenStar |
| D-He3/aneutronic FRC | 08-Helion, 18-TAE |
| p-B11 | 04-HB11, 06-CHARM, 24-DPF |
| Exotic | 02-Sonofusion, 03-Cortex, 13-Orbitron, 16-Acceleron, 19-Zephyr, 27-Polywell, 35-Polomac |

For each peer group (except Exotic, which is exempt from Q6 adjustments):
- Compute the peer median for each criterion
- Identify outliers: concepts with any criterion >= 1.0 away from the peer median
- For each outlier, read the synthesis justification
- If the gap is unjustified: adjust the score up to 1.0 toward the peer median
- If the gap reflects a genuine architectural differentiator: keep the score

### Q7: Review Q6 adjustments

Re-examine each Q6 adjustment from the previous step:
- **Revert** if the adjustment eliminates a genuine architectural differentiator
  (e.g., a concept genuinely has better modularization than its peers)
- **Keep** if the gap was truly unjustified (same architecture, similar design,
  no reason for the score difference)

Document each revert/keep decision with reasoning.

## Output Format

### Calibrated Score Table

Output the calibrated scores in this exact format (plain numbers only, no annotations):

```
| concept_id | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|------------|----|----|----|----|----|----|----|----|
| 01-hts-compact-tokamak | X.X | X.X | X.X | X.X | X.X | X.X | X.X | X.X |
...
```

### Adjustments Report

After the score table, report ALL adjustments made during calibration in this format:

| Concept | Question | Criterion | Original | Adjusted | Justification |
|---------|----------|-----------|----------|----------|---------------|
| ... | Q1/Q2/Q3/Q4/Q6 | C1/C3/... | X.X | X.X | ... |

Include Q7 revert/keep decisions as separate rows.

Write the calibrated score table and adjustments report to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/scores/calibration_body.md`
