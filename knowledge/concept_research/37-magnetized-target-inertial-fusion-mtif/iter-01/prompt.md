# Fusion Concept Research: Magnetized Target Inertial Fusion - MTIF (D-D)

You are a research agent investigating a specific fusion energy concept for a differentiation table. Your job is to find accurate, cited information for each column in the table schema.

## Concept

- **Name**: Magnetized Target Inertial Fusion - MTIF (D-D)
- **Company**: NearStar Fusion
- **Confinement approach**: Magneto-Inertial Fusion
- **Description**: Plasma armature railgun launches a magnetized fuel pellet (~10 km/s) into a molten Pb target chamber; D-D primary with D-T backup. Split from First Light row in v3 ontology.
- **Known fuel**: D-D (Deuterium-Deuterium)
- **Operation mode**: Pulsed

## Task

Research this concept and provide findings for each column listed under "Gaps to Fill" below. For columns already filled with high confidence, you do not need to re-research them — but if you find contradictory information, note it.

## Research Strategy

1. **Start broad**: Search the web for "NearStar Fusion fusion technology" and similar queries. Look for the company's website, Wikipedia page, Fusion Industry Association profile, press releases, and investor presentations.
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

**Version**: 0.3.0 (post-SCHEMA_REVISION_PROPOSALS)
**Last updated**: 2026-05-12

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
- **Confidence** (per-cell): `high` (directly stated by source) · `medium` (inferred from described approach) · `low` (extrapolated from similar concepts)
- **Overall Confidence** (per-concept, in `table.csv`): Five-level scale — `high` · `medium-high` · `medium` · `medium-low` · `low`. Reflects the aggregate quality of a concept's dossier. Per-cell confidence remains three-level.

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
| MFE | `Tokamak` · `Compact tokamak` · `Spherical tokamak` · `Negative triangularity tokamak` · `Stellarator (QI)` · `Stellarator (modular)` · `Stellarator (planar coil)` · `Stellarator (helical coil)` · `Magnetic mirror` · `FRC (beam-driven)` · `FRC (pulsed)` · `Z-pinch (sheared-flow)` · `Levitated dipole` · `Levitated dipole (orbital)` |
| IFE | `Laser ICF (indirect drive)` · `Laser ICF (direct drive)` · `Laser ICF (hybrid drive)` · `Laser ICF (fast ignition)` · `Laser ICF (ultrashort pulse)` · `Laser ICF (liquid jet)` · `Projectile ICF` · `Heavy ion beam ICF` |
| MIF | `Magnetized target (pneumatic)` · `Magnetized target (pulsed power)` · `FRC (pulsed compression)` |
| Electrostatic | `IEC / Fusor` · `Polywell` · `Orbital electrostatic` |
| Other | `Dense plasma focus` · `Muon-catalyzed fusion` · `Acoustic / Sonofusion` · `Lattice confinement` |

**Notes**:
- `Tokamak` (plain) is for conventional or mid-size devices (R > 3 m) that are not explicitly compact or spherical. `Compact tokamak` connotes a high-field-enabled compact design (R < ~2.5 m).
- `Stellarator (QI)` vs `Stellarator (modular)`: Use `(QI)` when the concept's primary innovation emphasis is the quasi-isodynamic physics optimization. Use `(modular)` when the emphasis is on manufacturing/assembly approach (modular coil cassettes). Both may be true — pick the dominant framing.

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

### Column 6: Magnet Type

**Definition**: The primary magnet technology used for plasma confinement. For concepts without magnetic confinement, record the driver's magnet subsystem only if it's a distinguishing feature.

| Value | Description |
|-------|-------------|
| `HTS (wound)` | High-temperature superconducting REBCO tape wound into coils. Tokamak D-coils, mirror solenoids. 12-20+ T. |
| `HTS (3D stellarator)` | HTS REBCO in complex 3D non-planar stellarator coil geometry. Includes modular and continuous helical winding approaches. |
| `HTS (planar array)` | Arrays of simple flat HTS coils producing stellarator fields via current distribution. |
| `HTS (levitated dipole)` | Single levitated HTS coil creating dipolar field. |
| `LTS` | Low-temperature superconducting (NbTi or Nb3Sn). ITER heritage. 4 K operation. |
| `LTS+HTS` | Dual development strategy with both conductor families. |
| `Resistive` | Resistive electromagnets (copper, aluminum, or custom alloy). Includes steady-state (continuous power) and pulsed (capacitor-bank-driven) duty cycles — duty cycle is captured by Operation Mode. |
| `None` | No external confinement magnets. Covers IFE drivers (plasma confined by inertia), self-confined plasmas (Z-pinch, DPF — plasma generates own field), mechanically-compressed concepts (MTF), and self-magnetizing concepts (Pacific Fusion). |
| `Electrostatic` | Confinement by electric fields, not magnetic fields. |
| `N/A` | Magnet technology is not a meaningful differentiator for this concept. |

