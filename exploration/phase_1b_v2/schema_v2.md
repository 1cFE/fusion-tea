# Phase 1b v2: Differentiation Table Schema

**Version**: 2.0
**Last updated**: 2026-03-08
**Based on**: Phase 1a schema v0.2.3

This document defines the columns, controlled vocabulary, and rules for the fusion concept differentiation table. Version 2.0 replaces the flat {Confinement Family, Confinement Concept} pair with a hierarchical tree of 8 family-specific and sub-type-specific columns that are real morphological dimensions. See `plan.md` for the rationale.

---

## Conventions

### N/A vs TBD vs Unknown

- **N/A**: The question is **structurally inapplicable** to this concept. The physics or architecture make the column meaningless. Just use `N/A` — no justification suffix needed.
- **TBD**: The question **applies** to this concept, but the answer is not publicly known or not yet decided by the company.
  - Example: "Tritium Breeding" for an early-stage D-T startup that hasn't specified blanket type → `TBD`
- **Unknown**: We could not determine the answer from available sources, but the question applies and the company may have an answer internally.
  - Example: A concept with almost no public information → `Unknown`

### Citation Format

Every non-obvious value in the table should be traceable. In per-concept dossiers, each column value carries:
- **Citation**: URL, paper reference, or `knowledge/sources/...` path
- **Confidence** (per-cell): `high` (directly stated by source) · `medium` (inferred from described approach) · `low` (extrapolated from similar concepts)
- **Overall Confidence** (per-concept, in `table.csv`): Five-level scale — `high` · `medium-high` · `medium` · `medium-low` · `low`. Reflects the aggregate quality of a concept's dossier. Per-cell confidence remains three-level.

### Controlled Vocabulary Rules

- Use the exact vocabulary string from this document. Do not paraphrase or abbreviate.
- If no vocabulary value fits, record the best-fit value AND add a note explaining the discrepancy. Flag for schema review at the next checkpoint.
- A value may include a parenthetical qualifier when the base vocabulary is correct but the specific variant matters: e.g., `RF (ECRH)` vs `RF (ICRH)`.

### N/A Scoping Rules for Confinement Columns

Columns 2–8 are **family-specific or sub-type-specific**. Each column applies only within its declared scope:

| Column | Applies to | N/A for |
|--------|-----------|---------|
| MFE Topology | MFE concepts (19) | All non-MFE (19) |
| IFE Driver | IFE concepts (12) | All non-IFE (26) |
| MIF Method | MIF concepts (3) | All non-MIF (35) |
| Non-Standard Mechanism | Non-Standard concepts (4) | All non-NS (34) |
| Tokamak Shape | Tokamak concepts (6) | All non-Tokamak (32) |
| Stellarator Type | Stellarator concepts (6) | All non-Stellarator (32) |
| Laser Approach | Laser IFE concepts (9) | All non-Laser (29) |

A concept gets N/A in every family-specific column outside its branch. These N/As are structurally justified — they represent questions that are not meaningful for that concept.

---

## Metadata Columns

These columns are carried for identification but are not part of the differentiation analysis.

| Column | Definition | Source |
|--------|-----------|--------|
| **Concept Name** | Descriptive name including distinguishing features | CSV / research |
| **Companies** | Companies actively pursuing this concept | CSV / research |
| **Description** | 1-3 sentence technical summary | CSV, enriched by research |
| **Published Machine/Plant?** | Has a specific reactor/plant design been published? | CSV / research |
| **Lab Experiments** | University or national lab experiments demonstrating relevant physics | CSV / research |

---

## Differentiation Columns

### Column 1: Confinement Family

**Definition**: Top-level physics category for how the plasma is confined (or not confined) during the fusion reaction.

| Value | Description |
|-------|-------------|
| `MFE` | Magnetic Fusion Energy — plasma confined by external or self-generated magnetic fields in steady-state or quasi-steady-state |
| `IFE` | Inertial Fusion Energy — plasma confined by its own inertia during a brief implosion event |
| `MIF` | Magneto-Inertial Fusion — magnetized plasma compressed by an external driver (pulsed power, mechanical, or magnetic); intermediate between MFE and IFE in density and timescale |
| `Non-Standard` | Concepts that do not fit MFE/IFE/MIF: electrostatic confinement (IEC, Polywell), dense plasma focus, muon-catalyzed fusion |

