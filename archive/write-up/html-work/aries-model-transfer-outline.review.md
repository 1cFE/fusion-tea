# Review — aries-model-transfer-outline.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/aries-model-transfer-outline.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/aries-model-transfer-outline.md
reviewed against: /home/reid/1cfe/fusion-tea/docs/write-up/html-render-prompt.md, /home/reid/1cfe/fusion-tea/docs/write-up/writing-prompt.md, ~/.claude/skills/_my_mental_model_v2/feedback/html.md, ~/.claude/skills/_my_mental_model_v2/feedback/synthesis.md, /home/reid/1cfe/fusion-tea/docs/write-up/html-feedback.md

## Method

I extracted every heading, paragraph, list item, table cell and figure caption from both files with a script (markdown parsed as HTML for a like-for-like comparison, page content filtered to exclude anything inside a `figure`, an `.evidence` details block, or an element carrying `data-added`) and diffed the two sequences block by block. I then read the full set of page-added text (everything with `data-added`, the three new-visual figure captions, and every `<summary>` line) end to end against the writer prompt and the feedback files, and read the closing `<script>` against the render prompt's hard constraints.

## Findings

1. **The inline script does more than track navigation state.** The render prompt's hard constraint says "An inline script may only track navigation state, as the style sample's script does." `html-work/style-sample.html`'s script (lines 611–637) only does scroll-spy and hash-opens-a-closed-detail. The page's script (`aries-model-transfer-outline.html:5023–5146`) does that too, but also builds live interactivity beyond it: a Figure 4 case-picker that toggles highlighted values in four boxes (lines 5028–5050), and a Figure 6 point-reader that draws rings on the chart and writes a formatted readout from embedded JSON data (lines 5052–5115). The script's own comment concedes this ("Navigation state, and two small live parts (Figures 4 and 6)"). (Cites: html-render-prompt.md, Hard constraints — "An inline script may only track navigation state, as the style sample's script does.")

2. **Fidelity to the markdown is otherwise intact.** Every heading, paragraph, list item and table cell carries over with its wording unchanged, in order. The only structural departure is the two bullet points under "The test asked two questions" (source lines 15–18): instead of staying a plain list, their exact wording is carried into the two cards of Figure 1 (`aries-model-transfer-outline.html:177–196`). No words are dropped or changed, but this turns a markdown list into a new visual, which is not one of the render prompt's explicitly enumerated adaptations (drop scaffolding, retarget links, anchor ids, inline source pointers). It is defensible as a "new visual, only where it helps" for a list of parallel items, but flag it for the coordinator to confirm, since it is a mechanical reordering-into-a-figure the fidelity rule does not name. (Cites: html-render-prompt.md § Keep the prose, enumerated adaptations list.)

3. **Additions, by section, all of which are marked with `data-added` (or, for the two new diagrams' captions, correspond to a `data-added` reading-guide sentence beside them) so they are traceable:**
   - §1: reading guide for Figure 1 ("Each card in Figure 1 holds one question...").
   - §2: reading guide for Figure 2 ("Figure 2 contrasts the two patterns..."); one inline sentence coining/naming a term already used undefined in the markdown, "We call that moment, when the withheld papers were opened, the reveal."; an evidence panel ("The false start and the repair") with a first-run account, an owner quote, the repair baseline, and the repair's scope.
   - §3.1: an evidence panel reconstructing the 56.6 T arithmetic step by step; a second evidence panel scoring the model against the original hold-out comparison criteria.
   - §3.2: reading guide for Figure 4; two evidence panels — the eight-increment build log, and the integrated-plant summary (nominal case, equipment/cost basis, Stellaris-unchanged claim).
   - §3.3: reading guide for Figure 5; two evidence panels — the power progression from the first ARIES case to 891 MW, and the cost-difference-by-cause table.
   - §4.1: a reading-guide line for Figure 6 plus a live "Choose a ratio..." prompt tied to the interactive panel (finding 1); an evidence panel with the plant, starting point, best points and study's stated limits.
   - §4.2: an evidence panel with the reactor's fixed parameters, the Brayton-at-2,800-MW explanation, verification note, and the earlier conversion-only comparison table.
   - §4.3: reading guides for Figures 11 and 12; an evidence panel of every tested sensitivity change.
   - §5: an evidence panel summarizing MR-7's four requirement bullets, sourced to the owner's quote in section 2.
   None of these additions state a fact, qualification or rationale that is not already in the markdown or its cited evidence files, so they do not appear to invent anything the render prompt prohibits.

## No findings beyond the above

The voice check (against writing-prompt.md and the synthesis/html feedback files) turned up no instances of the tracked bad patterns in the page's added text: no aphoristic openers, map/memory metaphors, callbacks to the page's own phrasing, narrative hooks, "not just X but Y," em-dash pileups, abstraction-performing-a-verb, double-clause dropdown summaries, or headings collapsed behind a closed `<details>`. Collapsible summaries are consistently bare noun phrases ("The false start and the repair," "Every tested change, at both heat loads"). Anchor ids match the GitHub-slug convention the render prompt requires, cross-support links point to `.html` except the main-post link (correctly left as `.md`), and repo-file links are rendered as plain paths per the allowed adaptation.
