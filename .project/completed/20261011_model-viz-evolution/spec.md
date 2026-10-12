# Spec: Model evolution page

**Status:** Implemented, not audited (owner skipped design and plan: "Please proceed straight to the build.")
**Owner:** Reid W
**Created:** 2026-09-20
**Complexity:** Medium
**Branch:** `feat/model-viz-evolution` (worktree `../fusion-tea-model-viz-evolution`, cut from `feat/model-viz-structural-view@b814d7d6`)

## Problem

The final project documentation needs a visual that shows how the stellarator model grew, one orchestration goal at a time. The v2 viewer shows one model state. Nothing shows the sequence, what each goal changed, or how the model's size moved.

## Owner's words

- [OWNER-VERBATIM] "I want a clear strategy for visualizing the model evolution over time. I want a way to demonstrate how the goals changed the models, one goal at a time."
- [OWNER-VERBATIM] "I am envisioning a page which has an embedded version of the calc graph. And underneath it, it has a slider or left/right arrows, where you can cycle through the model's history. And underneath the visual, you have a summary of the goal and changes. Ideally, we would also have some metrics for the model (e.g. number of calcs, constraints)."
- [OWNER-VERBATIM] "Requirement: we can't mess with the main git worktree. If we need to go back through git history, it must be in a separate worktree."

## Requirements

