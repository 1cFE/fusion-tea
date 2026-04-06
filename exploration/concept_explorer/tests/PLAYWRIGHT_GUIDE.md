# Writing Playwright Tests for Concept Explorer

Reference for agents writing browser-based acceptance tests against the Concept Explorer UI.

## Setup

**Playwright is installed in the project venv.** No extra install needed.

```bash
# Run tests (server must be running separately)
uv run python exploration/concept_explorer/tests/test_views_manual.py

# Start the server (in another terminal or backgrounded)
uv run python -m exploration.concept_explorer.server --port 8765
```

There is no pytest integration — tests are plain Python scripts using `playwright.sync_api`. Run them directly.

## Concept IDs

The explorer uses **analysis IDs** (two-digit strings), NOT taxonomy `concept_id` slugs.

| Analysis ID | Name | Family | Has Cost Model |
|-------------|------|--------|----------------|
| `04` | Laser ICF - p-B11 Fast Ignition | IFE | Yes |
| `05` | Planar Coil Stellarator | MFE | Yes |
| `06` | Magnetic Mirror (p-B11) | MFE | Yes |
| `08` | FRC w/ Direct Conversion | MIF | Yes |

These are the only concepts with data files. The taxonomy registry (`/api/taxonomy/registry`) has 38 concepts by slug (`hts-compact-tokamak`, etc.), but the comparison page manifest only knows about these 4.

**Currently all 4 have cost models.** There is no way to test the "no cost model" UI path without adding a concept to the manifest that lacks one.

URLs use analysis IDs:
- Compare: `/compare?concepts=05,06,04`
- Concept page: `/concept/05`
- API: `/api/concepts/05`

## Comparison Page Architecture

### Two Modes

| Mode | Layout | View Selection |
|------|--------|---------------|
| **Integrated** | Two side-by-side panels (left + right) | `#select-left`, `#select-right` — each is a `<select>` |
| **Landscape** | Per-concept cards in a grid | `#select-landscape` — single `<select>` |

Toggle between modes with `#mode-integrated` and `#mode-landscape` buttons.

### URL Parameters

| Param | Mode | Description |
|-------|------|-------------|
| `concepts` | Both | Comma-separated analysis IDs |
| `left` | Integrated | View key for left panel (e.g., `categorical`) |
| `right` | Integrated | View key for right panel (e.g., `summary`) |
| `view` | Landscape | View key for landscape |
| `mode` | Both | `integrated` or `landscape` |

### View Mutual Exclusion (Integrated Mode)

Left and right panels **cannot show the same view**. The dropdown disables the other panel's current selection. When swapping views between panels, you must use a third view as an intermediate:

```python
# WRONG — "summary" is disabled in left because right already has it
page.locator("#select-left").select_option("summary")  # timeout!

# RIGHT — free up "summary" first by changing right to something else
page.locator("#select-right").select_option("capex")    # intermediate
page.locator("#select-left").select_option("summary")   # now available
page.locator("#select-right").select_option("categorical")
```

Available view keys: `categorical`, `summary`, `capex`, `sensitivity`. Only `categorical` and `summary` have renderers (the others show placeholder text).

### VIEW_REGISTRY

Views register render functions on `window.VIEW_REGISTRY` from separate JS files loaded after `comparison.js`. The shell dispatches to them. Each view file is an IIFE that sets:

```javascript
window.VIEW_REGISTRY.viewname.renderIntegrated = function(container, concepts) { ... };
window.VIEW_REGISTRY.viewname.renderLandscape = function(container, concept, syncContext) { ... };
```

## Key Selectors

### Comparison Page Structure

```
#compare-content              — main content wrapper (visible after load)
#concept-bar                  — concept chips bar
  .badge                      — family badge on each chip (use for "loaded" signal)
#mode-integrated / #mode-landscape  — mode toggle buttons
#compare-integrated           — integrated layout container
  #content-left / #content-right    — panel content areas
  #select-left / #select-right      — view dropdowns
#compare-landscape            — landscape layout container
  #landscape-grid             — card grid
  #select-landscape           — view dropdown
```

