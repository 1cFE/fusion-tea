# Design: Visualization & Demo Completion

**Status**: Complete
**Owner**: Reid W
**Created**: 2026-03-03
**Branch**: init-demo
**Commit**: 9341a06

## Overview

Replace Section 8 stub in the demo with three views generated from/demonstrating the existing toolchain: structural containment, calculation data flow, and definition-vs-usage architecture. The section showcases what the toolchain produces, not just what the models contain.

## Related Artifacts

- **Spec**: `.project/active/visualization-demo/spec.md`
- **Epic**: `.project/backlog/epic-full-workflow-demo.md` (Item 7)
- **Web viewer**: `proof_of_concept/web/` (FastAPI + Cytoscape.js)
- **Extraction CLI**: `proof_of_concept/extraction/` (syside → Cytoscape/DOT)
- **SysML models**: `models/library/` + `models/designs/`

## Research Findings

### Extraction CLI — What Works

The extraction CLI successfully parses the fusion models when pointed at the full `models/` directory:

```
$ uv run python -m proof_of_concept.extraction models/ --format cytoscape
```

Produces 7 nodes:
| ID | Type | Parent |
|----|------|--------|
| `hif_plant` | IFE Power Plant | (root) |
| `hif_plant.driver` | IFE Driver | hif_plant |
| `hif_plant.target_factory` | Target Factory | hif_plant |
| `hif_plant.chamber` | Reaction Chamber | hif_plant |
| `hif_plant.chamber.blanket` | CAS22.1.1 First Wall Blanket | chamber |
| `hif_plant.chamber.shield` | CAS22.1.2 Shield | chamber |
| `hif_plant.chamber.structure` | CAS22.1.5 Primary Structure | chamber |

**Key constraint**: Must use `models/` (not `models/designs/hif_ife/`) because syside needs all files to resolve cross-package imports.

DOT output also works and produces clean subgraph notation:
```dot
digraph structural {
    subgraph cluster_hif_plant {
        label="hif_plant : IFE Power Plant";
        hif_plant_driver [label="driver : IFE Driver"];
        hif_plant_target_factory [label="target_factory : Target Factory"];
        subgraph cluster_hif_plant_chamber {
            label="chamber : Reaction Chamber";
            hif_plant_chamber_blanket [label="blanket : CAS22.1.1 First Wall Blanket"];
            ...
        }
    }
}
```

### What Doesn't Work (or needs workaround)

1. **Cost attachment** — the extraction engine calls `compute_costs()` from a `generate_costs.py` in the model directory. No such file exists for the fusion models (cost calculations live inside the SysML calc defs). So the structural view has no cost coloring.

2. **Extraction shows base types** — `type_name` shows `IFE Driver` not `HIF Driver`. The extraction resolves to the PartDefinition type, not the specializing definition. This is actually fine for the structural view and useful for showing the def-vs-usage pattern.

### Verified Working

- **DOT → SVG pipeline**: `uv run python -m proof_of_concept.extraction models/ --format dot | dot -Tsvg` produces clean 4KB SVG. Graphviz v2.43.0 installed at `/usr/bin/dot`.

### Demo CSS Vocabulary Available

Rich component library already in the demo:
- `.card`, `.callout`, `.callout-important` — content containers
- `.terminal` with `.prompt`, `.output`, `.comment` — terminal output blocks
- `.trace-chain` with `.trace-node`, `.trace-arrow` — horizontal flow diagrams
- `.diagram` — centered monospace diagram container
- `.table-wrap > table` — styled tables
- `.scope-grid` with `.scope-in`, `.scope-out` — two-column comparison
- `.subprocess` with `.sp-title` — process step boxes
- `.artifact-target` — output artifact pills
- `.report-highlight` with `.hl-key`, `.hl-value`, `.hl-comment` — syntax-colored code
- `<dialog>` — modal previews for full-size content
- `<details>` / `<summary>` — expandable sections

### SysML Calc Flow (from model analysis)

The HIF plant has two independent cost calculation chains:

