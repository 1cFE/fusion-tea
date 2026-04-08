# Design: Concept Landscape Context for Analysis Pipeline

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06T10:38:00-07:00
**Updated:** 2026-04-06T10:43:00-07:00
**Branch:** design-space-explore
**Commit:** 46afb62

## Overview

Inject a complete concept landscape (taxonomy + pipeline status + extraction status) inline into analysis and assessment prompts, simplify status codes to reflect the loop-based lifecycle, and track explorer extraction as an orthogonal status flag with staleness propagation.

## Related Artifacts

- **Spec:** `.project/active/concept-landscape-context/spec.md`
- **Research:** `.project/research/20260406-nearest-neighbor-cross-concept-bug.md`

## Research Findings

### Existing Architecture

**State detection** (`lib/state.py:10-57`): `get_concept_state()` returns one of 7 string states by checking filesystem artifacts in priority order: `approved → synthesized → reviewed → model-setup → drafted → gap-checked → not-started`. Appends `*` for downstream staleness.

**Iteration tracking** (`lib/iteration.py:57-95`): `read_loop_state()` scans `iter-N/` dirs, reads `verdict.json` files. Returns `LoopState` with `iterations` list, `last_complete`, `last_incomplete`. `get_iteration_summary()` in `lib/state.py:97-117` formats as `iter-N/VERDICT`.

**State consumers** — all code referencing `drafted` or `model-setup`:
1. `lib/state.py:13-38` — detection logic (source of these strings)
2. `run_analysis.py:103-111` — `state_symbols` dict in `cmd_status()`
3. `run_analysis.py:129-136` — counts display and legend in `cmd_status()`
4. `run_analysis.py:371` — `cmd_model_setup()` uses `target_state="model-setup"` for `--all` filtering
5. `run_analysis.py:412` — `label="model-setup"` for step runner display
6. No other files reference these strings programmatically

**Prompt building** (`run_analysis.py:_build_common_vars()`, lines 267-301): Returns a dict of template variables including `concept_name`, `company`, `dossier_path`, `source_paths`, `approved_analyses`, `exemplar_paths`, `memory_context`. No concept catalog injected.

**Template system** (`lib/templating.py`): Supports `{{variable}}` substitution, `{{#if var}}...{{/if}}` conditionals, `{{@path}}` file includes. The landscape will be a pre-rendered string variable.

**Staleness propagation** (`lib/state.py:60-94`): `propagate_staleness()` marks `model_setup.py`, `review.md`, `synthesis.md`. Two mechanisms: frontmatter `Stale: true` for `.md` files, `# STALE:` comment for `.py` files. No JSON staleness mechanism.

**Explorer data** (`concept_explorer/data/`): JSON files named `{num}.json` (e.g., `01.json`, `07.json`). Currently 6 extracted. `extract_explorer_data.py` reads `analysis.md` + `model_setup.py` only.

**Table structure** (`table.csv`): 38 rows × 23 columns. `load_table()` adds `_id`, `_num`, `_research_id`.

### Patterns Found

- `load_table()` in `lib/concepts.py:137` loads CSV with augmented fields
- `_get_subcategory()` in `lib/concepts.py:123-134` resolves family-specific sub-type column
- `format_path_list()` in `lib/memory.py:52` pattern for markdown list formatting
- `fill_template()` uses `{{#if var}}` — landscape gated by truthiness of the variable
- All `_build_common_vars()` callers have the `concepts` list available in scope

## Proposed Design

### Component 1: Status Code Simplification

**File:** `lib/state.py`

Collapse `drafted` and `model-setup` into `iterating`:

```python
# Before (lines 34-38):
elif model_path.exists():
    state = "model-setup"
else:
    state = "drafted"

# After:
else:
    state = "iterating"
```

Docstring return type: `'not-started' | 'gap-checked' | 'iterating' | 'reviewed' | 'synthesized' | 'approved'`

**All consumers to update:**