**Notes**:
- Renaissance Fusion's laser-patterned HTS film on cylinders is classified as `HTS (3D stellarator)` — the manufacturing method is novel but the functional result is a 3D stellarator field. Note the manufacturing distinction in the dossier.
- Helion's coils are `Resistive` (copper, aluminum, custom alloys); the capacitor-bank pulsed duty cycle is captured by `Operation Mode = Pulsed`, not by the magnet type.
- Concepts previously classified as `Self-confined` (Zap Energy Z-pinch, LPPFusion DPF, General Fusion MTF) now use `None` — no external confinement coils. The plasma physics distinction (self-pinch vs mechanical compression vs IFE) is captured in `Confinement Concept`.
- Pacific Fusion's self-magnetizing targets (axial field from drive current itself) → `None`. The Z-machine-class premagnetization coil heritage is captured under `Driver Technology`, not `Magnet Type`.

---

### Column 7: Blanket Config

**Definition**: The chemistry/architecture of the blanket system. For D-T concepts: how tritium is bred and how the first wall handles heat and neutrons. For non-D-T concepts: whether a blanket is needed at all.

| Value | Description |
|-------|-------------|
| `Liquid metal` | Liquid-metal blanket or wall — LiPb eutectic, pure liquid Li, Li-LiH, or flowing liquid metal first walls without solid multipliers. Includes both contained and flowing-wall architectures. |
| `Molten salt` | Molten-salt blanket — FLiBe, FLiNaBe, or related lithium-fluoride-bearing salts. Combined breeder/coolant/shield. |
| `Solid breeder` | Helium-cooled pebble bed with solid ceramic breeder (Li₄SiO₄ or Li₂TiO₃) and Be/Be₁₂Ti neutron multiplier. ITER TBM baseline; EU-DEMO HCPB heritage. |
| `Other/hybrid` | Architecturally hybrid blankets that don't fit a single chemistry (Renaissance: flowing Li-LiH wall + Pb pebble neutron multiplier). Also covers Helion's self-bred DD-bootstrap fuel cycle (D-He3 plasma producing tritium as DD side reaction, decaying to He3 — no contained breeder). **Flags concept for required per-concept cost-model override** — default unit costs do not apply. |
| `N/A (no tritium)` | Fuel cycle does not include tritium. Applies to p-B11 (aneutronic), D-D (neutronic but no tritium), and D-He3 concepts that don't bootstrap. |
| `N/A (non-power)` | Concept is not a power-producing reactor (neutron source, isotope production, materials testing). Applies regardless of fuel — distinct from `N/A (no tritium)`. |
| `TBD` | D-T concept where blanket configuration has not been disclosed. |

