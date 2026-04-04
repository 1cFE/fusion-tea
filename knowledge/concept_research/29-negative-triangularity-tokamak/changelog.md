# Changelog: Negative Triangularity Tokamak (D-T)

## Iteration 1 — 2026-03-06

### Changes
- **Confinement Family**: New value `MFE` (high confidence) — confirmed by all sources
- **Confinement Concept**: New value `Negative triangularity tokamak` (high confidence) — confirmed by all sources
- **Fuel**: New value `D-T` (high confidence) — from baseline CSV, consistent with target Q and device parameters
- **Primary Heating**: New value `RF (ECRH)` (medium confidence) — inferred from "microwaves" in Venture Kick profile; ohmic-only alternative noted from Ball et al. paper
- **Energy Capture**: New value `Thermal (unspecified)` (medium confidence) — default for D-T concept with no disclosed approach
- **Plasma State**: New value `Burning` (medium confidence) — Q>5 target, company uses "burning plasma" language
- **Magnet Type**: New value `HTS (wound)` (high confidence) — commercial target; copper for LUCIOLE prototype
- **Tritium Breeding**: Set to `TBD` (low confidence) — no information in any source
- **Neutron Management**: New value `Heavy shielding (14 MeV)` (low confidence) — inferred from D-T fuel
- **Operation Mode**: New value `Steady-state` (medium confidence) — from baseline CSV "Continuous"; noted conflict with pulsed MANTA reference design
- **Repetition Rate**: New value `N/A` (medium confidence) — follows from Steady-state
- **Driver Technology**: New value `HTS magnets + NT plasma shaping` (medium confidence)
- **New sources**: 5 sources saved to `iter-01/sources/`

### Gap Assessment
- **Columns still incomplete**: Tritium Breeding (TBD), Neutron Management (low), Energy Capture (medium/default), Primary Heating (medium/ambiguous), Operation Mode (medium/conflicting)
- **Recommendation**: Another iteration is warranted. Target queries: (1) MANTA reference design papers (Rutherford et al.) for operation mode and heating details, (2) Firefly conference presentations or FIA profile for blanket/energy capture, (3) any new Firefly preprints on arXiv. The operation mode conflict (steady-state vs. pulsed) is the most important gap to resolve.

## Iteration 2 — 2026-03-06

### Changes
- **Neutron Management**: `Heavy shielding (14 MeV)` (low) → `Integrated blanket/shield` (low) — MANTA reference design uses FLiBe blanket serving dual breeder/shield function
- **Primary Heating**: Kept `RF (ECRH)` (medium) but added ICRH and ohmic-only as competing hypotheses in Notes — MANTA uses ICRF (40 MW, 110 MHz), not ECRH
- **Operation Mode**: Kept `Steady-state` (medium) but strengthened conflict notes — MANTA is pulsed (~15 min), Ball's ohmic-only research implies inductive/pulsed
- **Tritium Breeding**: Still `TBD` but added MANTA FLiBe proxy (TBR 1.15) in Notes
- **Plasma State**: Added MANTA Q=11.5 as supporting evidence for Burning classification
- **Magnet Type**: Added MANTA REBCO HTS confirmation in Notes
- **Summary**: Expanded with MANTA context and early-stage caveat
- **New sources**: 2 sources saved to `iter-02/sources/` (MANTA reference design, Firefly website)

### Gap Assessment
- **Columns still incomplete**: Primary Heating (medium but three competing hypotheses), Energy Capture (medium/default), Tritium Breeding (TBD), Neutron Management (low/proxy), Operation Mode (medium but strong counter-evidence)
- **Recommendation**: Further iterations are unlikely to resolve gaps without new Firefly publications or conference presentations. The company is very early-stage (founded 2024) and its website discloses no reactor parameters. If a third iteration is run, target: (1) APS-DPP or IAEA FEC proceedings for any Firefly presentations, (2) new arXiv preprints from Ball/Ospanov, (3) FIA member database updates. The operation mode conflict remains the most important unresolved question.

## Iteration 3 — 2026-03-06

### Changes
- **No column values changed** — iter-03 found no new Firefly-specific technical information
- Firefly joined the Impulse deep-tech incubator near ITER/CEA Cadarache (LinkedIn post, business announcement only — no technical content)
- A patent search found US application 20250266176 ("spherical tokamak + NT + HTS") but this appears to be from a different company (describes spherical tokamak, not Firefly's compact tokamak)

### Gap Assessment
- **Columns still incomplete**: Primary Heating (medium, three competing hypotheses), Energy Capture (medium/default), Tritium Breeding (TBD), Neutron Management (low/proxy), Operation Mode (medium, strong counter-evidence for pulsed)
- **Recommendation**: Mark concept as research-complete at current confidence levels. Three iterations have been run with diminishing returns — the remaining gaps are structural (company hasn't disclosed, and likely hasn't yet determined, blanket/shielding/heating design). No further iterations recommended unless new Firefly publications emerge.
