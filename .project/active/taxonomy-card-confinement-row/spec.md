# Spec: Taxonomy Card — Confinement Row

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-04-12
**Complexity:** LOW
**Branch:** 13-16-17b

---

## Business Goals

### Why This Matters
The taxonomy card's attribute table shows design parameters (fuel, heating, magnets, etc.) but does not show the concept's confinement classification as a single readable field. The hierarchy is visible as badge chips, but a path-formatted row makes classification immediately legible at a glance alongside the other attributes.

### Success Criteria

- [ ] Each concept's taxonomy card shows its confinement hierarchy as a breadcrumb-style path
- [ ] Path is the first row in the attributes table

### Priority
Low complexity enhancement — small UI change, no data or backend work.

---

## Problem Statement

### Current State
The taxonomy card displays confinement hierarchy only as separate badge chips (e.g. `[MFE] [Tokamak] [Compact]`). There is no row in the attributes table that presents the full classification path.

### Desired Outcome
A "Confinement" row at the top of the attributes table showing the hierarchical path with `>` separators, e.g. "Inertial > Laser > Direct Drive".

---

## Scope

### In Scope
- New "Confinement" row in the taxonomy card attribute table
- Path assembled from existing fields in `concept_registry.json`
- Short family labels for the root level

### Out of Scope
- Changes to badge chips (remain as-is)
- Backend or data schema changes
- Changes to other views (cost model, tree view)

---

## Requirements

### Functional Requirements

1. **FR-1**: The taxonomy card MUST display a "Confinement" row as the first row in the attributes table (above "Fuel").
2. **FR-2**: The row value MUST be the hierarchical confinement path using ` > ` as separator.
3. **FR-3**: The path MUST be built from the concept's existing fields: `confinement_family` (level 1) → `mfe_topology` / `ife_driver` / `mif_method` / `non_standard_mechanism` (level 2) → `tokamak_shape` / `stellarator_type` / `laser_approach` (level 3).
4. **FR-4**: The root level MUST use short labels:
   - MFE → "Magnetic"
   - IFE → "Inertial"
   - MIF → "Magneto-Inertial"
   - NONSTANDARD → "Non-Standard"
5. **FR-5**: Levels 2 and 3 MUST use the field values as-is (they are already human-readable).
6. **FR-6**: If a level is null/absent, the path MUST stop at the last present level (e.g. "Non-Standard > Electrostatic" with no level 3).

---

## Acceptance Criteria

### Core Functionality
- [ ] "Confinement" row appears first in the attribute table for all concepts
- [ ] Path reads correctly for a 3-level concept (e.g. "Inertial > Laser > Direct Drive")
- [ ] Path reads correctly for a 2-level concept (e.g. "Non-Standard > Electrostatic")
- [ ] Path reads correctly for a 1-level concept (if any exist — just the short family label)
- [ ] Existing rows (Fuel, Heating, etc.) are unaffected and appear after Confinement

---

## Related Artifacts

- **Key file:** `exploration/concept_explorer/static/js/taxonomy_card.js` (lines 22-32 for `ATTR_DISPLAY`, card rendering logic)
- **Data:** `exploration/concept_explorer/data/concept_registry.json`
- **Design:** `.project/active/taxonomy-card-confinement-row/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