- **R1 [NEED]** One standalone HTML page embeds the interactive calc graph, with a slider and left/right arrows beneath it that step through the model's history one goal at a time. (Owner's words, second quote.)
- **R2 [NEED]** Beneath the graph, each frame shows a summary of the goal and of what changed in the model. (Owner's words, second quote.)
- **R3 [NEED]** Each frame shows metrics for the model. [EXAMPLE] "number of calcs, constraints". (Owner's words, second quote.)
- **R4 [HARD]** The build never alters the main git worktree. History is read from git's object store (`git show`, `git diff`, `git ls-tree`), which checks nothing out. Any step that needs a checkout at an old commit runs in a separate worktree. (Owner's words, third quote.)
- **R5 [NEED]** Goals that did not change the model are not frames. [OWNER-VERBATIM] "drop the no-model-change".
- **R6 [NEED]** The exported page has no snapshot file picker. [OWNER-VERBATIM] "it would be good to remove the "choose file" button".
- **R13 [NEED]** An expand control lets the model take the full window, and full screen where the browser allows it. [OWNER-VERBATIM] "Could we have a "expand" button so that the model itself takes the full window (or maybe even full screen)?" [INFERRED] Stepping stays available while expanded, so the big view can still move through goals. (Added 2026-09-20; `test_page.py::test_expand_gives_the_graph_the_window_and_keeps_the_stepping_bar`, `::test_full_screen_falls_back_to_the_full_window_view`.)
- **R7 [INFERRED]** Frames are the `instance-graph/v3` versions of `exploration/stellarator_e2e/stellarator.snapshot.json`, from the 2026-08-21 baseline onward. The ten July versions are an older format the viewer refuses; every goal falls after the baseline.
- **R8 [INFERRED]** A frame's change list is computed from the two snapshots (calcs keyed on `display_path`; a path change with the same calc name is a move) and from `git diff` over `exploration/stellarator_e2e/generated/handwritten/`. The second source exists because the snapshot holds no body for a `manual_required` calc; measured on the 47 versions, the snapshot alone misses 9 of 60 substantive Python edits. The `SysML Source: file:line` comment codegen rewrites is ignored.
- **R9 [INFERRED]** A handwritten calc in a change list shows its recovered Python body, and a diff when the body changed. The calc-to-file rule (`pkg::'Calc Name'` → `pkg/calc_name_impl.py`) resolved 1,007 of 1,007 cases across the 47 versions.
- **R10 [INFERRED]** The v2 viewer's files are not edited. The page is the v2 export plus a separate layer that uses only what v2 exposes on `window.modelVizApp`. The v1 and v2 test batteries stay green.
- **R11 [INFERRED]** The goal's Question is shown verbatim from `goal.md` with its provenance grade and path. The result text is an agent condensation of `answer.md` or the trail's close entry, and is labelled with its source path.
- **R12 [INFERRED]** The frame manifest is a checked-in file that pins exact commit shas, so the page rebuilds identically from any branch.

## Non-Goals

- Out of scope: holding calc positions fixed across frames. Each frame gets a fresh layout. [OWNER-VERBATIM] "I don't think we need to try to freeze it."
- Out of scope: a frame for `stellaris-reference-reconciliation`. Its only model change is source-attribution comments. [OWNER-VERBATIM] "fine to skip this". The version is recorded under `unframed` in `frames.json`.
- Out of scope: computed results per frame such as LCOE. The snapshot carries no computed values, and no per-version result file is tracked in git.
- Out of scope: a dark theme. The v2 canvas colours are fixed light values.

## Acceptance

- [x] The page opens from `file://` with no server and no network, and no page or console errors. (`tests/model_viz_evolution/conftest.py` `evo_page` fails any test on a page error, console error or http request.)
- [x] Left/right buttons, the slider and the arrow keys each move one frame; the graph, metrics, summary and change list all follow. (`test_page.py::test_buttons_slider_and_arrow_keys_each_move_one_frame`, `::test_tiles_and_graph_follow_the_frame`)
- [x] Every frame's metrics equal counts taken independently from that frame's snapshot. (`test_page.py::test_every_frames_metrics_match_the_oracle`, all 29 frames)
- [x] New, changed and moved calcs are marked in the graph; a closed part that hides marked calcs is marked too. (`test_page.py::test_new_calcs_are_marked_once_their_parts_are_open`)
- [x] A handwritten calc in a change list expands to its Python body. (`test_page.py::test_a_handwritten_calc_expands_to_its_python_body` compares the shown text with the committed file.)
- [x] `git status` is unchanged by a build. (`test_page.py::test_the_build_leaves_the_worktree_as_it_found_it`; the main worktree was also checked by hand after every build on 2026-09-20.)
- [x] `tests/model_viz` and `tests/model_viz_v2` still pass. (2026-09-20: 124 and 99 passed, each run on its own; `tests/model_viz_evolution` 30 passed.)

## Implementation notes — 2026-09-20

- Built in one session without a design or plan stage, on the owner's instruction. Not audited; `/_my_audit` has not run.
- [AGENT] R8 was sharpened during the build. Comparing each input's qualified name made all 44 relocated calcs look edited, because that name embeds the owning part. Inputs are now compared by the name of the calc or attribute that feeds them. This also surfaced rewirings the first version missed, which the change list now prints (`p_pump_total_in: calc primary_loop → calc cooling_energy`).
- [AGENT] Goal content and version attribution came from four read-only research agents over the 29 goal directories; every one of the 46 versions resolved to one goal with a file-and-line basis, recorded in `frames.json` `attribution`. One guess was corrected: `0e3bf944` belongs to magnet-design-transfer (WI-038 files, nine minutes before that goal's `48417c9e`), which makes every goal's versions a contiguous run.
- The result texts in `frames.json` are agent condensations and have not been owner-reviewed.

## Write-up integration — 2026-09-26

- **R14 [NEED]** Integrate the plotting code from `feat/model-viz-evolution` and render `docs/write-up/stellaris-evolution.md` following `docs/write-up/html-prompt.md`. Source: owner request, 2026-09-26.
- **R15 [INHERITED]** Preserve the approved markdown wording and order, show six themes visibly with a left contents rail, use the shared stylesheet unchanged, and convert repository links to plain paths. Source: `docs/write-up/html-render-prompt.md`.
- **R16 [INHERITED]** Edit the builder, keep viewer interaction, and make the narrative readable without scripts. Theme-note placement remains an owner decision. Source: the render prompt, including its Stellaris exception.
- **R17 [INFERRED]** Add an article build option while preserving standalone builds; put the notes below the graph and link frame references to its selected state. Keep a static frame table for readers without scripts.

### Import provenance

[AGENT] Imported the `src/model_viz` tree and its three test batteries from `6a4d241d`, including the evolution additions in `becf7ea3` and the structural/v2 dependencies at `b814d7d6`. HEAD lacked the exporter and v2 viewer. This is a scoped file integration; no branch history or unrelated project records are merged. The six themes come directly from the markdown at build time.

### Integration validation

[AGENT] Validation on 2026-09-26: `tests/model_viz` 124 passed; `tests/model_viz_v2` 99 passed; `tests/model_viz_evolution` 36 passed, followed by all five article tests passing after the final phone-overflow correction (37 tests now in the battery), including article tests covering static links/resources, no-script access, mobile/desktop frame navigation, hash preservation, expansion, and the cooling frame with every disclosure open at 390 px. Browser tests required sandbox escalation for Chromium. The original v1/v2 tests read the mutable live model and initially refused its changed hash; they now use their exact historical WI-057 snapshot under `tests/model_viz/fixtures/`, with all original counts and assertions retained. The evolution guard compares imported viewer/exporter bytes against `6a4d241d` instead of requiring a clean git index.

[AGENT] The article scopes imported viewer CSS to its viewer container, links `write-up.css` unchanged, and keeps the viewer's operational styling. Its extra CSS handles layout and responsive embedding. The generated article has no external viewer scripts, forms, iframes, or embeds; all in-page links resolve. The unconverted `aries-model-transfer-outline.html` support is the sole missing relative target allowed by the render prompt. Existing frame results remain labelled as agent condensations awaiting owner review.

### Owner correction — viewer controls and emphasis, 2026-09-26

- **R18 [NEED]** Rename the evolution viewer’s “Expand all” control to “Show structure” without changing its behavior. Source: owner correction, 2026-09-26.
- **R19 [NEED]** Make viewer expansion visible and usable. [INFERRED] Put prominent expansion and full-screen controls above the graph, reclaim the empty inspector width, and increase the embedded graph height while preserving expanded navigation and Escape.
- **R20 [NEED]** Visually emphasize important passages without changing their wording. [OWNER-VERBATIM] “If a sweep shows that a parameter can change cost without ever hitting a limit, then the model is missing a physical constraint. Modeling that constraint becomes the next goal.” Source: owner correction, 2026-09-26. [NEED] Follow `harness.html` with sentence-level `<mark class="skim">` highlights using the shared amber treatment. Source: owner correction rejecting the earlier bold treatment.

[AGENT] Owner-correction validation: all 32 standalone evolution tests pass, including expanded graph height and full-screen fallback; all six article tests pass after correcting the new expansion test to use a nested frame (the baseline has only leaf parts). The article checks the top controls, unchanged structure-expansion behavior, hidden empty inspector, the single highlighted causal passage, phone overflow, navigation, and no-script access. The source markdown wording is unchanged. The narrative follows the viewer under one parent heading, with six numbered subsections and matching nested contents links. The introductory sentence appears once at normal reading size below that heading. A separate “Model limits” section contains the unchanged closing paragraph and frame records. Six explicitly selected passages use the shared skim treatment: computing attributes, discovering missing constraints, design-dependent costing, preserving engineering choices, tracing differences, and domain limits.