### View-Specific Selectors

**Categorical:**
```
table.comparison-table        — integrated comparison table
thead .badge-mfe              — family badges in header
tbody tr.diff / tr.match      — diff-highlighted rows
td.val--na                    — inapplicable field ("—")
td.val--tbd                   — unknown/TBD field
.taxonomy-card__attrs         — landscape attribute card
.taxonomy-card__attr          — single attribute row in card
```

**Summary:**
```
.js-plotly-plot               — Plotly chart (integrated or landscape)
table.comparison-table--summary  — metrics table
.summary-metric-row           — landscape metric row
.view-no-data                 — "no cost model" placeholder
```

## Wait Patterns

### Page Load

```python
def wait_for_compare(page):
    page.wait_for_selector("#compare-content", state="visible", timeout=10000)
    page.wait_for_selector("#concept-bar .badge", timeout=10000)
```

The `.badge` selector confirms concept data has loaded and rendered into the concept bar. Without this, the comparison panels may not have data yet.

### Async View Rendering

Categorical fetches taxonomy data asynchronously. Summary renders Plotly charts. Both need extra wait time after the page load signal:

```python
wait_for_compare(page)
time.sleep(1.5)  # taxonomy fetch for categorical
time.sleep(2)    # Plotly render for summary
```

These are conservative. The taxonomy fetch is fast (~38 concepts from memory), but Plotly subplot rendering can take a moment.

### Mode Switching

After clicking a mode toggle, wait before asserting:

```python
page.click("#mode-landscape")
time.sleep(1)  # DOM rebuild + view render
```

## Console Error Capture

```python
errors = []
page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

# ... do stuff ...

js_errors = [e for e in errors if "favicon" not in e.lower()]
assert len(js_errors) == 0, f"JS errors: {js_errors}"
```

Register the listener **before** the actions you want to monitor. Filter out favicon 404s (common noise).

## Screenshots

Save to `/tmp` for agent review via the `Read` tool (which can display images):

```python
page.screenshot(path="/tmp/view_test_name.png", full_page=True)
```

Use `full_page=True` to capture content below the fold (landscape mode with 4 concepts scrolls).

## Test Script Pattern

```python
from playwright.sync_api import sync_playwright, Page

BASE = "http://127.0.0.1:8765"

def test_something(page: Page):
    print("\n--- Test Name ---")
    page.goto(f"{BASE}/compare?concepts=05,06&left=categorical")
    wait_for_compare(page)
    time.sleep(1.5)

    # Assert DOM state
    table = page.locator("#content-left table.comparison-table")
    assert table.count() == 1, "Expected comparison table"

    page.screenshot(path="/tmp/view_test_something.png", full_page=True)
    print("  PASS")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()
        # run tests...
        browser.close()
```

## Gotchas

1. **Analysis IDs, not slugs.** The compare page uses `04`/`05`/`06`/`08`. Taxonomy slugs like `planar-coil-stellarator` will show "Skipped unknown concept(s)" warning.

2. **Mutual exclusion on dropdowns.** Playwright's `select_option` will timeout on a disabled `<option>`. Always check what the other panel has before selecting.

3. **Landscape uses `view`, not `left`/`right`.** URL param `right=summary` does NOT affect landscape mode. Use `view=summary&mode=landscape`.

4. **Plotly charts need time.** `wait_for_selector(".js-plotly-plot")` finds the container div before Plotly finishes rendering. Add `time.sleep(2)` after page load for chart assertions.

5. **Server must be running.** Tests don't start the server. Start it first on port 8765 (or whatever `BASE` is set to).

6. **Headless Chromium works fine.** No need for `headless=False` unless you want to watch. The dark theme renders correctly in headless mode.

7. **`compare-content` is hidden until JS init.** Don't wait for panel content selectors directly — wait for `#compare-content` visibility first, then `#concept-bar .badge` for data readiness.
