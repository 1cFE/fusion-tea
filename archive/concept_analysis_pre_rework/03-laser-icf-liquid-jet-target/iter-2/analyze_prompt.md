# D1+ Concept Analysis: Laser ICF - Liquid Jet Target (D-D)

You are producing a D1+ analysis for the fusion concept **Laser ICF - Liquid Jet Target (D-D)** (Cortex Fusion).

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

## FLiBe Coolant Cost Data Is Consistently Sparse
Date: 2026-03-29 | Concepts: 09, 14, 22, IFE

IFE concepts using FLiBe as primary coolant/breeder consistently lack
cost data for coolant inventory and processing. Flag as [estimated] with
high uncertainty. The HYLIFE-II report (Moir 1994) is the only source
with FLiBe cost estimates but uses 1994 dollars.

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

## Concept Landscape (39 concepts)

Use this catalog for nearest-neighbor identification and cross-concept positioning.
Approved concepts have full analyses available; I{N} indicates N completed iterations.

### Approved (primary cross-reference pool)

| ID | Concept Name | Company | Confinement Family | MFE Topology | IFE Driver | MIF Method | Non-Standard Mechanism | Tokamak Shape | Stellarator Type | Laser Approach | Fuel | Primary Heating | Heating Type | Energy Capture | Magnet Type | Blanket Config | Operation Mode | Repetition Rate | Driver Technology | Driver Type | Overall Confidence | Iterations | Extracted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 21-spherical-tokamak-hts | Spherical Tokamak - HTS (D-T) | Tokamak Energy | MFE | Tokamak | N/A | N/A | N/A | Spherical | N/A | N/A | D-T | RF (ECRH) | ECRH | Thermal (unspecified) | HTS (wound) | Liquid metal | Quasi-steady | N/A | HTS magnets (REBCO, 5.25 T on-axis) | Magnetic | medium | iter-2/FAIL (3 findings) | E* |

### In Progress (by maturity)