**Hawker Chain** (14 inputs → LCOE):
```
driver.efficiency ─────────┐
driver.energy ─────────────┤
driver.cost_per_joule ─────┤
driver.lifetime_shots ─────┤
chamber.blanket_energy_m ──┤
chamber.yield_cost_const ──┼──→ IFE LCOE calc ──→ lcoe ($/MWh)
plant.availability ────────┤      (15 intermediate
plant.frequency ───────────┤       computations)
plant.gain ────────────────┤
plant.thermal_efficiency ──┤
plant.discount_rate ───────┤
plant.plant_cost_constant ─┤
plant.om_cost_constant ────┤
target_factory.cost ───────┘
```

**Meier Chain** (3 calcs, bottom-up):
```
driver params ──→ Meier Driver Cost ──→ driver_cost_billions ─┐
thermal_power ──→ Meier Reactor Cost ──→ reactor_cost_billions ┼──→ Meier Capital ──→ Meier COE
target_factory ──→ (fixed $0.1B) ──────────────────────────────┘       ↓
                                                              coe_cents_kwh (1988$)
```

**Physics Constraint**:
```
driver.efficiency × plant.gain ──→ Viability Threshold (≥ 10) ──→ assert
              └──→ Recirculating Power Fraction ──→ recirculating_fraction
```

### Definition vs. Usage Relationships

| Library Definition | Location | Design Usage | Location | What Gets Specialized |
|----|----|----|----|----|
| `Costed Component` (abstract) | `library/foundation/` | All CAS parts | `library/cost_structure/` | Base interface for cost rollup |
| `CAS22 Power Core` | `library/cost_structure/` | `CAS22.1.3 Driver`, `CAS22.1.8 Target Factory` | `designs/generic_ife/` | Sub-accounts with scope classification |
| `IFE Driver` (abstract) | `designs/generic_ife/` | `HIF Driver` | `designs/hif_ife/` | efficiency=0.35, Meier cost calc |
| `IFE Power Plant` (template) | `designs/generic_ife/` | `hif_plant` (Osiris) | `designs/hif_ife/` | All operating parameters, Meier chain |
| `IFE LCOE` (calc def) | `library/analyses/` | `lcoe_calc` in plant | `designs/generic_ife/` | Wired to subsystem attributes |
| `Recirculating Power Fraction` (calc def) | `library/analyses/` | `recirc_calc` in plant | `designs/generic_ife/` | Wired to driver/plant params |

Three-level pattern:
1. **Foundation** (library): concept-agnostic interfaces and economics
2. **Generic IFE** (designs/generic_ife): IFE-specific template with abstract driver
3. **HIF Specialization** (designs/hif_ife): concrete Osiris values from source literature

## Proposed Design

### Section 8 Structure

Rename section from "Cross-Concept Comparison" to **"Visualization & Analysis"** — honest about current state (one concept modeled, toolchain demonstrated) while showing the capabilities that will scale to cross-concept comparison.

Three subsections, each with a concrete artifact + brief explanation:

```
Section 8: Visualization & Analysis
├── 8.1 Structural View (screenshot of web viewer + terminal showing CLI)
├── 8.2 Calculation Flow (HTML/CSS data-flow diagram)
└── 8.3 Library vs. Design (table + SysML code snippets)
```

### 8.1 Structural View

**Approach**: Render the structural view as SVG using the extraction CLI → DOT → Graphviz pipeline. This is deterministic, scriptable, and embeds cleanly in HTML.

**Verified pipeline**:
```bash
uv run python -m proof_of_concept.extraction models/ --format dot | dot -Tsvg -o demo/images/structural-view-hif.svg
# Produces 4KB SVG, renders correctly
```

**Demo content**:
- Inline SVG diagram (the main artifact — crisp at any zoom, no raster artifacts)
- Terminal block showing the full pipeline command (extraction CLI → DOT → SVG proves this is real tooling, not a mockup)
- Callout explaining the interactive viewer is also available (`uv run python -m proof_of_concept.web` → Cytoscape.js with expand/collapse, cost coloring, PNG export)

