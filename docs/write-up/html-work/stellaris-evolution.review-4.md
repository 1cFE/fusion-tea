# Review — stellaris-evolution.html

page: docs/write-up/stellaris-evolution.html
source: docs/write-up/stellaris-evolution.md
reviewed against: docs/write-up/html-render-prompt.md, docs/write-up/writing-prompt.md, /home/reid/.claude/skills/_my_mental_model_v2/feedback/html.md, /home/reid/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Findings

1. The metric sparklines have no reading guide explaining the grey full history, blue history through the selected frame, selected-frame dot, or separate vertical scales. The guide at line 158 explains graph navigation; the legend at line 7038 explains calculation changes. Neither explains the charts generated at lines 7050–7092. The accessible chart labels give endpoints but do not explain these marks. (Cites: writer prompt, “New visuals, only where they help,” requiring a reading guide and labels; HTML feedback, “Caption carrying the fact that decodes the figure,” preferring the decoding fact beside the chart.)

2. Page-local styles extend beyond diagram layout. Lines 125–127 set viewer heading and prose sizes, and lines 135–152 style the evidence table outside the viewer. The earlier viewer style blocks also define typography and colors. The viewer exception explicitly exempts its scripts; it does not explicitly exempt styling from the shared-style rule. The table and reading typography are concrete departures even if inherited viewer styling is accepted. (Cites: writer prompt, “Style”: a small local style block is for diagram layout; everything else comes from write-up.css.)

3. Several added frame summaries use internal workflow shorthand without explaining it: frame 5, “closed by redirect”; frame 10, “17 of 23 rubric cells at target”; frames 22–25, “Independent review passed it at the target depth”; frame 27, “adopted ... as r3”; frame 29, “File-read verification and a synthetic comparison adapter.” These occur in the result cells at line 204 and in the selected-frame summary populated at lines 7144–7145. A reader cannot tell what the review establishes or what these workflow outcomes mean. Frame 5’s title, “Making the escape levers carry real costs,” adds a metaphor without explaining its referent. (Cites: writing-prompt.md, “Show enough machinery to make the process imaginable” and “Keep examples focused and evidence intact”: explain terms and runbook phrases in ordinary language; voice guidance against metaphors doing the explaining.)

## Mechanical fidelity check

Extracted HTML heading, paragraph and list-item text with Python’s HTMLParser and compared every nonblank source block in sequence, normalizing whitespace and applying the permitted repository-link-to-path transformation. All 37 source blocks matched: seven headings, nine paragraphs and 21 list items. No dropped, reordered or reworded source block was found. The source contains no tables, figures or code blocks. The seven source headings retain their GitHub-style anchor IDs. Support links become .html, the main-post link remains .md, and repository references become code.path text. “Part 3” in section 5 gains a working harness.html link without changing its wording.

## Added-text inventory

### Navigation and opening

- Browser title: “Stellarator model evolution” (line 5).
- Rail: “1cFE write-up · Part 4,” “Modeling Stellaris,” “Model evolution viewer,” “Frame records,” arrow markers, and repeated source section names (line 156).
- Viewer heading and reading guide: “Model evolution viewer”; “Step through the goals with the slider or arrows. Select a part to open it, then select a calculation to see its inputs and equations. Frame links in the themes return here. Expand gives the graph the whole window.” (line 158).
- Script-disabled note: “The interactive graph needs JavaScript. All six themes and the frame records below remain available.” (line 158).

### Interactive viewer

- Toolbar: “Snapshot” (hidden picker), “Expand all,” “Collapse all,” “Fit,” “Reset layout,” “Spacing,” “1×,” and “Find” (lines 159–174).
- Frame navigation: arrow buttons, frame position, frame-title options, “Open changed parts,” “Expand,” “Full screen,” loading/status text, expanded-view summary and accessibility/tool-tip instructions (lines 7020–7037 and associated update handlers).
- Change legend: “new calc,” “changed calc,” “moved calc,” and “Closed parts show the change color of their hidden calculations.” (line 7038).
- Metrics: “Calcs,” “Checks (constraints),” “Parts,” “Attributes,” “Calc-to-calc links,” and “Model source files”; values, previous-goal deltas, “starting point,” “no change from previous goal,” chart endpoint descriptions and frame/value tooltips (lines 6926–6933, 7050–7092).
- Selected-frame narrative: frame title; commit, fingerprint, date and work-item metadata; “Question” with attribution grade and question/source text; “Where the goals started” or “Result (condensed by an agent from the source below),” followed by the result and source. Results duplicate the frame-record entries described below (lines 7134–7146).
- Change inventory: new/changed/moved/removed calculations, new/changed/removed checks, new/removed parts, documentation-only changes, changed recorded values, attribute counts, names, containing parts, definitions and rewired inputs. Includes “handwritten body,” “Formula: before and after,” “Python body: what changed,” “Python body (… lines),” code/diff content, truncation notices and empty-state explanations (lines 7107–7172).
- Selected graph nodes supply model names, inputs, equations, attributes, documentation, source pointers and dependency information through the viewer’s detail panel. These are data-dependent additions, rather than source-markdown prose.

### Sections 1–6

No new explanatory prose. All six sections add plain repository paths after their original link labels and clickable frame numbers. Section 5 additionally links “Part 3.” The path additions belong to the allowed link adaptation, not a rewrite of the source blocks.

### Frame records

The closed evidence panel at line 204 adds “In the record,” “Frame records,” the introduction “Counts come from each committed snapshot. Results below are the viewer’s agent condensations of the cited records; they have not been owner-reviewed. The six themes above use the checked write-up text.” and the column headings “Frame,” “Calculations / checks / parts,” and “Recorded result and source.” Every row adds a frame title, a three-number snapshot count, an agent-written result paragraph and repository/commit references. The following inventory identifies the added subjects without reproducing those paragraphs:

| Rows / location | Added result subjects |
| --- | --- |
| #frame-1 | Starting model, migration history, earlier goals and routed pumping correction. |
| #frame-2–#frame-4 | Pumping correction and cost/check results; magnet calculations and cost change; confinement and heating feasibility. |
| #frame-5–#frame-9 | Coil sizing and failed studies; wall/heating corrections; ash-profile correction; burn-control study; bore-dependent magnet behavior and study outcome. |
| #frame-10–#frame-12 | Plant closure and grading; audit dispositions; structural reorganization and numerical comparison. |
| #frame-13–#frame-15 | Magnet cost decomposition and study limits; coil geometry/thermal changes; tape procurement correction and constraint results. |
| #frame-16–#frame-17 | Casing fit and current-margin failures, study pass counts and assumptions. |
| #frame-18–#frame-20 | Manufacturing charge coverage and cost changes; optional tape sizing and feasibility limits; divertor power accounting and study results. |
| #frame-21–#frame-23 | Breeding calculation and constraint tradeoff; cooling equipment and cost change; facilities and cost change. |
| #frame-24–#frame-26 | Fuel inventory/startup/throughput quantities; fuel-processing cost changes; estimate maturity and uncertainty envelope. |
| #frame-27–#frame-29 | Steam-cycle comparison and adopted package; preservation of equipment choices and capacity checks; supported-domain limits and verification scope. |

## Scope

This is a source-level pattern and fidelity review. Repository evidence was not opened, so the added technical claims are not fact-checked. No browser render was performed. Viewer scripts were treated as exempt as instructed. Main-flow headings remain expanded; the evidence table is closed by default. No external resource tag was found beyond the shared stylesheet, whose remote font import is allowed.
