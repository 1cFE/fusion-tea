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
- Per-concept `heritage_lineage`, `heritage_floor`, and `peer_group` derived from
  architecture (Confinement Family, topology, fuel, etc.) — use these for Q2
  binary-floor protection and Q6 peer comparisons. Do not infer lineage or peer
  group from concept IDs; the IDs have been renumbered and the per-concept
  fields above are authoritative.

**Do NOT re-extract scores from synthesis files.** Use this table as your starting point.

# Verified Scores

| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Binary Risks |
|---------|----|----|----|----|----|----|----|----|-------------|
| 01-hts-compact-tokamak | 2.8 | 2.5 | 2.7 | 4.0 | 1.7 | 2.5 | 4.0 | 4.0 | 4 |
| 02-acoustic-icf-sonofusion | 4.2 | 4.0 | 4.7 | 3.5 | 2.3 | 3.0 | 1.5 | 1.3 | 1 |
| 03-laser-icf-liquid-jet-target | 3.8 | 3.5 | 3.0 | 3.5 | 3.7 | 3.0 | 1.5 | 1.8 | 2 |
| 04-laser-icf | 4.3 | 3.5 | 3.7 | 3.0 | 3.7 | 4.0 | 1.5 | 2.1 | 1 |
| 05-planar-coil-stellarator | 3.2 | 2.5 | 3.3 | 3.8 | 2.5 | 2.5 | 4.0 | 3.5 | 2 |
| 06-magnetic-mirror | 2.8 | 3.5 | 3.7 | 2.5 | 4.3 | 4.5 | 3.0 | 2.0 | 1 |
| 07-maglif | 3.8 | 3.0 | 3.3 | 3.5 | 1.8 | 2.0 | 3.5 | 3.5 | 2 |
| 08-frc-w-direct-conversion | 4.2 | 3.5 | 3.9 | 3.3 | 3.7 | 3.5 | 3.0 | 2.8 | 4 |
| 09-qi-stellarator-hts | 5.0 | 2.5 | 3.4 | 4.0 | 1.7 | 2.5 | 4.0 | 3.8 | 2 |
| 10-large-scale-stellarator | 2.3 | 2.5 | 2.7 | 3.0 | 1.8 | 2.5 | 4.0 | 2.8 | 2 |
| 11-magnetic-mirror | 2.8 | 3.5 | 3.2 | 2.5 | 2.0 | 2.5 | 3.0 | 3.0 | 3 |
| 12-levitated-dipole | 3.8 | 2.0 | 2.7 | 3.5 | 1.7 | 2.5 | 1.5 | 3.8 | 3 |
| 13-electrostatic-hybrid | 4.3 | 4.0 | 4.2 | 3.5 | 1.7 | 2.5 | 1.5 | 1.8 | 5 |
| 14-magnetized-target-fusion-pneumatic-compression | 3.4 | 3.0 | 4.0 | 2.5 | 1.5 | 2.0 | 3.0 | 3.0 | 5 |
| 15-sheared-flow-stabilized-z-pinch | 4.8 | 3.5 | 2.5 | 3.5 | 1.7 | 2.0 | 2.5 | 3.0 | 6 |
| 16-muon-catalyzed-fusion | 1.8 | 4.0 | 2.4 | 3.5 | 1.7 | 2.5 | 2.5 | 1.5 | 5 |
| 17-laser-icf-direct-drive-fast-ignition | 2.5 | 3.5 | 3.3 | 2.8 | 1.7 | 2.0 | 3.5 | 3.0 | 3 |
| 18-p-b11-frc | 2.8 | 3.5 | 3.3 | 3.0 | 3.3 | 4.5 | 3.5 | 2.5 | 2 |
| 19-orbital-levitated-dipole | 3.0 | 2.0 | 1.7 | 2.5 | 4.5 | 4.0 | 1.5 | 1.5 | 4 |
| 20-type-one-stellarator | 1.3 | 2.5 | 4.2 | 4.0 | 1.7 | 2.5 | 4.0 | 3.8 | 4 |
| 21-renaissance-stellarator | 4.0 | 2.5 | 2.8 | 3.8 | 1.7 | 2.5 | 4.0 | 2.8 | 4 |
| 22-spherical-tokamak-hts | 3.3 | 3.0 | 3.7 | 2.5 | 1.8 | 2.5 | 3.5 | 2.8 | 2 |
| 23-projectile-icf | 3.2 | 4.0 | 2.8 | 4.0 | 1.7 | 2.0 | 1.5 | 2.3 | 4 |
| 24-laser-icf-nanostructured-target | 4.3 | 4.0 | 3.2 | 3.5 | 4.3 | 4.0 | 2.5 | 2.0 | 3 |
| 25-dense-plasma-focus | 4.6 | 4.0 | 3.2 | 3.5 | 5.0 | 4.0 | 1.5 | 1.8 | 5 |
| 26-heavy-ion-beam-icf | 5.0 | 3.5 | 2.8 | 3.5 | 1.7 | 2.0 | 2.5 | 3.2 | 6 |
| 27-laser-icf-hybrid-direct-drive | 2.8 | 4.0 | 2.8 | 3.0 | 1.7 | 2.0 | 3.5 | 3.0 | 6 |
| 28-polywell | 4.1 | 2.5 | 3.2 | 3.0 | 1.7 | 2.5 | 2.5 | 2.5 | 2 |
| 29-hts-tokamak-full-hts | 4.1 | 2.5 | 3.2 | 2.5 | 1.7 | 2.5 | 4.0 | 2.0 | 3 |
| 30-negative-triangularity-tokamak | 5.0 | 3.5 | 3.0 | 3.5 | 1.7 | 2.5 | 4.0 | 3.5 | 3 |
| 31-laser-icf-indirect-drive | 5.0 | 3.5 | 3.3 | 3.0 | 2.5 | 2.0 | 3.5 | 2.5 | 4 |
| 32-laser-icf-oec-architecture | 5.0 | 3.5 | 3.1 | 3.0 | 2.3 | 2.0 | 3.5 | 3.3 | 6 |
| 34-state-backed-tokamak-best | 2.7 | 2.5 | 3.5 | 3.0 | 1.8 | 2.5 | 4.0 | 2.5 | 3 |
| 35-polomac-magnetic-confinement | 2.5 | 4.0 | 3.6 | 3.5 | 2.5 | 3.5 | 1.5 | 1.5 | 3 |
| 36-helical-coil-stellarator | 2.5 | 2.5 | 2.8 | 4.0 | 1.7 | 2.5 | 4.0 | 2.5 | 2 |

