# Spec: Iterative Analysis Loop

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-28 12:25 PDT
**Complexity:** HIGH
**Branch:** design-space-explore
**Epic:** ANALYSIS-V2, Item 1

---

## Business Goals

### Why This Matters

The current analysis pipeline produces each concept's D1+ analysis in a single Claude call. Quality depends entirely on how well the prompt, sources, and exemplars align on the first try. There is no feedback mechanism — if the analysis misses a key hypothesis, mischaracterizes how a concept differs from others, or fails to identify the right modeling approach, the only corrective path is the review stage, which is designed for numerical accuracy, not conceptual framing.

An iterative loop lets the pipeline self-correct on the dimensions that matter most for downstream modeling: Does the analysis capture the *shape* of the concept? Are the right comparisons drawn? Are the key bets and assumptions identified? Are the modeling recommendations actionable? These are the questions that determine whether the cost model built in the next stage will be meaningful or will model the wrong things precisely.

### Success Criteria

- [ ] Analyses arrive at the review stage with the right conceptual framing — review only verifies numbers, not approach
- [ ] The assessment agent finds real issues on pass 1 that pass 2 fixes (demonstrated on ≥3 concepts)
- [ ] The loop converges (pass 2 or 3 comes back clean) for most concepts
- [ ] Goals and checklists are maintainable standalone files, not buried in prompts
- [ ] The feedback format is reusable by the future `/manage-concept` interactive agent

### Priority

P0 — foundational piece of ANALYSIS-V2 epic. Items 3 (source addition) and 5 (manage-concept) depend on the modal prompt, feedback format, and staleness propagation established here.

---

## Problem Statement

### Current State

The analyze stage (`cmd_analyze`, `run_analysis.py:820-921`) works as follows:
1. Loads the analysis prompt template, substitutes concept-specific paths
2. Pre-writes `analysis.md` with YAML frontmatter
3. Makes a single `claude -p` call — the agent reads all sources, dossier, exemplars, and approved pool, then writes the complete 8-section analysis
4. Script assembles frontmatter + body into final `analysis.md`

Problems:
- **No feedback loop.** If the first pass mischaracterizes the concept, there's no corrective mechanism before downstream stages consume the output.
- **Context overload.** The single call loads dossier + all sources (often 6-10 files) + exemplars + approved pool + output template + brief + schema into one context. For data-rich concepts, this pushes context limits.
- **Goals are implicit.** The analysis prompt says "write a D1+ analysis" but doesn't explicitly state what the analysis should *achieve* — the shape/comparison/hypothesis goals are implied by the output template sections, not stated as objectives the agent can be assessed against.
- **No separation between shape and accuracy.** The prompt's "Anti-Hallucination Rules" and "Citation Format" sections (accuracy concerns) are interleaved with "Quality Calibration" (shape concerns), muddling the agent's priorities.
- **Embedded configuration.** Goals, checklists, and quality standards are inline in prompt templates — modifying them requires editing long prompt files and risking unintended changes.

### Desired Outcome

An iterative analyze → assess → feedback loop where:
- The analysis agent focuses on getting the *shape* right (comparison, differences, hypotheses, modeling approach, risks)
- A separate assessment agent evaluates the analysis against explicit goals and provides focused feedback (≤3 issues per pass)
- The loop converges when the assessment agent finds no issues, or after a configurable max number of passes
- Each call is a fresh `claude -p` thread (no context accumulation across passes)
- The analysis agent uses per-source subagents for context-efficient source reading
- Goals, checklists, and standards live in standalone config files

---

## Scope

### In Scope

- Extract prompt configuration into standalone config files
- New modal analysis prompt (cold start / feedback pass / self-advance)
- New assessment prompt with structured feedback output
- Loop orchestration in `cmd_analyze` with `--max-passes` flag
- Per-source subagent pattern for context-efficient source reading
- Structured feedback format (shared with future `/manage-concept` agent)
- Staleness propagation when `analysis.md` changes after initial creation
- Full replacement of current `analysis.md` prompt (no fallback to old prompt)

