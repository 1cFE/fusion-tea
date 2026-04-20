# D1+ Concept Analysis: Muon-Catalyzed Fusion (D-T)

You are producing a D1+ analysis for the fusion concept **Muon-Catalyzed Fusion (D-T)** (Acceleron Fusion).

## Analysis Goals

# Analysis Goals

These are the objectives the analysis agent works toward. Every section of the
analysis should contribute to answering these questions.

1. **Concept Positioning**: How does this concept relate to and compare with
   other fusion approaches? What family does it belong to, and what are the
   nearest neighbors?

2. **Key Differentiators**: What are the key differences from the mainstream
   approach (conventional tokamak)? What is novel, what is borrowed, what is
   shared?

3. **TEA Implications**: How do those differences affect techno-economic
   analysis? Which differences create cost advantages, which create cost
   penalties, and which are cost-neutral?

4. **Modeling Approach**: What is the right way to model those differences?
   What are the key hypotheses that the cost model should test? What parameters
   have the most leverage?

5. **Risks and Assumptions**: Are the key risks and assumptions called out?
   How do we capture them in the TEA — as sensitivity parameters, scenario
   branches, or explicit flags?


## Quality Standards

# Quality Standards

## Citation Standards
Follow the Citation Format section in the output template exactly. Key rules:
- Parameter table Source column: `filename.md §Section Heading` (not bare filenames)
- 3-5 direct block quotes per section for critical claims
- Derivation chains for all [inferred] values
- Footnote-style references in prose with source path and section

## Anti-Hallucination Rules
- If data does not exist in the provided sources, say "No data found in
  available sources"
- Do NOT invent plausible-sounding technical facts, cost figures, or
  performance numbers
- Do NOT cite papers or sources not in the provided materials unless they
  are well-known landmark publications you are certain exist
- When a section has thin data, write a shorter section that honestly states
  what is and isn't known
- Prefer "unknown" over "likely" when evidence is absent

## Depth Expectations
- Match the analytical depth of the handwritten exemplars
- TRL assessments: Demonstrated / On paper only / Missing at scale
- LCOE challenges ranked by impact, not listed randomly
- Materials/supply chain: quantify demand vs. supply where possible
- The analysis should be useful to an engineer building an LCOE model


## Per-Source Reading Pattern

For each source document you need to read, spawn a **separate subagent** using the Agent tool. Do NOT read all sources in your main thread — delegate each source to a subagent for context efficiency.

Each subagent call should follow this pattern:

**Subagent prompt template:**
# Source Reader

Read the source document and answer the provided questions.

## Instructions
1. Read the entire source document
2. For each question, provide a focused answer with:
   - The relevant information from the source
   - The section heading or location where you found it (e.g., §Results, §Table 3)
   - Direct quotes for the most important claims
3. If the source does not contain information relevant to a question,
   say "Not addressed in this source"
4. Keep answers concise — focus on facts and data, not interpretation


Construct each subagent call as follows:
- Give the subagent the path to ONE source document
- Provide 3-5 specific questions (see your mode instructions below for what to ask)
- The subagent reads the source and returns answers with section references

After receiving subagent responses, **read the cited sections yourself** to confirm the subagent's characterization before incorporating claims into the analysis. Do not blindly trust subagent summaries for critical claims.


## Cross-Concept Memory

The following insights were captured from prior concept analyses. Use them
to avoid known pitfalls and apply established patterns. Do not cite these
memories as sources — they are guidance, not evidence. Verify any specific
claims against the actual source documents.

## Assessment Repeatedly Flags Missing O&M Breakdown
Date: 2026-03-29 | Concepts: all

The assessment agent flags missing O&M cost breakdown (fixed vs variable,
scheduled maintenance, unplanned outage costs) in >80% of first-pass
analyses. Cold-start analyses should include a placeholder O&M subsection
in Section 3 even when source data is sparse, to avoid a guaranteed
feedback finding.



## Concept Landscape

The complete taxonomy of all fusion concepts under investigation, grouped by
pipeline maturity. Use this to identify nearest-neighbor concepts for positioning
(Goal 1). Approved concepts have full analyses available for deep reading.
In-progress concepts (I{N}) have N iterations completed.

## Concept Landscape (37 concepts)

