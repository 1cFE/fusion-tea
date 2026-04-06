# Implementation Plan: Re-source NO-Verdict .orig.md Files

**Status:** Complete
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/orig-md-research/spec.md`
- **Design:** `.project/active/orig-md-research/design.md` — see here for component details, batch flow, JSON schemas, reuse inventory

## Implementation Strategy

**Phasing Rationale:**
Phase 1 proves all mechanics (discovery, grouping, iter creation, prompt saving) without spending money. Phase 2 builds the prompt template — the creative/uncertain part — and validates it via dry-run review. Phase 3 runs live on 2 files to validate end-to-end before committing to all 21.

**Overall Validation Approach:**
- No formal test framework (project convention)
- Validation via `--dry-run` inspection, manual execution, and filesystem verification
- Each phase has explicit "What We Know Works" criteria

---

## Phase 1: Orchestrator + Dry-Run

### Goal
Working CLI that discovers `.orig.md` files, groups by concept, creates new `iter-NN+1` directories, builds prompts from template, and saves them. All mechanics verified before any Claude calls.

### Changes Required

**See `design.md` for:**
- Batch grouping logic → `design.md#batch-grouping`
- `process_one()` signature → `design.md#core-function`
- `parse_concept_from_path()` → `design.md#path-parsing`
- `ensure_new_iter()` → `design.md#batch-grouping`
- CLI flags → `design.md#component-1`
- Report directory layout → `design.md#report-directory`

**Specific file changes:**

#### 1. Orchestrator Script
**File:** `exploration/concept_analysis/scripts/resurface_orig.py` (NEW)
- [x] Create script with argparse (`--all`, `FILE...`, `--dry-run`, `--max-extractions`, `--model`, `--timeout`, `--force`)
- [x] Implement `parse_concept_from_path()` — extract concept_id and concept_num from path
- [x] Implement `ensure_new_iter()` — create `iter-NN+1/sources/` idempotently
- [x] Implement `process_one()` — read content, fill template, save prompt, invoke agent (or skip on dry-run), filesystem-diff, parse output, build result dict
- [x] Implement `parse_agent_output()` — read JSON gracefully (handle missing/malformed)
- [x] Implement `main()` — discover files, group by concept, iterate, print summary table, write `summary.json`
- [x] Resumability: skip files that have existing report JSON with `"status": "complete"` (override with `--force`)

### Validation

**Automated:**
```bash
# Discovery finds all 21 files
uv run python scripts/resurface_orig.py --all --dry-run 2>&1 | head -5
# Should print "Found 21 .orig.md files across 15 concepts"

# Check iter creation happened correctly
ls -d knowledge/concept_research/22-projectile-icf/iter-*/
# Should show iter-01, iter-02, iter-03 (new)

# Prompt was saved
ls exploration/concept_analysis/resurface_reports/*.prompt.md | wc -l
# Should be 21
```

**Manual:**
- [x] `--all --dry-run` finds 21 files, groups into 15 concepts
- [x] New iter dirs created: iter-03 for most concepts, iter-04 for concepts 21/29, iter-02 for concepts 24/31
- [x] Concepts with multiple `.orig.md` files (04, 14, 21, 23) get ONE new iter, not multiple
- [x] Prompts saved to `resurface_reports/` with correct concept numbers
- [x] Running `--all --dry-run` a second time does NOT create additional iter dirs (idempotent)
- [x] Explicit file path works: `uv run python scripts/resurface_orig.py knowledge/concept_research/22-projectile-icf/iter-01/sources/first-light-fusion-technology.orig.md --dry-run`

**What We Know Works After This Phase:**
File discovery, path parsing, concept grouping, iter creation, prompt template filling, report directory structure, dry-run flow. Everything except the prompt content and live Claude invocation.

---

## Phase 2: Prompt Template

### Goal
Complete agent prompt that instructs the `claude -p` agent to: extract URLs from the file, try header URLs via `add-source`, search for uncovered claims, and produce a coverage assessment. Validated via dry-run prompt review.

### Changes Required

**See `design.md` for:**
- Prompt strategy (4 phases) → `design.md#component-2`
- Template variables → `design.md#component-2` (table)
- Output JSON schema → `design.md#component-2`
- Sections to copy from `research.md` → `design.md#researchmd-prompt--what-to-reuse-verbatim`

**Specific file changes:**

#### 1. Prompt Template
**File:** `exploration/concept_analysis/prompt_templates/resurface.md` (NEW)
- [x] Create template with `{{variable}}` substitution matching `fill_template()` syntax
- [x] Phase 1 instructions: extract URLs from all header format patterns (see `design.md#origmd-header-format-patterns`)
- [x] Phase 2 instructions: try each URL via `add-source {{concept_num}} "<url>"`, log outcomes
- [x] Phase 3 instructions: WebSearch for uncovered claims, WebFetch triage, `add-source` extract
- [x] Phase 4 instructions: coverage assessment with `delete`/`partial`/`keep` recommendation
- [x] Copy verbatim from `research.md`: Source Quality Hierarchy (lines 76-86), News-Site Heuristic (lines 88-99), Rules (lines 100-110)
- [x] Output JSON schema with example (adapted from `design.md#component-2`)
- [x] Include note about thin replacement `.md` file assessment

### Validation

**Automated:**
```bash
# Re-run dry-run, inspect a prompt for a URL-rich file
uv run python scripts/resurface_orig.py \
  knowledge/concept_research/22-projectile-icf/iter-01/sources/first-light-fusion-technology.orig.md \
  --dry-run

cat exploration/concept_analysis/resurface_reports/first-light-fusion-technology.prompt.md | head -40
```

