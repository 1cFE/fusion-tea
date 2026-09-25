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
| 3. The full harness | [harness-outline.md](harness-outline.md) | Story outline drafted 2026-09-25, awaiting owner discussion. |
| 4. The demo, support 1: modeling Stellaris | Evolution viewer (`feat/model-viz-evolution`, page at `~/1cfe/stellarator_evolution.html`) | Viewer built, 29 frames (baseline plus 28 goals). Capture of the evolution as a narrative still TODO. |
| 4. The demo, support 2: the ARIES test | [aries-model-transfer-outline.md](aries-model-transfer-outline.md) | Narrative draft awaiting owner discussion. |
| 5. Takeaways and forward outlook | Probably none | Main post only. |

## Strategy and sequencing

[OWNER]

1. Highest-level story first. Done: the main post outline exists.
2. Supporting explainers next. For each: first make the flow and story clear in bullet or outline form, then an agent uses the writing prompt to fill in the content.
3. Once all supporting pieces are ready, return to the main post and integrate diagrams, plots and links to the supports.

Working order for step 2, by readiness and dependency:

1. Part 3 outline (the gap; the main post's Part 3 and Part 4 both lean on the goal and round vocabulary it establishes).
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
- Harness size and shape data for the "repo size over time, actively used vs left behind" figure the main post sketches: `.project/active/harness-right-size/report.md` may already have counts.

[AGENT] Proposed outline for discussion:

1. What the harness is for: the goals above, and why a plain chat loop does not hold up as the model grows.
2. The filesystem view: `models/`, `knowledge/`, `work/`, `.project/`, `exploration/` and what each owns. One diagram.
3. The logical view: goal → round → tasks → native workflows (modeling PM, research, study) → review → learnings. One diagram.
4. A goal round walked once, using the example the main post sketches (Research, Ingest, Update model X, Update model Y, Study, Eval).
5. The checks that keep it honest: citations, the integration gates, fresh review, owner-held gates.
6. What we would change next.

## Part 4, support 1: capturing the Stellaris evolution

[OWNER] TODO: capture the evolution using the viewer.

[AGENT] Notes and questions:

- The viewer's frame result texts are agent condensations and not owner-reviewed (per the commit on `feat/model-viz-evolution`). The captured narrative should be checked against `trail.md` of each goal it features, not against the frame text.
- Existing narratives under `work/narratives/` (ten goal narratives from early September, plus a goal overview) are candidate raw material for the story, though they predate the later goals.
- The main post's thread (heating gap traced to helium ash, then ignited-plasma feasibility, then a new constraint) is the natural spine. Question for the owner: does support 1 walk all 28 goals briefly, or pick three to five turning points and use the viewer for the rest?
- Format question: does the evolution viewer itself become the HTML support, with a short narrative layer added, or is it embedded or linked from a separate HTML page?

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
2. How much of "moving forward" belongs in Part 3 versus Part 5 of the main post?
3. Stellaris evolution: full walk or turning points? Viewer as the support, or a page around it?
4. Figures for the main post: which come from the supports, and which are new (the repo-size figure, the nested-circles harness figure)?
