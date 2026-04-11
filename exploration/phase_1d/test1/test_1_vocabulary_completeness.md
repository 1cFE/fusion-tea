# Test 1: Vocabulary Completeness Audit

**Date**: 2026-03-08
**Input**: `exploration/phase_1b_v2/table_v2.csv` (38 concepts), `exploration/phase_1b_v2/schema_v2.md`

## Method

For each of the 18 differentiation columns:
1. List the current vocabulary (unique non-N/A, non-TBD, non-Unknown values observed in the table)
2. Classify as **Closed** (exhaustive of physically plausible options) or **Open** (sample-dependent, plausible values missing)
3. For open vocabularies, list physically plausible missing candidates
4. Classify each gap: **(a)** historical approach no startup has revived, **(b)** theoretically valid but never attempted, **(c)** values that exist but were lumped into a coarser label

Assessment basis: physics reasoning and domain knowledge. The question is whether the vocabulary spans the *physically plausible design space*, not just the startup sample.

---

## Summary Table

| # | Column | Observed Values | Schema Values | Open/Closed | Missing Candidates | Gap Types |
|---|--------|:-:|:-:|---|---|---|
| 1 | Confinement Family | 4 | 4 | **Closed** | — | — |
| 2 | MFE Topology | 5 | 5 | **Open** | Spheromak, RFP | a, c |
| 3 | IFE Driver | 4 | 4 | **Open** | Z-pinch (wire array), Light ion beam | a |
| 4 | MIF Method | 2 | 2 | **Open** | Plasma jet MITF, Laser-driven MIF | a, c |
| 5 | Non-Standard Mechanism | 3 | 3 | **Open** | Beam-target, Pyroelectric | b |
| 6 | Tokamak Shape | 4 | 4 | **Closed** | — | — |
| 7 | Stellarator Type | 4 | 4 | **Open** | Quasi-axisymmetric (QA), Quasi-helical (QH) | a |
| 8 | Laser Approach | 6 | 6 | **Open** | Shock ignition | a |
| 9 | Fuel | 4 | 6 | **Closed** | Cat-D (cost-relevant, not physics-distinct) | — |
| 10 | Primary Heating | 18 | 19 | **Open** | Lower hybrid (LH); see granularity note | c |
| 11 | Energy Capture | 7 | 8 | **Open** | MHD direct conversion, Brayton (He gas) | a, b |
| 12 | Plasma State | 7 | 8 | **Closed** | — | — |
| 13 | Magnet Type | 9 | 11 | **Open** | NI-HTS, Permanent (complementary) | c |
| 14 | Tritium Breeding | 7 | 9 | **Closed** | — | — |
| 15 | Neutron Management | 5 | 6 | **Closed** | — | — |
| 16 | Operation Mode | 3 | 3 | **Closed** | — | — |
| 17 | Repetition Rate | 5 | 7 | **Closed** | — | — |
| 18 | Driver Technology | 37 | free text | **Open (by design)** | N/A | — |

**Result**: 9 Closed, 8 Open (+ 1 open by design). Every open vocabulary has at least one concrete missing candidate with justification.

---

## Per-Column Analysis

### Column 1: Confinement Family — CLOSED

**Vocabulary (4)**: MFE, IFE, MIF, Non-Standard

These four categories are the canonical decomposition of fusion approaches by confinement mechanism. MFE covers all magnetic confinement (steady-state and quasi-steady fields). IFE covers all inertial confinement (implosion-driven). MIF covers the intermediate regime (magnetized plasma + external compression). Non-Standard is a principled catch-all for approaches that don't fit the MFE/IFE/MIF framework (electrostatic, catalytic, plasma focus).

**Why closed**: Any conceivable fusion approach confines plasma (or fuel) via magnetic fields (MFE), inertia (IFE), a combination (MIF), or some other mechanism (Non-Standard). The categories partition the physics space. One could argue for "Gravitational" (stellar confinement) but this is not engineering-relevant.

---

### Column 2: MFE Topology — OPEN

**Vocabulary (5)**: Tokamak, Stellarator, Open/Linear, Compact Toroid, Dipole

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Reversed-Field Pinch (RFP)** | Toroidal plasma where the toroidal field reverses direction at the edge, creating a self-organized minimum-energy state. Historically demonstrated (RFX-mod in Italy, MST at Wisconsin, EXTRAP-T2R in Sweden). Distinct confinement physics from tokamak — requires strong plasma current but achieves confinement via magnetic relaxation rather than external rotational transform. | (a) Historical — no active startup pursues RFP. Dead branch of the design space. |
| **Spheromak** | Compact toroid with both toroidal and poloidal fields generated entirely by internal plasma currents. Distinct from FRC (which has zero or near-zero toroidal field). Historically demonstrated (SSPX at LLNL, CTX at Los Alamos, S-1 at Princeton). Currently lumped under "Compact Toroid" alongside FRC. | (c) Lumped — Spheromak and FRC are both compact toroids but have different field topology (spheromak has toroidal field, FRC does not), different stability properties, and different heating/sustainment challenges. |

