# Write-up plan

Rough working plan for the final write-ups covering agentic-mbse, sysml-codegen and fusion-tea. Captured 2026-09-25 from the owner's description. `[OWNER]` marks what the owner stated; `[AGENT]` marks suggestions for discussion.

## Shape

[OWNER] One primary post, as succinct as possible, in the owner's own voice, very easy to read and follow. Dedicated HTML write-ups support it, one per part where a part needs one.

- Primary post outline: [fusion-tea-exploratory-modeling.md](fusion-tea-exploratory-modeling.md)
- Writing guidance for agents filling in supporting content: [writing-prompt.md](writing-prompt.md)
- Existing published context: [the earlier post on agentic modeling and SysML v2](https://1cf.energy/searching-the-fusion-design-space-systematically/)

## The five parts and their support

| Part | Support | Status |
|---|---|---|
| 1. Why SysMLv2 | The existing blog post | Done. Main post only needs the short argument (strict semantics fight AI entropy; composability enables categorical trade studies). |
| 2. Model execution and studies | [sysml-codegen-model-evaluation.md](sysml-codegen-model-evaluation.md), to become HTML | Prose revised through the writing prompt. Figures and evidence live in `sysml-codegen-assets/`. Needs HTML conversion. |
| 3. The full harness | [harness.md](harness.md) (outline: [harness-outline.md](harness-outline.md); figure: `harness-assets/`) | Drafted: sections 1–8 filled in and revised with the owner, 2026-09-26. Figure 1 (the goal loop) done. Open: whether section 4 gets a figure; HTML conversion. |
| 4. The demo, support 1: modeling Stellaris | Evolution viewer (`feat/model-viz-evolution`, page at `~/1cfe/stellarator_evolution.html`) plus [stellaris-evolution-outline.md](stellaris-evolution-outline.md) | Viewer built, 29 frames (baseline plus 28 goals). Outline at the right shape as of 2026-09-26. Next: fill-in as notes beside the frames, then merge into the viewer page. |
| 4. The demo, support 2: the ARIES test | [aries-model-transfer-outline.md](aries-model-transfer-outline.md) | Narrative draft awaiting owner discussion. |
| 5. Takeaways and forward outlook | Probably none | Main post only. |

## Strategy and sequencing

[OWNER]

1. Highest-level story first. Done: the main post outline exists.
2. Supporting explainers next. For each: first make the flow and story clear in outline form, then an agent uses the writing prompt to fill in the content.
   - **Outline stage shape** (settled 2026-09-25 on [harness-outline.md](harness-outline.md), which is the reference example). One numbered beat per section. Each beat is a bold title, one sentence of setup if needed, then the point in one sentence, then a few short bullets. Every sentence says an idea in plain words; no naming parts or systems as shorthand for the idea. No evidence paths, no figure specs, no sub-sections. The whole outline fits on one screen. Evidence and detail belong to the fill-in stage.
   - **Fill-in stage.** An agent takes the settled outline and [writing-prompt.md](writing-prompt.md) and drafts the prose, section by section, with evidence links and figures.
3. Once all supporting pieces are ready, return to the main post and integrate diagrams, plots and links to the supports.

Working order for step 2, by readiness and dependency:

1. Part 3 (the gap; the main post's Part 3 and Part 4 both lean on the goal and round vocabulary it establishes). Drafted 2026-09-26.
2. Part 4 support 1: capture the Stellaris evolution using the viewer.
3. Part 4 support 2: discuss and settle the ARIES narrative, then fill.
4. Part 2: convert the evaluation article to HTML.
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

Open for Part 3:

- Whether section 4 gets a figure. The outline proposed the evolution viewer's before-and-after frame for this goal; the viewer's frame texts are agent condensations and would need checking against the goal's trail.
- HTML conversion, with the other supports.

## Part 4, support 1: capturing the Stellaris evolution

[OWNER, 2026-09-25] The viewer is the page. The narrative is context added to it, since most readers will step through the frames rather than read a separate piece.

[OWNER, 2026-09-26] The narrative is organized by what drove the model's evolution, not by chronology: six themes (replacing typed-in numbers with physics; making the model push back; making cost follow the design; following the engineering design pattern; reconciling against Stellaris; fixing defects). Each theme names its example frames. The viewer carries the sequence. The outline is in [stellaris-evolution-outline.md](stellaris-evolution-outline.md), with a one-line close pointing at support 2.

[AGENT] Notes for fill-in:

- The viewer's frame result texts are agent condensations and not owner-reviewed (per the commit on `feat/model-viz-evolution`). Every number in the outline came from those texts and must be checked against each goal's `trail.md` at fill-in.
- Existing narratives under `work/narratives/` (ten goal narratives from early September, plus a goal overview) are candidate raw material, though they predate the later goals.
- The main post's count of nine goals and ten studies is from mid-September. The viewer's 28 goals is current.
- Where the theme notes live on the page (beside the slider, grouped frames, or a panel) is a fill-in and HTML decision, not settled.

## Part 4, support 2: the ARIES test

[OWNER, 2026-09-25] Organizing sequence settled: generalization hypothesis, brief false-start disclosure, design-instance-only test, required model enhancements, resulting studies. Explanations and takeaways are proposed editorial synthesis; linked records supply the evidence.

Next step: owner discussion of the draft, then fill using the writing prompt, then HTML.

## Cross-cutting

- [OWNER] All supporting pieces end up as HTML. Markdown stays the drafting format until the story is settled.
- [AGENT] Decide one HTML style and layout for all supports before converting any of them, so Part 2 does not get converted twice. The `html-explainer` skill and `docs/demo/` pages are the existing house style.
- [AGENT] Keep the evidence links in each support pointing at repo paths, and decide before publishing whether the published HTML links into the public repo or inlines the evidence.
- [AGENT] Update this plan as pieces move. It is a working note, not a record.

## Open questions for discussion

1. Part 3 scope: one HTML piece covering all four topics, or two (the workflow and PM recap; the goal layer and checks)?
2. How much of "moving forward" belongs in Part 3 versus Part 5 of the main post? [OWNER, 2026-09-26] Part 3 ends with its own assessment and open question (section 8); the forward outlook stays in Part 5.
3. Stellaris evolution: settled [OWNER, 2026-09-25 and 2026-09-26]. The viewer is the page; the narrative is six themes with example frames, not a walk or a chronology. See the Part 4 support 1 section.
4. Figures for the main post: which come from the supports, and which are new (the nested-circles harness figure)? The repo-size figure is dropped [OWNER, 2026-09-26].
