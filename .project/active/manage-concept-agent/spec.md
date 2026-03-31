# Spec: Interactive Manage-Concept Agent

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 17:11 PDT
**Complexity:** MEDIUM
**Branch:** design-space-explore
**Epic:** ANALYSIS-V2 (Item 5)

---

## Business Goals

### Why This Matters

The concept analysis pipeline produces structured analyses across 36 fusion concepts, but there is no interactive interface for a human reviewer to interrogate an analysis, build intuition about its assumptions, or request targeted improvements. Today the options are: re-run the full pipeline (expensive, lossy), manually edit artifacts (unreliable, no audit trail), or read the files cold and hope you catch what matters.

A reviewer needs to be able to sit down with a concept, ask questions, challenge assumptions, compare against other concepts, and drive improvements — all within a structured session that produces traceable outputs.

### Success Criteria

- [ ] A reviewer can open an interactive session for any concept and have a substantive conversation grounded in the concept's sources and analysis
- [ ] The agent adapts its focus to the concept's pipeline state (early-stage → key bets; reviewed → PA decision support; general → Q&A)
- [ ] Changes identified during the session flow back through the existing analysis agent via structured feedback, not direct artifact edits
- [ ] Cross-concept comparison is available on demand using existing pipeline data
- [ ] Learnings discovered during sessions accumulate in shared memory for future analyses

### Priority

Final item in the ANALYSIS-V2 epic. Unblocked by completion of Item 1 (iterative analysis loop + feedback format) and Item 4 (shared memory system). This is the "human frontend" that ties together all the pipeline infrastructure built in Items 1-4.

---

## Problem Statement

### Current State

- No interactive interface for concept vetting — reviewers read files manually
- No structured way to capture reviewer insights, questions, or requested changes
- No mechanism for cross-concept comparison during review
- Review stage PA-N Decision fields require manual file editing
- Learnings from review sessions are lost (no connection to shared memory)
- No "key bets" analysis — the most important question ("what is this concept betting on?") has no structured treatment

### Desired Outcome

