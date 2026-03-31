# Epic: Concept Analysis Pipeline v2

**Epic ID**: ANALYSIS-V2
**Status**: Active
**Priority**: High
**Created**: 2026-03-28
**Estimated Effort**: ~2 weeks

---

## Executive Summary

Upgrade the concept analysis pipeline from a single-pass, fire-and-forget system to an iterative, human-steerable pipeline with clear stage separation, interactive vetting, sensitivity exploration, and incremental source addition. Each stage has a distinct focus: the **analysis loop** finds the shape of a concept (what matters, how it differs, what to model), the **review** verifies numerical accuracy and traceability, and an **interactive agent** lets a human build intuition and steer both.

**Critical Success Factor**: A human reviewer can efficiently vet and improve an analysis without re-running the entire pipeline from scratch.

---

## Why This Epic?

**Current State**:
- Analysis is a single Claude call producing all 8 sections — no iteration, no quality feedback
- Review stage conflates analysis quality (shape, completeness, hypotheses) with numerical accuracy (citation verification, calculation checks)
- No way to interactively explore a concept or ask questions about the analysis
- No sensitivity visualization to sanity-check cost model behavior
- Adding a new data source requires manual file shuffling and a full re-analysis
- Prompt templates embed goals/checklists inline — hard to maintain
- No shared learning across concepts — each analysis starts from zero context

**Future State**:
- **Iterative analysis loop**: analyze → assess → feedback → analyze, converging on "no findings" or max iterations. Each call is a fresh thread. Assessment focuses on ≤3 issues per pass.
- **Clear stage focus**: Analysis loop owns the *shape* (comparison, differences, modeling approach, hypotheses, risks). Review owns *accuracy* (traceability, citations, calculations).
- **Unified feedback format**: Assessment agent and interactive `/manage-concept` agent both produce structured feedback that gets fed back into the analysis agent via the same modal prompt.
- **Interactive `/manage-concept` agent** for human vetting with stage-aware behavior
- **Sensitivity explorer HTML** for each concept's cost model
- **`add-source` + `update-analysis`** commands for incremental data addition
- **Extracted goals/checklists** as maintainable standalone files
- **Cross-concept shared memory** via a memory-handler subagent

---

## Success Criteria

- [ ] Analysis loop converges (assessment finds no issues or hits max iterations) for ≥3 test concepts
- [ ] Each stage has documented, distinct goals — no overlap between analysis-assessment and review
- [ ] A user can interactively vet a concept via `/manage-concept N` and have identified changes flow reliably back through the analysis agent
- [ ] Sensitivity explorer HTML loads and shows correct baseline LCOE for all modeled concepts
- [ ] A user can add a PDF source and update an existing analysis without full re-run
- [ ] Pipeline goals and checklists are in standalone files, not buried in prompt templates
- [ ] Shared learnings persist across concept analyses and are consulted by agents

---

## Key Architecture: The Analysis Loop

Inspired by the ralph-init.sh generate → review → refine pattern, but adapted for domain analysis:

```
[sources + objectives + memory]
         |
         v
    ┌─ analyze ──┐       Fresh claude -p thread each call.
    │             │       Reads sources, objectives, exemplars, approved pool.
    │  analysis.md│       Uses subagents for heavy source reading.
    │             │
    └─────┬───────┘
          │
          v
    ┌─ assess ───┐       Fresh thread. Reads analysis.md + objectives + guidelines.
    │             │       Produces structured feedback (≤3 issues).
    │ feedback.md │       Same format as /manage-concept output.
    │             │
    └─────┬───────┘
          │
          ├─ no findings → done (proceed to model-setup)
          ├─ max iterations → done (proceed, human reviews)
          │
          └─ has findings → loop back to analyze
                           (passes feedback.md as input)
```

**The analyze prompt is modal** (one base prompt, three modes):
1. **Cold start**: No `analysis.md` exists → write first draft from sources
2. **Feedback pass**: `analysis.md` exists + `feedback.md` → act on the specific feedback
3. **Self-advance**: `analysis.md` exists, no feedback → assess current state and try to advance