**HTML structure** (using existing components):
```html
<h3>Structural View</h3>
<p>Brief explanation of what this shows...</p>

<!-- SVG rendered from extraction CLI → Graphviz -->
<div class="card" style="text-align:center;">
  <img src="images/structural-view-hif.svg" alt="HIF plant containment hierarchy"
       style="max-width:100%;height:auto;">
</div>

<!-- Terminal showing how it was generated -->
<div class="terminal">
  <span class="prompt">$</span> uv run python -m proof_of_concept.extraction models/ --format dot \<br>
  &nbsp;&nbsp;| dot -Tsvg -o demo/images/structural-view-hif.svg<br>
</div>

<!-- Callout about interactive viewer -->
<div class="callout">
  For interactive exploration, run <code>uv run python -m proof_of_concept.web</code> —
  the same extraction engine powers a Cytoscape.js viewer with expand/collapse,
  cost coloring, and PNG export.
</div>
```

**Enhancement opportunity**: The DOT output can be styled — custom node shapes, colors by CAS scope (shared vs. ife_divergent), edge labels. A small Python wrapper script could generate an enhanced DOT with better styling than the default extraction output. Whether to do this is an implementation-time decision based on how the default looks.

### 8.2 Calculation Flow

**Approach**: Two complementary views — a Graphviz-rendered data flow diagram (SVG) showing the calc chains visually, plus an HTML parameter table grounding the diagram in concrete Osiris values.

**Why Graphviz**: The calc flow is a DAG (directed acyclic graph) — parameters flow from subsystems through calc defs to outputs. Graphviz renders DAGs cleanly with automatic layout. A small script generates the DOT from the known model structure.

**Why not extend the extraction engine**: Out of scope per the spec. The extraction engine does containment only. The calc flow DOT is generated from our knowledge of the model structure, not by parsing — it's a hand-authored diagram rendered by Graphviz.

**Diagram design**: DOT graph with three visual zones:
- **Input cluster** (left): parameter nodes grouped by source subsystem (driver, chamber, plant), colored by source
- **Calc cluster** (center): calc def nodes (IFE LCOE, Recirculating Power, Meier Driver/Reactor/COE)
- **Output cluster** (right): result nodes (LCOE $/MWh, recirculating fraction, Meier COE)
- Edges show data flow from parameters → calc inputs → outputs

Render: `dot -Tsvg calc_flow.dot -o demo/images/calc-flow-hif.svg`

**HTML structure**:
```html
<h3>Calculation Data Flow</h3>
<p>The HIF plant model encodes two independent cost calculation chains...</p>

<!-- SVG calc flow diagram -->
<div class="card" style="text-align:center;">
  <img src="images/calc-flow-hif.svg" alt="HIF cost calculation data flow"
       style="max-width:100%;height:auto;">
</div>

<p>Brief explanation of dual chains (Hawker for general IFE, Meier for HIF-specific validation)...</p>

<!-- Parameter table with concrete values -->
<details><summary>Osiris baseline parameters</summary>
<div class="table-wrap">
<table>
  <thead><tr><th>Parameter</th><th>Value</th><th>Source Subsystem</th><th>Citation</th></tr></thead>
  <tbody>
    <tr><td>driver.efficiency</td><td>0.35</td><td>HIF Driver</td><td>EIF-1992</td></tr>
    <tr><td>plant.gain</td><td>80.0</td><td>Plant operations</td><td>hif_plant.sysml</td></tr>
    ...
  </tbody>
</table>
</div>
</details>
```

### 8.3 Library vs. Design (Definition vs. Usage)

**Approach**: Two-part visualization — a summary table showing the three-level pattern, followed by a concrete side-by-side code comparison for the most instructive example (IFE Driver → HIF Driver specialization).

**Part 1: Architecture table** using the existing `table` styling:

| Layer | File | What It Defines | Concept-Specific? |
|-------|------|-----------------|--------------------|
| Foundation | `library/foundation/` | Economic Parameter, Costed Component | No — shared across all fusion |
| Cost Structure | `library/cost_structure/` | CAS20–CAS90, IFE Cost Parameters | No — CAS is universal |
| Analyses | `library/analyses/` | IFE LCOE, Recirculating Power, Meier costs | No — formulas are general |
| Generic IFE | `designs/generic_ife/` | IFE Power Plant template, subsystem defs | IFE-specific, driver-agnostic |
| HIF Instance | `designs/hif_ife/` | HIF Driver, Osiris plant values | HIF-specific, fully concrete |