**Notes**:
- The tritium supply crisis is existential for D-T fusion — global civilian tritium is ~25 kg, and a single 1 GWth D-T plant needs >55 kg/year. TBR > 1 is not optional. For D-T concepts, this column should never be `N/A (no tritium)`.
- For D-He3 concepts (Helion), `Other/hybrid` captures the unique DD-bootstrap fuel cycle.
- The two `N/A` flavors are distinct:
  - `N/A (no tritium)` = fuel cycle physics doesn't include tritium
  - `N/A (non-power)` = concept doesn't produce power, so blanket question doesn't apply (e.g., SHINE's accelerator-driven neutron source uses D-T but doesn't breed tritium because it's medical-isotope / materials-testing focused)
- The `Other/hybrid` bucket carries semantic weight downstream: per [SCHEMA_REVISION_PROPOSALS §W4](SCHEMA_REVISION_PROPOSALS.md), cost-modeling tools should treat this value as a flag that **default blanket unit costs are invalid; per-concept override required**.

---

### Column 8: Operation Mode

**Definition**: Temporal profile of the fusion burn.

| Value | Description |
|-------|-------------|
| `Steady-state` | Continuous plasma operation. Plasma maintained indefinitely by external heating/current drive. Characteristic of stellarators, advanced tokamaks, mirrors. |
| `Pulsed` | Discrete short burn events (seconds or less) separated by recovery/reload periods. Characteristic of IFE, MIF, pulsed FRC. |
| `Quasi-steady` | Long-pulse operation (~minutes to hours) with brief interruptions for refueling or re-magnetization. Intermediate between steady-state and pulsed. **Threshold**: pulse lengths > 5 minutes → Quasi-steady, regardless of company self-description. |

---

### Column 9: Repetition Rate

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

### Column 10: Driver Technology

**Definition**: The primary technology that creates and/or sustains the fusion conditions. This is the most concept-specific column — it captures the distinguishing engineering subsystem.

**Vocabulary**: Free text, but aim for consistency. Use the form: `{technology type}` with enough specificity to distinguish from similar concepts.

| Examples | Concept |
|----------|---------|
| `HTS magnets (REBCO, 20 T)` | CFS, Tokamak Energy |
| `Planar HTS coil array` | Thea Energy |
| `3D HTS stellarator coils` | Proxima Fusion |
| `Neutral beam injection` | TAE Technologies |
| `Capacitor-bank resistive coils` | Helion Energy |
| `Excimer laser (KrF, hybrid drive)` | Xcimer Energy |
| `Diode-pumped solid-state laser` | Focused Energy, Inertia Enterprises |
| `Electromagnetic gun` | First Light Fusion |
| `Plasma armature railgun` | NearStar Fusion |
| `Linear induction accelerator` | Intensity Energy |
| `Pneumatic pistons + liquid metal` | General Fusion |
| `Pulsed power (Z-machine class)` | Pacific Fusion |
| `Pulsed power (sheared-flow Z-pinch)` | Zap Energy |
| `CS-free spherical tokamak (ECRH non-inductive drive)` | ENN Energy |
| `Particle accelerator (beam-target)` | SHINE Technologies |
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
| 6 | Magnet Type | Controlled | 10 | Yes (non-magnetic concepts) |
| 7 | Blanket Config | Controlled | 7 | Yes (aneutronic, non-power) |
| 8 | Operation Mode | Controlled | 3 | No |
| 9 | Repetition Rate | Controlled | 7 | Yes (steady-state) |
| 10 | Driver Technology | Free text | — | No |

---

## Schema Evolution Log

| Date | Version | Changes | Trigger |
|------|---------|---------|---------|
| 2026-03-06 | 0.1 | Initial schema | Sprint plan creation |
| 2026-03-07 | 0.2 | +`Tokamak` (Col 2), +`Solid ceramic breeder (HCPB)` (Col 8), QI/modular note (Col 2), >5 min = Quasi-steady (Col 10), `Pulsed` narrowed to short events | Checkpoint 1 review |
| 2026-03-07 | 0.2.1 | Overall Confidence expanded to five-level scale (`high` / `medium-high` / `medium` / `medium-low` / `low`); per-cell confidence remains three-level | Checkpoint 3-4 review (Realta, MagLIF used `medium-high`) |
| 2026-03-08 | 0.2.2 | +`Laser ICF (hybrid drive)` (Col 2) for Xcimer HDD approach. Row restructuring: concept 17 split (Xcimer → hybrid drive, Focused Energy → fast ignition); concept 23 split (Marvel-only, HB11 stays in concept 04); concept 26 now Inertia-only (Xcimer → hybrid drive row) | Checkpoint 5 restructuring decisions |
| 2026-03-08 | 0.2.3 | Renamed `N/A (aneutronic)` → `N/A (no tritium in fuel cycle)` (Col 8) — old label was misleading for D-D concepts which ARE neutronic. Added `Heavy shielding (D-D)` (Col 9) for D-D concepts with 2.45 MeV neutrons; corrected 3 D-D cells from `Heavy shielding (14 MeV)` | Phase 1c measurement integrity |
| 2026-05-12 | 0.3.0 | **Eliminated** `Plasma State` column (Col 6) — derivable from Confinement Concept + Operation Mode. **Eliminated** `Neutron Management` column (Col 9) — implied by Fuel. **Renamed** `Tritium Breeding` → `Blanket Config` (Col 7) with 4 chemistry buckets (`Liquid metal`, `Molten salt`, `Solid breeder`, `Other/hybrid`) + `N/A (no tritium)` + `N/A (non-power)` + `TBD`. **Collapsed** Magnet Type vocabulary: folded `Pulsed EM` into `Resistive`; folded `Self-confined` and `None (IFE)` into single `None` value. Per-concept corrections: Pacific Fusion magnet → `None`; Renaissance blanket → `Other/hybrid`; Helion magnet → `Resistive` (via P4 fold). Net: 12 columns → 10 columns. | SCHEMA_REVISION_PROPOSALS.md + RECLASSIFIED_CONCEPTS.md audit (P3 N/A addendum) |


## Current Knowledge

From the initial concept CSV (no prior research):
- **Confinement Approach**: Magneto-Inertial Fusion
- **Description**: Plasma armature railgun launches a magnetized fuel pellet (~10 km/s) into a molten Pb target chamber; D-D primary with D-T backup. Split from First Light row in v3 ontology.
- **Fuel Type**: D-D (Deuterium-Deuterium)
- **Operation Mode**: Pulsed
- **Published Machine/Plant?**: No
- **Lab Experiments**: 

## Gaps to Fill

The following columns need values. Focus your research on these:

All columns — this is the first iteration. No prior research exists.

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