A `/manage-concept` Claude Code custom command that opens an interactive session providing:
- Stage-aware guidance (what to focus on given the concept's pipeline state)
- Key bets / assumptions / flags framework for early-stage vetting
- Structured feedback output compatible with the existing `update-analysis` flow
- Direct PA Decision field editing for reviewed concepts
- Cross-concept parameter comparison on demand
- Shared memory read/write integration
- Pipeline stage awareness with ability to trigger or guide re-runs

---

## Scope

### In Scope

1. **Custom command**: `.claude/commands/manage-concept.md` — takes concept ID as `$ARGUMENTS`
2. **Context loading**: Pipeline state, analysis, sources, model, review, memory
3. **Stage-aware behavior**: Different focus areas based on `get_concept_state()` result
4. **Key bets framework**: Structured analysis of technical/economic bets, assumptions, flags
5. **Structured feedback output**: `change_requests.md` using F-N format from `feedback_format.md`
6. **Change log**: `change_log.md` capturing session findings and decisions
7. **Review Decision editing**: Direct update of `**Decision:**` and `**User Notes:**` fields in `review.md`
8. **Cross-concept comparison**: On-demand parameter/assumption comparison against other analyzed concepts
9. **Memory integration**: Read shared memory at session start; save learnings by user request or agent suggestion (with confirmation)
10. **Pipeline stage guidance**: Ability to trigger pipeline stages or instruct the user how to run them

### Out of Scope

- Batch processing of multiple concepts in a single session
- Automated change application (user runs `update-analysis` separately after reviewing `change_requests.md`)
- New pipeline stages or modifications to existing stage logic
- Changes to the F-N feedback format itself

### Edge Cases & Considerations

- Concept with no analysis yet (`not-started` or `gap-checked` state) — agent should guide user to run pipeline stages first, not attempt to vet nonexistent artifacts
- Concept with stale downstream artifacts — agent should surface staleness and suggest re-runs
- Multiple interactive sessions on same concept — `change_requests.md` should be appendable (not overwrite previous session's requests); `change_log.md` should accumulate
- Review.md with no actionable PA items — agent should note this and shift to other vetting modes
- Cross-concept comparison when target concept hasn't been analyzed — agent should handle gracefully

---

## Requirements

### Functional Requirements

#### Context & State (FR-1 through FR-3)

1. **FR-1**: The command MUST load the concept's full context at session start: pipeline state (via `get_concept_state()` logic), analysis.md, sources (via `find_sources()`), model_setup.py, model_output.txt, review.md, synthesis.md — reading whichever artifacts exist.

2. **FR-2**: The command MUST load relevant shared memories at session start, matching on concept short ID and confinement family. The agent MAY read memory files directly (filtering entries by tag) or invoke the memory-handler subagent (`.claude/agents/memory-handler.md`) — either mechanism satisfies this requirement.

3. **FR-3**: The command MUST display the concept's current pipeline state and available artifacts to the user at session start, including any stale indicators.

#### Stage-Aware Behavior (FR-4 through FR-7)

4. **FR-4**: When the concept is in `drafted` or `model-setup` state, the agent SHOULD focus on **key bets analysis**:
   - "This concept bets that [X] is achievable" — impact if true/false, current evidence from sources
   - "The analysis assumes [Y]" — unique vs. shared with other concepts, basis, sensitivity
   - "Flag: [Z]" — noteworthy items, whether addressed in the analysis
   - The agent SHOULD proactively present initial key bets to start the conversation.

5. **FR-5**: When the concept is in `reviewed` state (has review.md with PA items), the agent SHOULD focus on **review decision support**:
   - Present PA items grouped by severity (blocking → important → minor)
   - Explain each PA item's finding and proposed fix in plain language
   - Help the user decide on each item (agree / reject / alternative)
   - Write decided values directly to the `**Decision:**` and `**User Notes:**` fields in `review.md` using the Edit tool

6. **FR-6**: When the concept is in `synthesized` or `approved` state, the agent SHOULD focus on **deep vetting**: challenge synthesis verdicts, probe risk ratings, cross-concept comparison.

7. **FR-7**: When the concept is in `not-started` or `gap-checked` state (no analysis.md), the agent MUST inform the user that analysis hasn't been run yet and SHOULD guide them on which pipeline command to run (e.g., `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept_id>`).

#### Feedback & Change Requests (FR-8 through FR-10)

8. **FR-8**: When the user identifies changes to the analysis during conversation, the agent MUST write structured feedback to `change_requests.md` in the concept's analysis directory, using the F-N format:
   ```
   ### F-N: [Short title]
   - **Target:** [Section number or aspect]
   - **Finding:** [What needs to change]
   - **Recommendation:** [Specific action for the analysis agent]
   - **Priority:** blocking | important | minor
   ```
   The agent MUST NOT directly edit `analysis.md` or `model_setup.py`. Change requests are the handoff mechanism to the analysis agent.

9. **FR-9**: The agent MUST maintain a `change_log.md` in the concept's analysis directory, appending a timestamped session entry that captures: session date, key findings discussed, decisions made, change requests written, learnings saved. This provides an audit trail across sessions.

10. **FR-10**: If `change_requests.md` already exists from a previous session, the agent MUST append new entries (incrementing F-N numbering from the last existing entry), not overwrite.

#### Review Decision Editing (FR-11)

11. **FR-11**: When the user decides on a PA item during conversation, the agent MUST use the Edit tool to update the `**Decision:**` field (and optionally `**User Notes:**`) in `review.md` directly. The agent SHOULD confirm the edit with the user before writing. Valid decision values are: `agree`, `reject`, `alternative: [description]`.

#### Cross-Concept Comparison (FR-12 through FR-13)

12. **FR-12**: The agent MUST be able to compare parameters, assumptions, or cost model structure against other analyzed concepts on demand. This includes:
    - Reading another concept's `analysis.md` (Section 5 parameter table, Section 3 differentiators)
    - Reading another concept's `model_setup.py` and `model_output.txt`
    - Comparing LCOE breakdowns, key parameters, and modeling approaches
    - The agent SHOULD use `find_sources()` path patterns and the analyses directory structure to locate comparison targets.

13. **FR-13**: The agent SHOULD be aware of the concept taxonomy (confinement families, nearest neighbors from the `Reuses` frontmatter field) to suggest relevant comparison targets.

#### Memory Integration (FR-14 through FR-15)

14. **FR-14**: The agent MUST read shared memory at session start (via memory-handler subagent) and surface any relevant cross-concept learnings to the user.

15. **FR-15**: The agent MUST save learnings to shared memory in two ways:
    - **By user request**: User explicitly asks to save an insight
    - **By agent suggestion**: Agent identifies a cross-concept insight during conversation, suggests saving it, and writes only after user confirmation
    - Learnings MUST follow the memory entry format: `## [Title]` / `Date: YYYY-MM-DD | Concepts: TAG[, TAG]*` / body (max 10 lines total)

#### Pipeline Stage Guidance (FR-16)

16. **FR-16**: The agent SHOULD be able to trigger pipeline stages or instruct the user how to run them. For each stage, the agent MUST know the correct CLI invocation:
    - `uv run python exploration/concept_analysis/scripts/run_analysis.py <stage> <concept_id>`
    - Stages: `gap-check`, `analyze`, `model-setup`, `build-visuals`, `review`, `address-review`, `synthesis`, `add-source`, `update-analysis`
    - The agent SHOULD suggest appropriate next stages based on current state and session findings (e.g., after writing change requests, suggest running `update-analysis`).
    - The agent MAY run stages directly via Bash if the user approves, or provide the exact command for the user to run.

### Non-Functional Requirements

1. **NFR-1**: The command prompt MUST be self-contained — all context loading, behavior rules, and output formats are in the command file itself. No external dependencies beyond the files it reads.

2. **NFR-2**: The command SHOULD NOT prescribe conversation flow rigidly. The stage-aware behavior sets the *default focus*, but the user can ask about anything at any time.

3. **NFR-3**: The command MUST NOT use `--dangerously-skip-permissions`. It runs as a normal interactive Claude session where the user approves tool calls.

---

## Acceptance Criteria

### Core Functionality
- [ ] `claude /manage-concept 11` opens an interactive session with concept 11's full context loaded
- [ ] Agent correctly identifies pipeline state and adapts its opening focus
- [ ] Key bets / assumptions / flags analysis is substantive and grounded in sources (for drafted/model-setup concepts)
- [ ] Agent can read and explain PA items from review.md (for reviewed concepts)

### Feedback & Changes
- [ ] Changes identified produce `change_requests.md` with valid F-N entries
- [ ] Multiple sessions append to (not overwrite) `change_requests.md`
- [ ] `change_log.md` captures session findings with timestamps
- [ ] After writing change requests, agent suggests running `update-analysis` with correct CLI syntax

### Review Support
- [ ] Agent can update `**Decision:**` fields in review.md via Edit tool
- [ ] Agent confirms with user before writing each decision

### Cross-Concept Comparison
- [ ] Agent can compare parameters between two concepts when asked
- [ ] Agent suggests relevant comparison targets based on confinement family / Reuses

### Memory
- [ ] Agent reads shared memory at session start and surfaces relevant learnings
- [ ] Agent can save new learnings (by request or suggestion with confirmation)
- [ ] Saved learnings follow the required entry format

### Pipeline Guidance
- [ ] Agent knows correct CLI invocations for all pipeline stages
- [ ] Agent suggests appropriate next stages based on current state
- [ ] Agent can trigger stages (with user approval) or provide exact commands

### Quality & Integration
- [ ] Existing pipeline stages continue to work unchanged
- [ ] The feedback format in `change_requests.md` is parseable by the analysis agent in feedback-pass mode

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 5)
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md` (Q2, Q3)
- **Dependencies:**
  - Item 1 deliverables: `prompt_templates/config/feedback_format.md`, `prompt_templates/analysis_v2.md` (feedback-pass mode)
  - Item 4 deliverables: `.claude/agents/memory-handler.md`, `exploration/concept_analysis/memory/learnings.md`
- **Pipeline script:** `exploration/concept_analysis/scripts/run_analysis.py`
- **Design:** `.project/active/manage-concept-agent/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
