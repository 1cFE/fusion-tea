
## Purpose
Generate HTML shell pages and copy static assets to `dist/`, producing a complete site ready for the server to serve.

## Requirements
- `build_explorer.py` orchestrates: (1) run extraction → `data/*.json`, (2) render Jinja2 templates → `dist/*.html`, (3) copy `static/` → `dist/static/`
- HTML pages are shells with no inline concept data — all data fetched at runtime via API
- Templates are rendered using Jinja2 with a `static_url()` helper that resolves to `/static/...` paths
- `--data-only` flag skips HTML rendering; `--html-only` skips data extraction; `--concept 01 04` rebuilds only the named concepts
- The build errors if `data/` is empty and `--html-only` is passed
- Build output is deterministic: same input data produces byte-identical output (no timestamps in HTML)

## Acceptance Criteria
- Running `uv run python build_explorer.py` produces `dist/index.html`, `dist/compare.html`, and one `dist/concept/{id}.html` per concept in `data/`
- Each produced HTML file contains a `<script src="/static/js/...">` tag (not inline data)
- `dist/static/js/tornado.js` exists after the build
- Running the build twice with unchanged inputs produces identical output files
- `--html-only` succeeds when `data/manifest.json` exists and fails with a clear error when it does not

## Interfaces
- **File**: `exploration/concept_explorer/build_explorer.py`
- **Reads**: `data/*.json` (produced by `06-data-extraction-pipeline.md`), `templates/*.html.j2`, `static/`
- **Writes**: `dist/index.html`, `dist/compare.html`, `dist/concept/*.html`, `dist/static/`
- **Templates**: `base.html.j2`, `index.html.j2`, `concept.html.j2`, `compare.html.j2`
- **Called by**: developer CLI before starting the server

## Constraints
- NEVER inline JSON data in HTML output — pages are shells only
- NEVER include a `--serve` flag — the server (`server.py`) is the serving mechanism
- `dist/` MUST be fully regenerated on each full build (not incrementally patched)

## Out of Scope
- Data extraction logic (see `06-data-extraction-pipeline.md`)
- CI/CD pipeline integration
- Minification or asset optimization