**Part 2: Code comparison** using `.scope-grid` (two-column) with `.report-highlight` blocks:

Left column: IFE Driver (abstract, in `designs/generic_ife/ife_subsystems.sysml`)
```sysml
abstract part def 'IFE Driver' :> 'CAS22.1.3 Driver' {
    attribute efficiency : Real;
    attribute cost_per_joule : Real;
    attribute energy : Real;
    attribute lifetime_shots : Real;
}
```

Right column: HIF Driver (concrete, in `designs/hif_ife/hif_driver.sysml`)
```sysml
part def 'HIF Driver' :> 'IFE Driver' {
    attribute beam_energy_mj : Real = 5.0;
    attribute efficiency :>> efficiency = 0.35;
    attribute cost_per_joule :>> cost_per_joule = meier_cost.gamma;
    ...
}
```

Annotation below explaining: the abstract def declares the interface (what every IFE driver must have), the concrete def fills in values from source literature. MR-3 enforces this separation — library stays concept-agnostic, designs bring in concept-specific values with citations.

### 8.4 Sidebar Navigation Update

Change the sidebar entry from:
```html
<a href="#cross-concept" class="stub"><span class="nav-num">8</span> Cross-Concept <span class="nav-badge">stub</span></a>
```
To:
```html
<a href="#visualization"><span class="nav-num">8</span> Visualization</a>
```

Remove the `stub` class and badge.

### Section 8 Narrative Flow

The section connects to Section 7 (Concept Modeling) as follows:
- Section 7 shows *building* the models through the MBSE workflow
- Section 8 shows *what those models produce* — the structural hierarchy, the cost calculations, and the architectural patterns

Opening paragraph (approximately):
> The models built through the workflow in Section 7 aren't just SysML files — they're machine-readable, introspectable artifacts. The extraction toolchain parses them via syside and produces structural views, while the calculation definitions encode the complete cost logic with traceable parameters.

Closing paragraph connects forward to future cross-concept comparison work:
> With one concept modeled (HIF/Osiris), the infrastructure is proven. Adding a second concept — laser IFE, pulsed-power, or magnetic fusion — means specializing the same generic template with different driver parameters and source literature. The comparison axes (LCOE, CAS breakdown, sensitivity profile) are already built into the model structure.

## Potential Risks

1. **SVG styling** — Default Graphviz output uses basic styling (black boxes, Times font). May need custom DOT attributes (colors, fonts, shapes) to look good embedded in the demo. **Mitigation**: DOT supports extensive styling; iterate on the DOT source until the SVGs look polished. Use `fontname="system-ui"` and colors from the demo's CSS palette.

2. **SysML code snippets may confuse readers** — SysML v2 syntax is unfamiliar to most. **Mitigation**: Keep snippets short (4–6 lines), annotate heavily, focus on the pattern (abstract → concrete) rather than syntax details.

3. **Section length** — Three views + narrative could be verbose. **Mitigation**: Use `<details>` for expandable content (parameter tables, full code). Keep the core narrative to ~3 paragraphs + 3 diagrams.

## Integration Strategy

- **Files modified**: `demo/index.html` (Section 8 content + sidebar nav entry)
- **Files added**: `demo/images/structural-view-hif.svg` (extraction CLI → DOT → SVG), `demo/images/calc-flow-hif.svg` (hand-authored DOT → SVG)
- **System dependency**: Graphviz (`dot` CLI, v2.43.0 installed)
- **No new CSS**: All visuals use existing classes (`.card`, `.terminal`, `.trace-chain`, `.scope-grid`, `.report-highlight`, `.callout`, `table`)

## Validation Approach

1. **Visual review**: Open `demo/index.html` in browser, verify Section 8 looks correct and flows from Section 7
2. **Link check**: Verify all `demo/images/` references resolve
3. **Narrative coherence**: Read sections 7 → 8 → Appendix A in sequence — should tell a continuous story
4. **Mobile responsive**: Check at narrow viewport — `.scope-grid` and `.trace-chain` should stack gracefully
5. **Technical accuracy**: Cross-check parameter values against source SysML files

---

**Next Step**: After approval → `/_my_plan` or `/_my_implement`
