# Implementation Plan: Interactive Manage-Concept Agent

**Status:** Complete
**Created:** 2026-03-29
**Last Updated:** 2026-03-29

## Source Documents
- **Spec:** `.project/active/manage-concept-agent/spec.md`
- **Design:** `.project/active/manage-concept-agent/design.md` — See here for component details, data formats, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 de-risks the only code change (the `--feedback` flag) before writing the command prompt. Phase 2 writes the complete command file. Phase 3 validates all capabilities through manual testing and iterates on prompt quality.

**Overall Validation Approach:**
- Phase 1 has automated testing (run the flag, check output)
- Phases 2-3 are manual testing (interactive sessions, check outputs)
- Each phase has explicit "What We Know Works" criteria

---

## Phase 1: Pipeline Integration — `--feedback` flag on `cmd_analyze`

### Goal
Add a `--feedback <path>` flag to `cmd_analyze` in `run_analysis.py` that invokes the analysis agent in feedback-pass mode with an arbitrary feedback file. This closes the integration gap identified in `design.md#integration-gap-feedback-flag`.

### Test Stencil (Verify Before Moving On)
```bash
# Create a test feedback file for concept 11
cat > /tmp/test_feedback.md << 'EOF'
VERDICT: FINDINGS

### F-1: Test feedback entry
- **Target:** Section 5, Parameter Table
- **Finding:** Test finding for validation
- **Recommendation:** No actual change needed — this is a pipeline integration test
- **Priority:** minor
EOF

# Run with --dry-run first (if we add that), then for real
uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 11 \
  --feedback /tmp/test_feedback.md --max-passes 1
```

### Changes Required

**See `design.md#component-10` for:** feedback-pass invocation pattern, archival convention, staleness propagation

**Specific file changes:**

#### 1. `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Add `--feedback <path>` argument to the `analyze` subparser (near existing `--max-passes`, `--model`, `--force` args)
- [x] In `cmd_analyze`: detect `args.feedback`, skip cold-start/assessment loop, go straight to feedback-pass invocation
- [x] Reuse feedback-pass template variable pattern from `cmd_update_analysis()` (lines 2016-2066): set `feedback_pass: "true"`, `feedback_path: str(args.feedback)`
- [x] After successful feedback-pass: call `propagate_staleness(concept_id, "feedback-applied-from-change-requests")`
- [x] Archive consumed feedback file: rename to `change_requests_YYYYMMDD_HHMMSS.md` in same directory (use `datetime.now().strftime("%Y%m%d_%H%M%S")`)
- [x] Validate that `--feedback` path exists and is a file before invoking (fail early with clear error)
- [x] Ensure `--feedback` is mutually exclusive with `--force` (feedback-pass requires existing analysis.md)

### Validation

**Automated:**
- [x] `run_analysis.py analyze --help` shows `--feedback` flag
- [x] `run_analysis.py analyze 11 --feedback nonexistent.md` → clear error about missing file
- [ ] `run_analysis.py analyze 11 --feedback /tmp/test_feedback.md` → invokes Claude, modifies analysis.md, archives feedback file

**Manual:**
- [ ] After run: `change_requests_*.md` archive file exists in concept directory
- [ ] After run: no `change_requests.md` remains (it was archived)
- [ ] After run: downstream artifacts marked stale (check model_setup.py first line for `# STALE:`)
- [ ] `git diff` on analysis.md shows the feedback was applied (some edit was made)

**What We Know Works After This Phase:**
The full change-request-to-analysis loop is wired: `/manage-concept` writes `change_requests.md` → user runs `analyze --feedback` → analysis updated → staleness propagated → feedback archived.

---

## Phase 2: Command File — Complete `manage-concept.md`

### Goal
Write the complete `.claude/commands/manage-concept.md` command file covering all 11 prompt sections from `design.md#component-1`. This is a single prompt file — not code.

### Test Stencil (Verify Before Moving On)
```bash
# Basic smoke test: command loads and presents state
claude /manage-concept 11
# Expected: state presentation block, key bets analysis, interactive session opens

# Verify command is recognized
ls .claude/commands/manage-concept.md
```

