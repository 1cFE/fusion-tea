# Score Explorer

Interactive UI for the 7-axis fusion-concept scoring framework. Adjust
axis weights with sliders, watch the rankings re-compute client-side in
real time, drill into per-axis diagnostics for any concept, and export
the active ranking + weights as CSV/JSON.

## Architecture

```
tools/score_explorer/
├── README.md          (this file)
├── build.py           Python script — reads scoring_v2 output → data/*.json
├── index.html         Single-page app (vanilla React + Recharts via CDN)
└── data/
    ├── concepts.json  Per-concept scores, evidence, features, diagnostics
    └── weights.json   Per-axis weight + sub-tables
```

**No build step.** React 18, Recharts, Babel-standalone all load from
CDN — no `npm install`, no bundler, no transpiler.

## Workflow

1. **Edit** weights in `exploration/scoring_v2/weights/default.yaml` (if you
   want to change axis-internal lookup values — bottleneck severities, mvs
   lookups, etc.). Skip this step if you only want to play with the seven
   composite-level axis weights — that's a UI slider.
2. **Re-score** the corpus:
   ```bash
   uv run python exploration/scoring_v2/score.py
   ```
3. **Rebuild** the data files:
   ```bash
   uv run python tools/score_explorer/build.py
   ```
4. **Serve** `tools/score_explorer/` over HTTP and open `index.html`:
   ```bash
   cd tools/score_explorer
   python -m http.server 8000
   # open http://localhost:8000/
   ```

   (The CDN-loaded React requires `http://` rather than `file://` due to
   CORS on the JSON `fetch()` calls.)

## What the UI gives you

### Sidebar

* **Presets** — three named weight profiles: Equal, Physics-first
  (Technical Feasibility × 2), Commercial-first (Modularity + Supply
  Chain + Plant Complexity × 1.5). Clicking one resets all sliders.
* **Seven axis-weight sliders** — range 0–3, step 0.05. Slider moves
  trigger immediate client-side composite re-computation. The composite
  formula matches `score.py`: weighted mean over non-null axes, with
  null axes skipped + remaining weights renormalized.
* **Advanced (sub-tables)** — read-only expansion showing each axis's
  internal lookup tables (mvs lookup, bottleneck severities, bracket
  schedules, etc.). To edit these, modify `weights/default.yaml` and
  rerun the workflow.
* **Export CSV / Export JSON** — downloads the current sorted ranking
  with the active weight vector.

### Main pane

* **Filter bar** — search by name/ID, filter by fuel, filter by
  confinement family.
* **Ranking table** — sortable by every column. Composite is the
  default sort (descending). Bars show relative score; color codes
  by tier (red = 1, orange = 2, white = 3, green = 4–5).
* **Concept detail** — click a row to expand: feature subset (fuel,
  blanket, etc.) + per-axis diagnostic block from the feature file.
  Composite shows how many of 7 axes contributed (skip-rescale honesty).

## What's client-side vs server-side

| Action | Where | Latency |
|---|---|---|
| Adjust axis weight slider | Client | <100 ms |
| Switch preset profile | Client | <100 ms |
| Filter / sort table | Client | <100 ms |
| Click concept for detail | Client | <100 ms |
| Edit axis-internal lookup tables | Server (Python) | Edit YAML → re-run score.py + build.py |
| Add a new concept | Server (Python) | Re-extract features → score.py → build.py |

Composite-level tuning (the seven sliders) is the fast iteration loop.
Within-axis recalibration (the sub-tables behind "Advanced") goes
through the deterministic Python framework so the changes are
recorded in git, not ephemeral.

## Determinism + reproducibility

* The score values in `concepts.json` are exactly what `score.py`
  emitted. The UI never recomputes axis scores — only the composite
  weighted-mean over those scores.
* Recomputing the composite with the slider weights produces the
  same value `score.py` would emit if you wrote those weights to
  `weights/default.yaml` and re-ran the framework.
* `composite_axes_included` matches between the UI and the Python
  framework (both use the same skip-and-rescale logic).

## Limitations / future

The "save & re-score" round-trip described in
`integrated_implementation_plan.md` (write new weights → invoke
`score.py` → reload) requires a tiny local HTTP server with a write
endpoint. The current implementation is client-only — sliders adjust
the *composite weights*, but any deeper edits (bottleneck severities,
mvs lookup values, bracket boundaries) require manually editing
`weights/default.yaml`. Adding a tiny Flask/aiohttp wrapper is a
future iteration.
