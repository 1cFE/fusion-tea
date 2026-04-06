# Spec: run_analysis.py Code Cleanup (Work Item #1)

**Status:** Draft
**Owner:** reid
**Created:** 2026-04-05
**Complexity:** LOW
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

`run_analysis.py` is 2306 lines in a single file. The practical problem is that agents (including Claude Code sessions) cannot hold the whole file in context cleanly, which makes every subsequent change — including Work Items #2 (stage1 loop + `--resume`) and #3 (final-stages rescope) — harder than it needs to be. The file is also structurally repetitive: eight command handlers each reimplement the same ~60-line "resolve → skip-if-exists → fill template → invoke Claude → check rc → save output" boilerplate.

This work item is a pure mechanical cleanup: split the file into navigable modules and extract the handler boilerplate into one shared helper. No behavior changes, no CLI changes, no prompt changes. The payoff is smaller files and fewer lines, which directly unblocks #2 and #3.

### Success Criteria

- [ ] No file in the concept-analysis scripts tree exceeds ~400 lines.
- [ ] The eight single-shot command handlers each shrink to roughly the part that is actually distinctive (variable construction + post-hook), with the shared shape lifted into one helper.
- [ ] An agent session can read any one module in a single Read call without hitting the 2000-line limit.
- [ ] Every existing CLI command produces identical output against a fixed concept fixture, before and after the refactor.

### Priority

Prerequisite for Work Items #2 and #3. Should land first because it is risk-free and makes the subsequent work items easier to review.

---

## Problem Statement

### Current State

