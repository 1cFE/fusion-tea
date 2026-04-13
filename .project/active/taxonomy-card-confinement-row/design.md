# Design: Taxonomy Card — Confinement Row

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-04-12
**Branch:** 13-16-17b

---

## Overview

Add a "Confinement" row as the first attribute row in the taxonomy card, showing the concept's confinement hierarchy as a `>` separated path (e.g. "Inertial > Laser > Direct Drive").

## Related Artifacts

- **Spec:** `.project/active/taxonomy-card-confinement-row/spec.md`

---

## Research Findings

Single file change in `exploration/concept_explorer/static/js/taxonomy_card.js`.

**Current rendering flow** (`renderTaxonomyCard`, line 76):
1. Header (name, company, hierarchy badges) — lines 81-87
2. Attribute rows loop over `ATTR_DISPLAY` array — lines 90-108
3. Driver technology — lines 112-117
4. Cost model link — lines 119-126
5. Confidence — lines 129-134

The attribute row loop (lines 91-108) already handles null/TBD/normal values with appropriate styling. The confinement row can use this same rendering path by being the first entry in the loop.

**Hierarchy fields** (from `buildHierarchyBadges`, lines 51-71):
- Level 1: `concept.confinement_family` — always present
- Level 2: `concept.mfe_topology || concept.ife_driver || concept.mif_method || concept.non_standard_mechanism`
- Level 3: `concept.tokamak_shape || concept.stellarator_type || concept.laser_approach`

---

## Proposed Design

**Approach:** Add a `buildConfinementPath(concept)` helper that returns the path string. Render it as a synthetic first row before the `ATTR_DISPLAY` loop, using the same row markup.

**`buildConfinementPath(concept)`** (new helper, ~15 lines):
```
FAMILY_LABELS = { MFE: "Magnetic", IFE: "Inertial", MIF: "Magneto-Inertial", NONSTANDARD: "Non-Standard" }

parts = [ FAMILY_LABELS[concept.confinement_family] || concept.confinement_family ]
level2 = concept.mfe_topology || concept.ife_driver || concept.mif_method || concept.non_standard_mechanism
if level2: parts.push(level2)
level3 = concept.tokamak_shape || concept.stellarator_type || concept.laser_approach
if level3: parts.push(level3)
return parts.join(" > ")
```

**Integration point:** In `renderTaxonomyCard` (line 90), after creating the `attrs` div and before the `ATTR_DISPLAY` loop, insert a single confinement row using the same `taxonomy-card__attr` / `taxonomy-card__label` / `taxonomy-card__value` markup.

No changes to `ATTR_DISPLAY`, `buildHierarchyBadges`, comparison logic, or any other function.

---

## Validation Approach

- Visual check: open taxonomy view, click concepts from each confinement family
- Verify 3-level (e.g. HTS Compact Tokamak → "Magnetic > Tokamak > Compact")
- Verify 2-level (e.g. Polywell → "Non-Standard > Electrostatic")
- Verify existing rows unchanged

---

**Next Step:** After approval → `/_my_implement`
