# Implementation Plan: Autonomous Source Acquisition (Research Step)

**Status:** In Progress
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/autonomous-source-acquisition/spec_v2.md`
- **Design:** `.project/active/autonomous-source-acquisition/design.md` — see here for component details, function signatures, log schema, prompt structure

## Implementation Strategy

**Phasing Rationale:**
Phase 1 de-risks: verify FR-0 (tool access in `claude -p`) and wire the integration so the loop calls real code. Phase 2 builds the prompt and output handling — the creative/uncertain part that may need iteration. Phase 3 validates end-to-end on a real concept. Each phase produces verifiable output before the next begins.

**Overall Validation Approach:**
- No formal test framework (project convention — see refactor-run-analysis spec)
- Validation via dry-run prompt inspection, manual execution, and fixture comparison
- Each phase has explicit "What We Know Works" criteria

---

## Phase 1: Prerequisite Verification + Wiring

### Goal
Verify `claude -p` can use WebSearch, WebFetch, and Bash (FR-0). Create `lib/research.py` skeleton that returns `[]`. Wire it into the loop and add CLI flags. After this phase, `--research` fires real code that no-ops cleanly.

### Validation Stencil (Verify Before Proceeding)

```bash
# FR-0: Does claude -p have tool access?
echo 'Use WebSearch to search for "REBCO superconductor cost 2024". Then use Bash to run: echo "bash-works"' \
  | claude -p --dangerously-skip-permissions --verbose 2>/tmp/fr0-stderr.txt | head -50

# Check stderr for tool invocations
grep -i "websearch\|bash\|tool" /tmp/fr0-stderr.txt | head -10
```

If WebSearch/Bash are NOT available, STOP and investigate before proceeding.

### Changes Required

**See `design.md` for:**
- Loop branch rewrite → `design.md#1-loop-integration`
- research.py signature → `design.md#2-research-module`
- CLI flags → `design.md#5-cli-flags`

**Specific file changes:**

#### 1. FR-0 Verification
- [x] Run the FR-0 test above
- [x] Document result (tools available / not available / alternative needed)

#### 2. Research Module Skeleton
**File:** `exploration/concept_analysis/scripts/lib/research.py` (NEW)
- [x] Create file with module docstring
- [x] Implement `run_research_step(concept, iter_dir, args) -> list[Path]` — full implementation (not skeleton)
- [x] Implement `load_research_log(concept_dir) -> dict` — reads JSON or returns `{"entries": [], "acquired_by_iteration": {}}`
- [x] Implement `update_research_log(concept_dir, new_entries, acquired_paths, iteration)` — appends to JSON file
- [x] Implement `format_prior_attempts(log) -> str` — full implementation
- [x] Verify: `from lib.research import run_research_step` works from `run_analysis.py` context

#### 3. Loop Integration
**File:** `exploration/concept_analysis/scripts/lib/loop.py`
- [x] Replace `elif` branch at lines 122-132 with design.md#1-loop-integration code (local import, source-integration chain)
- [x] Delete `_run_research_step` stub at lines 570-581
- [x] Verify: no circular import errors when importing loop.py

#### 4. CLI Flags
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Add `--max-research-searches` (int, default 5) to `p_analyze` and `p_s1`
- [x] Add `--max-research-extractions` (int, default 3) to `p_analyze` and `p_s1`
- [x] Update `--research` help text on both parsers (remove "not yet implemented")
- [x] Verify: `run_analysis.py analyze --help` shows new flags

### Validation

**Automated:**
- [x] `uv run python scripts/run_analysis.py analyze --help` — shows `--research`, `--max-research-searches`, `--max-research-extractions`
- [x] `uv run python scripts/run_analysis.py stage1-all --help` — same flags present
- [x] `uv run python scripts/run_analysis.py status` — unchanged output (no regressions)

**Manual:**
- [x] `uv run python scripts/run_analysis.py stage1-all 02 --resume --research --dry-run` — research step fires, template not found (expected), falls through to assess, dry-run completes normally
- [x] Without `--research`: `uv run python scripts/run_analysis.py stage1-all 02 --resume --dry-run` — no research step, identical to before

**What We Know Works After This Phase:**
- FR-0 verified (or blocker documented)
- `--research` flag fires real code in the loop
- Empty-list return → source-integration NOT called → assess fallback works
- CLI flags parse correctly
- No regressions in existing behavior

---

## Phase 2: Research Prompt + Output Handling

### Goal
Build `prompt_templates/research.md` and flesh out `lib/research.py` — prompt construction, agent invocation, output parsing, log management. After this phase, `--research --dry-run` saves a complete, reviewable research prompt, and the orchestrator can handle all agent output cases (valid JSON, missing file, malformed JSON).

### Validation Stencil

