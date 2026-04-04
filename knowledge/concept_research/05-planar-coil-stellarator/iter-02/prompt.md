# Fusion Concept Research: Planar Coil Stellarator (D-T)

You are a research agent investigating a specific fusion energy concept for a differentiation table. Your job is to find accurate, cited information for each column in the table schema.

## Concept

- **Name**: Planar Coil Stellarator (D-T)
- **Company**: Thea Energy
- **Confinement approach**: Magnetic Confinement
- **Description**: Stellarator using arrays of simple planar HTS coils instead of complex 3D-shaped windings. Simplifies manufacturing at the cost of requiring many more coils. Steady-state.
- **Known fuel**: D-T (Deuterium-Tritium)
- **Operation mode**: Continuous

## Task

Research this concept and provide findings for each column listed under "Gaps to Fill" below. For columns already filled with high confidence, you do not need to re-research them — but if you find contradictory information, note it.

## Research Strategy

1. **Start broad**: Search the web for "Thea Energy fusion technology" and similar queries. Look for the company's website, Wikipedia page, Fusion Industry Association profile, press releases, and investor presentations.
2. **Go deeper on gaps**: For columns that remain unfilled after the broad search, try more targeted queries:
   - Technical papers or preprints by the company's founders/scientists
   - ARPA-E or DOE award descriptions
   - Conference presentations (APS-DPP, IAEA FEC, IEEE SOFE)
   - News articles with technical detail (not just funding announcements)
3. **Save important sources**: When you find a page with substantial technical detail, save it to `./sources/` with a descriptive filename (e.g., `company-website-technology.md`, `arxiv-2025-paper-summary.md`). Use the Write tool. Save the key technical content, not the entire page.
4. **Be honest about confidence**: If you can't find a value, say so. If you're inferring from general physics rather than a specific source, say so. Do not guess.

## Column Schema

Use these exact vocabulary values. If no value fits, use the closest match and explain in your notes.

# Phase 1a: Differentiation Table Schema

**Version**: 0.1 (initial draft, pre-Batch 1)
**Last updated**: 2026-03-06

This document defines the columns, controlled vocabulary, and rules for the fusion concept differentiation table. The schema evolves at checkpoint reviews between batches.

---

## Conventions

### N/A vs TBD vs Unknown

- **N/A**: The question is **structurally inapplicable** to this concept. The physics or architecture make the column meaningless. Every N/A must include a one-line justification.
  - Example: "Tritium Breeding" for a p-B11 concept → `N/A — no tritium in fuel cycle`
  - Example: "Repetition Rate" for a steady-state concept → `N/A — continuous operation`
- **TBD**: The question **applies** to this concept, but the answer is not publicly known or not yet decided by the company.
  - Example: "Tritium Breeding" for an early-stage D-T startup that hasn't specified blanket type → `TBD`
- **Unknown**: We could not determine the answer from available sources, but the question applies and the company may have an answer internally.
  - Example: A concept with almost no public information → `Unknown`

### Citation Format

Every non-obvious value in the table should be traceable. In per-concept dossiers, each column value carries:
- **Citation**: URL, paper reference, or `knowledge/sources/...` path
- **Confidence**: `high` (directly stated by source) · `medium` (inferred from described approach) · `low` (extrapolated from similar concepts)

### Controlled Vocabulary Rules

- Use the exact vocabulary string from this document. Do not paraphrase or abbreviate.
- If no vocabulary value fits, record the best-fit value AND add a note explaining the discrepancy. Flag for schema review at the next checkpoint.
- A value may include a parenthetical qualifier when the base vocabulary is correct but the specific variant matters: e.g., `RF (ECRH)` vs `RF (ICRH)`.

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
| `Electrostatic` | Confinement via electric fields (IEC, fusor-type, Polywell) |
| `Other` | Does not fit cleanly into the above categories (muon catalysis, sonofusion, lattice confinement, dense plasma focus) |

