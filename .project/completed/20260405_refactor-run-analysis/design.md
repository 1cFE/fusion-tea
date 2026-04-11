# Design: run_analysis.py Code Cleanup (Work Item #1)

**Status:** Draft (rev 2 — addresses review comments C1, M1–M3, m1–m4)
**Owner:** reid
**Created:** 2026-04-05
**Branch:** design-space-explore
**Commit:** 50862bc
**Spec:** [spec.md](spec.md)

---

## Overview

Mechanical split of `exploration/concept_analysis/scripts/run_analysis.py` (2306 lines) into a `lib/` subpackage plus extraction of the repeated "resolve → skip → fill → invoke → check → save" handler boilerplate into one shared helper. No behavior changes, no CLI changes, no prompt changes. Verified by byte-diff of dry-run prompt fixtures.

## Related Artifacts

- **Spec:** `.project/active/refactor-run-analysis/spec.md` (the contract for this work item)
- **Broader vision (out of scope here):** `.project/active/refactor-run-analysis/design-concept.md` — Step/Loop/Pipeline primitives. Rev 2 explicitly defers iter-N layout, loop-as-object, and command surface collapse to Work Items #2/#3.
- **Research:** `.project/research/20260405-concept-analysis-refactor.md` — full file inventory and LOC breakdown.
- **Downstream blockers:** Work Item #2 (stage1 loop + `--resume`), Work Item #3 (final-stages rescope). Both need this split to land first.

## Research Findings

### Current file inventory (confirmed via read)

All line ranges in `exploration/concept_analysis/scripts/run_analysis.py`:

| Concern | Lines | Functions |
|---|---:|---|
| Module constants | 32–65 | `CONCEPT_ANALYSIS_DIR`, `TEMPLATES_DIR`, `COSTINGFE_*`, `EXTRACT_OUTPUT`, … |
| Concept mapping tables | 65–132 | `COSTINGFE_MAPPING`, `FREEFORM_CONCEPTS`, `FUEL_MAPPING`, `FAMILY_KEY_MAP` |
| Concept resolver | 134–303 | `get_model_path`, `get_costingfe_mapping`, `_get_subcategory`, `load_table`, `resolve_one`, `resolve_concepts` |
| Frontmatter | 305–384, 484–503 | `parse_frontmatter`, `update_frontmatter_field`, `make_frontmatter` |
| State detection | 386–482 | `get_concept_state`, `propagate_staleness`, `_has_downstream_artifacts` |
| Template + Claude | 505–617 | `fill_template`, `invoke_claude`, `run_model` |
| Source management | 619–829 | `find_sources`, `_slugify_*`, `slugify_source`, `flatten_companion_dir`, `find_latest_sources_dir`, `check_duplicate_source`, `resolve_source_names`, `get_dossier_path`, `format_source_list`, `parse_proposed_actions` |
| Memory + reuse pool | 831–941 | `find_approved`, `find_approved_syntheses`, `find_exemplars`, `format_path_list`, `load_relevant_memories`, `_MEMORY_META_RE` |
| Command handlers | 942–2155 | `cmd_list`, `cmd_status`, `cmd_gap_check`, `cmd_analyze`, `cmd_model_setup`, `cmd_review`, `cmd_address_review`, `cmd_synthesize`, `cmd_approve`, `cmd_stage1_all`, `cmd_add_source`, `cmd_update_analysis` |
| Argparse + dispatch | 2157–2306 | `build_parser`, `main` |

### Handler boilerplate pattern (confirmed)

Read of `cmd_gap_check` (1007–1077), `cmd_review` (1452–1551), `cmd_address_review` (1553–1655), `cmd_synthesize` (1656–1798), plus spot checks of `cmd_model_setup` and the cold-start branch of `cmd_analyze`, confirms the following shape repeats:

