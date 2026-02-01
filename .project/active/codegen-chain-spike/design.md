# Design: Codegen CalcUsage-Chain Spike

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-01 20:19:04 UTC
**Branch:** visualization

## Overview

Create a minimal 3-CalcDef chain model, run sysml-codegen on it, and evaluate whether the generated pipeline YAML correctly discovers all CalcUsages, wires inter-module dependencies, and orders modules topologically.

## Related Artifacts

- **Spec:** `.project/active/codegen-chain-spike/spec.md`
- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Item 2)
- **Reference chain pattern:** `models/tests/solar_battery/design.sysml:68-97`
- **Codegen source:** `/home/reid/1cfe/sysml-codegen/`

## Research Findings

### Codegen Has No CalcUsage Test Coverage

The existing codegen test fixtures (`/home/reid/1cfe/sysml-codegen/tests/fixtures/sample_model/`) contain only CalcDef definitions — no CalcUsages at all. The integration test (`test_full_pipeline.py:13-36`) exercises directory structure and file generation but never runs chain resolution through the graph builder. This means:

- The `CHAIN` binding type in `usage_extractor.py:291-302` has plumbing but is untested via codegen's own test suite
- The output catalog builder in `graph_builder.py:128-176` has never mapped `instance.output` keys
- The topological sort in `dependency_backtracker.py:700-780` has never ordered a real DAG
- The pipeline YAML wiring for `module_output` sources has never been generated

This confirms the spike provides genuine risk reduction — we're testing a code path that has never been exercised end-to-end.

### Chain Binding Flow (How It Should Work)

Based on code analysis of the codegen pipeline:

1. **Extraction** (`usage_extractor.py`): When a CalcUsage has `in param = other_calc.output`, the parser detects a `FeatureChainExpression` and creates a `BindingInfo` with `binding_type=CHAIN`, `source_path="other_calc.output"`
2. **Backtracking** (`dependency_backtracker.py`): Resolves the chain binding to a `BindingResolution` with `resolution_type=MODULE_OUTPUT` and `producer_channel="other_calc__output"`
3. **Graph building** (`graph_builder.py`): Builds an output catalog mapping `"instance.output"` → `(module_type, channel_name, field_name)`, then wires each module's inputs to either upstream channels or entry points
4. **YAML generation** (`pipeline.py`): Renders modules with `source: channel_name.root` (single-output) or `source: channel_name` (multi-output) for inter-module wires

### Minimal Model Requirements

From the solar battery reference pattern (`design.sysml:68-97`), the minimal chain needs:

- A **library file** with CalcDef declarations (in/out attributes)
- A **design file** with a `part` containing CalcUsage instances using dot-notation bindings
- At least one CalcUsage consuming another's output (`in param = instance.output`)
- At least one entry-point parameter (unbound, resolved from a part attribute)

The codegen CLI expects model files in a directory and invokes via:
```
sysml-codegen generate --models <dir> --output <dir> --package-name <name>
```

### SysML v2 Syntax for Chain Pattern

From the solar battery model, the minimal syntax is:

```sysml
// Library: CalcDef with in/out
calc def MyCalc {
    in attribute x : Real;
    out attribute y : Real = x * 2.0;
}

// Design: CalcUsage with chain binding
part my_design {
    attribute param : Real = 5.0;
    calc first : FirstCalc { in x = param; }
    calc second : SecondCalc { in x = first.y; }  // chain
}
```

## Proposed Design

### Component 1: Minimal Chain Model

**Location:** `models/tests/codegen_chain_spike/`

Two files, exercising specific codegen capabilities:

#### `library.sysml` (~25 lines)

Three CalcDefs forming a diamond-ish dependency:

| CalcDef | Inputs | Outputs | Tests |
|---------|--------|---------|-------|
| `AreaCalc` | `length : Real`, `width : Real` | `area : Real` = length * width | Single-output, entry-point-only inputs |
| `CostCalc` | `area : Real`, `rate : Real` | `total_cost : Real` = area * rate | Single-output, **one chain input** + one entry point |
| `SummaryCalc` | `area : Real`, `cost : Real` | `cost_per_area : Real` = cost / area | Single-output, **two chain inputs** from different calcs |

This structure tests:
- **Linear chain**: AreaCalc → CostCalc (one output feeds one input)
- **Fan-in**: AreaCalc + CostCalc → SummaryCalc (two upstream calcs feed one downstream)
- **Diamond**: AreaCalc's output is consumed by both CostCalc and SummaryCalc
- **Mixed input types**: CostCalc has both a chain input and an entry-point input
- **Topological ordering**: SummaryCalc must come after both AreaCalc and CostCalc

