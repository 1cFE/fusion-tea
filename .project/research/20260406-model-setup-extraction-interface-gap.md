# Research: model_setup.py ↔ Explorer Extraction Interface Gap

**Date**: 2026-04-06
**Context**: After merging the concept-explorer branch, extraction fails for 5 of 11 concepts with 2+ iterations. The analysis pipeline and the explorer extraction script have incompatible assumptions about what `model_setup.py` looks like.

---

## What the Analysis Pipeline Produces

The pipeline generates `model_setup.py` via LLM (Claude) using two prompt templates:

- **`model_setup_costingfe.md`** — for concepts that map to a `costingfe.CostModel` variant (tokamak, stellarator, IFE, etc.)
- **`model_setup_freeform.md`** — for concepts that don't map to any costingfe archetype

### costingfe template instructions

The prompt tells the LLM to write a script with this structure:
1. Docstring with modeling rationale
2. Imports and `model = CostModel(...)` creation
3. Plant configuration constants
4. `model.forward()` call with parameters and cost overrides
5. Results printing (LCOE, CAS breakdown)
6. Sensitivity analysis via `model.sensitivity()`

The prompt says to call `model.forward()` and print results. It does **not** mandate that the return value be assigned to a variable called `result`. The LLM follows convention most of the time, but is free to use any name.

### freeform template instructions

The prompt tells the LLM to write a self-contained script (no external dependencies) with:
- A `@dataclass` for plant parameters
- Five `_compute_*()` methods
- A `main()` function that creates the dataclass, runs the computation, and prints results

There is **no module-level `model` or `result`** by design. Everything lives inside functions.

### Post-generation validation

The pipeline validates model_setup.py by **executing it** and checking:
1. Exit code == 0
2. stdout is not empty
3. stdout contains the string "LCOE" (case-insensitive)

That's it. No check for module-level variable names, no check for `model` or `result` existence, no static analysis. If the script runs and prints an LCOE, the pipeline considers it valid.

### What actually gets generated (survey of all 17 concepts with model files)

| Pattern | Concepts | `model =` at module level | `result =` at module level |
|---------|----------|---------------------------|---------------------------|
| Conforming costingfe | 01, 03, 04, 05, 06, 07, 08, 10, 11, 14 | Yes | Yes |
| Multi-scenario costingfe | 09, 17a | Yes | No (`result_h4true`, `result_noak`, etc.) |
| Anomalous costingfe | 28 | Yes | No (results in local variables: `r_base`, `ref_base`) |
| Freeform (no costingfe) | 02, 12, 15, 22 | No | No (everything inside `main()`) |

10 of 14 costingfe concepts conform. 3 costingfe concepts use variant naming. All 4 freeform concepts have no module-level variables at all.

---

## What the Explorer Extraction Expects

The extraction script (`extract_explorer_data.py`) has two pathways:

### costingfe pathway (`extract_costingfe()`)

Triggered when `model_setup.py` exists in the concept directory. Does this:

```python
module = _load_module(model_setup_path)
model = getattr(module, "model", None)
result = getattr(module, "result", None)
if model is None or result is None:
    raise ExtractionError(
        f"{concept_id}: model_setup.py must define module-level 'model' and 'result'"
    )
```

Then it calls:
- `model.sensitivity(result.params)` to get elasticity data
- `dataclasses.asdict(result)` to flatten the result into a dict
- Constructs `CostModelData` from `result.costs`, `result.power_table`, `result.cas22_detail`, `result.overridden`, `result.params`

The server's `/api/compute` endpoint has the same hard requirement — it loads the module, grabs `model` and `result`, and uses `result.params` as the baseline for slider recomputation.

### standalone pathway (`extract_standalone()`)

Triggered when `model_setup.py` does NOT exist (only `analysis.md`). Looks for any `.py` file with a `to_explorer_dict()` function. Otherwise produces `ConceptData` with `cost_model=None`.

### The gap

The extraction script's branching logic is: **if `model_setup.py` exists → costingfe pathway → must have `model` and `result`**. There is no middle ground. A freeform `model_setup.py` (like concepts 02, 12, 15, 22) hits the costingfe pathway and immediately fails because it has no module-level `model`.

Similarly, a multi-scenario costingfe script (like 09, 17a) has `model` but not a bare `result` — it has `result_h4true`, `result_noak`, etc.

### Extraction results for all 11 concepts with 2+ iterations

| Concept | Extraction | Why |
|---------|-----------|-----|
| 01 — HTS Compact Tokamak | Success | Has `model` + `result` at module level |
| 07 — MagLIF | Success | Has `model` + `result` at module level |
| 08 — FRC w/ Direct Conversion | Success | Has `model` + `result` at module level |
| 10 — Large-Scale Stellarator | Success | Has `model` + `result` at module level |
| 14 — Magnetized Target Fusion | Success | Has `model` + `result` at module level |
| 28 — HTS Tokamak Full-HTS | Success | Has `model` + `result` (latest iteration conforms) |
| 09 — QI Stellarator HTS | **FAIL** | `model` exists, but `result` is `result_h4true` / `result_h4false` / `result_h2a` |
| 12 — Levitated Dipole | **FAIL** | Freeform — no `model` or `result` at module level |
| 15 — Sheared-Flow Z-Pinch | **FAIL** | Freeform — no `model` or `result` at module level |
| 17a — Laser ICF Hybrid Drive | **FAIL** | `model` exists, but `result` is `result_noak` / `result_steam` / `result_foak` / etc. |
| 22 — Projectile ICF | **FAIL** | Freeform — no `model` or `result` at module level |