**Notes**:
- FRC-based concepts are classified by their operational mode: steady-state beam-driven FRC (TAE) → `MFE`; pulsed FRC compression (Helion) → `MIF`.
- Z-pinch concepts that use self-generated fields are `MFE` (the confinement is magnetic, even though the geometry is linear and pulsed).
- "Hybrid" is not a family — use the dominant confinement mechanism.
- Acoustic / Sonofusion reclassified from "Other" to `IFE` — acoustic cavitation IS inertial compression.
- Old `Electrostatic` and `Other` families merged into `Non-Standard`.

---

### Column 2: MFE Topology

**Definition**: What magnetic topology does this MFE concept use? This distinguishes the fundamental magnetic field geometry.

**Applies to**: MFE concepts only (19 of 38). All non-MFE concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `Tokamak` | Axisymmetric torus with plasma current providing rotational transform. Includes compact, spherical, standard, and NT variants. |
| `Stellarator` | Non-axisymmetric torus where external coils provide all rotational transform. No plasma current needed. |
| `Open/Linear` | Open-ended magnetic geometry — mirrors, Z-pinch, other linear configurations. |
| `Compact Toroid` | Toroidal plasma without external toroidal field coils. FRC (field-reversed configuration). |
| `Dipole` | Plasma confined by the dipolar field of a single current loop. |

---

### Column 3: IFE Driver

**Definition**: What drives the implosion in this IFE concept? This distinguishes the energy delivery mechanism.

**Applies to**: IFE concepts only (12 of 38). All non-IFE concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `Laser` | Laser-driven target compression/ignition. Multiple sub-approaches (see Column 8: Laser Approach). |
| `Projectile` | Hypervelocity projectile impact drives target compression. |
| `Heavy ion beam` | Accelerator-driven heavy ion beams ablate target. |
| `Acoustic` | Sound-driven bubble implosion (sonoluminescence/cavitation). |

---

### Column 4: MIF Method

**Definition**: What compression method does this MIF concept use?

**Applies to**: MIF concepts only (3 of 38). All non-MIF concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `FRC compression` | Pulsed electromagnetic compression of FRC plasmoids. (Helion Energy.) |
| `Magnetized target` | Magnetized plasma compressed by liner implosion — pulsed power (MagLIF-type) or pneumatic (General Fusion). |

---

### Column 5: Non-Standard Mechanism

**Definition**: What non-standard mechanism does this concept use?

**Applies to**: Non-Standard concepts only (4 of 38). All non-NS concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `Electrostatic` | Confinement via electric fields — IEC, fusor-type, Polywell. Ions accelerated toward convergence point by electrostatic potential well. |
| `Plasma focus` | Dense plasma focus — pulsed coaxial electrode discharge creates self-compressed plasma pinch. |
| `Muon-catalyzed` | Muonic atom formation catalyzes fusion at room temperature. Not a thermal plasma process. |

---

### Column 6: Tokamak Shape

**Definition**: What shape/configuration is this tokamak? Distinguishes the major tokamak design variants.

**Applies to**: Tokamak concepts only (6 of 38). All non-Tokamak concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `Compact` | High-field-enabled compact design (R < ~2.5 m). HTS magnets enable strong field in small volume. (CFS, Renaissance.) |
| `Spherical` | Very low aspect ratio (A < 2). Tight center column, natural elongation. (Tokamak Energy, BEST-IN.) |
| `Standard` | Conventional or mid-size tokamak (R > 3 m). ITER-heritage geometry. |
| `Negative triangularity` | Reversed plasma shaping (δ < 0). Improved edge stability, no ELMs. (Type One / MANTA.) |

---

### Column 7: Stellarator Type

**Definition**: What stellarator optimization strategy or coil approach?

**Applies to**: Stellarator concepts only (6 of 38). All non-Stellarator concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `QI` | Quasi-isodynamic optimization — bounce-averaged particle drifts are optimized for confinement. (Proxima, Type One.) |
| `Modular` | Emphasis on modular coil cassette manufacturing/assembly. (Infinity Two, Stellarex.) |
| `Planar coil` | Arrays of simple flat coils producing stellarator fields via current distribution. (Thea Energy.) |
| `Helical coil` | Continuous helical coil winding. Wendelstein-class geometry. |

