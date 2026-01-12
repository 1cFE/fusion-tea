---
date: 2026-01-12T05:58:07-08:00
researcher: Claude
topic: "Multiplicity Cost Rollup - SOLUTION FOUND"
tags: [research, cost-modeling, sysmlv2, multiplicity, sum, NumericalFunctions, VALIDATED]
status: complete
last_updated: 2026-01-12
severity: RESOLVED
---

# Research: Multiplicity Cost Rollup - SOLUTION FOUND

**Date**: 2026-01-12 05:58 PST (Updated 06:15 PST)
**Researcher**: Claude
**Research Type**: Gap Analysis / De-Risking → **RESOLVED**
**Triggered By**: Coffee maker demo model review

## Executive Summary

**✅ SOLUTION FOUND**: `NumericalFunctions::sum` exists and works! The prior research reports and demo implementation **failed to import** the function from the standard library.

**Root Cause of Confusion**: The agent team:
1. Tried `sum()` without importing it → "No Type named 'sum' found"
2. Concluded `sum()` doesn't exist → **WRONG**
3. Never searched the standard library or official documentation

**Correct Pattern**:
```sysml
private import NumericalFunctions::sum;

part def Assembly {
    part child : Component [N];
    :>> capital_cost = sum(child.capital_cost);  // WORKS!
}
```

**Impact**: The coffee maker demo must be fixed to use this pattern. All prior workaround recommendations are obsolete.

---

## The Solution

### Official Standard Library Functions

From `/syside/sysml.library/Kernel Libraries/Kernel Function Library/NumericalFunctions.kerml`:

```kerml
abstract function sum { in collection: NumericalValue[0..*]; return : NumericalValue[1]; }
abstract function product { in collection: NumericalValue[0..*]; return : NumericalValue[1]; }
```

### Validated Pattern

Tested and passing with `syside check`:

```sysml
package CostRollupPattern {
    private import ScalarValues::Real;
    private import NumericalFunctions::sum;  // ← THE KEY IMPORT

    part def 'Costed Component' {
        attribute capital_cost : Real;
    }

    part def 'Brewing System' :> 'Costed Component' {
        part heater : 'Heating Element' [2];

        // AUTOMATIC AGGREGATION - works for any multiplicity!
        :>> capital_cost = sum(heater.capital_cost);
    }
}
```

### Test Results

| Test | Import | Result |
|------|--------|--------|
| `sum(child.capital_cost)` | None | ❌ "No Type named 'sum' found" |
| `sum(child.capital_cost)` | `NumericalFunctions::sum` | ✅ **WORKS** |

### Other Available Functions

From the standard library:

| Package | Functions |
|---------|-----------|
| `NumericalFunctions` | `sum`, `product`, `abs`, `max`, `min`, `isZero`, `isUnit` |
| `SequenceFunctions` | `size`, `isEmpty`, `notEmpty`, `includes`, `excludes`, `head`, `tail`, `last` |
| `CollectionFunctions` | `size`, `isEmpty`, `notEmpty`, `contains`, `head`, `tail`, `last`, `#` |

---

## The Original Problem (Now Resolved)

### What Was Found in the Coffee Maker Demo

In `models/tests/coffee_maker/library.sysml:407-414`:

```sysml
// For assembly aggregation with multiplicity, we need to handle heater[2]
// The heater.capital_cost reference accesses the array
// For now, we express 2x heater cost explicitly in the design file
// This is a known pattern - multiplicity handling varies by tooling
attribute heater_total_cost : Real;
attribute heater_total_material : Real;
attribute heater_total_fab : Real;
attribute heater_total_install : Real;
```

In `models/tests/coffee_maker/design.sysml:30-36`:

```sysml
// Bind the heater totals for 2 heaters
// Each heater: material=7.50, fab=4.50, install=1.125, total=13.125
// Two heaters: material=15.0, fab=9.0, install=2.25, total=26.25
:>> heater_total_cost = 26.25;      // ← HARDCODED!
:>> heater_total_material = 15.0;   // ← HARDCODED!
:>> heater_total_fab = 9.0;         // ← HARDCODED!
:>> heater_total_install = 2.25;    // ← HARDCODED!
```

**This is broken**: If `HeatingElementCostCalc` parameters change, these values become stale.

---

## Empirical Testing Results

### Test 1: `sum()` Function

**Test File**: `models/tests/multiplicity_sum_test.sysml`

```sysml
part def 'Test Assembly Direct Sum' {
    part child : 'Simple Component' [3];
    attribute total_cost : Real = sum(child.capital_cost);
}
```

**Result**: ❌ FAILS

```
error (reference-error): No Type named 'sum' found.
error (invocation-expression-instantiated-type): Invocation expression must invoke a `Behavior`
```

**Conclusion**: `sum()` does NOT exist in SysML v2 standard library or syside implementation.

---

### Test 2: Explicit Indexing with `#()`