## Function-Level Means (after heritage credit)

| Concept | F1 | F2 | F3 | F4 | F5 | F6 | F7 |
|---------|----|----|----|----|----|----|-----|
| 01-hts-compact-tokamak | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 02-acoustic-icf-sonofusion | 1.5 | 2.5 | 2.5 | 2.0 | 3.5 | 4.0 | 5.0 |
| 03-laser-icf-liquid-jet-target | 1.5 | 2.0 | 1.5 | 2.0 | 3.0 | 3.5 | 3.0 |
| 04-laser-icf | 1.5 | 3.0 | 2.5 | 2.5 | 5.0 | 4.5 | 4.0 |
| 05-planar-coil-stellarator | 4.0 | 5.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.5 |
| 06-magnetic-mirror | 2.0 | 2.5 | 3.0 | 3.5 | 5.0 | 3.0 | 2.5 |
| 07-maglif | 3.5 | 3.5 | 3.5 | 3.0 | 3.0 | 3.0 | 4.0 |
| 08-frc-w-direct-conversion | 2.5 | 3.0 | 3.0 | 3.0 | 4.0 | 2.0 | 3.5 |
| 09-qi-stellarator-hts | 4.0 | 4.0 | 4.5 | 4.0 | 4.0 | 4.0 | 4.0 |
| 10-large-scale-stellarator | 4.0 | 5.0 | 4.5 | 4.0 | 4.0 | 4.0 | 4.0 |
| 11-magnetic-mirror | 2.5 | 4.0 | 2.5 | 2.5 | 3.0 | 2.5 | 3.5 |
| 12-levitated-dipole | 2.0 | 1.5 | 3.0 | 2.5 | 2.5 | 2.0 | 2.0 |
| 13-electrostatic-hybrid | 1.5 | 2.5 | 2.0 | 1.5 | 4.5 | 1.5 | 3.5 |
| 14-magnetized-target-fusion-pneumatic-compression | 3.5 | 2.0 | 2.5 | 2.5 | 2.5 | 2.0 | 4.5 |
| 15-sheared-flow-stabilized-z-pinch | 2.5 | 2.5 | 3.0 | 2.5 | 2.5 | 2.5 | 3.5 |
| 16-muon-catalyzed-fusion | 2.0 | 2.0 | 3.0 | 3.0 | 2.5 | 2.0 | 3.5 |
| 17-laser-icf-direct-drive-fast-ignition | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 4.5 |
| 18-p-b11-frc | 2.0 | 3.0 | 3.0 | 3.0 | 5.0 | 4.5 | 4.5 |
| 19-orbital-levitated-dipole | 2.0 | 3.0 | 4.0 | 4.0 | 5.0 | 1.5 | 2.0 |
| 20-type-one-stellarator | 4.0 | 4.5 | 4.5 | 4.0 | 4.0 | 4.0 | 4.0 |
| 21-renaissance-stellarator | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 22-spherical-tokamak-hts | 3.5 | 3.5 | 4.0 | 3.5 | 3.0 | 3.0 | 4.0 |
| 23-projectile-icf | 1.5 | 2.5 | 2.5 | 3.0 | 3.5 | 3.5 | 5.0 |
| 24-laser-icf-nanostructured-target | 2.0 | 2.5 | 2.5 | 2.5 | 3.0 | 4.0 | 2.5 |
| 25-dense-plasma-focus | 1.5 | 3.5 | 1.5 | 2.5 | 2.5 | 2.0 | 1.5 |
| 26-heavy-ion-beam-icf | 2.0 | 2.0 | 2.0 | 2.0 | 2.5 | 3.0 | 3.5 |
| 27-laser-icf-hybrid-direct-drive | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 |
| 28-polywell | 2.0 | 2.5 | 2.0 | 2.0 | 2.5 | 2.0 | 5.0 |
| 29-hts-tokamak-full-hts | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 30-negative-triangularity-tokamak | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 31-laser-icf-indirect-drive | 3.5 | 3.5 | 4.5 | 3.5 | 3.5 | 3.5 | 3.5 |
| 32-laser-icf-oec-architecture | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 | 3.5 |
| 34-state-backed-tokamak-best | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| 35-polomac-magnetic-confinement | 2.5 | 5.0 | 1.5 | 3.5 | 3.5 | 3.5 | 5.0 |
| 36-helical-coil-stellarator | 4.0 | 4.0 | 5.0 | 4.0 | 4.0 | 4.0 | 4.0 |

## Energy Capture, Heritage, and Peer Group (audit trail)

Heritage lineage and floor are derived from architecture (table.csv), not from concept IDs, so they survive renumbering. Heritage credit applies to D-T fuel only — non-D-T concepts show floor 1.0.