**Manual:**
- [x] Prompt contains the full `.orig.md` content
- [x] `add-source` command uses correct concept number (e.g., `add-source 22`)
- [x] Max extractions cap is present
- [x] Output path is valid and writable
- [x] Source Quality Hierarchy and News-Site Heuristic are present verbatim
- [x] Rules section includes all 5 rules from design
- [x] Prompt for a no-URL file (`general-fusion-lm26-milestones-2025.orig.md`) still makes sense — Phase 1 finds no URLs, Phase 3 handles everything via search

**What We Know Works After This Phase:**
Complete prompt template produces well-formed, reviewable prompts for all 21 files. Ready for live execution.

---

## Phase 3: Live Test (2 Files)

### Goal
End-to-end validation on two files with different characteristics. No code changes — execution and observation.

### Test Cases

**File A:** `22-projectile-icf/iter-01/sources/first-light-fusion-technology.orig.md`
- 92 lines, 6 header URLs including `newatlas.com`, `neimagazine.com`, `interestingengineering.com`
- Tests: header-URL-first strategy, extractable news sites, multi-URL file
- Expected: 2-4 sources acquired from news sites, company site likely fails

**File B:** `14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-lm26-milestones-2025.orig.md`
- 30 lines, no explicit URLs in header
- Tests: web-search fallback, finding sources from claim text only
- Expected: 1-2 sources from news coverage of General Fusion milestones

### Execution

- [x] Run File A:
  ```bash
  uv run python scripts/resurface_orig.py \
    knowledge/concept_research/22-projectile-icf/iter-01/sources/first-light-fusion-technology.orig.md \
    --max-extractions 3
  ```

- [x] Run File B:
  ```bash
  uv run python scripts/resurface_orig.py \
    knowledge/concept_research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-lm26-milestones-2025.orig.md \
    --max-extractions 3
  ```

### Validation

- [x] **Sources acquired:** At least 1 source per file in the new iter directory (3 each)
- [x] **Source quality:** YAML frontmatter present, companion dir with `output.md` + `raw.*`
- [x] **New iter correct:** File A sources in `22-projectile-icf/iter-03/sources/`, File B in `14-magnetized-target-fusion-pneumatic-compression/iter-03/sources/`
- [x] **Report JSON valid:** `resurface_reports/<name>.json` exists, parseable, has `recommendation` field
- [x] **Coverage assessment reasonable:** Claims from `.orig.md` mapped to extracted sources
- [x] **Resumability:** Re-running the same command skips the file (report already exists)
- [x] **Cost acceptable:** File A: 182s, File B: 93s — well within budget

**What We Know Works After This Phase:**
Full pipeline operates correctly. Prompt quality is validated. Ready for `--all` run on remaining 19 files.

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
- **Phase 1 (idempotency)**: Test `ensure_new_iter()` by running `--dry-run` twice — second run must not create additional iter dirs.
- **Phase 2 (prompt quality)**: Review the dry-run prompt manually before any live execution. The 4-phase agent strategy may need iteration after Phase 3 results.
- **Phase 3 (cost)**: Use `--max-extractions 3` for test runs. Each HTML extraction is free (no Claude call in agentic-mbse for HTML). PDF extractions cost $1-2.

---

## Implementation Notes

_To be filled during execution._

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/resurface_orig.py` (~230 lines)
- Implements all planned functions: `parse_concept_from_path()`, `ensure_new_iter()`, `process_one()`, `parse_agent_output()`, `main()`
- CLI: `--all`, positional files, `--dry-run`, `--max-extractions`, `--model`, `--timeout`, `--force`
- Resumability via existing report JSON check
- Report dir: `exploration/concept_analysis/resurface_reports/`

**Issues:**
- Idempotency bug: first implementation always created new iter dirs on re-run. Fixed by checking if latest iter's `sources/` dir is empty (no `.md` files) and reusing it.
- Argparse mutually exclusive group with positional args didn't work cleanly. Switched to manual validation.
- Explicit file paths resolved relative to CWD (concept_analysis/), not repo root. Added fallback resolution via `REPO_ROOT`.

**Deviations:**
- Template placeholder used for dry-run when `resurface.md` doesn't exist yet (graceful fallback rather than error). Live runs still require the template.

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_analysis/prompt_templates/resurface.md`
- 4-phase agent prompt: extract URLs, try via add-source, search uncovered claims, coverage assessment
- Source Quality Hierarchy and News-Site Heuristic copied from research.md
- Output JSON schema with outcome enum values
- Template variables: `orig_filename`, `orig_content`, `concept_num`, `concept_id`, `max_extractions`, `output_path`

**Issues:** None

**Deviations:**
- Rules section has 6 rules (added "log everything") vs design's 5. The 6th was already in the design's prompt sketch but not counted in the rules list.
- Added domain-name skip heuristic in Phase 2 ("firstlightfusion.com" → skip, search news instead) since many headers list bare domains, not full URLs.

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- File A: 3 sources acquired (ipgroupplc, prnewswire, theengineer) → `partial` recommendation (~75% coverage)
- File B: 3 sources acquired (generalfusion x2, metaltechnews) → `delete` recommendation (>80% coverage)
- Fixed: moved resumability skip check before `ensure_new_iter()` to prevent spurious empty iter dirs on re-run

**Issues:**
- Resumability created empty iter dirs before checking skip status. Fixed by moving skip logic to main loop, deferring `ensure_new_iter()` until first non-skipped file.

**Deviations:**
- File B's no-URL case worked even better than expected: the agent found URLs in web search results and extracted 3 sources. The design predicted "1-2 sources from news coverage" but the agent found the company's own blog posts (which are standard HTML, not JS-heavy) plus a news article.