**Notes**:
- FRC-based concepts are classified by their operational mode: steady-state beam-driven FRC (TAE) → `MFE`; pulsed FRC compression (Helion) → `MIF`.
- Z-pinch concepts that use self-generated fields are `MFE` (the confinement is magnetic, even though the geometry is linear and pulsed).
- "Hybrid" is not a family — use the dominant confinement mechanism.

---

### Column 2: Confinement Concept

**Definition**: The specific confinement geometry or scheme. More granular than family — this is what distinguishes a tokamak from a stellarator from a mirror within MFE.

**Vocabulary**: Free text, but use standardized names where possible:

| Family | Standard concept names |
|--------|-----------------------|
| MFE | `Compact tokamak` · `Spherical tokamak` · `Negative triangularity tokamak` · `Stellarator (QI)` · `Stellarator (modular)` · `Stellarator (planar coil)` · `Stellarator (helical coil)` · `Magnetic mirror` · `FRC (beam-driven)` · `FRC (pulsed)` · `Z-pinch (sheared-flow)` · `Levitated dipole` · `Levitated dipole (orbital)` |
| IFE | `Laser ICF (indirect drive)` · `Laser ICF (direct drive)` · `Laser ICF (fast ignition)` · `Laser ICF (ultrashort pulse)` · `Laser ICF (liquid jet)` · `Projectile ICF` · `Heavy ion beam ICF` |
| MIF | `Magnetized target (pneumatic)` · `Magnetized target (pulsed power)` · `FRC (pulsed compression)` |
| Electrostatic | `IEC / Fusor` · `Polywell` · `Orbital electrostatic` |
| Other | `Dense plasma focus` · `Muon-catalyzed fusion` · `Acoustic / Sonofusion` · `Lattice confinement` |

**Rule**: If a company has a proprietary name for their concept, use the closest generic physics description. Note the proprietary name in the dossier.

---

### Column 3: Fuel

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

### Column 4: Primary Heating

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
| `Electrostatic acceleration` | High-voltage electric field accelerates ions toward convergence point | Electrostatic |
| `Electromagnetic pinch (DPF)` | Pulsed coaxial electrode discharge creates dense plasma pinch | Other |
| `Muon catalysis` | Muonic molecule formation; not a thermal heating method | Other |
| `Acoustic implosion` | Sound-driven bubble implosion (sonoluminescence) | Other |

**Notes**:
- For tokamaks, ohmic heating is always present during startup but is rarely the primary heating method at burn conditions. Record the primary auxiliary heating system.
- When RF type is uncertain but the concept is a stellarator, default to `RF (ECRH)` with `medium` confidence — ECRH is the universal stellarator heating method.

---

### Column 5: Energy Capture

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

### Column 6: Plasma State

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
- Muon-catalyzed fusion doesn't fit cleanly — the "plasma" is room-temperature gas/liquid. Use `N/A — non-thermal fusion` or the closest approximation.

---

### Column 7: Magnet Type

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
| `None (IFE)` | Inertial confinement — no magnetic confinement of plasma. (Driver subsystem may contain magnets, but these confine the beam, not the plasma.) |
| `Electrostatic` | Confinement by electric fields, not magnetic fields. |
| `N/A` | Magnet technology is not a meaningful differentiator for this concept. |

**Notes**:
- Renaissance Fusion's laser-patterned HTS film on cylinders is classified as `HTS (3D stellarator)` — the manufacturing method is novel but the functional result is a 3D stellarator field. Note the manufacturing distinction in the dossier.
- Helion uses `Pulsed EM` — their aluminum coils are pulsed with capacitor banks, not steady-state superconducting.
- General Fusion and Zap Energy are both `Self-confined` but for very different reasons (mechanical compression vs. self-pinch). The distinction is captured in Confinement Concept.

---

### Column 8: Tritium Breeding

**Definition**: How the concept supplies tritium fuel (for D-T and D-He3 concepts) or why breeding is unnecessary.

