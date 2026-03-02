# Revisit Plan: Codegen Chain Spike — Verify Gap Fixes

**Status:** Complete
**Created:** 2026-02-01
**Context:** Fixes implemented in upstream repos:
- `agentic-mbse`: commit `741307268bf0e96981634d2500dfe570752b5424`
- `sysml-codegen`: commit `61aa9071736986db14094eb622dff9bd2e2a104c`

## Source Documents

- **Gap Report:** `.project/reports/codegen-runtime-gaps-2026-02-01-2047.md`
- **Debug Findings:** `.project/active/gap1-default-value-debug/findings.md`
- **Fix Plan:** `.project/active/gap1-default-value-debug/fix-plan.md`
- **Original Spike:** `.project/active/codegen-chain-spike/plan.md`

## Objective

Verify that the three codegen runtime gaps identified in the gap report are fully resolved by the upstream fixes. The chain spike model should go from "requires 3 manual workarounds to run" to "runs cleanly end-to-end with no manual intervention."

**Success criterion:** `execute_pipeline()` runs on freshly-regenerated chain spike output with correct results (`area=50.0`, `total_cost=600.0`, `cost_per_area=12.0`) and zero manual workarounds.

---

## Phase 1: Update Dependencies

### Goal
Ensure fusion-tea uses the fixed versions of both upstream repos.

### Steps

- [x] Verify `agentic-mbse` is at commit `7413072` or later
  ```bash
  cd /home/reid/1cfe/agentic-mbse && git log --oneline -1
  ```
  Result: `7413072 L8 extractability validation: catch non-evaluable design attribute expressions`
- [x] Verify `sysml-codegen` is at commit `61aa907` or later
  ```bash
  cd /home/reid/1cfe/sysml-codegen && git log --oneline -1
  ```
  Result: `61aa907 Fix three codegen runtime gaps for TEAx pipeline execution`
- [x] Re-install both packages into fusion-tea's environment
  ```bash
  cd /home/reid/1cfe/fusion-tea
  uv pip install -e /home/reid/1cfe/agentic-mbse
  uv pip install -e /home/reid/1cfe/sysml-codegen
  ```
  Result: Both installed successfully as editable packages (v0.1.0)

### Gate
Both packages installed at correct commits. `uv pip list | grep -E "agentic-mbse|sysml-codegen"` shows expected versions.

---

## Phase 2: Re-run Codegen

### Goal
Regenerate the chain spike package from scratch using the fixed codegen, replacing all previous generated output.

### Steps

- [x] Delete previous generated output
  ```bash
  rm -rf generated/codegen_chain_spike/
  ```
- [x] Run codegen with verbose output
  ```bash
  cd /home/reid/1cfe/sysml-codegen
  uv run sysml-codegen generate \
      --models /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/ \
      --output /home/reid/1cfe/fusion-tea/generated/codegen_chain_spike/ \
      --package-name chain_spike \
      --verbose
  ```
- [x] Capture exit code — must be 0
  Result: EXIT_CODE=0
- [x] Save verbose output for analysis
  Key observations:
  - `Extracted 6 design attributes from 2 files (filter: '')` — empty filter (fix for Gap 1)
  - `Generated 1 JSON templates from graph` — JSON template generated
  - `Generated 3 TEAx module wrappers` — all modules present
  - No `chain_spike_schemas.py` in output — Gap 3 appears fixed
  - Pipeline file: `pipeline.yaml` (not `chain_spike_pipeline.yaml` — name changed)

### Gate
Codegen exits 0. Generated output directory exists with expected structure.

---

## Phase 3: Verify Gap 1 Fix (Empty JSON → Populated JSON)

### Goal
Confirm `design_params.json` is populated with correct default values from the SysML model.

### Steps

- [x] Inspect generated `inputs/design_params.json`
  ```bash
  cat generated/codegen_chain_spike/inputs/design_params.json
  ```
  Result: JSON contains all 3 fields with correct values.
- [x] Verify 3 required fields are present with correct values:
  ```
  ChainSpikeDesign__spike_design__area_calc__length: 10.0  ✓
  ChainSpikeDesign__spike_design__area_calc__width: 5.0    ✓
  ChainSpikeDesign__spike_design__cost_calc__rate: 12.0    ✓
  ```
