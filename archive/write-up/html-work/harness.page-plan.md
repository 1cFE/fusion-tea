# Page plan: harness.html

`harness.md` → `harness.html`, on `write-up.css` unchanged, with markup from the style sample. One page style block lays out Figures 1 and 3. The only script is the sample's navigation script.

## Pointers, paths and links

- Parenthetical source pointers render as `<code class="path">`. A `§` suffix stays plain text after the path, and a line suffix stays inside it.
- Paths that are part of the explanation (areas, table cells, the tree, script names) stay plain `<code>`.
- The main-post link is unchanged. The Part 2 link becomes `sysml-codegen-model-evaluation.html`. The web links are unchanged.
- "Section N", "Figure 1" and "Table 1" become in-page links. The tree summary's "section 4" stays text, because a link inside a summary competes with the toggle.
- Headings get GitHub ids. The rail lists sections 1–8, with "The outer loop" under 2.

## What the page adds

- **Opening, 8:** prose only.
- **1:** panel P1.
- **2:** Figure 1 rebuilt in HTML.
- **3:** Table 1 goes wide and scrolls. The tree becomes panel P2.
- **4:** panel P3. New Figure 2 after "The close".
- **5:** panels P4 and P5.
- **6:** the code block gets a file head, and the table's numbers are right-aligned. Panels P6–P8 follow Spec, Design and Plan.
- **7:** proposed Figure 3. Panel P9.

## Visuals

- **Figure 1** keeps the PNG's labels and layout. Two things change from the PNG. It is built from the CSS diagram parts. Its reading order follows the loop, so it reads without the layout. The alt text becomes the diagram's accessible label, and the caption stays (issue 4).
- **Figure 2 (new chart).** Job: show where the model's stored energy sits among the paper's values, which the close and the section 7 checkpoint rely on. It is one MJ axis. The paper's values sit above it: printed 504.65, its rules 518.3, readings 527–575, beta-implied 567. The model's values sit below it: 551 before, 519.9 after. It has a two-sentence reading guide. It is drawn by a new `harness-assets/render_stored_energy.py` with `figure_style.py`, gets a README row, and the SVG is inlined.
- **Figure 3 (new, HTML), proposed for owner approval.** Job: show that a check sits at each hand-off of round 2. It has two lanes, code checks and agent reviews, across seven steps: model change, pin, study plan, study run, study record, follow-up and round close. The boxes carry check names only. Cut it if it reads as a restatement like the Table 2 the owner cut.

## Collapsed blocks (all evidence panels, closed)

| # | § | Summary | Content |
|---|---|---|---|
| P1 | 1 | The four values without a source | The four values from WI-031's spec, one line each |
| P2 | 3 | the markdown's summary | The markdown's tree |
| P3 | 4 | The goal's record | `goal.md` sections with the four amendments named. The trail as an outline by round, with each task's scope/start/return folded into one line and the checkpoints, results and reviews kept. One reading line: "strategy" is the approach, and C-001.r1–r3 are round 1's three disposition submissions. |
| P4 | 5 | The request and its run log | The question verbatim, then the log's six searches and nine candidates with their decisions. No author email address. |
| P5 | 5 | The stored-energy calculation's source lines | The `**Source**:` lines naming the two sources. Home paths are summarized. |
| P6 | 6 | The spec's 15 requirements | The titles, plus MR-WI042-1's Validation and Source lines |
| P7 | 6 | Stored energy after the change, by machine size | The new-to-old ratio by (R, a), 0.768 to 0.991, from `window_corners.json` |
| P8 | 6 | The eight studies the account names | One study is re-executed at the new pin. Seven stand at their own pins. |
| P9 | 7 | What the integration check runs | Gates 0–9, one plain line each |

All other references stay as paths.

## Open questions from plan.md

- **A figure for section 4:** Figure 2 is proposed instead of the viewer frame, whose texts are unchecked. The owner decides.
- **One page or two:** the page follows the markdown, so it is one page.
- **Main-post figures:** Figure 1's PNG stays available for reuse.

## Source issues for owner ruling (not changed)

1. **§2, "The goal is written first" paragraph.** The bold lead has no period. Add one.
2. **§2, "The goal is not changed as it executes."** The example's `goal.md` has dated amendments made during the run: (b) added the owner's scaling invariant, and (c) reread the Package invariant. The question and "answered when" were unchanged. Figure 1 says the same thing. Proposed: "The question is not changed as it executes; any other change is a dated amendment."
3. **§2 and Figure 1: serial tasks and a fresh review of every round.** ADR-0001 was amended on 2026-09-11 to allow bounded parallel tasks. ADR-0002, ADR-0005 and the runbook were amended on 2026-09-14 to make review risk-based. The example ran on 4–6 September under the old rules. Proposed: add a dated qualifier, or frame §2 as the loop as the example ran.
4. **Figure 1 caption, "Rendered by `render_goal_loop.py`".** This is false for the HTML figure. Proposed: "Rebuilt from `harness-assets/render_goal_loop.py`", or drop it.
5. **§1, "four values in the model with no source anywhere in the repository".** The research note and the WI-031 spec call them values the study's comparison arms needed. The Nb3Sn value was not yet in the model, and the steam efficiency had a source awaiting confirmation. Proposed: "four values the study needed that no source in the repository supplied."
6. **For information only.** §6's "1 to 23 percent" is the design's prediction. The round 2 study measured 0.79–1.02 (L-007).

The split, the missed tests, the 27 minutes, the submission counts and the first-run pin were each checked against the record and hold.
