# Review — harness.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/harness.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/harness.md
reviewed against: docs/write-up/html-render-prompt.md, docs/write-up/writing-prompt.md, ~/.claude/skills/_my_mental_model_v2/feedback/html.md, ~/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Findings

1. Figure 1's text equivalent adds a clause the markdown's alt text does not have. The markdown's image alt text reads "...a round run by the AI: an approach, then tasks one at a time, with research and model changes before the model is pinned..."; the page's `aria-label` on `div.fig-loop` (harness.html, Figure 1, ~line 401) reads "...an approach, then tasks one at a time or independent tasks in parallel, with research and model changes before the model is pinned..." — "or independent tasks in parallel" is not in the markdown's alt text. (Cites: html-render-prompt.md, "Figures" — "Keep the markdown's alt text and caption.")

2. Figure 1's caption drops the markdown's closing sentence. The markdown caption ends "...runs through the review and the owner. Rendered by `harness-assets/render_goal_loop.py`." The page's `<figcaption>` (harness.html, ~line 453) stops at "...runs through the review and the owner." with no equivalent of the "Rendered by..." sentence. Dropping a caption sentence is not one of the listed adaptations, and the prompt says any other wanted change "goes in your report as a proposal with its location... Do not make the change." (Cites: html-render-prompt.md, "Keep the prose" intro and "Figures"; "Anything else you would change...".)

3. The page's local `<style>` block adds a rule for a table's caption position — `.table-figure figcaption { margin: 0 auto 0.6rem; }` (harness.html, ~line 10), justified in its own comment as keeping Table 1's caption above the table as the markdown has it. The render prompt scopes a page's own style additions to "the layout of its own diagrams," and states "everything else comes from write-up.css." Table 1 is a table, not a diagram, so this rule sits outside the stated scope even though the outcome (matching the markdown's caption-before-table order) is reasonable. (Cites: html-render-prompt.md, "Style".)

No other dropped, reordered or reworded blocks found. The markdown's headings, paragraphs, lists, the two tables, the directory-tree `<details>`, and the Python code block all appear in the page in order and with unchanged wording, apart from the allowed adaptations (Part 2's link retargeted to `.html`; the main-post link left as `.md`; inline repository-path citations shown as `<code class="path">`; bare "section N" / "Figure N" / "Table N" references turned into working in-page links; heading anchors match GitHub's slug convention).

## Additions (page text not in the markdown)

- Section 1: an evidence panel, "In the record — The four values without a source," summarizing the four uncited values and which comparisons they fed, from the linked work item's spec.
- Section 2 / "The outer loop": Figure 1 itself is a required redraw (the markdown's PNG became an HTML/CSS diagram), which is expected, but the diagram's own box labels are new wording not quoted from the markdown — e.g. "Tasks, one at a time or independent ones in parallel," "written first, not changed while it runs," "a bet on how to answer the question. No task list.," "what was tried, what was found, why it stopped," "by someone who did not do the work," "is the goal answered?," "not yet: next round, revised approach," "Goal closed," and the "the model can change" / "the model is fixed" state labels.
- Section 4: an evidence panel, "In the record — The goal's record," summarizing `goal.md`'s fields and dated amendments and `trail.md`'s round-by-round shape. A new paragraph and a new Figure 2 (an SVG chart comparing the paper's and the model's stored-energy values), with a reading-guide sentence ahead of it and a short caption.
- Section 5: an evidence panel, "In the record — The request and its run log," quoting the research request's question and tabulating every candidate source and its disposition. A second evidence panel, "In the model — The stored-energy calculation's source lines," excerpting (with an ellipsis) the SysML doc-comment that cites the two sources.
- Section 6: three evidence panels — "In the record — The spec's 15 requirements" (grouped restatement of the spec), "In the record — Stored energy after the change, by machine size" (a table from the design's prototype data), and "In the record — The eight studies the account names" (a table from the plan). The code block gets a presentational file/language header, not a wording change.
- Section 7: a new paragraph and a new Figure 3 (a seven-step diagram placing each code check and agent review at the round-2 step where it ran), with a reading-guide sentence ahead of it and a caption. An evidence panel, "In the tooling — What the integration check runs," tabulating the ten gates.
- Section 3 and Section 8 add nothing beyond the markdown's own prose and the markdown's own directory-tree `<details>`.

All of the above additions are the kind the render prompt invites (figures, referenced information, evidence panels), each collapsed or captioned rather than inserted into the main flow, and each traceable to a repository reference the surrounding prose already names. I did not fact-check their contents against the cited files; I checked only that they don't contradict the markdown's own claims, and found no contradiction.

## Feedback patterns

No repeated negative pattern from html.md or synthesis.md was found in the page's added text. Specifically checked and clear:

- No main-flow heading sits behind a closed dropdown; only reference material is collapsed.
- Figure 2's and Figure 3's decoding facts are labeled on the figures themselves (axis values, "printed"/"its own rules"/"implied by its beta" on the chart; "Code check"/"Agent review" on the diagram), with captions kept short, matching the positive pattern in html.md ("Caption carrying the fact that decodes the figure").
- Evidence-panel summary lines are bare noun phrases ("The four values without a source," "The spec's 15 requirements," etc.), not colon-joined double clauses.
- The evidence-kind labels ("In the record," "In the repository," "In the model," "In the tooling") are plain names, not claims dressed as headings.
- Every "section N" / "Figure N" / "Table N" reference in the body is a working in-page link; none are left for the reader to scroll for.
- New prose (reading-guide sentences, evidence-panel summaries) uses named members rather than bare counts (e.g., all four uncited values named, all fifteen requirements grouped and numbered, all eight studies named in a table, all ten gates named in a table), matches the "we/the team" voice, and shows no aphoristic openers, document-as-subject sentences, or abstraction-performs-a-verb phrasing from writing-prompt.md's "Texture that breaks this voice" list.
