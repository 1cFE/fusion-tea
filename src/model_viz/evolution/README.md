# Model evolution page

One standalone HTML file that steps through the stellarator model's history, one goal at a time. The calc graph is on top, a slider and arrows are beneath it, and under those sit the model's metrics, the goal's question and result, and a list of what the goal changed.

## Build it

```bash
uv run python src/model_viz/evolution/build.py -o stellarator_evolution.html
```

The build takes about three seconds and writes one file of about 9 MB. The file needs no server and no network. Open it with a double-click.

`--data-out data.json` also writes the page's frame data as readable JSON. `--repo <path>` points at any checkout of the repository; the default is the checkout this script sits in. `--manifest <file>` uses a different frame list.

## It never checks anything out

History is read with `git show`, `git diff`, `git log` and `git rev-parse`. These read git's object store and touch no worktree, so the build is safe to run while other sessions work in any checkout. Every worktree of a repository shares one object store, which is why a build on this branch can read commits from `fix/modeling-intent-after-reveal`. `tests/model_viz_evolution/test_page.py` checks that `git status` is the same before and after a build.

## Using the page

- **◀ ▶, the slider, the left and right arrow keys, and the goal list** each move between frames. The address bar's `#goal-slug` follows, so a link can open on one goal.
- **Frame 1 is the starting model.** Each later frame is one goal, shown as the model stood when that goal's last change landed.
- **Green halo: a new calc. Amber: a changed calc. Violet: a moved calc.** A closed part wears the halo of the calcs it hides. **Open changed parts** opens those parts, and keeps doing so as you step.
- Parts you open stay open when you step to another frame. Each frame gets a fresh layout, so boxes do move between frames.
- **Expand** gives the graph the whole window. The stepping bar and the legend stay along the bottom, with one line saying what the goal changed, so you can keep stepping. The side panel gives its width back until you select a calc or a part. **Collapse** or Esc goes back. **Full screen** does the same and also asks the browser for full screen; if the browser refuses, you still get the full-window view.
- **The tiles** show six counts, the change since the previous goal, and a small step chart of the whole history. Hover the chart for any goal's value; click it to jump there.
- **The change list** names every marked calc. A calc name is a link: it opens the calc's part, centres it and shows its panel. A changed calc lists its rewired inputs (`p_pump_total_in: calc primary_loop → calc cooling_energy`), its added and removed inputs, and its formula before and after.
- **"handwritten body"** marks a calc whose executable body is handwritten Python. Expand it to read the body, or to see what changed in it.

## What a frame is

The viewer reads one file, `exploration/stellarator_e2e/stellarator.snapshot.json`. Git holds 57 versions of it. The 47 from 2026-08-21 onward are `instance-graph/v3`, which the viewer reads; the ten July versions are an older format it refuses. Every model edit since that date was followed by a commit that regenerated the snapshot, so these versions are the model's complete history.

`frames.json` assigns each version to the goal that produced it. A goal with several versions is one frame, and its change list covers all of them. Goals that changed no model version are not frames.

The build refuses, and writes nothing, when the manifest and git disagree: a version between the baseline and the last frame that no frame lists, a listed commit that is not a snapshot version, or versions out of order. An unlisted version's changes would otherwise land silently in the next goal's list.

A version that is deliberately not a frame goes under `unframed` with its reason. There is one: `5dd9cbd0` (stellaris-reference-reconciliation), whose only model change is source-attribution comments.

## How changes are found

Calcs are matched on `display_path`. A path that disappears while the same calc name appears elsewhere is a move; the structural decomposition relocated 44 calcs into parts this way. A calc has changed when its formula lines, its expression tree, its outputs or what feeds its inputs differ. Feeds are compared by the feeding calc's or attribute's name, because ids and paths embed the owning part and would make every moved calc look edited. The doc comment codegen appends to the formula lines is compared separately, as "documentation changed only".

**The snapshot holds no body for a handwritten calc.** For a `manual_required` calc it records the input bindings and the doc comment, and `expression_ir` is null. The executable math is committed under `exploration/stellarator_e2e/generated/handwritten/`. So the build has a second source: `git diff` over that directory. A calc maps to its file by name (`mfe_cooling_equipment::'Cooling Equipment'` → `mfe_cooling_equipment/cooling_equipment_impl.py`); on the 47 versions this resolves 1,007 of 1,007 handwritten calcs. Codegen rewrites a `SysML Source: file:line` comment in these files whenever lines shift, so a diff that changes nothing else is ignored. Measured on the 47 versions, the snapshot alone catches 51 of 60 real body edits; the git diff catches the other nine, which the page lists as "Python body changed, model record unchanged".

The snapshot also carries no computed values, so the page shows no LCOE. Figures in a frame's result text come from the goal's own written answer.