### Out of Scope

- Changes to the review stage (stays focused on numerical accuracy/traceability)
- The `/manage-concept` interactive agent (epic Item 5)
- Source addition / update-analysis commands (epic Item 3)
- Shared memory system (epic Item 4)
- Build-visuals stage (epic Item 2)
- Changes to the output template structure (8 sections stay as-is)
- Multi-model strategy (analyze and assess use same `--model`)
- Changes to `stage1-all` ordering (quality-check is NOT a separate stage — it's the assessment within the loop)

### Edge Cases & Considerations

- **Context budget**: Cold-start pass loads the most context (sources + exemplars + approved pool). The per-source subagent pattern is the primary mitigation. The assessment agent reads only `analysis.md` + goals + checklist — much lighter.
- **Convergence failure**: If the assessment agent keeps finding issues past max-passes, the pipeline proceeds anyway. The human review stage is the final gate.
- **Assessment agent too soft**: If it rubber-stamps everything, the loop degenerates to single-pass. Mitigate with concrete, checkable assessment criteria tied to explicit goals.
- **Assessment agent too harsh**: If it finds phantom issues, the loop churns. Mitigate with ≤3 issues cap and convergence review after first batch of concepts.
- **Backward compatibility**: `--max-passes 1` skips the assessment entirely — analyze runs once, no feedback loop. This is the migration path for users who want the old behavior.
- **Reuse pool interaction**: The current analyze stage re-scans the approved pool before each *concept*. Within the loop (multiple passes for the same concept), the approved pool is stable — no need to re-scan between passes.
- **Existing analyses**: Running `analyze --force` on a concept that already has `analysis.md` MUST use cold-start mode (full rewrite), not self-advance mode. Self-advance is for when the user explicitly wants to improve without feedback.

---

## Requirements

### Functional Requirements

> Requirements are from user's request unless marked [INFERRED].

**Config Extraction**

1. **FR-1**: Analysis goals MUST be extracted into a standalone file (`prompt_templates/config/analysis_goals.md`) containing the 5 shape-focused goals:
   - How does the concept relate/compare to other concepts?
   - What are the key differences from the mainstream approach?
   - How do those differences affect TEA?
   - What is the right way to model those differences, and capture the key hypotheses?
   - Are the key risks and assumptions called out, and how do we capture them in the TEA?

2. **FR-2**: Assessment criteria MUST be extracted into a standalone file (`prompt_templates/config/assessment_checklist.md`) that the assessment agent evaluates against. Criteria MUST be concrete and checkable, not vague.

3. **FR-3**: Quality standards (citation format, anti-hallucination rules, depth expectations) MUST be extracted into a standalone file (`prompt_templates/config/quality_standards.md`).

4. **FR-4**: The review stage's checklist (numerical accuracy, traceability) SHOULD be extracted into `prompt_templates/config/review_checklist.md` for consistency, even though the review prompt itself is not changing in this item.

5. **FR-5**: `fill_template()` MUST support a mechanism for loading config file contents into template variables (e.g., a `{{@config/analysis_goals.md}}` syntax or a pre-processing step that injects config content).

**Modal Analysis Prompt**

6. **FR-6**: The analysis prompt MUST be replaced with a single modal prompt (`prompt_templates/analysis_v2.md`) that handles three modes:
   - **Cold start**: No `analysis.md` exists → write first draft from sources
   - **Feedback pass**: `analysis.md` exists AND `feedback.md` is provided → act on the specific feedback
   - **Self-advance**: `analysis.md` exists, no feedback → assess current state and try to advance

7. **FR-7**: The modal prompt MUST load the analysis goals from the config file (FR-1) and present them as explicit objectives the agent is working toward.

8. **FR-8**: In feedback-pass mode, the prompt MUST instruct the agent to read the existing `analysis.md`, read the feedback, and make targeted improvements using the Edit tool — NOT rewrite the entire analysis.

9. **FR-9**: In cold-start mode, the prompt MUST instruct the agent to write the analysis body to a separate file (`analysis_body.md`) which the pipeline assembles with frontmatter, matching the current assembly pattern.

10. **FR-10**: The output template structure (8 sections) MUST NOT change. The analysis goals influence what the agent emphasizes *within* those sections, not the section structure itself.

**Per-Source Subagent Pattern**

11. **FR-11**: The analysis prompt MUST instruct the agent to spawn one subagent per source document (Phase 1a extracted sources, dossier, exemplars, approved pool entries).

12. **FR-12**: Each subagent call MUST include one or more specific questions. On cold start, questions SHOULD be guided summaries (e.g., "What does this source tell us about [concept]'s cost structure, unique subsystems, and LCOE-relevant parameters?"). On feedback pass, questions SHOULD target the specific feedback (e.g., "Does this source contain evidence about [specific issue from feedback]?").

13. **FR-13**: Each subagent MUST return its response along with relevant section references (line offsets or section headings) from the source document.

14. **FR-14**: The main agent MUST read the cited sections from the source documents to confirm the subagent's characterization before incorporating claims into the analysis.

15. **FR-15**: [INFERRED] The subagent prompt template SHOULD be a standalone file (`prompt_templates/agents/source_reader.md`) so it can be tuned independently of the main analysis prompt.

**Assessment Prompt**

16. **FR-16**: The assessment prompt (`prompt_templates/assessment.md`) MUST read `analysis.md`, the analysis goals config, and the assessment checklist config.

17. **FR-17**: The assessment agent MUST NOT read raw source documents. Its job is to evaluate the analysis against the goals, not to re-derive the analysis.

18. **FR-18**: The assessment agent MUST produce structured feedback with at most 3 findings per pass. Each finding MUST include:
    - **Target**: Which section or aspect of the analysis
    - **Finding**: What is insufficient, missing, or incorrect (in terms of shape/framing, not numerical accuracy)
    - **Recommendation**: What the analysis agent should do differently
    - **Priority**: blocking / important / minor

19. **FR-19**: The assessment agent MUST produce a clear convergence signal: either `PASS` (no findings) or a findings list. The format MUST be parseable by the pipeline script to determine whether to loop or stop.

20. **FR-20**: The assessment agent MUST NOT evaluate numerical accuracy, citation correctness, or calculation verification. Those are the review stage's responsibility.

21. **FR-21**: [INFERRED] The feedback format (FR-18) MUST be documented in a standalone config file (`prompt_templates/config/feedback_format.md`) so that both the assessment agent and the future `/manage-concept` agent reference the same specification.

**Loop Orchestration**

22. **FR-22**: `cmd_analyze` MUST support a `--max-passes N` flag (default 3). Each pass consists of one analyze call followed by one assess call.

23. **FR-23**: When `--max-passes 1`, the assessment step MUST be skipped entirely — the analyze agent runs once with no feedback loop. This is the backward-compatible path.

24. **FR-24**: Each analyze call and each assess call MUST be a fresh `claude -p` thread (separate `invoke_claude()` calls with independent prompts). No context carries over between calls except through files on disk.

25. **FR-25**: Each iteration's feedback MUST be saved as `feedback_iter_N.md` in the concept's output directory (audit trail).

26. **FR-26**: The loop MUST stop when: (a) the assessment returns `PASS`, or (b) `--max-passes` is reached. When stopping due to max passes with outstanding findings, the pipeline MUST print a warning indicating the analysis has unresolved feedback.

27. **FR-27**: The pipeline MUST print per-pass status (pass number, duration, convergence result) so the user can monitor progress.

28. **FR-28**: [INFERRED] The analysis prompt path MUST be saved before each invocation (matching the existing `analysis_prompt.md` audit trail pattern). For multi-pass, save as `analysis_prompt_iter_N.md` and `assessment_prompt_iter_N.md`.

**Staleness Propagation**

29. **FR-29**: When `analysis.md` is modified after its initial creation (by a feedback pass, `update-analysis`, or future `/manage-concept` changes), the pipeline MUST mark downstream artifacts as stale:
    - `model_setup.py` → add `Stale-Upstream: analysis` to a sidecar or print a warning
    - `review.md` → rename to `review.md.stale` or add frontmatter flag
    - `synthesis.md` → rename to `synthesis.md.stale` or add frontmatter flag

30. **FR-30**: `get_concept_state()` MUST report stale downstream artifacts. The `status` command MUST show a stale indicator (e.g., `M*` for model-setup-stale, `R*` for review-stale).

31. **FR-31**: [INFERRED] Staleness SHOULD be tracked via frontmatter fields (e.g., `Stale: true`, `Stale-Reason: analysis-updated`) rather than file renames, to preserve the file for reference and keep git history clean.

### Non-Functional Requirements

32. **NFR-1**: Each analysis agent thread SHOULD stay under 50% of the model's context window. The per-source subagent pattern (FR-11–14) is the primary mechanism for achieving this.

33. **NFR-2**: The assessment agent thread SHOULD be lightweight — reading only `analysis.md` (~15-30K chars) plus config files (~2-5K chars). This SHOULD stay well under 25% of context.

34. **NFR-3**: The pipeline MUST remain idempotent: re-running `analyze` without `--force` skips concepts that already have `analysis.md`. With `--force`, it uses cold-start mode (full rewrite).

35. **NFR-4**: All prompt templates (analysis_v2.md, assessment.md, source_reader.md) MUST save before invocation for audit trail, matching the existing pattern.

---

## Acceptance Criteria

### Core Loop

- [ ] `run_analysis.py analyze N` runs the iterative loop (default 3 passes)
- [ ] `run_analysis.py analyze N --max-passes 1` runs single-pass with no assessment (backward compatible)
- [ ] Assessment finds real issues on pass 1 that pass 2 fixes (demonstrated on ≥3 concepts)
- [ ] Loop converges (assessment returns PASS) within 3 passes for ≥2 of 3 test concepts
- [ ] `feedback_iter_N.md` files exist in concept output directory after multi-pass run
- [ ] `analysis_prompt_iter_N.md` and `assessment_prompt_iter_N.md` saved for audit trail

### Config Extraction

- [ ] `prompt_templates/config/analysis_goals.md` exists and contains the 5 shape goals
- [ ] `prompt_templates/config/assessment_checklist.md` exists with concrete, checkable criteria
- [ ] `prompt_templates/config/quality_standards.md` exists with citation/anti-hallucination rules
- [ ] `prompt_templates/config/feedback_format.md` exists with the structured feedback spec
- [ ] `fill_template()` supports loading config files into template variables

### Subagent Pattern

- [ ] Analysis agent spawns one subagent per source document (visible in `--verbose` output or logs)
- [ ] Subagent responses include section references (line offsets or headings)
- [ ] Main agent reads cited sections before incorporating claims (visible in tool call sequence)

### Staleness

- [ ] Modifying `analysis.md` on a concept that has `review.md` marks the review as stale
- [ ] `status` command shows stale indicator for affected downstream artifacts
- [ ] Staleness is tracked via frontmatter, not file renames

### Quality & Integration

- [ ] All existing pipeline stages (gap-check, model-setup, review, address-review, synthesize, approve) continue to work
- [ ] `stage1-all` works with the new analyze loop
- [ ] `--dry-run` generates and saves prompts without calling Claude (for all passes)

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 1)
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md`
- **Current analysis prompt:** `exploration/concept_analysis/prompt_templates/analysis.md`
- **Current output template:** `exploration/concept_analysis/prompt_templates/output_template.md`
- **Pipeline script:** `exploration/concept_analysis/scripts/run_analysis.py`
- **Design:** `.project/active/iterative-analysis-loop/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
