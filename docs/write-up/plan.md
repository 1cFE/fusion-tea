# Write-up plan

Rough working plan for the final write-ups covering agentic-mbse, sysml-codegen and fusion-tea. Captured 2026-09-25 from the owner's description. `[OWNER]` marks what the owner stated; `[AGENT]` marks suggestions for discussion.

## Shape

[OWNER] One primary post, as succinct as possible, in the owner's own voice, very easy to read and follow. Dedicated HTML write-ups support it, one per part where a part needs one.

- Primary post outline: [fusion-tea-exploratory-modeling.md](fusion-tea-exploratory-modeling.md)
- Writing guidance for agents filling in supporting content: [writing-prompt.md](writing-prompt.md)
- HTML conversion of a settled support, with its review loop: [html-prompt.md](html-prompt.md) (draft, 2026-09-26, not yet owner-reviewed)
- Existing published context: [the earlier post on agentic modeling and SysML v2](https://1cf.energy/searching-the-fusion-design-space-systematically/)

## The five parts and their support

| Part | Support | Status |
|---|---|---|
| 1. Why SysMLv2 | The existing blog post | Done. Main post only needs the short argument (strict semantics fight AI entropy; composability enables categorical trade studies). |
| 2. Model execution and studies | [sysml-codegen-model-evaluation.html](sysml-codegen-model-evaluation.html) (source: [sysml-codegen-model-evaluation.md](sysml-codegen-model-evaluation.md); figures and evidence: `sysml-codegen-assets/`) | Done: HTML accepted by the owner, 2026-09-26. Retitled "Executing the trade studies on a SysML v2 plant model" [OWNER]. The page adds four interactive figures (field equation, calculation graph, breeding surrogate, feasibility map), approved by the owner for this page. |
| 3. The full harness | [harness.html](harness.html) (source: [harness.md](harness.md); outline: [harness-outline.md](harness-outline.md); figures: `harness-assets/`) | Done: HTML accepted by the owner, 2026-09-26. The page adds nine figures, three of them interactive (the goal loop, the repository areas, the checks), with the detail in collapsed sections. `harness.md` stays the full-text source; the page deliberately carries less text than it. |
| 4. The demo, support 1: modeling Stellaris | Evolution viewer (`feat/model-viz-evolution`, page at `~/1cfe/stellarator_evolution.html`) plus [stellaris-evolution.md](stellaris-evolution.md) (outline: [stellaris-evolution-outline.md](stellaris-evolution-outline.md); evidence: `stellaris-evolution-assets/`) | Done, per the owner, 2026-09-26: [stellaris-evolution.html](stellaris-evolution.html). Viewer built, 29 frames (baseline plus 28 goals); six theme notes with evidence links, every outline number checked against the goal records. |
| 4. The demo, support 2: the ARIES test | [aries-model-transfer-outline.md](aries-model-transfer-outline.md) | Done, per the owner, 2026-09-27: [aries-model-transfer-outline.html](aries-model-transfer-outline.html). |
| 5. Takeaways and forward outlook | Probably none | Main post only. |
| Main post | [main-post-draft.md](main-post-draft.md) (figures: `main-post-assets/`) | Drafted 2026-09-27; the owner is happy with it. See the Main post section. |

## Strategy and sequencing

[OWNER]

1. Highest-level story first. Done: the main post outline exists.
2. Supporting explainers next. For each: first make the flow and story clear in outline form, then an agent uses the writing prompt to fill in the content.
   - **Outline stage shape** (settled 2026-09-25 on [harness-outline.md](harness-outline.md), which is the reference example). One numbered beat per section. Each beat is a bold title, one sentence of setup if needed, then the point in one sentence, then a few short bullets. Every sentence says an idea in plain words; no naming parts or systems as shorthand for the idea. No evidence paths, no figure specs, no sub-sections. The whole outline fits on one screen. Evidence and detail belong to the fill-in stage.
   - **Fill-in stage.** An agent takes the settled outline and [writing-prompt.md](writing-prompt.md) and drafts the prose, section by section, with evidence links and figures.
3. Once all supporting pieces are ready, return to the main post and integrate diagrams, plots and links to the supports.
4. Publish and clean up, before the PR. [OWNER, 2026-09-26] Once all the HTML pages are finished, move them to a clean spot in the folder GitHub Pages publishes from, probably next to [the demo page](https://scoring.1cf.energy/demo/index.html#the-question). Before the PR:
   - Fix all the links.
   - Archive all the supporting docs and prompts.
   - [AGENT] Where Pages publishes from: this repo's `docs/` folder on `main`, served at scoring.1cf.energy (`docs/CNAME`). The demo page is `docs/demo/index.html`, so a folder beside it, `docs/<name>/`, publishes at `scoring.1cf.energy/<name>/`. There is no `.nojekyll`, so Jekyll also publishes markdown: anything left under `docs/` when the branch merges, including `docs/write-up/` with its drafts, prompts and `html-work/`, becomes public. The archive therefore has to land outside `docs/`.
   - [AGENT] Links found in the pages on 2026-09-26: each links `write-up.css` and the other pages by relative path, so those files move together. Two links point at the main post as `fusion-tea-exploratory-modeling.md`, which needs its published address. One points at `aries-model-transfer-outline.html`, which does not exist yet.

Working order for step 2, by readiness and dependency:

1. Part 3 (the gap; the main post's Part 3 and Part 4 both lean on the goal and round vocabulary it establishes). Drafted 2026-09-26; HTML accepted 2026-09-26.
2. Part 4 support 1: capture the Stellaris evolution using the viewer. Drafted 2026-09-26; HTML done 2026-09-26.
3. Part 4 support 2: discuss and settle the ARIES narrative, then fill.
4. Part 2: convert the evaluation article to HTML. Done 2026-09-26.
5. Return to the main post.

## Part 3: the full harness (the gap)

[OWNER] Needs a supporting piece that synthesizes:

- The run-goal model: what a goal is, what a round is, tasks under a strategy, the six close triggers, fresh review.
- Research and ingestion.
- A recap of the agentic-mbse `work` framework (the modeling PM: backlog, spec, design, plan, implement, validation).
- Traceability and checks: citations, the integration seam and its gates, the study evidence contract.
- Possibly what we would do moving forward.

Main post framing to preserve (from the outline): a harness is a large set of tools and prompts scaffolded by a file system and rules. The goals are high performance, reasonable token efficiency, and stability as the system grows. Two views to show: the filesystem view (where to find things) and the logical view (tasks, responsibilities, sequencing).

[AGENT] Candidate source material for the outline, all already written:

- Goal layer: `work/orchestration/GOAL_RUNBOOK.md` (the five surfaces, rounds, tasks, fresh review) and `.project/adr/0001` through `0007` for the reasoning behind it.
- Research seam: `docs/research_seam_operator_guide.md` and `knowledge/research/` (pending, approved, impacts, requests).
- Modeling PM: `CLAUDE.md` § Project Management, `modeling_project/MODELING_PROCESS.md`, `work/EPIC_GUIDE.md`.
- Traceability and checks: MR-4 and MR-7 in `modeling_project/REQUIREMENTS.md`, `docs/integration_seam_operator_guide.md` (ten gates), ADR-0008 through 0010, `.claude/skills/run-study/runbook.md`.
- Existing visuals to consider reusing or redrawing: `docs/workflow.d2` and `docs/workflow.png`, `docs/demo/closed-loop.html`.

The outline is in [harness-outline.md](harness-outline.md); the drafted piece is [harness.md](harness.md).

**Status, 2026-09-26.** All eight sections are drafted. Sections 1–3 and Figure 1 were settled in an earlier session; sections 4–8 were filled in and revised with the owner on 2026-09-26. Sections 4–7 follow one worked example, the `stored-energy-basis` goal: section 4 walks both rounds task by task, section 5 its research request, section 6 its work item (WI-042), and section 7 the checks it passed, each with an example of what it caught.

Decisions taken during fill-in:

- [OWNER] Beat 8 became a wrap-up, "Where the harness stands", and stays in Part 3. The outline's beat 8 bullets were dropped. The wrap-up answers whether the harness meets its targets, in the owner's terms: it is still being refined; it runs the demo's goals about 95 percent autonomously; its analysis has been credible but has relied on ground truth; the open question is whether its own checks suffice in a domain without ground truth.
- [OWNER] The repo-size figure is dropped as a tangent.
- [OWNER] Table 2 (the rounds against Figure 1) was cut as a forced synthesis.
- [OWNER] Section 6 summarizes the modeling workflow and links the earlier post instead of re-explaining it, then shows the example: the spec, the ash-rule code excerpt, and the predicted-versus-actual table.
- [AGENT] (ratified by owner, 2026-09-26) Section 7 ends by pointing to the Part 4 hold-out test as the test of whether the model predicts a real plant; section 8 cites the four integrated ARIES goals (Part 4) as the low-input example.
- [AGENT] Corrections to the outline found against the record: round 1's research wrote no "found nothing" record (the run returned `REGISTERED` with two candidates queued); the quarantine is checked by the script only at registration, with the before-fetch screen an instruction in the research agent's prompt; WI-042 changed two calculations, not one.

**HTML, 2026-09-26.** [OWNER] Accepted [harness.html](harness.html). Section 4 got its figures from the goal's own record (the discrepancy chain, a task strip for each round, the stored-energy values), so the evolution viewer's frame was not used. Markdown changes made with the owner during the conversion: section 2 now allows independent tasks to run in parallel and says the question, not the goal, is fixed while it runs; section 4 is split into Goal, Round 1 and Round 2; section 1's "four values" wording now matches the record; a missing period in section 2 was restored.

## Part 4, support 1: capturing the Stellaris evolution

[OWNER, 2026-09-25] The viewer is the page. The narrative is context added to it, since most readers will step through the frames rather than read a separate piece.

[OWNER, 2026-09-26] The narrative is organized by what drove the model's evolution, not by chronology: six themes (replacing typed-in numbers with physics; making the model push back; making cost follow the design; following the engineering design pattern; reconciling against Stellaris; fixing defects). Each theme names its example frames. The viewer carries the sequence. The outline is in [stellaris-evolution-outline.md](stellaris-evolution-outline.md), with a one-line close pointing at support 2.

[AGENT] Notes for fill-in:

- The viewer's frame result texts are agent condensations and not owner-reviewed (per the commit on `feat/model-viz-evolution`). Every number in the outline came from those texts and must be checked against each goal's `trail.md` at fill-in.
- Existing narratives under `work/narratives/` (ten goal narratives from early September, plus a goal overview) are candidate raw material, though they predate the later goals.
- The main post's count of nine goals and ten studies is from mid-September. The viewer's 28 goals is current.
- Where the theme notes live on the page (beside the slider, grouped frames, or a panel) is a fill-in and HTML decision, not settled.

**Status, 2026-09-26.** Drafted in [stellaris-evolution.md](stellaris-evolution.md) as the outline's lead and six beats with corrected numbers and one evidence link per example, about 1,000 words. A first fill-in expanded it to 3,200 words and the owner rejected it as far too wordy; the outline was already most of the piece. Every number came from the goal's trail or answer, not the viewer's frame texts; the per-frame design-point cost, with sources, is in [stellaris-evolution-assets/design-point-cost.md](stellaris-evolution-assets/design-point-cost.md). The viewer's tile counts in the lead were reproduced by rebuilding the page from the branch's build script (byte-identical to the owner's page).

[AGENT] Corrections to the outline found against the record, applied in the draft:

- Frame 2: the recirculating-power limit fired at 32 of 948 points before the fix, not never; the factor is 130 to 195, not 150.
- Frame 4: the "field bought nothing" finding is from a 2026-08-23 grid study, not optimizer runs.
- Frame 5: the lever priced was coil current; the conductor grade stayed free until frame 13. The goal's two unpriced levers were conductor grade and heating.
- Frame 13: the winding-pack multiplier was replaced, not split, and the cost before it was 224 $/MWh, not 146 (146 is frame 14's result).
- Theme 3's "installation, spares and replacements" holds for cooling only; buildings size for spares without pricing them, and fuel processing carries installation only. The largest cost move of the run is cooling; plant closure (theme 1) and the winding-pack replacement are next.
- Frame 28: the reveal run stopped at the magnet's conductor check, not the first calculation; 111 upstream calculations had run. The 56.6 T value is recorded only for the rerun on the repaired model. The second post-reveal goal (frame 29) is a readiness assessment, not a repair.
- Frame 29: the range measured was the model's own exploratory window (R 4 to 20 m, a 0.8 to 2.2 m), not an ARIES-sized range.
- Frame 11: the audit produced 20 findings, several of them known limitations rather than defects; the finance failures were at equal interest and inflation rates and at zero discount rate.
- The reconciliation goal found the reference is not one coherent published design point, and classified differences by cause without per-class counts.
- Frame 1: the cost side of the starting model was already parametric; the physics side was held constants.
- "Checked that the result still matched the paper at the design point" holds for frames 3 and 4; breeding and the steam cycle reproduce no paper value, so the draft says the anchoring applied where the paper gave a value.
- Frame 6's fatter-plasma reading (a = 1.5 to 2.2 m) was superseded by frame 7 the next day; the draft does not present it.

Open for support 1:

- The cost evidence note is an addition beyond the outline and is not linked from the piece.
- The design-choice audit under `work/analysis/` is untracked, so the draft links the tracked post-reveal results note under `.project/active/aries-comparison-preparation/` instead.

## Part 4, support 2: the ARIES test

[OWNER, 2026-09-25] Organizing sequence settled: generalization hypothesis, brief false-start disclosure, design-instance-only test, required model enhancements, resulting studies. Explanations and takeaways are proposed editorial synthesis; linked records supply the evidence.

Next step: owner discussion of the draft, then fill using the writing prompt, then HTML.

**Status, 2026-09-27.** [OWNER] Asked an agent to critique the draft and then revise it to the point the owner would be happiest with. The file is a full draft, not an outline, about 3,450 words. The settled sequence is kept, with section 5 (the comparison with ARIES) between the enhancements and the studies, and a closing section 7 added.

[AGENT] Changes made, each checked against the linked records (not yet owner-reviewed):

- Title and opening line match the other supports and link support 1 and Part 3. "Part 1" and "Part 2" of the test became "the reuse test" and "the extension test", because the main post uses Part 1 to 5.
- Section 1 now introduces the library-and-plant idea and the two tests, says what ARIES-CS is, and links the quarantine.
- Section 2 now says what the false start was: the first run stopped in a winding-sizing calculation, and all four ARIES papers had been read, so later work is a post-reveal comparison.
- Section 3 now says what the run supplied: 3 ARIES inputs, 701 at the Stellaris design. The 56.6 T is Stellaris's coils at ARIES's radius, 14.7 T on axis against ARIES's 5.7 T.
- Section 5 cost: our 891 MW case is $686/MWh, more than 90% of it purchased tritium, because breeding is unsupported. ARIES assumes self-sufficient breeding. The $59/MWh figure applies ARIES's conventions.
- Section 5 power: the series exchanger error and the published-inconsistency finding are now stated.
- Section 6 opens with a table of each study's plant and cost basis. The four comparisons use different plants and cost years, and the draft had not said so.
- Parameter study: the headline is now the record's own, 427 to 621 MW (+45%) from the design ratio 1.518, not from 1.45.
- Component study: now explains Brayton's poor output by temperature. The Brayton turbine inlet is 686 K (413 °C) against ARIES's 708 °C, read from the study's stored outputs. It also notes the earlier conversion-only study found the two options within $5/MWh.
- Architecture study: the bypass dependence moved up next to the result, and it applies to both layouts. The study now says the split network is ARIES's own arrangement.
- Section 7 is new: a verdict in four bullets, and an answer to Part 3's open question. It is proposed editorial synthesis.
- Section 6's closing summary was cut, as the writing prompt asks.

[OWNER, 2026-09-27] Restructured around two questions, which the owner preferred to the reuse and extension tests: "Can the model reproduce ARIES?" (sections 3.1 to 3.4) and "Can the combined model explore designs neither plant covers?" (sections 4.1 to 4.4, the three studies). Each question ends with its answer, and section 5 closes. The two-question framing was the agent's proposal, ratified by the owner. The point about stopping early in answer 1 is the owner's: "we made the big changes, but decided (for time reasons) to call it before closing every gap."

[OWNER, 2026-09-27] Section 5 re-angled during the HTML conversion, because the main sections already answer the two questions: "I wonder if it would be more interesting and additive to take a different angle." The logic: (1) the harness seems to be working, shown by the growth in calculations, checks and parts in the later goals in support 1's plots, and goals seemed to finish faster; (2) the framework seems to be working, holding up across two design points and producing studies; so we should keep pushing across design sets, keep pushing in detail, and try for more interesting knowledge transfer, e.g. "develop strong component models from first principles where the primary source papers don't have detail". The harness point stays short. Section 5 does not revisit the false start, because section 2 covers it and the owner judged it already over-emphasized. [AGENT] Redrafted to that logic; awaiting owner review. The main post draft says magnet and conductor models were added for ARIES; they were not (3.4 lists them as open). Fixed in the main post draft, 2026-09-27.

Open for the owner: whether the answers in 3.4, 4.4 and 5 say what the owner wants to claim, and whether the length is acceptable given that section 6's detail can collapse in the HTML. The parameter figure was left as is: its x-axis still runs up in ratio, so the caption says to read right to left.

## Main post

**Status, 2026-09-27.** Drafted in [main-post-draft.md](main-post-draft.md), built on the owner's outline, which stays unchanged. [OWNER] Happy with the draft.

Decisions taken while drafting:

- [OWNER] A human voice that keeps the character and points of the owner's notes, not the plainer voice of the supports. "I" for motivation and opinion, "we" for the work.
- [OWNER] Honest about what this is: a proof of concept. Results "suggest"; no conclusions, and study numbers are not to be trusted. The intro, the steam-versus-Brayton figure and Part 4's "What to make of it" carry this.
- [OWNER] The ARIES false start and the model refusing to calculate are not takeaways. The "didn't stay blind" paragraph was removed; the ARIES support covers it.
- [OWNER] Part 2 is features and limitations: three types of study, feasibility through constraints, DAG computation.
- [OWNER] Part 4's question 2 is framed as the test of whether all this was worth building, and ties back to Parts 1 to 3.
- [OWNER] Part 5 points are the owner's: coupled solvers as a path forward, system models as the context layer, "systems as code", and the companies Sensmetry, Flow Engineering, Dalus and Spread AI.

Figures (static PNG for Substack): `main-post-assets/design-iteration.png` (new, HTML-rendered, titled "Two levels of design iteration"), `harness-assets/goal-loop.png`, `main-post-assets/model-growth.png` (new, from the viewer's per-goal counts), `aries-study-assets/parameter-pressure-ratio.png`, `main-post-assets/steam-vs-brayton.png` (new) and `aries-study-assets/architecture-nominal-pair.png`. The nested-circles harness figure was not drawn.

## Cross-cutting

- [OWNER] All supporting pieces end up as HTML. Markdown stays the drafting format until the story is settled.
- [AGENT] Decide one HTML style and layout for all supports before converting any of them, so Part 2 does not get converted twice. [OWNER, 2026-09-26] This is a prerequisite for the HTML prompt. The owner's only reference, https://scoring.1cf.energy/demo/index.html, is one they do not care for. They want a nav bar on the left, and they use collapsible sections a lot to hide detail not every reader wants. [OWNER, 2026-09-26] Style settled: `write-up.css` follows the blog (Manrope, its warm grey-beige, navy and bright-blue accents), tuned to be easier to read, with a wide text column. [html-work/style-sample.html](html-work/style-sample.html) shows it in use; figures match it through `fonts/` and `figure_style.py`.
- [OWNER, 2026-09-26] The markdown keeps its repo links. The HTML replaces each with the file's path as plain text and, for important references, shows the referenced information on the page.
- [AGENT] Update this plan as pieces move. It is a working note, not a record.

## Open questions for discussion

1. Part 3 scope: one HTML piece covering all four topics, or two (the workflow and PM recap; the goal layer and checks)?
2. How much of "moving forward" belongs in Part 3 versus Part 5 of the main post? [OWNER, 2026-09-26] Part 3 ends with its own assessment and open question (section 8); the forward outlook stays in Part 5.
3. Stellaris evolution: settled [OWNER, 2026-09-25 and 2026-09-26]. The viewer is the page; the narrative is six themes with example frames, not a walk or a chronology. See the Part 4 support 1 section.
4. Figures for the main post: which come from the supports, and which are new (the nested-circles harness figure)? The repo-size figure is dropped [OWNER, 2026-09-26].