**Notes**:
- `QI` vs `Modular`: Use `QI` when the concept's primary innovation emphasis is the quasi-isodynamic physics optimization. Use `Modular` when the emphasis is on manufacturing/assembly approach (modular coil cassettes). Both may be true — pick the dominant framing.

---

### Column 8: Laser Approach

**Definition**: What laser drive scheme does this laser IFE concept use?

**Applies to**: Laser IFE concepts only (9 of 38). All non-Laser concepts → `N/A`.

| Value | Description |
|-------|-------------|
| `Direct drive` | Laser beams directly ablate fuel capsule surface. Uniform illumination critical. |
| `Indirect drive` | Laser → hohlraum → X-ray → capsule ablation. NIF approach. |
| `Fast ignition` | Separate compression and ignition laser pulses. Reduces symmetry requirements. |
| `Hybrid drive` | Combination of direct and indirect drive features. (Xcimer's HDD approach.) |
| `Ultrashort pulse` | Pico/femtosecond pulses on nanostructured targets; non-thermal acceleration. (HB11 p-B11.) |
| `Liquid jet` | Laser-driven compression of liquid fuel jet. No solid capsule. (Marathon Fusion.) |

---

### Column 9: Fuel

**Definition**: The primary fusion fuel cycle. This determines the reaction products, neutron environment, and downstream engineering requirements.

| Value | Description |
|-------|-------------|
| `D-T` | Deuterium-Tritium — highest reactivity, 14.1 MeV neutrons, requires tritium breeding |
| `D-D` | Deuterium-Deuterium — lower reactivity, 2.45 MeV neutrons, no tritium supply needed but still neutronic |
| `D-He3` | Deuterium-Helium-3 — primary reaction aneutronic, but DD side reactions produce ~10% neutron energy fraction |
| `p-B11` | Proton-Boron-11 — truly aneutronic (<1% neutron energy from side reactions), requires extreme temperatures (~150-300 keV) |
| `Multiple` | Concept explicitly targets multiple fuel cycles (e.g., D-T initial operation transitioning to advanced fuels) |
| `Unknown` | Fuel choice not publicly specified |

**Notes**:
- If a company claims D-D but the physics description suggests D-T bootstrap burn, note this discrepancy in the dossier.
- Helion's fuel is `D-He3` — they begin with D-D operations to breed He3 via tritium decay, but the target commercial fuel cycle is D-He3.

---

### Column 10: Primary Heating

**Definition**: The dominant mechanism by which plasma is heated to fusion-relevant temperatures. For multi-method systems, record the primary/dominant method. Note auxiliary methods in the dossier.

| Value | Description | Typical families |
|-------|-------------|-----------------|
| `RF (ECRH)` | Electron cyclotron resonance heating — gyrotrons at ~100-170 GHz | MFE (stellarators, some tokamaks) |
| `RF (ICRH)` | Ion cyclotron resonance heating — RF at ~40-55 MHz | MFE (tokamaks) |
| `RF + NBI` | Combined RF heating and neutral beam injection | MFE (spherical tokamaks, mirrors) |
| `NBI` | Neutral beam injection as primary/sole heating and sustainment | MFE (beam-driven FRC) |
| `Ohmic (self-pinch)` | Plasma current provides both confinement and heating via resistive dissipation | MFE (Z-pinch) |
| `Magnetic compression` | Adiabatic compression via rapidly increasing magnetic fields | MIF (pulsed FRC) |
| `Mechanical compression` | Compression by mechanically driven liquid metal liner | MIF (pneumatic MTF) |
| `Pulsed power implosion` | Massive current drives liner implosion; may include laser preheat | MIF (MagLIF-type) |
| `Laser (indirect drive)` | Laser → hohlraum → X-ray → capsule ablation | IFE |
| `Laser (direct drive)` | Laser → direct capsule ablation | IFE |
| `Laser (fast ignition)` | Separate compression and ignition laser pulses | IFE |
| `Laser (ultrashort pulse)` | Pico/femtosecond pulses on nanostructured targets; non-thermal acceleration | IFE (p-B11 concepts) |
| `Laser (novel/TBD)` | Laser-driven but specific physics pathway unclear or proprietary | IFE |
| `Heavy ion beam` | Accelerator-driven heavy ion beam ablation of targets | IFE |
| `Projectile impact` | Hypervelocity projectile → shockwave compression of target | IFE |
| `Electrostatic acceleration` | High-voltage electric field accelerates ions toward convergence point | Non-Standard |
| `Electromagnetic pinch (DPF)` | Pulsed coaxial electrode discharge creates dense plasma pinch | Non-Standard |
| `Muon catalysis` | Muonic molecule formation; not a thermal heating method | Non-Standard |
| `Acoustic implosion` | Sound-driven bubble implosion (sonoluminescence) | IFE |

**Notes**:
- For tokamaks, ohmic heating is always present during startup but is rarely the primary heating method at burn conditions. Record the primary auxiliary heating system.
- When RF type is uncertain but the concept is a stellarator, default to `RF (ECRH)` with `medium` confidence — ECRH is the universal stellarator heating method.

---

### Column 11: Energy Capture

**Definition**: How fusion energy is converted to electricity (or other useful output). The key engineering distinction is thermal cycle (heat → turbine) vs. direct conversion (charged particles → electricity without thermodynamic cycle).

| Value | Description |
|-------|-------------|
| `Thermal (steam)` | Neutron energy captured in blanket → steam Rankine cycle → turbine. Standard power conversion. |
| `Thermal (sCO2)` | Neutron energy captured in blanket → supercritical CO2 Brayton cycle. Higher efficiency, more compact. (TRL 5-6 for the cycle itself.) |
| `Thermal (unspecified)` | Thermal conversion confirmed but specific cycle not disclosed. Use when a D-T concept hasn't specified Rankine vs. sCO2. |
| `Direct (inductive)` | Expanding/compressing magnetized plasma induces current in coils. No thermal cycle. (Helion's approach.) |
| `Direct (charged particle)` | Charged fusion products decelerated by electrostatic or electromagnetic fields. Includes electrostatic DEC, inverse cyclotron converter (ICC), and ion beam recovery. |
| `Hybrid (thermal + direct)` | Dual-channel: neutrons → thermal cycle, charged particles → direct conversion. Applicable to open-ended D-T/D-He3 concepts. |
| `Neutron applications` | Neutrons are the product, not a byproduct. Medical isotopes, industrial imaging, materials testing. No electricity generation. |
| `TBD` | Concept has not specified energy conversion approach. |

**Notes**:
- Most D-T concepts default to `Thermal (unspecified)` unless they've explicitly stated their cycle choice.
- p-B11 concepts where nearly all energy is in charged particles should use `Direct (charged particle)` even if the specific DEC technology (electrostatic, ICC, etc.) is TBD.
- `Hybrid` is distinct from `Thermal` — it means the concept explicitly plans to capture charged particle energy separately, not just blanket thermalization.

---

### Column 12: Plasma State

**Definition**: The characteristic plasma regime during the fusion-producing phase of operation. This captures how the plasma behaves, not how it's created.

| Value | Description |
|-------|-------------|
| `Burning` | Self-sustaining plasma where alpha heating dominates external heating. Characteristic of steady-state MFE at Q >> 5. |
| `Sustained` | Externally maintained plasma in quasi-steady-state. Characteristic of beam-driven or RF-sustained MFE below ignition. |
| `Transient` | Short-lived plasma state (~ms) during a pulsed compression/collision event. Characteristic of pulsed FRC. |
| `Compressed` | Plasma driven to fusion conditions by implosion (laser, projectile, pulsed power, mechanical). Characteristic of IFE and MIF. |
| `Pinch` | Self-compressed plasma column maintained by its own current. Characteristic of Z-pinch. |
| `Confined` | Plasma in magnetic confinement but not necessarily approaching ignition. Characteristic of mirrors and other sub-ignition MFE. |
| `Non-burning` | Plasma used for neutron production or other applications, not approaching fusion energy gain. |
| `Solid-state` | Fusion occurs in solid medium (lattice confinement). Not a plasma state. |

**Notes**:
- The boundary between `Burning` and `Sustained` is fuzzy — it depends on target Q. Use `Burning` for concepts explicitly targeting ignition or high Q (>10). Use `Sustained` for concepts targeting moderate Q with significant recirculating power.
- Muon-catalyzed fusion doesn't fit cleanly — the "plasma" is room-temperature gas/liquid. Use `N/A`.

---

### Column 13: Magnet Type

**Definition**: The primary magnet technology used for plasma confinement. For concepts without magnetic confinement, record the driver's magnet subsystem only if it's a distinguishing feature.

| Value | Description |
|-------|-------------|
| `HTS (wound)` | High-temperature superconducting REBCO tape wound into coils. Tokamak D-coils, mirror solenoids. 12-20+ T. |
| `HTS (3D stellarator)` | HTS REBCO in complex 3D non-planar stellarator coil geometry. Includes modular and continuous helical winding approaches. |
| `HTS (planar array)` | Arrays of simple flat HTS coils producing stellarator fields via current distribution. |
| `HTS (levitated dipole)` | Single levitated HTS coil creating dipolar field. |
| `LTS` | Low-temperature superconducting (NbTi or Nb3Sn). ITER heritage. 4 K operation. |
| `LTS+HTS` | Dual development strategy with both conductor families. |
| `Resistive` | Conventional copper/aluminum electromagnets. Continuous power input, no cryogenics. |
| `Pulsed EM` | Pulsed resistive electromagnets driven by capacitor banks. Field exists only during pulse (~μs to ms). |
| `Self-confined` | Plasma generates its own confining magnetic field (Z-pinch, DPF) or is mechanically compressed (MTF). No external confinement magnets. |
| `Electrostatic` | Confinement by electric fields, not magnetic fields. |
| `N/A` | Magnet technology is not a meaningful differentiator for this concept. |

**Notes**:
- Renaissance Fusion's laser-patterned HTS film on cylinders is classified as `HTS (3D stellarator)` — the manufacturing method is novel but the functional result is a 3D stellarator field. Note the manufacturing distinction in the dossier.
- Helion uses `Pulsed EM` — their aluminum coils are pulsed with capacitor banks, not steady-state superconducting.
- General Fusion and Zap Energy are both `Self-confined` but for very different reasons (mechanical compression vs. self-pinch). The distinction is now captured in MFE Topology / MIF Method.

---

### Column 14: Tritium Breeding

**Definition**: How the concept supplies tritium fuel (for D-T and D-He3 concepts) or why breeding is unnecessary.

| Value | Description |
|-------|-------------|
| `FLiBe blanket` | Lithium fluoride-beryllium fluoride molten salt blanket. Combined breeder/coolant/shield. (CFS/ARC baseline.) |
| `LiPb blanket` | Lead-lithium eutectic blanket. Lead provides neutron multiplication. Various cooling schemes (water, helium, self-cooled). |
| `Liquid Li blanket` | Pure liquid lithium blanket. Highest TBR potential (~1.8). |
| `Li blanket (unspecified)` | Lithium-bearing blanket confirmed but specific type (solid/liquid/salt) not disclosed. |
| `Solid ceramic breeder (HCPB)` | Helium-cooled pebble bed with solid ceramic breeding material (Li₄SiO₄ or Li₂TiO₃) and Be/Be₁₂Ti neutron multiplier. ITER TBM baseline. |
| `Liquid metal wall` | Flowing liquid metal serves dual purpose as structural wall/liner AND tritium breeder. Distinct from a contained blanket. |
| `Self-bred (DD side)` | Tritium produced as byproduct of DD side reactions in D-He3 plasma. Tritium decays to He3, completing fuel cycle. No external blanket. |
| `N/A` | Tritium breeding is not applicable — either the fuel cycle does not involve tritium (p-B11, D-D, some D-He3) or the concept is not a power reactor. |
| `TBD` | D-T concept where blanket approach has not been disclosed. |

**Notes**:
- The tritium supply crisis is existential for D-T fusion — global civilian tritium is ~25 kg, and a single 1 GWth D-T plant needs >55 kg/year. TBR > 1 is not optional.
- For D-He3 concepts (Helion), `Self-bred (DD side)` captures the unique fuel cycle where DD byproduct tritium decays to He3.
- Solid ceramic breeders (Li₂TiO₃, Li₄SiO₄) are the ITER TBM / DEMO baseline. Type One Energy plans HCPB for their stellarator.

---

### Column 15: Neutron Management

**Definition**: How the concept handles fusion neutrons. Renamed from "Neutron Shielding" to "Neutron Management" because the approaches range from heavy shielding to eliminating neutrons entirely — "shielding" doesn't cover the full spectrum.

| Value | Description |
|-------|-------------|
| `Heavy shielding (14 MeV)` | Full multi-layer shielding for 14.1 MeV D-T neutrons. Remote handling required for all internal maintenance. Dominant engineering challenge. |
| `Heavy shielding (D-D)` | Shielding for 2.45 MeV D-D neutrons. 50% of D-D reactions produce neutrons — high flux but lower per-neutron energy and damage than D-T. Less activation, simpler materials, but still requires substantial shielding at power-relevant rates. |
| `Integrated blanket/shield` | Blanket material (FLiBe, liquid metal) provides both tritium breeding and neutron shielding in one system. Still 14 MeV neutrons, but simplified architecture. |
| `Reduced (D-He3)` | ~10% neutron energy fraction from DD side reactions. 2.45 MeV neutrons (less damaging than 14 MeV). Lighter shielding. Limited remote handling. |
| `Minimal (aneutronic)` | <1% neutron energy from side reactions. Thin shielding (~1m water + boron) for secondary neutrons and X-rays. Hands-on maintenance possible. |
| `N/A` | Concept is not a power reactor. |

**Notes**:
- `Heavy shielding` and `Integrated blanket/shield` are not mutually exclusive — the integrated approach IS the shielding for many concepts. Use `Integrated blanket/shield` when the blanket explicitly serves dual purpose (CFS FLiBe, General Fusion liquid metal wall, First Light liquid Li).
- The distinction matters for cost modeling: integrated approaches consolidate CAS accounts, while separate blanket + shield approaches have distinct cost streams.
- D-D concepts produce 2.45 MeV neutrons in 50% of reactions — they need `Heavy shielding (14 MeV)` equivalent if the neutron flux is high enough, or may be slightly less than D-T. Assess case-by-case.

---

### Column 16: Operation Mode

**Definition**: Temporal profile of the fusion burn.

| Value | Description |
|-------|-------------|
| `Steady-state` | Continuous plasma operation. Plasma maintained indefinitely by external heating/current drive. Characteristic of stellarators, advanced tokamaks, mirrors. |
| `Pulsed` | Discrete short burn events (seconds or less) separated by recovery/reload periods. Characteristic of IFE, MIF, pulsed FRC. |
| `Quasi-steady` | Long-pulse operation (~minutes to hours) with brief interruptions for refueling or re-magnetization. Intermediate between steady-state and pulsed. **Threshold**: pulse lengths > 5 minutes → Quasi-steady, regardless of company self-description. |

---

### Column 17: Repetition Rate

**Definition**: For pulsed concepts, the frequency of fusion burn events. Determines time-averaged power output and driver duty cycle.

| Value | Description |
|-------|-------------|
| `Sub-Hz` | Less than 1 pulse per second. Early-stage or very high-yield concepts. |
| `~1 Hz` | Approximately 1 pulse per second. Typical for MTF and some IFE. |
| `~10 Hz` | Approximately 10 pulses per second. Target for many laser IFE power plants. |
| `High (>10 Hz)` | Greater than 10 Hz. Required for some compact pulsed concepts to achieve competitive time-averaged power. |
| `kHz` | Kilohertz repetition rate. Claimed by some novel laser concepts. |
| `TBD` | Pulsed concept but target rep rate not disclosed. |
| `N/A` | Steady-state or quasi-steady concept — repetition rate is not applicable. |

---

### Column 18: Driver Technology

**Definition**: The primary technology that creates and/or sustains the fusion conditions. This is the most concept-specific column — it captures the distinguishing engineering subsystem.

**Vocabulary**: Free text, but aim for consistency. Use the form: `{technology type}` with enough specificity to distinguish from similar concepts.

| Examples | Concept |
|----------|---------|
| `HTS magnets (REBCO, 20 T)` | CFS, Tokamak Energy |
| `Planar HTS coil array` | Thea Energy |
| `3D HTS stellarator coils` | Proxima Fusion |
| `Neutral beam injection` | TAE Technologies |
| `Pulsed EM coils (capacitor bank)` | Helion Energy |
| `Excimer laser (KrF)` | Xcimer Energy |
| `Diode-pumped solid-state laser` | Focused Energy |
| `Electromagnetic gun` | First Light Fusion |
| `Linear induction accelerator` | Intensity Energy |
| `Pneumatic pistons + liquid metal` | General Fusion |
| `Pulsed power (Z-machine class)` | Pacific Fusion |
| `Pulsed power (sheared-flow Z-pinch)` | Zap Energy |
| `Electrostatic grid (IEC)` | SHINE Technologies |
| `Muon source (accelerator)` | Acceleron Fusion |

**Notes**: This column is intentionally the least constrained. It captures "what's the hard technology bet?" for each concept. The controlled vocabulary for other columns handles the physics; this column captures the engineering.

---

## Column Summary

| # | Column | Type | # Values | N/A possible? |
|---|--------|------|----------|---------------|
| 1 | Confinement Family | Controlled | 4 | No |
| 2 | MFE Topology | Controlled | 5 | Yes |
| 3 | IFE Driver | Controlled | 4 | Yes |
| 4 | MIF Method | Controlled | 2 | Yes |
| 5 | Non-Standard Mechanism | Controlled | 3 | Yes |
| 6 | Tokamak Shape | Controlled | 4 | Yes |
| 7 | Stellarator Type | Controlled | 4 | Yes |
| 8 | Laser Approach | Controlled | 6 | Yes |
| 9 | Fuel | Controlled | 6 | No |
| 10 | Primary Heating | Controlled | 19 | No |
| 11 | Energy Capture | Controlled | 8 | No |
| 12 | Plasma State | Controlled | 8 | Rare |
| 13 | Magnet Type | Controlled | 11 | Rare |
| 14 | Tritium Breeding | Controlled | 9 | Yes |
| 15 | Neutron Management | Controlled | 6 | Yes |
| 16 | Operation Mode | Controlled | 3 | No |
| 17 | Repetition Rate | Controlled | 7 | Yes |
| 18 | Driver Technology | Free text | — | No |

**Key changes from v1 (12 columns) → v2 (18 columns)**:
- Old Columns 1–2 (Confinement Family, Confinement Concept) → New Columns 1–8 (hierarchical tree)
- Old Columns 3–12 → New Columns 9–18 (unchanged content, renumbered)
- Confinement Family vocabulary: 5 → 4 (Electrostatic + Other merged to Non-Standard; Acoustic moved to IFE)
- Neutron Management value count corrected: was listed as 5, actually 6

---

## Schema Evolution Log

| Date | Version | Changes | Trigger |
|------|---------|---------|---------|
| 2026-03-06 | 0.1 | Initial schema | Sprint plan creation |
| 2026-03-07 | 0.2 | +`Tokamak` (Col 2), +`Solid ceramic breeder (HCPB)` (Col 8), QI/modular note (Col 2), >5 min = Quasi-steady (Col 10), `Pulsed` narrowed to short events | Checkpoint 1 review |
| 2026-03-07 | 0.2.1 | Overall Confidence expanded to five-level scale; per-cell confidence remains three-level | Checkpoint 3-4 review |
| 2026-03-08 | 0.2.2 | +`Laser ICF (hybrid drive)` (Col 2) for Xcimer HDD approach. Row restructuring. | Checkpoint 5 restructuring |
| 2026-03-08 | 0.2.3 | Renamed `N/A (aneutronic)` → `N/A (no tritium in fuel cycle)` (Col 8). Added `Heavy shielding (D-D)` (Col 9). | Phase 1c measurement integrity |
| 2026-03-08 | 2.0 | **Major restructure**: replaced {Confinement Family, Confinement Concept} with 8-column confinement hierarchy. Merged Electrostatic+Other → Non-Standard. Reclassified Acoustic → IFE. Renumbered columns 3-12 → 9-18. Fixed Neutron Management count (5→6). | Phase 1b v2 — context-dependent design space decomposition |