| Concept | Energy Capture | η_th | Heritage Lineage | Floor | Peer Group |
|---------|----------------|------|------------------|-------|------------|
| 01-hts-compact-tokamak | Thermal (steam) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 02-acoustic-icf-sonofusion | TBD | 0.35 | — | 1.0 | Exotic |
| 03-laser-icf-liquid-jet-target | TBD | 0.35 | — | 1.0 | Exotic |
| 04-laser-icf | Thermal (steam) | 0.35 | — | 1.0 | p-B11 |
| 05-planar-coil-stellarator | Thermal (steam) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 06-magnetic-mirror | Direct (charged particle) | 0.70 | — | 1.0 | p-B11 |
| 07-maglif | Thermal (unspecified) | 0.35 | magLIF | 3.0 | D-T Pulsed (MIF/Z-pinch) |
| 08-frc-w-direct-conversion | Direct (inductive) | 0.85 | — | 1.0 | Aneutronic |
| 09-qi-stellarator-hts | Thermal (unspecified) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 10-large-scale-stellarator | Thermal (unspecified) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 11-magnetic-mirror | Hybrid (thermal + direct) | 0.55 | Mirror | 2.5 | D-T Mirrors |
| 12-levitated-dipole | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 13-electrostatic-hybrid | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 14-magnetized-target-fusion-pneumatic-compression | Thermal (steam) | 0.35 | — | 1.0 | Exotic |
| 15-sheared-flow-stabilized-z-pinch | Thermal (steam) | 0.35 | Z-pinch | 2.5 | D-T Pulsed (MIF/Z-pinch) |
| 16-muon-catalyzed-fusion | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 17-laser-icf-direct-drive-fast-ignition | Thermal (steam) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 18-p-b11-frc | Thermal (steam) | 0.35 | — | 1.0 | Aneutronic FRC |
| 19-orbital-levitated-dipole | Direct (charged particle) | 0.70 | — | 1.0 | Aneutronic |
| 20-type-one-stellarator | Thermal (steam) | 0.35 | Stellarator | 4.0 | D-T Stellarators |
| 21-renaissance-stellarator | Thermal (sCO2) | 0.48 | Stellarator | 4.0 | D-T Stellarators |
| 22-spherical-tokamak-hts | Thermal (unspecified) | 0.35 | Spherical Tokamak | 3.0 | D-T Tokamaks |
| 23-projectile-icf | Thermal (steam) | 0.35 | — | 1.0 | Exotic |
| 24-laser-icf-nanostructured-target | Hybrid (thermal + direct) | 0.55 | — | 1.0 | p-B11 |
| 25-dense-plasma-focus | Direct (charged particle) | 0.70 | — | 1.0 | p-B11 |
| 26-heavy-ion-beam-icf | Thermal (steam) | 0.35 | — | 1.0 | Exotic |
| 27-laser-icf-hybrid-direct-drive | Thermal (unspecified) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 28-polywell | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 29-hts-tokamak-full-hts | Thermal (unspecified) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 30-negative-triangularity-tokamak | Thermal (unspecified) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 31-laser-icf-indirect-drive | Thermal (steam) | 0.35 | Laser IFE | 3.5 | D-T Laser IFE |
| 32-laser-icf-oec-architecture | Hybrid (thermal + direct) | 0.55 | Laser IFE | 3.5 | D-T Laser IFE |
| 34-state-backed-tokamak-best | Thermal (unspecified) | 0.35 | Tokamak | 4.0 | D-T Tokamaks |
| 35-polomac-magnetic-confinement | Thermal (unspecified) | 0.35 | — | 1.0 | Exotic |
| 36-helical-coil-stellarator | Thermal (sCO2) | 0.48 | Stellarator | 4.0 | D-T Stellarators |

## Binary Risks per Concept

### 01-hts-compact-tokamak
- TBR < 1.0: FLiBe blanket fails to achieve sustained tritium breeding self-sufficiency (TBR <1.05 accounting for decay and processing losses)
- Tritium extraction system failure >24 hours: on-site tritium inventory exceeds regulatory limits (~2 kg threshold), forcing plant shutdown
- Li-6 enrichment supply chain failure: cannot secure 40-90% enriched Li at required quantity (380-850 tonnes per reactor), causing TBR to drop below 1.0
- FLiBe blanket catastrophic failure: leak, MHD flow blockage, or chemical instability ceases tritium breeding, forcing plant shutdown

### 02-acoustic-icf-sonofusion
- Ion temperature <10 keV in bubble plasma—acoustic cavitation cannot reach D-D fusion cross-section peak (~10⁸ K), resulting in Q=0 and zero net electricity output

### 03-laser-icf-liquid-jet-target
- Plasmonic nanoshell fusion mechanism undemonstrated — if field enhancement fails to accelerate deuterons to fusion threshold, no fusion occurs (F1 physics)
- Anomalous 3333 MeV/event energy figure — if calculation error and true D-D energy is ~3.65 MeV, Q~100 collapses by 1000× and Q_eng becomes negative (F1 physics)

### 04-laser-icf
- F1 Physics: Avalanche gain mechanism—if non-thermal alpha-induced chain reaction does not achieve gain >100, thermal p-B11 ignition is impossible due to bremsstrahlung exceeding fusion power, and the concept produces zero net electricity

### 05-planar-coil-stellarator
- TBR < 1.0 due to port fractions or penetration geometry errors—external tritium supply unsustainable at commercial scale
- Tritium extraction failure from LiPb—vacuum permeator or heat exchanger permeation barrier failure depletes inventory in days to weeks

### 06-magnetic-mirror
- p-B11 nonthermal plasma fails to achieve Q>1 due to insufficient alpha channeling efficiency (<4× rather than required 6.9×) or unmanageable bremsstrahlung losses (electron temperature cannot be maintained <50 keV), preventing net energy production at any scale

### 07-maglif
- TBR <1.0 in FLiBe blanket due to port fractions and axial RTL penetrations reducing effective solid-angle coverage below breeding threshold
- Tritium extraction failure from FLiBe blanket—bred tritium cannot be continuously removed at kg/day rates, causing blanket saturation and uncontrolled permeation exceeding regulatory limits

