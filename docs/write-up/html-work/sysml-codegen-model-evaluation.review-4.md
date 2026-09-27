# Review — sysml-codegen-model-evaluation.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/sysml-codegen-model-evaluation.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/sysml-codegen-model-evaluation.md
reviewed against: docs/write-up/html-render-prompt.md, docs/write-up/writing-prompt.md, ~/.claude/skills/_my_mental_model_v2/feedback/html.md, ~/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Fidelity check

I walked every markdown block (127 blocks, headings through the closing sources list) against the page in document order. Every heading, paragraph, list item, code block, table (n/a — markdown has none), and link is present, in order, with unchanged wording, except for the adaptations the render prompt allows:

- Every heading carries the GitHub-style anchor id (verified against the `#nn-slug` form for every `h2`/`h3`/`h4`).
- Every repo-relative link (`../../models/...`, `sysml-codegen-assets/...`, `exploration/...`) is shown as plain-text `<code class="path">` with the correct resolved repository path, not as a link. Confirmed by extracting every `href="..."` in the page: only the two external URLs (`1cf.energy`, two `github.com` links) and in-page `#anchor` links remain as `<a>`.
- Every "section N.N" reference in prose (2.1, 2.2, 2.3, 2.4, 2.4.1, 2.7 — all nine occurrences) is a working in-page link to the right anchor.
- Image alt text and italic captions from the markdown are carried onto the corresponding figure's `aria-label`/`role="img"` and `<figcaption>` for all eleven figures (`fig-kinds` has no source image but is new; `fig-overview`/Fig.2, `fig-field`/Fig.3, `fig-fit`/Fig.4 [SVG redraw], `fig-graph`/Fig.5, `fig-breeding`/Fig.7, `fig-cases`/Fig.10, `fig-map`/Fig.11 all check out word for word against the markdown's `![alt](...)` and the following italic caption paragraph).

One departure from "carry every code block, in the same order and with the same wording":

1. **Section 2.5's three-declaration code fence is dissolved into a new diagram rather than also kept intact.** Markdown block 84–86 is one fenced `sysml` block holding three declarations in this order: the generic plant usage, the specialized definition, and the stellarator selection (`sysml-codegen-model-evaluation.md:187-202`). The page (`sysml-codegen-model-evaluation.html:1387-1441`) reproduces each of the three snippets verbatim inside separate `dg-box` cells of a new relationship diagram, but rearranges them into a 2D grid (specialized definition top-right, generic-plant usage bottom-left, stellarator design bottom-right) and adds a fourth box, "Base definition," holding a `'Blanket'` declaration (`attribute tbr : Real default 1.0;`) that is not in the markdown code fence at all — the box's own subtitle admits this ("· not in the code block"). Nowhere on the page is the original three-part fence reproduced as a single contiguous block in its original order. (Cites: html-render-prompt.md "Keep the prose" — "Carry every heading, paragraph, list, table, code block, figure and link into the page, in the same order and with the same wording.") This is different from the section 2.6.1 YAML case, where the page keeps the original fenced block verbatim in the main flow *and* adds a new connections diagram (`sysml-codegen-model-evaluation.html:1483-1492` plus Figure 8) — that treatment fully satisfies the constraint; 2.5 does not.

## Additions (text/diagrams not in the markdown)

By section, the recurring categories of addition:

- **1.3**: none beyond the required figure redraw (Figure 2, an image already in the markdown).
- **2.1**: a one-sentence reading guide before Figure 3 ("The walk below follows the numbered boxes..."); a "Try it" live slider panel (`#field-live`) with static fallback text.
- **2.2**: a reading-order sentence before Figure 4 ("Read it from the outside in..."); an evidence panel quoting the fit calculation's SysML (`In the model — What the fit calculation reads`).
- **2.3**: an evidence panel listing all 18 calculation-graph bindings as a table (`In the record — The 18 connections behind the graph`); an interactive "Explore" panel on Figure 5 with chip buttons and a static fallback sentence.
- **2.4**: an evidence panel with the generated Python wrapper around the field calculation (`In the package — The generated wrapper around it`).
- **2.4.1**: a "Try it" live slider on Figure 7 for the breeding surrogate; an evidence panel with the five-node response table and the interpolation code (`In the code`); an evidence panel on implementation preservation (`In the note`).
- **2.5**: the new relationship diagram discussed above (includes the "Base definition" box, new content); an evidence panel showing the specialized blanket's body (`In the model — What the specialized body adds`), which is new code excerpt content not in the markdown.
- **2.6.1**: a reading-guide sentence before Figure 8; the new Figure 8 connections diagram; an evidence panel on the surrounding pipeline size (113 vs. 269 entries) with a further YAML excerpt (`In the package — The pipeline around this entry`).
- **2.6.2**: two evidence panels — input-file counts and which calculations read which plant values (`In the package — The input files`), and general input-generation rules (`In the note — Input generation`).
- **2.7**: the new Figure 9 study-flow diagram (built from the markdown's own definitions/sentences); an evidence panel on the study record's directory layout (`In the record — The study record and the study runner`).
- **2.7.1**: a reading-order sentence before Figure 10; three small schematic SVGs per case (reusing Figure 4's visual vocabulary, as the added sentence states); an evidence panel with the full three-case comparison table (`In the record — The three recorded cases`).
- **2.7.2**: an interactive "Read a point" panel on Figure 11 (arrow buttons, legend, per-mark readout) with static fallback text; an evidence panel of held inputs for the sweep (`In the record — Held inputs for the map`).

These all fall inside the render prompt's allowances for figures, new visuals, collapsed detail, and referenced information, with the one exception noted above (the section 2.5 "Base definition" box, which is new *unsourced-in-brief* content, not just an evidence excerpt of something the markdown names).

## Writer-prompt violations

1. **Interactive scripts go beyond navigation-state tracking.** The render prompt's hard constraint states: "An inline script may only track navigation state, as the style sample's script does." The page's `<script>` block (`sysml-codegen-model-evaluation.html:14242-14517`) does far more: it computes the field equation live from two sliders (Figure 3), computes the breeding-surrogate interpolation live from a slider (Figure 7), builds a clickable dependency-highlighting graph explorer with generated chip buttons (Figure 5), and builds an arrow-driven, filterable map reader with a legend and per-point readout (Figure 11). The script's own leading comment says these are "the four figures the owner approved for scripting," which is an out-of-band claim I cannot verify from the materials named in my brief — the render prompt as written restricts inline scripts to navigation-state tracking only, and this page's script clearly does more than that. (Cites: html-render-prompt.md, "Hard constraints" — "An inline script may only track navigation state, as the style sample's script does.") Note: every one of these interactive panels does have static fallback text so the page still reads in full with scripts disabled, satisfying that separate hard constraint.
2. **Section 2.5 code-block handling**, described above under Fidelity, is also a concrete instance of not carrying a code block "in the same order and with the same wording" as its own contiguous unit.

## Feedback-pattern check

Scoped to text the page adds (reading guides, evidence-panel prose, live-panel labels, disclosure summaries), since the markdown's own prose is settled:

- No hits for hedging, false range, "not just X but Y," inflated stakes, nominalized verbs, em-dash pileups, or resume words in the added text.
- No structural heading was turned into a claim; all `<summary>` lines in evidence/detail panels are bare noun phrases or a `kind` tag plus a short noun phrase (e.g., "In the model — What the fit calculation reads," "In the record — Held inputs for the map"), matching the "write a summary line like a heading" guidance and avoiding the "double clause" pattern.
- No main-flow heading is hidden behind a closed dropdown that would break a single-pass read: the only headings placed inside `<details>` are 2.3.1–2.3.3, which the render prompt explicitly allows ("a detail section holds a lower-level subsection, such as implementation steps, with its heading as the summary"), and Figure 6 gives a one-line summary of each step in the main flow so a reader who opens nothing still gets the sequence.
- The decoding fact for each interactive/redrawn figure is placed in the body or on the figure itself (e.g., the reading-order sentences before Figures 3, 4, 8, 9, 10), not left stranded only in the caption — this matches the "caption carrying the fact that decodes the figure" guidance rather than repeating that mistake.
- No new prose commits the "document as its own subject," "abstraction performing a verb," or "count standing in for the members" patterns; where the page adds counts (e.g., "Fourteen calculations... joined by the eighteen recorded... bindings") the members are also given, in the table right below it.

No findings beyond the ones listed above under Fidelity and Writer-prompt violations.