## Where the words come from

- **Question:** verbatim from the goal's `goal.md` § Question, with the provenance grade written there. Many early questions are agent-worded and owner-ratified; the page says so rather than presenting them as the owner's words. Some goals record no grade, and the page says that too.
- **Result:** condensed by an agent from the goal's `answer.md`, or from the trail's close entry when there is no answer file. The source path is printed under it. It is presentation text: if it disagrees with its source, the source wins.
- **`closed`:** the date of the owner's close ruling. Nine goals have none, and the page shows "not formally closed".
- **`attribution` and `notes`** in `frames.json` record why each version belongs to its goal, with a file and line. They are for review and are not shown on the page.

## Adding a goal

1. Find the new snapshot versions: `git log --format='%h %ad %s' --date=short <last sha in frames.json>..<branch> -- exploration/stellarator_e2e/stellarator.snapshot.json`.
2. Append a frame to `frames.json` with those shas in order, the question copied from `goal.md`, and a result condensed from `answer.md`.
3. Rebuild. A refusal names any version you missed.

## It does not edit the viewer

The page is the v2 viewer, inlined by `export.py`'s own functions, plus `timeline.js` and `timeline.css`. The layer uses only what v2 exposes on `window.modelVizApp`: `cy`, `model`, `state`, `loadText`, `toggleContainer`, `resetLayout` and `navigateTo`. v2's file picker is hidden by the layer's stylesheet, not removed from v2.

One thing reaches past that surface. v2 re-runs its layout on every part it opens, so opening several parts would lay out several times. `timeline.js` stubs `cy.layout` while it toggles the parts, then calls v2's `resetLayout` once. If v2 changes how it lays out, look at `openParts` first.

## Files

- `build.py` — reads git, computes each frame's changes and metrics, embeds everything. The top half is pure functions.
- `frames.json` — the frame manifest: which commits belong to which goal, and each goal's words.
- `timeline.js` — the layer: stepping, graph marks, tiles, summary, change list.
- `timeline.css` — its styles. Light only, as v2's canvas colours are fixed light values.

Snapshots and frame data are embedded as gzip then base64, and unpacked with the browser's `DecompressionStream` (Chrome 80, Firefox 113, Safari 16.4, or newer). The 29 embedded snapshots are about 58 MB of JSON and embed as about 8 MB.

## Tests

```bash
uv run python -m pytest tests/model_viz_evolution
```

`test_diff.py` checks the pure functions on small synthetic graphs. `test_page.py` builds the page and drives it in headless Chromium; its numbers are checked against an oracle that reads each snapshot from git and counts for itself. Run this battery on its own, and `tests/model_viz` and `tests/model_viz_v2` on their own: each starts its own Chromium, and two in one pytest process collide.

The three marked hues (`#1baf7a`, `#eda100`, `#4a3aa7`) passed the dataviz palette validator on all pairs for colour-vision separation (worst ΔE 9.1, protan). Two fall below 3:1 contrast on the canvas, which is why every marked calc is also named in the change list.

## Write-up page

The integrated article is generated from the approved markdown, with the viewer first and six visible themes below it. This keeps the chronological controls together while the left contents rail lets a reader go straight to a theme. Frame references select the corresponding graph state. The closed frame-record table retains counts and result condensations without JavaScript; the result condensations remain explicitly unreviewed.

From the repository root:

```bash
uv run --no-sync python src/model_viz/evolution/build.py \
  --article docs/write-up/stellaris-evolution.md \
  -o docs/write-up/stellaris-evolution.html
```

Open `docs/write-up/stellaris-evolution.html` directly, or serve the repository. Publish it beside `write-up.css` and the other supports. The viewer and its snapshots are embedded; only the shared CSS and its permitted fonts are external to the HTML. The original standalone command still works without `--article`.

Imported from `feat/model-viz-evolution@6a4d241d`: evolution work in `becf7ea3` and `6a4d241d`, with its structural/v2 dependencies at `b814d7d6`. The viewer and exporter sources are unchanged from that revision. The integration changes only the evolution layer, adds article rendering and tests, and leaves the source markdown and shared stylesheet unchanged.

The top action row offers **Expand viewer** and **Full screen**. **Show structure** is the former **Expand all** control with the same behavior. An empty inspector gives its width back to the graph until a part or calculation is selected. The article uses the shared `mark.skim` treatment from `harness.html` for six selected passages, including the owner-selected explanation of how a sweep reveals a missing physical constraint.

The narrative follows the viewer as one section, “Six themes in the model’s evolution,” with six numbered subsections. The contents rail mirrors that hierarchy, and the introductory sentence stays with the group at normal reading size. A separate “Model limits” section contains the closing domain limitations and frame records.
