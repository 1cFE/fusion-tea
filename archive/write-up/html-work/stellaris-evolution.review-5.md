# Review — stellaris-evolution.html

page: docs/write-up/stellaris-evolution.html
source: docs/write-up/stellaris-evolution.md
reviewed against: docs/write-up/html-render-prompt.md; docs/write-up/writing-prompt.md; /home/reid/.claude/skills/_my_mental_model_v2/feedback/html.md; /home/reid/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Findings

1. The local CSS goes beyond diagram layout. The three style blocks at lines 6–164 set button colors, typography, panel backgrounds, prose sizes, disclosure styling and a new `.key-point` callout. The shared stylesheet is linked, but these rules define a second visual treatment. The viewer exception permits its scripts; it does not exempt its styles. (Cites: writer prompt, “Style”: only a small local block for diagram layout; everything else comes from `write-up.css`; “Part 4, support 1”: everything else applies.)
2. The added result in `#frame-27`, repeated by the viewer’s frame summary, ends “Four engineering failures remain visible” without naming them. The summary does not tell the reader which failures qualify the reported result. (Cites: synthesis feedback, “Count standing in for the members”; writer prompt, added text follows the voice.)
3. Generated calculation disclosures use `Python body (N lines)` and `Python body: what changed` (`calcItem`, around lines 7139–7140). The first adds an implementation count to the summary; the second uses the colon-joined form the feedback explicitly rejects. (Cites: HTML feedback, “Dropdown summary line written as a double clause”; writer prompt, disclosure summaries should read as headings.)

## Fidelity and static checks

A mechanical comparison of the current on-disk page found all 37 source blocks in order, with unchanged wording after the permitted repository-path and link adaptations. All five source bold spans remain `<strong>`. No dropped, reordered or reworded source blocks were found. All source heading anchors and all static fragment-link targets exist; no duplicate IDs were found.

All six theme headings remain visible. The frame table and generated code disclosures start closed. Controls have handlers for frame stepping, frame selection, search, spacing, expansion and fullscreen. The frame links select the corresponding zero-based frame and return to the viewer; their static targets are the matching table rows. This was source inspection, not a browser interaction test. Viewer scripts were treated as exempt. No domain-source verification was attempted.

## Added-text inventory

- Rail, line 167: publication eyebrow, shortened title, duplicated six section labels, plus “Model evolution viewer” and “Frame records” entries.
- Viewer, lines 169–190: heading, four-sentence reading guide, JavaScript fallback notice, toolbar labels and buttons. Runtime additions include frame navigation and expansion labels, change-color legend, metric labels/counts, frame titles and metadata, questions and attribution, result condensations, source paths, change lists, calculation details, code disclosure labels and status/error messages (`renderSummary`, `renderChanges`, panel rendering and navigation code).
- Themes 1–6, lines 191–214: no new explanatory prose. Repository links become label-plus-path pointers; frame numbers become links. “Part 3” becomes a support link.
- Frame records, line 215: disclosure label; three-sentence introduction; three column headings; all 29 row titles, metric triples, result paragraphs and source-pointer strings (`#frame-1` through `#frame-29`). The runtime frame summaries repeat the row results and add their questions and metadata. These are additions, not wording inherited from the settled markdown.
