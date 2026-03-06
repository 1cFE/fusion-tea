# Implementation Plan: Visualization & Demo Completion

**Status:** Complete
**Created:** 2026-03-03
**Last Updated:** 2026-03-03

## Source Documents
- **Spec:** `.project/active/visualization-demo/spec.md`
- **Design:** `.project/active/visualization-demo/design.md` — See here for component details, CSS vocabulary, model structure, narrative guidance

## Implementation Strategy

**Phasing Rationale:**
SVG artifacts first (Phase 1) because they're the riskiest — Graphviz styling requires iteration, and the SVGs must look good before embedding. HTML content second (Phase 2) because it's straightforward once the visual assets exist. Polish last (Phase 3) because narrative coherence and accuracy require seeing the full section assembled.

**Validation Approach:**
No traditional test suite — this is HTML content + SVG generation. Validation is:
- SVG renders correctly (Phase 1)
- HTML renders in browser, images load (Phase 2)
- Narrative flows, values are accurate, responsive layout works (Phase 3)

---

## Phase 1: Generate & Style SVG Artifacts

### Goal
Produce two presentation-quality SVGs: structural containment view (from extraction CLI) and calculation data flow (hand-authored DOT). De-risks the visual foundation before touching the demo HTML.

### Changes Required

#### 1. Structural View SVG
**Pipeline:** `uv run python -m proof_of_concept.extraction models/ --format dot | dot -Tsvg`

- [x] Run the extraction CLI → DOT pipeline and inspect raw output
- [x] Evaluate whether default DOT styling is acceptable or needs enhancement
- [x] If styling needed: create a wrapper that post-processes the DOT with custom attributes:
  - Font: `fontname="system-ui, sans-serif"` (matches demo)
  - Colors: use demo palette (`#2563eb` accent, `#059669` artifact, `#7c3aed` process)
  - Node shapes: rounded boxes for parts, distinct shape for the root
  - Subgraph (compound node) styling: fill colors to distinguish nesting levels
- [x] Render final SVG: `dot -Tsvg -o demo/images/structural-view-hif.svg`
- [x] Verify SVG opens correctly in browser and looks good at various widths

#### 2. Calc Flow SVG
**Source:** Hand-authored DOT file based on `design.md#sysml-calc-flow`

- [x] Author DOT file for the calc flow diagram with three visual clusters:
  - **Inputs** (left): parameter nodes grouped by subsystem (driver / chamber / plant / target), colored by source
  - **Calculations** (center): calc def nodes (IFE LCOE, Recirculating Power Fraction, Meier Driver Cost, Meier Reactor Cost, Meier COE)
  - **Outputs** (right): result nodes (lcoe $/MWh, recirculating_fraction, meier_coe cents/kWh)
  - Edges from parameters → calc inputs → outputs
  - Include concrete Osiris values as node labels where space permits
- [x] Style with same palette as structural view (consistent visual language)
- [x] Render: `dot -Tsvg -o demo/images/calc-flow-hif.svg`
- [x] Verify SVG renders correctly, is readable, not too cluttered

### Validation

- [x] Both SVGs open in browser tab (direct file open)
- [x] Both SVGs render at reasonable size (not tiny, not enormous)
- [x] Colors are visually consistent between the two diagrams
- [x] Structural view shows all 7 nodes with correct containment nesting
- [x] Calc flow shows both Hawker and Meier chains with parameter sources

**What We Know Works After This Phase:**
Both SVG artifacts exist, look presentable, and are ready to embed in the demo HTML.

---

## Phase 2: Build Section 8 HTML

### Goal
Replace the Section 8 stub in `demo/index.html` with the three views (structural, calc flow, def-vs-usage) plus framing narrative. Update sidebar navigation.

### Changes Required

**See `design.md#proposed-design` for:** Section structure, HTML patterns, narrative guidance, CSS classes to use.

**Single file:** `demo/index.html`

#### 1. Sidebar Navigation
- [x] Change Section 8 nav entry: remove `.stub` class and badge, update href to `#visualization`, update text to "Visualization"

#### 2. Section 8 Header & Opening
- [x] Replace `<section id="cross-concept">` with `<section id="visualization">`
- [x] Replace section title from "Cross-Concept Comparison" to "Visualization & Analysis"
- [x] Remove stub banner (`<div class="stub-banner">`)
- [x] Remove stub content container (`<div class="stub-content">`)
- [x] Write opening paragraph per `design.md#section-8-narrative-flow`

#### 3. Structural View Subsection (R1)
- [x] `<h3>` heading
- [x] SVG image in `.card` container: `<img src="images/structural-view-hif.svg">`
- [x] Terminal block showing the extraction CLI → DOT → SVG pipeline command
- [x] Callout about interactive web viewer (`uv run python -m proof_of_concept.web`)

#### 4. Calculation Flow Subsection (R2)
- [x] `<h3>` heading
- [x] SVG image in `.card` container: `<img src="images/calc-flow-hif.svg">`
- [x] Brief explanation of dual chains (Hawker LCOE vs. Meier COE for cross-validation)
- [x] Expandable `<details>` with parameter table (14 Hawker parameters with values, sources, citations)
  - Values from `models/designs/hif_ife/hif_plant.sysml` and `hif_driver.sysml`

