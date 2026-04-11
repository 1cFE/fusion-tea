# Design: Stage 1 Loop Refactor (Work Item #2)

**Status:** Complete
**Owner:** reid
**Created:** 2026-04-05
**Updated:** 2026-04-05
**Branch:** design-space-explore
**Commit at design time:** 280a4f0

---

## Overview

Extract `cmd_analyze`'s 270-line inlined loop into a dedicated loop runner with per-iteration directories (`iter-N/`), structured verdicts (`verdict.json`), substitutable feedback-producers, in-loop model-setup, and `--resume` semantics. Replace `cmd_update_analysis` with `source add` + `stage1-all --resume`.

## Related Artifacts

- **Spec:** `.project/active/refactor-stage1-loop/spec.md`
- **Prereq (landed):** `.project/active/refactor-run-analysis/spec.md` (WI#1 — lib/ split, commit 280a4f0)
- **Architecture review:** `.project/research/20260405-concept-analysis-refactor.md`
- **Autonomous source acquisition (follow-on):** `.project/active/autonomous-source-acquisition/spec.md`

---

## Research Findings

### Current Module Structure (post-WI#1)

```
scripts/
├── run_analysis.py          1380 lines  (CLI, dispatch, 12 handlers)
└── lib/
    ├── claude.py               73 lines  (invoke_claude, run_model)
    ├── concepts.py            235 lines  (CSV loader, resolver, costingfe mapping)
    ├── frontmatter.py         102 lines  (YAML frontmatter ops)
    ├── memory.py              109 lines  (reuse pool discovery)
    ├── paths.py                35 lines  (path constants)
    ├── sources.py             214 lines  (find_sources, slugify, format)
    ├── state.py                99 lines  (get_concept_state, propagate_staleness)
    ├── step_runner.py         154 lines  (run_claude_step helper)
    └── templating.py           47 lines  (fill_template)
```

### Key Integration Points

- **`cmd_analyze`** (`run_analysis.py:202-473`): Three modes — feedback-apply (286-332), cold start (334-386), assess loop (387-473). The assess loop calls `invoke_claude` directly (not `run_claude_step`) because it alternates assess and analyze with loop control.
- **`cmd_model_setup`** (`run_analysis.py:475-557`): Uses `run_claude_step` for prompt invocation, then `run_model()` for execution. Needs `get_model_path()` and `get_costingfe_mapping()` for template selection.
- **`cmd_update_analysis`** (`run_analysis.py:1077-1224`): Two-step source-integration → feedback-pass. Duplicate of `common_vars` construction.
- **`cmd_stage1_all`** (`run_analysis.py:923-965`): Calls handler functions sequentially with shared `args` namespace.
- **`run_claude_step`** (`lib/step_runner.py:45-154`): Generic step runner. Not usable for in-loop steps because it handles skip-if-exists and concept resolution. The loop needs a lower-level invocation pattern.
- **`get_concept_state`** (`lib/state.py:9-56`): File-existence-based FSM. No iteration awareness.
- **Verdict parsing** (`run_analysis.py:421-426`): `re.search(r"^VERDICT:\s*PASS", ...)` + `re.findall(r"^### F-\d+:", ...)`.

### Current Iteration Artifact Layout

Flat in concept root:
```
analyses/01-hts-compact-tokamak/
├── analysis.md                      # canonical (frontmatter + body)
├── analysis_prompt_iter_1.md        # cold-start prompt
├── analysis_prompt_iter_2.md        # feedback-pass prompt
├── analysis_prompt_iter_3.md        # feedback-pass prompt
├── assessment_prompt_iter_1.md      # assess prompt
├── assessment_prompt_iter_2.md
├── assessment_prompt_iter_3.md
├── feedback_iter_1.md               # assess output (findings)
├── feedback_iter_2.md
├── feedback_iter_3.md
├── gap_check_prompt.md              # non-iteration prompts
├── gap_report.md
├── model_setup_prompt.md
├── model_setup.py
├── model_output.txt
├── review_prompt.md
├── review.md
└── ...
```

30 concepts have 1 iteration, 8 have 3 iterations (with 3 feedback cycles). Only `17a-laser-icf-hybrid-drive` has source-integration artifacts (`source_integration_prompt_*.md`, `feedback_update_*.md`).

### Template System

- **analysis_v2.md**: Conditional modes via `{{#if cold_start}}`, `{{#if feedback_pass}}`, `{{#if self_advance}}`. Feedback-pass mode reads `{{feedback_path}}`. Claude uses Edit tool to modify `analysis.md` in-place during feedback passes.
- **assessment.md**: Takes `{{concept_name}}`, `{{analysis_path}}`, `{{feedback_path}}`. Claude writes findings to `feedback_path`.
- **source_integration.md**: Takes `{{concept_name}}`, `{{analysis_path}}`, `{{new_source_paths}}`, `{{feedback_path}}`. Claude writes findings to `feedback_path`.
- **feedback_format.md**: Shared schema — `VERDICT: PASS/FINDINGS` + `### F-N:` findings.

### Cold-Start Artifact Assembly

Cold start (`run_analysis.py:334-386`) works differently from feedback passes:
1. Pre-writes `analysis.md` with frontmatter only.
2. Claude writes body to `analysis_body.md`.
3. Post-step: read back frontmatter (Claude may have edited Reuses field) + body → assemble `analysis.md`.
4. Delete `analysis_body.md`.

Feedback passes: Claude uses Edit tool on `analysis.md` directly. No separate body file.

---

## Spec Deviations

### FR-17 Amendment: Source-Integration Output Naming

The spec (FR-2) says `iter-N/feedback.md` is "the assess step's output." FR-17 says source-integration "writes its output to iter-N/feedback.md." These conflict — both assess and source-integration would write to the same file in a source-integration iteration, and the assess output would overwrite the source-integration findings, losing the audit trail.

**Amendment:** `iter-N/feedback.md` is always the assess output (as FR-2 says). Source-integration output goes to `iter-N/source_integration_output.md`. The analyze step reads feedback from whichever file the feedback-producer wrote — it receives the path via template variable and doesn't care about the filename.

| Iteration type | Analyze reads feedback from | Assess writes to |
|---|---|---|
| Cold start (iter-1) | *(none)* | `iter-1/feedback.md` |
| Normal (iter N>1) | `iter-(N-1)/feedback.md` | `iter-N/feedback.md` |
| Source-integration | `iter-N/source_integration_output.md` | `iter-N/feedback.md` |
| Research (future) | `iter-N/research_output.md` | `iter-N/feedback.md` |

This preserves both the assess and source-integration outputs for audit, and keeps the naming contract from FR-2 intact.

---

## Proposed Design

### Architecture Overview

Two new modules, changes to three existing modules, one migration script:

```
scripts/
├── run_analysis.py          ~900 lines  (reduced: loop/update-analysis extracted)
├── migrate_iterations.py    ~200 lines  (one-shot migration)
└── lib/
    ├── iteration.py         ~180 lines  (NEW: iter state, verdict.json, feedback-producer)
    ├── loop.py              ~250 lines  (NEW: stage1 loop runner)
    ├── state.py             ~120 lines  (MODIFIED: iteration-aware get_concept_state)
    ├── step_runner.py       ~154 lines  (unchanged)
    └── ...                              (other lib/ modules unchanged)
```

### Component 1: `lib/iteration.py` — Iteration State Management (~180 lines)

**Purpose:** Read/write per-iteration state, select feedback-producers, detect resume points.

```python
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class IterationState:
    """Parsed state of one completed or in-progress iteration."""
    iteration: int
    verdict: str                    # "PASS" | "FAIL" | "ERROR" | "INTERRUPTED"
    finding_count: int
    feedback_source: str            # "cold_start" | "assess" | "source_integration" | "research"
    model_ran: bool
    model_ok: bool
    research_ran: bool
    sources: list[str]              # source paths used in this iteration's analyze prompt
    timestamp: str                  # ISO 8601

@dataclass
class LoopState:
    """Aggregate state of all iterations for a concept."""
    iterations: list[IterationState]
    last_complete: int              # highest iter with verdict.json (0 if none)
    last_incomplete: int | None     # iter with artifacts but no verdict.json

    @property
    def next_iteration(self) -> int:
        if self.last_incomplete is not None:
            return self.last_incomplete
        return self.last_complete + 1

    @property
    def all_prior_sources(self) -> set[str]:
        """Union of source paths across all completed iterations."""
        result: set[str] = set()
        for it in self.iterations:
            result.update(it.sources)
        return result
```

**Key functions:**

```python
def read_loop_state(concept_dir: Path) -> LoopState:
    """Scan iter-*/ dirs, read verdict.json files, detect incomplete iterations."""

def write_verdict(iter_dir: Path, *, iteration: int, verdict: str,
                  finding_count: int, feedback_source: str,
                  model_ran: bool, model_ok: bool, research_ran: bool,
                  sources: list[str]) -> Path:
    """Write verdict.json with ISO timestamp and source list. Returns path."""

def parse_verdict_from_feedback(feedback_text: str) -> tuple[str, int]:
    """Parse VERDICT: PASS/FAIL and finding count from feedback text.
    Returns (verdict_str, finding_count). Uses existing regex patterns."""

def detect_new_sources(loop_state: LoopState,
                       current_sources: list[Path]) -> list[Path]:
    """Compare current find_sources() output against sources recorded in
    prior iterations' verdict.json. Returns paths of newly-added sources."""

def clear_iterations(concept_dir: Path) -> int:
    """Delete all iter-*/ directories. Used by --force. Returns count deleted."""
```

**`read_loop_state` details:**
1. Glob `concept_dir / "iter-*"` → sort numerically.
2. For each `iter-N/`:
   - If `verdict.json` exists → parse into `IterationState` (including `sources` list), append to `iterations`.
   - If no `verdict.json` but `analyze_prompt.md` exists → mark as `last_incomplete = N`.

**`detect_new_sources` details:**
Compares `current_sources` (from `find_sources()`) against `loop_state.all_prior_sources` (union of all `verdict.json` `sources` fields). A source is "new" if its path string is not in `all_prior_sources`. No prompt parsing needed — `verdict.json` is the authoritative record of which sources were available at each iteration.

### Component 2: `lib/loop.py` — Stage 1 Loop Runner (~250 lines)

**Purpose:** The extracted, formalized stage1 assess↔analyze loop with model-setup inside.

**Top-level function:**

```python
def run_stage1_loop(
    concept: dict,
    args: argparse.Namespace,
    *,
    resume: bool = False,
    common_vars: dict,
    analysis_template: str,
    assessment_template: str,
) -> str:
    """Run the stage1 loop for one concept. Returns final verdict string."""
```

**Loop body (pseudocode):**

```python
def run_stage1_loop(concept, args, *, resume, common_vars, ...):
    cid = concept["_id"]
    concept_dir = ANALYSES_DIR / cid
    analysis_path = concept_dir / "analysis.md"
    max_passes = args.max_passes

    # Defensive copy — loop mutates source_paths each iteration (FR-12)
    common_vars = dict(common_vars)

    # 1. Handle --force: clean slate (delete all existing iter-*/ dirs)
    if args.force:
        deleted = clear_iterations(concept_dir)
        if deleted:
            print(f"  {cid}: cleared {deleted} prior iteration(s)")

    # 2. Read existing iteration state
    loop_state = read_loop_state(concept_dir)

    # 3. Determine start iteration
    if resume:
        start_iter = loop_state.next_iteration
        if start_iter > max_passes:
            print(f"  {cid}: max passes reached ({max_passes})")
            return loop_state.iterations[-1].verdict if loop_state.iterations else "NONE"
    else:
        start_iter = 1

    # 4. Detect new sources (for feedback-producer selection)
    current_sources = find_sources(concept["_research_id"])
    new_sources = detect_new_sources(loop_state, current_sources)
    used_source_integration = False

    for iter_num in range(start_iter, max_passes + 1):
        iter_dir = concept_dir / f"iter-{iter_num}"
        iter_dir.mkdir(parents=True, exist_ok=True)

        # --- Refresh sources each iteration (FR-12) ---
        current_sources = find_sources(concept["_research_id"])
        common_vars["source_paths"] = format_source_list(current_sources)

        # --- Select and run feedback-producer (FR-16) ---
        feedback_source = "cold_start"
        feedback_path = None

        if iter_num == 1 and not resume:
            # Cold start — no feedback producer
            feedback_source = "cold_start"
        elif new_sources and not used_source_integration:
            # Source-integration producer (FR-17)
            feedback_source = "source_integration"
            feedback_path = _run_source_integration(
                concept, iter_dir, new_sources, analysis_path, args)
            if feedback_path is None:
                # Source integration found PASS (no material additions)
                # Fall through to normal assess feedback
                feedback_source = "assess"
                feedback_path = _get_prior_feedback(concept_dir, iter_num)
            used_source_integration = True
        elif args.research and iter_num > 1:
            # Research extension point (FR-13, FR-14)
            feedback_source = "research"
            feedback_path = _run_research_step(concept, iter_dir, args)
            # FR-15: re-find sources after research
            current_sources = find_sources(concept["_research_id"])
            common_vars["source_paths"] = format_source_list(current_sources)
        else:
            # Normal: prior iteration's assess output
            feedback_source = "assess"
            feedback_path = _get_prior_feedback(concept_dir, iter_num)

        # --- Analyze step ---
        if feedback_source == "cold_start":
            _run_cold_start(concept, iter_dir, common_vars, analysis_template, args)
        else:
            _run_feedback_pass(concept, iter_dir, feedback_path, common_vars,
                               analysis_template, args)

        # --- Capture iteration output (FR-4) ---
        _capture_analysis_output(analysis_path, iter_dir)

        # --- Model-setup inside loop (FR-6) ---
        model_ran, model_ok = _run_model_in_iteration(concept, iter_dir, args)

        # --- Assess step ---
        verdict, finding_count = _run_assess(
            concept, iter_dir, analysis_path, assessment_template, args)

        # --- Write verdict.json (FR-3, FR-19) ---
        write_verdict(iter_dir,
                      iteration=iter_num, verdict=verdict,
                      finding_count=finding_count, feedback_source=feedback_source,
                      model_ran=model_ran, model_ok=model_ok,
                      research_ran=(feedback_source == "research"),
                      sources=[str(p) for p in current_sources])

        # --- Update canonical files (FR-4, FR-5) ---
        _update_canonical_files(concept_dir, iter_dir)

        # --- Propagate staleness ---
        propagate_staleness(cid, f"analysis-updated-iter-{iter_num}")

        if verdict == "PASS":
            return "PASS"

        # Last allowed pass?
        if iter_num >= max_passes:
            print(f"  warn: {cid} did not converge in {max_passes} passes")
            return verdict

    return verdict
```

**Internal helper functions in `lib/loop.py`:**

#### `_run_cold_start(concept, iter_dir, common_vars, template, args)`

Extracted from `run_analysis.py:334-386`. Key differences from current code:
- Writes `iter-N/analyze_prompt.md` (was `analysis_prompt_iter_1.md` at concept root).
- Writes `analysis_body.md` to `iter_dir` (was concept root).
- Assembly (frontmatter + body → `analysis.md`) is unchanged.
- On failure, writes verdict.json with `"ERROR"` and returns.

#### `_run_feedback_pass(concept, iter_dir, feedback_path, common_vars, template, args)`

Extracted from `run_analysis.py:440-472`. Key differences:
- Prompt saved to `iter-N/analyze_prompt.md`.
- `common_vars["feedback_path"]` set to the selected feedback source path.
- Claude still uses Edit tool on `analysis.md` — no template change needed.

#### `_capture_analysis_output(analysis_path, iter_dir)`

After each analyze step completes:
1. Read `analysis.md`, strip frontmatter, save body to `iter-N/analysis_output.md`.
2. This creates the per-iteration audit trail without changing how Claude writes (Edit tool on `analysis.md`).

#### `_run_model_in_iteration(concept, iter_dir, args) -> (bool, bool)`

Adapted from `cmd_model_setup` (`run_analysis.py:475-557`):
1. Determine template (costingfe vs free-form) using `get_model_path()`.
2. Build vars, fill template, save prompt to `iter-N/model_setup_prompt.md`.
3. Invoke Claude → writes `iter-N/model_setup.py`.
4. Run model → writes `iter-N/model_output.txt`.
5. Returns `(model_ran: bool, model_ok: bool)`.
6. On any failure: log and return `(False, False)` — does NOT abort the iteration (FR-7).

**Critical implementation note:** The in-loop model-setup must use `invoke_claude` directly (not `run_claude_step`) because `run_claude_step` has skip-if-exists and concept-resolution logic that doesn't apply inside the loop. The variable construction and template selection logic from `cmd_model_setup` will be extracted into a shared helper `_build_model_vars(concept, output_path)` so both the in-loop and standalone `cmd_model_setup` can use it.

#### `_run_source_integration(concept, iter_dir, new_sources, analysis_path, args) -> Path | None`

Extracted from `cmd_update_analysis` step 1 (`run_analysis.py:1111-1158`):
1. Fill `source_integration.md` template with new source paths.
2. Save prompt to `iter-N/source_integration_prompt.md`.
3. Invoke Claude → writes `iter-N/source_integration_output.md`.
4. Parse verdict. If PASS (no material additions), return `None`.
5. If FINDINGS, return `iter-N/source_integration_output.md` path (for analyze to consume as feedback).

#### `_run_research_step(concept, iter_dir, args) -> Path | None`

Stub for FR-13/FR-14:
```python
def _run_research_step(concept, iter_dir, args):
    """Extension point for autonomous-source-acquisition (FR-A3).
    Returns path to research feedback file, or None if no-op."""
    print(f"  research step not yet implemented — skipping")
    return None
```

When `None` is returned, the loop falls through to normal assess-based feedback.

#### `_run_assess(concept, iter_dir, analysis_path, template, args) -> (str, int)`

Extracted from `run_analysis.py:394-432`:
1. Fill assessment template.
2. Save prompt to `iter-N/assess_prompt.md`.
3. Invoke Claude → writes `iter-N/feedback.md`.
4. Parse verdict and finding count from feedback text.
5. Returns `(verdict, finding_count)`.

#### `_get_prior_feedback(concept_dir, iter_num) -> Path | None`

Returns `concept_dir / f"iter-{iter_num - 1}" / "feedback.md"` if it exists.

#### `_update_canonical_files(concept_dir, iter_dir)`

- Copy `iter-N/model_setup.py` → `concept_dir/model_setup.py` (FR-5).
- Copy `iter-N/model_output.txt` → `concept_dir/model_output.txt` (FR-5).
- Rebuild `analysis.md` from frontmatter + `iter-N/analysis_output.md` (FR-4 — already handled by `_capture_analysis_output`, but this ensures the canonical copy is current).

### Component 3: Changes to `run_analysis.py`

#### `cmd_analyze` Refactor

The 270-line function shrinks to ~60 lines:

```python
def cmd_analyze(concepts, args):
    """Stage 2: D1+ analysis with iterative assessment loop."""
    targets = resolve_concepts(...)
    resume = getattr(args, "resume", False)

    # Validate flag constraints
    if resume and args.force:
        print("Error: --resume and --force are mutually exclusive.")
        sys.exit(1)

    # Feedback-apply mode stays here (not part of the loop)
    feedback = getattr(args, "feedback", None)
    if feedback:
        _apply_external_feedback(targets, args, feedback)
        return

    # Load templates once
    analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text(...)
    assessment_template = (TEMPLATES_DIR / "assessment.md").read_text(...)

    for c in targets:
        cid = c["_id"]
        analysis_path = ANALYSES_DIR / cid / "analysis.md"

        # Skip logic (unchanged behavior without --resume)
        # --force: clear_iterations() runs inside run_stage1_loop, then cold-start from iter-1
        if not resume and not args.force and analysis_path.exists():
            print(f"  skip {cid} (analysis.md exists, use --force or --resume)")
            continue

        # Build common_vars (same as today)
        common_vars = _build_common_vars(c)

        # Delegate to loop runner
        run_stage1_loop(c, args, resume=resume,
                        common_vars=common_vars,
                        analysis_template=analysis_template,
                        assessment_template=assessment_template)
```

The `_build_common_vars(concept)` helper is extracted from the current lines 270-284 and shared with any code that needs it.

The `_apply_external_feedback` helper preserves the current feedback-apply mode (lines 286-332) for backward compat. This mode is unrelated to the loop and stays in `run_analysis.py`.

#### `cmd_stage1_all` Changes

```python
def cmd_stage1_all(concepts, args):
    # ... existing resolution and summary ...

    # Pass --resume through to analyze
    stages = []
    if getattr(args, "include_gap_analysis", False):
        stages.append(("Gap Check", cmd_gap_check))
    stages.extend([
        ("Analyze", cmd_analyze),       # respects args.resume
        ("Model Setup", cmd_model_setup),  # standalone, for non-loop re-runs
        ("Review", cmd_review),
    ])

    for stage_name, handler in stages:
        print(f"\n--- {stage_name} ---")
        handler(concepts, args)
```

With model-setup inside the loop, the standalone `cmd_model_setup` in the pipeline becomes a no-op for concepts that already have a current model from the loop. Its skip-if-exists logic (`model_setup.py exists`) handles this naturally — the loop already wrote `model_setup.py` to the concept root (FR-5).

#### `cmd_update_analysis` Removal (FR-18)

- Remove `cmd_update_analysis` function (~150 lines).
- Remove `"update-analysis"` from argparse and dispatch table.
- The equivalent workflow: `add-source <concept> <path>` + `stage1-all <concept> --resume`.

#### New Argparse Flags

```python
# On analyze subparser:
analyze_p.add_argument("--resume", action="store_true",
    help="Continue from last iteration (add more passes)")

# On stage1-all subparser:
stage1_p.add_argument("--resume", action="store_true",
    help="Resume analysis from last iteration")

# On both:
analyze_p.add_argument("--research", action="store_true",
    help="Enable autonomous research step between iterations (not yet implemented)")
stage1_p.add_argument("--research", action="store_true",
    help="Enable autonomous research step between iterations (not yet implemented)")
```

### Component 4: Changes to `lib/state.py`

**`get_concept_state` update (FR-11):**

Add iteration awareness. When `iter-*/` directories exist, use `verdict.json` for richer state:

```python
def get_concept_state(concept_id, analyses_dir=ANALYSES_DIR):
    # ... existing file-existence checks ...

    # New: if iter-*/ dirs exist, augment state with iteration info
    # This doesn't change the return type (still a string) but the
    # information is richer for status display
    # ... existing logic unchanged ...
```

The existing `get_concept_state` return values are consumed by `cmd_status` and `resolve_concepts` (which uses `target_state` to filter). These consumers don't need iteration details — they need the same state string. So `get_concept_state` signature is unchanged.

Add a separate function for detailed iteration state:

```python
def get_iteration_summary(concept_id, analyses_dir=ANALYSES_DIR) -> str | None:
    """Return human-readable iteration summary for status display.
    E.g., 'iter-3/PASS' or 'iter-2/FAIL (3 findings)' or None if no iterations."""
```

`cmd_status` can display this alongside the existing state.

### Component 5: `prompts/` Directory Cleanup (FR-20, FR-21)

Non-iteration prompt files move to `prompts/` subdirectory. This is handled by:

1. **Migration script** moves existing files.
2. **Code changes** in handlers that write these prompts:
   - `cmd_gap_check`: write to `prompts/gap_check_prompt.md`
   - `cmd_review`: write to `prompts/review_prompt.md`
   - `cmd_synthesize`: write to `prompts/synthesis_prompt.md`
   - `cmd_address_review`: write to `prompts/address_review_prompt.md`

These are ~1-line path changes per handler (changing `out_dir / "review_prompt.md"` to `out_dir / "prompts" / "review_prompt.md"` with a `mkdir`).

### Component 6: Migration Script (`scripts/migrate_iterations.py`, ~200 lines)

**Purpose:** One-shot reorganization of existing 38 concept directories.

**Operations per concept:**

1. **Detect existing iterations.** Glob `analysis_prompt_iter_*.md` → extract iter numbers. Also detect `feedback_iter_*.md` and `assessment_prompt_iter_*.md`.

2. **Create `iter-N/` directories and move files:**

   | Old location | New location |
   |---|---|
   | `analysis_prompt_iter_1.md` | `iter-1/analyze_prompt.md` |
   | `assessment_prompt_iter_N.md` | `iter-N/assess_prompt.md` |
   | `feedback_iter_N.md` | `iter-N/feedback.md` |
   | `analysis_body.md` (if present) | `iter-1/analysis_output.md` |

   For iter-1 `analysis_output.md`: if `analysis_body.md` doesn't exist (it's deleted after assembly), extract body from `analysis.md` by stripping frontmatter.