Use this catalog for nearest-neighbor identification and cross-concept positioning.
Approved concepts have full analyses available; I{N} indicates N completed iterations.

### Approved (primary cross-reference pool)

| ID | Concept Name | Company | Confinement Family | MFE Topology | IFE Driver | MIF Method | Non-Standard Mechanism | Tokamak Shape | Stellarator Type | Laser Approach | Fuel | Primary Heating | Energy Capture | Plasma State | Magnet Type | Tritium Breeding | Neutron Management | Operation Mode | Repetition Rate | Driver Technology | Overall Confidence | Iterations | Extracted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 21-spherical-tokamak-hts | Spherical Tokamak - HTS | Tokamak Energy | MFE | Tokamak | N/A | N/A | N/A | Spherical | N/A | N/A | D-T | RF (ECRH) | Thermal (unspecified) | Burning | HTS (wound) | Liquid Li blanket | Integrated blanket/shield | Quasi-steady | N/A | HTS magnets (REBCO, 5.25 T on-axis) | medium | iter-1/INTERRUPTED | E |

### In Progress (by maturity)

| ID | Concept Name | Company | Confinement Family | MFE Topology | IFE Driver | MIF Method | Non-Standard Mechanism | Tokamak Shape | Stellarator Type | Laser Approach | Fuel | Primary Heating | Energy Capture | Plasma State | Magnet Type | Tritium Breeding | Neutron Management | Operation Mode | Repetition Rate | Driver Technology | Overall Confidence | Iterations | Extracted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 07-maglif | MagLIF (D-T) | Pacific Fusion, Fuse Energy Technologies | MIF | N/A | N/A | Magnetized target | N/A | N/A | N/A | N/A | D-T | Pulsed power implosion | Thermal (unspecified) | Compressed | Pulsed EM | TBD | Integrated blanket/shield | Pulsed | Sub-Hz | Pulsed power (Z-machine class) | medium-high | iter-9/FAIL (3 findings) | E |
| 09-qi-stellarator-hts | QI Stellarator - HTS | Proxima Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | QI | N/A | D-T | RF (ECRH) | Thermal (unspecified) | Burning | HTS (3D stellarator) | LiPb blanket | Integrated blanket/shield | Steady-state | N/A | 3D HTS stellarator coils (REBCO, 20 T) | medium | iter-9/FAIL (3 findings) | E |
| 01-hts-compact-tokamak | HTS Compact Tokamak | Commonwealth Fusion Systems | MFE | Tokamak | N/A | N/A | N/A | Compact | N/A | N/A | D-T | RF (ICRH) | Thermal (steam) | Burning | HTS (wound) | FLiBe blanket | Integrated blanket/shield | Quasi-steady | N/A | HTS magnets (REBCO, 20 T) | high | iter-7/FAIL (3 findings) | E |
| 17a-laser-icf-hybrid-drive | Laser ICF - Hybrid Direct Drive (D-T) | Xcimer Energy | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Hybrid drive | D-T | Laser (direct drive) | Thermal (unspecified) | Compressed | N/A | FLiBe blanket | Integrated blanket/shield | Pulsed | Sub-Hz | Excimer laser (KrF, 248 nm, 10+ MJ, ASPEN architecture) | medium-high | iter-6/FAIL (1 findings) | E |
| 02-acoustic-icf-sonofusion | Acoustic ICF / Sonofusion (D-D) | Sonofusion Energy | IFE | N/A | Acoustic | N/A | N/A | N/A | N/A | N/A | D-D | Acoustic implosion | TBD | Compressed | N/A | N/A | Heavy shielding (D-D) | Pulsed | kHz | Ultrasonic transducers (acoustic cavitation) | low | iter-5/FAIL (3 findings) | E* |
| 22-projectile-icf | Projectile ICF (D-T) | First Light Fusion, NearStar Fusion | IFE | N/A | Projectile | N/A | N/A | N/A | N/A | N/A | D-T | Projectile impact | Thermal (steam) | Compressed | N/A | Liquid Li blanket | Integrated blanket/shield | Pulsed | Sub-Hz | Electromagnetic gun | medium-high | iter-5/PASS | E |
| 08-frc-w-direct-conversion | FRC w/ Direct Conversion | Helion Energy | MIF | N/A | N/A | FRC compression | N/A | N/A | N/A | N/A | D-He3 | Magnetic compression | Direct (inductive) | Transient | Pulsed EM | Self-bred (DD side) | Reduced (D-He3) | Pulsed | ~1 Hz | Pulsed EM coils (capacitor bank) | high | iter-3/FAIL (2 findings) | E |
| 10-large-scale-stellarator | Large-Scale Stellarator | Gauss Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | QI | N/A | D-T | RF (ECRH) | Thermal (unspecified) | Burning | LTS+HTS | Li blanket (unspecified) | Heavy shielding (14 MeV) | Steady-state | N/A | Non-planar modular SC coils (LTS+HTS, 40 coils, 6T axis / 12-13T peak, demountable) | medium | iter-3/FAIL (3 findings) | E |
| 12-levitated-dipole | Levitated Dipole (D-T) | OpenStar Technologies | MFE | Dipole | N/A | N/A | N/A | N/A | N/A | N/A | D-T | RF (ICRH) | Thermal (unspecified) | Sustained | HTS (levitated dipole) | Solid ceramic breeder (HCPB) | Integrated blanket/shield | Quasi-steady | N/A | Levitated HTS dipole coil (REBCO, 23 T) with on-board flux pump | high | iter-3/FAIL (2 findings) | E |
| 13-electrostatic-hybrid | Electrostatic Hybrid (D-T) | Avalanche Energy | Non-Standard | N/A | N/A | N/A | Electrostatic | N/A | N/A | N/A | D-T | Electrostatic acceleration | Thermal (unspecified) | Non-burning | Electrostatic | TBD | Heavy shielding (14 MeV) | Steady-state | N/A | High-voltage electrostatic cathode (300 kV) with E×B electron co-confinement | medium-low | iter-3/FAIL (3 findings) |  |
| 14-magnetized-target-fusion-pneumatic-compression | Magnetized Target Fusion - Pneumatic Compression (D-T) | General Fusion | MIF | N/A | N/A | Magnetized target | N/A | N/A | N/A | N/A | D-T | Mechanical compression | Thermal (steam) | Compressed | Self-confined | Liquid metal wall | Integrated blanket/shield | Pulsed | ~1 Hz | Pneumatic pistons + liquid metal | high | iter-3/PASS | E |
| 15-sheared-flow-stabilized-z-pinch | Sheared-Flow Stabilized Z-Pinch | Zap Energy | MFE | Open/Linear | N/A | N/A | N/A | N/A | N/A | N/A | D-T | Ohmic (self-pinch) | Thermal (steam) | Pinch | Self-confined | LiPb blanket | Integrated blanket/shield | Pulsed | ~10 Hz | Pulsed power (sheared-flow Z-pinch) | high | iter-3/FAIL (3 findings) | E |
| 28-hts-tokamak-full-hts | HTS Tokamak - Full HTS | Energy Singularity | MFE | Tokamak | N/A | N/A | N/A | Compact | N/A | N/A | D-T | RF (ICRH) | Thermal (unspecified) | Burning | HTS (wound) | TBD | Heavy shielding (14 MeV) | Steady-state | N/A | HTS magnets (REBCO, 25 T) | medium | iter-3/FAIL (3 findings) | E |
| 35-polomac-magnetic-confinement | PoloMac Magnetic Confinement | Deutelio | MFE | Dipole | N/A | N/A | N/A | N/A | N/A | N/A | D-D | Unknown | Thermal (unspecified) | Confined | Resistive | N/A | Heavy shielding (D-D) | Steady-state | N/A | Internal dipole coil with magnetic tunnel supports | medium-low | iter-2/FAIL (3 findings) | E |
| 03-laser-icf-liquid-jet-target | Laser ICF - Liquid Jet Target (D-D) | Cortex Fusion Systems | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Liquid jet | D-D | Laser (ultrashort pulse) | TBD | Compressed | N/A | N/A | Heavy shielding (D-D) | Pulsed | kHz | Femtosecond laser + plasmonic nanoshell targets | low | iter-1/INTERRUPTED | E |
| 04-laser-icf | Laser ICF - p-B11 Fast Ignition | HB11 Energy | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Fast ignition | p-B11 | Laser (fast ignition) | Thermal (steam) | Compressed | N/A | N/A | Minimal (aneutronic) | Pulsed | ~1 Hz | Petawatt ps CPA laser + laser-driven kT field | medium | iter-1/INTERRUPTED | E |
| 05-planar-coil-stellarator | Planar Coil Stellarator | Thea Energy | MFE | Stellarator | N/A | N/A | N/A | N/A | Planar coil | N/A | D-T | RF (ECRH) | Thermal (steam) | Burning | HTS (planar array) | LiPb blanket | Integrated blanket/shield | Steady-state | N/A | Planar HTS coil array (12 encircling + 324 shaping, 20 T, software-controlled) | high | iter-1/INTERRUPTED | E |
| 06-magnetic-mirror | Magnetic Mirror (p-B11) | Pale Blue Fusion | MFE | Open/Linear | N/A | N/A | N/A | N/A | N/A | N/A | p-B11 | RF (ICRH) | Direct (charged particle) | Sustained | TBD | N/A | Minimal (aneutronic) | Steady-state | N/A | Centrifugal mirror with alpha channeling (RF waves, E×B rotation, ponderomotive barriers) | medium | iter-1/INTERRUPTED | E |
| 11-magnetic-mirror | Magnetic Mirror (D-T) | Realta Fusion | MFE | Open/Linear | N/A | N/A | N/A | N/A | N/A | N/A | D-T | RF + NBI | Hybrid (thermal + direct) | Sustained | HTS (wound) | Li blanket (unspecified) | Integrated blanket/shield | Steady-state | N/A | HTS mirror magnets (REBCO, 17+ T) + NBI + ECH | medium-high | iter-1/INTERRUPTED | E |