**Structural note**: "Compact Toroid" conflates two physically distinct topologies (FRC and Spheromak). Since only one concept uses this value (TAE, which is FRC), the conflation is invisible in the current sample. A spheromak startup would need to distinguish itself.

**Not missing**: Bumpy torus (ELMO) — historical curiosity with no physics advantage that warrants its own entry. Torsatron — a stellarator variant, correctly lumped.

---

### Column 3: IFE Driver — OPEN

**Vocabulary (4)**: Laser, Projectile, Heavy ion beam, Acoustic

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Z-pinch (wire array)** | Pulsed-power-driven wire array implosion creates intense X-ray source that drives capsule compression. The Z-machine at Sandia is the world's most powerful X-ray source and has achieved thermonuclear conditions this way. Distinct from laser (pulsed power, not photons) and distinct from magnetic Z-pinch confinement (the Z-pinch here is the *driver*, not the confinement). | (a) Historical — extensively researched at Sandia, no commercial startup pursuing it as an IFE driver. |
| **Light ion beam** | Accelerator-produced light ions (protons, lithium) ablate target surface. Investigated extensively at Sandia (PBFA-II) in the 1980s-90s before being abandoned in favor of heavy ions and Z-pinch. | (a) Historical — abandoned approach. |

**Not missing**: Electron beam (1970s-80s concept, never demonstrated adequate coupling efficiency — fundamentally limited by range-energy relation in targets). Plasma jet (this would be MIF, not IFE — the magnetized plasma is an essential feature).

---

### Column 4: MIF Method — OPEN

**Vocabulary (2)**: FRC compression, Magnetized target

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Plasma jet MITF** | Multiple plasma jets converge to compress a magnetized target plasma. Distinct from liner-driven compression (MagLIF) and mechanical compression (General Fusion) — the compression medium is plasma, not metal or pistons. HyperJet Fusion pursued this before shutting down; the physics approach remains valid. | (a) Historical — company defunct, but the approach is physically distinct from both current MIF entries. |
| **Laser-driven MIF** | Laser ablation provides the compression of a pre-magnetized target. Distinct from pure IFE (the magnetic field is essential to the confinement during compression, not just an enhancement). MagLIF uses laser preheat but pulsed power for compression — a concept where laser is the primary compressor of magnetized fuel would be distinct. | (c) Lumped — currently would fall under "Magnetized target" but the driver mechanism is fundamentally different (photon pressure vs. electromagnetic vs. mechanical). |

**Structural note**: With only 3 MIF concepts in the table, this column's vocabulary is heavily sample-limited. The MIF design space has more internal diversity than 2 values suggest — the compression driver (pulsed power, mechanical, plasma jets, laser) is a genuine design dimension within MIF that is collapsed here.

---

### Column 5: Non-Standard Mechanism — OPEN

**Vocabulary (3)**: Electrostatic, Plasma focus, Muon-catalyzed

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Beam-target** | Accelerator-produced ions impinge on a stationary or counter-propagating target. No confinement — fusion occurs during the collision. Examples: existing neutron generators (D-T beam-target), proposed concepts for boron neutron capture therapy sources. Physically distinct from electrostatic confinement (no potential well, no recirculation). | (b) Theoretical — used industrially for neutron production but never proposed as a power source (Coulomb scattering losses dominate at power-relevant rates). |
| **Pyroelectric** | Pyroelectric crystals (e.g., LiTaO3) generate electric fields strong enough to accelerate deuterium ions to ~100 keV, producing D-D fusion reactions. Demonstrated at UCLA (2005). Not a confinement mechanism — fusion occurs in a beam-target mode driven by crystal-generated fields. | (b) Theoretical — demonstrated as a laboratory phenomenon but cannot scale to power production (nA beam currents). |

**Structural note**: "Non-Standard" is a residual category — it groups approaches by what they are *not* (not MFE, not IFE, not MIF) rather than by what they share. The missing candidates confirm this: beam-target, pyroelectric, and the existing three values have almost nothing in common physically. This is expected for a catch-all.

---

### Column 6: Tokamak Shape — CLOSED

**Vocabulary (4)**: Compact, Spherical, Standard, Negative triangularity

**Why closed**: These four categories cover the discrete clusters in tokamak design space that startups actually target, defined by aspect ratio (A) and triangularity (δ):
- Compact: A ~ 2.5-4, high field, HTS-enabled small size
- Spherical: A < 2, tight center column, natural elongation
- Standard: A ~ 3-4, ITER-heritage mid/large size
- Negative triangularity: δ < 0, improved edge stability

