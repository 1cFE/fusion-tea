# Review — stellaris-evolution.html

page: docs/write-up/stellaris-evolution.html
source: docs/write-up/stellaris-evolution.md
reviewed against: html-render-prompt.md, html-review-prompt.md, writing-prompt.md, shared mental-model feedback/html.md and feedback/synthesis.md

## Findings

1. The page adds local prose-spacing overrides at lines 165–167: the themes heading margins, introduction margins and first theme heading margin. These improve the transition visually, but exceed the render prompt’s stated allowance for a local style block for diagram layout. The frame-record table also has local presentation rules at lines 139–140 and 155–158. This is a prompt-compliance issue, not evidence that the new spacing reads badly. (Cites: html-render-prompt.md, “Style”: “A page may add a small style block for the layout of its own diagrams. Everything else comes from write-up.css.”)

## Hierarchy and visual inspection

The viewer-to-themes relationship is clear in the supplied desktop transition, phone transition and full desktop screenshots. The viewer and “Six themes in the model’s evolution” have matching section bands. The six numbered theme headings are visibly subordinate. On desktop, the contents rail repeats that structure with the themes nested under one parent. The gap after the viewer separates the two main sections; the shorter gap from the themes introduction to theme 1 keeps those together. On the phone, the band and smaller numbered heading preserve the relationship without needing the rail in view.

The whole-page screenshot confirms that themes 2–6 continue the same hierarchy. All theme headings and the domain qualification remain in the open reading flow. Only the frame records are collapsed. This applies the shared HTML feedback’s preference to keep main-flow headings visible. No additional hierarchy or spacing finding arose from these screenshots. They do not establish click behavior or the phone navigation outside the captured area.

## Mechanical fidelity

A standard-library HTML parser extracted the static page’s headings, paragraphs and list items. All 39 markdown blocks matched in order after normalizing whitespace, decoding HTML entities and applying the permitted repository-link replacement. No source block was dropped, reordered or reworded. Highlight spans and frame links preserve the prose. The source’s current grouping is retained: one h2 for the themes, followed by six h3 headings. The added viewer h2 precedes that group.

All source heading anchors match their GitHub-style slugs. Every static fragment link has a target, and no duplicate ids were found. The nested contents links address the six theme headings. Frame links retain static record targets and carry indices for the viewer handler; source inspection confirms that handler selects the frame and scrolls back to the viewer. Runtime behavior was not tested. The main-post link stays markdown, support links use HTML, and repository references appear as plain paths. No external src/href resources, forms or iframes were found in the HTML. Linked support files and underlying evidence were outside this review’s reading scope.

## Added text, compact inventory

- Page and navigation: browser title “Stellarator model evolution”; rail eyebrow “1cFE write-up · Part 4”; rail title “Modeling Stellaris”; viewer, themes and frame-record navigation labels, arrows and numbers. Theme names repeat the source headings.
- Viewer: “Model evolution viewer”; the four-sentence operating guide beginning “Step through the goals with the slider or arrows”; the no-script message; viewer controls, metric labels, change labels and selected-frame summaries. These form the interactive display rather than new theme prose.
- Six themes: no added explanatory sentences. Added visible repository paths replace source links; numbered frame references become links. The group heading and introduction are already in the current markdown.
- Frame records: “In the record”, “Frame records”, the paragraph explaining snapshot counts and agent condensations, three column labels, and 29 rows containing frame titles, counts, result summaries and source paths. These additions remain behind a closed evidence disclosure. Their domain claims were not fact-checked.
