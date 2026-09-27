# Review — stellaris-evolution.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/stellaris-evolution.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/stellaris-evolution.md
reviewed against: docs/write-up/html-render-prompt.md; docs/write-up/writing-prompt.md; /home/reid/.claude/skills/_my_mental_model_v2/feedback/html.md; /home/reid/.claude/skills/_my_mental_model_v2/feedback/synthesis.md; docs/write-up/write-up.css

## Findings

1. **Page styles extend beyond diagram layout.** At lines 113–153, the added style block changes viewer prose and heading font sizes, table presentation, and heading visibility (`.evo-title { display: none; }`), as well as layout. The earlier viewer style blocks also specify their own visual styling. The support-specific exception exempts viewer scripts but grants no corresponding stylesheet exception. (Cites: writer prompt, “Style”: “A page may add a small style block for the layout of its own diagrams. Everything else comes from `write-up.css`”; “Part 4, support 1”.)

2. **The added viewer heading lacks its required heading anchor.** At line 158, `<h2>Model evolution viewer</h2>` has no `id="model-evolution-viewer"`. Its wrapper supplies `evolution-viewer`, which works for the rail but differs from the GitHub heading slug. All seven source headings retain the expected anchors. (Cites: writer prompt, “Keep the prose”: “Give every heading the anchor id a GitHub markdown renderer gives it”.)

3. **Some added frame text retains opaque process language and metaphorical headings.** In the evidence table at line 204, frame 5 uses “Making the escape levers carry real costs” and “The goal closed by redirect”; frame 10 reports “17 of 23 rubric cells at target”; frame 27 says the package was adopted “as r3”; frame 29 ends with “File-read verification and a synthetic comparison adapter”. These terms are not explained in the added text or source narrative. Frame 6's “Making the wall-load and heating checks honest” likewise substitutes a rhetorical judgment for the subject of the correction. (Cites: writing prompt, “Write as the team doing the work” and “Show enough machinery to make the process imaginable”; synthesis feedback, “Heading that stacks counts and coined terms”.)

4. **Added failure counts leave the failures unnamed.** At line 204, frame 27 ends “Four engineering failures remain visible” and frame 28 ends “The baseline still fails six engineering checks”. The respective rows never identify those checks. (Cites: synthesis feedback, “Count standing in for the members”: “Name the members”.)

## Mechanical fidelity check

Parsed the static article into heading, paragraph and list-item blocks using Python's HTML parser. Converted markdown link labels to displayed text and repository references to the permitted label-plus-path form, then compared exact wording after whitespace normalization. All 37 source blocks match in their original order: seven headings, nine paragraphs and 21 list items. No source block was dropped, reordered or reworded beyond permitted link adaptations. The markdown contains no figures, tables or code blocks.

The main-post link remains `.md`; the two support links become `.html`; repository links become plain paths; frame numbers and the later “Part 3” reference become links. Every static fragment link has a target. All six theme headings, their lists and the closing domain qualification remain outside closed disclosures. The added frame table is closed by default. This review inspects static article content and styles; it does not execute or inventory the exempt viewer scripts or read linked evidence files, so it makes no claim about their runtime behavior or source accuracy.

## Added static text, by section

The following is an inventory, not a finding that additions are prohibited. Repository paths substituted into source blocks are permitted adaptations and are accounted for in the mechanical check.

### Contents rail

- “1cFE write-up · Part 4” and “Modeling Stellaris”.
- “Model evolution viewer” and “Frame records”, each preceded by the navigation symbol “↗”.
- The six theme titles repeat the source headings with separate navigation numbers.

### Introduction and viewer

- Model evolution viewer
- Step through the goals with the slider or arrows. Select a part to open it, then select a calculation to see its inputs and equations. Frame links in the themes return here. Expand gives the graph the whole window.
- The interactive graph needs JavaScript. All six themes and the frame records below remain available.
- Static viewer controls: “Snapshot”, “Expand all”, “Collapse all”, “Fit”, “Reset layout”, “Spacing”, “1×”, “Find”.

### Themes 1–6

No added prose. Source references are displayed as paths and frame numbers become links.

### Frame records