### 08-frc-w-direct-conversion
- F1 Physics: D-He3 ignition failure — below ~17 keV ion temperature threshold, D-He3 fusion is kinematically inaccessible; forces D-T fallback which structurally eliminates ~75% of direct conversion advantage
- F3 Physics: Gross FRC instability at 40 T compression — loss of confinement eliminates fusion yield; no mitigation if magnetic pressure exceeds stability limits
- F6 Physics: He3 self-breeding failure — eliminates fuel supply for commercial D-He3 operation; natural He3 supply cannot support even a single 50 MWe plant at commercial scale
- F6 Hardware: He3 extraction/purification failure — isotopic separation of He3 from D-He3/D-D exhaust at commercial throughput is undemonstrated; no operating analogue exists

### 09-qi-stellarator-hts
- TBR < 1.05 after all engineering losses (island divertor penetrations, coil support structures) causes tritium self-sufficiency failure requiring external tritium supply and limiting fleet deployment
- Island divertor failure to maintain detachment at 4.05 MW/m² causes tungsten sputtering accumulation leading to radiative collapse and operations halt

### 10-large-scale-stellarator
- TBR < 1.0 for D-T stellarator due to neutronics modeling error or geometric losses (gaps, ports, tight-clearance TBR/shielding trade-off), causing tritium self-sufficiency failure and inability to sustain burning plasma beyond startup inventory depletion
- Tritium extraction system failure (efficiency <90% or throughput <150 g/day) from Li₄SiO₄ pebbles or PbLi liquid, causing tritium inventory holdup exceeding regulatory limits or unacceptable environmental release, preventing full-duty-cycle operation

### 11-magnetic-mirror
- TBR < 1.0 after realistic port penetrations in cylindrical 2π blanket geometry
- Tritium extraction failure from Li circuit at kg/day fusion plant scale
- End-plug confinement failure below Q = 3 due to DCLC instability

### 12-levitated-dipole
- TBR < 1.0: 10% margin above breakeven leaves little tolerance for blanket module failures or extraction inefficiency
- Tritium extraction failure from Li₂O solid ceramic at kg/day scale: no operating analogue at fusion plant throughput
- F2 Physics: ICRH coupling in dipole geometry — never demonstrated; no published RF coupling study; if ICRH cannot deliver 44.5 MW absorbed power in dipole field topology, ECRH fallback at 30-40% efficiency breaks the recirculating power balance and plant cannot reach net electricity

### 13-electrostatic-hybrid
- F1-Physics: Q>1 not demonstrated — without ion density ≥5×10¹⁰ cm⁻³ and confinement time ≥0.1 ms, net electricity is impossible
- F2-Physics: Ion loading efficiency <50% — if true, recirculating power exceeds gross electric even at Q_plasma>1
- F3-Physics: Diocotron or ECDI instability at n>10¹⁰ cm⁻³ — if space-charge mitigation fails, Q>1 is impossible
- F4-Hardware: Neutron-induced HV breakdown in cathode or feedthrough — if 14 MeV neutrons cause electrical arc-through, module cannot sustain 300 kV required for fusion
- F6-Physics: Tritium self-breeding TBR<1.0 — mandatory for fleet-scale power generation; external tritium purchase is not valid fallback per framework mandatory binary classification

### 14-magnetized-target-fusion-pneumatic-compression
- Driver physics: 12:1 compression ratio in liquid metal (8:1 achieved in water vs. 12:1 target) — if unachieved, plasma cannot reach fusion conditions
- Driver hardware: Piston synchronization and <1 second reset time at 1 Hz — if failed, plant cannot achieve commercial rep rate
- Instability control hardware: Liquid metal vortex stable formation and <1 second reformation at 1 Hz — if failed, concept is not viable
- Fuel cycle physics: TBR < 1.0 — if unachieved, tritium self-sufficiency impossible
- Fuel cycle hardware: Tritium extraction efficiency >95% from liquid metal — if failed, radiological safety failure

### 15-sheared-flow-stabilized-z-pinch
- Plasma Q < 5 or pinch lifetime < 100 µs: recirculating fraction exceeds 85%, net output collapses to marginal levels
- Pulsed power capacitors/switches not manufacturable at 10⁸–10⁹ shot lifetime and 50–200 kV ratings: no viable driver technology
- MHD instabilities beyond 100 µs defeat sheared-flow stabilization: Q cannot reach commercial target
- LiPb flow failure at 10 Hz: simultaneous loss of first wall, breeding, shielding, and heat extraction
- TBR < 1.0 due to blanket coverage gaps or neutron leakage: tritium self-sufficiency lost, external supply infeasible
- Tritium extraction from LiPb < 1 kg/day plant-wide: inventory accumulation to unsafe levels or burn rate shortfall

### 16-muon-catalyzed-fusion
- Tritium breeding ratio (TBR < 1.0 for MCF chamber geometry with beam injection ports) — all D-T concepts require TBR > 1 for fuel self-sufficiency
- Fuel cycle closure (tritium extraction failure at kg/day or permeation loss >1% at 800–1300 K) — forces external tritium dependence, non-viable for commercial deployment
- Energy balance viability (Q_sci × M × η_th ≤ 1 at achievable E_mu and N_fus) — plant produces less gross electric than accelerator consumes; net electricity is impossible
- F1 Physics: D-T catalysis fusions/muon ceiling — if N_fus cannot exceed ~350 at E_mu ≤ 2.5 GeV (LAMPF demonstrated 150 at low-T; Yamashita 2022 high-T kinetics unvalidated by experiment), the energy balance Q_sci × M × η_th ≤ 1 and net electricity is impossible
- F2 Physics: Muon production energy cost — if E_mu cannot be reduced from current ~6 GeV/muon (PSI/TRIUMF/LAMPF) to <2.5 GeV/muon target via active-target geometry, recirculating power exceeds gross output and plant is a net energy consumer