### Gap-Checked

| ID | Concept Name | Company | Confinement Family | MFE Topology | IFE Driver | MIF Method | Non-Standard Mechanism | Tokamak Shape | Stellarator Type | Laser Approach | Fuel | Primary Heating | Energy Capture | Plasma State | Magnet Type | Tritium Breeding | Neutron Management | Operation Mode | Repetition Rate | Driver Technology | Overall Confidence | Extracted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17b-laser-icf-fast-ignition | Laser ICF - Fast Ignition (D-T) | Focused Energy | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Fast ignition | D-T | Laser (fast ignition) | Thermal (steam) | Compressed | N/A | Li blanket (unspecified) | Integrated blanket/shield | Pulsed | ~10 Hz | DPSSL (Nd:glass, 527 nm) + petawatt CPA ignition laser | medium |  |
| 18-p-b11-frc | p-B11 FRC | TAE Technologies | MFE | Compact Toroid | N/A | N/A | N/A | N/A | N/A | N/A | p-B11 | NBI | Thermal (steam) | Sustained | Resistive | N/A | Minimal (aneutronic) | Steady-state | N/A | Neutral beam injection (high-energy, tangential) | high |  |
| 19-orbital-levitated-dipole | Orbital Levitated Dipole (D-He3) | Zephyr Fusion | MFE | Dipole | N/A | N/A | N/A | N/A | N/A | N/A | D-He3 | RF (ECRH) | Direct (charged particle) | Sustained | HTS (levitated dipole) | N/A | Reduced (D-He3) | Steady-state | N/A | Orbital HTS dipole coil (meter-scale, Falcon 9 deployable) | low |  |
| 20a-type-one-stellarator | QI Modular HTS Stellarator - Infinity Two | Type One Energy | MFE | Stellarator | N/A | N/A | N/A | N/A | Modular | N/A | D-T | RF (ECRH) | Thermal (steam) | Burning | HTS (3D stellarator) | Solid ceramic breeder (HCPB) | Integrated blanket/shield | Steady-state | N/A | Modular HTS stellarator coils (REBCO, 9 T) | high |  |
| 20b-renaissance-stellarator | Compact Liquid-Wall HTS Stellarator | Renaissance Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | Modular | N/A | D-T | NBI | Thermal (sCO2) | Burning | HTS (3D stellarator) | Liquid metal wall | Integrated blanket/shield | Steady-state | N/A | Laser-patterned HTS film on cylinders (REBCO, 10-15 T) | high |  |
| 23-laser-icf-nanostructured-target | Laser ICF - Nanostructured Target (p-B11) | Marvel Fusion | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Ultrashort pulse | p-B11 | Laser (ultrashort pulse) | Hybrid (thermal + direct) | Compressed | N/A | N/A | Minimal (aneutronic) | Pulsed | ~10 Hz | Femtosecond DPSSL + nanostructured Si targets (nanowire arrays, semiconductor lithography) | medium-high |  |
| 24-dense-plasma-focus | Dense Plasma Focus (p-B11) | LPPFusion | Non-Standard | N/A | N/A | N/A | Plasma focus | N/A | N/A | N/A | p-B11 | Electromagnetic pinch (DPF) | Direct (charged particle) | Pinch | Self-confined | N/A | Minimal (aneutronic) | Pulsed | High (>10 Hz) | Pulsed coaxial electrodes (capacitor bank, 2.7 MA) | medium |  |
| 25-heavy-ion-beam-icf | Heavy Ion Beam ICF (D-T) | Intensity Energy | IFE | N/A | Heavy ion beam | N/A | N/A | N/A | N/A | N/A | D-T | Heavy ion beam | Thermal (steam) | Compressed | N/A | Li blanket (unspecified) | Integrated blanket/shield | Pulsed | ~10 Hz | Linear induction accelerator | medium |  |
| 26-laser-icf-indirect-drive | Laser ICF - Indirect Drive (D-T) | Inertia Enterprises | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Indirect drive | D-T | Laser (indirect drive) | Thermal (steam) | Compressed | N/A | Liquid Li blanket | Integrated blanket/shield | Pulsed | ~10 Hz | DPSSL (Thunderwall, 10 kJ x 1000+ beamlines, 10 Hz, 3w UV) | medium-high |  |
| 27-polywell | Polywell (D-T) | EMC2 | Non-Standard | N/A | N/A | N/A | Electrostatic | N/A | N/A | N/A | D-T | Electrostatic acceleration | Thermal (unspecified) | Confined | Resistive | TBD | Heavy shielding (14 MeV) | Steady-state | N/A | Polyhedral magnetic cusp coils + electron beam injection | medium |  |
| 29-negative-triangularity-tokamak | Negative Triangularity Tokamak | Firefly Fusion | MFE | Tokamak | N/A | N/A | N/A | Negative triangularity | N/A | N/A | D-T | RF (ECRH) | Thermal (unspecified) | Burning | HTS (wound) | TBD | Integrated blanket/shield | Quasi-steady | N/A | HTS magnets + NT plasma shaping | medium |  |
| 30-laser-icf-nif-commercialization | Laser ICF - NIF Commercialization (D-T) | Inertia Enterprises | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Indirect drive | D-T | Laser (indirect drive) | Thermal (steam) | Compressed | N/A | Liquid Li blanket | Integrated blanket/shield | Pulsed | ~10 Hz | Diode-pumped solid-state laser (DPSSL, 10 MJ, ~1000 beamlines) | medium-high |  |
| 31-laser-icf-oec-architecture | Laser ICF - OEC Architecture (D-T) | Blue Laser Fusion (BLF) | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Direct drive | D-T | Laser (direct drive) | Hybrid (thermal + direct) | Compressed | N/A | LiPb blanket | Integrated blanket/shield | Pulsed | ~10 Hz | CBC fiber laser + OEC, 5 MJ UV | medium-high |  |
| 32-laser-icf-french-national | Laser ICF - French National Direct Drive (D-T) | GenF Systems | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Direct drive | D-T | Laser (direct drive) | Thermal (unspecified) | Compressed | N/A | Liquid Li blanket | Integrated blanket/shield | Pulsed | ~10 Hz | Diode-pumped solid-state laser (DPSSL) | medium |  |
| 33-state-backed-tokamak-best | State-Backed Tokamak - BEST | Neo Fusion | MFE | Tokamak | N/A | N/A | N/A | Standard | N/A | N/A | D-T | RF + NBI | Thermal (unspecified) | Burning | LTS+HTS | TBD | Heavy shielding (14 MeV) | Quasi-steady | N/A | LTS+HTS magnets (Nb3Sn/YBCO, 6.15T) + multi-method H&CD (50 MW) | medium |  |
| 34-compact-spherical-tokamak-india | Compact Spherical Tokamak - India | Pranos Fusion | MFE | Tokamak | N/A | N/A | N/A | Spherical | N/A | N/A | D-T | TBD | Thermal (unspecified) | Burning | Unknown | TBD | Heavy shielding (14 MeV) | Steady-state | N/A | Unknown | low |  |
| 36-helical-coil-stellarator | Helical Coil Stellarator | Helical Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | Helical coil | N/A | D-T | RF (ECRH) | Thermal (sCO2) | Burning | HTS (3D stellarator) | Liquid metal wall | Integrated blanket/shield | Steady-state | N/A | Continuous helical HTS coils (REBCO WISE conductor, 8 T) + 250 GHz CW gyrotrons | high |  |