1. **`cmd_status()` `state_symbols`** (lines 103-111) — remove `drafted`/`model-setup`, add `iterating` (handled dynamically with iteration count, see Component 3)
2. **`cmd_status()` summary/legend** (lines 129-136) — update labels
3. **`cmd_model_setup()` `target_state`** (line 371) — remove `target_state="model-setup"`. **Behavioral equivalence proof**: The old `target_state="model-setup"` excluded concepts already at model-setup state, i.e., those with `model_setup.py`. The `output_mode="file_exists"` check at line 412 also skips when `model_setup.py` exists. Both gates produce the same skip set, so removing the coarse pre-filter changes no observable behavior — it's just checked later in the per-concept flow instead of up front. Remove `target_state` entirely from this call.
4. **`cmd_model_setup()` label** (line 412) — `label="model-setup"` is a display string, not a state check. Keep as-is (it describes the operation, not the state).

### Component 2: Extraction Status Tracking

**File:** `lib/state.py` — new functions

```python
def get_extraction_state(
    concept_id: str,
    explorer_data_dir: Path | None = None,
) -> str:
    """Check extraction status for a concept.

    Returns: 'not-extracted' | 'extracted' | 'stale'
    """
    if explorer_data_dir is None:
        explorer_data_dir = _default_explorer_data_dir()
    num = _concept_num(concept_id)
    json_path = explorer_data_dir / f"{num}.json"
    if not json_path.exists():
        return "not-extracted"
    stale_path = json_path.with_suffix(".json.stale")
    if stale_path.exists():
        return "stale"
    return "extracted"


def _concept_num(concept_id: str) -> str:
    """Extract numeric prefix: '07' from '07-maglif', '17a' from '17a-...'."""
    m = re.match(r"^(\d+[a-z]?)", concept_id)
    return m.group(1) if m else concept_id


def _default_explorer_data_dir() -> Path:
    """Default path to concept_explorer/data/ relative to ANALYSES_DIR."""
    return ANALYSES_DIR.parent.parent / "concept_explorer" / "data"
```

**Staleness mechanism**: Sidecar file `{num}.json.stale` alongside the JSON. Avoids modifying Pydantic-validated JSON. Contains the reason string.

**Update `propagate_staleness()`** — after existing downstream loop:

```python
# Mark explorer JSON as stale if it exists
explorer_dir = _default_explorer_data_dir()
num = _concept_num(concept_id)
explorer_json = explorer_dir / f"{num}.json"
if explorer_json.exists():
    stale_marker = explorer_json.with_suffix(".json.stale")
    if not stale_marker.exists():
        stale_marker.write_text(reason, encoding="utf-8")
    stale_files.append(f"explorer:{num}.json")
```

**gitignore**: Add `*.stale` to `concept_explorer/data/.gitignore` — these are ephemeral local state.

**Cleanup in `extract_explorer_data.py`**: After successful JSON write, delete the `.stale` sidecar if present. One-line addition.

### Component 3: CLI Status Display Update

**File:** `run_analysis.py` — `cmd_status()` (lines 92-136)

```python
state_symbols = {
    "not-started": "  -",
    "gap-checked": "  G",
    "iterating":   None,  # dynamic: " I{N}"
    "reviewed":    "  R",
    "synthesized": "  S",
    "approved":    "  A",
}

extraction_symbols = {
    "not-extracted": "  ",
    "extracted":     " E",
    "stale":         "E*",
}
```

For `iterating` state, derive `N` from `get_iteration_summary()`:

```python
def _extract_iter_count(iter_summary: str | None) -> int:
    """'iter-3/PASS' → 3, None → 0."""
    if not iter_summary:
        return 0
    m = re.match(r"iter-(\d+)", iter_summary)
    return int(m.group(1)) if m else 0

# NOTE: This regex-parses get_iteration_summary() output. If that format
# changes, this silently returns 0. A cleaner alternative would be adding
# get_iteration_count() -> int to lib/state.py (3-line function reading
# directly from read_loop_state()), usable by both landscape builder and
# cmd_status. Optional improvement — not blocking for this work item.
```

Display format per row: `I{N}` in the State column, plus extraction column:

```
ID                                            Concept Name                             State  Extr  Iterations
01-hts-compact-tokamak                        HTS Compact Tokamak                         A    E   iter-7/PASS
07-maglif                                     MagLIF                                     I5   E*   iter-5/FAIL (2)
22-some-concept                               Some Concept                                G         
```