- [x] Programmatic assertion:
  ```bash
  uv run python -c "
  import json
  data = json.load(open('generated/codegen_chain_spike/inputs/design_params.json'))
  assert len(data) == 3, f'Expected 3 params, got {len(data)}: {data}'
  assert data['ChainSpikeDesign__spike_design__area_calc__length'] == 10.0
  assert data['ChainSpikeDesign__spike_design__area_calc__width'] == 5.0
  assert data['ChainSpikeDesign__spike_design__cost_calc__rate'] == 12.0
  print('PASS: Gap 1 resolved — design_params.json is correctly populated')
  "
  ```

### Gate
All 3 assertions pass. JSON contains correct values extracted from `design.sysml` attribute defaults.

---

## Phase 4: Verify Gap 2 Fix (Missing RootModel[float] Handler)

### Goal
Confirm codegen generates proper handler registration for `RootModel[float]` exit point types, so no manual router workaround is needed.

### Steps

- [x] Inspect `__init__.py` for `RootModel[float]` or equivalent in `CUSTOM_SCHEMA_TYPES` or handler registrations:
  Result: `CUSTOM_SCHEMA_TYPES = [DesignParams, Float]` — `Float` is `RootModel[float]` from new `primitives.py`
- [x] Check generated registry function for exit point type handling:
  Result: New file `primitives.py` defines `Float = RootModel[float]`, imported in `__init__.py` and included in `CUSTOM_SCHEMA_TYPES`. Module wrappers return `ModuleResult[Float]`.
- [ ] Verify pipeline can be constructed without manual router creation (will be tested in Phase 6)

### Gate
Evidence that `RootModel[float]` is handled in generated code (either via `CUSTOM_SCHEMA_TYPES`, explicit handler registration, or equivalent mechanism).

---

## Phase 5: Verify Gap 3 Fix (Static FusionParams Template)

### Goal
Confirm the static `FusionParams` template is no longer unconditionally copied into the generated package.

### Steps

- [x] Check if `chain_spike_schemas.py` exists:
  Result: **File does not exist.** The static template copy was removed.
- [x] ~~If it exists, verify it does NOT contain `FusionParams` with CATF/MFE fields~~ (N/A — file removed)
- [x] If the file was removed entirely, that's also a valid fix — confirm no references to it remain:
  Result: **Zero matches** for `chain_spike_schemas` or `FusionParams` across all `.py` and `.yaml` files in generated output.

### Gate
No stale `FusionParams` class in the generated output. Either the file is gone, or its content is model-appropriate.

---

## Phase 6: End-to-End Pipeline Execution

### Goal
Execute the pipeline end-to-end using ONLY generated code — no manual workarounds.

### Prerequisites
- [x] Ensure handwritten implementations exist (they should already be there from the original spike):
  Regeneration overwrote all 3 stencils with `raise NotImplementedError`. Restored:
  - `areacalc_impl.py`: `return inputs.length * inputs.width`
  - `costcalc_impl.py`: `return inputs.area * inputs.rate`
  - `summarycalc_impl.py`: `return inputs.cost / inputs.area`

- [x] Ensure package symlink exists:
  ```bash
  ln -sfn codegen_chain_spike generated/chain_spike
  ```

### Attempt 1: Minimal invocation (no manual workarounds)

- [x] Run pipeline using only generated registry and schema types:
  Note: pipeline filename is `pipeline.yaml` (not `chain_spike_pipeline.yaml`)
  ```
  Pipeline completed successfully!
  Outputs: {
    '...area_calc__area': RootModel[float](root=50.0),
    '...cost_calc__total_cost': RootModel[float](root=600.0),
    '...summary__cost_per_area': RootModel[float](root=12.0)
  }
  ```
  **Attempt 1 SUCCEEDED — zero manual workarounds needed.**
- [x] ~~If this fails with a `RootModel[float]` handler error~~ — N/A, Attempt 1 passed.

### Attempt 2: With explicit router (if Attempt 1 fails)

Only run this if Attempt 1 fails on Gap 2:
```bash
PYTHONPATH="generated:$PYTHONPATH" uv run python -c "
from simkit.core.pipeline import execute_pipeline
from simkit.io.output_router import create_output_router_with_json_schemas
from chain_spike import create_chain_spike_registry, CUSTOM_SCHEMA_TYPES

registry = create_chain_spike_registry()
type_names = [t.__name__ for t in CUSTOM_SCHEMA_TYPES] + ['RootModel[float]']
router = create_output_router_with_json_schemas(type_names, include_builtins=True)

result = execute_pipeline(
    spec_path='generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml',
    output_dir='/tmp/chain_spike_revisit',
    registry=registry,
    output_router=router,
    custom_schema_types=CUSTOM_SCHEMA_TYPES,
)

print('Pipeline completed (with manual router).')
print('Outputs:', dict(result.outputs))
"
```

