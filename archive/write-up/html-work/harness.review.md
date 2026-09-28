# Review — harness.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/harness.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/harness.md
reviewed against: docs/write-up/html-render-prompt.md, docs/write-up/writing-prompt.md, ~/.claude/skills/_my_mental_model_v2/feedback/html.md, ~/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Findings

1. Figure 1's caption drops a sentence that is in the markdown. The markdown caption ends "...runs through the review and the owner. Rendered by `harness-assets/render_goal_loop.py`." The page's `<figcaption>` (harness.html, `id="figure-1"`) stops after "...review and the owner." and never states the render script at all. The writer prompt's only listed adaptations are dropping drafting scaffolding (provenance tags, draft/status notes, dated notes, HTML comments) — a figure's render-script attribution is none of these, and the prompt's own convention section expects render-script provenance to be carried ("A redrawn or new image figure gets a render script... following the existing convention"). This isn't a scaffolding drop; it's a dropped content block. (cites: html-render-prompt.md "Keep the prose" — only listed adaptations are permitted; the caption's script attribution is not one of them.)

2. Figure 1's accessible label was reworded, not carried unchanged. The markdown's image alt text reads "...an approach, then tasks one at a time, with research and model changes before the model is pinned..." The page's `aria-label` on `.fig-loop` (harness.html, `id="figure-1"`) reads "...an approach, then tasks one at a time or independent ones in parallel, with research and model changes before the model is pinned..." — the clause "or independent ones in parallel" is inserted and is not in the source alt text. (cites: html-render-prompt.md, Figures bullet — "Keep the markdown's alt text and caption.")

3. Figure 3 (new, in section 7) may be a restatement rather than an aid. Its seven step-boxes carry only the same eight check names the two bullet lists immediately below it already give ("Validation levels," "Regression tests," "Integration check," "Study checks" / "Critique of the study plan," "Recount of the study record," "Checkpoint on the conclusions," "Fresh review of the round"), now just sorted onto a step axis. The one thing it adds beyond the prose is the step-by-step ordering across round 2 — a real but thin addition. Flagging for the coordinator to weigh against "New visuals, only where they help... Do not add a visual to fill a catalog." (cites: html-render-prompt.md, "What the page adds" § New visuals.)

No other dropped, reordered or reworded blocks were found. A full block-by-block pass (every heading, paragraph, list item, table and code block in the markdown) matched the page's wording exactly, apart from the two Figure 1 items above; all internal "section N" / "Figure N" / "Table N" references were correctly turned into working in-page links; parenthetical source pointers consistently render as `<code class="path">` with `§` suffixes kept outside the code span and line-number suffixes kept inside it, matching the page plan's stated convention; the main-post link and the two `1cf.energy` web links are left unchanged; the Part 2 link correctly points to `sysml-codegen-model-evaluation.html`; and GitHub-style anchor ids on every heading (1–8, plus "The outer loop") check out against GitHub's slug algorithm.

## Additions (text and structural, by section)

These are sanctioned under "What the page adds" (referenced information, new visuals, evidence panels), listed here so the coordinator can see everything not in the markdown. None contradict the markdown's claims or add unsupported facts on their own read.

- **§1:** an evidence panel, "The four values without a source," listing the four values from WI-031's spec.
- **§2:** no new prose (Figure 1 is carried from the markdown, not new — see findings 1–2 for how it was altered).
- **§3:** no new prose; the directory tree and Table 1 are carried from the markdown into an evidence panel / wide table respectively.
- **§4:** an evidence panel, "The goal's record," summarizing `goal.md`'s sections/amendments and `trail.md`'s round-by-round outline; a new Figure 2 (a stored-energy number-line chart) with a one-sentence introduction ("Figure 2 places the goal's stored-energy values on one axis: the paper's above it, the model's below.") and its own caption — none of this exists in the markdown.
- **§5:** an evidence panel, "The request and its run log" (the request's question verbatim, six searches, nine candidates with decisions); an evidence panel, "The stored-energy calculation's source lines" (an excerpt of the SysML doc comment).
- **§6:** an evidence panel, "The spec's 15 requirements" (titles plus MR-WI042-1's detail); an evidence panel, "Stored energy after the change, by machine size" (a ratio table); an evidence panel, "The eight studies the account names"; a file-name/language head added above the markdown's own Python code block.
- **§7:** a new Figure 3 (checks-by-step diagram, see finding 3) with a one-sentence introduction and caption; an evidence panel, "What the integration check runs" (the ten gates).
- **§8:** prose only, no additions.

## Feedback-pattern check

No repeated negative patterns from `html.md` or `synthesis.md` were found in the page's added text. Specifically checked and clear: no main-flow heading sits behind a closed dropdown (only supplementary "In the record" / "In the model" / "In the tooling" panels are collapsed); no caption carries a fact needed to decode a chart (Figures 2 and 3 both have their decoding facts in the body sentence and on the visual itself, not only in the caption); every new evidence-panel summary is a bare noun phrase, not a double clause; every "section N" / "Figure N" reference, including in the newly added sentences, is a working link rather than a bare number. The two new one-sentence figure introductions read as plain, direct statements of what the figure shows and do not exhibit the "abstraction performing a verb," narrative-hook, or document-as-its-own-subject patterns called out in `synthesis.md`.