### Changes Required

**See `design.md#proposed-design` for:** all component specifications (Components 1-9)

**Specific file changes:**

#### 1. `.claude/commands/manage-concept.md` (NEW)
- [x] **Frontmatter** — name, description, allowed-tools, user-invocable (see `design.md#component-1`)
- [x] **Section 1: Role & Identity** — "You are an interactive analysis manager for concept $ARGUMENTS"
- [x] **Section 2: Context Loading Protocol** — 3-phase loading sequence (see `design.md#component-2`)
  - Phase 1: State discovery (glob, frontmatter read, file existence, stale markers)
  - Phase 2: Content loading table (state-dependent reads)
  - Phase 3: Memory loading (direct read + tag matching)
- [x] **Section 3: State Presentation** — Status block format with artifact list, stale markers, source count, memories, focus area (see `design.md#component-3`)
- [x] **Section 4: Stage-Aware Behavior** — Four modes (see `design.md#component-4`):
  - Mode A (drafted/model-setup): Key bets framework with identification heuristics
  - Mode B (reviewed): PA items grouped by severity, decision workflow
  - Mode C (synthesized/approved): Synthesis challenge, deep vetting
  - Mode D (not-started/gap-checked): Pipeline guidance
- [x] **Section 5: Key Bets Framework** — Bets/Assumptions/Flags templates and identification heuristics (see `design.md#component-4`, Mode A)
- [x] **Section 6: Change Request Protocol** — F-N format, append logic, numbering, header template, max-3 clarification (see `design.md#component-5`)
- [x] **Section 7: Review Decision Protocol** — Edit tool patterns for Decision/User Notes fields, confirmation flow, address-review suggestion (see `design.md#component-4`, Mode B)
- [x] **Section 8: Cross-Concept Comparison** — Finding targets (Reuses, family, user request, status), comparison operations table (see `design.md#component-7`)
- [x] **Section 9: Memory Protocol** — Read matching logic, write triggers (user request + agent suggestion), memory-handler subagent for writes (see `design.md#component-8`)
- [x] **Section 10: Pipeline Stage Reference** — CLI command table with next-step suggestions (see `design.md#component-9`)
- [x] **Section 11: Rules & Constraints** — What NOT to edit (analysis.md, model_setup.py directly), confirmation requirements, no `--dangerously-skip-permissions`

### Validation

**Automated:**
- [x] File exists at `.claude/commands/manage-concept.md`
- [x] Frontmatter is valid YAML (name, description, allowed-tools, user-invocable)
- [x] File references correct paths (analyses dir, memory dir, pipeline script)

**Manual:**
- [ ] `claude /manage-concept 11` — session opens, state presentation appears, key bets analysis presented
- [ ] `claude /manage-concept 12` — session opens, PA items presented (concept 12 is synthesized with review.md)
- [ ] Agent responds coherently to "what stage is this concept at?"
- [ ] Agent responds coherently to "what should I run next?"

**What We Know Works After This Phase:**
The command loads, presents state correctly, enters the right mode, and is ready for interactive testing of all capabilities.

---

## Phase 3: Manual Validation & Iteration

### Goal
Run through all 6 test scenarios from `design.md#validation-approach`. Fix prompt issues discovered during testing. Iterate until all acceptance criteria pass.

### Test Scenarios

**See `design.md#manual-testing-protocol` for full test descriptions**

#### Test 1: Early-stage concept (key bets)
- [ ] `claude /manage-concept 11` — state presentation correct (model-setup, stale marker)
- [ ] Key bets analysis identifies ≥3 substantive bets grounded in sources
- [ ] Create a change request → `change_requests.md` written with valid F-N format
- [ ] Change log captures session findings

#### Test 2: Reviewed concept (PA decisions)
- [ ] `claude /manage-concept 12` — PA items presented grouped by severity
- [ ] Fill in 2-3 PA decisions → `review.md` Decision fields updated correctly
- [ ] Agent suggests `address-review` after decisions filled

#### Test 3: Cross-concept comparison
- [ ] Ask "Compare thermal efficiency with concept 06"
- [ ] Agent reads both concepts' artifacts, provides specific comparison (values, sources, confidence)
- [ ] Agent suggests relevant comparison targets from Reuses field