**Analysis goals** (the *shape* of the concept — captured in standalone config file):
- How does the concept relate/compare to other concepts?
- What are the key differences from the mainstream approach?
- How do those differences affect TEA?
- What is the right way to model those differences, and capture the key hypotheses?
- Are the key risks and assumptions called out, and how do we capture them in the TEA?

**Assessment focus**: Quality of the analysis *shape*, not numerical accuracy. Does the analysis identify what matters? Are the hypotheses clear? Are the modeling recommendations actionable?

**Review focus** (separate stage, unchanged): Are the numbers traced to sources? Are citations real? Are calculations correct? Anti-hallucination.

**Feedback flow**: Both the automated assessment agent and the interactive `/manage-concept` agent produce feedback in the same structured format. Both get fed back into the analysis agent via the same modal prompt (feedback-pass mode). The existing `address-review` handles mechanical edits from the review stage's PA-N items.

---

## Backlog Items

### Item 1: Iterative Analysis Loop [3 days] — COMPLETE

**Type**: Implementation
**Effort**: 3 days (spec 2h, design 4h, plan 2h, execute 16h)
**Status**: Complete (2026-03-28)
**Dependencies**: None
**Work Item**: `.project/active/iterative-analysis-loop/` (spec, design, plan)

**Objective**: Replace the single-call analyze stage with an iterative analyze → assess → feedback loop, with extracted configuration and a structured feedback format.

**Scope**:

1. **Extract prompt configuration** into `prompt_templates/config/`:
   - `analysis_goals.md` — the 5 analysis shape goals
   - `assessment_checklist.md` — what the assessor checks against
   - `review_checklist.md` — numerical accuracy / traceability checks (for review stage)
   - `quality_standards.md` — citation format, anti-hallucination rules, depth expectations
   - Update `fill_template()` to support loading config files into template variables

2. **Unified analysis prompt** (`prompt_templates/analysis_v2.md`):
   - Modal: detects whether `analysis.md` and `feedback.md` exist
   - Cold start: reads sources, objectives, memory → writes full first draft
   - Feedback pass: reads existing analysis + specific feedback → makes targeted improvements
   - Self-advance: reads existing analysis, checks against objectives → identifies and fixes own gaps
   - Must use subagents for heavy source reading (context efficiency)
   - Prompt loads analysis goals from config

3. **Assessment prompt** (`prompt_templates/assessment.md`):
   - Reads `analysis.md` + objectives + assessment checklist
   - Produces `feedback.md` with structured findings (max 3 per pass)
   - Structured feedback format: entries with Target, Finding, Recommendation, Priority
   - Clear convergence signal: "PASS — no findings" or findings list
   - Does NOT check numerical accuracy (that's review's job)

4. **Loop orchestration** in `cmd_analyze`:
   - `--max-passes N` flag (default 3)
   - Each pass: invoke_claude (fresh thread) for analyze, then invoke_claude (fresh thread) for assess
   - Save each iteration's feedback as `feedback_iter_N.md` (audit trail)
   - Stop on "no findings" or max passes
   - Final `analysis.md` is the converged result

5. **Context budget management**:
   - Analysis agent uses subagents to read sources, returns summaries
   - Assessment agent reads only `analysis.md` + objectives + checklist (not raw sources)
   - Each call is a completely fresh `claude -p` thread

6. **Staleness propagation**: when `analysis.md` changes after initial creation (feedback pass, update-analysis, or manage-concept), mark downstream artifacts (model_setup, review, synthesis) as stale via frontmatter flag. Update `get_concept_state()` to report stale artifacts in status output.