#### 5. Library vs. Design Subsection (R3)
- [x] `<h3>` heading
- [x] Architecture table showing three-level pattern per `design.md#8.3`
  - Columns: Layer, Location, What It Defines, Concept-Specific?
  - 5 rows: Foundation → Cost Structure → Analyses → Generic IFE → HIF Instance
- [x] Side-by-side code comparison using `.scope-grid`:
  - Left: IFE Driver (abstract) in `.report-highlight`
  - Right: HIF Driver (concrete) in `.report-highlight`
- [x] Annotation paragraph connecting to MR-3

#### 6. Closing Narrative
- [x] Write closing paragraph connecting forward to cross-concept comparison per `design.md#section-8-narrative-flow`

### Validation

- [x] Open `demo/index.html` in browser
- [x] Section 8 renders without layout errors
- [x] Both SVG images load (no broken image icons)
- [x] Sidebar shows "8 Visualization" without stub badge
- [x] Clicking sidebar link scrolls to Section 8
- [x] `<details>` expands/collapses for parameter table
- [x] Scope grid shows two columns on desktop

**What We Know Works After This Phase:**
Section 8 is fully populated with all three views, images load, layout renders correctly.

---

## Phase 3: Validate & Polish

### Goal
End-to-end quality pass — narrative coherence, technical accuracy, responsive behavior.

### Changes Required

- [x] Read sections 7 → 8 → Appendix A sequentially — verify the story flows
- [x] Cross-check all parameter values in the HTML against source SysML files:
  - `models/designs/hif_ife/hif_plant.sysml` for plant-level params
  - `models/designs/hif_ife/hif_driver.sysml` for driver params
  - `models/library/analyses/ife_lcoe.sysml` for calc def structure
- [x] Check responsive layout at narrow viewport (≤ 900px):
  - `.scope-grid` should stack to single column
  - SVG images should scale within container
- [x] Verify SysML code snippets in the def-vs-usage view are accurate (match actual file content)
- [x] Fix any issues found

### Validation

- [x] Narrative reads as continuous story from Section 7 through Section 8
- [x] All parameter values match source SysML files (14/14 verified)
- [x] No broken layout at mobile viewport (scope-grid collapses, SVGs scale, tables scroll)
- [x] SysML snippets match actual code (IFE Driver 4 attrs, HIF Driver abbreviated but accurate)
- [x] Section is concise (not verbose or overwhelming) — parameter table collapsed by default

**What We Know Works After This Phase:**
Section 8 is complete, accurate, visually polished, and ready to ship.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1 — SVG styling**: If default DOT output is too ugly even with styling, consider using the DOT output format but rendering with a web-based Graphviz renderer (e.g., the `viz.js` library). But try native `dot` first.
- **Phase 2 — Section length**: If the section feels too long after assembly, collapse the parameter table and architecture table behind `<details>`, keeping only the SVGs and key narrative visible by default.
- **Phase 3 — Accuracy errors**: The SysML files are the ground truth. Any discrepancy is a bug in the HTML, not the models.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-03-03
**Actual Changes:**
- Created `demo/structural-view-hif.dot` — styled DOT with demo palette colors (blue inputs, purple chamber cluster), system fonts, rounded nodes
- Created `demo/calc-flow-hif.dot` — hand-authored calc flow with record-style subsystem nodes (Driver/Chamber/Plant/Target), calc def nodes, and output nodes
- Rendered `demo/images/structural-view-hif.svg` (765x134pt, 5KB) — all 7 containment elements
- Rendered `demo/images/calc-flow-hif.svg` (565x596pt, 22KB) — both Hawker and Meier chains with concrete Osiris values
**Issues:** Initial calc flow with individual parameter nodes was too tall (937x1265pt). Revised to use record-style grouped nodes → compact 565x596pt.
**Deviations:** Used hand-styled DOT instead of post-processing extraction CLI output. The extraction CLI's raw DOT was too plain; hand-styling gave better control over colors, fonts, and layout.

### Phase 2 Completion
**Completed:** 2026-03-03
**Actual Changes:**
- Updated sidebar nav: removed `.stub` class/badge, changed href to `#visualization`, text to "Visualization" (line 497)
- Replaced full Section 8 stub (lines 1545-1560) with ~140 lines of content:
  - Opening paragraph connecting from Section 7
  - 8.1 Structural View: SVG in card, terminal block, callout about web viewer
  - 8.2 Calculation Data Flow: SVG in card, dual-chain explanation, expandable parameter table (14 rows)
  - 8.3 Library vs. Design Architecture: 5-row architecture table, side-by-side SysML code comparison (scope-grid + report-highlight), MR-3 annotation
  - Closing paragraph connecting forward to cross-concept work
- All images reference existing files in `demo/images/`
- No new CSS added — uses existing `.card`, `.terminal`, `.callout`, `.table-wrap`, `.scope-grid`, `.scope-box`, `.report-highlight`, `<details>` vocabulary
**Issues:** None
**Deviations:** None — followed design.md closely

### Phase 3 Completion
**Completed:** 2026-03-03
**Actual Changes:**
- No code changes needed — all values and snippets matched source files
- Narrative flow verified: Section 7 (building models) → Section 8 (inspecting models) → Appendix A (PDF processing)
- Responsive layout verified: scope-grid collapses at ≤900px, SVGs scale with max-width:100%, tables scroll via .table-wrap
**Issues:** None
**Deviations:** None

---

**Status**: Complete