| ID | Concept Name | Company | Confinement Family | MFE Topology | IFE Driver | MIF Method | Non-Standard Mechanism | Tokamak Shape | Stellarator Type | Laser Approach | Fuel | Primary Heating | Heating Type | Energy Capture | Magnet Type | Blanket Config | Operation Mode | Repetition Rate | Driver Technology | Driver Type | Overall Confidence | Iterations | Extracted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 07-maglif | MagLIF (D-T) | Pacific Fusion | MIF | N/A | N/A | Magnetized target | N/A | N/A | N/A | N/A | D-T | Pulsed power implosion | N/A (compression-driven) | Thermal (unspecified) | None | TBD | Pulsed | Sub-Hz | Pulsed power (Z-machine class) | Magnetic pinch | medium-high | iter-11/FAIL (3 findings) | E* |
| 09-qi-stellarator-hts | QI Stellarator - HTS (D-T) | Proxima Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | QI | N/A | D-T | RF (ECRH) | ECRH | Thermal (unspecified) | HTS (3D stellarator) | Liquid metal | Steady-state | N/A | 3D HTS stellarator coils (REBCO, 20 T) | Magnetic | medium | iter-9/FAIL (3 findings) | E |
| 01-hts-compact-tokamak | HTS Compact Tokamak (D-T) | Commonwealth Fusion Systems | MFE | Tokamak | N/A | N/A | N/A | Compact | N/A | N/A | D-T | RF (ICRH) | ICRH | Thermal (steam) | HTS (wound) | Molten salt | Quasi-steady | N/A | HTS magnets (REBCO, 20 T) | Magnetic | high | iter-8/FAIL (3 findings) | E* |
| 17a-laser-icf-hybrid-drive | Laser ICF - Hybrid Direct Drive (D-T) | Xcimer Energy | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Hybrid drive | D-T | Laser (direct drive) | N/A (compression-driven) | Thermal (unspecified) | N/A | Molten salt | Pulsed | Sub-Hz | Excimer laser (KrF, 248 nm, 10+ MJ, ASPEN architecture) | Gas Laser | medium-high | iter-7/FAIL (3 findings) | E* |
| 02-acoustic-icf-sonofusion | Acoustic ICF / Sonofusion (D-D) | Sonofusion Energy | IFE | N/A | Acoustic | N/A | N/A | N/A | N/A | N/A | D-D | Acoustic implosion | N/A (non-thermal) | TBD | N/A | N/A | Pulsed | kHz | Ultrasonic transducers (acoustic cavitation) | Other | low | iter-6/FAIL (3 findings) | E |
| 13-electrostatic-hybrid | Electrostatic Hybrid (D-T) | Avalanche Energy | Non-Standard | N/A | N/A | N/A | Electrostatic | N/A | N/A | N/A | D-T | Electrostatic acceleration | N/A (non-thermal) | Thermal (unspecified) | Electrostatic | TBD | Steady-state | N/A | High-voltage electrostatic cathode (300 kV) with E×B electron co-confinement | Electrostatic | medium-low | iter-5/FAIL (3 findings) | E |
| 19-orbital-levitated-dipole | Orbital Levitated Dipole (D-He3) | Zephyr Fusion | MFE | Dipole | N/A | N/A | N/A | N/A | N/A | N/A | D-He3 | RF (ECRH) | ECRH | Direct (charged particle) | HTS (levitated dipole) | N/A | Steady-state | N/A | Orbital HTS dipole coil (meter-scale, Falcon 9 deployable) | Magnetic | low | iter-5/FAIL (3 findings) | E |
| 20a-type-one-stellarator | Type One Stellarator (D-T) | Type One Energy | MFE | Stellarator | N/A | N/A | N/A | N/A | Modular | N/A | D-T | RF (ECRH) | ECRH | Thermal (steam) | HTS (3D stellarator) | Solid breeder | Steady-state | N/A | Modular HTS stellarator coils (REBCO, 9 T) | Magnetic | high | iter-5/FAIL (3 findings) | E* |
| 22-projectile-icf | Projectile ICF (D-T) | First Light Fusion | IFE | N/A | Projectile | N/A | N/A | N/A | N/A | N/A | D-T | Projectile impact | N/A (compression-driven) | Thermal (steam) | N/A | Liquid metal | Pulsed | Sub-Hz | Electromagnetic gun | Mechanical/kinetic | medium-high | iter-5/PASS | E |
| 28-hts-tokamak-full-hts | HTS Tokamak - Full HTS (D-T) | Energy Singularity | MFE | Tokamak | N/A | N/A | N/A | Compact | N/A | N/A | D-T | RF (ICRH) | ICRH | Thermal (unspecified) | HTS (wound) | TBD | Steady-state | N/A | HTS magnets (REBCO, 25 T) | Magnetic | medium | iter-5/FAIL (3 findings) | E* |
| 08-frc-w-direct-conversion | FRC w/ Direct Conversion (D-He3) | Helion Energy | MIF | N/A | N/A | FRC compression | N/A | N/A | N/A | N/A | D-He3 | Magnetic compression | N/A (compression-driven) | Direct (inductive) | Resistive | Other/hybrid | Pulsed | ~1 Hz | Pulsed EM coils (capacitor bank) | Magnetic | high | iter-4/FAIL (3 findings) | E |
| 12-levitated-dipole | Levitated Dipole (D-T) | OpenStar Technologies | MFE | Dipole | N/A | N/A | N/A | N/A | N/A | N/A | D-T | RF (ICRH) | ICRH | Thermal (unspecified) | HTS (levitated dipole) | Solid breeder | Quasi-steady | N/A | Levitated HTS dipole coil (REBCO, 23 T) with on-board flux pump | Magnetic | high | iter-4/FAIL (3 findings) | E |
| 14-magnetized-target-fusion-pneumatic-compression | Magnetized Target Fusion - Pneumatic Compression (D-T) | General Fusion | MIF | N/A | N/A | Magnetized target | N/A | N/A | N/A | N/A | D-T | Mechanical compression | N/A (compression-driven) | Thermal (steam) | None | Liquid metal | Pulsed | ~1 Hz | Pneumatic pistons + liquid metal | Mechanical/kinetic | high | iter-4/FAIL (3 findings) | E* |
| 25-heavy-ion-beam-icf | Heavy Ion Beam ICF (D-T) | Intensity Energy | IFE | N/A | Heavy ion beam | N/A | N/A | N/A | N/A | N/A | D-T | Heavy ion beam | N/A (compression-driven) | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | Linear induction accelerator | Ion/particle beam | medium | iter-4/FAIL (3 findings) | E* |
| 29-negative-triangularity-tokamak | Negative Triangularity Tokamak (D-T) | Firefly Fusion | MFE | Tokamak | N/A | N/A | N/A | Negative triangularity | N/A | N/A | D-T | RF (ECRH) | ECRH | Thermal (unspecified) | HTS (wound) | TBD | Quasi-steady | N/A | HTS magnets + NT plasma shaping | Magnetic | medium | iter-4/FAIL (3 findings) | E* |
| 30-laser-icf-nif-commercialization | Laser ICF - NIF Commercialization (D-T) | Inertia Enterprises | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Indirect drive | D-T | Laser (indirect drive) | N/A (compression-driven) | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | Diode-pumped solid-state laser (DPSSL, 10 MJ, ~1000 beamlines) | DPSSL Laser | medium-high | iter-4/FAIL (3 findings) | E* |
| 33-state-backed-tokamak-best | State-Backed Tokamak - BEST (D-T) | Neo Fusion | MFE | Tokamak | N/A | N/A | N/A | Standard | N/A | N/A | D-T | RF + NBI | ICRH + ECRH + NBI | Thermal (unspecified) | LTS+HTS | TBD | Quasi-steady | N/A | LTS+HTS magnets (Nb3Sn/YBCO, 6.15T) + multi-method H&CD (50 MW) | Magnetic | medium | iter-4/FAIL (3 findings) | E* |
| 35-polomac-magnetic-confinement | PoloMac Magnetic Confinement | Deutelio | MFE | Dipole | N/A | N/A | N/A | N/A | N/A | N/A | D-D | Unknown | TBD | Thermal (unspecified) | Resistive | N/A | Steady-state | N/A | Internal dipole coil with magnetic tunnel supports | TBD | medium-low | iter-4/FAIL (3 findings) | E |
| 36-helical-coil-stellarator | Helical Coil Stellarator (D-T) | Helical Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | Helical coil | N/A | D-T | RF (ECRH) | ECRH | Thermal (sCO2) | HTS (3D stellarator) | Liquid metal | Steady-state | N/A | Continuous helical HTS coils (REBCO WISE conductor, 8 T) + 250 GHz CW gyrotrons | Magnetic | high | iter-4/FAIL (3 findings) | E* |
| 10-large-scale-stellarator | Large-Scale Stellarator (D-T) | Gauss Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | QI | N/A | D-T | RF (ECRH) | ECRH | Thermal (unspecified) | LTS+HTS | Liquid metal | Steady-state | N/A | Non-planar modular SC coils (LTS+HTS, 40 coils, 6T axis / 12-13T peak, demountable) | Magnetic | medium | iter-3/FAIL (3 findings) | E |
| 15-sheared-flow-stabilized-z-pinch | Sheared-Flow Stabilized Z-Pinch (D-T) | Zap Energy | MFE | Open/Linear | N/A | N/A | N/A | N/A | N/A | N/A | D-T | Ohmic (self-pinch) | Ohmic | Thermal (steam) | None | Liquid metal | Pulsed | ~10 Hz | Pulsed power (sheared-flow Z-pinch) | Magnetic pinch | high | iter-3/FAIL (3 findings) | E |
| 16-muon-catalyzed-fusion | Muon-Catalyzed Fusion (D-T) | Acceleron Fusion | Non-Standard | N/A | N/A | N/A | Muon-catalyzed | N/A | N/A | N/A | D-T | Muon catalysis | N/A (non-thermal) | Thermal (unspecified) | N/A | TBD | Steady-state | N/A | Muon source (accelerator) | Other | medium | iter-3/FAIL (3 findings) | E |
| 17b-laser-icf-fast-ignition | Laser ICF - Direct Drive Fast Ignition (D-T) | Focused Energy | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Fast ignition | D-T | Laser (fast ignition) | N/A (compression-driven) | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | DPSSL (Nd:glass, 527 nm) + petawatt CPA ignition laser | DPSSL Laser | medium | iter-3/FAIL (3 findings) | E |
| 18-p-b11-frc | p-B11 FRC (p-B11) | TAE Technologies | MFE | Compact Toroid | N/A | N/A | N/A | N/A | N/A | N/A | p-B11 | NBI | NBI | Thermal (steam) | Resistive | N/A | Steady-state | N/A | Neutral beam injection (high-energy, tangential) | Magnetic | high | iter-3/FAIL (3 findings) | E |
| 20b-renaissance-stellarator | Renaissance Stellarator (D-T) | Renaissance Fusion | MFE | Stellarator | N/A | N/A | N/A | N/A | Modular | N/A | D-T | NBI | NBI | Thermal (sCO2) | HTS (3D stellarator) | Other/hybrid | Steady-state | N/A | Laser-patterned HTS film on cylinders (REBCO, 10-15 T) | Magnetic | high | iter-3/FAIL (3 findings) | E |
| 23-laser-icf-nanostructured-target | Laser ICF - Nanostructured Target (p-B11) | Marvel Fusion | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Ultrashort pulse | p-B11 | Laser (ultrashort pulse) | N/A (compression-driven) | Hybrid (thermal + direct) | N/A | N/A | Pulsed | ~10 Hz | Femtosecond DPSSL + nanostructured Si targets (nanowire arrays, semiconductor lithography) | DPSSL Laser | medium-high | iter-3/FAIL (9 findings) | E |
| 24-dense-plasma-focus | Dense Plasma Focus (p-B11) | LPPFusion | Non-Standard | N/A | N/A | N/A | Plasma focus | N/A | N/A | N/A | p-B11 | Electromagnetic pinch (DPF) | Ohmic | Direct (charged particle) | None | N/A | Pulsed | High (>10 Hz) | Pulsed coaxial electrodes (capacitor bank, 2.7 MA) | Magnetic pinch | medium | iter-3/FAIL (3 findings) | E |
| 26-laser-icf-indirect-drive | Laser ICF - Indirect Drive (D-T) | Inertia Enterprises | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Indirect drive | D-T | Laser (indirect drive) | N/A (compression-driven) | Thermal (steam) | N/A | Liquid metal | Pulsed | ~10 Hz | DPSSL (Thunderwall, 10 kJ x 1000+ beamlines, 10 Hz, 3w UV) | DPSSL Laser | medium-high | iter-3/FAIL (3 findings) | E |
| 27-polywell | Polywell (D-T) | EMC2 | Non-Standard | N/A | N/A | N/A | Electrostatic | N/A | N/A | N/A | D-T | Electrostatic acceleration | N/A (non-thermal) | Thermal (unspecified) | Resistive | TBD | Steady-state | N/A | Polyhedral magnetic cusp coils + electron beam injection | Electrostatic | medium | iter-3/FAIL (3 findings) | E |
| 31-laser-icf-oec-architecture | Laser ICF - OEC Architecture (D-T) | Blue Laser Fusion | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Direct drive | D-T | Laser (direct drive) | N/A (compression-driven) | Hybrid (thermal + direct) | N/A | Liquid metal | Pulsed | ~10 Hz | CBC fiber laser + OEC, 5 MJ UV | DPSSL Laser | medium-high | iter-3/FAIL (3 findings) | E |
| 32-laser-icf-french-national | Laser ICF - French National (D-T) | GenF Systems | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Direct drive | D-T | Laser (direct drive) | N/A (compression-driven) | Thermal (unspecified) | N/A | Liquid metal | Pulsed | ~10 Hz | Diode-pumped solid-state laser (DPSSL) | DPSSL Laser | medium | iter-3/FAIL (3 findings) | E |
| 06-magnetic-mirror | Magnetic Mirror (p-B11) | Pale Blue | MFE | Open/Linear | N/A | N/A | N/A | N/A | N/A | N/A | p-B11 | RF (ICRH) | ICRH | Direct (charged particle) | TBD | N/A | Steady-state | N/A | Centrifugal mirror with alpha channeling (RF waves, E×B rotation, ponderomotive barriers) | Magnetic | medium | iter-2/FAIL (3 findings) | E* |
| 04-laser-icf | Laser ICF (p-B11) | hb11 | IFE | N/A | Laser | N/A | N/A | N/A | N/A | Fast ignition | p-B11 | Laser (fast ignition) | N/A (compression-driven) | Thermal (steam) | N/A | N/A | Pulsed | ~1 Hz | Petawatt ps CPA laser + laser-driven kT field | DPSSL Laser | medium | iter-1/INTERRUPTED | E |
| 05-planar-coil-stellarator | Planar Coil Stellarator (D-T) | Thea Energy | MFE | Stellarator | N/A | N/A | N/A | N/A | Planar coil | N/A | D-T | RF (ECRH) | ECRH | Thermal (steam) | HTS (planar array) | Liquid metal | Steady-state | N/A | Planar HTS coil array (12 encircling + 324 shaping, 20 T, software-controlled) | Magnetic | high | iter-1/INTERRUPTED | E |
| 11-magnetic-mirror | Magnetic Mirror (D-T) | Realta Fusion | MFE | Open/Linear | N/A | N/A | N/A | N/A | N/A | N/A | D-T | RF + NBI | ICRH + NBI | Hybrid (thermal + direct) | HTS (wound) | Liquid metal | Steady-state | N/A | HTS mirror magnets (REBCO, 17+ T) + NBI + ECH | Magnetic | medium-high | iter-1/INTERRUPTED | E |

