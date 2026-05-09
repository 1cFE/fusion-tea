---
name: browser-inspect
description: >
  Drive a real browser to inspect a web UI — take screenshots, click buttons, fill inputs,
  read element text, run JS, and capture console errors. Use whenever you need to SEE what
  a page renders, VERIFY a UI change took effect, REPRODUCE a click-driven bug, check that
  a slider / chart / form actually works, or sanity-check before committing frontend changes.
  Triggers: "screenshot the explorer", "look at the page", "what does it render", "click and
  re-screenshot", "check the slider", "is the chart showing", "verify the UI", "any console
  errors", "open localhost:8421", "see what concept 19 looks like", "test the comparison view",
  "check this HTML page", "did the button do anything", any browser/UI verification request.
allowed-tools: Bash, Read, Glob, Grep
user-invocable: false
---

# Browser Inspect

Drive a Chromium browser via `scripts/browser_inspect.py` (chained-flag CLI wrapping Playwright). Each shot writes a PNG **plus** a JSON sidecar with URL, title, console messages, and page errors — so you can verify UI behavior without re-running the script for every check.

## When to Use This

Use this skill instead of asking the user to screenshot, instead of guessing what a page looks like, and instead of editing-without-verifying for any UI change.

Specifically, reach for it when you need to:
- See what a page renders right now (the home grid, a concept profile, the comparison view)
- Verify a change you just made (CSS tweak, template edit, JS fix) actually shows up
- Reproduce or check a multi-step bug (click → expand → re-screenshot → confirm state)
- Check whether console errors or failed fetches are happening on a page
- Read a value off the page (e.g., the LCOE number after a slider drag) without screenshotting

If the user asks "does X work in the browser" or "what does Y look like", run this skill — don't speculate.

## Core Workflow

```
1. Make sure the server is running        (e.g., uv run python exploration/concept_explorer/server.py)
2. Run scripts/browser_inspect.py with chained step flags
3. Read the resulting PNG(s) to see the UI
4. Read the JSON sidecar(s) to check console / errors / DOM state
5. If something's wrong, edit and re-run with --clear
```

Always Read the JSON sidecar even when the PNG looks fine — console errors are invisible in screenshots and frequently explain "why is this chart blank" or "why didn't the slider update."

## Command Reference

Invoke as:
```bash
uv run python scripts/browser_inspect.py [--base URL] [--session NAME] [--clear] STEP_FLAGS...
```

Step flags execute in command-line order. Mix freely:

| Flag | Argument | What it does |
|---|---|---|
| `--goto` | `PATH` or full URL | Navigate. Path is appended to `--base`. Waits for networkidle + 800ms (configurable via `--default-wait`). |
| `--shot` | `NAME` | Full-page PNG → `NAME.png` + sidecar `NAME.json`. |
| `--shot-vp` | `NAME` | Viewport-only PNG (faster for above-the-fold checks). |
| `--click` | `SELECTOR` | Click first matching element. 5s timeout. |
| `--fill` | `SELECTOR=VALUE` | Type VALUE into an input. |
| `--press` | `SELECTOR=KEY` or `KEY` | Press a key on an element, or globally. |
| `--hover` | `SELECTOR` | Hover (useful for tooltip-revealed UI). |
| `--wait` | `MS` | Sleep N milliseconds (use after click → wait for animation). |
| `--wait-for` | `SELECTOR` | Wait until element is visible (10s timeout). Better than `--wait` when you can name the thing. |
| `--scroll-to` | `SELECTOR` | Scroll element into view (then maybe `--shot-vp`). |
| `--read` | `SELECTOR` or `SELECTOR=NAME` | Capture element text into `reads.json`. NAME labels it; defaults to the selector. |
| `--eval` | `JS_EXPR` | Run a JS expression, capture the result into `evals.json`. Returns must be JSON-serializable. |

Session-wide flags:

| Flag | Default | Notes |
|---|---|---|
| `--base` | `""` | URL prefix for relative `--goto` paths. Set this once per invocation. |
| `--session` | `default` | Output goes to `/tmp/browser_inspect/<session>/`. |
| `--out` | — | Override the output dir entirely. |
| `--viewport` | `1600x1100` | `WxH`. |
| `--dpr` | `2` | Device pixel ratio. Higher = sharper, ~4× file size. |
| `--default-wait` | `800` | ms to wait after networkidle on each `--goto`. Bump for slow chart renders. |
| `--clear` | off | Delete the session dir before running. **Use this when iterating** so old artifacts don't confuse you. |
| `--quiet` | off | Suppress per-step prints. |

Selectors are Playwright's standard CSS + extensions: `button:has-text('Expand')`, `text=LCOE`, `[data-testid=foo]`, etc.

## Conventions

### Output location

Everything goes under `/tmp/browser_inspect/<session>/`. For each session you get:

```
/tmp/browser_inspect/<session>/
├── <name>.png            # one per --shot
├── <name>.json           # sidecar per shot: url, title, console (cumulative), page_errors
├── reads.json            # all --read captures, in order
├── evals.json            # all --eval results, in order
├── session.json          # full step log + artifact list (always written, even on failure)
└── _fail_NN_<kind>.png   # auto-captured viewport shot if a step throws
```