### 17-laser-icf-direct-drive-fast-ignition
- TBR < 1.0: Tritium breeding ratio below 1.0 (accounting for extraction losses) prevents fuel self-sufficiency; plant shuts down after startup inventory depletion (5-10 years); global tritium supply insufficient for long-term D-T operation
- Proton coupling efficiency η_coup < 7%: Fast ignition threshold failure — hot spot never reaches thermonuclear conditions, fusion yield is zero, plant produces no net electricity
- Petawatt ignition laser failure at 10 Hz: If ignition laser cannot deliver 150 kJ at 10 Hz with ±10 ps timing, ignition fails and fusion yield is zero; compression laser alone produces Q < 1 (no ignition, no net electricity)

### 18-p-b11-frc
- Q_plasma < viability threshold—p-B11 FRC cannot achieve Q≥14 (steam) or Q≥5 (ICC) due to bremsstrahlung power balance failure or insufficient confinement quality at 150 keV ion temperature
- FRC tilt instability at reactor scale—NBI-driven stabilization fails at 1–2 m major radius and multi-megaampere plasma current, causing FRC collapse and loss of plasma confinement

### 19-orbital-levitated-dipole
- F1.1: Confinement scaling weaker than R² → net fusion power unachievable at viable spacecraft mass
- F1.2: HTS coil quench or radiation degradation in LEO → loss of confinement, no on-orbit repair
- F6.1: He3 self-breeding at equimolar D:He3 is 13× insufficient per cross-section arithmetic; market purchase at $30M/kg drives LCOE to $8,863/MWh (59× terrestrial parity)
- F6.2: He3 delivery failure (via self-breeding or launch resupply) → concept cannot operate, no substitute fuel exists

### 20-type-one-stellarator
- F1 Physics: Plasma confinement time insufficient for Q > 5 (no net electricity if τ_E does not scale to ignited burn)
- F5 Hardware: HTS coil radiation damage > 5% critical current degradation over 30-year lifetime (coil replacement impractical in stellarator non-axisymmetric geometry)
- F6 Physics: Tritium breeding ratio < 1.0 after extraction losses (tritium inventory depletes, no external supply at 50 kg/year scale)
- F6 Hardware: Tritium extraction efficiency < 85% from HCPB over 2-year continuous cycle (inventory depletion, cannot backfill mid-cycle)

### 21-renaissance-stellarator
- TBR < 1.0 (F5 physics; mandatory binary per framework)
- Tritium extraction failure from Li-LiH circuit (F6 physics; mandatory binary per framework)
- Tritium permeation through sCO2 heat exchangers exceeds regulatory limits (F6 hardware; mandatory binary per framework)
- Plasma confinement shortfall prevents ignition (Q=∞ target); if n·τ_E ~11× below Lawson threshold cannot be closed via higher T or confinement improvement, concept fails to achieve net electricity at competitive cost (F1 physics; binary due to ignition dependency)

### 22-spherical-tokamak-hts
- TBR <1.0 in operating blanket due to port fractions and assembly gaps reducing effective solid-angle coverage below breeding threshold
- Tritium extraction failure from liquid Li blanket—bred tritium cannot be continuously removed at kg/day rates, causing blanket saturation and uncontrolled permeation

### 23-projectile-icf
- Target gain <200× at 60 km/s prevents plant from achieving 333 MWe net output at stated rep rates (F1 Physics)
- Electromagnetic launcher bore lifetime <10^5 shots requires barrel replacement every ~35 days; if replacement cost >$10M and downtime >1 week, plant availability drops below 50% (F2 Hardware)
- Liquid lithium curtain blast disruption creating neutron streaming paths to vessel, causing dpa >0.5/FPY and forcing vessel replacement every 10–20 years instead of never (F4/F5 Hardware combined)
- Tritium breeding ratio <1.0 requires continuous external tritium supply at ~$1–2B/year for 333 MWe plant, collapsing economics (F6 Physics)

### 24-laser-icf-nanostructured-target
- F1 Physics: p-B11 ignition failure — HB11 experimental data at Q ~ 0.00005 (0.005% efficiency), four orders of magnitude below Q ≥ 1 required for net energy. Non-thermal ignition mechanisms (block ignition, avalanche fast ignition) theoretically plausible but experimentally unvalidated.
- F2 Physics: Laser wall-plug efficiency <5% — If WPE drops below ~5%, recirculating power fraction exceeds ~50% at Q_eng = 5, making plant a net energy consumer. 10% WPE target (HB11 stated; Marvel unpublished) is necessary for breakeven.
- F7 Physics: Marvel hybrid DEC failure — If Marvel's claimed 70% hybrid efficiency (magnetic + electrostatic + steam) fails to achieve >20% and no steam-cycle fallback is implemented, net electrical output falls by ~60%, pushing Q_eng requirement from 5 to >10. HB11's explicit steam-cycle fallback (38%) mitigates this risk for the p-B11 IFE concept family.

### 25-dense-plasma-focus
- QMF bremsstrahlung suppression factor < 1.5 (if QMF does not provide ≥1.5× suppression, classical bremsstrahlung losses make p-B11 net energy impossible in DPF geometry)
- Combined direct energy conversion efficiency < 60% (if ion beam decelerator + X-ray photoelectric converter combined efficiency < 60%, net electric power is negative at achievable Q < 2.5, eliminating the concept)
- F1-physics: nτ confinement product never reaches 2×10¹³ s/cm³ (22-year yield plateau at 0.25 J in FF-2B; current nτ is 8.3× below ignition threshold; the synthesis itself notes Q < 1.41 → zero net electricity, which is the binary criterion). Reclassified from Degrading to Binary.
- F3-physics: Filament disruption in current sheath remains unmitigated (firm observational evidence in FF-2B that filaments are disrupted during pulse run-down, causing 'low densities and lower-than-predicted yields' for 22 years; no demonstrated mitigation pathway; same Q < 1.41 binary threshold applies).
- F7-physics: Ion beam quality (divergence, energy spread, multi-species composition) incompatible with decelerator capture geometry. Beam characterization is incomplete and the only energy-conversion pathway has no thermal fallback; failure here eliminates LCOE entirely.