### Not Started

| ID | Concept Name | Company | Confinement Family | MFE Topology | IFE Driver | MIF Method | Non-Standard Mechanism | Tokamak Shape | Stellarator Type | Laser Approach | Fuel | Primary Heating | Heating Type | Energy Capture | Magnet Type | Blanket Config | Operation Mode | Repetition Rate | Driver Technology | Driver Type | Overall Confidence | Extracted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 37-magnetized-target-inertial-fusion-mtif | Magnetized Target Inertial Fusion - MTIF (D-D) | NearStar Fusion | MIF |  |  | Magnetized target |  |  |  |  | D-D | Mechanical compression | N/A (compression-driven) | Thermal (unspecified) | None | TBD | Pulsed | Unknown | Plasma armature railgun (~10 km/s into magnetized D-D targets) | Mechanical/kinetic | medium |  |
| 38-particle-accelerator-driven-fusion | Particle Accelerator-Driven Fusion (D-T) | SHINE Technologies | Non-Standard |  |  |  | Electrostatic |  |  |  | D-T | Electrostatic acceleration | N/A (non-thermal) | N/A | None | N/A (non-power) | Steady-state | N/A | High-current particle accelerator (beam-on-target neutron source) | Ion/particle beam | medium-high |  |
| 39-spherical-tokamak-cs-free-p-b11 | Spherical Tokamak - CS-free p-B11 (p-B11) | ENN Energy | MFE | Tokamak |  |  |  | Spherical |  |  | p-B11 | RF (ECRH) | ECRH | Direct (charged particle) | HTS (wound) | N/A (no tritium) | Quasi-steady | N/A | CS-free spherical tokamak with ECRH non-inductive current drive (EXL-50U / EHL-2) | Magnetic | medium |  |