## Mode: Cold Start

You are producing a D1+ analysis from scratch. No prior analysis exists for this concept.

### Required Reading

Read these files in this order before writing:

#### 1. Output Template (defines the section structure you must follow)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md`

#### 2. Analysis Brief (defines the purpose and quality expectations)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/concept_analysis_brief.md`

#### 3. Handwritten Exemplars (calibrate your depth and style against these)
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/01-hts-compact-tokamak.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/07-maglif.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/11-magnetic-mirror-comparison.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/11-magnetic-mirror.md`
- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/handwritten/26-laser-icf-indirect-drive.md`

Study the exemplars carefully. They show the expected level of technical depth, citation practice, and analytical rigor. Your output should match their quality. Note that exemplars may vary in structure — follow the output template for section structure, but match the exemplars for analytical depth and style.

#### 4. Phase 1a Dossier (structured research summary for this concept)
`/home/reid/1cfe/fusion-tea/knowledge/concept_research/16-muon-catalyzed-fusion/dossier.md`

The dossier contains per-column values with confidence ratings, citations, and notes from prior research iterations. This is your factual foundation.

#### 5. Extracted Source Documents (use subagents — see Per-Source Reading Pattern above)

Spawn one subagent per source document. For cold-start analysis, ask each subagent:
- What does this source tell us about the concept's cost structure and unique subsystems?
- What LCOE-relevant parameters or performance targets are stated?
- What cost advantages or penalties relative to conventional approaches are discussed?
- What technical risks, assumptions, or data gaps are mentioned?
- What materials, supply chain, or manufacturing considerations are relevant?