Summary line: `N approved, N synthesized, N reviewed, N iterating, N gap-checked, N not-started, N extracted (M stale)`

Legend: `A=approved  S=synthesized  R=reviewed  I{N}=iterating(N iterations)  G=gap-checked  -=not-started  E=extracted  E*=stale`

### Component 4: Landscape Builder

**File:** New `lib/landscape.py`

New module justified because it synthesizes data from three sources (table, state, extraction) and is consumed by two prompt templates. Not a good fit for `memory.py` (which handles file-based cross-concept memories).

```python
def build_concept_landscape(
    concepts: list[dict],
    exclude_id: str | None = None,
    analyses_dir: Path = ANALYSES_DIR,
) -> str:
    """Build inline markdown concept landscape for prompt injection.

    Groups by status tier: approved → in-progress → gap-checked → not-started.
    Includes all taxonomy columns plus pipeline status and extraction flag.
    """
```

**Grouping** (FR-2):
1. **Approved** — `get_concept_state() == "approved"` (with or without `*`)
2. **In-progress** — `iterating`, `reviewed`, or `synthesized` (ordered by iteration count descending)
3. **Gap-checked** — `gap-checked`
4. **Not started** — `not-started`

**Column handling**: The spec requires "all 22 columns" (FR-1, out-of-scope section). The CSV has 23 columns including ID and Research ID. Research ID is internal infrastructure, not useful for the agent. Output: 21 taxonomy columns + iteration summary + extraction status = 23 columns per row.

Many columns are `N/A` for concepts outside their family (e.g., `MFE Topology` is `N/A` for IFE concepts). Including them all keeps the data complete per spec, and the agent can ignore irrelevant columns.

**Output format**: One markdown table per tier with a heading. Concepts within each tier sorted by:
- Approved: alphabetical by ID
- In-progress: iteration count descending, then ID
- Gap-checked/Not-started: alphabetical by ID

```markdown
## Concept Landscape (37 concepts)

Use this catalog for nearest-neighbor identification and cross-concept positioning.
Approved concepts have full analyses available; I{N} indicates N completed iterations.

### Approved (primary cross-reference pool)

| ID | Concept Name | Company | Family | MFE Topology | ... | Confidence | Iterations | Extracted |
|----|-------------|---------|--------|-------------|-----|------------|------------|-----------|
| 09 | ... | ... | MFE | Stellarator | ... | high | iter-7/PASS | E |

### In Progress (by maturity)

| ID | Concept Name | ... | Iterations | Extracted |
|----|-------------|-----|------------|-----------|
| 10 | ... | ... | iter-5/FAIL (2) | E* |

### Gap-Checked

| ID | Concept Name | Company | Family | ... | Confidence |
...

### Not Started

| ID | Concept Name | Company | Family | ... | Confidence |
...
```

**Size estimate**: 37 rows × ~300 chars/row (including all columns) ≈ 11KB. Slightly above spec's 8-10KB estimate but acceptable. If it proves too large in practice, the first optimization is dropping columns that are `N/A` for all concepts in a given tier.

### Component 5: Prompt Integration

**File:** `run_analysis.py` — `_build_common_vars()` signature change

Current signature: `def _build_common_vars(concept: dict) -> dict | None:`
New signature: `def _build_common_vars(concept: dict, concepts: list[dict]) -> dict | None:`

Add landscape to the returned dict:

```python
from lib.landscape import build_concept_landscape

landscape = build_concept_landscape(concepts, exclude_id=cid)

return {
    ...existing keys...,
    "concept_landscape": landscape,
}
```

**Callers to update** (all have `concepts` available):
- `cmd_analyze()` → line 254: `common_vars = _build_common_vars(c, concepts)`
- `_apply_external_feedback()` → line 319: `common_vars = _build_common_vars(c, concepts)` — needs `concepts` parameter added to this function too
- Any other callers in `run_analysis.py` that pass `common_vars` to loop or template functions