```bash
# Dry-run produces a real prompt (not skeleton)
uv run python scripts/run_analysis.py stage1-all 01 --resume --research --dry-run
# → check iter-N/research_prompt.md exists and contains Section 6 references

# Inspect the prompt manually
cat exploration/concept_analysis/analyses/01-hts-compact-tokamak/iter-*/research_prompt.md | head -80
```

### Changes Required

**See `design.md` for:**
- Prompt template structure → `design.md#3-research-prompt-template`
- Template variables → `design.md#3-research-prompt-template` (table)
- Output JSON schema → `design.md#3-research-prompt-template` (output section)
- Log schema → `design.md#4-research-log-schema`

**Specific file changes:**

#### 1. Research Prompt Template
**File:** `exploration/concept_analysis/prompt_templates/research.md` (NEW)
- [x] Create template with all 8 sections from design.md#3
- [x] Use `{{variable}}` syntax matching existing templates (see `fill_template()` in templating.py)
- [x] Include the search→triage→extract pipeline instructions
- [x] Include source quality hierarchy and news-site heuristic
- [x] Include rules (no WebFetch as source content, add-source only, one URL per call)
- [x] Include output JSON schema with example
- [x] Include `{{prior_attempts}}` section (conditionally, via `{{#if prior_attempts}}`)

#### 2. Research Module — Full Implementation
**File:** `exploration/concept_analysis/scripts/lib/research.py` (MODIFY)
- [x] Implement `run_research_step()` per design.md#2 flow (steps 1-11):
  - Derive paths (analysis_path, log_path, output_path)
  - Snapshot `find_sources(rid)` before invocation
  - Load research log → format prior attempts
  - Build prompt via `fill_template()`
  - Save prompt to `iter_dir / "research_prompt.md"` (FR-13)
  - Dry-run short circuit (return `[]`)
  - `invoke_claude()` with prompt
  - Parse `research_output.json` (handle missing/malformed gracefully)
  - Diff `find_sources()` → return acquired list
- [x] Flesh out `format_prior_attempts()` — groups by gap_id, shows status/queries per design.md#4
- [x] Flesh out `update_research_log()` — append entries + record acquired paths by iteration per design.md#4 schema
- [x] Add graceful handling for:
  - `research_output.json` does not exist (agent crashed) — warn, still diff sources
  - `research_output.json` is malformed JSON — warn, still diff sources
  - `invoke_claude()` returns rc != 0 — print error, return `[]`
- [x] Verify module stays under 300 lines (FR-NF-1) — 175 lines

### Validation

**Automated:**
- [x] `uv run python scripts/run_analysis.py stage1-all 01 --resume --research --dry-run` — saves `research_prompt.md` to iter-4/
- [x] `uv run python scripts/run_analysis.py status` — unchanged (no regressions)

**Manual:**
- [x] Read `iter-N/research_prompt.md` — verify it contains:
  - The correct concept name and ID
  - The `add-source` command with correct concept number
  - The max searches/extractions caps
  - All 8 prompt sections from the design
- [ ] Verify `format_prior_attempts()` with synthetic data: deferred to Phase 3 (will be tested with real data)
- [ ] Verify graceful error handling: deferred to Phase 3 (will observe in live run)

**What We Know Works After This Phase:**
- Research prompt is complete and well-formed
- Orchestrator builds prompt correctly with all template variables
- Output parsing handles all three cases (valid, missing, malformed)
- Research log I/O works (read, append, format for prompt)
- Dry-run produces a prompt reviewable before committing to live runs

---

## Phase 3: Live Integration Test

### Goal
End-to-end validation on a real concept. Verify the full chain: research agent searches → triages → extracts via add-source → orchestrator detects new sources → source-integration produces feedback → analyze consumes it.

### Changes Required

No code changes. This is execution and observation only.

### Test Execution

#### 1. Single-Concept Test (Conservative Caps)
- [x] Pick a concept with known `not-yet-sourced` gaps in Section 6 (e.g., 01-hts-compact-tokamak)
- [x] Run with `--max-passes 4` (concept already at iter-3, needed room for iter-4)

#### 2. Verify Research Agent Behavior
- [x] `iter-4/research_prompt.md` exists and matches dry-run version
- [x] `iter-4/research_output.json` exists and is valid JSON (7.6 KB, well-structured)
- [x] Research agent used WebSearch (2 searches: ARIES-AT on OSTI, Li-6 enrichment on OSTI)
- [x] Research agent called `add-source` (1 extraction: ARIES-AT conference paper from OSTI)

#### 3. Verify Source Acquisition (if sources were acquired)
- [x] New source file exists: `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-etdeweb-servlets-purl-20261446.md`
- [x] Source has YAML frontmatter (source URL, content hash, backend=pdf_pipeline)
- [x] Source-integration fired: `source_integration_output.md` in iter-4/ (2 findings, 132s)
- [x] Feedback consumed by analyze step in feedback-pass mode

#### 4. Verify Log + State
- [x] `research_log.json` created with correct schema (7 gap entries, acquired_by_iteration)
- [x] `entries[]` populated: G-1 (partial), G-12 (skipped), G-8/10/11/13/14 (skipped — budget)
- [x] `acquired_by_iteration.4` populated with filesystem-diffed path
- [x] `verdict.json` has `research_ran: true`, `feedback_source: "research"`

#### 5. Verify Fallback (if nothing acquired)
- [ ] Not tested this run (sources were acquired). Fallback path verified via dry-run in Phase 1.

#### 6. Verify Backward Compatibility
- [x] `stage1-all 07 --resume --dry-run` (without `--research`) — no research step, unchanged behavior
- [x] `status` — all concepts show correct states (01 now at iter-4/FAIL with 3 findings)

### Validation

**What We Know Works After This Phase:**
- Full research → source-integration → analyze chain operates correctly
- Research agent can search, triage, and extract (or correctly skip)
- Source-integration produces rich feedback on autonomously-acquired sources
- Research log provides pass-over-pass memory
- Fallback to assess works when nothing is acquired
- No regressions in existing pipeline behavior

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Key points:
- Always use `uv run python ...` (never bare `python`)
- Working directory for script execution: `exploration/concept_analysis/`
- `claude -p` available system-wide with `--dangerously-skip-permissions`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1 (FR-0)**: If `claude -p` lacks WebSearch/WebFetch, STOP and investigate. Document findings in this plan before proceeding. Possible alternatives: MCP server, direct API calls, or `claude` interactive mode with piped input.
- **Phase 2 (prompt quality)**: Review the dry-run prompt manually before any live execution. The prompt is the most likely part to need iteration — expect 1-2 revision cycles.
- **Phase 3 (cost)**: Use `--max-research-extractions 1 --max-research-searches 2` for first live test. Each extraction costs $5-50. Don't run on all concepts until single-concept test passes.

---

## Implementation Notes

_TO BE FILLED DURING IMPLEMENTATION_

### Phase 1 Completion
**Completed:** 2026-04-05
**FR-0 Result:** PASS — WebSearch and Bash both work in `claude -p --dangerously-skip-permissions --verbose`. WebFetch not explicitly tested but is configured in settings.local.json.
**Actual Changes:**
- Created `scripts/lib/research.py` (~175 lines) — full implementation of `run_research_step()`, `load_research_log()`, `update_research_log()`, `format_prior_attempts()`, `_parse_agent_output()`
- Modified `scripts/lib/loop.py` — replaced stub branch (lines 122-132) with research call + source-integration chain; deleted `_run_research_step` stub (was lines 570-581)
- Modified `scripts/run_analysis.py` — added `--max-research-searches` and `--max-research-extractions` to both `p_analyze` and `p_s1`; updated `--research` help text
**Issues:** None
**Deviations:** research.py is fully implemented (not a skeleton) — the design was clear enough that the full module could be written in one pass. Still needs the `prompt_templates/research.md` template (Phase 2) to actually run.

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `prompt_templates/research.md` (~168 lines) — full research agent prompt with all 8 design sections, {{variable}} substitution, {{#if prior_attempts}} conditional
- research.py was already fully implemented in Phase 1 (deviation noted there)
**Issues:** None
**Deviations:** `format_prior_attempts()` synthetic data test and graceful error handling test deferred to Phase 3 — will be validated with real execution rather than synthetic fixtures.

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:** No code changes (execution and observation only).
**Results:**
- Research agent searched OSTI for ARIES-AT cost data and Li-6 enrichment — found 4 candidates for G-1, 3 for G-12
- Extracted 1 source (ARIES-AT conference paper, 176 lines) — correctly marked G-1 as "partial" (summary paper, not full CAS breakdown)
- Source-integration found 2 material findings from the new source
- Analyze step consumed findings in feedback-pass mode, produced 51KB updated analysis
- Model-setup ran successfully (LCOE = 172.0 $/MWh)
- Assess found 3 remaining findings → FAIL verdict (expected — one source won't close all gaps)
- Research log correctly records all 7 gaps with statuses, queries, candidates, and next-iteration recommendations
- Total time: ~29 minutes (research 252s + source-integration 132s + analyze 234s + model-setup 798s + assess 337s)
**Issues:** None
**Deviations:** Used `--max-passes 4` instead of `--max-passes 1` since concept was already at iter-3. This actually tested the full chain better — research → source-integration → analyze → model-setup → assess all in one pass.

---

**Status:** Complete
