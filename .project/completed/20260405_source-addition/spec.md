# Spec: Source Addition and Incremental Updates

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29T12:28:18-07:00
**Complexity:** MEDIUM
**Branch:** source-addition
**Epic:** ANALYSIS-V2, Item 3

---

## Business Goals

### Why This Matters

Adding a new data source to a concept currently requires manual file placement and a full re-analysis from scratch. As the project accumulates more sources (new papers, updated URLs, additional references), we need an incremental path: add one source, update the analysis to incorporate it, without re-running the entire pipeline.

This is the operational complement to the iterative analysis loop (Item 1) — the loop enables convergence on existing data; source addition enables growth of the data set.

### Success Criteria

- [ ] A user can add a PDF or URL source to any concept with a single command
- [ ] A user can update an existing analysis to incorporate new sources without full re-run
- [ ] Source layout matches established companion-directory + symlink conventions
- [ ] Downstream artifacts are marked stale after analysis update

### Priority

Second-week work per epic timeline. Depends on Item 1 (complete). Unblocks human vetting workflows where reviewers discover missing sources.

---

## Problem Statement

### Current State

- Sources are placed manually during Phase 1a research iterations
- Source replacement (`.project/active/source-replacement/`) established the companion-dir + symlink layout but operates as a batch replacement process, not incremental addition
- Re-incorporating a new source requires `--force` on the full `analyze` command, discarding the existing converged analysis
- No CLI path from "I found a relevant paper" to "it's in the analysis"

### Desired Outcome

Two new `run_analysis.py` subcommands:
1. `add-source` — extracts and places a source following conventions
2. `update-analysis` — incrementally updates the analysis to incorporate new sources

---

## Scope

### In Scope

- `cmd_add_source` subcommand with PDF path and URL support
- Automatic source name derivation (slugified from filename or URL)
- Companion-directory + symlink creation following established conventions
- `agentic-mbse extract --save-source` integration
- Nested PDF subdirectory flattening
- `cmd_update_analysis` subcommand using the analysis agent's feedback-pass mode
- Source name resolution: user provides short names (e.g., `sparc-icrf-heating-paper`), command finds the full path under the concept's `iter-*/sources/` directories
- Staleness propagation on downstream artifacts after update
- `--dry-run` support for both commands

### Out of Scope

- Batch source enrichment for already-analyzed concepts
- Dossier auto-update (dossier is a Phase 1a artifact, not updated here)
- Phase 1a prompt redesign
- New prompt templates for the analysis agent (reuses existing `analysis_v2.md` in feedback-pass mode). Note: the source-integration pre-pass (FR-15 Step 1) does require a new lightweight prompt template to generate F-N feedback from new sources.
- Source removal or replacement (covered by source-replacement work item)

### Edge Cases & Considerations

- Concept with no existing iterations: create `iter-01/sources/` automatically
- Concept with no existing analysis: `add-source` works (just places files); `update-analysis` SHOULD require an existing `analysis.md`
- Duplicate source name: MUST detect and refuse if a source with the same name already exists in any iteration
- URL that serves a PDF (not HTML): `agentic-mbse extract` auto-detects content type — no special handling needed
- Extraction failure: MUST clean up partial artifacts (companion dir) and report the error clearly
- Source name collision between iterations: `update-analysis` resolves source names by scanning all `iter-*/sources/` directories (same as `find_sources()`)

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

**`add-source` subcommand:**

1. **FR-1**: MUST accept a concept ID (positional) and a source path/URL (positional). Example: `run_analysis.py add-source 11 path/to/paper.pdf` or `run_analysis.py add-source 11 https://example.com/article`
2. **FR-2**: MUST automatically derive a descriptive source name from the input:
   - PDF: slugify the filename (strip extension, lowercase, hyphens for separators)
   - URL: slugify to produce a descriptive short name (e.g., `wham-experiment-details` style)