Pick session names that name the *thing being tested*, not the iteration:
- Good: `--session concept-19-slider`, `--session compare-tab-render`, `--session entry-grid`
- Bad: `--session test1`, `--session shot`, `--session try`

Use `--clear` when re-running the same session — otherwise old shots from a previous run linger and you'll Read stale images.

### Sidecar > re-screenshotting

Before adding another `--shot`, ask: do I actually need a new picture, or can `--read` / `--eval` answer this?

- "Did the LCOE display update?" → `--read ".headline-lcoe"` (one number, no screenshot needed)
- "Are there any console errors?" → look at the most recent shot's sidecar `console` field
- "Is the comparison set state correct?" → `--eval "JSON.parse(localStorage.getItem('comparison'))"` 
- "Did this button get re-enabled?" → `--eval "!document.querySelector('#btn').disabled"`

Screenshots are slow (1-3s each) and you have to Read them. Sidecars are cheap and exact.

### Failure handling

If any step throws, the script writes a `_fail_NN_<kind>.png` viewport screenshot of the page state at failure, sets exit code 2, and still writes `session.json`. Read both — the sidecar shows what console errors led up to the failure, the screenshot shows the visible state.

### When the server isn't running

The script will fail with a goto error. The fix is always: start the server first, then re-run. For the concept explorer specifically:
```bash
uv run python exploration/concept_explorer/server.py &
# wait ~2s for startup
uv run python scripts/browser_inspect.py --base http://localhost:8421 ...
```

## Examples

### A. Quick: "show me the home grid"

```bash
uv run python scripts/browser_inspect.py \
    --base http://localhost:8421 --session home --clear \
    --goto / --shot grid
```
Then `Read /tmp/browser_inspect/home/grid.png` and `Read /tmp/browser_inspect/home/grid.json`.

### B. Verify a fix: "did the parameter card render?"

```bash
uv run python scripts/browser_inspect.py \
    --base http://localhost:8421 --session param-card --clear \
    --goto /concept/19 \
    --click ".tornado-bar:first-child" \
    --wait-for ".parameter-card" \
    --shot card-open \
    --read ".parameter-card .display-name=name" \
    --read ".parameter-card .baseline-value=baseline"
```
Read `card-open.png` for the visual, `card-open.json` for any console warnings, `reads.json` for the captured text.

### C. Slider behavior: "does dragging the magnet-cost slider change LCOE?"

```bash
uv run python scripts/browser_inspect.py \
    --base http://localhost:8421 --session slider-magnet --clear \
    --goto /concept/19 \
    --read ".headline-lcoe=lcoe_baseline" \
    --eval "document.querySelector('input[name=cost_per_kg_hts]').value=200; document.querySelector('input[name=cost_per_kg_hts]').dispatchEvent(new Event('input', {bubbles:true}))" \
    --wait 500 \
    --read ".headline-lcoe=lcoe_after" \
    --shot after
```
Compare `lcoe_baseline` vs `lcoe_after` in `reads.json`. If they're identical, the slider isn't wired up.

### D. Multi-page tour with shared base

```bash
uv run python scripts/browser_inspect.py \
    --base http://localhost:8421 --session tour --clear \
    --goto / --shot home \
    --goto /concept/04 --shot c04 \
    --goto /concept/19 --shot c19 \
    --goto "/compare?concepts=04,19&mode=integrated" --shot compare
```
Single browser instance, one screenshot per page. Then Read each.

### E. Reading from the JSON sidecar

After running, the most useful checks are:

```bash
# any errors anywhere in the session?
cat /tmp/browser_inspect/<session>/session.json | jq '.page_errors_count, .console_count'

# what console messages appeared?
cat /tmp/browser_inspect/<session>/<last-shot>.json | jq '.console'

# what did --read capture?
cat /tmp/browser_inspect/<session>/reads.json
```

## Anti-patterns

- **Don't skip the JSON sidecar.** A page can render fine *and* be throwing console errors that explain a missing chart. Always glance at `console` and `page_errors` after a shot.
- **Don't `--shot` between every step "just in case".** Each PNG is ~200KB-2MB, takes a second to Read, and you're paying tokens for the image. Use `--read` and `--eval` when you only need state, not pixels.
- **Don't omit `--clear` when iterating.** Stale `before.png` from the previous run is a classic source of "wait, my fix didn't do anything" panic.
- **Don't stack `--wait 5000` chains.** Use `--wait-for SELECTOR` so the script proceeds the moment the element appears.
- **Don't rely on `nth-child` / brittle selectors when the project provides `data-testid` or stable classes.** When you find yourself counting `> div > div > span:nth-child(3)`, stop and add a `data-testid` to the template instead.

## Notes

- **Project context**: `scripts/screenshot_explorer.py` is the older, simpler version of this script (single-shot focused). It still works but this skill's driver is a strict superset. Prefer `browser_inspect.py` for new work.
- **Server URL for the concept explorer**: `http://localhost:8421`. Other localhost services use other ports — check with the user or `lsof -i :PORT` if unsure.
- **Playwright timeouts**: 5s for clicks/reads/fills, 10s for `--wait-for`, no script-level timeout. If a page legitimately takes longer, prefer chained `--wait-for` over bumping these.
- **The browser is closed at script exit.** Each invocation is a fresh session. There's no persistent browser mode — keep that in mind if you need to test login flows or stateful navigation (chain everything into a single invocation).