### Verify Outputs

- [x] Confirm correct computation results:
  ```
  area      = 10.0 * 5.0  = 50.0   ✓
  total_cost = 50.0 * 12.0 = 600.0  ✓
  cost_per_area = 600.0 / 50.0 = 12.0  ✓
  ```
- [x] Check output files were written:
  Output dir: `/tmp/chain_spike_revisit/chain-spike-results-d806f3f2/`
  - `...area_calc__area.json` → `50.0`
  - `...cost_calc__total_cost.json` → `600.0`
  - `...summary__cost_per_area.json` → `12.0`
  - `manifest.json` → all 3 artifacts with `produced: true`

### Gate
Pipeline runs to completion with correct outputs. Ideal: Attempt 1 succeeds (all 3 gaps fixed). Acceptable: Attempt 2 succeeds (Gap 2 still needs manual workaround, document status).

---

## Phase 7: Re-run Diagnostic Scripts

### Goal
Verify that the Gap 1 debug diagnostic scripts now produce clean results, confirming the fix at the extraction level.

### Steps

- [x] Re-run path filter diagnostic:
  ```bash
  uv run python .project/active/gap1-default-value-debug/scripts/diag_path_filter.py
  ```
  **Results:**
  - Default filter (`'models/designs'`): still 0 attrs (expected — the fix changed `build_pipeline_context`, not the diagnostic default)
  - Broad filter (`'models/tests'`): 6 attrs — **no longer crashes** (OperatorExpression guard working)
  - Empty filter (`''`): 6 attrs — **no longer crashes** (Change 2 fix confirmed)
  - Specific filter (`'design.sysml'`): 3 attrs with correct defaults

- [x] Re-run classification trace:
  ```bash
  uv run python .project/active/gap1-default-value-debug/scripts/diag_classification.py
  ```
  **Results:**
  - RUN 1 (uses `build_pipeline_context` default): all 3 EPs have non-None defaults (10.0, 5.0, 12.0)
  - RUN 2 (explicit `'design.sysml'` filter): same correct results
  - Script reports "UNEXPECTED: Default run had some non-None values" — this confirms the fix is working (script expected broken behavior)
  - Safety net (`_group_entry_points_via_deriver`) still resolves correctly via fuzzy match

### Gate
Diagnostic scripts confirm the fix at the extraction and classification levels.

---

## Phase 8: Document Results

### Goal
Write a summary of what was verified and what remains.

### Steps

- [x] For each gap, record:
  | Gap | Fixed? | Evidence | Remaining Work |
  |-----|--------|----------|----------------|
  | 1 (empty JSON) | **YES** | Phase 3: JSON has 3 correct values. Phase 7: diagnostics confirm extraction works with empty filter. | None |
  | 2 (RootModel handler) | **YES** | Phase 4: `Float = RootModel[float]` in `primitives.py`, included in `CUSTOM_SCHEMA_TYPES`. Phase 6: Attempt 1 succeeded. | None |
  | 3 (FusionParams template) | **YES** | Phase 5: `chain_spike_schemas.py` no longer generated. Zero references to `FusionParams`. | None |

- [x] Record which attempt succeeded in Phase 6: **Attempt 1 (fully clean, zero manual workarounds)**
- [x] All 3 gaps are fixed: update the gap report status to "Resolved"
- [x] No gaps remain — no follow-up work items needed for these 3 gaps

### Gate
Results documented. Gap report updated. Clear status for each of the 3 gaps.

---

## Risk Notes

1. **Regeneration may overwrite handwritten implementations.** Phase 6 prerequisites check for this and provide restore steps.

2. **Package symlink.** The `codegen_chain_spike/` vs `chain_spike` directory mismatch still requires a symlink. This is a convention issue, not a bug — it's noted in the gap report as an additional finding.

3. **`uv pip install -e` may not pick up changes if pyproject.toml versions didn't bump.** If diagnostic scripts show old behavior after install, try `uv pip install -e --force-reinstall`.