3. **FR-3**: MUST place the source in the latest existing `iter-NN/sources/` directory for the concept. If no iterations exist, MUST create `iter-01/sources/`.
4. **FR-4**: MUST run `agentic-mbse extract <source> --save-source --output <sources-dir>/<name>/` to extract the source
5. **FR-5**: MUST flatten nested PDF subdirectories if extraction creates them (same logic as source replacement)
6. **FR-6**: MUST create symlink `<name>.md` pointing to `<name>/output.md` in the sources directory
7. **FR-7**: MUST print confirmation with the new source symlink path on success
8. **FR-8**: MUST detect and refuse duplicate source names (same name exists in any `iter-*/sources/` for the concept)
9. **FR-9**: [INFERRED] MUST clean up partial artifacts on extraction failure (remove companion dir if created)
10. **FR-10**: [INFERRED] SHOULD support `--name` override flag for cases where automatic naming is inadequate
11. **FR-11**: [INFERRED] SHOULD support `--dry-run` to show what would be created without running extraction

**`update-analysis` subcommand:**

12. **FR-12**: MUST accept a concept ID (positional) and `--sources` flag with one or more source names. Example: `run_analysis.py update-analysis 11 --sources sparc-icrf-heating-paper new-paper-name`
13. **FR-13**: MUST resolve source names to full paths by scanning `iter-*/sources/<name>.md` under the concept's research directory
14. **FR-14**: MUST require an existing `analysis.md` for the concept (cannot update what doesn't exist)
15. **FR-15**: MUST use a two-step process to incorporate new sources:
    - **Step 1 (source integration pre-pass)**: A lightweight Claude call that reads the new source(s) + existing `analysis.md` and produces structured feedback in the same F-N format used by the assessment agent (Target, Finding, Recommendation, Priority). This feedback identifies *what specific information* from the new source should be integrated and *where* in the analysis.
    - **Step 2 (feedback-pass)**: Feed the generated feedback into the existing `analysis_v2.md` template in feedback-pass mode, exactly as assessment feedback is processed.
    - **Rationale**: This follows the unified feedback pattern established by Item 1 and continued by Item 5 — all agents (assessment, source-update, manage-concept) produce F-N feedback that flows through the same modal prompt. The pre-pass ensures the analysis agent gets specific, actionable integration instructions rather than a vague "read this source."
16. **FR-16**: MUST trigger `propagate_staleness()` on downstream artifacts after the analysis is updated
17. **FR-17**: MUST save the pre-pass feedback as `feedback_update_<timestamp>.md` for audit trail (same directory as `feedback_iter_N.md` files)
18. **FR-18**: [INFERRED] SHOULD support `--dry-run` to show the generated feedback without invoking the analysis agent (pre-pass runs, feedback-pass does not)
19. **FR-19**: [INFERRED] SHOULD support `--model` and `--timeout` flags consistent with other subcommands

### Non-Functional Requirements

- **NF-1**: Both commands MUST follow the same CLI patterns as existing subcommands (argparse, `--model`, `--timeout`, `--dry-run`, `--force`)
- **NF-2**: Source discovery in `find_sources()` MUST NOT require changes — new sources are automatically picked up by the existing `iter-*/sources/*.md` glob

---

## Acceptance Criteria

### Core Functionality

- [ ] `run_analysis.py add-source 11 path/to/paper.pdf` creates `iter-NN/sources/paper.md` (symlink) + `paper/` companion dir with `output.md`, `raw.pdf`, `metrics.json`
- [ ] `run_analysis.py add-source 11 https://example.com/article` creates same layout with `raw.html`
- [ ] Companion dir includes provenance artifacts (`--save-source`)
- [ ] `run_analysis.py update-analysis 11 --sources paper` generates F-N feedback from pre-pass, then applies via feedback-pass mode
- [ ] Pre-pass feedback saved as `feedback_update_<timestamp>.md` with specific integration instructions (not generic "read this source")
- [ ] Downstream artifacts marked stale after update
- [ ] `--dry-run` on `update-analysis` runs pre-pass and shows feedback but does not invoke analysis agent
- [ ] Duplicate source name is detected and rejected with clear error message

### Quality & Integration

- [ ] Existing tests continue to pass
- [ ] `find_sources()` automatically discovers added sources without code changes
- [ ] Error handling: extraction failure cleans up and reports clearly
- [ ] CLI help text is clear and consistent with existing subcommands

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 3)
- **Dependency:** `.project/active/iterative-analysis-loop/` (Item 1, complete — provides feedback format, modal prompt, staleness propagation)
- **Conventions:** `.project/active/source-replacement/` (companion-dir + symlink layout)
- **Design:** `.project/active/source-addition/design.md` (to be created)
- **Pipeline:** `exploration/concept_analysis/scripts/run_analysis.py`

---

**Next Steps:** After approval, proceed to `/_my_design`
