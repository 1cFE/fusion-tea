# Stellarator examples and figures

These assets support [Executing the trade studies on a SysML v2 plant model](../sysml-codegen-model-evaluation.md). The figures use the stellarator model and retained study records. They contain no invented study points. Captions identify historical model snapshots and their limits.

## Figures

| Figure | Purpose | Evidence |
|---|---|---|
| `iteration-overview.png` / `.svg` | Distinguish editing/regenerating a model from varying executable inputs | Authoring and evaluation architecture; actual blanket extension and radius/current study |
| `stellarator-component.png` / `.svg` | Connect actual magnet SysML to its plant-supplied inputs and field output | [Model evidence](model-evidence.md), [graph inputs](graph-evidence.md) |
| `stellarator-calculation-graph.png` / `.svg` | Show a selected real magnet dependency graph | [Exact nodes and port edges](graph-evidence.json); `.dot` is retained |
| `stellarator-magnet-tradeoff.png` / `.svg` | Show how current sizing and larger casing space change cost and failures | [Three matched native cases](magnet-sizing-comparison.csv) from the 2026-09-15 study |
| `stellarator-feasibility-cost.png` / `.svg` | Show sampled feasibility and conditional cost together | [256 native cases](feasibility-cost-map.csv) from the 2026-09-17 study |

### Figures the HTML page adds or redraws

The page `../sysml-codegen-model-evaluation.html` embeds these as inline SVG, drawn in the page's fonts through `../figure_style.py`. `render_page_figures.py` writes them and then refreshes the copies inside the page (between its `<!-- inline:NAME -->` markers). The markdown's figures above are untouched.

| File | Page figure | Purpose | Evidence |
|---|---|---|---|
| `page-calculation-graph.svg` (+ `.dot`) | Figure 5 | The magnet graph, redrawn in the page's fonts and colors; its node and edge titles drive the page's explore panel | [graph-evidence.json](graph-evidence.json) |
| `page-winding-pack-fit.svg` | Figure 4 | What the fit calculation compares: casing, cavity, required envelope, the two margins (names only, schematic proportions) | Normative equations in `models/library/analyses/mfe_winding_pack_fit.sysml` |
| `page-fit-case-{reference,reference-sized,reference-accommodated}.svg` | Figure 10 | Each recorded case's required envelope against its clear cavity, one shared scale | [magnet-sizing-comparison.csv](magnet-sizing-comparison.csv); margins agree with the 15 September report |
| `page-breeding-response.svg` (+ `page-breeding-nodes.json`) | Figure 7 | The five stored transport results and the interpolated response; the JSON and the SVG's `data-*` transform drive the page's slider | Table embedded in `exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py`, from `models/designs/stellarator_09/breeding_response.json` |
| `page-feasibility-cost.svg` (+ `page-map-data.json`) | Figure 11 | The 17 September map redrawn with one SVG group per case, a single-hue cost ramp, and text labels above the feasibility panel, each bracketing the stretch of the top row where its limit fails (read off the failing-check classes; no label sits on the grid and no region is shaded); the JSON drives the page's readout and check coloring | [feasibility-cost-map.csv](feasibility-cost-map.csv) |
| `page-feasibility-cost-stacked.svg` | Figure 11, narrow screens | The same map with the panels stacked, drawn at a phone's width; the page shows it below 56rem | [feasibility-cost-map.csv](feasibility-cost-map.csv) |

Reproduce from the repository root: `uv run python docs/write-up/sysml-codegen-assets/render_page_figures.py` (needs Graphviz `dot`).

The graph uses fourteen modules and eighteen port-level links; arrows joining the same pair of modules are combined visually. All represented links match both named historical study pipelines. Other dependencies are omitted explicitly; this is not the whole plant graph. Exact package identities and omitted inputs are preserved in `graph-evidence.json`.

The map distinguishes all twenty then-implemented checks passing, one or more failing, and an invalid power account. It does not interpolate a feasible region. Invalid power accounts are not assigned a cost color. The study costs predate later breeding, installed-cooling, and facility-model changes; they must not be presented as current complete plant prices or qualification evidence.

## Reproduce

From the repository root, using its prescribed Python launcher and Graphviz `dot`:

```sh
MPLCONFIGDIR=/tmp/codegen-writeup-mpl .codex-test/run python docs/write-up/sysml-codegen-assets/extract_study_evidence.py
MPLCONFIGDIR=/tmp/codegen-writeup-mpl .codex-test/run python docs/write-up/sysml-codegen-assets/render_figures.py
```

The extraction checks candidate joins, sample counts, classifications and source values. It reads the recorded study artifacts, not a new model run. The renderer reads those CSVs and the retained graph extraction. PNGs are embedded in the article; SVGs retain vector text and geometry for publication. The component figure's selected source excerpt is recorded in the rendering script and checked against the paths in `model-evidence.md`.

## Verification and provenance

[OWNER] Requested a full article pass with all examples from the stellarator demo, recent goal/study examples, graphical explanations, and images saved beside and embedded in the Markdown. [AGENT] Chose the magnet field/sizing/fit/cost thread, the September 15 and 17 studies, and the current blanket response-table extension. These are editorial selections, not new engineering conclusions.

Three subagents gathered and checked source-code, graph, and study evidence independently by topic. The figure builder uses deterministic plotting and Graphviz, and the rendered PNGs were visually inspected. Source hashes, study identities, held settings, and quantitative limitations are retained in the three evidence documents. The overview and layout choices are explanatory drawings; the data plots and graph connections come from the cited artifacts.