3. **Generate `verdict.json` for each iteration (FR-23):**
   - If `feedback_iter_N.md` exists: parse verdict/finding_count via existing regex.
   - If no feedback file: verdict = `"INTERRUPTED"`.
   - `feedback_source`: iter-1 = `"cold_start"`, iter-N>1 = `"assess"`.
   - `model_ran` / `model_ok`: `false` (model wasn't inside the loop pre-migration).
   - `research_ran`: `false`.
   - `sources`: populated by scanning the rendered `analysis_prompt_iter_N.md` for source paths (one-time migration-only parse; all future iterations use the live source list). This provides the baseline for `detect_new_sources` on first `--resume` after migration.
   - `timestamp`: use file mtime of the feedback or analysis file.

4. **Move non-iteration prompts to `prompts/`:**

   | Old | New |
   |---|---|
   | `gap_check_prompt.md` | `prompts/gap_check_prompt.md` |
   | `analysis_prompt.md` | `prompts/analysis_prompt.md` |
   | `review_prompt.md` | `prompts/review_prompt.md` |
   | `synthesis_prompt.md` | `prompts/synthesis_prompt.md` |
   | `address_review_prompt.md` | `prompts/address_review_prompt.md` |
   | `model_setup_prompt.md` | `prompts/model_setup_prompt.md` |
   | `source_integration_prompt_*.md` | `prompts/source_integration_prompt_*.md` |
   | `feedback_update_*.md` | `prompts/feedback_update_*.md` |
   | `update_analysis_prompt_*.md` | `prompts/update_analysis_prompt_*.md` |
   | `feedback_apply_prompt_*.md` | `prompts/feedback_apply_prompt_*.md` |

5. **Leave canonical files in place:** `analysis.md`, `model_setup.py`, `model_output.txt`, `gap_report.md`, `review.md`, `address_log.md`, `synthesis.md`.

**Idempotency (FR-24):** Before each move, check if destination already exists. If it does, skip. Before creating `verdict.json`, check if it already exists. This makes the script safe to re-run.

**CLI:**
```bash
uv run python scripts/migrate_iterations.py              # migrate all
uv run python scripts/migrate_iterations.py 02            # migrate one concept
uv run python scripts/migrate_iterations.py --dry-run     # preview
```

### Assess Prompt Template Change (FR-8)

The assess template currently takes `{{analysis_path}}` and `{{feedback_path}}`. To evaluate model quality (FR-6), it needs the model output. Add one variable:

```
{{#if model_output_path}}

## Model Output

The concept also has a quantitative LCOE model. The model output is at:
`{{model_output_path}}`

Evaluate whether the model's assumptions and parameter values are consistent
with the analysis. Note any discrepancies in your findings.
{{/if}}
```

This is a minimal template addition (~6 lines), well within the spec's "if trivial, in scope" guidance for FR-8.

---

## Potential Risks

1. **Claude's Edit-tool workflow.** The analyze feedback-pass tells Claude to edit `analysis.md` in place. The new `_capture_analysis_output` step reads back the body after Claude finishes. Risk: if Claude fails partway through edits, the captured body may be partial. **Mitigation:** The same risk exists today — partial edits are caught by `rc != 0` from `invoke_claude`.

2. **Model-setup inside the loop adds ~2-3 min per iteration.** Currently model-setup runs once after the loop. With 3 iterations, that's 3 model runs instead of 1. **Mitigation:** The spec explicitly requires this (FR-6). The cost is justified because the assess step can now evaluate model quality. For concepts where model generation is slow, `--max-passes 1` skips the loop.

3. **Migration script and git history.** Moving files changes git blame. **Mitigation:** Use `git mv` where possible so git tracks renames. The migration commit should be standalone (no other changes) so it's easy to identify.

4. **`--feedback` mode interaction with `--resume`.** The `--feedback` flag applies an external feedback file to an existing analysis. This is orthogonal to the loop and should remain a separate mode. **Mitigation:** `--feedback`, `--force`, and `--resume` are all mutually exclusive. The error message for invalid combinations is clear.

5. **Migrated verdicts show `model_ran: false`.** All 38 pre-migration iterations will have `model_ran: false` / `model_ok: false` even for concepts that have working models at the concept root. This is accurate — model-setup was not inside the loop before this change. **Mitigation:** Status display should treat `model_ran: false` as "pre-loop model" when the iteration predates this change (identifiable by the migration-era timestamp). The `get_iteration_summary` function should show iteration count and verdict without surfacing model_ran for migrated iterations.

---

## Integration Strategy

### How This Fits Into the Existing Workflow

**Before this change:**
- `analyze 02` → cold start + assess loop (flat artifacts)
- `model-setup 02` → standalone model generation
- `review 02` → human review
- `update-analysis 02 new-source` → opaque source integration

**After this change:**
- `analyze 02` → unchanged (skip-if-exists or `--force` to restart)
- `analyze 02 --resume` → continue from last iteration
- `stage1-all 02 --resume` → resume analysis + model-setup + review
- `add-source 02 <path>` + `stage1-all 02 --resume` → replaces `update-analysis`
- `model-setup 02` → still works standalone for re-runs outside the loop

**Non-stage1 commands unaffected:** `review`, `address-review`, `synthesize`, `approve`, `status`, `list` all read from concept root (`analysis.md`, `review.md`, etc.) which is unchanged.

### Backward Compatibility

- `analyze 02` without `--resume` preserves muscle memory: skip if exists, `--force` to restart.
- `stage1-all 02` without `--resume` runs the full pipeline from scratch (or skips completed steps), same as today.
- The `--feedback` flag continues to work for ad-hoc feedback application.
- After migration, existing concept directories have the same canonical files at the concept root. Only the audit-trail artifacts have moved into `iter-N/` and `prompts/`.

---

## Validation Approach

### Testing Strategy

1. **Dry-run comparison.** For a concept with 3 existing iterations (e.g., `01`), run `analyze 01 --dry-run` before and after. The rendered prompt should be identical (the template, variables, and analysis_path are all the same).

2. **Migration verification.** After running the migration script:
   - `status` output matches pre-migration.
   - `get_concept_state` returns same values for all 38 concepts.
   - Every `feedback_iter_N.md` has been moved to `iter-N/feedback.md`.
   - Every migrated iteration has a `verdict.json` with correct verdict/finding_count.
   - `analysis.md` content is unchanged (byte-identical).

3. **Resume on a test concept.** Pick a concept with a FAIL verdict at its last iteration. Run `stage1-all <id> --resume --max-passes 1 --dry-run`. Verify:
   - It detects the existing iterations.
   - It generates the next iteration's prompt with the correct feedback path.
   - The model-setup prompt is generated.

4. **Mutual exclusivity.** `analyze 02 --resume --force` exits with error. `analyze 02 --resume --feedback x` exits with error.

5. **Source-integration flow.** After `add-source` + `stage1-all --resume --dry-run`, verify the first new iteration uses the source-integration template.

### Success Criteria

Per the spec's acceptance criteria — all items in the Resume, Loop Structure, Substitutable Feedback-Producers, Research Extension Point, Directory Layout & Migration, Backward Compatibility, and Quality sections.

---

Next Step: After approval → `/_my_plan` to create phased implementation plan.