### 26-heavy-ion-beam-icf
- F1 Physics: Target gain < 30 prevents net electricity (Q_eng < 3)
- F2 Physics: Beam delivery failure (cannot achieve 5-8 MJ at <5 mm spot size) collapses target gain
- F3 Physics: Compression asymmetry >5% prevents ignition
- F4 Physics: FLiBe jet reformation failure or vapor pressure exceeds beam transport threshold stops shots
- F6 Physics: TBR < 1.0 prevents tritium self-sufficiency; no external supply at scale
- F1 Hardware: Target fabrication throughput failure (cannot sustain 6 Hz with quality control) stops plant operation

### 27-laser-icf-hybrid-direct-drive
- Two-beam HDD implosion achieving Qc > 200 at 8–12 MJ scale — if implosion symmetry fails or gain plateaus below Qsci ~150, wall-plug gain Q_wp < 10 and concept is non-viable
- Two-beam illumination geometry delivering <5% drive asymmetry — if asymmetry exceeds tolerance, implosion fails
- Rayleigh-Taylor instability growth limited to <5% for Qc > 200 in two-beam HDD geometry — if RT cannot be controlled, implosion fails
- SBS/NLO pulse compression preserving wavefront quality at >100 kJ per pulse — if phase conjugation fails, beam delivery is compromised and implosion fails
- Tritium breeding ratio TBR ≥ 1.05 (FLiNaK commercial blanket) — if TBR < 1.0, external tritium supply required (economically disqualifying)
- Tritium extraction from FLiBe at kg/day scale — if extraction fails, tritium inventory exceeds regulatory limits and forces shutdown

### 28-polywell
- F1 Physics: Virtual cathode formation and electron confinement (γ ≤ 0.18) required for net power — if virtual cathode does not form at reactor density ~10²¹ m⁻³ or if loss reduction factor γ > 0.18, net electric output is negative
- F6 Physics: Tritium breeding ratio TBR ≥ 1.0 in polyhedral coil geometry — neutron shadowing by six coil faces may prevent TBR ≥ 1.0; no neutronics study exists; external tritium purchase is cost-prohibitive

### 29-hts-tokamak-full-hts
- TBR < 1.0 for D-T fuel cycle (F6 Physics) — fuel self-sufficiency failure if tritium breeding ratio falls below 1.0; external tritium purchase not valid fallback per framework
- Tritium extraction failure (F6 Hardware) — if extraction efficiency from blanket <90%, fuel cycle inventory balance fails; external tritium supply not valid fallback
- Steady-state D-T burn at Q_eng ≥ 4.5 not achieved (F1 Physics) — if AI plasma control fails to suppress disruptions and achieve steady-state burn with engineering gain ≥4.5, recirculating power exceeds gross electric output

### 30-negative-triangularity-tokamak
- TBR < 1.0 in NT geometry with realistic blanket penetrations — tritium self-sufficiency failure
- Tritium extraction from FLiBe at kg/day scale — failed chemistry or permeation control causing inventory loss
- Ohmic-only scenario failure if H_NA < 1.5 at burning plasma — insufficient heating requiring auxiliary systems restoration

### 31-laser-icf-indirect-drive
- Target gain Q_sci < 30×: no net electricity; plant operates at severe loss
- Laser driver system failure: no fusion pulse, zero generation output
- Rayleigh-Taylor instability runaway: capsule implosion fails, no ignition
- Tritium breeding ratio TBR < 1.0: cannot sustain fuel inventory, external tritium purchase required (limited global supply, plant shutdown when CANDU depletes)

### 32-laser-icf-oec-architecture
- Plasma performance: Target gain G<60 at 10 Hz → recirculating power fraction exceeds unity → no net electricity
- Driver (OEC enhancement): Cavity enhancement factor <10^4 → insufficient laser energy delivery (<0.5 MJ/shot UV) → no ignition possible
- Driver (mirror degradation): OEC mirror reflectivity degradation >0.01% per 10^6 shots → enhancement factor collapse → driver energy <0.5 MJ/shot → no ignition
- Instability control: Laser-plasma instability backscatter >20% → absorbed energy below ignition threshold → gain <50 → no net electricity at 10 Hz operation
- Fuel cycle (TBR): Tritium breeding ratio <1.0 → cannot sustain D-T fuel cycle without external tritium purchase (mandatory binary per framework)
- Fuel cycle (extraction failure): Tritium extraction system complete failure (0% efficiency) → fuel starvation → forced shutdown

### 34-state-backed-tokamak-best
- Disruption frequency >36/yr causes cumulative first-wall damage requiring replacement every 1–2 years, rendering plant economically non-viable
- RWM stabilization failure at βN>3.5 prevents access to CFETR Phase II performance, limiting Q to ~3 (insufficient for commercial viability)
- TBR<1.0 forces external tritium purchase at $13M/yr, unsustainable at commercial scale