```python
def cmd_X(concepts, args):
    targets = resolve_concepts(args.concepts, concepts, family=..., all_remaining=..., target_state="...")
    if not targets: print("No concepts to X."); return
    template_text = (TEMPLATES_DIR / "X.md").read_text(encoding="utf-8")
    for c in targets:
        cid = c["_id"]; rid = c["_research_id"]
        out_dir = ANALYSES_DIR / cid
        output_path = out_dir / "<artifact>.md"
        # prereq checks (vary)
        if not <prereq>.exists(): print(f"  skip {cid} (…)"); continue
        # skip-if-exists
        if output_path.exists() and not args.force: print(f"  skip {cid} (… use --force)"); continue
        # distinctive inputs (10–20 lines: iteration count, sources, prior syntheses, decisions block, …)
        prompt = fill_template(template_text, {...})
        out_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = out_dir / "X_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        if args.dry_run: print(f"  dry-run {cid}: prompt saved to {prompt_path}"); continue
        print(f"  X {cid} ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model)
        elapsed = time.time() - t0
        if rc != 0: print(f" FAILED ({elapsed:.0f}s, rc={rc})"); print(f"    stderr: {stderr[:500]}", file=sys.stderr); continue
        # output verification (two variants — see below)
        # post-hook (varies: frontmatter update, run model, parse verdict, assemble final file)
        print(f" done ({elapsed:.0f}s, {size} chars)")
```

**Output-verification variants observed (4 modes, not 3):**

1. **stdout → file** (`cmd_gap_check`): Claude prints, script writes `stdout` to `gap_report.md`.
2. **file-with-stdout-fallback** (`cmd_review`, `cmd_synthesize`): Claude is expected to use the Write tool; if the file is missing but `stdout.strip()`, fall back to writing stdout. Synthesize additionally unlinks `synthesis.md` on rc!=0.
3. **file-exists-no-fallback** (`cmd_model_setup`, lines 1432–1434): Claude is expected to use the Write tool to produce `model_setup.py`. If the file does not exist after the call, print `f" FAILED ({elapsed:.0f}s) — Claude did not write {model_path}"` and `continue`. **No stdout fallback.** This is its own mode, not a parameter of (2).
4. **no-output-file** (`cmd_address_review`): Claude uses the Edit tool; there is nothing to verify beyond rc==0. Post-hook re-runs the model and updates frontmatter.

**Label-suffix variant (`cmd_model_setup`):** both the dry-run print and the progress print embed `(path_label)` — either `"1costingfe"` or `"free-form"` — mid-string:
- Dry-run: `f"  dry-run {cid} ({path_label}): prompt saved to {prompt_path}"`
- Progress: `f"  model-setup {cid} ({path_label}) ..."`

This is a per-concept computed suffix (not a constant — `get_model_path(c)` branches on concept metadata), which the helper must accept as a parameter. **Size suffix also varies:** `model_setup` prints `"{size} bytes"` while `review`/`synthesize`/`gap_check` print `"{size} chars"`. The size-suffix is the post-hook's problem (see M3 resolution below), but the label-suffix is the helper's.

**Post-hook variants observed:**

- `gap_check`: none.
- `review`: parse `review.md` for `**Overall:** CLEAN`, write `Review-Iterations` / `Last-Review` / `Review-Status` frontmatter.
- `address_review`: optional `run_model` re-execution, set `Review-Status: addressed`.
- `synthesize`: pre-write controlled frontmatter to `synthesis.md`, then assemble `synthesis.md = frontmatter + body_path contents` and unlink body file.
- `model_setup`: execute the written `model_setup.py` and capture output.

### Importers of `run_analysis.py` (confirmed via grep)

- `exploration/concept_analysis/scripts/test_memory.py` — imports `load_relevant_memories` (will need update to `from lib.memory import load_relevant_memories`).
- `.project/active/shared-memory-system/plan.md` — documentation only, no code import.

No other script in the repo imports from `run_analysis`.

## Proposed Design

### Module layout