Domain is deliberately trivial (area/cost) to keep focus on the chain mechanism.

```
AreaCalc ──→ CostCalc ──→ SummaryCalc
    └────────────────────→
```

#### `design.sysml` (~25 lines)

A part definition with:
- Three entry-point attributes (`length`, `width`, `rate`) bound to literal values
- Three CalcUsages with bindings:
  - `area_calc` binds inputs to attributes (REFERENCE type)
  - `cost_calc` binds `area` to `area_calc.area` (CHAIN type) and `rate` to attribute (REFERENCE type)
  - `summary` binds `area` to `area_calc.area` and `cost` to `cost_calc.total_cost` (both CHAIN type)

```sysml
package ChainSpikeDesign {
    private import ScalarValues::Real;
    private import ChainSpikeLibrary::*;

    part spike_design {
        // Entry-point attributes
        attribute length : Real = 10.0;
        attribute width : Real = 5.0;
        attribute rate : Real = 12.0;

        // Calc A: entry-point-only inputs
        calc area_calc : AreaCalc {
            in length = length;
            in width = width;
        }

        // Calc B: one chain input (area_calc.area) + one entry point (rate)
        calc cost_calc : CostCalc {
            in area = area_calc.area;
            in rate = rate;
        }

        // Calc C: two chain inputs from different upstream calcs
        calc summary : SummaryCalc {
            in area = area_calc.area;
            in cost = cost_calc.total_cost;
        }
    }
}
```

Package name should be distinct (`ChainSpikeDesign` / `ChainSpikeLibrary`) to avoid collisions with other test models.

### Component 2: Codegen Execution

**Invocation:**
```bash
cd /home/reid/1cfe/sysml-codegen && \
uv run sysml-codegen generate \
  --models /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike \
  --output /home/reid/1cfe/fusion-tea/generated/codegen_chain_spike \
  --package-name chain_spike \
  --pipeline-name chain_spike_pipeline \
  --verbose
```

Run from the sysml-codegen directory so its `pyproject.toml` is active.

### Component 3: Evaluation Checklist

Evaluate codegen output against these criteria, in pipeline order:

**Stage 1 — Extraction:**
- Does codegen discover all 3 CalcUsages? (check verbose output or generated module count)
- Are binding types correct? (CHAIN for dot-notation, REFERENCE for attributes)

**Stage 2 — Graph Building:**
- Does the output catalog contain entries for all calc outputs? (`area_calc.area`, `cost_calc.total_cost`)
- Are chain bindings resolved to `MODULE_OUTPUT` resolution type?
- Are entry-point bindings resolved to `ENTRY_POINT` resolution type?

**Stage 3 — Pipeline YAML (`generated/codegen_chain_spike/pipelines/chain_spike_pipeline.yaml`):**
- Are all 3 modules present?
- Is `area_calc` before both `cost_calc` and `summary` in module ordering?
- Is `cost_calc` before `summary`?
- Does `cost_calc`'s `area` input wire to `area_calc__area` channel?
- Does `summary`'s `area` input wire to `area_calc__area` channel?
- Does `summary`'s `cost` input wire to `cost_calc__total_cost` channel?
- Are entry-point inputs (`length`, `width`, `rate`) wired to parameter groups?

**Stage 4 — Generated Code Structure:**
- Do 3 module wrappers exist in `modules/`?
- Do 3 implementation stencils exist in `handwritten/`?
- Does `__init__.py` have a registry function?

### Component 4: Findings Document

**Location:** Written as a section in the spike findings (can be appended to this design doc or a separate file in `.project/active/codegen-chain-spike/`).

Structure:
```
## Spike Results

### Go/No-Go: [GO | NO-GO | PARTIAL]

### What Works
- [bullet list of passing checks]

### What Doesn't Work (if any)
- [bullet list of failures with description]
- [estimated fix scope for each]

### Implications for Items 4-5
- [what this means for the solar battery codegen run]
```

## Potential Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Model doesn't compile (syside syntax issues) | Low | Use exact patterns from solar battery `design.sysml` |
| Codegen crashes on chain bindings | Medium | This is exactly what we're testing — document and scope the fix |
| Codegen discovers CalcUsages but misorders them | Low | Topological sort exists in code; diamond pattern exercises it |
| Pipeline YAML has wrong channel names | Medium | Compare generated names against output catalog format in `graph_builder.py:128-176` |

