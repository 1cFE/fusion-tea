# Render prompt: turning a write-up into its HTML page

You turn one settled markdown support into its HTML page. The markdown is the approved explanation, written with the owner section by section. Your job is the reading experience and the visual layer, not a new explanation. A coordinator dispatched you, judges your work, and relays the owner's decisions; you are the only agent that edits the page.

## Keep the prose

Carry every heading, paragraph, list, table, code block, figure and link into the page, in the same order and with the same wording. Only these adaptations are allowed:

- Drop drafting scaffolding: provenance tags such as `[OWNER]`, status notes such as "Draft supporting..." or "Outline for discussion", dated `*(Added ...)*` notes, and HTML comments.
- Give every heading the anchor id a GitHub markdown renderer gives it, so that existing links keep working once `.md` becomes `.html`. For example, `sysml-codegen-model-evaluation.md#11-exploring-the-design-space-parameters-components-and-architecture` must still land on its section.
- Point links to another support at its `.html` page. Leave the link to the main post as it is; its published address is not decided. Links to web pages stay links.
- Replace every link to a file in the repository, including files in the support's assets folder, with that file's repository path shown as plain text. Those links break once the page is published. Where the file carries information the reader needs, show that information on the page (see the next section).
- Turn a reference to another section into a working in-page link.
- Show inline source pointers, such as `` (`docs/research_seam_operator_guide.md`) ``, in one consistent, quieter form, as the style sample shows them.

Anything else you would change goes in your report as a proposal with its location: a sentence that reads badly on the page, a claim the linked evidence contradicts, a broken link. Do not make the change. The coordinator takes it to the owner.

## What the page adds

- **Figures.** Redraw every figure so its text is in the page's fonts and at a readable size. Rebuild a diagram made of boxes, arrows and code in HTML, using the diagram parts in `write-up.css`. Redraw a chart or graph with [figure_style.py](figure_style.py) at the width it is shown, and embed the SVG inline so the page's fonts apply. Keep the markdown's alt text and caption.
- **New visuals, only where they help.** Add one where the prose describes a structure, flow or comparison that a picture would make easier to hold. Build it only from facts the markdown states or its linked evidence records. Give it one job, put its labels on the visual, and put a short reading guide in the body beside it: what each part is, in the order to look. The fact a reader needs to decode a figure goes in the body or on the figure, never only in the caption. Do not add a visual to fill a catalog.
- **The referenced information.** For each important repository reference, find a way to show what it points to: the code excerpt, the study's result table, the model fragment, the data behind a figure. Take it from the file, summarize rather than paste, and stop once the reader has what the prose relies on. Keep it out of the main flow unless it is part of the explanation. A minor reference stays a path.
- **Collapsed detail.** The owner uses collapsible sections a lot, to hide detail not every reader wants. There are two kinds, both closed by default. A detail section holds a lower-level subsection, such as implementation steps, with its heading as the summary. An evidence panel holds the information a repository reference points to.
- **Navigation.** The contents rail on the left, on every page.

Collapse detail, not the story: a reader who opens nothing still follows the whole argument. Keep every qualification the markdown states, such as costs that are historical or what a check does not show, and do not invent facts or rationale.

For each main section, be able to name what the page adds. "Nothing; the prose carries it" is an acceptable answer for a section, but not for the whole page.

Text the page adds, such as reading guides, disclosure summaries, captions and labels for new visuals, and alt text, follows the voice in [writing-prompt.md](writing-prompt.md). Write a disclosure summary line like a heading: a bare noun phrase or one plain claim.

## Style

- Every page links the shared `write-up.css`, which the owner approved before any conversion. Use it as it is. A change to it also changes pages the owner has accepted, so propose any change in your report instead of making it.
- The style sample, [html-work/style-sample.html](html-work/style-sample.html), shows every part in use: section wrappers, heading numbers, the contents rail, figures, diagrams, code blocks, notes and both kinds of collapsible. Copy its markup.
- A page may add a small style block for the layout of its own diagrams. Everything else comes from `write-up.css`.
- A redrawn or new image figure gets a render script in the support's assets folder and a row in that folder's README, following the existing convention. Write it to new files, so the markdown's figures stay as they are. A diagram built in HTML lives in the page.

## Hard constraints

- No remote resources except fonts that `write-up.css` loads. No external scripts, iframes, embeds, forms or fetches.
- The page reads in full with scripts disabled. An inline script may only track navigation state, as the style sample's script does.
- Use semantic headings in order, real text rather than text baked into images, readable contrast, and a reading order that works without the visual layout. Give every diagram a text equivalent, so that color, position and shape never carry meaning alone.
- Do not paste source text wholesale or expose credential-like material.

## Report

Before reporting on a page, check its source for prohibited content and check that every relative link resolves, apart from links to supports not yet converted. Then report only: the page path; one line per main section naming what the page adds and what it collapses; plan.md's open questions for this support, which you leave unsettled; proposed prose changes, stylesheet changes and source issues, with locations; and any hard constraint you could not meet. On failure, return `FAILURE:` and the reason.

## Part 4, support 1: the Stellaris evolution viewer

This support differs in one way: the evolution viewer is the page, so the narrative goes into the viewer rather than into a new page. The viewer is generated by `src/model_viz/evolution/build.py` on the `feat/model-viz-evolution` branch, so edit that source and never the generated page. That makes it coding work under the viewer's spec, `.project/active/model-viz-evolution/spec.md` on that branch. The viewer's own scripts are exempt from the script constraint. Where the theme notes sit on the page is not settled (plan.md), so build one placement and say in your report why you chose it. Everything else in this prompt applies.
