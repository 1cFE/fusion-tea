# Spec: Visualization & Demo Completion

**Status**: Complete
**Owner**: Reid W
**Created**: 2026-03-03
**Complexity**: Standard (0.5–1 day)
**Epic**: `epic-full-workflow-demo.md` — Item 7
**Branch**: init-demo

---

## Objective

Replace the Section 8 stub in `demo/index.html` with real visualizations generated from the existing toolchain (`proof_of_concept/web/`, `proof_of_concept/extraction/`, `archive/models/tests/coffee_maker/generate_costs.py`). The section should showcase three capabilities:

1. **Structural view** — the containment hierarchy of the HIF plant rendered by the existing Cytoscape.js viewer
2. **Calculation flow** — how calc defs wire parameters from subsystems through intermediate computations to LCOE output
3. **Definition vs. usage** — how library part defs become concept-specific part usages (the `models/library/` → `models/designs/` pattern)

---

## Context

### What exists and works

- **Web viewer** (`proof_of_concept/web/`): FastAPI server + Cytoscape.js frontend. Loads any SysML model via `/api/model/{path}`, renders interactive diagrams with cost coloring, expand/collapse, PNG export. Invoked with `uv run python -m proof_of_concept.web`.
- **Extraction CLI** (`proof_of_concept/extraction/`): `extract_structural_view()` walks the syside AST to produce Cytoscape.js or DOT output. Supports multiplicity, cost attribute attachment, root element auto-detection.
- **Cost evaluation engine** (`archive/models/tests/coffee_maker/generate_costs.py`): Parses `CalculationDefinition` elements via syside, extracts inputs/outputs/formulas, evaluates bottom-up. `compute_costs()` returns `dict[path → dict[attr → float]]`.
- **SysML models** (`models/library/` + `models/designs/`): 11 files — 6 library (foundation, cost structure, analyses) + 4 design (generic IFE, HIF specialization). The HIF plant (`hif_plant.sysml`) is the most complete: Osiris reference design with dual cost models (Hawker LCOE + Meier COE).
- **Demo HTML** (`demo/index.html`): Sections 1–7 and Appendix A are complete. Section 8 is a stub with a "Coming soon" banner. Vanilla CSS, no framework. Extensive style vocabulary (cards, terminals, trace chains, chat transcripts, dialogs, tables).

### What the previous design got wrong

The previous design proposed creating `scripts/generate_viz.py` from scratch and hardcoding values into the demo HTML. It completely missed the existing web viewer and cost evaluation engine. This spec corrects that by building on what exists.

---

## Requirements

### R1: Structural View — Use the Existing Viewer

Generate a structural view of the HIF plant model using the existing toolchain.

**Acceptance criteria:**
- [ ] Run the web viewer against `models/designs/hif_ife/` (or the full `models/` path) and capture the rendered diagram
- [ ] The diagram shows the containment hierarchy: `hif_plant` → `driver`, `target_factory`, `chamber` → `blanket`, `shield`, `structure`
- [ ] Include the captured diagram as a static image in Section 8 of the demo
- [ ] Accompany it with a brief explanation of what the viewer does (loads model via syside, extracts containment tree, renders with Cytoscape.js)
- [ ] Mention that the viewer is interactive (path input, expand/collapse, cost coloring, PNG export) — the demo image is a snapshot of that capability

**Implementation approach:** Point the existing viewer at the fusion models, screenshot the result, embed in the demo. If the viewer doesn't currently handle the fusion models cleanly (e.g., missing cost data hookup, root detection issues), fix the extraction rather than working around it.

**Fallback:** If syside can't parse the fusion models (license issues, syntax incompatibilities), use the extraction CLI to produce DOT output, render with Graphviz to SVG/PNG, and embed that. Document why the web viewer path didn't work.

### R2: Calculation Flow Visualization

Show how calc defs wire parameters from physical subsystems through intermediate computations to final outputs (LCOE, recirculating fraction, Meier COE).

