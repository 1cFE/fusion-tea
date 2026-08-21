# Spec: Explorer Identity & Shared Spine (Theme A)

**Status:** Implementation Complete (A1 + A2 + A3 all done; awaiting audit)
**Owner:** Reid W
**Created:** 2026-06-06 15:00 PDT
**Complexity:** MEDIUM
**Branch:** feat/concept-explorer-omit-list (Theme A work to branch separately)

---

## Work Item Summary

Theme A of the EXPLORER-UX-V3 Phase 2+ vision: the **identity & shared spine** — the cross-cutting infrastructure every later surface (the living ontology matrix B1, the rebranded constellation C1) depends on. It does three things: (A1) gives each concept **one canonical display name** of the form `Name (Fuel)` plus a clearly-shown concept **code (#)**, used identically on every surface; (A2) defines one shared **ontology facet + color vocabulary** (colors traceable to `concept_ontology_v3.png`) and applies the colors to the surfaces that exist today; (A3) replaces the quiet, inconsistent uncertainty markers with one **honest-caveat device** used everywhere a value appears. "Done" means a concept looks and is labeled the same wherever you meet it, the field's design vocabulary has one consistent color language, and missing/low-confidence data announces itself instead of hiding.

## Why This Matters Now

The matrix and constellation are both built on this spine, so it has to exist before they do — but it also fixes live problems on the pages that ship today. A single concept currently carries four-plus different name strings (dir slug, CSV-with-fuel, frontmatter-with-company, extracted-JSON-name, design-point plant name), and the code (#) is almost never visible to the user (URL, `<title>`, one muted compare label). Uncertainty is expressed today as a quiet ⚠ that's easy to miss and inconsistent across surfaces. Settling identity and the caveat treatment first means every later surface inherits one vocabulary instead of re-inventing it — and the epic's next-action note explicitly calls for resolving the canonical-name question before anything else.

## Key Bets / Constraints

- **Bet (A1):** the canonical name is **`Name (Fuel)`** for *all* concepts — fuel is part of identity; company is *not* (it stays a separate badge). One source of truth + one render helper makes the four-strings divergence structurally impossible to recur.
- **Bet (A2):** the filter *vocabulary and colors* are worth landing now even though the filter *widget* isn't — the colors are immediately visible on existing surfaces, and B1/C1 inherit a settled palette.
- **Constraint:** honest degradation is a hard rule — missing fields say so; they never silently vanish (carried from Phase 1).
- **Constraint:** the color vocabulary must be **traceable to `concept_ontology_v3.png`**, not invented ad hoc.
- **Non-goal:** building the ontology matrix, the constellation rebrand, or any working filter control. Theme A is the spine, not the maps.
- **Non-goal:** surfacing the design-point/plant name (that is Theme D2).

---

## Business Goals

### Why This Matters

A researcher or enthusiast should be able to recognize a concept instantly and identically wherever they meet it — landing, concept page, compare, constellation — and should be able to refer to it by a stable handle (the code) when the prose names are unreliable. Today they can't: the name shifts surface to surface, the code is hidden, and the tool's honesty about its own uncertainty is a marker most users never notice. Fixing this is both a usability win now and the precondition for the matrix/constellation later.

### Success Criteria

- [ ] The same concept shows the same `Name (Fuel)` label and the same `#NN` code on every surface it appears.
- [ ] A user can read a concept's code off the screen (not just the URL) and use it as a stable reference.
- [ ] The ontology design dimensions have one consistent color language, visibly applied on the surfaces that exist today.
- [ ] Wherever a value is low-confidence, single-source, archetype-fit-None, or not recorded, the UI says so in plain language — it never silently omits.

### Priority

P1, first item of Phase 2. Blocks B1 (matrix) and C1 (constellation rebrand), which consume A1/A2/A3. Independent of the remaining Phase-1 loose ends (Item 2-FU).

---

## Problem Statement

### Current State

- **Naming:** one concept carries four-plus name strings; the explorer renders inconsistent forms (fuel suffix dropped here, company added there, punctuation reformatted). The code (#) is rendered to the user in essentially one muted place (`comparison.js:548`) and the `<title>` tag; everywhere else only the name shows.
- **Color vocabulary:** the constellation colors points by confinement family (four hard-coded colors); family badges use their own colors; nothing ties either to the ontology dimensions or to `concept_ontology_v3.png`. There is no shared facet model.
- **Uncertainty:** expressed as a quiet ⚠ low-grounding marker on landing cards, with no consistent treatment on the concept page, compare, or constellation, and missing fields tend to vanish (whiskers disappear, sliders show "—") rather than announce absence.

### Desired Outcome

One canonical identity (name + code) and one design-vocabulary color language, applied consistently to every existing surface, plus one reusable caveat device that makes uncertainty and absence honest and visible everywhere. The facet/filter *model* is defined and the colors are live; the filter *widget* is left for B1.

---

## Scope

### In Scope

- **A1:** define the canonical name resolution (`Name (Fuel)`), a single source of truth for it, and one render helper returning `{ code, name }`; show the `#NN` code as a consistent visible handle and the `Name (Fuel)` label on every surface that names a concept (landing cards, concept hero + breadcrumb + sticky headline, compare columns/picker/placeholders, constellation nodes/hover, taxonomy card, neighbor tables, parameter-card links).
- **A2:** define the ontology facet set and a palette of color tokens traceable to `concept_ontology_v3.png`; apply the color tokens to existing surfaces (family badges, constellation point coloring); define the shared filter-state model that B1/C1 will consume.
- **A3:** one reusable caveat marker + plain-language hover copy, covering low-grounding, single-source, archetype-fit None, and field-not-recorded; applied across landing / concept / compare / constellation, replacing the current quiet ⚠.

### Out of Scope

- The living ontology matrix (B1), constellation rebrand/refocus (C1), parcats (B2).
- Any working **filter control / widget** and its application to a view — deferred to B1.
- Concept-page provenance/maturity depth, including the design-point/plant name (Theme D).
- Changing the underlying concept-analysis data files; Theme A reconciles at the explorer's data/render layer, not by editing `analysis.md` frontmatter or the CSV.

### Edge Cases & Considerations

- **Suffix variants** (`17a`, `17b`, `20a`, `20b`) keep their letter in the code (`#17a`) and resolve a distinct name each.
- **Concepts missing a fuel value** — the name needs a defined behavior (e.g. show base name without the `(Fuel)` parenthetical, honestly) rather than `(None)` or a fabricated fuel.
- **Fuel display form** — the structured fuel field is `DT/DD/DHe3/PB11`; the display form is `D-T / D-D / D-He3 / p-B11`. The canonical name needs one fuel→display mapping (design decides whether to reuse the CSV suffix or compose from the structured field).
- **Company** still appears where it does today, but as a separate badge — *not* inside the name.
- **Freeform / no-cost-model concepts** — must still get a canonical name + code and a caveat treatment, degrading honestly.
- **Two family notions disagree** — `ConfinementFamily` enum (MFE/IFE/MIF/NONSTANDARD; ARC is NONSTANDARD) vs. the richer ontology subfamily. A2's color vocabulary must pick which one its family color keys off; design to resolve.

---

## Requirement Selection Notes

The normative requirements below fix what we have actually decided: the canonical name *form*, the visible code, color *traceability* to the PNG, the facet model existing, and honest degradation. They deliberately do **not** fix: the fuel→display mapping mechanism, where exactly the source-of-truth field lives, the precise visual form of the code chip and caveat marker, or which family notion keys the color — those are design decisions. We are also deliberately *not* writing requirements for the filter widget, since it's out of scope for Theme A.

---

## Requirements

### Functional Requirements

> From the user's request unless marked [INFERRED].

**A1 — Canonical naming + visible code**

1. **FR-A1.1**: Every concept MUST have one canonical display name of the form `Name (Fuel)`, used identically on every surface that names it.
2. **FR-A1.2**: The concept **code** (`NN`, including letter suffixes like `17a`) MUST be shown to the user as a visible, consistent handle on every surface that names a concept — not only in the URL/title.
3. **FR-A1.3**: The company MUST NOT be part of the canonical name; where company is shown today it remains a separate element (e.g. a badge).
4. **FR-A1.4**: There MUST be a single source of truth for the canonical name and one shared render helper (returning code + name) that all surfaces use, so divergent name strings cannot recur.
5. **FR-A1.5** [INFERRED]: A concept with no fuel value MUST render an honest name (base name without a fabricated or `(None)` fuel), not an error or placeholder fuel.

**A2 — Shared facet + color vocabulary**

6. **FR-A2.1**: The ontology facet set MUST be defined as shared data (family, fuel, magnet, driver, capture, blanket, op-mode, rep-rate, plus fit-grade and has-cost-model), available for B1/C1 to consume.
7. **FR-A2.2**: A palette of color tokens for the design dimensions MUST be defined and MUST be traceable to `concept_ontology_v3.png` (documented mapping), not invented ad hoc.
8. **FR-A2.3**: The color tokens MUST be applied to the surfaces that exist today (at minimum family badges and constellation point coloring) so the vocabulary is visibly in use within Theme A.
9. **FR-A2.4**: A shared filter-state model MUST be defined for B1/C1 to consume. The filter *widget/control* is out of scope (deferred to B1).

**A3 — Honest-caveat device**

10. **FR-A3.1**: There MUST be one reusable caveat device (a consistent marker + plain-language hover) used identically across landing, concept, compare, and constellation.
11. **FR-A3.2**: The device MUST cover at least: low grounding, single-source, archetype-fit None, and field-not-recorded.
12. **FR-A3.3**: Where a field is absent or unrecorded, the UI MUST say so via the caveat device; it MUST NOT silently omit the field (no "silent vanish").

### Non-Functional Requirements

- The name/code render helper and caveat device SHOULD be shared components, not per-page reimplementations (the divergence this spec fixes came from per-surface rendering).

---

## Acceptance Criteria

### Core Functionality

- [ ] For ≥3 concepts spanning families (e.g. 01, 24, 17a), the `Name (Fuel)` label and `#NN` code are identical on landing, concept page, compare, and constellation. *(FR-A1.1–A1.4)*
- [ ] A concept lacking a fuel value renders an honest base name with no fabricated fuel. *(FR-A1.5)*
- [ ] Family badges and constellation points use the new color tokens, and the palette↔PNG mapping is documented. *(FR-A2.2–A2.3)*
- [ ] The facet set and filter-state model exist as shared, importable definitions with no filter widget required to use them. *(FR-A2.1, A2.4)*
- [ ] The same caveat device renders on landing, concept, compare, and constellation, and an absent field shows an explicit "not recorded" state rather than vanishing. *(FR-A3.1–A3.3)*

### Quality & Integration

- [ ] Existing test suite continues to pass.
- [ ] New test: the render helper returns the expected `{code, name}` for a normal concept, a suffix-variant (17a), and a fuel-missing concept.

---

## Next-Stage Handoff

**Settled in this spec:**
- Canonical name form is `Name (Fuel)` for all; company is excluded from the name.
- The code is a visible handle on every surface.
- Color tokens trace to `concept_ontology_v3.png`.
- Filter *widget* is out of scope; facet model + filter-state model + colors are in.
- Honest degradation is mandatory.

**Design must figure out:**
- Where the single source-of-truth name field lives and how it's populated (extractor field? render-time composition from base name + structured fuel?).
- The fuel→display mapping mechanism (`DT`→`D-T`, `PB11`→`p-B11`).
- The visual form of the `#NN` code handle and the caveat marker.
- Which family notion (`ConfinementFamily` enum vs. ontology subfamily) keys the family color, and the full dimension→color mapping from the PNG.
- The shape of the shared filter-state model (so it cleanly fits B1's matrix and C1's constellation).
- Whether A1/A2/A3 implement as one work item or split (the spec covers the theme; design may decompose).

**Watch-outs for design:**
- Suffix variants (17a/17b, 20a/20b) and fuel-missing concepts are the easy cases to get wrong.
- The PNG is an image — extracting an exact, documented palette from it is a small but real task (offered as investigation if design wants it).
- Don't let "apply colors to existing surfaces" (A2.3) quietly drift into building the matrix early.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` — "Phase 2+ Vision" section (Theme A definition).
- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md` (Tier 2 origin; note the economics-first framing was reversed).
- **Ontology image:** `.project/research/concept_ontology_v3.png` (color vocabulary source).
- **Design:** `.project/active/explorer-identity-spine/design.md` (to be created).

---

**Next Steps:** After approval, proceed to `/_my_design`.