The tokamak shape parameter space is continuous (aspect ratio × elongation × triangularity × ...), but these four categories capture all the commercially distinct design strategies. "Advanced tokamak" (high bootstrap fraction, internal transport barriers) is a plasma operation mode, not a shape — it's captured by other columns (Operation Mode, Primary Heating).

**Potential edge case**: High-field spherical tokamaks (e.g., STEP-class at A ~ 1.7-2) blur the Compact/Spherical boundary. The current categorization places them in "Spherical" by aspect ratio, which is correct since the physics advantages are spherical-tokamak-specific (natural elongation, high β limits).

---

### Column 7: Stellarator Type — OPEN

**Vocabulary (4)**: QI, Modular, Planar coil, Helical coil

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Quasi-axisymmetric (QA)** | Stellarator optimized so that the magnetic field strength is symmetric in the direction of the magnetic axis (like a tokamak), even though the flux surfaces are non-axisymmetric. Distinct confinement physics from QI — QA minimizes neoclassical transport by mimicking tokamak symmetry, while QI minimizes bounce-averaged drift orbits. NCSX was designed as QA before cancellation. Some renewed academic interest. | (a) Historical — no active startup, but a physically distinct optimization with different trade-offs (better particle confinement at the cost of requiring some bootstrap current, unlike QI). |
| **Quasi-helical (QH)** | Stellarator optimized so that the magnetic field strength has helical symmetry. HSX at the University of Wisconsin demonstrated this optimization — excellent neoclassical transport, but challenging coils. | (a) Historical — demonstrated experimentally but no commercial pursuit. |

**Structural problem**: This column mixes two different taxonomic axes:
- **Optimization strategy**: QI, QA, QH — what symmetry does the magnetic field approximate?
- **Coil approach**: Modular, Planar coil, Helical coil — how are the coils physically arranged?

These are not the same question. A QI stellarator could use modular coils, helical coils, or planar coils. A modular coil stellarator could target QI, QA, or QH optimization. The column conflates them because the sample happens to have each concept emphasize one or the other as its distinguishing feature. This is a *classification artifact* — a design space column would separate these into two independent dimensions.

---

### Column 8: Laser Approach — OPEN

**Vocabulary (6)**: Direct drive, Indirect drive, Fast ignition, Hybrid drive, Ultrashort pulse, Liquid jet

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Shock ignition** | Distinct from fast ignition. Uses a high-intensity spike at the end of the compression pulse to launch a converging shock wave that ignites the fuel. Does NOT require a separate ignition beam (unlike fast ignition, which needs a petawatt short-pulse laser). Achieves ignition with a single laser system at higher total energy. Actively researched in Europe (HiPER project), US (NRL), and theoretically demonstrated in simulations. | (a) Historical — actively researched in labs but no commercial startup has adopted it. Differs from fast ignition in driver architecture (one laser vs. two), target physics (shock vs. relativistic electrons), and cost structure (no petawatt system needed). |

**Not missing**: Volume ignition (uniform fuel heating without hot spot — theoretically possible but requires impractically large driver energies; no path to commercial viability). Polar direct drive (a geometric variant of direct drive, not a distinct approach). Double-shell targets (a target design, not a drive scheme).