## Mode: Feedback Pass

You are improving an existing analysis based on specific feedback from the assessment agent.

### Existing Analysis
Read this file completely first:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/analysis.md`

### Feedback to Address
Then read the feedback:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/iter-2/pre_feedback.md`

The feedback contains specific findings (F-1, F-2, etc.) with targets, findings, and recommendations. Address each finding.

Findings marked `Category: model` primarily target the model code (sensitivity
sweeps, scenarios, parameters in model_setup.py). You should still update
analysis prose where relevant (e.g., Section 5 parameter tables, modeling
approach descriptions) to support the model change, but do NOT try to resolve
model findings solely through narrative rewording — the model-setup agent
will receive these findings directly.

If the feedback contains a "Carried-Forward Assessment Findings" section,
those are unresolved findings from the prior assessment that were preserved
across a source-integration pass. Treat them with the same priority as
regular findings — they represent issues the assessment flagged that you
haven't yet had a chance to address.

### Source Documents (use subagents for targeted evidence gathering)

For each finding in the feedback, spawn subagents to gather targeted evidence from the relevant sources. Ask questions specific to the feedback — e.g., if the feedback says "missing cost implication for direct energy conversion", ask subagents: "Does this source contain evidence about direct energy conversion costs, BOP impact, or conversion efficiency?"

Sources available for subagent queries:
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/arxiv-2308-levitt-quantum-control.md` (49 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/arxiv-2503-nanoshell-paper.md` (46 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/cortex-fusion-website.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/03-laser-icf-liquid-jet-target/iter-01/sources/kHz-liquid-sheet-fusion-paper.md` (50 KB)

Dossier (read directly — it's structured and short):
`/home/reid/1cfe/fusion-tea/knowledge/concept_research/03-laser-icf-liquid-jet-target/dossier.md`

### Instructions
1. Read the existing analysis completely
2. Read the feedback — it contains specific findings to address
3. For each finding, use the per-source subagent pattern to gather targeted evidence from the sources
4. Use the Edit tool to make targeted improvements to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/analysis.md`
5. Do NOT rewrite sections that aren't addressed by the feedback
6. Maintain all existing citations — only add/modify what the feedback requires
7. If a finding recommends adding parameter rows, add them in the correct table position with Source and Confidence columns
8. After making edits, re-read the modified sections to verify coherence




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