**Out of Scope**:
- Changing the review stage (stays as-is, focused on accuracy)
- Multi-model strategy (use same model for both agents initially)
- Interactive feedback (that's Item 5)
- Human-driven change request workflow (that's Item 5)

**Success Criteria**:
- [x] No goals/checklists remain inline in prompt templates — all in `config/`
- [x] Loop runs end-to-end for ≥3 concepts (ran on concepts 09, 14, 22)
- [x] Assessment finds real issues on pass 1 that pass 2 fixes
- [~] Loop converges (pass 2 or 3 comes back clean) for most concepts — 1/3 converged (concept 14); see Lessons Learned re: tuning
- [x] Each thread stays well under context limit
- [x] `feedback_iter_N.md` files provide clear audit trail
- [x] `--max-passes 1` reproduces current single-pass behavior (backward compatible)
- [x] `status` command shows stale indicators for downstream artifacts

**Deliverables**:
- `prompt_templates/config/` directory with extracted config files
- `prompt_templates/analysis_v2.md` (modal analysis prompt)
- `prompt_templates/assessment.md` (assessment prompt)
- Updated `cmd_analyze` with loop orchestration and staleness propagation
- `feedback_iter_N.md` audit trail files

---

### Item 2: Build-Visuals Stage [1.5 days] — IN PROGRESS

**Type**: Implementation
**Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h) — revised scope is more ambitious
**Dependencies**: None
**Concept**: `.project/concepts/concept-explorer.md`
**Worktree**: `/home/reid/1cfe/fusion-tea_concept-explorer`

**Objective**: Add a stage that generates an interactive HTML sensitivity explorer from the cost model, allowing users to sanity-check parameter impacts before review.

**Scope**:
1. New prompt template `prompt_templates/build_visuals.md` — reads model_setup.py + model_output.txt + analysis.md, generates single-file HTML
2. New `cmd_build_visuals` subcommand
3. HTML output includes:
   - Sliders for each `forward()` parameter
   - Real-time LCOE recalculation (JS reimplementation of cost model)
   - Tornado chart ranking parameters by sensitivity
   - Baseline values matching `model_output.txt`
   - Parameter ranges keyed to confidence levels (high ±20%, medium ±35%, low ±50%)
4. Validation: baseline LCOE in HTML matches `model_output.txt`
5. Add to `stage1-all` between model-setup and review
6. Skip if `model_setup.py` doesn't exist

**Out of Scope**:
- Complex multi-CAS model visualization (start with top-level LCOE sensitivity)
- Server-side rendering or build tools (single-file HTML only)

**Success Criteria**:
- [ ] `run_analysis.py build-visuals N` produces `sensitivity_explorer.html`
- [ ] HTML opens in browser and shows functional sliders + tornado chart
- [ ] Baseline LCOE matches `model_output.txt` ±1%
- [ ] Works for all concepts that have `model_setup.py`

**Deliverables**:
- `prompt_templates/build_visuals.md`
- Updated `run_analysis.py` with `cmd_build_visuals`
- Example `sensitivity_explorer.html` for at least one concept

---

### Item 3: Source Addition and Incremental Updates [1.5 days] — COMPLETE

**Type**: Implementation
**Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)
**Status**: Complete (2026-03-29)
**Dependencies**: Item 1 (reuses feedback format, modal analysis prompt, staleness propagation)
**Conventions**: Must follow companion-directory + symlink layout established by source replacement (`.project/active/source-replacement/`)
**External Dep**: ~~`agentic-mbse[web]` feature (in progress on `webfetch-tools` branch)~~ — RESOLVED, merged. URL and PDF modes both work.
**Work Item**: `.project/active/source-addition/` (spec, design, plan)

**Objective**: Enable adding new data sources (PDF or URL) to a concept and incrementally updating the analysis without full re-run.

**Scope**:
1. New `cmd_add_source` subcommand:
   - Accepts a local PDF path or URL
   - Determines placement: add to latest existing `iter-NN/sources/` directory (supplementary material), not a new iteration. New `iter-NN` only if no iterations exist yet.
   - Runs extraction (`agentic-mbse extract <source> --save-source --output <sources-dir>/<name>/`)
   - Flattens nested PDF subdirectories if needed (same logic as source replacement)
   - Creates symlink: `<name>.md` → `<name>/output.md` (preserves relative image paths)
   - Prints confirmation with new source path
2. New `cmd_update_analysis` subcommand:
   - Accepts concept ID + `--sources` flag (specific new source files)
   - Invokes the analysis agent in feedback-pass mode with feedback constructed from the new source context
   - Triggers staleness propagation (from Item 1) after update