**Signature change for `_apply_external_feedback()`**: This function is called from `cmd_analyze()` which has the full 38-concept list in scope. The `concepts` parameter passed here must be the **full unfiltered list** from `cmd_analyze()`, not the filtered `targets` list. The landscape needs all concepts to be useful for cross-concept positioning. Updated signature: `_apply_external_feedback(targets, args, feedback, concepts)` where `concepts` is the complete list from `load_table()`.

**File:** `prompt_templates/analysis_v2.md`

Add after the `{{#if memory_context}}` block and before `{{#if cold_start}}`:

```markdown
{{#if concept_landscape}}
## Concept Landscape

The complete taxonomy of all fusion concepts under investigation, grouped by
pipeline maturity. Use this to identify nearest-neighbor concepts for positioning
(Goal 1). Approved concepts have full analyses available for deep reading.
In-progress concepts (I{N}) have N iterations completed.

{{concept_landscape}}
{{/if}}
```

**File:** `prompt_templates/assessment.md`

Add after "Assessment Checklist" include and before "Instructions":

```markdown
{{#if concept_landscape}}
## Concept Landscape

Use this to verify nearest-neighbor selections. Check that named neighbors are
structurally appropriate given the concept's taxonomy properties.

{{concept_landscape}}
{{/if}}
```

### Component 6: Extraction Cleanup in Explorer

**File:** `exploration/concept_explorer/extract_explorer_data.py`

After successful JSON write per concept, delete the stale sidecar:

```python
# After writing {num}.json successfully:
stale_marker = data_dir / f"{num}.json.stale"
if stale_marker.exists():
    stale_marker.unlink()
```

## Potential Risks

1. **Prompt size (~11KB addition)**: Largest single context addition to prompts. Acceptable per spec budget. If too large in practice, drop N/A-heavy columns per tier as first optimization.

2. **`_build_common_vars` signature change**: All callers need updating. Limited blast radius — only `cmd_analyze()` and `_apply_external_feedback()` call it directly, and both have `concepts` in scope.

3. **Explorer data path coupling**: `propagate_staleness()` now knows about `concept_explorer/data/`. Minimal coupling (path knowledge only, no explorer code imports). Spec explicitly acknowledges this.

4. **`cmd_model_setup` target_state removal**: With `target_state` removed, `--all` no longer pre-filters. But the per-concept `output_mode="file_exists"` check at line 412 already handles skipping, so behavior is unchanged — just checked later in the flow.

5. **Pre-loop era concepts**: Concepts with `analysis.md` but no `iter-*/` dirs get `iteration_summary=None`, showing as `I0`. Correctly represents "has analysis, no loop iterations" per spec edge case.

## Integration Strategy

- The landscape **complements** the existing `approved_analyses` file-path list (FR-8). Landscape = catalog for positioning. Approved analyses = file paths for deep reading.
- `lib/landscape.py` depends on `lib/state` and `lib/concepts` — clean dependency direction (no circular imports).
- `propagate_staleness()` addition is backward-compatible — the sidecar mechanism is additive.
- `extract_explorer_data.py` cleanup is a one-line defensive deletion.

## Validation Approach

1. **Status display**: Run `cmd_status` before and after — verify `I{N}` replaces `D`/`M`, extraction column present
2. **Consumer audit**: `grep -r "drafted\|model-setup" exploration/concept_analysis/scripts/` — zero hits in code (comments/docstrings allowed). Note: `resolve_concepts()` in `lib/concepts.py` is safe — it's a parameterized comparator that filters by whatever states are passed to it, not a hardcoded consumer of `drafted`/`model-setup`.
3. **Dry-run prompt**: `uv run python run_analysis.py analyze --dry-run 01` — saved prompt contains landscape with 37 concepts grouped by tier
4. **Assessment prompt**: Similar dry-run for review — verify landscape appears
5. **Staleness propagation**: Call `propagate_staleness("01", "test")` — verify `.stale` sidecar appears in `concept_explorer/data/`
6. **Extraction cleanup**: Run `extract_explorer_data.py --concept 01` — verify `.stale` sidecar deleted
7. **Size check**: Measure landscape string length — should be ≤12KB

---

Next Step: After approval → `/_my_plan` → `/_my_implement`