- `exploration/concept_analysis/scripts/run_analysis.py` is 2306 lines containing: path constants, costingfe mapping tables, CSV loader, concept resolver, frontmatter parser, state detection, template engine, Claude/model invocation, source discovery, source addition helpers, memory loader, 14 command handlers, and the argparse builder.
- Eight of the command handlers (`gap_check`, `analyze` cold-start, `model_setup`, `review`, `address_review`, `synthesize`, plus the assess and feedback-pass calls inside the analyze loop) each contain a near-identical ~60-line sequence: resolve targets → iterate → skip-if-exists → load template → gather inputs → `fill_template` → save prompt → dry-run short-circuit → `invoke_claude` → rc check → verify output file → done-print. The distinctive parts (which template, which inputs, which post-hook) are usually 10-20 lines per handler.
- The 270-line `cmd_analyze` and 150-line `cmd_update_analysis` contain the same boilerplate *plus* the assess loop and source-integration logic; this work item leaves those structural pieces alone (they are #2's job) and only extracts what is straightforwardly shared.

### Desired Outcome

- The ~20 utility functions are moved into a `lib/` subpackage, grouped by concern.
- The handler boilerplate becomes one helper function (`run_claude_step` or similar) that takes a template path, a variable-builder callable, an output path, and optional pre/post hooks.
- `run_analysis.py` shrinks to the CLI surface (argparse + dispatch) plus handler bodies that call into `lib/` and the step runner.

---

## Scope

### In Scope

- Create `exploration/concept_analysis/scripts/lib/` as a Python package.
- Move utility functions into grouped modules (proposed split below — exact boundaries may shift during implementation as long as no file exceeds ~400 lines).
- Extract the single-shot-handler boilerplate into one shared helper.
- Update imports in `run_analysis.py` to consume the new modules.
- Update any other script in `exploration/concept_analysis/scripts/` that imports from `run_analysis.py` (if any — to be confirmed during implementation).

### Out of Scope

- **No behavior changes.** Every CLI command must produce byte-identical artifacts (prompts, outputs, frontmatter updates, skip messages, timing output) before and after.
- **No CLI changes.** All 14 subcommands keep their names, flags, and argparse surface.
- **No changes to the assess↔analyze loop structure.** The 270-line `cmd_analyze` is left alone except for the parts that can trivially use the new shared helper for its non-loop sections. Loop restructuring is Work Item #2.
- **No changes to `cmd_update_analysis`.** It stays a separate opaque command. Work Item #2 collapses it.
- **No `iter-N/` directory migration.** That is Work Item #2.
- **No `--resume` flag.** That is Work Item #2.
- **No prompt template changes.**
- **No new dependencies.**
- **No test framework introduction.** Verification is done by fixture comparison (see Acceptance Criteria).

### Edge Cases & Considerations

- **Circular imports:** the step-runner helper needs `invoke_claude`, `fill_template`, and path constants. It should live in a module that imports from others but isn't imported by them. `lib/step_runner.py` is the natural leaf.
- **Path constants:** `CONCEPT_ANALYSIS_DIR`, `TEMPLATES_DIR`, etc. are used everywhere. They can stay in `run_analysis.py` and be imported by lib modules, OR move to `lib/paths.py`. Either works; pick whichever produces fewer import lines.
- **`cmd_analyze`'s loop body** is out of scope, but its *cold-start branch* and *feedback-apply branch* are structurally similar to the other handlers and MAY use the shared helper if it falls out cleanly. If it doesn't, leave them alone — #2 rewrites this function anyway.
- **`cmd_update_analysis`** contains two Claude invocations (source-integration pre-pass + feedback-pass analysis). The helper MAY be used for each, or the function MAY be left untouched. Prefer leaving it untouched to minimize risk.
- The handler boilerplate's "verify output file exists" check has two variants in the codebase: some handlers write to a known path and check `path.exists()`; `review` and `synthesize` additionally fall back to stdout if the agent printed instead of writing. The helper must support both variants (e.g., via an optional "stdout fallback" flag).
- **No silent improvements.** If the helper can "fix" what looks like a minor inconsistency between handlers, don't — preserve the exact current behavior so the fixture diff is empty. Cleanup goes in a later pass.

---

## Requirements

### Functional Requirements

> All requirements are from user's request.

1. **FR-1:** The single 2306-line `run_analysis.py` SHALL be split such that no resulting file exceeds ~400 lines.
2. **FR-2:** Utility functions SHALL be moved into a `lib/` subpackage grouped by concern. Proposed modules (exact grouping MAY change):
   - `lib/concepts.py` — CSV loader, resolver, `FAMILY_KEY_MAP`, `COSTINGFE_MAPPING`, `FREEFORM_CONCEPTS`, `FUEL_MAPPING`, `get_model_path`, `get_costingfe_mapping`.
   - `lib/frontmatter.py` — `parse_frontmatter`, `update_frontmatter_field`, `make_frontmatter`.
   - `lib/state.py` — `get_concept_state`, `propagate_staleness`, `_has_downstream_artifacts`.
   - `lib/sources.py` — `find_sources`, `format_source_list`, `slugify_source`, `_slugify_*`, `find_latest_sources_dir`, `check_duplicate_source`, `resolve_source_names`, `get_dossier_path`, `flatten_companion_dir`, `parse_proposed_actions`.
   - `lib/memory.py` — `load_relevant_memories`, `find_approved`, `find_approved_syntheses`, `find_exemplars`, `format_path_list`.
   - `lib/templating.py` — `fill_template`.
   - `lib/claude.py` — `invoke_claude`, `run_model`.
   - `lib/step_runner.py` — the shared handler boilerplate helper (see FR-3).
3. **FR-3:** The repeated ~60-line handler pattern SHALL be extracted into one shared helper with approximately this signature:
   ```python
   def run_claude_step(
       concept: dict,
       *,
       template_name: str,           # filename under TEMPLATES_DIR
       build_vars: Callable[[dict], dict],
       prompt_path: Path,            # where to save the rendered prompt
       output_path: Path,            # artifact Claude is expected to produce
       label: str,                   # for progress prints, e.g. "gap-check"
       args: argparse.Namespace,     # for --dry-run, --timeout, --model
       skip_if_exists: bool = True,
       allow_stdout_fallback: bool = False,
       post_hook: Callable[[dict, Path, str], None] | None = None,
   ) -> bool:                         # True on success, False on skip/failure
   ```
   The exact signature MAY differ; the requirement is that the helper replaces the handler boilerplate without altering its observed behavior.
4. **FR-4:** The eight single-shot command handlers — `cmd_gap_check`, `cmd_model_setup`, `cmd_review`, `cmd_address_review`, `cmd_synthesize`, and any of the simpler branches of `cmd_analyze` that fall out cleanly — SHALL use the helper from FR-3 for their main Claude invocation.
5. **FR-5:** `cmd_analyze`'s assess↔analyze loop, `cmd_update_analysis`, and `cmd_add_source` MAY remain structurally unchanged in this work item. They must still import from the new `lib/` modules where applicable but their internal flow is not a refactor target here.
6. **FR-6:** `run_analysis.py` SHALL retain: the CLI argparse builder, the dispatch table, the 14 command handlers (now thinner), and path constants used across the file (or move them to `lib/paths.py` if that reduces total import lines).
7. **FR-7:** All 14 existing CLI subcommands SHALL continue to parse identically and dispatch to the same handlers. No flag is added, removed, or renamed.

### Non-Functional Requirements

- **FR-NF-1:** No new third-party dependencies.
- **FR-NF-2:** Each module SHOULD be importable in isolation without circular-import errors.
- **FR-NF-3:** Total line count across the split SHOULD be *lower* than 2306, primarily from the FR-3 extraction collapsing ~300-400 lines of duplication.

---

## Acceptance Criteria

### Core Functionality

- [ ] `run_analysis.py` plus all `lib/*.py` modules total fewer lines than the original 2306.
- [ ] No file in `exploration/concept_analysis/scripts/` exceeds ~400 lines (`run_analysis.py` itself may be slightly larger if the CLI argparse section pushes it over; target is ~400, hard ceiling is 500).
- [ ] Every `lib/*.py` module is under 300 lines.
- [ ] All 14 subcommands parse without error (`run_analysis.py <cmd> --help` works for each).

### Behavior Preservation (the load-bearing check)

- [ ] **Dry-run fixture comparison.** For a representative concept (suggest `02` or whichever has the most complete analysis state), run each of the 8 dry-run-capable commands before and after the refactor and diff the generated prompt files. Diffs MUST be empty modulo absolute path differences from temp dirs (if any).
  - `gap-check 02 --dry-run`
  - `analyze 02 --dry-run`
  - `model-setup 02 --dry-run`
  - `review 02 --dry-run`
  - `address-review 02 --dry-run` (requires a review.md with filled decisions — use an existing one)
  - `synthesize 02 --dry-run`
  - `stage1-all 02 --dry-run`
  - `add-source 02 <any PDF> --dry-run`
- [ ] **Frontmatter round-trip.** `parse_frontmatter` + `update_frontmatter_field` on one real `analysis.md` produces byte-identical output before and after.
- [ ] **State detection.** `get_concept_state` returns the same value for every existing concept in `analyses/` before and after (a one-shot script that walks all 36 dirs and prints the state is sufficient).
- [ ] **`status` output.** `uv run python run_analysis.py status` produces byte-identical output before and after.

### Quality & Integration

- [ ] `ruff` / existing project linting (if any) passes on all new files.
- [ ] No `TODO`/`FIXME` markers introduced.
- [ ] Imports are explicit; no `from lib.foo import *`.
- [ ] The shared step-runner helper is used by ≥5 of the 8 candidate handlers, otherwise the extraction isn't earning its complexity.

---

## Related Artifacts

- **Research:** `.project/research/20260405-concept-analysis-refactor.md` — the original architecture review that motivated the broader refactor. Provides a full inventory of the current file.
- **Follow-on work items:**
  - Work Item #2: Stage1 loop refactor + `--resume` + `iter-N/` layout (separate spec to be written).
  - Work Item #3: Final-stages rescope (human review kick-back, final approval gate) (separate spec to be written later).

---

**Next Steps:** After approval, proceed to `/_my_design` (or skip straight to `/_my_plan` given the mechanical nature of this work item).