**Out of Scope**:
- Batch source enrichment for already-analyzed concepts
- Dossier auto-update
- Phase 1a prompt redesign

**Success Criteria**:
- [x] `run_analysis.py add-source 17a <pdf>` creates `iter-02/sources/<name>.md` (symlink) + `<name>/` companion dir with `output.md`, `metrics.json` — verified via checkpoint-test-concept17 (2026-03-29)
- [ ] `run_analysis.py add-source 11 https://example.com/article` creates same layout with `raw.html` — URL mode not tested
- [~] Companion dir includes provenance artifacts — `output.md`, `metrics.json`, `cost.json`, `decisions.json`, `images/` present; `raw.pdf` NOT created (extraction pipeline does not copy source by default)
- [x] `run_analysis.py update-analysis 17a --sources <name>` updates `analysis.md` via analysis agent — verified: 3 findings applied, 39 whitepaper-specific term mentions
- [x] Downstream artifacts marked stale after update — verified: `model_setup.py` flagged stale

**Deliverables**:
- Updated `run_analysis.py` with `cmd_add_source` and `cmd_update_analysis`

---

### Item 4: Shared Memory System [1.5 days] — COMPLETE

**Type**: Implementation
**Effort**: 1.5 days (spec 2h, design 3h, plan 1h, execute 6h)
**Status**: Complete (2026-03-29)
**Dependencies**: None (but should be ready before Item 5)
**Work Item**: `.project/active/shared-memory-system/` (spec, design, plan)

**Objective**: Build a cross-concept memory system that accumulates learnings (common pitfalls, good data sources, parameter sanity ranges, recurring feedback patterns) and makes them available to all pipeline agents via a memory-handler subagent.

**Scope**:
1. Memory storage: `exploration/concept_analysis/memory/` directory
   - Initial categories TBD — start with broad files, split as patterns emerge
   - Each entry timestamped and tagged with originating concept(s)
   - Simple markdown with structured entries (grep-friendly, no database)
2. Memory-handler subagent prompt (`prompt_templates/agents/memory_handler.md`):
   - **Read mode**: Given current task context (concept, stage, topic), return relevant memories
   - **Write mode**: Given a learning/insight, categorize and append to appropriate memory file
   - Designed to be invoked as a subagent by other agents (analyze, assess, review, manage-concept)
3. Integration pattern: every main agent invokes memory-handler at start of run to check for relevant context
4. Abstraction layer: since we don't know what memories will be most useful, the handler should be flexible about categories — discover the right structure through use

**Out of Scope**:
- Semantic search / embeddings (keyword matching and concept tags for now)
- Automated memory extraction (memories saved explicitly via interactive agent or after review)
- Memory pruning / expiration (manual curation)

**Success Criteria**:
- [x] Memory files exist and can be read/written by agents
- [x] Memory-handler subagent returns relevant context when given a concept + task description
- [x] At least one pipeline stage (analyze or review) consults memory before running
- [ ] `/manage-concept` can save learnings to shared memory *(deferred — Item 5)*
- [ ] Memory is useful — after 3-5 concept analyses, accumulated learnings improve subsequent ones *(deferred — requires organic accumulation)*

**Deliverables**:
- `exploration/concept_analysis/memory/` directory with initial structure and 3 sample entries
- `.claude/agents/memory-handler.md` (interactive read/write agent)
- `load_relevant_memories()` in `run_analysis.py` (pipeline integration)
- `{{#if memory_context}}` conditional section in `analysis_v2.md`
- 11 unit tests in `test_memory.py`

---

### Item 5: Interactive Manage-Concept Agent [2 days] — COMPLETE

**Type**: Implementation
**Effort**: 2 days (spec 2h, design 3h, plan 1h, execute 10h)
**Status**: Complete (2026-03-29)
**Dependencies**: Item 1 (feedback format, modal analysis prompt), Item 4 (shared memory)
**Work Item**: `.project/active/manage-concept-agent/` (spec, design, plan)