Sources to read via subagents:
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/16-muon-catalyzed-fusion/iter-01/sources/acceleron-arpa-e-presentation-2025.md` (7 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/16-muon-catalyzed-fusion/iter-01/sources/acceleron-company-overview.md` (3 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/16-muon-catalyzed-fusion/iter-01/sources/muon-catalyzed-fusion-physics.md` (39 KB)

#### 6. Schema (controlled vocabulary and column definitions)
`/home/reid/1cfe/fusion-tea/exploration/phase_1a/schema.md`

### Content Requirements
- Follow the output template section structure exactly (Sections 1-8)
- Do NOT include YAML frontmatter — the pipeline generates it automatically
- Every factual claim must cite a specific source (Phase 1a source document, dossier citation, or extracted document)
- Every quantitative value in Section 5 must have a Source and Confidence column entry
- Values without sources must be flagged as `[inferred]`, `[analogue]`, or `[estimated]` with reasoning

### Output

#### Step 1: Write the analysis body

Write the complete analysis to this file using the Write tool:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-1/analysis_body.md`

Write ONLY the analysis content (Sections 1-8). Do NOT include:
- YAML frontmatter (the pipeline adds it automatically)
- Preamble or commentary
- Code fences wrapping the document

Start the file with `# D1+ Analysis:` and end after Section 8.

#### Step 2: Update Reuses (if applicable)

If you referenced any approved prior analyses, update the Reuses field in:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/analysis.md`

The file already contains `Reuses: []`. Use the Edit tool to replace it with the concept IDs you referenced, e.g.:
`Reuses: [21-spherical-tokamak-hts, 28-hts-tokamak-full-hts]`

If you did not reference any approved analyses, leave Reuses unchanged.






## Output Template Structure

`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md` defines the 8 required sections. The analysis must follow this structure regardless of mode.

## Cross-Concept Reuse

- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

If approved prior analyses are available:
- Read all approved prior analyses listed above
- Identify shared subsystems, materials, cost structures, or physics
- Reuse consistent assumptions where appropriate — cite the source concept
- Note divergences in Section 7 (Cross-Concept Notes)
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics
