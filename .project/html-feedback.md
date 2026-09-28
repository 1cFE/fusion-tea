# HTML feedback for the write-up pages
Project-local feedback on the HTML write-up pages in `docs/exploratory-modeling/`, moved here from the write-up archive on 2026-09-28. Entries are append-only and are written only when the owner asks.

## Skim accents that the eye catches
Prefer. Mark the sentence that carries a dense paragraph with a visible colored mark, not italics. Owner's request: "Can you add some accents to make it easier to skim, especially when we have blocks of text?"
- Bad: `<em>Fighting that entropy is the job of the harness.</em>`. The owner said: "the italics is virtually unnoticeable."
- Good: the owner's suggestion was "maybe a colored underline or something?" It was built as the amber highlighter band, `<mark class="skim">` in `write-up.css`.
- From: 2026-09-26, harness.html

## A visual that carries the text, with the text collapsed beneath it
Prefer. The owner's direction: "in general if you can make a visual that captures the text, and then move the text into a collapsible section, that is a win. see sysml-codegen-model-evaluation.html"
- Bad: section 7 of version 3 showed Figure 3 and then the full code-check and agent-review lists open in the main flow.
- Good: the owner's words: "make the full list of code checks and agent checks each collapsible. they add good detail, but many readers will be happier to see a diagram and keep moving."
- From: 2026-09-26, harness.html

## Interactivity
Prefer. The owner said: "I would have liked more visuals and more interactivity." The reference page is `sysml-codegen-model-evaluation.html`.
- Bad: version 3 of harness.html had three figures and none was interactive.
- Good: no corrected form was given. On version 4, which added explore panels to Figures 1, 2 and 9 and clickable task cards, the owner said: "the interactivity thing is good".
- From: 2026-09-26, harness.html

## One home for each passage
Avoid. The same text should not appear in a figure, in its explore readout and in a collapsed section.
- Bad: the `Explore: How each part of the loop works` readout repeated the "The loop, part by part" collapsed section word for word. The owner said: "you have introduced a LOT of redundancy."
- Good: the owner's words: "you should remove the text if it is covered by the graphic. if there is extra stuff, make sure they compliment, not overlap"
- From: 2026-09-26, harness.html