**Test File**: `models/tests/multiplicity_alternatives_test.sysml`

```sysml
part def 'Test Explicit Index' {
    part child : 'Simple Component' [2];

    attribute cost_1 : Real = child#(1).capital_cost;
    attribute cost_2 : Real = child#(2).capital_cost;
    attribute total_cost : Real = cost_1 + cost_2;
}
```

**Result**: ✅ PARSES (warnings only, no errors)

**Conclusion**: Explicit indexing works but requires knowing the exact count at definition time.

---

### Test 3: Named Individual Parts

```sysml
part def 'Test Named Parts' {
    part child_1 : 'Simple Component';
    part child_2 : 'Simple Component';

    attribute total_cost : Real = child_1.capital_cost + child_2.capital_cost;
}
```

**Result**: ✅ WORKS

**Conclusion**: Works perfectly but doesn't scale and defeats the purpose of multiplicity.

---

### Test 4: Calc with Unit Cost × Quantity

```sysml
calc def MultiplyCalc {
    in attribute unit_cost : Real;
    in attribute quantity : Real;
    out attribute total : Real = unit_cost * quantity;
}

part def 'Test Calc Multiply' {
    attribute unit_cost : Real;
    attribute quantity : Real = 2.0;

    calc cost_rollup : MultiplyCalc {
        in unit_cost = unit_cost;
        in quantity = quantity;
    }

    attribute total_cost : Real = cost_rollup.total;
}
```

**Result**: ✅ WORKS

**Conclusion**: Works but requires:
1. Knowing the count at design time
2. Assuming all instances have the same unit cost

---

## What Prior Research Reports Said

### Report 1: `heirarchical-cost-modeling-mbse-patterns.md`

**Claim** (line 184):
```sysml
constraint costRollup {
    totalCost == directCost + sum(subParts.totalCost)
}
```

**Reality**: `sum()` does NOT exist. This was **never tested**.

---

### Report 2: `20260106-050051_cost-modeling-lcoe-strategy.md`

**Claim** (line 113):
> "SysMLv2 does NOT support collection operations like `parts.cost->sum()`"

**Reality**: Correct, but no working alternative was validated.

---

### Report 3: `20260106-065431_cost-architecture-patterns.md`

**Claim** (lines 127-138):
```sysml
calc rollup : TFCoilArrayCost {
    in unit_cost = tf_coils.capital_cost;  // ← ASSUMES THIS WORKS
    in quantity = 12;
}
```

**Reality**: `tf_coils.capital_cost` on a `[12]` array returns what exactly? Never tested.

---

### Report 4: `20260107-final-cost-architecture.md`

**Pattern shown** (lines 88-105):
```sysml
part def Bike {
    part front_wheel : Wheel { ... }
    part rear_wheel : Wheel { ... }

    :>> capital_cost = front_wheel.capital_cost + rear_wheel.capital_cost;
}
```

**Reality**: This **avoids** multiplicity entirely. Uses named parts instead of `wheel[2]`.

---

### Report 5: `20260110-strategic-cost-patterns.md`

**What it did** (lines 406-414):
```sysml
// For now, we express 2x heater cost explicitly in the design file
// This is a known pattern - multiplicity handling varies by tooling
attribute heater_total_cost : Real;  // ← The pattern that ended up in coffee maker
```

**Reality**: Gave up. This is the pattern that led to the hardcoded `26.25`.

---

## Summary of Contradictions

| Report | Date | Claim | Tested? | Correct? |
|--------|------|-------|---------|----------|
| #1 Hierarchical | N/A | `sum()` works | NO | ❌ |
| #2 Strategy | Jan 6 | `sum()` doesn't exist | NO | ✅ |
| #3 Architecture | Jan 6 | Pass array to calc | NO | ❓ |
| #4 Final | Jan 7 | (Avoided the issue) | N/A | N/A |
| #5 Strategic | Jan 10 | Manual values | YES | ✅ (but broken) |

---

## The Fundamental Requirements

Per user requirements:
1. **Always allow for multiplicity** - Don't require knowing "there may be multiple"
2. **Fully recursive** - Any depth of decomposition should roll up automatically

Current state **violates both requirements**.

---

## Analysis of Possible Solutions

### Solution A: Explicit Indexing (Limited)

```sysml
part def Assembly {
    part child : Component [2];

    :>> capital_cost = child#(1).capital_cost + child#(2).capital_cost;
}
```

| Pros | Cons |
|------|------|
| Works today | Must know exact count |
| Explicit | Doesn't scale (imagine `[48]`) |
| | Changes if multiplicity changes |

**Verdict**: Only viable for small, fixed multiplicities.

---

### Solution B: Named Parts (Workaround)

```sysml
part def Assembly {
    part child_1 : Component;
    part child_2 : Component;

    :>> capital_cost = child_1.capital_cost + child_2.capital_cost;
}
```

| Pros | Cons |
|------|------|
| Works today | Loses multiplicity benefits |
| Clear semantics | Verbose |
| | Can't parameterize count |