| Value | Description |
|-------|-------------|
| `FLiBe blanket` | Lithium fluoride-beryllium fluoride molten salt blanket. Combined breeder/coolant/shield. (CFS/ARC baseline.) |
| `LiPb blanket` | Lead-lithium eutectic blanket. Lead provides neutron multiplication. Various cooling schemes (water, helium, self-cooled). |
| `Liquid Li blanket` | Pure liquid lithium blanket. Highest TBR potential (~1.8). |
| `Li blanket (unspecified)` | Lithium-bearing blanket confirmed but specific type (solid/liquid/salt) not disclosed. |
| `Liquid metal wall` | Flowing liquid metal serves dual purpose as structural wall/liner AND tritium breeder. Distinct from a contained blanket. |
| `Self-bred (DD side)` | Tritium produced as byproduct of DD side reactions in D-He3 plasma. Tritium decays to He3, completing fuel cycle. No external blanket. |
| `N/A (aneutronic)` | Fuel cycle does not involve tritium. p-B11 and pure D-D concepts. |
| `N/A (non-power)` | Concept is not a power-producing reactor (neutron source, isotope production). |
| `TBD` | D-T concept where blanket approach has not been disclosed. |

**Notes**:
- The tritium supply crisis is existential for D-T fusion — global civilian tritium is ~25 kg, and a single 1 GWth D-T plant needs >55 kg/year. TBR > 1 is not optional.
- For D-He3 concepts (Helion), `Self-bred (DD side)` captures the unique fuel cycle where DD byproduct tritium decays to He3.
- Solid ceramic breeders (Li2TiO3, Li4SiO4) are ITER TBM / DEMO concepts, not currently planned by any private company. Include if needed.

---

### Column 9: Neutron Management

**Definition**: How the concept handles fusion neutrons. Renamed from "Neutron Shielding" to "Neutron Management" because the approaches range from heavy shielding to eliminating neutrons entirely — "shielding" doesn't cover the full spectrum.

| Value | Description |
|-------|-------------|
| `Heavy shielding (14 MeV)` | Full multi-layer shielding for 14.1 MeV D-T neutrons. Remote handling required for all internal maintenance. Dominant engineering challenge. |
| `Integrated blanket/shield` | Blanket material (FLiBe, liquid metal) provides both tritium breeding and neutron shielding in one system. Still 14 MeV neutrons, but simplified architecture. |
| `Reduced (D-He3)` | ~10% neutron energy fraction from DD side reactions. 2.45 MeV neutrons (less damaging than 14 MeV). Lighter shielding. Limited remote handling. |
| `Minimal (aneutronic)` | <1% neutron energy from side reactions. Thin shielding (~1m water + boron) for secondary neutrons and X-rays. Hands-on maintenance possible. |
| `N/A (non-power)` | Concept is not a power reactor; neutron management handled differently or not applicable. |

**Notes**:
- `Heavy shielding` and `Integrated blanket/shield` are not mutually exclusive — the integrated approach IS the shielding for many concepts. Use `Integrated blanket/shield` when the blanket explicitly serves dual purpose (CFS FLiBe, General Fusion liquid metal wall, First Light liquid Li).
- The distinction matters for cost modeling: integrated approaches consolidate CAS accounts, while separate blanket + shield approaches have distinct cost streams.
- D-D concepts produce 2.45 MeV neutrons in 50% of reactions — they need `Heavy shielding (14 MeV)` equivalent if the neutron flux is high enough, or may be slightly less than D-T. Assess case-by-case.

---

### Column 10: Operation Mode

**Definition**: Temporal profile of the fusion burn.

| Value | Description |
|-------|-------------|
| `Steady-state` | Continuous plasma operation. Plasma maintained indefinitely by external heating/current drive. Characteristic of stellarators, advanced tokamaks, mirrors. |
| `Pulsed` | Discrete burn events separated by recovery/reload periods. Characteristic of IFE, MIF, pulsed FRC. |
| `Quasi-steady` | Long-pulse operation (~minutes to hours) with brief interruptions for refueling or re-magnetization. Intermediate between steady-state and pulsed. |