---

## How This Gap Was Missed

1. **The explorer branch was developed against early concepts.** The architecture survey (Appendix B of the design doc) examined 8 concepts. All 6 costingfe ones at that time used `model` + `result`. The convention hadn't been violated yet.

2. **data/ was gitignored on both branches.** No extracted JSON was ever committed before the merge. The merge spec verified 3 specific interface gaps (CAS22 keys, extraction paths, Playwright) but extraction was never actually run against the full concept set.

3. **The pipeline has no knowledge of the extractor.** The LLM prompt templates don't mention the explorer, extraction, or the `model`/`result` naming requirement. The pipeline validates by execution only (does it run? does it print LCOE?).

4. **Multi-scenario concepts emerged after the survey.** Concepts 09 and 17a were analyzed later and naturally produced multiple `result_*` variables because the analysis called for scenario comparison. The LLM chose semantically meaningful names.

5. **The server.py audit almost caught it.** It flagged that `getattr(module, "model")` has "no validation that the dynamically-loaded module conforms to any expected interface." But this was framed as a robustness concern and no action was taken.

---

## Options for Closing the Gap

### Option A: Enforce naming convention in the pipeline

Add a post-generation validation step that checks `model_setup.py` defines `model` and `result` at module level. If multi-scenario, require the script to also assign `result = result_<primary>` as an alias for the "reference case."

**Pros:**
- No changes to extraction or explorer code
- Convention is simple and LLM-enforceable (add it to the prompt template)
- Existing conforming concepts keep working

**Cons:**
- Requires re-running pipeline for all 5 failing concepts
- Forces multi-scenario scripts into a single "primary" result, losing the other scenarios in the explorer
- Freeform concepts would need a compatibility shim or a separate code path
- Fragile: the LLM might still drift on future concepts

### Option B: Make the extractor discover what's available

Change `extract_costingfe()` to scan the loaded module for costingfe objects instead of hardcoding names:
- Find `model` by type: `isinstance(obj, CostModel)`
- Find `result` by type: look for dataclass instances with `.costs`, `.power_table`, etc.
- For multi-scenario: find all `result_*` variables matching the type, extract the first (or largest plant) as primary

**Pros:**
- Works with existing model_setup.py files without re-running the pipeline
- Handles naming drift gracefully
- Could support multi-scenario display in the future

**Cons:**
- More complex extraction logic
- Type-based discovery is fragile if costingfe changes its class hierarchy
- Doesn't help freeform concepts (still no `CostModel` to find)

### Option C: Require an explicit export contract

Define a lightweight protocol that model_setup.py must implement — a dict or function that the extractor calls:

```python
# At the bottom of every model_setup.py:
__explorer__ = {
    "model": model,
    "result": result,          # or result_noak, or whatever the primary case is
    "scenarios": {             # optional
        "noak": result_noak,
        "foak": result_foak,
    }
}
```

The extractor reads `__explorer__` instead of hardcoding `model`/`result`.

**Pros:**
- Explicit contract — no guessing
- Supports multi-scenario natively
- Pipeline prompt template can mandate it
- Easy to validate post-generation (`__explorer__` must exist and have required keys)

**Cons:**
- Requires updating all existing model_setup.py files (17 concepts)
- One more thing for the LLM to get right
- More complex than Option A for the common single-result case

### Option D: Fix it at both ends (recommended)

Combine pipeline enforcement with extractor resilience:

1. **Pipeline side**: Add `result = model.forward(...)` as an explicit requirement in the prompt template. For multi-scenario scripts, require the primary/reference case to be assigned to `result` (other scenarios can use any name). Add a post-generation check that `result` exists at module level.

2. **Extractor side**: Add a fallback for the costingfe pathway — if `result` is missing, scan for `result_*` variables and pick the first one (with a warning). If `model` is missing, fall through to standalone pathway instead of erroring.

3. **Freeform concepts**: Change the branching logic. Instead of "model_setup.py exists → costingfe pathway", check whether the module actually imports from costingfe. If not, use the standalone pathway regardless of filename.

**Pros:**
- Works with existing files (extractor fallback)
- Prevents future drift (pipeline enforcement)
- Freeform concepts handled correctly
- No breaking changes to working concepts

**Cons:**
- Changes in two places
- Fallback logic adds complexity to extraction

### Option E: Do nothing, fix the 5 scripts manually

Edit the 5 failing model_setup.py files by hand to add `result = ...` at module level. For multi-scenario scripts, pick the reference case.

**Pros:**
- Fastest fix
- No code changes to pipeline or extractor

**Cons:**
- Manual edits get overwritten next time the pipeline re-generates model_setup.py
- Doesn't prevent the same problem on future concepts
- Doesn't address the root cause