```
exploration/concept_analysis/scripts/
├── run_analysis.py                # CLI: argparse + dispatch + thin handler bodies
├── lib/
│   ├── __init__.py                # empty; explicit imports only
│   ├── paths.py                   # module constants (CONCEPT_ANALYSIS_DIR, TEMPLATES_DIR, …)
│   ├── concepts.py                # load_table, resolve_one, resolve_concepts,
│   │                              #   get_model_path, get_costingfe_mapping, _get_subcategory,
│   │                              #   COSTINGFE_MAPPING, FREEFORM_CONCEPTS, FUEL_MAPPING, FAMILY_KEY_MAP
│   ├── frontmatter.py             # parse_frontmatter, update_frontmatter_field, make_frontmatter
│   ├── state.py                   # get_concept_state, propagate_staleness, _has_downstream_artifacts
│   ├── sources.py                 # find_sources, format_source_list, slugify_source,
│   │                              #   _slugify_text, _slugify_url, find_latest_sources_dir,
│   │                              #   check_duplicate_source, resolve_source_names,
│   │                              #   get_dossier_path, flatten_companion_dir, parse_proposed_actions
│   ├── memory.py                  # load_relevant_memories, find_approved, find_approved_syntheses,
│   │                              #   find_exemplars, format_path_list, _MEMORY_META_RE
│   ├── templating.py              # fill_template
│   ├── claude.py                  # invoke_claude, run_model
│   └── step_runner.py             # run_claude_step (the shared helper)
└── test_memory.py                 # updated import: from lib.memory import load_relevant_memories
```

**Decision on path constants:** `lib/paths.py`. Every other `lib/*.py` module needs at least one path constant, and pulling them into the leaf keeps the import DAG clean (`paths` is imported by everything else; it imports nothing). If we left them in `run_analysis.py`, every lib module would need `from run_analysis import TEMPLATES_DIR`, which is the exact circular-import risk FR-NF-2 warns against.

**Estimated line counts** (after dedup; target is ≤300 lines for each `lib/*.py`, ≤400 lines for `run_analysis.py`):

| File | Rough LOC |
|---|---:|
| `lib/paths.py` | ~40 |
| `lib/concepts.py` | ~180 |
| `lib/frontmatter.py` | ~80 |
| `lib/state.py` | ~100 |
| `lib/sources.py` | ~220 |
| `lib/memory.py` | ~120 |
| `lib/templating.py` | ~45 |
| `lib/claude.py` | ~80 |
| `lib/step_runner.py` | ~110 |
| `run_analysis.py` | ~380–450 (CLI + 14 thinned handlers + dispatch) |
| **Total** | **~1350–1425** |

This comes in under the 2306 original (FR-NF-3) primarily because the ~60-line boilerplate × ~6 deduplicated call sites ≈ 300 lines collapses into one helper.

### Import DAG (acyclic)

```
paths ── (no deps)
frontmatter ── (no deps)
templating ── (no deps)
claude ── paths
concepts ── paths
sources ── paths
memory ── paths
state ── paths, frontmatter
step_runner ── paths, templating, claude
run_analysis.py ── ALL of lib/*
test_memory.py ── lib.memory
```

No module under `lib/` imports from `run_analysis.py`. Import order is validated by `python -c "import lib.<module>"` for each module in isolation (Acceptance Criteria FR-NF-2).

### The shared helper: `run_claude_step`

Lives at `lib/step_runner.py`. Signature (revised to close C1, M1, M2, M3):

```python
from typing import Callable, Literal
from pathlib import Path
import argparse

OutputMode = Literal[
    "stdout_to_file",      # write stdout to output_path (cmd_gap_check)
    "file_with_fallback",  # expect Claude to write output_path; fall back to stdout (cmd_review, cmd_synthesize body_path)
    "file_exists",         # expect Claude to write output_path; no fallback, fail if missing (cmd_model_setup)
    "no_output",           # Claude uses Edit tool; only verify rc==0 (cmd_address_review)
]

def run_claude_step(
    concept: dict,
    *,
    template_name: str,                         # filename under TEMPLATES_DIR
    build_vars: Callable[[dict], dict],         # returns template substitution dict
    prompt_path: Path,                          # where to save the rendered prompt
    output_path: Path | None,                   # artifact expected from Claude (None if no_output)
    label: str,                                 # progress-print label, e.g. "gap-check", "model-setup"
    label_suffix: str = "",                     # optional mid-string suffix, e.g. " (1costingfe)" — inserted
                                                #   after {cid} in BOTH dry-run and progress prints
    args: argparse.Namespace,                   # supplies --dry-run, --timeout, --model, --force
    output_mode: OutputMode = "file_with_fallback",
    skip_if_exists: bool = True,
    skip_message: str | None = None,            # full skip line, minus the "  skip {cid} " prefix;
                                                #   e.g. "(gap_report.md exists, use --force to re-run)".
                                                #   Helper emits f"  skip {cid} {skip_message}" when
                                                #   skip_if_exists triggers. Required if skip_if_exists=True
                                                #   and output_path is not None.
    missing_output_message: str | None = None,  # for file_with_fallback / file_exists: tail of the
                                                #   "FAILED ... — <msg>" line when output is missing.
                                                #   Defaults match current handler wording per mode.
    on_failure_cleanup: Callable[[], None] | None = None,  # e.g. synthesis.md unlink
    post_hook: Callable[[dict, "StepResult"], None] = REQUIRED_POST_HOOK,
) -> "StepResult":
    ...
```