---

### Column 11: Repetition Rate

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

### Column 12: Driver Technology

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
| 1 | Confinement Family | Controlled | 5 | No |
| 2 | Confinement Concept | Semi-controlled | ~25 | No |
| 3 | Fuel | Controlled | 6 | No |
| 4 | Primary Heating | Controlled | 19 | No |
| 5 | Energy Capture | Controlled | 8 | No |
| 6 | Plasma State | Controlled | 8 | Rare (muon catalysis) |
| 7 | Magnet Type | Controlled | 12 | Rare |
| 8 | Tritium Breeding | Controlled | 9 | Yes (aneutronic, non-power) |
| 9 | Neutron Management | Controlled | 5 | Yes (non-power) |
| 10 | Operation Mode | Controlled | 3 | No |
| 11 | Repetition Rate | Controlled | 7 | Yes (steady-state) |
| 12 | Driver Technology | Free text | — | No |

---

## Schema Evolution Log

| Date | Version | Changes | Trigger |
|------|---------|---------|---------|
| 2026-03-06 | 0.1 | Initial schema | Sprint plan creation |


## Current Knowledge

From previous research iterations (see dossier for full context):

# Planar Coil Stellarator (D-T)

**Company**: Thea Energy
**Last updated**: 2026-03-06
**Iterations completed**: 1
**Overall confidence**: high

## Summary

Thea Energy's planar coil stellarator replaces the complex 3D-shaped coils of conventional stellarators with arrays of simple, flat HTS coils whose currents are individually software-controlled to produce the desired stellarator magnetic field. The Helios preconceptual design (arXiv:2512.08027, DOE Milestone-certified) specifies a two-field-period quasi-axisymmetric (QA) stellarator with 12 encircling coils and 324 shaping coils, producing 958 MW fusion power and 390 MWe net electric output. This approach trades hardware complexity for software complexity, enabling mass manufacturing of simple coils and dynamic field optimization during operation.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: https://thea.energy/fusion-technology/ — "Inherently stable magnetic confinement with no risk of disruptions"
- **Notes**: Stellarator is a canonical MFE concept. Steady-state magnetic confinement.

### Confinement Concept
- **Value**: `Stellarator (planar coil)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "two-field-period quasi-axisymmetric (QA) stellarator"
- **Notes**: Thea Energy's innovation is using arrays of planar (flat) HTS coils rather than complex 3D-wound coils. The stellarator equilibrium is quasi-axisymmetric (QA), which is distinct from the quasi-isodynamic (QI) approach of W7-X/Proxima or the modular coil approach of earlier designs. QA optimization produces tokamak-like transport properties while retaining stellarator steady-state advantages.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Helios designed for D-T with LiPb breeding blanket, TBR 1.3
- **Notes**: Eos (demonstration device) operates on D-D for tritium breeding and isotope production. Helios (commercial plant) is explicitly D-T with a full tritium breeding system.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "10 MW of electron cyclotron resonance heating power" at 170 GHz for startup; 1 MW during ignited operation for impurity control
- **Notes**: ECRH is the sole heating system. No NBI. Uses ITER-specification gyrotrons at 170 GHz with X1 polarization from the high-field side. Operational budget is 2.5 MW (1 MW + overhead), notably low because Helios targets ignited operation where alpha heating dominates.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "Steam Rankine cycle" at 635C superheated, three-stage turbines, ~40.2% efficiency
- **Notes**: 1,094 MW thermal -> 438 MWe gross electric -> 390 MWe net to grid. Intermediate heat exchangers transfer heat from helium blanket/divertor coolant loops to water/steam.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Only 1 MW ECRH during ignited operation (vs. 958 MW fusion power); recirculating power fraction <3%
- **Notes**: At 958 MW fusion power with only 1 MW external heating, this is deeply into the burning plasma regime. Q is effectively infinite (ignited). The 1 MW ECRH is for impurity control, not energy input.

### Magnet Type
- **Value**: `HTS (planar array)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — 12 encircling coils + 324 shaping coils, all planar and convex, wound in tension, max 20 T on coil, operating at 20 K
- **Notes**: This is the defining innovation. 12 large toroidal field coils (4 unique shapes) provide bulk confinement; 324 smaller individually controllable planar coils create the stellarator shaping. HTS (REBCO implied), helium-cooled at 20 K. Complexity is transferred from hardware geometry to software control (450+ independent control variables). Thea has demonstrated a 3x3 superconducting planar coil array prototype.

### Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "Pb-17Li (lead-lithium eutectic, 17% Li by atom)" with 65% Li-6 enrichment, 50 cm thick, EUROFER97 structure, SiC MHD inserts
- **Notes**: Idealized TBR = 1.3, required TBR = 1.1. Startup tritium inventory = 1-2 kg. Helium gas cooled. Flow rate 6.6 cm/s. LiPb breeding produces 135 MW additional thermal power from Li-6 + n reactions.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Multi-layer shield: WC -> B4C -> 316L SS (vacuum vessel) -> borated water -> borated HDPE -> 2.0 m concrete bioshield
- **Notes**: Full 14.1 MeV D-T neutron management. LiPb blanket serves as breeder, with dedicated multi-layer shielding behind it to protect HTS coils for 40+ year lifetime. Minimum 1.2 m plasma-to-coil distance provides space for blanket + shield. Sector-based remote maintenance with full toroidal sector removal.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://thea.energy/fusion-technology/ — "steady-state magnetic confinement fusion"; arXiv:2512.08027 confirms continuous operation
- **Notes**: Inherent stellarator advantage — no plasma current to sustain, so no disruption risk. Eos targets 24+ hour continuous pulses. Helios designed for continuous operation with 88% capacity factor (limited by planned maintenance, not plasma physics).

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed burn cycle.

