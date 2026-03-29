# Concept Explorer UX Tool — Design Space Exploration

**Created:** 2026-03-28
**Status:** Draft — brainstorming approaches
**Input:** concept-explorer.md (vision), concept_analysis pipeline (data source), 1costingfe (cost model framework)

> ## Summary
>
> **9 approaches examined, 3 rounds of independent critique, 2 new hybrid approaches emerged.**
>
> **The core finding**: The frontend visualization work (JSON schema, chart components, page templates) is roughly constant across all viable approaches. The real architectural decision is about **Layer 4 computation** (JS transpilation vs. Python server vs. reactive notebook) and **toolchain** (Python-only vs. adding npm). Everything else is secondary.
>
> **Three prerequisite work items** are needed regardless of architecture: (1) structured JSON output from the pipeline (serialize `model.forward()` results, don't parse model_output.txt), (2) parameter metadata format (resolve the ~280-record content authoring problem for detail cards), and (3) profiling 1costingfe.forward() latency to determine slider viability.
>
> **Recommended path**: **Marimo (Approach F/J)** received the strongest critique endorsement — "Build this first." It is the only approach that delivers Layers 1-4 (including live sliders with authentic computation) in a single pure-Python tool with zero JS, zero cost model transpilation, and zero server complexity beyond `uv run`. The critique challenged the original "just a prototype" framing, arguing that for this project's actual constraints (single user, Python-native, 8-13 concepts, values traceability over polish), Marimo may be the final form, not just a stepping stone.
>
> **Upgrade path if Marimo's layout ceiling is genuinely blocking**: Promote to Approach I (Hybrid) — static frontend (Jinja2 + Plotly/D3) served from FastAPI, with the same `model.forward()` backing the `/compute` endpoint. The Marimo prototype will have validated the information architecture and data loading patterns that Approach I needs.
>
> **The `/manage-concept` agent (Approach G) is complementary**, not competing. Build it as epic Item 5 — it provides the "explain WHY" that no visualization tool can replicate. The Marimo server or FastAPI backend gives the agent a clean interface to read explorer state.
>
> **Eliminated**: Pyodide/WASM (D) — solves a distribution problem that doesn't exist. Agent-first as primary tool (G) — collapses the tool/agent separation the concept doc explicitly defines.
>
> **Decision framework**: Start the three prerequisites now. Build a Marimo prototype for one concept. If the layout works, continue in Marimo. If it doesn't, you've validated the data layer and chart patterns needed for Approach B/I at zero wasted effort.

---

## Context

### What We're Building

An interactive exploration tool that makes the output of the concept analysis pipeline — currently 8 finalized concepts (growing to ~13+) with standardized cost models, sensitivity analyses, CAS breakdowns, and rich narrative context — visually navigable, comparable, and trustworthy. The full vision is documented in `concept-explorer.md`.

### Key Data Characteristics

- **8 concepts with full 1costingfe models** (model_setup.py + model_output.txt), 6 more with analysis-only
- **Standardized output structure**: identical CAS hierarchy (CAS10-90), 15+ CAS22 sub-accounts, same LCOE formula, same sensitivity computation (JAX autodiff elasticities)
- **~30-40 parameters per concept** with elasticities, each needing: baseline value, range, source citation, confidence level, category (shared baseline / key innovation / concept-unique / high-risk)
- **Rich narrative** in analysis.md (35-45 KiB) and synthesis.md (20-30 KiB) — the "why" behind every number
- **Pipeline is Claude-driven**: all analysis artifacts produced by `claude -p` calls via `run_analysis.py`

### Constraints from the Ecosystem

- Project uses `uv` for Python, no npm/node currently in the toolchain
- Existing interactive content pattern: single-file HTML (docs/demo/index.html)
- The `/manage-concept` agent (planned, not yet built) needs to access explorer state
- Parameter category metadata doesn't exist yet — must be authored alongside or extracted from analysis artifacts
- Data changes infrequently (per-concept, not real-time) — new concepts added every few days during active analysis

### Core UX Requirements (from concept-explorer.md)

1. **Concept profile at a glance** — identity, headline economics, confidence
2. **Sensitivity tornado chart** with contextual detail cards on interaction
3. **CAS composition visualization** (stacked bar / waterfall)
4. **Cross-concept comparison** with aligned shared parameters
5. **Interactive "what-if" sliders** with live LCOE recalculation
6. **Trust through traceability** — confidence encoded visually everywhere
7. **Narrative at point of need** — context appears where the reviewer needs it

---

## Approach A: Single-File Claude-Generated HTML

### Description

Extend the existing pattern from `docs/demo/index.html` and the planned epic Item 2 (build-visuals stage). Claude generates a self-contained HTML file per concept with embedded JavaScript, CSS, and data. A separate comparison page aggregates data from multiple concepts. Generation happens as a pipeline stage — `run_analysis.py` calls Claude to produce the HTML after model-setup completes.

### General Architecture

```
model_setup.py + model_output.txt + analysis.md + synthesis.md
    ↓
[Claude -p with HTML generation prompt]
    ↓
sensitivity_explorer.html (per concept, ~200-500 KiB)
comparison.html (cross-concept, generated separately)
```

- **Data embedding**: All concept data inlined as `<script>` JSON blobs
- **Visualization**: Hand-authored D3.js or Chart.js via CDN link, or inline SVG generation
- **Interactivity**: Vanilla JS event handlers for hover/click detail cards, tab navigation
- **Sliders**: JS reimplementation of the cost model (Claude writes the JS translation of model_setup.py)
- **Comparison**: Separate generation pass reads all concept JSONs and produces a unified page

### What Would Need to Be True

- Claude can reliably produce correct, well-structured HTML+JS for complex interactive visualizations (~500 lines of JS)
- The JS cost model reimplementation matches Python output within ±1% (validation gate exists in epic spec)
- A structured data extraction step produces clean JSON from model_output.txt (parsing the text format)
- Parameter metadata (categories, confidence, ranges) exists in a machine-readable format
- The HTML generation prompt is stable enough to produce consistent quality across concepts

### Biggest Challenges

1. **JS cost model fidelity**: Translating Python 1costingfe logic to JS per-concept is error-prone. Each concept has different parameter sets, overrides, and power balance equations. Claude must get the math right every time.
2. **Visual consistency**: Each generation is independent — layouts, color schemes, and interaction patterns may drift across concepts unless the prompt is very prescriptive.
3. **Comparison page complexity**: Aggregating data from 8+ concepts into aligned tornado charts and CAS breakdowns is a significantly harder generation task than single-concept profiles.
4. **Iteration cost**: Every visual tweak requires re-running the Claude generation for all concepts. No hot-reload, no component reuse.
5. **File size**: Embedding all data + JS + CSS per concept could produce large files. Comparison page with 8+ concepts could be >1 MiB.

### Pros

- **Zero dependencies**: No build step, no server, no npm. Opens in any browser.
- **Matches existing pattern**: docs/demo/index.html already works this way.
- **Pipeline-native**: Fits naturally as a stage in run_analysis.py.
- **Self-documenting**: Each HTML file is a complete, portable artifact.
- **Low entry cost**: First concept can be built in hours, not days.

### Cons

- **Fragile at scale**: 13+ concepts × re-generation on every change = slow, expensive iteration loop.
- **No shared components**: Bug fix in tornado chart logic must be regenerated across all files.
- **Limited interactivity ceiling**: Complex features (cross-concept parameter linking, URL-based state sharing) are hard to add incrementally.
- **AI-dependent quality**: Visualization quality depends on prompt engineering, not design iteration.
- **Comparison view is the hard part**: Single-concept profiles are tractable; the comparison page is where this approach strains.

### Key Assessment

Best suited as a **Layer 1 proof-of-concept** (single-concept profile). Natural fit for the epic Item 2 deliverable. Starts to strain at Layer 3 (comparison) and breaks down at Layer 4 (live sliders with correct math). Good for validating the information architecture before investing in a more engineered solution.

### Subagent Critique Summary

**Validated**: The honest Layer 1 scoping is well-calibrated. The zero-dependency, opens-in-any-browser advantage is genuinely differentiated — no other approach produces a truly self-contained portable artifact. The `docs/demo/index.html` existence proof (2,155 lines, fully self-contained) validates the pattern at non-trivial scale.

**Missed/underweighted**: (1) Claude is actually quite good at HTML+D3 generation in 2026 — the "AI-dependent quality" framing is too pessimistic about capability and not pessimistic enough about *cross-run consistency*. The real risk is prompt stability, not capability. (2) The cost of iteration is *review time* (checking 8 generated files for correctness), not money (~$1-2 for all concepts at Sonnet). (3) The file size concern (>1 MiB) is a non-issue — loads in milliseconds locally. (4) **Critical gap**: no mechanism for regression detection across re-generations. A validation gate comparing HTML-embedded JSON against model_output.txt is essential and unmentioned.

**Hidden dependency**: The comparison page requires a "gather all concept JSONs" aggregation phase that breaks the existing per-concept `run_analysis.py` pipeline structure.

**Verdict**: Prototype one concept as a Layer 1 proof-of-concept to validate the information architecture. Do not plan for this to be the production solution.

---

## Approach B: Static Site Generator + Interactive Visualization Library

### Description

A build pipeline extracts structured data from all concept artifacts into a canonical JSON format, then a static site generator (Astro, Eleventy, or even a simple Python Jinja2 template) produces an interactive multi-page site using a professional visualization library (Plotly, ECharts, or D3). The site is purely static — no server needed after build.

### General Architecture

```
[Data Extraction Script (Python)]
    reads: model_setup.py, model_output.txt, analysis.md, synthesis.md
    writes: data/concepts/{id}.json, data/comparison.json

[Static Site Generator]
    reads: data/*.json + templates/
    writes: dist/ (HTML + JS + CSS bundle)

[Visualization Library]
    Plotly.js, ECharts, or D3 — loaded from CDN or bundled
    Reads JSON data at page load, renders interactive charts
```

- **Data layer**: Python script parses all artifacts → normalized JSON schema per concept
- **Template layer**: Jinja2 / Astro / 11ty templates define page structure, inject data
- **Viz layer**: Library renders tornado charts, stacked bars, comparison grids
- **Slider layer**: JS cost model (hand-written once, parameterized per concept) or call Python via API

### What Would Need to Be True

- A well-defined JSON schema for concept data (parameters, sensitivities, CAS breakdown, metadata, narrative excerpts)
- The data extraction script handles the diversity in model_setup.py formats (1costingfe path vs. free-form)
- A static site generator is acceptable in the toolchain (may need node/npm for Astro/11ty, or stay Python-only with Jinja2)
- Visualization library chosen can handle all chart types: horizontal bar (tornado), stacked bar (CAS), scatter (comparison), and slider-driven updates

### Biggest Challenges

1. **Data extraction robustness**: model_output.txt is a text format designed for humans, not machines. Parsing it reliably across all concept variants requires careful regex or structured output from 1costingfe.
2. **JS cost model for sliders**: Same challenge as Approach A — need a JS reimplementation of the cost model for live parameter adjustment. Could be deferred (sliders = Layer 4).
3. **Build toolchain**: Adding npm/node to a uv-only Python project is a friction point. Pure-Python alternatives (Jinja2 + manual JS) work but are less ergonomic.
4. **Keeping data fresh**: JSON must be regenerated when any upstream artifact changes. Need a "build" step or watcher.

### Pros

- **Professional visualization quality**: Plotly/ECharts/D3 produce publication-grade interactive charts out of the box.
- **Shared components**: Tornado chart template written once, data-driven for all concepts.
- **Fast iteration on design**: Change a template or CSS, rebuild, see all concepts update.
- **Clean data/presentation separation**: JSON schema becomes a stable interface; visualization can evolve independently.
- **Scalable**: Adding concept 13 is "add JSON, rebuild" — no per-concept generation.
- **Portable output**: dist/ folder can be opened locally, hosted on GitHub Pages, or served anywhere.

### Cons

- **Build step required**: Not zero-config; someone must run the build.
- **Toolchain expansion**: Likely needs node/npm alongside uv, unless using a Python-only SSG.
- **Upfront schema design**: Getting the JSON schema right is design work that precedes any visualization.
- **Narrative integration is manual**: Extracting the right prose excerpts from 35 KiB analysis.md into structured JSON requires judgment calls about what to include.
- **Slider interactivity requires JS cost model**: Full what-if capability needs the same JS translation challenge.

### Key Assessment

The **strongest general-purpose option** for Layers 1-3. Clean separation of concerns, professional output quality, scales well. The JSON schema design is the critical upfront investment — once that's right, the visualization layer can be iterated rapidly. Sliders (Layer 4) remain hard but are cleanly deferrable. Consider a Python-only SSG (Jinja2 + a simple build script) to avoid adding node to the toolchain.

### Subagent Critique Summary

**Validated**: JSON schema design as the critical upfront investment is "the most important insight in the entire document." The Jinja2 recommendation to avoid npm is well-calibrated. The "adding concept 13 is just add JSON, rebuild" scalability is precisely correct and is the single strongest argument over Approach A.

**Missed/underweighted**: (1) **Data extraction robustness is much harder than described.** The model_setup.py files have structural divergence: some are ~188-line wrappers around `costingfe.model.forward()`, others are 1100+ line standalone implementations with custom print formatting. Parsing model_output.txt means parsing 8 different output formats. **The real solution is to not parse model_output.txt at all** — instead, add a pipeline stage that calls `model.forward()` programmatically and serializes the result object to JSON directly. This prerequisite refactoring is unacknowledged. (2) "Narrative integration is manual" hides the actual scope: US-5 detail cards require authoring ~240-320 metadata records (30-40 parameters × 8 concepts) with source citations, ranges, confidence, and categories. This is a major content effort. (3) **B has a natural upgrade path to I** (static frontend → add FastAPI backend for sliders). This evolutionary path is B's strongest strategic argument and is not mentioned.

**Hidden dependency**: The JSON schema must accommodate structural differences between costingfe-backed concepts (JAX autodiff elasticities) and standalone concepts (hand-computed sensitivities) without lying about comparability.

**Verdict**: Build it — but start with the JSON schema and data extraction pipeline, not the visualization. The schema is the hard part; the charts are downstream.

---

## Approach C: Python Dashboard (Panel / Dash / Streamlit)

### Description

Build the explorer as a Python web application using a dashboard framework. The app runs a local server, loads concept data directly from the filesystem (or from 1costingfe), and renders interactive visualizations. Panel (HoloViz), Dash (Plotly), or Streamlit are the main candidates.

### General Architecture

```
[Python Dashboard App]
    ├── data_loader.py — reads model_setup.py, model_output.txt, analysis.md
    ├── cost_model.py — imports 1costingfe directly for live computation
    ├── views/
    │   ├── profile.py — single-concept profile view
    │   ├── sensitivity.py — tornado chart + detail cards
    │   ├── comparison.py — multi-concept comparison
    │   └── explorer.py — entry view / concept grid
    └── app.py — routing, layout, state management

[Browser]
    ← Server renders HTML with interactive widgets →
    Slider changes → server recomputes via 1costingfe → returns updated chart
```

- **Data**: Direct filesystem reads + 1costingfe Python imports
- **Computation**: Sliders trigger actual Python model.forward() calls — no JS translation needed
- **Visualization**: Plotly (via Dash), Bokeh (via Panel), or Altair (via Streamlit)
- **State**: Server-side session state; comparison set managed in Python

### What Would Need to Be True

- A Python dashboard framework is acceptable (adds dependency, requires `uv run` to launch)
- Server-side computation latency for 1costingfe.forward() is acceptable (<500ms per slider change)
- The chosen framework supports the information density and interaction patterns needed (hover cards, side-by-side layouts, tabbed navigation)
- Deployment is local-only (acceptable for a single-user research tool)

### Biggest Challenges

1. **Framework limitations on UX polish**: Streamlit's layout model is simple but constraining — information-dense "Bloomberg terminal" aesthetic is hard. Dash is more flexible but verbose. Panel is powerful but has a learning curve.
2. **Latency on slider interaction**: Each slider change round-trips to the server. If 1costingfe.forward() takes >200ms, the experience feels laggy. Need to profile.
3. **Narrative integration**: Dashboard frameworks are chart-centric. Embedding rich prose (hover cards with multi-paragraph explanations, source citations) requires custom HTML components.
4. **Deployment friction**: User must run `uv run python app.py` and open a browser. Not as frictionless as opening an HTML file. Not easily shareable.
5. **State sharing with agent**: The `/manage-concept` agent needs to read explorer state. A running server adds complexity — need an API endpoint or state file.

### Pros

- **Native 1costingfe integration**: Sliders call actual Python cost model — no translation, no fidelity concerns. This is the killer advantage.
- **Stays in the Python ecosystem**: No npm, no JS to write, uses uv toolchain.
- **Rich computation**: Can do things static sites can't — Monte Carlo sweeps, parameter correlation analysis, optimization.
- **Rapid prototyping**: Streamlit especially — working prototype in hours.
- **Live data**: Reads filesystem directly; no build step when artifacts change.

### Cons

- **Requires running server**: Not a portable artifact; can't email someone an HTML file.
- **UX ceiling**: Dashboard frameworks optimize for data apps, not information-dense review instruments. Achieving the design aesthetic in concept-explorer.md (trustworthy density, narrative at point of need) will fight the framework.
- **Single-user**: Not designed for concurrent users (fine for this use case, but limits sharing).
- **Framework lock-in**: Significant rewrite to switch frameworks or move to a different approach later.
- **Testing and CI**: Harder to validate than static HTML files.

### Key Assessment

The **best option for Layer 4 (sliders)** because it avoids the JS cost model translation entirely. Trades UX polish for computational authenticity. Consider as the **computation backend** for a separate frontend (hybrid approach), or as a **rapid prototype** to validate the information architecture before building a polished static frontend. Streamlit for speed, Dash for flexibility, Panel for power.

### Subagent Critique Summary

**Validated**: Native 1costingfe integration is correctly identified as the killer advantage — eliminates an entire class of fidelity bugs. The framework ranking (Streamlit speed / Dash flexibility / Panel power) is correct. A Streamlit prototype could be working in 2-4 hours — genuinely rapid.

**Missed/underweighted**: (1) **Streamlit's re-run model is worse than described for sliders.** Every slider change re-runs the entire script. While `@st.cache_data` helps for data loading, the model computation itself must re-execute. JAX has a cold-start JIT compilation penalty making the *first* slider interaction much slower than subsequent ones. (2) The "requires running server" friction is larger than acknowledged — a quick-glance check takes 10-15s (start server, navigate) vs. 1s (open HTML file). Over weeks this compounds into the tool being used less. (3) **Testing story is absent.** Dashboard apps are notoriously hard to test. For a TEA tool where correctness matters, not being able to assert "dipole shows availability as #1 sensitivity" is a real gap. (4) The comparison view triggers server-side recomputation for all concepts — 4 concepts × 30 parameters = 120 sensitivity recomputations per comparison update.

**Missed combination**: Use Streamlit/Dash as a rapid prototype to validate the information architecture and slider model, then extract the JSON schema and data loading code into Approach B's pipeline, keeping the Python dashboard as the Layer 4 computation backend — which is essentially Approach I. This evolutionary path is more natural than the document acknowledges.

**Verdict**: Prototype it as the fastest path to live sliders, but plan for it to evolve into Approach I when a polished frontend is needed.

---

## Approach D: Pyodide / WASM — Python in the Browser

### Description

Use Pyodide (CPython compiled to WebAssembly) to run the actual 1costingfe Python code directly in the browser. The user opens a static HTML page; Pyodide loads, imports 1costingfe, and all computation happens client-side. No server needed. Combines the portability of static HTML with the computational authenticity of Python.

### General Architecture

```
[Static HTML + JS Shell]
    ├── index.html — UI layout, chart containers, slider controls
    ├── app.js — UI logic, event handlers, calls into Pyodide
    └── pyodide/ — WASM runtime (loaded from CDN or bundled, ~20 MiB)

[Pyodide Runtime (in browser)]
    ├── costingfe/ — 1costingfe package loaded as wheel
    ├── concept_data/ — model_setup.py configs as Python modules
    └── compute.py — bridge: receives slider values, calls model.forward(), returns JSON

[Visualization]
    Plotly.js or D3 in the JS layer, fed by Pyodide computation results
```

- **Data flow**: Slider change → JS calls Pyodide → Python runs model.forward() → returns JSON → JS updates charts
- **Loading**: First load downloads Pyodide WASM + 1costingfe wheel (~30s). Subsequent runs are cached.
- **Packaging**: 1costingfe must be pip-installable as a pure-Python wheel (or have its C extensions compiled to WASM)

### What Would Need to Be True

- **1costingfe is pure Python** (or its compiled dependencies — JAX, numpy — are available in Pyodide). JAX is NOT available in Pyodide as of 2025. This is a potential blocker.
- Pyodide startup time (~5-15s) is acceptable for the use case
- The 1costingfe package can be packaged as a wheel and loaded into Pyodide
- Users are comfortable with a ~20-30 MiB initial download (cached after first load)

### Biggest Challenges

1. **JAX dependency**: 1costingfe uses JAX for autodiff sensitivity analysis. JAX is NOT available in Pyodide. Sensitivity computation would need to be either pre-computed (losing live recalculation) or reimplemented with a Pyodide-compatible autodiff library.
2. **Startup latency**: 5-15 seconds to load Pyodide + packages on first visit. Unacceptable for casual browsing; tolerable for a dedicated research tool.
3. **Debugging complexity**: Python errors in the browser are harder to diagnose than server-side errors.
4. **Package compatibility**: Any C-extension dependency in 1costingfe or its transitive deps must be compiled to WASM or replaced.
5. **Initial download size**: ~20-30 MiB for Pyodide + packages. Fine on broadband, painful on slow connections.

### Pros

- **Computational authenticity without a server**: Actual Python cost model runs in the browser. No JS translation.
- **Static deployment**: Just HTML + JS + WASM files. Host on GitHub Pages, open locally, share as a zip.
- **Full Python ecosystem**: Can use numpy, scipy, matplotlib (all available in Pyodide) for additional analysis.
- **Offline capable**: Once cached, works without internet.

### Cons

- **JAX blocker**: Sensitivity analysis (the core feature) depends on JAX, which isn't available in Pyodide. Would need pre-computed sensitivities or a workaround.
- **Slow startup**: 5-15s load time undermines "fluid navigation" requirement.
- **Large download**: ~20-30 MiB initial payload.
- **Fragile dependency chain**: Any change to 1costingfe's dependencies could break Pyodide compatibility.
- **Niche technology**: Fewer developers know Pyodide; debugging is harder; community support is thinner.

### Key Assessment

Elegant in theory but **blocked by the JAX dependency** for live sensitivity computation. If sensitivities are pre-computed (which they are in model_output.txt), the main value proposition — running the actual cost model — is reduced to slider-driven LCOE recalculation, which is achievable with a much simpler JS reimplementation. Consider only if 1costingfe's JAX dependency is removed or if a Pyodide-compatible autodiff alternative exists. The startup latency also conflicts with the "fluid navigation" design principle.

### Subagent Critique Summary

**Validated**: The JAX blocker identification is correct and well-handled. The key insight that "if sensitivities are pre-computed, the value proposition reduces to slider-driven LCOE recalculation achievable with simpler JS" is sharp thinking.

**Missed/underweighted**: (1) **The forward cost model may not actually need JAX.** Looking at actual model_setup.py files, the forward model is a chain of arithmetic operations on a dataclass (multiplications, power-law scaling, CAS summation). JAX is used specifically for autodiff sensitivity computation, not the forward pass. If sliders only need LCOE recalculation (not re-derived sensitivities), the forward pass could potentially run in Pyodide without JAX. This changes the verdict from "blocked" to "possible but with reduced scope that eliminates the main motivation." (2) The debugging story is worse than described — when Pyodide silently produces wrong LCOE values due to numpy version mismatches or float64/float32 discrepancies, there's no easy way to diff against native Python output. (3) Browser cache eviction makes "offline capable once cached" less reliable than implied for infrequent use.

**Hidden dependency**: Testing parity (native Python vs. Pyodide) requires a headless browser (Playwright/Puppeteer), which adds npm through the back door. Also, model_setup.py files aren't directly importable as modules — they have `__main__` blocks and inline print formatting.

**Verdict**: Pass. Every benefit Pyodide provides is delivered more cleanly by other approaches. This solves a distribution problem this project doesn't have.

---

## Approach E: Modern SPA (React/Svelte) with Transpiled Cost Model

### Description

Build a full single-page application using a modern frontend framework (React, Svelte, or Vue). The cost model is manually transpiled to TypeScript once, parameterized per concept. Data is extracted to JSON. The app is a polished, professional-grade web application with component reuse, state management, and URL-based routing.

### General Architecture

```
[Data Pipeline (Python)]
    extract_data.py → data/concepts/{id}.json

[Frontend Application]
    ├── src/
    │   ├── components/
    │   │   ├── TornadoChart.tsx — reusable tornado chart
    │   │   ├── CASBreakdown.tsx — stacked bar / waterfall
    │   │   ├── ParameterCard.tsx — hover detail card
    │   │   ├── ConceptProfile.tsx — identity + summary
    │   │   ├── ComparisonView.tsx — side-by-side alignment
    │   │   └── Slider.tsx — parameter adjustment with live update
    │   ├── models/
    │   │   └── costModel.ts — 1costingfe logic in TypeScript
    │   ├── data/
    │   │   └── loader.ts — fetches concept JSON
    │   └── App.tsx — routing, layout, state
    ├── package.json
    └── vite.config.ts

[Build]
    npm run build → dist/ (static files, deployable anywhere)
```

- **Visualization**: D3 for custom charts, or Recharts/Nivo for React-native charting
- **State**: URL params encode comparison set + slider positions → shareable, agent-readable
- **Cost model**: TypeScript implementation validated against Python output for all concepts
- **Deployment**: Static dist/ folder — GitHub Pages, local file://, or any CDN

### What Would Need to Be True

- The project is willing to adopt npm/node as a build dependency
- Someone transpiles the 1costingfe cost model to TypeScript (one-time effort, ~500-1000 LOC)
- The TS cost model is validated against Python output for all concepts (automated test suite)
- Frontend development skills are available (or Claude can write and iterate the components)
- The JSON data schema is designed and extraction pipeline built

### Biggest Challenges

1. **Cost model transpilation**: Translating 1costingfe's Python logic (including concept-specific branches, CAS hierarchy, power balance equations) to TypeScript is a significant one-time effort. Must be validated per-concept.
2. **Toolchain expansion**: Adding npm/node/vite to a Python-only project is a cultural and maintenance cost.
3. **Development velocity**: React/Svelte components require more boilerplate than dashboard frameworks. The first working version takes longer.
4. **Keeping TS model in sync**: When 1costingfe updates its cost formulas, the TS version must be updated too. Drift is a real risk.
5. **Over-engineering risk**: For a single-user research tool with 8-13 concepts, a full SPA may be more infrastructure than the problem warrants.

### Pros

- **Maximum UX quality**: Full control over layout, animation, interaction design. Can achieve the "trustworthy density" aesthetic.
- **Component reuse**: Tornado chart, CAS breakdown, parameter card written once, used everywhere.
- **URL-based state**: Comparison set and slider positions encoded in URL — agent can read it, users can share it.
- **Performance**: Client-side rendering with optimized JS — sub-millisecond slider updates.
- **Professional output**: The result looks and feels like a production web application.
- **Static deployment**: Build once, deploy anywhere, no server.

### Cons

- **Highest development cost**: Full SPA architecture for 8-13 concepts may be over-engineered.
- **Toolchain expansion**: npm/node added to project.
- **Cost model maintenance**: TS transpilation must track Python changes.
- **Slower time-to-first-value**: Weeks to a polished first version vs. hours for simpler approaches.
- **Dependency surface**: React/Svelte ecosystem has deep dependency trees.

### Key Assessment

The **highest-ceiling option** for UX quality and long-term maintainability. Overkill for Layer 1, justified if the tool becomes a primary research instrument used daily. The cost model transpilation is the key risk — consider deferring sliders to Layer 4 and using pre-computed data for Layers 1-3. Svelte is lighter than React for this use case (less boilerplate, better performance for a data-heavy app).

### Subagent Critique Summary

**Validated**: The "over-engineering risk" callout is the most important sentence in this section. The Svelte-over-React recommendation is sound. URL-based state as the most natural agent integration interface is a genuine architectural insight.

**Missed/underweighted**: (1) **Transpilation is NOT a one-time effort.** Each concept has 30-40 parameters with concept-specific overrides, different power balance equations (MFE vs IFE vs MIF), and custom CAS account zeroing. The active pipeline is producing new concepts — concept 9 with a novel override pattern forces TS model extension. This is ongoing maintenance, not a one-time cost. (2) **Claude-as-frontend-developer is an untested assumption** doing heavy lifting. Iterating on interactive D3 visualizations through text-based feedback loops is significantly slower than hot-reload direct manipulation. (3) **The JSON schema design is underweighted as a risk** — getting it right determines whether the visualization layer is clean or full of special cases, and it must be designed before any frontend code is written (weeks of upfront work with no visible progress). (4) **Two-codebase maintenance**: Python pipeline and TypeScript frontend must agree on data formats, cost model semantics, and parameter definitions. Any upstream change requires updating both.

**Hidden dependency**: A validation harness running all concepts through both Python and TS cost models, asserting numerical parity. Without it, the transpiled model drifts silently.

**Verdict**: Validate the information architecture and stabilize the JSON schema in a simpler approach (B or F) first. Build the SPA only after the schema is stable and the UX ceiling of simpler approaches is proven to be the bottleneck.

---

## Approach F: Marimo Reactive Notebook

### Description

Use Marimo, a reactive Python notebook framework, to build the explorer as an interactive notebook that can be exported as a standalone web application. Marimo's reactive execution model means changing a slider automatically re-executes all dependent cells — natural fit for parameter exploration. The notebook can be served locally or exported as a static WASM app.

### General Architecture

```
[Marimo Notebook]
    concept_explorer.py (single file, Marimo notebook format)
    ├── Cell 1: Data loading — read concept artifacts, build data structures
    ├── Cell 2: Concept selector — dropdown/grid to pick concept
    ├── Cell 3: Profile view — identity card, headline metrics
    ├── Cell 4: Tornado chart — Plotly/Altair sensitivity visualization
    ├── Cell 5: CAS breakdown — stacked bar chart
    ├── Cell 6: Sliders — parameter adjustment widgets
    ├── Cell 7: Live computation — model.forward() with slider values
    ├── Cell 8: Comparison — multi-concept aligned charts
    └── Cell 9: Narrative — extracted analysis excerpts

[Execution Modes]
    uv run marimo run concept_explorer.py          # App mode (hides code)
    uv run marimo edit concept_explorer.py          # Notebook mode (shows code)
    uv run marimo export concept_explorer.py --wasm # Static WASM export
```

- **Reactivity**: Change concept selector → all downstream cells re-execute automatically
- **Computation**: Direct 1costingfe import — actual Python cost model
- **Visualization**: Altair, Plotly, or Matplotlib — all supported natively
- **Export**: Can produce a static WASM site (uses Pyodide under the hood) or run as a server

### What Would Need to Be True

- Marimo's layout capabilities can achieve the information density needed (it supports custom CSS and HTML cells)
- The reactive execution model is fast enough for slider interaction (depends on 1costingfe.forward() latency)
- Marimo is acceptable as a project dependency (`uv add marimo`)
- The notebook format is maintainable (Marimo stores notebooks as pure Python, unlike Jupyter's JSON)

### Biggest Challenges

1. **Layout constraints**: Marimo's default layout is vertical cell flow. Achieving the "Bloomberg terminal" density with side-by-side panels, hover cards, and tabbed navigation requires heavy use of `mo.ui.tabs()`, `mo.hstack()`, `mo.vstack()`, and custom HTML — possible but not the framework's sweet spot.
2. **Comparison view complexity**: Showing 2-4 concepts side-by-side with aligned parameters pushes Marimo's layout system.
3. **WASM export inherits Pyodide limitations**: If exporting as static WASM, the JAX dependency issue (Approach D) resurfaces.
4. **Polish ceiling**: Marimo produces functional, clean UIs — but not the custom-designed, branded experience of a dedicated SPA.
5. **Single-file scaling**: A single notebook file covering all views (profile, sensitivity, comparison, entry) could become unwieldy. Marimo does support imports, but the primary unit is one notebook.

### Pros

- **Fastest path to live sliders**: Direct 1costingfe import means sliders work on day one. No translation.
- **Pure Python**: No npm, no JS. Fits the uv toolchain perfectly.
- **Reactive by default**: Changing any input automatically updates all dependent outputs. Natural for parameter exploration.
- **Dual mode**: Same file works as an app (for reviewers) or a notebook (for developers/analysts).
- **Pure Python storage**: Unlike Jupyter, Marimo notebooks are plain .py files — clean diffs, no JSON noise.
- **Rapid iteration**: Change a cell, see it update instantly. Ideal for prototyping.

### Cons

- **Layout ceiling**: Achieving the full design vision may require fighting the framework.
- **Less polished output**: Looks like a data app, not a bespoke review instrument.
- **Comparison views are hard**: Multi-concept side-by-side is not Marimo's strength.
- **WASM export has JAX issues**: Static deployment option is limited.
- **Niche framework**: Smaller community than Streamlit or Dash, though growing rapidly.

### Key Assessment

**Excellent rapid-prototyping option** that delivers live sliders immediately with zero JS. Best for validating the information architecture and interaction model before investing in a polished frontend. The reactive execution model is a natural fit for "what-if" exploration. Consider as the **prototyping vehicle** that informs the final architecture, or as the **permanent solution** if the layout constraints are acceptable. Marimo's pure-Python storage is a significant advantage for this project's toolchain.

### Subagent Critique Summary

**Validated**: Direct 1costingfe import eliminating an entire class of fidelity bugs is "not a minor convenience — it eliminates the riskiest technical challenge entirely." The dual app/notebook mode and pure-Python storage advantages are real and underappreciated.

**Key challenge to the original assessment — layout is BETTER than described**: (1) Marimo's `mo.ui.tabs()`, `mo.hstack()`, `mo.vstack()`, and `mo.Html()` can achieve "functional information density" at ~70% of the Bloomberg terminal aesthetic — and for a single-user research tool, 70% fidelity at 10% engineering cost is an excellent trade. (2) Comparison view difficulty is overstated relative to other approaches — Plotly subplots or Altair faceted charts handle alignment, and the difficulty delta between Marimo and an SPA for this feature is smaller than implied. (3) The WASM export limitation is a **red herring** — this is a single-user tool launched via `uv run`, not a public web app. (4) **`mo.state()` and reactive forms are unmentioned** — Marimo has a state management system handling complex multi-widget interactions (concept selector → tornado chart + CAS breakdown; slider → LCOE summary + re-rank tornado). This is the exact interaction pattern in US-7. (5) Agent integration is straightforward: Marimo runs a local server, can expose state via custom routes or write a state file on interaction.

**Hidden dependency**: 1costingfe.forward() latency must be profiled early. Slider drags produce 10-20 intermediate values; if forward() > 200ms, explicit debouncing is needed. Also, data loading for 8-13 concepts must be pre-loaded at startup, not per-concept-switch.

**Strongest endorsement from any critique**: "Build this first. It is the fastest path to a working tool covering Layers 1-4. If layout limitations prove blocking, every hour spent produces reusable artifacts (data loading, charts, metadata structure) that transfer directly to Approach B or I." The framing as "just a prototype" undersells it — for this project's actual constraints, **Marimo may be the final form**.

---

## Approach G: Agent-First — LLM Generates Visualizations On Demand

### Description

Instead of building a traditional application, lean into the AI-native workflow already established in the project. The `/manage-concept` agent (or a new `/explore-concept` agent) generates visualizations, comparisons, and analysis on demand in response to natural language queries. The "explorer" is a conversational interface, not a traditional GUI.

### General Architecture

```
[User Query]
    "Compare the sensitivity profiles of dipole and laser ICF"
    "Show me the CAS breakdown for mirror, highlighting where it differs from tokamak"
    "What happens to dipole LCOE if availability drops to 50%?"

[Agent]
    ├── Reads relevant artifacts (model_setup.py, model_output.txt, analysis.md)
    ├── Runs 1costingfe computations as needed
    ├── Generates visualization (HTML snippet, Plotly JSON, or matplotlib PNG)
    └── Returns narrative explanation + chart

[Output]
    Inline visualization in terminal (if supported) or saved HTML file
    Narrative explanation with traceability to sources
```

- **No persistent UI**: Each query produces a fresh response with relevant data and charts
- **Computation**: Agent calls 1costingfe directly for any what-if scenario
- **Visualization**: Agent generates charts using matplotlib/plotly, saves as HTML or images
- **Context**: Agent reads all artifacts, cross-references sources, explains causally

### What Would Need to Be True

- LLM can reliably produce correct, useful visualizations from structured data
- Response latency (10-30s for a Claude call) is acceptable for the exploration workflow
- Users are comfortable with conversational exploration rather than direct manipulation
- The agent can maintain enough context to handle multi-step exploration ("now compare that to...")
- Visualization output is viewable in the user's workflow (inline images, HTML files, or browser tabs)

### Biggest Challenges

1. **Latency**: Each "interaction" is a 10-30s LLM call. Comparing this to sub-second slider updates in a GUI — the exploration cadence is fundamentally different.
2. **Reproducibility**: Same query may produce different visualizations. No guarantee of consistency.
3. **Discovery**: A GUI shows you what's available (browse concepts, see all parameters). A conversational interface requires you to know what to ask for.
4. **Visual consistency**: Each generated chart may use different scales, colors, layouts — hard to do systematic comparison.
5. **Cost**: Each query is an API call. Heavy exploration sessions could cost $5-20 in API usage.

### Pros

- **Maximum flexibility**: Any question, any comparison, any what-if — no predetermined views.
- **Narrative integration is native**: The agent can explain WHY alongside showing WHAT. This is the only approach where causal explanation is built-in.
- **Zero frontend code**: No HTML, no JS, no CSS, no build step.
- **Leverages existing infrastructure**: Uses the same Claude -p pipeline, same 1costingfe integration.
- **Handles edge cases gracefully**: Unusual comparisons, concept-specific quirks, and novel questions don't require new UI components.
- **Already partially planned**: The `/manage-concept` agent in the epic is designed for exactly this kind of interaction.

### Cons

- **Latency kills exploration flow**: The "what does this look like?" → "what about that?" cadence of visual exploration is disrupted by 10-30s waits.
- **No persistent overview**: Can't glance at all concepts at once. No entry view, no discovery.
- **No visual consistency**: Charts from different queries may use different scales, colors, encodings.
- **Expensive at scale**: Heavy exploration sessions accumulate API costs.
- **Not self-service for non-technical users**: Requires knowing what questions to ask.
- **Reproducibility concerns**: Regenerating the same chart may produce different results.

### Key Assessment

**Complementary, not primary**. This approach excels at the "explain WHY" half of the vision (US-12) but fails at the "show WHAT" half that requires persistent, consistent, browsable views. The concept-explorer.md explicitly separates tool (visual, self-service) from agent (conversational, interpretive). This approach collapses that separation. Best used as the **companion agent** alongside a persistent visual tool, not as a replacement for it. Aligns with the epic's `/manage-concept` agent (Item 5), which is designed for exactly this role.

### Subagent Critique Summary

**Validated**: The "complementary, not primary" assessment is exactly right. The concept-explorer.md explicitly separates tool from agent, and collapsing that separation is architecturally wrong. G is not competing with the other approaches — it IS the `/manage-concept` agent (epic Item 5).

**Missed/underweighted**: (1) **Session context problem** is harder than described. "Now compare that to stellarator" requires tracking what was previously computed, what comparison set was active, and what parameter overrides were in effect — either a growing context window (expensive, eventually truncated) or state serialization (which lands you back at building a persistent data layer). (2) **Visualization quality ceiling is a fundamental conflict**, not an annoyance. Two tornado charts from separate LLM calls cannot reliably use the same axis scales, color encoding, and layout. This directly conflicts with US-9 (aligned sensitivity profiles) and "trustworthy density." If the reviewer can't trust two charts use the same scale, the comparison is meaningless. (3) **Worst debuggability** of any approach — when a chart looks wrong, is it the data, the prompt, or the LLM hallucinating a number? No way to verify independently.

**Verdict**: Build as the companion agent (epic Item 5), not as the visual explorer. This is a different tool serving a different need — the critique agrees with the original assessment completely.

---

## Approach H: Observable Framework

### Description

Use Observable Framework, a static site generator designed specifically for data-driven interactive pages. Observable's reactive runtime means values flow through a dependency graph — change one input, all dependent outputs update. Data loaders run at build time (can be Python scripts), and the frontend uses Observable's reactive JavaScript for interactivity.

### General Architecture

```
[Observable Framework Project]
    ├── src/
    │   ├── data/
    │   │   ├── concepts.json.py   # Python data loader → runs at build time
    │   │   └── sensitivities.json.py
    │   ├── index.md               # Entry view (Observable Markdown)
    │   ├── concept/[id].md        # Parameterized concept profile pages
    │   └── compare.md             # Comparison view
    ├── src/components/
    │   ├── tornado.js             # Reusable tornado chart (D3)
    │   ├── cas-breakdown.js       # CAS stacked bar
    │   └── parameter-card.js      # Detail card component
    └── observablehq.config.js

[Build]
    observable build → dist/ (static site)
    Python data loaders execute during build → produce JSON
    Observable JS renders interactive charts from JSON
```

- **Data loaders**: Python scripts that run at build time, can import 1costingfe, produce JSON
- **Reactive cells**: Observable JS cells with automatic dependency tracking
- **Visualization**: D3 is first-class; Plot (Observable's charting library) for common chart types
- **Deployment**: Static dist/ folder; also supports Observable Cloud hosting

### What Would Need to Be True

- node/npm is acceptable in the toolchain (Observable Framework requires it)
- Observable's reactive model can handle the complexity of comparison views with multiple concepts
- D3 or Observable Plot can produce the tornado chart, CAS breakdown, and comparison layouts needed
- A JS cost model (or pre-computed sweep data) exists for slider functionality
- The team is willing to learn Observable's reactive JavaScript idiom

### Biggest Challenges

1. **Learning curve**: Observable's reactive JavaScript is different from both traditional JS and Python. The reactive cell model has its own idioms and gotchas.
2. **Slider computation**: Same as other static approaches — need a JS cost model for live recalculation. Observable's data loaders run at build time, not at interaction time.
3. **Toolchain**: Requires node/npm alongside Python/uv.
4. **Framework maturity**: Observable Framework is relatively new (v1 released 2024). Community and documentation are growing but not as deep as React/Svelte.
5. **Custom components**: Building the information-dense layout with hover cards, side-by-side panels, and narrative integration requires significant D3/HTML work within Observable's framework.

### Pros

- **Built for data exploration**: Observable Framework is purpose-built for exactly this kind of work — data loaders, reactive updates, interactive charts.
- **Python data loaders**: Can run Python scripts (including 1costingfe) at build time to produce data. Natural bridge between Python backend and JS frontend.
- **D3 is first-class**: No wrapper library friction — write D3 directly.
- **Observable Plot**: High-level charting library that handles common patterns (bar charts, scatter plots) with minimal code.
- **Reactive updates**: Change a slider → all dependent charts update automatically. No manual event wiring.
- **Static output**: Builds to static files, deployable anywhere.
- **Markdown-based authoring**: Pages are Markdown with embedded JS cells — easy to mix narrative and code.

### Cons

- **Requires node/npm**: Toolchain expansion.
- **Learning curve**: Observable's reactive model is unfamiliar to most developers.
- **Slider computation needs JS model**: Same challenge as other static approaches.
- **Newer framework**: Less ecosystem support, fewer examples, potential for breaking changes.
- **Layout flexibility**: Observable Framework pages are primarily vertical scroll — achieving the dense dashboard layout requires custom CSS work.

### Key Assessment

**Purpose-built for this problem space** — data exploration with reactive updates, Python data integration, and D3 visualization. The best "right tool for the right job" argument. The Python data loader feature elegantly bridges the Python/JS gap for build-time computation. Main concern is the learning curve and toolchain expansion. If the team is willing to invest in Observable's paradigm, this could produce the most natural and maintainable solution for Layers 1-3. Slider computation (Layer 4) still requires a JS cost model, same as other static approaches.

### Subagent Critique Summary

**Validated**: Observable Framework is genuinely purpose-built for this problem. Python data loaders and Markdown-based authoring are real advantages. D3 as a first-class citizen is significant.

**Missed/underweighted**: (1) **The learning curve is worse than "unfamiliar"** — for a single-user project where the user is also the developer (via Claude), the reactive cell model investment competes directly with time spent on actual research. Observable's module system, D3 integration patterns, and deployment model are all unfamiliar territory. (2) **Operational overhead of a second package manager** is significant: `package.json`, `node_modules/`, lock file conflicts, and JS ecosystem security updates create a parallel dependency universe that doesn't exist today. (3) **Observable Cloud lock-in risk**: the framework is open-source but the company monetizes through hosted services — docs/examples nudge toward Observable Cloud. Not a problem today but means swimming against commercial incentives. (4) **Parameterized routes (`concept/[id].md`) are powerful but rigid** — when the data schema evolves (parameter categories don't exist yet, reduced profiles are TBD), templates must evolve in lockstep, and template changes are in a different language than the data pipeline.

**Key counter-argument**: Approach B with Jinja2 delivers 80% of what Observable delivers, without node/npm, without the learning curve, and with templates in the same language as the data pipeline. Observable's reactive runtime is elegant, but for 8-13 concepts with infrequent updates, "rebuild the static site" is fast enough that reactive client-side updates may be solving a problem that doesn't need solving at Layers 1-3.

**Verdict**: Prototype only if genuinely interested in learning Observable's paradigm; otherwise, Approach B with Jinja2 gets to the same Layers 1-3 destination with less disruption.

---

## Approach I: Hybrid — Static Visual Shell + Python Computation Server

### Description

Split the tool into two parts: a lightweight static frontend for visualization and navigation, and a tiny Python backend that wraps 1costingfe for live computation. The frontend is a single HTML file (or small set of files) with embedded JS; the backend is a minimal FastAPI/Flask server that exposes a `/compute` endpoint. For non-slider use cases, the frontend works standalone with pre-computed data.

### General Architecture

```
[Static Frontend]
    explorer.html (or small set of HTML files)
    ├── Embedded JSON data for pre-computed sensitivities, CAS breakdowns
    ├── D3/Plotly for visualization
    ├── Slider controls that POST to backend
    └── Graceful degradation: sliders disabled if backend not running

[Python Backend (optional)]
    server.py — minimal FastAPI app
    ├── POST /compute — receives parameters, calls model.forward(), returns JSON
    ├── POST /sensitivity — receives parameters, calls model.sensitivity(), returns JSON
    └── GET /concepts — returns available concept list with metadata

[Startup]
    uv run python server.py    # Launches backend on localhost:8421
    # Then open explorer.html in browser
    # OR just open explorer.html without server for read-only mode
```

- **Graceful degradation**: Frontend works without server (pre-computed data, no sliders). With server, sliders light up.
- **Computation**: All cost model computation stays in Python — no transpilation
- **API contract**: Simple JSON request/response; easy for the /manage-concept agent to call too
- **State sharing**: Backend can expose a GET /state endpoint with current slider positions — agent reads this

### What Would Need to Be True

- Users accept running a local server for slider functionality (or are happy with read-only mode without it)
- FastAPI/Flask request latency + 1costingfe.forward() < 500ms for acceptable slider responsiveness
- The backend API becomes the canonical computation interface (agent and frontend both use it)
- CORS and localhost networking "just works" for the user's browser + server combo

### Biggest Challenges

1. **Two-process coordination**: User must start the server AND open the HTML. Small friction but real.
2. **CORS configuration**: Browser security policies for localhost can be finicky.
3. **State synchronization**: Frontend and backend must agree on which concept is active and what parameters are set.
4. **Graceful degradation UX**: The experience difference between "with server" (full interactivity) and "without server" (read-only) must be clearly communicated.
5. **Deployment complexity**: Sharing the tool requires sharing both frontend files and the Python server setup.

### Pros

- **Best of both worlds**: Professional static frontend + authentic Python computation.
- **No cost model transpilation**: Python stays Python; JS stays JS.
- **Agent integration is natural**: The `/manage-concept` agent can call the same API endpoints.
- **Graceful degradation**: Useful even without the server running.
- **Clean API contract**: JSON over HTTP — universal, testable, debuggable.
- **Incremental**: Start with static frontend (Layers 1-3), add server later (Layer 4).

### Cons

- **Two-process UX**: Starting a server is friction, even if minimal.
- **CORS headaches**: Localhost cross-origin requests can be tricky.
- **Not portable**: Can't just send someone an HTML file and have sliders work.
- **Server dependency for key feature**: The most impressive feature (live sliders) requires the server.
- **More moving parts**: More things that can break, more to document, more to maintain.

### Key Assessment

**Pragmatic architecture** that cleanly separates concerns and avoids the hardest technical challenge (JS cost model transpilation). The API-based computation layer is reusable by the agent, making this the most natural fit for the tool + agent complementarity described in the concept document. The two-process startup is the main UX friction — could be mitigated with a single launcher script (`uv run python launch.py` that starts server + opens browser). Consider this as the **production architecture** if sliders are a must-have and cost model fidelity is non-negotiable.

### Subagent Critique Summary

**Validated**: The API-as-canonical-computation-interface insight is "the strongest point in the entire document." This is the only approach where agent integration (Layer 5) falls out naturally from the architecture. The incremental delivery path (static frontend for Layers 1-3, add server for Layer 4) is realistic.

**Missed/underweighted**: (1) **CORS is not a configuration annoyance — it's an architecture change.** A single-file HTML opened via `file://` cannot fetch() to `localhost:8421`. The realistic architecture is: **FastAPI serves both static files AND /compute endpoint**. One `uv run python server.py` starts everything, user opens `http://localhost:8421`. This is cleaner than described but eliminates the "just open the HTML file" local-use graceful degradation. The static-only mode only works when hosted elsewhere (GitHub Pages). (2) **Latency threshold is too generous.** The document says 500ms is acceptable for sliders — real UX needs <100ms for drag-feel, which means **debounced slider input** (compute on release or after 200ms pause). This is solvable but must be designed in. (3) **The static frontend IS the bulk of the work** regardless of whether the server exists. The document frames the frontend as "lightweight" — it requires the same D3/Plotly, JSON schema, and template work as Approach B. The hybrid architecture doesn't reduce frontend effort; it only changes Layer 4 from "JS cost model" to "API calls." (4) State management between frontend and backend (per-concept slider state, comparison set, agent state exposure) requires design decisions the document glosses over.

**Strongest cross-approach insight**: "Approach I is Approach B with a server bolted on for Layer 4." If building Layers 1-3 as a static site anyway, the question is whether the Layer 4 server addition is worth the complexity. For a researcher who will use sliders heavily to build intuition, the answer is probably yes. The natural sequence is: **build B for Layers 1-3, promote to I for Layer 4.**

**Verdict**: Build this — but recognize the frontend is the bulk of the work, so start there. The server is the straightforward part.

---

## Final Pass: Missed Ideas, Combinations, and Emergent Patterns

After examining all nine approaches and three rounds of critique, several patterns and missed ideas emerge.

### Cross-Cutting Insight 1: The Frontend Work Is Constant

The critiques independently converged on the same observation: **Layers 1-3 require the same frontend effort regardless of architecture choice.** The JSON schema, D3/Plotly chart components, page templates, and data extraction pipeline must be built whether the final tool is a static site (B), a Marimo notebook (F), a hybrid (I), or an SPA (E). The real decision is about Layer 4 computation (JS transpilation vs. Python server vs. reactive notebook) and the toolchain (Python-only vs. adding npm).

### Cross-Cutting Insight 2: The Data Extraction Problem Is Under-Scoped

Multiple critiques flagged that **model_output.txt is a human-readable text format, not a data interchange format.** The model_setup.py files diverge structurally — costingfe-backed concepts are ~200-line wrappers, standalone concepts (dipole, acoustic ICF) are 1100+ lines with custom formatting. The real solution is a **structured JSON output mode** from the pipeline — either by adding a `--json` flag to model_setup.py execution, or by adding a pipeline stage that calls `model.forward()` and serializes `result.costs`, `result.power_table`, and `result.cas22_detail` directly. This is a prerequisite for ANY approach except G (agent-first), and should be the first work item.

### Cross-Cutting Insight 3: The Parameter Metadata Problem Is the Hardest Content Work

The concept-explorer.md vision (US-5) requires detail cards with baseline values, source citations, ranges, confidence, category labels, and modeling mechanism descriptions. **This metadata doesn't exist in any machine-readable form.** For 8 concepts × ~35 parameters, that's ~280 metadata records to author. This is a major content effort that is prerequisite for Layers 2-3 regardless of architecture. The format decision (Open Question 1 in the concept doc) must be resolved early — likely a `model_metadata.yaml` per concept alongside model_setup.py.

---

### Approach J (NEW): Marimo Core + Static Export for Sharing

**Emerged from**: Critique of F (Marimo's strengths) + Critique of B (portability) + Critique of I (agent integration)

#### Description

Use Marimo as the **primary development and daily-use tool** (F), but add a **static HTML export pipeline** that periodically snapshots the current state as a read-only static site (borrowing from B). The Marimo notebook is the source of truth; the static export is a sharing/archival artifact.

```
[Marimo Notebook — daily driver]
    concept_explorer.py
    ├── Live sliders (1costingfe direct import)
    ├── Reactive comparison views
    ├── Parameter detail cards
    └── Entry view with concept grid

[Export Script — periodic or on-demand]
    uv run python export_static.py
    ├── Calls model.forward() for all concepts → JSON
    ├── Renders Jinja2 templates → dist/ (static HTML + Plotly charts)
    └── Pre-computed data only (no sliders in static version)

[Agent Integration]
    Marimo server exposes state via custom route or state file
    /manage-concept agent reads state, calls same 1costingfe API
```

#### Architecture

- **Marimo is the daily instrument**: Full interactivity, live computation, reactive updates. Launched via `uv run marimo run concept_explorer.py`.
- **Static export is the snapshot**: Periodically generate a read-only static site from the same data. No sliders, but all pre-computed views (profiles, tornado charts, CAS breakdowns, comparisons). Shareable, archivable, opens in any browser.
- **Shared data layer**: Both the Marimo notebook and the export script read from the same structured JSON (produced by the data extraction prerequisite). The Marimo notebook additionally calls 1costingfe for live computation.
- **Agent integration through Marimo**: When running the Marimo app, state is accessible to the `/manage-concept` agent. The static export doesn't need agent integration (it's for archival/sharing).

#### What Would Need to Be True

- Marimo's layout capabilities are sufficient for the daily-use tool (critique of F suggests they are, at ~70% of the aesthetic ceiling)
- The static export templates are simple Jinja2 (no new framework — reuses the JSON schema from the data extraction layer)
- The data extraction pipeline (JSON output from 1costingfe) is the shared foundation for both modes

#### Why This Combination Works

- **Eliminates the "prototype vs. production" dilemma**: Marimo IS the production tool for the single-user daily workflow. The static export serves the secondary need (sharing, archiving) without forcing the primary tool to be static.
- **No JS cost model ever**: Live computation stays in Python (Marimo). Static views use pre-computed data. The transpilation problem is eliminated entirely.
- **Incremental**: Start with Marimo-only (Layer 1-4 in one tool). Add static export later when sharing becomes a need.
- **Natural agent integration**: Marimo runs a local server, state is accessible. The `/manage-concept` agent calls the same 1costingfe Python API.
- **Python-only toolchain**: No npm, no node. `uv add marimo` and done.

#### Biggest Risks

- Marimo's layout ceiling is genuinely blocking for comparison views (mitigated by the critique's finding that it's better than initially assessed)
- Two output modes (Marimo + static) means maintaining two rendering paths (mitigated by shared JSON data layer)
- If the static export becomes the primary use mode, you've built two tools when one would have sufficed (monitor usage patterns)

---

### Approach K (NEW): Progressive Enhancement — Claude HTML → Jinja2 SSG → FastAPI Backend

**Emerged from**: Multiple critiques noting the natural upgrade path A → B → I

#### Description

Rather than choosing one approach upfront, **design for progressive enhancement** — start with the simplest approach that delivers value, and evolve the architecture as needs grow. Each stage reuses work from the previous stage.

```
Phase 1 (this week): Approach A — Claude-generated HTML
    Single concept profile, validates information architecture
    Artifact: one HTML file per concept, manually reviewed

Phase 2 (next week): Approach B — Jinja2 SSG
    Extract the validated design into templates + JSON
    All concepts rendered consistently from shared templates
    Artifact: dist/ folder with static site

Phase 3 (when sliders needed): Approach I — Add FastAPI backend
    Same static frontend, now served from FastAPI
    /compute endpoint wraps 1costingfe.forward()
    Sliders light up, agent integration via same API
    Artifact: uv run python server.py → full interactive tool
```

#### Why This Sequence Works

- **Phase 1 costs almost nothing**: Claude generates one HTML file for one concept in a single session. The output validates (or invalidates) the information architecture, chart types, and data presentation before any infrastructure is built.
- **Phase 2 reuses Phase 1's design**: The validated HTML layout becomes the Jinja2 template. The chart library (Plotly/D3) carries over. The data extraction script is new but shared with all downstream phases.
- **Phase 3 reuses Phase 2's frontend**: The static HTML/JS carries over unchanged. FastAPI wraps the existing 1costingfe code. No new frontend work for sliders — just API calls replacing static data lookups.
- **Each phase is independently useful**: Phase 1 is a review artifact. Phase 2 is a browsable site. Phase 3 is the full interactive tool.
- **Decisions are deferred until informed**: The choice between Plotly and D3 is made during Phase 1 (whichever Claude produces best). The JSON schema is designed during Phase 2 (informed by what Phase 1 needed). The slider UX is designed during Phase 3 (informed by how Phase 2 is actually used).

#### Comparison to Approach J (Marimo Core)

Both J and K avoid the "choose one architecture upfront" trap, but they take different paths:
- **J (Marimo)** bets that the daily-use tool should be a reactive Python notebook, with static export for sharing. Best if live sliders are a primary need from day one and the layout ceiling is acceptable.
- **K (Progressive)** bets that the tool should evolve from static to interactive as the information architecture solidifies. Best if the design needs iteration and the user wants to see something before committing to an architecture.

**J is the faster path to sliders. K is the safer path to the right design.** For this project, both are viable — the choice depends on whether the user's primary anxiety is "will sliders work?" (choose J) or "will the information architecture be right?" (choose K).

---

### Eliminated from Consideration

Based on the critique analysis, the following approaches should be **dropped from further consideration**:

- **Approach D (Pyodide/WASM)**: Pass. Every benefit is delivered more cleanly by other approaches. The JAX blocker is real, the startup latency conflicts with fluid navigation, and this solves a distribution problem the project doesn't have.
- **Approach G (Agent-First) as the primary tool**: Pass as primary. Build as the companion `/manage-concept` agent (epic Item 5), which is its natural role. Not competing with the visual explorer.

### Remaining in Consideration (ranked by critique consensus)

| Rank | Approach | Role | Critique Verdict |
|------|----------|------|------------------|
| 1 | **F (Marimo)** | Daily-driver tool | "Build this first" — strongest endorsement |
| 2 | **J (Marimo + Static Export)** | Daily driver + sharing | Natural extension of F |
| 3 | **I (Hybrid)** | Production architecture | "Build this" — best for agent integration |
| 4 | **B (Static SSG)** | Layers 1-3 foundation | "Build it" — strongest general-purpose |
| 5 | **K (Progressive A→B→I)** | Evolutionary path | Safest path to the right design |
| 6 | **A (Claude HTML)** | Layer 1 proof-of-concept | "Prototype one concept" |
| 7 | **E (SPA)** | Long-term if tool scales | "Only after schema is stable" |
| 8 | **C (Dashboard)** | Rapid slider prototype | "Prototype, then evolve to I" |
| 9 | **H (Observable)** | If learning Observable | "Only if genuinely interested" |

### The Prerequisite Work (Regardless of Architecture)

Every viable approach needs these, so they should be started before committing to a specific architecture:

1. **Structured JSON output from the pipeline** — Add a stage that serializes `model.forward()` results to JSON. This is the data contract for any visualization tool.
2. **Parameter metadata format** — Resolve Open Question 1: define `model_metadata.yaml` schema for parameter categories, confidence, ranges, and narrative context. Author metadata for the first 2-3 concepts.
3. **Profile 1costingfe.forward() latency** — Determines whether live sliders are sub-second (Marimo/Dash viable) or need debouncing (all approaches except pre-computed).