### 35-polomac-magnetic-confinement
- F1 Plasma Performance (physics): D-D confinement at Q ≥ 10 unvalidated—if Q < 7, net power is minimal or negative, rendering the concept economically nonviable. Historical dipole experiments achieved few-eV plasma at 10¹⁶ m⁻³ (seven orders of magnitude below fusion-relevant 100–200 keV, 10²¹ m⁻³). Company claims 20–40 s confinement with no experimental basis, no physics model, and no independent validation (Tier 1).
- F3 Instability Control (physics): High-beta dipole confinement at β = 70–80% (JTSP 2024 claim, vs. 20–30% Elio 2014—3× discrepancy unexplained) must be MHD-stable at fusion conditions. If ballooning or interchange instabilities are triggered at β > 30–40%, plasma is lost and cannot be confined. No MHD stability analysis exists; magnetic tunnel structural supports are validated only by FEA (Tier 2, simulation); no experimental demonstration at any scale.
- F6 Fuel Cycle Closure (physics-contingent): D-D fuel eliminates tritium breeding but requires D-D confinement at Q ≥ 10 for economic viability. If D-D confinement physics limits Q ≤ 7 (plausible given lower fusion cross-section and higher bremsstrahlung radiation at 100–200 keV), the fuel cycle advantage (no blanket) is negated by inability to achieve net power. D₂ fuel handling is mature (Tier 5), but D-D ignition scaling is unvalidated (Tier 1)—fuel cycle closure is contingent on F1 plasma performance.

### 36-helical-coil-stellarator
- TBR < 1.0 at 80 at.% Li-6 enrichment (if 3D neutron transport calculation yields TBR below unity, tritium self-sufficiency is impossible and design cannot proceed)
- Tritium breeding failure in Sn-In-Pb-Li blanket system (heliotron coil geometry intrusion into blanket space reduces coverage; if TBR cannot reach ≥1.05 even with 80 at.% Li-6—highest enrichment feasible due to global supply constraints—concept is not viable for D-T operation)



## Concept File Paths

When you need justification detail for a calibration question, read the synthesis
and/or analysis file at the paths below. Read on demand — do not read all files upfront.