### Driver Technology
- **Value**: `Planar HTS coil array (12 encircling + 324 shaping, 20 T, software-controlled)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027; https://thea.energy/fusion-technology/
- **Notes**: The key technology bet is the planar coil array with software-defined magnetic field control. Rather than building complex 3D coils that precisely match a target magnetic geometry, Thea uses many simple flat coils whose currents are individually controlled. This enables: (1) mass manufacturing of simple coils, (2) dynamic field optimization during operation, (3) sector-based maintenance with removable toroidal sections. The 324 shaping coils have 450+ independent control variables. Thea describes this as "transferring complexity from hardware to software."

## Metadata

### Published Machine/Plant
- **Helios**: Full preconceptual design published (arXiv:2512.08027, ~200-page report, DOE Milestone-certified). 1.1 GW thermal, 390 MWe net.
- **Eos**: Design published in Nuclear Fusion (Jan 2025). Demonstration stellarator / neutron source.
- **Assessment**: Yes — Helios is a published plant design (preconceptual level, DOE-certified).

### Lab Experiments
- **Wendelstein 7-X** (IPP Greifswald): World's largest stellarator, demonstrates stellarator physics
- **CNT** (Columbia Non-neutral Torus, Columbia University): Stellarator experiment with heritage connection
- **Thea Energy 3x3 array**: Company's own superconducting planar coil array prototype (2025), demonstrated stellarator-relevant field production with 10x better optimization than W7-X

### Key Design Parameters
| Parameter | Value |
|-----------|-------|
| Major radius | 8 m |
| Aspect ratio | 4.5 |
| On-axis field | 6 T |
| Max coil field | 20 T |
| Fusion power | 958 MW |
| Thermal power | 1,094 MW |
| Net electric | 390 MWe |
| Capacity factor | 88% |
| First wall lifetime | 15 full-power years |
| First wall material | V-4Cr-4Ti + W armor |
| Divertor | Tokamak-like X-point (novel for stellarator) |
| Thermal efficiency | ~40.2% |
| LCOE target | $150/MWh -> $60/MWh at scale |
| Eos first plasma | 2030 |
| Helios first plasma | mid-2030s |

## Remaining Gaps

All 12 differentiation columns have been filled with **high confidence**. No remaining gaps.

The Helios preconceptual design paper (arXiv:2512.08027) is exceptionally detailed and provides direct, authoritative answers for every column. This is one of the most thoroughly documented private fusion concepts, likely because the DOE Milestone program required a comprehensive preconceptual design report.

Minor notes:
- The specific HTS conductor (REBCO vs other HTS) is implied but not explicitly named. REBCO is the only commercial HTS tape capable of 20 T at 20 K, so this is effectively certain.
- The exact Q value is not stated as a number, but with 958 MW fusion / 1 MW ECRH, Q > 900 — effectively ignited.

## Key Sources

1. **arXiv:2512.08027** — "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant" (Dec 2025). Primary technical source (~200 pages).
   - https://arxiv.org/html/2512.08027v1
   - https://thea.energy/wp-content/uploads/2025/12/20251210_FPP_Helios_overview_paper.pdf
   - Saved: `iter-01/sources/thea-energy-helios-arxiv-2512-08027.md`

2. **Thea Energy website** — Technology page, Eos page, press releases
   - https://thea.energy/fusion-technology/
   - https://thea.energy/eos/
   - https://thea.energy/press-release/thea-energy-announces-peer-reviewed-publications-outlining-the-planar-coil-stellarator-approach-for-commercial-fusion-energy/
   - https://thea.energy/press-release/u-s-department-of-energy-certifies-thea-energys-fusion-pilot-plant-preconceptual-design/
   - https://thea.energy/press-release/thea-energy-demonstrates-performance-and-controllability-of-small-and-simple-magnets-for-fusion-energy/
   - Saved: `iter-01/sources/thea-energy-website-and-press.md`

3. **Nuclear Fusion papers** (Jan 2025) — 4 peer-reviewed papers on planar coil stellarator approach (referenced via press release; not individually fetched)

4. **ANS Nuclear Newswire** — https://www.ans.org/news/2025-12-18/article-7628/

5. **Interesting Engineering** — https://interestingengineering.com/energy/thea-energy-unveils-helios-realistic-fusion-power-plant

6. **POWER Magazine** — https://www.powermag.com/thea-energy-completes-fusion-power-plant-preconceptual-design/

7. **PPPL** — Edison Patent Award and DOE Milestone selection press releases


## Gaps to Fill

The following columns need values. Focus your research on these:

No obvious gaps — verify and strengthen existing values.

## Output Format

For EACH column in the schema (including ones already filled — confirm or update them), write:

### [Column Name]
- **Value**: [exact vocabulary value from schema]
- **Confidence**: high | medium | low
- **Citation**: [specific URL, paper reference, or reasoning basis]
- **Notes**: [anything relevant — how you determined this, source disagreements, caveats, qualifiers not captured by the vocabulary value]

Rules:
- **high** confidence: value directly stated by an authoritative source (company website, peer-reviewed paper, official press release)
- **medium** confidence: value inferred from the described approach and general domain knowledge (e.g., "stellarators use ECRH" is medium unless the specific company confirms it)
- **low** confidence: value extrapolated from similar concepts or fragmentary information
- If a column is structurally inapplicable, write `N/A` as the value with a one-line justification
- If you searched and found nothing, write `Unknown` or `TBD` and explain what you tried

After all columns, write a final section:

## Remaining Gaps

List any columns where:
- You could not find a value (explain what sources you checked)
- Your confidence is low (explain what would raise it)
- You found conflicting information (summarize the conflict)
- A specific source type (paper, patent, technical report) might resolve the gap

## Sources Consulted

List all URLs and documents you consulted during this research, even if they didn't yield useful information for the gaps. This helps avoid re-searching the same sources in future iterations.