**`post_hook` is mandatory for the success path.** The helper never prints a `" done ..."` line. On `status="done"` the helper returns to the caller, and the post-hook is invoked to emit whatever success format that handler uses. This closes M3: there is now one rule ("helper owns skip + dry-run + failure; post-hook owns success"), not a fragile "default tail when post_hook is None" split. The 2 simple cases (`gap_check`, `model_setup`) pay ~3 lines of trivial post-hook each — acceptable for the clarity win.

**Closing C1 via `label_suffix`.** For `cmd_model_setup` the caller computes `path_label` from the concept before calling the helper and passes `label_suffix=f" ({path_label})"`. The helper inserts it after `{cid}` in both the dry-run and progress prints, producing byte-identical output to the current handler:

```python
# Dry-run print (inside helper):
print(f"  dry-run {cid}{label_suffix}: prompt saved to {prompt_path}")
# Progress print (inside helper):
print(f"  {label} {cid}{label_suffix} ...", end="", flush=True)
```

For the 5 other handlers `label_suffix=""` and these prints are unchanged.

**Closing M1 via `skip_message`.** Each handler's skip message varies in artifact name and suffix wording. Observed verbatim:

| Handler | Current skip line |
|---|---|
| `gap_check` | `  skip {cid} (gap_report.md exists, use --force to re-run)` |
| `model_setup` | `  skip {cid} (model_setup.py exists, use --force)` |
| `review` | `  skip {cid} (review.md exists, use --force to re-run)` |
| `address_review` | n/a (no output-based skip; prereq skips handled by caller before helper call) |
| `synthesize` | `  skip {cid} (synthesis.md exists, use --force to re-run)` |

The helper takes the tail of each as `skip_message` (e.g. `"(gap_report.md exists, use --force to re-run)"`) and emits `f"  skip {cid} {skip_message}"`. Prereq skips ("no analysis.md — run analyze first", "no review.md — run review first", etc.) remain in the caller, **before** the `run_claude_step` call — the helper does not try to own them because their printing sometimes happens before `output_path` is even known.

**Closing M2 via `output_mode="file_exists"`.** Confirmed by reading lines 1432–1434: `cmd_model_setup` expects `model_path.exists()` after the call, with no stdout fallback, and prints `f" FAILED ({elapsed:.0f}s) — Claude did not write {model_path}"` on miss. This is `output_mode="file_exists"` with `missing_output_message=f"Claude did not write {model_path}"` passed by the caller. The helper's failure-print is then:

```python
print(f" FAILED ({elapsed:.0f}s) — {missing_output_message}")
```