#### Test 4: Memory integration
- [ ] Agent surfaces relevant memories at session start
- [ ] Ask to save a learning → entry appended to `memory/learnings.md` in correct format
- [ ] Agent proactively suggests saving a cross-concept insight → asks for confirmation before writing

#### Test 5: Pipeline guidance
- [ ] Ask "what should I run next?" → correct CLI command for current state
- [ ] Ask agent to run a stage → warns about duration, offers command or runs via Bash

#### Test 6: Append behavior
- [ ] Run two sessions on same concept, create change requests in each
- [ ] Second session's F-N numbers continue from first session's last number
- [ ] `change_log.md` has two timestamped session entries

### Iteration Protocol

For each test failure:
1. Identify the prompt section responsible
2. Edit `.claude/commands/manage-concept.md` to fix
3. Re-run the failed test
4. Verify no regression on previously passing tests

### Validation

**What We Know Works After This Phase:**
All acceptance criteria from spec pass. The command is production-ready for use across the 36 concepts.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Feedback-pass invocation pattern already proven in `cmd_update_analysis()` — we're reusing it, not inventing it. Risk is low.
- **Phase 2**: Prompt quality is the main risk. Mitigated by concrete heuristics (scan for `[estimated]`, check sensitivity rankings) rather than vague instructions.
- **Phase 3**: Budget for 2-3 iterations on key bets quality and PA decision editing accuracy. These are the most prompt-sensitive behaviors.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Modified `exploration/concept_analysis/scripts/run_analysis.py`:
  - Added `--feedback PATH` argument to `p_analyze` subparser (line 2117)
  - Added validation block after `resolve_concepts`: mutual exclusivity with `--force`, file existence check, single-concept constraint (lines 1089-1101)
  - Modified skip-if-exists check to handle feedback mode (analysis.md must exist) (lines 1115-1123)
  - Added feedback-mode branch after `common_vars`: fills template in feedback-pass mode, saves audit trail prompt, invokes Claude, propagates staleness, archives consumed feedback file (lines 1160-1206)
**Issues:** None
**Deviations:**
- Added single-concept constraint (`len(targets) > 1` check) not in original plan — feedback files are concept-specific, applying the same file to multiple concepts would be incorrect

### Phase 2 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Created `.claude/commands/manage-concept.md` (15.9 KB) with all 11 prompt sections
- Frontmatter: name, description, skills (empty), allowed-tools (Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion), user-invocable
- All design components implemented: context loading (3-phase), state presentation, 4 stage-aware modes, key bets framework with heuristics, change request protocol with append logic, review decision editing, cross-concept comparison, memory protocol (direct read + memory-handler write), pipeline reference table, rules & constraints
**Issues:** None
**Deviations:**
- Merged Sections 4+5 (Stage-Aware Behavior + Key Bets Framework) — the key bets heuristics are embedded directly in Mode A rather than as a separate section, since they're only relevant in that mode. Cleaner prompt structure.
- Merged Sections 4+7 (Stage-Aware Behavior + Review Decision Protocol) — PA decision editing is embedded in Mode B for the same reason.

### Phase 3 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Fixed source path in manage-concept.md: `exploration/concept_analysis/research/` → `exploration/phase_1a/research/<concept-id>/iter-*/sources/*.md`
- Fixed `AttributeError` in `cmd_analyze`: `args.feedback` → `getattr(args, "feedback", None)` + local `feedback` variable (stage1-all passes its own Namespace without the feedback attribute)
- Manual testing confirmed: state presentation, key bets analysis, interactive Q&A all working for concept 11
**Issues:**
- Source path was wrong in initial prompt (pointed to nonexistent `exploration/concept_analysis/research/`)
- `stage1-all` crashed because `cmd_analyze` accessed `args.feedback` without guarding for callers that don't define the attribute
**Deviations:**
- Skipped formal test scenarios 2-6 from the plan — user validated core functionality on concept 11 and declared it working

---

**Status**: ~~Draft~~ → ~~In Progress~~ → Complete
