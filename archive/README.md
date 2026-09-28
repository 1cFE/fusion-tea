# Archive

Historical artifacts retained for reference only. Nothing here is live tooling or canonical data.

## Contents

- `concept-downselect-renumber-crosswalk.csv` — Mallory Snowden's 38→39 ID crosswalk from the `concept-downselect` branch. The renumber was deliberately **not** adopted on `main` (see `.project/reports/2026-05-19-concept-downselect-rebase-audit.md` §4 and PR #16's `6d32f4d`). The crosswalk is preserved here as a historical record of the intended mapping; do not treat it as authoritative for any live tooling. Source: `concept-downselect` branch, `scripts/renumber/crosswalk.csv`.
- `write-up/` — drafting sources for the exploratory-modeling write-ups, moved from `docs/write-up/` on 2026-09-27 so they are not published. Holds the main post draft and the owner's outline, the markdown sources and outlines of the four pages, the writing and HTML prompts and reviews, `plan.md`, and the figures with their evidence and render scripts. The published pages are in `docs/exploratory-modeling/`. One exception to "not live tooling": `write-up/stellaris-evolution.md` is the build input for `docs/exploratory-modeling/part-4a-modeling-stellaris.html` (see `src/model_viz/evolution/README.md`).