**Objective**: Create a `/manage-concept` Claude Code custom command that opens an interactive session for vetting, questioning, and improving a specific concept's analysis. Includes designing the handoff pattern for how human-driven changes flow back through the analysis agent.

**Scope**:
1. `.claude/commands/manage-concept.md` — custom command prompt template
2. Stage-aware behavior:
   - **Early stages** (drafted, model-setup): Key bets analysis, critical assumptions, asterisks/flags
   - **Review stage**: Help fill Decision fields, explain PA items, triage proposed actions
   - **General**: Answer questions about analysis/sources, trace claims to sources, cross-concept comparison
3. **Change handoff design**: How the interactive agent captures requested changes and feeds them back to the analysis agent:
   - Agent writes structured feedback (same format as assessment agent's `feedback.md`)
   - User then runs `analyze` in feedback-pass mode to apply (or reviews feedback first)
   - Design must account for the fact that interactive sessions are unreliable for direct artifact edits
   - Output: `change_requests.md` with structured feedback entries + a `change_log.md` documenting the session's findings and decisions
4. Memory integration: agent reads shared memory at start (via memory-handler), can save learnings during session
5. Key bets framework:
   - "This concept bets that [X] is achievable" — impact if true/false, current evidence
   - "The analysis assumes [Y]" — unique vs. shared, basis, sensitivity
   - "Flag: [Z]" — noteworthy items, whether addressed

**Out of Scope**:
- Triggering pipeline stages from within the interactive session
- Multi-concept comparison mode (single-concept focus)

**Success Criteria**:
- [x] `claude /manage-concept 11` opens interactive session with full concept context
- [x] Agent correctly identifies pipeline state and adapts behavior
- [x] Key bets / assumptions / asterisks analysis is substantive and grounded in sources
- [x] Changes produce structured feedback that can be fed into the analysis agent — `--feedback` flag added to `cmd_analyze`
- [x] Change log captures session findings for audit trail — change_log.md protocol in command prompt
- [x] Agent can save learnings to shared memory via memory-handler

**Deliverables**:
- `.claude/commands/manage-concept.md`
- Documentation of the key-bets framework and change handoff pattern
- Example session transcript showing the workflow

---

## Dependencies

**External**:
- ~~`agentic-mbse[web]` — web source capture feature~~ — RESOLVED, merged. No longer blocks Item 3.
- Source replacement conventions (`.project/active/source-replacement/`) — companion-dir + symlink layout. Not a blocking dep (conventions are established), but Item 3 must follow them.

**Internal**:
- Items 1, 2, and 4 can proceed in parallel (no dependencies between them)
- Item 3 depends on Item 1 (feedback format, modal prompt, staleness propagation)
- Item 5 depends on Items 1 and 4 (feedback format + shared memory)

**Item Dependency Graph**:
```
Item 1 (iterative analysis loop + config + feedback format)
  ├─> Item 3 (source addition — uses modal prompt + staleness)
  └─> Item 5 (manage-concept — uses feedback format)

Item 2 (build-visuals — independent)

Item 4 (shared memory)
  └─> Item 5 (manage-concept — reads/writes memory)
```

**Parallel tracks**:
- Track A: Item 1 (the big foundational piece)
- Track B: Item 2 (independent)
- Track C: Item 4 (independent)
- Then: Item 3 (after Item 1), Item 5 (after Items 1 + 4)

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Analysis loop doesn't converge (assessment keeps finding issues) | Medium | Max iterations cap (default 3); human review is the final gate anyway |
| Context budget exceeded on cold-start analysis pass | High | Subagents for source reading; measure actual context usage on 2-3 concepts before scaling |
| Assessment agent too soft (rubber-stamps everything) | Medium | Concrete checklist tied to analysis goals; test on known-weak analyses |
| Assessment agent too harsh (finds phantom issues, loop churns) | Medium | Max 3 issues per pass; convergence review after first batch of concepts |
| HTML sensitivity explorer JS diverges from Python model | High | Validate baseline LCOE match as acceptance gate; start with simple models |
| Interactive change handoff unreliable | Medium | Design in Item 5; structured feedback format → analysis agent, not direct edits |
| Shared memory grows noisy | Low | Manual curation; start minimal; grow from actual review sessions |
| agentic-mbse[web] not ready when Item 3 needs it | Low | PDF mode works without it; URL mode can wait |

---

## Timeline

**Total Effort**: ~9.5 days (~2 weeks calendar with review/iteration)

| Item | Effort | Dependencies | Track |
|------|--------|--------------|-------|
| Item 1: Iterative Analysis Loop | 3 days | None | A |
| Item 2: Build-Visuals Stage | 1.5 days | None | B |
| Item 3: Source Addition | 1.5 days | Item 1 | A (cont.) |
| Item 4: Shared Memory | 1.5 days | None | C |
| Item 5: Manage-Concept Agent | 2 days | Items 1, 4 | Convergence |

**Suggested execution order**:

Week 1: Items 1, 2, 4 (all independent — Item 1 is the critical path)
Week 2: Items 3, 5 (depend on week 1)

---

## Lessons Learned (Post-Completion)

### Item 1: Convergence Tuning Needed

Assessment agent found real, progressively deeper issues each pass — only 1 of 3 test concepts converged within `--max-passes 3`. The non-convergent findings are genuinely useful (not phantom issues), suggesting the assessment is appropriately rigorous but the default iteration budget is tight. Consider:
- Increasing `--max-passes` default to 4-5
- Lightening assessment criteria (fewer findings per pass, or a "good enough" threshold)
- Gathering more data across concepts before tuning — current sample is 3 concepts

This is a tuning question, not a code bug. The pipeline works correctly at any `--max-passes` value.

### Item 3: Checkpoint Test Results (concept 17a, Xcimer Whitepaper)

**Verified by**: `.project/active/checkpoint-test-concept17/` (spec, plan — both Complete)
**Date**: 2026-03-29

**End-to-end pipeline validated**: gap-check → analyze (3-pass, PASS) → model-setup (LCOE $101.6/MWh) → review → add-source (28-page PDF, 89KB extraction) → update-analysis (3 findings applied) → spot checks (6/8 PASS).

**Quality observations to watch for**:

1. **Feedback-pass partial implementation**: The pre-pass generated 3 high-quality findings (F-1: laser cost component breakdown, F-2: development roadmap milestones, F-3: TRUMPF supply chain). The feedback-pass successfully applied F-1 and F-3 but only partially implemented F-2 — Phoenix/Argos/Athena milestones appear in the analysis but Anvil and Vulcan were dropped. This suggests the feedback-pass agent may lose detail on multi-item recommendations. Watch for this pattern on future `update-analysis` runs.

2. **No `raw.pdf` provenance copy**: The `add-source` pipeline does not create a `raw.pdf` copy in the companion directory despite the design calling for `--save-source`. The extraction produces `output.md`, `metrics.json`, `cost.json`, `decisions.json`, and `images/` but no source copy. Low severity — source PDF path is known externally — but the `--save-source` flag may not be wired through correctly.

3. **`update-analysis` targets `analysis.md`, not `output.md`**: The spec and plan assumed `output.md` (differentiation table in `iter-02/`) would be modified, but the pipeline correctly modifies `analysis.md` (detailed analysis in `analyses/`). This is correct behavior — the spec language was inaccurate. Future specs referencing update-analysis should say `analysis.md`.

4. **Spot check SC-8 (tritium specifics) failed**: The specific values (TBR ~1.05, inventory <200g) come from the HYLIFE-III paper which is behind a ScienceDirect paywall and not extracted. The analysis discusses TBR and tritium conceptually but lacks these quantitative anchors. This is a data availability gap, not a pipeline issue.

**Remaining untested Item 3 features**:
- URL-based source addition (only PDF tested)
- `--force` re-extraction
- Error case: `update-analysis` on concept with no existing analysis
- Staleness indicator (`*`) in `status` output after update

---

**Last Updated**: 2026-03-29
**Next Action**: Item 2 (build-visuals, in progress) — only remaining incomplete item