The default for `missing_output_message` in `file_with_fallback` mode is `f"no {label} output"` (matches current `cmd_synthesize` wording `"Claude did not write {body_path}"` — implementer passes it explicitly if the default doesn't match exactly; fixture diff catches any miss).

**`StepResult` dataclass** captures everything a post-hook might need:

```python
@dataclass
class StepResult:
    status: Literal["done", "skipped", "failed", "dry_run"]
    stdout: str = ""
    stderr: str = ""
    rc: int = 0
    elapsed: float = 0.0
    output_text: str = ""   # contents of output_path after the call (or stdout for stdout_to_file)
```

**What the helper does, in order** (matches current handler shape exactly):

1. Ensure `output_path.parent` exists (if `output_path is not None`).
2. If `skip_if_exists` and `output_path` and `output_path.exists()` and not `args.force`: print `f"  skip {cid} {skip_message}"`, return `StepResult(status="skipped")`.
3. Call `build_vars(concept)` → dict. Load `TEMPLATES_DIR/template_name`, `fill_template(...)`.
4. Write the filled prompt to `prompt_path`.
5. If `args.dry_run`: print `f"  dry-run {cid}{label_suffix}: prompt saved to {prompt_path}"`, return `StepResult(status="dry_run")`. **This print must be byte-identical to the current handler — matching is verified by fixture diff.**
6. Print `f"  {label} {cid}{label_suffix} ...", end="", flush=True`, record `t0`.
7. `invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model)`.
8. `elapsed = time.time() - t0`.
9. If `rc != 0`: print `f" FAILED ({elapsed:.0f}s, rc={rc})"` + stderr snippet. Call `on_failure_cleanup()` if provided. Return `StepResult(status="failed", ...)`.
10. Resolve output based on `output_mode`:
    - `stdout_to_file`: `output_path.write_text(stdout)`, set `output_text=stdout`.
    - `file_with_fallback`: if `output_path.exists()`, read it into `output_text`. Else if `stdout.strip()`, write stdout to `output_path` and set `output_text=stdout`. Else print `f" FAILED ({elapsed:.0f}s) — {missing_output_message}"`, cleanup, return failed.
    - `file_exists`: if `output_path.exists()`, read it into `output_text`. Else print `f" FAILED ({elapsed:.0f}s) — {missing_output_message}"`, cleanup, return failed. **No stdout fallback.**
    - `no_output`: `output_text = ""`.
11. Call `post_hook(concept, result)`. **Post-hook is mandatory and always owns the success tail print** — the helper never emits `" done ..."`. See M3 resolution above.

### How each handler uses the helper

Every handler keeps its `resolve_concepts` call, the `if not targets: return` guard, and the `for c in targets:` loop. Inside the loop it (a) constructs `output_path`, (b) does any prereq checks that would have caused an early `continue`, (c) calls `run_claude_step(...)`, (d) if `result.status == "done"` runs its distinctive post-hook.

**`cmd_gap_check`** — uses `stdout_to_file`. Trivial post-hook prints the done line (M3: post-hook is mandatory):
```python
def _gap_check_post(c, r):
    print(f" done ({r.elapsed:.0f}s, {len(r.output_text)} chars)")

run_claude_step(
    c,
    template_name="gap_check.md",
    build_vars=lambda c: {...},
    prompt_path=out_dir / "gap_check_prompt.md",
    output_path=out_dir / "gap_report.md",
    label="gap-check",
    args=args,
    output_mode="stdout_to_file",
    skip_message="(gap_report.md exists, use --force to re-run)",
    post_hook=_gap_check_post,
)
```

**`cmd_review`** — uses `file_with_fallback`, post-hook:
```python
def _review_post_hook(c, result):
    # parse review.md for Overall: CLEAN, update analysis.md frontmatter
    review_status = "clean" if re.search(r"\*\*Overall:\*\*\s*CLEAN", result.output_text, re.M) else "has-actions"
    text = analysis_path.read_text(encoding="utf-8")
    text = update_frontmatter_field(text, "Review-Iterations", str(iteration))
    text = update_frontmatter_field(text, "Last-Review", date.today().isoformat())
    text = update_frontmatter_field(text, "Review-Status", review_status)
    analysis_path.write_text(text, encoding="utf-8")
    print(f" done ({result.elapsed:.0f}s, {len(result.output_text)} chars) — {review_status}")
```
Iteration number and `analysis_path` are captured by closure over the loop body. The post-hook signature `(concept, StepResult)` is enough because `cid`/`iteration`/`analysis_path` are closed over.

**`cmd_address_review`** — uses `no_output`, post-hook runs the model and writes `Review-Status: addressed`.

**`cmd_synthesize`** — uses `file_with_fallback` with `output_path=body_path`, `on_failure_cleanup=lambda: synthesis_path.unlink(missing_ok=True)`, post-hook assembles `synthesis.md = frontmatter + body`, unlinks `body_path`, prints the done line.

**`cmd_model_setup`** — uses `output_mode="file_exists"` (confirmed by reading lines 1352–1451; Claude uses the Write tool to produce `model_setup.py`, no stdout fallback). Caller computes `path_label` (`"1costingfe"` or `"free-form"`) from `get_model_path(c)` and passes it as `label_suffix=f" ({path_label})"`. Two templates (`model_setup_costingfe.md` vs `model_setup_freeform.md`) selected by the caller; `build_vars` branches on `path_label` and returns the appropriate dict — the helper stays single-template-per-call. Post-hook:

```python
def _model_setup_post(c, r):
    print(f" done ({r.elapsed:.0f}s, {model_path.stat().st_size} bytes)")  # NB: "bytes", not "chars"
    print(f"    running model ...", end="", flush=True)
    ok, msg = run_model(model_path, out_dir / "model_output.txt")
    if ok:
        lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
        lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
        print(f" ok{lcoe_str}")
    else:
        print(f" FAILED: {msg}")
        print(f"    hint: fix model_setup.py and run: uv run python {model_path}")
```

The `missing_output_message` arg is set to `f"Claude did not write {model_path}"` to match the current wording exactly.

**`cmd_analyze` (cold-start branch only)** — the simple cold-start path (no assess loop) maps cleanly onto `file_with_fallback`. The feedback branch and the assess↔analyze loop are **explicitly out of scope** per spec FR-5 and are left untouched. If the cold-start branch does not fall out cleanly in under ~20 lines of glue, **leave it alone** — #2 will rewrite it anyway. The acceptance criterion requires ≥5 of 8 candidate handlers to use the helper; we have `gap_check`, `review`, `address_review`, `synthesize`, `model_setup` as a solid 5 even if `analyze` and `update_analysis` stay untouched.

**`cmd_update_analysis`** — **leave untouched** per spec edge case note. It has two sequential Claude invocations with a PASS-gate between them. Wedging it into the helper is high-risk for minimal gain; Work Item #2 rewrites this as a Pipeline with an explicit Gate.

**`cmd_add_source`** — not a Claude-invoking handler (calls `agentic-mbse extract` subprocess). Out of scope for FR-3. Stays in `run_analysis.py` unchanged.

**`cmd_approve`** — pure frontmatter mutation, no Claude call. Out of scope for FR-3. Stays unchanged.

**`cmd_list`, `cmd_status`, `cmd_stage1_all`** — composites / pure output. Unchanged.

### Handler coverage summary

| Handler | Uses `run_claude_step`? | Mode |
|---|---|---|
| `cmd_gap_check` | Yes | `stdout_to_file` |
| `cmd_model_setup` | Yes | `file_exists` (confirmed — no stdout fallback) |
| `cmd_review` | Yes | `file_with_fallback` |
| `cmd_address_review` | Yes | `no_output` |
| `cmd_synthesize` | Yes | `file_with_fallback` (body_path) |
| `cmd_analyze` cold-start | Maybe (only if glue <20 lines) | `file_with_fallback` |
| `cmd_analyze` assess loop | **No** (WI #2) | — |
| `cmd_update_analysis` | **No** (WI #2) | — |
| `cmd_add_source` | **No** (not Claude) | — |
| `cmd_approve` | **No** (no prompt) | — |

**Minimum coverage:** 5 handlers. **Expected:** 6. The acceptance criterion (≥5) is met.

## Potential Risks

1. **Closure capture of loop variables in post-hooks.** Python's late-binding closure bug — defining `_post_hook` as a `lambda` inside the `for c in targets:` loop and having it capture `iteration` or `analysis_path` can bite if the loop moves on. **Mitigation:** define post-hooks as nested `def` functions with default-argument capture (`def hook(c, r, _ap=analysis_path, _it=iteration): ...`) or build a partial with `functools.partial`. This warning is also duplicated in the `step_runner.py` module docstring so the next person to add a handler sees it without reading this design doc.
3. **Print-format drift from refactor.** The load-bearing acceptance test is byte-identical fixture diff. Any tiny change to print formatting (an extra space, a different decimal format, a reordered field) blows the diff. **Mitigation:** implement one handler at a time, run the dry-run fixture diff after each, only proceed when clean.
4. **Circular imports during incremental extraction.** If `state.py` is extracted before `frontmatter.py` is ready, or path constants are imported from the wrong place, you can get import-order failures that aren't caught until runtime. **Mitigation:** plan phases in DAG order — `paths.py` first, then leaves (`frontmatter`, `templating`), then mid (`concepts`, `sources`, `memory`, `claude`, `state`), then `step_runner.py`, then handler rewrites.
5. **`test_memory.py` import.** One-line fix but easy to forget. Listed as an explicit step in the plan.
6. **Hidden behavior in the synthesize pre-write / body-assemble flow.** `cmd_synthesize` pre-writes `synthesis.md` with controlled frontmatter BEFORE calling Claude, then Claude writes a body to `body_path`, then the script assembles `synthesis.md = frontmatter + body`. The helper's `output_path` is `body_path`, not `synthesis.md`. On failure, `synthesis.md` must be unlinked. `on_failure_cleanup` is the hook for this.

## Integration Strategy

- Does not touch prompt templates, `knowledge/concept_research/`, or any CLI surface.
- Updates `exploration/concept_analysis/scripts/test_memory.py` imports (one line).
- Unblocks Work Item #2 (stage1 loop refactor) and Work Item #3 (final-stages rescope) — both have specs waiting on this split.
- Does not conflict with `.project/active/autonomous-source-acquisition/` — that spec's integration point is inside the assess↔analyze loop (WI #2 territory) and is unaffected by this mechanical split.

## Validation Approach

Verification is **fixture diff**, not a test suite, because spec FR-NF explicitly declines to introduce a test framework.

### Fixture methodology — state priming

**(Closes m1.)** `resolve_concepts(..., target_state="X")` filters out concepts whose current state already equals or exceeds `X`. If we capture all 8 dry-runs against concept `02` without priming, most commands will print `"No concepts to X."` and never exercise the prompt-building path — producing a hollow fixture that diffs empty for the wrong reason.

Two options considered:

- **(a) Different concepts per command**, chosen to match each target state. Rejected because it couples fixture validity to the specific state of 36 concepts at capture time, and the states drift between sessions.
- **(b) State priming on a single concept**, chosen. Before each capture, `rm` the downstream artifact the command would produce so the concept's state rewinds to the right level. Captured fixtures are tied to one concept (`02`) whose baseline is snapshotted first.

**Concrete priming per command:**

| Command | Prime action before dry-run |
|---|---|
| `gap-check 02 --dry-run` | `rm -f gap_report.md` (under `analyses/02-*/`) |
| `analyze 02 --dry-run` | `rm -f analysis.md` (cold-start branch — leaves `gap_report.md` in place) |
| `model-setup 02 --dry-run` | `rm -f model_setup.py` (requires `analysis.md`) |
| `review 02 --dry-run` | `rm -f review.md` (requires `analysis.md`) |
| `address-review 02 --dry-run` | require pre-existing `review.md` with ≥1 filled `Decision:` field — **do not remove**; copy a known-good one into place from the baseline snapshot |
| `synthesize 02 --dry-run` | `rm -f synthesis.md` (requires `analysis.md` with `Review-Status ∈ {addressed, clean}`) |
| `stage1-all 02 --dry-run` | fresh state — `rm -f analysis.md model_setup.py review.md synthesis.md` |
| `add-source 02 <pdf> --dry-run` | none — dry-run does not mutate |

**Baseline snapshot:** before any of this, `cp -a analyses/02-acoustic-icf /tmp/ra_fixtures/baseline_02` so the pre-refactor captures can restore the concept between commands and the post-refactor run starts from the same baseline. After the full before/after cycle, restore `analyses/02-*` from the baseline so nothing in the working tree changes.

The fixture capture script below automates the prime-capture-restore cycle.

### Pre-refactor fixture capture

Before starting extraction, on the **current** code, capture fixtures for concept `02`:

```bash
# Baseline snapshot + fresh temp dirs
CONCEPT_DIR=$(echo exploration/concept_analysis/analyses/02-*)
mkdir -p /tmp/ra_fixtures/before /tmp/ra_fixtures/baseline_02
cp -a "$CONCEPT_DIR"/. /tmp/ra_fixtures/baseline_02/

restore() { rm -rf "$CONCEPT_DIR"; mkdir -p "$CONCEPT_DIR"; cp -a /tmp/ra_fixtures/baseline_02/. "$CONCEPT_DIR"/; }

capture() {
  local cmd="$1" prime="$2"
  restore
  eval "$prime"
  uv run python exploration/concept_analysis/scripts/run_analysis.py $cmd 02 --dry-run \
    > /tmp/ra_fixtures/before/${cmd// /_}.stdout.txt 2>&1
  # copy whatever prompt files the command produced
  find "$CONCEPT_DIR" -name '*_prompt.md' -newer /tmp/ra_fixtures/baseline_02/. \
    -exec cp {} /tmp/ra_fixtures/before/${cmd// /_}__{} \;
}

capture "gap-check"       "rm -f $CONCEPT_DIR/gap_report.md"
capture "analyze"         "rm -f $CONCEPT_DIR/analysis.md"
capture "model-setup"     "rm -f $CONCEPT_DIR/model_setup.py"
capture "review"          "rm -f $CONCEPT_DIR/review.md"
capture "address-review"  ""   # requires existing review.md from baseline — do not rm
capture "synthesize"      "rm -f $CONCEPT_DIR/synthesis.md"
capture "stage1-all"      "rm -f $CONCEPT_DIR/analysis.md $CONCEPT_DIR/model_setup.py $CONCEPT_DIR/review.md $CONCEPT_DIR/synthesis.md"
capture "add-source 02 /path/to/test.pdf"  ""

restore

# Full status output
uv run python exploration/concept_analysis/scripts/run_analysis.py status \
  > /tmp/ra_fixtures/before/status.stdout.txt 2>&1

# State of every concept (one-shot script)
uv run python -c "
from run_analysis import load_table, get_concept_state
for c in load_table():
    print(c['_id'], get_concept_state(c['_id']))
" > /tmp/ra_fixtures/before/all_states.txt

# Frontmatter round-trip on one real analysis.md
uv run python -c "
from run_analysis import parse_frontmatter, update_frontmatter_field
from pathlib import Path
p = Path('exploration/concept_analysis/analyses/02-acoustic-icf/analysis.md')
text = p.read_text()
fm = parse_frontmatter(p)
# No-op update — round-trip
updated = update_frontmatter_field(text, 'ID', fm.get('ID', '02'))
print('MATCH' if updated == text else 'DIFF')
" > /tmp/ra_fixtures/before/frontmatter_roundtrip.txt
```

### Post-refactor fixture comparison

After each phase (not just at the end), repeat the capture into `/tmp/ra_fixtures/after/` and diff:

```bash
# Precheck: m4 — confirm no /tmp or absolute temp paths snuck into fixtures
grep -rn '/tmp/' /tmp/ra_fixtures/before/ && echo "WARN: temp paths in fixtures — will cause spurious diffs"

diff -r /tmp/ra_fixtures/before/ /tmp/ra_fixtures/after/
```

**Acceptance:** empty diff. The grep precheck ensures there is no noise to "modulo" away — if the precheck finds `/tmp` paths in the captured prompts, investigate before declaring the diff clean. (No current handler constructs paths under `/tmp`, so the grep should find nothing.)

### Line-count verification

```bash
wc -l exploration/concept_analysis/scripts/run_analysis.py exploration/concept_analysis/scripts/lib/*.py
```

- Each `lib/*.py` must be ≤300 lines (FR / AC).
- `run_analysis.py` target ≤400, hard ceiling 500.
- Total across all files must be **less** than 2306 (FR-NF-3).

### Import isolation

```bash
for m in paths concepts frontmatter state sources memory templating claude step_runner; do
  uv run python -c "from exploration.concept_analysis.scripts.lib import $m; print('ok:', $m.__name__)"
done
```

Each must succeed without ImportError.

### Success criteria (from spec, verbatim check)

- [ ] No file exceeds ~400 lines; each `lib/*.py` ≤300
- [ ] 14 subcommands still `--help` cleanly
- [ ] Dry-run fixture diff empty for 8 listed commands
- [ ] Frontmatter round-trip byte-identical
- [ ] `get_concept_state` returns same value for all 36 concepts
- [ ] `status` output byte-identical
- [ ] `ruff` clean on new files (if project uses ruff — check `pyproject.toml`)
- [ ] ≥5 of 8 candidate handlers use `run_claude_step`
- [ ] No `from lib.foo import *`
- [ ] `test_memory.py` imports updated and still runs

---

**Next Step:** After approval → `/_my_plan` to sequence the phased extraction (paths → leaves → mid → step_runner → handler migrations → cleanup), with a fixture-diff checkpoint between each phase.