**Verdict**: Acceptable for assemblies where count never changes.

---

### Solution C: Unit Cost × Quantity Pattern

```sysml
part def Assembly {
    part child : Component [N];  // N defined elsewhere

    // Assume all children have same unit cost
    calc rollup : MultiplyCalc {
        in unit_cost = ... // HOW TO GET ONE child's cost?
        in quantity = N;
    }
}
```

| Pros | Cons |
|------|------|
| Scales to any N | Assumes uniform cost |
| | Can't handle heterogeneous children |
| | Still need to access one child's cost |

**Verdict**: Only works if all instances are identical.

---

### Solution D: Tooling Enhancement (sysml-codegen)

Enhance sysml-codegen to:
1. Detect parts with multiplicity > 1
2. Generate Python code that iterates and sums
3. Produce pipeline that correctly aggregates

| Pros | Cons |
|------|------|
| Solves root problem | Requires tooling work |
| Works for any N | Doesn't work in pure SysML |
| Handles heterogeneous | Development effort |

**Verdict**: The only solution that meets the requirements. Requires investment.

---

### Solution E: Define Custom `sum` Calc Def

```sysml
calc def SumRealArray {
    doc /* Custom sum function for Real arrays */
    in values : Real [0..*];
    out total : Real;  // = ??? Can't implement iteration in SysML
}
```

| Pros | Cons |
|------|------|
| Clean interface | SysML can't express iteration |
| | Would need tool-specific implementation |

**Verdict**: Not possible in pure SysML v2.

---

## Required Actions

### Immediate: Fix the Coffee Maker Demo

1. **Add import**: `private import NumericalFunctions::sum;`
2. **Remove** placeholder attributes (`heater_total_cost`, etc.)
3. **Replace** aggregation with `sum(heater.capital_cost)`
4. **Remove** hardcoded values from design.sysml

### Update MODELING_GUIDE.md

Add required import pattern for all cost-bearing models:

```sysml
// REQUIRED for any model with part multiplicities
private import NumericalFunctions::sum;
private import NumericalFunctions::product;  // if needed
```

### Update All Prior Research Reports

Mark the following as **OBSOLETE/INCORRECT**:
- Claims that `sum()` doesn't exist
- Workaround patterns using hardcoded values
- Recommendations to use named parts instead of multiplicity

### No Tooling Enhancement Needed

The prior recommendation to enhance sysml-codegen is **unnecessary** - the standard library already provides the solution. The only requirement is proper imports.

---

## Test Files Created

| File | Purpose | Status |
|------|---------|--------|
| `models/tests/multiplicity_sum_test.sysml` | Test `sum()` function | ❌ FAILS |
| `models/tests/multiplicity_alternatives_test.sysml` | Test alternatives | ✅ Parses |

---

## Action Items

1. **[CRITICAL]** Fix coffee maker demo to use a valid pattern (not hardcoded)
2. **[HIGH]** Update MODELING_GUIDE with multiplicity limitations
3. **[HIGH]** Create issue for sysml-codegen multiplicity enhancement
4. **[MEDIUM]** Review all models for `[N]` parts with N > 1
5. **[LOW]** Propose CollectionFunctions enhancement to SysML community

---

## Conclusion

**The solution exists and has always existed.** `NumericalFunctions::sum` is part of the official SysML v2 standard library.

The failure was a research failure - the agent team:
1. Tried bare `sum()` without importing
2. Got an error and concluded the function doesn't exist
3. Never searched the standard library files
4. Never consulted official documentation or web resources
5. Implemented a broken workaround (hardcoded values)

**Lesson learned**: Before concluding something is impossible, **search the standard library** and **check official documentation**.

### Validated Test Files

- `models/tests/multiplicity_cost_rollup_validated.sysml` - Complete working pattern
- `models/tests/multiplicity_sum_import_test.sysml` - Basic import test

### Sources

- [SysML v2 Release Repository](https://github.com/Systems-Modeling/SysML-v2-Release)
- `/syside/sysml.library/Kernel Libraries/Kernel Function Library/NumericalFunctions.kerml`
- [OMG SysML v2 Specification](https://www.omg.org/sysml/sysmlv2/)

---

**Related Files**:
- `models/tests/coffee_maker/library.sysml` - The problematic pattern
- `models/tests/coffee_maker/design.sysml` - Hardcoded values
- `models/tests/multiplicity_sum_test.sysml` - Failed sum() test
- `models/tests/multiplicity_alternatives_test.sysml` - Working alternatives

**Related Research**:
- `project/research/heirarchical-cost-modeling-mbse-patterns.md`
- `project/research/20260106-050051_cost-modeling-lcoe-strategy.md`
- `project/research/20260106-065431_cost-architecture-patterns.md`
- `project/research/20260107-final-cost-architecture.md`
- `project/research/20260110-strategic-cost-patterns.md`