- Disclosure summary: “In the record” / “Frame records”.
- Counts come from each committed snapshot. Results below are the viewer’s agent condensations of the cited records; they have not been owner-reviewed. The six themes above use the checked write-up text.
- Frame | Calculations / checks / parts | Recorded result and source
- `#frame-1` (HTML line 204): “1. Starting point: the migrated model”; counts `55 / 6 / 14`; added result summary and plain-text source citation.
- `#frame-2` (HTML line 204): “2. Rerunning the model with pumping power corrected to 195 MW”; counts `55 / 6 / 14`; added result summary and plain-text source citation.
- `#frame-3` (HTML line 204): “3. Deriving the magnets from their own design”; counts `60 / 7 / 14`; added result summary and plain-text source citation.
- `#frame-4` (HTML line 204): “4. Checking the plasma operating point against the machine”; counts `61 / 8 / 14`; added result summary and plain-text source citation.
- `#frame-5` (HTML line 204): “5. Making the escape levers carry real costs”; counts `65 / 9 / 14`; added result summary and plain-text source citation.
- `#frame-6` (HTML line 204): “6. Making the wall-load and heating checks honest”; counts `68 / 9 / 14`; added result summary and plain-text source citation.
- `#frame-7` (HTML line 204): “7. Why the stored energy ran 9% high”; counts `68 / 9 / 14`; added result summary and plain-text source citation.
- `#frame-8` (HTML line 204): “8. Ruling out plasmas the heating cannot hold”; counts `68 / 10 / 14`; added result summary and plain-text source citation.
- `#frame-9` (HTML line 204): “9. Making a fatter plasma cost something”; counts `70 / 10 / 14`; added result summary and plain-text source citation.
- `#frame-10` (HTML line 204): “10. Compute the plant's pumping power, cycle efficiency and availability from the design”; counts `76 / 14 / 14`; added result summary and plain-text source citation.
- `#frame-11` (HTML line 204): “11. Fix the defects found by the fusion model audit”; counts `77 / 18 / 14`; added result summary and plain-text source citation.
- `#frame-12` (HTML line 204): “12. Restructure the model into nested physical parts without changing its numbers”; counts `77 / 18 / 23`; added result summary and plain-text source citation.
- `#frame-13` (HTML line 204): “13. Price the winding pack and conductor so magnet results can move off the reference design”; counts `80 / 18 / 23`; added result summary and plain-text source citation.
- `#frame-14` (HTML line 204): “14. Make winding length, cooling load and support structure follow the coil the model builds”; counts `86 / 18 / 23`; added result summary and plain-text source citation.
- `#frame-15` (HTML line 204): “15. Price conductor tape by its physical length”; counts `86 / 18 / 23`; added result summary and plain-text source citation.
- `#frame-16` (HTML line 204): “16. Check that the winding pack fits inside its casing”; counts `87 / 19 / 23`; added result summary and plain-text source citation.
- `#frame-17` (HTML line 204): “17. Estimate conductor critical current and operating margin”; counts `88 / 20 / 23`; added result summary and plain-text source citation.
- `#frame-18` (HTML line 204): “18. Account for what the magnet manufacturing charges cover”; counts `89 / 20 / 23`; added result summary and plain-text source citation.
- `#frame-19` (HTML line 204): “19. Size the magnet tape inventory from the required current”; counts `90 / 20 / 23`; added result summary and plain-text source citation.
- `#frame-20` (HTML line 204): “20. Trace divertor heat from plasma exhaust to peak load”; counts `90 / 20 / 23`; added result summary and plain-text source citation.
- `#frame-21` (HTML line 204): “21. Calculate tritium breeding from the blanket”; counts `92 / 20 / 23`; added result summary and plain-text source citation.
- `#frame-22` (HTML line 204): “22. Installed cooling equipment costs”; counts `97 / 20 / 30`; added result summary and plain-text source citation.
- `#frame-23` (HTML line 204): “23. Buildings sized from equipment and maintenance needs”; counts `133 / 25 / 57`; added result summary and plain-text source citation.
- `#frame-24` (HTML line 204): “24. Fuel inventory, startup stock and processing throughput”; counts `134 / 25 / 64`; added result summary and plain-text source citation.
- `#frame-25` (HTML line 204): “25. Fuel-processing cost that follows throughput”; counts `135 / 25 / 64`; added result summary and plain-text source citation.
- `#frame-26` (HTML line 204): “26. Cost-estimate maturity and uncertainty”; counts `135 / 25 / 64`; added result summary and plain-text source citation.
- `#frame-27` (HTML line 204): “27. Getting the current model ready for comparison”; counts `138 / 28 / 76`; added result summary and plain-text source citation.
- `#frame-28` (HTML line 204): “28. Keeping supplied design choices through evaluation”; counts `199 / 67 / 76`; added result summary and plain-text source citation.
- `#frame-29` (HTML line 204): “29. How far the repaired model can be evaluated”; counts `199 / 67 / 76`; added result summary and plain-text source citation.