**Acceptance criteria:**
- [ ] Visualize the data flow for at least the Hawker LCOE calculation: 14 input parameters → 15 intermediate computations → LCOE output
- [ ] Show where each input parameter comes from (which subsystem or plant-level attribute provides the value)
- [ ] Make the dual cost model visible: Hawker chain and Meier chain both feed from the same plant, producing independent outputs for cross-validation
- [ ] This can be a hand-crafted diagram (HTML/CSS in the demo, or a static image) if the existing toolchain doesn't support data-flow views — the extraction engine currently does containment only
- [ ] Include concrete numbers from the Osiris baseline (e.g., driver efficiency = 0.35, gain = 80, availability = 0.90) so the visualization is grounded in real data

**Notes:** The existing `generate_costs.py` demonstrates programmatic evaluation of calc defs. The extraction engine (`visualization.py`) only does structural/containment views today. A data-flow view is a different perspective — it may require new visualization work, or it may be effectively communicated as a styled HTML diagram in the demo.

### R3: Definition vs. Usage View

Show the library/designs separation pattern — how abstract part defs in `models/library/` become concrete part usages in `models/designs/`.

**Acceptance criteria:**
- [ ] Visualize the relationship between at least these pairs:
  - `IFE Driver` (abstract, library) → `HIF Driver` (specialized, designs)
  - `IFE Power Plant` (generic template, designs/generic_ife) → `hif_plant` (concrete instance, designs/hif_ife)
  - `IFE LCOE` calc def (library) → `lcoe_calc` usage (wired into plant)
- [ ] Show what comes from library (concept-agnostic) vs. what comes from designs (concept-specific values)
- [ ] Connect this to MR-3 (library concept-agnostic, designs concept-specific) — this isn't just a code organization choice, it's an architectural requirement that enables multi-concept comparison
- [ ] This can be a table, a side-by-side code comparison, a diagram, or a combination — whatever communicates the pattern most clearly

### R4: Section 8 Integration

Replace the current Section 8 stub content with the real visualizations.

**Acceptance criteria:**
- [ ] Remove the stub banner and placeholder content
- [ ] The section title may change from "Cross-Concept Comparison" to something that better reflects what we're actually showing (e.g., "Model Visualization" or "Structural & Cost Analysis") — the narrative should be honest about where we are in the investigation
- [ ] The section flows naturally from Section 7 (Concept Modeling) — Section 7 shows *building* the models, Section 8 shows *what the models look like* and *what the toolchain can do with them*
- [ ] All images are stored in `demo/images/` and referenced with relative paths
- [ ] Use existing CSS vocabulary (cards, terminals, tables, trace chains) — no new CSS unless absolutely necessary
- [ ] The section reads as a natural continuation of the demo narrative, not a disconnected appendix

---

## Out of Scope

- **Building a second concept model** for actual cross-concept comparison (that's future work beyond this epic)
- **New features in the web viewer or extraction CLI** (we use what exists; if something is broken we fix it, but we don't add features)
- **Programmatic cost evaluation of the fusion models** — the cost engine works for the coffee maker test model but may not work for the fusion models without adaptation. If it works, great; if not, we use the values already in the SysML source files
- **Interactive embedded visualizations** in the demo HTML — the demo is a static explainer. We show what the interactive viewer looks like via screenshots, and note that it's runnable locally
- **Sections 1–7 or Appendix A changes** — those are done. We only touch Section 8

---

## Risks

1. **syside may not parse the fusion models.** The models were written and validated via `uv run syside check`, but the extraction engine may trip on features not present in the coffee maker test model (e.g., calc def wiring, redefinition, `expose`). **Mitigation:** Try it first. If it fails, use Graphviz DOT as fallback, or hand-craft the structural diagram from the known model structure.

2. **The web viewer's cost hookup may not work for fusion models.** `compute_costs()` is designed for the coffee maker pattern (a `generate_costs.py` in the model directory). The fusion models use a different cost pattern (calc defs within the SysML, not a Python script). **Mitigation:** The structural view works without costs. Show the structural view and handle cost visualization separately (R2).

3. **The demo section could become too large.** Three views plus explanatory text could overwhelm. **Mitigation:** Keep each view concise — one image/diagram + one paragraph of explanation. Use `<details>` for additional depth if needed.

---

## Deliverables

- Updated `demo/index.html` with Section 8 populated
- Visualization images in `demo/images/`
- This spec at `.project/active/visualization-demo/spec.md`