- **01-hts-compact-tokamak**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\01-hts-compact-tokamak\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\01-hts-compact-tokamak\analysis.md`
- **02-acoustic-icf-sonofusion**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\02-acoustic-icf-sonofusion\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\02-acoustic-icf-sonofusion\analysis.md`
- **03-laser-icf-liquid-jet-target**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\analysis.md`
- **04-laser-icf**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\analysis.md`
- **05-planar-coil-stellarator**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\05-planar-coil-stellarator\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\05-planar-coil-stellarator\analysis.md`
- **06-magnetic-mirror**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\06-magnetic-mirror\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\06-magnetic-mirror\analysis.md`
- **07-maglif**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\07-maglif\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\07-maglif\analysis.md`
- **08-frc-w-direct-conversion**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\08-frc-w-direct-conversion\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\08-frc-w-direct-conversion\analysis.md`
- **09-qi-stellarator-hts**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\09-qi-stellarator-hts\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\09-qi-stellarator-hts\analysis.md`
- **10-large-scale-stellarator**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\10-large-scale-stellarator\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\10-large-scale-stellarator\analysis.md`
- **11-magnetic-mirror**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\11-magnetic-mirror\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\11-magnetic-mirror\analysis.md`
- **12-levitated-dipole**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\12-levitated-dipole\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\12-levitated-dipole\analysis.md`
- **13-electrostatic-hybrid**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\analysis.md`
- **14-magnetized-target-fusion-pneumatic-compression**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\14-magnetized-target-fusion-pneumatic-compression\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\14-magnetized-target-fusion-pneumatic-compression\analysis.md`
- **15-sheared-flow-stabilized-z-pinch**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\15-sheared-flow-stabilized-z-pinch\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\15-sheared-flow-stabilized-z-pinch\analysis.md`
- **16-muon-catalyzed-fusion**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\16-muon-catalyzed-fusion\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\16-muon-catalyzed-fusion\analysis.md`
- **17-laser-icf-direct-drive-fast-ignition**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\17-laser-icf-direct-drive-fast-ignition\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\17-laser-icf-direct-drive-fast-ignition\analysis.md`
- **18-p-b11-frc**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\18-p-b11-frc\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\18-p-b11-frc\analysis.md`
- **19-orbital-levitated-dipole**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\19-orbital-levitated-dipole\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\19-orbital-levitated-dipole\analysis.md`
- **20-type-one-stellarator**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\20-type-one-stellarator\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\20-type-one-stellarator\analysis.md`
- **21-renaissance-stellarator**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\21-renaissance-stellarator\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\21-renaissance-stellarator\analysis.md`
- **22-spherical-tokamak-hts**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\22-spherical-tokamak-hts\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\22-spherical-tokamak-hts\analysis.md`
- **23-projectile-icf**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\23-projectile-icf\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\23-projectile-icf\analysis.md`
- **24-laser-icf-nanostructured-target**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\24-laser-icf-nanostructured-target\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\24-laser-icf-nanostructured-target\analysis.md`
- **25-dense-plasma-focus**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\25-dense-plasma-focus\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\25-dense-plasma-focus\analysis.md`
- **26-heavy-ion-beam-icf**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\26-heavy-ion-beam-icf\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\26-heavy-ion-beam-icf\analysis.md`
- **27-laser-icf-hybrid-direct-drive**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\27-laser-icf-hybrid-direct-drive\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\27-laser-icf-hybrid-direct-drive\analysis.md`
- **28-polywell**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\28-polywell\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\28-polywell\analysis.md`
- **29-hts-tokamak-full-hts**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\29-hts-tokamak-full-hts\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\29-hts-tokamak-full-hts\analysis.md`
- **30-negative-triangularity-tokamak**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\30-negative-triangularity-tokamak\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\30-negative-triangularity-tokamak\analysis.md`
- **31-laser-icf-indirect-drive**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\31-laser-icf-indirect-drive\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\31-laser-icf-indirect-drive\analysis.md`
- **32-laser-icf-oec-architecture**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\32-laser-icf-oec-architecture\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\32-laser-icf-oec-architecture\analysis.md`
- **33-laser-icf-french-national**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\33-laser-icf-french-national\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\33-laser-icf-french-national\analysis.md`
- **34-state-backed-tokamak-best**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\34-state-backed-tokamak-best\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\34-state-backed-tokamak-best\analysis.md`
- **35-polomac-magnetic-confinement**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\35-polomac-magnetic-confinement\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\35-polomac-magnetic-confinement\analysis.md`
- **36-helical-coil-stellarator**
  - Synthesis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\36-helical-coil-stellarator\synthesis.md`
  - Analysis: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\analyses\36-helical-coil-stellarator\analysis.md`

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

**Use the `heritage_floor` column in the verified scores table for each concept.**
Do not infer it from the concept ID. The lineage values that can appear are:

| Heritage lineage | Floor |
|-----------------|-------|
| Tokamak | 4.0 |
| Spherical Tokamak | 3.0 |
| Stellarator | 4.0 |
| Laser IFE | 3.5 |
| Mirror | 2.5 |
| FRC | 2.5 |
| Z-pinch | 2.5 |
| magLIF | 3.0 |
| (none) — non-D-T or no recognized lineage | 1.0 |

For non-D-T concepts (p-B11, D-He3, aneutronic, exotic), the heritage_floor is
1.0 — the override fully crushes C7 as before.

**Worked examples** (lineage is shown in the verified scores table for each):
- A D-T stellarator concept with 6 binaries: heritage_floor = 4.0,
  C7_current = 4.0. Override → min(4.0, max(1.0, 4.0)) = 4.0. No change.
- A D-T laser IFE concept with 7 binaries: heritage_floor = 3.5,
  C7_current = 3.5. Override → min(3.5, max(1.0, 3.5)) = 3.5. No change.
- A non-heritage D-T concept (e.g. polywell, muon-catalyzed) with 6 binaries:
  heritage_floor = 1.0, C7_current = 3.0. Override → min(3.0, max(1.0, 1.0))
  = 1.0. Full crush as before.

### Q3: Site-specific C5 check

For each concept, check if C5 includes site-specific adjustments (named sites,
brownfield advantages, proximity to water sources). If found, strip the adjustment
and recompute C5 from the rubric sub-factors only (thermal rejection + fuel safety).

### Q4: Sub-factor arithmetic check (MANDATORY for EVERY concept)

For **every** concept (no spot-checking — do all 35), open the synthesis and
recompute each criterion from its enumerated sub-factors. Apply corrections
**by adjusting the score in the calibrated table**, not just by flagging.

Specific checks that must be performed on every concept:

1. **C3 Sub-factor B**: Find the synthesis's bottleneck enumeration. Verify:
   - He-3 dependency uses **-1.5** (not -1.0 hard constraint)
   - Each hard constraint correctly applies -1.0
   - Each scaling constraint correctly applies -0.5
   - Each sole-source dependency correctly applies -0.25
   - Sum: `B_new = 5.0 - sum(corrected penalties)`, clamped to [1, 5]
   - Recompute `C3 = (A + B_new + C) / 3`

2. **C5 site-specific stripping**: per Q3.

3. **Sub-factor denominator sanity**: if sub-factor weights (capital shares,
   etc.) don't sum to ~100%, recompute on a normalized basis.

4. **Internal contradictions**: if the synthesis text states one C3/C4/C5 value
   in prose but the YAML reports a different value, use the YAML and flag the
   inconsistency. If both prose and YAML disagree with the sub-factor
   arithmetic, use the arithmetic.

5. **Single-concept ad-hoc adjustments**: remove any bonuses or penalties not
   in the framework.

For each correction, record an entry in the adjustments report with original
score, adjusted score, and the explicit arithmetic chain.

### Q5: C7 verification and correction

For each concept, verify the Python-computed C7. **Override C7 in the
calibrated table** (not just flag) if:

- **Evidence Tier mis-assignment**: Any cell in the C7 risk matrix has Tier
  ≥ 3 when the synthesis's own evidence summary indicates Tier 1-2 per the
  anti-leniency, time-stuck, or operating-hardware rules in
  `scoring_framework.md`. Recompute the affected F as the mean of corrected
  cell tiers, then C7 = mean(F1..F7) with heritage floor and function-level
  cap re-applied.

- **Binary mis-classification**: Any "Degrading" cell whose synthesis text
  describes a Q < 1 failure mode (i.e., zero net electricity outcome). Recount
  binaries with corrections; if count crosses ≥ 5, apply the Q2 floor crush:
  `C7_new = min(C7_recomputed, max(1.0, heritage_floor))`.

- **Function-level cap missed**: if any function score F_n ≤ 1.5 after
  corrections, C7 must equal min(mean_C7, min F).

Document each C7 override in the adjustments report with the cell-level
corrections that drove it.

Heritage credit and mean computation: if these were applied incorrectly by
Python, flag (do not override — Python owns the heritage and mean math).

### Q6: Peer consistency check

Group concepts by the `peer_group` column in the verified scores table. The
groups assigned by the extractor are:

| Peer Group | Description |
|-----------|-------------|
| D-T Tokamaks | D-T fuel + Tokamak or Spherical Tokamak lineage |
| D-T Stellarators | D-T fuel + Stellarator lineage |
| D-T Mirrors | D-T fuel + Mirror lineage |
| D-T Laser IFE | D-T fuel + Laser IFE lineage |
| D-T Pulsed (MIF/Z-pinch) | D-T fuel + Z-pinch or magLIF lineage |
| Aneutronic FRC | D-He3 or p-B11 fuel + Compact Toroid (FRC) topology |
| p-B11 | p-B11 fuel, non-FRC |
| Aneutronic | D-He3 fuel, non-FRC |
| Exotic | D-T concepts with no recognized heritage lineage, D-D concepts, and exotic/non-power |

For each peer group (except Exotic and any singleton group, which are exempt
from Q6 adjustments):
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

Write the calibrated score table and adjustments report to: `C:\Users\mallo\1cfe\fusion-tea\exploration\concept_analysis\scores\calibration_body.md`
