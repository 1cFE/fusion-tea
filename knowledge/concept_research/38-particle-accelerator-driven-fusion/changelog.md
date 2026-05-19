## Iteration 1 — 2026-05-17

### Changes
- Created dossier from scratch (no prior version).
- Confinement Family: (none) → `Other` (high)
- Confinement Concept: (none) → `Beam-target fusion` (high, free-text — not in schema vocabulary)
- Fuel: baseline `D-T` → `D-T` (high, confirmed)
- Primary Heating: (none) → `Electrostatic acceleration` (high; geometry caveat noted)
- Energy Capture: (none) → `Neutron applications` (high)
- Magnet Type: (none) → `N/A` (high)
- Blanket Config: (none) → `N/A (non-power)` (high; SHINE is the schema's canonical example)
- Operation Mode: baseline `Continuous` → `Steady-state` (high)
- Repetition Rate: (none) → `N/A` (high)
- Driver Technology: (none) → `Particle accelerator (beam-target)` (high; matches schema example row)
- New sources: SHINE corporate (shinefusion.com), Wikipedia, Piefer et al. ANL Mo-99 paper, NRC license documents, PR Newswire FLARE release, Science magazine profile.
- No conflicts discovered.

### Gap Assessment
- **Columns still incomplete**: None at the value level. Two schema-vocabulary mismatches flagged:
  - Confinement Concept: "Beam-target fusion" is not in the controlled list under `Other`.
  - Primary Heating: `Electrostatic acceleration` description implies IEC convergence geometry; SHINE is linear beam-on-gas.
- **Recommendation**: No further research iteration needed. Open a schema-review item to (a) add `Beam-target` under `Other` for Confinement Concept and (b) consider a new `Accelerator (beam-target)` value for Primary Heating.

## Iteration 2 — 2026-05-17

### Changes
- Overall confidence upgraded: `medium-high` → `high` (all columns at high cell confidence; remaining issues are schema-vocabulary, not research gaps).
- No column values changed — iteration 2 re-verified prior values against the schema.
- No new sources consulted.
- No conflicts discovered.

### Gap Assessment
- **Columns still incomplete**: None at the value level. Two flagged schema-vocabulary mismatches persist (Confinement Concept: `Beam-target fusion` not in controlled list; Primary Heating: `Electrostatic acceleration` description leans IEC-geometric).
- **Recommendation**: Stop iterating. Open a schema-review item to (a) add `Beam-target` under `Other` for Confinement Concept and (b) consider an `Accelerator (beam-target)` value for Primary Heating. Further iterations would not improve the differentiation table.