## Integration Strategy

This spike is standalone — no integration with existing code. The model lives in `models/tests/codegen_chain_spike/` and generated output in `generated/codegen_chain_spike/`. Neither directory affects other models or tests.

The findings directly inform whether Items 4-5 can proceed as planned or need workarounds.

## Validation Approach

1. **Model compiles:** `uv run syside check models/tests/codegen_chain_spike/` exits 0
2. **Codegen runs:** exit code 0, no errors in output
3. **Manual inspection:** of pipeline YAML against the evaluation checklist above
4. **Go/no-go documented:** with specific evidence

No automated tests needed — this is an observational spike.

---

## Spike Results

### Go/No-Go: GO

All 4 evaluation stages passed with zero failures. Codegen correctly handles CalcUsage chains end-to-end.

### What Works

**Stage 1 — Extraction (PASS):**
- All 3 CalcUsages discovered (verbose: "Extracted 3 calculation definitions", "Built computation graph with 3 modules")
- Binding types correctly distinguished — CHAIN for dot-notation (`area_calc.area`, `cost_calc.total_cost`), REFERENCE for attribute bindings (`length`, `width`, `rate`)

**Stage 2 — Graph Building (PASS):**
- Output catalog contains entries for both calc outputs: `ChainSpikeDesign__spike_design__area_calc__area`, `ChainSpikeDesign__spike_design__cost_calc__total_cost`
- Chain bindings resolved to MODULE_OUTPUT — evidenced by inter-module channel wiring in YAML
- Entry-point bindings resolved to ENTRY_POINT — evidenced by `design_params.*` wiring in YAML
- Diamond dependency handled correctly — `area_calc.area` consumed by both `cost_calc` and `summary`

**Stage 3 — Pipeline YAML (PASS):**
- All 3 modules present: `chainspikedesign__spike_design__area_calc`, `chainspikedesign__spike_design__cost_calc`, `chainspikedesign__spike_design__summary`
- Topological order correct: area_calc (line 19) → cost_calc (line 28) → summary (line 37)
- `cost_calc.area` input wires to `ChainSpikeDesign__spike_design__area_calc__area.root` — correct
- `summary.area` input wires to `ChainSpikeDesign__spike_design__area_calc__area.root` — correct (diamond fan-out)
- `summary.cost` input wires to `ChainSpikeDesign__spike_design__cost_calc__total_cost.root` — correct
- Entry-point inputs (`length`, `width`, `rate`) wire to `design_params.*` parameter group — correct
- Channel naming convention: `{Package}__{part}__{calc}__{output}` with `.root` suffix for single-output modules

**Stage 4 — Generated Code Structure (PASS):**
- 3 module wrappers: `modules/chainspikelibrary/areacalc.py`, `costcalc.py`, `summarycalc.py`
- 3 implementation stencils: `handwritten/chainspikelibrary/areacalc_impl.py`, `costcalc_impl.py`, `summarycalc_impl.py`
- `__init__.py` has `create_chain_spike_registry()` registering all 3 modules with namespaced module types
- Module wrappers import from handwritten stencils and delegate to `run_*` functions
- Exit point captures all 3 calc outputs to JSON files

### What Doesn't Work

Nothing. All checklist items passed.

### Implications for Items 4-5

- **Items 4-5 can proceed as planned.** The solar+battery model's 5-CalcUsage chain (EnergyProduction → AnnualizedOM/Fuel/Financial → LCOE) uses the same chain binding pattern exercised here.
- **No codegen fixes needed.** The CHAIN binding type, output catalog, topological sort, and pipeline YAML wiring all work correctly out of the box.
- **Channel naming is predictable:** `{Package}__{part}__{calc}__{output}` — this will produce longer names for the solar battery model (e.g., `SolarBatteryDesign__solar_battery_plant__annualized_financial__annualized_capital_cost`) but should work identically.
- **Diamond dependencies work:** The solar battery LCOE calc consuming outputs from 3 upstream calcs is analogous to our SummaryCalc consuming from 2 — codegen handles fan-in correctly.
- **Parameter groups derive correctly:** All 6 binding-traced attributes were collected into a single `DesignParams` group, matching the pattern Items 4-5 need.

---

**Next Step:** Items 4-5 can proceed with confidence. No blockers identified.