**Note**: "Hybrid drive" (Xcimer's HDD) is used by only one concept. It may be too company-specific for a morphological dimension — though it does represent a physically distinct approach (direct illumination + indirect X-ray conversion in the same shot).

---

### Column 9: Fuel — CLOSED (with TEA caveat)

**Vocabulary (observed: 4, schema: 6)**: D-T (28), p-B11 (5), D-D (3), D-He3 (2). Schema also includes "Multiple" and "Unknown" (neither observed in sample).

**Why closed (as physics taxonomy)**: The four primary values (D-T, D-D, D-He3, p-B11) are the only fusion fuel cycles with cross-sections high enough to plausibly produce net energy in a terrestrial device. "Multiple" and "Unknown" handle edge cases. No physically plausible fuel cycle is missing.

**Cat-D deserves more weight for TEA purposes**:

| Candidate | Description | Assessment |
|-----------|-------------|------------|
| **Catalyzed-DD (Cat-D)** | D-D plasma operated at conditions where the T and He3 products from D-D reactions are burned in situ before escaping. The tritium branch (D+D → T + p, then T+D → He4 + n) introduces 14.1 MeV neutrons and requires tritium handling infrastructure. The He3 branch (D+D → He3 + n, then D+He3 → He4 + p) adds charged-particle energy. The effective neutron spectrum, shielding requirements, and tritium inventory all differ from pure D-D. | Not a separate fuel — it's an *operating regime* of D-D. But for techno-economic analysis, Cat-D has meaningfully different cost implications from pure D-D: (1) tritium handling infrastructure is needed (pure D-D produces tritium that must either be burned or managed), (2) the neutron spectrum shifts toward 14.1 MeV (heavier shielding, more activation), (3) the energy balance changes (higher energy yield per D consumed, but higher recirculating power to reach Cat-D temperatures). These are cost-relevant distinctions that a pure physics taxonomy misses. |

**Verdict**: Closed for physics taxonomy — the fuel *inputs* are D and D regardless of operating regime. But incomplete for cost-relevant differentiation — the Fuel column alone cannot distinguish a D-D concept operating in pure D-D mode (2.45 MeV neutrons, no tritium management) from one in Cat-D mode (14.1 MeV neutrons, tritium handling, different shielding). This is a case where the table's categorical resolution is too coarse for the project's TEA purpose. The difference would need to be captured by a supplementary column or by the downstream cost model's parametric inputs.

**Not missing (physics)**: p-Li6 and D-Li6 (cross-sections far too low for terrestrial reactors). He3-He3 (even lower cross-section than p-B11; requires He3 supply which doesn't exist on Earth). p-p (solar cycle — 10^-25 barn at solar temperatures).

---

### Column 10: Primary Heating — OPEN

**Vocabulary (observed: 18 real values + TBD + Unknown, schema: 19)**: RF (ECRH), RF (ICRH), RF + NBI, NBI, Ohmic (self-pinch), Magnetic compression, Mechanical compression, Pulsed power implosion, Laser (indirect drive), Laser (direct drive), Laser (fast ignition), Laser (ultrashort pulse), Laser (novel/TBD), Heavy ion beam, Projectile impact, Electrostatic acceleration, Electromagnetic pinch (DPF), Muon catalysis, Acoustic implosion

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Lower hybrid (LH)** | RF waves at the lower hybrid resonance frequency (~1-8 GHz). Primarily used for non-inductive current drive in tokamaks (LHCD). Distinct physics from ECRH (electron heating via cyclotron resonance) and ICRH (ion heating via ion cyclotron resonance) — LH waves couple to the electron Landau damping and drive directional current. Planned for ITER. Widely used on JET, EAST, KSTAR. | (c) Lumped — LH is collapsed into the RF umbrella, but it operates in a different frequency regime, couples via different physics, and serves a different primary purpose (current drive vs. bulk heating). No startup uses it as *primary* heating because LH is a current drive tool — but for steady-state tokamaks, current drive IS the primary sustainment mechanism. |

**Not missing**: Alpha heating (a consequence, not an external heating method). Compression heating in tokamak major-radius shifts (historical technique from TFTR era — not used commercially). Runaway electron heating (a pathological scenario, not a design choice).

**Granularity asymmetry and hidden context-dependence**: This column has 19 schema values — extremely granular, and exhibiting the same structural problem that Phase 1b identified in Confinement Concept. The column has *different information-theoretic roles in different families*:

- **For IFE and Non-Standard concepts**, the heating method IS the concept. "Laser (direct drive)" doesn't describe a choice *within* an IFE concept — it describes the concept itself. Changing the heating method changes the concept. The column is functioning as an identifier, not a morphological dimension.
- **For MFE concepts**, heating IS a genuine design choice. An ECRH-heated tokamak and an ICRH-heated tokamak are the same confinement concept with a different engineering decision. The column carries real combinatorial information.

This means the column has family-dependent semantics — exactly the context-dependence the investigation is probing, hiding inside a flat column. The 18 values are not 18 positions along a single design dimension; they are drawn from at least 4 disjoint sub-vocabularies (MFE heating methods, IFE driver-as-heating, MIF compression-as-heating, Non-Standard mechanism-as-heating) that only look like they occupy the same axis because the tree was flattened.

This is a milder version of the Phase 1b Confinement Concept problem. Confinement Concept had 29 values and was functionally an ID. Primary Heating has 18 values and is functionally an ID *within IFE/MIF/Non-Standard* while remaining a genuine dimension *within MFE*. The mixed role is invisible in a flat table but would be explicit in a branching structure where IFE concepts don't have a "heating method" design choice — they just have their driver.

---

### Column 11: Energy Capture — OPEN

**Vocabulary (observed: 5 real + 2 state, schema: 8)**: Thermal (steam) (12), Thermal (unspecified) (15), Thermal (sCO2) (2), Direct (inductive) (1), Direct (charged particle) (3), Hybrid (thermal + direct) (3), TBD (2). Schema also includes "Neutron applications" (not observed).

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **MHD direct conversion** | Liquid metal or ionized gas flows through a magnetic field, inducing an electric current. No moving parts, no thermal cycle. Theoretically applicable to liquid metal blanket systems (flowing LiPb or Li). Studied extensively in the 1960s-70s for coal MHD and proposed for fusion blankets. Efficiency limited by Hartmann boundary layers and electrode erosion. | (a) Historical for coal; (b) theoretical for fusion — no fusion concept has adopted MHD conversion, but it's physically compatible with several liquid-metal-blanket concepts (Renaissance, Helical Fusion, General Fusion). |
| **Brayton (He gas)** | High-temperature helium Brayton cycle. Higher Carnot efficiency than steam Rankine at the same peak temperature, more compact than steam turbines. Proposed for some Gen-IV fission reactors and the EU DEMO helium-cooled blanket concepts. Distinct from sCO2 Brayton in working fluid, operating conditions, and equipment. | (c) Lumped — could be considered a thermal variant, but the engineering (He turbomachinery, large volumetric flow rates) is substantially different from both steam Rankine and sCO2 Brayton. |

**Not missing**: Thermoelectric conversion (too low efficiency for bulk power — Carnot-limited Seebeck devices). Thermophotovoltaic (theoretical but efficiency too low and degradation too rapid for fusion power plant duty cycles).

**Abstraction-level mixing**: The vocabulary contains values at different levels of specificity: "Thermal (steam)" and "Thermal (sCO2)" name specific thermodynamic cycles, while "Thermal (unspecified)" indicates the category without committing to a cycle. These coexist as vocabulary peers, but they answer different questions — one says "I know the power conversion approach," the other says "I know it's thermal but not which kind." This is a minor version of the Stellarator Type problem (mixing abstraction levels in one column). It's pragmatic — early-stage concepts genuinely haven't chosen — but it means two concepts classified as "Thermal (unspecified)" could turn out to be making very different engineering choices. For the 15 concepts (39%) currently at "Thermal (unspecified)", this column carries less information than it appears to.

---

### Column 12: Plasma State — CLOSED

**Vocabulary (observed: 7, schema: 8)**: Burning (12), Compressed (14), Sustained (5), Pinch (2), Confined (2), Transient (1), Non-burning (1). Schema also includes "Solid-state" (not observed in sample — would apply to lattice confinement concepts if any were included).

**Why closed**: These categories span the meaningful plasma regimes for fusion:
- **Burning/Sustained**: steady-state MFE, distinguished by Q (self-heating vs. externally sustained)
- **Compressed**: all IFE and MIF during the implosion event
- **Transient**: pulsed MIF between steady-state and single-shot
- **Pinch**: self-compressed current-carrying plasma
- **Confined**: sub-ignition steady-state MFE
- **Non-burning**: sub-Q=1 devices (neutron sources)
- **Solid-state**: non-plasma fusion (lattice effects)

**Borderline candidate**: "Detonation" — a propagating burn wave through fuel, distinct from hot-spot ignition followed by volumetric burn. Proposed theoretically for some high-gain IFE and for ICF physics. However, this is a *burn mode* within the Compressed state, not a separate plasma state. Keeping as closed.

---

### Column 13: Magnet Type — OPEN

**Vocabulary (observed: 9 real values + TBD + Unknown, schema: 11)**: HTS (wound), HTS (3D stellarator), HTS (planar array), HTS (levitated dipole), LTS+HTS, Pulsed EM, Self-confined, Resistive, Electrostatic. Schema also includes standalone "LTS" and "N/A" (both used — LTS appears in BEST tokamak as part of LTS+HTS; N/A appears for IFE concepts).

**Missing candidates**:

| Candidate | Description | Gap Type |
|-----------|-------------|----------|
| **Non-insulated HTS (NI-HTS)** | HTS coils wound without inter-turn electrical insulation. Fundamentally different quench behavior from insulated HTS — current redistributes through radial turn-to-turn contacts during a local quench, making the coil self-protecting rather than catastrophically failing. Different manufacturing process (no co-winding of insulation), different charging dynamics (long time constants due to eddy currents), different steady-state performance (some current leakage). Tokamak Energy has explored NI-HTS; several magnet development programs investigate it. Physically distinct from insulated HTS in the same way that QA vs QI are distinct for stellarators — same base material, different engineering approach with different trade-off profiles. | (c) Lumped — currently collapsed into the HTS variants (wound, 3D, etc.), but insulation strategy is an independent design axis from winding geometry. |
| **Permanent magnets (complementary)** | Permanent magnets used alongside electromagnetic coils for partial field shaping — not as the primary confinement field, but as a complementary element that reduces the required electromagnetic coil current or simplifies coil geometry. Some stellarator proposals investigate permanent magnet arrays to provide part of the non-axisymmetric field. Physically distinct from a pure electromagnetic approach because it introduces field-quality constraints (demagnetization at temperature, limited field tunability). | (c) Lumped — would currently fall under the primary coil technology (e.g., "HTS (3D stellarator)") with the permanent magnet contribution invisible. |

**Structural problem**: Like Stellarator Type, this column conflates multiple independent design axes into a single vocabulary:
- **Superconductor material**: REBCO vs. Nb3Sn vs. BSCCO vs. none
- **Winding geometry**: wound solenoid/D-coil vs. 3D stellarator vs. planar array vs. single dipole
- **Insulation strategy**: insulated vs. non-insulated (NI-HTS)
- **Operating mode**: steady-state (superconducting) vs. pulsed (resistive/capacitor-driven)

The current vocabulary bundles these into compound labels (e.g., "HTS (wound)" = REBCO + solenoid/D-coil + insulated + steady-state). This works as long as the sample doesn't include concepts that combine these axes differently — but a NI-HTS wound tokamak coil vs. an insulated HTS wound tokamak coil would have the same vocabulary value despite genuinely different engineering trade-offs (quench management, charging time, manufacturing, cost).

**Not missing**: Flux-compressed magnets (single-shot devices, incompatible with power plant duty cycles). BSCCO conductor (functionally obsoleted by REBCO for fusion — any BSCCO concept would be captured under the appropriate HTS variant).

---

### Column 14: Tritium Breeding — CLOSED

**Vocabulary (observed: 7 real + TBD, schema: 9)**: Liquid Li blanket (5), LiPb blanket (4), Li blanket (unspecified) (4), Liquid metal wall (3), FLiBe blanket (2), Solid ceramic breeder (HCPB) (2), Self-bred (DD side) (1), TBD (8). Schema also includes "N/A" (observed for non-tritium concepts).

**Why closed**: The vocabulary covers all breeding material approaches:
- Three lithium-bearing liquids (pure Li, LiPb eutectic, FLiBe molten salt)
- One solid breeder (ceramic pebble bed with neutron multiplier)
- One dual-purpose approach (liquid metal wall — breeding + structural)
- One unique cycle (DD side-reaction self-breeding)
- "Li blanket (unspecified)" handles early-stage concepts
- N/A for non-tritium fuel cycles

The *cooling* approach (water-cooled vs. He-cooled vs. self-cooled) is not captured — but that's a separate design dimension, not a gap in the breeding vocabulary. EU DEMO's WCLL and DCLL differ in cooling, not in breeding material (both use LiPb). Similarly, HCPB captures the breeding material; the helium cooling is implicit.

**TBD density note**: 8 of the ~29 D-T/D-He3 concepts (28%) have TBD for Tritium Breeding — the highest TBD rate of any column. The vocabulary is complete but the data is not: many concepts have not committed to a breeding approach. This doesn't affect the open/closed verdict (the vocabulary spans the option space), but it limits how much the table actually tells you about each concept. For a TEA comparison, breeding approach is a major cost driver (blanket material choice cascades through CAS 22-26), and 28% undetermined means the table cannot distinguish nearly a third of D-T concepts on this axis. This is a *data completeness* problem, not a *vocabulary completeness* problem, but it matters for how actionable the table is.

---

### Column 15: Neutron Management — CLOSED

**Vocabulary (observed: 5, schema: 6)**: Integrated blanket/shield (21), Heavy shielding (14 MeV) (7), Minimal (aneutronic) (5), Heavy shielding (D-D) (3), Reduced (D-He3) (2). Schema also includes "N/A" (not observed — all 38 concepts have some neutron management answer).

**Why closed**: The five values form a monotonic spectrum from heaviest neutron burden (14 MeV D-T) to lightest (aneutronic), with an integrated option that consolidates blanket + shield functions. This covers the full range of neutron management strategies.

**Not missing**: "Sacrificial/replaceable first wall" is a *maintenance strategy*, not a management approach — it would apply alongside any of the existing values. "Active neutron economy" (using neutrons for both breeding and commercial isotope production) is a *business model* addition to any of the existing approaches, not a separate management category.

---

### Column 16: Operation Mode — CLOSED

**Vocabulary (3)**: Pulsed (17), Steady-state (16), Quasi-steady (5)

**Why closed**: Every fusion concept operates somewhere on the temporal axis. These three categories partition it at the only physically meaningful boundaries:
- **Pulsed**: discrete burn events (sub-second to seconds) with recovery/reload
- **Quasi-steady**: long pulses (>5 minutes) with brief interruptions
- **Steady-state**: continuous operation

The schema's >5 minute threshold for quasi-steady vs. pulsed is a reasonable operational boundary (below ~5 minutes, the thermal cycling of the first wall becomes a dominant engineering constraint; above it, it does not).

---

### Column 17: Repetition Rate — CLOSED

**Vocabulary (observed: 5, schema: 7)**: ~10 Hz (8), Sub-Hz (3), ~1 Hz (3), kHz (2), High (>10 Hz) (1). Schema also includes "TBD" and "N/A" (both used by concepts in the table).

**Why closed**: This is a logarithmic binning of a continuous parameter. The bins span from Sub-Hz to kHz, covering all physically meaningful repetition rate regimes for pulsed fusion. No concept operates above kHz (limited by driver recovery time, target injection, and chamber clearing). No concept operates below Sub-Hz that isn't better characterized as single-shot (which isn't a power plant mode).

---

### Column 18: Driver Technology — OPEN (by design)

**Vocabulary**: 37 unique free-text entries (38 concepts, 1 "Unknown").

This column is intentionally unconstrained — it captures the concept-specific engineering subsystem. Every concept has a different driver technology entry. The column functions as a semi-structured identifier, not a morphological dimension. It is open by design and will always be open.

**Not assessed** for vocabulary completeness — the question "is the vocabulary exhaustive?" is not meaningful for a free-text column.

---

## Cross-Cutting Observations

### 1. Open vs. Closed correlates with hierarchy depth

The **closed** columns are generally those that operate at the top level of a well-understood design space:
- Confinement Family (4 canonical categories)
- Tokamak Shape (4 well-characterized design clusters)
- Fuel (4 commercially relevant cycles — with a TEA caveat on Cat-D)
- Plasma State, Operation Mode, Repetition Rate (monotonic spectra with natural boundaries)
- Tritium Breeding, Neutron Management (complete approach inventories)

The **open** columns are those that:
- Sit deeper in the confinement hierarchy (MFE Topology, Stellarator Type, Laser Approach) — where the tree keeps branching and the sample doesn't reach every leaf
- Are tightly coupled to the specific concepts in the sample (IFE Driver, MIF Method, Primary Heating, Energy Capture) — where the vocabulary is empirically derived from "what the 38 concepts actually chose" rather than "what is physically possible"
- Conflate multiple independent design axes (Stellarator Type, Magnet Type) — where the vocabulary's structure conceals orthogonal choices

### 2. Gap type distribution

| Gap type | Count | Pattern |
|----------|-------|---------|
| (a) Historical — no startup has revived | 10 | Dominant gap type. Most missing values are approaches that were historically investigated and abandoned — RFP, spheromak, wire-array Z-pinch, light ion beam, plasma jet MITF, QA/QH stellarators, shock ignition. The table reflects the current startup landscape, not the full historical design space. |
| (b) Theoretical — never attempted | 4 | Rarer. Beam-target, pyroelectric, MHD direct conversion, He Brayton for fusion. These are physically valid but have never been engineering-committed for fusion power. |
| (c) Lumped — exist but hidden | 7 | Spheromak in Compact Toroid, laser-driven MIF in Magnetized target, LH in RF, He Brayton in Thermal, QA/QH vs coil-type mixing in Stellarator Type, NI-HTS in HTS variants, permanent magnets in primary coil type. These indicate places where the vocabulary's resolution is coarser than the underlying design space. |

**Pattern**: The table's vocabulary is shaped by *which concepts are currently being pursued commercially*. The missing values are overwhelmingly approaches that were historically explored but have no active startup (gap type a). This is expected for a table built from the startup sample — but it means the vocabulary describes the *current commercial landscape*, not the *physically accessible design space*.

The lumped gaps (type c) are equally telling: they show places where independent design axes are compressed into compound labels. This is a classification move — it works when each concept maps cleanly to one compound label, but it hides the combinatorial structure that a design space would expose.

### 3. Axis conflation is a recurring structural problem

Three columns exhibit the same structural issue — conflating independent design axes into a single vocabulary:

**Stellarator Type** mixes optimization strategy (QI, QA, QH) with coil engineering (Modular, Planar, Helical). A QI stellarator can use modular coils (Type One), 3D wound coils (Proxima), or planar coils (Thea). A modular-coil stellarator could target QI or QA optimization. The two axes are independent but conflated because each startup emphasizes one thing.

**Magnet Type** mixes superconductor material (REBCO, Nb3Sn, none), winding geometry (solenoid, 3D, planar, dipole), insulation strategy (insulated, NI-HTS), and operating mode (steady-state, pulsed). The compound labels (e.g., "HTS (wound)") work for classification but hide the trade-off space — a NI-HTS wound coil vs. an insulated HTS wound coil have the same label but genuinely different quench behavior, manufacturing, and cost.

**Primary Heating** mixes genuine design choices (RF heating method for MFE) with concept-defining identities (laser drive scheme for IFE). See Section 4 below.

In all three cases, the conflation is invisible as long as the sample maps cleanly to the compound labels. It becomes visible when you try to *generate* new concepts — the compound labels can't be independently varied because they bundle axes that should be orthogonal.

### 4. Primary Heating has family-dependent semantics (hidden context-dependence)

This is the most important structural finding of the vocabulary audit. Primary Heating has 18 real values — a 4.5× vocabulary size ratio compared to Confinement Family's 4 values — and its information-theoretic role changes by family:

| Family | Role of Primary Heating | Semantics |
|--------|------------------------|-----------|
| MFE | Genuine design choice | RF (ECRH) vs RF (ICRH) vs NBI are independent decisions within the same concept type |
| IFE | Concept identity | "Laser (direct drive)" doesn't describe a choice *within* the concept — it IS the concept |
| MIF | Concept identity | "Mechanical compression" IS General Fusion; "Pulsed power implosion" IS MagLIF |
| Non-Standard | Concept identity | "Muon catalysis" IS the concept; "Electrostatic acceleration" IS the concept |

For IFE/MIF/Non-Standard, the heating method is functionally an identifier — changing it changes the concept entirely. For MFE, it's a genuine design dimension with combinatorial freedom. This means the column carries *context-dependent information* — exactly the phenomenon the investigation is probing — hidden inside a flat column.

This is a milder version of the Phase 1b Confinement Concept problem. Confinement Concept had 29 values and was a near-ID column. Primary Heating has 18 values and is a near-ID *within non-MFE families* while remaining a genuine dimension *within MFE*. The mixed role would be explicit in a branching structure where IFE concepts don't have a separate "heating method" node — they just have their driver.

### 5. Granularity inconsistency across columns

The vocabulary size varies by 4.5× across controlled-vocabulary columns:

| Vocabulary size | Columns |
|:-:|---|
| 2 | MIF Method |
| 3 | Operation Mode, Non-Standard Mechanism |
| 4 | Confinement Family, IFE Driver, Tokamak Shape, Stellarator Type, Fuel |
| 5 | MFE Topology |
| 6 | Laser Approach, Neutron Management, Repetition Rate |
| 7-9 | Tritium Breeding, Energy Capture, Plasma State |
| 11 | Magnet Type |
| 18 | Primary Heating |

Zwicky's original General Morphological Analysis assumed roughly comparable vocabulary sizes per dimension (~4-6 values), because the power of cross-consistency assessment depends on the dimensions being comparable in granularity. When one column has 18 values and another has 2, they are operating at fundamentally different levels of abstraction.

The uneven granularity is itself evidence of classification rather than design-space structure:

- **Low-granularity columns** (2-6 values) tend to represent genuine morphological dimensions — real questions with comparable alternatives. These are the columns closest to what Zwicky envisioned.
- **High-granularity columns** (11-18 values) tend to be empirical enumerations — catalogs of what exists rather than spectra of what's possible. They approach the near-ID behavior that Phase 1b identified as the collapse mode of classification schemes.

A morphological design space would have columns of comparable resolving power. The 4.5× range suggests the table is mixing true dimensions (small vocabulary, high combinatorial freedom) with empirical inventories (large vocabulary, low combinatorial freedom — most value-pairs are N/A or physically forbidden).

### 6. TBD and abstraction-level mixing limit actionability

Two columns have significant data-completeness or abstraction-level issues that don't affect the open/closed verdict but limit how actionable the table is:

**Tritium Breeding**: 8 of ~29 applicable concepts (28%) are TBD. The vocabulary is complete (the option space is spanned) but nearly a third of D-T concepts haven't committed to a breeding approach. Since blanket choice is a major cost driver (cascading through CAS 22-26), this means the table can't distinguish a third of its D-T population on one of the most cost-relevant axes.

**Energy Capture**: 15 of 38 concepts (39%) are "Thermal (unspecified)" — a placeholder that coexists alongside specific values like "Thermal (steam)" and "Thermal (sCO2)". The vocabulary mixes specificity levels: some entries answer "what is your power conversion cycle?" while others answer "what category is it in?" Two concepts both classified as "Thermal (unspecified)" could turn out to be making very different engineering choices (Rankine vs. Brayton vs. sCO2) with very different cost implications.

These are not vocabulary gaps — they're *information resolution* problems. The table has the right categories but lacks the data to populate them, or mixes definite answers with indefinite ones in the same column. For TEA purposes, this dilutes the table's discriminating power on cost-critical axes.

### 7. Implications for Test 2 (Generative Coherence)

The open vocabularies have a specific implication for random concept generation: if the vocabulary doesn't span the full space, random sampling will only produce combinations from the observed startup landscape. The generative test will measure how constrained the *observed* space is, not the *physically possible* space. This is still informative — it tells us how much implicit constraint exists among the choices startups actually make — but the distinction matters for interpreting the coherence rate.

The granularity asymmetry (Observation 5) also affects generation: random sampling from an 18-value column produces much more diversity than from a 4-value column, but this diversity may be spurious if the 18 values include many family-specific entries that are incompatible with most other column values.
